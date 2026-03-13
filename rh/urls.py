from django.urls import path
from . import views

app_name = 'rh'

urlpatterns = [
    # Rotas de Cargos
    path('cargos/', views.lista_cargos, name='lista_cargos'),
    path('cargos/novo/', views.gerenciar_cargo, name='novo_cargo'),
    path('cargos/editar/<int:pk>/', views.gerenciar_cargo, name='editar_cargo'),
    path('cargos/excluir/<int:pk>/', views.excluir_cargo, name='excluir_cargo'),
    
    # Rotas de Funcionários
    path('funcionarios/', views.lista_funcionarios, name='lista_funcionarios'),
    path('funcionarios/novo/', views.gerenciar_funcionario, name='novo_funcionario'),
    path('funcionarios/editar/<int:pk>/', views.gerenciar_funcionario, name='editar_funcionario'),
    path('funcionarios/excluir/<int:pk>/', views.excluir_funcionario, name='excluir_funcionario'),
]