from django.urls import path
from .views import PagarModalidadeView

app_name = 'pagamentos_modal' # Define um namespace para as URLs deste app

urlpatterns = [
    # Rota para a página de pagamento de uma modalidade específica
    path('<int:modalidade_pk>/', PagarModalidadeView.as_view(), name='pagar_modalidade'),
]
