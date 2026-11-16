-- Calendário do curso em semanas. A semana 1 vai do dia 0 ao dia 6.
-- O dia 28, usado como corte do alerta, é o primeiro dia da semana 5.
SELECT
    semana,
    CASE WHEN semana = 0 THEN 'Antes do início' ELSE 'Semana ' || semana END AS nome_da_semana,
    CASE WHEN semana = 0 THEN 'Antes do início'
         WHEN semana <= 4 THEN 'Semanas 1 a 4'
         WHEN semana <= 20 THEN 'Semanas 5 a 20'
         ELSE 'Semana 21 em diante' END AS fase,
    CASE WHEN semana = 0 THEN 1 WHEN semana <= 4 THEN 2 WHEN semana <= 20 THEN 3 ELSE 4 END AS ordem_fase,
    CASE WHEN semana <= 4 THEN 'Até o dia 28' ELSE 'Depois do dia 28' END AS lado_do_corte,
    CASE WHEN semana = 0 THEN 'Antes'
         ELSE (CAST(floor((semana - 1) / 4.0) AS INTEGER) * 4 + 1)
              || ' a ' || least(CAST(floor((semana - 1) / 4.0) AS INTEGER) * 4 + 4, 39) END AS bloco_de_4_semanas,
    CASE WHEN semana = 0 THEN 0 ELSE CAST(floor((semana - 1) / 4.0) AS INTEGER) + 1 END AS ordem_bloco,
    semana >= 1 AS durante_o_curso
FROM (SELECT CAST(range AS INTEGER) AS semana FROM range(0, 40))
