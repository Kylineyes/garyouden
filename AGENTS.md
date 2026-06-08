# Repository Guidelines

## Project Purpose

This Python 3.14 project reads and modifies DAT save/scenario files for
`卧龙传` (`臥竜伝 三国制覇の計`, Garyouden Sangoku Seiha no Kei). The game is a
Three Kingdoms strategy title for PC-9801/DOS. Treat this repository as a
binary save-file parser/editor, not a game clone, ROM set, or walkthrough site.

## Project Structure & Module Organization

- `main.ipynb` is for reverse-engineering experiments with `construct`.
- `SINARIO.DAT` is the default scenario input.
- `save/` holds local save samples and is ignored by Git.
- `pyproject.toml` and `uv.lock` define Python 3.14 and dependencies.

Keep stable parsing/editing code in modules. Promote notebook work only after
offsets, byte order, encodings, and field sizes are confirmed.

## Format Notes & References

Primary format source:

- Jiangsheng DAT notes: https://jiangsheng.net/build/html/games/dragon/index.html

Jiangsheng documents `SINARIO.DAT` as 88,832 bytes, split into four 22,208-byte
scenarios. `SAVE.DAT` uses the same structure with save data replacing scenario
data. Text fields are Big5, and short strings are padded with `A140`.

Project background and metadata sources:

- Wikipedia overview: https://zh.wikipedia.org/wiki/卧龙传
- PC98 GAME profile: https://pc-9801.com/臥竜伝-三国制覇の計/
- PC98 Refuge catalog: https://refuge.tokyo/pc9801/pc98/00834.html
- MAME PC-98 software list: https://mame.spludlow.co.uk/SoftwareLists.aspx?Exact=true&List=pc98&Page=5

Use the Japanese/English sources above to cross-check title variants, platform,
publisher, release year, media count, and preservation status. Do not add the
previous Chinese gameplay/blog sources unless explicitly requested. When
sources conflict, prefer direct DAT evidence for parser behavior.

## Build, Test, and Development Commands

- `uv sync --python 3.14` updates the project environment.
- `uv run --python 3.14 python main.py` parses `SINARIO.DAT` when a CLI exists.
- `uv run --python 3.14 python main.py path/to/SAVE.DAT` parses a specific save file.
- `python3.14 -m compileall .` performs a basic syntax check.

If `.venv` is invalid, rebuild it before using `uv run`.

## Coding Style & Naming Conventions

Use 4-space indentation, type hints, `pathlib.Path`, dataclasses for parsed
records, and constants such as `SCENARIO_SIZE` or `FORCE_TABLE_OFFSET`. Prefer
`struct` or `construct` over ad hoc slicing. Validate lengths before unpacking.

## Testing Guidelines

No test framework is configured yet. When adding editing behavior, create
`tests/` with `pytest` and synthetic byte fixtures. Test short-file rejection,
round-trip parse/build behavior, Big5 text handling, and modified offsets.

## Safety Rules

Treat DAT files as untrusted binary input. Keep original saves backed up, never
commit personal `save/` files, and write edits to an explicit output path unless
in-place modification is requested.
