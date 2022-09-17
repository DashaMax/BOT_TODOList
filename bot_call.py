import telebot
import datetime
import time

from connect import connection, cursor
from admin import token

#Данные бота
bot = telebot.TeleBot(token)

while True:
    date_today = datetime.date.today()
    select = f"SELECT `time_notify` FROM `list_del` WHERE `dates` = '{date_today}' AND `time_notify` is not NULL"
    cursor.execute(select)
    connection.commit()
    if cursor.fetchall() is not None:
        select_1 = f"SELECT * FROM list_del WHERE dates = '{date_today}' AND `time_notify` is not NULL"
        cursor.execute(select_1)
        connection.commit()
        list_el = cursor.fetchall()
        if list_el is not None:
            for el in range(len(list_el)):
                N1 = str(list_el[el]['N'])
                id_1 = str(list_el[el]['id'])
                time_1 = str(list_el[el]['time_notify'])
                task_1 = str(list_el[el]['active tasks'])
                but_notif = telebot.types.InlineKeyboardMarkup()
                b15 = telebot.types.InlineKeyboardButton('На 15 мин', callback_data='call' + '/' + '15' + '/' + N1 + '/' + task_1)
                b30 = telebot.types.InlineKeyboardButton('На 30 мин', callback_data='call' + '/' + '30' + '/' + N1 + '/' + task_1)
                b60 = telebot.types.InlineKeyboardButton('На 1 час', callback_data='call' + '/' + '60' + '/' + N1 + '/' + task_1)
                b = telebot.types.InlineKeyboardButton('Другое время', callback_data='call' + '/' + 'time' + '/' + N1 + '/' + task_1)
                comp = telebot.types.InlineKeyboardButton('Задача выполнена', callback_data='call' + '/' + 'comp' + '/' + N1 + '/' + task_1)
                but_notif.row(b15, b30, b60)
                but_notif.row(b, comp)
                time_now = str(datetime.time.strftime(datetime.datetime.now().time(), '%H:%M'))
                if time_now == time_1:
                    bot.send_message(id_1, 'Напоминаю:\n--> ' + task_1)
                    bot.send_message(id_1, 'Отложить напоминание?', reply_markup=but_notif)
            time.sleep(60)




