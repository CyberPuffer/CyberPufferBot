def delete_message(context):
    context.bot.delete_message(context.job.context['chat_id'], context.job.context['message_id'])
def auto_delete(context, reply):
    from utils import config
    timer = config.auto_delete_timer
    if timer > 0:
        for message in reply:
            context.job_queue.run_once(delete_message, timer, context={'chat_id': message.chat_id, 'message_id': message.message_id})
    else:
        pass