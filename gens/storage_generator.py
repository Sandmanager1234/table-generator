import os
from gens.classes.pd_table import pdTable

def create_storages():
    folder = 'input\\table2\\'
    file = os.listdir(folder)[0]
    d = pdTable(folder+file)
    path = d.create_storages()
    os.remove(folder+file)
    return path