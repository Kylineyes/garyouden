"""Garyouden DAT parser."""

from garyouden.models import DatFile
from garyouden.parser import read_dat_file
from garyouden.workbook import write_dat_workbook

parse_dat_file = read_dat_file

__all__ = ["DatFile", "parse_dat_file", "read_dat_file", "write_dat_workbook"]
