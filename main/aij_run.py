import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from common.option import *
from engine.aij import Aij

# 現在時刻取得
now = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

def main():
    aij = Aij()
    # 変更予定
    search_category = input("categoryIdを入力してください。 >>> ")
    try:
        category_num = int(search_category)
        categoryId = str(category_num)
    except ValueError:
        return '数字を入力してください。\n'
    if len(categoryId) != 3:
        return '3桁で入力してください。\n'
    fld = input("フォルダ名を入力してください。 >>> ")
    fnm = input("ファイル名を入力してください。 >>> ")
    
    url = "https://www.aij.or.jp/paper/search.html?categoryId=" + categoryId
    # DataFrameに格納
    df, end = aij.get_items(url)
    csv_path = f'{crdir(fld)}/{fnm}.csv'
    df_csv = df.to_csv(csv_path)

    return end

# 直接起動された場合はmain()を起動(モジュールとして呼び出された場合は起動しないようにするため)
if __name__ == "__main__":
    main()