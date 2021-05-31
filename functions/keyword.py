from utils import log
from jsoncomment import JsonComment

json = JsonComment()
logger = log.get_logger(name = 'Keyword')
word_list = json.loadf('conf/keyword_list.json')

class reply:
    def __init__(self, message) -> None:
        self.type = None
        for word in word_list:
            if word in message:
                self.match = word
                self.type = word_list[word]['type']
                if self.type == "forward":
                    self.from_chat_id = word_list[word]['from_chat_id']
                    self.message_id = word_list[word]['message_id']
                elif self.type == "plaintext":
                    self.text = word_list[word]['text']
                elif self.type == "sticker":
                    self.sticker_id = word_list[word]['sticker_id']
                else:
                    pass
                break