from .cart import get_cart_items
def cart_context(request):
    items, total = get_cart_items(request)
    return {"cart_items_count": sum(item["quantity"] for item in items), "cart_total": total}
