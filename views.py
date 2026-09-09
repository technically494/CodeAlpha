from django.shortcuts import render, redirect
from .models import Product, Order
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Product, Order

def home(request):
    products = Product.objects.all()

    return render(request, 'store/home.html', {
        'products': products
    })


def product_detail(request, id):
    product = Product.objects.get(id=id)

    return render(request, 'store/product_detail.html', {
        'product': product
    })



def add_to_cart(request, id):
    cart = request.session.get('cart', {})

    if str(id) in cart:
        cart[str(id)] += 1
    else:
        cart[str(id)] = 1

    request.session['cart'] = cart

    return redirect('cart')


def cart(request):
    cart_data = request.session.get('cart', {})
    products = []
    total = 0

    for product_id, quantity in cart_data.items():
        product = Product.objects.get(id=product_id)

        item_total = product.price * quantity
        total += item_total

        products.append({
            'product': product,
            'quantity': quantity,
            'item_total': item_total
        })

    return render(request, 'store/cart.html', {
        'products': products,
        'total': total
    })

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        User.objects.create_user(
            username=username,
            password=password
        )

        return redirect('login')

    return render(request, 'store/register.html')


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect('home')

    return render(request, 'store/login.html')


def user_logout(request):
    logout(request)
    return redirect('home')


@login_required(login_url='/login/')
def checkout(request):
    cart_data = request.session.get('cart', {})

    if not cart_data:
        return redirect('cart')

    total = 0

    for product_id, quantity in cart_data.items():
        product = Product.objects.get(id=product_id)
        total += product.price * quantity

    order = Order.objects.create(
        user=request.user,
        total_price=total
    )

    request.session['cart'] = {}

    return render(request, 'store/order_success.html', {
        'order': order
    })