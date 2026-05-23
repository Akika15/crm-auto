from django.core.management.base import BaseCommand
from crm_app.models import Category, Product

class Command(BaseCommand):
    help = 'Создаёт категории и товары для интернет-магазина'

    def handle(self, *args, **options):
        self.stdout.write('Создание категорий...')
        
        # Создаём основные категории
        categories_data = {
            'dvigatel': {'name': 'Двигатель', 'order': 1},
            'podveska': {'name': 'Подвеска', 'order': 2},
            'tormoza': {'name': 'Тормозная система', 'order': 3},
            'kpp': {'name': 'Коробка передач', 'order': 4},
            'vyhlop': {'name': 'Выхлопная система', 'order': 5},
            'elektrika': {'name': 'Электрооборудование', 'order': 6},
            'kuzov': {'name': 'Кузов', 'order': 7},
            'masla': {'name': 'Масла и жидкости', 'order': 8},
            'filtry': {'name': 'Фильтры', 'order': 9},
        }
        
        created_categories = {}
        for slug, data in categories_data.items():
            cat, created = Category.objects.get_or_create(
                slug=slug,
                defaults={
                    'name': data['name'],
                    'order': data['order']
                }
            )
            created_categories[slug] = cat
            self.stdout.write(f'  {"✅" if created else "📁"} {cat.name}')
        
        # Создаём подкатегории (для Двигателя)
        subcategories_data = [
            {'name': 'Моторные масла', 'slug': 'motornye-masla', 'parent_slug': 'dvigatel'},
            {'name': 'Фильтры двигателя', 'slug': 'filtry-dvigatelya', 'parent_slug': 'dvigatel'},
            {'name': 'Ремни ГРМ', 'slug': 'remni-grm', 'parent_slug': 'dvigatel'},
            {'name': 'Свечи зажигания', 'slug': 'svechi-zazhiganiya', 'parent_slug': 'dvigatel'},
        ]
        
        for sub in subcategories_data:
            parent = created_categories.get(sub['parent_slug'])
            if parent:
                cat, created = Category.objects.get_or_create(
                    slug=sub['slug'],
                    defaults={
                        'name': sub['name'],
                        'parent': parent
                    }
                )
                self.stdout.write(f'  {"✅" if created else "📁"}   └─ {cat.name}')
        
        self.stdout.write('\nСоздание товаров...')
        
        # Создаём товары
        products_data = [
            {
                'article': 'OIL-5W30-4L',
                'name': 'Моторное масло Castrol 5W-30 4л',
                'slug': 'castrol-5w30-4l',
                'description': 'Полностью синтетическое моторное масло для современных бензиновых и дизельных двигателей. Обеспечивает отличную защиту при любых нагрузках.',
                'price': 3500,
                'is_new': True,
                'stock_quantity': 50,
                'manufacturer': 'Castrol',
                'category_slug': 'motornye-masla'
            },
            {
                'article': 'FILT-001',
                'name': 'Масляный фильтр Mann',
                'slug': 'maslyanyy-filtr-mann',
                'description': 'Высококачественный масляный фильтр для эффективной очистки моторного масла.',
                'price': 500,
                'is_hit': True,
                'stock_quantity': 100,
                'manufacturer': 'Mann',
                'category_slug': 'filtry-dvigatelya'
            },
            {
                'article': 'SPARK-4',
                'name': 'Свечи зажигания NGK (4 шт)',
                'slug': 'svechi-ngk-4',
                'description': 'Иридиевые свечи зажигания для стабильной работы двигателя в любых условиях.',
                'price': 1200,
                'is_recommended': True,
                'stock_quantity': 40,
                'manufacturer': 'NGK',
                'category_slug': 'svechi-zazhiganiya'
            },
            {
                'article': 'TIMING-001',
                'name': 'Ремень ГРМ Gates',
                'slug': 'remen-grm-gates',
                'description': 'Высокопрочный зубчатый ремень для привода газораспределительного механизма.',
                'price': 1800,
                'is_available': True,
                'stock_quantity': 25,
                'manufacturer': 'Gates',
                'category_slug': 'remni-grm'
            },
            {
                'article': 'BRAKE-PAD-01',
                'name': 'Тормозные колодки TRW передние',
                'slug': 'tormoznye-kolodki-trw',
                'description': 'Высокоэффективные тормозные колодки для безопасного торможения.',
                'price': 2500,
                'is_hit': True,
                'stock_quantity': 60,
                'manufacturer': 'TRW',
                'category_slug': 'tormoza'
            },
            {
                'article': 'SHOCK-ABS-01',
                'name': 'Амортизатор Bilstein B6',
                'slug': 'amortizator-bilstein',
                'description': 'Спортивный амортизатор с улучшенными характеристиками.',
                'price': 5500,
                'is_available': True,
                'stock_quantity': 15,
                'manufacturer': 'Bilstein',
                'category_slug': 'podveska'
            },
        ]
        
        created_products = 0
        for prod_data in products_data:
            category_slug = prod_data.pop('category_slug')
            category = Category.objects.filter(slug=category_slug).first()
            
            if category:
                prod, created = Product.objects.get_or_create(
                    article=prod_data['article'],
                    defaults={
                        **prod_data,
                        'category': category,
                        'is_available': prod_data.get('is_available', True)
                    }
                )
                if created:
                    created_products += 1
                    self.stdout.write(f'  ✅ {prod.name} — {prod.price} ₽')
                else:
                    self.stdout.write(f'  📁 {prod.name} (уже существует)')
        
        self.stdout.write(self.style.SUCCESS(f'\n🎉 Готово! Создано {len(categories_data)} категорий и {created_products} товаров.'))