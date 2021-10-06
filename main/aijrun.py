from engine.aij import Aij

def main():
    aij = Aij()
    search_category = input("categoryIdを入力してください。 >>> ")
    aij.main(search_category)

# 直接起動された場合はmain()を起動(モジュールとして呼び出された場合は起動しないようにするため)
if __name__ == "__main__":
    main()