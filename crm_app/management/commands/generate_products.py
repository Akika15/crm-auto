from django.core.management.base import BaseCommand
from crm_app.models import Product

class Command(BaseCommand):
    help = 'Создаёт 1000 тестовых запчастей'

    def handle(self, *args, **options):
        categories = [
            'Моторные масла', 'Трансмиссионные масла', 'Масляные фильтры', 'Воздушные фильтры',
            'Тормозные колодки', 'Тормозные диски', 'Амортизаторы', 'Пружины подвески',
            'Свечи зажигания', 'Ремни ГРМ', 'Ролики натяжные', 'Водяные насосы',
            'Аккумуляторы', 'Лампы', 'Стеклоочистители', 'Термостаты',
            'Датчики', 'Втулки стабилизатора', 'Шаровые опоры', 'Сайлентблоки'
        ]

        manufacturers = [
            'Bosch', 'Mann', 'Castrol', 'Mobil', 'Shell', 'NGK', 'TRW', 'ATE', 'Brembo',
            'Lemforder', 'Febi', 'Meyle', 'Sachs', 'Bilstein', 'KYB', 'Gates', 'Contitech',
            'Valeo', 'Hella', 'Denso', 'Liqui Moly', 'Motul', 'ZIC', 'Total', 'Elring',
            'SKF', 'INA', 'Mahle', 'Hengst', 'Fram', 'Textar', 'Ferodo', 'Pagid',
            'Monroe', 'Moog', 'Ruville', 'Nissens', 'Behr', 'Van Wezel'
        ]

        if Product.objects.count() >= 500:
            self.stdout.write(self.style.WARNING('Товары уже есть. Скрипт не запущен.'))
            return

        count = 0
        target = 1000

        for category in categories:
            for manufacturer in manufacturers[:5]:
                if count >= target:
                    break
                for level in range(4):
                    if count >= target:
                        break
                    
                    quality = ['Premium', 'Standard', 'Econom', 'Budget'][level]
                    article = f"{category[:2].upper()}{manufacturer[:3].upper()}{level}"
                    name = f"{category} {manufacturer} {quality}"
                    price = round(300 + level * 200 + len(manufacturer) * 5, 2)
                    
                    obj, created = Product.objects.get_or_create(
                        article=article,
                        defaults={
                            'name': name,
                            'category': category,
                            'manufacturer': manufacturer,
                            'retail_price': price,
                            'stock_quantity': 20 + level * 10
                        }
                    )
                    if created:
                        count += 1
                        self.stdout.write(f"✅ {count}. {name} — {price} руб.")
            
            if count >= target:
                break

        self.stdout.write(self.style.SUCCESS(f'\n🎉 ГОТОВО! Создано {count} товаров.'))