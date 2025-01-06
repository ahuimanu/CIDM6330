from dataclasses import dataclass, asdict, field, InitVar
from redbird.repos import CSVFileRepo, MemoryRepo

from abc import ABC, abstractmethod


@dataclass
class FlightPlan:
    id: int
    airline: str
    flightnum: str
    orig: str
    dest: str
    date: int
    dephour: int
    depmin: int
    route: str
    stehour: int
    stemin: int
    altn: str
    pic: str
    picid: int


class BaseRBRepo(ABC):
    @abstractmethod
    def do_create(self, obj):
        pass

    @abstractmethod
    def do_read(self, id):
        pass

    @abstractmethod
    def do_update(self, id, field, value):
        pass

    @abstractmethod
    def do_delete(self, id):
        pass


class MyCSVRepo(BaseRBRepo):
    """
    This class is a wrapper around the CSVFileRepo class from the redbird.repos module.
    Note: CSV files don’t maintain the data types. All field values are considered str and empty values are considered None.
    """

    def __init__(self, filename: str, id_field: str, fieldnames: list):
        self.repo = CSVFileRepo(
            filename=filename, id_field=id_field, fieldnames=fieldnames
        )

    def do_create(self, obj):
        self.repo.insert(obj)

    def do_read(self, id):
        return self.repo[str(id)]

    def do_update(self, id, field, value):
        self.repo[str(id)] = {field: value}

    def do_delete(self, id):
        del self.repo[str(id)]


class MyMemoryRepo(BaseRBRepo):
    def __init__(self, id_field: str):
        # repo = MemoryRepo(id_field="id")
        self.repo = MemoryRepo(id_field=id_field)

    def do_create(self, obj):
        self.repo.insert(obj)

    def do_read(self, id):
        return self.repo[id]

    def do_update(self, id, field, value):
        self.repo[id] = {field: value}

    def do_delete(self, id):
        del self.repo[id]
