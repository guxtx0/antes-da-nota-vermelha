-- Uma linha por material publicado no ambiente virtual (AVA), com o tipo traduzido e agrupado.
SELECT
    CAST(v.id_site AS INTEGER)                   AS material,
    v.code_module || '-' || v.code_presentation  AS chave_turma,
    v.activity_type                              AS codigo_atividade,
    t.traducao                                   AS atividade,
    t.grupo                                      AS finalidade,
    CAST(t.ordem AS INTEGER)                     AS ordem_atividade,
    TRY_CAST(nullif(v.week_from, '?') AS INTEGER) AS semana_prevista_inicio,
    TRY_CAST(nullif(v.week_to, '?') AS INTEGER)   AS semana_prevista_fim
FROM bruto.vle AS v
LEFT JOIN ref.traducoes AS t ON t.campo = 'atividade' AND t.original = v.activity_type
