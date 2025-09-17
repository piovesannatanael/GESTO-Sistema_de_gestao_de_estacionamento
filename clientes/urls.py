from django.urls import path

from .views import ClientesPFView, ClientePFAddView, ClientePFUpdateView, ClientePFDeleteView, ClientesPJView, \
    ClientePJUpdateView, ClientePJAddView, ClientePJDeleteView

urlpatterns = [
    # URLS clientes pessoa fisica
    path('clientespf', ClientesPFView.as_view(), name='clientespf'),
    path('clientepf/adicionar', ClientePFAddView.as_view(), name='clientespf_adicionar'),
    path('<int:pk>/clientepf/editar', ClientePFUpdateView.as_view(), name='clientespf_editar'),
    path('<int:pk>/clientepf/apagar', ClientePFDeleteView.as_view(), name='clientespf_apagar'),

    #URLS clientes pessoa juridica
path('clientespj', ClientesPJView.as_view(), name='clientespj'),
    path('clientepj/adicionar', ClientePJAddView.as_view(), name='clientespj_adicionar'),
    path('<int:pk>/clientepj/editar', ClientePJUpdateView.as_view(), name='clientespj_editar'),
    path('<int:pk>/clientepj/apagar', ClientePJDeleteView.as_view(), name='clientespj_apagar'),

]