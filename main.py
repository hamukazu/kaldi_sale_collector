import json
import csv
import jinja2
import re
from datetime import datetime


def trim(s):
    ss = re.sub("【.*$", "", s)
    return ss.strip()


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
        pref = d.get(trim(s["shop"]), "NOT_FOUND")
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
        prefectures=prefectures, pref_sales=pref_sales, datestr=datestr
    )
    with open("kaldi_sale_info.html", "w") as fp:
        fp.write(html)


if __name__ == "__main__":
    main()
