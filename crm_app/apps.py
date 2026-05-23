from django.apps import AppConfig
from django.db.models.signals import post_migrate

def create_categories_and_products(sender, **kwargs):
    from crm_app.models import Category, Product
    from django.utils.text import slugify
    
    # Создаём категории
    categories_data = {
        'rashodniki-dlya-to': 'Расходники для ТО',
        'podveska': 'Подвеска',
        'tormoznaya-sistema': 'Тормозная система',
        'dvigatel': 'Двигатель',
        'elektrooborudovanie': 'Электрооборудование',
        'kuzov': 'Кузов',
        'optika': 'Оптика',
        'kolesa': 'Колеса',
        'rulevoe-upravlenie': 'Рулевое управление',
        'toplivnaya-sistema': 'Топливная система',
        'vyhlopnaya-sistema': 'Выхлопная система',
        'vpusknaya-sistema': 'Впускная система',
        'salon': 'Салон',
        'avtoaksessuary': 'Автоаксессуары',
    }
    
    categories = {}
    for slug, name in categories_data.items():
        cat, created = Category.objects.get_or_create(slug=slug, defaults={'name': name})
        categories[slug] = cat
        if created:
            print(f'📁 Создана категория: {name}')
    
    # Проверяем, есть ли товары
    if Product.objects.count() == 0:
        print('🚀 Создаём товары...')
        
        # Производители
        manufacturers = [
            ('Bosch', 'Германия', 'Bosch Automotive'),
            ('Mann', 'Германия', 'Mann Filter GmbH'),
            ('Castrol', 'Великобритания', 'Castrol UK'),
            ('NGK', 'Япония', 'NGK Spark Plug'),
            ('TRW', 'Германия', 'TRW Automotive'),
            ('KYB', 'Япония', 'KYB Corporation'),
            ('Gates', 'США', 'Gates Corporation'),
            ('Varta', 'Германия', 'Varta AG'),
            ('Valeo', 'Франция', 'Valeo SA'),
            ('Febi', 'Германия', 'Febi Bilstein'),
        ]
        
        # Товары для каждой категории
        product_templates = {
            'rashodniki-dlya-to': [
                ('Моторное масло 5W-30', 2500, 4000),
                ('Масляный фильтр', 400, 800),
                ('Воздушный фильтр', 500, 1000),
                ('Салонный фильтр', 400, 800),
                ('Топливный фильтр', 600, 1200),
                ('Свечи зажигания (4 шт)', 800, 1500),
                ('Ремень ГРМ', 1500, 3000),
                ('Антифриз 5л', 800, 1500),
            ],
            'tormoznaya-sistema': [
                ('Колодки тормозные передние', 2000, 3500),
                ('Колодки тормозные задние', 1800, 3000),
                ('Диск тормозной передний', 2500, 5000),
                ('Диск тормозной задний', 2200, 4500),
                ('Тормозная жидкость 1л', 400, 800),
            ],
            'podveska': [
                ('Амортизатор передний', 3500, 6000),
                ('Амортизатор задний', 3000, 5500),
                ('Пружина подвески', 2000, 4000),
                ('Сайлентблок', 400, 1000),
                ('Шаровая опора', 800, 1500),
            ],
            'dvigatel': [
                ('Ремень ГРМ', 1500, 3000),
                ('Ролик ГРМ', 1000, 2000),
                ('Водяной насос', 2500, 5000),
                ('Термостат', 600, 1200),
                ('Катушка зажигания', 2000, 4000),
            ],
            'elektrooborudovanie': [
                ('Аккумулятор 60Ah', 5000, 8000),
                ('Генератор', 6000, 10000),
                ('Стартер', 5000, 9000),
                ('Датчик кислорода', 2500, 4500),
                ('Датчик ABS', 1200, 2500),
            ],
            'optika': [
                ('Фара передняя левая', 3500, 7000),
                ('Фара передняя правая', 3500, 7000),
                ('Фонарь задний', 2000, 4500),
                ('Лампа H7', 300, 600),
                ('Противотуманная фара', 1500, 3500),
            ],
            'kuzov': [
                ('Бампер передний', 4000, 8000),
                ('Крыло', 2500, 5000),
                ('Зеркало боковое', 1500, 3000),
                ('Решетка радиатора', 1200, 2500),
            ],
            'avtoaksessuary': [
                ('Щетки стеклоочистителя', 500, 1000),
                ('Чехол на сиденье', 800, 2000),
                ('Коврик в салон', 600, 1500),
                ('Буксировочный трос', 400, 800),
                ('Ароматизатор', 200, 500),
            ],
        }
        
        added = 0
        for cat_slug, products in product_templates.items():
            category = categories.get(cat_slug)
            if not category:
                continue
            
            for prod_name, min_price, max_price in products:
                for manufacturer, country, factory in manufacturers[:3]:
                    import random
                    price = random.randint(min_price, max_price)
                    article = f"{prod_name[:2].upper()}{manufacturer[:2].upper()}{random.randint(100,999)}"
                    
                    Product.objects.get_or_create(
                        article=article,
                        defaults={
                            'name': f"{prod_name} {manufacturer}",
                            'category': category,
                            'price': price,
                            'manufacturer': manufacturer,
                            'country_of_origin': country,
                            'factory': factory,
                            'is_available': True,
                            'stock_quantity': random.randint(10, 100),
                            'description': f"{prod_name} от {manufacturer}. Произведено в {country}. Гарантия качества.",
                        }
                    )
                    added += 1
                    print(f'  ✅ {added}. {prod_name} {manufacturer} — {price} ₽')
        
        print(f'🎉 Готово! Создано {added} товаров.')

class CrmAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'crm_app'
    
    def ready(self):
        post_migrate.connect(create_categories_and_products, sender=self)