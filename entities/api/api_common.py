class RequestApi:
    def __init__(self, id, name, page, size):
        self.id = id
        self.name = name
        self.page = page
        self.size = size

class ResponseApi:
    def __init__(self, responseId, data):
        self.responseId = responseId
        self.data = data
