import random
from datetime import datetime

from selenium import webdriver
from PIL import Image
import requests
import json

from entities.novel.novel import Novel, RecentChapter, FirstChapter


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


# xử lý tiến trình cào novel
def process(url):
    driver = __init__()
    driver.get(url)
    # ---------------------------------------------------------------------------------------------
    novel_info = driver.find_element_by_class_name('novel-info')
    # ---------------------------------------------------------------------------------------------
    novelRate = novel_info.find_element_by_class_name('rating-star').find_element_by_tag_name('strong').text
    if float(novelRate) < 3:
        return
    # ---------------------------------------------------------------------------------------------
    novelId = url.replace('https://www.novelpub.com/novel/', '')
    # ---------------------------------------------------------------------------------------------
    novelName = novel_info.find_element_by_tag_name('h1').text
    # ---------------------------------------------------------------------------------------------
    novelAuthor = novel_info.find_element_by_tag_name('a').find_element_by_tag_name('span').text
    # ---------------------------------------------------------------------------------------------
    novelRank = novel_info.find_element_by_class_name('rank').find_element_by_tag_name('strong').text
    novelRank = novelRank.replace('RANK', '').strip()
    novelHot = 0
    if int(novelRank) < 100:
        novelHot = 1

    # ---------------------------------------------------------------------------------------------
    novelLinkImage = driver.find_element_by_class_name('fixed-img').find_element_by_tag_name('img').get_attribute('src')
    processImage(novelId, novelLinkImage)
    # ---------------------------------------------------------------------------------------------
    headerStats = novel_info.find_element_by_class_name('header-stats').find_elements_by_tag_name('strong')
    novelTotalChapter = headerStats[0].text
    novelView = headerStats[1].text
    novelView = processView(novelView)
    novelBookmarked = headerStats[2].text
    novelStatusStr = headerStats[3].text
    if novelStatusStr == 'Ongoing':
        novelStatus = 0
    else:
        novelStatus = 1
    # ---------------------------------------------------------------------------------------------
    categories = novel_info.find_element_by_class_name('categories').find_elements_by_tag_name('li')
    novelListCategories = []
    for category in categories:
        novelListCategories.append(category.text)
    # ---------------------------------------------------------------------------------------------
    novelChapterId = 'chapter-' + novelTotalChapter
    novel_body = driver.find_element_by_class_name('novel-body')
    text1row = novel_body.find_element_by_class_name('content-nav').find_elements_by_class_name('text1row')
    novelChapterName = text1row[0].text
    novelVoteCount = text1row[1].text.replace('Reviews from ', '').replace(' readers', '')
    # ---------------------------------------------------------------------------------------------
    info = novel_body.find_element_by_id('info')
    novelContent = info.find_element_by_class_name('summary').find_element_by_class_name('content').text
    # ---------------------------------------------------------------------------------------------
    listTags = info.find_element_by_class_name('tags').find_elements_by_tag_name('li')
    novelListTags = []
    for tag in listTags:
        novelListTags.append(tag.text)
    # print(novelListTags)
    # ---------------------------------------------------------------------------------------------
    driver.close()
    # ---------------------------------------------------------------------------------------------
    crawlerDate = datetime.today().strftime('%Y-%m-%d')
    recentChapter = json.dumps(RecentChapter(novelChapterId, novelChapterName).__dict__)
    firstChapter = json.dumps(FirstChapter('chapter-1', 'chapter-1').__dict__)
    novel = Novel(None, novelBookmarked, novelView, None, novelListCategories, not novelName, novelAuthor, None,
                  novelStatus, novelContent, crawlerDate, novelId, crawlerDate, 0, recentChapter, firstChapter, novelHot, 0,
                  novelTotalChapter, novelVoteCount, float(novelRate)*2, 'novelpub.com', novelVoteCount, novelRate, novelListTags)
    jsonNovel = json.dumps(novel.__dict__)
    print(jsonNovel)


def processView(novelView):
    if 'K' in novelView:
        view = novelView.replace('K', '')
        return int(view) * 1000 + random.randrange(999)
    elif 'M' in novelView:
        view = novelView.replace('M', '')
        return float(view) * 1000000 + random.randrange(999999)
    else:
        return int(novelView)


def processImage(novelId, novelLinkImage):
    pathSaveImageRaw = '../image/novel/' + novelId + '.jpg'
    print(pathSaveImageRaw)
    downloadImage(novelLinkImage, pathSaveImageRaw)
    # ---------------------------------------------------------------------------------------------
    pathSaveImage = '../image/novel_80_113/' + novelId + '.jpg'
    resizeImage(pathSaveImageRaw, 80, 113, pathSaveImage)
    # ---------------------------------------------------------------------------------------------
    pathSaveImage = '../image/novel_150_223/' + novelId + '.jpg'
    resizeImage(pathSaveImageRaw, 150, 223, pathSaveImage)
    # ---------------------------------------------------------------------------------------------
    pathSaveImage = '../image/novel_164_245/' + novelId + '.jpg'
    resizeImage(pathSaveImageRaw, 164, 245, pathSaveImage)
    # ---------------------------------------------------------------------------------------------
    pathSaveImage = '../image/novel_200_89/' + novelId + '.jpg'
    resizeImage(pathSaveImageRaw, 200, 89, pathSaveImage)


def resizeImage(pathSaveImageRaw, width, height, pathSaveImage):
    image = Image.open(pathSaveImageRaw)
    new_image = image.resize((width, height))
    new_image.save(pathSaveImage)


def downloadImage(url, pathSaveImage):
    response = requests.get(url)
    file = open(pathSaveImage, "wb")
    file.write(response.content)
    file.close()
