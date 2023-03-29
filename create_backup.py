import re


def clear(a: str):
    return re.sub(r'[\?\\\/\*\|\"<>]', '', a)


def create_backup(tb: list):
    arts = []
    for row in tb:
        try:
            arts.append(row[1][3])
        except:
            print(row)
    with open('backup.txt', 'w', encoding='utf8') as file:
        file.write('\n'.join(arts))
