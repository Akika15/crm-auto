from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Пользователь')
    last_name = models.CharField('Фамилия', max_length=50, blank=True, null=True)
    first_name = models.CharField('Имя', max_length=50, blank=True, null=True)
    middle_name = models.CharField('Отчество', max_length=50, blank=True, null=True)
    phone = models.CharField('Телефон', max_length=20, blank=True, null=True)
    email = models.EmailField('Email', blank=True, null=True)
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


class Category(models.Model):
    """Модель категории товаров (древовидная структура)"""
    name = models.CharField('Название', max_length=100)
    slug = models.SlugField(unique=True, db_index=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    image = models.ImageField('Изображение категории', upload_to='categories/', blank=True, null=True)
    order = models.PositiveIntegerField('Порядок', default=0)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['order', 'name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('crm_app:catalog', kwargs={'slug': self.slug})

    def get_products(self):
        """Возвращает все товары из этой категории и подкатегорий"""
        products = Product.objects.filter(category__in=self.get_descendants(include_self=True))
        return products

    def get_descendants(self, include_self=False):
        """Возвращает список всех подкатегорий"""
        descendants = []
        if include_self:
            descendants.append(self)
        for child in self.children.all():
            descendants.extend(child.get_descendants(include_self=True))
        return descendants


class Product(models.Model):
    """Модель товара"""
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', verbose_name='Категория', null=True, blank=True)
    article = models.CharField('Артикул', max_length=50, unique=True)
    name = models.CharField('Наименование', max_length=200)
    slug = models.SlugField(unique=True, db_index=True, blank=True)
    description = models.TextField('Описание', blank=True, null=True)
    image = models.ImageField('Главное изображение', upload_to='products/', blank=True, null=True)
    price = models.DecimalField('Цена', max_digits=10, decimal_places=2, default=0)
    is_available = models.BooleanField('В наличии', default=True)
    is_new = models.BooleanField('Новинка', default=False)
    is_hit = models.BooleanField('Хит продаж', default=False)
    is_recommended = models.BooleanField('Рекомендуемый', default=False)
    stock_quantity = models.IntegerField('Остаток на складе', default=0)
    manufacturer = models.CharField('Производитель', max_length=100, blank=True, null=True)
    compatible_brands = models.TextField('Совместимые марки (через запятую)', blank=True, null=True)
    compatible_models = models.TextField('Совместимые модели (через запятую)', blank=True, null=True)

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['-id']

    def __str__(self):
        return f'{self.name} ({self.article})'

    def get_absolute_url(self):
        return reverse('crm_app:product_detail', kwargs={'slug': self.slug})


class Order(models.Model):
    STATUS_CHOICES = [
        ('new', 'Новый'),
        ('confirmed', 'Подтверждён'),
        ('paid', 'Оплачен'),
        ('shipped', 'Отгружен'),
        ('completed', 'Выполнен'),
        ('cancelled', 'Отменён'),
    ]

    PAYMENT_CHOICES = [
        ('cash', 'Наличные при получении'),
        ('card', 'Банковская карта (онлайн)'),
        ('card_courier', 'Банковская карта курьеру'),
        ('bank_transfer', 'Безналичный расчет (для юрлиц)'),
    ]

    DELIVERY_CHOICES = [
        ('pickup', 'Самовывоз (магазин)'),
        ('courier', 'Доставка курьером'),
        ('delivery', 'Доставка транспортной компанией'),
    ]

    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='orders', verbose_name='Клиент')
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='orders', verbose_name='Автомобиль', null=True, blank=True)
    manager = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders', verbose_name='Менеджер')
    order_date = models.DateTimeField('Дата заказа', auto_now_add=True)
    status = models.CharField('Статус', max_length=20, choices=STATUS_CHOICES, default='new')
    total_amount = models.DecimalField('Общая сумма', max_digits=10, decimal_places=2, default=0)
    payment_method = models.CharField('Способ оплаты', max_length=20, choices=PAYMENT_CHOICES, blank=True, null=True)
    delivery_method = models.CharField('Способ доставки', max_length=20, choices=DELIVERY_CHOICES, blank=True, null=True)
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


class Cart(models.Model):
    """Модель корзины"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, related_name='cart')
    session_key = models.CharField(max_length=40, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'

    def __str__(self):
        if self.user:
            return f'Корзина {self.user.username}'
        return f'Корзина (сессия: {self.session_key})'

    def get_total_price(self):
        return sum(item.get_total_price() for item in self.items.all())

    def get_total_quantity(self):
        return sum(item.quantity for item in self.items.all())


class CartItem(models.Model):
    """Модель позиции в корзине"""
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        verbose_name = 'Товар в корзине'
        verbose_name_plural = 'Товары в корзине'

    def __str__(self):
        return f'{self.product.name} x {self.quantity}'

    def get_total_price(self):
        return self.product.price * self.quantity


class Wishlist(models.Model):
    """Модель избранного"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wishlist')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'
        unique_together = ('user', 'product')

    def __str__(self):
        return f'{self.user.username} - {self.product.name}'