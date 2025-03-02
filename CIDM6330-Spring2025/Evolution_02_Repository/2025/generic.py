from abc import ABC, abstractmethod
from dataclasses import dataclass, asdict, field, InitVar
import csv


# typehints review

# For most types, just use the name of the type in the annotation
# Note that mypy can usually infer the type of a variable from its value,
# so technically these annotations are redundant
x: int = 1
x: float = 1.0
x: bool = True
x: str = "test"
x: bytes = b"test"

# For collections on Python 3.9+, the type of the collection item is in brackets
x: list[int] = [1]
x: set[int] = {6, 7}

# For mappings, we need the types of both keys and values
x: dict[str, float] = {"field": 2.0}  # Python 3.9+

# For tuples of fixed size, we specify the types of all the elements
x: tuple[int, str, float] = (3, "yes", 7.5)  # Python 3.9+

# For tuples of variable size, we use one type and ellipsis
x: tuple[int, ...] = (1, 2, 3)  # Python 3.9+

# On Python 3.10+, use the | operator when something could be one of a few types
x: list[int | str] = [3, 5, "test", "fun"]  # Python 3.10+


@dataclass
class Product:
    id: int
    name: str
    price: float


class BaseProductRepository(ABC):
    @abstractmethod
    def do_create(self, product: Product):
        pass

    @abstractmethod
    def read_all(self):
        pass

    @abstractmethod
    def do_read(self, id):
        pass

    @abstractmethod
    def do_update(self, id, product: Product):
        pass

    @abstractmethod
    def do_delete(self, id):
        pass


class MyCSVRepo(BaseProductRepository):
    """
    Note: CSV files don’t maintain data types. All field values are considered str and empty values are considered None.
    """

    def __init__(self, filename: str, id_field: str, fieldnames: list):

        self.repo = list[Product] # this is a typehint for a list of Product objects
        self.filename = filename
        self.fieldnames = fieldnames

        with open(filename, mode="r", newline="") as file:
            csv_reader = csv.DictReader(file)
            # list comprehension: https://www.w3schools.com/python/python_lists_comprehension.asp
            self.repo = [Product(**row) for row in csv_reader]

    def do_create(self, product: Product):
        self.repo.append(product)
        self.do_save_file()

    def read_all(self):
        return self.repo

    def do_read(self, id):
        return self.repo[str(id)]

    def do_update(self, id, product: Product):
        self.repo[str(id)] = product
        self.do_save_file()

    def do_delete(self, id):
        for product in self.repo:
            if int(product.id) == int(id):
                self.repo.remove(product)
                break

        self.do_save_file()

    def do_save_file(self):
        with open(self.filename, mode="w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=self.fieldnames)
            writer.writeheader()
            for product in self.repo:
                writer.writerow(asdict(product))


class MyMemoryRepo(BaseProductRepository):

    def __init__(self, id_field: str):

        self.repo = list[Product]

    def do_create(self, product: Product):
        self.repo.append(product)

    def read_all(self):
        return self.repo

    def do_read(self, id):
        return self.repo[id]

    def do_update(self, id, product: Product):
        self.repo[id] = product

    def do_delete(self, id):
        for product in self.repo:
            if int(product.id) == int(id):
                self.repo.remove(product)
                break
        


# Defining main function
def main():
    print("generic repository example")
    csv_repo = MyCSVRepo("products.csv", "id", ["id", "name", "price"])
    # csv_repo.do_create(Product(1, "apple", 1.99))
    # csv_repo.do_create(Product(2, "banana", 0.99))
    # csv_repo.do_create(Product(3, "cherry", 2.99))

    # csv_repo.do_create(Product(4, "pear", 1.59))
    # csv_repo.do_create(Product(5, "raspberry", 1.09))
    # csv_repo.do_create(Product(6, "lemon", 0.59))

    # csv_repo.do_create(Product(7, "pineapple", 5.99))
    csv_repo.do_delete(3)

    print(csv_repo.read_all())


# Using the special variable
# __name__
if __name__ == "__main__":
    main()
