from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from .models import User_admin
from .crud import (
    crear_categoria,
    obtener_categorias,
    crear_producto,
    obtener_productos,
    eliminar_producto,
    eliminar_categoria,
)


def login(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre', '').strip()
        password = request.POST.get('password', '')

        try:
            user = User_admin.objects.get(nombre=nombre)
            if user.bloqueado:
                messages.error(request, 'Usuario bloqueado')
            elif user.password == password or check_password(password, user.password):
                request.session['user_admin_id'] = user.id
                return redirect('control')
            else:
                messages.error(request, 'Contraseña incorrecta')
            return render(request, 'login.html')
        except User_admin.DoesNotExist:
            messages.error(request, 'Usuario no encontrado')
            return render(request, 'login.html')

    return render(request, 'login.html')


def control(request):
    user_id = request.session.get('user_admin_id')
    if not user_id:
        messages.error(request, 'Debe iniciar sesión primero')
        return redirect('login')
    try:
        user = User_admin.objects.get(id=user_id)
    except User_admin.DoesNotExist:
        messages.error(request, 'Usuario no encontrado')
        return redirect('login')
    # Nuevas operaciones: categorías y productos
    if request.method == 'POST':
        # Crear categoría
        if 'crear_categoria' in request.POST:
            nombre_cat = request.POST.get('categoria_nombre', '').strip()
            if nombre_cat:
                crear_categoria(nombre_cat)
                messages.success(request, 'Categoría creada')
            else:
                messages.error(request, 'El nombre de la categoría es obligatorio')

        # Crear producto
        elif 'crear_producto' in request.POST:
            nombre = request.POST.get('nombre', '').strip()
            precio = request.POST.get('precio', '0')
            descripcion = request.POST.get('descripcion', '')
            categoria_id = request.POST.get('categoria_id') or None
            imagen = request.FILES.get('imagen')
            if nombre:
                try:
                    crear_producto(nombre, precio, descripcion, categoria_id, imagen)
                    messages.success(request, 'Producto creado correctamente')
                except Exception as e:
                    messages.error(request, f'Error al crear el producto: {e}')
            else:
                messages.error(request, 'El nombre del producto es obligatorio')

        # Eliminar producto
        elif 'eliminar_producto' in request.POST:
            pid = request.POST.get('eliminar_producto')
            if pid:
                eliminar_producto(pid)
                messages.success(request, 'Producto eliminado')

        # Eliminar categoría
        elif 'eliminar_categoria' in request.POST:
            cid = request.POST.get('eliminar_categoria')
            if cid:
                eliminar_categoria(cid)
                messages.success(request, 'Categoría eliminada')

    categorias = obtener_categorias()
    productos = obtener_productos()
    return render(request, 'control.html', {'productos': productos, 'categorias': categorias})