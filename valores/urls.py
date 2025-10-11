from django.urls import path
from valores.views import ValoresView

urlpatterns = [
    path('valores', ValoresView.as_view(), name='valores'),
    path('valores/adicionar', ValoresAddView.as_view(), name='valores_adicionar'),
    path('<int:pk>/valores/editar', ValoresUpdateView.as_view(), name='valores_editar'),
    path('<int:pk>/valores/apagar', ValoresDeleteView.as_view(), name='valores_apagar'),
]