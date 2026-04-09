from django.contrib import admin
from .models import PlanoDeContas, Caixa, Conta, Lancamento
from cadastros.models import Cadastro

# Classe base para aplicar o filtro SaaS em todos os admins do Financeiro
class FinanceiroSaaSAdmin(admin.ModelAdmin):
    # 1. REMOVEMOS o `exclude = ('empresa',)` fixo daqui.
    
    # 2. Criamos uma regra inteligente para esconder ou mostrar a Empresa
    def get_exclude(self, request, obj=None):
        if request.user.is_superuser:
            return [] # Superuser vê a caixinha e escolhe a empresa
        return['empresa'] # Usuário comum não vê

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        
        # Tenta pegar a empresa direto do usuário (SaaS) ou do funcionário do RH
        if hasattr(request.user, 'empresa') and request.user.empresa:
            return qs.filter(empresa=request.user.empresa)
        if hasattr(request.user, 'funcionario') and request.user.funcionario:
            return qs.filter(empresa=request.user.funcionario.empresa)
            
        return qs.none()

    def save_model(self, request, obj, form, change):
        # Só preenche automático se estiver vazio (ou seja, se estava oculto)
        if not obj.empresa_id:
            if hasattr(request.user, 'empresa') and request.user.empresa:
                 obj.empresa = request.user.empresa
            elif hasattr(request.user, 'funcionario') and request.user.funcionario:
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
    list_display = ('descricao', 'get_favorecido', 'valor', 'data_vencimento', 'status', 'plano_de_contas')
    list_filter = ('status', 'tipo_favorecido', 'data_vencimento', 'plano_de_contas')
    search_fields = ('descricao', 'cadastro__nome', 'funcionario__nome_completo')
    
    fieldsets = (
        ('Classificação', {
            'fields': ('plano_de_contas', 'descricao')
        }),
        ('Favorecido (Quem paga/recebe)', {
            'fields': ('tipo_favorecido', 'cadastro', 'funcionario'),
            'description': "Escolha o tipo e preencha apenas o campo correspondente."
        }),
        ('Valores e Datas', {
            'fields': ('valor', 'data_vencimento', 'status', 'documento')
        }),
        ('Outros', {
            'fields': ('observacoes',),
            'classes': ('collapse',)
        })
    )

    # Método que junta Cliente e Funcionário na mesma coluna da tabela visual
    def get_favorecido(self, obj):
        if obj.tipo_favorecido == 'FUNCIONARIO' and obj.funcionario:
            return f"👨‍🔧 {obj.funcionario.nome_completo} (Func)"
        elif obj.cadastro:
            return f"🏢 {obj.cadastro.nome}"
        return "-"
    get_favorecido.short_description = "Favorecido"

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if not request.user.is_superuser and hasattr(request.user, 'funcionario'):
            empresa_user = request.user.funcionario.empresa
            
            if db_field.name == "cadastro": # Filtra Clientes/Fornecedores
                from cadastros.models import Cadastro
                kwargs["queryset"] = Cadastro.objects.filter(empresa=empresa_user)
            
            if db_field.name == "funcionario": # Filtra Funcionários do RH
                from rh.models import Funcionario
                kwargs["queryset"] = Funcionario.objects.filter(empresa=empresa_user)
                
            if db_field.name == "plano_de_contas": # Filtra Plano de Contas
                from .models import PlanoDeContas
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
    