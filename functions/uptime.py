# -*- coding: utf-8 -*-
from telegram.ext import CommandHandler
from utils import globals
from humanfriendly import format_timespan
try:
    from time import monotonic
except ImportError:
    from time import clock as monotonic

def uptime(update, context):
    time_now = monotonic() 
    time_text = format_timespan(int(time_now - globals.time_start))\
        .replace('years',u'年').replace('year',u'年')\
        .replace('months',u'个月').replace('month',u'个月')\
        .replace('weeks',u'周').replace('week',u'周')\
        .replace('days',u'日').replace('day',u'日')\
        .replace('hours',u'小时').replace('hour',u'小时')\
        .replace('minutes',u'分').replace('minute',u'分')\
        .replace('seconds',u'秒').replace('second',u'秒')\
        .replace('and ','').replace(',','')
    text = u"咱已经正常运行了 {}".format(time_text)
    context.bot.send_message(chat_id=update.effective_chat.id, text=text)
uptime_handler = CommandHandler('uptime', uptime)