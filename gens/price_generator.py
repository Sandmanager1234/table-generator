import os
import pygsheets
import pandas as pd
from datetime import date
from gens.classes.pd_table import pdTable


def dround(i: float):
    if i%int(i) >= 0.5:
        return int(i)+1
    else:
        return int(i)


def create_first_table(cny):
    client = pygsheets.authorize('credentials.json')

    file = os.listdir('input\\table1')[0]
    path = f'input\\table1\\{file}'
    inp_df = pdTable(path)
    out_path = f'output\\tables\\prices-{date.today().strftime("%d%m%Y")}.csv'

    sh = client.open('Кроссовки')

    wks = sh.worksheet('title', 'Total (заказы)')

    statuses = wks.get_col(15)
    articles = wks.get_col(7)
    prices = wks.get_col(12)

    i = 1
    data = []
    for status in statuses:
        if status == 'Выложен на сайт':
            article = str(articles[i-1])
            price = dround(float(prices[i].replace(',', '.'))/cny)
            row = {'Код артикула': article,'Цена': price}
            data.append(row.copy())
    gdf = pd.DataFrame(data)
    result = pd.merge(inp_df, gdf)
    result.to_csv(out_path, sep=';', encoding='cp1251', lineterminator='\n', index=False)
    os.remove(path)
    #удалить выходной файл с сервера в боте
    return out_path

def main():
    cyn = 10.06
    create_first_table(cyn)
    

if __name__ == '__main__':
    main()