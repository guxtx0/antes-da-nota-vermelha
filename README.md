# Antes da nota vermelha

O que as quatro primeiras semanas de um curso a distância já dizem sobre quem não vai concluir.

Este repositório acompanha 32.593 matrículas de uma universidade aberta, do arquivo bruto até a lista de
alunos que o tutor deve procurar. O trabalho passa por três frentes, e cada uma tem lugar próprio no código
e no painel.

| Frente | O que foi feito | Onde está |
|---|---|---|
| Engenharia de dados | Pipeline em três camadas, com tradução por tabela de-para, auditoria e testes automáticos | `sql/`, `src/camadas.py`, `src/auditoria.py`, `testes/`, `.github/workflows/` |
| Análise de dados | Modelo estrela, 56 medidas DAX e um painel de seis páginas | `powerbi/`, `docs/medidas.md` |
| Ciência de dados | Modelo de alerta precoce com corte no dia 28 e validação temporal | `sql/4_alerta/`, `src/alerta.py` |

## O que os dados mostram

- De cada 100 matrículas, 47 terminam em aprovação, 31 em desistência e 22 em reprovação.
- Metade das desistências (49,6%) acontece antes do dia 28. Oito em cada 100 alunos saem antes da primeira aula.
- Quem entrega o primeiro trabalho conclui em 61% dos casos. Quem não entrega, em 13%.
- Na quarta semana, 86% dos futuros concluintes acessam o ambiente virtual. Entre os demais, 51%.
- Com os dados dos primeiros 28 dias, o modelo chega a AUC de 0,753 em turmas que nunca viu.
- Com limiar de 60%, a lista do tutor reúne 28% da turma e acerta 73% dos nomes. Um sorteio acertaria 44%.

## Como abrir o painel

1. Extraia o zip inteiro, de preferência perto da raiz do disco (por exemplo, em `C:\`).
2. Dê dois cliques em `Abrir painel.bat`. Ele aponta o painel para a pasta `dados\3_modelo` deste projeto,
   esteja ela onde estiver, e abre o Power BI Desktop (versão de 2025 ou mais nova).
3. No Power BI, clique em **Atualizar**.

O painel lê os dados por um caminho completo, guardado no parâmetro `PastaDados`. Se preferir ajustar à mão,
abra `powerbi\AntesDaNotaVermelha.pbip`, vá em **Transformar dados > Editar parâmetros** e cole ali o caminho
completo da sua pasta `dados\3_modelo`.

Mantenha a pasta perto da raiz do disco: o formato de projeto do Power BI cria caminhos longos, e o Windows
recusa os que passam de 260 caracteres.

Depois de atualizar, compare alguns números com `docs/valores_de_conferencia.md`.

## Como refazer os dados

```bash
pip install -r requirements.txt
python src/executar.py    # baixa o dataset se dados/0_origem estiver vazia; leva menos de um minuto
pytest -q
```

A pasta `dados/3_modelo` já vem no repositório, então o painel abre sem rodar o pipeline.

## Engenharia: como os dados chegam ao painel

```
dados/0_origem   7 arquivos CSV, 10,9 milhões de linhas (não versionados)
      |  src/camadas.py: cópia fiel em Parquet
dados/1_bruto    tudo como texto, exatamente como veio
      |  sql/2_tratado: tipos, vazios, duplicatas e tradução
dados/2_tratado  seis tabelas limpas, em português
      |  sql/3_modelo: modelo estrela
      |  sql/4_alerta + src/alerta.py: nota de risco
      |  src/auditoria.py: linhagem, tratamentos e verificações
dados/3_modelo   quinze tabelas Parquet, lidas pelo Power BI
```

- Toda transformação é um arquivo `.sql` com uma única consulta. O Python só decide a ordem e grava o resultado.
- O DuckDB faz o papel de banco local. As consultas usam SQL padrão e rodam em outros bancos com poucos ajustes.
- A tradução usa a tabela `referencias/traducoes.csv`. Um teste falha se surgir na origem um valor sem tradução.
- A cada execução, 25 verificações conferem volume, chaves, integridade, faixas de valores e a qualidade do modelo.
  O resultado vai para o painel, na página de engenharia. Se uma verificação falha, o pipeline termina com erro.
- O GitHub Actions refaz tudo e roda os testes a cada alteração.

## Análise: como o painel foi pensado

Cada página abre com a conclusão escrita por extenso e mostra ao lado os gráficos que a sustentam.
As cores têm um só significado em todo o painel, tirado do boletim escolar: azul para quem conclui,
vermelho para quem não conclui.

O modelo tem quatro dimensões (turma, matrícula, semana, tipo de atividade) e quatro fatos (acessos, presença
semanal, entregas, risco). As medidas estão descritas em `docs/medidas.md`.

## Ciência: as escolhas do modelo de alerta

- **Corte no dia 28.** As variáveis só usam o que aconteceu antes do corte. Quem já tinha cancelado fica de fora.
- **Validação temporal.** O modelo aprende com as turmas de 2013 e é avaliado nas de 2014, como seria no uso real.
- **Notas de 2013 por validação cruzada.** O painel nunca mostra a previsão de um modelo que já tinha visto o aluno.
- **Sem variáveis sensíveis.** Gênero, deficiência, região, idade e faixa de privação não entram.
- **Dois modelos comparados.** Regressão logística e gradient boosting; fica o de maior AUC no teste.
- **Calibração conferida.** Em cada décimo de risco, a taxa prevista fica a menos de 10 pontos da observada.

## Limites

- Os dados são do Reino Unido, de 2013 e 2014. O método se transfere; os números, não.
- O alerta dispara no dia 28, quando metade dos desistentes já saiu. Para esses, o sinal teria de vir da matrícula.
- O alvo junta desistência e reprovação, que podem pedir intervenções diferentes.
- AUC de 0,75 serve para ordenar uma fila de contatos. Não serve para decidir sozinho sobre um aluno.

## Documentação

- `docs/guia_de_leitura.md`: como ler o painel, para quem não é da área
- `docs/dicionario_de_dados.md`: tabelas, colunas e relacionamentos
- `docs/medidas.md`: as medidas DAX, com descrição e fórmula
- `docs/traducao_dos_dados.md`: como cada termo do dataset foi traduzido
- `docs/valores_de_conferencia.md`: números para conferir o painel

## Fonte dos dados

Kuzilek, J., Hlosta, M. e Zdrahal, Z. (2017). Open University Learning Analytics dataset.
Scientific Data, 4, 170171. Licença CC BY 4.0. https://analyse.kmi.open.ac.uk/open_dataset

Os cadastros e as categorias foram traduzidos para o português neste projeto.
