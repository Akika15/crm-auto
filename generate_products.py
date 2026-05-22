import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crm_project.settings')
django.setup()

from crm_app.models import Product

categories = {
    'Масла': ['Castrol', 'Mobil', 'Shell', 'Liqui Moly', 'Total', 'ELF', 'Motul', 'ZIC', 'Lukoil', 'Rosneft'],
    'Фильтры': ['Mann', 'Bosch', 'Knecht', 'Mahle', 'Fram', 'Hengst', 'SCT', 'JS Asakashi', 'Nipparts', 'Filtron'],
    'Тормозная система': ['TRW', 'ATE', 'Bosch', 'Brembo', 'Textar', 'Ferodo', 'Pagid', 'Jurid', 'LPR', 'NK'],
    'Подвеска': ['Lemforder', 'Febi', 'Meyle', 'TRW', 'Sachs', 'Bilstein', 'Monroe', 'KYB', 'Moog', 'Ruville'],
    'Двигатель': ['Gates', 'Contitech', 'INA', 'SKF', 'Elring', 'Reinz', 'Victor Reinz', 'Goetze', 'Payen', 'Ajusa'],
    'Электрика': ['Bosch', 'Valeo', 'Hella', 'Magneti Marelli', 'Denso', 'NGK', 'Champion', 'Beru', 'Brisk', 'EQS'],
    'Охлаждение': ['Valeo', 'Mahle', 'Behr', 'Nissens', 'Denso', 'AVA', 'Hella', 'Trucktec', 'Van Wezel', 'NRF'],
    'Выхлопная система': ['Bosal', 'Walker', 'Eberspacher', 'Remus', 'Magnaflow', 'Boris', 'Polmostrow', 'Fonos', 'Venix', 'Stenex']
}

def generate_products():
    count = 0
    for category, manufacturers in categories.items():
        for i, manufacturer in enumerate(manufacturers):
            for j in range(3):  # по 3 товара на производителя
                if count >= 1000:
                    break
                article = f"{category[:3].upper()}-{manufacturer[:3].upper()}-{j+1:03d}"
                name = f"{category[:-1]} {manufacturer} {'Premium' if j==0 else 'Standard' if j==1 else 'Econom'}"
                price = round((j+1) * 500 + len(manufacturer) * 10, 2)
                
                Product.objects.get_or_create(
                    article=article,
                    defaults={
                        'name': name,
                        'category': category,
                        'manufacturer': manufacturer,
                        'retail_price': price,
                        'stock_quantity': 50 + j * 20
                    }
                )
                count += 1
                print(f"Создан товар: {article} - {name} ({price} руб.)")
            
            if count >= 1000:
                break
        if count >= 1000:
            break
    
    print(f"\n✅ Готово! Создано {count} товаров.")

if __name__ == "__main__":
    generate_products()