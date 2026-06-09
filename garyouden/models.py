from __future__ import annotations

from dataclasses import dataclass
from enum import IntEnum
from pathlib import Path


class MonarchListStatus(IntEnum):
    standby = 0
    army_commander = 1
    civil_minister = 2
    diplomat = 3
    captive = 4


class CityType(IntEnum):
    small_city = 0
    middle_city = 1
    large_city = 2
    pass_city = 3


MONARCH_LIST_STATUS_LABELS = {
    MonarchListStatus.standby: "待命",
    MonarchListStatus.army_commander: "军团长",
    MonarchListStatus.civil_minister: "内政官",
    MonarchListStatus.diplomat: "外交官",
    MonarchListStatus.captive: "被俘",
}

CITY_TYPE_LABELS = {
    CityType.small_city: "小城",
    CityType.middle_city: "中城",
    CityType.large_city: "大城",
    CityType.pass_city: "关卡",
}

MONARCH_ABILITY_MIN = 0x00
MONARCH_ABILITY_MAX = 0xA0


@dataclass(frozen=True)
class SaveHeader:
    day: int
    month: int
    year: int
    player_power_id: int
    trust: int
    save_id: int
    this_month_tax: int
    this_month_recruits: tuple[int, int, int]
    next_month_tax: int
    next_month_recruits: tuple[int, int, int]
    power_count: int
    name: str
    raw_prefix: bytes
    unknown_19: int
    unknown_21: int


@dataclass(frozen=True)
class PowerRecord:
    index: int
    status: int
    ruler_monarch_id: int
    strategist_monarch_id: int
    capital_city_id: int
    starting_troops: tuple[int, int, int]
    monarch_count: int
    money: int
    city_count: int
    diplomat_monarch_id: int

    @property
    def is_active(self) -> bool:
        return self.status != 0


@dataclass(frozen=True)
class CityRecord:
    index: int
    status: int
    owner_power_id: int
    name: str
    coordinate_bytes: tuple[int, int, int, int]
    max_productivity: int
    current_productivity: int
    growth_value: int
    disaster_resistance: int
    garrison_troops: int
    city_type: CityType | int
    civil_monarch_id: int

    @property
    def is_known(self) -> bool:
        return bool(self.name)

    @property
    def city_type_value(self) -> int:
        return int(self.city_type)

    @property
    def city_type_label(self) -> str:
        if isinstance(self.city_type, CityType):
            return CITY_TYPE_LABELS[self.city_type]
        return f"unknown:{self.city_type}"


@dataclass(frozen=True)
class ArmyUnitRecord:
    role: str
    troops: int
    troop_type: int
    raw: bytes


@dataclass(frozen=True)
class ArmyRecord:
    index: int
    status: int
    owner_power_id: int
    commander_monarch_id: int
    total_troops: int
    morale: int
    current_coordinate_bytes: tuple[int, int, int, int]
    target_coordinate_bytes: tuple[int, int, int, int]
    destination_city_id: int
    units: tuple[ArmyUnitRecord, ...]
    raw: bytes

    @property
    def is_active(self) -> bool:
        return any(self.raw)


@dataclass(frozen=True)
class MonarchRecord:
    index: int
    attributes: int
    portrait_id: int
    name: str
    courtesy_name: str
    siege_ability: int
    field_ability: int
    naval_ability: int
    prowess: int
    command: int
    politics: int
    list_status: MonarchListStatus | int
    appearance_countdown: int
    target_power_id: int
    owner_power_id: int
    captive_owner_power_id: int

    @property
    def avoids_capture(self) -> bool:
        return bool(self.attributes & 0x10)

    @property
    def is_ruler(self) -> bool:
        return bool(self.attributes & 0x40)

    @property
    def is_appeared(self) -> bool:
        return bool(self.attributes & 0x80)

    @property
    def list_status_value(self) -> int:
        return int(self.list_status)

    @property
    def list_status_label(self) -> str:
        if isinstance(self.list_status, MonarchListStatus):
            return MONARCH_LIST_STATUS_LABELS[self.list_status]
        return f"unknown:{self.list_status}"

    @property
    def ability_values(self) -> tuple[int, int, int, int, int, int]:
        return (
            self.siege_ability,
            self.field_ability,
            self.naval_ability,
            self.prowess,
            self.command,
            self.politics,
        )

    @property
    def has_valid_ability_range(self) -> bool:
        return all(MONARCH_ABILITY_MIN <= value <= MONARCH_ABILITY_MAX for value in self.ability_values)


@dataclass(frozen=True)
class UnknownBlock:
    offset: int
    size: int
    nonzero_bytes: int

    @property
    def has_data(self) -> bool:
        return self.nonzero_bytes > 0


@dataclass(frozen=True)
class Save:
    index: int
    header: SaveHeader
    powers: tuple[PowerRecord, ...]
    diplomacy: tuple[tuple[int, ...], ...]
    cities: tuple[CityRecord, ...]
    armies: tuple[ArmyRecord, ...]
    monarchs: tuple[MonarchRecord, ...]
    pre_army_block: UnknownBlock
    tail_block: UnknownBlock

    @property
    def active_powers(self) -> tuple[PowerRecord, ...]:
        return tuple(power for power in self.powers if power.is_active)

    @property
    def known_cities(self) -> tuple[CityRecord, ...]:
        return tuple(city for city in self.cities if city.is_known)

    @property
    def active_armies(self) -> tuple[ArmyRecord, ...]:
        return tuple(army for army in self.armies if army.is_active)

    @property
    def appeared_monarchs(self) -> tuple[MonarchRecord, ...]:
        return tuple(monarch for monarch in self.monarchs if monarch.is_appeared)


@dataclass(frozen=True)
class DatFile:
    path: Path
    saves: tuple[Save, ...]
