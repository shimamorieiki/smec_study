#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
analysis.mdファイルを新フォーマットに変換するスクリプト
"""

import os
import re
import glob
from pathlib import Path

def extract_industry_name(file_path):
    """ファイルパスから業界名を抽出"""
    path_parts = Path(file_path).parts
    # 二次試験/業界分析/の後の最初のフォルダ名を業界名とする
    try:
        idx = path_parts.index('業界分析')
        if idx + 1 < len(path_parts):
            return path_parts[idx + 1]
    except ValueError:
        pass
    return "業界"

def create_title_from_content(content):
    """内容から適切な小タイトルを生成"""
    # 課題を示すキーワード
    challenge_keywords = ['課題', '困難', '問題', 'リスク', '負担', '不足', '減少', '低下', '高騰', '変動', '影響']

    # 最初の10文字程度から判断
    first_part = content[:30]

    # キーワードマッチング
    if any(kw in content for kw in ['需要', '市場']):
        if '拡大' in content or '増加' in content or '成長' in content:
            return "需要拡大・市場成長"
        elif '縮小' in content or '減少' in content:
            return "市場縮小"

    if '価格' in content:
        if '高騰' in content or '上昇' in content:
            return "価格高騰"
        elif '低下' in content or '下落' in content or '変動' in content:
            return "価格変動・低下"

    if '技術' in content:
        if '導入' in content or '活用' in content or 'デジタル' in content or 'IoT' in content or 'AI' in content:
            return "技術革新・デジタル化"
        elif '習得' in content or '継承' in content:
            return "技術習得・継承"

    if '投資' in content:
        return "投資負担"

    if '労働' in content or '人材' in content or '担い手' in content:
        if '不足' in content:
            return "労働力・人材不足"
        else:
            return "労働・人材環境"

    if '規模' in content:
        return "経営規模"

    if '環境' in content and ('保全' in content or '対策' in content):
        return "環境対策"

    if '輸出' in content:
        return "輸出展開"

    if 'ブランド' in content:
        return "ブランド戦略"

    if '政策' in content or '支援' in content or '補助' in content:
        return "政策支援"

    # デフォルト：最初の数文字から
    for i, char in enumerate(content):
        if char in ['が', 'の', 'は', 'を']:
            return content[:i]

    return content[:15]

def is_challenge_item(content):
    """課題を述べている項目かどうか判定"""
    challenge_indicators = [
        '課題', '困難', '問題', 'リスク', '負担', 'ハードルが高',
        '不足', '減少', '低下', '悪化', '困難', '圧迫',
        '制約', '限定', '阻害', '妨げ', '遅れ', '停滞',
        'ため、', 'により、', 'ので、'  # ネガティブな因果関係
    ]

    # ポジティブな内容は除外
    positive_indicators = [
        '可能', '実現', '向上', '拡大', '増加', '成長', '改善',
        '強化', '促進', '期待', '機会', 'チャンス', '有利'
    ]

    has_challenge = any(indicator in content for indicator in challenge_indicators)
    is_positive = any(indicator in content for indicator in positive_indicators)

    # 課題キーワードがあり、ポジティブ要素が少ない場合に課題と判定
    return has_challenge and not (is_positive and '期待' in content or 'チャンス' in content)

def generate_countermeasures(content, industry_name):
    """内容に応じた対策案を生成"""
    measures = []

    if '価格' in content and ('高騰' in content or '上昇' in content):
        measures.extend([
            "代替品・代替手段の検討",
            "コスト削減策の実施",
            "価格転嫁の交渉力強化",
            "長期契約による価格安定化",
            "効率化による使用量削減"
        ])
    elif '価格' in content and ('変動' in content or '低下' in content):
        measures.extend([
            "契約栽培・契約取引による価格安定化",
            "収入保険への加入",
            "差別化・高付加価値化",
            "直販ルートの確立",
            "複数販路の確保"
        ])

    if '労働' in content or '人材' in content or '担い手' in content:
        if '不足' in content:
            measures.extend([
                "労働環境の改善による人材確保",
                "自動化・機械化による省力化",
                "外部委託・協業の活用",
                "法人化による組織的雇用",
                "多様な人材(女性・高齢者・外国人)の活用"
            ])
        elif '長時間' in content or '拘束' in content:
            measures.extend([
                "自動化・機械化による作業軽減",
                "外部委託・代替要員の確保",
                "交代制・シフト制の導入",
                "作業効率化による時間短縮",
                "法人化による役割分担"
            ])

    if '投資' in content and '高額' in content or '初期投資' in content:
        measures.extend([
            "補助金・助成金の積極活用",
            "リース・レンタルによる初期負担軽減",
            "共同購入・共同利用",
            "段階的な導入計画",
            "投資効果の見える化と計画的実施"
        ])

    if '技術' in content:
        if '習得' in content or '難しさ' in content:
            measures.extend([
                "研修・講習会への参加",
                "専門家・先進事例からの学習",
                "マニュアル・教材の整備",
                "段階的な技術導入",
                "外部専門家の活用"
            ])
        elif '継承' in content:
            measures.extend([
                "技術のマニュアル化・見える化",
                "OJT・メンタリング制度",
                "動画・デジタル技術活用",
                "後継者育成プログラム",
                "地域での技術伝承システム"
            ])

    if '環境' in content and ('負荷' in content or '対策' in content):
        measures.extend([
            "環境配慮型技術の導入",
            "資源循環システムの構築",
            "環境認証の取得",
            "地域との合意形成",
            "補助事業の活用"
        ])

    if '規模' in content and ('小規模' in content or '非効率' in content):
        measures.extend([
            "農地・事業基盤の集約化",
            "協業・共同化による実質規模拡大",
            "作業受委託の活用",
            "法人化による組織的経営",
            "ICT活用による効率化"
        ])

    if '販路' in content or '流通' in content:
        measures.extend([
            "直販ルートの開拓",
            "EC・通販の活用",
            "契約取引の拡大",
            "複数チャネルの確保",
            "ブランド化による差別化"
        ])

    if '需要' in content and '減少' in content:
        measures.extend([
            "新市場・新用途の開拓",
            "輸出への展開",
            "商品開発・差別化",
            "需要喚起キャンペーン",
            "異業種連携"
        ])

    if '認証' in content or '許可' in content:
        measures.extend([
            "認証取得支援制度の活用",
            "デジタルツールによる管理効率化",
            "グループ認証の検討",
            "専門家のサポート活用",
            "段階的な取得計画"
        ])

    # 対策が少ない場合は汎用的なものを追加
    if len(measures) < 3:
        measures.extend([
            "専門家・コンサルタントへの相談",
            "先進事例の研究・ベンチマーキング",
            "補助金・支援制度の活用",
            "業界団体・組合との連携",
            "段階的・計画的な取組み"
        ])

    # 重複排除と最大5個まで
    unique_measures = []
    for m in measures:
        if m not in unique_measures:
            unique_measures.append(m)
        if len(unique_measures) >= 5:
            break

    return unique_measures[:5]

def convert_file(file_path):
    """1つのファイルを新フォーマットに変換"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 既に新フォーマットの場合はスキップ
    if content.startswith('# ') and '特徴' in content.split('\n')[0]:
        print(f"Skip (already converted): {file_path}")
        return False

    # 業界名を取得
    industry_name = extract_industry_name(file_path)

    # 行ごとに分割
    lines = content.strip().split('\n')

    # 新しいコンテンツを構築
    new_content = f"# {industry_name}の特徴\n\n"

    for line in lines:
        # 番号付きリスト項目を抽出（2つのパターンに対応）
        # パターン1: "1→1. 内容" (農業フォルダなど)
        # パターン2: "1. 内容" (その他のフォルダ)
        match = re.match(r'\s*(?:\d+→)?(\d+)\.\s*(.+)', line)
        if match:
            num = match.group(1)
            item_content = match.group(2)

            # タイトルを生成
            title = create_title_from_content(item_content)

            new_content += f"## {num}. {title}\n\n"
            new_content += f"{item_content}\n\n"

            # 課題項目には対策を追加
            if is_challenge_item(item_content):
                measures = generate_countermeasures(item_content, industry_name)
                if measures:
                    new_content += "💡 **対策**\n"
                    for measure in measures:
                        new_content += f"- {measure}\n"
                    new_content += "\n"

    # ファイルに書き込み
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)

    print(f"Converted: {file_path}")
    return True

def main():
    """メイン処理"""
    base_dir = Path(__file__).parent / "二次試験" / "業界分析"

    # すべてのanalysis.mdファイルを取得
    files = list(base_dir.glob('**/analysis.md'))

    print(f"Found {len(files)} files")
    print("=" * 60)

    converted_count = 0
    skipped_count = 0

    for file_path in sorted(files):
        try:
            if convert_file(str(file_path)):
                converted_count += 1
            else:
                skipped_count += 1
        except Exception as e:
            print(f"Error processing {file_path}: {e}")

    print("=" * 60)
    print(f"Conversion completed!")
    print(f"  Converted: {converted_count} files")
    print(f"  Skipped: {skipped_count} files")
    print(f"  Total: {len(files)} files")

if __name__ == "__main__":
    main()