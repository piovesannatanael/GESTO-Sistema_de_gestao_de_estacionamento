from django.urls import path
from .views import ProcessarPagamentoModalView, PagamentoPixView, PagamentoCartaoView, PagamentoConcluidoView

urlpatterns = [
    path('<int:estada_pk>/', ProcessarPagamentoModalView.as_view(), name='pagamento_modal'),
    path('<int:pagamento_pk>/pix/', PagamentoPixView.as_view(), name='pagamento_pix'),
    path('<int:pagamento_pk>/cartao/', PagamentoCartaoView.as_view(), name='pagamento_cartao'),
    path('<int:pagamento_pk>/concluido/', PagamentoConcluidoView.as_view(), name='pagamento_concluido'),
]