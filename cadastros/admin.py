from django.contrib import admin
from .models import CategoriaCliente, Cadastro

@admin.register(CategoriaCliente)
class CategoriaClienteAdmin(admin.ModelAdmin):
    list_display = ('nome', 'empresa')
    list_filter = ('empresa',)
    search_fields = ('nome',)

@admin.register(Cadastro)
class CadastroAdmin(admin.ModelAdmin):
    list_display = ('nome', 'papel', 'tipo_pessoa', 'cpf', 'cnpj', 'celular', 'situacao')
    list_filter = ('empresa', 'situacao', 'papel', 'tipo_pessoa', 'categoria')
    
    # IMPORTANTE: Busca atualizada para os novos campos
    search_fields = ('nome', 'razao_social', 'cpf', 'cnpj')
    
    fieldsets = (
        ('Classificação', {
            'fields': (
                ('empresa', 'situacao'),
                ('papel', 'categoria'),
                'tipo_pessoa',
            )
        }),
        ('Pessoa Física', {
            'fields': (
                ('nome', 'cpf'),
                ('rg', 'data_nascimento'),
                'foto',
            ),
            # Oculta essa seção via CSS/JS no futuro se for PJ, por enquanto mostra tudo
        }),
        ('Pessoa Jurídica', {
            'fields': (
                ('razao_social', 'cnpj'),
                ('inscricao_estadual', 'is_produtor_rural'),
            ),
        }),
        ('Contato', {
            'fields': (
                ('email', 'celular', 'telefone_fixo'),
            )
        }),
        ('Endereço Completo', {
            'fields': (
                ('cep', 'logradouro', 'numero'),
                ('complemento', 'bairro'),
                ('cidade', 'uf'),
            )
        }),
        ('Outros', {
            'fields': ('observacoes',),
            'classes': ('collapse',),
        }),
    )

    def save_model(self, request, obj, form, change):
        if not obj.empresa_id and hasattr(request.user, 'funcionario'):
             obj.empresa = request.user.funcionario.empresa
        super().save_model(request, obj, form, change)