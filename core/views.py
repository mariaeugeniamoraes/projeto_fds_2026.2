from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

from .forms import (
    FeedbackForm,
    CadastroUsuarioForm,
    EditarUsuarioForm,
    EmpresaForm,
    CalculadoraEmbalagemForm,
    RegistroFinanceiroForm,
)
from .models import (
    Empresa,
    PerguntaESG,
    DiagnosticoESG,
    RespostaDiagnostico,
    PlanoAcaoESG,
    RegistroFinanceiro,
)

# Catálogo de alternativas sustentáveis de embalagem
ALTERNATIVAS_SUSTENTAVEIS = {
    'plastico_bolha': {
        'nome': 'Papel Colmeia Flexível / Bio-Pack de Milho',
        'fator_custo': 1.12,
        'plastico_evitado_unitario_kg': 0.05,
        'impacto_descricao': 'Substitui o plástico por material 100% compostável ou reciclável.'
    },
    'fita_plastica': {
        'nome': 'Fita Gomada Kraft (Cola Vegetal)',
        'fator_custo': 1.05,
        'plastico_evitado_unitario_kg': 0.02,
        'impacto_descricao': 'Permite reciclar a caixa de papelão sem necessidade de separar a fita.'
    },
    'envelopes_plasticos': {
        'nome': 'Envelope de Papel Kraft Hidro-repelente / Plástico Compostável',
        'fator_custo': 1.18,
        'plastico_evitado_unitario_kg': 0.08,
        'impacto_descricao': 'Decomposição em poucos meses em compostagem doméstica/industrial.'
    },
    'caixa_virgem': {
        'nome': 'Caixa de Papelão 100% Reciclado (Selo FSC)',
        'fator_custo': 0.95,
        'plastico_evitado_unitario_kg': 0.00,
        'impacto_descricao': 'Evita o desmatamento e reduz o consumo de água na fabricação.'
    }
}


def home(request):
    return render(request, 'core/home.html')


def cadastro(request):
    if request.method == 'POST':
        form = CadastroUsuarioForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('login')

    else:
        form = CadastroUsuarioForm()

    return render(
        request,
        'core/cadastro.html',
        {'form': form}
    )


def entrar(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect('home')

        else:
            return render(
                request,
                'core/login.html',
                {'erro': 'Usuário ou senha inválidos.'}
            )

    return render(request, 'core/login.html')


def sair(request):
    logout(request)
    return redirect('home')


def feedback(request):
    if request.method == 'POST':

        if not request.user.is_authenticated:
            return redirect('login')

        form = FeedbackForm(request.POST)

        if form.is_valid():
            novo_feedback = form.save(commit=False)
            novo_feedback.usuario = request.user
            novo_feedback.save()

            return render(
                request,
                'core/feedback_sucesso.html'
            )

    else:
        form = FeedbackForm()

    return render(
        request,
        'core/feedback.html',
        {'form': form}
    )


def quem_somos(request):
    return render(request, 'core/quem_somos.html')


def projeto(request):
    return render(request, 'core/projeto.html')


@login_required
def perfil(request):
    return render(
        request,
        'core/perfil.html'
    )


@login_required
def editar_perfil(request):

    if request.method == 'POST':
        form = EditarUsuarioForm(
            request.POST,
            instance=request.user
        )

        if form.is_valid():
            form.save()
            return redirect('perfil')

    else:
        form = EditarUsuarioForm(
            instance=request.user
        )

    return render(
        request,
        'core/editar_perfil.html',
        {'form': form}
    )


@login_required
def minhas_empresas(request):
    empresas = Empresa.objects.filter(usuario=request.user)

    if request.method == "POST":
        form = EmpresaForm(request.POST)

        if form.is_valid():
            empresa = form.save(commit=False)
            empresa.usuario = request.user
            empresa.save()
            return redirect("minhas_empresas")
    else:
        form = EmpresaForm()

    return render(
        request,
        "core/minhas_empresas.html",
        {
            "empresas": empresas,
            "form": form,
        },
    )


@login_required
def iniciar_diagnostico(request, empresa_id):
    empresa = get_object_or_404(
        Empresa,
        id=empresa_id,
        usuario=request.user,
    )

    perguntas = PerguntaESG.objects.filter(
        ativa=True
    ).order_by("dimensao", "ordem")
    print("PERGUNTAS ESG NO RENDER:", perguntas.count())
    if request.method == "POST":
        diagnostico = DiagnosticoESG.objects.create(
            empresa=empresa
        )

        for pergunta in perguntas:
            valor = request.POST.get(f"pergunta_{pergunta.id}")

            if valor not in {"0", "1", "2", "3"}:
                diagnostico.delete()
                return render(
                    request,
                    "core/diagnostico.html",
                    {
                        "empresa": empresa,
                        "perguntas": perguntas,
                        "erro": "Responda a todas as perguntas antes de continuar.",
                    },
                )

            RespostaDiagnostico.objects.create(
                diagnostico=diagnostico,
                pergunta=pergunta,
                pontuacao=int(valor),
            )

        respostas = diagnostico.respostas.select_related(
            "pergunta"
        )

        pontuacoes = {
            "E": 0,
            "S": 0,
            "G": 0,
        }

        quantidades = {
            "E": 0,
            "S": 0,
            "G": 0,
        }

        for resposta in respostas:
            dimensao = resposta.pergunta.dimensao
            pontuacoes[dimensao] += resposta.pontuacao
            quantidades[dimensao] += 1

        percentuais = {}

        for dimensao in ("E", "S", "G"):
            maximo = quantidades[dimensao] * 3

            percentuais[dimensao] = (
                pontuacoes[dimensao] / maximo * 100
                if maximo
                else 0
            )

        diagnostico.pontuacao_ambiental = pontuacoes["E"]
        diagnostico.pontuacao_social = pontuacoes["S"]
        diagnostico.pontuacao_governanca = pontuacoes["G"]

        diagnostico.percentual_ambiental = percentuais["E"]
        diagnostico.percentual_social = percentuais["S"]
        diagnostico.percentual_governanca = percentuais["G"]

        total_pontos = sum(pontuacoes.values())
        total_maximo = sum(quantidades.values()) * 3

        diagnostico.percentual_geral = (
            total_pontos / total_maximo * 100
            if total_maximo
            else 0
        )

        diagnostico.concluido = True
        diagnostico.save()

        return redirect(
            "resultado_diagnostico",
            diagnostico_id=diagnostico.id,
        )

    return render(
        request,
        "core/diagnostico.html",
        {
            "empresa": empresa,
            "perguntas": perguntas,
        },
    )


@login_required
def resultado_diagnostico(request, diagnostico_id):
    diagnostico = get_object_or_404(
        DiagnosticoESG.objects.select_related("empresa"),
        id=diagnostico_id,
        empresa__usuario=request.user,
        concluido=True,
    )

    respostas = diagnostico.respostas.select_related(
        "pergunta"
    ).order_by("pergunta__dimensao", "pergunta__ordem")

    dimensoes = [
        {
            "codigo": "E",
            "nome": "Ambiental",
            "pontuacao": diagnostico.pontuacao_ambiental,
            "percentual": diagnostico.percentual_ambiental,
        },
        {
            "codigo": "S",
            "nome": "Social",
            "pontuacao": diagnostico.pontuacao_social,
            "percentual": diagnostico.percentual_social,
        },
        {
            "codigo": "G",
            "nome": "Governança",
            "pontuacao": diagnostico.pontuacao_governanca,
            "percentual": diagnostico.percentual_governanca,
        },
    ]

    return render(
        request,
        "core/resultado_diagnostico.html",
        {
            "diagnostico": diagnostico,
            "respostas": respostas,
            "dimensoes": dimensoes,
        },
    )


@login_required
def historico_diagnosticos(request):
    diagnosticos = (
        DiagnosticoESG.objects
        .filter(
            empresa__usuario=request.user,
            concluido=True
        )
        .select_related("empresa")
        .order_by("-data_criacao")
    )

    empresa_id = request.GET.get("empresa")

    if empresa_id:
        diagnosticos = diagnosticos.filter(empresa_id=empresa_id)

    return render(
        request,
        "core/historico_diagnosticos.html",
        {"diagnosticos": diagnosticos}
    )


def portal_transparencia(request, empresa_id):
    empresa = get_object_or_404(
        Empresa,
        id=empresa_id,
        publicar_resultados=True
    )

    diagnostico = empresa.diagnosticos.filter(
        concluido=True
    ).first()

    return render(request, "core/portal_transparencia.html", {
        "empresa": empresa,
        "diagnostico": diagnostico
    })


@login_required
@require_POST
def alterar_publicacao_esg(request, empresa_id):
    empresa = get_object_or_404(
        Empresa,
        id=empresa_id,
        usuario=request.user
    )

    empresa.publicar_resultados = not empresa.publicar_resultados
    empresa.save(update_fields=["publicar_resultados"])

    return redirect("minhas_empresas")


def politica_privacidade(request):
    return render(request, "core/politica_privacidade.html")


@login_required
def ferramentas(request):
    return render(request, 'core/ferramentas.html')


@login_required
def calculadora_embalagens(request):
    resultado = None
    if request.method == 'POST':
        form = CalculadoraEmbalagemForm(request.POST)
        if form.is_valid():
            material_key = form.cleaned_data['material_atual']
            qtd = form.cleaned_data['quantidade_mensal']
            custo_unit_atual = float(form.cleaned_data['custo_unitario_atual'])

            custo_total_atual = qtd * custo_unit_atual
            alternativa = ALTERNATIVAS_SUSTENTAVEIS.get(material_key)

            custo_unit_alternativa = custo_unit_atual * float(alternativa['fator_custo'])
            custo_total_alternativa = float(qtd) * custo_unit_alternativa
            diferenca_custo = custo_total_alternativa - custo_total_atual

            plastico_evitado_ano = (alternativa['plastico_evitado_unitario_kg'] * qtd) * 12

            resultado = {
                'alternativa_nome': alternativa['nome'],
                'impacto_descricao': alternativa['impacto_descricao'],
                'custo_total_atual': f"{custo_total_atual:.2f}",
                'custo_total_alternativa': f"{custo_total_alternativa:.2f}",
                'diferenca_custo': f"{diferenca_custo:.2f}",
                'plastico_evitado_ano': f"{plastico_evitado_ano:.2f}",
            }
    else:
        form = CalculadoraEmbalagemForm()

    return render(
        request,
        'core/calculadora_embalagens.html',
        {
            'form': form,
            'resultado': resultado
        }
    )


@login_required
def listar_registros_financeiros(request, empresa_id):
    empresa = get_object_or_404(
        Empresa,
        id=empresa_id,
        usuario=request.user,
    )

    registros = empresa.registros_financeiros.all()

    receitas = sum(
        registro.valor
        for registro in registros
        if registro.tipo == RegistroFinanceiro.Tipo.RECEITA
    )

    custos = sum(
        registro.valor
        for registro in registros
        if registro.tipo == RegistroFinanceiro.Tipo.CUSTO
    )

    saldo = receitas - custos

    return render(
        request,
        "core/financeiro.html",
        {
            "empresa": empresa,
            "registros": registros,
            "receitas": receitas,
            "custos": custos,
            "saldo": saldo,
        },
    )


@login_required
def adicionar_registro_financeiro(request, empresa_id):
    empresa = get_object_or_404(
        Empresa,
        id=empresa_id,
        usuario=request.user,
    )

    if request.method == "POST":
        form = RegistroFinanceiroForm(request.POST)

        if form.is_valid():
            registro = form.save(commit=False)
            registro.empresa = empresa
            registro.save()

            return redirect(
                "listar_registros_financeiros",
                empresa_id=empresa.id,
            )
    else:
        form = RegistroFinanceiroForm()

    return render(
        request,
        "core/form_financeiro.html",
        {
            "empresa": empresa,
            "form": form,
            "titulo": "Adicionar movimentação",
        },
    )


@login_required
def editar_registro_financeiro(request, empresa_id, registro_id):
    empresa = get_object_or_404(
        Empresa,
        id=empresa_id,
        usuario=request.user,
    )

    registro = get_object_or_404(
        RegistroFinanceiro,
        id=registro_id,
        empresa=empresa,
    )

    if request.method == "POST":
        form = RegistroFinanceiroForm(
            request.POST,
            instance=registro,
        )

        if form.is_valid():
            form.save()

            return redirect(
                "listar_registros_financeiros",
                empresa_id=empresa.id,
            )
    else:
        form = RegistroFinanceiroForm(instance=registro)

    return render(
        request,
        "core/form_financeiro.html",
        {
            "empresa": empresa,
            "form": form,
            "titulo": "Editar movimentação",
        },
    )


@login_required
@require_POST
def excluir_registro_financeiro(request, empresa_id, registro_id):
    empresa = get_object_or_404(
        Empresa,
        id=empresa_id,
        usuario=request.user,
    )

    registro = get_object_or_404(
        RegistroFinanceiro,
        id=registro_id,
        empresa=empresa,
    )

    registro.delete()

    return redirect(
        "listar_registros_financeiros",
        empresa_id=empresa.id,
    )


@login_required
def dashboard(request):
    from decimal import Decimal
    from datetime import date
    from django.db.models import Sum
    from django.utils import timezone

    empresas = Empresa.objects.filter(usuario=request.user)

    empresa_id = request.GET.get("empresa")

    if empresa_id and empresa_id.isdigit():
        empresa = empresas.filter(id=int(empresa_id)).first()
    else:
        empresa = empresas.first()

    contexto = {
        "empresas": empresas,
        "empresa_selecionada": empresa,
        "total_diagnosticos": 0,
        "ultimo_diagnostico": None,
        "planos_pendentes": 0,
        "planos_em_andamento": 0,
        "planos_concluidos": 0,
        "ultimos_planos": [],
        "receitas": Decimal("0.00"),
        "custos": Decimal("0.00"),
        "saldo": Decimal("0.00"),
        "dados_graficos": {
            "esg": {
                "labels": ["Ambiental", "Social", "Governança"],
                "valores": [0, 0, 0],
            },
            "historico": {
                "labels": [],
                "valores": [],
            },
            "financeiro": {
                "labels": [],
                "receitas": [],
                "custos": [],
            },
            "planos": {
                "labels": ["Pendentes", "Em andamento", "Concluídos"],
                "valores": [0, 0, 0],
            },
        },
    }

    if empresa:
        diagnosticos = DiagnosticoESG.objects.filter(
            empresa=empresa,
            concluido=True,
        ).order_by("-data_criacao")

        ultimo = diagnosticos.first()

        planos = PlanoAcaoESG.objects.filter(
            diagnostico__empresa=empresa,
        )

        # Filtra os 5 planos de ação não concluídos mais recentes para exibir na lista do dashboard
        ultimos_planos = planos.exclude(status="concluida")[:5]

        registros = RegistroFinanceiro.objects.filter(
            empresa=empresa,
        )

        receitas = (
            registros.filter(tipo="receita")
            .aggregate(total=Sum("valor"))["total"]
            or Decimal("0.00")
        )

        custos = (
            registros.filter(tipo="custo")
            .aggregate(total=Sum("valor"))["total"]
            or Decimal("0.00")
        )

        pendentes = planos.filter(status="pendente").count()
        em_andamento = planos.filter(status="em_andamento").count()
        concluidos = planos.filter(status="concluida").count()

        # Histórico dos diagnósticos, do mais antigo ao mais recente.
        historico = diagnosticos.order_by("data_criacao")

        dados_historico = {
            "labels": [
                d.data_criacao.strftime("%d/%m/%Y")
                for d in historico
            ],
            "valores": [
                float(d.percentual_geral or 0)
                for d in historico
            ],
        }

        # Desempenho das três dimensões no último diagnóstico.
        dados_esg = {
            "labels": ["Ambiental", "Social", "Governança"],
            "valores": [
                float(ultimo.percentual_ambiental or 0),
                float(ultimo.percentual_social or 0),
                float(ultimo.percentual_governanca or 0),
            ] if ultimo else [0, 0, 0],
        }

        # Últimos seis meses, incluindo meses sem movimentação.
        hoje = timezone.localdate()
        meses = []

        ano = hoje.year
        mes = hoje.month

        for _ in range(5):
            mes -= 1
            if mes == 0:
                mes = 12
                ano -= 1

        for _ in range(6):
            meses.append((ano, mes))
            mes += 1
            if mes == 13:
                mes = 1
                ano += 1

        financeiro_por_mes = {
            chave: {
                "receitas": Decimal("0.00"),
                "custos": Decimal("0.00"),
            }
            for chave in meses
        }

        movimentacoes = registros.filter(
            data__year__gte=meses[0][0]
        ).values_list("data", "tipo", "valor")

        for data_registro, tipo, valor in movimentacoes:
            chave = (data_registro.year, data_registro.month)

            if chave not in financeiro_por_mes:
                continue

            if tipo == "receita":
                financeiro_por_mes[chave]["receitas"] += valor
            elif tipo == "custo":
                financeiro_por_mes[chave]["custos"] += valor

        dados_financeiros = {
            "labels": [
                f"{mes:02d}/{ano}"
                for ano, mes in meses
            ],
            "receitas": [
                float(financeiro_por_mes[chave]["receitas"])
                for chave in meses
            ],
            "custos": [
                float(financeiro_por_mes[chave]["custos"])
                for chave in meses
            ],
        }

        contexto.update({
            "total_diagnosticos": diagnosticos.count(),
            "ultimo_diagnostico": ultimo,
            "planos_pendentes": pendentes,
            "planos_em_andamento": em_andamento,
            "planos_concluidos": concluidos,
            "ultimos_planos": ultimos_planos,
            "receitas": receitas,
            "custos": custos,
            "saldo": receitas - custos,
            "dados_graficos": {
                "esg": dados_esg,
                "historico": dados_historico,
                "financeiro": dados_financeiros,
                "planos": {
                    "labels": [
                        "Pendentes",
                        "Em andamento",
                        "Concluídos",
                    ],
                    "valores": [
                        pendentes,
                        em_andamento,
                        concluidos,
                    ],
                },
            },
        })

    return render(request, "core/dashboard.html", contexto)

from .forms import PlanoAcaoForm  # Lembre-se de importar o PlanoAcaoForm no topo do ficheiro

@login_required
def listar_planos_acao(request, empresa_id):
    empresa = get_object_or_404(Empresa, id=empresa_id, usuario=request.user)
    
    # Busca os planos vinculados aos diagnósticos da empresa
    planos = PlanoAcaoESG.objects.filter(diagnostico__empresa=empresa).order_by('-id')
    
    # Filtro opcional por status via GET
    status_filtro = request.GET.get('status')
    if status_filtro:
        planos = planos.filter(status=status_filtro)

    form = PlanoAcaoForm()

    return render(
        request,
        'core/planos_acao.html',
        {
            'empresa': empresa,
            'planos': planos,
            'form': form,
            'status_filtro': status_filtro,
        }
    )


@login_required
def adicionar_plano_acao(request, empresa_id):
    empresa = get_object_or_404(Empresa, id=empresa_id, usuario=request.user)
    ultimo_diagnostico = empresa.diagnosticos.filter(concluido=True).first()

    if not ultimo_diagnostico:
        # Se a empresa não tiver diagnóstico, pode criar um automático ou avisar o usuário
        ultimo_diagnostico = DiagnosticoESG.objects.create(empresa=empresa, concluido=True)

    if request.method == 'POST':
        form = PlanoAcaoForm(request.POST)
        if form.is_valid():
            plano = form.save(commit=False)
            plano.diagnostico = ultimo_diagnostico
            plano.save()
            return redirect('listar_planos_acao', empresa_id=empresa.id)

    return redirect('listar_planos_acao', empresa_id=empresa.id)


@login_required
@require_POST
def alterar_status_plano(request, empresa_id, plano_id):
    empresa = get_object_or_404(Empresa, id=empresa_id, usuario=request.user)
    plano = get_object_or_404(PlanoAcaoESG, id=plano_id, diagnostico__empresa=empresa)

    novo_status = request.POST.get('status')
    if novo_status in ['pendente', 'em_andamento', 'concluida']:
        plano.status = novo_status
        plano.save(update_fields=['status'])

    return redirect('listar_planos_acao', empresa_id=empresa.id)


@login_required
@require_POST
def excluir_plano_acao(request, empresa_id, plano_id):
    empresa = get_object_or_404(Empresa, id=empresa_id, usuario=request.user)
    plano = get_object_or_404(PlanoAcaoESG, id=plano_id, diagnostico__empresa=empresa)
    plano.delete()

    return redirect('listar_planos_acao', empresa_id=empresa.id)