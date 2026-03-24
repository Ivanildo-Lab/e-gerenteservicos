from django.db import models
from django.utils import timezone
from core.models import Empresa
from rh.models import Funcionario # O vendedor/atendente que vai fazer a visita

class Lead(models.Model):
    STATUS_CHOICES =[
        ('NOVO', 'Novo Lead (Não contatado)'),
        ('CONTATO', 'Em Contato / Qualificação'),
        ('AGENDADO', 'Visita ou Reunião Agendada'),
        ('PROPOSTA', 'Proposta Enviada'),
        ('GANHO', 'Negócio Fechado (Ganho)'),
        ('PERDIDO', 'Negócio Perdido'),
    ]

    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    
    # Pré-Cadastro Rápido
    nome_empresa = models.CharField(max_length=200, verbose_name="Nome da Empresa / Negócio")
    nome_contato = models.CharField(max_length=100, verbose_name="Pessoa de Contato")
    telefone = models.CharField(max_length=20, verbose_name="WhatsApp / Celular")
    email = models.EmailField(blank=True, null=True)
    
    origem = models.CharField(max_length=50, blank=True, null=True, help_text="Ex: Instagram, Indicação, Google")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='NOVO')
    
    # Campo para anotar o motivo se o negócio for perdido
    motivo_perda = models.TextField(blank=True, null=True, verbose_name="Motivo da Perda")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.nome_empresa} ({self.nome_contato})"

    class Meta:
        verbose_name = "Lead / Prospecto"
        verbose_name_plural = "Leads"
        ordering = ['-created_at']


class Interacao(models.Model):
    """
    Agenda de contatos, visitas e ligações com o Lead.
    """
    TIPO_CHOICES =[
        ('LIGACAO', 'Ligação Telefônica'),
        ('WHATSAPP', 'Mensagem (WhatsApp)'),
        ('EMAIL', 'E-mail'),
        ('VISITA', 'Visita Presencial'),
        ('REUNIAO', 'Reunião Online'),
    ]

    lead = models.ForeignKey(Lead, on_delete=models.CASCADE, related_name='interacoes')
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    
    # Quem vai fazer a visita/ligação
    responsavel = models.ForeignKey(Funcionario, on_delete=models.PROTECT, verbose_name="Responsável")
    
    data_agendada = models.DateTimeField(verbose_name="Data e Hora do Contato")
    descricao = models.TextField(verbose_name="Assunto / Notas da Reunião")
    
    realizada = models.BooleanField(default=False, verbose_name="Concluída?")

    def __str__(self):
        return f"{self.get_tipo_display()} com {self.lead.nome_empresa}"

    class Meta:
        verbose_name = "Interação / Agendamento"
        verbose_name_plural = "Agenda do CRM"
        ordering = ['data_agendada']
        