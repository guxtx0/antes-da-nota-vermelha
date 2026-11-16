"""Auditoria do pipeline: o que entrou, o que foi tratado e se o resultado merece confiança.

As três tabelas geradas aqui vão para o Power BI, para que o próprio painel mostre a engenharia.
"""
import pandas as pd

from camadas import conectar
from config import MODELO

# (grupo, o que se verifica, consulta que devolve o valor observado, regra, valor esperado)
VERIFICACOES = [
    ("Volume", "Toda matrícula do arquivo de origem chegou ao modelo",
     "SELECT (SELECT count(*) FROM modelo.dMatricula) - (SELECT count(*) FROM bruto.student_info)", "=", 0),
    ("Volume", "Toda turma do arquivo de origem chegou ao modelo",
     "SELECT (SELECT count(*) FROM modelo.dTurma) - (SELECT count(*) FROM bruto.courses)", "=", 0),
    ("Volume", "Toda entrega do arquivo de origem chegou ao modelo",
     "SELECT (SELECT count(*) FROM modelo.fEntregas) - (SELECT count(*) FROM bruto.student_assessment)", "=", 0),
    ("Conservação", "Nenhum clique se perdeu entre o log bruto e a tabela de acessos",
     "SELECT (SELECT sum(CAST(sum_click AS BIGINT)) FROM bruto.student_vle) - (SELECT sum(cliques) FROM modelo.fAcessos)", "=", 0),
    ("Conservação", "As duas tabelas de fato somam o mesmo total de cliques",
     "SELECT (SELECT sum(cliques) FROM modelo.fAcessos) - (SELECT sum(cliques) FROM modelo.fPresenca)", "=", 0),
    ("Chaves", "Turma não se repete na dimensão de turmas",
     "SELECT count(*) - count(DISTINCT chave_turma) FROM modelo.dTurma", "=", 0),
    ("Chaves", "Matrícula não se repete na dimensão de matrículas",
     "SELECT count(*) - count(DISTINCT chave_matricula) FROM modelo.dMatricula", "=", 0),
    ("Chaves", "Semana não se repete no calendário",
     "SELECT count(*) - count(DISTINCT semana) FROM modelo.dSemana", "=", 0),
    ("Chaves", "Tipo de atividade não se repete",
     "SELECT count(*) - count(DISTINCT codigo_atividade) FROM modelo.dAtividade", "=", 0),
    ("Chaves", "Cada matrícula tem no máximo uma nota de risco",
     "SELECT count(*) - count(DISTINCT chave_matricula) FROM modelo.fRisco", "=", 0),
    ("Integridade", "Toda matrícula aponta para uma turma existente",
     "SELECT count(*) FROM modelo.dMatricula f ANTI JOIN modelo.dTurma d USING (chave_turma)", "=", 0),
    ("Integridade", "Todo acesso pertence a uma matrícula existente",
     "SELECT count(*) FROM modelo.fAcessos f ANTI JOIN modelo.dMatricula d USING (chave_matricula)", "=", 0),
    ("Integridade", "Todo acesso cai em uma semana do calendário",
     "SELECT count(*) FROM modelo.fAcessos f ANTI JOIN modelo.dSemana d USING (semana)", "=", 0),
    ("Integridade", "Todo acesso tem tipo de atividade conhecido",
     "SELECT count(*) FROM modelo.fAcessos f ANTI JOIN modelo.dAtividade d USING (codigo_atividade)", "=", 0),
    ("Integridade", "Toda presença semanal pertence a uma matrícula existente",
     "SELECT count(*) FROM modelo.fPresenca f ANTI JOIN modelo.dMatricula d USING (chave_matricula)", "=", 0),
    ("Integridade", "Toda entrega pertence a uma matrícula existente",
     "SELECT count(*) FROM modelo.fEntregas f ANTI JOIN modelo.dMatricula d USING (chave_matricula)", "=", 0),
    ("Integridade", "Toda nota de risco pertence a uma matrícula existente",
     "SELECT count(*) FROM modelo.fRisco f ANTI JOIN modelo.dMatricula d USING (chave_matricula)", "=", 0),
    ("Tradução", "Nenhum campo de cadastro ficou sem tradução",
     """SELECT count(*) FROM tratado.matriculas WHERE genero IS NULL OR regiao IS NULL OR escolaridade IS NULL
        OR faixa_etaria IS NULL OR declarou_deficiencia IS NULL OR resultado IS NULL""", "=", 0),
    ("Tradução", "Nenhum tipo de atividade ou de avaliação ficou sem tradução",
     """SELECT (SELECT count(*) FROM tratado.materiais WHERE atividade IS NULL)
             + (SELECT count(*) FROM tratado.avaliacoes WHERE tipo_de_avaliacao IS NULL)""", "=", 0),
    ("Faixas", "Toda nota está entre 0 e 100",
     "SELECT count(*) FROM modelo.fEntregas WHERE nota < 0 OR nota > 100", "=", 0),
    ("Faixas", "Nenhuma semana de aula tem mais de 7 dias com acesso",
     "SELECT count(*) FROM modelo.fPresenca WHERE semana >= 1 AND dias_com_acesso NOT BETWEEN 1 AND 7", "=", 0),
    ("Faixas", "Toda nota de risco está entre 0 e 1",
     "SELECT count(*) FROM modelo.fRisco WHERE risco < 0 OR risco > 1", "=", 0),
    ("Alerta", "Só recebe nota de risco quem seguia matriculado no dia 28",
     """SELECT count(*) FROM modelo.fRisco r JOIN modelo.dMatricula m USING (chave_matricula)
        WHERE m.situacao_no_dia_28 <> 'Seguia matriculado no dia 28'""", "=", 0),
    ("Alerta", "Todo aluno matriculado no dia 28 recebeu nota de risco",
     """SELECT (SELECT count(*) FROM modelo.dMatricula WHERE situacao_no_dia_28 = 'Seguia matriculado no dia 28')
             - (SELECT count(*) FROM modelo.fRisco)""", "=", 0),
    ("Alerta", "O modelo escolhido passa do piso de qualidade (AUC de 0,70 no teste)",
     """SELECT valor FROM modelo.mlMetricas
        WHERE escolhido = 'Sim' AND metrica = 'AUC' AND conjunto LIKE '%teste%'""", ">=", 0.70),
]

# (o que foi feito, onde, consulta que conta os registros afetados, decisão tomada)
TRATAMENTOS = [
    ("Linhas repetidas do log reunidas em uma só", "student_vle",
     "SELECT (SELECT count(*) FROM bruto.student_vle) - (SELECT count(*) FROM tratado.acessos)",
     "Mesmo aluno, material e dia viram uma linha, com os cliques somados"),
    ("Data de cancelamento marcada com '?'", "student_registration.date_unregistration",
     "SELECT count(*) FROM bruto.student_registration WHERE date_unregistration = '?'",
     "Vira vazio: o aluno não cancelou a matrícula"),
    ("Semana prevista do material marcada com '?'", "vle.week_from",
     "SELECT count(*) FROM bruto.vle WHERE week_from = '?'",
     "Vira vazio: material sem semana planejada"),
    ("Faixa de privação marcada com '?'", "student_info.imd_band",
     "SELECT count(*) FROM bruto.student_info WHERE imd_band = '?'",
     "Vira 'Não informada', para não sumir dos gráficos"),
    ("Faixa de privação escrita sem o símbolo de %", "student_info.imd_band",
     "SELECT count(*) FROM bruto.student_info WHERE imd_band = '10-20'",
     "Padronizada para o mesmo formato das outras faixas"),
    ("Nota marcada com '?'", "student_assessment.score",
     "SELECT count(*) FROM bruto.student_assessment WHERE score = '?'",
     "Vira vazio e fica fora das médias"),
    ("Desistente sem data de cancelamento", "student_registration.date_unregistration",
     "SELECT count(*) FROM tratado.matriculas WHERE resultado = 'Desistente' AND dia_cancelamento IS NULL",
     "Continua desistente, mas não entra na curva de permanência por semana"),
    ("Data de matrícula marcada com '?'", "student_registration.date_registration",
     "SELECT count(*) FROM bruto.student_registration WHERE date_registration = '?'",
     "Vira vazio; no modelo de alerta recebe a mediana"),
    ("Prazo de avaliação marcado com '?'", "assessments.date",
     "SELECT count(*) FROM bruto.assessments WHERE date = '?'",
     "Vira vazio: em geral são exames sem data publicada"),
    ("Termos do cadastro traduzidos para o português", "referencias/traducoes.csv",
     "SELECT count(*) FROM ref.traducoes",
     "Tradução por tabela de-para, auditável e sem texto fixo no código"),
]

COMPARA = {"=": lambda obs, esp: obs == esp, ">=": lambda obs, esp: obs >= esp}


def executar(linhagem):
    con = conectar()

    linhas = []
    for ordem, (grupo, descricao, consulta, regra, esperado) in enumerate(VERIFICACOES, start=1):
        observado = float(con.execute(consulta).fetchone()[0])
        linhas.append({"ordem": ordem, "grupo": grupo, "verificacao": descricao,
                       "regra": f"{'igual a' if regra == '=' else 'no mínimo'} {esperado:g}".replace(".", ","),
                       "observado": observado,
                       "situacao": "Passou" if COMPARA[regra](observado, esperado) else "Falhou"})
    verificacoes = pd.DataFrame(linhas)

    tratamentos = pd.DataFrame([
        {"ordem": ordem, "tratamento": nome, "onde": onde,
         "registros": int(con.execute(consulta).fetchone()[0]), "decisao": decisao}
        for ordem, (nome, onde, consulta, decisao) in enumerate(TRATAMENTOS, start=1)])

    tabelas = {"engVerificacoes": (verificacoes, "Resultado de cada verificação de qualidade"),
               "engTratamentos": (tratamentos, "O que foi corrigido nos dados e quantos registros afetou")}
    for nome, (tabela, descricao) in tabelas.items():
        tabela.to_parquet(MODELO / f"{nome}.parquet", index=False, compression="snappy")
        linhagem.append(("3. Modelo", nome, "src/auditoria.py", len(tabela), tabela.shape[1], descricao))

    # a linhagem é gravada por último, para incluir a si mesma
    colunas = ["camada", "tabela", "origem", "linhas", "colunas", "o_que_acontece"]
    linhagem.append(("3. Modelo", "engLinhagem", "src/auditoria.py", len(linhagem) + 1, len(colunas) + 1,
                     "Caminho de cada tabela, da origem ao modelo"))
    tab_linhagem = pd.DataFrame(linhagem, columns=colunas)
    tab_linhagem.insert(0, "ordem", range(1, len(tab_linhagem) + 1))
    tab_linhagem.to_parquet(MODELO / "engLinhagem.parquet", index=False, compression="snappy")

    falhas = verificacoes[verificacoes.situacao == "Falhou"]
    print(f"  verificações: {len(verificacoes) - len(falhas)} de {len(verificacoes)} passaram")
    if len(falhas):
        print(falhas[["verificacao", "observado"]].to_string(index=False))
    return verificacoes
