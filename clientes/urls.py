from django.urls import path
from .views import (
    ClientePFAddView, ClientePFUpdateView, ClientePFDeleteView,
    ClientePJAddView, ClientePJUpdateView, ClientePJDeleteView,
    ClientesView,  # aqui ClientesView é uma função
)

urlpatterns = [
    path('clientes', ClientesView, name='clientes'),

        #CLiente pf
    path('pf/adicionar/', ClientePFAddView.as_view(), name='pf_adicionar'),
    path('pf/<int:pk>/editar/', ClientePFUpdateView.as_view(), name='pf_editar'),
    path('pf/<int:pk>/apagar/', ClientePFDeleteView.as_view(), name='pf_apagar'),
        #cliente pj
    path('pj/adicionar/', ClientePJAddView.as_view(), name='pj_adicionar'),
    path('pj/<int:pk>/editar/', ClientePJUpdateView.as_view(), name='pj_editar'),
    path('pj/<int:pk>/apagar/', ClientePJDeleteView.as_view(), name='pj_apagar'),
]

'''from django.urls import path

from clientes.views import ClientesView, ClienteAddView, ClienteDeleteView, ClienteUpdateView

from .views import ClientePFAddView, ClientePFUpdateView, ClientePFDeleteView, \
    ClientePJUpdateView, ClientePJAddView, ClientePJDeleteView, ClientesView

urlpatterns = [
    path('clientes/', ClientesView.as_view(), name='clientes'),

    # URLS clientes pessoa fisica
    path('clientepf/adicionar', ClientePFAddView.as_view(), name='clientespf_adicionar'),
    path('<int:pk>/clientepf/editar', ClientePFUpdateView.as_view(), name='clientespf_editar'),
    path('<int:pk>/clientepf/apagar', ClientePFDeleteView.as_view(), name='clientespf_apagar'),

    #URLS clientes pessoa juridica
    path('clientepj/adicionar', ClientePJAddView.as_view(), name='clientespj_adicionar'),
    path('<int:pk>/clientepj/editar', ClientePJUpdateView.as_view(), name='clientespj_editar'),
    path('<int:pk>/clientepj/apagar', ClientePJDeleteView.as_view(), name='clientespj_apagar'),
]
'''
