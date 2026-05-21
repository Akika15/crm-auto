from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Client, Vehicle, Order, Product, ServiceReminder
from .forms import ClientForm, OrderForm, ReminderForm
from datetime import datetime

# Главная страница (дашборд)
@login_required
def dashboard(request):
    recent_clients = Client.objects.all().order_by('-registration_date')[:5]
    recent_orders = Order.objects.all().order_by('-order_date')[:5]
    pending_reminders = ServiceReminder.objects.filter(
        status='pending', 
        scheduled_date__lte=datetime.now().date()
    )[:5]
    
    context = {
        'recent_clients': recent_clients,
        'recent_orders': recent_orders,
        'pending_reminders': pending_reminders,
    }
    return render(request, 'crm_app/dashboard.html', context)

# Список всех клиентов
@login_required
def client_list(request):
    clients = Client.objects.all().order_by('last_name')
    return render(request, 'crm_app/client_list.html', {'clients': clients})

# Карточка клиента (с его автомобилями и историей заказов)
@login_required
def client_detail(request, pk):
    client = get_object_or_404(Client, pk=pk)
    vehicles = client.vehicles.all()
    orders = client.orders.all().order_by('-order_date')
    reminders = client.reminders.all().order_by('-scheduled_date')
    
    context = {
        'client': client,
        'vehicles': vehicles,
        'orders': orders,
        'reminders': reminders,
    }
    return render(request, 'crm_app/client_detail.html', context)

# Добавление нового клиента
@login_required
def client_create(request):
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            client = form.save()
            return redirect('crm_app:client_detail', pk=client.pk)
    else:
        form = ClientForm()
    return render(request, 'crm_app/client_form.html', {'form': form, 'title': 'Добавление клиента'})

# Редактирование клиента
@login_required
def client_edit(request, pk):
    client = get_object_or_404(Client, pk=pk)
    if request.method == 'POST':
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            return redirect('crm_app:client_detail', pk=client.pk)
    else:
        form = ClientForm(instance=client)
    return render(request, 'crm_app/client_form.html', {'form': form, 'title': 'Редактирование клиента'})

# Список всех заказов
@login_required
def order_list(request):
    orders = Order.objects.all().order_by('-order_date')
    return render(request, 'crm_app/order_list.html', {'orders': orders})

# Детали заказа
@login_required
def order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk)
    return render(request, 'crm_app/order_detail.html', {'order': order})

# Создание нового заказа
@login_required
def order_create(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.manager = request.user
            order.save()
            return redirect('crm_app:order_detail', pk=order.pk)
    else:
        form = OrderForm()
    return render(request, 'crm_app/order_form.html', {'form': form, 'title': 'Новый заказ'})

# Список сервисных напоминаний
@login_required
def reminder_list(request):
    reminders = ServiceReminder.objects.all().order_by('scheduled_date')
    return render(request, 'crm_app/reminder_list.html', {'reminders': reminders})

# Создание напоминания
@login_required
def reminder_create(request):
    if request.method == 'POST':
        form = ReminderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('crm_app:reminder_list')
    else:
        form = ReminderForm()
    return render(request, 'crm_app/reminder_form.html', {'form': form, 'title': 'Новое напоминание'})