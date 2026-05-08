-- ============================================================
-- Aurora 4x 日本商船名テーマ追加SQL
-- ThemeID=44（空きID）を使用
-- 何度実行しても同じ結果になります（冪等性）
-- ============================================================

DELETE FROM DIM_NamingThemeTypes WHERE ThemeID=44;
INSERT INTO DIM_NamingThemeTypes (ThemeID, Description, RaceNameEligible) VALUES (44, '艦名テーマ・日本の商船（丸）', 0);

DELETE FROM DIM_NamingTheme WHERE NameThemeID=44;

-- 地名系
INSERT INTO DIM_NamingTheme (NameThemeID, Name) VALUES (44, '江戸丸');
INSERT INTO DIM_NamingTheme (NameThemeID, Name) VALUES (44, '京都丸');
INSERT INTO DIM_NamingTheme (NameThemeID, Name) VALUES (44, '大坂丸');
INSERT INTO DIM_NamingTheme (NameThemeID, Name) VALUES (44, '薩摩丸');
INSERT INTO DIM_NamingTheme (NameThemeID, Name) VALUES (44, '長崎丸');
INSERT INTO DIM_NamingTheme (NameThemeID, Name) VALUES (44, '函館丸');
INSERT INTO DIM_NamingTheme (NameThemeID, Name) VALUES (44, '横浜丸');
INSERT INTO DIM_NamingTheme (NameThemeID, Name) VALUES (44, '神戸丸');
INSERT INTO DIM_NamingTheme (NameThemeID, Name) VALUES (44, '博多丸');
INSERT INTO DIM_NamingTheme (NameThemeID, Name) VALUES (44, '那覇丸');
INSERT INTO DIM_NamingTheme (NameThemeID, Name) VALUES (44, '仙台丸');
INSERT INTO DIM_NamingTheme (NameThemeID, Name) VALUES (44, '新潟丸');
INSERT INTO DIM_NamingTheme (NameThemeID, Name) VALUES (44, '広島丸');
INSERT INTO DIM_NamingTheme (NameThemeID, Name) VALUES (44, '富山丸');
INSERT INTO DIM_NamingTheme (NameThemeID, Name) VALUES (44, '金沢丸');

-- 自然・山系
INSERT INTO DIM_NamingTheme (NameThemeID, Name) VALUES (44, '富士丸');
INSERT INTO DIM_NamingTheme (NameThemeID, Name) VALUES (44, '白山丸');
INSERT INTO DIM_NamingTheme (NameThemeID, Name) VALUES (44, '立山丸');
INSERT INTO DIM_NamingTheme (NameThemeID, Name) VALUES (44, '浅間丸');
INSERT INTO DIM_NamingTheme (NameThemeID, Name) VALUES (44, '磐梯丸');
INSERT INTO DIM_NamingTheme (NameThemeID, Name) VALUES (44, '蔵王丸');
INSERT INTO DIM_NamingTheme (NameThemeID, Name) VALUES (44, '鳥海丸');
INSERT INTO DIM_NamingTheme (NameThemeID, Name) VALUES (44, '岩木丸');
INSERT INTO DIM_NamingTheme (NameThemeID, Name) VALUES (44, '阿蘇丸');
INSERT INTO DIM_NamingTheme (NameThemeID, Name) VALUES (44, '霧島丸');

-- 自然・海・川系
INSERT INTO DIM_NamingTheme (NameThemeID, Name) VALUES (44, '白波丸');
INSERT INTO DIM_NamingTheme (NameThemeID, Name) VALUES (44, '潮丸');
INSERT INTO DIM_NamingTheme (NameThemeID, Name) VALUES (44, '黒潮丸');
INSERT INTO DIM_NamingTheme (NameThemeID, Name) VALUES (44, '親潮丸');
INSERT INTO DIM_NamingTheme (NameThemeID, Name) VALUES (44, '利根丸');
INSERT INTO DIM_NamingTheme (NameThemeID, Name) VALUES (44, '信濃丸');
INSERT INTO DIM_NamingTheme (NameThemeID, Name) VALUES (44, '木曽丸');
INSERT INTO DIM_NamingTheme (NameThemeID, Name) VALUES (44, '天塩丸');
INSERT INTO DIM_NamingTheme (NameThemeID, Name) VALUES (44, '石狩丸');
INSERT INTO DIM_NamingTheme (NameThemeID, Name) VALUES (44, '最上丸');

-- 花・植物系
INSERT INTO DIM_NamingTheme (NameThemeID, Name) VALUES (44, '桜丸');
INSERT INTO DIM_NamingTheme (NameThemeID, Name) VALUES (44, '梅丸');
INSERT INTO DIM_NamingTheme (NameThemeID, Name) VALUES (44, '菊丸');
INSERT INTO DIM_NamingTheme (NameThemeID, Name) VALUES (44, '藤丸');
INSERT INTO DIM_NamingTheme (NameThemeID, Name) VALUES (44, '松丸');
INSERT INTO DIM_NamingTheme (NameThemeID, Name) VALUES (44, '竹丸');
INSERT INTO DIM_NamingTheme (NameThemeID, Name) VALUES (44, '楠丸');
INSERT INTO DIM_NamingTheme (NameThemeID, Name) VALUES (44, '柏丸');
INSERT INTO DIM_NamingTheme (NameThemeID, Name) VALUES (44, '桐丸');
INSERT INTO DIM_NamingTheme (NameThemeID, Name) VALUES (44, '橘丸');

-- 風・空・気象系
INSERT INTO DIM_NamingTheme (NameThemeID, Name) VALUES (44, '春風丸');
INSERT INTO DIM_NamingTheme (NameThemeID, Name) VALUES (44, '夏風丸');
INSERT INTO DIM_NamingTheme (NameThemeID, Name) VALUES (44, '秋風丸');
INSERT INTO DIM_NamingTheme (NameThemeID, Name) VALUES (44, '冬風丸');
INSERT INTO DIM_NamingTheme (NameThemeID, Name) VALUES (44, '松風丸');
INSERT INTO DIM_NamingTheme (NameThemeID, Name) VALUES (44, '朝風丸');
INSERT INTO DIM_NamingTheme (NameThemeID, Name) VALUES (44, '夕風丸');
INSERT INTO DIM_NamingTheme (NameThemeID, Name) VALUES (44, '疾風丸');
INSERT INTO DIM_NamingTheme (NameThemeID, Name) VALUES (44, '旋風丸');
INSERT INTO DIM_NamingTheme (NameThemeID, Name) VALUES (44, '暁風丸');

-- 空・光・天体系
INSERT INTO DIM_NamingTheme (NameThemeID, Name) VALUES (44, '朝日丸');
INSERT INTO DIM_NamingTheme (NameThemeID, Name) VALUES (44, '夕日丸');
INSERT INTO DIM_NamingTheme (NameThemeID, Name) VALUES (44, '月光丸');
INSERT INTO DIM_NamingTheme (NameThemeID, Name) VALUES (44, '星光丸');
INSERT INTO DIM_NamingTheme (NameThemeID, Name) VALUES (44, '明星丸');
INSERT INTO DIM_NamingTheme (NameThemeID, Name) VALUES (44, '彗星丸');
INSERT INTO DIM_NamingTheme (NameThemeID, Name) VALUES (44, '銀河丸');
INSERT INTO DIM_NamingTheme (NameThemeID, Name) VALUES (44, '天河丸');
INSERT INTO DIM_NamingTheme (NameThemeID, Name) VALUES (44, '瑞星丸');
INSERT INTO DIM_NamingTheme (NameThemeID, Name) VALUES (44, '曙丸');

-- 縁起・吉祥系
INSERT INTO DIM_NamingTheme (NameThemeID, Name) VALUES (44, '宝栄丸');
INSERT INTO DIM_NamingTheme (NameThemeID, Name) VALUES (44, '千代丸');
INSERT INTO DIM_NamingTheme (NameThemeID, Name) VALUES (44, '万代丸');
INSERT INTO DIM_NamingTheme (NameThemeID, Name) VALUES (44, '大漁丸');
INSERT INTO DIM_NamingTheme (NameThemeID, Name) VALUES (44, '鶴丸');
INSERT INTO DIM_NamingTheme (NameThemeID, Name) VALUES (44, '亀丸');
INSERT INTO DIM_NamingTheme (NameThemeID, Name) VALUES (44, '鳳凰丸');
INSERT INTO DIM_NamingTheme (NameThemeID, Name) VALUES (44, '瑞鶴丸');
INSERT INTO DIM_NamingTheme (NameThemeID, Name) VALUES (44, '吉祥丸');
INSERT INTO DIM_NamingTheme (NameThemeID, Name) VALUES (44, '福徳丸');

-- 勇壮系
INSERT INTO DIM_NamingTheme (NameThemeID, Name) VALUES (44, '武蔵野丸');
INSERT INTO DIM_NamingTheme (NameThemeID, Name) VALUES (44, '日本丸');
INSERT INTO DIM_NamingTheme (NameThemeID, Name) VALUES (44, '大和丸');
INSERT INTO DIM_NamingTheme (NameThemeID, Name) VALUES (44, '扶桑丸');
INSERT INTO DIM_NamingTheme (NameThemeID, Name) VALUES (44, '八洲丸');
INSERT INTO DIM_NamingTheme (NameThemeID, Name) VALUES (44, '皇国丸');
INSERT INTO DIM_NamingTheme (NameThemeID, Name) VALUES (44, '興国丸');
INSERT INTO DIM_NamingTheme (NameThemeID, Name) VALUES (44, '建国丸');
INSERT INTO DIM_NamingTheme (NameThemeID, Name) VALUES (44, '天洋丸');
INSERT INTO DIM_NamingTheme (NameThemeID, Name) VALUES (44, '神洋丸');

-- 鳥・動物系
INSERT INTO DIM_NamingTheme (NameThemeID, Name) VALUES (44, '鷹丸');
INSERT INTO DIM_NamingTheme (NameThemeID, Name) VALUES (44, '鷲丸');
INSERT INTO DIM_NamingTheme (NameThemeID, Name) VALUES (44, '鶯丸');
INSERT INTO DIM_NamingTheme (NameThemeID, Name) VALUES (44, '隼丸');
INSERT INTO DIM_NamingTheme (NameThemeID, Name) VALUES (44, '鴎丸');
INSERT INTO DIM_NamingTheme (NameThemeID, Name) VALUES (44, '千鳥丸');
INSERT INTO DIM_NamingTheme (NameThemeID, Name) VALUES (44, '白鷺丸');
INSERT INTO DIM_NamingTheme (NameThemeID, Name) VALUES (44, '蒼鷹丸');
INSERT INTO DIM_NamingTheme (NameThemeID, Name) VALUES (44, '玄龍丸');
INSERT INTO DIM_NamingTheme (NameThemeID, Name) VALUES (44, '白虎丸');

-- 色・光沢系
INSERT INTO DIM_NamingTheme (NameThemeID, Name) VALUES (44, '白鳳丸');
INSERT INTO DIM_NamingTheme (NameThemeID, Name) VALUES (44, '蒼洋丸');
INSERT INTO DIM_NamingTheme (NameThemeID, Name) VALUES (44, '碧海丸');
INSERT INTO DIM_NamingTheme (NameThemeID, Name) VALUES (44, '金剛丸');
INSERT INTO DIM_NamingTheme (NameThemeID, Name) VALUES (44, '玉響丸');

-- ============================================================
-- プレイヤー民間船クラスに丸テーマを適用
-- Commercial=1 かつ プレイヤー帝国（NPR=0）の船クラスが対象
-- RandomShipNameFromTheme=1 でテーマからランダム命名を有効化
-- ============================================================
UPDATE FCT_ShipClass
SET NameThemeID = 44, RandomShipNameFromTheme = 1
WHERE Commercial = 1
  AND RaceID IN (SELECT RaceID FROM FCT_Race WHERE NPR = 0);
