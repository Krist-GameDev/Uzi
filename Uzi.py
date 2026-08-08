from re import *
import requests
from datetime import date, datetime
import time
import random
import schedule

tg_token = str(open('uzi.txt').readline())
admin_id = 7644347447
msg_keys = ['message', 'edited_message']
url = f"https://api.telegram.org/bot{tg_token}"


#Отправка сообщений
def send_message(id, text):
    answer = requests.post(url+"/sendMessage", json={"chat_id": id, "text": text})
#send_message(admin_id, input())

#Просмотр последних сообщений
def LastMsg(url):
    while True:
        all_msg_base = requests.get(url+"/getUpdates").json()
        amb = [msg for msg in all_msg_base['result'][-6:] if all_msg_base['result']]
        utmb = [i[x]['text'] for i in amb for x in msg_keys if x in i]

#Чек даты
def TimeCheck():
    data = str(datetime.now())[:-10]
    return data


#Список просьб

#Напоминание о дедлайнах


#Пожелание доброй ночи и утра
gmn_ms = False
gmn_ns = False
gmn_ld = None
rnd_m = "07:00"
rnd_n = "22:00"
Gm = ['Утречка', 'Доброе утро', 'Утречка :3']
Gn = ['Спокойной ночи, сладких снов', 'Доброй ночи', 'Спокойной ночи']
def GMN():
    global gmn_ms, gmn_ns, gmn_ld, rnd_m, rnd_n
    tm = TimeCheck()[-5:]
    today = date.today()
    if gmn_ld!=today:
        gmn_ms = False
        gmn_ns = False
        gmn_ld = today
        rnd_m = ':'.join([str(random.choice(['0'+str(x) for x in range(7,10)]+[str(x) for x in range(10,13)])), \
        str(random.choice(['0'+str(x) for x in range(0,10)]+[str(x) for x in range(10,60)]))])
        rnd_n = ':'.join([str(random.choice(['22','23'])), \
        str(random.choice(['0'+str(x) for x in range(0,10)]+[str(x) for x in range(10,60)]))])
    #Утро
    if 6<int(tm[:2])<13:
        if not gmn_ms:
            if int(''.join(tm.split(':')))>=int(''.join(rnd_m.split(':'))):
                send_message(admin_id, random.choice(Gm))
                gmn_ms = True
    #Ночь
    elif 21<int(tm[:2])<25:
        if not gmn_ns:
            if int(''.join(tm.split(':')))>=int(''.join(rnd_n.split(':'))):
                send_message(admin_id, random.choice(Gn))
                gmn_ns = True
def SelfPing():
    try:
        requests.get("https://uzi-ecu4.onrender.com")
        print("Бот успешно отправил пинг сам себе для защиты от сна.")
    except Exception as e:
        print("Ошибка самопинга:", e)

schedule.every(10).minutes.do(SelfPing)
schedule.every(5).minutes.do(LastMsg, url=url)
schedule.every(10).seconds.do(GMN)

while True:
    schedule.run_pending()
    time.sleep(1)
