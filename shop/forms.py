from django import forms
from .models import Order
class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["customer_name", "address", "phone"]
        widgets = {
            "customer_name": forms.TextInput(attrs={"placeholder": "Ваше имя"}),
            "address": forms.TextInput(attrs={"placeholder": "Адрес доставки"}),
            "phone": forms.TextInput(attrs={"placeholder": "Номер телефона"}),
        }
