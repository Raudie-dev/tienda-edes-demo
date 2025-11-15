from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('registro/', views.registro, name='registro'),
    path('control_productos/', views.control_productos, name='control_productos'),
    path('solicitudes/', views.solicitudes_cotizacion, name='solicitudes_cotizacion'),
]