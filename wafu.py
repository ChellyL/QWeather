import datetime
import time
import sxtwl
import requests

date = str(datetime.datetime.now())[:4] + str(datetime.datetime.now())[5:7] + str(datetime.datetime.now())[8:10]
key = '' # 你自己的api，建议申请个人开发者，否则无法获取逐时天气预报
place = '101270411' #你所在城市的代码，查看api文档获取，或者打开和风天气你所在地的天气首页，拼音后的一串数字就是城市代码

location = 'https://geoapi.qweather.com/v2/city/lookup?key=' + key + '&location=' + place
now = 'https://devapi.qweather.com/v7/weather/now?key=' + key + '&location=' + place
life = 'https://devapi.qweather.com/v7/indices/1d?type=0&key=' + key + '&location=' + place
warning = 'https://devapi.qweather.com/v7/warning/now?key=' + key + '&location=' + place
air = 'https://devapi.qweather.com/v7/air/now?key=' + key + '&location=' + place
sun = 'https://devapi.qweather.com/v7/astronomy/sun?key=' + key + '&location=' + place + '&date=' + date
hour = 'https://devapi.qweather.com/v7/weather/24h?key=' + key + '&location=' + place
days = 'https://devapi.qweather.com/v7/weather/3d?key=' + key + '&location=' + place

Gan = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
Zhi = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
ShX = ["鼠", "牛", "虎", "兔", "龙", "蛇", "马", "羊", "猴", "鸡", "狗", "猪"]
numCn = ["零", "一", "二", "三", "四", "五", "六", "七", "八", "九", "十"]
jqmc = ["冬至", "小寒", "大寒", "立春", "雨水", "惊蛰", "春分", "清明", "谷雨", "立夏",
        "小满", "芒种", "夏至", "小暑", "大暑", "立秋", "处暑", "白露", "秋分", "寒露", "霜降",
        "立冬", "小雪", "大雪"]
ymc = ["十一", "十二", "正", "二", "三", "四", "五", "六", "七", "八", "九", "十"]
rmc = ["初一", "初二", "初三", "初四", "初五", "初六", "初七", "初八", "初九", "初十",
       "十一", "十二", "十三", "十四", "十五", "十六", "十七", "十八", "十九", "二十",
       "廿一", "廿二", "廿三", "廿四", "廿五", "廿六", "廿七", "廿八", "廿九", "三十", "卅一"]
XiZ = ['摩羯', '水瓶', '双鱼', '白羊', '金牛', '双子', '巨蟹', '狮子', '处女', '天秤', '天蝎', '射手']
WeekCn = ["星期日", "星期一", "星期二", "星期三", "星期四", "星期五", "星期六"]
moon = {'新月': '🌑', '蛾眉月': '🌒', '上弦月': '🌓', '盈凸月': '🌔', '满月': '🌕', '亏凸月': '🌖', '下弦月': '🌗', '残月': '🌘'}
lunar = sxtwl.fromSolar(int(datetime.datetime.fromtimestamp(time.time()).year),
                        int(datetime.datetime.fromtimestamp(time.time()).month),
                        int(datetime.datetime.fromtimestamp(time.time()).day))

htkt = 'https://international.v1.hitokoto.cn/'
hito = requests.get(htkt).json()

# 获取地址信息
def locate():
    city = requests.get(location).json()
    name = city['location'][0]['name']
    adm = city['location'][0]['adm2']
    where = '📍 ' + adm + ' ' + name
    return where

# 获取今天天气
def today_wt():
    today = requests.get(days).json()
    td_date = today['daily'][0]['fxDate']
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
    td = '今天是 ' + td_date + '\n' + lunar_td(
        lunar) + '\n\n白天' + td_day + ' 夜间' + td_night + ' ' + td_max + '°~' + td_min + '° ' + '紫外线' + td_uv + '级 ' + td_wind + td_winds + '级\n' + '😎' + td_sunrise + '~' + td_sunset + ' ' + \
         moon[td_moon] + td_moonrise + '~' + td_moonset
    return td

# 获取明天天气
def tomorrow_wt():
    tomorrow = requests.get(days).json()
    tm_date = tomorrow['daily'][1]['fxDate']
    tm_max = tomorrow['daily'][1]['tempMax']
    tm_min = tomorrow['daily'][1]['tempMin']
    tm_day = tomorrow['daily'][1]['textDay']
    tm_night = tomorrow['daily'][1]['textNight']
    tm_sunset = tomorrow['daily'][1]['sunset']
    tm_sunrise = tomorrow['daily'][1]['sunrise']
    tm_moonset = tomorrow['daily'][1]['moonset']
    tm_moonrise = tomorrow['daily'][1]['moonrise']
    tm_moon = tomorrow['daily'][1]['moonPhase']
    tm_wind = tomorrow['daily'][1]['windDirDay']
    tm_winds = tomorrow['daily'][1]['windScaleDay']
    tm_uv = tomorrow['daily'][1]['uvIndex']
    tm = '明天是 ' + tm_date + '\n白天' + tm_day + ' 夜间' + tm_night + ' ' + tm_max + '°~' + tm_min + '° ' + '紫外线' + tm_uv + '级 ' + tm_wind + tm_winds + '级\n' + '😎' + tm_sunrise + '~' + tm_sunset + ' ' + \
         moon[tm_moon] + tm_moonrise + '~' + tm_moonset
    return tm

# 获取空气指数
def air_index():
    now_air = requests.get(air).json()
    air_aqi = now_air['now']['aqi']
    air_text = now_air['now']['category']
    air_pm25 = now_air['now']['pm2p5']
    air_id = '空气指数 ' + air_aqi + ' ' + air_text + ' PM2.5:' + air_pm25
    return air_id

# 获取天气预警
def now_warning():
    warn = requests.get(warning).json()
    if len(warn['warning']) == 0:
        warn_msg = '无事发生！'
    else:
        title = warn['warning'][0]['title']
        text = warn['warning'][0]['text']
        warn_msg = title + '\n' + text + '\n'
    return warn_msg

# 获取实时天气情况
def now_wt():
    now_weather = requests.get(now).json()
    now_time = now_weather['now']['obsTime'][:10] + ' ' + now_weather['now']['obsTime'][11:16]
    now_temp = now_weather['now']['temp']
    now_des = now_weather['now']['text']
    now_wind = now_weather['now']['windDir']
    now_windscale = now_weather['now']['windScale']
    now_wt = now_time + ' 测定\n现在 ' + now_temp + '° ' + now_des + ' ' + now_wind + ' ' + now_windscale + '级'
    return now_wt

# 获取当前所在城市的和风天气网页链接
def wt_link():
    now_weather = requests.get(now).json()
    link = now_weather['fxLink']
    return link

# 获取未来6小时天气预报
def hour1():
    list = []
    for i in range(6):
        hours = requests.get(hour).json()
        hour_time = hours['hourly'][i]['fxTime'][11:16]
        hour_text = hours['hourly'][i]['text']
        hour_temp = hours['hourly'][i]['temp']
        hour_wind = hours['hourly'][i]['windDir']
        hour_windsc = hours['hourly'][i]['windScale']
        hour_weather = hour_time + ' ' + hour_temp + '° ' + hour_text + ' ' + hour_wind + ' ' + hour_windsc + '级'

        list.append(hour_weather)
        six = '\n'.join(list)
    return six

# 获取生活指数
def life_index():
    life_index = requests.get(life).json()
    living = life_index['daily'][7]['category'] + ' ' + life_index['daily'][7]['text']
    # sport = life_index['daily'][0]['category'] + '运动 ' + life_index['daily'][0]['text'] + '\n'
    # wear = '天气' + life_index['daily'][1]['category'] + ' ' + life_index['daily'][1]['text'] + '\n'
    # sunburn = life_index['daily'][2]['text'] + '\n'  # '紫外线' + life_index['daily'][2]['category'] + ' ' +

    life_id = living
    return life_id

# 获取当天农历信息
def lunar_td(day):
    yTG = day.getYearGZ(True)
    week = WeekCn[day.getWeek()]
    star = XiZ[day.getConstellation()]
    ganzhi = Gan[yTG.tg] + Zhi[yTG.dz]
    lunar = "%s%d月%d日" % ('闰' if day.isLunarLeap() else '', day.getLunarMonth(), day.getLunarDay())
    shengxiao = ShX[yTG.dz]
    if day.hasJieQi():
        jd = day.getJieQiJD()
        t = sxtwl.JD2DD(jd)
        return (week + ' ' + star + ' ' + ganzhi + '(' + shengxiao + ')年 ' + lunar + ' ' + '%s' % jqmc[
            day.getJieQi()] + '' + "(%d-%d-%d %d:%d:%d)" % (t.Y, t.M, t.D, t.h, t.m, round(t.s)))
    else:
        return week + ' ' + star + ' ' + ganzhi + '(' + shengxiao + ')年 ' + lunar

# 获取一言（Hitokoto）
def ichiba():
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

# 获取一言的链接
def htkt_link():
    uuid = hito['uuid']
    link = 'https://hitokoto.cn?uuid=' + uuid
    return link
