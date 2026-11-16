# Como os dados foram traduzidos

O dataset original está em inglês e usa o vocabulário da Open University. Para o painel fazer sentido a um leitor brasileiro, cada termo foi traduzido por uma tabela de-para (`referencias/traducoes.csv`), e não por texto fixo no código. Um teste falha se aparecer na origem um valor sem tradução.

## Vocabulário

| No dataset | Neste projeto | Por quê |
|---|---|---|
| module | curso | É a unidade em que o aluno se matricula e recebe um resultado final |
| presentation | turma | Uma oferta do curso, com início em fevereiro (B) ou outubro (J) |
| VLE | ambiente virtual, ou AVA | Equivale ao Moodle de uma instituição brasileira |
| TMA (tutor marked assessment) | trabalho corrigido pelo tutor | |
| CMA (computer marked assessment) | atividade de correção automática | |
| withdrawn | desistente | O aluno cancelou a matrícula |
| IMD band | faixa de privação | Índice britânico de privação da região onde o aluno mora; 0 a 10% é a faixa mais vulnerável |

## Pontos de atenção

- **Escolaridade.** O sistema britânico não tem equivalente exato no Brasil. *A Level* é a certificação que encerra o ensino secundário e dá acesso à universidade, por isso virou "Ensino médio completo"; *Lower than A Level* virou "Ensino médio incompleto".
- **Cursos.** Os códigos AAA a GGG são anônimos no dataset. Aqui viraram Curso A a Curso G. A área de cada um (ciências sociais ou exatas e tecnologia) vem da tabela de módulos do artigo que apresenta o dataset; confira essa tabela antes de citar a área em público.
- **Nota azul e nota vermelha.** No dataset, nota abaixo de 40 é insuficiente. A coluna "Cor da nota" usa a expressão brasileira para essa mesma regra.
- **Regiões.** São regiões do Reino Unido e da Irlanda, com o nome em português.

## Tabela de-para completa


### Gênero (`gender`)

| Original | Tradução | Grupo |
|---|---|---|
| M | Masculino |  |
| F | Feminino |  |

### Região (`region`)

| Original | Tradução | Grupo |
|---|---|---|
| East Anglian Region | Leste da Inglaterra |  |
| East Midlands Region | Midlands Orientais |  |
| Ireland | Irlanda |  |
| London Region | Londres |  |
| North Region | Norte da Inglaterra |  |
| North Western Region | Noroeste da Inglaterra |  |
| Scotland | Escócia |  |
| South East Region | Sudeste da Inglaterra |  |
| South Region | Sul da Inglaterra |  |
| South West Region | Sudoeste da Inglaterra |  |
| Wales | País de Gales |  |
| West Midlands Region | Midlands Ocidentais |  |
| Yorkshire Region | Yorkshire |  |

### Escolaridade na entrada (`highest_education`)

| Original | Tradução | Grupo |
|---|---|---|
| No Formal quals | Sem certificação formal |  |
| Lower Than A Level | Ensino médio incompleto |  |
| A Level or Equivalent | Ensino médio completo |  |
| HE Qualification | Ensino superior |  |
| Post Graduate Qualification | Pós-graduação |  |

### Faixa etária (`age_band`)

| Original | Tradução | Grupo |
|---|---|---|
| 0-35 | Até 35 anos |  |
| 35-55 | De 35 a 55 anos |  |
| 55<= | 55 anos ou mais |  |

### Faixa de privação (`imd_band`)

| Original | Tradução | Grupo |
|---|---|---|
| 0-10% | 0 a 10% (mais vulnerável) |  |
| 10-20% | 10 a 20% |  |
| 20-30% | 20 a 30% |  |
| 30-40% | 30 a 40% |  |
| 40-50% | 40 a 50% |  |
| 50-60% | 50 a 60% |  |
| 60-70% | 60 a 70% |  |
| 70-80% | 70 a 80% |  |
| 80-90% | 80 a 90% |  |
| 90-100% | 90 a 100% (menos vulnerável) |  |

### Declarou deficiência (`disability`)

| Original | Tradução | Grupo |
|---|---|---|
| Y | Sim |  |
| N | Não |  |

### Resultado final (`final_result`)

| Original | Tradução | Grupo |
|---|---|---|
| Distinction | Aprovado com distinção | Concluiu |
| Pass | Aprovado | Concluiu |
| Fail | Reprovado | Não concluiu |
| Withdrawn | Desistente | Não concluiu |

### Curso (`code_module`)

| Original | Tradução | Grupo |
|---|---|---|
| AAA | Curso A | Ciências sociais |
| BBB | Curso B | Ciências sociais |
| CCC | Curso C | Exatas e tecnologia |
| DDD | Curso D | Exatas e tecnologia |
| EEE | Curso E | Exatas e tecnologia |
| FFF | Curso F | Exatas e tecnologia |
| GGG | Curso G | Ciências sociais |

### Mês de início da turma (`code_presentation`)

| Original | Tradução | Grupo |
|---|---|---|
| B | Fevereiro | fev |
| J | Outubro | out |

### Tipo de avaliação (`assessment_type`)

| Original | Tradução | Grupo |
|---|---|---|
| TMA | Trabalho corrigido pelo tutor |  |
| CMA | Atividade de correção automática |  |
| Exam | Exame final |  |

### Tipo de atividade (`activity_type`)

| Original | Tradução | Grupo |
|---|---|---|
| oucontent | Conteúdo da disciplina | Estudo |
| resource | Arquivo para leitura | Estudo |
| url | Link externo | Estudo |
| page | Página de texto | Estudo |
| glossary | Glossário | Estudo |
| dataplus | Base de consulta | Estudo |
| dualpane | Conteúdo em painel duplo | Estudo |
| htmlactivity | Atividade interativa | Estudo |
| forumng | Fórum | Troca com colegas e tutor |
| oucollaborate | Sala de videoconferência | Troca com colegas e tutor |
| ouelluminate | Aula ao vivo | Troca com colegas e tutor |
| ouwiki | Wiki colaborativa | Troca com colegas e tutor |
| quiz | Questionário | Prática e avaliação |
| externalquiz | Questionário externo | Prática e avaliação |
| questionnaire | Pesquisa de opinião | Prática e avaliação |
| repeatactivity | Atividade de revisão | Prática e avaliação |
| homepage | Página inicial da turma | Navegação |
| subpage | Página de seção | Navegação |
| sharedsubpage | Página de seção compartilhada | Navegação |
| folder | Pasta | Navegação |
