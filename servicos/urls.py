from django.urls import path
from . import views

app_name = 'servicos'

urlpatterns =[
    # --- CATÁLOGO DE SERVIÇOS ---
    path('catalogo/', views.lista_catalogo, name='lista_catalogo'),
    
    # IMPORTANTE: Note que o 'novo' e o 'editar' agora apontam para a mesma view: gerenciar_servico
    path('catalogo/novo/', views.gerenciar_servico, name='novo_servico'),
    path('catalogo/editar/<int:pk>/', views.gerenciar_servico, name='editar_servico'),
    path('catalogo/excluir/<int:pk>/', views.excluir_servico, name='excluir_servico'),
    
    # --- PEDIDOS / ORDENS DE SERVIÇO ---
    path('pedidos/', views.lista_pedidos, name='lista_pedidos'),
    path('pedidos/novo/', views.novo_pedido, name='novo_pedido'),
    path('pedidos/editar/<int:pk>/', views.novo_pedido, name='editar_pedido'),
    path('pedidos/excluir/<int:pk>/', views.excluir_pedido, name='excluir_pedido'),
    
    # --- IMPRESSÃO ---
    path('pedido/<int:pedido_id>/imprimir/', views.imprimir_nota_servico, name='imprimir_nota_servico'),
]