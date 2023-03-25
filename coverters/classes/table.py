import csv
from datetime import date

fn1 = [
    'Код артикула',
    'ID артикула',
    'ID товара',
    'Цена'
]
fn2 = [
    'ID артикула',
    'ID товара',
    'Склады'
]
fn3 = [
    '"Тип строки"', # 0
    'Наименование', # 1
    '"Наименование артикула"', # 2
    '"Код артикула"', # 3
    'Валюта', # 4
    '"ID артикула"', # 5
    'Цена', # 6
    '"Доступен для заказа"', # 7
    '"Видимость на витрине"', # 8
    '"Зачеркнутая цена"', # 9
    '"Закупочная цена"', # 10
    '"В наличии"', # 11
    '"В наличии @Наличие в Москве"', # 12
    '"В наличии @Склад в Китае"', # 13
    '"ID товара"', # 14
    '"Краткое описание"', # 15
    'Наклейка', # 16
    'Статус', # 17
    '"Выбор вариантов товара"', # 18
    '"Тип товаров"', # 19
    'Теги', # 20
    '"Облагается налогом"', # 21
    'Заголовок', # 22
    '"META Keywords"', # 23
    '"META Description"', # 24
    '"Ссылка на витрину"', # 25
    '"Адрес видео на Rutube, YouTube или Vimeo"', # 26
    '"Артикул модели"', # 27
    'Бренд', # 28
    '"Размер EU"', # 29
    'Пол', # 30
    'Склады', # 31
    '"Изображения товаров"', # 32
    '"Описания изображений товаров"', # 33
    '"Изображения товаров"', # 34
    '"Описания изображений товаров"', # 35
    '"Изображения товаров"', # 36
    '"Описания изображений товаров"', # 37
    '"Изображения товаров"', # 38
    '"Описания изображений товаров"', # 39
    '"Изображения товаров"', # 40
    '"Описания изображений товаров"', # 41
    '"Изображения товаров"', # 42
    '"Описания изображений товаров"', # 43
    '"Изображения товаров"', # 44
    '"Описания изображений товаров"', # 45
    '"Изображения товаров"', # 46
    '"Описания изображений товаров"', # 47
    '"Изображения товаров"', # 48
    '"Описания изображений товаров"', # 49
    '"Изображения товаров"', # 50
    '"Описания изображений товаров"', # 51
    '"Изображения товаров"', # 52
    '"Описания изображений товаров"', # 53
    '"Изображения товаров"', # 54
    '"Описания изображений товаров"', # 55
    '"Изображения товаров"', # 56
    '"Описания изображений товаров"', # 57
    '"Изображения товаров"', # 58
    '"Описания изображений товаров"', # 59
    '"Изображения товаров"', # 60
    '"Описания изображений товаров"', # 61
    '"Изображения товаров"', # 62
    '"Описания изображений товаров"', # 63
    '"Изображения товаров"', # 64
    '"Описания изображений товаров"', # 65
    '"Изображения товаров"', # 66
    '"Описания изображений товаров"' # 67
]


class Table():
    def __init__(self, _path: str, _table_type: int):
        self.path = _path
        self.table_type = _table_type

    
    def create_table(self):
        with open(f'{self.path}', 'w', encoding='cp1251', errors="ignore")as file:
            if self.table_type == 1:
                writer = csv.DictWriter(file, fieldnames=fn1, delimiter=';', lineterminator='\n')
                writer.writeheader()
            elif self.table_type == 2:
                writer = csv.DictWriter(file, fieldnames=fn2, delimiter=';', lineterminator='\n')
                writer.writeheader()
            else:
                print('Error: table incorrect table type.')
            

    def open_table(self):
        data = []
        with open(f'{self.path}', 'r', encoding='cp1251', errors="ignore") as file:
            if self.table_type == 3:
                reader = csv.reader(file, delimiter=';', lineterminator='\n')
                for row in reader:
                    data.append(row)
            elif self.table_type == 1:
                reader = csv.reader(file, delimiter=';', lineterminator='\n')
                for row in reader:
                    data.append(row)
            else:
                print('Error: table incorrect table type.')
        return data


    def write_row(self, data):
        with open(f'{self.path}', 'a', encoding='cp1251', errors="ignore") as file:
            if self.table_type == 1:
                writer = csv.DictWriter(file, fieldnames=fn1, delimiter=';', lineterminator='\n')
                writer.writerow(data)
            elif self.table_type == 2:
                writer = csv.DictWriter(file, fieldnames=fn2, delimiter=';', lineterminator='\n')
                writer.writerow(data)
            else:
                print('Error: table incorrect table type.')
