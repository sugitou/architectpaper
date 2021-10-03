import os
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from webdriver_manager.chrome import ChromeDriverManager


class Start:
    # Chromeを起動する関数
    @staticmethod
    def set_driver(driver_path, headless_flg):
        if "chrome" in driver_path:
            options = ChromeOptions()
        else:
            options = Options()

        # ヘッドレスモード（画面非表示モード）をの設定
        if headless_flg == True:
            options.add_argument('--headless')

        # 起動オプションの設定
        options.add_argument(
            '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36')
        # options.add_argument('log-level=3')
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--ignore-ssl-errors')
        options.add_argument('--incognito')          # シークレットモードの設定を付与

        # ChromeのWebDriverオブジェクトを作成する。
        if "chrome" in driver_path:
            return Chrome(ChromeDriverManager().install(),options=options)
        else:
            return Firefox(executable_path=os.getcwd()  + "/" + driver_path,options=options)