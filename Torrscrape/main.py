import requests
import qbittorrentapi
import pandas
from tabulate import tabulate
import json
from multiprocessing.dummy import Pool as ThreadPool
import click 
import os
import pyshorteners
global bitly_key
bitly_key="aa98784a33cb701c60e40aabb5dfa97c15e6aa62"
global jackett_config
global qbit_config
jackett_config = {"api_key":"","url":"http://localhost:9117"}
qbit_config = {
    "host":"localhost",
    "port":"8080",
    "username":"admin",
    "password":"adminadmin"
}
@click.command()
@click.option("--api", help="jackett api key")
@click.option("--search", help="search term")
@click.option("--catagory", help="catagory")
def main(search,catagory,api=None):
    if api==None:
        try:
            with open("jackett_api.json","r") as f :
                apikey=json.load(f)
            jackett_config["api_key"]=str(apikey["api_key"])
        except:
            print("please provide a jackett api key")
            exit()
    elif api != None:
        api_key={"api_key":f"{api}"}
        if os.path.exists("./jackett_api.json"):
            os.remove("jackett_api.json")
        with open("jackett_api.json", "x") as outfile:
            json.dump(api_key, outfile)
            print("jackett api key saved")
        exit()
    t = search
    cat =catagory
    if t == None or cat == None:
        print("please provide a search term and a catagory")
        exit()
    res = []
    def filter(i, catagory=cat):
        if i["catagory"] == catagory:
            return True
        else:
            return False

    def shorten(i):
        s = pyshorteners.Shortener(api_key=bitly_key)
        i= s.bitly.short(i)
        return i
    def extract_info(i):
        item = {}
        item["Title"] = i["Title"]
        item["catagory"] = i["CategoryDesc"]
        item["source"] = i['Tracker']
        item["link"] = shorten(i["Link"])
        item["magnet"] = i["MagnetUri"]
        item["size"] = i["Size"]/1024/1024/1024
        item["size"] = round(item["size"], 2)
        item["size"] = f"{item['size']} GB"
        if item["magnet"] is not None:
            item["qbit"] = True
        else:
            item["qbit"] = False
        if filter(item):
            res.append(item)
    url = f"{jackett_config['url']}/api/v2.0/indexers/all/results?apikey={jackett_config['api_key']}&Query="
    qbt_client = qbittorrentapi.Client(**qbit_config)
    try:
        qbt_client.auth_log_in()
        print("connected to qbit")
    except qbittorrentapi.LoginFailed as e:
        print("login failed")
        exit()
    print("Searching for torrents..........")
    url=url+t
    r = requests.get(url)
    r = r.text
    r = json.loads(r)
    r = r["Results"]
    pool = ThreadPool(1000)
    pool.map(extract_info, (r))
    pool.close()
    pool.join()
    df = pandas.DataFrame(res)
    if df.empty:
        print("no results found")
        exit()
    else:
        print(tabulate(df.drop(["magnet"], axis=1), tablefmt="grid"))
        print("select the index no of the torrent to add to qbit")
        print("note:the torrent will be added to qbit only if it has a magnet link")
        print("1.Add Torrent:add index_no\n2.exit:exit")
        while True:
            i = input("enter the option :")
            if i == "exit":
                break
            elif i.startswith("add"):
                i = i.split(" ")
                i = i[1]
                i = int(i)
                if res[i]["qbit"]:
                    qbt_client.torrents_add(urls=res[i]["magnet"])
                    print("torrent added")
                else:
                    print("no magnet link")
            else:
                print("invalid option")

    qbt_client.auth_log_out()

        
if __name__ == "__main__":
    main()