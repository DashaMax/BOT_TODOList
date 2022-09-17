from connect import connection, cursor
import aiogram
from BUTS import naz_menu
import datetime

def add_tasks(id, date, task, text_exit):
    select = f"SELECT * FROM list_del WHERE id = {id} AND dates = '{date}' AND `active tasks` = '{task}'"
    cursor.execute(select)
    if cursor.fetchall() == ():
        insert_add = f"INSERT INTO `list_del` (`id`, `dates`, `active tasks`) VALUES ({id}, '{date}', '{task}')"
        cursor.execute(insert_add)
        connection.commit()
    text = 'Задача ' + text_exit + '. Хотите установить напоминание для данной задачи?'
    return text


def show_all(id, text):
    select_dates = f'SELECT DISTINCT `dates` FROM list_del WHERE id = {id} AND `{text}` is not NULL ORDER BY `dates`'
    cursor.execute(select_dates)
    text_res = ''
    for el in cursor.fetchall():
        data = str(el['dates']).split('-')
        text_res += data[2] + '.' + data[1] + '.' + data[0] + ':\n'
        select_tasks = f"SELECT `{text}` FROM list_del WHERE id = {id} AND dates = '{el['dates']}' AND `{text}` is not NULL"
        cursor.execute(select_tasks)
        for task in cursor.fetchall():
            text_res += task[text] + '\n'
        text_res += '\n'
    return text_res


def choise_date(id, text, text_but):
    select_dates = f'SELECT DISTINCT `dates` FROM list_del WHERE id = {id} AND `{text}` is not NULL ORDER BY `dates`'
    cursor.execute(select_dates)
    date_list = []
    but_data_list = aiogram.types.InlineKeyboardMarkup(resize_keyboard=True)
    for el in cursor.fetchall():
        data = str(el['dates']).split('-')
        data = data[2] + '.' + data[1] + '.' + data[0]
        date_list.append(data)
        date_but = aiogram.types.InlineKeyboardButton(data, callback_data=data)
        but_data_list.add(date_but)
    but = aiogram.types.InlineKeyboardButton('<< Назад', callback_data=text_but)
    but_data_list.add(but)
    return date_list, but_data_list


def task(id, data, text):
    dat = (datetime.datetime.strptime(data, '%d.%m.%Y')).date()
    select = f"SELECT `{text}` FROM list_del WHERE id = {id} AND dates = '{dat}' AND `{text}` is not NULL"
    cursor.execute(select)
    text_res = data + ':\n'
    for el in cursor.fetchall():
        text_res += str(el[text]) + '\n'
    return text_res


def but_tasks(id, data, text_but):
    data = (datetime.datetime.strptime(data, '%d.%m.%Y')).date()
    select = f"SELECT `active tasks` FROM list_del WHERE id = {id} AND dates = '{data}' AND `active tasks` is not NULL"
    cursor.execute(select)
    but_task_list = aiogram.types.InlineKeyboardMarkup(resize_keyboard=True)
    list_task_active = []
    for el in cursor.fetchall():
        list_task_active.append(el['active tasks'])
        task_but = aiogram.types.InlineKeyboardButton(el['active tasks'], callback_data=el['active tasks'])
        but_task_list.add(task_but)
    naz_data = aiogram.types.InlineKeyboardButton('<< Назад', callback_data=text_but)
    but_task_list.add(naz_data)
    return but_task_list


def delete_list(id):
    select = f'SELECT `active tasks`, `complite tasks` FROM list_del WHERE id = {id} AND `active tasks` is NULL AND `complite tasks` is NULL'
    cursor.execute(select)
    if cursor.fetchall() != ():
        delete = f'DELETE FROM list_del WHERE id = {id} AND `active tasks` is NULL AND `complite tasks` is NULL'
        cursor.execute(delete)
        connection.commit()


def reschedule_f(id, date, task):
    data = (datetime.datetime.strptime(date, '%d.%m.%Y')).date()
    update = f"UPDATE `list_del` SET `active tasks` = NULL, `time_notify` = NULL WHERE id = {id} AND dates = '{data}' AND `active tasks` = '{task}'"
    cursor.execute(update)
    connection.commit()
    select = f'SELECT `active tasks`, `complite tasks` FROM list_del WHERE id = {id} AND `active tasks` is NULL AND `complite tasks` is NULL'
    cursor.execute(select)
    if cursor.fetchall() != ():
        delete = f'DELETE FROM list_del WHERE id = {id} AND `active tasks` is NULL AND `complite tasks` is NULL'
        cursor.execute(delete)
        connection.commit()


def noti_date(id, text_but, isnot):
    select_dates = f"SELECT DISTINCT `dates` FROM list_del WHERE id = {id} AND `active tasks` is not NULL AND " \
                   f"`time_notify` {isnot} NULL ORDER BY `dates`"
    cursor.execute(select_dates)
    but_data_list = aiogram.types.InlineKeyboardMarkup(resize_keyboard=True)
    for el in cursor.fetchall():
        data = str(el['dates']).split('-')
        data = data[2] + '.' + data[1] + '.' + data[0]
        date_but = aiogram.types.InlineKeyboardButton(data, callback_data=data)
        but_data_list.add(date_but)
    but = aiogram.types.InlineKeyboardButton('<< Назад', callback_data=text_but)
    but_data_list.add(but)
    return but_data_list


def noti_task(id, data, text_but, isnot):
    select_dates = f"SELECT `active tasks` FROM list_del WHERE id = {id} AND dates = '{data}' AND `active tasks` is not NULL AND " \
                   f"`time_notify` {isnot} NULL ORDER BY `dates`"
    cursor.execute(select_dates)
    but_tasks_list = aiogram.types.InlineKeyboardMarkup(resize_keyboard=True)
    for el in cursor.fetchall():
        task_but = aiogram.types.InlineKeyboardButton(el['active tasks'], callback_data=el['active tasks'])
        but_tasks_list.add(task_but)
    but = aiogram.types.InlineKeyboardButton('<< Назад', callback_data=text_but)
    but_tasks_list.add(but)
    return  but_tasks_list