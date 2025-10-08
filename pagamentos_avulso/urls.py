from django.urls import path
from .views import ProcessarPagamentoView, PagamentoPixView, PagamentoCartaoView, PagamentoConcluidoView

app_name = 'pagamentos_avulso'

urlpatterns = [
    path('<int:estada_avulso_pk>/', ProcessarPagamentoView.as_view(), name='pagamento_avulso'),
    path('<int:pagamento_pk>/pix/', PagamentoPixView.as_view(), name='pagamento_pix'),
    path('<int:pagamento_pk>/cartao/', PagamentoCartaoView.as_view(), name='pagamento_cartao'),
    path('<int:pagamento_pk>/concluido/', PagamentoConcluidoView.as_view(), name='pagamento_concluido'),
]

