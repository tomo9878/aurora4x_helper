-- ============================================================
-- Aurora 4x 日本人苗字テーマ追加SQL
-- ThemeID=706（空きID）を使用
-- RaceNameEligible=1 で指揮官名にも使用可能
-- 何度実行しても同じ結果になります（冪等性）
-- ============================================================

DELETE FROM DIM_NamingThemeTypes WHERE ThemeID=706;
INSERT INTO DIM_NamingThemeTypes (ThemeID, Description, RaceNameEligible) VALUES (706, '日本人苗字', 1);

DELETE FROM DIM_NamingTheme WHERE NameThemeID=706;

-- 最頻出苗字
INSERT INTO DIM_NamingTheme (NameThemeID, Name) VALUES (706, '佐藤');
INSERT INTO DIM_NamingTheme (NameThemeID, Name) VALUES (706, '鈴木');
INSERT INTO DIM_NamingTheme (NameThemeID, Name) VALUES (706, '高橋');
INSERT INTO DIM_NamingTheme (NameThemeID, Name) VALUES (706, '田中');
INSERT INTO DIM_NamingTheme (NameThemeID, Name) VALUES (706, '渡辺');
INSERT INTO DIM_NamingTheme (NameThemeID, Name) VALUES (706, '伊藤');
INSERT INTO DIM_NamingTheme (NameThemeID, Name) VALUES (706, '山本');
INSERT INTO DIM_NamingTheme (NameThemeID, Name) VALUES (706, '中村');
INSERT INTO DIM_NamingTheme (NameThemeID, Name) VALUES (706, '小林');
INSERT INTO DIM_NamingTheme (NameThemeID, Name) VALUES (706, '加藤');

-- 山・田・川系
INSERT INTO DIM_NamingTheme (NameThemeID, Name) VALUES (706, '吉田');
INSERT INTO DIM_NamingTheme (NameThemeID, Name) VALUES (706, '山田');
INSERT INTO DIM_NamingTheme (NameThemeID, Name) VALUES (706, '山口');
INSERT INTO DIM_NamingTheme (NameThemeID, Name) VALUES (706, '山崎');
INSERT INTO DIM_NamingTheme (NameThemeID, Name) VALUES (706, '山下');
INSERT INTO DIM_NamingTheme (NameThemeID, Name) VALUES (706, '山川');
INSERT INTO DIM_NamingTheme (NameThemeID, Name) VALUES (706, '中川');
INSERT INTO DIM_NamingTheme (NameThemeID, Name) VALUES (706, '石川');
INSERT INTO DIM_NamingTheme (NameThemeID, Name) VALUES (706, '長谷川');
INSERT INTO DIM_NamingTheme (NameThemeID, Name) VALUES (706, '小川');

-- 木・林・森系
INSERT INTO DIM_NamingTheme (NameThemeID, Name) VALUES (706, '木村');
INSERT INTO DIM_NamingTheme (NameThemeID, Name) VALUES (706, '林');
INSERT INTO DIM_NamingTheme (NameThemeID, Name) VALUES (706, '森');
INSERT INTO DIM_NamingTheme (NameThemeID, Name) VALUES (706, '松本');
INSERT INTO DIM_NamingTheme (NameThemeID, Name) VALUES (706, '松田');
INSERT INTO DIM_NamingTheme (NameThemeID, Name) VALUES (706, '竹内');
INSERT INTO DIM_NamingTheme (NameThemeID, Name) VALUES (706, '黒木');
INSERT INTO DIM_NamingTheme (NameThemeID, Name) VALUES (706, '青木');
INSERT INTO DIM_NamingTheme (NameThemeID, Name) VALUES (706, '高木');
INSERT INTO DIM_NamingTheme (NameThemeID, Name) VALUES (706, '鈴木');

-- 橋・本系
INSERT INTO DIM_NamingTheme (NameThemeID, Name) VALUES (706, '橋本');
INSERT INTO DIM_NamingTheme (NameThemeID, Name) VALUES (706, '石橋');
INSERT INTO DIM_NamingTheme (NameThemeID, Name) VALUES (706, '岩橋');
INSERT INTO DIM_NamingTheme (NameThemeID, Name) VALUES (706, '坂本');
INSERT INTO DIM_NamingTheme (NameThemeID, Name) VALUES (706, '松本');
INSERT INTO DIM_NamingTheme (NameThemeID, Name) VALUES (706, '岡本');
INSERT INTO DIM_NamingTheme (NameThemeID, Name) VALUES (706, '西本');
INSERT INTO DIM_NamingTheme (NameThemeID, Name) VALUES (706, '宮本');

-- 藤系（歴史的に多い）
INSERT INTO DIM_NamingTheme (NameThemeID, Name) VALUES (706, '藤原');
INSERT INTO DIM_NamingTheme (NameThemeID, Name) VALUES (706, '藤田');
INSERT INTO DIM_NamingTheme (NameThemeID, Name) VALUES (706, '藤井');
INSERT INTO DIM_NamingTheme (NameThemeID, Name) VALUES (706, '斎藤');
INSERT INTO DIM_NamingTheme (NameThemeID, Name) VALUES (706, '後藤');
INSERT INTO DIM_NamingTheme (NameThemeID, Name) VALUES (706, '近藤');
INSERT INTO DIM_NamingTheme (NameThemeID, Name) VALUES (706, '遠藤');
INSERT INTO DIM_NamingTheme (NameThemeID, Name) VALUES (706, '工藤');
INSERT INTO DIM_NamingTheme (NameThemeID, Name) VALUES (706, '内藤');
INSERT INTO DIM_NamingTheme (NameThemeID, Name) VALUES (706, '武藤');

-- 野・原系
INSERT INTO DIM_NamingTheme (NameThemeID, Name) VALUES (706, '中野');
INSERT INTO DIM_NamingTheme (NameThemeID, Name) VALUES (706, '大野');
INSERT INTO DIM_NamingTheme (NameThemeID, Name) VALUES (706, '小野');
INSERT INTO DIM_NamingTheme (NameThemeID, Name) VALUES (706, '上野');
INSERT INTO DIM_NamingTheme (NameThemeID, Name) VALUES (706, '原田');
INSERT INTO DIM_NamingTheme (NameThemeID, Name) VALUES (706, '菅原');
INSERT INTO DIM_NamingTheme (NameThemeID, Name) VALUES (706, '平原');
INSERT INTO DIM_NamingTheme (NameThemeID, Name) VALUES (706, '榎原');

-- 島・浦・海系
INSERT INTO DIM_NamingTheme (NameThemeID, Name) VALUES (706, '中島');
INSERT INTO DIM_NamingTheme (NameThemeID, Name) VALUES (706, '三浦');
INSERT INTO DIM_NamingTheme (NameThemeID, Name) VALUES (706, '桐島');
INSERT INTO DIM_NamingTheme (NameThemeID, Name) VALUES (706, '白石');
INSERT INTO DIM_NamingTheme (NameThemeID, Name) VALUES (706, '黒田');
INSERT INTO DIM_NamingTheme (NameThemeID, Name) VALUES (706, '丸山');
INSERT INTO DIM_NamingTheme (NameThemeID, Name) VALUES (706, '岡田');

-- 武士・歴史的苗字
INSERT INTO DIM_NamingTheme (NameThemeID, Name) VALUES (706, '武田');
INSERT INTO DIM_NamingTheme (NameThemeID, Name) VALUES (706, '上杉');
INSERT INTO DIM_NamingTheme (NameThemeID, Name) VALUES (706, '織田');
INSERT INTO DIM_NamingTheme (NameThemeID, Name) VALUES (706, '徳川');
INSERT INTO DIM_NamingTheme (NameThemeID, Name) VALUES (706, '豊臣');
INSERT INTO DIM_NamingTheme (NameThemeID, Name) VALUES (706, '伊達');
INSERT INTO DIM_NamingTheme (NameThemeID, Name) VALUES (706, '毛利');
INSERT INTO DIM_NamingTheme (NameThemeID, Name) VALUES (706, '島津');
INSERT INTO DIM_NamingTheme (NameThemeID, Name) VALUES (706, '北条');
INSERT INTO DIM_NamingTheme (NameThemeID, Name) VALUES (706, '今川');
INSERT INTO DIM_NamingTheme (NameThemeID, Name) VALUES (706, '長宗我部');
INSERT INTO DIM_NamingTheme (NameThemeID, Name) VALUES (706, '真田');
INSERT INTO DIM_NamingTheme (NameThemeID, Name) VALUES (706, '立花');
INSERT INTO DIM_NamingTheme (NameThemeID, Name) VALUES (706, '黒田');
INSERT INTO DIM_NamingTheme (NameThemeID, Name) VALUES (706, '加藤');

-- その他よく見る苗字
INSERT INTO DIM_NamingTheme (NameThemeID, Name) VALUES (706, '村上');
INSERT INTO DIM_NamingTheme (NameThemeID, Name) VALUES (706, '池田');
INSERT INTO DIM_NamingTheme (NameThemeID, Name) VALUES (706, '清水');
INSERT INTO DIM_NamingTheme (NameThemeID, Name) VALUES (706, '西村');
INSERT INTO DIM_NamingTheme (NameThemeID, Name) VALUES (706, '福田');
INSERT INTO DIM_NamingTheme (NameThemeID, Name) VALUES (706, '阿部');
INSERT INTO DIM_NamingTheme (NameThemeID, Name) VALUES (706, '菊地');
INSERT INTO DIM_NamingTheme (NameThemeID, Name) VALUES (706, '今井');
INSERT INTO DIM_NamingTheme (NameThemeID, Name) VALUES (706, '井上');
INSERT INTO DIM_NamingTheme (NameThemeID, Name) VALUES (706, '内田');
INSERT INTO DIM_NamingTheme (NameThemeID, Name) VALUES (706, '田村');
INSERT INTO DIM_NamingTheme (NameThemeID, Name) VALUES (706, '金子');
INSERT INTO DIM_NamingTheme (NameThemeID, Name) VALUES (706, '和田');
INSERT INTO DIM_NamingTheme (NameThemeID, Name) VALUES (706, '太田');
INSERT INTO DIM_NamingTheme (NameThemeID, Name) VALUES (706, '佐々木');
INSERT INTO DIM_NamingTheme (NameThemeID, Name) VALUES (706, '宮崎');
INSERT INTO DIM_NamingTheme (NameThemeID, Name) VALUES (706, '石田');
INSERT INTO DIM_NamingTheme (NameThemeID, Name) VALUES (706, '西田');

-- リクエスト
INSERT INTO DIM_NamingTheme (NameThemeID, Name) VALUES (706, '眞鍋');
