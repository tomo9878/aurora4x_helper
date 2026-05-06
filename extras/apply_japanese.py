"""
Aurora 4x 日本語化SQL 一括適用ツール
使い方:
  python apply_japanese.py                        # AuroraDB.dbを自動検索
  python apply_japanese.py C:\path\to\AuroraDB.db # パス直接指定
"""

import sqlite3
import os
import sys
import glob

# AuroraDB.db を探す
def find_db():
    if len(sys.argv) > 1:
        path = sys.argv[1]
        if os.path.exists(path):
            return path
        print(f"指定されたDBが見つかりません: {path}")
        return None

    # extras/ の親ディレクトリ (Aurora インストールフォルダ) を優先
    parent = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    candidate = os.path.join(parent, "AuroraDB.db")
    if os.path.exists(candidate):
        return candidate

    # カレントディレクトリ
    if os.path.exists("AuroraDB.db"):
        return os.path.abspath("AuroraDB.db")

    return None


def main():
    db_path = find_db()
    if not db_path:
        print()
        print("AuroraDB.db が見つかりませんでした。")
        print("このスクリプトを Aurora のインストールフォルダ内の extras/ に置くか、")
        print("パスを引数で指定してください。")
        print("  例: apply_japanese.bat C:\\Games\\Aurora1130Full\\AuroraDB.db")
        input("\nEnterで終了...")
        sys.exit(1)

    print(f"DB: {db_path}")
    print()

    script_dir = os.path.dirname(os.path.abspath(__file__))
    sql_files = sorted(glob.glob(os.path.join(script_dir, "*.sql")))

    if not sql_files:
        print("SQLファイルが見つかりません。")
        input("\nEnterで終了...")
        sys.exit(1)

    conn = sqlite3.connect(db_path)
    errors = []

    for path in sql_files:
        name = os.path.basename(path)
        try:
            with open(path, encoding="utf-8") as f:
                sql = f.read()
            conn.executescript(sql)
            print(f"[OK] {name}")
        except Exception as e:
            print(f"[NG] {name} — {e}")
            errors.append(name)

    conn.commit()
    conn.close()

    print()
    if errors:
        print(f"警告: {len(errors)}件のSQLでエラーが発生しました: {', '.join(errors)}")
    else:
        print("日本語化完了！ Aurora 4x を再起動すると反映されます。")

    input("\nEnterで終了...")


if __name__ == "__main__":
    main()
