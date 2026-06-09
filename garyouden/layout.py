from __future__ import annotations

from construct import Array, Byte, Bytes, Int16ul, Int24ul, Struct


DAT_FILE_SIZE = 88_832
SAVE_COUNT = 4
SAVE_SIZE = 22_208
BIG5_PAD = "\u3000"

HEADER_OFFSET = 0x00
HEADER_SIZE = 0x60
DAY_OFFSET = 0x03
MONTH_OFFSET = 0x04
YEAR_OFFSET = 0x06
PLAYER_POWER_OFFSET = 0x0F
TRUST_OFFSET = 0x10
SAVE_ID_OFFSET = 0x11
THIS_MONTH_TAX_OFFSET = 0x18
THIS_MONTH_RECRUITS_OFFSET = 0x1A
NEXT_MONTH_TAX_OFFSET = 0x20
NEXT_MONTH_RECRUITS_OFFSET = 0x22
POWER_COUNT_OFFSET = 0x3A
SAVE_NAME_OFFSET = 0x40
SAVE_NAME_SIZE = 0x20

POWER_TABLE_OFFSET = 0x80
POWER_RECORD_SIZE = 0x40
POWER_CAPACITY = 24

DIPLOMACY_TABLE_OFFSET = 0x680
DIPLOMACY_RECORD_SIZE = 24
DIPLOMACY_CAPACITY = 24

CITY_TABLE_OFFSET = 0x8C0
CITY_RECORD_SIZE = 0x20
CITY_CAPACITY = 200

PRE_ARMY_BLOCK_OFFSET = 0x21C0
PRE_ARMY_BLOCK_SIZE = 0x100

ARMY_TABLE_OFFSET = 0x22C0
ARMY_RECORD_SIZE = 0x40
ARMY_CAPACITY = 128
ARMY_UNIT_BLOCK_OFFSET = 0x28
ARMY_UNIT_RECORD_SIZE = 0x04
ARMY_UNIT_ROLES = (
    "commander",
    "vanguard",
    "left_wing",
    "right_wing",
    "left_reserve",
    "right_reserve",
)

MONARCH_TABLE_OFFSET = 0x42C0
MONARCH_RECORD_SIZE = 0x20
MONARCH_CAPACITY = 128

TAIL_BLOCK_OFFSET = 0x52C0
TAIL_BLOCK_SIZE = 0x400

FREE_POWER_ID = 0xFF
EMPTY_CITY_POWER_ID = 0x18
NO_MONARCH_ID = 0xFF
NO_STRATEGIST_ID = 0x7F

SAVE_HEADER_STRUCT = Struct(
    "unknown_00_02" / Bytes(3),
    "day" / Byte,
    "month" / Byte,
    "unknown_05" / Byte,
    "year" / Byte,
    "unknown_07_0e" / Bytes(8),
    "player_power_id" / Byte,
    "trust" / Byte,
    "save_id" / Byte,
    "unknown_12_17" / Bytes(6),
    "this_month_tax" / Byte,
    "unknown_19" / Byte,
    "this_month_recruits" / Array(3, Int16ul),
    "next_month_tax" / Byte,
    "unknown_21" / Byte,
    "next_month_recruits" / Array(3, Int16ul),
    "unknown_28_39" / Bytes(POWER_COUNT_OFFSET - 0x28),
    "power_count" / Byte,
    "unknown_3b_3f" / Bytes(5),
    "name_raw" / Bytes(SAVE_NAME_SIZE),
)

POWER_STRUCT = Struct(
    "status" / Byte,
    "ruler_monarch_id" / Byte,
    "strategist_monarch_id" / Byte,
    "capital_city_id" / Byte,
    "starting_troops" / Array(3, Int16ul),
    "unknown_0a_17" / Bytes(0x18 - 0x0A),
    "monarch_count" / Byte,
    "unknown_19_1f" / Bytes(0x20 - 0x19),
    "money" / Int24ul,
    "city_count" / Byte,
    "unknown_24_39" / Bytes(0x3A - 0x24),
    "diplomat_monarch_id" / Byte,
    "unknown_3b_3f" / Bytes(POWER_RECORD_SIZE - 0x3B),
)


def validate_layout() -> None:
    expected_sizes = {
        "header": HEADER_SIZE,
        "power": POWER_RECORD_SIZE,
    }
    actual_sizes = {
        "header": SAVE_HEADER_STRUCT.sizeof(),
        "power": POWER_STRUCT.sizeof(),
    }
    for name, expected in expected_sizes.items():
        actual = actual_sizes[name]
        if actual != expected:
            raise AssertionError(f"{name} struct must be {expected} bytes, got {actual}")

    table_ranges = (
        (POWER_TABLE_OFFSET, DIPLOMACY_TABLE_OFFSET),
        (DIPLOMACY_TABLE_OFFSET, CITY_TABLE_OFFSET),
        (CITY_TABLE_OFFSET, PRE_ARMY_BLOCK_OFFSET),
        (PRE_ARMY_BLOCK_OFFSET, ARMY_TABLE_OFFSET),
        (ARMY_TABLE_OFFSET, MONARCH_TABLE_OFFSET),
        (MONARCH_TABLE_OFFSET, TAIL_BLOCK_OFFSET),
        (TAIL_BLOCK_OFFSET, SAVE_SIZE),
    )
    for start, end in table_ranges:
        if start >= end:
            raise AssertionError(f"invalid table range 0x{start:x}-0x{end:x}")

    expected_ends = {
        "power": POWER_TABLE_OFFSET + POWER_RECORD_SIZE * POWER_CAPACITY,
        "diplomacy": DIPLOMACY_TABLE_OFFSET + DIPLOMACY_RECORD_SIZE * DIPLOMACY_CAPACITY,
        "city": CITY_TABLE_OFFSET + CITY_RECORD_SIZE * CITY_CAPACITY,
        "pre_army": PRE_ARMY_BLOCK_OFFSET + PRE_ARMY_BLOCK_SIZE,
        "army": ARMY_TABLE_OFFSET + ARMY_RECORD_SIZE * ARMY_CAPACITY,
        "monarch": MONARCH_TABLE_OFFSET + MONARCH_RECORD_SIZE * MONARCH_CAPACITY,
        "tail": TAIL_BLOCK_OFFSET + TAIL_BLOCK_SIZE,
    }
    actual_ends = {
        "power": DIPLOMACY_TABLE_OFFSET,
        "diplomacy": CITY_TABLE_OFFSET,
        "city": PRE_ARMY_BLOCK_OFFSET,
        "pre_army": ARMY_TABLE_OFFSET,
        "army": MONARCH_TABLE_OFFSET,
        "monarch": TAIL_BLOCK_OFFSET,
        "tail": SAVE_SIZE,
    }
    for name, expected_end in expected_ends.items():
        actual_end = actual_ends[name]
        if expected_end != actual_end:
            raise AssertionError(f"{name} must end at 0x{actual_end:x}, got 0x{expected_end:x}")


validate_layout()
