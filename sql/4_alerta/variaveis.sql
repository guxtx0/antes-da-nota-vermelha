-- Variáveis do alerta precoce. Regra de ouro: só entra o que aconteceu ANTES do dia de corte.
-- Quem já tinha cancelado a matrícula até o corte fica de fora (não há mais o que prever).
-- Ficam de fora, por decisão ética: gênero, deficiência, região, idade e faixa de privação.
WITH base AS (
    SELECT
        m.chave_matricula,
        m.chave_turma,
        t.ano,
        CASE WHEN m.concluiu THEN 0 ELSE 1 END AS nao_concluiu,
        m.dia_matricula,
        m.tentativas_anteriores,
        m.creditos_em_curso,
        m.ordem_escolaridade AS nivel_de_escolaridade
    FROM modelo.dMatricula AS m
    JOIN modelo.dTurma AS t ON t.chave_turma = m.chave_turma
    WHERE m.dia_cancelamento IS NULL OR m.dia_cancelamento >= $dia_corte
),
acessos AS (
    SELECT
        a.chave_matricula,
        SUM(a.cliques)                                         AS cliques,
        SUM(CASE WHEN a.dia < 0 THEN a.cliques ELSE 0 END)     AS cliques_antes_do_inicio,
        COUNT(DISTINCT a.dia)                                  AS dias_com_acesso,
        COUNT(DISTINCT a.material)                             AS materiais_diferentes,
        $dia_corte - 1 - MAX(a.dia)                            AS dias_sem_acessar,
        COUNT(DISTINCT CASE WHEN a.dia >= 0 THEN floor(a.dia / 7.0) END) AS semanas_com_acesso,
        SUM(CASE WHEN a.dia BETWEEN $dia_corte - 7 AND $dia_corte - 1 THEN a.cliques ELSE 0 END)
          - SUM(CASE WHEN a.dia BETWEEN 0 AND 6 THEN a.cliques ELSE 0 END) AS variacao_de_cliques,
        SUM(CASE WHEN mt.finalidade = 'Estudo' THEN a.cliques ELSE 0 END)                    AS cliques_em_estudo,
        SUM(CASE WHEN mt.finalidade = 'Troca com colegas e tutor' THEN a.cliques ELSE 0 END) AS cliques_em_troca,
        SUM(CASE WHEN mt.finalidade = 'Prática e avaliação' THEN a.cliques ELSE 0 END)       AS cliques_em_pratica,
        SUM(CASE WHEN mt.finalidade = 'Navegação' THEN a.cliques ELSE 0 END)                 AS cliques_em_navegacao
    FROM tratado.acessos AS a
    JOIN tratado.materiais AS mt ON mt.material = a.material
    WHERE a.dia < $dia_corte
    GROUP BY 1
),
previstas AS (
    SELECT chave_turma, COUNT(*) AS avaliacoes_com_prazo_vencido
    FROM tratado.avaliacoes
    WHERE dia_do_prazo < $dia_corte
    GROUP BY 1
),
entregas AS (
    SELECT e.chave_matricula, COUNT(*) AS entregas, AVG(e.nota) AS nota_media
    FROM tratado.entregas AS e
    JOIN tratado.avaliacoes AS a ON a.avaliacao = e.avaliacao
    WHERE e.dia_da_entrega < $dia_corte AND a.dia_do_prazo < $dia_corte AND NOT e.nota_aproveitada
    GROUP BY 1
)
SELECT
    b.*,
    coalesce(ac.cliques, 0)                 AS cliques,
    coalesce(ac.cliques_antes_do_inicio, 0) AS cliques_antes_do_inicio,
    coalesce(ac.dias_com_acesso, 0)         AS dias_com_acesso,
    coalesce(ac.materiais_diferentes, 0)    AS materiais_diferentes,
    coalesce(ac.dias_sem_acessar, $dia_corte + 30) AS dias_sem_acessar,
    coalesce(ac.semanas_com_acesso, 0)      AS semanas_com_acesso,
    coalesce(ac.variacao_de_cliques, 0)     AS variacao_de_cliques,
    percent_rank() OVER (PARTITION BY b.chave_turma ORDER BY coalesce(ac.cliques, 0)) AS posicao_na_turma,
    coalesce(ac.cliques_em_estudo, 0)       AS cliques_em_estudo,
    coalesce(ac.cliques_em_troca, 0)        AS cliques_em_troca,
    coalesce(ac.cliques_em_pratica, 0)      AS cliques_em_pratica,
    coalesce(ac.cliques_em_navegacao, 0)    AS cliques_em_navegacao,
    coalesce(p.avaliacoes_com_prazo_vencido, 0) AS avaliacoes_com_prazo_vencido,
    CASE WHEN coalesce(p.avaliacoes_com_prazo_vencido, 0) = 0 THEN 1.0
         ELSE least(coalesce(en.entregas, 0) * 1.0 / p.avaliacoes_com_prazo_vencido, 1.0) END AS parcela_entregue,
    coalesce(en.nota_media, 0)              AS nota_media,
    CASE WHEN en.nota_media IS NULL THEN 1 ELSE 0 END AS sem_nota_ate_o_corte
FROM base AS b
LEFT JOIN acessos   AS ac ON ac.chave_matricula = b.chave_matricula
LEFT JOIN previstas AS p  ON p.chave_turma = b.chave_turma
LEFT JOIN entregas  AS en ON en.chave_matricula = b.chave_matricula
ORDER BY b.chave_matricula
