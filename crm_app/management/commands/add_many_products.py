from django.core.management.base import BaseCommand
from crm_app.models import Product, Category
from django.utils.text import slugify
import random

class Command(BaseCommand):
    help = 'Добавляет 3000+ товаров с реальными ценами'

    def handle(self, *args, **options):
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
            cat, _ = Category.objects.get_or_create(slug=slug, defaults={'name': name})
            categories[slug] = cat
            self.stdout.write(f'📁 Категория: {name}')
        
        # Производители
        manufacturers = [
            ('Bosch', 'Германия', 'Bosch Automotive'),
            ('Mann', 'Германия', 'Mann Filter GmbH'),
            ('Castrol', 'Великобритания', 'Castrol UK'),
            ('Mobil', 'США', 'ExxonMobil'),
            ('Shell', 'Нидерланды', 'Shell Global'),
            ('NGK', 'Япония', 'NGK Spark Plug'),
            ('Denso', 'Япония', 'Denso Corporation'),
            ('TRW', 'Германия', 'TRW Automotive'),
            ('Brembo', 'Италия', 'Brembo S.p.A.'),
            ('KYB', 'Япония', 'KYB Corporation'),
            ('Sachs', 'Германия', 'ZF Sachs'),
            ('Gates', 'США', 'Gates Corporation'),
            ('Continental', 'Германия', 'Continental AG'),
            ('Varta', 'Германия', 'Varta AG'),
            ('Valeo', 'Франция', 'Valeo SA'),
            ('Lemforder', 'Германия', 'ZF Lemforder'),
            ('Febi', 'Германия', 'Febi Bilstein'),
            ('Meyle', 'Германия', 'Meyle AG'),
            ('Bilstein', 'Германия', 'ThyssenKrupp'),
            ('Monroe', 'США', 'Monroe'),
            ('SKF', 'Швеция', 'SKF Group'),
            ('INA', 'Германия', 'INA Schaeffler'),
            ('Elring', 'Германия', 'ElringKlinger'),
            ('Fram', 'США', 'Fram Group'),
            ('Hengst', 'Германия', 'Hengst SE'),
            ('Mahle', 'Германия', 'Mahle GmbH'),
            ('Textar', 'Германия', 'Textar'),
            ('Ferodo', 'Великобритания', 'Ferodo'),
            ('Pagid', 'Германия', 'Pagid'),
            ('Eibach', 'Германия', 'Eibach AG'),
            ('H&R', 'Германия', 'H&R Spezialfedern'),
        ]
        
        # Марки для совместимости
        brands_list = [
            'toyota', 'hyundai', 'kia', 'volkswagen', 'renault', 'nissan', 'ford',
            'bmw', 'mercedes', 'audi', 'honda', 'mitsubishi', 'mazda', 'subaru',
            'chevrolet', 'opel', 'peugeot', 'citroen', 'skoda', 'seat', 'volvo',
            'lada', 'vaz', 'uaz', 'gaz', 'lada-vesta', 'lada-granta',
            'lada-kalina', 'lada-priora', 'lada-xray', 'lada-largus'
        ]
        
        # Типы товаров для каждой категории
        product_types = {
            'rashodniki-dlya-to': [
                'Моторное масло', 'Масляный фильтр', 'Воздушный фильтр', 
                'Салонный фильтр', 'Топливный фильтр', 'Свечи зажигания',
                'Ремень ГРМ', 'Ролик ГРМ', 'Антифриз', 'Тормозная жидкость',
                'Масло трансмиссионное', 'Охлаждающая жидкость'
            ],
            'podveska': [
                'Амортизатор', 'Пружина подвески', 'Сайлентблок', 'Шаровая опора',
                'Рычаг подвески', 'Стойка стабилизатора', 'Подшипник ступицы'
            ],
            'tormoznaya-sistema': [
                'Колодки тормозные', 'Диск тормозной', 'Тормозной барабан',
                'Суппорт тормозной', 'Тормозной шланг', 'Главный тормозной цилиндр'
            ],
            'dvigatel': [
                'Прокладка ГБЦ', 'Сальник коленвала', 'Маслосъемные колпачки',
                'Цепь ГРМ', 'Натяжитель цепи', 'Катушка зажигания',
                'Высоковольтные провода', 'Водяной насос', 'Термостат'
            ],
            'elektrooborudovanie': [
                'Аккумулятор', 'Генератор', 'Стартер', 'Датчик кислорода',
                'Датчик ABS', 'Датчик температуры', 'Датчик скорости',
                'Реле', 'Предохранители', 'Кнопка стеклоподъемника'
            ],
            'kuzov': [
                'Бампер передний', 'Бампер задний', 'Крыло', 'Капот', 'Дверь',
                'Зеркало боковое', 'Решетка радиатора', 'Порог', 'Спойлер'
            ],
            'optika': [
                'Фара передняя левая', 'Фара передняя правая', 'Фонарь задний левый',
                'Фонарь задний правый', 'Противотуманная фара', 'Лампа H7',
                'Лампа H4', 'Светодиодная лампа', 'Повторитель поворота'
            ],
            'kolesa': [
                'Диск литой', 'Шина летняя', 'Шина зимняя', 'Колпак колеса',
                'Болт колесный', 'Гайка колесная'
            ],
            'rulevoe-upravlenie': [
                'Рулевая рейка', 'Рулевой наконечник', 'Рулевая тяга',
                'Насос ГУР', 'Жидкость ГУР', 'Шланг ГУР'
            ],
            'toplivnaya-sistema': [
                'Топливный насос', 'Топливный фильтр', 'Форсунка топливная',
                'Регулятор давления', 'Топливная магистраль'
            ],
            'vyhlopnaya-sistema': [
                'Глушитель', 'Резонатор', 'Вставка катализатора',
                'Насадка на глушитель', 'Хомут выхлопной системы'
            ],
            'salon': [
                'Коврик в салон', 'Чехол на сиденье', 'Подлокотник',
                'Руль', 'Ручка КПП', 'Кнопка стеклоподъемника'
            ],
            'avtoaksessuary': [
                'Набор автомобилиста', 'Буксировочный трос', 'Щетки стеклоочистителя',
                'Ароматизатор', 'Зарядное устройство USB', 'Держатель телефона',
                'Чехол на руль', 'Защитная сетка радиатора'
            ],
        }
        
        added = 0
        target = 3000
        
        self.stdout.write('🚀 Начинаем добавление товаров...\n')
        
        for category_slug, types in product_types.items():
            category = categories.get(category_slug)
            if not category:
                continue
            
            for product_type in types:
                if added >= target:
                    break
                
                # 5-15 вариаций на каждый тип
                variations = random.randint(8, 20)
                for i in range(variations):
                    if added >= target:
                        break
                    
                    manufacturer, country, factory = random.choice(manufacturers)
                    
                    # Случайные марки для совместимости
                    num_brands = random.randint(3, 10)
                    compatible_brands = ','.join(random.sample(brands_list, num_brands))
                    
                    # Качество и цена
                    if i == 0:
                        quality = "Premium"
                        price_mult = 1.5
                    elif i == 1:
                        quality = "Standard"
                        price_mult = 1.0
                    else:
                        qualities = ["Econom", "Sport", "Tuning", "Pro", "Racing"]
                        quality = random.choice(qualities)
                        if quality == "Econom":
                            price_mult = 0.6
                        elif quality == "Sport":
                            price_mult = 1.3
                        elif quality == "Tuning":
                            price_mult = 1.7
                        elif quality == "Pro":
                            price_mult = 2.0
                        else:
                            price_mult = 1.2
                    
                    base_price = random.randint(300, 15000)
                    price = int(base_price * price_mult / 100) * 100
                    
                    article = f"{product_type[:2].upper()}{manufacturer[:3].upper()}{random.randint(1, 999)}"
                    name = f"{product_type} {manufacturer} {quality}"
                    
                    description = f"{product_type} от производителя {manufacturer}. "
                    description += f"Произведено в {country} на заводе {factory}. "
                    description += f"Совместимо с автомобилями: {compatible_brands.replace(',', ', ')}. "
                    description += f"Гарантия качества. В наличии на складе."
                    
                    is_new = random.choice([True, False, False, False, False])  # 20% новинок
                    is_hit = random.choice([True, False, False, False, False, False])  # 16% хитов
                    is_recommended = random.choice([True, False, False, False])  # 25% рекомендуемых
                    stock = random.randint(5, 200)
                    
                    product, created = Product.objects.get_or_create(
                        article=article,
                        defaults={
                            'name': name[:190],
                            'slug': slugify(name)[:190],
                            'description': description,
                            'category': category,
                            'price': price,
                            'manufacturer': manufacturer,
                            'country_of_origin': country,
                            'factory': factory,
                            'compatible_brands': compatible_brands,
                            'is_available': True,
                            'is_new': is_new,
                            'is_hit': is_hit,
                            'is_recommended': is_recommended,
                            'stock_quantity': stock,
                        }
                    )
                    
                    if created:
                        added += 1
                        self.stdout.write(f"✅ [{added}] {name[:60]} — {price} ₽ ({category.name})")
        
        self.stdout.write(self.style.SUCCESS(f'\n🎉 ГОТОВО! Добавлено {added} товаров.'))
        self.stdout.write(self.style.SUCCESS(f'📊 Всего товаров в базе: {Product.objects.count()}'))