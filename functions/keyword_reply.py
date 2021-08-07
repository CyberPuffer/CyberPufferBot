from telegram.ext import MessageHandler, Filters

def keyword_reply(update, context):
    from functions import luck, ganzhi, keyword
    from datetime import datetime
    from utils import messages
    if (update.message is not None):
        reply=[]
        # Special commands detection
        if update.message.text.startswith("/"):
            if update.message.text.startswith("/luck"):
                arg = update.message.text.partition(' ')
                if arg[2] == '':
                    name = update.effective_user.first_name
                    if update.effective_user.last_name is not None:
                        name += update.effective_user.last_name
                else:
                    name = arg[2]
                luck_text = '\n'.join([luck.get_luck(update.effective_user.id, datetime.now()),ganzhi.get_ganzhi(datetime.now())])
                reply.append(context.bot.send_message(chat_id=update.effective_chat.id, text=luck_text))
        result = keyword.reply(update.message.text)
        if result.type is not None:
            # Filter mismatched replys
            if update.message.text.startswith("/") ^ result.match.startswith("/"):
                pass
            elif result.type == 'forward':
                reply.append(context.bot.forward_message(chat_id=update.effective_chat.id, from_chat_id=result.from_chat_id, message_id=result.message_id))
            elif result.type == 'plaintext':
                reply.append(context.bot.send_message(chat_id=update.effective_chat.id, text=result.text))
            elif result.type == 'sticker':
                reply.append(context.bot.send_sticker(chat_id=update.effective_chat.id, sticker=result.sticker_id))
            else:
                pass
        messages.auto_delete(context, reply)
handler = MessageHandler(Filters.text & (~Filters.command) | Filters.regex('^/[luck|lottery|caffeine|caculate]'), keyword_reply)