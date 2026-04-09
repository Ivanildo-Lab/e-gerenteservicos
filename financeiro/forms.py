from django import forms
from django.forms import DateInput, Textarea, FileInput
from .models import Conta, Lancamento, Caixa, PlanoDeContas
from cadastros.models import Cadastro
from rh.models import Funcionario

# --- FORMULÁRIO DE CAIXA / BANCO ---
class CaixaForm(forms.ModelForm):
    class Meta:
        model = Caixa
        fields = ['nome', 'saldo_inicial']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name == 'saldo_inicial':
                field.widget.attrs['class'] = 'w-full pl-10 pr-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500'
            else:
                field.widget.attrs['class'] = 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500'

# --- FORMULÁRIO DE PLANO DE CONTAS ---
class PlanoContasForm(forms.ModelForm):
    class Meta:
        model = PlanoDeContas
        fields = ['codigo', 'nome', 'tipo']
        widgets = {
            'tipo': forms.Select(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md bg-white'}),
        }
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if 'class' not in field.widget.attrs:
                 field.widget.attrs['class'] = 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500'

    def clean_codigo(self):
        codigo = self.cleaned_data.get('codigo')
        if self.user and codigo:
            existe = PlanoDeContas.objects.filter(
                empresa=self.user.empresa,
                codigo=codigo
            ).exclude(id=self.instance.id).exists()
            if existe:
                raise forms.ValidationError("Este Código já está em uso nesta empresa.")
        return codigo

# --- FORMULÁRIO DE CONTA (A PAGAR / RECEBER) ---
# financeiro/forms.py
class ContaForm(forms.ModelForm):
    gerar_parcelas = forms.BooleanField(required=False, initial=False)
    qtd_parcelas = forms.IntegerField(required=False, initial=1, min_value=1)
    taxa_juros = forms.DecimalField(required=False, initial=0, max_digits=5, decimal_places=2)

    class Meta:
        model = Conta
        fields = [
            'tipo_favorecido', 'descricao', 'plano_de_contas', 
            'cadastro', 'funcionario', 'valor', 'data_vencimento', 
            'status', 'documento', 'observacoes', 'arquivo'
        ]
        widgets = {
            'data_vencimento': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
            'observacoes': forms.Textarea(attrs={'rows': 3}),
            # FileInput puro para o anexo
            'arquivo': forms.FileInput(attrs={'class': 'hidden', 'accept': 'image/*,application/pdf'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        tipo_filtro = kwargs.pop('tipo_filtro', None)
        super().__init__(*args, **kwargs)
        
        for field_name, field in self.fields.items():
            if field_name in ['arquivo', 'gerar_parcelas']: continue
            css_class = 'w-full border border-gray-300 rounded p-2 text-sm shadow-sm focus:ring-blue-500 focus:border-blue-500'
            if isinstance(field.widget, forms.Select): css_class += ' bg-white'
            field.widget.attrs.update({'class': css_class})
            
        if user and user.empresa:
            self.fields['cadastro'].queryset = Cadastro.objects.filter(empresa=user.empresa)
            self.fields['funcionario'].queryset = Funcionario.objects.filter(empresa=user.empresa)
            planos = PlanoDeContas.objects.filter(empresa=user.empresa)
            if tipo_filtro: planos = planos.filter(tipo=tipo_filtro)
            self.fields['plano_de_contas'].queryset = planos
# --- FORMULÁRIO DE LANÇAMENTO MANUAL ---
class LancamentoManualForm(forms.ModelForm):
    class Meta:
        model = Lancamento
        fields = ['caixa', 'data_lancamento', 'tipo', 'plano_de_contas', 'descricao', 'valor']
        widgets = {
            'data_lancamento': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
            'tipo': forms.Select(attrs={'class': 'bg-white'}),
        }
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        for field_name, field in self.fields.items():
            css_class = 'w-full border border-gray-300 rounded p-2 text-sm focus:ring-2 focus:ring-blue-500'
            if field_name == 'valor':
                css_class = 'w-full pl-10 pr-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500'
            
            field.widget.attrs['class'] = css_class
        
        if user and user.empresa:
            self.fields['caixa'].queryset = Caixa.objects.filter(empresa=user.empresa)
            self.fields['plano_de_contas'].queryset = PlanoDeContas.objects.filter(empresa=user.empresa)