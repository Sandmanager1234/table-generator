import os
import re
from coverters.classes.table import Table


def create_csv_table():

    print('Create csv...')
    i = 0
    file = os.listdir('input\\table2')[0]

    path = f'input\\table2\\{file}'

    table1 = Table(path, 3)
    # table2 = Table('output\\tables\\storages.csv', 2)

    # table2.create_table()

    tb = table1.open_table()
    tb_moscow = []
    prod_tb = []
    j = -1
    for row in tb:
        if row[0] == 'product':
            prod_tb.append(row)
            j += 1
        if row[0] == 'variant':
            try:
                k = int(row[12])
            except:
                # print(row)
                pass
            if k > 0:
                # data = {
                #     'ID артикула': row[5],
                #     'ID товара': row[14],
                #     'Склады': 'Наличие в Москве'
                # }
                # for prow in prod_tb:
                
                res = (prod_tb[j], row)
                tb_moscow.append(res)
            # else:
            #     data = {
            #         'ID артикула': row[5],
            #         'ID товара': row[14],
            #         'Склады': 'Склад в Китае'
            #     }
            # table2.write_row(data)
        # print(f'{i}/много')
        # i+=1
    return tb_moscow


def create_backup(tb: list):
    arts = []
    tb = create_csv_table()
    for row in tb:
        try:
            arts.append(row[1][3])
        except:
            print(row)
    with open('backup.txt', 'w', encoding='utf8') as file:
        file.write('\n'.join(arts))


def clear(a: str):
    return re.sub(r'[\?\\\/\*\|\"<>]', '', a)

print(clear('ПРивет, тебя зовут Егор? Я думаю \, /, ты * я < они >, мы | """'))
