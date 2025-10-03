from django.urls import path

from modalidades.views import ModalidadeListView, PagarModalidadeView

# Define um 'namespace' para evitar conflito de nomes de URL com outros apps
app_name = 'modalidades'

urlpatterns = [
    # Rota para a lista de modalidades (ex: /modalidades/)
    path('', ModalidadeListView.as_view(), name='modalidade_list'),

    # Rota para a página de pagamento de uma modalidade específica
    # (ex: /modalidades/3/pagar/)
    path('<int:modalidade_pk>/pagar/', PagarModalidadeView.as_view(), name='pagar_modalidade'),
]
#### Próximo Passo


