from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from core_app.models import Product, Cart, CartItem
from django.core.files.uploadedfile import SimpleUploadedFile

class ViewsTestCase(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testuser', password='password')

    def test_home_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base.html')

    def test_register_view(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core_app/register.html')
        data = {
            'username': 'newuser',
            'password1': 'ComplexPassword123',
            'password2': 'ComplexPassword123',
            'email': 'newuser@example.com',
            'phone': '1234567890',
            'address': '123 Main St',
        }
        response = self.client.post(reverse('register'), data)
        if response.status_code != 302:
            form = response.context['form']
            print("Form errors:", form.errors)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))

    def test_user_login(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core_app/login.html')
        data = {
            'username': 'testuser',
            'password': 'password',
        }
        response = self.client.post(reverse('login'), data)
        self.assertRedirects(response, reverse('home'))

    def test_user_logout(self):
        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('logout'))
        self.assertRedirects(response, reverse('login'))

    def test_catalog_view(self):
        response = self.client.get(reverse('catalog'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core_app/catalog.html')

    def test_product_detail_view(self):
        image_file = SimpleUploadedFile(name='test_image.jpg', content=b'', content_type='image/jpeg')
        product = Product.objects.create(name='Flower', description='Beautiful flower', price=10.99, image=image_file)
        response = self.client.get(reverse('product_detail', args=[product.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core_app/product_detail.html')
        self.client.login(username='testuser', password='password')
        review_data = {
            'review_text': 'Great product!',
            'rating': 5
        }
        response = self.client.post(reverse('product_detail', args=[product.id]), review_data)
        self.assertRedirects(response, reverse('product_detail', args=[product.id]))

    def test_cart_view(self):
        self.client.login(username='testuser', password='password')
        cart = Cart.objects.create(user=self.user)
        product = Product.objects.create(name='Flower', description='Beautiful flower', price=10.99)
        CartItem.objects.create(cart=cart, product=product, quantity=2)
        response = self.client.get(reverse('cart_view'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core_app/cart.html')

    def test_add_to_cart(self):
        self.client.login(username='testuser', password='password')
        product = Product.objects.create(name='Flower', description='Beautiful flower', price=10.99)
        response = self.client.get(reverse('add_to_cart', args=[product.id]))
        self.assertRedirects(response, reverse('cart_view'))
        cart = Cart.objects.get(user=self.user)
        cart_item = CartItem.objects.get(cart=cart, product=product)
        self.assertEqual(cart_item.quantity, 1)

    def test_remove_from_cart(self):
        self.client.login(username='testuser', password='password')
        cart = Cart.objects.create(user=self.user)
        product = Product.objects.create(name='Flower', description='Beautiful flower', price=10.99)
        cart_item = CartItem.objects.create(cart=cart, product=product, quantity=2)
        response = self.client.get(reverse('remove_from_cart', args=[cart_item.id]))
        self.assertRedirects(response, reverse('cart_view'))
        with self.assertRaises(CartItem.DoesNotExist):
            CartItem.objects.get(id=cart_item.id)

    def test_checkout_view(self):
        self.client.login(username='testuser', password='password')
        cart = Cart.objects.create(user=self.user)
        product = Product.objects.create(name='Flower', description='Beautiful flower', price=10.99)
        CartItem.objects.create(cart=cart, product=product, quantity=2)
        response = self.client.get(reverse('checkout'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core_app/checkout.html')
        order_data = {
            'address': '123 Main St',
        }
        response = self.client.post(reverse('checkout'), order_data)
        self.assertRedirects(response, reverse('order_history'))
