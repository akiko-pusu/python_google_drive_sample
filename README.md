## このスクリプトについて

- Google DriveのAPIを使ってみるサンプルです
    - 出来についてはご容赦を....
    - 静的解析の実験用にも利用します
- 実行の前提は Python3 (MacOS上でvenv利用) です
 
### venvでのPython3への切り替え

```
$ python -m venv python3_env
$ source
.git/            README.md        drive_upload.py  python3_env/     quickstart.py

$ source python3_env/bin/activate
(python3_env) $ python --version
Python 3.7.0
```

#### Google Client用のパッケージ追加

venvでの管理なので、作成したpython3_env 以下の site-packages/ というディレクトリ以下に、パッケージ（関連パッケージも）が配置されます。

```
(python3_env) $ pip install --upgrade google-api-python-client oauth2client

(python3_env) $ tree -L 2 python3_env/
python3_env/
├── bin
│   ├── activate
│   ├── activate.csh
│   ├── activate.fish
│   ├── easy_install
│   ├── easy_install-3.7
│   ├── pip
│   ├── pip3
│   ├── pip3.7
│   ├── pyrsa-decrypt
│   ├── pyrsa-encrypt
│   ├── pyrsa-keygen
│   ├── pyrsa-priv2pub
│   ├── pyrsa-sign
│   ├── pyrsa-verify
│   ├── python -> /usr/local/bin/python
│   └── python3 -> python
├── include
├── lib
│   └── python3.7
├── pip-selfcheck.json
└── pyvenv.cfg

4 directories, 18 files
```