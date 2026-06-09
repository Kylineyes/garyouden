from __future__ import annotations

from collections.abc import Iterable
from typing import Any

from garyouden.layout import (
    ARMY_CAPACITY,
    CITY_CAPACITY,
    FREE_POWER_ID,
    MONARCH_CAPACITY,
    NO_MONARCH_ID,
    NO_STRATEGIST_ID,
    POWER_CAPACITY,
)
from garyouden.models import DatFile, Save


def dat_file_to_dict(dat_file: DatFile, saves: Iterable[Save] | None = None) -> dict[str, Any]:
    selected = dat_file.saves if saves is None else tuple(saves)
    return {
        "path": str(dat_file.path),
        "saves": [save_to_summary_dict(save) for save in selected],
    }


def save_to_summary_dict(save: Save) -> dict[str, Any]:
    header = save.header
    return {
        "index": save.index,
        "name": header.name,
        "date": {"year": header.year, "month": header.month, "day": header.day},
        "player_power_id": none_if_free_power_id(header.player_power_id),
        "trust": header.trust,
        "save_id": header.save_id,
        "power_count": header.power_count,
        "this_month": {
            "tax": header.this_month_tax,
            "recruits": header.this_month_recruits,
        },
        "next_month": {
            "tax": header.next_month_tax,
            "recruits": header.next_month_recruits,
        },
        "table_counts": {
            "total_powers": header.power_count,
            "nonempty_power_slots": len(save.active_powers),
            "known_cities": len(save.known_cities),
            "nonempty_army_slots": len(save.active_armies),
            "appeared_monarchs": len(save.appeared_monarchs),
        },
        "unknown_blocks": unknown_blocks_to_dict(save),
    }


def format_save_overview(save: Save) -> str:
    header = save.header
    player_power = none_if_free_power_id(header.player_power_id)
    lines = [
        f"save[{save.index}] {header.name}",
        f"  date: {header.year:04d}-{header.month:02d}-{header.day:02d}",
        f"  id: {header.save_id}, player_power: {format_optional_id(player_power)}, "
        f"trust: {header.trust}, total_powers: {header.power_count}",
        f"  this_month: tax={header.this_month_tax}, recruits={header.this_month_recruits}",
        f"  next_month: tax={header.next_month_tax}, recruits={header.next_month_recruits}",
        f"  tables: nonempty_power_slots={len(save.active_powers)}/{POWER_CAPACITY}, "
        f"known_cities={len(save.known_cities)}/{CITY_CAPACITY}, "
        f"nonempty_army_slots={len(save.active_armies)}/{ARMY_CAPACITY}, "
        f"appeared_monarchs={len(save.appeared_monarchs)}/{MONARCH_CAPACITY}",
        f"  raw_blocks: pre_army_nonzero={save.pre_army_block.nonzero_bytes}/"
        f"{save.pre_army_block.size}, tail_nonzero={save.tail_block.nonzero_bytes}/"
        f"{save.tail_block.size}",
    ]

    if player_power is not None and player_power < len(save.powers):
        lines.extend(format_player_power(save, player_power))

    return "\n".join(lines)


def format_player_power(save: Save, power_id: int) -> list[str]:
    power = save.powers[power_id]
    ruler_name = monarch_name(save, power.ruler_monarch_id)
    strategist_name = monarch_name(save, power.strategist_monarch_id)
    capital_name = city_name(save, power.capital_city_id)
    return [
        f"  player_power_detail: ruler={format_person(power.ruler_monarch_id, ruler_name)}, "
        f"strategist={format_person(power.strategist_monarch_id, strategist_name)}, "
        f"capital={format_place(power.capital_city_id, capital_name)}",
        f"  player_power_resources: leaders={power.monarch_count}, cities={power.city_count}, "
        f"money={power.money}, starting_troops={power.starting_troops}",
    ]


def none_if_free_power_id(value: int) -> int | None:
    return None if value == FREE_POWER_ID else value


def monarch_name(save: Save, monarch_id: int) -> str | None:
    if monarch_id == NO_MONARCH_ID or monarch_id >= len(save.monarchs):
        return None
    return save.monarchs[monarch_id].name or None


def city_name(save: Save, city_id: int) -> str | None:
    if city_id >= len(save.cities):
        return None
    return save.cities[city_id].name or None


def power_ruler_name(save: Save, power_id: int) -> str | None:
    if power_id == FREE_POWER_ID or power_id >= len(save.powers):
        return None
    return monarch_name(save, save.powers[power_id].ruler_monarch_id)


def format_optional_id(value: int | None) -> str:
    return "none" if value is None else str(value)


def format_person(person_id: int, name: str | None) -> str:
    if person_id in (NO_MONARCH_ID, NO_STRATEGIST_ID):
        return "none"
    return f"{person_id}({name})" if name else str(person_id)


def format_place(place_id: int, name: str | None) -> str:
    return f"{place_id}({name})" if name else str(place_id)


def unknown_blocks_to_dict(save: Save) -> dict[str, dict[str, int]]:
    return {
        "pre_army": {
            "offset": save.pre_army_block.offset,
            "size": save.pre_army_block.size,
            "nonzero_bytes": save.pre_army_block.nonzero_bytes,
        },
        "tail": {
            "offset": save.tail_block.offset,
            "size": save.tail_block.size,
            "nonzero_bytes": save.tail_block.nonzero_bytes,
        },
    }
