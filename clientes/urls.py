# clientes/urls.py
from django.urls import path
from .views import (
    ClienteListView,
    ClienteCreateView,
    ClienteUpdateView,
    ClienteDeleteView
)

urlpatterns = [
    path('clientes/', ClienteListView.as_view(), name='clientes'),
    path('cliente/adicionar/', ClienteCreateView.as_view(), name='cliente_adicionar'),
    path('cliente/<int:pk>/editar/', ClienteUpdateView.as_view(), name='cliente_editar'),
    path('cliente/<int:pk>/apagar/', ClienteDeleteView.as_view(), name='cliente_apagar'),
]


