from utils.log import get_logger
from utils.global_vars import message_handler
from traceback import print_exc
from datetime import datetime

logger = get_logger(name='财联社')

def get_url(lasttime):
    from hashlib import sha1, md5
    url_base = "https://www.cls.cn/nodeapi/updateTelegraphList?"
    url_args = "app=CailianpressWeb&category=&hasFirstVipArticle=1&lastTime={}&os=web&rn=20&subscribedColumnIds=&sv=7.7.5".format(lasttime)
    sign_step1 = sha1(bytes(url_args,"ascii")).hexdigest()
    sign_step2 = md5(bytes(sign_step1,"ascii")).hexdigest()
    url_sign = "&sign={}".format(sign_step2)
    return url_base + url_args + url_sign

def parse_data(data, robot):
    try:
        logger.debug('Current lasttime is ' + str(datetime.fromtimestamp(robot['lasttime'])))
        update = data.json()
        for handler in message_handler.values():
            sender = handler['sender']
            config = handler['config']
            receiver = {"user_id": int(config['cailianshe_channel_id'])}
            for telegraph in update['data']['roll_data']:
                if telegraph['level'] < 'C':
                    sender(telegraph['content'], receiver)
                    pass
        ctime_list = [telegraph['ctime'] for telegraph in update['data']['roll_data']]
        if len(ctime_list) > 0:
            robot['lasttime'] = max(ctime_list)
            logger.debug('Change lasttime to ' + str(datetime.fromtimestamp(robot['lasttime'])))
        else:
            pass
    except:
        print_exc()