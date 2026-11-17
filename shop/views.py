from django.contrib import messages
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from .cart import SESSION_CART_KEY, get_cart_items
from .forms import OrderForm
from .models import Order, OrderItem, Product

def product_list(request):
    products = Product.objects.select_related("category").all()
    return render(request, "shop/product_list.html", {"products": products})

@require_POST
def add_to_cart(request, product_id):
    get_object_or_404(Product, pk=product_id)
    cart = request.session.get(SESSION_CART_KEY, {})
    key = str(product_id)
    cart[key] = int(cart.get(key, 0)) + 1
    request.session[SESSION_CART_KEY] = cart
    messages.success(request, "Товар добавлен в корзину.")
    return redirect("shop:cart")

@require_POST
def remove_one_from_cart(request, product_id):
    cart = request.session.get(SESSION_CART_KEY, {})
    key = str(product_id)
    if key in cart:
        quantity = int(cart[key])
        if quantity > 1:
            cart[key] = quantity - 1
        else:
            del cart[key]
        request.session[SESSION_CART_KEY] = cart
    return redirect("shop:cart")

def cart_view(request):
    items, total = get_cart_items(request)
    return render(request, "shop/cart.html", {"items": items, "total": total, "form": OrderForm()})

@require_POST
def create_order(request):
    items, total = get_cart_items(request)
    if not items:
        messages.error(request, "Корзина пуста. Добавьте товары перед оформлением заказа.")
        return redirect("shop:cart")
    form = OrderForm(request.POST)
    if not form.is_valid():
        return render(request, "shop/cart.html", {"items": items, "total": total, "form": form}, status=400)
    with transaction.atomic():
        order = form.save()
        OrderItem.objects.bulk_create([
            OrderItem(order=order, product=item["product"], quantity=item["quantity"])
            for item in items
        ])
    request.session[SESSION_CART_KEY] = {}
    messages.success(request, f"Заказ №{order.pk} успешно оформлен.")
    return redirect("shop:order_success", order_id=order.pk)

def order_success(request, order_id):
    order = get_object_or_404(Order.objects.prefetch_related("items__product"), pk=order_id)
    return render(request, "shop/order_success.html", {"order": order})
