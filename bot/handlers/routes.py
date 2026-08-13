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
            [KeyboardButton(text="Помощь")]
        ],
        resize_keyboard=True
    )

    return keyboard
# Клава выбора валюты
def get_currency_keyboard():
    keyboard = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="USD"), KeyboardButton(text="EUR"), KeyboardButton(text="CNY"), KeyboardButton(text="GBP")],
            [KeyboardButton(text="JPY"), KeyboardButton(text="CHF"), KeyboardButton(text="CAD"), KeyboardButton(text="AUD")],
            [KeyboardButton(text="TRY"), KeyboardButton(text="KZT"), KeyboardButton(text="UAH"), KeyboardButton(text="BYN")],
            [KeyboardButton(text="AMD"), KeyboardButton(text="AZN"), KeyboardButton(text="GEL"), KeyboardButton(text="KGS")],
            [KeyboardButton(text="MDL"), KeyboardButton(text="TJS"), KeyboardButton(text="UZS"), KeyboardButton(text="PLN")],
            [KeyboardButton(text="CZK"), KeyboardButton(text="HUF"), KeyboardButton(text="RON"), KeyboardButton(text="SEK")],
            [KeyboardButton(text="NOK"), KeyboardButton(text="DKK"), KeyboardButton(text="BGN"), KeyboardButton(text="RSD")],
            [KeyboardButton(text="XDR"), KeyboardButton(text="HKD"), KeyboardButton(text="SGD"), KeyboardButton(text="AED")],
            [KeyboardButton(text="SAR"), KeyboardButton(text="QAR"), KeyboardButton(text="OMR"), KeyboardButton(text="BHD")],
            [KeyboardButton(text="EGP"), KeyboardButton(text="INR"), KeyboardButton(text="IDR"), KeyboardButton(text="THB")],
            [KeyboardButton(text="VND"), KeyboardButton(text="KRW"), KeyboardButton(text="NGN"), KeyboardButton(text="ZAR")],
            [KeyboardButton(text="BRL"), KeyboardButton(text="MXN")],
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
        #"/rates  - выбор актуальных валют на сегодняшний день"
        "/usd - Курс USD\n"
        "/eur - Курс EUR\n"
        "/gbp - Курс GBP\n"
        "/cny - Курс CNY\n",
        reply_markup=get_main_reply_keyboard())


@router.message(Command("about"))
async def about_command(message: Message):
    await message.answer("Данный бот помогает вывести актуальные курсы валют с сайта ЦБ России\n")

# @router.message(Command("rates"))
# async def all_rates_command(message: Message):
#     rates = currency_parser.get_exchange_rates()

#     if rates:
#         title = "Актуальные курсы валют:\n\n"
#         popular = ['USD', 'EUR', 'CNY', 'GBP']
#         for item in popular:
#             if item in rates:
#                 currency = rates[item]
#                 rate = currency['value'] / currency['nominal']
#                 title += f"{item}: {rate:.4f} RUB\n"


#         title += f"\n {datetime.now().strftime('%d.%m.%Y %H:%M')}"
#         await message.answer(title)
#     else:
#         await message.answer("Try again later")


# Подтягиваем команды

CURRENCY_CODES = [
    "USD", "EUR", "GBP", "CNY", "JPY", "CHF", "CAD", "AUD", 
    "TRY", "KZT", "UAH", "BYN", "AMD", "AZN", "GEL", "KGS", 
    "MDL", "TJS", "UZS", "PLN", "CZK", "HUF", "RON", "SEK", 
    "NOK", "DKK", "BGN", "RSD", "XDR", "HKD", "SGD", "AED", 
    "SAR", "QAR", "OMR", "BHD", "EGP", "INR", "IDR", "THB", 
    "VND", "KRW", "NGN", "ZAR", "BRL", "MXN"
]

@router.message(F.text.in_(CURRENCY_CODES))
async def currency_buttons(message: Message):
    """Обработка нажатия на кнопку с валютой"""
    await show_currency_rate(message, message.text)
# @router.message(Command("usd"))
# async def usd_comand(message: Message):

#     await show_currency_rate(message, 'USD')

# @router.message(Command("eur"))
# async def eur_comand(message: Message):

#     await show_currency_rate(message, 'EUR')

# @router.message(Command("gbp"))
# async def gbp_comand(message: Message):

#     await show_currency_rate(message, 'GBP')

# @router.message(Command("cny"))
# async def cny_comand(message: Message):

#     await show_currency_rate(message, 'CNY')

@router.message(Command("current_exchange_rate"))
async def current_exchange_rate(message: Message):
    """Меню выбора валют"""
    current_time = datetime.now().strftime("%H:%M:%S")
    current_date = datetime.now().strftime("%d.%m.%Y")

    await message.answer(
        f"Актуальные курсы валют\n"
        f"{current_date} {current_time}\n\n"
        f"Выберите валюту или используйте команды:\n"
        f"/usd - Доллар США\n"
        f"/eur - Евро\n"
        f"/gbp - Фунт стерлингов\n"
        f"/cny - Китайский юань\n"
        f"/jpy - Японская иена\n"
        f"/chf - Швейцарский франк\n"
        f"/cad - Канадский доллар\n"
        f"/aud - Австралийский доллар\n"
        f"/try - Турецкая лира\n"
        f"/kzt - Казахстанский тенге\n"
        f"/uah - Украинская гривна\n"
        f"/byn - Белорусский рубль\n"
        f"/amd - Армянский драм\n"
        f"/azn - Азербайджанский манат\n"
        f"/gel - Грузинский лари\n"
        f"/kgs - Киргизский сом\n"
        f"/mdl - Молдавский лей\n"
        f"/tjs - Таджикский сомони\n"
        f"/uzs - Узбекский сум\n"
        f"/pln - Польский злотый\n"
        f"/czk - Чешская крона\n"
        f"/huf - Венгерский форинт\n"
        f"/ron - Румынский лей\n"
        f"/sek - Шведская крона\n"
        f"/nok - Норвежская крона\n"
        f"/dkk - Датская крона\n"
        f"/bgn - Болгарский лев\n"
        f"/rsd - Сербский динар\n"
        f"/xdr - СДР (спецправа заимствования)\n"
        f"/hkd - Гонконгский доллар\n"
        f"/sgd - Сингапурский доллар\n"
        f"/aed - Дирхам ОАЭ\n"
        f"/sar - Саудовский риял\n"
        f"/qar - Катарский риал\n"
        f"/omr - Оманский риал\n"
        f"/bhd - Бахрейнский динар\n"
        f"/egp - Египетский фунт\n"
        f"/inr - Индийская рупия\n"
        f"/idr - Индонезийская рупия\n"
        f"/thb - Тайский бат\n"
        f"/vnd - Вьетнамский донг\n"
        f"/krw - Южнокорейская вона\n"
        f"/ngn - Нигерийская найра\n"
        f"/zar - Южноафриканский рэнд\n"
        f"/brl - Бразильский реал\n"
        f"/mxn - Мексиканское песо\n",
        #f"/rates - Все курсы",
        reply_markup=get_currency_keyboard()
    )

#Обработчики кнопок
CURRENCY_COMMANDS = [
    "usd", "eur", "gbp", "cny", "jpy", "chf", "cad", "aud", 
    "try", "kzt", "uah", "byn", "amd", "azn", "gel", "kgs", 
    "mdl", "tjs", "uzs", "pln", "czk", "huf", "ron", "sek", 
    "nok", "dkk", "bgn", "rsd", "xdr", "hkd", "sgd", "aed", 
    "sar", "qar", "omr", "bhd", "egp", "inr", "idr", "thb", 
    "vnd", "krw", "ngn", "zar", "brl", "mxn"
]

# Универсальный обработчик
@router.message(Command(*CURRENCY_COMMANDS))
async def currency_command(message: Message):
    """Универсальный обработчик для всех валютных команд"""
    currency_code = message.text.replace('/', '').upper()
    await show_currency_rate(message, currency_code)


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

# @router.message(F.text.in_(["USD", "EUR", "CNY", "GBP"]))
# async def currency_buttons(message: Message):
#     currency_list = {
#         "USD": "USD",
#         "EUR": "EUR",
#         "GBP": "GBP",
#         "CNY": "CNY"
#     }

#     currency_code = currency_list.get(message.text)
#     if currency_code:
#         await show_currency_rate(message, currency_code)

async def show_currency_rate(message: Message, currency_code: str):
    currency_info = currency_parser.format_currency_message(currency_code)
    await message.answer(
        currency_info,
        reply_markup=get_currency_keyboard())




   




    

