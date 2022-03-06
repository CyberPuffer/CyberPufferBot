from utils import globals

word_list = globals.config['keywords']

class Reply:
    reply_type = None
    from_chat_id = None
    message_id = None
    text = None
    sticker_id = None
    def __init__(self, message):
        for keyword in word_list:
            if keyword['keyword'] in message:
                self.match = keyword['keyword']
                self.reply_type = keyword['type']
                if self.reply_type == "forward":
                    self.from_chat_id = keyword['from_chat_id']
                    self.message_id = keyword['message_id']
                elif self.reply_type == "plaintext":
                    self.text = keyword['text']
                elif self.reply_type == "sticker":
                    self.sticker_id = keyword['sticker_id']
                else:
                    pass
                break