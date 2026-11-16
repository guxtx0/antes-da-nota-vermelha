-- Dimensão dos tipos de atividade do AVA, agrupados pela finalidade pedagógica.
SELECT DISTINCT
    codigo_atividade,
    atividade,
    finalidade,
    ordem_atividade
FROM tratado.materiais
