# Valores de conferência

Depois de atualizar os dados no Power BI, confira alguns destes números. Eles foram recalculados em SQL, direto nas tabelas da pasta `dados/3_modelo`, sem passar pelo DAX. Se o painel mostrar os mesmos valores, o modelo, os relacionamentos e as medidas estão corretos.

## Capa e engenharia (sem nenhum filtro)

| Medida | Valor esperado |
|---|---|
| Linhas lidas na origem | 10.900.970 |
| Tabelas entregues ao painel | 15 |
| Placar das verificações | 25 de 25 |
| Registros tratados | 2.228.744 |

## Análise 1 (sem nenhum filtro)

| Medida | Valor esperado |
|---|---|
| Matrículas | 32.593 |
| Taxa de conclusão | 47,2% |
| Taxa de desistência | 31,2% |
| Taxa de reprovação | 21,6% |
| Saídas antes da primeira aula | 2.678 |
| Saídas até o dia 28 | 5.040 |
| Desistências até o dia 28 | 49,6% |
| Permanência na semana 0 | 91,8% |
| Permanência na semana 4 | 84,5% |
| Taxa de conclusão de quem tem Primeiro trabalho = Entregou | 61,0% |
| Taxa de conclusão de quem tem Primeiro trabalho = Não entregou | 13,2% |

## Análise 2 (sem nenhum filtro)

| Medida | Valor esperado |
|---|---|
| Total de cliques | 39.605.099 |
| Matrículas com acesso | 89,7% |
| Cliques por matrícula de quem concluiu | 2.068,2 |
| Cliques por matrícula de quem não concluiu | 452,4 |
| Vezes mais cliques de quem conclui | 4,6 |
| Com acesso entre quem concluiu, na semana 4 | 86,4% |
| Com acesso entre quem não concluiu, na semana 4 | 51,4% |
| Dias com acesso por semana, Curso A, bloco 1 a 4 | 3,2 |

## Ciência e decisão (páginas filtradas nas turmas de 2014, limiar em 60%)

| Medida | Valor esperado |
|---|---|
| AUC no teste | 0,753 |
| Alunos avaliados | 15.735 |
| Alunos na lista | 4.385 |
| Alertas certos | 3.184 |
| Acerto do alerta | 72,6% |
| Alcance do alerta | 46,0% |
| Parcela da turma na lista | 27,9% |
| Não conclusão entre os avaliados | 44,0% |
| Ganho sobre o acaso | 1,65 |
| Ficam fora da lista | 3.736 |
| Não conclusão na faixa Baixo (menos de 30%) | 21,9% |
| Não conclusão na faixa Médio (30% a 59%) | 43,5% |
| Não conclusão na faixa Alto (60% ou mais) | 72,6% |
