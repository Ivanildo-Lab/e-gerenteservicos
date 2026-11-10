/*
 * Busca inteligente para <select> do Django.
 *
 * Converte um select em um campo de texto com filtro instantâneo:
 *  - filtra enquanto digita (ignora acentos e caixa maiúscula)
 *  - por padrão apresenta as opções em ordem alfabética
 *  - navegação por teclado: setas ↓/↑, Enter seleciona, Esc fecha
 *  - botão "×" limpa a seleção
 *  - se o usuário digitar e sair sem escolher, volta a exibir a opção
 *    realmente selecionada (evita enviar um valor errado de forma invisível)
 *
 * Uso:
 *   criarBuscaInteligente(document.getElementById('id_campo'),
 *                         'Placeholder...',
 *                         true)  // true = manter a ordem original das opções
 */
(function (global) {
    'use strict';

    function normalizarTexto(txt) {
        return (txt || '').normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase().trim();
    }

    function criarBuscaInteligente(select, placeholder, manterOrdemOriginal) {
        if (!select) return null;
        // Não converte duas vezes o mesmo campo
        if (select.dataset.buscaAtiva === '1') return null;

        // Snapshot das opções (por padrão em ordem alfabética, independente da ordem do banco)
        const opcoes = Array.from(select.options)
            .filter(o => o.value !== '')
            .map(o => ({ valor: o.value, texto: o.textContent.trim(), chave: normalizarTexto(o.textContent) }));

        if (!opcoes.length) return null;

        if (!manterOrdemOriginal) {
            opcoes.sort((a, b) => a.chave.localeCompare(b.chave, 'pt-BR'));
        }

        const caixa = document.createElement('div');
        caixa.className = 'relative';

        const inputBusca = document.createElement('input');
        inputBusca.type = 'text';
        inputBusca.autocomplete = 'off';
        inputBusca.spellcheck = false;
        inputBusca.className = select.className + ' pr-8';
        inputBusca.placeholder = placeholder || 'Digite para pesquisar...';

        const botaoLimpar = document.createElement('button');
        botaoLimpar.type = 'button';
        botaoLimpar.title = 'Limpar pesquisa';
        botaoLimpar.innerHTML = '&times;';
        botaoLimpar.className = 'absolute right-2 top-0 h-full px-1 text-lg leading-none text-gray-400 hover:text-red-500 hidden';

        const lista = document.createElement('div');
        lista.className = 'absolute left-0 right-0 top-full mt-1 bg-white border border-gray-300 rounded-md shadow-xl max-h-64 overflow-y-auto hidden z-[70]';

        caixa.appendChild(inputBusca);
        caixa.appendChild(botaoLimpar);
        caixa.appendChild(lista);
        select.parentNode.insertBefore(caixa, select);
        select.style.display = 'none';
        select.setAttribute('aria-hidden', 'true');
        select.dataset.buscaAtiva = '1';

        let itens = [];
        let ativo = -1;

        function textoSelecionado() {
            const atual = select.options[select.selectedIndex];
            return (atual && atual.value !== '') ? atual.textContent.trim() : '';
        }

        function sincronizar() {
            const texto = textoSelecionado();
            inputBusca.value = texto;
            botaoLimpar.classList.toggle('hidden', !texto);
        }

        function filtrar(consulta) {
            const palavras = normalizarTexto(consulta).split(/\s+/).filter(Boolean);
            if (!palavras.length) return opcoes;
            return opcoes.filter(o => palavras.every(p => o.chave.includes(p)));
        }

        function abrir() { lista.classList.remove('hidden'); }

        function fechar() {
            lista.classList.add('hidden');
            ativo = -1;
        }

        function destacar(indice) {
            itens.forEach((el, i) => {
                const on = i === indice;
                el.classList.toggle('bg-blue-600', on);
                el.classList.toggle('text-white', on);
                if (on) el.scrollIntoView({ block: 'nearest' });
            });
        }

        function renderizar(consulta) {
            const resultados = filtrar(consulta);
            lista.innerHTML = '';
            itens = [];
            ativo = -1;

            if (!resultados.length) {
                const vazio = document.createElement('div');
                vazio.className = 'px-3 py-2 text-xs text-gray-400 italic';
                vazio.textContent = 'Nenhuma opção encontrada';
                lista.appendChild(vazio);
            } else {
                resultados.forEach(r => {
                    const item = document.createElement('div');
                    item.className = 'px-3 py-2 text-sm text-gray-700 cursor-pointer border-b border-gray-50 last:border-0 hover:bg-gray-100';
                    item.textContent = r.texto;
                    item.dataset.valor = r.valor;
                    item.addEventListener('mousedown', e => {
                        e.preventDefault(); // evita o blur antes do clique
                        selecionar(r.valor);
                    });
                    item.addEventListener('mouseenter', () => {
                        ativo = itens.indexOf(item);
                        destacar(ativo);
                    });
                    lista.appendChild(item);
                    itens.push(item);
                });
            }
            abrir();
        }

        function selecionar(valor) {
            select.value = valor;
            select.dispatchEvent(new Event('change', { bubbles: true }));
            sincronizar();
            fechar();
            inputBusca.focus();
        }

        inputBusca.addEventListener('focus', () => renderizar(''));
        inputBusca.addEventListener('input', () => renderizar(inputBusca.value));
        inputBusca.addEventListener('blur', e => {
            if (!caixa.contains(e.relatedTarget)) {
                fechar();
                sincronizar(); // volta a mostrar a opção realmente selecionada
            }
        });
        inputBusca.addEventListener('keydown', e => {
            if (e.key === 'ArrowDown' || e.key === 'ArrowUp') {
                e.preventDefault();
                if (lista.classList.contains('hidden')) renderizar(inputBusca.value);
                if (!itens.length) return;
                ativo = e.key === 'ArrowDown'
                    ? (ativo + 1) % itens.length
                    : (ativo <= 0 ? itens.length - 1 : ativo - 1);
                destacar(ativo);
            } else if (e.key === 'Enter') {
                if (!lista.classList.contains('hidden') && ativo >= 0 && itens[ativo]) {
                    e.preventDefault();
                    selecionar(itens[ativo].dataset.valor);
                }
            } else if (e.key === 'Escape') {
                fechar();
                sincronizar();
            }
        });
        botaoLimpar.addEventListener('click', () => {
            select.value = '';
            select.dispatchEvent(new Event('change', { bubbles: true }));
            sincronizar();
            renderizar('');
            inputBusca.focus();
        });
        document.addEventListener('mousedown', e => {
            if (!caixa.contains(e.target)) { fechar(); sincronizar(); }
        });
        // Mantém o texto do campo em sincronia quando outro script altera a seleção
        select.addEventListener('change', () => { sincronizar(); fechar(); });

        sincronizar();
        return { sincronizar: sincronizar };
    }

    global.normalizarTexto = normalizarTexto;
    global.criarBuscaInteligente = criarBuscaInteligente;
})(window);
