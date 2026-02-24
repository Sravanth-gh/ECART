from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Cart, Order, OrderItem, Category
from django.contrib import messages


def get_session_id(request):
    if not request.session.session_key:
        request.session.create()
    return request.session.session_key


def home(request):
    category_id = request.GET.get('category')
    categories = Category.objects.all()

    if category_id:
        products = Product.objects.filter(category_id=category_id)
    else:
        products = Product.objects.all()

    return render(request, 'home.html', {
        'products': products,
        'categories': categories
    })


def add_to_cart(request, product_id):
    session_id = get_session_id(request)
    product = get_object_or_404(Product, id=product_id)

    cart_item, created = Cart.objects.get_or_create(
        session_id=session_id,
        product=product
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    messages.success(request, "Added to cart!")
    return redirect('home')


def cart_view(request):
    session_id = get_session_id(request)
    cart_items = Cart.objects.filter(session_id=session_id)
    total = sum(item.total_price() for item in cart_items)

    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total': total
    })


def increase_quantity(request, cart_id):
    cart_item = get_object_or_404(Cart, id=cart_id)
    cart_item.quantity += 1
    cart_item.save()
    return redirect('cart')


def decrease_quantity(request, cart_id):
    cart_item = get_object_or_404(Cart, id=cart_id)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    return redirect('cart')


def remove_from_cart(request, cart_id):
    cart_item = get_object_or_404(Cart, id=cart_id)
    cart_item.delete()
    return redirect('cart')


def checkout(request):
    session_id = get_session_id(request)
    cart_items = Cart.objects.filter(session_id=session_id)

    if request.method == "POST":
        name = request.POST.get('name')
        address = request.POST.get('address')
        phone = request.POST.get('phone')

        order = Order.objects.create(
            name=name,
            address=address,
            phone=phone
        )

        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )

        cart_items.delete()
        messages.success(request, "Order placed successfully!")
        return redirect('home')

    total = sum(item.total_price() for item in cart_items)

    return render(request, 'checkout.html', {'total': total})
