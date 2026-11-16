-- Uma linha por avaliação entregue. A turma vem do cadastro da avaliação, porque o arquivo
-- original só traz o número do aluno e o da avaliação.
SELECT
    a.code_module || '-' || a.code_presentation || '-' || s.id_student AS chave_matricula,
    CAST(s.id_assessment AS INTEGER)                    AS avaliacao,
    TRY_CAST(nullif(s.date_submitted, '?') AS INTEGER)  AS dia_da_entrega,
    s.is_banked = '1'                                   AS nota_aproveitada,
    TRY_CAST(nullif(s.score, '?') AS DOUBLE)            AS nota
FROM bruto.student_assessment AS s
JOIN bruto.assessments AS a ON a.id_assessment = s.id_assessment
