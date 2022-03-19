class Product:
    """
    Represents a product in an e-commerce system.
    A product has:
        name
        size
        color
    Produces a stock keeping unit (SKU).
    A SKU is a unique, internal ID used by companies
    for pricing and inventory that often uses an all-uppercase format.
    """

    def __init__(self, name, size, color):
        self.name = name
        self.size = size
        self.color = color

    def __str__(self) -> str:
        return f"This shoe, {self.name}, has a size of {self.size} and is {self.color} in color"

    def __repr__(self) -> str:
        return f"REPR: name: {self.name} size:{self.size} color:{self.color}"

    def transform_name_for_sku(self):
        return self.name.upper()

    def transform_color_for_sku(self):
        return self.color.upper()

    def generate_sku(self):
        """
        Generates a SKU for this product.

        Example:
            >>> small_black_shoes = Product('shoes', 'S', 'black')
            >>> small_black_shoes.generate_sku()
            'SHOES-S-BLACK'
        """
        name = self.transform_name_for_sku()
        color = self.transform_color_for_sku()
        return f"{name}-{self.size}-{color}"
