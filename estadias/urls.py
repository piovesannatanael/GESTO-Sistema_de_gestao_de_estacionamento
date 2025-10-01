from django.urls import path
from .views import (
    EstadiaChegadaCreateView, EstadiaSaidaUpdateView, EstadiaDetailView, EstadiaDeleteView, EstadiaListView,
)

urlpatterns = [

    path('estadias/', EstadiaListView.as_view(), name='estadias'),
    path('chegada/', EstadiaChegadaCreateView.as_view(), name='estadia_chegada'),
    path('<int:pk>/saida/', EstadiaSaidaUpdateView.as_view(), name='estadia_saida'),
    path('<int:pk>/detail', EstadiaDetailView.as_view(), name='estadia_detail'),
    path('<int:pk>/apagar/', EstadiaDeleteView.as_view(), name='estadia_apagar'),
]