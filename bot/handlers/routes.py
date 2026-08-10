from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from datetime import datetime
from parser import CurrencyParser

router = Router()
currency_parser = CurrencyParser()


# Основная панель бота
def get_main_reply_keyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Узнать курс валют на сегодня")],
            [KeyboardButton(text="о боте")],
            [KeyboardButton(text="Старт"), KeyboardButton(text="Помощь")]
        ],
        resize_keyboard=True
    )

    return keyboard
# Клава выбора валюты
def get_currency_keyboard():
    keyboard = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="USD")],
                [KeyboardButton(text="EUR")],
                [KeyboardButton(text="CNY")],
                [KeyboardButton(text="GBP")],
                [KeyboardButton(text="Назад")]
            ],
        resize_keyboard=True
    )

    return keyboard
# Вызов события старта
@router.message(Command("start"))
async def start(message: Message):
    await message.answer("Добро пожаловать в парсер актуальных валют, что желаете узнать?", reply_markup=get_main_reply_keyboard())

# Вызов события помощи
@router.message(Command("help"))
async def help_command(message: Message):
    await message.answer(
        "Команды:\n\n"
        "/start - запуск бота \n"
        "/help - помощь \n"
        "/about - О нас \n"
        "/rates  - выбор актуальных валют на сегодняшний день"
        "/usd - Курс USD\n"
        "/eur - Курс EUR\n"
        "/gbp - Курс GBP\n"
        "/cny - Курс CNY\n",
        reply_markup=get_main_reply_keyboard())


@router.message(Command("about"))
async def about_command(message: Message):
    await message.answer("Empty space\n")

@router.message(Command("rates"))
async def all_rates_command(message: Message):
    """
    # Старый вариант
    # current_time = datetime.now().strftime("%H:%M:%S")
    # current_date = datetime.now().strftime("%d.%m.%Y")

     # await message.answer(
        #     f"Актуальные курсы валют\n"
        #     f"Сегодня по ВДК {current_time} - {current_date}\n\n"
        #     f"\n/USD - Доллары \n"
        #     f"\n/EUR - Евро \n"
        #     f"\n/CNY - Юани",
        #     reply_markup=get_the_current_exchange_rate())
    """
    rates = currency_parser.get_exchange_rates()

    if rates:
        title = "Актуальные курсы валют:\n\n"
        popular = ['USD', 'EUR', 'CNY', 'GBP']
        for item in popular:
            if item in rates:
                currency = rates[item]
                rate = currency['value'] / currency['nominal']
                title += f"{item}: {rate:.4f} RUB\n"


        title += f"\n {datetime.now().strftime('%d.%m.%Y %H:%M')}"
        await message.answer(title)
    else:
        await message.answer("Try again later")


# Подтягиваем команды
@router.message(Command("usd"))
async def usd_comand(message: Message):

    await show_currency_rate(message, 'USD')

@router.message(Command("eur"))
async def eur_comand(message: Message):

    await show_currency_rate(message, 'EUR')

@router.message(Command("gbp"))
async def gbp_comand(message: Message):

    await show_currency_rate(message, 'GBP')

@router.message(Command("cny"))
async def cny_comand(message: Message):

    await show_currency_rate(message, 'CNY')

@router.message(Command("current_exchange_rate"))
async def current_exchange_rate(message: Message):
    """Меню выбора валют"""
    current_time = datetime.now().strftime("%H:%M:%S")
    current_date = datetime.now().strftime("%d.%m.%Y")

    await message.answer(
        f"Актуальные курсы валют\n"
        f"{current_date} {current_time}\n\n"
        f"Выберите валюту или используйте команды:\n"
        f"/usd - Доллары США\n"
        f"/eur - Евро\n"
        f"/gbp - Евро\n"
        f"/cny - Юани\n"
        f"/rates - Все курсы",
        reply_markup=get_currency_keyboard()
    )

#Обработчики кнопок

@router.message(F.text == "Узнать курс валют на сегодня")
async def button_rates(message: Message):
    await current_exchange_rate(message)

@router.message(F.text == "О боте")
async def button_about(message: Message):
    await about_command(message)

@router.message(F.text == "Старт")
async def button_start(message: Message):
    await start(message)

@router.message(F.text == "Помощь")
async def button_help(message: Message):
    await help_command(message)

@router.message(F.text == "Назад")
async def button_back(message: Message):
    await start(message)

@router.message(F.text.in_(["USD", "EUR", "CNY", "GBP"]))
async def currency_buttons(message: Message):
    currency_list = {
        "USD": "USD",
        "EUR": "EUR",
        "GBP": "GBP",
        "CNY": "CNY"
    }

    currency_code = currency_list.get(message.text)
    if currency_code:
        await show_currency_rate(message, currency_code)

async def show_currency_rate(message: Message, currency_code: str):
    currency_info = currency_parser.format_currency_message(currency_code)
    await message.answer(
        currency_info,
        reply_markup=get_currency_keyboard())




   




    

