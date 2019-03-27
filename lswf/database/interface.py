
from abc import ABCMeta, abstractmethod
from lswf.data.database.sql_helper import SQLHelper


class SQL(SQLHelper, metaclass=ABCMeta):
    @property
    @abstractmethod
    def table():
        raise NotImplementedError

    @property
    @abstractmethod
    def key_name():
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def create(obj):
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def read(obj):
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def update(obj):
        raise NotImplementedError

    def delete(self, obj):
        self._delete(obj)

    def update_or_create(self, obj):
        if not obj.key:
            self.read(obj)
        if obj.key:
            self.update(obj)
        else:
            self.create(obj)
