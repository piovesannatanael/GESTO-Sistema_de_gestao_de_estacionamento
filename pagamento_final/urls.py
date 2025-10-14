
from django.urls import path

from pagamento_final.views import PagamentoPixView, PagamentoCreditoView, PagamentoDebitoView, PagamentoConcluidoView, \
    PagamentoDinheiroView

app_name = 'pagamento_final'

urlpatterns = [

    path('pix/<int:estadia_pk>/', PagamentoPixView.as_view(), name='pagamento_pix'),
    path('credito/<int:estadia_pk>/', PagamentoCreditoView.as_view(), name='pagamento_credito'),
    path('debito/<int:estadia_pk>/', PagamentoDebitoView.as_view(), name='pagamento_debito'),
    path('dinheiro/<int:estadia_pk>/', PagamentoDinheiroView.as_view(), name='pagamento_dinheiro'),

    path('concluido/<int:estadia_pk>/', PagamentoConcluidoView.as_view(), name='pagamento_concluido'),
]