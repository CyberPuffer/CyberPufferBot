from telegram.ext import ChatMemberHandler
from regex import search
from utils import log

logger = log.get_logger(name = 'AntiSpam')

def anti_tgstat_bot(update, context):
    is_join = False
    if 'status' in update.chat_member.difference():
        is_join = update.chat_member.difference()['status'] == ('left', 'member')
    if is_join:
        new_user = update.chat_member.new_chat_member.user
        chat_id = update.chat_member.chat.id
        check1 = bool(search(r'\p{IsCyrillic}', new_user.first_name))
        check2 = bool(search(r'\p{IsCyrillic}', new_user.last_name))
        check3 = new_user.username is None
        if (check1 & check2 & check3):
            context.bot.kick_chat_member(chat_id, new_user.id)
            logger.info("User {user_id} is suspicious and banned.".format(user_id = new_user.id))
        else:
            logger.info("User {user_id} subscribed.".format(user_id = new_user.id))

channel_handler = ChatMemberHandler(anti_tgstat_bot, chat_member_types = 1)