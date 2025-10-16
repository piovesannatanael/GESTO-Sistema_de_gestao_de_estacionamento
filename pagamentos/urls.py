from django.urls import path

from pagamentos.views import PagamentosView, PagamentoCreateView, PagamentoUpdateView, PagamentoDeleteView

urlpatterns = [
    path('pagamentos', PagamentosView.as_view(), name='pagamentos'),
    path('pagamentos/adicionar', PagamentoCreateView.as_view(), name='pagamento_adicionar'),
    path('<int:pk>pagamentos/editar', PagamentoUpdateView.as_view(), name='pagamento_editar'),
    path('<int:pk>pagamentos/apagar', PagamentoDeleteView.as_view(), name='pagamento_apagar'),

]