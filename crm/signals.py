from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Lead
from cadastros.models import Cadastro

@receiver(post_save, sender=Lead)
def converter_lead_em_cliente(sender, instance, created, **kwargs):
    """
    Se o negócio for ganho, transforma o Lead em um Cadastro (Cliente) automaticamente.
    """
    if instance.status == 'GANHO':
        # Verifica se já existe um cliente com esse nome na empresa para não duplicar
        existe = Cadastro.objects.filter(
            empresa=instance.empresa, 
            nome=instance.nome_empresa
        ).exists()
        
        if not existe:
            # Cria o cliente novo automaticamente
            Cadastro.objects.create(
                empresa=instance.empresa,
                nome=instance.nome_empresa,        # Nome da empresa/pessoa
                celular=instance.telefone,         # Traz o WhatsApp
                email=instance.email,              # Traz o e-mail
                papel='CLI',                       # Define como Cliente
                situacao='ATIVO',                  # Já entra Ativo
                tipo_pessoa='PJ',                  # Por padrão assume PJ (pode ser editado depois)
                observacoes=f"🌟 Lead convertido com sucesso do CRM! Falar com: {instance.nome_contato}."
            )
            print(f"🎉 Lead {instance.nome_empresa} convertido em Cliente Oficial!")
            
            