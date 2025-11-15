from django.shortcuts import render
from .models import Category, Product

def index(request):
    categoria_id = request.GET.get('categoria')
    categorias = Category.objects.all()
    productos = Product.objects.all()
    if categoria_id:
        productos = productos.filter(categoria_id=categoria_id)
    return render(request, 'index.html', {
        'categorias': categorias,
        'productos': productos,
        'categoria_id': categoria_id,
    })


# Vista de detalle de producto
from django.shortcuts import get_object_or_404
import random

def productos(request, producto_id):
    producto = get_object_or_404(Product, id=producto_id)
    # Carrusel: por ahora solo una imagen, pero estructura lista para varias
    imagenes = [producto.imagen] if producto.imagen else []

    # Sugeridos: otros productos de la misma categoría, si hay; si no, aleatorios
    sugeridos = Product.objects.exclude(id=producto.id)
    if producto.categoria:
        sugeridos = sugeridos.filter(categoria=producto.categoria)
    sugeridos = list(sugeridos)
    random.shuffle(sugeridos)
    sugeridos = sugeridos[:4]

    return render(request, 'productos.html', {
        'producto': producto,
        'imagenes': imagenes,
        'sugeridos': sugeridos,
    })
