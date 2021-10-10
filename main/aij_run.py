import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from common.option import *
from engine.aij import Aij


def main(search_category, fnm, fld):
    aij = Aij()
    try:
        category_num = int(search_category)
        categoryId = str(category_num)
    except ValueError:
        return '数字を入力してください。\n'
    if len(categoryId) != 3:
        return '3桁で入力してください。\n'
    
    url = "https://www.aij.or.jp/paper/search.html?categoryId=" + categoryId
    # DataFrameに格納
    df, end = aij.get_items(url)
    end = 'categoryId：' + categoryId + 'の' + end
    csv_path = f'{crdir(fld)}/{fnm}.csv'
    df_csv = df.to_csv(csv_path)

    return end