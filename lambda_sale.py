import json
import time
import datastore
import sale


def lambda_handler(event, context):
    store = datastore.store("sale.json")
    sid = sale.SaleInfoDownloader()
    html = sid.get()
    n = 3
    success = False
    while n > 0:
        try:
            saleinfo = sale.parse(html)
            success = True
            break
        except Exception as e:
            print("PARSE ERROR:", e)
            print(html)
        finally:
            n -= 1
            time.sleep(1)
    if success:
        store.put(json.dumps(saleinfo))


if __name__ == "__main__":
    lambda_handler(None, None)
