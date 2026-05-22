from django.db import models
from django.contrib.auth.models import User

class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Пользователь')
    last_name = models.CharField('Фамилия', max_length=50, blank=True, null=True)
    first_name = models.CharField('Имя', max_length=50, blank=True, null=True)
    middle_name = models.CharField('Отчество', max_length=50, blank=True, null=True)
    phone = models.CharField('Телефон', max_length=20, blank=True, null=True, unique=True)
    email = models.EmailField('Email', blank=True, null=True, unique=True)
    address = models.TextField('Адрес', blank=True, null=True)
    registration_date = models.DateField('Дата регистрации', auto_now_add=True)
    comments = models.TextField('Комментарии', blank=True, null=True)
    
    def __str__(self):
        return f'{self.last_name} {self.first_name}'

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'


class Vehicle(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='vehicles', verbose_name='Клиент')
    brand = models.CharField('Марка', max_length=50)
    model = models.CharField('Модель', max_length=50)
    year = models.IntegerField('Год выпуска')
    vin = models.CharField('VIN-код', max_length=17, unique=True, blank=True, null=True)
    license_plate = models.CharField('Госномер', max_length=20, blank=True, null=True)
    engine_volume = models.DecimalField('Объём двигателя', max_digits=3, decimal_places=1, blank=True, null=True)
    current_mileage = models.IntegerField('Текущий пробег', blank=True, null=True)

    def __str__(self):
        return f'{self.brand} {self.model} ({self.year})'

    class Meta:
        verbose_name = 'Автомобиль'
        verbose_name_plural = 'Автомобили'


class Product(models.Model):
    article = models.CharField('Артикул', max_length=50, unique=True)
    name = models.CharField('Наименование', max_length=200)
    category = models.CharField('Категория', max_length=50, blank=True, null=True)
    manufacturer = models.CharField('Производитель', max_length=100, blank=True, null=True)
    retail_price = models.DecimalField('Розничная цена', max_digits=10, decimal_places=2)
    stock_quantity = models.IntegerField('Остаток на складе', default=0)
    compatible_brands = models.TextField(blank=True, null=True, verbose_name='Совместимые марки (через запятую)')
    compatible_models = models.TextField(blank=True, null=True, verbose_name='Совместимые модели (через запятую)')

    def __str__(self):
        return f'{self.article} - {self.name}'

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class Order(models.Model):
    STATUS_CHOICES = [
        ('new', 'Новый'),
        ('confirmed', 'Подтверждён'),
        ('paid', 'Оплачен'),
        ('shipped', 'Отгружен'),
        ('completed', 'Выполнен'),
        ('cancelled', 'Отменён'),
    ]

    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='orders', verbose_name='Клиент')
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='orders', verbose_name='Автомобиль')
    manager = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders', verbose_name='Менеджер')
    order_date = models.DateTimeField('Дата заказа', auto_now_add=True)
    status = models.CharField('Статус', max_length=20, choices=STATUS_CHOICES, default='new')
    total_amount = models.DecimalField('Общая сумма', max_digits=10, decimal_places=2)
    payment_method = models.CharField('Способ оплаты', max_length=20, blank=True, null=True)
    delivery_method = models.CharField('Способ доставки', max_length=20, blank=True, null=True)
    comments = models.TextField('Комментарии', blank=True, null=True)

    def __str__(self):
        return f'Заказ №{self.id} от {self.order_date}'

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', verbose_name='Заказ')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товар')
    quantity = models.IntegerField('Количество')
    price_at_moment = models.DecimalField('Цена на момент продажи', max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.product.name} x {self.quantity}'

    class Meta:
        verbose_name = 'Позиция заказа'
        verbose_name_plural = 'Позиции заказов'


class ServiceReminder(models.Model):
    REMINDER_TYPES = [
        ('oil_change', 'Замена масла'),
        ('filter_change', 'Замена фильтров'),
        ('brake_pads', 'Замена колодок'),
        ('seasonal_tires', 'Сезонная смена шин'),
        ('timing_belt', 'Замена ремня ГРМ'),
        ('coolant', 'Замена охлаждающей жидкости'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Ожидает'),
        ('sent', 'Отправлено'),
        ('viewed', 'Просмотрено'),
        ('responded', 'Клиент откликнулся'),
    ]

    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='reminders', verbose_name='Клиент')
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='reminders', verbose_name='Автомобиль')
    reminder_type = models.CharField('Тип напоминания', max_length=30, choices=REMINDER_TYPES)
    last_service_date = models.DateField('Дата последнего обслуживания', blank=True, null=True)
    last_service_mileage = models.IntegerField('Пробег при последнем обслуживании', blank=True, null=True)
    interval_days = models.IntegerField('Интервал в днях', blank=True, null=True)
    interval_km = models.IntegerField('Интервал в км', blank=True, null=True)
    scheduled_date = models.DateField('Дата планируемой отправки')
    sent_date = models.DateField('Дата отправки', blank=True, null=True)
    status = models.CharField('Статус', max_length=20, choices=STATUS_CHOICES, default='pending')
    consent_given = models.BooleanField('Согласие на получение', default=False)
    consent_date = models.DateTimeField('Дата согласия', blank=True, null=True)
    consent_ip = models.GenericIPAddressField('IP-адрес согласия', blank=True, null=True)

    def __str__(self):
        return f'{self.get_reminder_type_display()} для {self.client}'

    class Meta:
        verbose_name = 'Сервисное напоминание'
        verbose_name_plural = 'Сервисные напоминания'