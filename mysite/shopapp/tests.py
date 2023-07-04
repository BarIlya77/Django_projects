from random import choices
from string import ascii_letters

from django.contrib.auth.models import User, Permission
from django.test import TestCase
from django.urls import reverse
from shopapp.utils import add_two_numbers

from shopapp.models import Product, Order


# Create your tests here.
class AddTwoNumbersTestCase(TestCase):
    def test_add_two_numbers(self):
        result = add_two_numbers(1, 4)
        self.assertEqual(result, 5)


class ProductCreateViewTestCase(TestCase):
    def setUp(self) -> None:
        self.product_name = ''.join(choices(ascii_letters, k=10))
        Product.objects.filter(name=self.product_name).delete()
    def test_order_create_view(self):
        response = self.client.post(
            reverse('shopapp:product_create'),
            {
                "name": self.product_name,
                "price": "123.45",
                "description": "good table",
                "discount": "10"
            }
        )
        self.assertRedirects(response, reverse('shopapp:products_list'))
        self.assertTrue(Product.objects.filter(name=self.product_name).exists())


class ProductDetailsViewTestCase(TestCase):
    @classmethod
    def setUp(cls) -> None:
        cls.product = Product.objects.create(name='some product')

    @classmethod
    def tearDown(cls) -> None:
        cls.product.delete()

    def test_get_product(self):
        response = self.client.get(
            reverse('shopapp:product_details', kwargs={"pk": self.product.pk})
        )
        self.assertEqual(response.status_code, 200)

    def test_get_product_and_check_content(self):
        response = self.client.get(
            reverse('shopapp:product_details', kwargs={"pk": self.product.pk})
        )
        self.assertContains(response, self.product.name)


class ProductListViewTestCase(TestCase):
    fixtures = [
        'product-fixtures.json',
    ]

    def test_products(self):
        response = self.client.get(reverse('shopapp:products_list'))
        self.assertQuerysetEqual(
            qs=Product.objects.filter(archived=False).all(),
            values=(p.pk for p in response.context['products']),
            transform=lambda p: p.pk,
        )


class OrderDetailViewTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.user = User.objects.create_user(username='test_user', password='qwert')
        permission = Permission.objects.get(codename='view_order')
        cls.user.user_permissions.add(permission)

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()

    def setUp(self) -> None:
        self.client.force_login(self.user)
        self.order = Order.objects.create(
            delivery_address='Some address',
            promocode='SalePromo',
            user=self.user,
        )

    def tearDown(self) -> None:
        self.order.delete()

    def test_order_details(self):
        response = self.client.get(reverse('shopapp:order_details', kwargs={'pk': self.order.pk}))
        received_data = response.context["order"].pk
        expected_data = self.order.pk
        print('order.pk = ', expected_data)
        print('received_data = ', received_data)
        self.assertEqual(received_data, expected_data)


class OrdersExportTestCase(TestCase):
    fixtures = [
        'group-fixtures.json',
        'order-fixtures.json',
        'product-fixtures.json',
        'user-fixtures.json',
    ]

    @classmethod
    def setUpClass(cls):
        cls.user = User.objects.create_user(username='test_user', password='qwert', is_staff=True)

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()

    def setUp(self) -> None:
        self.client.force_login(self.user)

    def test_get_order_view(self):
        response = self.client.get(reverse('shopapp:orders-export'))
        self.assertEqual(response.status_code, 200)
        orders = Order.objects.order_by('pk').all()
        expected_data = [
            {
                'ID': order.id,
                'address': order.delivery_address,
                'promo': order.promocode,
                'user': order.user_id,
                'products': order.products
            }
            for order in orders
        ]
        orders_data = response.json()
        self.assertEqual(expected_data, orders_data['orders'])
