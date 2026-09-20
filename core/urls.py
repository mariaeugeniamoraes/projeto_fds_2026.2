from django.urls import path
from . import views


urlpatterns = [
    # Página inicial
    path('', views.home, name='home'),

    # Cadastro e autenticação
    path('cadastro/', views.cadastro, name='cadastro'),
    path('login/', views.entrar, name='login'),
    path('logout/', views.sair, name='logout'),

    # Fale Conosco / Feedback
    path('fale-conosco/', views.feedback, name='feedback'),

    # Páginas institucionais
    path('quem-somos/', views.quem_somos, name='quem_somos'),
    path('projeto/', views.projeto, name='projeto'),

    # Perfil do usuário
    path('perfil/', views.perfil, name='perfil'),
    path('perfil/editar/', views.editar_perfil, name='editar_perfil'),
]