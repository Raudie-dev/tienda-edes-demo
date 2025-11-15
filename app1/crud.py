from .models import Cliente, Cotizacion, CotizacionItem, Product

def crear_cliente(nombre, correo, telefono=''):
    nombre = (nombre or '').strip()
    correo = (correo or '').strip()
    telefono = (telefono or '').strip()
    if not nombre or not correo:
        raise ValueError("Nombre y correo son obligatorios")
    cliente = Cliente.objects.create(nombre=nombre, correo=correo, telefono=telefono)
    return cliente

def crear_cotizacion_desde_carrito(cliente, items, mensaje=''):
    """
    items: iterable de dicts {'product_id': int, 'cantidad': int}
    Crea la cotización y items asociados. Devuelve la instancia Cotizacion.
    """
    if not items:
        raise ValueError("No hay items en la cotización")
    cot = Cotizacion.objects.create(cliente=cliente, mensaje=(mensaje or '').strip())
    for it in items:
        pid = int(it.get('product_id'))
        cantidad = int(it.get('cantidad') or 1)
        try:
            prod = Product.objects.get(id=pid)
        except Product.DoesNotExist:
            continue
        CotizacionItem.objects.create(
            cotizacion=cot,
            producto=prod,
            cantidad=cantidad,
            precio_unitario=prod.precio
        )
    return cot
