import json
import datastore
import shops


def lambda_handler(event, context):
    store = datastore.store("shops.json")
    sid = shops.ShopInfoDownloader()
    htmls = sid.get()
    shop_data = shops.parse(htmls)
    shop_data2 = list(
        map(lambda x: {"prefecture": x[0], "name": x[1], "address": x[2]}, shop_data)
    )
    store.put(json.dumps(shop_data2))


if __name__ == "__main__":
    lambda_handler(None, None)
