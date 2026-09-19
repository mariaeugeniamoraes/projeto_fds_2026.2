from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import FeedbackForm


def home(request):
    return render(request, 'core/home.html')


def cadastro(request):

    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('login')

    else:
        form = UserCreationForm()

    return render(request, 'core/cadastro.html', {'form': form})

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