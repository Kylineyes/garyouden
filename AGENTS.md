# Repository Guidelines

## Project Purpose

This Python 3.14 project reads and modifies DAT save files for
`卧龙传` (`臥竜伝 三国制覇の計`, Garyouden Sangoku Seiha no Kei). The game is a
Three Kingdoms strategy title for PC-9801/DOS. Treat this repository as a
binary save-file parser/editor, not a game clone, ROM set, or walkthrough site.

## Project Structure & Module Organization

- `main.ipynb` is for reverse-engineering experiments with `construct`.
- `SINARIO.DAT` is the bundled save sample.
- `save/` holds local save samples and is ignored by Git.
- `.venv/` is the project-local Python 3.14 environment.
- `requirements.txt` lists runtime packages for `pip install`, currently
  including `construct` for binary parsing and `openpyxl` for workbook export.
- `main.py` is only a thin compatibility entry point.
- `garyouden/cli.py` owns command-line parsing.
- `garyouden/layout.py` owns binary offsets, record sizes, capacities, and
  `construct` layouts.
- `garyouden/models.py` owns parsed dataclasses.
- `garyouden/parser.py` owns DAT file reading and parsing. Prefer
  `read_dat_file()` for new code.
- `garyouden/summaries.py` owns JSON/text summaries.
- `garyouden/workbook.py` owns XLSX export.

Keep stable parsing/editing code in modules. Promote notebook work only after
offsets, byte order, encodings, and field sizes are confirmed.

## Format Notes & References

Primary format source:

- Jiangsheng DAT notes: https://jiangsheng.net/build/html/games/dragon/index.html
- Project terminology: `TERMINOLOGY.md`

Jiangsheng documents `SINARIO.DAT` as 88,832 bytes, split into four 22,208-byte
save slots. `SAVE.DAT` uses the same structure with user save data. Text fields
are Big5, and short strings are padded with `A140`.

Project background and metadata sources:

- Wikipedia overview: https://zh.wikipedia.org/wiki/卧龙传
- PC98 GAME profile: https://pc-9801.com/臥竜伝-三国制覇の計/
- PC98 Refuge catalog: https://refuge.tokyo/pc9801/pc98/00834.html

Use the Japanese/English sources above to cross-check title variants, platform,
publisher, release year, media count, and preservation status. Do not add the
previous Chinese gameplay/blog sources unless explicitly requested. When
sources conflict, prefer direct DAT evidence for parser behavior.

## Terminology And Naming

Always consult `TERMINOLOGY.md` before writing documentation or choosing names
for classes, variables, functions, JSON keys, and workbook export fields.

Use only the canonical terms above for project identifiers. Do not spell out
legacy English alternatives in project documentation.

## Build, Test, and Development Commands

Before running any project Python command, activate the project environment:

- `source .venv/bin/activate`

After activation:

- `python -m pip install -r requirements.txt` installs runtime dependencies.
- `python main.py SINARIO.DAT` parses the bundled save sample.
- `python main.py path/to/SAVE.DAT` parses a specific save file.
- `python main.py path/to/SAVE.DAT --xlsx path/to/output.xlsx` exports a workbook.
- `pycodestyle main.py garyouden` runs style checks when the dev dependencies are installed.

The CLI requires the DAT path; do not reintroduce a default input path.

If `.venv` is invalid, rebuild or repair the project-local virtual environment 
first, then activate it again.

## Coding Style & Naming Conventions

Use 4-space indentation, type hints, `pathlib.Path`, dataclasses for parsed
records, and constants such as `SAVE_SIZE` or `POWER_TABLE_OFFSET`. Prefer
`struct` or `construct` over ad hoc slicing. Validate lengths before unpacking.
When exporting strings to Excel, escape control bytes instead of writing them
directly because `openpyxl` rejects values containing bytes such as
`U+0000` from unused DAT slots.

## Testing Guidelines

No test framework is configured yet. When adding editing behavior, create
`tests/` with `pytest` and synthetic byte fixtures. Test short-file rejection,
round-trip parse/build behavior, Big5 text handling, and modified offsets.

## Safety Rules

Treat DAT files as untrusted binary input. Keep original saves backed up, never
commit personal `save/` files, and write edits to an explicit output path unless
in-place modification is requested.
