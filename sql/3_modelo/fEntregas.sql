-- Fato de entregas: cada avaliação entregue, com prazo, nota e pontualidade.
SELECT
    e.chave_matricula,
    e.avaliacao,
    a.tipo_de_avaliacao,
    a.ordem_tipo,
    a.peso,
    a.dia_do_prazo,
    e.dia_da_entrega,
    e.nota,
    e.dia_da_entrega - a.dia_do_prazo AS dias_de_atraso,
    CASE WHEN a.dia_do_prazo IS NULL THEN 'Sem prazo registrado'
         WHEN e.dia_da_entrega <= a.dia_do_prazo THEN 'No prazo'
         ELSE 'Com atraso' END AS pontualidade,
    CASE WHEN e.nota IS NULL THEN 'Sem nota'
         WHEN e.nota >= 40 THEN 'Nota azul (40 ou mais)'
         ELSE 'Nota vermelha (abaixo de 40)' END AS cor_da_nota
FROM tratado.entregas AS e
JOIN tratado.avaliacoes AS a ON a.avaliacao = e.avaliacao
