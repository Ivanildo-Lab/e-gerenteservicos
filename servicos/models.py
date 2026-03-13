from django.db import models
from django.db.models import Q
from django.utils import timezone
from core.models import Empresa 

# Importação correta baseada no seu código
from cadastros.models import Cadastro 
from rh.models import Funcionario

class TipoServico(models.Model):
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    nome = models.CharField(max_length=100, verbose_name="Nome do Serviço")
    descricao = models.TextField(blank=True, null=True)
    valor_base = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Valor Base (R$)")
    unidade = models.CharField(max_length=20, default='HORA', choices=[('HORA', 'Por Hora'), ('DIA', 'Diária'), ('MES', 'Mensal')])

    def __str__(self):
        return f"{self.nome} (R$ {self.valor_base}/{self.unidade})"

    class Meta:
        verbose_name = "Catálogo de Serviço"
        verbose_name_plural = "Catálogo de Serviços"
        unique_together = ['empresa', 'nome']


class Pedido(models.Model):
    STATUS_CHOICES = [
        ('ORCAMENTO', 'Orçamento'),
        ('APROVADO', 'Aprovado / A Executar'),
        ('CONCLUIDO', 'Concluído'),
        ('CANCELADO', 'Cancelado'),
        ('FATURADO', 'Faturado (Nota Emitida)'),
    ]

    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    
    # --- MUDANÇA AQUI: Aponta para Cadastro ---
    cliente = models.ForeignKey(
        Cadastro, 
        on_delete=models.PROTECT, 
        verbose_name="Cliente Solicitante",
        # Filtra no banco: Só aceita se for Cliente ou Ambos, e se estiver Ativo
        limit_choices_to=Q(situacao='ATIVO') & (Q(papel='CLI') | Q(papel='AMB'))
    )

    data_solicitacao = models.DateField(default=timezone.now, verbose_name="Data do Pedido")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ORCAMENTO')
    observacoes = models.TextField(blank=True, null=True, verbose_name="Observações do Pedido")
    
    valor_total = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, editable=False)

    def atualizar_total(self):
        total = sum(item.valor_total_item for item in self.alocacoes.all())
        self.valor_total = total
        self.save()

    def __str__(self):
        return f"Pedido #{self.id} - {self.cliente.nome} ({self.get_status_display()})"

    class Meta:
        verbose_name = "Pedido de Serviço"
        verbose_name_plural = "Pedidos de Serviços"


class Alocacao(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='alocacoes')
    servico = models.ForeignKey(TipoServico, on_delete=models.PROTECT, verbose_name="Serviço a Executar")
    funcionario = models.ForeignKey(Funcionario, on_delete=models.PROTECT, verbose_name="Profissional Alocado")
    
    data_inicio = models.DateTimeField(verbose_name="Início Previsto")
    data_fim = models.DateTimeField(verbose_name="Fim Previsto")
    
    valor_unitario = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Valor Cobrado")
    quantidade = models.DecimalField(max_digits=5, decimal_places=2, default=1, verbose_name="Qtd (Horas/Dias)")
    valor_total_item = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    
    realizado = models.BooleanField(default=False, verbose_name="Serviço Realizado?")

    def save(self, *args, **kwargs):
        if not self.valor_unitario and self.servico:
            self.valor_unitario = self.servico.valor_base
        
        self.valor_total_item = self.valor_unitario * self.quantidade
        super().save(*args, **kwargs)
        self.pedido.atualizar_total()

    def __str__(self):
        return f"{self.funcionario} - {self.servico}"

    class Meta:
        verbose_name = "Alocação de Profissional"
        verbose_name_plural = "Alocações"
        