
from abc import ABCMeta, abstractmethod


class SQLService(metaclass=ABCMeta):
    @property
    @abstractmethod
    def table():
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def create(obj):
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def read(obj):
        """
            take one unique property or the key id
            return None if not found
        """
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def update(obj):
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def delete(obj):
        raise NotImplementedError

    def update_or_create(self, obj):
        if not obj.key:
            self.read(obj)
        if obj.key:
            self.update(obj)
        else:
            self.create(obj)
