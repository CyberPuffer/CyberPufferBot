from utils.log import get_logger
from traceback import print_exc

logger = get_logger(name='气象预警')

def get_url(lasttime):
    return "http://weather.cma.cn/api/map/alarm?adcode="

def parse_data(data, robot):
    from utils.global_vars import message_handler
    from datetime import datetime
    try:
        if isinstance(robot['lasttime'], int):
            robot['lasttime'] = datetime.fromtimestamp(robot['lasttime'])
        logger.debug('Current lasttime is ' + str(robot['lasttime']))
        alarm_list = data.json()
        time_list = []
        for alarm in alarm_list['data']:
            geocode, alarm_time = alarm['id'].split('_')
            date_fmt="%Y%m%d%H%M%S"
            alarm_time = datetime.strptime(alarm_time,date_fmt)
            time_list.append(alarm_time)
            if alarm_time > robot['lasttime']:
                for handler in message_handler:
                    sender = handler['sender']
                    config = handler['config']
                    receiver = {"user_id": int(config['weather_channel_id'])}
                    sender(alarm['description'],receiver)
        robot['lasttime'] = max(time_list)
        logger.debug('Change lasttime to ' + str(robot['lasttime']))
    except:
        print_exc()