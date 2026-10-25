from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('servicos/', include('servicos.urls')),
    path('rh/', include('rh.urls')),
    path('crm/', include('crm.urls')),

    # Rotas dos Apps
    path('cadastros/', include('cadastros.urls')),
    path('financeiro/', include('financeiro.urls')),

    # O App WEB assume a raiz do site
    path('', include('web.urls')),

    path('configuracoes/', views.configuracoes_sistema, name='configuracoes'),
    path('configuracoes/editar/<int:id>/', views.editar_parametro, name='editar_parametro'),

    # Rota /media/ INCONDICIONAL (o helper static() não serve nada com DEBUG=False ->
    # imagens/fotos dariam 404 em produção; correção igual ao padrão dos outros apps)
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]

# Configuração para servir Arquivos em modo DEBUG (static files)
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0] if settings.STATICFILES_DIRS else settings.STATIC_ROOT)