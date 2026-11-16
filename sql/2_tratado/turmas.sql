-- Uma linha por turma (oferta de um curso em um semestre).
-- No OULAD a turma se chama "presentation": o ano seguido de B (início em fevereiro) ou J (outubro).
SELECT
    c.code_module || '-' || c.code_presentation              AS chave_turma,
    c.code_module                                            AS codigo_curso,
    c.code_presentation                                      AS codigo_turma,
    tc.traducao                                              AS curso,
    tc.grupo                                                 AS area,
    CAST(tc.ordem AS INTEGER)                                AS ordem_curso,
    CAST(substr(c.code_presentation, 1, 4) AS INTEGER)       AS ano,
    ti.traducao                                              AS mes_de_inicio,
    tc.traducao || ', ' || ti.grupo || '/' || substr(c.code_presentation, 1, 4) AS turma,
    CAST(c.module_presentation_length AS INTEGER)            AS duracao_dias
FROM bruto.courses AS c
JOIN ref.traducoes AS tc ON tc.campo = 'curso'  AND tc.original = c.code_module
JOIN ref.traducoes AS ti ON ti.campo = 'inicio' AND ti.original = substr(c.code_presentation, 5, 1)
