# -*- coding: utf-8 -*-
from telegram.ext import CommandHandler

def get_weibo_hotlist():
    from requests import session
    s = session()
    s.headers.update(
        {'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.0 Mobile/14E304 Safari/602.1'})
    weibo_hot_json = s.get(
        url='https://m.weibo.cn/api/container/getIndex?containerid=106003type%3D25%26t%3D3%26disable_hot%3D1%26filter_type%3Drealtimehot&title=热搜榜&extparam=').json()
    return [{'title': item['desc'],
             'score':item['desc_extr'] if 'desc_extr' in item else None}
            for item in weibo_hot_json['data']['cards'][0]['card_group']]

def format_weibo_hotlist(hotlist, list_type='hot', num=None):
    text = '微博实时热搜榜\n'
    counter = 0
    for item in hotlist:
        bad_item = True if item['score'] is None else False
        text += '{rank}. {title}\n'.format(rank = str(counter+1) if not bad_item else '#', title = item['title'])
        if not bad_item:
            counter += 1
        if counter == num:
            break
    return text

def weibo(update, context):
    # from utils import messages
    if len(context.args) == 0:
        num = 10
    else:
        try:
            num = int(context.args[0])
        except ValueError:
            if context.args[0] == 'all':
                num = None

    hotlist = get_weibo_hotlist()
    hotlist_text = format_weibo_hotlist(hotlist,num=num)
    reply = [context.bot.send_message(chat_id=update.effective_chat.id, text=hotlist_text)]
    # messages.auto_delete(context, reply)

def get_handler():
    return CommandHandler('weibo', weibo)