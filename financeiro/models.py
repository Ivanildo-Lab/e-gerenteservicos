from django.db import models
from core.models import ModeloSaaS
from cadastros.models import Cadastro
from django.core.exceptions import ValidationError 
from decimal import Decimal, ROUND_HALF_UP, InvalidOperation
from datetime import date
from django.utils.dateparse import parse_date

def get_taxa_juros_mensal(empresa):
    """
    Busca ParametroSistema chave TAXA_JUROS_MENSAL por empresa.
    Retorna Decimal (default 2.0), tratando vírgula.
    """
    try:
        from core.models import ParametroSistema
        param = ParametroSistema.objects.filter(empresa=empresa, chave='TAXA_JUROS_MENSAL').first()
        if param and param.valor:
            raw = str(param.valor).strip().replace(',', '.')
            try:
                taxa = Decimal(raw)
                return taxa
            except (InvalidOperation, ValueError, AttributeError):
                return Decimal('2.0')
    except Exception:
        pass
    return Decimal('2.0')

class PlanoDeContas(ModeloSaaS):
    TIPO_CHOICES = [
        ('R', 'Receita'),
        ('D', 'Despesa'),
    ]
    
    nome = models.CharField(max_length=100)
    tipo = models.CharField(max_length=1, choices=TIPO_CHOICES)
    codigo = models.CharField(max_length=20, blank=True, help_text="Ex: 1.01")
    
    def __str__(self):
        return f"{self.codigo} - {self.nome}" if self.codigo else self.nome

    class Meta:
        verbose_name = "Plano de Contas"
        verbose_name_plural = "Planos de Contas"
        ordering = ['codigo', 'nome']
        unique_together = [['empresa', 'codigo']]


class Caixa(ModeloSaaS):
    """Representa contas bancárias ou caixas físicos"""
    nome = models.CharField(max_length=100)
    saldo_inicial = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    
    def __str__(self):
        return self.nome

class Conta(ModeloSaaS):
    """Contas a Pagar e Receber (Previsão/Agendamento)"""
    STATUS_CHOICES =[
        ('PENDENTE', 'Pendente'),
        ('PAGA', 'Paga / Recebida'),
        ('CANCELADA', 'Cancelada'),
    ]

    # --- NOVA OPÇÃO: QUEM É O FAVORECIDO? ---
    TIPO_FAVORECIDO_CHOICES =[
        ('CADASTRO', 'Cliente / Fornecedor'),
        ('FUNCIONARIO', 'Funcionário (Folha / Adiantamento)'),
        ('SIMPLES', 'Simples Nacional'),
    ]

    tipo_favorecido = models.CharField(max_length=15, choices=TIPO_FAVORECIDO_CHOICES, default='CADASTRO', verbose_name="Tipo de Favorecido")
    
    descricao = models.CharField(max_length=255, verbose_name="Descrição")
    plano_de_contas = models.ForeignKey('PlanoDeContas', on_delete=models.PROTECT, verbose_name="Plano de Contas")
    
    # Campo antigo (Agora aceita ficar em branco se for funcionário)
    cadastro = models.ForeignKey(Cadastro, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Cliente/Fornecedor")
    
    funcionario = models.ForeignKey('rh.Funcionario', on_delete=models.PROTECT, verbose_name="Funcionário", null=True, blank=True, related_name='contas_financeiras')    
    valor = models.DecimalField(max_digits=12, decimal_places=2)
    data_vencimento = models.DateField(verbose_name="Vencimento")
    
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDENTE')
    documento = models.CharField(max_length=50, blank=True, null=True, verbose_name="Nº Doc / Parcela")

    observacoes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    arquivo = models.FileField(upload_to='financeiro/contas/', blank=True, null=True, verbose_name="Anexo / Comprovante")

    # --- VALIDAÇÃO INTELIGENTE ---
    def clean(self):
        if self.tipo_favorecido == 'CADASTRO' and not self.cadastro:
            raise ValidationError({'cadastro': 'Você escolheu Cliente/Fornecedor. Por favor, selecione-o na lista.'})
        
        if self.tipo_favorecido == 'FUNCIONARIO' and not self.funcionario:
            raise ValidationError({'funcionario': 'Você escolheu Funcionário. Por favor, selecione-o na lista.'})
        
        # Limpa o campo que não está sendo usado para não sujar o banco de dados
        if self.tipo_favorecido == 'CADASTRO':
            self.funcionario = None
        elif self.tipo_favorecido == 'FUNCIONARIO':
            self.cadastro = None

    @property
    def valor_restante(self):
        # Compatibilidade: se houver valor_pago field, usa; senão considera status
        try:
            # tenta verificar se modelo tem valor_pago attribute de BD
            vp = getattr(self, 'valor_pago', None)
            if vp is not None:
                return self.valor - vp
        except Exception:
            pass
        if self.status == 'PAGA':
            return Decimal('0.00')
        return self.valor

    @property
    def data_pagamento(self):
        # tenta buscar lancamento associado
        try:
            # pode ser OneToOne (lancamento_caixa) ou FK (lancamentos_vinculados)
            if hasattr(self, 'lancamento_caixa') and self.lancamento_caixa:
                return self.lancamento_caixa.data_lancamento
            if hasattr(self, 'lancamentos_vinculados'):
                ultimo = self.lancamentos_vinculados.order_by('-data_lancamento').first()
                return ultimo.data_lancamento if ultimo else None
        except Exception:
            pass
        return None

    def dias_atraso(self, data_ref=None):
        if self.status in ('PAGA', 'CANCELADA'):
            return 0
        if data_ref is None:
            data_ref = date.today()
        elif isinstance(data_ref, str):
            try:
                parsed = parse_date(data_ref)
                if parsed:
                    data_ref = parsed
                else:
                    from datetime import datetime
                    try:
                        data_ref = datetime.strptime(data_ref, '%Y-%m-%d').date()
                    except Exception:
                        data_ref = date.today()
            except Exception:
                data_ref = date.today()
        if hasattr(data_ref, 'date') and not isinstance(data_ref, date):
            try:
                data_ref = data_ref.date()
            except Exception:
                pass
        if not isinstance(data_ref, date):
            return 0
        if self.data_vencimento >= data_ref:
            return 0
        delta = (data_ref - self.data_vencimento).days
        return delta if delta > 0 else 0

    def calcular_juros(self, taxa_mensal, data_ref=None):
        dias = self.dias_atraso(data_ref)
        if dias <= 0:
            return Decimal('0.00')
        try:
            taxa = Decimal(str(taxa_mensal).replace(',', '.').strip())
        except (InvalidOperation, ValueError, AttributeError):
            taxa = Decimal('2.0')
        try:
            base = Decimal(str(self.valor_restante))
        except Exception:
            base = Decimal('0.00')
        if base <= 0:
            return Decimal('0.00')
        juros = base * (taxa / Decimal('100')) * (Decimal(dias) / Decimal('30'))
        return juros.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

    def total_com_juros(self, taxa_mensal, data_ref=None):
        juros = self.calcular_juros(taxa_mensal, data_ref)
        total = Decimal(str(self.valor_restante)) + juros
        return total.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

    def __str__(self):
        return f"{self.descricao} - {self.data_vencimento}"

class Lancamento(ModeloSaaS):
    """
    FLUXO DE CAIXA REAL.
    """
   
    TIPO_CHOICES = [
        ('C', 'Receita (Crédito-Entrada)'),
        ('D', 'Despesa (Débito-Saída)'),
    ]

    caixa = models.ForeignKey(Caixa, on_delete=models.PROTECT, verbose_name="Conta Bancária/Caixa")
    plano_de_contas = models.ForeignKey(PlanoDeContas, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Se veio de uma conta a pagar/receber, vinculamos aqui
    conta_origem = models.OneToOneField(Conta, on_delete=models.SET_NULL, null=True, blank=True, related_name="lancamento_caixa")
    
    # ATENÇÃO: O nome do campo é 'data_lancamento'
    data_lancamento = models.DateField(verbose_name="Data do Movimento")
    
    descricao = models.CharField(max_length=255)
    valor = models.DecimalField(max_digits=12, decimal_places=2)
    tipo = models.CharField(max_length=1, choices=TIPO_CHOICES)

    def save(self, *args, **kwargs):
        # Garante que despesas (D) sejam negativas e Receitas (C) positivas
        if self.tipo == 'D' and self.valor > 0:
            self.valor = self.valor * -1
        elif self.tipo == 'C' and self.valor < 0:
            self.valor = self.valor * -1
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.data_lancamento} - {self.descricao} ({self.valor})"

    class Meta:
        ordering = ['-data_lancamento']
