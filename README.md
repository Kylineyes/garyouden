# garyouden

`garyouden` は、PC-9801/DOS 向け戦略ゲーム『臥竜伝 三国制覇の計』
（卧龙传）のセーブデータおよびシナリオデータを解析・編集するための
Python プロジェクトです。

対象となる主なファイルは `SINARIO.DAT` と `SAVE.DAT` です。
バイナリ形式のデータ構造、各種オフセット、Big5 文字列などを確認しながら、
ゲーム内のシナリオ情報やセーブ情報を安全に読み書きできるツールを目指します。

## 構成

| パス | 役割 |
| --- | --- |
| `main.py` | 互換用の薄い入口です。 |
| `garyouden/cli.py` | コマンドライン引数を扱います。 |
| `garyouden/layout.py` | DAT のオフセット、サイズ、`construct` 定義を持ちます。 |
| `garyouden/models.py` | 解析後の dataclass を持ちます。 |
| `garyouden/parser.py` | DAT の読み込みと解析を行います。 |
| `garyouden/summaries.py` | テキスト/JSON の概要出力を行います。 |
| `garyouden/workbook.py` | XLSX 出力を行います。 |

## 環境

開発にはプロジェクト内の Python 3.14 仮想環境を使用します。
Python 関連のコマンドを実行する前に、必ず次を実行してください。

```bash
source .venv/bin/activate
python -m pip install -r requirements.txt
```

## 使い方

DAT ファイルのパスは必須です。デフォルト入力はありません。

```bash
python main.py SINARIO.DAT
python main.py save/SINARIO_caocao0.DAT --scenario 0 --json
python main.py path/to/SAVE.DAT --xlsx path/to/output.xlsx
```

## XLSX 出力

XLSX 出力では、資料の大項目に合わせて次の sheet を作成します。

- `剧本信息`
- `势力`
- `外交`
- `城池信息`
- `军团信息`
- `武将信息`
- `未知区块`

未使用スロットなどに含まれる Excel 非対応の制御文字は、`\x00` のような
見える表記へ変換して出力します。
