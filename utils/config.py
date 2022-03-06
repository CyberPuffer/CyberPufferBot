def get_config(dispatcher, args):
    from tomli import loads
    channel_info = dispatcher.bot.get_chat(args.config_id)
    if channel_info.pinned_message is None:
        msg = dispatcher.bot.send_message(args.config_id, init_index(),protect_content=True)
        dispatcher.bot.pin_chat_message(args.config_id,msg.message_id,disable_notification=True)
        index = msg
    else:
        index = channel_info.pinned_message
    return loads(index.text)

def init_index():
    from tomli_w import dumps
    index = {
        'version': 0
    }
    return dumps(index)

def set_key():
    pass

def del_key():
    pass

def parse_index():
    pass

def find_message():
    pass