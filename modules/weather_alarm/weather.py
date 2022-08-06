from utils import config, log, global_vars
logger = log.get_logger(name = 'WeatherAlarm')

def robot(args):
    from requests import session
    from datetime import datetime, timedelta
    from time import sleep
    while True:
        try:
            bot = global_vars.dispatcher.bot
        except:
            logger.warning('Get dispatcher failed, retry after 1s')
            sleep(1)
            continue
        break
    s = session()
    s.headers.update(
    {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.0.0 Safari/537.36 Edg/98.0.0.0'})
    test_delta = timedelta(hours=0)
    lasttime = datetime.now()-test_delta
    url_base = "http://weather.cma.cn/api/map/alarm?adcode="
    while True:
        try:
            alarm_list = s.get(url= url_base).json()
        except:
            continue
        time_list = []
        for alarm in alarm_list['data']:
            geocode, alarm_time = alarm['id'].split('_')
            date_fmt="%Y%m%d%H%M%S"
            alarm_time = datetime.strptime(alarm_time,date_fmt)
            time_list.append(alarm_time)
            if alarm_time > lasttime:
                try:
                    msg = bot.send_message(chat_id=global_vars.telegram_config['weather_channel_id'], text=alarm['description'])
                except:
                    sleep(30)
                    msg = bot.send_message(chat_id=global_vars.telegram_config['weather_channel_id'], text=alarm['description'])
           # notify_user(geocode, msg)
        lasttime = max(time_list)
        sleep(60)