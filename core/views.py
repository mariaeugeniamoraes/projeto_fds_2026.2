from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Empresa

from .forms import (
    FeedbackForm,
    CadastroUsuarioForm,
    EditarUsuarioForm,
    EmpresaForm,
)
from .models import (
    Empresa,
    PerguntaESG,
    DiagnosticoESG,
    RespostaDiagnostico,
)
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

from django.views.decorators.http import require_POST

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
