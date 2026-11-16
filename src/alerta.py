"""Alerta precoce: entre os alunos ainda matriculados no dia 28, quem tende a não concluir?

Cuidados para a nota de risco não parecer melhor do que é:
  * as variáveis usam só o que aconteceu antes do dia de corte (ver sql/4_alerta/variaveis.sql);
  * o modelo aprende com as turmas de 2013 e é posto à prova nas de 2014;
  * a nota das turmas de 2013 vem de validação cruzada, nunca do modelo que já viu o aluno.
"""
import numpy as np
import pandas as pd
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.inspection import permutation_importance
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import average_precision_score, brier_score_loss, roc_auc_score
from sklearn.model_selection import StratifiedKFold, cross_val_predict
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

from camadas import conectar
from config import ANO_TESTE, ANO_TREINO, DIA_CORTE, MODELO, SEMENTE, SQL

# variável -> (nome para leigos, família)
VARIAVEIS = {
    "nota_media": ("Nota média nas primeiras entregas", "Notas e entregas"),
    "parcela_entregue": ("Parcela das avaliações entregue", "Notas e entregas"),
    "sem_nota_ate_o_corte": ("Chegou ao dia 28 sem nenhuma nota", "Notas e entregas"),
    "avaliacoes_com_prazo_vencido": ("Avaliações com prazo até o dia 28", "Notas e entregas"),
    "posicao_na_turma": ("Posição na turma em volume de acessos", "Acessos ao AVA"),
    "cliques": ("Cliques até o dia 28", "Acessos ao AVA"),
    "cliques_antes_do_inicio": ("Cliques antes do início das aulas", "Acessos ao AVA"),
    "dias_com_acesso": ("Dias com acesso", "Acessos ao AVA"),
    "semanas_com_acesso": ("Semanas com acesso", "Acessos ao AVA"),
    "dias_sem_acessar": ("Dias sem acessar, contados no dia 28", "Acessos ao AVA"),
    "materiais_diferentes": ("Materiais diferentes abertos", "Acessos ao AVA"),
    "variacao_de_cliques": ("Variação de cliques entre a 1ª e a 4ª semana", "Acessos ao AVA"),
    "cliques_em_estudo": ("Cliques em materiais de estudo", "Acessos ao AVA"),
    "cliques_em_troca": ("Cliques em fórum e aulas ao vivo", "Acessos ao AVA"),
    "cliques_em_pratica": ("Cliques em questionários", "Acessos ao AVA"),
    "cliques_em_navegacao": ("Cliques em páginas de navegação", "Acessos ao AVA"),
    "nivel_de_escolaridade": ("Escolaridade na entrada", "Histórico do aluno"),
    "dia_matricula": ("Antecedência da matrícula", "Histórico do aluno"),
    "tentativas_anteriores": ("Tentativas anteriores no mesmo curso", "Histórico do aluno"),
    "creditos_em_curso": ("Créditos cursados ao mesmo tempo", "Histórico do aluno"),
}

FAIXAS = [(0.60, "Alto (60% ou mais)", 3), (0.30, "Médio (30% a 59%)", 2), (0.0, "Baixo (menos de 30%)", 1)]


def medir(real, previsto):
    return {"AUC": roc_auc_score(real, previsto),
            "Precisão média": average_precision_score(real, previsto),
            "Erro de Brier": brier_score_loss(real, previsto)}


def faixa(risco):
    for piso, nome, ordem in FAIXAS:
        if risco >= piso:
            return nome, ordem


def executar(linhagem):
    con = conectar()
    consulta = (SQL / "4_alerta" / "variaveis.sql").read_text(encoding="utf-8")
    dados = con.execute(consulta, {"dia_corte": DIA_CORTE}).df()
    colunas = list(VARIAVEIS)
    dados["dia_matricula"] = dados["dia_matricula"].fillna(dados["dia_matricula"].median())

    treino, teste = dados[dados.ano == ANO_TREINO], dados[dados.ano == ANO_TESTE]
    x_treino, y_treino = treino[colunas], treino.nao_concluiu
    x_teste, y_teste = teste[colunas], teste.nao_concluiu
    print(f"  treino {ANO_TREINO}: {len(treino):,} matrículas | teste {ANO_TESTE}: {len(teste):,}")

    candidatos = {
        "Regressão logística": make_pipeline(StandardScaler(), LogisticRegression(max_iter=2000)),
        "Gradient boosting": HistGradientBoostingClassifier(
            max_iter=300, learning_rate=0.05, max_leaf_nodes=15, l2_regularization=1.0, random_state=SEMENTE),
    }
    metricas, ajustados = [], {}
    for nome, modelo in candidatos.items():
        ajustados[nome] = modelo.fit(x_treino, y_treino)
        for metrica, valor in medir(y_teste, modelo.predict_proba(x_teste)[:, 1]).items():
            metricas.append({"modelo": nome, "conjunto": "Turmas de 2014 (teste)", "metrica": metrica, "valor": valor})
    escolhido = max(candidatos, key=lambda n: next(
        m["valor"] for m in metricas if m["modelo"] == n and m["metrica"] == "AUC"))
    print(f"  modelo escolhido: {escolhido}")

    dobras = StratifiedKFold(5, shuffle=True, random_state=SEMENTE)
    risco_treino = cross_val_predict(candidatos[escolhido], x_treino, y_treino, cv=dobras,
                                     method="predict_proba")[:, 1]
    risco_teste = ajustados[escolhido].predict_proba(x_teste)[:, 1]
    for metrica, valor in medir(y_treino, risco_treino).items():
        metricas.append({"modelo": escolhido, "conjunto": "Turmas de 2013 (validação cruzada)",
                         "metrica": metrica, "valor": valor})
    tab_metricas = pd.DataFrame(metricas)
    tab_metricas["valor"] = tab_metricas.valor.round(4)
    tab_metricas["escolhido"] = np.where(tab_metricas.modelo == escolhido, "Sim", "Não")

    # ---- nota de risco por matrícula, com os sinais que o tutor consegue ler
    def montar(base, risco, origem):
        saida = pd.DataFrame({"chave_matricula": base.chave_matricula.values, "risco": np.round(risco, 4)})
        saida["origem_da_nota"] = origem
        saida["cliques_ate_dia_28"] = base.cliques.values.astype(int)
        saida["dias_com_acesso_ate_dia_28"] = base.dias_com_acesso.values.astype(int)
        saida["dias_sem_acessar_no_dia_28"] = np.where(base.cliques.values == 0, np.nan, base.dias_sem_acessar.values)
        saida["parcela_entregue_ate_dia_28"] = np.round(base.parcela_entregue.values, 4)
        saida["nota_media_ate_dia_28"] = np.where(base.sem_nota_ate_o_corte.values == 1, np.nan,
                                                  np.round(base.nota_media.values, 1))
        return saida

    risco = pd.concat([montar(treino, risco_treino, "Validação cruzada (2013)"),
                       montar(teste, risco_teste, "Modelo final (2014)")], ignore_index=True)
    risco[["faixa_de_risco", "ordem_faixa"]] = [faixa(r) for r in risco.risco]

    # ---- calibração: a nota prevista bate com o que aconteceu? (só no teste)
    cal = pd.DataFrame({"risco": risco_teste, "nao_concluiu": y_teste.values})
    cal["decimo"] = pd.qcut(cal.risco, 10, labels=False) + 1
    calibracao = cal.groupby("decimo").agg(risco_previsto=("risco", "mean"),
                                           taxa_observada=("nao_concluiu", "mean"),
                                           alunos=("risco", "size")).reset_index()
    calibracao["nome_do_decimo"] = calibracao.decimo.map(lambda d: f"{d}º")
    calibracao[["risco_previsto", "taxa_observada"]] = calibracao[["risco_previsto", "taxa_observada"]].round(4)

    # ---- peso de cada variável: quanto a AUC cai quando ela é embaralhada
    imp = permutation_importance(ajustados[escolhido], x_teste, y_teste, scoring="roc_auc",
                                 n_repeats=5, random_state=SEMENTE)
    variaveis = pd.DataFrame({"variavel": [VARIAVEIS[c][0] for c in colunas],
                              "familia": [VARIAVEIS[c][1] for c in colunas],
                              "peso": imp.importances_mean.clip(min=0).round(4)})
    variaveis = variaveis.sort_values("peso", ascending=False).reset_index(drop=True)
    variaveis["posicao"] = variaveis.index + 1

    limiares = pd.DataFrame({"limiar": np.round(np.arange(0.10, 0.91, 0.05), 2)})
    limiares["nome_do_limiar"] = limiares.limiar.map(lambda v: f"{v:.0%}")

    saidas = {"fRisco": (risco, "Nota de risco de cada matrícula ativa no dia 28"),
              "mlMetricas": (tab_metricas, "Qualidade dos modelos comparados"),
              "mlVariaveis": (variaveis, "Peso de cada variável na previsão"),
              "mlCalibracao": (calibracao, "Risco previsto contra resultado observado, em décimos"),
              "pLimiar": (limiares, "Limiares de risco para simular a lista do tutor")}
    for nome, (tabela, descricao) in saidas.items():
        tabela.to_parquet(MODELO / f"{nome}.parquet", index=False, compression="snappy")
        linhagem.append(("3. Modelo", nome, "src/alerta.py", len(tabela), tabela.shape[1], descricao))
        print(f"  modelo.{nome}: {len(tabela):,} linhas")
