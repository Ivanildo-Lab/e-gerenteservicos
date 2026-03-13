from django import forms
from django.forms import inlineformset_factory, FileInput, DateInput, Textarea
from .models import Funcionario, Ocorrencia, Cargo

class FuncionarioForm(forms.ModelForm):
    class Meta:
        model = Funcionario
        exclude = ['empresa']
        widgets = {
            'data_nascimento': DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
            'data_admissao': DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
            'cnh_validade': DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
            'observacoes': Textarea(attrs={'rows': 3}),
            # A classe 'hidden' do Tailwind esconde o botão feio do navegador de vez
            'foto': FileInput(attrs={'class': 'hidden'}),
        }

    def __init__(self, *args, **kwargs):
        empresa = kwargs.pop('empresa', None)
        super().__init__(*args, **kwargs)
        
        for field_name, field in self.fields.items():
            # Pula o campo foto para não sobrescrever a classe hidden
            if field_name == 'foto': 
                continue
                
            css_classes = 'w-full border-gray-300 rounded p-2 text-sm border shadow-sm focus:ring-indigo-500'
            if isinstance(field.widget, forms.Select): 
                css_classes += ' bg-white'
            field.widget.attrs.update({'class': css_classes})
            
        if empresa:
            self.fields['cargo'].queryset = Cargo.objects.filter(empresa=empresa)

class CargoForm(forms.ModelForm):
    class Meta:
        model = Cargo
        exclude = ['empresa']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'w-full border-gray-300 rounded p-2 text-sm border shadow-sm bg-white'
            })

# --- FORMSET DAS OCORRÊNCIAS ---
# --- FORMSET DAS OCORRÊNCIAS ---

# 1. Criamos um Form específico para a Ocorrência para podermos colocar a nossa "Regra Inteligente"
class OcorrenciaForm(forms.ModelForm):
    class Meta:
        model = Ocorrencia
        fields = ('data', 'tipo', 'descricao', 'documento')
        widgets = {
            'data': DateInput(format='%Y-%m-%d', attrs={'type': 'date', 'class': 'w-full border-gray-300 rounded p-1 text-xs'}),
            'tipo': forms.Select(attrs={'class': 'w-full border-gray-300 rounded p-1 text-xs bg-white'}),
            'descricao': Textarea(attrs={'class': 'w-full border-gray-300 rounded p-1 text-xs', 'rows': '3'}),
            'documento': FileInput(attrs={'class': 'hidden'}),
        }

    def has_changed(self):
        """
        O PULO DO GATO:
        Verifica se o formulário realmente foi alterado pelo usuário.
        Se a linha for nova (sem PK) e não tiver Descrição nem Documento,
        dizemos ao Django que nada mudou, assim ele ignora a linha vazia e não dá erro.
        """
        changed = super().has_changed()
        
        if changed and not self.instance.pk:
            # Pega o que o usuário digitou no campo descrição
            descricao = self.data.get(self.add_prefix('descricao'), '').strip()
            documento = self.files.get(self.add_prefix('documento'))
            
            # Se a descrição estiver vazia e não tiver anexo, ignora a validação!
            if not descricao and not documento:
                return False
                
        return changed

# --- FORMSET DAS OCORRÊNCIAS ---

# 1. Criamos um Form específico para a Ocorrência para podermos colocar a nossa "Regra Inteligente"
class OcorrenciaForm(forms.ModelForm):
    class Meta:
        model = Ocorrencia
        fields = ('data', 'tipo', 'descricao', 'documento')
        widgets = {
            'data': DateInput(format='%Y-%m-%d', attrs={'type': 'date', 'class': 'w-full border-gray-300 rounded p-1 text-xs'}),
            'tipo': forms.Select(attrs={'class': 'w-full border-gray-300 rounded p-1 text-xs bg-white'}),
            'descricao': Textarea(attrs={'class': 'w-full border-gray-300 rounded p-1 text-xs', 'rows': '3'}),
            'documento': FileInput(attrs={'class': 'hidden'}),
        }

    def has_changed(self):
        """
        O PULO DO GATO:
        Verifica se o formulário realmente foi alterado pelo usuário.
        Se a linha for nova (sem PK) e não tiver Descrição nem Documento,
        dizemos ao Django que nada mudou, assim ele ignora a linha vazia e não dá erro.
        """
        changed = super().has_changed()
        
        if changed and not self.instance.pk:
            # Pega o que o usuário digitou no campo descrição
            descricao = self.data.get(self.add_prefix('descricao'), '').strip()
            documento = self.files.get(self.add_prefix('documento'))
            
            # Se a descrição estiver vazia e não tiver anexo, ignora a validação!
            if not descricao and not documento:
                return False
                
        return changed

# 2. Usamos o nosso Form inteligente na fábrica de Formsets
OcorrenciaFormSet = inlineformset_factory(
    Funcionario, Ocorrencia,
    form=OcorrenciaForm, # Aponta para a classe que criamos acima
    extra=1, 
    can_delete=True
)

# Garante que o Django saiba que o documento não é obrigatório
OcorrenciaFormSet.form.base_fields['documento'].required = False