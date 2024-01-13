import datastore
import json
import main


def lambda_handler(event, context):
    store = datastore.store("shops.json")
    shops = json.loads(store.get())
    store = datastore.store("sale.json")
    saleinfo = json.loads(store.get())
    prefectures = main.get_prefectures()
    pref_sale = main.get_pref_sale(prefectures, shops, saleinfo)
    store = datastore.store("pref_sale.json")
    store.put(json.dumps(pref_sale))

    with open("index.html", "w") as fp:
        main.write(prefectures, pref_sale, fp)


if __name__ == "__main__":
    lambda_handler(None, None)
