# MongoDB - bases

## Mapa do conteúdo

| Arquivo | Tema |
| --- | --- |
| [Architecture.md](Architecture.md) | processos, nodes, clusters, replica set, sharding e Atlas |
| [DocumentModel.md](DocumentModel.md) | collections, documents, JSON, BSON e dados polimórficos |
| [Embedding.md](Embedding.md) | embedding (documentos embutidos) — trade‑offs e exemplos |
| [References.md](References.md) | referências, `$lookup` e padrões de relacionamento |
| [DocRelationships.md](DocRelationships.md) | padrões 1:1, 1:N, N:N e estratégias de modelagem |
| [Entities.md](Entities.md) | entidades, agregados, validação e versionamento |
| [DataTypes.md](DataTypes.md) | tipos BSON e mapeamento para PyMongo |
| [Arrays.md](Arrays.md) | arrays, operadores e índices multichave |
| [KeyPairs.md](KeyPairs.md) | nomes de campo, restrições e boas práticas |
| [Documents.md](Documents.md) | operações, atomicidade e projeções |
| [Commands.md](Commands.md) | comandos básicos em Python com PyMongo |
| [CRUD.md](CRUD.md) | operações CRUD em Python |
| [Tiers.md](Tiers.md) | planos de cluster m0, m2 e m10 no MongoDB Atlas |

## O que é MongoDB

MongoDB é um banco de dados NoSQL orientado a documentos. Em vez de tabelas e linhas, ele armazena dados em documentos parecidos com JSON, dentro de coleções.

Ele é usado quando se quer alta flexibilidade de schema, evolução rápida do modelo de dados e boa escalabilidade horizontal.

## Por que estudar assim

| Vantagem | O que isso resolve |
| --- | --- |
| Schema flexível | facilita mudanças rápidas no modelo |
| Estrutura documental | combina bem com dados semi-estruturados |
| Escala horizontal | ajuda em bases maiores e distribuídas |
| Leitura natural | o modelo lembra JSON e é fácil de visualizar |

## Conceitos centrais

- Banco de dados
- Coleções
- Documentos

Cada coleção agrupa documentos relacionados, e cada documento pode ter estrutura diferente dentro da mesma coleção.
