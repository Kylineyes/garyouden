# garyouden

`garyouden` は、PC-9801/DOS 向け戦略ゲーム『臥竜伝 三国制覇の計』（卧龙传）のセーブデータおよびシナリオデータを解析・編集するための Python プロジェクトです。

対象となる主なファイルは `SINARIO.DAT` と `SAVE.DAT` です。バイナリ形式のデータ構造、各種オフセット、Big5 文字列などを確認しながら、ゲーム内のシナリオ情報やセーブ情報を安全に読み書きできるツールを目指します。

開発にはプロジェクト内の Python 3.14 仮想環境を使用します。Python 関連の
コマンドを実行する前に、必ず次を実行してください。

```bash
source .venv/bin/activate
```

実行例:

```bash
python main.py
python main.py path/to/SAVE.DAT
```
