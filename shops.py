import os
import time
import csv
import json
import itertools
import bs4
import requests

URL_TEMPLATE = "https://map.kaldi.co.jp/kaldi/articleList?account=kaldi&accmd=0&ftop=1&adr={:02d}&pg={}"

def shop_name_split(s):
    if "】" in s:
        idx = s.index("】")+1
        return (s[:idx].strip(), s[idx:].strip())
    else:
        return (None, s)

class ShopInfoDownloader:
    def __init__(self):
        pass

    def get(self, save_dir=None):
        ret = []
        if save_dir is None or not os.path.exists(save_dir):
            if save_dir is not None:
                os.makedirs(save_dir, exist_ok=True)
            for i in range(1, 48):
                for pg in itertools.count(1):
                    r = requests.get(URL_TEMPLATE.format(i, pg))
                    if save_dir is not None:
                        fn = f"{save_dir}/{i:02d}_{pg}.html"
                        with open(fn, "w") as fp:
                            fp.write(r.text)
                    ret.append(r.text)
                    soup = bs4.BeautifulSoup(r.text, "html.parser")
                    pagenation = soup.find_all("div", class_="pagenation")
                    if len(pagenation[0].find_all("a", string="次へ")) == 0:
                        break
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
            note, name = shop_name_split(tds[0].text.strip())
            address = tds[1].text.strip()
            d = {"prefecture": pref, "name": name, "address": address, "note":note}
            ret.append(d)
            
    return ret


def main():
    sid = ShopInfoDownloader()
    htmls = sid.get(save_dir="shops")
    shops = parse(htmls)
    with open("shops.csv", "w") as fp:
        writer = csv.writer(fp)
        writer.writerow(("index", "都道府県", "店舗名", "住所", "備考"))
        index = 1
        for s in shops:
            if s["note"] is None:
                note = ""
            else:
                note = s["note"]
            writer.writerow((index, s["prefecture"], s["name"], s["address"], note))
            index += 1
    with open("shops.json", "w") as fp:
        json.dump(shops, fp)


if __name__ == "__main__":
    main()
