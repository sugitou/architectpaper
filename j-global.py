from logging import debug, error, log

import json
import os
import time
import datetime
import pandas as pd
import requests
import pprint

from driver import set_driver


# 現在時刻取得
now = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')


def crdir(fdname):
    new_dir = f'{os.getcwd()}\\{fdname}'
    # 指定ディレクトリ作成
    if not os.path.exists(new_dir):
        os.mkdir(new_dir)
    return new_dir


def logfile(log_path, log_text):
    with open(log_path, 'a', encoding='utf-8_sig') as f:
        # 件数ごとに出力時間を記載する
        log_now = datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
        log = f'[{log_now}] {log_text}'
        f.write(log + '\n')


class Jglobal:
    def __init__(self):
        # driverを起動
        self.driver = set_driver("chromedriver.exe", False)
        # 任意のclassを見つけるまで暗示的に10秒待つ
        self.driver.implicitly_wait(10)
        
    
    def get_items(self):
        # ログファイル作成
        log_path = f'{crdir("log")}/log_{now}.log'
        # 件数カウンター作成
        link_num = 0
        # リンク一覧
        elem_urls = []
        # ページ数カウント
        i = 0
        # DataFrameに入れるリスト
        dict_array = []

        while True:
            try:
                titles = self.driver.find_elements_by_class_name('listbox_title_a')    # タイトル
                source = self.driver.find_elements_by_css_selector("div.listbox_info1 > div")
                source_even = source[0::2]    # 著者
                source_odd = source[1::2]    # 発行媒体
                # ページがなくなったら止める
                if len(titles) == 0:
                    print('これ以上ページがありません。')
                    print('次に論文詳細ページをスクレイピングします。')
                    break

                for title, writer, source_title in zip(titles, source_even, source_odd):
                    elem_urls.append(title.get_attribute("href"))
                    # 件数をカウント
                    link_num += 1
                    out_num = f'{link_num}件目'
                    logfile(log_path, out_num)

                    dict_array.append(
                        {"論文の発行年": '', 
                        "論文が発行された媒体": source_title.text,
                        "媒体の巻号": '',
                        "論文タイトル": title.text,
                        "著者": writer.text,
                        "媒体のページ数": ''})
                
                page_param = {
                    "category" : 2,
                    "keyword" : 'X0722A',
                    "page" : i
                }
                next = requests.get("https://jglobal.jst.go.jp/search/articles#" + json.dumps(page_param))
                self.driver.get(next.url)
                
            except Exception as e:
                er = f'{link_num}件目でエラーが発生しました。'
                logfile(log_path, er)
                print(e)
                continue
            
            i += 1
            # 削除予定
            # 5ページで終了
            if i == 5:
                break
        
        return elem_urls, dict_array


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


    def item_to_csv(self):
        # Webサイトを開く
        self.driver.get("https://jglobal.jst.go.jp/search/articles#%7B%22category%22%3A%222%22%2C%22keyword%22%3A%22%5C%22X0722A%5C%22%22%2C%22page%22%3A1%7D")
        time.sleep(5)
        try:
            # ポップアップを閉じる
            self.driver.execute_script('document.querySelector(".karte-close").click()')
            time.sleep(5)
            # ポップアップを閉じる
            self.driver.execute_script('document.querySelector(".karte-close").click()')
        except:
            pass

        elem_urls, dict_array = self.get_items()
        conc_dict = self.get_another_items(elem_urls, dict_array)

        df = pd.DataFrame(conc_dict)

        csv_path = f'{crdir("csv_jgl")}/jgl_{now}.csv'
        # csvファイルに取得データを出力
        df.to_csv(csv_path)


# 直接起動された場合はmain()を起動(モジュールとして呼び出された場合は起動しないようにするため)
if __name__ == "__main__":
    jglobal = Jglobal()
    jglobal.item_to_csv()