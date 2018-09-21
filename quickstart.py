# Python3で実行していますが、GoogleのサンプルではPython2でも利用可能です
from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
# コマンドライン引数を処理する際に必要
import sys

# 例外でなくwarningを抑止する際に利用
import warnings

# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/drive.metadata.readonly'

def main(keyword):
    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
    """
    try:
        # token.jsonが無いとoauth2clientからwarningが出るので、warningを非表示に
        warnings.filterwarnings('ignore')
        store = file.Storage('token.json')
        creds = store.get()
    
        if not creds or creds.invalid:
            flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
            creds = tools.run_flow(flow, store)     

        service = build('drive', 'v3', http=creds.authorize(Http()))

        # Call the Drive v3 API
        results = service.files().list(
            pageSize=10, fields="nextPageToken, files(id, name, mimeType)", 
                q="name contains '{0}'".format(keyword)).execute()
        items = results.get('files', [])
    except FileNotFoundError as e:
        print('You should turn on the Drive API and store credential.json.')
        exit()
    except Exception as e:
        print("例外が発生しました: {0}".format(e.__class__.__name__))
        sys.exit(1)        

    if not items:
        print('No files found.')
    else:
        print('Files:')
        for item in items:
            print('{0} ({1})'.format(item['name'], item['mimeType']))

if __name__ == '__main__':
    keyword = 'SRE'
    if (len(sys.argv) == 2):
        keyword = sys.argv[1]
    main(keyword)

'''
実行例です。
- 引数がない場合はSREをキーワードに
- 引数があれば引数をキーワードに

(python3_env) $ python quickstart.py
Files:
SRE本ページ構成 (application/vnd.google-apps.spreadsheet)
20180806 & 20180820 SRE本輪読会#18&19  第17章 信頼性のためのテスト (application/vnd.google-apps.presentation)
20180806-0820 SRE本輪読会#18  第17章 信頼性のためのテスト (application/vnd.google-apps.presentation)
第16回 SRE本輪読会 (application/vnd.google-apps.presentation)
20180716 SRE本輪読会#15 インシデント管理 (application/vnd.google-apps.presentation)
第13回SRE本輪読会 第12章 - 効果的なトラブルシューティング (application/vnd.google-apps.presentation)

(python3_env) $ python quickstart.py トラブル
Files:
第13回SRE本輪読会 第12章 - 効果的なトラブルシューティング (application/vnd.google-apps.presentation)

'''