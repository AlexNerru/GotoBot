# -*- coding: utf-8 -*-
import config
import telebot
import sqlite3
import datetime
import time
from threading import Thread
#import os

bot = telebot.TeleBot(config.token)

conf = config.Configuration()

achieve_storage = {}
time_storage = {}
log_passwerd_storage = {}
texts = []
line = 0

#Сделать справки и оптимизировать UX
#Общая оптимизация после создания полного функционала
#Прикрутить webhook
# Переделать перевод языка


def upcoming_event():  #обработка событий
    while True:
        time_now = datetime.datetime.now()
        current_date = time_now.strftime('%Y-%m-%d')
        current_time = time_now.strftime('%H-%M')
        conf.bd_on()
        conf.conn_db_cursor.execute("SELECT * FROM Events WHERE Date=?",(current_date,))
        events = conf.conn_db_cursor.fetchall()
        cur = conf.conn_db_cursor.execute("SELECT Telegram_id FROM People")
        all_id = cur.fetchall()
        was_sent = 'True'
        for i in range(len(events)):
            row=events [i]
            if (current_time==row[1] and (row[6]=='False')):
                str = conf.now + row [4] + "' - " + conf.address + ": " + row [3]
                conf.conn_db_cursor.execute("UPDATE Events SET Was_sent=? WHERE Date = ? AND Start_Time = ? AND End_Time=? AND Address=? AND Name=? AND Description=?",
                                            (was_sent,row [0],row[1],row[2],row[3],row[4],row[5],))
                for i in range(len(all_id)):
                    row1 = all_id[i]
                    id = row1[0]
                    bot.send_message(id, str)
        conf.bd_of()
        time.sleep (10)

@bot.message_handler(commands=['start','help'])  #стартуем, обработка id
def handle_start(message):
     bot.send_message(message.chat.id, conf.main_hello)
     current_id=message.chat.id
     conf.bd_on()
     conf.conn_db_cursor.execute ("SELECT * FROM People WHERE Telegram_id=?", (current_id,))
     row=conf.conn_db_cursor.fetchone ()
     if (row == None):
         current_user_name = message.chat.first_name
         current_user_last_name = message.chat.last_name
         conf.conn_db.execute("INSERT INTO People (Telegram_id, Name, Second_name) VALUES (?, ?, ?)",
                         (current_id, current_user_name, current_user_last_name))
         conf.conn_db.execute("UPDATE People SET Id=rowid")
         bot.send_message(message.chat.id, conf.add_phone_and_address)
     conf.bd_of()

@bot.message_handler(commands=['admin']) #перейти в режим админа
def change_mod(message):
    try:
        msg = bot.reply_to(message, conf.log_enter)
        bot.register_next_step_handler(msg, change_mod2)
    except TypeError:
        bot.send_message(message.chat.id, conf.type_error)

def change_mod2(message):
    str1 = message.text
    str1.lower()
    if str1 == config.log_password:
        bot.send_message (message.chat.id, conf.admin_main_text)
        conf.admin_bool = True
    elif str1== '':
        text = conf.admin_write_any
        bot.send_message (message.chat.id, text)
    else:
        text = conf.admin_wrong
        bot.send_message (message.chat.id, text)

@bot.message_handler (commands=['user'])   #вернуться в режим юзера
def change_mod_user(message):
    text = conf.user_now
    bot.send_message(message.chat.id, text)
    conf.admin_bool = False

@bot.message_handler(commands=['add_phone'])       #Добавить/изменить телефон
def add_phone(message):
    try:
        msg = bot.reply_to(message, conf.phone_enter)
        bot.register_next_step_handler(msg, add_phone2)
    except TypeError:
        bot.send_message(message.chat.id, conf.type_error)

def add_phone2 (message):
    try:
        str1 = message.text
        conf.bd_on()
        if ("/" not in str1):
            current_id = message.chat.id
            conf.conn_db_cursor.execute("UPDATE People SET Phone=? WHERE Telegram_id=?", (str1,current_id,))
            bot.send_message(message.chat.id, conf.phone_ok)
        conf.bd_of()
    except TypeError:
        bot.send_message(message.chat.id, conf.type_error)

@bot.message_handler(commands=['add_address'])      #Добавить/изменить адрес
def add_address(message):
    try:
        msg = bot.reply_to(message, conf.address_enter)
        bot.register_next_step_handler(msg, add_address2)
    except TypeError:
        bot.send_message(message.chat.id, conf.type_error)

def add_address2(message):
    try:
        str = message.text
        conf.bd_on()
        if ("/" not in str):
            current_id = message.chat.id
            conf.conn_db_cursor.execute("UPDATE People SET Address=? WHERE Telegram_id=?", (str,current_id,))
            bot.send_message(message.chat.id, conf.address_ok)
        conf.bd_of()
    except TypeError:
        bot.send_message(message.chat.id, conf.type_error)

@bot.message_handler(commands=['language'])      #Изменить язык, потом подумать нафиг нужен класс (с ним удобнее, засунуть туда работу с бд) хД
def language(message):
    if conf.admin_bool == True:
        conf.change_language ()
    else:
        bot.send_message(message.chat.id, conf.need_admin)

@bot.message_handler(commands=['phone'])      #Узнать номер телефона
def phone(message):
    try:
        msg = bot.reply_to(message, conf.achieve_guy)
        bot.register_next_step_handler(msg, phone2)
    except TypeError:
        bot.send_message(message.chat.id, conf.type_error)

def phone2 (message):
    try:
        str1 = message.text
        conf.bd_on()
        if ("/" not in str1):
            first_space=str1.find (' ')
            if first_space!=-1:
                name=str1[:first_space]
                second_name=str1[first_space+1:]
                conf.conn_db_cursor.execute("SELECT * FROM People WHERE Second_name=? OR Name=? OR Name=? OR Second_name=?" , (str1,str1,name,second_name,))
                row = conf.conn_db_cursor.fetchone()
                if row [3]!=None:
                    bot.send_message(message.chat.id, row [3])          #менять цифру, если меняешь столбцы в бд
                else:
                    bot.send_message(message.chat.id, conf.data_exist)
            else:
                bot.send_message(message.chat.id,conf.achieve_guy)
        conf.bd_of()
    except TypeError:
        bot.send_message(message.chat.id, conf.type_error)

@bot.message_handler(commands=['address'])      #Узнать адрес
def address(message):
    try:
        msg = bot.reply_to(message, conf.achieve_guy)
        bot.register_next_step_handler(msg, address2)
    except TypeError:
        bot.send_message(message.chat.id, conf.type_error)

def address2 (message):
    try:
        str1 = message.text
        conf.bd_on()
        if ("/" not in str1):
            first_space = str1.find(' ')
            if first_space != -1:
                name = str1[:first_space]
                second_name = str1[first_space + 1:]
                conf.conn_db_cursor.execute("SELECT * FROM People WHERE Second_name=? OR Name=? OR Name=? OR Second_name=?", (str1,str1,name,second_name,))
                row = conf.conn_db_cursor.fetchone()
                if row[4] != None:
                    bot.send_message(message.chat.id, row [4])          #менять цифру, если меняешь столбцы в бд
                else:
                    bot.send_message(message.chat.id, conf.data_exist)
            else:
                bot.send_message(message.chat.id,conf.achieve_guy)
        conf.bd_of()
    except TypeError:
        bot.send_message(message.chat.id, conf.type_error)

@bot.message_handler(commands= ['achieve'])   #Перейти к вводу ачивки (удаление ачивки, есть ли юзер делать?)
def give_achieve (message):
    if conf.admin_bool == True:
        msg = bot.reply_to(message, conf.achieve_guy)
        bot.register_next_step_handler(msg, name_enter)
    else:
        bot.send_message(message.chat.id, conf.need_admin)

def name_enter(message):        #Ввод ачивки, выбираем пользователя
    try :
        conf.bd_on()
        str1=message.text
        if ("/" not in str1):
            first_space = str1.find(' ')
            name = str1[:first_space]
            second_name = str1[first_space + 1:]
            conf.conn_db_cursor.execute("SELECT * FROM People WHERE Second_name=? OR Name=? OR Name=? OR Second_name=?" , (str1,str1,name,second_name,))
            row=conf.conn_db_cursor.fetchone()
            #print(row)
            if (row!=None):
                id=row[5]
                #print(id)
                achieve_storage [0]=id
                msg = bot.reply_to(message, conf.achieve)
                bot.register_next_step_handler(msg, achieve_enter)
            else:
                bot.send_message(message.chat.id, conf.user_not_exist)
                achieve_storage.clear()
        conf.bd_of()
    except TypeError:
        bot.send_message(message.chat.id, conf.type_error)
        achieve_storage.clear()

def achieve_enter (message):  #Ввод ачивки, название ачивки
    try:
        str=message.text
        if ("/" not in str):
            achieve_storage [1] = str
            msg = bot.reply_to(message, conf.achieve_descr)
            bot.register_next_step_handler(msg, achieve_descr)
    except TypeError:
        bot.send_message(message.chat.id, conf.type_error)
        achieve_storage.clear()

def achieve_descr (message): #Ввод ачивки, описание ачивки
      try:
        str=message.text
        conf.bd_on()
        if ("/" not in str):
            conf.conn_db_cursor.execute("SELECT * FROM Achievments Where Id=? AND Name=?" ,(achieve_storage[0], achieve_storage[1],))
            row = conf.conn_db_cursor.fetchone()
            if (row == None):
                conf.conn_db_cursor.execute("INSERT INTO Achievments (Id, Name, Description) VALUES (?, ?, ?)",
                                     (achieve_storage[0], achieve_storage[1], str))
                achieve_storage[2] = str
                conf.bd_of()
                achiev_notification()
            else:
                bot.send_message(message.chat.id, conf.achieve_exist)
                achieve_storage.clear()
      except TypeError:
          bot.send_message(message.chat.id, conf.type_error)
          achieve_storage.clear()

def achiev_notification (): #написать всем об ошибке
    conf.bd_on()
    cur = conf.conn_db_cursor.execute("SELECT Telegram_id FROM People")
    all_id = cur.fetchall()
    id1=int (achieve_storage[0])
    print(id1)
    cur = conf.conn_db_cursor.execute("SELECT * FROM People Where Id=?", (id1,))
    row = cur.fetchone()
    str2 = (row [1] + " " + row [2] + " получил/получила ачивку ' " + achieve_storage[1] + " ' - "+ achieve_storage[2] + "!")
    for i in range(len(all_id)):
        id = (all_id[i]) [0]
        bot.send_message(id, str2)
    achieve_storage.clear()
    conf.bd_of()

@bot.message_handler(commands= ['achieve_list']) #список ачивок пользователя
def achieve_list (message):
    try:
        msg = bot.reply_to(message, conf.achieve_guy)
        bot.register_next_step_handler(msg, achieve_list2)
    except TypeError:
        bot.send_message(message.chat.id, conf.type_error)

def achieve_list2(message):
    try:
        str2=message.text
        conf.bd_on()
        if ("/" not in str2):
            first_space = str2.find(' ')
            name = str2[:first_space]
            second_name = str2[first_space + 1:]
            conf.conn_db_cursor.execute("SELECT * FROM People WHERE Second_name=? OR Name=? OR Name=? OR Second_name=?",
                                    (str2, str2, name, second_name,))
            row = conf.conn_db_cursor.fetchone()
            if row!=None:
                id = row [5]
                conf.conn_db_cursor.execute("SELECT * FROM Achievments WHERE Id = ?",
                                        (id,))
                achievelist=conf.conn_db_cursor.fetchall()
                for i in range(len(achievelist)):
                    row1 = achievelist [i]
                    bot.send_message(message.chat.id, row1 [1])
            else:
                bot.send_message(message.chat.id, conf.user_not_exist)
                achieve_storage.clear()
        conf.bd_of()
    except TypeError:
        bot.send_message(message.chat.id, conf.type_error)
        achieve_storage.clear()

@bot.message_handler(commands= ['add_event'])  #добавление события в бд
def add_event (message):
    if conf.admin_bool == True:
        msg = bot.reply_to(message, conf.add_date)
        bot.register_next_step_handler(msg, date)
    else:
        bot.send_message(message.chat.id, conf.need_admin)

def date(message):
    try:
        str1=message.text
        if ("/" not in str1):
            time_storage[0] = str1
            msg = bot.reply_to(message, conf.add_starttime)
            bot.register_next_step_handler(msg, start_time)
    except TypeError:
        bot.send_message(message.chat.id, conf.type_error)
        time_storage.clear()

def start_time (message):
    try:
        str1 = message.text
        if ("/" not in str1):
            time_storage [1]=str1
            msg = bot.reply_to(message, conf.add_endtime)
            bot.register_next_step_handler(msg, end_time)
    except TypeError:
        bot.send_message(message.chat.id, conf.type_error)
        time_storage.clear()

def end_time (message):
    try:
        str1 = message.text
        if ("/" not in str1):
            time_storage[2] = str1
            msg = bot.reply_to(message, conf.event_address)
            bot.register_next_step_handler(msg, event_address)
    except TypeError:
        bot.send_message(message.chat.id, conf.type_error)
        time_storage.clear()

def event_address (message):
    try:
        str1 = message.text
        if ("/" not in str1):
            time_storage[3] = str1
            msg = bot.reply_to(message, conf.event_name)
            bot.register_next_step_handler(msg, event_name)
    except TypeError:
        bot.send_message(message.chat.id, conf.type_error)
        time_storage.clear()

def event_name (message):
    try:
        str1 = message.text
        if ("/" not in str1):
            time_storage[4] = str1
            msg = bot.reply_to(message, conf.event_descr)
            bot.register_next_step_handler(msg, event_descr)
    except TypeError:
        bot.send_message(message.chat.id, conf.type_error)
        time_storage.clear()

def event_descr (message):
    try:
        str1 = message.text
        if ("/" not in str1):
            time_storage[5] = str1
            conf.bd_on()
            conf.conn_db_cursor.execute("SELECT * FROM Events Where Date = ? AND Start_Time = ? AND End_Time=? AND Address=? AND Name=? AND Description=?",
                             (time_storage [0], time_storage [1], time_storage [2],time_storage [3],time_storage [4],time_storage [5]))
            row = conf.conn_db_cursor.fetchone()
            if (row == None):
                conf.conn_db.execute("INSERT INTO Events (Date, Start_Time,End_Time,Address, Name, Description, Was_sent) VALUES (?, ?, ?, ?,?,?,?)",
                                 (time_storage [0], time_storage [1], time_storage [2],time_storage [3],time_storage [4],time_storage [5],'False'))
                bot.send_message(message.chat.id, conf.event_added)
                bot.send_message(message.chat.id, conf.admin_text)
            else:
                bot.send_message(message.chat.id, conf.event_exist)
                achieve_storage.clear()
        conf.bd_of()

    except TypeError:
        bot.send_message(message.chat.id, conf.type_error)
        time_storage.clear()
    except sqlite3.ProgrammingError:
        bot.send_message(message.chat.id, conf.type_error)
        time_storage.clear()

@bot.message_handler(commands= ['schedule']) #расписание на день
def schedule (message):
    time=datetime.datetime.now()
    current_date=time.strftime ('%Y-%m-%d')
    conf.bd_on()
    conf.conn_db_cursor.execute ("SELECT * FROM Events WHERE Date=?" , (current_date,))
    events=conf.conn_db_cursor.fetchall()
    bot.send_message(message.chat.id, conf.schedule)
    str=""
    for i in range (len(events)):
        row=events [i]
        #for j in range (len(row)-1):
        str = conf.at + " " + row [1] + conf.till + row [2] + " - '" + row [4] + "' - " + row[5] + " - "+ conf.address + ": "+ row[3]
        bot.send_message(message.chat.id, str)
        str = ""

@bot.message_handler(commands= ['now']) #что и где сейчас идет
def now(message):
    time_now = datetime.datetime.now()
    current_date = time_now.strftime('%Y-%m-%d')
    current_time = time_now.strftime('%H-%M')
    conf.bd_on()
    conf.conn_db_cursor.execute("SELECT * FROM Events WHERE Date=?", (current_date,))
    events = conf.conn_db_cursor.fetchall()
    if events:
        for i in range(len(events)):
            row=events[i]
            if (row[1]<=current_time and row[2]>=current_time):
                str=conf.now1 + row [4] + "' " + conf.address + ": " + row [3]
                bot.send_message(message.chat.id, str)
            else:
                bot.send_message(message.chat.id, conf.nothing)
    else:
        bot.send_message(message.chat.id, conf.nothing)

@bot.message_handler(commands= ['alarm'])   #срочное сообщение всем
def alarm (message):
    if conf.admin_bool == True:
        msg = bot.reply_to(message, conf.alarm)
        bot.register_next_step_handler(msg, alarm2)
    else:
        bot.send_message(message.chat.id, conf.need_admin)

def alarm2 (message):
    try:
        conf.bd_on()
        str1 = message.text
        if conf.admin_bool == True:
            if ("/" not in str1):
                cur = conf.conn_db_cursor.execute("SELECT Telegram_id FROM People")
                all_id = cur.fetchall()
                for i in range(len(all_id)):
                    row = all_id[i]
                    id = row[0]
                    if id != message.chat.id:
                        bot.send_message(id, str1)
        else:
            bot.send_message(message.chat.id, conf.need_admin)
        conf.bd_of()
    except TypeError:
        bot.send_message(message.chat.id, conf.type_error)
        conf.bd_of()
    except sqlite3.ProgrammingError:
        bot.send_message(message.chat.id, conf.type_error)
        conf.bd_of()

@bot.message_handler(commands= ['quest']) #режим квеста
def quest_stert(message):
    try:
        msg = bot.reply_to(message, conf.team_login)
        bot.register_next_step_handler(msg, quest1)
    except TypeError:
        bot.send_message(message.chat.id, conf.type_error)

def quest1 (message): #читаем логин
    try:
        str=message.text
        if ("/" not in str):
            log_passwerd_storage [0]=str
            msg = bot.reply_to(message, conf.team_pass)
            bot.register_next_step_handler(msg, quest2)
    except TypeError:
        bot.send_message(message.chat.id, conf.type_error)
        log_passwerd_storage.clear()


def quest2 (message):  # менять положение файла при смене, открываем файл и проверяем лог и пароль
    try:
        str=message.text
        if ("/" not in str):
            log_passwerd_storage [1]=str
            global texts
            file = open(r'C:\Users\AlexK\PycharmProjects\FirstBot\quest.txt', 'r')
            texts = file.readlines()
            for i in range ( len (texts)):
                texts [i] = texts [i] [0:-1]
            print (texts)
            str1=log_passwerd_storage[0] + " " + log_passwerd_storage [1]
            global line
            while line < (len (texts)):
                if (texts[line]==str1):
                    line+=1
                    log_passwerd_storage.clear()
                    msg = bot.reply_to(message, texts[line])
                    bot.register_next_step_handler(msg, quest_check)
                    break
                line+=1
            if str1 not in texts:
                bot.send_message(message.chat.id, conf.admin_wrong)
                line = 0
                log_passwerd_storage.clear()


    except TypeError:
        bot.send_message(message.chat.id, conf.type_error)
        log_passwerd_storage.clear()

def quest_check (message): # не трогать, работает хД Рекурсивная функция, проходящая по строкам
    try:
        log_passwerd_storage.clear()
        if ("/" not in message.text):
            str1=message.text
            if str1[0].istitle () ==True:
                global line
                if message.text ==  texts [line+1]:
                        line+=2
                        if texts[line + 1] != "" and message.text != "":
                            msg = bot.reply_to(message, texts[line])
                            bot.register_next_step_handler(msg, quest_check)
                        else:
                            bot.send_message(message.chat.id, conf.quest)
                            line = 0
                else:
                    msg = bot.reply_to(message, texts[line])
                    bot.register_next_step_handler(msg, quest_check)
            else:
                bot.send_message(message.chat.id, conf.big_letter)
                msg = bot.reply_to(message, texts[line])
                bot.register_next_step_handler(msg, quest_check)
    except TypeError:
        bot.send_message(message.chat.id, conf.type_error)
    except Exception:  #работает, т.к. при пустом сообщении вылетает error, как бороться не знаю
        bot.send_message(message.chat.id, conf.quest)
        line = 0


def polling():
    bot.polling(none_stop=True)

if __name__ == '__main__':
     thread = Thread(target=upcoming_event)
     thread.start()
     thread1 = Thread(target=polling)
     thread1.start()
