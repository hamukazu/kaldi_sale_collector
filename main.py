import json
import csv
import jinja2
import re
from datetime import datetime, timezone, timedelta


def trim(s):
    ss = re.sub("【.*$", "", s)
    return ss.strip()


def split(s):
    if "【" in s:
        idx = s.index("【")
        return (s[:idx], s[idx:])
    else:
        return (s, "")


# itertools.batched is implemented in Python 3.12
# This function is for earlier version
def batched(l, n):
    ret = []
    while len(l) > 0:
        ret.append(l[:n])
        l = l[n:]
    return ret


def get_prefectures():
    prefectures = []
    with open("japan_prefectures/japan_prefectures.csv") as fp:
        reader = csv.reader(fp)
        next(reader)
        for row in reader:
            pref = row[3] if row[4] == "道" else row[3] + row[4]
            prefectures.append((pref, row[5]))
    return prefectures


def get_pref_sale(prefectures, shops, sale):
    pref_sale = {}
    for pref, _ in prefectures:
        pref_sale[pref] = []
    pref_sale["NOT_FOUND"] = []

    l = []
    for s in shops:
        l.append((trim(s["name"]), s["prefecture"]))
    d = dict(l)
    for s in sale:
        shop, shop_note = split(s["shop"])
        s["shop"] = shop
        s["shop_note"] = shop_note
        pref = d.get(s["shop"], "NOT_FOUND")
        pref_sale[pref].append(s)
    if len(pref_sale["NOT_FOUND"]) > 0:
        print("******* NOT FOUND *******")
        print(pref_sale["NOT_FOUND"])
    return pref_sale


def write(prefectures, pref_sale, fp):
    env = jinja2.Environment(loader=jinja2.FileSystemLoader("./"))
    template = env.get_template("template.html")
    tz_jst = timezone(timedelta(hours=9), name="JST")
    datestr = datetime.strftime(datetime.now(tz=tz_jst), "%Y-%m-%d %H:%H:%M")
    html = template.render(
        prefectures=prefectures,
        pref_sale=pref_sale,
        datestr=datestr,
        batched=batched,
    )
    fp.write(html)


def main():
    with open("shops.json") as fp:
        shops = json.load(fp)
    with open("sale.json") as fp:
        sale = json.load(fp)
    prefectures = get_prefectures()
    pref_sale = get_pref_sale(prefectures, shops, sale)
    with open("index.html", "w") as fp:
        write(prefectures, pref_sale, fp)


if __name__ == "__main__":
    main()
