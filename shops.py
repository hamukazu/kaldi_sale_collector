import os
import time
import csv
import bs4
import requests

URL_TEMPLATE1 = (
    "https://map.kaldi.co.jp/kaldi/articleList?account=kaldi&accmd=0&ftop=1&adr={:02d}"
)
URL_TEMPLATE2 = "https://map.kaldi.co.jp/kaldi/articleList?account=kaldi&accmd=0&ftop=1&adr={:02d}&pg={}"


class ShopInfoDownloader:
    def __init__(self):
        pass

    def get(self, save_dir=None):
        ret = []
        if save_dir is None or not os.path.exists(save_dir):
            if save_dir is not None:
                os.makedirs(save_dir, exist_ok=True)
            for i in range(1, 48):
                r = requests.get(URL_TEMPLATE1.format(i))
                soup = bs4.BeautifulSoup(r.text, "html.parser")
                pagenation = soup.find_all("div", class_="pagenation")
                n_pages = len(pagenation[0].find_all("a")) - 1
                fn = f"{save_dir}/{i:02d}_01.html"
                with open(fn, "w") as fp:
                    fp.write(r.text)

                for j in range(2, n_pages + 1):
                    print(i, j)
                    r = requests.get(URL_TEMPLATE2.format(i, j))
                    if save_dir is not None:
                        fn = f"{save_dir}/{i:02d}_{j:02d}.html"
                        with open(fn, "w") as fp:
                            fp.write(r.text)
                    ret.append(r.text)
                time.sleep(0.5)
        else:
            for fn in sorted(os.listdir(save_dir)):
                if fn.endswith(".html"):
                    with open(f"{save_dir}/{fn}") as fp:
                        text = fp.read()
                        ret.append(text)

        return ret


def parse(htmls):
    ret = []
    for html in htmls:
        soup = bs4.BeautifulSoup(html, "html.parser")
        tables = soup.body.find_all("table")
        pref = tables[0].tbody.td.text
        for tr in tables[1].tbody.find_all("tr"):
            tds = tr.find_all("td")
            ret.append((pref, tds[0].text.strip(), tds[1].text.strip()))
    return ret


def main():
    sid = ShopInfoDownloader()
    htmls = sid.get(save_dir="shops")
    shops = parse(htmls)
    with open("shops.csv", "w") as fp:
        writer = csv.writer(fp)
        writer.writerow(("index", "都道府県", "店舗名", "住所"))
        index = 1
        for s in shops:
            writer.writerow((index,) + s)
            index += 1


if __name__ == "__main__":
    main()
