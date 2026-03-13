from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Pedido
from financeiro.models import Conta, PlanoDeContas
from core.models import ParametroSistema # Importa o seu modelo de parâmetro

@receiver(post_save, sender=Pedido)
def gerar_conta_financeira(sender, instance, created, **kwargs):
    if instance.status == 'FATURADO':
        descricao_padrao = f"Ref. Pedido de Serviço #{instance.id}"
        
        # Verifica se já gerou para não duplicar
        existe = Conta.objects.filter(
            empresa=instance.empresa,
            descricao__contains=f"Pedido de Serviço #{instance.id}"
        ).exists()
        
        if not existe:
            plano_selecionado = None
            
            # --- 1. LÊ O PARÂMETRO DO SISTEMA ---
            parametro = ParametroSistema.objects.filter(
                empresa=instance.empresa, 
                chave='PLANO_CONTAS_SERVICOS_ID'
            ).first()

            # Se achou o parâmetro e ele tem um valor numérico válido
            if parametro and parametro.valor and parametro.valor.isdigit():
                try:
                    # Tenta buscar o plano de contas com esse ID exato
                    plano_selecionado = PlanoDeContas.objects.get(
                        id=int(parametro.valor), 
                        empresa=instance.empresa
                    )
                except PlanoDeContas.DoesNotExist:
                    print("⚠️ Parâmetro aponta para um ID inexistente.")
                    plano_selecionado = None

            # --- 2. PLANO B (FALLBACK) ---
            if not plano_selecionado:
                print("⚠️ Usando Plano de Contas padrão de contingência.")
                plano_selecionado, _ = PlanoDeContas.objects.get_or_create(
                    empresa=instance.empresa,
                    codigo="1.01", 
                    defaults={'nome': 'Receita com Serviços (Padrão)', 'tipo': 'R'}
                )

            # --- 3. CRIA A CONTA A RECEBER ---
            Conta.objects.create(
                empresa=instance.empresa,
                descricao=descricao_padrao,
                plano_de_contas=plano_selecionado,
                cadastro=instance.cliente,
                valor=instance.valor_total,
                data_vencimento=instance.data_solicitacao,
                status='PENDENTE',
                documento=f"PED-{instance.id}",
                observacoes="Gerado via Integração Automática de Serviços."
            )
            print(f"💰 Conta gerada usando o plano: {plano_selecionado.nome}")