def main():
    from argparse import ArgumentParser
    from os import environ
    parser = ArgumentParser(
        prog='CyberPuffer', description='CyberPuffer - Just yet another telegram bot')
    parser.add_argument('--secret', '-s', dest='api_secret')
    parser.add_argument('--config', '-c', dest='config_id')
    parser.add_argument('--proxy', '-x', dest='proxy')
    parser.add_argument('--verbose', '-v', dest='verbose', action='store_true')
    parser.add_argument('--version', action='version', version='%(prog)s 2.0')
    args = parser.parse_args()
    if args.api_secret is None:
        try:
            args.api_secret = environ['API_SECRET']
        except KeyError:
            raise ValueError('Telegram API secret not specific')
    if args.config_id is None:
        try:
            args.config_id = environ['CONFIG_ID']
        except KeyError:
            raise ValueError('Config channel id not specific')
    start_all_jobs(args)

def start_all_jobs(args):
    from utils.polling import polling
    from modules.cailianshe.cailianshe import robot as news_robot
    from modules.weather_alarm.weather import robot as weather_robot
    telegram_job = start_job(polling, args)
    news_job = start_job(news_robot, args)
    weather_job = start_job(weather_robot, args)
    return

def start_job(target, args):
    from threading import Thread
    t = Thread(target=target, args=[args])
    t.start()
    return t

if __name__ == "__main__":
    main()