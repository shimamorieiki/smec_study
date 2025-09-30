import os
import re
from pathlib import Path

# 検索対象ディレクトリ
base_dir = Path(r"C:\Users\aifor\prog\smec_study\二次試験\業界分析")

# 結果を格納するリスト
incomplete_files = []
complete_files = []

# すべてのanalysis.mdファイルを検索
for analysis_file in base_dir.rglob("analysis.md"):
    try:
        with open(analysis_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # 「1. 」から「10. 」までのパターンを検索
        pattern = r'^\d+\.\s'
        matches = re.findall(pattern, content, re.MULTILINE)

        # マッチした番号を抽出
        numbers = [int(m.strip('. ')) for m in matches]

        # 重複を除去してソート
        unique_numbers = sorted(set(numbers))

        # 1から10まで揃っているかチェック
        expected = list(range(1, 11))

        # 相対パスを取得
        rel_path = analysis_file.relative_to(base_dir)

        if unique_numbers == expected:
            complete_files.append(str(rel_path))
        else:
            missing = [n for n in expected if n not in unique_numbers]
            incomplete_files.append({
                'path': str(rel_path),
                'found_numbers': unique_numbers,
                'missing': missing,
                'count': len(unique_numbers)
            })

    except Exception as e:
        print(f"エラー: {analysis_file}: {e}")

# 結果を出力
print("=" * 80)
print("チェック結果サマリー")
print("=" * 80)
print(f"総ファイル数: {len(complete_files) + len(incomplete_files)}")
print(f"完全なファイル（10項目）: {len(complete_files)}")
print(f"不完全なファイル（10項目未満）: {len(incomplete_files)}")
print()

if incomplete_files:
    print("=" * 80)
    print("【10項目未満のファイル一覧】")
    print("=" * 80)

    # 業界ごとにグループ化
    by_industry = {}
    for item in incomplete_files:
        parts = Path(item['path']).parts
        industry = parts[0] if len(parts) > 0 else "その他"

        if industry not in by_industry:
            by_industry[industry] = []
        by_industry[industry].append(item)

    # 業界ごとに表示
    for industry, files in sorted(by_industry.items()):
        print(f"\n【{industry}】({len(files)}件)")
        print("-" * 80)
        for item in files:
            print(f"  ファイル: {item['path']}")
            print(f"  項目数: {item['count']}/10")
            print(f"  見つかった番号: {item['found_numbers']}")
            if item['missing']:
                print(f"  欠けている番号: {item['missing']}")
            print()
else:
    print("\n全てのファイルが10項目を満たしています！")

# 結果をファイルに保存
output_file = Path(r"C:\Users\aifor\prog\smec_study\analysis_check_report.txt")
with open(output_file, 'w', encoding='utf-8') as f:
    f.write("=" * 80 + "\n")
    f.write("analysis.md ファイルチェック結果\n")
    f.write("=" * 80 + "\n\n")
    f.write(f"総ファイル数: {len(complete_files) + len(incomplete_files)}\n")
    f.write(f"完全なファイル（10項目）: {len(complete_files)}\n")
    f.write(f"不完全なファイル（10項目未満）: {len(incomplete_files)}\n\n")

    if incomplete_files:
        f.write("=" * 80 + "\n")
        f.write("【10項目未満のファイル一覧】\n")
        f.write("=" * 80 + "\n")

        for industry, files in sorted(by_industry.items()):
            f.write(f"\n【{industry}】({len(files)}件)\n")
            f.write("-" * 80 + "\n")
            for item in files:
                f.write(f"  ファイル: {item['path']}\n")
                f.write(f"  項目数: {item['count']}/10\n")
                f.write(f"  見つかった番号: {item['found_numbers']}\n")
                if item['missing']:
                    f.write(f"  欠けている番号: {item['missing']}\n")
                f.write("\n")
    else:
        f.write("\n全てのファイルが10項目を満たしています！\n")

print(f"\n結果をファイルに保存しました: {output_file}")