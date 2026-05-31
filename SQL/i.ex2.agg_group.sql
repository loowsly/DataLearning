TABELA
=================================================================

CREATE TABLE vendas (
    id_venda INT PRIMARY KEY,
    produto VARCHAR(50),
    categoria VARCHAR(50),
    quantidade INT,
    valor_unitario DECIMAL(10,2),
    id_vendedor INT
);

INSERT INTO vendas VALUES 
(1, 'Notebook', 'Eletrônicos', 2, 3500.00, 101),
(2, 'Smartphone', 'Eletrônicos', 5, 2000.00, 101),
(3, 'Cadeira Gamer', 'Móveis', 3, 1200.00, 102),
(4, 'Mouse Sem Fio', 'Eletrônicos', 10, 150.00, 103),
(5, 'Mesa de Escritório', 'Móveis', 1, 800.00, 102),
(6, 'Monitor 24', 'Eletrônicos', 4, 1100.00, 101),
(7, 'Monitor 24', 'Eletrônicos', 2, 1100.00, 103),
(8, 'Sofá', 'Móveis', 1, 2500.00, 102);

EXERCÍCIO:
Utilizando a tabela vendas criada acima, escreva uma única consulta SQL que agrupe os dados por categoria e
retorne as seguintes informações para cada uma delas:
O total de dinheiro faturado (multiplicando a quantidade pelo valor unitário).
A média do valor unitário dos produtos vendidos.
A quantidade total de transações de vendas realizadas.
O maior valor unitário registrado naquela categoria.
A soma total de itens (quantidade) vendidos.

RESOLUÇÃO:
select  categoria, 
        sum(quantidade * valor_unitario) as total,
        avg(valor_unitario) as media, count(*) as qtd_vendas,
        max(valor_unitario) as maior_valor,
        sum(quantidade) as total_itens
from vendas
group by categoria;