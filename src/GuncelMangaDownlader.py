from time import sleep
from selenium import webdriver
from progress.bar import Bar
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import *
from selenium.webdriver.common.keys import Keys
import os
from peewee import *
import requests
from bs4 import BeautifulSoup
from PIL import Image
from PyPDF2 import PdfFileMerger

bolumDict = []
downPath = 'Y:\\Download\\Manga\\Downloader'
geckodriver = 'geckodriver.exe'
options = webdriver.FirefoxOptions()
options.add_argument('-headless')
profile = webdriver.FirefoxProfile()
profile.set_preference("driver.download.folderList", 2)
profile.set_preference("driver.download.manager.showWhenStarting", False)
profile.set_preference("driver.download.dir", downPath)
profile.set_preference(
    "driver.helperApps.neverAsk.saveToDisk", "video/mp4, video/x-matroska")

driver = webdriver.Firefox(
    executable_path=geckodriver, firefox_options=options, firefox_profile=profile)

wait = WebDriverWait(driver, 50)


def Calistir():
    baseLink = 'https://guncelmanga.com/manga/komi-san-wa-komyushou-desu/bolum-223/'
    driver.get(baseLink)
    driver.maximize_window()
    bolumSelect = driver.find_element_by_class_name('single-chapter-select')
    bolumler = bolumSelect.find_elements_by_class_name('short')

    for bolum in bolumler:
        bolumNo = bolum.get_attribute("value").split("-")[1]
        if int(bolumNo) < 191:
            continue
        bolumDict.append(
            {"id": int(bolumNo), "uri": bolum.get_attribute('data-redirect')})


def Bolumindirici():
    newlist = sorted(bolumDict, key=lambda d: d['id'])
    for bolum in newlist:
        print("Basladi : "+str(bolum["id"]))
        path = ("D:\Manga\\"+str(bolum["id"]))
        try:
            os.mkdir(path)
        except FileExistsError:
            continue
        driver.get(bolum['uri'])
        images = driver.find_elements_by_class_name('wp-manga-chapter-img')
        merger = PdfFileMerger()
        for image in images:
            src = image.get_attribute("src")
            filename, file_extension = os.path.splitext(src)
            response = None
            while response == None:
                try:
                    response = requests.get(src, stream=True)
                except:
                   print("tekrar deneniyor")
                   sleep(5)
            altPath = path+"\\"+image.get_attribute("id")+".pdf"
            cover = Image.open(response.raw).convert("RGB")
            cover.save(altPath, save_all=True)
            merger.append(altPath)
        merger.write(path+".pdf")


Calistir()
Bolumindirici()
