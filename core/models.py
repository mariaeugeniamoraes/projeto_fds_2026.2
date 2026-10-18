
from django.db import models
from django.contrib.auth.models import User


class Empresa(models.Model):
    usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="empresas"
    )
    nome = models.CharField(max_length=200)
    cnpj = models.CharField(max_length=18, blank=True)
    setor = models.CharField(max_length=100, blank=True)
    data_criacao = models.DateTimeField(auto_now_add=True)
    publicar_resultados = models.BooleanField(default=False)

    def __str__(self):
        return self.nome


class Feedback(models.Model):
    usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    nota = models.IntegerField()
    comentario = models.TextField()
    data = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback de {self.usuario.username}"


class PerguntaESG(models.Model):
    class Dimensao(models.TextChoices):
        AMBIENTAL = "E", "Ambiental"
        SOCIAL = "S", "Social"
        GOVERNANCA = "G", "Governança"

    texto = models.TextField()
    dimensao = models.CharField(
        max_length=1,
        choices=Dimensao.choices
    )
    ordem = models.PositiveIntegerField()
    ativa = models.BooleanField(default=True)

    class Meta:
        ordering = ["dimensao", "ordem"]
        constraints = [
            models.UniqueConstraint(
                fields=["dimensao", "ordem"],
                name="pergunta_esg_ordem_unica_por_dimensao"
            )
        ]

    def __str__(self):
        return f"{self.get_dimensao_display()}: {self.texto[:70]}"


class DiagnosticoESG(models.Model):
    empresa = models.ForeignKey(
        Empresa,
        on_delete=models.CASCADE,
        related_name="diagnosticos"
    )
    data_criacao = models.DateTimeField(auto_now_add=True)

    pontuacao_ambiental = models.PositiveIntegerField(default=0)
    pontuacao_social = models.PositiveIntegerField(default=0)
    pontuacao_governanca = models.PositiveIntegerField(default=0)

    percentual_ambiental = models.DecimalField(
        max_digits=5, decimal_places=2, default=0
    )
    percentual_social = models.DecimalField(
        max_digits=5, decimal_places=2, default=0
    )
    percentual_governanca = models.DecimalField(
        max_digits=5, decimal_places=2, default=0
    )
    percentual_geral = models.DecimalField(
        max_digits=5, decimal_places=2, default=0
    )

    concluido = models.BooleanField(default=False)

    class Meta:
        ordering = ["-data_criacao"]

    def __str__(self):
        return f"Diagnóstico de {self.empresa.nome} - {self.data_criacao:%d/%m/%Y}"


class RespostaDiagnostico(models.Model):
    diagnostico = models.ForeignKey(
        DiagnosticoESG,
        on_delete=models.CASCADE,
        related_name="respostas"
    )
    pergunta = models.ForeignKey(
        PerguntaESG,
        on_delete=models.PROTECT,
        related_name="respostas"
    )
    pontuacao = models.PositiveSmallIntegerField(
        choices=[
            (0, "0 - Não implementado"),
            (1, "1 - Em início"),
            (2, "2 - Parcialmente implementado"),
            (3, "3 - Implementado e monitorado"),
        ]
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["diagnostico", "pergunta"],
                name="resposta_unica_por_pergunta_diagnostico"
            )
        ]

    def __str__(self):
        return f"Resposta {self.pontuacao} - {self.pergunta_id}"


class PlanoAcaoESG(models.Model):
    class Prioridade(models.TextChoices):
        BAIXA = "baixa", "Baixa"
        MEDIA = "media", "Média"
        ALTA = "alta", "Alta"

    class Status(models.TextChoices):
        PENDENTE = "pendente", "Pendente"
        EM_ANDAMENTO = "em_andamento", "Em andamento"
        CONCLUIDA = "concluida", "Concluída"
        CANCELADA = "cancelada", "Cancelada"

    diagnostico = models.ForeignKey(
        DiagnosticoESG,
        on_delete=models.CASCADE,
        related_name="plano_acoes"
    )
    titulo = models.CharField(max_length=200)
    descricao = models.TextField()
    dimensao = models.CharField(
        max_length=1,
        choices=PerguntaESG.Dimensao.choices
    )
    justificativa = models.TextField(blank=True)
    prioridade = models.CharField(
        max_length=10,
        choices=Prioridade.choices,
        default=Prioridade.MEDIA
    )
    prazo = models.DateField(null=True, blank=True)
    responsavel = models.CharField(max_length=150, blank=True)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDENTE
    )
    data_criacao = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["prazo", "prioridade"]

    def __str__(self):
        return self.titulo


class IndicadorESG(models.Model):
    empresa = models.ForeignKey(
        Empresa,
        on_delete=models.CASCADE,
        related_name="indicadores"
    )
    nome = models.CharField(max_length=150)
    dimensao = models.CharField(
        max_length=1,
        choices=PerguntaESG.Dimensao.choices
    )
    valor_atual = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True
    )
    unidade = models.CharField(max_length=40, blank=True)
    data_atualizacao = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["dimensao", "nome"]
        constraints = [
            models.UniqueConstraint(
                fields=["empresa", "nome"],
                name="indicador_nome_unico_por_empresa"
            )
        ]

    def __str__(self):
        return f"{self.nome} - {self.empresa.nome}"


class HistoricoIndicador(models.Model):
    indicador = models.ForeignKey(
        IndicadorESG,
        on_delete=models.CASCADE,
        related_name="historico"
    )
    valor = models.DecimalField(max_digits=12, decimal_places=2)
    data_registro = models.DateTimeField(auto_now_add=True)
    observacao = models.TextField(blank=True)

    class Meta:
        ordering = ["-data_registro"]

    def __str__(self):
        return f"{self.indicador.nome}: {self.valor}"


class RegistroFinanceiro(models.Model):
    class Tipo(models.TextChoices):
        CUSTO = "custo", "Custo"
        RECEITA = "receita", "Receita"

    empresa = models.ForeignKey(
        Empresa,
        on_delete=models.CASCADE,
        related_name="registros_financeiros"
    )
    tipo = models.CharField(
        max_length=10,
        choices=Tipo.choices
    )
    descricao = models.CharField(max_length=200)
    categoria = models.CharField(max_length=100)
    valor = models.DecimalField(max_digits=12, decimal_places=2)
    data = models.DateField()
    observacao = models.TextField(blank=True)
    data_criacao = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-data", "-data_criacao"]

    def __str__(self):
        return f"{self.get_tipo_display()}: {self.descricao}"

from .models import Empresa  # ajuste se necessário

class Fornecedor(models.Model):
    STATUS_RISCO = [
        ('baixo', 'Baixo Risco'),
        ('medio', 'Médio Risco'),
        ('alto', 'Alto Risco'),
    ]

    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='fornecedores')
    nome = models.CharField(max_length=200, verbose_name="Nome da Oficina / Fornecedor")
    servico = models.CharField(max_length=100, blank=True, verbose_name="Tipo de Serviço (ex: Costura, Estamparia)")
    
    # Alertas Críticos
    auditoria_pendente = models.BooleanField(default=True, verbose_name="Auditoria Pendente")
    contrato_assinado = models.BooleanField(default=False, verbose_name="Contrato Assinado")
    tecidos_certificados = models.BooleanField(default=False, verbose_name="Tecidos Certificados")

    status_risco = models.CharField(max_length=20, choices=STATUS_RISCO, default='medio')
    data_criacao = models.DateTimeField(auto_now_add=True)

    def calcular_nivel_risco(self):
        # Lógica para categorização automática na Matriz de Risco
        alertas = 0
        if self.auditoria_pendente:
            alertas += 1
        if not self.contrato_assinado:
            alertas += 1
        if not self.tecidos_certificados:
            alertas += 1

        if alertas >= 2:
            return 'alto'
        elif alertas == 1:
            return 'medio'
        return 'baixo'

    def save(self, *args, **kwargs):
        self.status_risco = self.calcular_nivel_risco()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nome} ({self.get_status_risco_display()})"