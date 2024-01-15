import json
import os
import configparser
import datastore
import main


def write_html(filename):
    store = datastore.store("shops.json")
    shops = json.loads(store.get())
    store = datastore.store("sale.json")
    saleinfo = json.loads(store.get())
    prefectures = main.get_prefectures()
    pref_sale = main.get_pref_sale(prefectures, shops, saleinfo)
    store = datastore.store("pref_sale.json")
    store.put(json.dumps(pref_sale))

    with open(filename, "w") as fp:
        main.write(prefectures, pref_sale, fp)


def lambda_handler(event, context):
    config = configparser.ConfigParser()
    config.read("github.ini")
    user_name = config["user"]["name"]
    user_email = config["user"]["email"]

    ssh_prefix = "GIT_SSH_COMMAND='ssh -i github -o IdentitiesOnly=yes' "
    cmd = (
        ssh_prefix + "git clone -b gh-pages git@github.com:hamukazu/kaldi_sale_info.git"
    )
    os.system(cmd)
    write_html("./kaldi_sale_info/index.html")
    os.chdir("./kaldi_sale_info/")
    cmd = "git add index.html"
    os.system(cmd)
    cmd = f"git config --local user.name '{user_name}'"
    os.system(cmd)
    cmd = f"git config --local user.email '{user_email}'"
    os.system(cmd)
    cmd = "git commit -m 'auto commit'"
    os.system(cmd)
    cmd = ssh_prefix + "git push"
    os.system(cmd)


if __name__ == "__main__":
    lambda_handler(None, None)
