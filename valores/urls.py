from django.urls import path
from django.views.generic import TemplateView

from valores.views import PlanosView, PlanoCreateView, PlanoUpdateView, PlanoDeleteView

urlpatterns = [
    path('', TemplateView.as_view(template_name='valores.html'), name='valores'),

    path('planos/', PlanosView.as_view(), name='planos'),
    path('planos/adicionar/', PlanoCreateView.as_view(), name='plano_adicionar'),
    path('planos/editar/<int:pk>/', PlanoUpdateView.as_view(), name='plano_editar'),
    path('planos/apagar/<int:pk>/', PlanoDeleteView.as_view(), name='plano_apagar'),

    # path('descontos/', RegraDeDescontoListView.as_view(), name='descontos'),
    # path('descontos/adicionar/', RegraDeDescontoCreateView.as_view(), name='desconto_adicionar'),
    # path('descontos/editar/<int:pk>/', RegraDeDescontoUpdateView.as_view(), name='desconto_editar'),
    # path('descontos/apagar/<int:pk>/', RegraDeDescontoDeleteView.as_view(), name='desconto_apagar'),
]