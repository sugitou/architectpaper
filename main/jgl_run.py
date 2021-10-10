import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from engine.jglobal import Jglobal

def main():
    jglobal = Jglobal()
    jglobal.item_to_csv()

# 直接起動された場合はmain()を起動(モジュールとして呼び出された場合は起動しないようにするため)
if __name__ == "__main__":
    main()