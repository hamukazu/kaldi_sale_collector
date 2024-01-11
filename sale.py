import os
import time
import csv
import bs4
import requests
from selenium import webdriver

URL = "https://kaldi.co.jp"


class SaleInfoDownloader:
    def __init__(self):
        pass

    def get(self, save_dir=None):
        if save_dir is None or not os.path.exists(save_dir):
            if save_dir is not None:
                os.makedirs(save_dir, exist_ok=True)
            r = requests.get(URL)
            soup = bs4.BeautifulSoup(r.text, "html.parser")
            for a in soup.find_all("a"):
                if a.text == "周年セール":
                    href = a["href"]
                    break
            options = webdriver.chrome.options.Options()
            options.add_argument("--disable-extensions")
            options.add_argument("--headless=new")
            driver = webdriver.Chrome(options=options)
            driver.get(href)
            if save_dir is not None:
                fn = f"{save_dir}/sale.html"
                with open(fn, "w") as fp:
                    fp.write(driver.page_source)
            return driver.page_source
        else:
            fn = f"{save_dir}/sale.html"
            with open(fn) as fp:
                ret = fp.read()
            return ret


def parse(html):
    soup = bs4.BeautifulSoup(html, "html.parser")
    trs = soup.table.tbody.find_all("tr")
    saleinfo = []
    for tr in trs:
        shop = tr.find("a").text
        address = tr.find("td", class_="saleadress").text
        title = tr.find("td", class_="saletitle").text
        date = tr.find("p", class_="saledate").text
        detail = tr.find("p", class_="saledetail").text
        d = dict(shop=shop, address=address, title=title, date=date, detail=detail)
        saleinfo.append(d)
    return saleinfo


def main():
    sid = SaleInfoDownloader()
    html = sid.get(save_dir="sale")
    saleinfo = parse(html)
    print(saleinfo)


if __name__ == "__main__":
    main()
