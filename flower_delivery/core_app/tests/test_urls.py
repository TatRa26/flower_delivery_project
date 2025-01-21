from django.test import TestCase
from django.urls import reverse, resolve
from core_app import views

class TestUrls(TestCase):
    def test_register_url(self):
        url = reverse('register')
        self.assertEqual(resolve(url).func, views.register_view)

    def test_login_url(self):
        url = reverse('login')
        self.assertEqual(resolve(url).func, views.user_login)

    def test_logout_url(self):
        url = reverse('logout')
        self.assertEqual(resolve(url).func, views.user_logout)

    def test_home_url(self):
        url = reverse('home')
        self.assertEqual(resolve(url).func, views.home)

    def test_catalog_url(self):
        url = reverse('catalog')
        self.assertEqual(resolve(url).func, views.catalog_view)

    def test_product_detail_url(self):
        url = reverse('product_detail', args=[1])
        self.assertEqual(resolve(url).func, views.product_detail_view)

    def test_cart_view_url(self):
        url = reverse('cart_view')
        self.assertEqual(resolve(url).func, views.cart_view)

    def test_add_to_cart_url(self):
        url = reverse('add_to_cart', args=[1])
        self.assertEqual(resolve(url).func, views.add_to_cart)

    def test_update_cart_item_url(self):
        url = reverse('update_cart_item', args=[1])
        self.assertEqual(resolve(url).func, views.update_cart_item)

    def test_remove_from_cart_url(self):
        url = reverse('remove_from_cart', args=[1])
        self.assertEqual(resolve(url).func, views.remove_from_cart)

    def test_clear_cart_url(self):
        url = reverse('clear_cart')
        self.assertEqual(resolve(url).func, views.clear_cart)

    def test_checkout_url(self):
        url = reverse('checkout')
        self.assertEqual(resolve(url).func, views.checkout)

    def test_order_history_url(self):
        url = reverse('order_history')
        self.assertEqual(resolve(url).func, views.order_history)

    def test_repeat_order_url(self):
        url = reverse('repeat_order', args=[1])
        self.assertEqual(resolve(url).func, views.repeat_order)
