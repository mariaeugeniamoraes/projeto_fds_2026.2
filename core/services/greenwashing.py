
import re


# Expressões ambientais que merecem verificação
REGRAS = [
    {
        "padrao": r"\b100\s*%\s*(?:ecol[oó]gic[oa]s?|sustent[aá]ve(?:l|is)|verde(?:s)?|natural(?:is)?)\b",
        "categoria": "Alegação absoluta",
        "explicacao": (
            "A expressão apresenta um benefício ambiental "
            "absoluto sem especificar sua comprovação."
        ),
        "sugestao": (
            "Informe a característica ambiental específica "
            "e apresente evidências verificáveis."
        ),
    },
    {
        "padrao": r"\b(?:totalmente|completamente)\s+(?:sustent[aá]ve(?:l|is)|ecol[oó]gic[oa]s?|verde(?:s)?)\b",
        "categoria": "Afirmação genérica",
        "explicacao": (
            "O texto apresenta uma afirmação ampla "
            "sem indicar exatamente o benefício ambiental."
        ),
        "sugestao": (
            "Explique qual característica do produto "
            "é sustentável e como foi verificada."
        ),
    },
    {
        "padrao": r"\b(?:zero\s+impacto|sem\s+impacto\s+ambiental|n[aã]o\s+causa\s+nenhum\s+impacto\s+ambiental)\b",
        "categoria": "Ausência de impacto ambiental",
        "explicacao": (
            "A afirmação sugere ausência de impacto ambiental, "
            "algo que exige fundamentação especialmente rigorosa."
        ),
        "sugestao": (
            "Especifique os impactos avaliados e "
            "apresente informações comprováveis."
        ),
    },
    {
        "padrao": r"\b(?:carbono\s+neutro|neutro\s+em\s+carbono|carbono\s+zero|zero\s+carbono)\b",
        "categoria": "Alegação climática",
        "explicacao": (
            "A alegação de neutralidade de carbono "
            "precisa de metodologia e evidências."
        ),
        "sugestao": (
            "Informe o escopo das emissões, a metodologia "
            "e o papel de eventuais compensações."
        ),
    },
    {
        "padrao": r"\b(?:biodegrad[aá]ve(?:l|is)|compost[aá]ve(?:l|is))\b",
        "categoria": "Descarte e decomposição",
        "explicacao": (
            "A decomposição pode depender de condições "
            "específicas que não foram informadas."
        ),
        "sugestao": (
            "Apresente as condições de decomposição "
            "e os documentos que sustentam a alegação."
        ),
    },
    {
        "padrao": r"\b(?:amig[oa]\s+d[oa]\s+meio\s+ambiente|amig[oa]\s+d[oa]\s+natureza|eco[\s-]?friendly)\b",
        "categoria": "Expressão ambiental vaga",
        "explicacao": (
            "A expressão não descreve claramente "
            "qual é o benefício ambiental do produto."
        ),
        "sugestao": (
            "Substitua a expressão por uma característica "
            "ambiental concreta e verificável."
        ),
    },
]


def analisar_greenwashing(texto):
    alertas = []

    for regra in REGRAS:
        correspondencias = re.finditer(
            regra["padrao"],
            texto,
            flags=re.IGNORECASE,
        )

        for correspondencia in correspondencias:
            alertas.append({
                "trecho": correspondencia.group(0),
                "categoria": regra["categoria"],
                "explicacao": regra["explicacao"],
                "sugestao": regra["sugestao"],
            })

    return {
        "total": len(alertas),
        "alertas": alertas,
        "mensagem": (
            "Encontramos alegações que precisam ser verificadas."
            if alertas
            else
            "Nenhuma expressão monitorada foi encontrada. "
            "Isso não garante ausência de greenwashing."
        ),
    }
