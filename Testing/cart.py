from collections import defaultdict


class ShoppingCart:
    """
    Contains methods to add and remove a product to and from a products dictionary
    What is a Dictionary? https://www.w3schools.com/python/python_dictionaries.asp
    """

    def __init__(self):
        self.products = defaultdict(lambda: defaultdict(int))

    def add_product(self, product, quantity=1):
        self.products[product.generate_sku()]["quantity"] += quantity

    def remove_product(self, product, quantity=1):
        sku = product.generate_sku()
        self.products[sku]["quantity"] -= quantity
        if self.products[sku]["quantity"] == 0:
            del self.products[sku]
