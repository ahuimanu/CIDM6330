import unittest

from cart import ShoppingCart
from product import Product


class ShoppingCartTestCase(unittest.TestCase):
    def test_add_and_remove_product(self):
        """
        We can consider this an integration test as it tests a chain of functional units
        """        
        cart = ShoppingCart()
        product = Product('shoes', 'S', 'blue')

        # these are two distinct actions
        cart.add_product(product)
        cart.remove_product(product)

        self.assertDictEqual({}, cart.products)

