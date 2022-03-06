from utils import config, log, globals
logger = log.get_logger(name = 'CaiLianShe')

def robot(args):
    from requests import session
    from time import time, sleep
    while True:
        try:
            bot = globals.dispatcher.bot
        except:
            logger.warning('Get dispatcher failed, retry after 1s')
            sleep(1)
            continue
        break
    s = session()
    s.headers.update(
    {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.0.0 Safari/537.36 Edg/98.0.0.0'})
    lasttime = int(time())
    while True:
        try:
            update = get_telegraph_update(s, lasttime)
        except:
            continue
        if update['data']['update_num'] == 0:
            sleep(30)
            continue
        for telegraph in update['data']['roll_data']:
            if telegraph['level'] < 'C':
                logger.info(telegraph['level'] + ' ' + telegraph['title'])
                bot.send_message(chat_id=globals.config['cailianshe_channel_id'], text=telegraph['content'])
        lasttime = max([telegraph['ctime'] for telegraph in update['data']['roll_data']])
        sleep(15)

def get_telegraph_update(s,lasttime):
    from hashlib import sha1, md5
    url_base = "https://www.cls.cn/nodeapi/updateTelegraphList?"
    url_args = "app=CailianpressWeb&category=&hasFirstVipArticle=1&lastTime={}&os=web&rn=20&subscribedColumnIds=&sv=7.7.5".format(lasttime)
    sign_step1 = sha1(bytes(url_args,"ascii")).hexdigest()
    sign_step2 = md5(bytes(sign_step1,"ascii")).hexdigest()
    url_sign = "&sign={}".format(sign_step2)
    telegraph_update = s.get(url= url_base + url_args + url_sign).json()
    return telegraph_update