#!/usr/bin/python
# -*- coding: utf-8 -*-
from selenium import webdriver
from mega import Mega
from lxml import html
import sys
import requests
import json
import os
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import *
from selenium.webdriver.common.keys import Keys
from tkinter import filedialog
from tqdm import tqdm
from tkinter import *
# version to display
version = 'animeDown v0.4.1 alpha by Shakku\n'


class Episode:
    def __init__(self, name, num, url):
        self.name = name
        self.num = num
        self.url = url


class Anime:
    def __init__(self, name, num, url):
        self.name = name
        self.num = num
        self.url = url


def Clear():
    if os.name == "posix":
        os.system('clear')
    else:
        os.system('cls')
    return


# checks directory


def CheckDir(Dir):
    if not os.path.exists(Dir):
        print('[!] Comprueba la carpeta!')
        sys.exit(1)
    return


def SearchEngine():
    url = 'http://www.animekalesi.com/bolumler-243-fairy-tail-2014.html'
    downPath = 'Y:\\Download\\Anime\\Downloader'
    geckodriver = 'geckodriver.exe'
    options = webdriver.FirefoxOptions()
    # options.add_argument('-headless')
    profile = webdriver.FirefoxProfile()
    profile.set_preference("driver.download.folderList", 2)
    profile.set_preference("driver.download.manager.showWhenStarting", False)
    profile.set_preference("driver.download.dir", downPath)
    profile.set_preference(
        "driver.helperApps.neverAsk.saveToDisk", "video/mp4, video/x-matroska")

    driver = webdriver.Firefox(
        executable_path=geckodriver, firefox_options=options, firefox_profile=profile)
    driver.get(url)
    driver.maximize_window()
    wait = WebDriverWait(driver, 60)

    divTwo = driver.find_element_by_id('colTwo')
    alar = divTwo.find_elements_by_tag_name('a')
    imgler = divTwo.find_elements_by_xpath('//img[@alt="Bu Bölümü İndir"]')
    animeList = []
    i = 175
    for img in imgler:
        i += 1
        a = img.find_element_by_xpath('..')
        title = a.get_attribute("title")
        href = a.get_attribute("href")
        response = requests.get(href)
        link = response.url
        anime = Anime(title, i, link)
        jsAnime = json.dumps(anime.__dict__)
        animeList.append(jsAnime)

    with open('data.json', 'w') as outfile:
        json.dump(animeList, outfile)
    return animeList
# main function


def main():
    # animeList = SearchEngine()

    w = Tk()
    w.withdraw()
    path = 'Y:/Download/Anime'  # filedialog.askdirectory()
    if not os.path.exists(path):
        print('[!] Error, quitting!')
        sys.exit(1)
    folderName = 'FairyTail'

# Creating the folder
    savePath = os.path.join(path, folderName)
    if not os.path.exists(savePath):
        os.mkdir(savePath)
    Clear()
    with open('data.json') as f:
        dtl = json.load(f)
        pbar2 = tqdm(dtl)
        # pbar = tqdm(total=100)
        os.chdir(savePath)
    for anis in pbar2:
        ani = json.loads(anis)
        pbar2.set_description("Processing %s" % ani["name"])
        # pbar.update()
        fn = 'ANKAFT'+str(ani['num'])+'.mkv'
        fileName = os.path.join(savePath, fn)
        if os.path.exists(fn):
            continue
        mega = Mega({'verbose': True})
        try:
            mega.download_url(ani["url"], savePath)
        except PermissionError:
            continue
        except:
            print("Unexpected error:", sys.exc_info()[0])
    pbar2.close()
    print('[*] Bitti')
    sys.exit(0)


def sadeceMega():
    w = Tk()
    w.withdraw()
    path = 'Y:/Download/Anime'  # filedialog.askdirectory()
    if not os.path.exists(path):
        print('[!] Error, quitting!')
        sys.exit(1)
    folderName = 'HS'

# Creating the folder
    savePath = os.path.join(path, folderName)
    if not os.path.exists(savePath):
        os.mkdir(savePath)
    Clear()
    mega = Mega({'verbose': True})
    # mega=Mega();
    # m=mega.login();
    url = "https://mega.nz/file/O8lUiazQ#_KlWhgNDqv-Ttj00Wg-W8TeW7YFOTEk6-egkfjU9Nr0"
    try:       
        mega.download_url(url, savePath)
    except PermissionError:
        print("error")
    


if __name__ == "__main__":
    sadeceMega()
