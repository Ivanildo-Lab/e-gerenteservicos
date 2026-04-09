from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Pedido, TipoServico
from .forms import PedidoForm, AlocacaoFormSet, TipoServicoForm
from django.db import models 
from django.db.models import Q

# --- VIEWS DOS PEDIDOS ---

@login_required
def lista_pedidos(request):
    # Regra SaaS: Filtra os pedidos da empresa do usuário
    pedidos = Pedido.objects.filter(empresa=request.user.empresa)
    return render(request, 'servicos/lista_pedidos.html', {'pedidos': pedidos})

# --- VIEWS DO PEDIDO (COMPLEXA) ---
@login_required
def novo_pedido(request, pk=None):
    pedido = get_object_or_404(Pedido, pk=pk, empresa=request.user.empresa) if pk else None
    
    if request.method == 'POST':
        form = PedidoForm(request.POST, instance=pedido, empresa=request.user.empresa)
        formset = AlocacaoFormSet(request.POST, instance=pedido)
        
        if form.is_valid() and formset.is_valid():
            pedido = form.save(commit=False)
            pedido.empresa = request.user.empresa
            pedido.save()
            
            formset.instance = pedido
            formset.save()
            
            pedido.atualizar_total() # Chama o método que criamos no model
            messages.success(request, "Pedido/OS salvo com sucesso!")
            return redirect('servicos:lista_pedidos')
    else:
        form = PedidoForm(instance=pedido, empresa=request.user.empresa)
        formset = AlocacaoFormSet(instance=pedido)
        
        # Filtra os dropdowns dentro do formset
        for f in formset:
            f.fields['servico'].queryset = TipoServico.objects.filter(empresa=request.user.empresa)
            f.fields['funcionario'].queryset = request.user.empresa.funcionario_set.all()

    return render(request, 'servicos/formulario_pedido.html', {
        'form': form,
        'formset': formset,
        'is_edit': pk is not None
    })


# --- VIEWS DO CATÁLOGO ---
@login_required
@login_required
def lista_catalogo(request):
    # Pega todos os serviços da empresa
    catalogo = TipoServico.objects.filter(empresa=request.user.empresa)
    
    # Lógica de Busca (Search)
    query = request.GET.get('q')
    if query:
        catalogo = catalogo.filter(
            Q(nome__icontains=query) | 
            Q(descricao__icontains=query)
        )
        
    return render(request, 'servicos/lista_catalogo.html', {'catalogo': catalogo})

@login_required
def gerenciar_servico(request, pk=None):
    # Serve tanto para NOVO quanto para EDITAR
    servico = get_object_or_404(TipoServico, pk=pk, empresa=request.user.empresa) if pk else None
    
    if request.method == 'POST':
        form = TipoServicoForm(request.POST, instance=servico)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.empresa = request.user.empresa
            obj.save()
            messages.success(request, "Serviço salvo com sucesso no catálogo!")
            return redirect('servicos:lista_catalogo')
    else:
        form = TipoServicoForm(instance=servico)
        
    return render(request, 'servicos/formulario_catalogo.html', {'form': form})

@login_required
def excluir_servico(request, pk):
    servico = get_object_or_404(TipoServico, pk=pk, empresa=request.user.empresa)
    try:
        nome = servico.nome
        servico.delete()
        messages.success(request, f"Serviço '{nome}' removido do catálogo.")
    except models.ProtectedError:
        # Se já tiver uma OS usando esse serviço, o banco bloqueia para não quebrar o financeiro
        messages.error(request, "Não é possível excluir este serviço pois ele já foi utilizado em Pedidos/OS.")
    
    return redirect('servicos:lista_catalogo')

# Mantenha aqui a sua função imprimir_nota_servico que já criamos antes!
@login_required
def imprimir_nota_servico(request, pedido_id):
    # Regra SaaS: Garante que o usuário só imprima pedidos da PRÓPRIA empresa
    if request.user.is_superuser:
        pedido = get_object_or_404(Pedido, id=pedido_id)
    else:
        # Pega a empresa do usuário logado
        if hasattr(request.user, 'funcionario') and request.user.funcionario:
            empresa_user = request.user.funcionario.empresa
        elif hasattr(request.user, 'empresa') and request.user.empresa:
            empresa_user = request.user.empresa
        else:
            empresa_user = None
            
        pedido = get_object_or_404(Pedido, id=pedido_id, empresa=empresa_user)

    context = {
        'pedido': pedido,
        'alocacoes': pedido.alocacoes.all(),
        'empresa': pedido.empresa
    }
    return render(request, 'servicos/imprimir_nota_servico.html', context)

@login_required
def excluir_pedido(request, pk):
    # Busca o pedido garantindo que pertence à empresa do usuário
    pedido = get_object_or_404(Pedido, pk=pk, empresa=request.user.empresa)
    
    # Opcional: Você pode impedir a exclusão de pedidos já FATURADOS por segurança contábil
    if pedido.status == 'FATURADO':
        messages.error(request, "Não é permitido excluir um pedido que já foi FATURADO.")
    else:
        id_pedido = pedido.id
        pedido.delete()
        messages.success(request, f"Pedido #{id_pedido} removido com sucesso.")
    
    return redirect('servicos:lista_pedidos')