import aiogram
from aiogram.utils import executor
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
import datetime

from connect import connection, cursor
from admin import bot, dp
from BUTS import blocnote_buts, but_today, but, but_year, but_month, but_days_31, but_days_30, but_days_29, \
    but_days_28, month, but_1, information, tasks_but, but_all_choise, but_delete_all, but_next_other, but_per, but_year_res, but_time, \
    but_main, but_not, naz_back
from defs_to_bot_TODO import add_tasks, show_all, choise_date, task, but_tasks, delete_list, reschedule_f, noti_date, noti_task


'''Создание таблицы, если нужно'''
# table = 'CREATE TABLE IF NOT EXISTS `list_del`(`N` INT AUTO_INCREMENT, `id` INT NOT NULL, ' \
#         '`dates` DATE NOT NULL, `active tasks` VARCHAR(128), `time_notify` VARCHAR(12), `complite tasks` VARCHAR(128), PRIMARY KEY(`N`))'
# cursor.execute(table)


'''Классы'''
class start_menu(StatesGroup):
    menu_blocknot_state = State()
    main_state = State()

class show(StatesGroup):
    list_active_or_no_state = State()
    all_list_or_choise_data_state = State()
    tasks_to_data_state = State()

class add(StatesGroup):
    add_today_tomorrow_or_no_state = State()
    add_task_state = State()
    add_notification_or_no_state = State()
    time_notification_state = State()
    vvod_time_state = State()
    choise_mounth_state = State()
    choise_day_state = State()
    add_task_to_list_state = State()

class task_in_list_complete(StatesGroup):
    choise_task_state = State()
    reschedule_task_state = State()

class delete(StatesGroup):
    delete_all_or_no_state = State()
    del_comp_task_state = State()
    del_all_task_state = State()
    choise_task_delete_state = State()
    delete_task_state = State()

class reschedule(StatesGroup):
    data_choise_state = State()
    task_choise_state = State()
    day_choise_state = State()

class notific(StatesGroup):
    setting_state = State()
    date_and_task_state = State()
    time_state = State()
    add_noti_state = State()
    dele_state = State()

'''Команды'''
# @dp.message_handler(state = '*', commands=['start'])
async def start(message: aiogram.types.Message, state: FSMContext):
    id = message.chat.id
    current_state = await state.get_state()
    if current_state is not None:
        await state.finish()
    await bot.send_message(id, 'Привет! Рад вас видеть. Открываю блокнот.', reply_markup=blocnote_buts)
    await start_menu.menu_blocknot_state.set()

# @dp.message_handler(state = '*', commands=['info'])
async def info(message: aiogram.types.Message, state: FSMContext):
    id = message.chat.id
    current_state = await state.get_state()
    if current_state is not None:
        await state.finish()
    await bot.send_message(id, information, reply_markup=aiogram.types.ReplyKeyboardRemove())

# @dp.message_handler(state = '*', commands=['notification'])
async def notif(message: aiogram.types.Message, state: FSMContext):
    id = message.chat.id
    await bot.send_message(id, 'Хотите настроить уведомления?', reply_markup=but_not)
    await notific.setting_state.set()


'''Настройка уведомлений'''
# @dp.callback_query_handler(state = notific.setting_state)
async def setting(callback: aiogram.types.CallbackQuery):
    id = callback.message.chat.id
    global text_noti

    if callback.data == 'watch':
        select = f'SELECT dates, `active tasks`, `time_notify` FROM list_del WHERE id = {id} AND `active tasks` is not NULL ' \
                 f'AND `time_notify` is not NULL ORDER BY `dates`, `time_notify`'
        cursor.execute(select)
        li = cursor.fetchall()
        text_mes = ''
        if li != ():
            for el in li:
                dat = str(el['dates']).split('-')
                norm_dat = dat[2] + '.' + dat[1] + '.' + dat[0]
                text_mes += norm_dat + ':\n' + el['active tasks'] + '\nВремя напоминания: ' + el['time_notify'] + '\n\n'
            await bot.send_message(id, text_mes, reply_markup=but_not)
        else:
            await bot.send_message(id, 'У вас нет уведомлений.', reply_markup=but_not)
        await notific.setting_state.set()

    elif callback.data == 'delete_not':
        text_noti = 'del'
        select = f'SELECT dates, `active tasks`, `time_notify` FROM list_del WHERE id = {id} AND `active tasks` is not NULL ' \
                 f'AND `time_notify` is not NULL ORDER BY `dates`, `time_notify`'
        cursor.execute(select)
        if cursor.fetchall() != ():
            await bot.send_message(id, 'Выберите дату задачи, с которой хотите снять напоминание.', reply_markup=noti_date(id, 'back', 'is not'))
            await notific.date_and_task_state.set()
        else:
            await bot.send_message(id, 'У вас нет уведомлений. Удалять ничего не нужно.', reply_markup=but_not)
            await notific.setting_state.set()

    elif callback.data == 'add_not':
        text_noti = 'add'
        select = f'SELECT dates, `active tasks` FROM list_del WHERE id = {id} AND `active tasks` is not NULL ' \
                 f'ORDER BY `dates`'
        cursor.execute(select)
        if cursor.fetchall() != ():
            await bot.send_message(id, 'Выберите дату задачи, для которой хотите установить напоминание.', reply_markup=noti_date(id, 'back', 'is'))
            await notific.date_and_task_state.set()
        else:
            await bot.send_message(id, 'Список активных задач пуст. Установить уведомление невозможно.', reply_markup=but_not)
            await notific.setting_state.set()

# @dp.callback_query_handler(state = notific.date_and_task_state)
async def date_and_task(callback: aiogram.types.CallbackQuery):
    id = callback.message.chat.id

    if callback.data == 'back':
        await bot.send_message(id, 'Возвращаюсь к настройкам уведомлений.', reply_markup=but_not)
        await notific.setting_state.set()

    else:
        global data_noti
        data_noti = (datetime.datetime.strptime(callback.data, '%d.%m.%Y')).date()
        if text_noti == 'del':
            await bot.send_message(id, 'Выберите задачу, с которой хотите снять напоминание.', reply_markup=noti_task(id, data_noti, 'back', 'is not'))
            await notific.dele_state.set()
        else:
            await bot.send_message(id, 'Выберите задачу, на которую хотите установить напоминание.', reply_markup=noti_task(id, data_noti, 'back', 'is'))
            await notific.time_state.set()

#@dp.callback_query_handler(state = notific.dele_state)
async def dele(callback: aiogram.types.CallbackQuery, state = FSMContext):
    id = callback.message.chat.id

    if callback.data == 'back':
        await bot.send_message(id, 'Выберите дату задачи.', reply_markup=noti_date(id, 'back', 'is not'))
        await notific.date_and_task_state.set()

    else:
        update = f"UPDATE list_del SET `time_notify` = NULL WHERE id = {id} AND dates = '{data_noti}' AND" \
                 f"`active tasks` = '{callback.data}'"
        cursor.execute(update)
        connection.commit()
        await bot.send_message(id, 'Напоминание удалено.')
        await state.finish()

#@dp.callback_query_handler(state = notific.time_state_state)
async def time(callback: aiogram.types.CallbackQuery, state = FSMContext):
    id = callback.message.chat.id

    if callback.data == 'back':
        await bot.send_message(id, 'Выберите дату задачи.', reply_markup=noti_date(id, 'back', 'is'))
        await notific.date_and_task_state.set()

    else:
        global task_noti
        task_noti = callback.data
        await bot.send_message(id, 'Выберите время напоминания.', reply_markup=but_time)
        await notific.add_noti_state.set()

# @dp.callback_query_handler(state = notific.add_noti_state)
async def add_noti(callback: aiogram.types.CallbackQuery, state = FSMContext):
    id = callback.message.chat.id

    if callback.data == 'main menu':
        await bot.send_message(id, 'Выберите задачу, на которую хотите установить напоминание.', reply_markup=noti_task(id, data_noti, 'back', 'is'))
        await notific.time_state.set()

    else:
        update = f"UPDATE list_del SET `time_notify` = '{callback.data}' WHERE id = {id} AND " \
                 f"dates = '{data_noti}' AND `active tasks` = '{task_noti}'"
        cursor.execute(update)
        connection.commit()
        await bot.send_message(id, 'Напоминание установлено.')
        await state.finish()


'''Откладываем напоминание или задача выполнена'''
# @dp.callback_query_handler(lambda callback: 'call' in callback.data, state = '*')
async def notification(callback: aiogram.types.CallbackQuery, state: FSMContext):
    id = callback.message.chat.id
    global Nom
    Nom = int(callback.data.split('/')[2])
    global taskN
    taskN = callback.data.split('/')[3]
    current_state = await state.get_state()
    if current_state is not None:
        await state.finish()

    if callback.data.split('/')[1] == '15' or callback.data.split('/')[1] == '30' or callback.data.split('/')[1] == '60':
        time_new = (datetime.datetime.now() + datetime.timedelta(minutes=int(callback.data.split('/')[1]))).time()
        date_new = (datetime.datetime.now() + datetime.timedelta(minutes=int(callback.data.split('/')[1]))).date()
        time_task = str(datetime.time.strftime(time_new, '%H:%M'))
        update = f"UPDATE list_del SET dates = '{date_new}', time_notify = '{time_task}' WHERE N = {Nom}"
        cursor.execute(update)
        connection.commit()
        await bot.send_message(id, 'Напоминание перенесено.', reply_markup=but_main)
        await start_menu.main_state.set()

    elif callback.data.split('/')[1] == 'time':
        await bot.send_message(id, 'Введите время в формате: 18:00')
        await add.vvod_time_state.set()

    elif callback.data.split('/')[1] == 'comp':
        update = f"UPDATE list_del SET `active tasks` = NULL, `time_notify` = NULL, `complite tasks` = '{taskN}' WHERE N = {Nom}"
        cursor.execute(update)
        connection.commit()
        await bot.send_message(id, 'Задача перенесена в список выполненных дел.', reply_markup=but_main)
        await start_menu.main_state.set()

# @dp.message_handler(state = add.vvod_time_state)
async def vvod_time(message: aiogram.types.Message):
    id = message.chat.id

    try:
        time_vvod = str(datetime.datetime.strptime(message.text, '%H:%M').time()).split(':')
        time_vvod = time_vvod[0] + ':' + time_vvod[1]
        update = f"UPDATE `list_del` SET `time_notify` = '{time_vvod}' WHERE N = {Nom}"
        cursor.execute(update)
        connection.commit()
        await bot.send_message(id, 'Напоминание установлено.', reply_markup=but_main)
        await start_menu.main_state.set()
    except:
        await bot.send_message(id, 'Неверные формат времени! Попробуйте ещё раз.')
        await add.vvod_time_state.set()


'''Основное меню блокнота'''
# @dp.callback_query_handler(state = start_menu.menu_blocknot_state)
async def menu_blocknot(callback: aiogram.types.CallbackQuery, state = FSMContext):
    id = callback.message.chat.id

    if callback.data == 'show_list_tasks':
        select = f'SELECT * FROM list_del WHERE id = {id}'
        cursor.execute(select)
        if cursor.fetchall() != ():
            await bot.send_message(id, 'Какой список хотите посмотреть?', reply_markup=tasks_but)
            await show.list_active_or_no_state.set()
        else:
            await bot.send_message(id, 'Ваш список пуст.', reply_markup=but_main)
            await start_menu.main_state.set()

    elif callback.data == 'add_task':
        await bot.send_message(id, 'Добавить задачу на сегодня, завтра или другой день?', reply_markup=but_today)
        await add.add_today_tomorrow_or_no_state.set()

    elif callback.data == 'reschedule_task_in_list_complete':
        select = f'SELECT dates FROM list_del WHERE id = {id} AND `active tasks` is not NULL'
        cursor.execute(select)
        if cursor.fetchall() != ():
            global list_data
            list_data = choise_date(id, 'active tasks', 'but_back_menu')[0]
            await bot.send_message(id, 'Выберите дату задачи, которую хотите переместить в список выполненных.', reply_markup=choise_date(id, 'active tasks', 'but_back_menu')[1])
            await task_in_list_complete.choise_task_state.set()
        else:
            await bot.send_message(id, 'У вас нет активных дел. Нельзя перенести несуществующую задачу.', reply_markup=but_main)
            await start_menu.main_state.set()

    elif callback.data == 'reschedule_task_another_day':
        select = f'SELECT `active tasks` FROM list_del WHERE id = {id} AND `active tasks` is not NULL'
        cursor.execute(select)
        if cursor.fetchall() != ():
            await bot.send_message(id, 'Выберите дату задачи, которую хотите перенести.', reply_markup=choise_date(id, 'active tasks', 'naz_menu')[1])
            await reschedule.data_choise_state.set()
        else:
            await bot.send_message(id, 'Ваш список пуст. Переносить ничего не нужно.', reply_markup=but_main)
            await start_menu.main_state.set()

    elif callback.data == 'delete_task':
        select = f'SELECT `dates` FROM list_del WHERE id = {id} AND (`active tasks` is not NULL OR `complite tasks` is not NULL)'
        cursor.execute(select)
        if cursor.fetchall() != ():
            await bot.send_message(id, 'Выберите, что будем удалять.', reply_markup=but_delete_all)
            await delete.delete_all_or_no_state.set()
        else:
            await bot.send_message(id, 'Ваш список пуст. Удалять нечего.', reply_markup=but_main)
            await start_menu.main_state.set()

    elif callback.data == 'show_list_tasks_today':
        data_today = datetime.date.today()
        select = f"SELECT `active tasks` FROM list_del WHERE id = {id} AND dates = '{data_today}' AND `active tasks` is not NULL"
        cursor.execute(select)
        data_today = str(data_today).split('-')
        data_today = data_today[2] + '.' + data_today[1] + '.' + data_today[0]
        list_tasks = cursor.fetchall()
        text_res = ''
        if list_tasks != ():
            for el in list_tasks:
                text_res += el['active tasks'] + '\n'
            await bot.send_message(id, data_today + ':\n' + text_res, reply_markup=but_main)
        else:
            await bot.send_message(id, 'На сегодня никаких дел не запланировано.', reply_markup=but_main)
        await start_menu.main_state.set()

    elif callback.data == 'exit':
        await bot.send_message(id, 'Пока-пока, возвращайтесь скорее!', reply_markup=aiogram.types.ReplyKeyboardRemove())
        await state.finish()


'''Ответочка на кнопочку <<< Главное меню'''
# @dp.callback_query_handler(state=start_menu.main_state)
async def main(callback: aiogram.types.CallbackQuery):
    id = callback.message.chat.id
    if callback.data == 'main menu':
        await bot.send_message(id, 'Возвращаюсь в меню блокнота.', reply_markup=blocnote_buts)
        await start_menu.menu_blocknot_state.set()


'''Состояния для "посмотреть список дел" '''
# @dp.callback_query_handler(state=show.list_active_or_no_state)
async def list_active_or_no(callback: aiogram.types.CallbackQuery):
    id = callback.message.chat.id
    global text

    if callback.data == 'active_tasks_list':
        text = 'active tasks'
        select = f'SELECT `active tasks` FROM list_del WHERE id = {id} AND `active tasks` is not NULL'
        cursor.execute(select)
        if cursor.fetchall() != ():
            await bot.send_message(id, 'Показать весь список активных дел или выбрать дату?', reply_markup=but_all_choise)
            await show.all_list_or_choise_data_state.set()
        else:
            await bot.send_message(id, 'У вас нет активных дел.', reply_markup=tasks_but)
            await show.list_active_or_no_state.set()

    elif callback.data == 'complete_tasks_list':
        text = 'complite tasks'
        select = f'SELECT `complite tasks` FROM list_del WHERE id = {id} AND `complite tasks` is not NULL'
        cursor.execute(select)
        if cursor.fetchall() != ():
            await bot.send_message(id, 'Показать весь список выполненных дел или выбрать дату?', reply_markup=but_all_choise)
            await show.all_list_or_choise_data_state.set()
        else:
            await bot.send_message(id, 'У вас нет выполненных дел.', reply_markup=tasks_but)
            await show.list_active_or_no_state.set()

    elif callback.data == 'but_back_menu':
        await bot.send_message(id, 'Возвращаюсь обратно.', reply_markup=blocnote_buts)
        await start_menu.menu_blocknot_state.set()

# @dp.callback_query_handler(state=show.all_list_or_choise_data_state)
async def all_list_or_choise_data(callback: aiogram.types.CallbackQuery):
    id = callback.message.chat.id

    if callback.data == 'all_list':
        await bot.send_message(id, show_all(id, text), reply_markup=but_main)
        await start_menu.main_state.set()

    elif callback.data == 'choise_date':
        global date_list
        date_list = choise_date(id, text, 'but_back_allchoise')[0]
        await bot.send_message(id, 'Выберите дату, на которую хотите посмотреть список дел.', reply_markup=choise_date(id, text, 'but_back_allchoise')[1])
        await show.tasks_to_data_state.set()

    elif callback.data == 'show_tasks':
        await bot.send_message(id, 'Возвращаюсь обратно.', reply_markup=tasks_but)
        await show.list_active_or_no_state.set()

# @dp.callback_query_handler(state=show.tasks_to_data_state)
async def tasks_to_data(callback: aiogram.types.CallbackQuery):
    id = callback.message.chat.id

    if callback.data == 'but_back_allchoise':
        await bot.send_message(id, 'Показать весь список активных дел или выбрать дату?', reply_markup=but_all_choise)
        await show.all_list_or_choise_data_state.set()

    else:
        await bot.send_message(id, task(id, callback.data, text), reply_markup=but_main)
        await start_menu.main_state.set()


'''Состояния для "добавить задачу" '''
# @dp.callback_query_handler(state=add.add_today_tomorrow_or_no_state)
async def add_today_tomorrow_or_no(callback: aiogram.types.CallbackQuery):
    id = callback.message.chat.id
    global text
    text = 'add'

    if callback.data == 'but_today' or callback.data == 'but_tomorrow':
        await bot.send_message(id, 'Введите задачу.\nВнимание! За один раз можно внести только одну задачу.')
        global dates
        if callback.data == 'but_today':
            dates = datetime.date.today()
        else:
            dates = datetime.date.today() + datetime.timedelta(days=1)
        await add.add_task_state.set()

    elif callback.data == 'but_anotherday':
        await bot.send_message(id, 'Выберите год.', reply_markup=but_year)
        await add.choise_mounth_state.set()

    elif callback.data == 'but_back_menu':
        await bot.send_message(id, 'Возвращаюсь в меню блокнота.', reply_markup=blocnote_buts)
        await start_menu.menu_blocknot_state.set()

# @dp.message_handler(state=add.add_task_state)
async def add_task(message: aiogram.types.Message):
    id = message.chat.id
    global taskk
    taskk = message.text
    await bot.send_message(id, add_tasks(id, dates, taskk, 'добавлена'), reply_markup=but)
    await add.add_notification_or_no_state.set()

# @dp.callback_query_handler(state=add.add_notification_or_no_state)
async def add_notification_or_no(callback: aiogram.types.CallbackQuery):
    id = callback.message.chat.id

    if callback.data == 'but_no':
        await bot.send_message(id, 'Хорошо!', reply_markup=but_main)
        await start_menu.main_state.set()

    elif callback.data == 'but_yes':
        await bot.send_message(id, 'Я напомню в день выполнения задачи. Выберите время напоминания.', reply_markup=but_time)
        await add.time_notification_state.set()

# @dp.callback_query_handler(state=add.choise_mounth_state)
async def choise_mounth(callback: aiogram.types.CallbackQuery):
    id = callback.message.chat.id
    global year

    if callback.data == 'back_choise_data':
        await bot.send_message(id, 'Добавить задачу на сегодня, завтра или другой день?', reply_markup=but_today)
        await add.add_today_tomorrow_or_no_state.set()

    elif callback.data == 'now_year':
        year = str(datetime.datetime.now().year)
        await bot.send_message(id, 'Выберите месяц.', reply_markup=but_month)
        await add.choise_day_state.set()

    elif callback.data == 'back':
        await bot.send_message(id, 'Задачу перенести на последующий день? Или выбрать другую дату?', reply_markup=but_per)
        await reschedule.day_choise_state.set()

    elif callback.data == 'next_year':
        year = str(datetime.datetime.now().year + 1)
        await bot.send_message(id, 'Выберите месяц.', reply_markup=but_month)
        await add.choise_day_state.set()

# @dp.callback_query_handler(state=add.choise_day_state)
async def choise_day(callback: aiogram.types.CallbackQuery):
    id = callback.message.chat.id

    if callback.data == 'back_choise_year':
        if text == 'add':
            await bot.send_message(id, 'Выберите год.', reply_markup=but_year)
        elif text == 'resch':
            await bot.send_message(id, 'Выберите год.', reply_markup=but_year_res)
        await add.choise_mounth_state.set()

    else:
        global mounth
        mounth = str(int(month.index(callback.data)) + 1)

        if callback.data in [month[0], month[2], month[4], month[6], month[7], month[9], month[11]]:
            await bot.send_message(id, 'Выберите день.', reply_markup=but_days_31)

        elif callback.data in [month[3], month[5], month[8], month[10]]:
            await bot.send_message(id, 'Выберите день.', reply_markup=but_days_30)

        elif callback.data in [month[1]]:

            if int(year) % 4 == 0:
                a = True
                if int(year) % 100 == 0:
                    a = False
                    if int(year) % 400 == 0:
                        a = True
            else:
                a = False

            if a == True:
                await bot.send_message(id, 'Выберите день.', reply_markup=but_days_29)

            elif a == False:
                await bot.send_message(id, 'Выберите день.', reply_markup=but_days_28)
        await add.add_task_to_list_state.set()

# @dp.callback_query_handler(state=add.add_task_to_list_state)
async def add_task_to_list(callback: aiogram.types.CallbackQuery):
    id = callback.message.chat.id

    if callback.data == 'back_choise_mounth':
        await bot.send_message(id, 'Выберите месяц.', reply_markup=but_month)
        await add.choise_day_state.set()
    else:
        day = str(callback.data)
        data_time = datetime.datetime.strptime(year + '.' + mounth + '.' + day, '%Y.%m.%d')
        global dates
        dates = data_time.date()
        if text == 'add':
            await bot.send_message(id, 'Введите задачу.\nВнимание! За один раз можно внести только одну задачу.')
            await add.add_task_state.set()
        elif text == 'resch':
            await bot.send_message(id, add_tasks(id, dates, taskk, 'перенесена'), reply_markup=but)
            reschedule_f(id, data_per)
            await add.add_notification_or_no_state.set()

# @dp.callback_query_handler(state=add.time_notification_state)
async def time_notification(callback: aiogram.types.CallbackQuery):
    id = callback.message.chat.id

    update = f"UPDATE `list_del` SET `time_notify` = '{callback.data}' WHERE id = {id} AND dates = '{dates}' AND `active tasks` = '{taskk}'"
    cursor.execute(update)
    connection.commit()
    await bot.send_message(id, 'Напоминание установлено.', reply_markup=but_main)
    await start_menu.main_state.set()


'''Состояния для "перенести задачу в список выполненных" '''
# @dp.callback_query_handler(state = task_in_list_complete.choise_task_state)
async def choise_task(callback: aiogram.types.CallbackQuery):
    id = callback.message.chat.id

    if callback.data == 'but_back_menu':
        await bot.send_message(id, 'Возвращаюсь обратно.', reply_markup=blocnote_buts)
        await start_menu.menu_blocknot_state.set()

    else:
        global data_0
        data_0 = (datetime.datetime.strptime(callback.data, '%d.%m.%Y')).date()
        await bot.send_message(id, 'Выберите задачу, которую хотите перенести.', reply_markup=but_tasks(id, callback.data, 'but_back_data'))
        await task_in_list_complete.reschedule_task_state.set()

# @dp.callback_query_handler(state = task_in_list_complete.reschedule_task_state)
async def reschedule_task(callback: aiogram.types.CallbackQuery):
    id = callback.message.chat.id

    if callback.data == 'but_back_data':
        await bot.send_message(id, 'Выберите дату задачи, которую хотите перенести в список выполненных.', reply_markup=choise_date(id, 'active tasks', 'but_back_menu')[1])
        await task_in_list_complete.choise_task_state.set()

    else:
        update = f"UPDATE list_del SET `active tasks` = NULL, `complite tasks` = '{callback.data}', `time_notify` = NULL WHERE id = {id} AND dates = '{data_0}' AND `active tasks` = '{callback.data}'"
        cursor.execute(update)
        connection.commit()
        await bot.send_message(id, 'Готово!', reply_markup=but_main)
        await start_menu.main_state.set()


'''Состояния для "удалить" '''
# @dp.callback_query_handler(state = delete.delete_all_or_no_state)
async def delete_all_or_no(callback: aiogram.types.CallbackQuery):
    id = callback.message.chat.id

    if callback.data == 'but_back_menu':
        await bot.send_message(id, 'Возвращаюсь назад.', reply_markup=blocnote_buts)
        await start_menu.menu_blocknot_state.set()

    elif callback.data == 'all_complete_tasks':
        select = f'SELECT `complite tasks` FROM list_del WHERE id = {id} AND `complite tasks` is not NULL'
        cursor.execute(select)
        if cursor.fetchall() != ():
            await bot.send_message(id, 'Уверены, что хотите удалить все выполненные задачи?', reply_markup=but)
            await delete.del_comp_task_state.set()
        else:
            await bot.send_message(id, 'Список выполненных задач пуст.', reply_markup=but_delete_all)
            await delete.delete_all_or_no_state.set()

    elif callback.data == 'choise_task':
        data_list_delete = choise_date(id, 'active tasks', 'naz_delete')[0]
        await bot.send_message(id, 'Выберите дату задачи.', reply_markup=choise_date(id, 'active tasks', 'naz_delete')[1])
        await delete.choise_task_delete_state.set()

    elif callback.data == 'all_tasks_delete':
        await bot.send_message(id, 'Уверены, что хотите очистить весь список?', reply_markup=but)
        await delete.del_all_task_state.set()

# @dp.callback_query_handler(state = delete.del_all_task_state)
async def del_all_task(callback: aiogram.types.CallbackQuery):
    id = callback.message.chat.id

    if callback.data == 'but_yes':
        deletee = f'DELETE FROM list_del WHERE id = {id}'
        cursor.execute(deletee)
        connection.commit()
        await bot.send_message(id, 'Весь список был очищен.', reply_markup=but_main)
        await start_menu.main_state.set()

    elif callback.data == 'but_no':
        await bot.send_message(id, 'Ок! Выберите, что будем удалять.', reply_markup=but_delete_all)
        await delete.delete_all_or_no_state.set()

# @dp.callback_query_handler(state = delete.del_comp_task_state)
async def del_comp_task(callback: aiogram.types.CallbackQuery):
    id = callback.message.chat.id

    if callback.data == 'but_yes':
        update = f'UPDATE list_del SET `complite tasks` = NULL WHERE id = {id}'
        cursor.execute(update)
        connection.commit()
        delete_list(id)
        await bot.send_message(id, 'Готово!', reply_markup=but_main)
        await start_menu.main_state.set()

    elif callback.data == 'but_no':
        await bot.send_message(id, 'Ок! Выберите, что будем удалять.', reply_markup=but_delete_all)
        await delete.delete_all_or_no_state.set()

# @dp.callback_query_handler(state = delete.choise_task_delete_state)
async def choise_task_delete(callback: aiogram.types.CallbackQuery):
    id = callback.message.chat.id

    if callback.data == 'naz_delete':
        await bot.send_message(id, 'Выберите, что будем удалять.', reply_markup=but_delete_all)
        await delete.delete_all_or_no_state.set()

    else:
        global data_1
        data_1 = (datetime.datetime.strptime(callback.data, '%d.%m.%Y')).date()
        await bot.send_message(id, 'Выберите задачу.', reply_markup=but_tasks(id, callback.data, 'naz_data_delete'))
        await delete.delete_task_state.set()

# @dp.callback_query_handler(state = delete.delete_task_state)
async def delete_task(callback: aiogram.types.CallbackQuery):
    id = callback.message.chat.id

    if callback.data == 'naz_data_delete':
        await bot.send_message(id, 'Выберите дату задачи.', reply_markup=choise_date(id, 'active tasks', 'naz_delete')[1])
        await delete.choise_task_delete_state.set()

    else:
        update = f"UPDATE list_del SET `active tasks` = NULL WHERE id = {id} AND dates = '{data_1}' AND `active tasks` = '{callback.data}'"
        cursor.execute(update)
        connection.commit()
        delete_list(id)
        await bot.send_message(id, 'Задача удалена из списка.', reply_markup=but_main)
        await start_menu.main_state.set()


'''Состояния для "перенести задачу на другой день"'''
# @dp.callback_query_handler(state = reschedule.data_choise_state)
async def data_choise(callback: aiogram.types.CallbackQuery):
    id = callback.message.chat.id

    if callback.data == 'naz_menu':
        await bot.send_message(id, 'Возвращаюсь в меню блокнота.', reply_markup=blocnote_buts)
        await start_menu.menu_blocknot_state.set()

    else:
        global data_per
        data_per = callback.data
        await bot.send_message(id, 'Выберите задачу, которую хотите перенести.', reply_markup=but_tasks(id, callback.data, 'naz_data'))
        await reschedule.task_choise_state.set()

# @dp.callback_query_handler(state = reschedule.task_choise_state)
async def task_choise(callback: aiogram.types.CallbackQuery):
    id = callback.message.chat.id

    if callback.data == 'naz_data':
        await bot.send_message(id, 'Выберите дату задачи, которую хотите перенести.', reply_markup=choise_date(id, 'active tasks', 'naz_menu')[1])
        await reschedule.data_choise_state.set()

    else:
        global taskk
        taskk = callback.data
        await bot.send_message(id, 'Задачу перенести на последующий день? Или выбрать другую дату?', reply_markup=but_next_other)
        await reschedule.day_choise_state.set()

# @dp.callback_query_handler(state = reschedule.day_choise_state)
async def day_choise(callback: aiogram.types.CallbackQuery):
    id = callback.message.chat.id

    if callback.data == 'but_back_task':
        await bot.send_message(id, 'Выберите задачу, которую хотите перенести.', reply_markup=but_tasks(id, data_per, 'naz_data'))
        await reschedule.task_choise_state.set()

    elif callback.data == 'next':
        global dates
        dates = (datetime.datetime.strptime(data_per, '%d.%m.%Y')).date() + datetime.timedelta(days=1)
        await bot.send_message(id, add_tasks(id, dates, taskk, 'перенесена'), reply_markup=but)
        reschedule_f(id, data_per, taskk)
        await add.add_notification_or_no_state.set()

    elif callback.data == 'anotherday':
        global text
        text = 'resch'
        await bot.send_message(id, 'Выберите год.', reply_markup=but_year_res)
        await add.choise_mounth_state.set()



'''Регистрация хендлеров'''
def register(dp: aiogram.Dispatcher):
    dp.register_message_handler(start, commands=['start'], state='*')
    dp.register_message_handler(info, commands=['info'], state='*')
    dp.register_message_handler(notif, commands=['notification'], state='*')
    dp.register_callback_query_handler(notification, lambda callback: 'call' in callback.data, state='*')
    dp.register_message_handler(vvod_time, state=add.vvod_time_state)
    dp.register_callback_query_handler(menu_blocknot, state=start_menu.menu_blocknot_state)
    dp.register_callback_query_handler(main, state=start_menu.main_state)
    dp.register_callback_query_handler(list_active_or_no, state=show.list_active_or_no_state)
    dp.register_callback_query_handler(all_list_or_choise_data, state=show.all_list_or_choise_data_state)
    dp.register_callback_query_handler(tasks_to_data, state=show.tasks_to_data_state)
    dp.register_callback_query_handler(add_today_tomorrow_or_no, state=add.add_today_tomorrow_or_no_state)
    dp.register_message_handler(add_task, state=add.add_task_state)
    dp.register_callback_query_handler(add_notification_or_no, state=add.add_notification_or_no_state)
    dp.register_callback_query_handler(choise_mounth, state=add.choise_mounth_state)
    dp.register_callback_query_handler(choise_day, state=add.choise_day_state)
    dp.register_callback_query_handler(add_task_to_list, state=add.add_task_to_list_state)
    dp.register_callback_query_handler(time_notification, state=add.time_notification_state)
    dp.register_callback_query_handler(choise_task, state=task_in_list_complete.choise_task_state)
    dp.register_callback_query_handler(reschedule_task, state=task_in_list_complete.reschedule_task_state)
    dp.register_callback_query_handler(delete_all_or_no, state=delete.delete_all_or_no_state)
    dp.register_callback_query_handler(del_comp_task, state=delete.del_comp_task_state)
    dp.register_callback_query_handler(del_all_task, state=delete.del_all_task_state)
    dp.register_callback_query_handler(choise_task_delete, state=delete.choise_task_delete_state)
    dp.register_callback_query_handler(delete_task, state=delete.delete_task_state)
    dp.register_callback_query_handler(data_choise, state=reschedule.data_choise_state)
    dp.register_callback_query_handler(task_choise, state=reschedule.task_choise_state)
    dp.register_callback_query_handler(day_choise, state=reschedule.day_choise_state)
    dp.register_callback_query_handler(setting, state=notific.setting_state)
    dp.register_callback_query_handler(date_and_task, state=notific.date_and_task_state)
    dp.register_callback_query_handler(time, state=notific.time_state)
    dp.register_callback_query_handler(add_noti, state=notific.add_noti_state)
    dp.register_callback_query_handler(dele, state=notific.dele_state)

