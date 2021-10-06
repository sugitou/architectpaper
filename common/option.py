import os
import datetime

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