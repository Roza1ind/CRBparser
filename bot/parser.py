import requests
from bs4 import BeautifulSoup
from datetime import datetime

class CurrencyParser:
     
    def __init__(self):
        self.url = "https://www.cbr.ru/scripts/XML_daily.asp"
        self.cache = {}
        self.last_update = None

    def get_exchange_rates(self):
        try:
            response = requests.get(self.url)
            response.encoding = 'windows-1251'

            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'lxml-xml')
                currencies = {}

                for valute in soup.find_all('Valute'):
                    # 🔹 Получаем ТЕГИ (объекты BeautifulSoup)
                    char_code_tag = valute.find('CharCode')
                    name_tag = valute.find('Name')
                    value_tag = valute.find('Value')
                    nominal_tag = valute.find('Nominal')

                    # 🔹 Проверяем, что все теги существуют
                    if char_code_tag and name_tag and value_tag and nominal_tag:
                        # 🔹 Теперь получаем ТЕКСТ из тегов
                        char_code = char_code_tag.text
                        name = name_tag.text
                        value_str = value_tag.text.replace(',', '.')
                        nominal_str = nominal_tag.text

                        # 🔹 Сохраняем данные
                        currencies[char_code] = {
                            'name': name,
                            'value': float(value_str),
                            'nominal': int(nominal_str)
                        }

                self.last_update = datetime.now()
                self.cache = currencies
                return currencies    
            
        except Exception as e:
            print(f"Ошибка парсинга: {e}")
            return self.cache if self.cache else None

    def get_concret_rates(self, currency_code):
        rates = self.get_exchange_rates()
        if rates and currency_code in rates:
            currency = rates[currency_code]
            return {
                'code': currency_code,
                'name': currency['name'],
                'rate': currency['value'] / currency['nominal'],
                'nominal': currency['nominal'] 
            }
        return None

    def format_currency_message(self, currency_code):
        currency = self.get_concret_rates(currency_code)
        if currency:
            return(
                f"{currency['name']} ({currency['code']})\n"
                f"Курс: {currency['rate']:.4f} RUB\n"
                f"Актуально на: {datetime.now().strftime('%d.%m.%Y %H:%M')}\n"
                f"Номинал: {currency['nominal']} {currency['code']}"
            )
        return f"Курс для {currency_code} не найден"