from telegram.ext import MessageHandler, Filters
from base64 import b64encode
from utils import globals

def quick_check(update):
    # Filter blank message
    if update.message is None:
        return True
    # Check debug command
    dbg_sig = b64encode(bytes(globals.config['debug_signature'],'UTF-8'), altchars=b'-_').decode('ASCII')
    if dbg_sig in update.message.text:
        return True
    if not update.message.text.startswith("/"):
        return False
    else:
        # TODO: need to dispatch commands here
        pass
        return True

def keyword(update, context):
    if quick_check(update):
        return
    # from utils import messages
    from .reply import Reply
    if (update.message is not None):
        reply=[]
        result = Reply(update.message.text)
        if result.reply_type is not None:
            # Filter mismatched replys
            if update.message.text.startswith("/") ^ result.match.startswith("/"):
                pass
            elif result.reply_type == 'forward':
                reply.append(context.bot.forward_message(chat_id=update.effective_chat.id, from_chat_id=result.from_chat_id, message_id=result.message_id))
            elif result.reply_type == 'plaintext':
                reply.append(context.bot.send_message(chat_id=update.effective_chat.id, text=result.text))
            elif result.reply_type == 'sticker':
                reply.append(context.bot.send_sticker(chat_id=update.effective_chat.id, sticker=result.sticker_id))
            else:
                pass
        # messages.auto_delete(context, reply)

def get_handler():
    if len(globals.global_commands) == 0:
        return MessageHandler(Filters.text & (~Filters.command), keyword)
    else:
        cmd_regex = '|'.join(['^/'+ c for c in globals.global_commands])
        return MessageHandler(Filters.text & (~Filters.command) | Filters.regex(cmd_regex), keyword)