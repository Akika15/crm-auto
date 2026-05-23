import os
import django
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crm_project.settings')
django.setup()

from crm_app.models import Category, Product
from django.utils.text import slugify

print("Добавление товаров в категорию 'Впускная система'...")

category, _ = Category.objects.get_or_create(
    slug='vpusknaya-sistema',
    defaults={'name': 'Впускная система'}
)

manufacturers = [
    ('Bosch', 'Германия', 'Bosch Automotive'),
    ('Mann', 'Германия', 'Mann Filter GmbH'),
    ('Mahle', 'Германия', 'Mahle GmbH'),
    ('K&N', 'США', 'K&N Engineering'),
    ('Gates', 'США', 'Gates Corporation'),
    ('Continental', 'Германия', 'Continental AG'),
    ('Valeo', 'Франция', 'Valeo SA'),
    ('Febi', 'Германия', 'Febi Bilstein'),
    ('Meyle', 'Германия', 'Meyle AG'),
    ('Hengst', 'Германия', 'Hengst SE'),
    ('Fram', 'США', 'Fram Group'),
    ('HKS', 'Япония', 'HKS'),
    ('APEXi', 'Япония', 'APEXi'),
]

product_types = [
    'Воздушный фильтр', 'Воздушный фильтр спортивный', 'Фильтр нулевого сопротивления',
    'Дроссельная заслонка', 'Карбюратор', 'Ресивер впускной', 'Впускной коллектор',
    'Впускной патрубок', 'Прокладка впускного коллектора', 'Крепление впуска',
    'Датчик массового расхода воздуха', 'Датчик температуры воздуха',
    'Интеркулер', 'Турбина', 'Клапан рециркуляции',
    'Гофрированный патрубок', 'Хомут впускной', 'Шланг впускной',
    'Адаптер фильтра', 'Кожух воздушного фильтра', 'Воздуховод',
]

brands_list = [
    'toyota', 'hyundai', 'kia', 'volkswagen', 'renault', 'nissan', 'ford',
    'bmw', 'mercedes', 'audi', 'honda', 'mitsubishi', 'mazda', 'subaru',
    'chevrolet', 'opel', 'peugeot', 'citroen', 'skoda', 'seat', 'volvo',
    'lada', 'vaz', 'uaz', 'gaz'
]

added = 0
target = 200

for product_type in product_types:
    if added >= target:
        break
    
    for i in range(8):
        if added >= target:
            break
        
        manufacturer, country, factory = random.choice(manufacturers)
        
        qualities = ['Premium', 'Standard', 'Sport', 'Econom', 'Racing', 'Tuning', 'Pro']
        quality = random.choice(qualities)
        
        if quality == 'Premium':
            price_mult = 1.5
        elif quality == 'Racing':
            price_mult = 2.0
        elif quality == 'Sport':
            price_mult = 1.4
        elif quality == 'Tuning':
            price_mult = 1.6
        elif quality == 'Pro':
            price_mult = 1.3
        elif quality == 'Econom':
            price_mult = 0.7
        else:
            price_mult = 1.0
        
        if 'фильтр' in product_type.lower():
            base_price = random.randint(500, 8000)
        elif 'дроссель' in product_type.lower():
            base_price = random.randint(3000, 12000)
        elif 'турбин' in product_type.lower():
            base_price = random.randint(8000, 35000)
        elif 'интеркулер' in product_type.lower():
            base_price = random.randint(6000, 25000)
        elif 'датчик' in product_type.lower():
            base_price = random.randint(800, 5000)
        else:
            base_price = random.randint(500, 6000)
        
        price = int(base_price * price_mult / 100) * 100
        
        article = f"IN{manufacturer[:3].upper()}{added+1}"
        name = f"{product_type} {manufacturer} {quality}"
        
        num_brands = random.randint(3, 8)
        compatible_brands = ','.join(random.sample(brands_list, num_brands))
        
        if not Product.objects.filter(article=article).exists():
            product = Product(
                article=article,
                name=name[:190],
                slug=f"{slugify(name)}_{added}",
                description=f"{product_type} от {manufacturer}. Совместимо с: {compatible_brands}",
                category=category,
                price=price,
                manufacturer=manufacturer,
                country_of_origin=country,
                factory=factory,
                compatible_brands=compatible_brands,
                is_available=True,
                stock_quantity=random.randint(5, 100),
            )
            product.save()
            added += 1
            print(f"Added: {name[:50]} - {price} RUB")

print(f"Done! Added {added} products to {category.name}")