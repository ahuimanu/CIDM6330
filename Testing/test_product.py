import unittest

from product import Product

"""
Recall the basic steps of a functional test:
* Set up the inputs.
* Identify the expected output.
* Obtain the actual output.
* Compare the expected and actual outputs.

Put another way, we call this:
* Arrange
* Act 
* Assert
"""

class ProductTestCase(unittest.TestCase):
    def test_working(self):
        pass

    def test_transform_name_for_sku(self):
        #arrange
        small_black_shoes = Product('shoes', 'S', 'black')
        expected_value = 'SHOES'
        #act
        actual_value = small_black_shoes.transform_name_for_sku()
        #assert
        self.assertEqual(expected_value, actual_value)    

