-- Fato de presença: matrícula x semana. Dias com acesso não podem ser somados entre
-- tipos de atividade, por isso ficam numa tabela própria.
SELECT
    chave_matricula,
    CASE WHEN dia < 0 THEN 0 ELSE CAST(floor(dia / 7.0) AS INTEGER) + 1 END AS semana,
    CAST(SUM(cliques) AS INTEGER)          AS cliques,
    CAST(COUNT(DISTINCT dia) AS INTEGER)   AS dias_com_acesso
FROM tratado.acessos
GROUP BY 1, 2
