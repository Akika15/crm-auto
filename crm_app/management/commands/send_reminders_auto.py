from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.conf import settings
from crm_app.models import ServiceReminder
from datetime import date

class Command(BaseCommand):
    help = 'Автоматическая отправка сервисных напоминаний'

    def handle(self, *args, **options):
        today = date.today()
        self.stdout.write(f'Проверка напоминаний на {today}...')
        
        reminders = ServiceReminder.objects.filter(
            scheduled_date=today,
            status='pending',
            consent_given=True
        )
        
        count = 0
        for reminder in reminders:
            client = reminder.client
            vehicle = reminder.vehicle
            
            subject = f'Сервисное напоминание: {reminder.get_reminder_type_display()}'
            message = f"""Здравствуйте, {client.first_name} {client.last_name}!

Напоминаем, что для вашего автомобиля {vehicle.brand} {vehicle.model} ({vehicle.year})
требуется: {reminder.get_reminder_type_display()}.

Пожалуйста, посетите наш магазин.

---
Это автоматическое сообщение."""
            
            try:
                send_mail(
                    subject=subject,
                    message=message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[client.email],
                    fail_silently=False,
                )
                
                reminder.status = 'sent'
                reminder.sent_date = today
                reminder.save()
                
                count += 1
                self.stdout.write(self.style.SUCCESS(f'  Отправлено: {client.last_name} {client.first_name}'))
                
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'  Ошибка: {e}'))
        
        self.stdout.write(f'\nОтправлено напоминаний: {count}')