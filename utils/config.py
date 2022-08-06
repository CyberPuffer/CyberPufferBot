def start_jobs(args):
    job_status = {}
    # Parse API source
    for api_slice in args.api_list:
        for item in api_slice.split(';'):
            if item.strip().startswith('telegram:'):
                if 'telegram' in job_status.keys():
                    raise RuntimeWarning('Duplicated API config detected')
                else:
                    conf = {
                        'config': item.strip(),
                        'proxy': args.proxy,
                        'verbose': args.verbose
                        }
                    from api.telegram import polling
                    telegram_job = start_job(polling, conf)
                    job_status['telegram'] = telegram_job
            if item.strip().startswith('robot:'):
                if 'robot' in job_status.keys():
                    raise RuntimeWarning('Duplicated API config detected')
                else:
                    conf = {
                        'config': item.strip(),
                        'proxy': args.proxy,
                        'verbose': args.verbose
                        }
                    from api.robot import init
                    robot_job = start_job(init, conf)
                    job_status['robot'] = robot_job
    return

def start_job(target, args):
    from threading import Thread
    t = Thread(target=target, args=[args])
    t.start()
    return t