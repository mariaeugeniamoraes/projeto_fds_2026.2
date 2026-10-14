
from django.contrib import admin
from .models import (
    Empresa,
    Feedback,
    PerguntaESG,
    DiagnosticoESG,
    RespostaDiagnostico,
    PlanoAcaoESG,
    IndicadorESG,
    HistoricoIndicador,
    RegistroFinanceiro,
)


@admin.register(Empresa)
class EmpresaAdmin(admin.ModelAdmin):
    list_display = ("nome", "usuario", "setor", "data_criacao")
    search_fields = ("nome", "usuario__username", "cnpj")


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ("usuario", "nota", "data")
    list_filter = ("nota", "data")
    search_fields = ("usuario__username", "comentario")


@admin.register(PerguntaESG)
class PerguntaESGAdmin(admin.ModelAdmin):
    list_display = ("texto", "dimensao", "ordem", "ativa")
    list_filter = ("dimensao", "ativa")
    search_fields = ("texto",)


@admin.register(DiagnosticoESG)
class DiagnosticoESGAdmin(admin.ModelAdmin):
    list_display = (
        "empresa",
        "data_criacao",
        "percentual_ambiental",
        "percentual_social",
        "percentual_governanca",
        "concluido",
    )
    list_filter = ("concluido", "data_criacao")
    search_fields = ("empresa__nome",)


@admin.register(RespostaDiagnostico)
class RespostaDiagnosticoAdmin(admin.ModelAdmin):
    list_display = ("diagnostico", "pergunta", "pontuacao")
    list_filter = ("pontuacao",)
    search_fields = ("pergunta__texto", "diagnostico__empresa__nome")


@admin.register(PlanoAcaoESG)
class PlanoAcaoESGAdmin(admin.ModelAdmin):
    list_display = (
        "titulo",
        "diagnostico",
        "dimensao",
        "prioridade",
        "status",
        "prazo",
    )
    list_filter = ("dimensao", "prioridade", "status")
    search_fields = ("titulo", "diagnostico__empresa__nome")


@admin.register(IndicadorESG)
class IndicadorESGAdmin(admin.ModelAdmin):
    list_display = ("nome", "empresa", "dimensao", "valor_atual", "unidade")
    list_filter = ("dimensao",)
    search_fields = ("nome", "empresa__nome")


@admin.register(HistoricoIndicador)
class HistoricoIndicadorAdmin(admin.ModelAdmin):
    list_display = ("indicador", "valor", "data_registro")
    list_filter = ("data_registro",)
    search_fields = ("indicador__nome",)


@admin.register(RegistroFinanceiro)
class RegistroFinanceiroAdmin(admin.ModelAdmin):
    list_display = (
        "empresa",
        "tipo",
        "descricao",
        "categoria",
        "valor",
        "data",
    )
    list_filter = ("tipo", "categoria", "data")
    search_fields = ("empresa__nome", "descricao", "categoria")
