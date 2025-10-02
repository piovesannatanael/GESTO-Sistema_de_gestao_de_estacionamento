from django.urls import path
from .views import ProcessarPagamentoView, PagamentoPixView, PagamentoCartaoView, PagamentoConcluidoView

urlpatterns = [
    # A rota principal para iniciar o pagamento. Ela sempre precisa do ID da estada.
    path('<int:estada_pk>/', ProcessarPagamentoView.as_view(), name='pagamento_processar'),

    # Rotas para as etapas seguintes do pagamento, usando o ID do pagamento.
    path('<int:pagamento_pk>/pix/', PagamentoPixView.as_view(), name='pagamento_pix'),
    path('<int:pagamento_pk>/cartao/', PagamentoCartaoView.as_view(), name='pagamento_cartao'),
    path('<int:pagamento_pk>/concluido/', PagamentoConcluidoView.as_view(), name='pagamento_concluido'),
]

