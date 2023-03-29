import os
import re
import base64
import zipfile
from datetime import datetime
import pdfkit
import imgkit
import pandas as pd
from classes.table import Table
from classes.pd_table import pdTable
from excel_generator import create_rozn_table, add_rozn_row, create_opt_table, add_opt_row, create_price


def html_to_str(a: str):
    b = re.sub(r'<br>', '\n', a)
    c = re.sub(r'<[^>]*>', '', b)
    return c


def create_zip():
    newzip = zipfile.ZipFile('output\\zips\\result.zip', 'w', zipfile.ZIP_DEFLATED)
    folder = 'output\\files\\'
    files = os.listdir(folder)
    for file in files:
        newzip.write(folder+file)
    newzip.close()


def clear_cache():
    folders = [
        'excel_images/small/',
        # 'output/files/',
        # 'output/tables/',
        'input/picopt/',
        'input/picrozn/',
        'input/table1/',
        'input/table2/'
    ]
    for folder in folders:
        files = os.listdir(folder)
        for file in files:
            os.remove(folder+file)

def clear(a: str):
    return re.sub(r'[\?\\\/\*\|\"<>]', '', a)


def delim(v, srez: int):
    counts = int(v.shape[0] / srez) + 1
    res = []
    for i in range(counts):
        start = i * 9
        end = 9 + i * 9
        res.append(v.iloc[start:end])
    return res


def create_excel_rozn_table(vp_aviable: tuple[pd.DataFrame], vp_new: tuple[pd.DataFrame], cny, p_type, margin, r_size, r_text):
    file_path = create_rozn_table(r_text)
    v, p = vp_aviable
    nv, vp = vp_new
    for i, row in enumerate(v.iterrows()):
        add_rozn_row(i, file_path, row[1], p_type, cny, margin, r_size, nv, p)


def create_excel_opt_table(vp_aviable: tuple[pd.DataFrame], vp_new: tuple[pd.DataFrame], cny, opt_p_type, opt_margin, opt_r_size, rozn_p_type, rozn_margin, rozn_r_size, o_text, flag):
    file_path = create_opt_table(o_text, flag)
    v, p = vp_aviable
    nv, vp = vp_new
    for i, row in enumerate(v.iterrows()):
        add_opt_row(i, file_path, row[1], opt_p_type, cny, opt_margin, opt_r_size, rozn_p_type, rozn_margin, rozn_r_size, nv, p)


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


def create_rozn_html(vp_av: tuple[pd.DataFrame], vp_new: tuple[pd.DataFrame], cny, p_type, margin, r_size, text, news=False):
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
    v, p = vp_av
    nv, np = vp_new
    for row in v.iterrows():
        _row = row[1]
        img_url = p.loc[p['ID товара'] == _row['ID товара'], ['Изображения товаров']].values.item(0)
        form = img_url.split('.')[-1]
        if _row['Код артикула'] in nv['Код артикула'].to_numpy():
            with open('html_patterns\\rozn_row_with_new.html', 'r', encoding='utf8') as file:
                hrow = file.read()
        else:
            with open('html_patterns\\rozn_row_no_new.html', 'r', encoding='utf8') as file:
                hrow = file.read()

        with open(f"excel_images\\small\\pic_{clear(_row['Код артикула'])}_small.{form}", "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read())
        rb = hrow.split('\n')
        rb[1] = rb[1].replace('></td>', f'>{_row["Наименование артикула"]}</td>')
        rb[2] = rb[2].replace('src=""', f'src="data:image/png;base64,{encoded_string.decode()}"').replace("name=''", f"name='рисунок {j}'")
        rb[3] = rb[3].replace('></td>', f'>{create_price(p_type, cny, margin, _row["Цена"], r_size)}</td>') 
        rb[4] = rb[4].replace('href=""', f'href="https://exclusive-only.ru/{_row["Ссылка на витрину"]}"').replace("<span style='display:none'></span>", f"<span style='display:none'>.ru/{_row['Ссылка на витрину']}</span>")
        rb[5] = rb[5].replace('></td>', f'>{p.loc[p["ID товара"] == _row["ID товара"]["Изображения товаров"]].values.item(0)}</td>') 
        rb[6] = rb[6].replace('></td>', f'>{_row["Наименование"]}</td>') 
        rb[7] = rb[7].replace('></td>', f'>{_row["Код артикула"]}</td>')
        new_row = '\n'.join(rb) 
        html_page.write(new_row)
        j += 1
    html_page.write(bott)
    html_page.close()
    return path


def create_opt_html(vp_av, vp_new, cny, rozn_p_type, rozn_margin, rozn_r_size, opt_p_type, opt_margin, opt_r_size, text, flag, news=False):
    today = datetime.today()
    if news == True:
        path = f'output\\files\\news-{today.strftime("%d%m%Y")}.html'
    else:   
        path = f'output\\files\\opt-{today.strftime("%d%m%Y")}.html'
    html_page = open(path, 'w', encoding='utf8')
    j = 0
    if flag == True:
        dop = '_with_rozn'
    else:
        dop = 'no_rozn'
    with open(f'html_patterns\\opt_head{dop}.html', 'r', encoding='utf8') as file:
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
    v, p = vp_av
    nv, np = vp_new
    for row in v.iterrows():
        _row = row[1]
        img_url = p.loc[p['ID товара'] == _row['ID товара'], ['Изображения товаров']].values.item(0)
        form = img_url.split('.')[-1]
        if _row["Код артикула"] in nv['Код артикула'].to_numpy():
            with open(f'html_patterns\\opt_row_with_new{dop}.html', 'r', encoding='utf8') as file:
                hrow = file.read()
        else:
            with open(f'html_patterns\\opt_row_no_new{dop}.html', 'r', encoding='utf8') as file:
                hrow = file.read()

        with open(f"excel_images\\small\\pic_{clear(_row['Код артикула'])}_small.{form}", "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read())
        if flag == True:
            rb = hrow.split('\n')
            rb[1] = rb[1].replace('></td>', f'>{_row["Наименвание артикула"]}</td>')
            rb[2] = rb[2].replace('src=""', f'src="data:image/png;base64,{encoded_string.decode()}"').replace("name=''", f"name='рисунок {j}'")
            rb[4] = rb[4].replace('></td>', f'>{create_price(opt_p_type, cny, opt_margin, _row["Цена"], opt_r_size)}</td>') 
            if flag == True:
                rb[3] = rb[3].replace('></td>', f'>{create_price(rozn_p_type, cny, rozn_margin, _row["Цена"], rozn_r_size)}</td>') 
            rb[5] = rb[5].replace('></td>', f'>{p.loc[p["ID товара"] == _row["ID товара"], ["Бренд"]].values.item(0)}</td>') 
            rb[6] = rb[6].replace('></td>', f'>{_row["Наименование"]}</td>') 
            rb[7] = rb[7].replace('></td>', f'>{_row["Код артикула"]}</td>')
            rb[8] = rb[8].replace('></td>', f'>{_row["В наличии @Наличие в Москве"]}</td>')
        new_row = '\n'.join(rb) 
        html_page.write(new_row)
        j += 1
    html_page.write(bott)
    html_page.close()
    return path


def create_rozn(vp_av, vp_new, cny, rozn_p_type, rozn_margin, rozn_r_size, r_text):
    # Создаю табличку с розницей
    clear_text = html_to_str(r_text)
    create_excel_rozn_table(vp_av, vp_new, cny, rozn_p_type, rozn_margin, rozn_r_size, clear_text)
    rozn_path = create_rozn_html(vp_av, vp_new, cny, rozn_p_type, rozn_margin, rozn_r_size, r_text)
    create_pdf(rozn_path, 'rozn')


def create_opt(vp_av, vp_new, cny, opt_p_type, opt_margin, opt_r_size, rozn_p_type, rozn_margin, rozn_r_size, o_text, flag):
    clear_text = html_to_str(o_text)
    # Создаю табличку с оптом
    create_excel_opt_table(vp_av, vp_new, cny, opt_p_type, opt_margin, opt_r_size, rozn_p_type, rozn_margin, rozn_r_size, clear_text, flag)
    # Создаю html
    opt_path = create_opt_html(vp_av, vp_new, cny, opt_p_type, opt_margin, opt_r_size, rozn_p_type, rozn_margin, rozn_r_size, o_text, flag)
    create_pdf(opt_path, 'opt')


def create_tables(cny, rozn_p_type, rozn_margin, rozn_r_size, opt_p_type, opt_margin, opt_r_size, r_text, o_text, text_news, or_flag, flag):
    path = 'input/table2/' + os.listdir('input/table2/')[0]
    d = pdTable(path)
    vp_av = d.get_available()
    # Нахожу новинки
    vp_new = d.get_news()

    if or_flag == 'ro':
        create_rozn(vp_av, vp_new, cny, rozn_p_type, rozn_margin, rozn_r_size, r_text)
        create_opt(vp_av, vp_new, cny, opt_p_type, opt_margin, opt_r_size, rozn_p_type, rozn_margin, rozn_r_size, o_text, flag)
    elif or_flag == 'r':
        create_rozn(vp_av, vp_new, cny, rozn_p_type, rozn_margin, rozn_r_size, r_text)
    elif or_flag == 'o':
        create_opt(vp_av, vp_new, cny, opt_p_type, opt_margin, opt_r_size, rozn_p_type, rozn_margin, rozn_r_size, o_text, flag)
    else:
        print('Error: or_flag value.')
        exit()
    
    del_news = delim(vp_new, 9)
    i = 0
    d.create_backup()
    for tb in del_news:
        if or_flag == 'o':
            news_path = create_opt_html(vp_av, vp_new, cny, opt_p_type, opt_margin, opt_r_size, rozn_p_type, rozn_margin, rozn_r_size, o_text, flag, news = True)
        else:
            news_path = create_rozn_html(tb, vp_new, cny, rozn_p_type, rozn_margin, rozn_r_size, text_news, news=True)
        create_photo(news_path, i)
        i += 1
    os.remove('output\\files\\new-rozn-19032023.html')
    create_zip()

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
    flag = True
    or_flag = 'ro'
    create_tables(
        currency,
        r_p_type,
        r_m,
        rrs,
        opt,
        om,
        ors,
        r_txt,
        o_txt,
        n_txt,
        or_flag,
        flag,
    )
    clear_cache()

if __name__ == '__main__':
    main()
