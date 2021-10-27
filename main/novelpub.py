from process import crawl_latest, crawl_novel

# Crawl dữ liệu latest
listUrlNovels = []
listUrlChapters = []
for x in range(1, 3):
    url = 'https://www.novelpub.com/latest-updates?p='+ str(x)
    # print(url)
    crawl_latest.process(url, listUrlNovels, listUrlChapters)
    break
# print(len(listUrlNovels))
# print(len(listUrlChapters))
# Crawl dữ liệu novel
for urlNovel in listUrlNovels:
    print(urlNovel)
    crawl_novel.process(urlNovel)
    break

# soup = BeautifulSoup(source, 'lxml')
# print(soup)