import os
from tools.pip_my_term import Color
import tools.path.size

from lswf.database import sql


def list_frequently_modify(frequency, limit):
    sql_general = """
        select count({file_or_dir}_id) as update_frequency, path
        from {file_or_dir}
        JOIN {file_or_dir}_update_frequence USING ({file_or_dir}_id)

        group by path
        HAVING update_frequency > ?
        ORDER by update_frequency desc
        LIMIT ?
    """
    sql_file = sql(sql_general.format(file_or_dir='file'),
                   frequency, limit)
    sql_dir = sql(sql_general.format(file_or_dir='directory'),
                  frequency, limit)
    return sql_file, sql_dir


def extract_already_in_ram(li, li_symlink):
    deleted = []
    for el in li[:]:
        splited_path = os.path.join(el[1], 'will_be_splited')
        while True:
            splited_path, rest = os.path.split(splited_path)
            if rest == '':
                break
            if splited_path in li_symlink:
                li.remove(el)
                deleted.append((el, splited_path))
                break
    return deleted


def print_frequently_modify_and_in_ram(frequency, limit):
    file, dir = list_frequently_modify(frequency, limit)
    path_already_in_ram = []
    li_symlink = list(map(lambda t: t[0], sql('select path from symlink')))
    path_already_in_ram += extract_already_in_ram(file, li_symlink)
    path_already_in_ram += extract_already_in_ram(dir, li_symlink)

    print('\n')
    print_table(('update frequency', 'directory path'), dir)
    print('\n\n')
    print_table(('update frequency', 'file path'), file)
    print('\n\n')
    print_table(
        ('update frequency', 'path already in RAM', 'from symlinked path'),
        map(lambda t: (t[0][0], t[0][1], t[1]), path_already_in_ram))

    print('\n\n')
    total_size = 0

    def get_and_store_size(path):
        nonlocal total_size
        size = tools.path.size.get_size(path, human_readable=False)
        total_size += size
        return tools.path.size.convert_to_human(size)

    print_table(('            size', 'path in RAM'),
                map(lambda path: (get_and_store_size(path), path), li_symlink))

    c = Color.c
    print('\n{} {}'.format(c('  Total:', 'BOLD', 'WARNING'),
                           tools.path.size.convert_to_human(total_size)))


def print_table(col_names, data):
    c = Color.c
    extra = "    {}" if len(col_names) == 3 else ""
    row_format = "{:>16}" + "    {:<80}" + extra
    print(row_format.format(*(map(lambda m: c(m, 'OKBLUE'), col_names))))
    for row in data:
        print(row_format.format(*row))
