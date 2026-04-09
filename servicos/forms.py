from django import forms
from .models import TipoServico, Pedido, Alocacao
from cadastros.models import Cadastro
from rh.models import Funcionario

class TipoServicoForm(forms.ModelForm):
    class Meta:
        model = TipoServico
        exclude = ['empresa']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'w-full border-gray-300 rounded p-2 text-sm border shadow-sm'}),
            'descricao': forms.Textarea(attrs={'class': 'w-full border-gray-300 rounded p-2 text-sm border shadow-sm', 'rows': 3}),
            'valor_base': forms.NumberInput(attrs={'class': 'w-full border-gray-300 rounded p-2 text-sm border shadow-sm'}),
            'unidade': forms.Select(attrs={'class': 'w-full border-gray-300 rounded p-2 text-sm border shadow-sm bg-white'}),
        }

class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        exclude = ['empresa', 'valor_total']
        widgets = {
            'cliente': forms.Select(attrs={'class': 'w-full border-gray-300 rounded p-2 text-sm border shadow-sm bg-white'}),
            # O 'format' é o segredo para a data aparecer na edição
            'data_solicitacao': forms.DateInput(format='%Y-%m-%d', attrs={'class': 'w-full border-gray-300 rounded p-2 text-sm border shadow-sm', 'type': 'date'}),
            'status': forms.Select(attrs={'class': 'w-full border-gray-300 rounded p-2 text-sm border shadow-sm bg-white'}),
            'observacoes': forms.Textarea(attrs={'class': 'w-full border-gray-300 rounded p-2 text-sm border shadow-sm', 'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        empresa = kwargs.pop('empresa', None)
        super().__init__(*args, **kwargs)
        if empresa:
            self.fields['cliente'].queryset = Cadastro.objects.filter(
                empresa=empresa, papel__in=['CLI', 'AMB'], situacao='ATIVO'
            )

# Formset para as Alocações (Itens do Pedido)
AlocacaoFormSet = forms.inlineformset_factory(
    Pedido, Alocacao,
    fields=('servico', 'funcionario', 'data_inicio', 'data_fim', 'quantidade', 'valor_unitario'),
    extra=1,
    can_delete=True,
    widgets={
        'servico': forms.Select(attrs={'class': 'w-full border-gray-300 rounded p-1 text-xs border bg-white'}),
        'funcionario': forms.Select(attrs={'class': 'w-full border-gray-300 rounded p-1 text-xs border bg-white'}),
        # DATAS COM HORA (format exige o 'T' no meio para o navegador aceitar)
        'data_inicio': forms.DateTimeInput(format='%Y-%m-%dT%H:%M', attrs={'class': 'w-full border-gray-300 rounded p-1 text-xs border', 'type': 'datetime-local'}),
        'data_fim': forms.DateTimeInput(format='%Y-%m-%dT%H:%M', attrs={'class': 'w-full border-gray-300 rounded p-1 text-xs border', 'type': 'datetime-local'}),
        'quantidade': forms.NumberInput(attrs={'class': 'w-full border-gray-300 rounded p-1 text-xs border'}),
        'valor_unitario': forms.NumberInput(attrs={'class': 'w-full border-gray-300 rounded p-1 text-xs border'}),
    }
)