
from django.core.management.base import BaseCommand
from core.models import PerguntaESG


PERGUNTAS = {
    "E": [
        "A empresa utiliza embalagens recicláveis, reutilizáveis ou biodegradáveis?",
        "A empresa separa e destina corretamente os resíduos gerados?",
        "A empresa monitora o consumo de energia elétrica?",
        "A empresa adota medidas para reduzir o consumo de água e outros recursos?",
        "A empresa busca reduzir o impacto ambiental do transporte e das entregas?",
        "A empresa acompanha os impactos ambientais de seus produtos e operações?",
    ],
    "S": [
        "A loja virtual oferece recursos de acessibilidade para pessoas com deficiência?",
        "A empresa promove condições de trabalho seguras e adequadas?",
        "A empresa adota práticas de respeito à diversidade e à inclusão?",
        "A empresa possui um canal para receber e resolver reclamações de clientes?",
        "A empresa protege os dados pessoais de clientes e colaboradores?",
        "A empresa busca oferecer informações claras e atendimento acessível aos clientes?",
    ],
    "G": [
        "A empresa mantém suas políticas e práticas de negócio documentadas?",
        "A empresa informa com clareza as características, os preços e as condições dos produtos?",
        "A empresa possui regras para prevenir fraudes e conflitos de interesse?",
        "A empresa controla quem pode acessar dados e informações internas?",
        "A empresa mantém procedimentos para cumprir a legislação aplicável ao negócio?",
        "A empresa acompanha riscos e revisa periodicamente seus processos?",
    ],
}


class Command(BaseCommand):
    help = "Cadastra as 18 perguntas iniciais do questionário ESG."

    def handle(self, *args, **options):
        criadas = 0

        for dimensao, perguntas in PERGUNTAS.items():
            for ordem, texto in enumerate(perguntas, start=1):
                _, foi_criada = PerguntaESG.objects.get_or_create(
                    dimensao=dimensao,
                    ordem=ordem,
                    defaults={
                        "texto": texto,
                        "ativa": True,
                    },
                )

                if foi_criada:
                    criadas += 1

        total = PerguntaESG.objects.filter(ativa=True).count()

        self.stdout.write(
            self.style.SUCCESS(
                f"Concluído! {criadas} perguntas novas cadastradas. "
                f"Total de perguntas ativas: {total}."
            )
        )
