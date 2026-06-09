from __future__ import annotations

from pathlib import Path

from garyouden.layout import (
    ARMY_CAPACITY,
    ARMY_RECORD_SIZE,
    ARMY_TABLE_OFFSET,
    ARMY_UNIT_BLOCK_OFFSET,
    ARMY_UNIT_RECORD_SIZE,
    ARMY_UNIT_ROLES,
    BIG5_PAD,
    CITY_CAPACITY,
    CITY_RECORD_SIZE,
    CITY_TABLE_OFFSET,
    DAT_FILE_SIZE,
    DIPLOMACY_CAPACITY,
    DIPLOMACY_RECORD_SIZE,
    DIPLOMACY_TABLE_OFFSET,
    HEADER_OFFSET,
    HEADER_SIZE,
    MONARCH_CAPACITY,
    MONARCH_RECORD_SIZE,
    MONARCH_TABLE_OFFSET,
    POWER_CAPACITY,
    POWER_RECORD_SIZE,
    POWER_STRUCT,
    POWER_TABLE_OFFSET,
    PRE_ARMY_BLOCK_OFFSET,
    PRE_ARMY_BLOCK_SIZE,
    SAVE_COUNT,
    SAVE_HEADER_STRUCT,
    SAVE_SIZE,
    TAIL_BLOCK_OFFSET,
    TAIL_BLOCK_SIZE,
)
from garyouden.models import (
    ArmyRecord,
    ArmyUnitRecord,
    CityType,
    CityRecord,
    DatFile,
    MonarchListStatus,
    MonarchRecord,
    PowerRecord,
    Save,
    SaveHeader,
    UnknownBlock,
)


def read_dat_file(path: str | Path) -> DatFile:
    dat_path = Path(path)
    data = dat_path.read_bytes()
    if len(data) != DAT_FILE_SIZE:
        raise ValueError(f"{dat_path} must be {DAT_FILE_SIZE} bytes, got {len(data)}")

    saves = tuple(
        read_save(index, data[index * SAVE_SIZE: (index + 1) * SAVE_SIZE])
        for index in range(SAVE_COUNT)
    )
    return DatFile(path=dat_path, saves=saves)


def read_save(index: int, data: bytes) -> Save:
    if len(data) != SAVE_SIZE:
        raise ValueError(f"save {index} must be {SAVE_SIZE} bytes, got {len(data)}")

    return Save(
        index=index,
        header=read_header(data),
        powers=read_power_table(data),
        diplomacy=read_diplomacy_table(data),
        cities=read_city_table(data),
        armies=read_army_table(data),
        monarchs=read_monarch_table(data),
        pre_army_block=read_unknown_block(data, PRE_ARMY_BLOCK_OFFSET, PRE_ARMY_BLOCK_SIZE),
        tail_block=read_unknown_block(data, TAIL_BLOCK_OFFSET, TAIL_BLOCK_SIZE),
    )


def read_header(data: bytes) -> SaveHeader:
    parsed = SAVE_HEADER_STRUCT.parse(data[HEADER_OFFSET: HEADER_OFFSET + HEADER_SIZE])
    return SaveHeader(
        day=parsed.day,
        month=parsed.month,
        year=parsed.year,
        player_power_id=parsed.player_power_id,
        trust=parsed.trust,
        save_id=parsed.save_id,
        this_month_tax=parsed.this_month_tax,
        this_month_recruits=tuple(parsed.this_month_recruits),
        next_month_tax=parsed.next_month_tax,
        next_month_recruits=tuple(parsed.next_month_recruits),
        power_count=parsed.power_count,
        name=decode_big5_padded(parsed.name_raw),
        raw_prefix=parsed.unknown_00_02,
        unknown_19=parsed.unknown_19,
        unknown_21=parsed.unknown_21,
    )


def read_power_table(data: bytes) -> tuple[PowerRecord, ...]:
    return tuple(
        read_power_record(index, read_record(data, POWER_TABLE_OFFSET, POWER_RECORD_SIZE, index))
        for index in range(POWER_CAPACITY)
    )


def read_power_record(index: int, data: bytes) -> PowerRecord:
    parsed = POWER_STRUCT.parse(data)
    return PowerRecord(
        index=index,
        status=parsed.status,
        ruler_monarch_id=parsed.ruler_monarch_id,
        strategist_monarch_id=parsed.strategist_monarch_id,
        capital_city_id=parsed.capital_city_id,
        starting_troops=tuple(parsed.starting_troops),
        monarch_count=parsed.monarch_count,
        money=parsed.money,
        city_count=parsed.city_count,
        diplomat_monarch_id=parsed.diplomat_monarch_id,
    )


def read_diplomacy_table(data: bytes) -> tuple[tuple[int, ...], ...]:
    start = DIPLOMACY_TABLE_OFFSET
    end = start + DIPLOMACY_RECORD_SIZE * DIPLOMACY_CAPACITY
    table = data[start:end]
    return tuple(
        tuple(table[index * DIPLOMACY_RECORD_SIZE: (index + 1) * DIPLOMACY_RECORD_SIZE])
        for index in range(DIPLOMACY_CAPACITY)
    )


def read_city_table(data: bytes) -> tuple[CityRecord, ...]:
    return tuple(
        read_city_record(index, read_record(data, CITY_TABLE_OFFSET, CITY_RECORD_SIZE, index))
        for index in range(CITY_CAPACITY)
    )


def read_city_record(index: int, data: bytes) -> CityRecord:
    return CityRecord(
        index=index,
        status=data[0x00],
        owner_power_id=data[0x01],
        name=decode_big5_padded(data[0x02:0x08]),
        coordinate_bytes=tuple(data[0x08:0x0C]),
        max_productivity=data[0x0C],
        current_productivity=data[0x0E],
        growth_value=data[0x10],
        disaster_resistance=data[0x11],
        garrison_troops=data[0x12],
        city_type=CityType(data[0x17] & 0x03),
        civil_monarch_id=data[0x19],
    )


def read_army_table(data: bytes) -> tuple[ArmyRecord, ...]:
    return tuple(
        read_army_record(index, read_record(data, ARMY_TABLE_OFFSET, ARMY_RECORD_SIZE, index))
        for index in range(ARMY_CAPACITY)
    )


def read_army_record(index: int, data: bytes) -> ArmyRecord:
    return ArmyRecord(
        index=index,
        status=data[0x00],
        owner_power_id=data[0x01],
        commander_monarch_id=data[0x02],
        total_troops=int.from_bytes(data[0x04:0x06], "little"),
        morale=data[0x06],
        current_coordinate_bytes=tuple(data[0x0E:0x12]),
        target_coordinate_bytes=tuple(data[0x16:0x1A]),
        destination_city_id=data[0x20],
        units=read_army_units(data),
        raw=data,
    )


def read_army_units(data: bytes) -> tuple[ArmyUnitRecord, ...]:
    units = []
    for index, role in enumerate(ARMY_UNIT_ROLES):
        start = ARMY_UNIT_BLOCK_OFFSET + index * ARMY_UNIT_RECORD_SIZE
        raw = data[start: start + ARMY_UNIT_RECORD_SIZE]
        units.append(ArmyUnitRecord(role=role, troops=raw[0], troop_type=raw[1], raw=raw))
    return tuple(units)


def read_monarch_table(data: bytes) -> tuple[MonarchRecord, ...]:
    return tuple(
        read_monarch_record(index, read_record(data, MONARCH_TABLE_OFFSET, MONARCH_RECORD_SIZE, index))
        for index in range(MONARCH_CAPACITY)
    )


def read_monarch_record(index: int, data: bytes) -> MonarchRecord:
    return MonarchRecord(
        index=index,
        attributes=data[0x00],
        portrait_id=data[0x01],
        name=decode_big5_padded(data[0x02:0x08]),
        courtesy_name=decode_big5_padded(data[0x08:0x0E]),
        siege_ability=read_monarch_ability(data[0x0E]),
        field_ability=read_monarch_ability(data[0x0F]),
        naval_ability=read_monarch_ability(data[0x10]),
        prowess=read_monarch_ability(data[0x11]),
        command=read_monarch_ability(data[0x12]),
        politics=read_monarch_ability(data[0x13]),
        list_status=read_monarch_list_status(data[0x17]),
        appearance_countdown=data[0x18],
        target_power_id=data[0x19],
        owner_power_id=data[0x1C],
        captive_owner_power_id=data[0x1D],
    )


def read_unknown_block(data: bytes, offset: int, size: int) -> UnknownBlock:
    block = data[offset: offset + size]
    return UnknownBlock(offset=offset, size=size, nonzero_bytes=sum(1 for byte in block if byte))


def read_monarch_list_status(value: int) -> MonarchListStatus | int:
    try:
        return MonarchListStatus(value)
    except ValueError:
        return value


def read_monarch_ability(value: int) -> int:
    return min(value, 0xA0)


def decode_big5_padded(raw: bytes) -> str:
    text = raw.rstrip(b"\x00").decode("big5", errors="replace")
    return text.strip(f"{BIG5_PAD} \x00")


def read_record(data: bytes, table_offset: int, record_size: int, index: int) -> bytes:
    start = table_offset + index * record_size
    end = start + record_size
    if end > len(data):
        raise ValueError(f"record {index} at 0x{table_offset:x} exceeds save size")
    return data[start:end]
