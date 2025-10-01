# clientes/urls.py
from django.urls import path
from .views import (
    ClienteListView,
    ClienteCreateView,
    ClienteUpdateView,
    ClienteDeleteView
)

urlpatterns = [
    path('clientes/', ClienteListView.as_view(), name='cliente_list'),
    path('cliente/adicionar/', ClienteCreateView.as_view(), name='cliente_add'),
    path('cliente/<int:pk>/editar/', ClienteUpdateView.as_view(), name='cliente_edit'),
    path('cliente/<int:pk>/apagar/', ClienteDeleteView.as_view(), name='cliente_delete'),
]
#
#
#
# from .views import ClientesView, ClientePFAddView, ClientePFUpdateView, ClientePFDeleteView, ClientePJAddView, \
#     ClientePJUpdateView, ClientePJDeleteView
#
# urlpatterns = [
#     path('clientes/', ClientesView.as_view(), name='clientes'),
#
#     # URLS clientes pessoa fisica
#     path('clientepf/adicionar', ClientePFAddView.as_view(), name='pf_adicionar'),
#     path('<int:pk>/clientepf/editar', ClientePFUpdateView.as_view(), name='pf_editar'),
#     path('<int:pk>/clientepf/apagar', ClientePFDeleteView.as_view(), name='pf_apagar'),
#
#     #URLS clientes pessoa juridica
#     path('clientepj/adicionar', ClientePJAddView.as_view(), name='pj_adicionar'),
#     path('<int:pk>/clientepj/editar', ClientePJUpdateView.as_view(), name='pj_editar'),
#     path('<int:pk>/clientepj/apagar', ClientePJDeleteView.as_view(), name='pj_apagar'),
# ]

