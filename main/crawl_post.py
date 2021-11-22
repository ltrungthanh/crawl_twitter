import json
import requests
from selenium import webdriver

from entities.api import api_common


def __init__():
    # 1. Khai báo biến options của ChromeOptions
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["ignore-certificate-errors"])
    options.add_argument('--disable-gpu')
    options.add_argument('--headless')

    # 2. Khai báo biến driver
    driver = webdriver.Chrome(executable_path="../chromedriver.exe", options=options)
    # driver = webdriver.Chrome(executable_path="../chromedriver.exe")

    # 3. set browser
    driver.set_script_timeout(10)

    return driver


# xử lý tiến trình cào latest
def process(url, listUrlNovel, listUrlChapter):
    driver = __init__()
    driver.get(url)
    # ---------------------------------------------------------------------------------------------
    listNovels = driver.find_element_by_class_name('novel-list').find_elements_by_tag_name('li')
    for novel in listNovels:
        linkChapter = novel.find_element_by_tag_name('a').get_attribute('href')
        linkNovel = linkChapter
        uriNovel = linkNovel.replace('https://www.novelpub.com/novel/', '')
        uriNovels = uriNovel.split("/")
        novelIdRaw = uriNovels[0]
        print('novelIdRaw: ' + novelIdRaw)
        chapterId = uriNovels[1]
        # -----------------------------------------------------------------------------------------
        novelName = novel.find_element_by_class_name('item-body').find_element_by_tag_name('h4').text
        novelId = novelIdRaw
        if '(' in novelName:
            indexChar = novelName.rfind('(')
            novelNameTmp = novelName[:indexChar].strip()
            print('novelNameTmp: ' + novelNameTmp)
            novelNameTmp = novelNameTmp.replace('~', '').replace('`', '').replace('!', '') \
                .replace('\'', '').replace('@', '').replace('#', '').replace('$', '').replace('%', '') \
                .replace('^', '').replace('&', '').replace('*', '').replace('(', '').replace(')', '') \
                .replace('_', '').replace('=', '').replace('+', '').replace('.', '').replace(',', '') \
                .replace(':', '').replace(';', '') \
                .lower()
            novelId = novelNameTmp.replace(' ', '-')
        print('novelId: ' + novelId)
        print('------------------------------------------------------------------------------')
        # -----------------------------------------------------------------------------------------
        objRequest = api_common.RequestApi(novelId, '', 0, 0)
        # convert to JSON string
        jsonStr = json.dumps(objRequest.__dict__)
        resonse_tmp = requests.post('https://novel84.xyz/novels/findNovelById', json=json.loads(jsonStr))
        # -----------------------------------------------------------------------------------------
        response_json = json.loads(resonse_tmp.text)
        objResponse = api_common.ResponseApi(**response_json)
        # -----------------------------------------------------------------------------------------
        objData = json.loads(json.dumps(objResponse.data))
        try:
            id = objData['id']
            if not id:
                print(novelId)
                listUrlNovel.append('https://www.novelpub.com/novel/' + novelIdRaw)
            else:
                listUrlChapter.append('https://www.novelpub.com/novel/' + novelIdRaw + '/' + chapterId)
        except:
            listUrlNovel.append('https://www.novelpub.com/novel/' + novelIdRaw)

        # for key, value in resonse_json.items():
        #     data = value
        # break

    # close
    driver.close()
