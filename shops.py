import os
import time
from collections import defaultdict
import csv
import bs4
import requests

URL_TEMPLATE = (
    "https://map.kaldi.co.jp/kaldi/articleList?account=kaldi&accmd=0&ftop=1&adr={:02d}"
)


class ShopInfoDownloader:
    def __init__(self):
        pass

    def get(self, save_dir=None):
        ret = []
        if save_dir is None or not os.path.exists(save_dir):
            if save_dir is not None:
                os.makedirs(save_dir, exist_ok=True)
            for i in range(1, 48):
                print(i)
                r = requests.get(URL_TEMPLATE.format(i))
                if save_dir is None:
                    ret.append(r.text)
                else:
                    fn = f"{save_dir}/{i:02d}.html"
                    with open(fn, "w") as fp:
                        fp.write(r.text)
                time.sleep(0.5)
        else:
            for i in range(1, 48):
                fn = f"{save_dir}/{i:02d}.html"
                with open(fn) as fp:
                    text = fp.read()
                ret.append(text)

        return ret


def parse(htmls):
    ret = defaultdict(list)
    for html in htmls:
        soup = bs4.BeautifulSoup(html, "html.parser")
        tables = soup.body.find_all("table")
        pref = tables[0].tbody.td.text
        for tr in tables[1].tbody.find_all("tr"):
            tds = tr.find_all("td")
            ret[pref].append((tds[0].text.strip(), tds[1].text.strip()))
    return ret


def main():
    sid = ShopInfoDownloader()
    htmls = sid.get(save_dir="download")
    shops = parse(htmls)
    with open("shops.csv", "w") as fp:
        writer = csv.writer(fp)
        writer.writerow(("index", "都道府県", "店舗名", "住所"))
        index = 1
        for pref, v in shops.items():
            for name, addr in v:
                writer.writerow((index, pref, name, addr))
                index += 1


if __name__ == "__main__":
    main()
