-- Dimensão de matrículas: quem é o aluno, como terminou e quando saiu (se saiu).
-- A semana 0 reúne tudo o que acontece antes do primeiro dia de aula.
-- O "primeiro trabalho" é a primeira avaliação corrigida pelo tutor prevista para a turma.
WITH primeiro_trabalho AS (
    SELECT chave_turma, avaliacao, dia_do_prazo
    FROM (
        SELECT chave_turma, avaliacao, dia_do_prazo,
               row_number() OVER (PARTITION BY chave_turma ORDER BY dia_do_prazo, avaliacao) AS posicao
        FROM tratado.avaliacoes
        WHERE tipo_de_avaliacao = 'Trabalho corrigido pelo tutor' AND dia_do_prazo IS NOT NULL
    ) AS ordenadas
    WHERE posicao = 1
),
entregou AS (
    SELECT DISTINCT e.chave_matricula
    FROM tratado.entregas AS e
    JOIN primeiro_trabalho AS p ON p.avaliacao = e.avaliacao
)
SELECT
    m.chave_matricula,
    m.chave_turma,
    aluno,
    genero,
    regiao,
    escolaridade,
    ordem_escolaridade,
    faixa_etaria,
    ordem_faixa_etaria,
    faixa_privacao,
    ordem_faixa_privacao,
    tentativas_anteriores,
    creditos_em_curso,
    declarou_deficiencia,
    resultado,
    ordem_resultado,
    desfecho,
    desfecho = 'Concluiu' AS concluiu,
    dia_matricula,
    dia_cancelamento,
    CASE WHEN dia_cancelamento IS NULL THEN NULL
         WHEN dia_cancelamento < 0 THEN 0
         ELSE CAST(floor(dia_cancelamento / 7.0) AS INTEGER) + 1 END AS semana_do_cancelamento,
    coalesce(dia_cancelamento < 0, FALSE) AS saiu_antes_do_inicio,
    CASE WHEN dia_cancelamento IS NULL OR dia_cancelamento >= 28
         THEN 'Seguia matriculado no dia 28' ELSE 'Saiu antes do dia 28' END AS situacao_no_dia_28,
    CASE WHEN en.chave_matricula IS NOT NULL THEN 'Entregou'
         WHEN m.dia_cancelamento IS NOT NULL AND m.dia_cancelamento <= p.dia_do_prazo THEN 'Saiu antes do prazo'
         ELSE 'Não entregou' END AS primeiro_trabalho,
    CASE WHEN en.chave_matricula IS NOT NULL THEN 1
         WHEN m.dia_cancelamento IS NOT NULL AND m.dia_cancelamento <= p.dia_do_prazo THEN 3
         ELSE 2 END AS ordem_primeiro_trabalho
FROM tratado.matriculas AS m
LEFT JOIN primeiro_trabalho AS p ON p.chave_turma = m.chave_turma
LEFT JOIN entregou AS en ON en.chave_matricula = m.chave_matricula
