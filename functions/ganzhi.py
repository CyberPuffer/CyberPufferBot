# -*- coding: utf-8 -*-
from functions.zhdate import ZhDate
from datetime import datetime

def get_ganzhi(date):

    gans = u'甲乙丙丁戊己庚辛壬癸'
    zhis = u'子丑寅卯辰巳午未申酉戌亥'

    lunar_date = ZhDate.from_datetime(date)
    year_gan = (lunar_date.lunar_year - 4) % 10
    year_zhi = (lunar_date.lunar_year - 4) % 12
    month_gan = (year_gan * 2 + lunar_date.lunar_month + 1) % 10
    month_zhi = (lunar_date.lunar_month + 1) % 12
    day_gan = (date - datetime(1970,2,13)).days % 10
    day_zhi = (date - datetime(1970,2,13)).days % 12
    hour_zhi = (date.hour + 1) // 2 % 12
    hour_gan = ((day_gan) % 5 * 2 + hour_zhi) % 10

    ganzhi_text = u'当前干支：{}{}年 {}{}月 {}{}日 {}{}时'.format(
    gans[year_gan],zhis[year_zhi],gans[month_gan],zhis[month_zhi],gans[day_gan],zhis[day_zhi],gans[hour_gan],zhis[hour_zhi])

    return ganzhi_text