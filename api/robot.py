from modules.cailianshe.cailianshe import robot as news_robot
from modules.weather_alarm.weather import robot as weather_robot
from utils.config import start_job

def init(args):

    job_list = []

    news_job = start_job(news_robot, args)
    job_list.append(news_job)

    weather_job = start_job(weather_robot, args)
    job_list.append(weather_job)

    return job_list