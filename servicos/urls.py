from django.urls import path
from . import views

app_name = 'servicos'

urlpatterns = [
    path('pedidos/', views.lista_pedidos, name='lista_pedidos'),
    path('pedidos/novo/', views.novo_pedido, name='novo_pedido'),
    path('pedido/<int:pedido_id>/imprimir/', views.imprimir_nota_servico, name='imprimir_nota_servico'),
    path('pedidos/editar/<int:pk>/', views.novo_pedido, name='editar_pedido'),
    path('catalogo/', views.lista_catalogo, name='lista_catalogo'),
    path('catalogo/novo/', views.novo_servico, name='novo_servico'),
]