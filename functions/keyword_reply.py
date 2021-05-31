from telegram.ext import MessageHandler, Filters
from functions import luck, keyword
from utils import database
from datetime import date

def keyword_reply(update, context):
    if (update.message is not None):
        database.query(update.effective_user.id, 'role')
        # Special commands detection
        if update.message.text.startswith("/"):
            if update.message.text.startswith("/luck"):
                luck_text = luck.get_luck(update.effective_user.id, date.today())
                context.bot.send_message(chat_id=update.effective_chat.id, text=luck_text)
        reply = keyword.reply(update.message.text)
        if reply.type is not None:
            # Filter mismatched replys
            if update.message.text.startswith("/") ^ reply.match.startswith("/"):
                return
            if reply.type == 'forward':
                context.bot.forward_message(chat_id=update.effective_chat.id, from_chat_id=reply.from_chat_id, message_id=reply.message_id)
            elif reply.type == 'plaintext':
                context.bot.send_message(chat_id=update.effective_chat.id, text=reply.text)
            elif reply.type == 'sticker':
                context.bot.send_sticker(chat_id=update.effective_chat.id, sticker=reply.sticker_id)
            else:
                pass
keyword_handler = MessageHandler(Filters.text & (~Filters.command) | Filters.regex('^/[luck|lottery|caffeine|caculate]'), keyword_reply)