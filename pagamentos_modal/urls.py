from django.urls import path

from pagamentos_modal.views import ProcessarPagamentoModalView

app_name = 'pagamentos_modal'

urlpatterns = [
    path(
        'processar/<int:estada_modal_pk>/',ProcessarPagamentoModalView.as_view(),name='processar_pagamento_modal'),
]
