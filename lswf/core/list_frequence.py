
from tools.pip_my_term import Color

from lswf.database import sql


def list_frequently_modify(frequency, limit):
    sql_general = """
        select path, count({file_or_dir}_id) as update_frequency
        from {file_or_dir}
        JOIN {file_or_dir}_update_frequence USING ({file_or_dir}_id)

        group by path
        HAVING update_frequency > ?
        ORDER by update_frequency desc
        LIMIT ?
    """
    sql_dir = sql(sql_general.format(file_or_dir='directory'),
                  frequency, limit)
    sql_file = sql(sql_general.format(file_or_dir='file'),
                   frequency, limit)

    print('\n')
    print_table(('update frequency', 'directory path'), map(reversed, sql_dir))
    print('\n\n')
    print_table(('update frequency', 'file path'), map(reversed, sql_file))


def print_table(list_names, data):
    c = Color.c
    row_format = "{:>16}    {:<20}"
    print(row_format.format(*(map(lambda m: c(m, 'OKBLUE'), list_names))))
    for row in data:
        print(row_format.format(*row))
