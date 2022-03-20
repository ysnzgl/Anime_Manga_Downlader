import requests
from bs4 import BeautifulSoup
import os,stat
from PIL import Image
from PyPDF2 import PdfFileMerger
from tqdm import tqdm


def SeriManga():
    r = requests.get("https://serimanga.com/manga/komi-san-wa-komyushou-desu/191")
    soup1=BeautifulSoup(r.content)
    selector = soup1.find("select",{"id":"chapterSelect"})
    bolumler =selector.findChildren("option")

    for i in tqdm(range(len(bolumler))):
        bolum=bolumler[i] 
        r=requests.get(bolum["value"])
        insoup=BeautifulSoup(r.content)
        images=insoup.find_all("img",{"class":"chapter-pages__item"})
        path=("D:\Manga\\"+str(bolum.text.replace("\n","").replace(":","").replace(",","").replace(".",""))).strip()
        try:
            os.mkdir(path)
        except FileExistsError:
            print("Zaten Dosya Var")
            continue  
        merger = PdfFileMerger()
        for image in images:                
            try:
                src= image["src"] 
            except KeyError:
                src= image["data-src"]
            filename, file_extension=os.path.splitext(src)
            response=requests.get(src,stream=True)     
            altPath=path+"\\"+image["data-number"]+".pdf"          
            cover = Image.open(response.raw).convert("RGB")
            cover.save(altPath, save_all=True)
            merger.append(altPath)
        merger.write(path+".pdf")

def GuncelManga():
    r = requests.get("https://guncelmanga.com/manga/komi-san-wa-komyushou-desu/bolum-191/")
    soup1=BeautifulSoup(r.content)
    selector = soup1.find("select",{"class":"single-chapter-select"})
    bolumler =selector.findChildren("option")

    for i in tqdm(range(len(bolumler))):
        bolum=bolumler[i] 
        r=requests.get(bolum["value"])
        insoup=BeautifulSoup(r.content)
        images=insoup.find_all("img",{"class":"wp-manga-chapter-img"})
        path=("D:\Manga\\"+str(bolum.text.replace("\n","").replace(":","").replace(",","").replace(".",""))).strip()
        try:
            os.mkdir(path)
        except FileExistsError:
            print("Zaten Dosya Var")
            continue  
        merger = PdfFileMerger()
        for image in images:                
            try:
                src= image["src"] 
            except KeyError:
                src= image["data-src"]
            filename, file_extension=os.path.splitext(src)
            response=requests.get(src,stream=True)     
            altPath=path+"\\"+image["data-number"]+".pdf"          
            cover = Image.open(response.raw).convert("RGB")
            cover.save(altPath, save_all=True)
            merger.append(altPath)
        merger.write(path+".pdf")

GuncelManga();