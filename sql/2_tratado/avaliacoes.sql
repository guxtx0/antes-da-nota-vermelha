-- Uma linha por avaliação prevista no plano de cada turma.
SELECT
    CAST(a.id_assessment AS INTEGER)              AS avaliacao,
    a.code_module || '-' || a.code_presentation   AS chave_turma,
    t.traducao                                    AS tipo_de_avaliacao,
    CAST(t.ordem AS INTEGER)                      AS ordem_tipo,
    TRY_CAST(nullif(a.date, '?') AS INTEGER)      AS dia_do_prazo,
    TRY_CAST(nullif(a.weight, '?') AS DOUBLE)     AS peso
FROM bruto.assessments AS a
LEFT JOIN ref.traducoes AS t ON t.campo = 'avaliacao' AND t.original = a.assessment_type
