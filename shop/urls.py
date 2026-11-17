from django.urls import path
from . import views
app_name = "shop"
urlpatterns = [
    path("", views.product_list, name="product_list"),
    path("cart/", views.cart_view, name="cart"),
    path("cart/add/<int:product_id>/", views.add_to_cart, name="add_to_cart"),
    path("cart/remove/<int:product_id>/", views.remove_one_from_cart, name="remove_one"),
    path("orders/create/", views.create_order, name="create_order"),
    path("orders/<int:order_id>/success/", views.order_success, name="order_success"),
]
