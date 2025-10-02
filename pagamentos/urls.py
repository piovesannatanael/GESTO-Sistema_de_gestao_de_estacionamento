from django.urls import path
from .views import ProcessarPagamentoView, PagamentoPixView, PagamentoCartaoView, PagamentoConcluidoView

urlpatterns = [
    path('', ProcessarPagamentoView.as_view(), name='pagamentos'),
    path('<int:estada_pk>/', ProcessarPagamentoView.as_view(), name='pagamento_processar'),
    path('<int:pagamento_pk>/pix/', PagamentoPixView.as_view(), name='pagamento_pix'),
    path('<int:pagamento_pk>/cartao/', PagamentoCartaoView.as_view(), name='pagamento_cartao'),
    path('<int:pagamento_pk>/concluido/', PagamentoConcluidoView.as_view(), name='pagamento_concluido'),
]
