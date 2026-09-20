from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .forms import FeedbackForm, CadastroUsuarioForm, EditarUsuarioForm


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