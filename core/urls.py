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
    path(
        "minhas-empresas/",
        views.minhas_empresas,
        name="minhas_empresas",
    ),
    path(
        "empresas/<int:empresa_id>/diagnostico/",
        views.iniciar_diagnostico,
        name="iniciar_diagnostico",
    ),
    path(
        "diagnosticos/<int:diagnostico_id>/resultado/",
        views.resultado_diagnostico,
        name="resultado_diagnostico",
    ),
    path(
        "historico-diagnosticos/",
        views.historico_diagnosticos,
        name="historico_diagnosticos",
    ),
    path(
        "transparencia/<int:empresa_id>/",
        views.portal_transparencia,
        name="portal_transparencia"
    ),
    path(
        "empresas/<int:empresa_id>/publicacao/",
        views.alterar_publicacao_esg,
        name="alterar_publicacao_esg"
    ),
    path(
        "politica-de-privacidade/",
        views.politica_privacidade,
        name="politica_privacidade"
    ),

    # Hub de Ferramentas e Calculadora
    path(
        "ferramentas/",
        views.ferramentas,
        name="ferramentas",
    ),
    path(
        "calculadora-embalagens/",
        views.calculadora_embalagens,
        name="calculadora_embalagens",
    ),
    
    # Controle financeiro
    path(
        "empresas/<int:empresa_id>/financeiro/",
        views.listar_registros_financeiros,
        name="listar_registros_financeiros",
    ),
    path(
        "empresas/<int:empresa_id>/financeiro/adicionar/",
        views.adicionar_registro_financeiro,
        name="adicionar_registro_financeiro",
    ),
    path(
        "empresas/<int:empresa_id>/financeiro/<int:registro_id>/editar/",
        views.editar_registro_financeiro,
        name="editar_registro_financeiro",
    ),
    path(
        "empresas/<int:empresa_id>/financeiro/<int:registro_id>/excluir/",
        views.excluir_registro_financeiro,
        name="excluir_registro_financeiro",
    ),
    path(
        "dashboard/", 
        views.dashboard, 
        name="dashboard"
    ),

    path('empresas/<int:empresa_id>/planos-de-acao/', views.listar_planos_acao, name='listar_planos_acao'),
    path('empresas/<int:empresa_id>/planos-de-acao/adicionar/', views.adicionar_plano_acao, name='adicionar_plano_acao'),
    path('empresas/<int:empresa_id>/planos-de-acao/<int:plano_id>/status/', views.alterar_status_plano, name='alterar_status_plano'),
    path('empresas/<int:empresa_id>/planos-de-acao/<int:plano_id>/excluir/', views.excluir_plano_acao, name='excluir_plano_acao'),

    # Central de Monitoramento de Fornecedores
    path('empresas/<int:empresa_id>/fornecedores/', views.listar_fornecedores, name='listar_fornecedores'),
    path('empresas/<int:empresa_id>/fornecedores/adicionar/', views.adicionar_fornecedor, name='adicionar_fornecedor'),
    path('empresas/<int:empresa_id>/fornecedores/<int:fornecedor_id>/alerta/', views.alternar_alerta_fornecedor, name='alternar_alerta_fornecedor'),
    path('empresas/<int:empresa_id>/fornecedores/<int:fornecedor_id>/excluir/', views.excluir_fornecedor, name='excluir_fornecedor'),

    # Painel Admin (somente superusers)
    path("painel-admin/", views.painel_admin, name="painel_admin"),
    path("painel-admin/usuarios/<int:usuario_id>/", views.admin_usuario, name="admin_usuario"),
]
