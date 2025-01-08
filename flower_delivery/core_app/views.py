from .forms import CustomUserCreationForm, CustomAuthenticationForm
from core_app.models import Order, OrderItem, Product
from core_app.models import Cart, CartItem
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Review
from .forms import ReviewForm

def home(request):
    return render(request, 'base.html')



def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Перенаправляем на страницу входа после успешной регистрации
    else:
        form = CustomUserCreationForm()
    return render(request, 'core_app/register.html', {'form': form})


# Авторизация пользователя
def user_login(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            next_url = request.GET.get('next', 'home')
            return redirect(next_url)
    else:
        form = CustomAuthenticationForm()
    return render(request, 'core_app/login.html', {'form': form})


# Выход пользователя
@login_required
def user_logout(request):
    logout(request)  # Выходим из системы
    return redirect('login')  # Перенаправляем на страницу авторизации

# Просмотр каталога товаров
def catalog_view(request):
    products = Product.objects.all()
    return render(request, 'core_app/catalog.html', {'products': products})

# Детальная страница товара


def product_detail_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    reviews = Review.objects.filter(product=product)  # Получаем отзывы для данного товара

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user  # Связываем отзыв с текущим пользователем
            review.save()
            return redirect('product_detail', product_id=product.id)  # Перезагружаем страницу, чтобы увидеть новый отзыв
    else:
        form = ReviewForm()

    context = {
        'product': product,
        'reviews': reviews,
        'form': form,
    }
    return render(request, 'core_app/product_detail.html', context)

@login_required
def cart_view(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    items = cart.items.all()

    # Добавление общей цены для каждого товара
    for item in items:
        item.total_price = item.product.price * item.quantity

    total_price = sum(item.total_price for item in items)

    return render(request, 'core_app/cart.html', {'cart': cart, 'items': items, 'total_price': total_price})



# Добавление товара в корзину
@login_required
def add_to_cart(request, product_id):
    cart, created = Cart.objects.get_or_create(user=request.user)
    product = get_object_or_404(Product, id=product_id)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('cart_view')

# Обновление количества товара
@login_required
def update_cart_item(request, product_id):
    cart = get_object_or_404(Cart, user=request.user)  # Получаем корзину текущего пользователя
    product = get_object_or_404(Product, id=product_id)  # Проверяем, что продукт существует

    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        if quantity < 1:
            quantity = 1

        # Проверяем, существует ли товар в корзине
        try:
            cart_item = CartItem.objects.get(cart=cart, product=product)
            cart_item.quantity = quantity
            cart_item.save()
        except CartItem.DoesNotExist:
            # Если товар отсутствует, просто ничего не делаем или редиректим
            return redirect('cart_view')

    return redirect('cart_view')



# Удаление товара из корзины
@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    cart_item.delete()
    return redirect('cart_view')

# Очистка корзины
@login_required
def clear_cart(request):
    cart = get_object_or_404(Cart, user=request.user)
    cart.items.all().delete()
    return redirect('cart_view')

@login_required
def checkout(request):
    cart = get_object_or_404(Cart, user=request.user)
    items = cart.items.all()

    # Общая сумма заказа
    total_price = sum(item.product.price * item.quantity for item in items)

    if request.method == 'POST':
        address = request.POST.get('address')
        order = Order.objects.create(
            user=request.user,
            delivery_address=address,
            status='pending'
        )

        for item in items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity
            )

        cart.items.all().delete()  # Очищаем корзину после оформления заказа
        return redirect('order_history')

    return render(request, 'core_app/checkout.html', {'items': items, 'total_price': total_price})


@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-order_date')
    return render(request, 'core_app/order_history.html', {'orders': orders})

@login_required
def repeat_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    cart, created = Cart.objects.get_or_create(user=request.user)

    for item in order.order_items.all():
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=item.product
        )
        if not created:
            cart_item.quantity += item.quantity
        cart_item.save()

    return redirect('cart_view')

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    reviews = product.reviews.all()

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.product = product
            review.save()
            return redirect('product_detail', product_id=product.id)
    else:
        form = ReviewForm()

    return render(request, 'product_detail.html', {
        'product': product,
        'reviews': reviews,
        'form': form,
    })












