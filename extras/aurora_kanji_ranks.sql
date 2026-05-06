-- ============================================================
-- Aurora 4x Nihon階級名 漢字化SQL
-- DIM_RankThemes ThemeID=3 を直接上書き
-- 何度実行しても同じ結果になります（冪等性）
-- ============================================================

UPDATE DIM_RankThemes SET RankName='元帥海軍大将', GFRankName='元帥陸軍大将' WHERE ThemeID=3 AND ThemeRankID=1;
UPDATE DIM_RankThemes SET RankName='海軍大将',     GFRankName='陸軍大将'     WHERE ThemeID=3 AND ThemeRankID=2;
UPDATE DIM_RankThemes SET RankName='海軍中将',     GFRankName='陸軍中将'     WHERE ThemeID=3 AND ThemeRankID=3;
UPDATE DIM_RankThemes SET RankName='海軍少将',     GFRankName='陸軍少将'     WHERE ThemeID=3 AND ThemeRankID=4;
UPDATE DIM_RankThemes SET RankName='海軍大佐',     GFRankName='陸軍大佐'     WHERE ThemeID=3 AND ThemeRankID=5;
UPDATE DIM_RankThemes SET RankName='海軍中佐',     GFRankName='陸軍中佐'     WHERE ThemeID=3 AND ThemeRankID=6;
UPDATE DIM_RankThemes SET RankName='海軍少佐',     GFRankName='陸軍少佐'     WHERE ThemeID=3 AND ThemeRankID=7;

-- テーマ名も日本語化
UPDATE DIM_RankThemeTypes SET ThemeName='日本' WHERE ThemeID=3;
