from lswf.service.init import sql
import lswf.data.implemented.file

__all__ = ["sql", "db", "File", ]
File = lswf.data.implemented.file.File


class SQL_Service:
    sql_services = {
        File.__name__: lswf.data.implemented.file.SQL_Service(),
    }

    def __getattr__(self, name):
        def chose_service(obj, *args):
            service_name = obj.__class__.__name__
            f = getattr(self.sql_services[service_name], name)
            return f(obj, *args)

        return chose_service


db = SQL_Service()
