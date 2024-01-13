import json
import csv
import jinja2
import re
from datetime import datetime


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


def main():
    with open("shops.json") as fp:
        shops = json.load(fp)
    with open("sale.json") as fp:
        sale = json.load(fp)
    prefectures = []
    with open("japan_prefectures/japan_prefectures.csv") as fp:
        reader = csv.reader(fp)
        next(reader)
        for row in reader:
            pref = row[3] if row[4] == "道" else row[3] + row[4]
            prefectures.append((pref, row[5]))
    pref_sales = {}
    for pref, _ in prefectures:
        pref_sales[pref] = []
    pref_sales["NOT_FOUND"] = []

    l = []
    for s in shops:
        l.append((trim(s["name"]), s["prefecture"]))
    d = dict(l)
    print(d)
    for s in sale:
        shop, shop_note = split(s["shop"])
        s["shop"] = shop
        s["shop_note"] = shop_note
        pref = d.get(s["shop"], "NOT_FOUND")
        pref_sales[pref].append(s)
    for pref, pref_en in prefectures:
        if len(pref_sales[pref]) > 0:
            print(f"=== {pref} ===")
            print(pref_sales[pref])
    print("******* NOT FOUND *******")
    print(pref_sales["NOT_FOUND"])

    env = jinja2.Environment(loader=jinja2.FileSystemLoader("./"))
    template = env.get_template("template.html")
    datestr = datetime.strftime(datetime.now(), "%Y-%m-%d %H:%H:%M")
    html = template.render(
        prefectures=prefectures,
        pref_sales=pref_sales,
        datestr=datestr,
        batched=batched,
    )
    with open("index.html", "w") as fp:
        fp.write(html)


if __name__ == "__main__":
    main()
