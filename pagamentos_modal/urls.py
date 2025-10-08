from django.urls import path
from .views import (ProcessarPagamentoModalView, PagamentoPixModalView, PagamentoCartaoModalView, PagamentoConcluidoModalView)

app_name = 'pagamentos_modal'

urlpatterns = [
    path('<int:estada_modal_pk>/', ProcessarPagamentoModalView.as_view(), name='pagamento_modal_processar'),
    path('<int:pagamento_pk>/pix/', PagamentoPixModalView.as_view(), name='pagamento_modal_pix'),
    path('<int:pagamento_pk>/cartao/', PagamentoCartaoModalView.as_view(), name='pagamento_modal_cartao'),
    path('<int:pagamento_pk>/concluido/', PagamentoConcluidoModalView.as_view(), name='pagamento_modal_concluido'),
]
