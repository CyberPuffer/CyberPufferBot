def delete_message(context):
    context.bot.delete_message(context.job.context['chat_id'], context.job.context['message_id'])

def auto_delete(context, reply):
    from utils import globals, config
    timeout = config.auto_delete_timer
    if timeout > 0 and globals.webhook == False:
        for message in reply:
            context.job_queue.run_once(delete_message, timeout, context={'chat_id': message.chat_id, 'message_id': message.message_id})
    else:
        pass