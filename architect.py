from logging import debug, error, log
import os
import wakeup_web
import time
import datetime
import pandas as pd
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
def main(categoryId='', csv_name=''):
    start = wakeup_web.Start()  # chrome起動クラス
    # driverを起動
    if os.name == 'nt':  # Windows
        driver = start.set_driver("chromedriver.exe", False)
    elif os.name == 'posix':  # Mac
        driver = start.set_driver("chromedriver", False)
    # Webサイトを開く
    driver.get("https://www.aij.or.jp/paper/search.html?categoryId=" + categoryId)
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

    comp_list = []
    while True:
        try:
            # テーブルの数
            table_num = driver.find_elements_by_css_selector('tbody > tr')
            # print('テーブル数:', len(table_num))
            # print('中身:', table_num[0].text.split('\n'))
            for tr in table_num:
                tbs = tr.text.split('\n')
                title = tbs[1]
                writer = tbs[2]
                source_number = tbs[3]
                source_page = tbs[4]
                year = tbs[5]
                source_title = tbs[6]

                # 件数をカウント
                job_num += 1
                out_num = f'{job_num}件目'
                logfile(log_path, out_num)

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
            next_page = driver.find_elements_by_css_selector('li.next > a.page-link')
            if len(next_page) > 0:
                page_link = next_page[0].get_attribute("href")
                driver.get(page_link)
            else:
                print('これ以上ページがありません。')
                print('スクレイピングを終了します。')
                break
        except Exception as e:
            er = f'{job_num}件目でエラーが発生しました。'
            logfile(log_path, er)
            print(e)
            continue

    # pprint.pprint(df)
    # csvファイルに取得データを出力
    df_csv = df.to_csv('dfcsv.csv')

# 直接起動された場合はmain()を起動(モジュールとして呼び出された場合は起動しないようにするため)
if __name__ == "__main__":
    search_category = input("categoryIdを入力してください。 >>> ")
    main(search_category)