from database import DataBase

from lswf.core.init import sql

import lswf


__all__ = ["sql", "db", "File", "Directory", "UpdateFrequence"]
File = lswf.models.File
Directory = lswf.models.Directory
SymLink = lswf.models.SymLink
UpdateFrequence = lswf.models.UpdateFrequence


db = DataBase({
    File.__name__: lswf.data_access.File(sql),
    Directory.__name__: lswf.data_access.Directory(sql),
    SymLink.__name__: lswf.data_access.SymLink(sql),
    'FileUpdateFrequence': lswf.data_access.FileUpdateFrequence(sql),
    'DirectoryUpdateFrequence': lswf.data_access.DirectoryUpdateFrequence(sql),
})
