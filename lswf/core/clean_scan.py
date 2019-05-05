
from datetime import datetime

from lswf.database import sql


def del_older_than(delta):
    too_old = datetime.now() - delta

    def sql_delete_time(table):
        sql("""DELETE from {}_update_frequence
            where update_time < ?""".format(table), too_old)
        sql("""delete from {table}
            where not EXISTS
            (
                select 1 from {table}_update_frequence
                where {table}.{table}_id = {table}_update_frequence.{table}_id)
            """.format(table=table))

    sql_delete_time("file")
    sql_delete_time("directory")
