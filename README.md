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
| `aurora_dashboard.html` | 帝国ダッシュボード（日本語） |
| `aurora_dashboard_en.html` | 帝国ダッシュボード（英語） |
| `aurora_minerals.html` | 鉱物リソースビューワー |
| `aurora_gamelog.txt` | 全ゲームログ（累積） |
| `aurora_gamelog_diff.txt` | 前回実行以降の差分ログ |

---

### aurora_reader.py — 帝国ダッシュボード

ブラウザで開くと6つのタブで帝国情報を確認できます。

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
- **有望な入植候補 (コスト < 3.0)** — 地理調査済みの未入植天体を種族耐性から概算コスト計算し、入植コスト3未満の天体のみ星系ごとに表示。既存コロニーは DB の実測値を使用。

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
- **速度・必要EP計算** — 艦クラスを選択して目標速度を入力すると必要合計EPを自動計算。研究済みエンジンごとに必要基数・合計EP・余剰EPを一覧表示。エンジン数入力で1基あたり必要EPも算出。

#### INTEL タブ
- 把握済みのエイリアン勢力・艦船クラス情報
- 艦船クラスごとの速度・熱シグネチャ・シールド・装甲・艦数

#### TECH タブ
- 研究済みコンポーネントの俯瞰ビュー
- 研究分野ごとのカード表示（Power、Sensors、Direct Fire、Missiles 等）
- 分野内タブで技術種別ごとに最新テクノロジーを色付きでハイライト
- カスタム設計済みコンポーネントの一覧

---

### aurora_minerals.py — 鉱物リソースビューワー

調査済み天体の全鉱物情報を一覧表示します。

- 11種鉱物の埋蔵量・アクセシビリティを天体ごとに表示
- アクセシビリティで色分け（緑=0.8以上 / 橙=0.5以上 / 赤=0.5未満）
- **自動鉱山計算** — 鉱山台数を入力すると年間採掘量をリアルタイム計算
- **軌道採掘判定** — ⛏マークで軌道採掘可能天体を表示
- 星系フィルター・列クリックでソート

---

### ship_designer.html — 艦船設計計算表

手動で開くスタンドアロン計算ツールです（スクリプト不要）。

- **艦種タブ** — ビーム戦闘艦・ミサイル戦闘艦・調査船・キャリア・PDエスコートのプリセット割合
- **総トン数入力** → カテゴリ別トン数・HS をリアルタイム計算
- **設計テキスト解析** — Aurora の艦船設計テキストを貼り付けると自動解析してカテゴリ別HS を算出
- **速度・必要EP計算** — トン数・目標速度を入力するだけで必要合計EPを即計算。エンジン数入力で1基あたり必要EPも算出。

---

### ログ差分機能

`aurora_reader.py` は実行のたびに前回終了時点のログ位置を記録します。  
次回実行時は**前回以降の新規イベントのみ** `aurora_gamelog_diff.txt` に出力します。  
AAR（プレイ日記）の下書きや、ChatGPT等への状況報告に便利です。

---

### おまけ（extras/）

Aurora の DB に直接書き込む日本語化・日本風カスタマイズ用 SQL ファイルのセットです。  
`apply_japanese.bat` をダブルクリックするか `apply_japanese.py` を実行すると、フォルダ内の全 SQL をまとめて適用できます。  
**Aurora 起動中は実行しないでください。**

| ファイル | 内容 |
|---|---|
| `apply_japanese.bat` / `apply_japanese.py` | extras/ 内の全 SQL を一括適用するランチャー |
| `aurora_kanji_names.sql` | 漢字艦名テーマ6種を追加（ThemeID 700〜705） |
| `aurora_maru_names.sql` | 民間船向け「丸」命名テーマを追加（ThemeID 44、101件） |
| `aurora_jp_firstnames.sql` | 日本人指揮官の名（下の名前）を漢字に置換（689件） |
| `aurora_jp_surnames.sql` | 日本人指揮官の姓（苗字）を漢字に置換（974件） |
| `aurora_kanji_ranks.sql` | 階級名を日本語に変更（元帥海軍大将〜） |
| `aurora_theme_names_ja.sql` | 既存の命名テーマ説明文を日本語に更新 |

#### 漢字艦名テーマ詳細

| ThemeID | テーマ名 | 件数 | 内容 |
|---|---|---|---|
| 700 | 艦名テーマ・日本艦（漢字） | 240件 | 日本海軍艦艇名の総合プール |
| 701 | 艦名テーマ・日本戦艦（漢字） | 87件 | 旧律令国68国を含む戦艦名 |
| 702 | 艦名テーマ・日本巡洋艦（漢字） | 72件 | 巡洋艦名 |
| 703 | 艦名テーマ・日本空母（漢字） | 30件 | 空母名 |
| 704 | 艦名テーマ・日本駆逐艦（漢字） | 261件 | 駆逐艦名 |
| 705 | クラステーマ・日本（漢字） | 36件 | 艦型クラス名用 |
| 44 | 艦名テーマ・日本の商船（丸） | 101件 | 民間船向け「○○丸」名 |

---

## English

### Requirements
- Python 3.x
- Aurora 4x C# edition (`AuroraDB.db` must be in the same folder)

### Usage

**English players:** double-click `aurora_reader_en.bat` — generates the English dashboard and mineral viewer.

```
aurora_reader_en.bat
```

**Japanese players (or both languages):** double-click `aurora_reader.bat` — generates Japanese, English, and mineral viewer in one go.

```
aurora_reader.bat
```

To run manually from the command line:

```
python aurora_reader.py              # Japanese dashboard (default)
python aurora_reader.py --lang en    # English dashboard
python aurora_minerals.py            # Mineral viewer
```

Generated files:
| File | Contents |
|---|---|
| `aurora_dashboard.html` | Empire dashboard (Japanese) |
| `aurora_dashboard_en.html` | Empire dashboard (English) |
| `aurora_minerals.html` | Mineral resource viewer |
| `aurora_gamelog.txt` | Full game log (cumulative) |
| `aurora_gamelog_diff.txt` | Events since last run |

---

### aurora_reader.py — Empire Dashboard

Opens in a browser with six tabs.

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
- **Colony Candidates (Cost < 3.0)** — Geo-surveyed uninhabited bodies with estimated colony cost below 3.0, grouped by system. Cost is approximated from surface temperature, gravity, and atmosphere against the player species' tolerances. Existing colonies show the exact value from the database.

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
- **Required EP Calculator** — Select a ship class and enter a target speed to compute the total EP needed. Shows required engine count, total EP, and surplus for each researched engine. Optional engine count input to calculate required EP per engine.

#### INTEL Tab
- Known alien races and ship class information
- Speed, thermal signature, shields, armour, and ship count per class

#### TECH Tab
- Bird's-eye view of all researched components
- Cards per research field (Power, Sensors, Direct Fire, Missiles, etc.)
- Latest technology highlighted in green within each field/type
- Custom-designed component list

---

### aurora_minerals.py — Mineral Resource Viewer

Displays all mineral deposits on surveyed bodies.

- Shows all 11 minerals per body with quantity and accessibility
- Color-coded accessibility (green=0.8+ / orange=0.5+ / red=below 0.5)
- **Mining calculator** — Enter a mine count to compute annual output in real time
- **Orbital mining indicator** — ⛏ marks bodies eligible for orbital mining
- System filter and sortable columns

---

### ship_designer.html — Ship Design Calculator

A standalone tool — open directly in a browser, no Python required.

- **Ship type tabs** — Preset allocation percentages for beam, missile, survey, carrier, and PD escort designs
- **Total tonnage input** → real-time per-category tonnage and HS calculation
- **Design text parser** — Paste Aurora ship design text for automatic category breakdown
- **Required EP Calculator** — Enter tonnage and target speed to instantly compute required total EP. Optional engine count input for per-engine EP target.

---

### Log Diff Feature

`aurora_reader.py` records the last log position on each run.  
On the next run, only **new events since the previous session** are written to `aurora_gamelog_diff.txt`.  
Useful for AAR write-ups or feeding game status to an AI assistant.

---

## File Structure

```
Aurora1130Full/
├── aurora_reader.bat           # Run all tools — Japanese + English (double-click)
├── aurora_reader_en.bat        # English players: dashboard + mineral viewer
├── aurora_reader.py            # Empire dashboard generator
├── aurora_minerals.py          # Mineral resource viewer
├── ship_designer.html          # Standalone ship design calculator
├── AuroraDB.db                 # Aurora 4x save data (not committed)
├── aurora_dashboard.html       # Generated dashboard — Japanese (not committed)
├── aurora_dashboard_en.html    # Generated dashboard — English (not committed)
├── aurora_minerals.html        # Generated mineral viewer (not committed)
├── aurora_gamelog.txt          # Cumulative game log (not committed)
├── aurora_gamelog_diff.txt     # Diff log since last run (not committed)
└── extras/
    ├── apply_japanese.bat      # Run all SQL files (double-click)
    ├── apply_japanese.py       # Run all SQL files (Python)
    ├── aurora_kanji_names.sql  # Kanji ship name themes (ThemeID 700-705)
    ├── aurora_maru_names.sql   # Maru civilian ship theme (ThemeID 44)
    ├── aurora_jp_firstnames.sql# Japanese commander first names (kanji)
    ├── aurora_jp_surnames.sql  # Japanese commander surnames (kanji)
    ├── aurora_kanji_ranks.sql  # Japanese rank names
    └── aurora_theme_names_ja.sql # Japanese descriptions for existing themes
```
