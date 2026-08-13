import requests
from bs4 import BeautifulSoup
import json

url = "https://www.cbr.ru/scripts/XML_daily.asp"
rate = {}

def get_all_courses():
    try:
        response = requests.get(url)
        response.encoding='windows-1251'

        soup = BeautifulSoup(response.content, 'lxml-xml')
        
        def get_date_time():
            ValCurs = soup.find('ValCurs')
            date_tag = ValCurs.get('Date')
            return date_tag

        currencies = {}
        date = get_date_time()
        
        for valute in soup.find_all('Valute'):

            char_tag = valute.find('CharCode')
            name_tag = valute.find('Name')
            nominal_tag = valute.find('Nominal')
            value_tag = valute.find('Value')

            if char_tag and name_tag and nominal_tag and value_tag:

                char_code = char_tag.text
                name = name_tag.text
                nominal = nominal_tag.text
                value = value_tag.text.replace(',','.')

                currencies[char_code] = {

                   
                   'name': name,
                   'value': float(value),
                   'nominal': int(nominal) 
                }

                save_json_courses = {
                    'date': date,
                    'currencies': currencies
                }


                with open("save_json_courses.json", "w", encoding='utf-8') as c:
                    json.dump(save_json_courses, c, ensure_ascii=False, indent=4)

        return date, currencies

    except Exception as e:
        print(f'error {e}')

def get_format_message(date, currencies):
    if not date or not currencies:
        return 'No data'

    lines = []
    lines.append("=" * 50)
    lines.append(f"  КУРСЫ ВАЛЮТ НА {date}".center(50))
    lines.append("=" * 50)
    lines.append(f"{'Код':<6} {'Номинал':<8} {'Курс (₽)':<12} {'Название'}")
    lines.append("-" * 50)
    
    for code, data in currencies.items():
        lines.append(f"{code:<6} {data['nominal']:<8} {data['value']:<12.4f} {data['name']}")
    
    lines.append("=" * 50)
    lines.append(f"  Всего валют: {len(currencies)}".center(50))
    lines.append("=" * 50)
    
    return "\n".join(lines)    

date, currencies = get_all_courses()
message = get_format_message(date, currencies)
print(message)

def save_to_txt(message, filename="courses.txt"):
    with open(filename, "w", encoding='utf-8') as f:
        f.write(message)
    print(f"Сообщение сохранено в {filename}")

date, currencies = get_all_courses()
message = get_format_message(date, currencies)

save_to_txt(message)