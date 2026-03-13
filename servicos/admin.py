from django.contrib import admin
from django.utils.html import format_html 
from django.urls import reverse
from .models import TipoServico, Pedido, Alocacao
from cadastros.models import Cadastro 

class AlocacaoInline(admin.TabularInline):
    model = Alocacao
    extra = 1
    fields = ('servico', 'funcionario', 'data_inicio', 'data_fim', 'quantidade', 'valor_unitario', 'realizado')
    autocomplete_fields = ['funcionario'] 

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if not request.user.is_superuser and hasattr(request.user, 'funcionario'):
            empresa_usuario = request.user.funcionario.empresa
            if db_field.name == "servico":
                kwargs["queryset"] = TipoServico.objects.filter(empresa=empresa_usuario)
            if db_field.name == "funcionario":
                kwargs["queryset"] = request.user.funcionario.empresa.funcionarios.all()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(TipoServico)
class TipoServicoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'unidade', 'valor_base', 'empresa')
    list_filter = ('empresa',)

    def get_exclude(self, request, obj=None):
        if request.user.is_superuser:
            return [] 
        return ['empresa'] 

    def save_model(self, request, obj, form, change):
        if not obj.empresa_id and hasattr(request.user, 'funcionario'):
             obj.empresa = request.user.funcionario.empresa
        super().save_model(request, obj, form, change)
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        if hasattr(request.user, 'funcionario'):
            return qs.filter(empresa=request.user.funcionario.empresa)
        return qs.none()


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    inlines = [AlocacaoInline]
    
    # Adicionamos 'link_impressao' na listagem principal
    list_display = ('id', 'cliente', 'data_solicitacao', 'status', 'valor_total', 'link_impressao', 'empresa')
    list_filter = ('empresa', 'status', 'data_solicitacao')
    autocomplete_fields = ['cliente'] 

    # Campos que o usuário não pode editar manualmente
    readonly_fields = ('valor_total', 'link_impressao') 

    # CORREÇÃO: Apenas um get_exclude. (valor_total já está no readonly)
    def get_exclude(self, request, obj=None):
        if not request.user.is_superuser:
            return ['empresa']
        return[]

    # --- MÉTODO NOVO: Cria o botão de impressão ---
    def link_impressao(self, obj):
        # Só mostra o botão se o pedido já foi salvo no banco (tem um ID)
        if obj.id: 
            # Aponta para a URL que criamos no Passo 2
            url = reverse('servicos:imprimir_nota_servico', args=[obj.id])
            return format_html(
                '<a class="button" href="{}" target="_blank" '
                'style="background-color: #4CAF50; color: white; padding: 6px 12px; '
                'border-radius: 4px; text-decoration: none; font-weight: bold;">'
                '🖨️ Imprimir OS</a>', url
            )
        return "Salve o pedido primeiro"
    link_impressao.short_description = "Ações" # Nome da coluna


    def save_model(self, request, obj, form, change):
        if not obj.empresa_id and hasattr(request.user, 'funcionario'):
            obj.empresa = request.user.funcionario.empresa
        super().save_model(request, obj, form, change)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        if hasattr(request.user, 'funcionario'):
            return qs.filter(empresa=request.user.funcionario.empresa)
        return qs.none()

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if not request.user.is_superuser and hasattr(request.user, 'funcionario'):
            if db_field.name == "cliente":
                kwargs["queryset"] = Cadastro.objects.filter(
                    empresa=request.user.funcionario.empresa,
                    papel__in=['CLI', 'AMB'],
                    situacao='ATIVO'
                )
        return super().formfield_for_foreignkey(db_field, request, **kwargs)