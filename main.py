import json
import csv
import re

def trim(s):
    ss = re.sub("【.*$","",s)
    return ss.strip()
    
def main():
    with open("shops.json") as fp:
        shops = json.load(fp)
    with open("sample.json") as fp:
        sale = json.load(fp)
    prefectures = []
    with open("japan_prefectures/japan_prefectures.csv") as fp:
        reader = csv.reader(fp)
        next(reader)
        for row in reader:
            pref = row[3] if row[4] == "道" else row[3] + row[4]
            prefectures.append(pref)
    pref_sales={}
    for pref in prefectures:
        pref_sales[pref]=[]
    pref_sales["NOT_FOUND"]=[]

    l=[]
    for s in shops:
        l.append((trim(s["name"]), s["prefecture"]))
    d = dict(l)
    print(d)
    for s in sale:
        pref = d.get(trim(s["shop"]),"NOT_FOUND")
        pref_sales[pref].append(s)
    for pref in prefectures:
        print(f"=== {pref} ===")
        print(pref_sales[pref])
    print("******* NOT FOUND *******")
    print(pref_sales["NOT_FOUND"])
    

if __name__ == "__main__":
    main()
