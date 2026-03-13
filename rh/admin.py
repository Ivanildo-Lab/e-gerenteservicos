from django.contrib import admin
from .models import Cargo, Funcionario

@admin.register(Cargo)
class CargoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'cbo', 'salario_base')
    search_fields = ('titulo', 'cbo')
    list_filter = ('empresa',) 

@admin.register(Funcionario)
class FuncionarioAdmin(admin.ModelAdmin):
    list_display = ('nome_completo', 'cargo', 'situacao', 'telefone_celular', 'cidade', 'uf')
    list_filter = ('situacao', 'cargo', 'tipo_contrato', 'uf')
    list_filter = ('empresa', 'situacao', 'cargo')
    search_fields = ('nome_completo', 'cpf', 'rg', 'pis')

    fieldsets = (
        ('Vínculo Empresarial', {
            'fields': ('empresa',)
        }),

        ('Dados Pessoais', {
            'fields': (
                ('nome_completo', 'foto'),
                ('data_nascimento', 'estado_civil'),
                ('nacionalidade', 'naturalidade'),
                ('nome_mae', 'nome_pai'),
            )
        }),
        ('Documentação', {
            'fields': (
                ('cpf', 'rg', 'rg_orgao'),
                'pis',
                ('ctps_numero', 'ctps_serie', 'ctps_uf'),
                ('cnh_numero', 'cnh_categoria', 'cnh_validade'),
            )
        }),
        ('Endereço e Contato', {
            'fields': (
                ('cep', 'logradouro', 'numero'),
                ('complemento', 'bairro'),
                ('cidade', 'uf'),
                ('telefone_celular', 'telefone_fixo', 'email'),
            )
        }),
        ('Contrato de Trabalho', {
            'fields': (
                ('cargo', 'tipo_contrato'),
                ('data_admissao', 'situacao'),
                ('horario_trabalho', 'salario_contratual'),
            )
        }),
        ('Dados Bancários', {
            'fields': (
                ('banco', 'agencia', 'conta'),
                'pix',
            )
        }),
    )