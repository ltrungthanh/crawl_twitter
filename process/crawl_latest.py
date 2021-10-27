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
        novelId = uriNovels[0]
        chapterId = uriNovels[1]
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
                listUrlNovel.append('https://www.novelpub.com/novel/' + str(novelId))
            else:
                listUrlChapter.append('https://www.novelpub.com/novel/' + str(novelId))
        except:
            listUrlNovel.append('https://www.novelpub.com/novel/' + str(novelId))

        # for key, value in resonse_json.items():
        #     data = value
        # break

    # close
    driver.close()
