from django.urls import path
from django.views.generic import TemplateView

from valores.views import PlanosView, PlanoCreateView, PlanoUpdateView, PlanoDeleteView, DescontosView, \
    DescontoCreateView, DescontoUpdateView, DescontoDeleteView, ExtraView, ExtraCreateView, ExtraUpdateView, \
    ExtraDeleteView, CategoriaView, CategoriaCreateView, CategoriaUpdateView, CategoriaDeleteView

urlpatterns = [
    path('', TemplateView.as_view(template_name='valores.html'), name='valores'),

    path('planos/', PlanosView.as_view(), name='planos'),
    path('planos/adicionar/', PlanoCreateView.as_view(), name='plano_adicionar'),
    path('planos/editar/<int:pk>/', PlanoUpdateView.as_view(), name='plano_editar'),
    path('planos/apagar/<int:pk>/', PlanoDeleteView.as_view(), name='plano_apagar'),

    path('descontos/', DescontosView.as_view(), name='descontos'),
    path('descontos/adicionar/', DescontoCreateView.as_view(), name='desconto_adicionar'),
    path('descontos/editar/<int:pk>/', DescontoUpdateView.as_view(), name='desconto_editar'),
    path('descontos/apagar/<int:pk>/', DescontoDeleteView.as_view(), name='desconto_apagar'),

    path('extras/', ExtraView.as_view(), name='extras'),
    path('extras/adicionar/', ExtraCreateView.as_view(), name='extra_adicionar'),
    path('extras/editar/<int:pk>/', ExtraUpdateView.as_view(), name='extra_editar'),
    path('extras/apagar/<int:pk>/', ExtraDeleteView.as_view(), name='extra_apagar'),

    path('categorias/', CategoriaView.as_view(), name='categorias'),
    path('categorias/adicionar/', CategoriaCreateView.as_view(), name='categoria_adicionar'),
    path('categorias/editar/<int:pk>/', CategoriaUpdateView.as_view(), name='categoria_editar'),
    path('categorias/apagar/<int:pk>/', CategoriaDeleteView.as_view(), name='categoria_apagar'),

]



