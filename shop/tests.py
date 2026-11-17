from django.test import TestCase
from django.urls import reverse
from .models import Category, Order, Product

class CartAndOrderTests(TestCase):
    def setUp(self):
        category = Category.objects.create(name="Тестовая категория")
        self.product = Product.objects.create(name="Тестовый товар", category=category, description="Описание", price="100.00")
    def set_cart(self, quantity):
        session = self.client.session
        session["cart"] = {str(self.product.pk): quantity}
        session.save()
    def test_remove_one_decreases_quantity(self):
        self.set_cart(3)
        response = self.client.post(reverse("shop:remove_one", args=[self.product.pk]))
        self.assertRedirects(response, reverse("shop:cart"))
        self.assertEqual(self.client.session["cart"][str(self.product.pk)], 2)
    def test_remove_one_deletes_last_item(self):
        self.set_cart(1)
        self.client.post(reverse("shop:remove_one", args=[self.product.pk]))
        self.assertNotIn(str(self.product.pk), self.client.session["cart"])
    def test_order_saves_quantity_and_clears_cart(self):
        self.set_cart(2)
        response = self.client.post(reverse("shop:create_order"), {
            "customer_name": "Иван", "address": "Тестовый адрес", "phone": "+996700000000",
        })
        order = Order.objects.get()
        self.assertRedirects(response, reverse("shop:order_success", args=[order.pk]))
        self.assertEqual(order.items.get().quantity, 2)
        self.assertEqual(order.items.get().product, self.product)
        self.assertEqual(self.client.session["cart"], {})
    def test_order_requires_all_fields(self):
        self.set_cart(1)
        response = self.client.post(reverse("shop:create_order"), {"customer_name": "", "address": "", "phone": ""})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(Order.objects.count(), 0)
    def test_empty_cart_does_not_create_order(self):
        response = self.client.post(reverse("shop:create_order"), {
            "customer_name": "Иван", "address": "Адрес", "phone": "123",
        })
        self.assertRedirects(response, reverse("shop:cart"))
        self.assertEqual(Order.objects.count(), 0)
