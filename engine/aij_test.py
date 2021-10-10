from engine.aij import *

def test_get_items():
    aij = Aij()
    test_url = "https://www.aij.or.jp/paper/search.html?categoryId=421"
    df, end = aij.get_items(test_url)

    print(end)
    assert df["論文タイトル"][0]
