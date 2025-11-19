from django.urls import path

from pagamentos import views


app_name = 'pagamentos'

urlpatterns = [
    path('', views.PagamentosView.as_view(), name='pagamentos'),

    # controle pagamento
    path('processar/<int:estadia_pk>/', views.ProcessarPagamentoView.as_view(), name='processar_pagamento'),
    path('concluido/<int:pagamento_id>/', views.PagamentoConcluidoDetalhesView.as_view(),name='pagamento_concluido'),
    path('adicionar/', views.PagamentoCreateView.as_view(), name='pagamento_adicionar'),
    path('editar/<int:pk>/', views.PagamentoUpdateView.as_view(), name='pagamento_editar'),
    path('apagar/<int:pk>/', views.PagamentoDeleteView.as_view(), name='pagamento_apagar'),

    # formas pagamento
    path('dinheiro/<int:pagamento_id>/', views.PagamentoDinheiroView.as_view(), name='dinheiro'),
    path('pix/<int:pagamento_id>/', views.PagamentoPixView.as_view(), name='pix'),
    path('credito/<int:pagamento_id>/', views.PagamentoCreditoView.as_view(), name='credito'),
    path('debito/<int:pagamento_id>/', views.PagamentoDebitoView.as_view(), name='debito'),

   path('plano_valido/<int:estadia_id>/', views.SaidaPlanoValidoView.as_view(), name='plano_valido'),

path('relatorio/', views.RelatorioPagamentosView.as_view(), name='relatorio_pagamentos'),
]