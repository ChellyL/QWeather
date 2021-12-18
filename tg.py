import telegram
# import os
#
# os.environ['http_proxy'] = 'http://127.0.0.1:7890'
# os.environ['https_proxy'] = 'https://127.0.0.1:7890'
# 国内机器建议用代理
token = '' # 频道token
userid = '' # 个人id


def tgme(words):
    bot = telegram.Bot(token)
    bot.sendMessage(chat_id=userid, text=words, parse_mode=telegram.ParseMode.HTML)
