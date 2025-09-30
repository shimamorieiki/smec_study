#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
from pathlib import Path

def check_analysis_format(file_path):
    """
    analysis.mdファイルが正しい形式に従っているかをチェック

    正しい形式:
    - 各項目は「○○であるため、△△である。」の形で書く
    - 箇条書きで10個挙げる
    - 1つの項目は1文で完結
    """

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 番号付き箇条書きのパターン
    # 例: 1. ○○であるため、△△である。
    pattern_correct = r'^\d+\.\s+.+ため、.+。$'

    # 間違った形式のパターン（見出しと説明文に分かれている）
    pattern_wrong_heading = r'^##\s+\d+\.\s+'
    pattern_wrong_asterisk = r'^\*\*原因\*\*:|^\*\*結果\*\*:|^\*\*因果関係\*\*:'

    lines = content.split('\n')

    correct_items = []
    wrong_items = []
    has_wrong_format = False

    for i, line in enumerate(lines):
        line = line.strip()

        # 正しい形式のチェック
        if re.match(pattern_correct, line):
            correct_items.append((i+1, line))

        # 間違った形式のチェック（見出し形式）
        if re.match(pattern_wrong_heading, line):
            has_wrong_format = True
            wrong_items.append((i+1, line, "見出し形式になっている"))

        # 間違った形式のチェック（原因・結果に分かれている）
        if re.match(pattern_wrong_asterisk, line):
            has_wrong_format = True
            if (i+1, lines[max(0, i-1)].strip(), "原因・結果形式に分かれている") not in wrong_items:
                wrong_items.append((i+1, lines[max(0, i-1)].strip(), "原因・結果形式に分かれている"))

    return {
        'correct_count': len(correct_items),
        'has_wrong_format': has_wrong_format,
        'correct_items': correct_items,
        'wrong_items': wrong_items
    }

def main():
    base_path = Path(r'C:\Users\aifor\prog\smec_study\二次試験\業界分析')

    correct_files = []
    wrong_files = []

    # すべてのanalysis.mdファイルを検索
    for analysis_file in base_path.rglob('analysis.md'):
        result = check_analysis_format(analysis_file)

        relative_path = analysis_file.relative_to(base_path)

        if result['correct_count'] >= 8 and not result['has_wrong_format']:
            correct_files.append({
                'path': str(analysis_file),
                'relative_path': str(relative_path),
                'correct_count': result['correct_count']
            })
        else:
            wrong_files.append({
                'path': str(analysis_file),
                'relative_path': str(relative_path),
                'correct_count': result['correct_count'],
                'has_wrong_format': result['has_wrong_format'],
                'wrong_items': result['wrong_items']
            })

    # レポート出力
    report_path = Path(r'C:\Users\aifor\prog\smec_study\analysis_check_report.txt')

    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("=" * 80 + "\n")
        f.write("業界分析 analysis.md フォーマットチェックレポート\n")
        f.write("=" * 80 + "\n\n")

        f.write(f"総ファイル数: {len(correct_files) + len(wrong_files)}\n")
        f.write(f"正しい形式: {len(correct_files)} ファイル\n")
        f.write(f"間違った形式: {len(wrong_files)} ファイル\n\n")

        f.write("=" * 80 + "\n")
        f.write("【正しい形式のファイル一覧】\n")
        f.write("=" * 80 + "\n\n")

        for file_info in sorted(correct_files, key=lambda x: x['relative_path']):
            f.write(f"✓ {file_info['relative_path']}\n")
            f.write(f"  正しい形式の項目数: {file_info['correct_count']}\n")
            f.write(f"  絶対パス: {file_info['path']}\n\n")

        f.write("=" * 80 + "\n")
        f.write("【間違った形式のファイル一覧】\n")
        f.write("=" * 80 + "\n\n")

        for file_info in sorted(wrong_files, key=lambda x: x['relative_path']):
            f.write(f"✗ {file_info['relative_path']}\n")
            f.write(f"  正しい形式の項目数: {file_info['correct_count']}\n")

            if file_info['has_wrong_format']:
                f.write(f"  問題点: 見出しや原因・結果形式に分かれている\n")
                f.write(f"  詳細:\n")
                for line_num, line, reason in file_info['wrong_items'][:3]:
                    f.write(f"    行{line_num}: {reason}\n")
                    f.write(f"      内容: {line[:100]}...\n")

            f.write(f"  絶対パス: {file_info['path']}\n\n")

    print(f"レポートを作成しました: {report_path}")
    print(f"\n総ファイル数: {len(correct_files) + len(wrong_files)}")
    print(f"正しい形式: {len(correct_files)} ファイル")
    print(f"間違った形式: {len(wrong_files)} ファイル")

if __name__ == "__main__":
    main()