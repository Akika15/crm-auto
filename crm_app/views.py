from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .models import Client, Vehicle, Order, Product, ServiceReminder, OrderItem, Category, Cart, CartItem, Wishlist
from .forms import ClientForm, OrderForm, ReminderForm, VehicleForm
from datetime import datetime

def dashboard(request):
    if request.user.is_authenticated:
        is_staff = request.user.is_staff
        if is_staff:
            recent_clients = Client.objects.all().order_by('-registration_date')[:5]
            recent_orders = Order.objects.all().order_by('-order_date')[:5]
            pending_reminders = ServiceReminder.objects.filter(
                status='pending', scheduled_date__lte=datetime.now().date()
            )[:5]
        else:
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
    if not request.user.is_staff:
        return redirect('crm_app:dashboard')
    clients = Client.objects.all().order_by('last_name')
    return render(request, 'crm_app/client_list.html', {'clients': clients})

@login_required
def client_detail(request, pk):
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
        orders = Order.objects.all().order_by('-order_date')
    else:
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
    selected_vehicle_id = request.GET.get('vehicle') or (vehicles.first().id if vehicles else None)
    selected_vehicle = None
    products = []
    
    if selected_vehicle_id:
        selected_vehicle = get_object_or_404(Vehicle, id=selected_vehicle_id, client=client)
        products = get_compatible_products(selected_vehicle)
    else:
        products = Product.objects.filter(is_available=True)
    
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.manager = request.user
            order.total_amount = 0
            order.save()
            
            # Обрабатываем несколько товаров
            total = 0
            product_ids = request.POST.getlist('product_ids')
            quantities = request.POST.getlist('quantities')
            
            for product_id, quantity in zip(product_ids, quantities):
                if product_id and int(quantity) > 0:
                    product = Product.objects.get(id=product_id)
                    OrderItem.objects.create(
                        order=order,
                        product=product,
                        quantity=int(quantity),
                        price_at_moment=product.price
                    )
                    total += product.price * int(quantity)
            
            order.total_amount = total
            order.save()
            return redirect('crm_app:order_detail', pk=order.pk)
    else:
        form = OrderForm(initial={'client': client, 'vehicle': selected_vehicle})
        form.fields['client'].queryset = Client.objects.filter(id=client.id)
        form.fields['vehicle'].queryset = vehicles
    
    context = {
        'form': form,
        'title': 'Новый заказ',
        'vehicles': vehicles,
        'products': products,
        'selected_vehicle': selected_vehicle,
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


# ========== НОВЫЕ ФУНКЦИИ ДЛЯ ИНТЕРНЕТ-МАГАЗИНА ==========

def catalog(request, slug=None):
    """Страница каталога"""
    products = Product.objects.filter(is_available=True)
    categories = Category.objects.filter(parent__isnull=True)
    
    current_category = None
    breadcrumbs = []
    
    if slug:
        current_category = get_object_or_404(Category, slug=slug)
        # Получаем все товары из этой категории и подкатегорий
        products = products.filter(category__in=current_category.get_descendants(include_self=True))
        # Строим хлебные крошки
        parent = current_category.parent
        while parent:
            breadcrumbs.insert(0, parent)
            parent = parent.parent
    
    context = {
        'products': products,
        'categories': categories,
        'current_category': current_category,
        'breadcrumbs': breadcrumbs,
    }
    return render(request, 'crm_app/catalog.html', context)


def product_detail(request, slug):
    """Страница товара"""
    product = get_object_or_404(Product, slug=slug)
    related_products = Product.objects.filter(
        category=product.category, 
        is_available=True
    ).exclude(id=product.id)[:6]
    
    context = {
        'product': product,
        'related_products': related_products,
    }
    return render(request, 'crm_app/product_detail.html', context)


def get_cart(request):
    """Вспомогательная функция для получения корзины"""
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        if not request.session.session_key:
            request.session.create()
        cart, created = Cart.objects.get_or_create(session_key=request.session.session_key)
    return cart


def cart_view(request):
    """Страница корзины"""
    cart = get_cart(request)
    context = {'cart': cart}
    return render(request, 'crm_app/cart.html', context)


def cart_add(request, product_id):
    """Добавление товара в корзину"""
    product = get_object_or_404(Product, id=product_id)
    cart = get_cart(request)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('crm_app:cart_view')


def cart_remove(request, item_id):
    """Удаление товара из корзины"""
    cart_item = get_object_or_404(CartItem, id=item_id)
    cart_item.delete()
    return redirect('crm_app:cart_view')


def cart_update(request, item_id):
    """Обновление количества товара в корзине"""
    cart_item = get_object_or_404(CartItem, id=item_id)
    quantity = int(request.POST.get('quantity', 1))
    if quantity > 0:
        cart_item.quantity = quantity
        cart_item.save()
    return redirect('crm_app:cart_view')

def page(request, title):
    return render(request, 'crm_app/pages.html', {'title': title})    

@login_required
def wishlist_view(request):
    wishlist_items = Wishlist.objects.filter(user=request.user)
    return render(request, 'crm_app/wishlist.html', {'wishlist_items': wishlist_items})

def guest_home(request):
    new_products = Product.objects.filter(is_new=True, is_available=True)[:8]
    hit_products = Product.objects.filter(is_hit=True, is_available=True)[:8]
    recommended_products = Product.objects.filter(is_recommended=True, is_available=True)[:8]
    context = {
        'new_products': new_products,
        'hit_products': hit_products,
        'recommended_products': recommended_products,
    }
    return render(request, 'crm_app/guest_home.html', context)

@login_required
def wishlist_add(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    Wishlist.objects.get_or_create(user=request.user, product=product)
    return redirect(request.META.get('HTTP_REFERER', 'crm_app:catalog'))

@login_required
def wishlist_remove(request, product_id):
    Wishlist.objects.filter(user=request.user, product_id=product_id).delete()
    return redirect('crm_app:wishlist')

def page(request, title):
    return render(request, 'crm_app/pages.html', {'title': title})

def help_page(request):
    return render(request, 'crm_app/help.html')

def get_compatible_products(vehicle):
    """Возвращает товары, совместимые с указанным автомобилем"""
    if not vehicle:
        return Product.objects.filter(is_available=True)
    
    products = Product.objects.filter(is_available=True)
    
    # Фильтруем по марке и модели
    compatible = []
    for product in products:
        brands = [b.strip().lower() for b in (product.compatible_brands or '').split(',') if b.strip()]
        models = [m.strip().lower() for m in (product.compatible_models or '').split(',') if m.strip()]
        
        if brands and vehicle.brand.lower() not in brands:
            continue
        if models and vehicle.model.lower() not in models:
            continue
        compatible.append(product.id)
    
    if compatible:
        return Product.objects.filter(id__in=compatible, is_available=True)
    return products