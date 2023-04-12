import os
from datetime import date
import pandas as pd
import numpy as np

class pdTable:
    def __init__(self, path):
        self.df = pd.read_csv(path, delimiter=';', encoding='cp1251', low_memory=False)

    def create_storages(self):
        out_path = f'output/tables/storages-{date.today().strftime("%d%m%Y")}.csv'
        t =  self.df.loc[self.df['Тип строки'] == 'variant', ['Тип строки', 'ID артикула', 'ID товара', "В наличии @Наличие в Москве"]]
        t['Склады'] = np.where(t['В наличии @Наличие в Москве'] > 0, 'Наличие в Москве', 'Склад в Китае')
        out = t[['ID артикула', 'ID товара', 'Склады']]
        out = out.astype({'ID артикула': int})
        out.to_csv(out_path, sep=';', encoding='cp1251', lineterminator='\n', index=False)
        return out_path

    def get_available(self):
        variants = self.df.loc[
            (self.df['В наличии @Наличие в Москве'] > 0) & (self.df['Тип строки'] == 'variant'), 
            ['Наименование', 'Наименование артикула', 'Код артикула', 'Цена', 'ID товара', 'В наличии @Наличие в Москве', 'Ссылка на витрину']
            ].sort_values('Наименование артикула')
        prods = self.df.loc[
            self.df['Тип строки'] == 'product'
            ].loc[
                self.df['ID товара'].isin(variants['ID товара'].to_numpy()),
                ['ID товара', 'Изображения товаров', 'Бренд']
            ]
        return (variants, prods)
    
    def get_news(self):
        with open('backup/backup.txt', 'r', encoding='utf8') as file:
            olds = file.read().split('\n')
        v, p = self.get_available()
        new_v = v.loc[~v['Код артикула'].isin(olds)]
        new_p = p.loc[p['ID товара'].isin(new_v['ID товара'].to_numpy())]
        return new_v, new_p

    def create_backup(self):
        path = 'backup/backup.txt'
        os.remove('backup/backup.txt')
        v, p = self.get_available()
        data = "\n".join(v['Код артикула'].tolist())
        with open(path, 'w', encoding='utf8') as file:
            file.write(data)

    def get_goods_list(self, google: pd.DataFrame):
        variants = self.df.loc[
            self.df['Тип строки'] == 'variant', 
            ['Код артикула', 'ID артикула', 'ID товара']
            ]
        variants = variants.astype({'ID артикула': int})
        
        return variants