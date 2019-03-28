from database import DataBase

from lswf.core.init import sql
import lswf.models.file
import lswf.data_access.file

__all__ = ["sql", "db", "File", ]
File = lswf.models.file.File


db = DataBase({
    File.__name__: lswf.data_access.file.SQL(sql),
})
