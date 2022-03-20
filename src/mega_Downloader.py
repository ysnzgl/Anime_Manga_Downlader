#!/usr/bin/python
# -*- coding: utf-8 -*-
from mega import Mega
from lxml import html
import sys
import os
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import *
from selenium.webdriver.common.keys import Keys
from tkinter import filedialog
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

# http request


def GetUrl(Url):
    try:      
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
        response = requests.get(Url, headers=headers)
        # print(response.content)
        print(response.text)
    except:
        print('[!] Error! No se pudo conectar!')
        sys.exit(1)
    page = html.fromstring(response.content)
    return page

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
    alar = page.findall('a')
    for a in alar:
        print(a)
        # check links, todo better
    # linkNum = len(animeLinks)
    # if linkNum != len(animeNames):
    #     print('[!] Error, links ausentes!')
    #     sys.exit(1)

        # create anime list
        animeList = []

        for n in range(0, linkNum):
            anime = Anime(animeNames[n], n, animeLinks[n])
            animeList.append(anime)
        return animeList

# main function


def main():
    test = SearchEngine()
    w = Tk()
    w.withdraw()
    path = filedialog.askdirectory()
    if not os.path.exists(path):
        print('[!] Error, quitting!')
        sys.exit(1)
    folderName = 'Test'

# Creating the folder
    savePath = os.path.join(path, folderName)
    if not os.path.exists(savePath):
        os.mkdir(savePath)

# create Mega downloader object
    mega = Mega({'verbose': True})

# Starting download...
    Clear()
    print('[*] Descargando ' + 'TestTitle' + ' en ' + savePath)
    print('[*] ' + str(1) + ' capitulos en cola...')

    try:
        mega.download_url(
            'https://mega.nz/file/jtAGkTTA#H5NEsfn-gVmkeJwTK__gxij3fyIh3xyngbUmuX7tu0Q', savePath)
    except:
        print("Unexpected error:", sys.exc_info()[0])

        # iterate through episodes list and download
        # for episode in episodes:
        # 	print '[*] Capitulo numero ' + str(episode.num) + ' descargando...'
        # 	try:

        # 	except:
        # 		print '[!] Error! Saliendo!'
        # 		exit(1)
        # 	print '[*] Capitulo ' + str(episode.num) + ' descargado!'

        # Finish and exit if no errors
    print('[*] Descarga terminada! Presiona enter para salir.')
    # raw_input()
    sys.exit(0)


if __name__ == "__main__":
    main()
