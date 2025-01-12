import os
import time
import csv
import bs4
import json
from tempfile import mkdtemp
import requests
from selenium import webdriver


URL = "https://kaldi.co.jp"


def shop_name_split(s):
    if "】" in s:
        idx = s.index("】")+1
        return (s[:idx].strip(), s[idx:].strip())
    else:
        return (None, s)

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
            if os.uname().sysname != "Darwin":
                service = webdriver.ChromeService("/opt/chromedriver")
            else:
                service = None

            options.binary_location = "/opt/chrome/chrome"
            options.add_argument("--headless=new")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-gpu")
            options.add_argument("--window-size=1280x1696")
            options.add_argument("--single-process")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-dev-tools")
            options.add_argument("--no-zygote")
            options.add_argument(f"--user-data-dir={mkdtemp()}")
            options.add_argument(f"--data-path={mkdtemp()}")
            options.add_argument(f"--disk-cache-dir={mkdtemp()}")
            options.add_argument("--remote-debugging-port=9222")

            driver = webdriver.Chrome(options=options, service=service)
            driver.get(href)
            driver.implicitly_wait(3)
            if save_dir is not None:
                fn = f"{save_dir}/sale.html"
                with open(fn, "w") as fp:
                    fp.write(driver.page_source)
            print("URL:", driver.current_url)
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
        _, shop = shop_name_split(shop.strip())
        address = tr.find(class_="saleadress").text
        address = address.strip()
        f = tr.find(class_="saletitle")
        if f is None:
            title = tr.find(class_="saletitle_f").text
        else:
            title = f.text
        title = title.strip()
        f = tr.find(class_="saledate")
        if f is None:
            date = tr.find(class_="saledate_f").text
        else:
            date = f.text
        date = date.strip()
        detail = tr.find(class_="saledetail").text
        d = dict(shop=shop, address=address, title=title, date=date, detail=detail)
        saleinfo.append(d)
    return saleinfo


def main():
    sid = SaleInfoDownloader()
    html = sid.get(save_dir="sale")
    saleinfo = parse(html)

    with open("sale.json", "w") as fp:
        json.dump(saleinfo, fp)


if __name__ == "__main__":
    main()
