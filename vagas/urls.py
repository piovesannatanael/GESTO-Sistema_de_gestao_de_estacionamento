# vagas/urls.py

from django.urls import path
from vagas.views import VagasView, VagaAddView, VagaUpdateView, VagaDeleteView

urlpatterns = [
    path('vagas', VagasView.as_view(), name='vagas'),
    path('vaga/adicionar', VagaAddView.as_view(), name='vaga_adicionar'),
    path('<int:pk>/editar', VagaUpdateView.as_view(), name='vaga_editar'),
    path('<int:pk>/apagar', VagaDeleteView.as_view(), name='vaga_apagar'),
]