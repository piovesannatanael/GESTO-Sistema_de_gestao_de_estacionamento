from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

admin.site.site_header = "Gestão de Estacionamento"
admin.site.index_title = "GESTO - System Parking"

urlpatterns = [
      path('admin/', admin.site.urls),
      path('', include('home.urls')),
      path('clientes/', include('clientes.urls')),
      path('funcionarios/', include('funcionarios.urls')),
      path('veiculos/', include('veiculos.urls')),
      path('vagas/', include('vagas.urls')),
      path('estadias/', include('estadias.urls')),
      # path('modalidades/', include('modalidades.urls')),
      path('pagamento/avulso/', include('pagamentos_avulso.urls')),
      path('pagamento/modal/', include('pagamentos_modal.urls')),
      path('valores/', include('valores.urls')),
      path('pagamento/final/', include('pagamento_final.urls')),


              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
