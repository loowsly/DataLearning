Tabela Teste
=======================================================================================
DROP TABLE IF EXISTS historico_visualizacao;
DROP TABLE IF EXISTS filmes;
DROP TABLE IF EXISTS usuarios;

CREATE TABLE usuarios (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL 
);

CREATE TABLE filmes (
    id SERIAL PRIMARY KEY,
    titulo VARCHAR(150) NOT NULL,
    duracao_minutos INT NOT NULL
);

CREATE TABLE historico_visualizacao (
    usuario_id INT REFERENCES usuarios(id),
    filme_id INT REFERENCES filmes(id),
    assistido_em TIMESTAMPTZ DEFAULT NOW(),
    PRIMARY KEY (usuario_id, filme_id, assistido_em) 

INSERT INTO usuarios (nome, email) VALUES 
('Fábio', 'fabio@email.com'),
('Ana', 'ana@email.com');     

INSERT INTO filmes (titulo, duracao_minutos) VALUES 
('Interestelar', 169),      
('Matrix', 136),      
('O Início', 148);            

INSERT INTO historico_visualizacao (usuario_id, filme_id) VALUES 
(1, 1), -- Fábio viu Interestelar
(1, 2), -- Fábio viu Matrix
(2, 2); -- Ana viu Matrix
======================================================================================

Exercício:
Escreva uma consulta SQL que retorne uma lista com as seguintes colunas na tela:
O nome do usuário
O e-mail do usuário
O título do filme que ele assistiu
A data/hora em que ele assistiu 

Resolução:
select u.nome, u.email, f.titulo, hv.assistido_em
from usuarios u
inner join historico_visualizacao hv on u.id = hv.usuario_id
inner join filmes f on hv.filme_id = f.id;  