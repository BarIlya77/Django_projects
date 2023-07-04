from django.test import TestCase
from shopapp.utils import add_two_numbers


# Create your tests here.
class AddTwoNumbersTestCase(TestCase):
    def test_add_two_numbers(self):
        result = add_two_numbers(3, 4)
        self.assertEqual(result, 7)


# class ProductCreateViewTestCase(TestCase):
#     def test_order_create_view(self):


