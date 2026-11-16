"""Caminhos e parâmetros do projeto. Tudo o que muda de máquina para máquina mora aqui."""
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
DADOS = RAIZ / "dados"
ORIGEM = DADOS / "0_origem"     # CSVs do OULAD, como publicados (fora do repositório)
BRUTO = DADOS / "1_bruto"       # cópia fiel em Parquet
TRATADO = DADOS / "2_tratado"   # tipado, deduplicado e em português
MODELO = DADOS / "3_modelo"     # tabelas que o Power BI lê
SQL = RAIZ / "sql"
REFERENCIAS = RAIZ / "referencias"

URL_OULAD = ("https://archive.ics.uci.edu/static/public/349/"
             "open+university+learning+analytics+dataset.zip")

# arquivo de origem -> nome da tabela na camada bruta
ARQUIVOS = {
    "courses": "courses",
    "assessments": "assessments",
    "vle": "vle",
    "studentInfo": "student_info",
    "studentRegistration": "student_registration",
    "studentAssessment": "student_assessment",
    "studentVle": "student_vle",
}

DIA_CORTE = 28          # o alerta só enxerga o que aconteceu antes deste dia
ANO_TREINO = 2013       # turmas que ensinam o modelo
ANO_TESTE = 2014        # turmas que o modelo nunca viu
LIMIAR_PADRAO = 0.60    # a partir desta nota de risco o aluno entra na lista do tutor
SEMENTE = 42
