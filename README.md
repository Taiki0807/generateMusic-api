# FastAPI ML Template

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## 導入ライブラリー

- black: コードフォーマッター
- isort: import 整理ツール
- flake8: 品質チェック
- mypy: 型チェック
- pre-commit:コミット前に行うチェックを管理するツール
- pipenv: 仮想環境,パッケージ管理

## Run Web API

### Local

```sh
$ sh run.sh
```

### Docker

```sh
$ docker build -f Dockerfile -t fastapi-ml .
$ docker run -p 9000:9000 --rm --name fastapi-ml -t -i fastapi-ml
```

### Docker Compose

```sh
$ docker compose up --build
```

## ディレクトリ構成

```
app
├── api
│   ├── api.py           # 機械学習の推論のエンドポイント
│   └── heartbeat.py     # WebAPIの外部監視用のエンドポイント
├── core
│   ├── config.py        # WebAPI全体の設定
│   └── event_handler.py # WebAPI起動/終了時に実行する処理
├── main.py              # WebAPI本体
├── models
│   └── predict.py       # WebAPIの入力/出力のモデル
└── services
    └── model.py         # 機械学習の推論の実装
```

## 参考

- [機械学習の推論 WebAPI の実装をテンプレート化して使い回せるようした](https://zenn.dev/yag_ays/articles/eef1a8c8e1ee39)
