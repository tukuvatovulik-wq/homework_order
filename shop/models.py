from django.db import models

class Category(models.Model):
    name = models.CharField("Название", max_length=100, unique=True)
    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ["name"]
    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField("Название", max_length=200)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="products", verbose_name="Категория")
    description = models.TextField("Описание", blank=True)
    price = models.DecimalField("Цена", max_digits=9, decimal_places=2)
    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
        ordering = ["name"]
    def __str__(self):
        return self.name

class Order(models.Model):
    customer_name = models.CharField("Имя пользователя", max_length=150)
    phone = models.CharField("Телефон", max_length=30)
    address = models.CharField("Адрес", max_length=255)
    created_at = models.DateTimeField("Дата и время создания", auto_now_add=True)
    products = models.ManyToManyField(Product, through="OrderItem", related_name="orders", verbose_name="Товары")
    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
        ordering = ["-created_at"]
    def __str__(self):
        return f"Заказ №{self.pk} — {self.customer_name}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items", verbose_name="Заказ")
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name="order_items", verbose_name="Товар")
    quantity = models.PositiveIntegerField("Количество")
    class Meta:
        verbose_name = "Товар в заказе"
        verbose_name_plural = "Товары в заказе"
        constraints = [models.UniqueConstraint(fields=["order", "product"], name="unique_product_in_order")]
    def __str__(self):
        return f"{self.product} × {self.quantity}"
