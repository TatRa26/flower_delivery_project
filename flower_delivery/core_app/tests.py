from django.test import TestCase
from .models import User, Product, Order, OrderItem, Cart, CartItem, Review


class UserModelTest(TestCase):
    def test_user_str(self):
        user = User.objects.create_user(username='testuser', password='password')
        self.assertEqual(str(user), 'testuser')


class ProductModelTest(TestCase):
    def test_product_str(self):
        product = Product.objects.create(
            name='Flower',
            description='A beautiful flower',
            price=10.99,
            image='flower.jpg'
        )
        self.assertEqual(str(product), 'Flower')


class OrderModelTest(TestCase):
    def test_order_str(self):
        user = User.objects.create_user(username='testuser', password='password')
        product = Product.objects.create(
            name='Flower',
            description='A beautiful flower',
            price=10.99,
            image='flower.jpg'
        )
        order = Order.objects.create(
            user=user,
            status='pending',
            delivery_address='123 Main St'
        )
        OrderItem.objects.create(order=order, product=product, quantity=2)
        self.assertEqual(str(order), f"Заказ №{order.id} - testuser")

    def test_order_status(self):
        user = User.objects.create_user(username='testuser', password='password')
        order = Order.objects.create(
            user=user,
            status='confirmed',
            delivery_address='123 Main St'
        )
        self.assertEqual(order.status, 'confirmed')


class OrderItemModelTest(TestCase):
    def test_order_item_str(self):
        user = User.objects.create_user(username='testuser', password='password')
        product = Product.objects.create(
            name='Flower',
            description='A beautiful flower',
            price=10.99,
            image='flower.jpg'
        )
        order = Order.objects.create(
            user=user,
            status='pending',
            delivery_address='123 Main St'
        )
        order_item = OrderItem.objects.create(order=order, product=product, quantity=2)
        self.assertEqual(str(order_item), 'Flower (x2)')


class CartModelTest(TestCase):
    def test_cart_str(self):
        user = User.objects.create_user(username='testuser', password='password')
        cart = Cart.objects.create(user=user)
        self.assertEqual(str(cart), 'Корзина testuser')


class CartItemModelTest(TestCase):
    def test_cart_item_str(self):
        user = User.objects.create_user(username='testuser', password='password')
        product = Product.objects.create(
            name='Flower',
            description='A beautiful flower',
            price=10.99,
            image='flower.jpg'
        )
        cart = Cart.objects.create(user=user)
        cart_item = CartItem.objects.create(cart=cart, product=product, quantity=2)
        self.assertEqual(str(cart_item), 'Flower x 2')


class ReviewModelTest(TestCase):
    def test_review_str(self):
        user = User.objects.create_user(username='testuser', password='password')
        product = Product.objects.create(
            name='Flower',
            description='A beautiful flower',
            price=10.99,
            image='flower.jpg'
        )
        review = Review.objects.create(
            user=user,
            product=product,
            review_text='Great product!',
            rating=5
        )
        self.assertEqual(str(review), 'Отзыв от testuser на Flower')

    def test_review_rating(self):
        user = User.objects.create_user(username='testuser', password='password')
        product = Product.objects.create(
            name='Flower',
            description='A beautiful flower',
            price=10.99,
            image='flower.jpg'
        )
        review = Review.objects.create(
            user=user,
            product=product,
            review_text='Great product!',
            rating=5
        )
        self.assertEqual(review.rating, 5)










