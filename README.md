# Aurora 4x Support Tools

Aurora 4x (C#版) のセーブデータ（SQLiteDB）を読み取り、ゲーム情報をブラウザで確認できるHTMLダッシュボードを生成するツールです。

---

## 日本語

### 必要環境
- Python 3.x
- Aurora 4x C# 版（`AuroraDB.db` が同フォルダに存在すること）

### 使い方

`aurora_reader.bat` をダブルクリックするだけで両方のツールが自動実行されます。

```
aurora_reader.bat
```

生成されるファイル:
| ファイル | 内容 |
|---|---|
| `aurora_dashboard.html` | 帝国ダッシュボード |
| `aurora_minerals.html` | 鉱物リソースビューワー |
| `aurora_gamelog.txt` | 全ゲームログ（累積） |
| `aurora_gamelog_diff.txt` | 前回実行以降の差分ログ |

---

### aurora_reader.py — 帝国ダッシュボード

ブラウザで開くと4つのタブで帝国情報を確認できます。

#### EMPIRE タブ
- **資産・研究ポイント** — 現在の富・研究キャパシティ
- **研究キュー** — 研究中テクノロジーの残りRP・施設数・進捗バー
- **造船タスク** — 建造中艦船の進捗・造船所名
- **植民地一覧** — 全コロニーと人口
- **鉱物在庫（首都）** — 11種鉱物の在庫量・バー・前回比増減（▲▼）
- **艦船一覧** — 全艦船のクラス・艦隊・燃料・整備状態
- **造船所一覧** — 名称・種別・スリップウェイ数・最大容量

#### SYSTEMS タブ
- 発見済み星系の一覧
- 重力探査・地理探査の完了状況
- ジャンプポイント通過状況
- 調査済み鉱物 Top 3

#### ARMY タブ
- 配備中の地上部隊一覧
- **行クリック** で部隊の詳細展開
  - 構成ユニット（クラス名・数・重量・装甲値・火力値）
  - 装備コンポーネント（貫通力・ダメージ・射数）
  - 特殊能力（Mountain Warfare 等）
- 指揮官名・配備星系・配備天体
- **警察力**（`floor(Σ √size / 100 × units)`）
- 士気・要塞レベル

#### DESIGNS タブ
- 設計済み艦船クラスの一覧（廃止クラスは別表示・チェックで切替）
- サイズ・速度・コスト・乗員・燃料・シールド・就役数
- エンジン・武装・センサー・特殊装備のタグ表示

---

### aurora_minerals.py — 鉱物リソースビューワー

調査済み天体の全鉱物情報を一覧表示します。

- 11種鉱物の埋蔵量・アクセシビリティを天体ごとに表示
- アクセシビリティで色分け（緑=0.8以上 / 橙=0.5以上 / 赤=0.5未満）
- **自動鉱山計算** — 鉱山台数を入力すると年間採掘量をリアルタイム計算
- **軌道採掘判定** — ⛏マークで軌道採掘可能天体を表示
- 星系フィルター・列クリックでソート

---

### ログ差分機能

`aurora_reader.py` は実行のたびに前回終了時点のログ位置を記録します。  
次回実行時は**前回以降の新規イベントのみ** `aurora_gamelog_diff.txt` に出力します。  
AAR（プレイ日記）の下書きや、ChatGPT等への状況報告に便利です。

---

## English

### Requirements
- Python 3.x
- Aurora 4x C# edition (`AuroraDB.db` must be in the same folder)

### Usage

Simply double-click `aurora_reader.bat` to run both tools automatically.

```
aurora_reader.bat
```

Generated files:
| File | Contents |
|---|---|
| `aurora_dashboard.html` | Empire dashboard |
| `aurora_minerals.html` | Mineral resource viewer |
| `aurora_gamelog.txt` | Full game log (cumulative) |
| `aurora_gamelog_diff.txt` | Events since last run |

---

### aurora_reader.py — Empire Dashboard

Opens in a browser with four tabs.

#### EMPIRE Tab
- **Wealth & Research** — Current wealth points and research capacity
- **Research Queue** — Technologies in progress with remaining RP, lab count, and progress bars
- **Shipyard Tasks** — Ships under construction with progress and shipyard name
- **Colonies** — All colonies with population
- **Mineral Stockpile (Capital)** — All 11 minerals with quantity, bar chart, and change indicator vs. last run (▲▼)
- **Active Ships** — All ships with class, fleet, fuel, and maintenance status
- **Shipyards** — Name, type, slipways, and max capacity

#### SYSTEMS Tab
- List of all discovered star systems
- Gravitational and geological survey completion status
- Jump point passage status
- Top 3 surveyed minerals per system

#### ARMY Tab
- List of all deployed ground formations
- **Click any row** to expand unit details:
  - Unit composition (class name, count, tonnage, armour rating, weapon rating)
  - Equipment components (penetration, damage, shots)
  - Special capabilities (Mountain Warfare, etc.)
- Commander name, star system, and deployed body
- **Police Strength** — calculated as `floor(Σ √size_in_tons / 100 × units)` (verified against in-game display)
- Morale and fortification level

#### DESIGNS Tab
- All ship class designs (obsolete classes toggled separately)
- Size, speed, cost, crew, fuel, shields, and active hulls
- Engine, weapon, sensor, and special equipment tags

---

### aurora_minerals.py — Mineral Resource Viewer

Displays all mineral deposits on surveyed bodies.

- Shows all 11 minerals per body with quantity and accessibility
- Color-coded accessibility (green=0.8+ / orange=0.5+ / red=below 0.5)
- **Mining calculator** — Enter a mine count to compute annual output in real time
- **Orbital mining indicator** — ⛏ marks bodies eligible for orbital mining
- System filter and sortable columns

---

### Log Diff Feature

`aurora_reader.py` records the last log position on each run.  
On the next run, only **new events since the previous session** are written to `aurora_gamelog_diff.txt`.  
Useful for AAR write-ups or feeding game status to an AI assistant.

---

## File Structure

```
Aurora1130Full/
├── aurora_reader.bat       # Run both tools (double-click)
├── aurora_reader.py        # Empire dashboard generator
├── aurora_minerals.py      # Mineral resource viewer
├── AuroraDB.db             # Aurora 4x save data (not committed)
├── aurora_dashboard.html   # Generated dashboard (not committed)
├── aurora_minerals.html    # Generated mineral viewer (not committed)
├── aurora_gamelog.txt      # Cumulative game log (not committed)
└── aurora_gamelog_diff.txt # Diff log since last run (not committed)
```
