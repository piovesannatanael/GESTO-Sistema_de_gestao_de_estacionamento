from django.urls import path

from pagamentos_avulso.views import ProcessarPagamentoAvulsoView

app_name = 'pagamentos_avulso'

urlpatterns = [
    path('processar/<int:estada_avulso_pk>/', ProcessarPagamentoAvulsoView.as_view(),name='processar_pagamento_avulso'),

]

