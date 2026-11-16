-- Dimensão de turmas. As de 2013 ensinam o modelo de alerta; as de 2014 servem de prova.
SELECT
    chave_turma,
    curso,
    area,
    ordem_curso,
    ano,
    mes_de_inicio,
    turma,
    duracao_dias,
    CAST(ceil(duracao_dias / 7.0) AS INTEGER) AS duracao_semanas,
    CASE WHEN ano = 2013 THEN 'Turmas de 2013 (treino)' ELSE 'Turmas de 2014 (teste)' END AS papel_no_alerta,
    codigo_curso || ' ' || codigo_turma AS codigo_original
FROM tratado.turmas
