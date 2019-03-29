from database import DataBase

from lswf.core.init import sql

import lswf


__all__ = ["sql", "db", "File", "Directory", "UpdateFrequence"]
File = lswf.models.File
Directory = lswf.models.Directory
SymLink = lswf.models.SymLink
TooBig = lswf.models.TooBig
UpdateFrequence = lswf.models.UpdateFrequence


db = DataBase({
    File.__name__: lswf.data_access.File(sql),
    Directory.__name__: lswf.data_access.Directory(sql),
    SymLink.__name__: lswf.data_access.SymLink(sql),
    TooBig.__name__: lswf.data_access.TooBig(sql),
    'FileUpdateFrequence': lswf.data_access.FileUpdateFrequence(sql),
    'DirectoryUpdateFrequence': lswf.data_access.DirectoryUpdateFrequence(sql),
})
