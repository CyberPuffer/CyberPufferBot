# -*- coding: utf-8 -*-
from telegram.ext import CommandHandler

def stats(update, context):
    from utils import database, messages
    num = database.stats('users')
    text = u"咱总共见过{num}个人啦！".format(num=num)
    reply = [context.bot.send_message(chat_id=update.effective_chat.id, text=text)]
    messages.auto_delete(context, reply)
handler = CommandHandler('stats', stats)