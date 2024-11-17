from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import TaskForm
from .models import *
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import json

# Vista de la página principal
def home(request):
    return render(request, 'home.html')

# Vista para registrarse (crear usuario)
def singup(request):
    if request.method == 'GET':
        # Renderiza el formulario de registro
        return render(request, 'singup.html', {'form': UserCreationForm})
    else:
        # Valida si las contraseñas coinciden
        if request.POST['password1'] == request.POST['password2']:
            try:
                # Crea el usuario y lo guarda en la base de datos
                user = User.objects.create_user(
                    username=request.POST['username'], password=request.POST['password1'])
                user.save()
                # Inicia sesión automáticamente al registrarse
                login(request, user)
                return redirect('task')
            except IntegrityError:
                # Maneja error si el usuario ya existe
                return render(request, 'singup.html', {
                    'form': UserCreationForm,
                    "error": 'Usuario ya existe'
                })
        # Maneja el caso donde las contraseñas no coincidan
        return render(request, 'singup.html', {
            'form': UserCreationForm,
            "error": 'Contraseñas no coinciden'
        })

# Vista para mostrar las tareas pendientes del usuario
@login_required
def task(request):
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=True)
    return render(request, 'tasks.html', {'tasks': tasks})

# Vista para mostrar las tareas completadas del usuario
@login_required
def task_completed(request):
    tasks = Task.objects.filter(
        user=request.user, datecompleted__isnull=False).order_by('-datecompleted')
    return render(request, 'tasks.html', {'tasks': tasks})

# Vista para crear nuevas tareas
@login_required
def create_task(request):
    if request.method == 'GET':
        # Renderiza el formulario para crear una tarea
        return render(request, 'create_task.html', {'form': TaskForm})
    else:
        try:
            # Procesa el formulario y asocia la tarea al usuario actual
            form = TaskForm(request.POST)
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.save()
            return redirect('task')
        except ValueError:
            # Maneja errores en la entrada del formulario
            return render(request, 'create_task.html', {
                'form': TaskForm,
                'error': 'Por favor introduce un dato válido'
            })

# Vista para mostrar y editar detalles de una tarea específica
@login_required
def task_detail(request, task_id):
    if request.method == 'GET':
        # Obtiene la tarea del usuario y la muestra en un formulario
        task = get_object_or_404(Task, pk=task_id, user=request.user)
        form = TaskForm(instance=task)
        return render(request, 'task_detail.html', {'task': task, 'form': form})
    else:
        try:
            # Actualiza la tarea con los datos del formulario
            task = get_object_or_404(Task, pk=task_id, user=request.user)
            form = TaskForm(request.POST, instance=task)
            form.save()
            return redirect('home')
        except ValueError:
            # Maneja errores al actualizar la tarea
            return render(request, 'task_detail.html', {
                'task': task, 'form': form, 'error': "Error al cambiar la tarea"
            })

# Vista para marcar una tarea como completada
@login_required
def complete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.datecompleted = timezone.now()
        task.save()
        return redirect('task')

# Vista para eliminar una tarea
@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('task')

# Vista para cerrar sesión
@login_required
def singout(request):
    logout(request)
    return redirect('home')

# Vista para iniciar sesión
def singin(request):
    if request.method == 'GET':
        # Renderiza el formulario de inicio de sesión
        return render(request, 'singin.html', {'form': AuthenticationForm()})
    else:
        # Autentica al usuario
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            # Muestra error si las credenciales son inválidas
            return render(request, 'singin.html', {
                'form': AuthenticationForm(),
                'error': 'Por favor, ingresa un usuario y contraseña válidos.'
            })
        else:
            # Inicia sesión y redirige a las tareas
            login(request, user)
            return redirect('task')

# Vista para mostrar la tienda (productos disponibles)
def store(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        # Datos vacíos para usuarios no autenticados
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        cartItems = order['get_cart_items']

    products = Product.objects.all()
    context = {'products': products, 'cartItems': cartItems}
    return render(request, 'store/store.html', context)

# Vista para mostrar el carrito de compras
def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        # Datos vacíos para usuarios no autenticados
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        cartItems = order['get_cart_items']

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'store/cart.html', context)

# Vista para el proceso de pago
def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        # Datos vacíos para usuarios no autenticados
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        cartItems = order['get_cart_items']

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'store/checkout.html', context)

# Vista para gestionar favoritos
def fav(request):
    plant_id = request.GET.get('plant_id')
    if plant_id:
        # Añade una planta a los favoritos
        plant = Plants.objects.get(id=plant_id)
        favorite, created = FavoritePlant.objects.get_or_create(
            user=request.user, plant=plant)
        if created:
            message = f"{plant.name} se ha añadido a tus favoritos."
        else:
            message = f"{plant.name} ya estaba en tus favoritos."
    else:
        message = ""

    # Elimina una planta de los favoritos si es necesario
    remove_plant_id = request.GET.get('remove_id')
    if remove_plant_id:
        plant_to_remove = get_object_or_404(Plants, id=remove_plant_id)
        favorite_to_remove = FavoritePlant.objects.filter(
            user=request.user, plant=plant_to_remove)
        favorite_to_remove.delete()
        message = f"{plant_to_remove.name} ha sido eliminado de tus favoritos."

    favorites = FavoritePlant.objects.filter(user=request.user)
    context = {'favorites': favorites, 'message': message}
    return render(request, 'store/fav.html', context)

# Vista para listar todas las plantas
def plants(request):
    plantas = Plants.objects.all()
    context = {'plants': plantas}
    return render(request, 'store/plants.html', context)

# Vista para actualizar elementos del carrito de compras
def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('Action:', action)
    print('Product:', productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(
        customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(
        order=order, product=product)

    # Incrementa o reduce la cantidad de un producto en el carrito
    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    # Elimina el artículo si la cantidad llega a cero
    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item añadido', safe=False)
