from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .models import Client, Vehicle, Order, Product, ServiceReminder, OrderItem
from .forms import ClientForm, OrderForm, ReminderForm, VehicleForm
from datetime import datetime

def dashboard(request):
    if request.user.is_authenticated:
        # Проверяем, является ли пользователь администратором (сотрудником)
        is_staff = request.user.is_staff
        
        if is_staff:
            # Администратор видит всех клиентов, заказы, напоминания
            recent_clients = Client.objects.all().order_by('-registration_date')[:5]
            recent_orders = Order.objects.all().order_by('-order_date')[:5]
            pending_reminders = ServiceReminder.objects.filter(
                status='pending', scheduled_date__lte=datetime.now().date()
            )[:5]
        else:
            # Обычный пользователь (клиент) видит только свои данные
            try:
                client = request.user.client
                recent_clients = []
                recent_orders = Order.objects.filter(client=client).order_by('-order_date')[:5]
                pending_reminders = ServiceReminder.objects.filter(
                    client=client, status='pending', scheduled_date__lte=datetime.now().date()
                )[:5]
            except:
                recent_clients = []
                recent_orders = []
                pending_reminders = []
        
        context = {
            'recent_clients': recent_clients,
            'recent_orders': recent_orders,
            'pending_reminders': pending_reminders,
            'is_staff': is_staff,
        }
        return render(request, 'crm_app/dashboard.html', context)
    else:
        return render(request, 'crm_app/guest_home.html')

@login_required
def client_list(request):
    # Проверяем, является ли пользователь администратором
    if not request.user.is_staff:
        return redirect('crm_app:dashboard')
    
    clients = Client.objects.all().order_by('last_name')
    return render(request, 'crm_app/client_list.html', {'clients': clients})

@login_required
def client_detail(request, pk):
    # Проверяем, является ли пользователь администратором
    if not request.user.is_staff:
        return redirect('crm_app:dashboard')
    
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

@login_required
def client_create(request):
    # Только администраторы могут создавать клиентов
    if not request.user.is_staff:
        return redirect('crm_app:dashboard')
    
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            client = form.save()
            return redirect('crm_app:client_detail', pk=client.pk)
    else:
        form = ClientForm()
    return render(request, 'crm_app/client_form.html', {'form': form, 'title': 'Добавление клиента'})

@login_required
def client_edit(request, pk):
    # Только администраторы могут редактировать клиентов
    if not request.user.is_staff:
        return redirect('crm_app:dashboard')
    
    client = get_object_or_404(Client, pk=pk)
    if request.method == 'POST':
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            return redirect('crm_app:client_detail', pk=client.pk)
    else:
        form = ClientForm(instance=client)
    return render(request, 'crm_app/client_form.html', {'form': form, 'title': 'Редактирование клиента'})

@login_required
def order_list(request):
    if request.user.is_staff:
        # Администратор видит все заказы
        orders = Order.objects.all().order_by('-order_date')
    else:
        # Клиент видит только свои заказы
        try:
            client = request.user.client
            orders = Order.objects.filter(client=client).order_by('-order_date')
        except:
            orders = []
    return render(request, 'crm_app/order_list.html', {'orders': orders})

@login_required
def order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk)
    
    if not request.user.is_staff:
        # Клиент может смотреть только свои заказы
        try:
            client = request.user.client
            if order.client.id != client.id:
                return redirect('crm_app:order_list')
        except:
            return redirect('crm_app:order_list')
    
    return render(request, 'crm_app/order_detail.html', {'order': order})

@login_required
def order_create(request):
    try:
        client = request.user.client
    except:
        return redirect('crm_app:profile')
    
    vehicles = Vehicle.objects.filter(client=client)
    products = Product.objects.all().order_by('category', 'name')[:100]
    
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.manager = request.user
            order.total_amount = 0
            order.save()
            
            product_id = request.POST.get('product')
            quantity = int(request.POST.get('quantity', 1))
            if product_id:
                product = Product.objects.get(id=product_id)
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=quantity,
                    price_at_moment=product.retail_price
                )
                order.total_amount = product.retail_price * quantity
                order.save()
            
            return redirect('crm_app:order_detail', pk=order.pk)
    else:
        form = OrderForm(initial={'client': client})
        form.fields['client'].queryset = Client.objects.filter(id=client.id)
        form.fields['vehicle'].queryset = vehicles
    
    context = {
        'form': form,
        'title': 'Новый заказ',
        'vehicles': vehicles,
        'products': products,
    }
    return render(request, 'crm_app/order_form.html', context)

@login_required
def reminder_list(request):
    if request.user.is_staff:
        reminders = ServiceReminder.objects.all().order_by('scheduled_date')
    else:
        try:
            client = request.user.client
            reminders = ServiceReminder.objects.filter(client=client).order_by('scheduled_date')
        except:
            reminders = []
    return render(request, 'crm_app/reminder_list.html', {'reminders': reminders})

@login_required
def reminder_create(request):
    if request.user.is_staff:
        if request.method == 'POST':
            form = ReminderForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('crm_app:reminder_list')
        else:
            form = ReminderForm()
    else:
        # Обычный клиент создаёт напоминание только для себя
        try:
            client = request.user.client
            if request.method == 'POST':
                form = ReminderForm(request.POST)
                if form.is_valid():
                    reminder = form.save(commit=False)
                    reminder.client = client
                    reminder.save()
                    return redirect('crm_app:reminder_list')
            else:
                form = ReminderForm(initial={'client': client})
                form.fields['client'].queryset = Client.objects.filter(id=client.id)
                form.fields['vehicle'].queryset = Vehicle.objects.filter(client=client)
        except:
            return redirect('crm_app:profile')
    
    return render(request, 'crm_app/reminder_form.html', {'form': form, 'title': 'Новое напоминание'})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Client.objects.create(
                user=user,
                last_name=user.username,
                first_name='',
                phone='',
                email=user.email
            )
            login(request, user)
            return redirect('crm_app:dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})
@login_required
def profile(request):
    try:
        client = request.user.client
    except:
        client = Client.objects.create(
            user=request.user,
            last_name=request.user.username,
            first_name='',
            phone='',
            email=request.user.email
        )
    
    if request.method == 'POST':
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            return redirect('crm_app:profile')
    else:
        form = ClientForm(instance=client)
    
    vehicles = client.vehicles.all()
    
    context = {
        'form': form,
        'client': client,
        'vehicles': vehicles,
    }
    return render(request, 'crm_app/profile.html', context)

@login_required
def vehicle_add(request):
    try:
        client = request.user.client
    except:
        return redirect('crm_app:profile')
    
    if request.method == 'POST':
        form = VehicleForm(request.POST)
        if form.is_valid():
            vehicle = form.save(commit=False)
            vehicle.client = client
            vehicle.save()
            return redirect('crm_app:profile')
    else:
        form = VehicleForm()
    return render(request, 'crm_app/vehicle_form.html', {'form': form, 'title': 'Добавление автомобиля'})

@login_required
def vehicle_edit(request, pk):
    try:
        client = request.user.client
        vehicle = get_object_or_404(Vehicle, pk=pk, client=client)
    except:
        return redirect('crm_app:profile')
    
    if request.method == 'POST':
        form = VehicleForm(request.POST, instance=vehicle)
        if form.is_valid():
            form.save()
            return redirect('crm_app:profile')
    else:
        form = VehicleForm(instance=vehicle)
    return render(request, 'crm_app/vehicle_form.html', {'form': form, 'title': 'Редактирование автомобиля'})

@login_required
def vehicle_delete(request, pk):
    try:
        client = request.user.client
        vehicle = get_object_or_404(Vehicle, pk=pk, client=client)
        vehicle.delete()
    except:
        pass
    return redirect('crm_app:profile')