class Novel:
    def __init__(self, id, followCount, view, novel_author_cn, novel_genres, novel_name, novel_author, novel_other_name,
                 novel_status, novel_desc, crawler_date, novel_id, created_date, __v, recentChapter, firstChapter, hot,
                 new, totalChapter, voteCountType2, avgPointType2, novel_source, voteCount, avgPoint, list_tag):
        self.id = id
        self.followCount = followCount
        self.view = view
        self.novel_author_cn = novel_author_cn
        self.novel_genres = novel_genres
        self.novel_name = novel_name
        self.novel_author = novel_author
        self.novel_other_name = novel_other_name
        self.novel_status = novel_status
        self.novel_desc = novel_desc
        self.crawler_date = crawler_date
        self.novel_id = novel_id
        self.created_date = created_date
        self.__v = __v
        self.recentChapter = recentChapter
        self.firstChapter = firstChapter
        self.hot = hot
        self.new = new
        self.totalChapter = totalChapter
        self.voteCountType2 = voteCountType2
        self.avgPointType2 = avgPointType2
        self.novel_source = novel_source
        self.voteCount = voteCount
        self.avgPoint = avgPoint
        self.list_tag = list_tag


class FirstChapter:
    def __init__(self, chapter_id, chapter_name):
        self.chapter_id = chapter_id
        self.chapter_name = chapter_name


class RecentChapter:
    def __init__(self, chapter_id, chapter_name):
        self.chapter_id = chapter_id
        self.chapter_name = chapter_name
