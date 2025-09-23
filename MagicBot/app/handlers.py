import os

from aiogram import  F, Router, types
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from app.keyboards import matrix_busy
import app.keyboards as kb

router = Router()

review = [('\n<b>— Дмитрий Петров, папа Софии (10) — Web-разработка</b>\n'
           '«София начала с нуля и за 3 месяца создала свой первый сайт! '
           'Магическая атмосфера обучения в ByteHut превратила программирование в увлекательное приключение.»\n'),
          ('\n<b>— Алина Сергеева, мама Максима (12) — Python</b>\n'
          '«Максим с нетерпением ждёт каждое занятие! '
          'Уже пишет свои первые программы — спасибо за тёплый и понятный подход.»\n'),
          ('\n<b>— Олег Воронов, папа Кирилла (11) — Разработка игр</b>\n'
          '«Кирилл сделал свою первую игру и показал друзьям — теперь все хотят учиться в ByteHut! '
          'Видимый результат — лучшая мотивация.»\n'),
          ('\n<b>— Екатерина Ильина, мама Полины (9) — Scratch</b>\n'
          '«Полина в восторге: всё так игриво и понятно, что даже я заглядываю на уроки. Отличное начало для ребёнка.»\n'),
          ('\n<b>— Артём Белов, папа Даниила (13) — Введение в ИИ</b>\n'
          '«Даниил уже рассуждает о нейросетях и машинном обучении — спасибо за то, что открываете детям технологии будущего!»\n')]

FAQ = [('\n💻 <b>Что требуется для работы?</b>\n'
       'Для занятий потребуется компьютер/ноутбук и стабильный интернет. На первом уроке преподаватель подробно расскажет, '
       'какие программы нужно установить для комфортного и эффективного обучения.\n'),
       ('\n📚 <b>Домашнее задание обязательно?</b>\n'
       'Да, выполнение домашних заданий — важная часть обучения. '
       'У каждого ученика будет доступ к учебным материалам и записям занятий для их прохождения.\n'),
       ('\n🎓 <b>Что я получу после окончания курса?</b>\n'
       'Вы создадите несколько проектов, которые пополнят ваше портфолио. '
       'А после успешного завершения курса каждый ученик получает сертификат.\n'),
       ('\n👥 <b>Как проходят занятия?</b>\n'                            
        'Занятия доступны в индивидуальном и групповом формате (до 5 человек). '
        'Длительность урока — 60 минут. Преподаватель сочетает теорию с практикой, чтобы материал был понятен и интересен.\n'),
       ('\n🔄 <b>Можно ли вернуть деньги, если передумали учиться?</b>\n'
       'При покупке модуля (нескольких занятий) возврат возможен только в случае, '
       'если было проведено не более одного занятия из модуля.\n'),
       ('\n🧠 <b>Можно ли начать с нуля?</b>\n'
       'Да, именно так! Мы предлагаем курсы для любого уровня подготовки — '
       'от полного нуля до углублённого изучения. '
       'Ваш ребёнок сможет начать с основ и постепенно прогрессировать, осваивая всё более сложные темы и технологии вместе с нами.\n')]

sales = []


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer('Пока что привет! потом здесь будет текст о школе + картинка', reply_markup=kb.settings)

@router.callback_query(F.data == 'offers')
async def offers(callback: CallbackQuery):
    await callback.answer('Вы выбрали просмотр информации о школе')
    await callback.message.edit_text('Наша школа магов приветствует Вас! + мб потом картинку', reply_markup= await kb.inline_menu())

# кнопка вводный урок и иже с ней
@router.callback_query(F.data == 'step_1')
async def step_intro(callback: CallbackQuery):
    await callback.answer('Вы выбрали просмотр информации про вводный урок')
    await callback.message.edit_text('✨ <b><i>Бесплатная консультация!</i></b> ✨\n'
                                        '\nПриглашаем вас и вашего ребенка на знакомство с уникальной атмосферой нашей онлайн-школы программирования ByteHut!\n'
                                        '\nПогрузитесь в мир, где технологии встречаются с творчеством, а обучение становится увлекательным приключением!\n'
                                        '\n🚀 <b><i>Что ждет на вводном занятии:</i></b>\n'
                                        '• Познакомим с курсами, и объясним в чем особенности обучения.\n'
                                        '• Покажем, как устроен процесс обучения в нашей цифровой среде.\n'
                                        '• Ответим на все вопросы по программе и правилам платформы.\n'
                                        '• Поможем выбрать идеальное направление для развития юного айтишника.\n'

                                        '\nОткройте дверь в мир, где программирование становится захватывающим'
                                        ' путешествием в подземелье за сокровищем, а каждый урок - это новый опыт для повышения вашего уровня! 🎮\n',
                                     reply_markup= await kb.inline_intro())

@router.callback_query(F.data == 'intro_1')
async def step_record_to_intro(callback: CallbackQuery):
    await callback.answer('Вы выбрали запись на вводный урок')
    await callback.message.edit_text('Выберите месяц для записи на ✨вводный урок✨', reply_markup=await kb.inline_calendar())

@router.callback_query(F.data == 'back_from_calendar')
async def step_back_from_calendar(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text('✨ <b><i>Бесплатная консультация!</i></b> ✨\n'
                                     '\nПриглашаем вас и вашего ребенка на знакомство с уникальной атмосферой нашей онлайн-школы программирования ByteHut!\n'
                                     '\nПогрузитесь в мир, где технологии встречаются с творчеством, а обучение становится увлекательным приключением!\n'
                                     '\n🚀  <b><i>Что ждет на вводном занятии:</i></b>\n'
                                     '• Познакомим с курсами, и объясним в чем особенности обучения.\n'
                                     '• Покажем, как устроен процесс обучения в нашей цифровой среде.\n'
                                     '• Ответим на все вопросы по программе и правилам платформы.\n'
                                     '• Поможем выбрать идеальное направление для развития юного айтишника.\n'

                                     '\nОткройте дверь в мир, где программирование становится захватывающим'
                                     ' путешествием в подземелье за сокровищем, а каждый урок - это новый опыт для повышения вашего уровня! 🎮\n',
                                     reply_markup=await kb.inline_intro())

# кнопка перехода к записи на вводный урок
@router.callback_query(F.data.startswith('month_'))
async def reg_to_lesson(callback: CallbackQuery):
    month_id = int(callback.data.replace('month_', ''))
    # потом убери month_id он тут для отладки стоит
    await callback.answer(f"Выбранный для записи месяц - {kb.months[month_id].lower()}")
    await callback.message.edit_text("Выберите подходящую дату из представленных ниже:", reply_markup=await kb.month_to_register(month_id))

# кнопка назад на главное меню
@router.callback_query(F.data == 'intro_2')
async def step_back_from_intro(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text('Наша школа магов приветствует Вас! + мб потом картинку', reply_markup= await kb.inline_menu())

# кнопка преподаватели
@router.callback_query(F.data == 'step_2')
async def step_teachers(callback: CallbackQuery):
    await callback.answer('Вы выбрали просмотр информации о преподавателях')
    await callback.message.edit_text('✅ Школа имеет официальную лицензию на образовательную деятельность\n'
                                     '✅ Только практикующие преподаватели с опытом в IT-индустрии\n'
                                     '✅ 150+ успешных выпускников\n'
                                     '✅ Индивидуальный подход к каждому ученику\n'
                                     '\nЗапишитесь на <b>бесплатный вводный урок</b> и помогите ребенку сделать первый шаг в мире IT-профессий! 🚀',
                                     reply_markup=await kb.inline_back())

# кнопка наши курсы
@router.callback_query(F.data == 'step_3')
async def step_courses(callback: CallbackQuery):
    await callback.answer('Вы выбрали просмотр информации о курсах')
    await callback.message.edit_text('✨ <b><i>Откройте мир IT-образования для вашего ребенка!</i></b> ✨\n'
                                    '\nВ онлайн-школе ByteHut мы предлагаем комплексную программу обучения, разработанную специально для <b>юных IT-гениев</b>!\n'
                                    '\n🎮 <b>Scratch</b> — идеальный старт для самых юных программистов!\n'
                                    'Визуальное программирование, создание первых игр и анимаций. Развиваем логику и креативное мышление.\n'

                                    '\n🐍 <b>Базовый Python</b> — основа программирования для начинающих\n'
                                    'Изучение фундаментальных concepts через создание практических проектов. Первые шаги в мире кода.\n'

                                    '\n🚀 <b>Продвинутый Python</b> — углубленное погружение в разработку\n'
                                    'Сложные проекты, алгоритмы и работа с библиотеками. Подготовка к серьезным IT-профессиям.\n'

                                    '\n💻 <b>Компьютерная грамотность</b> — уверенное владение digital-навыками\n'
                                    'Основы работы с ПО, безопасность в интернете, эффективное использование технологий.\n'

                                    '\n🧠 <b>Введение в ИИ</b> — знакомство с искусственным интеллектом\n'
                                    'Основы машинного обучения, нейросети и технологии будущего уже сегодня!\n'
                                    '\nПодробное описание всех курсов доступно на сайте: ' #сюда потом ссылку на лендинг?
                                    'https://www.youtube.com/watch?v=QvENfMFhP60&list=PLV0FNhq3XMOJ31X9eBWLIZJ4OVjBwb-KM&index=5&ab_channel=%24sudoteachIT%E2%9A%99%EF%B8%8F',
                                    reply_markup=await kb.inline_back())

# кнопка FAQ
@router.callback_query(F.data == 'step_4')
async def step_FAQ(callback: CallbackQuery):
    await callback.answer('Вы выбрали просмотр часто задаваемых вопросов')
    text = "✨ <b><i>Часто задаваемые вопросы (FAQ)</i></b> ✨\n"
    for item in FAQ:
        text += f"{item}"
    await callback.message.edit_text(text, reply_markup=await kb.inline_back())

# кнопка отзывы
@router.callback_query(F.data == 'step_5')
async def step_review(callback: CallbackQuery):
    await callback.answer('Вы выбрали просмотр отзывов')
    text = "✨ <b><i>Отзывы родителей о курсах ByteHut</i></b> ✨\n"
    for item in review:
        text += f"{item}"
    text += '\n📌 Хотите, чтобы ваш ребёнок тоже полюбил IT? <b>Запишитесь на вводный урок</b> и пройдите консультацию с нашими специалистами.'
    await callback.message.edit_text(text, reply_markup=await kb.inline_back())

# кнопка акции
@router.callback_query(F.data == 'step_6')
async def step_sale(callback: CallbackQuery):
    await callback.answer('Вы выбрали просмотр акций')
    text=""
    if sales!=[]:
        for item in sales:
            text += f"{item}"
    else: text = "Сейчас акций нет, но <b>следите за обновлениями!</b>"
    await callback.message.edit_text(text, reply_markup=await kb.inline_back())

# кнопка назад которая менюшная
@router.callback_query(F.data == 'step_7')
async def step_back_to_first_menu(callback: CallbackQuery):
    await callback.answer('')
    await callback.message.edit_text('Пока что привет! потом здесь будет текст о школе + картинка', reply_markup=kb.settings)

# кнопка назад на месяц записи
@router.callback_query(F.data == 'back_from_record')
async def back_from_record_to_months(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text('Выберите месяц для записи на ✨вводный урок✨', reply_markup=await kb.inline_calendar())

# кнопка записи на день
@router.callback_query(F.data.startswith('record_month_'))
async def choose_time(callback: CallbackQuery):
    new_str = (callback.data.replace('record_month_', '').replace('_day', '').split(sep='_'))
    month_id = int(new_str[0])
    day_id = int(new_str[1])
    await callback.answer()
    await callback.message.edit_text("Выберите подходящий вариант из представленных ниже:", reply_markup=await kb.records_for_data(day_id, month_id))

# кнопка назад к выбору дня
@router.callback_query(F.data.startswith('back_from_choose_'))
async def back_from_choose_to_calendar(callback: CallbackQuery):
    month_id = int(callback.data.replace('back_from_choose_', ''))
    await callback.answer()
    await callback.message.edit_text("Выберите подходящую дату из представленных ниже:", reply_markup=await kb.month_to_register(month_id))


class Form(StatesGroup):
    waiting_for_contact = State()

# Обработчик текста пользователя
@router.message(F.text, Form.waiting_for_contact)
async def process_contact(message: types.Message, state: FSMContext):
    contact_info = message.text
    user_id = str(message.from_user.id)
    data = await state.get_data()
    month_id = data.get('month_id')
    day_id = data.get('day_id')
    button = data.get('button')
    await state.update_data(contact=contact_info)
    await message.answer(
        f"Спасибо! Ваши данные сохранены: {contact_info}\n"
        "Вы были успешно записаны на выбранную Вами дату и время!\n"
        "Будем рады видеть Вас на вводном уроке✨"
    )
    contact_info+=" " + user_id
    await kb.delete_free_add_busy(day_id, month_id, button, contact_info)
    await state.clear()

# кнопка после успешной записи, просит данные
@router.callback_query(F.data.startswith('successful_record_'))
async def successful_record(callback: CallbackQuery, state: FSMContext):
    new_str = (callback.data.replace('successful_record_', '').replace('_day', '').split(sep='_'))
    month_id = int(new_str[0])
    day_id = int(new_str[1])
    button = new_str[2]
    await state.update_data(month_id=month_id, day_id=day_id, button=button, show_success=True)
    await callback.message.answer(
        "Пожалуйста, введите ваши контактные данные: телефон и почту в формате <b>'+7-XXX-XXX-XX-XX/cutecat@gmail.ru'</b>")
    await state.set_state(Form.waiting_for_contact)
    await callback.answer("")
    await callback.message.edit_text('Наша школа магов приветствует Вас! + мб потом картинку', reply_markup= await kb.inline_menu())


# штука для админов вся ниже
@router.message(F.text, Command("admin"))
async def admin_panel(message: Message):
    user_id = str(message.from_user.id)
    if user_id in os.getenv('ADMINS'):
        await message.answer("Добро пожаловать в ✨админ-панель✨", reply_markup=kb.admin_keyboard)
    else: await message.answer('К сожалению, Вы не являетесь админом(\n'
                               'Для работы с ботом воспользуйтесь командой /start')

# кнопка просмотра записей
@router.callback_query(F.data == 'look_records')
async def look_records(callback: CallbackQuery):
    await callback.answer('')
    await callback.message.edit_text("Выберите месяц, чтобы посмотреть записи", reply_markup=await kb.inline_admin_calendar_to_look())

# кнопка возврата на админ-панель
@router.callback_query(F.data == 'back_to_admin_panel')
async def back_to_admin_panel(callback: CallbackQuery):
    await callback.answer('')
    await callback.message.edit_text("Добро пожаловать в ✨админ-панель✨", reply_markup=kb.admin_keyboard)

# кнопка просмотра записей на месяц
@router.callback_query(F.data.startswith('rec_month_'))
async def show_records_by_month(callback: CallbackQuery):
    new_str = (callback.data.replace('rec_month_', '').split("_"))
    month_name = new_str[0]
    month_id = int(new_str[1])
    await callback.answer(f"Выбранный для просмотра записей месяц - {kb.months[month_id].lower()}")
    if any(matrix_busy[month_id]):
        text = "<b>Записи за выбранный месяц: </b>\n\n"
        for j in range(1, kb.days_in_month_by_name(month_name)+1):
            for _ in kb.matrix_busy[month_id][j]:
                text += _ + "\n"
    else: text = 'Записей на данный месяц нет('
    await callback.message.edit_text(text, reply_markup=kb.back_to_months)

# кнопка назад к выбору месяца просмотра записей
@router.callback_query(F.data == 'back_to_months')
async def back_to_months(callback: CallbackQuery):
    await callback.answer('')
    await callback.message.edit_text("Выберите месяц, чтобы посмотреть записи", reply_markup=await kb.inline_admin_calendar_to_look())

# кнопка отмены записей на месяц
@router.callback_query(F.data == 'change_calendar')
async def edit_records(callback: CallbackQuery):
    await callback.answer('')
    await callback.message.edit_text("Выберите месяц, чтобы отменить записи", reply_markup=await kb.inline_admin_calendar_to_edit())

# тут можно будет выбрать запись которую хочешь отменить в конкретный месяц
@router.callback_query(F.data.startswith('edit_month_'))
async def edit_records_by_month(callback: CallbackQuery):
    new_str = (callback.data.replace('edit_month_', '').split("_"))
    month_id = int(new_str[1])
    await callback.answer('')
    if any(matrix_busy[month_id]):
        text = "<b>Записи за выбранный месяц: </b>\n\n"
    else: text = 'Записей на данный месяц нет('
    await callback.message.edit_text(text, reply_markup=await kb.edit_records_for_month(month_id))

# кнопка назад на выбор месяца удаления
@router.callback_query(F.data == 'back_from_edit')
async def back_to_months(callback: CallbackQuery):
    await callback.answer('')
    await callback.message.edit_text("Выберите месяц, чтобы отменить записи", reply_markup=await kb.inline_admin_calendar_to_edit())

# успешное удаление+сообщение пользователю
@router.callback_query(F.data.startswith('edit_record_'))
async def delete_record(callback: CallbackQuery):
    new_str = (callback.data.replace('edit_record_', '').split("_"))
    user_id=new_str[0]
    data=new_str[1]
    month_id=int(new_str[2])
    for cell in matrix_busy[month_id]:
        for record in cell:
            if record.startswith(data):
                find = record
                cell.remove(find)
                break
    await callback.answer(f'Запись пользователя {user_id} успешно удалена. Сообщение об этом было доставлено!', show_alert=True)
    await callback.message.edit_text("Добро пожаловать в ✨админ-панель✨", reply_markup=kb.admin_keyboard)
    await callback.bot.send_message(chat_id=user_id, text=f'Вынуждены сообщить, что ваша запись на {data.lower()} <b>была отменена администратором</b>. '
                                                          f'В случае возникновения вопросов свяжитесь с менеджером через главное меню бота!')

# кнопка редактировать FAq
@router.callback_query(F.data == 'edit_FAQ')
async def edit_FAQ(callback: CallbackQuery):
    await callback.answer('')
    text = ("<b>Сейчас раздел FAQ выглядит следующим образом:</b>\n\n"
            "✨ <b><i>Часто задаваемые вопросы (FAQ)</i></b> ✨\n")
    i=0
    for item in FAQ:
        i+=1
        text += f"№{i}) {item}"
    text+="\n<b>Выберите желаемое действие</b>"
    await callback.message.edit_text(text,
                                     reply_markup=kb.edit_FAQ_keyboard)

class FAQForm(StatesGroup):
    waiting_for_faq = State()
    waiting_for_delete = State()

@router.callback_query(F.data == 'add_to_FAQ')
async def add_to_FAQ(callback: CallbackQuery, state: FSMContext):
    text = 'Введите строку, которую хотите добавить в FAQ'
    await callback.message.answer(text)
    await state.set_state(FAQForm.waiting_for_faq)
    await callback.answer('')
    await callback.message.edit_text("Добро пожаловать в ✨админ-панель✨", reply_markup=kb.admin_keyboard)

@router.callback_query(F.data == 'delete_from_FAQ')
async def delete_from_FAQ(callback: CallbackQuery, state: FSMContext):
    text = "<b>Введите номер строки, которую хотите удалить.</b>\n\nТекущий список FAQ:\n"
    text += "\n".join([f"№{i+1}) {entry}" for i, entry in enumerate(FAQ)])
    await callback.message.answer(text)
    await state.set_state(FAQForm.waiting_for_delete)
    await callback.message.edit_text("Добро пожаловать в ✨админ-панель✨", reply_markup=kb.admin_keyboard)


@router.message(F.text, FAQForm.waiting_for_delete)
async def process_faq_deletion(message: types.Message, state: FSMContext):
    num = int(message.text.strip())
    if 1 <= num <= len(FAQ):
        removed = FAQ.pop(num - 1)
        await message.answer(f"Запись удалена из FAQ:\n{removed}\n\n")
    else:
        await message.answer("Неверный номер. Попробуйте снова.")
        return

    await state.clear()


@router.message(F.text, FAQForm.waiting_for_faq)
async def process_faq_entry(message: types.Message, state: FSMContext):
    text = message.text.strip()

    if "\n" in text:
        q, a = text.split("\n", 1)
        faq_ = f"<b>{q.strip()}</b>\n{a}"
    else:
        faq_ = f"<b>{text}</b>"
    faq_ = "\n" + faq_ + "\n"
    FAQ.append(faq_)
    await message.answer(
        f"Запись добавлена в FAQ в следующем виде:\n{faq_}",
        parse_mode="HTML"
    )
    await state.clear()

@router.callback_query(F.data == 'edit_review')
async def edit_review(callback: CallbackQuery):
    await callback.answer('')
    text = ("<b>Сейчас раздел отзывов выглядит следующим образом:</b>\n\n")
    i = 0
    for item in review:
        i += 1
        text += f"№{i}) {item}"
    text += "\n<b>Выберите желаемое действие</b>"
    await callback.message.edit_text(text, reply_markup=kb.edit_review_keyboard)

class ReviewForm(StatesGroup):
    waiting_for_review = State()
    waiting_for_rew_delete = State()


@router.callback_query(F.data == 'add_to_review')
async def add_to_review(callback: CallbackQuery, state: FSMContext):
    text = 'Введите строку, которую хотите добавить в раздел отзывов'
    await callback.message.answer(text)
    await state.set_state(ReviewForm.waiting_for_review)
    await callback.answer('')
    await callback.message.edit_text("Добро пожаловать в ✨админ-панель✨", reply_markup=kb.admin_keyboard)

@router.callback_query(F.data == 'delete_from_review')
async def delete_from_review(callback: CallbackQuery, state: FSMContext):
    text = "<b>Введите номер строки, которую хотите удалить.</b>\n\nТекущий список отзывов:\n"
    text += "\n".join([f"№{i+1}) {entry}" for i, entry in enumerate(review)])
    await callback.message.answer(text)
    await state.set_state(ReviewForm.waiting_for_rew_delete)
    await callback.message.edit_text("Добро пожаловать в ✨админ-панель✨", reply_markup=kb.admin_keyboard)


@router.message(F.text, ReviewForm.waiting_for_rew_delete)
async def process_rev_deletion(message: types.Message, state: FSMContext):
    num = int(message.text.strip())
    if 1 <= num <= len(review):
        removed = review.pop(num - 1)
        await message.answer(f"Запись удалена из раздела отзывов:\n{removed}\n\n")
    else:
        await message.answer("Неверный номер. Попробуйте снова.")
        return

    await state.clear()


@router.message(F.text, ReviewForm.waiting_for_review)
async def process_rev_entry(message: types.Message, state: FSMContext):
    text = message.text.strip()

    if "\n" in text:
        q, a = text.split("\n", 1)
        rev_ = f"<b>{q.strip()}</b>\n{a}"
    else:
        rev_ = f"<b>{text}</b>"
    rev_ = "\n" + rev_ + "\n"
    rev_=rev_.replace('"', "«", 1).replace('"', "»", 1).replace("-", "—")
    review.append(rev_)
    await message.answer(
        f"Запись добавлена в раздел отзывов в следующем виде:\n{rev_}",
        parse_mode="HTML"
    )
    await state.clear()

@router.callback_query(F.data == 'edit_sales')
async def edit_sales(callback: CallbackQuery):
    text = "<b>Сейчас список акций выглядит следующим образом:</b>\n\n"
    if sales!=[]:
        text += "\n".join([f"№{i+1}) {entry}" for i, entry in enumerate(sales)])
    else: text+= "Он пуст🥲"
    await callback.answer('')
    await callback.message.edit_text(text, reply_markup=kb.edit_sales_keyboard)

class SalesForm(StatesGroup):
    waiting_for_sales = State()
    waiting_for_sale_delete = State()


@router.callback_query(F.data == 'add_to_sales')
async def add_to_sales(callback: CallbackQuery, state: FSMContext):
    text = 'Введите строку, которую хотите добавить в раздел акций'
    await callback.message.answer(text)
    await state.set_state(SalesForm.waiting_for_sales)
    await callback.answer('')
    await callback.message.edit_text("Добро пожаловать в ✨админ-панель✨", reply_markup=kb.admin_keyboard)

@router.callback_query(F.data == 'delete_from_sales')
async def delete_from_sales(callback: CallbackQuery, state: FSMContext):
    text = "<b>Введите номер строки, которую хотите удалить.</b>\n\nТекущий список акций:\n"
    if sales!=[]:
        text += "\n".join([f"№{i+1}) {entry}" for i, entry in enumerate(sales)])
    else: text+= "Он пуст🥲"
    await callback.message.answer(text)
    await state.set_state(SalesForm.waiting_for_sale_delete)
    await callback.message.edit_text("Добро пожаловать в ✨админ-панель✨", reply_markup=kb.admin_keyboard)


@router.message(F.text, SalesForm.waiting_for_sale_delete)
async def process_sale_deletion(message: types.Message, state: FSMContext):
    num = int(message.text.strip())
    if 1 <= num <= len(sales):
        removed = sales.pop(num - 1)
        await message.answer(f"Запись удалена из раздела акций:\n{removed}\n\n")
    else:
        await message.answer("Неверный номер. Попробуйте снова.")
        return

    await state.clear()


@router.message(F.text, SalesForm.waiting_for_sales)
async def process_sale_entry(message: types.Message, state: FSMContext):
    text = message.text.strip()

    if "\n" in text:
        q, a = text.split("\n", 1)
        sale_ = f"<b>{q.strip()}</b>\n{a}"
    else:
        sale_ = f"<b>{text}</b>"
    sale_ = "\n" + sale_ + "\n"
    sales.append(sale_)
    await message.answer(
        f"Запись добавлена в раздел акций в следующем виде:\n{sale_}",
        parse_mode="HTML"
    )
    await state.clear()