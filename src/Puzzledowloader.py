from selenium import webdriver
import os
import fnmatch,time


def find(pattern, path):
    result = []
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                result.append(os.path.join(root, name))
    return result
    

downPath='Y:\\Download\\Anime\\Downloader'
geckodriver = 'geckodriver.exe'
options = webdriver.FirefoxOptions()
# options.add_argument('-headless')
profile = webdriver.FirefoxProfile()
profile.set_preference("browser.download.folderList", 2)
profile.set_preference("browser.download.manager.showWhenStarting", False)
profile.set_preference("browser.download.dir", downPath)
profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "video/mp4")

browser = webdriver.Firefox(
    executable_path=geckodriver, firefox_options=options, firefox_profile=profile)
browser.get("https://puzzlesubs.com/ceviriler/anime/sword-art-online-alicization-war-of-underworld")
browser.maximize_window()
# iframe=browser.find_element_by_tag_name('iframe')
labels = browser.find_elements_by_css_selector('.MuiButton-label')
adresler = []

for label in labels:
    text = 0
    ind = 0
    try:
        ind = label.text.index('.')
    except ValueError as ex:
        print('"%s" cannot be converted to an int: %s' % (label.text, ex))
    if ind > 0:
        text = int(label.text[:ind])

    if text > 0:
        print(text)
        button = label.find_element_by_xpath('..')
        browser.execute_script("arguments[0].click();", button)
        time.sleep(2)
        boxbul = browser.find_elements_by_css_selector(
            '#simple-popper > .MuiBox-root > a')
        yandex = boxbul[len(boxbul)-1]
        if yandex.text == 'YANDEX':
            adresler.append(yandex.get_attribute("href"))
        browser.execute_script("arguments[0].click();", button)
        time.sleep(2)

for adres in adresler:
    browser.get(adres)
    dwnButton = browser.find_element_by_css_selector(
        '.download-button.action-buttons__button.action-buttons__button_download')
    dwnButton.click()
    time.sleep(10)

devam = True
while devam:
    files = find('*.*.part', downPath)
    devam = True if len(files) > 0 else False
    if devam:
        print('inen dosya sayısı : '+str(len(files)))
        time.sleep(10)

print('bitti')
browser.quit()
