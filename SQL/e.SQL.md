# SQL

## 1. Informações gerais

- SQL é usado em bancos relacionais, muito comuns em OLTPs, que são transações online, e OLAPs, que são análises em grandes volumes
- O modelo relacional organiza os dados em tables, com colunas e linhas
- Essas tables seguem um schema, que define a estrutura dos dados, as relações e as regras
- SQL é conhecido por seguir as propriedades ACID:
  - Atomicidade: a operação acontece por completo ou não acontece
  - Consistência: toda mudança precisa respeitar as regras do schema
  - Isolamento: operações simultâneas não devem interferir incorretamente umas nas outras
  - Durabilidade: depois de confirmada, a operação deve continuar salva mesmo em caso de falha
- Performance depende de vários fatores, como hardware, indexes, estrutura do schema e modelo das queries
- Pode ser escalado verticalmente aumentando recursos como memória e CPU
- Também pode ser escalado horizontalmente com réplicas read-only, sharding ou estratégias específicas do banco
- APIs normalmente usam queries SQL para enviar, buscar, atualizar e remover informações

## 2. Schema

- Schema é a estrutura lógica do banco de dados
- O schema define:
  - Quais tabelas existem
  - Quais colunas cada tabela possui
  - O tipo de dado de cada coluna, como `INT`, `VARCHAR`, `DATE`, `BOOLEAN` e `TIMESTAMP`
  - Quais campos são obrigatórios ou opcionais
  - Chaves primárias, como `id`
  - Chaves estrangeiras, que criam relações entre tabelas
  - Regras de validação, como valores únicos, limites e valores padrão
  - Relações entre entidades, como um usuário tendo vários pedidos

## 3. Tables

- Tables são estruturas que armazenam dados em formato de linhas e colunas
- Cada coluna representa um atributo do dado, como `name`, `email` ou `created_at`
- Cada linha representa um registro completo dentro da tabela
- Tables seguem o schema definido, respeitando tipos de dados, chaves e regras

Exemplo:

```sql
CREATE TABLE users (
  id INT PRIMARY KEY,
  name VARCHAR(100),
  email VARCHAR(150) UNIQUE,
  created_at TIMESTAMP
);
```

- Nesse exemplo:
  - `users` é o nome da tabela
  - `id`, `name`, `email` e `created_at` são colunas
  - `INT`, `VARCHAR` e `TIMESTAMP` são tipos de dados
  - `PRIMARY KEY` garante que `id` identifique cada registro de forma única
  - `UNIQUE` impede emails repetidos

## 4. DDL - Comandos de estrutura

DDL significa Data Definition Language. São comandos usados para criar, alterar ou remover estruturas do banco

### CREATE TABLE

- `CREATE TABLE` é usado para criar uma tabela

```sql
CREATE TABLE users (
  id INT PRIMARY KEY,
  name VARCHAR(100),
  email VARCHAR(150) UNIQUE,
  created_at TIMESTAMP
);
```

- No MySQL, um `id` automático normalmente seria:

```sql
id INT AUTO_INCREMENT PRIMARY KEY
```

- No PostgreSQL, é comum usar:

```sql
id SERIAL PRIMARY KEY
```

### DROP TABLE

- `DROP TABLE` remove uma tabela inteira, incluindo sua estrutura e seus dados

```sql
DROP TABLE users;
```

- Diferente de `DELETE`, que remove linhas, `DROP` remove a tabela inteira

### TRUNCATE

- `TRUNCATE` remove todas as linhas de uma tabela, mas mantém a estrutura dela

```sql
TRUNCATE TABLE users;
```

- Ele costuma ser mais rápido que `DELETE FROM users`, porque o banco não trata linha por linha do mesmo jeito
- Use com cuidado, porque ele apaga todos os registros da tabela
- Em alguns bancos, também pode reiniciar contadores automáticos, como `SERIAL` ou `AUTO_INCREMENT`

PostgreSQL com reset de ids:

```sql
TRUNCATE TABLE users RESTART IDENTITY;
```

PostgreSQL removendo também dados de tabelas relacionadas:

```sql
TRUNCATE TABLE users CASCADE;
```

### CREATE INDEX

- `CREATE INDEX` cria um índice para melhorar a performance de buscas

```sql
CREATE INDEX idx_users_email
ON users (email);
```

- Nesse exemplo, criamos um índice na coluna `email`, deixando buscas por email mais rápidas
- Índices ajudam em consultas com `WHERE`, `JOIN`, `ORDER BY` e `GROUP BY`
- Índices também ocupam espaço e podem deixar `INSERT`, `UPDATE` e `DELETE` um pouco mais lentos

### DROP INDEX

- `DROP INDEX` remove um índice

PostgreSQL:

```sql
DROP INDEX idx_users_email;
```

MySQL:

```sql
ALTER TABLE users
DROP INDEX idx_users_email;
```

## 5. DML - Comandos de dados

DML significa Data Manipulation Language. São comandos usados para inserir, atualizar e remover registros

### INSERT INTO

- `INSERT INTO` insere novos registros em uma tabela

```sql
INSERT INTO users (name, email, created_at)
VALUES ('Fabio', 'fabio@email.com', CURRENT_TIMESTAMP);
```

- Nesse exemplo, adicionamos um usuário na tabela `users`

### UPDATE

- `UPDATE` altera registros que já existem

```sql
UPDATE users
SET email = 'novo@email.com'
WHERE id = 1;
```

- Nesse exemplo, alteramos o `email` do usuário com `id = 1`
- Normalmente `UPDATE` deve usar `WHERE`, para evitar alterar todos os registros da tabela

### DELETE

- `DELETE` remove linhas de uma tabela

```sql
DELETE FROM users
WHERE id = 1;
```

- Nesse exemplo, removemos o usuário com `id = 1`
- Sem `WHERE`, o `DELETE` pode remover todas as linhas da tabela

## 6. Transações

- Transações servem para agrupar várias operações como se fossem uma única operação
- Se tudo der certo, usamos `COMMIT`
- Se algo der errado, usamos `ROLLBACK`
- Isso tem ligação direta com ACID, principalmente atomicidade e consistência

### BEGIN

- `BEGIN` inicia uma transação

```sql
BEGIN;
```

### COMMIT

- `COMMIT` confirma as mudanças feitas dentro da transação

```sql
BEGIN;

UPDATE accounts
SET balance = balance - 100
WHERE id = 1;

UPDATE accounts
SET balance = balance + 100
WHERE id = 2;

COMMIT;
```

- Nesse exemplo, a transferência só é confirmada quando chega no `COMMIT`

### ROLLBACK

- `ROLLBACK` desfaz as mudanças feitas dentro da transação

```sql
BEGIN;

DELETE FROM users
WHERE id = 1;

ROLLBACK;
```

- Nesse exemplo, o `DELETE` é desfeito porque a transação não foi confirmada

### SAVEPOINT

- `SAVEPOINT` cria um ponto intermediário dentro da transação
- Ele permite desfazer só uma parte da transação, sem cancelar tudo

```sql
BEGIN;

UPDATE users
SET email = 'novo@email.com'
WHERE id = 1;

SAVEPOINT antes_do_delete;

DELETE FROM users
WHERE id = 2;

ROLLBACK TO SAVEPOINT antes_do_delete;

COMMIT;
```

- Nesse exemplo, o `UPDATE` continua valendo, mas o `DELETE` é desfeito

## 7. Consultas

### SELECT

- `SELECT` busca dados dentro de uma tabela

```sql
SELECT name, email
FROM users;
```

- Nesse exemplo, buscamos as colunas `name` e `email` da tabela `users`

### FROM

- `FROM` indica de qual tabela os dados serão buscados

```sql
SELECT *
FROM users;
```

- O `*` significa que queremos buscar todas as colunas da tabela

### WHERE

- `WHERE` filtra os dados retornados

```sql
SELECT *
FROM users
WHERE id = 1;
```

- Nesse exemplo, buscamos apenas o usuário cujo `id` é igual a `1`

### ORDER BY

- `ORDER BY` ordena os resultados

```sql
SELECT *
FROM users
ORDER BY created_at DESC;
```

- `DESC` ordena do maior para o menor, ou do mais recente para o mais antigo
- `ASC` ordena do menor para o maior, ou do mais antigo para o mais recente

### LIMIT

- `LIMIT` limita a quantidade de registros retornados

```sql
SELECT *
FROM users
LIMIT 10;
```

- Nesse exemplo, retornamos apenas 10 registros

### Filtro por datas

- Para buscar registros de um ano completo, prefira intervalo de datas

```sql
SELECT *
FROM compras
WHERE data_compra >= '2023-01-01'
  AND data_compra < '2024-01-01';
```

- Isso costuma ser melhor do que:

```sql
SELECT *
FROM compras
WHERE EXTRACT(YEAR FROM data_compra) = 2023;
```

- `EXTRACT` funciona, mas pode atrapalhar o uso de índices na coluna `data_compra`

## 8. Relacionamentos

### PRIMARY KEY

- `PRIMARY KEY` identifica cada registro de forma única

```sql
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  name VARCHAR(100) NOT NULL
);
```

- Nesse exemplo, `id` identifica cada usuário

### FOREIGN KEY

- `FOREIGN KEY` cria uma relação com outra tabela
- Ela garante que um valor em uma tabela exista em outra tabela

```sql
CREATE TABLE orders (
  id SERIAL PRIMARY KEY,
  user_id INT REFERENCES users(id),
  total NUMERIC(10, 2)
);
```

- Nesse exemplo:
  - `users.id` identifica o usuário
  - `orders.user_id` indica qual usuário fez o pedido
  - `REFERENCES users(id)` garante que o usuário exista

### JOIN

- `JOIN` combina dados de duas ou mais tabelas relacionadas
- Quando escrevemos apenas `JOIN`, normalmente estamos usando `INNER JOIN`

```sql
SELECT users.name, orders.total
FROM users
JOIN orders ON users.id = orders.user_id;
```

- Nesse exemplo:
  - `users.id` identifica cada usuário
  - `orders.user_id` aponta para `users.id`
  - O resultado mostra dados da tabela `users` junto com dados da tabela `orders`

### INNER JOIN

- `INNER JOIN` retorna apenas registros que têm correspondência nas duas tabelas

```sql
SELECT users.name, orders.total
FROM users
INNER JOIN orders ON users.id = orders.user_id;
```

- Se existir um usuário sem pedido, ele não aparece
- Se existir um pedido sem usuário correspondente, ele também não aparece

### LEFT OUTER JOIN

- `LEFT OUTER JOIN`, normalmente escrito como `LEFT JOIN`, retorna todos os registros da tabela da esquerda
- Se não houver correspondência na tabela da direita, os campos dela aparecem como `NULL`

```sql
SELECT users.name, orders.total
FROM users
LEFT JOIN orders ON users.id = orders.user_id;
```

- Nesse exemplo, todos os usuários aparecem, mesmo os que ainda não fizeram pedido

### RIGHT OUTER JOIN

- `RIGHT OUTER JOIN`, normalmente escrito como `RIGHT JOIN`, retorna todos os registros da tabela da direita
- Se não houver correspondência na tabela da esquerda, os campos dela aparecem como `NULL`

```sql
SELECT users.name, orders.total
FROM users
RIGHT JOIN orders ON users.id = orders.user_id;
```

- Nesse exemplo, todos os pedidos aparecem, mesmo que algum pedido não tenha usuário correspondente

### FULL OUTER JOIN

- `FULL OUTER JOIN` retorna tudo dos dois lados
- Quando não existe correspondência, o lado sem dados aparece como `NULL`

```sql
SELECT users.name, orders.total
FROM users
FULL OUTER JOIN orders ON users.id = orders.user_id;
```

- Nesse exemplo, aparecem usuários sem pedidos e pedidos sem usuário correspondente
- MySQL não tem `FULL OUTER JOIN` direto, então normalmente ele é simulado com `LEFT JOIN`, `RIGHT JOIN` e `UNION`

### INNER JOIN com tabela intermediária

Exemplo de schema:

```sql
CREATE TABLE produtos (
  id SERIAL PRIMARY KEY,
  nome VARCHAR(100) NOT NULL,
  preco NUMERIC(10, 2) NOT NULL
);

CREATE TABLE pedidos (
  id SERIAL PRIMARY KEY,
  cliente VARCHAR(100) NOT NULL,
  comprado_em TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE itens_pedido (
  pedido_id INT REFERENCES pedidos(id),
  produto_id INT REFERENCES produtos(id),
  quantidade INT NOT NULL,
  PRIMARY KEY (pedido_id, produto_id)
);
```

Query:

```sql
SELECT
  p.cliente AS nome_cliente,
  pr.nome AS nome_produto,
  ip.quantidade
FROM pedidos p
INNER JOIN itens_pedido ip ON p.id = ip.pedido_id
INNER JOIN produtos pr ON ip.produto_id = pr.id;
```

- `pedidos p` usa `p` como apelido para a tabela `pedidos`
- `itens_pedido ip` usa `ip` como apelido para a tabela intermediária
- `produtos pr` usa `pr` como apelido para a tabela `produtos`
- `p.id = ip.pedido_id` liga o pedido aos itens comprados
- `ip.produto_id = pr.id` liga cada item ao produto real
- Como é `INNER JOIN`, só aparecem registros com correspondência nas tabelas envolvidas

## 9. Agrupamento e agregações

### COUNT

- `COUNT` conta registros

```sql
SELECT COUNT(*) AS total_users
FROM users;
```

### GROUP BY

- `GROUP BY` agrupa resultados

```sql
SELECT user_id, COUNT(*) AS total_orders
FROM orders
GROUP BY user_id;
```

- Nesse exemplo, contamos quantos pedidos cada usuário tem

### HAVING

- `HAVING` filtra dados depois do agrupamento

```sql
SELECT user_id, COUNT(*) AS total_orders
FROM orders
GROUP BY user_id
HAVING COUNT(*) > 5;
```

- `WHERE` filtra linhas antes do agrupamento
- `HAVING` filtra grupos depois do agrupamento
- Nesse exemplo, retornamos apenas usuários com mais de 5 pedidos

## 10. ALTER TABLE

- `ALTER TABLE` modifica a estrutura de uma tabela existente

### ADD COLUMN

- Adiciona uma nova coluna

```sql
ALTER TABLE users
ADD COLUMN phone VARCHAR(20);
```

### DROP COLUMN

- Remove uma coluna

```sql
ALTER TABLE users
DROP COLUMN phone;
```

### MODIFY COLUMN

- No MySQL, `MODIFY COLUMN` muda o tipo ou propriedades de uma coluna

```sql
ALTER TABLE users
MODIFY COLUMN name VARCHAR(150) NOT NULL;
```

- Nesse exemplo, `name` passa a aceitar até 150 caracteres e não permite valor nulo

### ALTER COLUMN TYPE

- No PostgreSQL, `ALTER COLUMN ... TYPE` muda o tipo de dado de uma coluna

```sql
ALTER TABLE users
ALTER COLUMN name TYPE VARCHAR(150);
```

### RENAME COLUMN

- Renomeia uma coluna

```sql
ALTER TABLE users
RENAME COLUMN phone TO phone_number;
```

### RENAME TO

- Renomeia uma tabela

```sql
ALTER TABLE users
RENAME TO customers;
```

### ADD CONSTRAINT

- Adiciona uma regra na tabela

```sql
ALTER TABLE users
ADD CONSTRAINT unique_users_email UNIQUE (email);
```

- Nesse exemplo, impedimos emails repetidos

### DROP CONSTRAINT

- Remove uma constraint no PostgreSQL

```sql
ALTER TABLE users
DROP CONSTRAINT unique_users_email;
```

### ADD PRIMARY KEY

- Adiciona uma chave primária

```sql
ALTER TABLE users
ADD PRIMARY KEY (id);
```

### DROP PRIMARY KEY

- No MySQL, remove a chave primária

```sql
ALTER TABLE users
DROP PRIMARY KEY;
```

### ADD FOREIGN KEY

- Cria uma relação com outra tabela

```sql
ALTER TABLE orders
ADD CONSTRAINT fk_orders_users
FOREIGN KEY (user_id) REFERENCES users(id);
```

- Nesse exemplo, `orders.user_id` passa a referenciar `users.id`

### DROP FOREIGN KEY

- No MySQL, remove uma chave estrangeira

```sql
ALTER TABLE orders
DROP FOREIGN KEY fk_orders_users;
```

- No PostgreSQL, usa-se `DROP CONSTRAINT`

```sql
ALTER TABLE orders
DROP CONSTRAINT fk_orders_users;
```

### SET DEFAULT

- Define um valor padrão para uma coluna

```sql
ALTER TABLE users
ALTER COLUMN status SET DEFAULT 'active';
```

- Se nenhum valor for informado, `status` recebe `'active'`

### DROP DEFAULT

- Remove o valor padrão

```sql
ALTER TABLE users
ALTER COLUMN status DROP DEFAULT;
```

### SET NOT NULL

- Impede valores nulos, deixando a coluna obrigatória

```sql
ALTER TABLE users
ALTER COLUMN email SET NOT NULL;
```

### DROP NOT NULL

- Permite valores nulos

```sql
ALTER TABLE users
ALTER COLUMN email DROP NOT NULL;
```

### AUTO_INCREMENT

- No MySQL, `AUTO_INCREMENT` gera valores automáticos

```sql
ALTER TABLE users
MODIFY COLUMN id INT AUTO_INCREMENT;
```

### FIRST e AFTER

- No MySQL, `FIRST` e `AFTER` mudam a posição de uma coluna

```sql
ALTER TABLE users
MODIFY COLUMN email VARCHAR(150) AFTER name;
```

- Nesse exemplo, `email` passa a ficar depois de `name`

```sql
ALTER TABLE users
MODIFY COLUMN id INT FIRST;
```

- Nesse exemplo, `id` passa a ser a primeira coluna da tabela

## 11. Observações rápidas

- `NOT NULL` significa que a coluna é obrigatória
- `NULL` significa ausência de valor
- `''` significa string vazia, que ainda é um valor
- `DELETE` remove linhas
- `TRUNCATE` remove todas as linhas e mantém a tabela
- `DROP` remove estruturas
- `COMMIT` confirma uma transação
- `ROLLBACK` desfaz uma transação ainda não confirmada
- `WHERE` filtra antes do agrupamento
- `HAVING` filtra depois do agrupamento
- `INNER JOIN` retorna apenas registros que existem nos dois lados da relação
- `LEFT JOIN` mantém tudo da tabela da esquerda
- `RIGHT JOIN` mantém tudo da tabela da direita
- `FULL OUTER JOIN` mantém tudo dos dois lados
