import random

from aiogram.types import (InlineKeyboardMarkup, InlineKeyboardButton)
from aiogram.utils.keyboard import InlineKeyboardBuilder
import time
import locale
import calendar

locale.setlocale(locale.LC_TIME, 'Russian_Russia.1251')  # Для Windows

settings=InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Обратиться за помощью к менеджеру',
                          url='https://t.me/Natochike', callback_data='help_manager')],
    [InlineKeyboardButton(text='Что мы предлагаем', callback_data='offers')]
])

menu = ['Вводный урок', 'Преподаватели', 'Наши курсы', 'FAQ',
        'Отзывы', 'Акции', 'Назад (возврат в главное меню)']

async def inline_menu():
    keyboard = InlineKeyboardBuilder()
    i=0
    for step in menu:
        i+=1
        keyboard.add(InlineKeyboardButton(text=step, callback_data=f'step_{i}'))
    return keyboard.adjust(2).as_markup()

introduce = ['Запись на урок', 'Назад']
async def inline_intro():
    keyboard = InlineKeyboardBuilder()
    i=0
    for step in introduce:
        i+=1
        keyboard.add(InlineKeyboardButton(text=step, callback_data=f'intro_{i}'))
    return keyboard.adjust(1).as_markup()

async def inline_back(): # прикручивается только если эта кнопка единственная, возврат в главное меню ПОЛЬЗОВАТЕЛЯ
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text='Назад', callback_data='intro_2'))
    return keyboard.adjust(1).as_markup()

data=time.localtime()
# список трёх всегда актуальных месяцев
months = [time.strftime("%B", data), time.strftime("%B", time.strptime(str(data.tm_mon+1), "%m")), time.strftime("%B", time.strptime(str(data.tm_mon+2), "%m"))]

async def inline_calendar():
    keyboard = InlineKeyboardBuilder()
    i=0
    for month in months:
        keyboard.add(InlineKeyboardButton(text=months[i], callback_data=f'month_{i}'))
        i+=1
    keyboard.add(InlineKeyboardButton(text='Вернуться к описанию занятия', callback_data='back_from_calendar'))
    return keyboard.adjust(3).as_markup()

row = 3
col = 32
matrix_free = [[[] for _ in range(col)] for _ in range(row)]
for i in range(row):
    for j in range(col):
        for k in range(random.randint(1,3)):
            matrix_free[i][j].append(f'{j} {months[i]} в 1{k}:00')

matrix_busy = [[[] for _ in range(col)] for _ in range(row)]
# абсолютно такая же матрица, но пустая
# по мере продвижения сюда кладутся занятые слоты

def days_in_month_by_name(month_name, year=None):
    if year is None:
        year = time.localtime().tm_year
    t = time.strptime(f"{month_name} {year}", "%B %Y")
    month = t.tm_mon
    return calendar.monthrange(year, month)[1]

async def month_to_register(i: int):
    keyboard = InlineKeyboardBuilder()

    for j in range(1, days_in_month_by_name(months[i])+1):
        keyboard.add(InlineKeyboardButton(text=str(j), callback_data=f'record_month_{i}_day_{j}'))
    #добавление пустышек для равномерного распределения кнопок
    if (j<35):
        for _ in range(35-j):
            keyboard.add(InlineKeyboardButton(text=' ', callback_data='empty_button'))
    keyboard.add(InlineKeyboardButton(text="Вернуться к выбору месяца", callback_data='back_from_record'))
    return keyboard.adjust(7).as_markup()

# на каждый день выводит свои записи
async def records_for_data(day: int, month: int):
    keyboard = InlineKeyboardBuilder()
    #это сработает если нет дублей, если буду дубли - удалять надо будет по индексу
    for _ in matrix_free[month][day]:
        keyboard.add(InlineKeyboardButton(text=_.lower(), callback_data=f'successful_record_{month}_day_{day}_{_}'))
    keyboard.add(InlineKeyboardButton(text="Вернуться к выбору даты", callback_data=f'back_from_choose_{month}'))
    return keyboard.adjust(1).as_markup()

async def delete_free_add_busy(day: int, month: int, value: str, contact_info: str):
    matrix_free[month][day].remove(value)
    matrix_busy[month][day].append(value+" "+contact_info)
    print(matrix_busy)

admin_keyboard=InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Просмотр заявок на вводный урок', callback_data='look_records')],
    [InlineKeyboardButton(text='Управление календарём', callback_data='change_calendar'),
    InlineKeyboardButton(text='Редактировать FAQ', callback_data='edit_FAQ')],
    [InlineKeyboardButton(text='Редактировать отзывы', callback_data='edit_review'),
    InlineKeyboardButton(text='Редактировать акции', callback_data='edit_sales')]])

async def inline_admin_calendar_to_look():
    keyboard = InlineKeyboardBuilder()
    i = 0
    for month in months:
        keyboard.add(InlineKeyboardButton(text=months[i], callback_data=f'rec_month_{month}_{i}'))
        i += 1
    keyboard.add(InlineKeyboardButton(text='Вернуться к админ-панели', callback_data='back_to_admin_panel'))
    return keyboard.adjust(3).as_markup()

back_to_months=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Вернуться к выбору месяца', callback_data='back_to_months')]])

async def inline_admin_calendar_to_edit():
    keyboard = InlineKeyboardBuilder()
    i = 0
    for month in months:
        keyboard.add(InlineKeyboardButton(text=months[i], callback_data=f'edit_month_{month}_{i}'))
        i += 1
    keyboard.add(InlineKeyboardButton(text='Вернуться к админ-панели', callback_data='back_to_admin_panel'))
    return keyboard.adjust(3).as_markup()

async def edit_records_for_month(month_id: int):
    keyboard = InlineKeyboardBuilder()
    if any(matrix_busy[month_id]):
        for j in range(1, days_in_month_by_name(months[month_id]) + 1):
            for _ in matrix_busy[month_id][j]:
                str = _.split(" ")
                data = str[0]+' '+str[1]+' '+str[2]+' '+str[3] #нужно для последующего удаления по совпадению
                user_id = str[-1] #нужно для сообщения пользователю о том что его опрокинули
                #но нельзя колбэк длиннее 64 символов
                keyboard.add(InlineKeyboardButton(text=_, callback_data=f'edit_record_{user_id}_{data}_{month_id}'))
    keyboard.add(InlineKeyboardButton(text="Вернуться к выбору месяца", callback_data='back_from_edit'))
    return keyboard.adjust(1).as_markup()

edit_FAQ_keyboard=InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Добавить вопрос+ответ', callback_data='add_to_FAQ'),
    InlineKeyboardButton(text='Удалить вопрос+ответ', callback_data='delete_from_FAQ')],
    [InlineKeyboardButton(text='Вернуться к админ-панели', callback_data='back_to_admin_panel')]])

edit_review_keyboard=InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Добавить отзыв', callback_data='add_to_review'),
    InlineKeyboardButton(text='Удалить отзыв', callback_data='delete_from_review')],
    [InlineKeyboardButton(text='Вернуться к админ-панели', callback_data='back_to_admin_panel')]])

edit_sales_keyboard=InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Добавить акцию', callback_data='add_to_sales'),
    InlineKeyboardButton(text='Удалить акцию', callback_data='delete_from_sales')],
    [InlineKeyboardButton(text='Вернуться к админ-панели', callback_data='back_to_admin_panel')]])