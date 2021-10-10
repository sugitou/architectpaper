from logging import debug, error, log

import json
import os
import time
import datetime
import pandas as pd
import requests
import pprint

from common.option import *
from common.driver import set_driver


# 現在時刻取得
now = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

class Jgl:
    def __init__(self):
        # driverを起動
        self.driver = set_driver("chromedriver.exe", False)
        # 任意のclassを見つけるまで暗示的に10秒待つ
        self.driver.implicitly_wait(10)
        
    
    def get_items(self, url):
        # Webサイトを開く
        self.driver.get(url)
        time.sleep(5)

        # ログファイル作成
        log_path = f'{crdir("log")}/log_{now}.log'
        # 件数カウンター作成
        link_num = 0
        # 空のDataFrame作成
        df = pd.DataFrame()
        # ページ数カウント
        i = 2

        while True:
            try:
                titles = self.driver.find_elements_by_class_name('listbox_title_a')    # タイトル
                source = self.driver.find_elements_by_css_selector("div.listbox_info1 > div")
                source_even = source[0::2]    # 著者
                source_odd = source[1::2]    # 発行媒体
                # ページがなくなったら止める
                if len(titles) == 0:
                    print('これ以上ページがありません。')
                    print('スクレイピングを終了します。')
                    end_alert = 'スクレイピングが完了しました。\n'
                    break

                for title, writer, source_title in zip(titles, source_even, source_odd):
                    re_wirter = writer.text.replace('著者： ', '')
                    ws = source_title.text.split(' ')
                    re_source_title = ws[1]
                    year = ws[2]

                    # 件数をカウント
                    link_num += 1
                    out_num = f'{link_num}件目'
                    logfile(log_path, out_num)

                    # DataFrameに対して辞書形式でデータを追加する
                    df = df.append(
                        {"論文の発行年": year, 
                        "論文が発行された媒体": re_source_title,
                        "媒体の巻号": '',
                        "論文タイトル": title.text,
                        "著者": re_wirter,
                        "媒体のページ数": ''},
                        ignore_index=True)
                
                page_param = {
                    "category" : 2,
                    "keyword" : 'X0722A',
                    "page" : i
                }
                next = requests.get("https://jglobal.jst.go.jp/search/articles#" + json.dumps(page_param))
                self.driver.get(next.url)

                i += 1
                # 削除予定
                # 1ページで終了
                # if i == 4:
                #     print('強制終了')
                #     end_alert = 'スクレイピングが完了しました。\n'
                #     break
                
            except Exception as e:
                er = f'{link_num}件目でエラーが発生しました。'
                logfile(log_path, er)
                print(e)
                continue
        
        return df, end_alert


    def get_another_items(self, elem_urls, dict_array):
        for n, source_page_link in enumerate(elem_urls):
            self.driver.get(source_page_link)
            detail = self.driver.find_element_by_class_name('search_detail')
            details = detail.text.split('\n')
            source_number = ''
            source_page = ''
            year = ''
            for row in details:
                if row.startswith('巻：'):
                    source_npy = row.split('  ')
                    source_number = source_npy[0].split('： ')[1]
                    source_page = source_npy[1].split('： ')[1]
                    year = source_npy[2].split('： ')[1]
            
            dict_array[n]["論文の発行年"] = year
            dict_array[n]["媒体の巻号"] = source_number
            dict_array[n]["媒体のページ数"] = source_page
        
        return dict_array