from django.core.management.base import BaseCommand
from crm_app.models import Product, Category
from django.utils.text import slugify
import random

class Command(BaseCommand):
    help = 'Добавляет 2000+ товаров с реальными ценами'

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
        
        # Производители с реальными странами и заводами
        manufacturers = [
            ('Bosch', 'Германия', 'Bosch Automotive, Германия', 0.9, 1.3),
            ('Mann', 'Германия', 'Mann Filter GmbH, Германия', 0.8, 1.2),
            ('Castrol', 'Великобритания', 'Castrol UK Limited', 0.8, 1.2),
            ('Mobil', 'США', 'ExxonMobil, США', 0.9, 1.4),
            ('Shell', 'Нидерланды', 'Shell Global, Нидерланды', 0.8, 1.3),
            ('NGK', 'Япония', 'NGK Spark Plug Co, Япония', 0.8, 1.2),
            ('Denso', 'Япония', 'Denso Corporation, Япония', 0.9, 1.4),
            ('TRW', 'Германия', 'TRW Automotive, Германия', 0.8, 1.2),
            ('Brembo', 'Италия', 'Brembo S.p.A., Италия', 1.2, 1.8),
            ('KYB', 'Япония', 'KYB Corporation, Япония', 0.8, 1.2),
            ('Sachs', 'Германия', 'ZF Sachs AG, Германия', 0.9, 1.3),
            ('Gates', 'США', 'Gates Corporation, США', 0.8, 1.2),
            ('Continental', 'Германия', 'Continental AG, Германия', 0.9, 1.3),
            ('Varta', 'Германия', 'Varta AG, Германия', 0.9, 1.4),
            ('Hella', 'Германия', 'Hella GmbH & Co, Германия', 0.8, 1.2),
            ('Valeo', 'Франция', 'Valeo SA, Франция', 0.9, 1.3),
            ('Lemforder', 'Германия', 'ZF Lemforder, Германия', 0.9, 1.3),
            ('Febi', 'Германия', 'Febi Bilstein, Германия', 0.7, 1.1),
            ('Meyle', 'Германия', 'Meyle AG, Германия', 0.7, 1.1),
            ('Bilstein', 'Германия', 'ThyssenKrupp Bilstein, Германия', 1.0, 1.5),
            ('Monroe', 'США', 'Monroe, США', 0.7, 1.1),
            ('Moog', 'США', 'Moog Inc, США', 0.8, 1.2),
            ('SKF', 'Швеция', 'SKF Group, Швеция', 0.9, 1.3),
            ('INA', 'Германия', 'INA Schaeffler, Германия', 0.8, 1.2),
            ('Elring', 'Германия', 'ElringKlinger, Германия', 0.8, 1.2),
            ('Victor Reinz', 'Германия', 'Dana Holding, Германия', 0.7, 1.1),
            ('Payen', 'Испания', 'Payen, Испания', 0.6, 1.0),
            ('Ajusa', 'Испания', 'Ajusa, Испания', 0.5, 0.9),
            ('Goetze', 'Германия', 'Goetze, Германия', 0.7, 1.1),
            ('Fram', 'США', 'Fram Group, США', 0.6, 1.0),
            ('Hengst', 'Германия', 'Hengst SE, Германия', 0.8, 1.2),
            ('Mahle', 'Германия', 'Mahle GmbH, Германия', 0.8, 1.2),
            ('Textar', 'Германия', 'Textar, Германия', 0.8, 1.2),
            ('Ferodo', 'Великобритания', 'Ferodo, Великобритания', 0.7, 1.1),
            ('Pagid', 'Германия', 'Pagid, Германия', 0.8, 1.2),
            ('Eibach', 'Германия', 'Eibach AG, Германия', 1.2, 1.8),
            ('H&R', 'Германия', 'H&R Spezialfedern, Германия', 1.1, 1.7),
            ('K&N', 'США', 'K&N Engineering, США', 0.9, 1.5),
            ('Magnaflow', 'США', 'Magnaflow, США', 0.8, 1.4),
        ]
        
        # Марки для совместимости
        brands_list = [
            'toyota', 'hyundai', 'kia', 'volkswagen', 'renault', 'nissan', 'ford',
            'bmw', 'mercedes', 'audi', 'honda', 'mitsubishi', 'mazda', 'subaru',
            'chevrolet', 'opel', 'peugeot', 'citroen', 'skoda', 'seat', 'volvo',
            'lada', 'vaz', 'uaz', 'gaz', 'lada-vesta', 'lada-granta',
            'lada-kalina', 'lada-priora', 'lada-xray', 'lada-largus'
        ]
        
        # Типы товаров с реальными ценовыми диапазонами
        product_types = {
            'rashodniki-dlya-to': [
                ('Моторное масло', 2500, 6000),
                ('Масляный фильтр', 300, 1200),
                ('Воздушный фильтр', 400, 1500),
                ('Салонный фильтр', 300, 1000),
                ('Топливный фильтр', 500, 2000),
                ('Свечи зажигания (4 шт)', 800, 2500),
                ('Ремень ГРМ', 1000, 4000),
                ('Ролик ГРМ', 800, 3000),
                ('Водяной насос', 2000, 7000),
                ('Термостат', 500, 2000),
                ('Антифриз 5л', 800, 2000),
                ('Тормозная жидкость 1л', 300, 800),
                ('Масло трансмиссионное 1л', 400, 1200),
            ],
            'podveska': [
                ('Амортизатор передний', 3000, 12000),
                ('Амортизатор задний', 2500, 10000),
                ('Пружина подвески передняя', 2000, 6000),
                ('Пружина подвески задняя', 1800, 5500),
                ('Сайлентблок рычага', 300, 1200),
                ('Шаровая опора', 800, 2500),
                ('Рычаг подвески передний', 3000, 10000),
                ('Рычаг подвески задний', 2500, 8000),
                ('Стойка стабилизатора', 500, 2000),
                ('Втулка стабилизатора', 200, 800),
                ('Подшипник ступицы', 1500, 5000),
                ('Ступица в сборе', 3000, 9000),
            ],
            'tormoznaya-sistema': [
                ('Колодки тормозные передние', 1500, 4500),
                ('Колодки тормозные задние', 1200, 4000),
                ('Диск тормозной передний', 2000, 8000),
                ('Диск тормозной задний', 1800, 7000),
                ('Тормозной барабан', 2000, 6000),
                ('Суппорт тормозной', 3000, 10000),
                ('Главный тормозной цилиндр', 2000, 6000),
                ('Вакуумный усилитель', 3000, 8000),
                ('Тормозной шланг', 500, 1500),
                ('Ручной тормоз (комплект)', 1500, 4000),
            ],
            'dvigatel': [
                ('Ремень ГРМ', 1500, 4000),
                ('Ролик ГРМ', 1000, 3000),
                ('Водяной насос', 2500, 7000),
                ('Термостат', 800, 2000),
                ('Прокладка ГБЦ', 800, 2500),
                ('Сальник коленвала', 300, 800),
                ('Маслосъемные колпачки (комплект)', 800, 2000),
                ('Цепь ГРМ', 2000, 6000),
                ('Натяжитель цепи', 1500, 4000),
                ('Катушка зажигания', 2000, 5000),
                ('Высоковольтные провода (комплект)', 1000, 3000),
                ('Крышка клапанов', 1500, 4000),
            ],
            'elektrooborudovanie': [
                ('Аккумулятор 60Ah', 5000, 10000),
                ('Генератор', 5000, 15000),
                ('Стартер', 4000, 12000),
                ('Датчик кислорода (лямбда)', 2000, 8000),
                ('Датчик ABS', 1000, 3000),
                ('Датчик температуры', 500, 1500),
                ('Датчик положения коленвала', 800, 2000),
                ('Датчик скорости', 500, 1500),
                ('Блок управления двигателем (ЭБУ)', 8000, 25000),
                ('Реле поворотов', 200, 600),
                ('Предохранители (набор)', 300, 800),
                ('Кнопка аварийки', 300, 800),
            ],
            'optika': [
                ('Фара передняя левая', 3000, 12000),
                ('Фара передняя правая', 3000, 12000),
                ('Фонарь задний левый', 2000, 6000),
                ('Фонарь задний правый', 2000, 6000),
                ('Противотуманная фара', 1500, 5000),
                ('Лампа H7 (2 шт)', 300, 800),
                ('Лампа H4 (2 шт)', 350, 900),
                ('Лампа LED H7', 1500, 3500),
                ('Повторитель поворота', 300, 800),
                ('ДХО светодиодная', 800, 2000),
            ],
            'kuzov': [
                ('Бампер передний', 3000, 12000),
                ('Бампер задний', 2800, 10000),
                ('Крыло переднее', 2500, 8000),
                ('Капот', 5000, 15000),
                ('Дверь передняя', 8000, 20000),
                ('Зеркало боковое левое', 1500, 5000),
                ('Зеркало боковое правое', 1500, 5000),
                ('Решетка радиатора', 1000, 3000),
                ('Порог', 1500, 4000),
                ('Спойлер', 2000, 6000),
                ('Накладка на порог', 500, 1500),
            ],
            'kolesa': [
                ('Диск литой R15', 4000, 8000),
                ('Диск литой R16', 5000, 10000),
                ('Диск литой R17', 6000, 12000),
                ('Шина летняя R15', 3000, 8000),
                ('Шина летняя R16', 4000, 10000),
                ('Шина зимняя R15', 3500, 9000),
                ('Колпак колеса', 300, 800),
                ('Болт колесный (4 шт)', 200, 500),
                ('Гайка колесная (4 шт)', 200, 500),
            ],
            'rulevoe-upravlenie': [
                ('Рулевая рейка', 8000, 20000),
                ('Рулевой наконечник', 800, 2000),
                ('Рулевая тяга', 1000, 2500),
                ('Рулевая колонка', 5000, 15000),
                ('Насос ГУР', 4000, 10000),
                ('Жидкость ГУР 1л', 500, 1500),
                ('Шланг ГУР', 800, 2000),
            ],
            'toplivnaya-sistema': [
                ('Топливный насос', 2000, 6000),
                ('Топливный фильтр', 500, 2000),
                ('Форсунка топливная', 2000, 6000),
                ('Регулятор давления топлива', 800, 2000),
                ('Топливный бак', 5000, 15000),
                ('Топливная магистраль', 500, 1500),
            ],
            'vyhlopnaya-sistema': [
                ('Глушитель', 3000, 10000),
                ('Резонатор', 2000, 6000),
                ('Вставка катализатора', 1500, 4000),
                ('Насадка на глушитель', 500, 2000),
                ('Хомут выхлопной системы', 200, 600),
                ('Прокладка выхлопной', 200, 500),
            ],
            'salon': [
                ('Коврик в салон (комплект)', 1000, 3000),
                ('Чехол на сиденье', 1500, 5000),
                ('Подлокотник', 1000, 3000),
                ('Руль', 3000, 10000),
                ('Ручка КПП', 500, 2000),
                ('Кнопка стеклоподъемника', 300, 800),
            ],
            'avtoaksessuary': [
                ('Набор автомобилиста', 500, 1500),
                ('Буксировочный трос', 300, 800),
                ('Щетки стеклоочистителя', 500, 1500),
                ('Ароматизатор', 150, 500),
                ('Зарядное устройство USB', 300, 800),
                ('Держатель телефона', 200, 600),
                ('Чехол на руль', 300, 800),
                ('Защитная сетка радиатора', 800, 2000),
            ],
        }
        
        added = 0
        target = 2000
        
        self.stdout.write('🚀 Начинаем добавление товаров...\n')
        
        for category_slug, type_list in product_types.items():
            category = categories.get(category_slug)
            if not category:
                continue
            
            for product_type, min_price, max_price in type_list:
                if added >= target:
                    break
                
                # Для каждого типа создаём 3-10 вариаций
                num_variations = random.randint(5, 12)
                for i in range(num_variations):
                    if added >= target:
                        break
                    
                    # Выбираем случайного производителя
                    manufacturer, country, factory, price_min_mult, price_max_mult = random.choice(manufacturers)
                    
                    # Выбираем случайные марки для совместимости (3-8 марок)
                    num_brands = random.randint(3, 8)
                    compatible_brands = ','.join(random.sample(brands_list, num_brands))
                    
                    # Формируем цену
                    base_price = random.randint(min_price, max_price)
                    price = int(base_price * random.uniform(price_min_mult, price_max_mult))
                    price = round(price / 100) * 100  # Красивая цена
                    
                    # Формируем название
                    if i == 0:
                        quality = "Premium"
                    elif i == 1:
                        quality = "Standard"
                    else:
                        qualities = ["Econom", "Sport", "Tuning", "OEM", "Pro"]
                        quality = random.choice(qualities)
                    
                    # Корректируем цену в зависимости от качества
                    if quality == "Premium":
                        price = int(price * 1.3)
                    elif quality == "Sport" or quality == "Tuning":
                        price = int(price * 1.2)
                    elif quality == "Econom":
                        price = int(price * 0.7)
                    
                    price = round(price / 100) * 100
                    
                    article = f"{product_type[:3].upper()}{manufacturer[:3].upper()}{random.randint(1, 999)}"
                    name = f"{product_type} {manufacturer} {quality}"
                    
                    description = f"{product_type} высокого качества от производителя {manufacturer}. "
                    description += f"Оригинальная продукция, произведена в {country} на заводе {factory}. "
                    description += f"Совместима с автомобилями: {compatible_brands.replace(',', ', ')}. "
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
                        self.stdout.write(f"✅ [{added}] {name[:60]} — {price} ₽")
        
        self.stdout.write(self.style.SUCCESS(f'\n🎉 ГОТОВО! Добавлено {added} товаров.'))
        self.stdout.write(self.style.SUCCESS(f'📊 Всего товаров в базе: {Product.objects.count()}'))