from aiogram import types
import datetime


#Создаем кнопки блокнота
blocnote_buts = types.InlineKeyboardMarkup(resize_keyboard = True)
show = types.InlineKeyboardButton('\U0001F538  Посмотреть список задач', callback_data='show_list_tasks')
add = types.InlineKeyboardButton('\U0001F538  Добавить задачу', callback_data='add_task')
complete = types.InlineKeyboardButton('\U0001F538  Перенести задачу в список выполненных', callback_data='reschedule_task_in_list_complete')
another = types.InlineKeyboardButton('\U0001F538  Перенести задачу на другой день', callback_data='reschedule_task_another_day')
delete = types.InlineKeyboardButton('\U0001F538  Удалить', callback_data='delete_task')
see_task = types.InlineKeyboardButton('\U0001F538  Посмотреть список дел на сегодня', callback_data='show_list_tasks_today')
exit = types.InlineKeyboardButton('Выйти >>>', callback_data='exit')
blocnote_buts.add(see_task).add(add).add(show).add(complete).add(another).add(delete).add(exit)



#Создаем кнопки сегодня, завтра, другой день
but_today = types.InlineKeyboardMarkup(resize_keyboard=True)
today = types.InlineKeyboardButton('Сегодня', callback_data='but_today')
tomorrow = types.InlineKeyboardButton('Завтра', callback_data='but_tomorrow')
any = types.InlineKeyboardButton('Другой день', callback_data='but_anotherday')
naz_menu = types.InlineKeyboardButton('<< Назад', callback_data='but_back_menu')
but_today.row(today, tomorrow).add(any).add(naz_menu)



#Кнопки для перенесения на другой день
but_next_other = types.InlineKeyboardMarkup(resize_keyboard=True)
next = types.InlineKeyboardButton('Следующий день', callback_data='next')
an = types.InlineKeyboardButton('Выбрать день', callback_data='anotherday')
nazad = types.InlineKeyboardButton('<< Назад', callback_data='but_back_task')
but_next_other.row(next, an).add(nazad)

but_per = types.InlineKeyboardMarkup(resize_keyboard=True)
naz_back = types.InlineKeyboardButton('<< Назад', callback_data='back')
but_per.row(next, an).add(naz_back)



#Кнопки удаления
but_delete_all = types.InlineKeyboardMarkup(resize_keyboard = True)
all_tasks = types.InlineKeyboardButton('Очистить всё', callback_data='all_tasks_delete')
all_complete_tasks = types.InlineKeyboardButton('Очистить список выполненных задач', callback_data='all_complete_tasks')
choise_task = types.InlineKeyboardButton('Выбрать задачу ', callback_data='choise_task')
but_delete_all.row(all_tasks, choise_task).add(all_complete_tasks).add(naz_menu)



#Создаем кнопки для выбора ответа "да" или "нет"
but = types.InlineKeyboardMarkup(resize_keyboard = True)
but_1 = types.InlineKeyboardButton('Да', callback_data='but_yes')
but_2 = types.InlineKeyboardButton('Нет', callback_data='but_no')
but.row(but_1, but_2)



#Создаем кнопки для команды - /notfication
but_not = types.InlineKeyboardMarkup(resize_keyboard = True)
but_n1 = types.InlineKeyboardButton('Посмотреть мои уведомления', callback_data='watch')
but_n2 = types.InlineKeyboardButton('Добавить', callback_data='add_not')
but_n3 = types.InlineKeyboardButton('Удалить', callback_data='delete_not')
but_not.add(but_n1).add(but_n2).add(but_n3)



#Создаем кнопки текущих и выполненных задач
tasks_but = types.InlineKeyboardMarkup(resize_keyboard = True)
real_task = types.InlineKeyboardButton('Активные задачи', callback_data='active_tasks_list')
complete_task = types.InlineKeyboardButton('Выполненные задачи', callback_data='complete_tasks_list')
tasks_but.add(real_task).add(complete_task).add(naz_menu)



#Создаем кнопки весь список или выбрать дату
but_all_choise = types.InlineKeyboardMarkup(resize_keyboard = True)
all = types.InlineKeyboardButton('Весь список', callback_data='all_list')
choise = types.InlineKeyboardButton('Выбрать дату', callback_data='choise_date')
naz_task = types.InlineKeyboardButton('<< Назад', callback_data='show_tasks')
but_all_choise.add(all).add(choise).add(naz_task)



#Создаем кнопки - календарь (год)
but_year = types.InlineKeyboardMarkup(resize_keyboard=True)
year_1 = types.InlineKeyboardButton(str(datetime.datetime.now().year), callback_data='now_year')
year_2 = types.InlineKeyboardButton(str(datetime.datetime.now().year + 1), callback_data='next_year')
naz_choise_data = types.InlineKeyboardButton('<< Назад', callback_data='back_choise_data')
but_year.row(year_1, year_2).add(naz_choise_data)

but_year_res = types.InlineKeyboardMarkup(resize_keyboard=True)
but_year_res.row(year_1, year_2)
but_year_res.add(naz_back)



#Создаем кнопки - календарь (месяцы)
but_month = types.InlineKeyboardMarkup(resize_keyboard=True)
month = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь']
el = 0
while el < len(month):
    m_but_1 = types.InlineKeyboardButton(month[el], callback_data= month[el])
    m_but_2 = types.InlineKeyboardButton(month[el + 1], callback_data= month[el + 1])
    m_but_3 = types.InlineKeyboardButton(month[el + 2], callback_data= month[el + 2])
    but_month.row(m_but_1, m_but_2, m_but_3)
    el += 3
naz_choise_year = types.InlineKeyboardButton('<< Назад', callback_data='back_choise_year')
but_month.add(naz_choise_year)



#Создаем кнопки - календарь (дни 31)
but_days_31 = types.InlineKeyboardMarkup(resize_keyboard=True)
i = 1
while i < 32:
    if i == 31:
        d_but_1 = types.InlineKeyboardButton(str(i), callback_data=i)
        but_days_31.row(d_but_1)
    else:
        d_but_1 = types.InlineKeyboardButton(str(i), callback_data=i)
        d_but_2 = types.InlineKeyboardButton(str(i + 1), callback_data=i + 1)
        d_but_3 = types.InlineKeyboardButton(str(i + 2), callback_data=i + 2)
        d_but_4 = types.InlineKeyboardButton(str(i + 3), callback_data=i + 3)
        d_but_5 = types.InlineKeyboardButton(str(i + 4), callback_data=i + 5)
        but_days_31.row(d_but_1, d_but_2, d_but_3, d_but_4, d_but_5)
    i += 5
naz_choise_mounth = types.InlineKeyboardButton('<< Назад', callback_data='back_choise_mounth')
but_days_31.add(naz_choise_mounth)



#Создаем кнопки - календарь (дни 30)
but_days_30 = types.InlineKeyboardMarkup(resize_keyboard=True)
i = 1
while i < 31:
    d3_but_1 = types.InlineKeyboardButton(str(i), callback_data=i)
    d3_but_2 = types.InlineKeyboardButton(str(i + 1), callback_data=i + 1)
    d3_but_3 = types.InlineKeyboardButton(str(i + 2), callback_data=i + 2)
    d3_but_4 = types.InlineKeyboardButton(str(i + 3), callback_data=i + 3)
    d3_but_5 = types.InlineKeyboardButton(str(i + 4), callback_data=i + 4)
    but_days_30.row(d3_but_1, d3_but_2, d3_but_3, d3_but_4, d3_but_5)
    i += 5
but_days_30.add(naz_choise_mounth)



#Создаем кнопки - календарь (дни 29)
but_days_29 = types.InlineKeyboardMarkup(resize_keyboard=True)
i = 1
while i < 30:
    if i == 26:
        d3_but_1 = types.InlineKeyboardButton(str(i), callback_data=i)
        d3_but_2 = types.InlineKeyboardButton(str(i + 1), callback_data=i + 1)
        d3_but_3 = types.InlineKeyboardButton(str(i + 2), callback_data=i + 2)
        d3_but_4 = types.InlineKeyboardButton(str(i + 3), callback_data=i + 3)
        but_days_29.row(d3_but_1, d3_but_2, d3_but_3, d3_but_4)
    else:
        d3_but_1 = types.InlineKeyboardButton(str(i), callback_data=i)
        d3_but_2 = types.InlineKeyboardButton(str(i + 1), callback_data=i + 1)
        d3_but_3 = types.InlineKeyboardButton(str(i + 2), callback_data=i + 2)
        d3_but_4 = types.InlineKeyboardButton(str(i + 3), callback_data=i + 3)
        d3_but_5 = types.InlineKeyboardButton(str(i + 4), callback_data=i + 4)
        but_days_29.row(d3_but_1, d3_but_2, d3_but_3, d3_but_4, d3_but_5)
    i += 5
but_days_29.add(naz_choise_mounth)



#Создаем кнопки - календарь (дни 28)
but_days_28 = types.InlineKeyboardMarkup(resize_keyboard=True)
i = 1
while i < 29:
    if i == 26:
        d3_but_1 = types.InlineKeyboardButton(str(i), callback_data=i)
        d3_but_2 = types.InlineKeyboardButton(str(i + 1), callback_data=i + 1)
        d3_but_3 = types.InlineKeyboardButton(str(i + 2), callback_data=i + 2)
        but_days_28.row(d3_but_1, d3_but_2, d3_but_3)
    else:
        d3_but_1 = types.InlineKeyboardButton(str(i), callback_data=i)
        d3_but_2 = types.InlineKeyboardButton(str(i + 1), callback_data=i + 1)
        d3_but_3 = types.InlineKeyboardButton(str(i + 2), callback_data=i + 2)
        d3_but_4 = types.InlineKeyboardButton(str(i + 3), callback_data=i + 3)
        d3_but_5 = types.InlineKeyboardButton(str(i + 4), callback_data=i + 4)
        but_days_28.row(d3_but_1, d3_but_2, d3_but_3, d3_but_4, d3_but_5)
    i += 5
but_days_28.add(naz_choise_mounth)



#Создаем кнопки времени
but_time = types.InlineKeyboardMarkup(resize_keyboard=True)
list_time = []
for i in range(0, 10):
    list_time.append('0' + str(i) + ':00')
for i in range(10, 24):
    list_time.append(str(i) + ':00')
i = 0
while i < len(list_time):
    b = types.InlineKeyboardButton(list_time[i], callback_data=list_time[i])
    b1 = types.InlineKeyboardButton(list_time[i + 1], callback_data=list_time[i + 1])
    b2 = types.InlineKeyboardButton(list_time[i + 2], callback_data=list_time[i + 2])
    b3 = types.InlineKeyboardButton(list_time[i + 3], callback_data=list_time[i + 3])
    but_time.row(b, b1, b2, b3)
    i += 4

but_main = types.InlineKeyboardMarkup(resize_keyboard=True)
naz = types.InlineKeyboardButton('<<< Главное меню', callback_data='main menu')
but_main.add(naz)



#Инструкция текст
information = """Я - бот для ведения дел. Данная инструкция поможет разобраться с моим интерфейсом.

\U0001F539 Вы можете вносить задачи, просматривать их, переносить или удалять;
\U0001F539 Вы также можете устанавливать и настраивать уведомления;
\U0001F539 Для удобства, практически для каждого действия, созданы специальные кнопки - нажимайте на них, чтобы не тратить своё драгоценное время;
\U0001F539 Общайтесь со мной текстом, я ещё не умею распознавать слова из фото, видео или аудио;
\U0001F539 Как заканчиваете общение со мной, нажимайте кнопку 'Выйти'.

Если возникнут трудности, пишите моему создателю - @be9emot."""
