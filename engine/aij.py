from logging import debug, error, log
import datetime
import pandas as pd
import pprint

from common.option import *
from common.driver import set_driver
from pandas.core.frame import DataFrame


# 現在時刻取得
now = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

class Aij():
    def __init__(self):
        # driverを起動
        self.driver = set_driver("chromedriver.exe", False)


    def get_items(self, url: str):
        # Webサイトを開く
        self.driver.get(url)

        # ログファイル作成
        # log_path = f'{crdir("log")}/log_{now}.log'
        # 空のDataFrame作成
        df = pd.DataFrame()
        # 件数カウンター作成
        job_num = 0
        # 終了通知
        end_alert = ''
        # i = 0

        while True:
            try:
                # テーブルの数
                table_num = self.driver.find_elements_by_css_selector('tbody > tr')
                # if i == 1:
                #     print('強制終了')
                #     break

                for tr in table_num:
                    tbs = tr.text.split('\n')
                    title = tbs[1]
                    writer = tbs[2].replace('著者名：', '')
                    source_number = tbs[3].replace('巻　号：', '')
                    source_page = tbs[4].replace('ページ：', '')
                    year = tbs[5].replace('年月次：', '')
                    if "-" in year:
                        year = year.split("-")[0]
                    papers = tbs[6].split('[ ')
                    if len(papers) <= 1:
                        source_title = ''
                    else:
                        source_title = papers[-2].replace(' ] ', '')

                    # 件数をカウント
                    # job_num += 1
                    # out_num = f'{job_num}件目'
                    # logfile(log_path, out_num)

                    # DataFrameに対して辞書形式でデータを追加する
                    df = df.append(
                        {"論文の発行年": year, 
                        "論文が発行された媒体": source_title,
                        "媒体の巻号": source_number,
                        "論文タイトル": title,
                        "著者": writer,
                        "媒体のページ数": source_page}, 
                        ignore_index=True)

                # 次のページ情報を取得
                next_page = self.driver.find_elements_by_css_selector('li.next > a.page-link')
                if len(next_page) > 0:
                    page_link = next_page[0].get_attribute("href")
                    self.driver.get(page_link)
                    # i += 1
                else:
                    end_alert = 'スクレイピングが完了しました。\n'
                    break
            except Exception as e:
                # er = f'{job_num}件目でエラーが発生しました。'
                # logfile(log_path, er)
                print(e)
                continue
        
        self.driver.close()

        return df, end_alert