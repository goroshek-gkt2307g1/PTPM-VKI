from abc import ABC, abstractmethod

class DatabaseInterface(ABC):
    @abstractmethod
    def get_by_id(self, comment_id : int):
        pass

    @abstractmethod
    def get_by_name(self, username: str):
        pass

    @abstractmethod
    def add(self, comment_id: int, username: str, message: str):
        pass

    @abstractmethod
    def update(self, comment_id: int, new_message: str):
        pass

    @abstractmethod
    def delete(self, comment_id: int):
        pass