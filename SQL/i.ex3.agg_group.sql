Tabela
-- ==========================================================

CREATE TABLE funcionarios (
    id_funcionario INT PRIMARY KEY,
    nome VARCHAR(50),
    departamento VARCHAR(50),
    cargo VARCHAR(50),
    salario DECIMAL(10,2),
    projetos_ativos INT
);

INSERT INTO funcionarios VALUES 
(1, 'Ana Silva', 'Tecnologia', 'Desenvolvedora', 8000.00, 3),
(2, 'Bruno Costa', 'Tecnologia', 'Data Analyst', 6500.00, 2),
(3, 'Carlos Souza', 'Marketing', 'Designer', 4500.00, 4),
(4, 'Daniela Lima', 'RH', 'Analista de RH', 5000.00, 1),
(5, 'Eduardo Alves', 'Tecnologia', 'Gerente', 12000.00, 5),
(6, 'Fernanda Dias', 'Marketing', 'Copywriter', 4200.00, 2),
(7, 'Gabriel Cruz', 'RH', 'Psicólogo', 5500.00, 1),
(8, 'Helena Reis', 'Marketing', 'Gerente', 11000.00, 3);

-- ===========================================================
EXERCÍCIO:
Utilizando a tabela funcionarios, escreva uma única consulta SQL que agrupe os dados por departamento e retorne as seguintes informações:
O custo total da folha de pagamento (soma de todos os salários).
A média salarial paga aos funcionários daquele departamento.
O total de funcionários trabalhando na área.
O maior salário pago no departamento.
A soma total de todos os projetos ativos sob a responsabilidade do departamento.

-- ===========================================================
RESOLUÇÃO:
select departamento,
       sum(salario) as folha_pag,
       avg(salario) as mediaSal,
       count(*) as funcionarios,
       max(salario) as maiorSal,
       sum(projetos_ativos) as projetos
from funcionarios
group by departamento