Tabela 
==================================================

CREATE TABLE estoque (
    id_item INT PRIMARY KEY,
    marca VARCHAR(50),
    tipo VARCHAR(50),
    quantidade INT
);

INSERT INTO estoque VALUES 
(1, 'Apple', 'iPhone', 10),
(2, 'Apple', 'MacBook', 5),
(3, 'Samsung', 'Galaxy', 15),
(4, 'Samsung', 'Book', 8);

====================================================

EXERCÍCIO:
Escreva uma consulta SQL utilizando ROLLUP que agrupe os dados por marca e tipo, 
mostrando a soma total da coluna quantidade. 
A consulta deve gerar os subtotais por marca e o total geral de itens no estoque.

select marca, 
       tipo,
       sum(quantidade) as estoques
from estoque
group by rollup(marca, tipo)
order by marca nulls last, tipo nulls last