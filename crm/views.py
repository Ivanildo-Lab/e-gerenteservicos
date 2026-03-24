from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Lead
from .forms import LeadForm, InteracaoFormSet
from rh.models import Funcionario

@login_required
def lista_leads(request):
    leads = Lead.objects.filter(empresa=request.user.empresa)
    return render(request, 'crm/lista_leads.html', {'leads': leads})

@login_required
def gerenciar_lead(request, pk=None):
    lead = get_object_or_404(Lead, pk=pk, empresa=request.user.empresa) if pk else None
    
    if request.method == 'POST':
        form = LeadForm(request.POST, instance=lead)
        formset = InteracaoFormSet(request.POST, instance=lead)
        
        if form.is_valid() and formset.is_valid():
            obj = form.save(commit=False)
            obj.empresa = request.user.empresa
            obj.save()
            
            formset.instance = obj
            formset.save()
            
            messages.success(request, "Lead atualizado no Funil de Vendas!")
            return redirect('crm:lista_leads')
    else:
        form = LeadForm(instance=lead)
        formset = InteracaoFormSet(instance=lead)
        
        # Filtra os funcionários para mostrar apenas os da empresa na hora de agendar visita
        for f in formset:
            f.fields['responsavel'].queryset = Funcionario.objects.filter(empresa=request.user.empresa, situacao='ATIVO')

    return render(request, 'crm/formulario_lead.html', {'form': form, 'formset': formset})