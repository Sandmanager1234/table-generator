import os
import re
import base64
import pdfkit
import imgkit
from datetime import datetime
from classes.table import Table
from excel_generator import create_rozn_table, add_rozn_row, create_opt_table, add_opt_row, create_price


def clear(a: str):
    return re.sub(r'[\?\\\/\*\|\"<>]', '', a)


def create_backup(tb: list):
    arts = []
    # tb = create_csv_table()
    for row in tb:
        try:
            arts.append(row[1][3])
        except:
            print(row)
    with open(f'output\\files\\backup-{datetime.today().strftime("%d%m%Y")}.txt', 'w', encoding='utf8') as file:
        file.write('\n'.join(arts))


def bySize(duo: tuple):
    return duo[1][2]


def delim(a: list, i: int):
    b = []
    c = a[0:i]
    b.append(c)
    del a[0:i]
    if len(a) != 0:
        b.extend(delim(a, i))
    return b


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
                print(row)
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


def find_new_goods(tb: list):
    with open('backup.txt', 'r', encoding='utf8') as file:
        arts = file.read().split('\n')
    tb_new = []
    for duo in tb:
        if duo[1][3] not in arts:
            tb_new.append(duo)
    return tb_new


def create_excel_rozn_table(tb_aviable, tb_new, cny, p_type, margin, r_size):
    file_path = create_rozn_table()
    for i in range(len(tb_aviable)):
        # try:
        add_rozn_row(i, file_path, tb_aviable[i], p_type, cny, margin, r_size, tb_new)
        # except Exception as ex:
            # print(ex)
            # print(tb_aviable[i])
            # exit()


def create_excel_opt_table(tb_aviable, tb_new, cny, opt_p_type, opt_margin, opt_r_size, rozn_p_type, rozn_margin, rozn_r_size):
    file_path = create_opt_table()
    for i in range(len(tb_aviable)):
        add_opt_row(i, file_path, tb_aviable[i], opt_p_type, cny, opt_margin, opt_r_size, rozn_p_type, rozn_margin, rozn_r_size, tb_new)


def create_photo(path, i):
    conf = imgkit.config(wkhtmltoimage=r'C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltoimage.exe')
    if i == 0:
        file_name = 'Новинки.png'
    else:
        file_name = f'Новинки ({i}).png'
    imgkit.from_file(path, f'output\\files\\{file_name}', config=conf)
    


def create_pdf(path, type):
    conf = pdfkit.configuration(wkhtmltopdf=r'C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe')
    pdfkit.from_file(path, f'output\\files\\{type}-{datetime.today().strftime("%d%m%Y")}.pdf', configuration=conf)


def create_rozn_html(tb_av, tb_new, cny, p_type, margin, r_size, text, news=False):
    today = datetime.today()
    if news == True:
        path = f'output\\files\\new-rozn-{today.strftime("%d%m%Y")}.html'
    else:
        path = f'output\\files\\rozn-{today.strftime("%d%m%Y")}.html'
    html_page = open(path, 'w', encoding='utf8')
    j = 0
    with open('html_patterns\\rozn_head.html', 'r', encoding='utf8') as file:
        head = file.read() 

    with open('html_patterns\\rozn_bottom.html', 'r', encoding='utf8') as file:
        bott = file.read()
    filename = os.listdir("input\picrozn")[0]
    with open(f'input\\picrozn\\{filename}', 'rb') as file:
        string_b64_image = base64.b64encode(file.read()).decode()

    rh = head.split('\n')
    rh[426] = rh[426].replace('src=""', f'src="data:image/png;base64,{string_b64_image}"')
    rh[424] = rh[424].replace('Sample text', text)
    fin_head = '\n'.join(rh)

    html_page.write(fin_head)

    for row in tb_av:
        form = row[0][35].split('.')[-1]
        if row in tb_new:
            with open('html_patterns\\rozn_row_with_new.html', 'r', encoding='utf8') as file:
                hrow = file.read()
        else:
            with open('html_patterns\\rozn_row_no_new.html', 'r', encoding='utf8') as file:
                hrow = file.read()

        with open(f"excel_images\\small\\pic_{clear(row[1][3])}_small.{form}", "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read())
        rb = hrow.split('\n')
        rb[1] = rb[1].replace('></td>', f'>{row[1][2]}</td>')
        rb[2] = rb[2].replace('src=""', f'src="data:image/png;base64,{encoded_string.decode()}"').replace("name=''", f"name='рисунок {j}'")
        rb[3] = rb[3].replace('></td>', f'>{create_price(p_type, cny, margin, row[1][6], r_size)}</td>') 
        rb[4] = rb[4].replace('href=""', f'href="https://exclusive-only.ru/{row[1][25]}"').replace("<span style='display:none'></span>", f"<span style='display:none'>.ru/{row[1][25]}</span>")
        rb[5] = rb[5].replace('></td>', f'>{row[0][28]}</td>') 
        rb[6] = rb[6].replace('></td>', f'>{row[1][1]}</td>') 
        rb[7] = rb[7].replace('></td>', f'>{row[1][3]}</td>')
        new_row = '\n'.join(rb) 
        html_page.write(new_row)
        j += 1
    html_page.write(bott)
    html_page.close()
    return path


def create_opt_html(tb_av, tb_new, cny, rozn_p_type, rozn_margin, rozn_r_size, opt_p_type, opt_margin, opt_r_size, text):
    today = datetime.today()
    path = f'output\\files\\opt-{today.strftime("%d%m%Y")}.html'
    html_page = open(path, 'w', encoding='utf8')
    j = 0
    with open('html_patterns\\opt_head.html', 'r', encoding='utf8') as file:
        head = file.read() 

    with open('html_patterns\\opt_bottom.html', 'r', encoding='utf8') as file:
        bott = file.read()
    
    filename = os.listdir("input\\picopt")[0]
    with open(f'input\\picopt\\{filename}', 'rb') as file:
        string_b64_image = base64.b64encode(file.read()).decode()

    rh = head.split('\n')

    rh[422] = rh[422].replace('Sample text', text).replace('src=""', f'src="data:image/png;base64,{string_b64_image}"')

    fin_head = '\n'.join(rh)

    html_page.write(fin_head)

    for row in tb_av:
        form = row[0][35].split('.')[-1]
        if row in tb_new:
            with open('html_patterns\\opt_row_with_new.html', 'r', encoding='utf8') as file:
                hrow = file.read()
        else:
            with open('html_patterns\\opt_row_no_new.html', 'r', encoding='utf8') as file:
                hrow = file.read()

        with open(f"excel_images\\small\\pic_{clear(row[1][3])}_small.{form}", "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read())
        rb = hrow.split('\n')
        rb[1] = rb[1].replace('></td>', f'>{row[1][2]}</td>')
        rb[2] = rb[2].replace('src=""', f'src="data:image/png;base64,{encoded_string.decode()}"').replace("name=''", f"name='рисунок {j}'")
        rb[4] = rb[4].replace('></td>', f'>{create_price(opt_p_type, cny, opt_margin, row[1][6], opt_r_size)}</td>') 
        rb[3] = rb[3].replace('></td>', f'>{create_price(rozn_p_type, cny, rozn_margin, row[1][6], rozn_r_size)}</td>') 
        rb[5] = rb[5].replace('></td>', f'>{row[0][28]}</td>') 
        rb[6] = rb[6].replace('></td>', f'>{row[1][1]}</td>') 
        rb[7] = rb[7].replace('></td>', f'>{row[1][3]}</td>')
        rb[8] = rb[8].replace('></td>', f'>{row[1][12]}</td>')
        new_row = '\n'.join(rb) 
        html_page.write(new_row)
        j += 1
    html_page.write(bott)
    html_page.close()
    return path


def create_rozn(cny, rozn_p_type, rozn_margin, rozn_r_size):
    tb_av = create_csv_table()
    tb_new = find_new_goods(tb_av)
    create_excel_rozn_table(tb_av, tb_new, cny, rozn_p_type, rozn_margin, rozn_r_size)
    create_rozn_html(tb_av, tb_new, cny, rozn_p_type, rozn_margin, rozn_r_size)


def create_opt(cny, rozn_p_type, rozn_margin, rozn_r_size, opt_p_type, opt_margin, opt_r_size):
    tb_av = create_csv_table()
    tb_new = find_new_goods(tb_av)
    create_excel_opt_table(tb_av, tb_new, cny, opt_p_type, opt_margin, opt_r_size, rozn_p_type, rozn_margin, rozn_r_size)
    create_opt_html(tb_av, tb_new, cny, opt_p_type, opt_margin, opt_r_size, rozn_p_type, rozn_margin, rozn_r_size)


def create_both(cny, rozn_p_type, rozn_margin, rozn_r_size, opt_p_type, opt_margin, opt_r_size, r_text, o_text, text_news):
    # Создаю CSV и возвращаю табличку имеющихся на складах кроссовок
    tb_av = create_csv_table()
    tb_av.sort(key=bySize)
    # Нахожу новинки
    tb_new = find_new_goods(tb_av)
    save_tb(tb_av, 'availiable')
    save_tb(tb_new, 'news')
    # Создаю табличку с розницей
    create_excel_rozn_table(tb_av, tb_new, cny, rozn_p_type, rozn_margin, rozn_r_size)
    # # Создаю табличку с оптом
    # create_excel_opt_table(tb_av, tb_new, cny, opt_p_type, opt_margin, opt_r_size, rozn_p_type, rozn_margin, rozn_r_size)
    # # Создаю html
    # opt_path = create_opt_html(tb_av, tb_new, cny, opt_p_type, opt_margin, opt_r_size, rozn_p_type, rozn_margin, rozn_r_size, o_text)
    rozn_path = create_rozn_html(tb_av, tb_new, cny, rozn_p_type, rozn_margin, rozn_r_size, r_text)
    # # Создаю pdf
    # create_pdf(opt_path, 'opt')
    create_pdf(rozn_path, 'rozn')
    # Create news
    del_news = delim(tb_new, 9)
    i = 0
    create_backup(tb_av)
    for tb in del_news:
        news_path = create_rozn_html(tb, tb_new, cny, rozn_p_type, rozn_margin, rozn_r_size, text_news, news=True)
        create_photo(news_path, i)
        i += 1


def save_tb(tb, type):
    file = open(f'tb-{type}.txt', 'w', encoding='utf8')
    for duo in tb:
        for row in duo:
            rw = ';'.join(row)
            file.write(f'{rw}\n')
    file.close()

def main():
    currency = 11.9
    r_p_type = 1
    r_m = 0
    rrs = 10
    opt = 2
    om = 0
    ors = 10
    r_txt = 'Прайс лист наличие Москва Exclusive Only<br>19.03.23<br>Cайт: <a href="https://exclusive-only.ru/" style=\'text-decoration:none;\' target="_parent">https://exclusive-only.ru</a><br>Телеграм канал: <a href="https://exclusive-only.ru/shoes/telegram-kanal" style=\'text-decoration:none;\' target="_parent">https://exclusive-only.ru/shoes/telegram-kanal</a><br>Авито профиль и отзывы: <a href="https://vk.cc/chKyDn" style=\'text-decoration:none;\' target="_parent">https://vk.cc/chKyDn</a><br>Телефон: +7-495-204-19-30'
    o_txt = 'Прайс-лист, наличие Москва<br>06.03.23'
    n_txt = 'Новинки (Москва)<br>Поступление на склад в Москву'
    create_both(
        currency,
        r_p_type,
        r_m,
        rrs,
        opt,
        om,
        ors,
        r_txt,
        o_txt,
        n_txt
    )


if __name__ == '__main__':
    main()

# Починить отображение картинок у новинок, сохранять с названием артикула
# Добавить вариации опту "С розничной ценой" и "Без розничной цены"
# Нормальная вставка картинок в excel_generator.py 
# Изменить алгоритм новинок, добавить бэкап прошлой генерации с артикулами \/
