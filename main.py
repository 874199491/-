from datetime import date, datetime
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random
import time

week_list = ["星期日", "星期一", "星期二", "星期三", "星期四", "星期五", "星期六"]
year = time.localtime().tm_year  # 既可以获取当前年份，也可以指定年份
month = time.localtime().tm_mon  # 既可以获取当前月份，也可以指定年月份
day = time.localtime().tm_mday  # 既可以获取当前天数，也可以指定天数
date = datetime.date(datetime(year=year, month=month, day=day))
food = {"Monday": ["玉米+鸡蛋", "西红柿炒蛋、咸鸭蛋", "香菇炒肉、咸鸭蛋"],
        "Tuesday": ["肉丝米粉", "香菇炒肉、咸鸭蛋", "鸡蛋干炒肉、咸鸭蛋"],
        "Wednesday": ["两个鸡蛋", "火腿肠炒蛋", "榨菜炒肉"],
        "Thursday": ["玉米", "蒸鸡蛋", "香菇炒肉"],
        "Friday": ["肉丝粉", "鸡蛋干炒肉", "西红柿炒蛋"],
        "Saturday": ["两个鸡蛋", "两个鸡蛋", "蒸鸡蛋+炒火腿肠"],
        "Sunday": ["牛肉粉", "香菇香菜汤", "香菇炒肉"],
        }
morning = food[date.strftime("%A")][0]
lunch = food[date.strftime("%A")][1]
night = food[date.strftime("%A")][2]


today = datetime.now()
start_date = os.environ['START_DATE']
city = os.environ['CITY']
birthday = os.environ['BIRTHDAY']

app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]

user_id = os.environ["USER_ID"]
template_id = os.environ["TEMPLATE_ID"]

def get_weather():
  url = "http://autodev.openspeech.cn/csp/api/v2.1/weather?openId=aiuicus&clientType=android&sign=android&city=" + city
  res = requests.get(url).json()
  weather = res['data']['list'][0]
  return weather['weather'], math.floor(weather['temp'])

def get_count():
  delta = today - datetime.strptime(start_date, "%Y-%m-%d")
  return delta.days

def get_birthday():
  next = datetime.strptime(str(date.today().year) + "-" + birthday, "%Y-%m-%d")
  if next < datetime.now():
    next = next.replace(year=next.year + 1)
  return (next - today).days

def get_words():
  words = requests.get("https://api.shadiao.pro/chp")
  if words.status_code != 200:
    return get_words()
  return words.json()['data']['text']

def get_random_color():
  return "#%06x" % random.randint(0, 0xFFFFFF)


client = WeChatClient(app_id, app_secret)

wm = WeChatMessage(client)
wea, temperature = get_weather()
data = {"city":{"value":city},"weather":{"value":wea},"temperature":{"value":temperature},"love_days":{"value":get_count()},"birthday_left":{"value":get_birthday()},"words":{"value":get_words(), "color":get_random_color()}}
res = wm.send_template(user_id, template_id, data)
print(res)
