import json
import os
import shutil
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
    current_dir = os.getcwd()
    shutil.copy2(f"{current_dir}/github", "/tmp/github")
    os.chmod("/tmp/github", 0o600)
    os.chdir("/tmp")
    os.system("ls -l")
    ssh_prefix = f"GIT_SSH_COMMAND='ssh -i /tmp/github -o IdentitiesOnly=yes -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null' HOME=/tmp "
    cmd = (
        ssh_prefix + "git clone -b gh-pages git@github.com:hamukazu/kaldi_sale_info.git"
    )
    print(cmd)
    os.system(cmd)
    os.chdir(current_dir)
    write_html("/tmp/kaldi_sale_info/index.html")
    os.chdir("/tmp/kaldi_sale_info/")
    cmd = "git add index.html"
    print(cmd)
    os.system(cmd)
    cmd = f"git config --local user.name '{user_name}'"
    print(cmd)
    os.system(cmd)
    cmd = f"git config --local user.email '{user_email}'"
    print(cmd)
    os.system(cmd)
    cmd = "git commit -m 'auto commit'"
    print(cmd)
    os.system(cmd)
    cmd = ssh_prefix + "git push"
    print(cmd)
    os.system(cmd)


if __name__ == "__main__":
    lambda_handler(None, None)
