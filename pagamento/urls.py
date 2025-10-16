from django.urls import path

from pagamento.views import PagamentosView, PagamentoCreateView, PagamentoUpdateView, PagamentoDeleteView

urlpatterns = [
    path('pagamento', PagamentosView.as_view(), name='pagamentos'),
    path('pagamento/adicionar', PagamentoCreateView.as_view(), name='pagamento_adicionar'),
    path('<int:pk>pagamento/editar', PagamentoUpdateView.as_view(), name='pagamento_editar'),
    path('<int:pk>pagamento/apagar', PagamentoDeleteView.as_view(), name='pagamento_apagar'),

]