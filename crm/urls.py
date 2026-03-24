from django.urls import path
from . import views

app_name = 'crm'

urlpatterns =[
    path('leads/', views.lista_leads, name='lista_leads'),
    path('leads/novo/', views.gerenciar_lead, name='novo_lead'),
    path('leads/editar/<int:pk>/', views.gerenciar_lead, name='editar_lead'),
]