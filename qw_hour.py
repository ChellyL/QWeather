# encoding=utf-8
# -- coding:utf-8 --

import datetime
import time
import telegram
import requests

# 你的tg 信息：
token = ''
userid = ''

date = str(datetime.datetime.now())[:4] + str(datetime.datetime.now())[5:7] + str(datetime.datetime.now())[8:10]
key = '' # 建议申请专业开发者的
place = ''

location = 'https://geoapi.qweather.com/v2/city/lookup?location=anzhou&key=' + key

now = 'https://devapi.qweather.com/v7/weather/now?key=' + key + '&location=' + place
life = 'https://devapi.qweather.com/v7/indices/1d?type=0&key=' + key + '&location=' + place
warning = 'https://devapi.qweather.com/v7/warning/now?key=' + key + '&location=' + place
air = 'https://devapi.qweather.com/v7/air/now?key=' + key + '&location=' + place
sun = 'https://devapi.qweather.com/v7/astronomy/sun?key=' + key + '&location=' + place + '&date=' + date
hour = 'https://devapi.qweather.com/v7/weather/24h?key=' + key + '&location=' + place
days = 'https://devapi.qweather.com/v7/weather/3d?key=' + key + '&location=' + place
htkt = 'https://international.v1.hitokoto.cn/'

# 地点
def locate():
    city = requests.get(location).json()
    name = city['location'][0]['name']
    adm = city['location'][0]['adm2']
    where = '📍 ' + adm + ' ' + name
    return where

# 空气质量
def air_index():
    now_air = requests.get(air).json()
    air_aqi = now_air['now']['aqi']
    air_text = now_air['now']['category']
    air_pm25 = now_air['now']['pm2p5']
    air_id = '空气指数: ' + air_aqi + ' ' + air_text + ' PM2.5: ' + air_pm25
    return air_id

# 天气预警
def now_warning():
    warn = requests.get(warning).json()
    if len(warn['warning']) == 0:
        warn_msg = '🎉 无异常天气发生！请继续努力发财！记得喝水提肛！'
    else:
        title = warn['warning'][0]['title']
        text = warn['warning'][0]['text']
        warn_msg = title + '\n' + text + '\n'
    return warn_msg

# 当时天气
def now_wt():
    now_weather = requests.get(now).json()
    now_time = now_weather['now']['obsTime'][:10] + ' ' + now_weather['now']['obsTime'][11:16]
    # now_time = str(datetime.datetime.now().hour) + ':' + str(datetime.datetime.now().minute).zfill(2)
    now_temp = now_weather['now']['temp']
    now_des = now_weather['now']['text']
    now_wind = now_weather['now']['windDir']
    now_windscale = now_weather['now']['windScale']
    now_wt = now_time + ' 测定\n现在为 ' + now_temp + '℃ ' + now_des + ' ' + now_wind + ' ' + now_windscale + '级'
    return now_wt

# 天气预报网页
def wt_link():
    now_weather = requests.get(now).json()
    link = now_weather['fxLink']
    return link

# 此后6小时天气
def hour1():
    list = []
    for i in range(6):
        hours = requests.get(hour).json()
        hour_time = hours['hourly'][i]['fxTime'][11:16]
        hour_text = hours['hourly'][i]['text']
        hour_temp = hours['hourly'][i]['temp']
        hour_wind = hours['hourly'][i]['windDir']
        hour_windsc = hours['hourly'][i]['windScale']
        hour_weather = hour_time + ' ' + hour_temp + '℃ ' + hour_text + ' ' + hour_wind + ' ' + hour_windsc + '级'

        list.append(hour_weather)
        six = '\n'.join(list)
    return six

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


# 国内设备需要代理才能推送
# import os

# os.environ['http_proxy'] = 'http://127.0.0.1:7890'
# os.environ['https_proxy'] = 'https://127.0.0.1:7890'

# 推送样式
word = locate() + '\n🌡️ 小时播报\n\n' + now_wt() + ' ' + air_index() + '\n\n' + now_warning() + '\n\n☃️ 未来6小时天气:\n' + hour1() + '\n\n' + ichiba() + '\n\n' + '<a href="' + wt_link() + '">info</a>'


bot = telegram.Bot(token)
bot.send_message(chat_id=userid, text=word, parse_mode=telegram.ParseMode.HTML)
