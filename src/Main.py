from selenium import webdriver
from progress.bar import Bar
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import *
from selenium.webdriver.common.keys import Keys
import os
import time
import fnmatch
import datetime
from peewee import *
db = SqliteDatabase('CarDB.db')


class BaseModel(Model):
    class Meta:
        database = db


class Anime(BaseModel):
    Ad = TextField(unique=True)
    Aciklama = TextField(null=True)
    Link = TextField(index=True)
    Durum = IntegerField(default=0)
    created_date = DateTimeField(default=datetime.datetime.now)


class Episode(BaseModel):
    Anime = ForeignKeyField(Anime, backref='episodes')
    Ad = TextField()
    Link = TextField(index=True)
    DLink = TextField(null=True)
    Durum = IntegerField(default=0)
    Created_date = DateTimeField(default=datetime.datetime.now)


def find(pattern, path):
    result = []
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                result.append(os.path.join(root, name))
    return result


def Calistir():

    db.connect()
    db.create_tables([Anime, Episode])

    baseLink = 'https://www.anizm.tv/shokugeki-no-souma-shin-no-sara'
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
    driver.get(baseLink)
    driver.maximize_window()
    wait = WebDriverWait(driver, 50)

    col = driver.find_element_by_class_name('col-lg-7')
    ad = col.find_element_by_tag_name('h2')
    aciklama = col.find_element_by_tag_name('p')

    try:
        anime = Anime.get(Anime.Link == baseLink)
    except DoesNotExist:
        anime = Anime(Ad=ad.text, Aciklama=aciklama.text,
                      Link=baseLink)
        anime.save()

    liste = driver.find_elements_by_css_selector('span.name')
    linkler = []

    def GetDownloadLink():
        buttons = driver.find_elements_by_css_selector('a.kaynakbtn')
        downloadLinks = []
        for button in buttons:
            text = button.text.lower()
            dLinkItem = None
            if text.find('gdrive') > -1 or text.find('google') > -1 or text.find('videomega') > -1 or text.find('yourupload') > -1:
                driver.execute_script("arguments[0].click();", button)
                time.sleep(2)
                iframes = driver.find_elements_by_tag_name('iframe')
                iframe = None
                if len(iframes) > 0:
                    iframe = iframes[0]
                    if iframe != None:
                        iframeSrc = iframe.get_attribute('src')
                        driver.switch_to.frame(iframe)
                        nameMeta = wait.until(lambda d: driver.find_element_by_css_selector(
                            "meta[property='og:title']"))
                        name = nameMeta.get_attribute('context')
                        if iframeSrc.find('drive.google') > -1:
                            id = str(iframeSrc).split('/')[5]
                            downloadAdres = 'https://drive.google.com/uc?id='+id+'&export=download'
                            dLinkItem = {"Type": "GoogleDrive",
                                         "Link": downloadAdres}
                        elif iframeSrc.find('mega.nz') > -1:
                            id = str(iframeSrc).replace(
                                'https://mega.nz/embed/', '')
                            downloadAdres = 'https://mega.nz/file/'+id
                            dLinkItem = {"Type": "MegaNZ",
                                         "Link": downloadAdres}
                        elif iframeSrc.find('yourupload.com') > -1:
                            pageS = driver.page_source
                            start = pageS.find("https://www.yourupload.com/download?file=") + len(
                                "https://www.yourupload.com/download?file=")
                            end = pageS.find("','_blank');")
                            id = pageS[start:end]
                            downloadAdres = 'https://www.yourupload.com/download?file='+id
                            dLinkItem = {"Type": "YourUpload",
                                         "Link": downloadAdres}
                        if dLinkItem:
                            downloadLinks.append(dLinkItem)
                        driver.switch_to.default_content()
        return downloadLinks

    for li in liste:
        max_attemps = 3
        while max_attemps > 0:
            try:
                a = wait.until(lambda d: li.find_element_by_tag_name('a'))
                link = a.get_attribute("href")
                if link != None:
                    try:
                        Episode.get(Episode.Link == link)
                    except DoesNotExist:
                        item = {"text": li.text, "link": link}
                        linkler.append(item)
                break
            except StaleElementReferenceException:
                time.sleep(0.5)
                max_attemps -= 1

    bar = Bar('Processing', max=len(linkler))
    for link in linkler:
        driveUrl = None
        driver.get(link['link'])
        time.sleep(1)
        try:
            labelFan = driver.find_element_by_xpath(
                '/html/body/div[1]/div[2]/div/div[2]/div[1]/div[1]/div[3]/h4')
        except NoSuchElementException as exception:
            driveUrl = GetDownloadLink()
        else:
            if labelFan != None and labelFan.text.index('Fansublar') > -1:
                buttons = []
                divFan = labelFan.find_element_by_xpath('..')
                FanButtons = divFan.find_elements_by_css_selector('a.btn')
                divBag = driver.find_element_by_xpath(
                    '/html/body/div[1]/div[2]/div/div[2]/div[1]/div[1]/div[4]')
                BagButtons = divBag.find_elements_by_css_selector('a.btn')
                for i in range(len(FanButtons)):
                    buttons.append(
                        '/html/body/div[1]/div[2]/div/div[2]/div[1]/div[1]/div[3]/a['+str(i+1)+']')
                for i in range(len(BagButtons)):
                    buttons.append(
                        '/html/body/div[1]/div[2]/div/div[2]/div[1]/div[1]/div[4]/a['+str(i+1)+']')
                driveUrl = []
                for btnPath in buttons:
                    time.sleep(1)
                    btn = wait.until(
                        ec.element_to_be_clickable((By.XPATH, btnPath)))
                    time.sleep(1)
                    btn.click()
                    time.sleep(1)
                    wait.until(ec.visibility_of_element_located(
                        (By.ID, "video-alani")))
                    driveUrl.extend(GetDownloadLink())
                    driver.refresh()
        finally:
            driveUrl = None if driveUrl == [] else driveUrl
            Episode.create(Ad=link['text'], Link=link['link'],
                           DLink=driveUrl, Anime=anime)
            handles = driver.window_handles
            size = len(handles)
            if size > 1:
                for x in range(size-1):
                    driver.switch_to.window(handles[x+1])
                    driver.close()
                driver.switch_to.window(handles[0])
            bar.next()
    bar.finish()
    driver.quit()


Calistir()
