from os import path, environ
from json import load, loads

word_list = None
word_list_path = path.join(path.dirname(__file__), 'keyword_list.json')
if (path.exists(word_list_path)):
    with open(word_list_path, "r",encoding="utf-8") as fp:
        word_list = load(fp)

class Reply:
    reply_type = None
    from_chat_id = None
    message_id = None
    text = None
    sticker_id = None
    def __init__(self, message):
        from utils import config
        for word in word_list:
            if word in message:
                self.match = word
                self.reply_type = word_list[word]['type']
                if self.reply_type == "forward":
                    self.from_chat_id = word_list[word]['from_chat_id']
                    self.message_id = word_list[word]['message_id']
                elif self.reply_type == "plaintext":
                    self.text = word_list[word]['text']
                elif self.reply_type == "sticker":
                    self.sticker_id = word_list[word]['sticker_id']
                else:
                    pass
                break