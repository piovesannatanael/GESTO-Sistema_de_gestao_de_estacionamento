from django.urls import path

from veiculos.views import VeiculosView, VeiculoAddView, VeiculoUpdateView, VeiculoDeleteView

urlpatterns = [
    path('veiculos', VeiculosView.as_view(), name='veiculos'),
    path('veiculos/adicionar', VeiculoAddView.as_view(), name='veiculo_adicionar'),
    path('<int:pk>veiculos/editar', VeiculoUpdateView.as_view(), name='veiculo_editar'),
    path('<int:pk>veiculos/apagar', VeiculoDeleteView.as_view(), name='veiculo_apagar'),
]