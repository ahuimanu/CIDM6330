import abc
from allocation.domain import model

from sqlalchemy import select


class AbstractRepository(abc.ABC):
    @abc.abstractmethod
    def add(self, batch: model.Product):
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, sku) -> model.Product:
        raise NotImplementedError


class SqlAlchemyRepository(AbstractRepository):
    def __init__(self, session):
        self.session = session

    def add(self, product):
        self.session.add(product)

    def get(self, sku):
        return self.session.scalars(
            select(model.Product).filter_by(sku=sku)
        ).first()

