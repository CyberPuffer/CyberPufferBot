from requests import session
from time import time, sleep
from utils.global_vars import message_handler
from utils.log import get_logger
from traceback import print_exc
from itertools import starmap
import asyncio

logger = get_logger(name='Robot')

def polling(args):

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    s = session()
    s.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.0.0 Safari/537.36 Edg/98.0.0.0'})
    lasttime = int(time())
    robot_config = ''
    robot_list = []
    config_list = []

    for i in range(10):
        try:
            config_list = [handler['config'] for handler in message_handler.values()]
        except KeyError:
            logger.warn("Get robot list failed, retry after 3s")
            sleep(3)

    for config in config_list:
        if 'enabled_robots' in config.keys():
            robot_config = config['enabled_robots']

    # Load all robots configs
    for name in [n.strip() for n in robot_config.split(',')]:
        try:
            robot = __import__('modules.{name}.{name}'.format(name=name))
            robot_url = getattr(getattr(robot, name), name).get_url
            robot_handler = getattr(getattr(robot, name), name).parse_data
            robot_list.append({
                'name': name,
                'url': robot_url,
                'handler': robot_handler,
                'lasttime': lasttime
                })
        except:
            logger.warning('Robot {} failed to load'.format(name))
            print_exc()
    loop.run_until_complete(fetch_job(s,robot_list))

def periodic(period):
    def scheduler(fn):
        async def wrapper(*args, **kwargs):
            while True:
                asyncio.create_task(fn(*args, **kwargs))
                await asyncio.sleep(period)
        return wrapper
    return scheduler

@periodic(10)
async def fetch_job(s, robot_list):
    arg_map = [(s, robot) for robot in robot_list]
    tasks = starmap(handle_data, arg_map)
    await asyncio.gather(*tasks)

async def handle_data(s, robot):
    url = robot['url'](robot['lasttime'])
    logger.debug('Fetch: ' + url)
    data = s.get(url=url, timeout=3)
    result = robot['handler'](data, robot)
    return result