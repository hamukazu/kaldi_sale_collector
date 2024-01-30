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


def parse_date(s):
    a = s.split("～")
    ret = []
    for x in a:
        dt = datetime.strptime(re.sub("\(.*\)", "", x.strip()), "%Y年%m月%d日")
        ret.append(dt.isoformat())
    return ret


def include_now(now, strdate_from, strdate_to):
    datetime_from = datetime.fromisoformat(strdate_from + "+09:00")
    datetime_to = datetime.fromisoformat(strdate_to + "+09:00") + timedelta(hours=21)
    return now >= datetime_from and now <= datetime_to


# itertools.batched is implemented in Python 3.12
# This function is for earlier version
def batched(l, n):
    ret = []
    while len(l) > 0:
        ret.append(l[:n])
        l = l[n:]
    return ret


def get_prefectures(home_dir="."):
    prefectures = []
    with open(f"{home_dir}/japan_prefectures/japan_prefectures.csv") as fp:
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
        date_from, date_to = parse_date(s["date"])
        s["date_from"] = date_from
        s["date_to"] = date_to
        pref = d.get(s["shop"], "NOT_FOUND")
        pref_sale[pref].append(s)
    if len(pref_sale["NOT_FOUND"]) > 0:
        print("******* NOT FOUND *******")
        print(pref_sale["NOT_FOUND"])
    return pref_sale


def write(prefectures, pref_sale, fp, home_dir="."):
    env = jinja2.Environment(loader=jinja2.FileSystemLoader(home_dir + "/"))
    template = env.get_template("template.html")
    tz_jst = timezone(timedelta(hours=9), name="JST")
    now = datetime.now(tz=tz_jst)
    datestr = datetime.strftime(now, "%Y-%m-%d %H:%H:%M")
    pref_sale_modified = {}
    for k in pref_sale:
        ss = []
        for d in pref_sale[k]:
            dd = d.copy()
            dd["include_now"] = include_now(now, dd["date_from"], dd["date_to"])
            ss.append(dd)
        pref_sale_modified[k] = ss

    html = template.render(
        prefectures=prefectures,
        pref_sale=pref_sale_modified,
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
    with open("pref_sale.json", "w") as fp:
        json.dump(pref_sale, fp)
    with open("index.html", "w") as fp:
        write(prefectures, pref_sale, fp)


if __name__ == "__main__":
    main()
