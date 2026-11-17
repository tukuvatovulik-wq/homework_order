# Homework: корзина и оформление заказов

## Возможности
- Каталог товаров и корзина на сессиях.
- «Убрать 1» уменьшает количество на единицу; если оно равно 1, товар удаляется.
- Модель Order содержит имя, телефон, адрес и дату создания.
- Связь заказа с товарами реализована через промежуточную модель OrderItem с полем quantity.
- После успешного оформления корзина очищается.
- Заказы доступны в админке, новые отображаются первыми.

## Запуск в Windows
```cmd
py -m venv .venv
.venv\Scripts\activate
py -m pip install -r requirements.txt
py manage.py makemigrations
py manage.py migrate
py manage.py loaddata shop/fixtures/products.json
py manage.py createsuperuser
py manage.py runserver
```
Сайт: http://127.0.0.1:8000/ — админка: http://127.0.0.1:8000/admin/

Сначала добавьте товары через админку или загрузите демонстрационные данные командой loaddata.

## Проверка
```cmd
py manage.py test
py manage.py check
```
