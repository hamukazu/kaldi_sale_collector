import json
import datastore
import shops


def lambda_handler(event, context):
    store = datastore.store("shops.json")
    sid = shops.ShopInfoDownloader()
    htmls = sid.get()
    shop_data = shops.parse(htmls)
    store.put(json.dumps(shop_data))


if __name__ == "__main__":
    lambda_handler(None, None)
