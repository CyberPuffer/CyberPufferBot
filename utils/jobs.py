from utils.log import get_logger

logger = get_logger(name='Jobs')

def start_jobs(args):
    job_status = {}
    # Parse API source
    for api_slice in args.api_list:
        for item in api_slice.split(';'):
            conf = {'config': item.strip(), 'proxy': args.proxy}
            if item.strip().startswith('telegram:'):
                if 'telegram' in job_status.keys():
                    logger.warn('Duplicated Telegram API config detected')
                else:
                    from api.telegram import polling
                    telegram_job = start_job(polling, conf)
                    job_status['telegram'] = telegram_job
            if item.strip().startswith('robot:'):
                if 'robot' in job_status.keys():
                    logger.warn('Duplicated robot API config detected')
                else:
                    from api.robot import polling
                    robot_job = start_job(polling, conf)
                    job_status['robot'] = robot_job

def start_job(target, args):
    from threading import Thread
    t = Thread(target=target, args=[args])
    t.start()
    return t