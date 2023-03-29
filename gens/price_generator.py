import os
import pygsheets
from datetime import date
from classes.table import Table


def dround(i: float):
    if i%int(i) >= 0.5:
        return int(i)+1
    else:
        return int(i)


def create_first_table(cny):
    client = pygsheets.authorize('credentials.json')

    file = os.listdir('input\\table1')[0]
    path = f'input\\table1\\{file}'
    output_name = f'output\\tables\\prices-{date.today().strftime("%d%m%Y")}.csv'
    table_input = Table(path, 3)
    table_output = Table(output_name, 1)
    table_output.create_table()

    tb = table_input.open_table()
    sh = client.open('Кроссовки')

    wks = sh.worksheet('title', 'Total (заказы)')

    statuses = wks.get_col(15)
    articles = wks.get_col(7)
    prices = wks.get_col(12)

    i = 1

    for status in statuses:
        if status == 'Выложен на сайт':
            article = str(articles[i-1])
            for row in tb:
                if row[3] == article:
                    data = {
                        'Код артикула': article,
                        'ID артикула': row[5],
                        'ID товара': row[14],
                        'Цена': str(dround(float(prices[i].replace(',', '.'))/cny))
                    }
                    table_output.write_row(data)
                    break
                # else:
                    # print(f'не нашло {article}')
        i += 1
    os.remove(path)
    #удалить выходной файл с сервера в боте
    return output_name

def main():
    cyn = 10.06
    create_first_table(cyn)
    


if __name__ == '__main__':
    main()