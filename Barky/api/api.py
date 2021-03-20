from abc import ABC, abstractmethod

class AbstractBookMarkAPI(ABC):
    @abstractmethod
    def one(id):
        raise NotImplementedError("Derived classes must implement one")
    
    def many(filter):
        raise NotImplementedError("Derived classes must implement many")
    
    def add()