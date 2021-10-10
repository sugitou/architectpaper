import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from common.option import *
from engine.jgl import Jgl


def main(fnm, fld):
    jglobal = Jgl()
    # fld = 'csv_jgl'
    # fnm = 'result'
    url = "https://jglobal.jst.go.jp/search/articles#%7B%22category%22%3A%222%22%2C%22keyword%22%3A%22%5C%22X0722A%5C%22%22%2C%22page%22%3A1%7D"
    # DataFrameに格納
    df, end = jglobal.get_items(url)
    csv_path = f'{crdir(fld)}/{fnm}.csv'
    df_csv = df.to_csv(csv_path)

    return end


# 直接起動された場合はmain()を起動(モジュールとして呼び出された場合は起動しないようにするため)
# if __name__ == "__main__":
#     main()