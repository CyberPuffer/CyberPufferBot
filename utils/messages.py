def delete_message(context):
    context.bot.delete_message(context.job.context['chat_id'], context.job.context['message_id'])

def delete_message_webhook(context, message):
    context.bot.delete_message(chat_id=message.chat_id,message_id=message.message_id)

def auto_delete(context, reply):
    from utils import globals, config
    from threading import Timer
    timeout = config.auto_delete_timer
    if timeout > 0:
        for message in reply:
            if globals.webhook == True:
                delete_timer=Timer(timeout, delete_message_webhook, [context, message])
                delete_timer.start()
                delete_timer.join()
            else:
                context.job_queue.run_once(delete_message, timeout, context={'chat_id': message.chat_id, 'message_id': message.message_id})

    else:
        pass