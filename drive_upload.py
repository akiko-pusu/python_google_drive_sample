# Python3を前提にしています
from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from apiclient import discovery
from apiclient.http import MediaFileUpload
import os, json
from pathlib import Path

# コマンドライン引数を処理する際に必要
import sys

# 例外でなくwarningを抑止する際に利用
import warnings

# コンテンツのMediaType判定
import mimetypes

# 学習のため、簡単なクラスを作ります
class GoogleDriveUpload():
    def __init__(self, folder_id):
        self.set_service()
        self.upload_folder_id = folder_id

    def set_service(self):
        # If modifying these scopes, delete the file token.json.
        SCOPES = 'https://www.googleapis.com/auth/drive.file'
        flags = tools.argparser.parse_args('--auth_host_name localhost --logging_level INFO'.split())
        warnings.filterwarnings('ignore')
        store = file.Storage('token.json')
        creds = store.get()

        if not creds or creds.invalid:
            flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
            creds = tools.run_flow(flow, store, flags)
        self.service = build('drive', 'v3', http=creds.authorize(Http()))

    # 一個づつアップロードする関数 / 基本はここがメイン
    def upload(self, filename, title, mediaType='application/pdf'):
        # ファイルのメタデータを設定
        file_metadata = {
            'name': title,
            'mimeType': mediaType,
            'parents': [self.upload_folder_id]
        }
        media = MediaFileUpload(str(filename),
                            mimetype='application/vnd.google-apps-document',
                               resumable=True)
        self.service.files().create(body=file_metadata,
                                    media_body=media,
                                    fields='id').execute()

    # 渡されたファイルのリストと、各ファイルのメタデータをマッピングさせたjsonデータを
    # 使って、forで一個ずつアップロードします
    def bulk_upload(self, target_files, file_map):
        for target in target_files:
            filename = os.path.splitext(os.path.basename(target))
            original_id = filename[0]
            try:
                document_title = filename
                try:
                    if file_map is not None:
                        json_data = open(file_map).read()
                        data = json.loads(json_data)
                        updated_at = data[original_id]['updated_at']
                        title = data[original_id]['title']
                        author = data[original_id]['author']

                        # [yyyymmdd] 本来のタイトル (作者) [本来のドキュメントのID] というドキュメントタイトルにする
                        document_title = "[{updated}] {title} ({author}) [id: {original_id}]".format(
                            title=title, updated=updated_at[0:10], author=author, original_id=original_id
                            )
                except FileNotFoundError:
                    print('mapping file does not exist. Original filename is applied.')
                
                # ここでは一個づづアップロードしています
                print("{0} : {1}".format(original_id, document_title))

                mediaType = mimetypes.guess_type(os.path.realpath(target))
                self.upload(target, document_title, mediaType[0])
            except KeyError:
                print("Error - {0} {1}".format(original_id, target))
        return 'Finished upload.'


# アップロード対象のファイル一覧を取得します
# PDFを対象にします
def target_files(from_dir='results', ext=None):
    p = Path(from_dir)

    if ext is None:
        return sorted(list(p.glob('./*')))
    # 今回の例は16進のファイル名になっているのでソートして返す
    return sorted(list(p.glob("[0-9a-f]*.{0}".format(ext))))

def upload_files(upload_folder_id, from_dir, start_index=0):
    file_map = 'mapping_file.json'

    g = GoogleDriveUpload(upload_folder_id)
    files = target_files(from_dir)

    g.bulk_upload(files[start_index:], file_map)


if __name__ == '__main__':
    if (len(sys.argv) < 3):
        print('google_target_folder_id, from_dir are required.')
        exit()

    # たくさんありすぎたりサイズが大きくて途中でタイムアウトしちゃった場合に番号を指定して再開
    start_index = 0

    # Googleドライブ上のアップロード先のフォルダIDを引数に取ります
    google_target_folder_id = sys.argv[1]
    from_dir = sys.argv[2]
    if (len(sys.argv) == 4):
        start_index = int(sys.argv[3])
    upload_files(google_target_folder_id, from_dir, start_index)
