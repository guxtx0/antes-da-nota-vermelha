"""Testes do projeto. Rodar depois do pipeline: pytest -q

O pipeline já grava o resultado das verificações em dados/3_modelo/engVerificacoes.parquet.
Aqui elas viram testes, junto com conferências de tradução e de alguns números de referência.
"""
import sys
from pathlib import Path

import duckdb
import pytest

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / "src"))
from camadas import conectar  # noqa: E402

con = conectar()


def um(sql):
    return con.execute(sql).fetchone()[0]


VERIFICACOES = con.execute("SELECT verificacao, situacao, observado FROM modelo.engVerificacoes ORDER BY ordem").fetchall()


@pytest.mark.parametrize("verificacao,situacao,observado", VERIFICACOES, ids=[v[0] for v in VERIFICACOES])
def test_verificacao_do_pipeline(verificacao, situacao, observado):
    assert situacao == "Passou", f"{verificacao} (observado: {observado})"


@pytest.mark.parametrize("campo,tabela,coluna", [
    ("genero", "student_info", "gender"),
    ("regiao", "student_info", "region"),
    ("escolaridade", "student_info", "highest_education"),
    ("faixa_etaria", "student_info", "age_band"),
    ("deficiencia", "student_info", "disability"),
    ("resultado", "student_info", "final_result"),
    ("curso", "courses", "code_module"),
    ("avaliacao", "assessments", "assessment_type"),
    ("atividade", "vle", "activity_type"),
])
def test_todo_valor_de_origem_tem_traducao(campo, tabela, coluna):
    sem_traducao = con.execute(f"""
        SELECT DISTINCT b.{coluna} FROM bruto.{tabela} AS b
        LEFT JOIN ref.traducoes AS t ON t.campo = '{campo}' AND t.original = b.{coluna}
        WHERE t.traducao IS NULL""").fetchall()
    assert sem_traducao == []


def test_nenhum_texto_em_ingles_sobrou_no_modelo():
    originais = {r[0] for r in con.execute(
        "SELECT original FROM ref.traducoes WHERE campo IN ('regiao', 'escolaridade', 'resultado', 'avaliacao')").fetchall()}
    usados = {r[0] for r in con.execute("""
        SELECT regiao FROM modelo.dMatricula UNION SELECT escolaridade FROM modelo.dMatricula
        UNION SELECT resultado FROM modelo.dMatricula UNION SELECT tipo_de_avaliacao FROM modelo.fEntregas""").fetchall()}
    assert originais.isdisjoint(usados)


def test_numeros_de_referencia():
    assert um("SELECT count(*) FROM modelo.dMatricula") == 32593
    assert um("SELECT count(*) FROM modelo.dTurma") == 22
    assert um("SELECT sum(cliques) FROM modelo.fAcessos") == 39605099
    assert round(um("SELECT avg(CAST(concluiu AS INTEGER)) FROM modelo.dMatricula"), 3) == 0.472
    assert um("SELECT count(*) FROM modelo.dMatricula WHERE situacao_no_dia_28 = 'Saiu antes do dia 28'") == 5040


def test_modelo_de_alerta_e_reproduzivel_e_calibrado():
    auc = um("SELECT valor FROM modelo.mlMetricas WHERE escolhido = 'Sim' AND metrica = 'AUC' AND conjunto LIKE '%teste%'")
    assert auc >= 0.70
    # em cada décimo, o risco previsto não pode se afastar mais de 10 pontos do que foi observado
    assert um("SELECT max(abs(risco_previsto - taxa_observada)) FROM modelo.mlCalibracao") < 0.10
    # o risco observado tem de crescer do primeiro ao último décimo
    taxas = [r[0] for r in con.execute("SELECT taxa_observada FROM modelo.mlCalibracao ORDER BY decimo").fetchall()]
    assert taxas == sorted(taxas)
