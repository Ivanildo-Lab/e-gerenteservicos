from django import forms
from django.forms import inlineformset_factory
from .models import Lead, Interacao
from rh.models import Funcionario

class LeadForm(forms.ModelForm):
    class Meta:
        model = Lead
        exclude =['empresa']
        widgets = {
            'motivo_perda': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Preencha apenas se o negócio for perdido...'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            css_classes = 'w-full border-gray-300 rounded p-2 text-sm border shadow-sm focus:ring-orange-500'
            if isinstance(field.widget, forms.Select):
                css_classes += ' bg-white'
            field.widget.attrs.update({'class': css_classes})

# Formset para a Agenda de Interações (Visitas/Ligações)
InteracaoFormSet = inlineformset_factory(
    Lead, Interacao,
    fields=('data_agendada', 'tipo', 'responsavel', 'descricao', 'realizada'),
    extra=1,
    can_delete=True,
    widgets={
        'data_agendada': forms.DateTimeInput(format='%Y-%m-%dT%H:%M', attrs={'type': 'datetime-local', 'class': 'w-full border-gray-300 rounded p-1 text-xs'}),
        'tipo': forms.Select(attrs={'class': 'w-full border-gray-300 rounded p-1 text-xs bg-white'}),
        'responsavel': forms.Select(attrs={'class': 'w-full border-gray-300 rounded p-1 text-xs bg-white'}),
        'descricao': forms.TextInput(attrs={'class': 'w-full border-gray-300 rounded p-1 text-xs', 'placeholder': 'Assunto da visita/ligação...'}),
    }
)