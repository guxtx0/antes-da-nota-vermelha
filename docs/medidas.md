# Medidas DAX

As 56 medidas ficam na tabela `Medidas`, em pastas que seguem as etapas do trabalho. No Power BI, a descrição de cada uma aparece ao passar o mouse sobre o nome.

## 1 Engenharia

### Total de linhas

Linhas somadas das tabelas do pipeline.

```dax
SUM(engLinhagem[Linhas])
```

### Linhas lidas na origem

Total de linhas dos sete arquivos de origem.

```dax
CALCULATE([Total de linhas], engLinhagem[Camada] = "1. Bruto")
```

### Tabelas entregues ao painel

Quantidade de tabelas da camada de modelo.

```dax
CALCULATE(COUNTROWS(engLinhagem), engLinhagem[Camada] = "3. Modelo")
```

### Verificações

Verificações de qualidade executadas.

```dax
COUNTROWS(engVerificacoes)
```

### Verificações aprovadas

Verificações de qualidade que passaram.

```dax
CALCULATE(COUNTROWS(engVerificacoes), engVerificacoes[Situação] = "Passou") + 0
```

### Placar das verificações

Texto no formato 25 de 25.

```dax
[Verificações aprovadas] & " de " & [Verificações]
```

### Registros tratados

Registros afetados pelos tratamentos da camada tratada.

```dax
SUM(engTratamentos[Registros])
```

## 2 Análise > Resultado

### Matrículas

Uma matrícula é um aluno em uma turma.

```dax
COUNTROWS(dMatricula)
```

### Concluintes

Matrículas que terminaram em aprovação, com ou sem distinção.

```dax
CALCULATE([Matrículas], dMatricula[Desfecho] = "Concluiu")
```

### Taxa de conclusão

Parcela das matrículas que termina em aprovação.

```dax
DIVIDE([Concluintes], [Matrículas])
```

### Taxa de aprovação com distinção

Parcela das matrículas aprovadas com distinção.

```dax
DIVIDE(CALCULATE([Matrículas], dMatricula[Resultado] = "Aprovado com distinção"), [Matrículas])
```

### Taxa de aprovação simples

Parcela das matrículas aprovadas sem distinção.

```dax
DIVIDE(CALCULATE([Matrículas], dMatricula[Resultado] = "Aprovado"), [Matrículas])
```

### Desistentes

Matrículas canceladas pelo aluno.

```dax
CALCULATE([Matrículas], dMatricula[Resultado] = "Desistente")
```

### Taxa de desistência

Parcela das matrículas que termina em desistência.

```dax
DIVIDE([Desistentes], [Matrículas])
```

### Reprovados

Matrículas que foram até o fim e não atingiram a nota.

```dax
CALCULATE([Matrículas], dMatricula[Resultado] = "Reprovado")
```

### Taxa de reprovação

Parcela das matrículas que termina em reprovação.

```dax
DIVIDE([Reprovados], [Matrículas])
```

## 2 Análise > Permanência

### Saídas antes da primeira aula

Matrículas canceladas antes do dia 0.

```dax
CALCULATE([Matrículas], dMatricula[Saiu antes do início] = TRUE())
```

### Saídas até o dia 28

Matrículas canceladas antes do dia de corte do alerta.

```dax
CALCULATE([Matrículas], dMatricula[Situação no dia 28] = "Saiu antes do dia 28")
```

### Desistências até o dia 28

Parcela das desistências que acontece antes do dia de corte.

```dax
DIVIDE([Saídas até o dia 28], [Desistentes])
```

### Seguem matriculados

Matrículas que não tinham sido canceladas até o fim da semana em análise.

```dax
VAR SemanaAtual = MAX(dSemana[Semana])
RETURN
    CALCULATE(
        [Matrículas],
        FILTER(
            ALL(dMatricula[Semana do cancelamento]),
            ISBLANK(dMatricula[Semana do cancelamento])
                || dMatricula[Semana do cancelamento] > SemanaAtual
        )
    )
```

### Permanência

Parcela das matrículas que segue ativa ao fim da semana em análise.

```dax
DIVIDE([Seguem matriculados], [Matrículas])
```

### Cancelamentos na semana

Matrículas canceladas na semana em análise.

```dax
VAR SemanaAtual = MAX(dSemana[Semana])
RETURN
    CALCULATE(
        [Matrículas],
        FILTER(
            ALL(dMatricula[Semana do cancelamento]),
            NOT(ISBLANK(dMatricula[Semana do cancelamento]))
                && dMatricula[Semana do cancelamento] = SemanaAtual
        )
    )
```

## 2 Análise > Engajamento

### Total de cliques

Cliques registrados no ambiente virtual.

```dax
SUM(fAcessos[Cliques])
```

### Alunos com acesso

Matrículas com pelo menos um acesso no período em análise.

```dax
DISTINCTCOUNT(fPresenca[Chave da matrícula])
```

### Matrículas com acesso

Parcela das matrículas que acessou o ambiente virtual no período em análise.

```dax
DIVIDE([Alunos com acesso], [Matrículas])
```

### Com acesso entre quem concluiu

Parcela dos futuros concluintes com acesso no período.

```dax
CALCULATE([Matrículas com acesso], dMatricula[Desfecho] = "Concluiu")
```

### Com acesso entre quem não concluiu

Parcela dos futuros não concluintes com acesso no período.

```dax
CALCULATE([Matrículas com acesso], dMatricula[Desfecho] = "Não concluiu")
```

### Cliques por matrícula

Média de cliques por matrícula.

```dax
DIVIDE([Total de cliques], [Matrículas])
```

### Cliques por matrícula de quem concluiu

Média de cliques entre as matrículas que concluíram.

```dax
CALCULATE([Cliques por matrícula], dMatricula[Desfecho] = "Concluiu")
```

### Cliques por matrícula de quem não concluiu

Média de cliques entre as matrículas que não concluíram.

```dax
CALCULATE([Cliques por matrícula], dMatricula[Desfecho] = "Não concluiu")
```

### Vezes mais cliques de quem conclui

Quantas vezes o concluinte clica mais que o não concluinte.

```dax
DIVIDE([Cliques por matrícula de quem concluiu], [Cliques por matrícula de quem não concluiu])
```

### Dias com acesso por semana

Média de dias com acesso por matrícula em cada semana de aula. Vai de 0 a 7.

```dax
VAR SemanasDeAula = CALCULATE(DISTINCTCOUNT(dSemana[Semana]), dSemana[Durante o curso] = TRUE())
VAR Dias = CALCULATE(SUM(fPresenca[Dias com acesso]), dSemana[Durante o curso] = TRUE())
RETURN
    DIVIDE(Dias, [Matrículas] * SemanasDeAula)
```

### Entregas

Avaliações entregues.

```dax
COUNTROWS(fEntregas)
```

### Nota média

Média das notas, de 0 a 100.

```dax
AVERAGE(fEntregas[Nota])
```

## 3 Ciência

### AUC no teste

AUC do modelo escolhido nas turmas que ele nunca viu.

```dax
CALCULATE(
    MAX(mlMetricas[Valor]),
    mlMetricas[Escolhido] = "Sim",
    mlMetricas[Métrica] = "AUC",
    mlMetricas[Conjunto] = "Turmas de 2014 (teste)"
)
```

### Métrica no teste

Valor da métrica nas turmas de teste.

```dax
CALCULATE(MAX(mlMetricas[Valor]), mlMetricas[Conjunto] = "Turmas de 2014 (teste)")
```

### Peso da variável

Queda na AUC quando a variável é embaralhada.

```dax
SUM(mlVariaveis[Peso])
```

### Peso das 10 principais

Peso da variável, só para as dez mais importantes.

```dax
IF(MAX(mlVariaveis[Posição]) <= 10, [Peso da variável])
```

### Risco previsto médio

Risco médio previsto no décimo.

```dax
AVERAGE(mlCalibracao[Risco previsto])
```

### Não conclusão observada

Parcela que de fato não concluiu no décimo.

```dax
AVERAGE(mlCalibracao[Taxa observada])
```

## 4 Decisão

### Alunos avaliados

Matrículas ativas no dia 28, que recebem nota de risco.

```dax
COUNTROWS(fRisco)
```

### Limiar escolhido

Nota de risco a partir da qual o aluno entra na lista. Sem seleção, vale 60%.

```dax
SELECTEDVALUE(pLimiar[Limiar], 0.6)
```

### Alunos na lista

Alunos com nota de risco igual ou acima do limiar.

```dax
VAR Corte = [Limiar escolhido]
RETURN
    COUNTROWS(FILTER(fRisco, fRisco[Risco] >= Corte)) + 0
```

### Alertas certos

Alunos da lista que de fato não concluíram.

```dax
VAR Corte = [Limiar escolhido]
RETURN
    CALCULATE(
        COUNTROWS(FILTER(fRisco, fRisco[Risco] >= Corte)),
        dMatricula[Desfecho] = "Não concluiu"
    ) + 0
```

### Não concluintes avaliados

Alunos avaliados que não concluíram.

```dax
CALCULATE([Alunos avaliados], dMatricula[Desfecho] = "Não concluiu")
```

### Acerto do alerta

De cada 100 alunos da lista, quantos de fato não concluíram (precisão).

```dax
DIVIDE([Alertas certos], [Alunos na lista])
```

### Alcance do alerta

De cada 100 alunos que não concluíram, quantos estavam na lista (recall).

```dax
DIVIDE([Alertas certos], [Não concluintes avaliados])
```

### Parcela da turma na lista

Tamanho da lista em relação aos alunos avaliados.

```dax
DIVIDE([Alunos na lista], [Alunos avaliados])
```

### Não conclusão entre os avaliados

Taxa de não conclusão entre os alunos avaliados. É o acerto de uma lista montada ao acaso.

```dax
DIVIDE([Não concluintes avaliados], [Alunos avaliados])
```

### Ganho sobre o acaso

Quantas vezes a lista acerta mais do que um sorteio.

```dax
DIVIDE([Acerto do alerta], [Não conclusão entre os avaliados])
```

### Ficam fora da lista

Alunos que não concluíram e não entraram na lista.

```dax
[Não concluintes avaliados] - [Alertas certos]
```

### Risco do aluno

Nota de risco do aluno, exibida só para quem está na lista.

```dax
VAR Nota = MAX(fRisco[Risco])
RETURN
    IF(Nota >= [Limiar escolhido], Nota)
```

### Dias sem acessar do aluno

Dias desde o último acesso, contados no dia 28.

```dax
IF(NOT(ISBLANK([Risco do aluno])), MAX(fRisco[Dias sem acessar no dia 28]))
```

### Dias com acesso do aluno

Dias com acesso até o dia 28.

```dax
IF(NOT(ISBLANK([Risco do aluno])), MAX(fRisco[Dias com acesso até o dia 28]) + 0)
```

### Entregas do aluno

Parcela das avaliações com prazo vencido que o aluno entregou.

```dax
IF(NOT(ISBLANK([Risco do aluno])), MAX(fRisco[Parcela entregue até o dia 28]))
```

### Nota do aluno

Nota média nas entregas feitas até o dia 28.

```dax
IF(NOT(ISBLANK([Risco do aluno])), MAX(fRisco[Nota média até o dia 28]))
```
