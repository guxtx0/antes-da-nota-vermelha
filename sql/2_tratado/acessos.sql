-- Log de acessos ao AVA. O arquivo original repete linhas para o mesmo aluno, material e dia;
-- aqui cada combinação vira uma linha só, somando os cliques (nenhum clique se perde).
SELECT
    code_module || '-' || code_presentation || '-' || id_student AS chave_matricula,
    CAST(id_site AS INTEGER)        AS material,
    CAST("date" AS INTEGER)         AS dia,
    SUM(CAST(sum_click AS INTEGER)) AS cliques
FROM bruto.student_vle
GROUP BY 1, 2, 3
