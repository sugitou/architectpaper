from engine.jgl import *

def test_get_items():
    aij = Jgl()
    test_url = "https://jglobal.jst.go.jp/search/articles#%7B%22category%22%3A%222%22%2C%22keyword%22%3A%22%5C%22X0722A%5C%22%22%2C%22page%22%3A1%7D"
    df, end = aij.get_items(test_url)

    print(end)
    assert df["論文タイトル"][0]
