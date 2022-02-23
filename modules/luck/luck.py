# -*- coding: utf-8 -*-
from telegram.ext import CommandHandler

def get_luck(uid, date):
    from binascii import crc32, unhexlify
    seed = uid + date.year + date.month + date.day + (date.hour + 1) // 2
    width = seed.bit_length()
    width += 8 - ((width % 8) or 8)
    fmt = '%%0%dx' % (width // 4)
    s = unhexlify(fmt % seed)
    luck_level = crc32(s) % 5 + 1
    luck_text = u'当前人品：{}{}'.format(u'★' * luck_level, u'☆' * (5 - luck_level))
    return luck_text

def luck(update, context):
    from utils import messages
    from datetime import datetime
    from .ganzhi import get_ganzhi
    luck_text = '\n'.join([get_luck(update.effective_user.id, datetime.now()),get_ganzhi(datetime.now())])
    reply = [context.bot.send_message(chat_id=update.effective_chat.id, text=luck_text)]
    messages.auto_delete(context, reply)

def register_global_command(name):
    from utils import globals
    if name in globals.global_commands:
        return True
    else:
        globals.global_commands.append(name)
        return False

def get_handler():
    if not register_global_command('luck'):
        return CommandHandler('luck', luck), {'reload':['keyword']}
    else:
        return CommandHandler('luck', luck)