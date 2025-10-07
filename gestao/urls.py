
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

admin.site.site_header = "Gestão de Estacionamento"
admin.site.index_title = "GESTO - System Parking"


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    path('', include('clientes.urls')),
    path('', include('funcionarios.urls')),
    path('', include('veiculos.urls')),
    path('', include('vagas.urls')),
    path('', include('estadias.urls')),
    path('', include('pagamentos.urls')),
    path('', include('modalidades.urls')),
    path('', include('pagamentos_modal.urls')),

]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


