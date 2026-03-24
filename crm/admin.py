from django.contrib import admin
from .models import Lead, Interacao
from rh.models import Funcionario

class InteracaoInline(admin.TabularInline):
    model = Interacao
    extra = 1
    fields = ('data_agendada', 'tipo', 'responsavel', 'descricao', 'realizada')
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if not request.user.is_superuser and hasattr(request.user, 'funcionario'):
            if db_field.name == "responsavel":
                # Só mostra funcionários da própria empresa para fazer a visita
                kwargs["queryset"] = Funcionario.objects.filter(empresa=request.user.funcionario.empresa)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    inlines = [InteracaoInline]
    list_display = ('nome_empresa', 'nome_contato', 'telefone', 'status', 'created_at')
    list_filter = ('status', 'origem', 'created_at')
    search_fields = ('nome_empresa', 'nome_contato', 'telefone')

    def get_exclude(self, request, obj=None):
        if not request.user.is_superuser:
            return ['empresa']
        return
    