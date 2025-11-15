from django.core.exceptions import ObjectDoesNotExist
from app1.models import Product, Category


def crear_categoria(nombre):
    """Crea una categoría nueva o devuelve la existente."""
    nombre = (nombre or '').strip()
    if not nombre:
        return None
    cat, _ = Category.objects.get_or_create(nombre=nombre)
    return cat


def obtener_categorias():
    return Category.objects.all()


def eliminar_categoria(cat_id):
    Category.objects.filter(id=cat_id).delete()


def crear_producto(nombre, precio, descripcion='', categoria_id=None, imagen=None):
    """Crea un producto. `imagen` puede ser un File (request.FILES['imagen'])."""
    nombre = (nombre or '').strip()
    if not nombre:
        raise ValueError('El nombre es obligatorio')
    try:
        precio_val = float(precio)
    except (TypeError, ValueError):
        precio_val = 0

    categoria = None
    if categoria_id:
        try:
            categoria = Category.objects.get(id=categoria_id)
        except ObjectDoesNotExist:
            categoria = None

    producto = Product.objects.create(
        nombre=nombre,
        precio=precio_val,
        descripcion=descripcion or '',
        categoria=categoria,
        imagen=imagen,
    )
    return producto


def obtener_productos():
    return Product.objects.select_related('categoria').all()


def eliminar_producto(producto_id):
    Product.objects.filter(id=producto_id).delete()


def actualizar_producto(producto_id, **kwargs):
    """Actualizar campos permitidos de un producto."""
    try:
        p = Product.objects.get(id=producto_id)
    except ObjectDoesNotExist:
        return None

    for field in ('nombre', 'descripcion', 'precio'):
        if field in kwargs and kwargs[field] is not None:
            setattr(p, field, kwargs[field])

    if 'categoria_id' in kwargs:
        cat_id = kwargs.get('categoria_id')
        if cat_id:
            try:
                p.categoria = Category.objects.get(id=cat_id)
            except ObjectDoesNotExist:
                p.categoria = None
        else:
            p.categoria = None

    if 'imagen' in kwargs and kwargs['imagen'] is not None:
        p.imagen = kwargs['imagen']

    p.save()
    return p
