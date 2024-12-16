# encoding=utf-8
# -- coding:utf-8 --

import datetime
import time
import sxtwl
import requests
import telegram
# python-telegram-bot == 13.7

# tg信息
token = ''
userid = ''

key = '' # 个人申请的key，专业版比较好
place = '' # 所在地点

header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}

date = str(datetime.datetime.now())[:4] + str(datetime.datetime.now())[5:7] + str(datetime.datetime.now())[8:10]

location = 'https://geoapi.qweather.com/v2/city/lookup?location=anzhou&key=' + key

now = 'https://devapi.qweather.com/v7/weather/now?key=' + key + '&location=' + place
life = 'https://devapi.qweather.com/v7/indices/1d?type=0&key=' + key + '&location=' + place
warning = 'https://devapi.qweather.com/v7/warning/now?key=' + key + '&location=' + place
air = 'https://devapi.qweather.com/v7/air/now?key=' + key + '&location=' + place
sun = 'https://devapi.qweather.com/v7/astronomy/sun?key=' + key + '&location=' + place + '&date=' + date
hour = 'https://devapi.qweather.com/v7/weather/24h?key=' + key + '&location=' + place
days = 'https://devapi.qweather.com/v7/weather/3d?key=' + key + '&location=' + place
htkt = 'https://international.v1.hitokoto.cn/?c=a&c=b&c=c&c=d&c=h&c=i&c=k'

Gan = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
Zhi = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
ShX = ["鼠", "牛", "虎", "兔", "龙", "蛇", "马", "羊", "猴", "鸡", "狗", "猪"]
numCn = ["零", "一", "二", "三", "四", "五", "六", "七", "八", "九", "十"]
jqmc = ["冬至", "小寒", "大寒", "立春", "雨水", "惊蛰", "春分", "清明", "谷雨", "立夏",
        "小满", "芒种", "夏至", "小暑", "大暑", "立秋", "处暑", "白露", "秋分", "寒露", "霜降",
        "立冬", "小雪", "大雪"]
ymc = ["正", "二", "三", "四", "五", "六", "七", "八", "九", "十", "冬", "腊"]
rmc = ["初一", "初二", "初三", "初四", "初五", "初六", "初七", "初八", "初九", "初十",
       "十一", "十二", "十三", "十四", "十五", "十六", "十七", "十八", "十九", "二十",
       "廿一", "廿二", "廿三", "廿四", "廿五", "廿六", "廿七", "廿八", "廿九", "三十", "卅一"]
XiZ = ['♑️摩羯', '♒️水瓶', '♓️双鱼', '♈️白羊', '♉️金牛', '♊️双子', '♋️巨蟹', '♌️狮子', '♍️处女', '♎️天秤', '♏️天蝎', '♐️射手']
WeekCn = ["星期日", "星期一", "星期二", "星期三", "星期四", "星期五", "星期六"]
moon = {'新月': '🌑', '峨眉月': '🌒', '上弦月': '🌓', '盈凸月': '🌔', '满月': '🌕', '亏凸月': '🌖', '下弦月': '🌗',
        '残月': '🌘'}
lunar = sxtwl.fromSolar(int(datetime.datetime.fromtimestamp(time.time()).year),
                        int(datetime.datetime.fromtimestamp(time.time()).month),
                        int(datetime.datetime.fromtimestamp(time.time()).day))

today = requests.get(days, headers=header).json()

# 地点
def locate():
    city = requests.get(location).json()
    name = city['location'][0]['name']
    adm = city['location'][0]['adm2']
    where = '📍 ' + adm + ' ' + name
    return where

# 农历
def lunar_td(day):
    yTG = day.getYearGZ(True)
    week = WeekCn[day.getWeek()]
    star = XiZ[day.getConstellation()]
    dTG = day.getDayGZ()
    ganzhi = Gan[yTG.tg] + Zhi[yTG.dz]
    #  lunardate = "%s%d月%d日" % ('闰' if day.isLunarLeap() else '', day.getLunarMonth(), day.getLunarDay())
    if day.isLunarLeap():
        lunardate = '闰' + ymc[day.getLunarMonth() - 1] + '月' + rmc[day.getLunarDay() - 1]
    else:
        lunardate = ymc[day.getLunarMonth() - 1] + '月' + rmc[day.getLunarDay() - 1]
    shengxiao = ShX[yTG.dz]
    if day.hasJieQi():
        jd = day.getJieQiJD()
        t = sxtwl.JD2DD(jd)
        return (week + ' ' + star + '座 ' + '\n' + ganzhi + '(' + shengxiao + ')年 ' + lunardate + '(' + Gan[dTG.tg] + Zhi[dTG.dz] + ') ' + '%s' % jqmc[
            day.getJieQi()] + '' + "(%d-%d-%d %d:%d:%d)" % (t.Y, t.M, t.D, t.h, t.m, round(t.s)))
    else:
        return week + ' ' + star + '座 ' + '\n' + ganzhi + '(' + shengxiao + ')年 ' + lunardate + '(' + Gan[dTG.tg] + Zhi[dTG.dz] + ') '

# 今日天气
def today_wt():
    td_max = today['daily'][0]['tempMax']
    td_min = today['daily'][0]['tempMin']
    td_day = today['daily'][0]['textDay']
    td_night = today['daily'][0]['textNight']
    td_sunset = today['daily'][0]['sunset']
    td_sunrise = today['daily'][0]['sunrise']
    td_moonset = today['daily'][0]['moonset']
    td_moonrise = today['daily'][0]['moonrise']
    td_moon = today['daily'][0]['moonPhase']
    td_wind = today['daily'][0]['windDirDay']
    td_winds = today['daily'][0]['windScaleDay']
    td_uv = today['daily'][0]['uvIndex']
    td = '白天' + td_day + ' 夜间' + td_night + ' ' + td_max + '°~' + td_min + '° ' + '紫外线' + td_uv + '级 ' + td_wind + td_winds + '级\n' + '☀ ' + td_sunrise + '~' + td_sunset + ' ' + \
         moon[td_moon] + td_moonrise + '~' + td_moonset  # td_moonrise + '~' + td_moonset + ' ' + td_moon
    return td

# 明日天气
def tomorrow_wt():
    # tomorrow = requests.get(days,headers=header).json()
    tm_date = today['daily'][1]['fxDate']
    tm_max = today['daily'][1]['tempMax']
    tm_min = today['daily'][1]['tempMin']
    tm_day = today['daily'][1]['textDay']
    tm_night = today['daily'][1]['textNight']
    tm_sunset = today['daily'][1]['sunset']
    tm_sunrise = today['daily'][1]['sunrise']
    tm_moonset = today['daily'][1]['moonset']
    tm_moonrise = today['daily'][1]['moonrise']
    tm_moon = today['daily'][1]['moonPhase']
    tm_wind = today['daily'][1]['windDirDay']
    tm_winds = today['daily'][1]['windScaleDay']
    tm_uv = today['daily'][1]['uvIndex']
    tm = '明天是 ' + tm_date + '\n白天' + tm_day + ' 夜间' + tm_night + ' ' + tm_max + '°~' + tm_min + '° ' + '紫外线' + tm_uv + '级 ' + tm_wind + tm_winds + '级\n' + '☀ ' + tm_sunrise + '~' + tm_sunset + ' ' + \
         moon[tm_moon] + tm_moonrise + '~' + tm_moonset  # tm_moonrise + '~' + tm_moonset + ' ' + tm_moon
    return tm

# 生活指数
def life_index():
    life_index = requests.get(life).json()
    living = life_index['daily'][7]['text']
    return living

# 预报网页
def wt_link():
    now_weather = requests.get(now).json()
    link = now_weather['fxLink']
    return link
  
# 一言
def ichiba():
    hito = requests.get(htkt).json()
    hitokoto = hito['hitokoto']
    author = hito['from_who']
    source = hito['from']

    if source is not None and author is not None:
        sentence = '『 ' + hitokoto + ' 』 ——' + author + '「' + source + '」'
    elif source is not None:
        sentence = '『 ' + hitokoto + ' 』 ——' + '「' + source + '」'
    elif author is not None:
        sentence = '『 ' + hitokoto + ' 』 ——' + author + ' '
    return sentence

# 国内推送需代理
# import os

# os.environ['http_proxy'] = 'http://127.0.0.1:7890'
# os.environ['https_proxy'] = 'https://127.0.0.1:7890'

# 推送样式
daily = locate() + '\n🛰️ 每日播报\n\n' + '今天是 ' + today['daily'][0]['fxDate'] + ' ' + lunar_td(
    lunar) + '\n' + today_wt() + '\n' + life_index() + '\n\n' + tomorrow_wt() + '\n\n' + ichiba() + '\n\n' + '<a href="' + wt_link() + '">info</a>'

bot = telegram.Bot(token)
bot.sendMessage(chat_id=userid, text=daily, parse_mode=telegram.ParseMode.HTML)
