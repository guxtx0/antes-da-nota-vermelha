# Dicionário de dados

Tabelas da pasta `dados/3_modelo`, que são as que o Power BI lê. A primeira coluna traz o nome que aparece no painel; a segunda, o nome no arquivo Parquet.

Convenções: os dias são contados a partir do início da turma (dia 0), e dias negativos vêm antes do início. A semana 1 vai do dia 0 ao dia 6. A semana 0 reúne tudo o que acontece antes do primeiro dia de aula. O dia 28, usado como corte do alerta, é o primeiro dia da semana 5.

Prefixos: `d` para dimensões, `f` para fatos, `eng` para a auditoria do pipeline, `ml` para a avaliação do modelo e `p` para parâmetros do painel.

## dTurma

Uma linha por turma: o curso, a área, o ano e o papel da turma no alerta.

| No painel | No arquivo | Tipo | Observação |
|---|---|---|---|
| Chave da turma | `chave_turma` | Texto | oculta (chave ou ordenação) |
| Curso | `curso` | Texto | ordenada por Ordem do curso |
| Área | `area` | Texto |  |
| Ordem do curso | `ordem_curso` | Número inteiro | oculta (chave ou ordenação) |
| Ano | `ano` | Número inteiro |  |
| Mês de início | `mes_de_inicio` | Texto |  |
| Turma | `turma` | Texto |  |
| Duração em dias | `duracao_dias` | Número inteiro |  |
| Duração em semanas | `duracao_semanas` | Número inteiro |  |
| Papel no alerta | `papel_no_alerta` | Texto |  |
| Código original | `codigo_original` | Texto |  |

## dMatricula

Uma linha por matrícula: perfil do aluno, resultado final e momento da saída.

| No painel | No arquivo | Tipo | Observação |
|---|---|---|---|
| Chave da matrícula | `chave_matricula` | Texto | oculta (chave ou ordenação) |
| Chave da turma | `chave_turma` | Texto | oculta (chave ou ordenação) |
| Aluno | `aluno` | Número inteiro |  |
| Gênero | `genero` | Texto |  |
| Região | `regiao` | Texto |  |
| Escolaridade | `escolaridade` | Texto | ordenada por Ordem da escolaridade |
| Ordem da escolaridade | `ordem_escolaridade` | Número inteiro | oculta (chave ou ordenação) |
| Faixa etária | `faixa_etaria` | Texto | ordenada por Ordem da faixa etária |
| Ordem da faixa etária | `ordem_faixa_etaria` | Número inteiro | oculta (chave ou ordenação) |
| Faixa de privação | `faixa_privacao` | Texto | ordenada por Ordem da faixa de privação |
| Ordem da faixa de privação | `ordem_faixa_privacao` | Número inteiro | oculta (chave ou ordenação) |
| Tentativas anteriores | `tentativas_anteriores` | Número inteiro |  |
| Créditos em curso | `creditos_em_curso` | Número inteiro |  |
| Declarou deficiência | `declarou_deficiencia` | Texto |  |
| Resultado | `resultado` | Texto | ordenada por Ordem do resultado |
| Ordem do resultado | `ordem_resultado` | Número inteiro | oculta (chave ou ordenação) |
| Desfecho | `desfecho` | Texto |  |
| Concluiu | `concluiu` | Verdadeiro ou falso |  |
| Dia da matrícula | `dia_matricula` | Número inteiro |  |
| Dia do cancelamento | `dia_cancelamento` | Número inteiro |  |
| Semana do cancelamento | `semana_do_cancelamento` | Número inteiro |  |
| Saiu antes do início | `saiu_antes_do_inicio` | Verdadeiro ou falso |  |
| Situação no dia 28 | `situacao_no_dia_28` | Texto |  |
| Primeiro trabalho | `primeiro_trabalho` | Texto | ordenada por Ordem do primeiro trabalho |
| Ordem do primeiro trabalho | `ordem_primeiro_trabalho` | Número inteiro | oculta (chave ou ordenação) |

## dSemana

Calendário do curso em semanas. A semana 0 reúne o período antes do início das aulas.

| No painel | No arquivo | Tipo | Observação |
|---|---|---|---|
| Semana | `semana` | Número inteiro |  |
| Nome da semana | `nome_da_semana` | Texto | ordenada por Semana |
| Fase | `fase` | Texto | ordenada por Ordem da fase |
| Ordem da fase | `ordem_fase` | Número inteiro | oculta (chave ou ordenação) |
| Lado do corte | `lado_do_corte` | Texto |  |
| Bloco de 4 semanas | `bloco_de_4_semanas` | Texto | ordenada por Ordem do bloco |
| Ordem do bloco | `ordem_bloco` | Número inteiro | oculta (chave ou ordenação) |
| Durante o curso | `durante_o_curso` | Verdadeiro ou falso |  |

## dAtividade

Tipos de atividade do ambiente virtual, agrupados pela finalidade pedagógica.

| No painel | No arquivo | Tipo | Observação |
|---|---|---|---|
| Código da atividade | `codigo_atividade` | Texto | oculta (chave ou ordenação) |
| Atividade | `atividade` | Texto | ordenada por Ordem da atividade |
| Finalidade | `finalidade` | Texto |  |
| Ordem da atividade | `ordem_atividade` | Número inteiro | oculta (chave ou ordenação) |

## fAcessos

Cliques por matrícula, semana e tipo de atividade.

| No painel | No arquivo | Tipo | Observação |
|---|---|---|---|
| Chave da matrícula | `chave_matricula` | Texto | oculta (chave ou ordenação) |
| Semana do acesso | `semana` | Número inteiro | oculta (chave ou ordenação) |
| Código da atividade | `codigo_atividade` | Texto | oculta (chave ou ordenação) |
| Cliques | `cliques` | Número inteiro |  |
| Materiais diferentes | `materiais_diferentes` | Número inteiro |  |

## fPresenca

Presença semanal no ambiente virtual: cliques e dias com acesso por matrícula e semana.

| No painel | No arquivo | Tipo | Observação |
|---|---|---|---|
| Chave da matrícula | `chave_matricula` | Texto | oculta (chave ou ordenação) |
| Semana do acesso | `semana` | Número inteiro | oculta (chave ou ordenação) |
| Cliques | `cliques` | Número inteiro |  |
| Dias com acesso | `dias_com_acesso` | Número inteiro |  |

## fEntregas

Avaliações entregues, com prazo, nota e pontualidade.

| No painel | No arquivo | Tipo | Observação |
|---|---|---|---|
| Chave da matrícula | `chave_matricula` | Texto | oculta (chave ou ordenação) |
| Avaliação | `avaliacao` | Número inteiro |  |
| Tipo de avaliação | `tipo_de_avaliacao` | Texto | ordenada por Ordem do tipo |
| Ordem do tipo | `ordem_tipo` | Número inteiro | oculta (chave ou ordenação) |
| Peso | `peso` | Número decimal |  |
| Dia do prazo | `dia_do_prazo` | Número inteiro |  |
| Dia da entrega | `dia_da_entrega` | Número inteiro |  |
| Nota | `nota` | Número decimal |  |
| Dias de atraso | `dias_de_atraso` | Número inteiro |  |
| Pontualidade | `pontualidade` | Texto |  |
| Cor da nota | `cor_da_nota` | Texto |  |

## fRisco

Nota de risco de cada matrícula ativa no dia 28, com os sinais que a explicam.

| No painel | No arquivo | Tipo | Observação |
|---|---|---|---|
| Chave da matrícula | `chave_matricula` | Texto | oculta (chave ou ordenação) |
| Risco | `risco` | Número decimal |  |
| Origem da nota | `origem_da_nota` | Texto |  |
| Cliques até o dia 28 | `cliques_ate_dia_28` | Número inteiro |  |
| Dias com acesso até o dia 28 | `dias_com_acesso_ate_dia_28` | Número inteiro |  |
| Dias sem acessar no dia 28 | `dias_sem_acessar_no_dia_28` | Número decimal |  |
| Parcela entregue até o dia 28 | `parcela_entregue_ate_dia_28` | Número decimal |  |
| Nota média até o dia 28 | `nota_media_ate_dia_28` | Número decimal |  |
| Faixa de risco | `faixa_de_risco` | Texto | ordenada por Ordem da faixa |
| Ordem da faixa | `ordem_faixa` | Número inteiro | oculta (chave ou ordenação) |

## pLimiar

Limiares de risco para simular o tamanho da lista do tutor.

| No painel | No arquivo | Tipo | Observação |
|---|---|---|---|
| Limiar | `limiar` | Número decimal |  |
| Nome do limiar | `nome_do_limiar` | Texto | ordenada por Limiar |

## engLinhagem

Caminho de cada tabela pelo pipeline, com o volume em cada camada.

| No painel | No arquivo | Tipo | Observação |
|---|---|---|---|
| Ordem | `ordem` | Número inteiro |  |
| Camada | `camada` | Texto |  |
| Tabela | `tabela` | Texto | ordenada por Ordem |
| Origem | `origem` | Texto |  |
| Linhas | `linhas` | Número inteiro |  |
| Colunas | `colunas` | Número inteiro |  |
| O que acontece | `o_que_acontece` | Texto |  |

## engVerificacoes

Resultado de cada verificação de qualidade executada pelo pipeline.

| No painel | No arquivo | Tipo | Observação |
|---|---|---|---|
| Ordem | `ordem` | Número inteiro |  |
| Grupo | `grupo` | Texto |  |
| Verificação | `verificacao` | Texto | ordenada por Ordem |
| Regra | `regra` | Texto |  |
| Observado | `observado` | Número decimal |  |
| Situação | `situacao` | Texto |  |

## engTratamentos

O que foi corrigido nos dados de origem e quantos registros cada correção afetou.

| No painel | No arquivo | Tipo | Observação |
|---|---|---|---|
| Ordem | `ordem` | Número inteiro |  |
| Tratamento | `tratamento` | Texto | ordenada por Ordem |
| Onde | `onde` | Texto |  |
| Registros | `registros` | Número inteiro |  |
| Decisão | `decisao` | Texto |  |

## mlMetricas

Métricas de qualidade dos modelos comparados.

| No painel | No arquivo | Tipo | Observação |
|---|---|---|---|
| Modelo | `modelo` | Texto |  |
| Conjunto | `conjunto` | Texto |  |
| Métrica | `metrica` | Texto |  |
| Valor | `valor` | Número decimal |  |
| Escolhido | `escolhido` | Texto |  |

## mlVariaveis

Peso de cada variável na previsão: quanto a AUC cai quando ela é embaralhada.

| No painel | No arquivo | Tipo | Observação |
|---|---|---|---|
| Variável | `variavel` | Texto | ordenada por Posição |
| Família | `familia` | Texto |  |
| Peso | `peso` | Número decimal |  |
| Posição | `posicao` | Número inteiro |  |

## mlCalibracao

Risco previsto contra a taxa observada de não conclusão, em décimos das turmas de teste.

| No painel | No arquivo | Tipo | Observação |
|---|---|---|---|
| Décimo | `decimo` | Número inteiro |  |
| Risco previsto | `risco_previsto` | Número decimal |  |
| Taxa observada | `taxa_observada` | Número decimal |  |
| Alunos | `alunos` | Número inteiro |  |
| Nome do décimo | `nome_do_decimo` | Texto | ordenada por Décimo |

## Relacionamentos

Todos de muitos para um, com filtro em direção única, da dimensão para o fato.

| Tabela (lado muitos) | Coluna | Tabela (lado um) | Coluna |
|---|---|---|---|
| dMatricula | Chave da turma | dTurma | Chave da turma |
| fAcessos | Chave da matrícula | dMatricula | Chave da matrícula |
| fAcessos | Semana do acesso | dSemana | Semana |
| fAcessos | Código da atividade | dAtividade | Código da atividade |
| fPresenca | Chave da matrícula | dMatricula | Chave da matrícula |
| fPresenca | Semana do acesso | dSemana | Semana |
| fEntregas | Chave da matrícula | dMatricula | Chave da matrícula |
| fRisco | Chave da matrícula | dMatricula | Chave da matrícula |

A semana do cancelamento (em `dMatricula`) não se relaciona com `dSemana` de propósito: a curva de permanência compara as duas dentro da medida, o que deixa o calendário livre para filtrar os acessos.
