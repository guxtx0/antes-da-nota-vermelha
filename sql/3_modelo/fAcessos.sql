-- Fato de acessos: matrícula x semana x tipo de atividade.
-- É a tabela que responde "o que o aluno fez no AVA, e quando".
SELECT
    a.chave_matricula,
    CASE WHEN a.dia < 0 THEN 0 ELSE CAST(floor(a.dia / 7.0) AS INTEGER) + 1 END AS semana,
    m.codigo_atividade,
    CAST(SUM(a.cliques) AS INTEGER)   AS cliques,
    CAST(COUNT(DISTINCT a.material) AS INTEGER) AS materiais_diferentes
FROM tratado.acessos AS a
JOIN tratado.materiais AS m ON m.material = a.material
GROUP BY 1, 2, 3
