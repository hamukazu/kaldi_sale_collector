import json
import datastore
import sale


def lambda_handler(event, context):
    store = datastore.store("sale.json")
    sid = sale.SaleInfoDownloader()
    html = sid.get()
    saleinfo = sale.parse(html)
    store.put(json.dumps(saleinfo))


if __name__ == "__main__":
    lambda_handler(None, None)
