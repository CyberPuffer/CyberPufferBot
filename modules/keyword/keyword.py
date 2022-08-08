from utils.global_vars import message_handler

def keyword(message, sender):
    word_list = message_handler[sender['source']]['config']['keywords']
    for keyword in word_list:
        if keyword['keyword'] in message:
            recevier = sender
            recevier['type'] = keyword['type']
            return keyword['content'], recevier