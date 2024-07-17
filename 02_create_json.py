from pprint import pprint
import requests
from bs4 import BeautifulSoup
import re
import json

# pattern = "https://kids.yahoo.co.jp/zukan/animal/kind/"

with open("./animalList.txt","r",encoding="utf-8") as textfile:
    urls = textfile.read()
    urls = urls.split("\n")
    # urls = urls[:-1]

animals = [] 
for j,url in enumerate(urls):
    str_j = str(j).zfill(4)
    print(f"----------{j+1}/{len(urls)}----------")
    response = requests.get(url)
    if response.status_code == 200:
        html = response.text
        soup = BeautifulSoup(html,"html.parser")
        contents = soup.find("div",class_="Contents")
        animal_img = contents.find("img").get("src")
        animal_name = contents.find("h1").text
        animal_description = contents.find("p",class_="cont").text
        ddlist = contents.find_all("dd")
        animal_category = ddlist[1].text
        try:
            animal_size = ddlist[4].text
        except:
            animal_size = None
        animal = {
            "animalId":f"an_{str_j}",
            "url":url,
            "imgurl":animal_img,
            "name":animal_name,
            "description":animal_description,
            "category":animal_category,
            "size":animal_size
        }
        if not animal in animals:
            animals.append(animal)
    else:
        print(f"問題が発生しました\nステータスコード：{response.status_code}\n{response.content}")
with open("./animals.json","w",encoding="utf-8") as jsonfile:
    json.dump(animals,jsonfile,indent=4,ensure_ascii=False)