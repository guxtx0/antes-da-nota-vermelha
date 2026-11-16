-- Uma linha por matrícula (um aluno em uma turma), já com o cadastro em português.
-- O marcador '?' do arquivo original vira valor vazio. A faixa '10-20' vem sem o '%' e é corrigida aqui.
SELECT
    i.code_module || '-' || i.code_presentation || '-' || i.id_student AS chave_matricula,
    i.code_module || '-' || i.code_presentation                        AS chave_turma,
    CAST(i.id_student AS INTEGER)                                      AS aluno,
    tg.traducao                                                        AS genero,
    tr.traducao                                                        AS regiao,
    te.traducao                                                        AS escolaridade,
    CAST(te.ordem AS INTEGER)                                          AS ordem_escolaridade,
    ta.traducao                                                        AS faixa_etaria,
    CAST(ta.ordem AS INTEGER)                                          AS ordem_faixa_etaria,
    coalesce(tp.traducao, 'Não informada')                             AS faixa_privacao,
    coalesce(CAST(tp.ordem AS INTEGER), 99)                            AS ordem_faixa_privacao,
    CAST(i.num_of_prev_attempts AS INTEGER)                            AS tentativas_anteriores,
    CAST(i.studied_credits AS INTEGER)                                 AS creditos_em_curso,
    td.traducao                                                        AS declarou_deficiencia,
    tf.traducao                                                        AS resultado,
    CAST(tf.ordem AS INTEGER)                                          AS ordem_resultado,
    tf.grupo                                                           AS desfecho,
    TRY_CAST(nullif(r.date_registration, '?') AS INTEGER)              AS dia_matricula,
    TRY_CAST(nullif(r.date_unregistration, '?') AS INTEGER)            AS dia_cancelamento
FROM bruto.student_info AS i
LEFT JOIN bruto.student_registration AS r
       ON r.code_module = i.code_module
      AND r.code_presentation = i.code_presentation
      AND r.id_student = i.id_student
LEFT JOIN ref.traducoes AS tg ON tg.campo = 'genero'         AND tg.original = i.gender
LEFT JOIN ref.traducoes AS tr ON tr.campo = 'regiao'         AND tr.original = i.region
LEFT JOIN ref.traducoes AS te ON te.campo = 'escolaridade'   AND te.original = i.highest_education
LEFT JOIN ref.traducoes AS ta ON ta.campo = 'faixa_etaria'   AND ta.original = i.age_band
LEFT JOIN ref.traducoes AS tp ON tp.campo = 'faixa_privacao'
                             AND tp.original = CASE WHEN i.imd_band = '10-20' THEN '10-20%' ELSE i.imd_band END
LEFT JOIN ref.traducoes AS td ON td.campo = 'deficiencia'    AND td.original = i.disability
LEFT JOIN ref.traducoes AS tf ON tf.campo = 'resultado'      AND tf.original = i.final_result
