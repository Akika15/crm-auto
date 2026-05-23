from django.contrib import admin
from django.core.mail import send_mail
from django.conf import settings
from datetime import date
from .models import *

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'last_name', 'first_name', 'phone', 'email', 'registration_date')
    list_filter = ('registration_date',)
    search_fields = ('last_name', 'first_name', 'phone', 'email')

@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ('id', 'client', 'brand', 'model', 'year', 'vin', 'license_plate')
    list_filter = ('brand', 'year')
    search_fields = ('brand', 'model', 'vin', 'license_plate')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'client', 'order_date', 'status', 'total_amount', 'manager')
    list_filter = ('status', 'order_date')
    search_fields = ('client__last_name', 'client__first_name')

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'product', 'quantity', 'price_at_moment')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'article', 'short_name', 'slug_short', 'category', 'price', 'is_available', 'is_new', 'is_hit', 'is_recommended', 'stock_quantity')
    list_filter = ('category', 'is_available', 'is_new', 'is_hit', 'is_recommended')
    search_fields = ('article', 'name', 'manufacturer', 'slug')
    list_editable = ('price', 'is_available', 'is_new', 'is_hit', 'is_recommended', 'stock_quantity')
    prepopulated_fields = {'slug': ('name',)}
    list_per_page = 50
    
    def short_name(self, obj):
        return obj.name[:35] + '...' if len(obj.name) > 35 else obj.name
    short_name.short_description = 'Название'
    
    def slug_short(self, obj):
        return obj.slug[:25] + '...' if obj.slug and len(obj.slug) > 25 else obj.slug
    slug_short.short_description = 'Slug'
    
    fieldsets = (
        ('Основное', {'fields': ('category', 'article', 'name', 'slug', 'description', 'image', 'manufacturer', 'country_of_origin', 'factory')}),
        ('Цены и наличие', {'fields': ('price', 'is_available', 'stock_quantity')}),
        ('Акции и метки', {'fields': ('is_new', 'is_hit', 'is_recommended')}),
    )

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug', 'parent', 'order')
    list_filter = ('parent',)
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}

@admin.register(ServiceReminder)
class ServiceReminderAdmin(admin.ModelAdmin):
    list_display = ('id', 'client', 'vehicle', 'reminder_type', 'scheduled_date', 'status', 'consent_given')
    list_filter = ('reminder_type', 'status', 'scheduled_date')
    search_fields = ('client__last_name', 'client__first_name')
    
    actions = ['send_reminder_email']
    
    def send_reminder_email(self, request, queryset):
        count = 0
        for reminder in queryset:
            if reminder.consent_given and reminder.status != 'sent':
                client = reminder.client
                vehicle = reminder.vehicle
                
                subject = f'Сервисное напоминание: {reminder.get_reminder_type_display()}'
                message = f"""Здравствуйте, {client.first_name} {client.last_name}!

Напоминаем, что для вашего автомобиля {vehicle.brand} {vehicle.model} ({vehicle.year})
требуется: {reminder.get_reminder_type_display()}.

Пожалуйста, посетите наш магазин.

---
Это автоматическое сообщение."""
                
                send_mail(
                    subject=subject,
                    message=message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[client.email],
                    fail_silently=False,
                )
                
                reminder.status = 'sent'
                reminder.sent_date = date.today()
                reminder.save()
                count += 1
        
        self.message_user(request, f'Отправлено напоминаний: {count}')
    
    send_reminder_email.short_description = 'Отправить выбранные напоминания по email'

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'session_key', 'created_at')
    search_fields = ('user__username', 'session_key')

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'cart', 'product', 'quantity')

@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'product', 'added_at')
    search_fields = ('user__username', 'product__name')