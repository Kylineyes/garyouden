# Garyouden Terminology

This document fixes the project vocabulary used in code, documentation, JSON
keys, and workbook export. When external references use different words, keep
the external wording in quotes only when necessary, and use the English name
below for project identifiers.

## Core Terms

| English name | Japanese name | Chinese name | Usage |
| --- | --- | --- | --- |
| `Save` | セーブ | 存档 | One 22,208-byte slot inside `SINARIO.DAT` or `SAVE.DAT`. |
| `DatFile` | DATファイル | DAT 文件 | Whole 88,832-byte DAT file containing four `Save` slots. |
| `SaveHeader` | セーブヘッダー | 存档头 | The first `0x60` bytes of a `Save`. |
| `Power` | 勢力 | 势力 | Political faction or playable side. |
| `Diplomacy` | 外交 | 外交 | 24 by 24 friendship matrix between powers. |
| `City` | 城 | 城池 | City or pass record. |
| `Army` | 軍団 | 军团 | Mobile military unit record. |
| `ArmyUnit` | 部隊 | 部队 | One army formation role, such as commander, vanguard, wing, or reserve. |
| `Leader` | 武将 | 武将 | Leader record. |
| `UnknownBlock` | 未知ブロック | 未知区块 | Parsed-but-undocumented bytes retained as block metadata. |

## Header And Save Fields

| English name | Japanese name | Chinese name | Notes |
| --- | --- | --- | --- |
| `save_id` | 番号 | 编号 | Documented byte at offset `0x11`. |
| `name` | シナリオ名/セーブ名 | 剧本名/存档名 | Big5 text at `0x40-0x5F`, padded by full-width spaces. |
| `year` | 年 | 年 | Start/current year byte. |
| `month` | 月 | 月 | Start/current month byte. |
| `day` | 日 | 日 | Start/current day byte. |
| `player_power_id` | プレイヤー勢力番号 | 玩家势力编号 | `0xFF` means no player power. |
| `trust` | 信頼度 | 信赖度 | Trust value. |
| `this_month_tax` | 今月税率 | 本月税率 | Current month tax rate. |
| `this_month_recruits` | 今月徴兵数 | 本月征兵数 | Three little-endian recruit values. |
| `next_month_tax` | 来月税率 | 下月税率 | Next month tax rate. |
| `next_month_recruits` | 来月徴兵数 | 下月征兵数 | Three little-endian recruit values. |
| `power_count` | 勢力数 | 总势力数 | Total number of powers. |

## Power Fields

| English name | Japanese name | Chinese name | Notes |
| --- | --- | --- | --- |
| `status` | 状態 | 状态 | Power record status byte. `0` is treated as an empty slot; nonzero values are active. |
| `ruler_leader_id` | 君主番号 | 君主编号 | Leader id of the ruler. |
| `strategist_leader_id` | 軍師番号 | 军师编号 | `0x7F` means no strategist. |
| `capital_city_id` | 首都番号 | 首都城池编号 | Capital city id. |
| `starting_troops` | 初期兵数 | 起始兵数 | Three little-endian troop values. |
| `leader_count` | 武将数 | 武将数量 | Number of leader records in the power. |
| `money` | 資金 | 钱 | Three-byte little-endian money value. |
| `city_count` | 城数 | 城池数 | Number of cities controlled by the power. |
| `diplomat_leader_id` | 外交官番号 | 外交官编号 | `0xFF` means no diplomat. |

## City Fields

| English name | Japanese name | Chinese name | Notes |
| --- | --- | --- | --- |
| `owner_power_id` | 所属勢力番号 | 所属势力编号 | `0x18` means empty city in the external notes. |
| `coordinate_bytes` | 座標原始値 | 坐标原始值 | Raw coordinate bytes. |
| `max_productivity` | 最大生産力 | 最大生产力 | City production cap. |
| `current_productivity` | 現在生産力 | 当前生产力 | Current production value. |
| `growth_value` | 上昇値 | 上升值 | Stored display-related growth value. |
| `disaster_resistance` | 防災値 | 防灾值 | Disaster prevention value. |
| `garrison_troops` | 城兵 | 城兵 | City troops. |
| `city_type` | 城種別 | 类型 | See `CityType` values below. |
| `civil_leader_id` | 内政官番号 | 内政官序号 | Leader handling civil affairs. |

## Army Fields

| English name | Japanese name | Chinese name | Notes |
| --- | --- | --- | --- |
| `status` | 状態 | 状态 | Army record status byte. The parser currently treats any nonzero raw record as active. |
| `owner_power_id` | 所属勢力番号 | 所属势力编号 | Owning power id. |
| `commander_leader_id` | 軍団長番号 | 军团长编号 | Army commander leader id. |
| `total_troops` | 総兵数 | 总兵数 | Total troops. |
| `morale` | 士気 | 士气 | Morale. |
| `current_coordinate_bytes` | 現在座標原始値 | 当前坐标原始值 | Raw current coordinate bytes. |
| `target_coordinate_bytes` | 目標座標原始値 | 目标坐标原始值 | Raw target coordinate bytes. |
| `destination_city_id` | 目的地城番号 | 目的地城池编号 | Destination city id. |
| `units` | 兵種編成 | 兵种编成 | Six `ArmyUnit` records from Army offset `0x28`, each 4 bytes. See `ArmyUnit Structure`. |

## ArmyUnit Structure

Each `ArmyUnit` is one 4-byte slot inside an `Army` record's `units` block.
The six slots are ordered by `ArmyUnitRole` values.

| Relative offset | Size | English name | Japanese name | Chinese name | Notes |
| --- | --- | --- | --- | --- | --- |
| `0x00` | 1 | `troops` | 兵数 | 兵数 | Troop count for this formation slot. |
| `0x01` | 1 | `troop_type` | 兵種 | 兵种 | Troop type byte; detailed values are not confirmed yet. |
| `0x02-0x03` | 2 | `unknown_02_03` | 未確認 | 未确认 | Preserved by the parser; meaning is not confirmed yet. |

## Leader Fields

| English name | Japanese name | Chinese name | Notes |
| --- | --- | --- | --- |
| `attributes` | 属性 | 属性 | Bit flags for capture, ruler, appeared, and related status. |
| `portrait_id` | 顔番号 | 头像序号 | Portrait id. |
| `courtesy_name` | 字 | 号 | Courtesy name or style name. |
| `siege_ability` | 城塞戦能力 | 城塞战能力 | Ability value, min `0x00`, max `0xA0`. |
| `field_ability` | 野戦能力 | 野战能力 | Ability value, min `0x00`, max `0xA0`. |
| `naval_ability` | 水戦能力 | 水战能力 | Ability value, min `0x00`, max `0xA0`. |
| `prowess` | 武力 | 武力 | Ability value, min `0x00`, max `0xA0`. |
| `command` | 統率 | 统率 | Ability value, min `0x00`, max `0xA0`. |
| `politics` | 政治 | 政治 | Ability value, min `0x00`, max `0xA0`. |
| `list_status` | 一覧状態 | 列表状态 | Leader list status. See `LeaderListStatus`. |
| `appearance_countdown` | 登場カウントダウン | 登场倒计时 | Months until appearance. |
| `target_power_id` | 投奔勢力番号 | 投奔势力 | Power the leader will join under documented conditions. |
| `owner_power_id` | 所属勢力番号 | 所属势力 | Current owner power. |
| `captive_owner_power_id` | 捕虜所属勢力番号 | 被俘所属势力 | Original owner when captive. |

## LeaderAttributes Structure

`attributes` is a one-byte bit field at relative offset `0x00` in each Leader
record. Confirmed meanings are listed below.

| Bit mask | English name | Japanese name | Chinese name | Notes |
| --- | --- | --- | --- | --- |
| `0x10` | `avoids_capture` | 捕虜回避 | 不会被俘 | Leader is marked as avoiding capture. |
| `0x40` | `is_ruler` | 君主 | 是否君主 | Leader is the ruler of a power. |
| `0x80` | `is_appeared` | 登場済み | 是否登场 | Leader has appeared in the save. |

## Naming Rules

- Use `Save`, `Power`, `Army`, and `Prowess` in code and documentation.
- Constants and JSON keys should follow the same vocabulary where practical,
  for example `SAVE_SIZE`, `POWER_CAPACITY`, `ARMY_RECORD_SIZE`.

## CityType Values

| Value | English name | Japanese name | Chinese name |
| --- | --- | --- | --- |
| `0` | `small_city` | 小城 | 小城 |
| `1` | `middle_city` | 中城 | 中城 |
| `2` | `large_city` | 大城 | 大城 |
| `3` | `pass_city` | 関 | 关卡 |

## ArmyUnitRole Values

| Value | English name | Japanese name | Chinese name |
| --- | --- | --- | --- |
| `0` | `commander` | 主将 | 主将 |
| `1` | `vanguard` | 先鋒 | 先锋 |
| `2` | `left_wing` | 左翼 | 左翼 |
| `3` | `right_wing` | 右翼 | 右翼 |
| `4` | `left_reserve` | 左備 | 左备 |
| `5` | `right_reserve` | 右備 | 右备 |

## LeaderListStatus Values

| Value | English name | Japanese name | Chinese name |
| --- | --- | --- | --- |
| `0` | `standby` | 待機 | 待命 |
| `1` | `army_commander` | 軍団長 | 军团长 |
| `2` | `civil_minister` | 内政官 | 内政官 |
| `3` | `diplomat` | 外交官 | 外交官 |
| `4` | `captive` | 捕虜 | 被俘 |
