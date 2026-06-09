from __future__ import annotations

import argparse
import json
from collections.abc import Sequence
from pathlib import Path

from garyouden.parser import read_dat_file
from garyouden.summaries import dat_file_to_dict, format_save_overview
from garyouden.workbook import write_dat_workbook


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Parse Garyouden SINARIO.DAT/SAVE.DAT files.")
    parser.add_argument(
        "path",
        type=Path,
        help="DAT file path.",
    )
    parser.add_argument(
        "--save",
        type=int,
        choices=range(4),
        metavar="0-3",
        help="Only display one save slot.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Print a machine-readable summary.",
    )
    parser.add_argument(
        "--xlsx",
        type=Path,
        metavar="PATH",
        help="Write the DAT structure to an XLSX workbook.",
    )
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    dat_file = read_dat_file(args.path)
    saves = dat_file.saves
    if args.save is not None:
        saves = (dat_file.saves[args.save],)

    if args.xlsx:
        workbook_path = write_dat_workbook(dat_file, args.xlsx, saves)
        if not args.json:
            print(f"wrote {workbook_path}")
            return 0

    if args.json:
        payload = dat_file_to_dict(dat_file, saves)
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0

    print(f"{dat_file.path} ({dat_file.path.stat().st_size} bytes)")
    print()
    print("\n\n".join(format_save_overview(save) for save in saves))
    return 0
