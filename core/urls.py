from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('cadastro/', views.cadastro, name='cadastro'),
    path('login/', views.entrar, name='login'),
    path('logout/', views.sair, name='logout'),
    path('fale-conosco/', views.feedback, name='feedback'),
    path('quem-somos/', views.quem_somos, name='quem_somos'),
    path('projeto/', views.projeto, name='projeto'),
]