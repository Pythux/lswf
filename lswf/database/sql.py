from lswf.service.init import sql
import lswf.models.file
import lswf.data_access.file_DAO

__all__ = ["sql", "db", "File", ]
File = lswf.models.file.File


class SQL:
    dict_entity = {
        File.__name__: lswf.data_access.file_DAO.SQL(),
    }

    def __getattr__(self, name):
        def chose_service(obj, *args):
            entity_name = obj.__class__.__name__
            f = getattr(self.dict_entity[entity_name], name)
            return f(obj, *args)

        return chose_service


db = SQL()
