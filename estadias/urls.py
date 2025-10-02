from django.urls import path
from .views import (

    EstadiaListView, EstadiaChegadaCreateView, EstadiaChegadaUpdateView, EstadiaSaidaUpdateView, EstadiaDeleteView)

urlpatterns = [
    path('estadias', EstadiaListView.as_view(), name='estadias'),
    path('estadia/chegada/', EstadiaChegadaCreateView.as_view(), name='estadia_chegada'),
    path('estadia/<int:pk>/editar/', EstadiaChegadaUpdateView.as_view(), name='estadia_editar'),
    path('estadia/<int:pk>/saida/', EstadiaSaidaUpdateView.as_view(), name='estadia_saida'),
    path('estadia/<int:pk>/apagar/', EstadiaDeleteView.as_view(), name='estadia_apagar'),
]

