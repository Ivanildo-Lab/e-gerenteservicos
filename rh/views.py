from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import models
from .models import Funcionario, Cargo
from .forms import FuncionarioForm, OcorrenciaFormSet,CargoForm # Adicione o import

# --- CARGOS ---
@login_required
def lista_cargos(request):
    cargos = Cargo.objects.filter(empresa=request.user.empresa)
    return render(request, 'rh/lista_cargos.html', {'cargos': cargos})

@login_required
def gerenciar_cargo(request, pk=None):
    cargo = get_object_or_404(Cargo, pk=pk, empresa=request.user.empresa) if pk else None
    if request.method == 'POST':
        form = CargoForm(request.POST, instance=cargo)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.empresa = request.user.empresa
            obj.save()
            messages.success(request, "Cargo salvo com sucesso!")
            return redirect('rh:lista_cargos')
    else:
        form = CargoForm(instance=cargo)
    return render(request, 'rh/formulario_cargo.html', {'form': form})


@login_required
def excluir_cargo(request, pk):
    cargo = get_object_or_404(Cargo, pk=pk, empresa=request.user.empresa)
    try:
        cargo.delete()
        messages.success(request, "Cargo removido com sucesso!")
    except models.ProtectedError:
        messages.error(request, "Não é possível excluir este cargo pois existem funcionários vinculados a ele.")
    
    return redirect('rh:lista_cargos')

# --- FUNCIONÁRIOS ---
@login_required
def lista_funcionarios(request):
    funcionarios = Funcionario.objects.filter(empresa=request.user.empresa)
    return render(request, 'rh/lista_funcionarios.html', {'funcionarios': funcionarios})


@login_required
def gerenciar_funcionario(request, pk=None):
    func = get_object_or_404(Funcionario, pk=pk, empresa=request.user.empresa) if pk else None
    
    if request.method == 'POST':
        form = FuncionarioForm(request.POST, request.FILES, instance=func, empresa=request.user.empresa)
        formset = OcorrenciaFormSet(request.POST, request.FILES, instance=func) # Captura as ocorrências
        
        if form.is_valid() and formset.is_valid():
            obj = form.save(commit=False)
            obj.empresa = request.user.empresa
            obj.save()
            
            formset.instance = obj # Vincula as ocorrências ao funcionário salvo
            formset.save()
            
            messages.success(request, "Cadastro e histórico atualizados!")
            return redirect('rh:lista_funcionarios')
    else:
        form = FuncionarioForm(instance=func, empresa=request.user.empresa)
        formset = OcorrenciaFormSet(instance=func)
        
    return render(request, 'rh/formulario_funcionario.html', {'form': form, 'formset': formset})
@login_required
def excluir_funcionario(request, pk):
    # Busca o funcionário garantindo que pertence à empresa do usuário logado
    funcionario = get_object_or_404(Funcionario, pk=pk, empresa=request.user.empresa)
    
    nome = funcionario.nome_completo
    funcionario.delete()
    
    messages.success(request, f"Funcionário {nome} removido com sucesso!")
    return redirect('rh:lista_funcionarios')
