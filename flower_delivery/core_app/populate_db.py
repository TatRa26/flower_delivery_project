# Импортируем модель Product
from core_app.models import Product

# Список данных для добавления
products = [
    {"name": "Розы классика", "description": "Букет из белых роз . Идеально подходит для свидания .", "price": 2500.00, "image": "product_images/bouquet1.jpg"},
    {"name": "Весеннее настроение", "description": "Нежный микс из розовых  и белых  пионов .", "price": 3200.00, "image": "product_images/bouquet2.jpg"},
    {"name": "Летний день", "description": "Ароматный  букет из  лилий,  роз  и васильков .", "price": 2800.00, "image": "product_images/bouquet3.jpg"},
    {"name": "Нежность", "description": "Нежнейшие розовые   лилии . ", "price": 3500.00, "image": "product_images/bouquet4.jpg"},
    {"name": "Романтика", "description": "Классический букет из     белых и  розовых роз .", "price": 4500.00, "image": "product_images/bouquet5.jpg"},
    {"name": "Солнечный привет", "description": "Белые и розовые тюльпаны .", "price": 3100.00, "image": "product_images/bouquet6.jpg"},
    {"name": "Для мамы", "description": "Белые розы и нежная сирень .", "price": 2900.00, "image": "product_images/bouquet7.jpg"},
    {"name": "Праздник", "description": "Микс из нежных белых и розовых роз .", "price": 3800.00, "image": "product_images/bouquet8.jpg"},
    {"name": "Осенний букет", "description": "Тюльпаны в ярких осенних оттенках .", "price": 3400.00, "image": "product_images/bouquet9.jpg"},
    {"name": "Королевский выбор", "description": "Элегантный букет из лилий и роз .", "price": 5500.00, "image": "product_images/bouquet10.jpg"},
    {"name": "Радость жизни", "description": "Пестрый микс из весенних цветов .", "price": 3000.00, "image": "product_images/bouquet11.jpg"},
]

# Добавляем данные в базу
for product_data in products:
    Product.objects.create(
        name=product_data["name"],
        description=product_data["description"],
        price=product_data["price"],
        image=product_data["image"],
    )

# Сообщаем об успешном добавлении
print("Данные успешно добавлены!")
