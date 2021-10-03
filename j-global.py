from logging import debug, error, log

import json
import os
import wakeup_web
import time
import datetime
import pandas as pd
import requests
import pprint


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


# main処理
def main():
    start = wakeup_web.Start()  # chrome起動クラス
    # driverを起動
    if os.name == 'nt':  # Windows
        driver = start.set_driver("chromedriver.exe", False)
        driver.implicitly_wait(10)
    elif os.name == 'posix':  # Mac
        driver = start.set_driver("chromedriver", False)
    # Webサイトを開く
    driver.get("https://jglobal.jst.go.jp/search/articles#%7B%22category%22%3A%222%22%2C%22keyword%22%3A%22%5C%22X0722A%5C%22%22%2C%22page%22%3A1%7D")
    time.sleep(5)
    try:
        # ポップアップを閉じる
        driver.execute_script('document.querySelector(".karte-close").click()')
        time.sleep(5)
        # ポップアップを閉じる
        driver.execute_script('document.querySelector(".karte-close").click()')
    except:
        pass

    # ログファイル作成
    log_path = f'{crdir("log")}/log_{now}.log'
    # 空のDataFrame作成
    df = pd.DataFrame()
    # 件数カウンター作成
    job_num = 0

    titles = driver.find_elements_by_class_name('listbox_title_a')    # タイトル
    print('title：', titles[0].text)
    source = driver.find_elements_by_css_selector("div.listbox_info1 > div")
    source_even = source[0::2]    # 著者
    source_odd = source[1::2]    # 発行媒体
    # ページがなくなったら止める
    # if len(titles) == 0:
    #     print(str(i))
    #     break

    for title, writer, source_title in zip(titles, source_even, source_odd):
        t_title = title.text
        t_writer = writer.text
        t_source_title = source_title.text
        source_page_link = title.get_attribute("href")
        driver.get(source_page_link)
        detail = driver.find_element_by_class_name('search_detail')
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
        
        # 件数をカウント
        job_num += 1
        out_num = f'{job_num}件目'
        logfile(log_path, out_num)

        df = df.append(
            {"論文の発行年": year, 
            "論文が発行された媒体": t_source_title,
            "媒体の巻号": source_number,
            "論文タイトル": t_title,
            "著者": t_writer,
            "媒体のページ数": source_page}, 
            ignore_index=True)
        
        driver.back()

    i = 2

    # while True:
    #     try:
    #         titles = driver.find_elements_by_class_name('listbox_title_a')    # タイトル
    #         source = driver.find_elements_by_css_selector("div.listbox_info1 > div")
    #         source_even = source[0::2]    # 著者
    #         source_odd = source[1::2]    # 発行媒体
    #         # ページがなくなったら止める
    #         if len(titles) == 0:
    #             print(str(i))
    #             break

    #         for title, writer, source_title in zip(titles, source_even, source_odd):
    #             source_page_link = title.get_attribute("href")
    #             driver.get(source_page_link)
    #             detail = driver.find_element_by_class_name('search_detail')
    #             details = detail.text.split('\n')
    #             source_number = ''
    #             source_page = ''
    #             year = ''
    #             for row in details:
    #                 if row.startswith('巻：'):
    #                     source_npy = row.split('  ')
    #                     source_number = source_npy[0].split('： ')[1]
    #                     source_page = source_npy[1].split('： ')[1]
    #                     year = source_npy[2].split('： ')[1]
    #             driver.back()

    #             # 件数をカウント
    #             job_num += 1
    #             out_num = f'{job_num}件目'
    #             logfile(log_path, out_num)

    #             df = df.append(
    #                 {"論文の発行年": year, 
    #                 "論文が発行された媒体": source_title.text,
    #                 "媒体の巻号": source_number,
    #                 "論文タイトル": title.text,
    #                 "著者": writer.text,
    #                 "媒体のページ数": source_page}, 
    #                 ignore_index=True)

    #     except Exception as e:
    #         er = f'{job_num}件目でエラーが発生しました。'
    #         logfile(log_path, er)
    #         print(e)
    #         continue

        # page_param = {
        #     "category" : 2,
        #     "keyword" : 'X0722A',
        #     "page" : i
        # }
        # next = requests.get("https://jglobal.jst.go.jp/search/articles#" + json.dumps(page_param))
        # driver.get(next.url)
        
        # i += 1
    pprint.pprint(df)


# 直接起動された場合はmain()を起動(モジュールとして呼び出された場合は起動しないようにするため)
if __name__ == "__main__":
    main()