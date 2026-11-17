from decimal import Decimal
from .models import Product
SESSION_CART_KEY = "cart"
def get_cart_items(request):
    cart = request.session.get(SESSION_CART_KEY, {})
    ids = [int(product_id) for product_id in cart.keys()]
    products = Product.objects.filter(id__in=ids)
    items, total = [], Decimal("0.00")
    for product in products:
        quantity = int(cart.get(str(product.pk), 0))
        if quantity < 1:
            continue
        subtotal = product.price * quantity
        total += subtotal
        items.append({"product": product, "quantity": quantity, "subtotal": subtotal})
    return items, total
