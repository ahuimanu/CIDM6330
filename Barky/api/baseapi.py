from abc import ABC, abstractmethod

class AbstractBookMarkAPI(ABC):
    @abstractmethod
    def one(id):
        raise NotImplementedError("Derived classes must implement one")

    @abstractmethod
    def first(filter):
        raise NotImplementedError("Derived classes must implement one")
    
    @abstractmethod    
    def many(filter, sort):
        raise NotImplementedError("Derived classes must implement many")
    
    @abstractmethod    
    def add(bookmark):
        raise NotImplementedError("Derived classes must implement many")

    @abstractmethod    
    def delete(bookmark):
        raise NotImplementedError("Derived classes must implement many")

    @abstractmethod    
    def update(bookmark):
        raise NotImplementedError("Derived classes must implement many")


