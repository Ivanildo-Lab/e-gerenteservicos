from django.contrib import admin
from .models import PlanoDeContas, Caixa, Conta, Lancamento
from cadastros.models import Cadastro

# Classe base para aplicar o filtro SaaS em todos os admins do Financeiro
class FinanceiroSaaSAdmin(admin.ModelAdmin):
    exclude = ('empresa',) # Esconde o campo empresa (preenchemos via código)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        if hasattr(request.user, 'funcionario'):
            return qs.filter(empresa=request.user.funcionario.empresa)
        return qs.none()

    def save_model(self, request, obj, form, change):
        if not obj.empresa_id and hasattr(request.user, 'funcionario'):
             obj.empresa = request.user.funcionario.empresa
        super().save_model(request, obj, form, change)

@admin.register(PlanoDeContas)
class PlanoDeContasAdmin(FinanceiroSaaSAdmin):
    list_display = ('codigo', 'nome', 'tipo', 'empresa')
    list_filter = ('tipo', 'empresa')
    search_fields = ('nome', 'codigo')

@admin.register(Caixa)
class CaixaAdmin(FinanceiroSaaSAdmin):
    list_display = ('nome', 'saldo_inicial', 'empresa')

@admin.register(Conta)
class ContaAdmin(FinanceiroSaaSAdmin):
    list_display = ('descricao', 'cadastro', 'valor', 'data_vencimento', 'status', 'plano_de_contas')
    list_filter = ('status', 'data_vencimento', 'plano_de_contas__tipo')
    search_fields = ('descricao', 'documento', 'cadastro__nome')
    
    fieldsets = (
        ('Detalhes da Conta', {
            'fields': ('plano_de_contas', 'cadastro', 'descricao', 'documento')
        }),
        ('Valores e Datas', {
            'fields': ('valor', 'data_vencimento', 'status')
        }),
        ('Outros', {
            'fields': ('observacoes',),
            'classes': ('collapse',)
        })
    )

    # Filtra os Dropdowns (Só mostra Clientes e Planos da minha empresa)
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if not request.user.is_superuser and hasattr(request.user, 'funcionario'):
            empresa_user = request.user.funcionario.empresa
            
            if db_field.name == "cadastro":
                kwargs["queryset"] = Cadastro.objects.filter(empresa=empresa_user)
            if db_field.name == "plano_de_contas":
                kwargs["queryset"] = PlanoDeContas.objects.filter(empresa=empresa_user)
                
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

@admin.register(Lancamento)
class LancamentoAdmin(FinanceiroSaaSAdmin):
    list_display = ('data_lancamento', 'descricao', 'tipo', 'valor', 'caixa')
    list_filter = ('tipo', 'data_lancamento', 'caixa')
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if not request.user.is_superuser and hasattr(request.user, 'funcionario'):
            empresa_user = request.user.funcionario.empresa
            if db_field.name == "caixa":
                kwargs["queryset"] = Caixa.objects.filter(empresa=empresa_user)
            if db_field.name == "plano_de_contas":
                kwargs["queryset"] = PlanoDeContas.objects.filter(empresa=empresa_user)
                
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    