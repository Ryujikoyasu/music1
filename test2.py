import pandas as pd
import re

def count_papers_per_theme(filename):
    """
    CSVファイルを読み込み、テーマとその論文数を表示する関数

    Args:
      filename: CSVファイル名

    Returns:
      テーマとその論文数を格納した辞書
    """

    df = pd.read_csv(filename)
    theme_counts = {}

    for session in df["Session"]:
        # セッション名の末尾のローマ数字を削除
        theme = re.sub(r' (I|II|III|IV|V|VI|VII|VIII|IX|X|XI|XII|XIII)$', '', session).strip()
        if theme in theme_counts:
            theme_counts[theme] += 1
        else:
            theme_counts[theme] = 1

    return theme_counts

# CSVファイル名
filename = "/Users/ryujikoyasu/Downloads/icra2024_paper_list.csv"

# テーマ別の論文数を計算
theme_counts = count_papers_per_theme(filename)

# 結果を表示
for theme_name, count in theme_counts.items():
    print(f"{theme_name}: {count}")

