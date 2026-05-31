# MongoDB - bases

## O que é MongoDB

MongoDB é um banco de dados NoSQL orientado a documentos. Em vez de tabelas e linhas, ele armazena dados em documentos parecidos com JSON, dentro de coleções.

Ele é usado quando se quer alta flexibilidade de schema, evolução rápida do modelo de dados e boa escalabilidade horizontal.

## Como funciona

O modelo básico é:

- Banco de dados
- Coleções
- Documentos

Uma coleção é um grupo de documentos relacionados. Cada documento é um conjunto de pares chave/valor e pode ter estrutura diferente dos outros documentos da mesma coleção.

Exemplo de documento:

```json
{
	"nome": "Ana",
	"idade": 28,
	"cidade": "Sao Paulo",
	"habilidades": ["Python", "SQL", "MongoDB"]
}
```

## Características principais

- Orientado a documentos.
- Schema flexível.
- Suporte a consultas ricas e indexação.
- Escalabilidade horizontal com sharding(particionar e dividir dados em diferentes servidores).
- Alta disponibilidade com replica sets.
- Boa adaptação para dados semi-estruturados e em mudança constante.

## JSON e BSON

MongoDB usa um formato inspirado em JSON para facilitar leitura e escrita, mas internamente trabalha com BSON.

### JSON

JSON é um formato textual, leve e fácil de ler por humanos e sistemas.

### BSON

BSON significa Binary JSON. É a representação binária usada pelo MongoDB para armazenar e transmitir documentos.

Vantagens do BSON:

- É mais eficiente para leitura e escrita interna.
- Suporta tipos extras além do JSON, como data, decimal, ObjectId e binário.
- Permite melhor desempenho em alguns cenários.

Exemplo de tipos que o BSON suporta melhor que o JSON puro:

- Data e hora.
- Identificadores únicos.
- Binários.
- Números com maior precisão.

## Estrutura flexível

Em MongoDB, cada documento pode ter campos diferentes. Isso reduz a dependência de migrações rígidas de schema.

Exemplo:

```json
{
	"nome": "Carlos",
	"email": "carlos@email.com"
}

{
	"nome": "Marina",
	"email": "marina@email.com",
	"telefone": "11999999999"
}
```

Isso é útil quando o domínio muda com frequência ou quando diferentes entidades compartilham uma coleção, mas com atributos extras diferentes.

## Dados polimórficos

Dados polimórficos são documentos que compartilham uma base comum, mas podem ter variações de estrutura conforme o tipo ou o contexto.

Exemplo: uma coleção de veículos pode ter carros e motos.

```json
{
	"tipo": "carro",
	"marca": "Fiat",
	"portas": 4
}

{
	"tipo": "moto",
	"marca": "Honda",
	"cilindradas": 160
}
```

Este modelo é comum em MongoDB porque a coleção não exige que todos os documentos tenham exatamente os mesmos campos.

## MongoDB Atlas

MongoDB Atlas é o serviço gerenciado na nuvem da MongoDB.

Com o Atlas, você pode:

- Criar clusters sem cuidar da infraestrutura manualmente.
- Fazer backup e restauração.
- Usar monitoramento e métricas.
- Aplicar regras de segurança e controle de acesso.
- Conectar aplicativos com facilidade.

É uma boa opção para desenvolvimento, homologação e produção quando se quer menos trabalho operacional.

## Resumo rápido

- MongoDB armazena dados em documentos.
- O formato externo lembra JSON, mas o formato interno é BSON.
- O schema é flexível e aceita documentos diferentes na mesma coleção.
- Isso ajuda em dados polimórficos e evolução rápida do modelo.
- Atlas é a versão gerenciada do MongoDB na nuvem.
