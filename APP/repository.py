import abc
import model


class AbstractRepository(abc.ABC):
    """
    Python's provisions for creating class hiearchy abstractions is provided in the module `abc`:
    https://docs.python.org/3.9/library/abc.html
    """

    @abc.abstractmethod
    def add(self, batch: model.Batch):
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, reference) -> model.Batch:
        raise NotImplementedError



class SqlAlchemyRepository(AbstractRepository):
    """
    A concrete SqlAlchemy implementation of the AbstractRepository 
    """

    def __init__(self, session):
        self.session = session

    def add(self, batch):
        self.session.add(batch)

    def get(self, reference):
        return self.session.query(model.Batch).filter_by(reference=reference).one()

    def list(self):
        return self.session.query(model.Batch).all()