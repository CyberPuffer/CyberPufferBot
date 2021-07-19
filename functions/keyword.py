from utils import log, config

logger = log.get_logger(name = 'Keyword')

class reply:
    def __init__(self, message) -> None:
        self.type = None
        for word in config.word_list:
            if word in message:
                self.match = word
                self.type = config.word_list[word]['type']
                if self.type == "forward":
                    self.from_chat_id = config.word_list[word]['from_chat_id']
                    self.message_id = config.word_list[word]['message_id']
                elif self.type == "plaintext":
                    self.text = config.word_list[word]['text']
                elif self.type == "sticker":
                    self.sticker_id = config.word_list[word]['sticker_id']
                else:
                    pass
                break