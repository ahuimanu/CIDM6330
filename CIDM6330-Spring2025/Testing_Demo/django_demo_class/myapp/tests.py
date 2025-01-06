from django.test import TestCase
from .forms import ItemForm


class ItemFormTests(TestCase):
    def test_item_form_valid(self):
        """
        Test that the ItemForm is valid when provided with valid data.
        """
        # Add test 1 here
        form_data = {
            "name": "Test Item",
            "description": "text text",
            "price": 9.99,
            "quantity": 10,
        }
        form = ItemForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_item_form_invalid(self):
        """
        Test that the ItemForm is invalid when required fields are missing.
        """
        # Add test 2 here
        form_data = {
            "name": "",
            "description": "text text",
            "price": 9.99,
            "quantity": 10,
        }
        form = ItemForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("name", form.errors)

    def test_item_form_invalid_price(self):
        """
        Test that the ItemForm is invalid when price is negative or zero.
        """
        # Add test 3 here
        form_data = {
            "name": "abcd",
            "description": "text text",
            "price": -9.99,
            "quantity": 10,
        }
        form = ItemForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("price", form.errors)

    def test_item_form_invalid_quantity(self):
        """
        Test that the ItemForm is invalid when quantity is negative or zero.
        """
        # Add test 4 here
        form_data = {
            "name": "abcd",
            "description": "text text",
            "price": 9.99,
            "quantity": -10,
        }
        form = ItemForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("quantity", form.errors)
