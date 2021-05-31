from telegram.ext import CommandHandler
from time import monotonic
from utils import database, globals

def stats(update, context):
    global time_start
    num = database.stats('users')
    time_now = monotonic() 
    text = "咱已经正常运行了{time}秒，咱总共见过{num}个人啦".format(time=int(time_now - globals.time_start), num=num)
    context.bot.send_message(chat_id=update.effective_chat.id, text=text)
stats_handler = CommandHandler('stats', stats)