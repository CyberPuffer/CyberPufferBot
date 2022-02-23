# -*- coding: utf-8 -*-
from utils import log
from distutils.version import LooseVersion
from telegram import __version__ as ptb_version
logger = log.get_logger(name = 'AntiSpam')

def anti_tgstat_bot(update, context):
    from re import search
    is_join = False
    if 'status' in update.chat_member.difference():
        is_join = update.chat_member.difference()['status'] == ('left', 'member')
    if is_join:
        new_user = update.chat_member.new_chat_member.user
        chat_id = update.chat_member.chat.id
        check1 = bool(search(u'[а-яА-Я]', new_user.first_name))
        check2 = bool(search(u'[а-яА-Я]', new_user.last_name))
        check3 = new_user.username is None
        if (check1 & check2 & check3):
            context.bot.kick_chat_member(chat_id, new_user.id)
            logger.info("User {user_id} is suspicious and banned.".format(user_id = new_user.id))
        else:
            logger.info("User {user_id} subscribed.".format(user_id = new_user.id))

def get_handler():
    if LooseVersion(ptb_version) < LooseVersion('13.4'):
        logger.error('AntiSpam requires PTB version >= 13.4, current version is {}, please consider upgrade.'.format(ptb_version))
        return None
    else:
        from telegram.ext import ChatMemberHandler
        return ChatMemberHandler(anti_tgstat_bot, chat_member_types = 1)