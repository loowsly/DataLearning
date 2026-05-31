# Embedding (Documentos embutidos) no MongoDB

Embedding é a prática de colocar subdocumentos diretamente dentro do documento pai (um documento dentro de outro). É uma ferramenta central no design de modelos em MongoDB e deve ser usada com cuidado.

## Por que embutir (embedding)?

- Reduz a necessidade de joins/lookup, melhorando a latência de leitura.
- Mantém dados fortemente acoplados juntos (ex.: usuário + endereço primário).
- Permite leitura consistente e simples (tudo em um único documento, leitura atômica).

## Quando preferir embedding

- Relações 1:1 ou 1:pequenos em que o subdocumento é sempre lido junto com o pai.
- Dados com baixa cardinalidade e crescimento limitado (ex.: endereços, preferências pequenas).
- Quando atualizações transacionais por documento são suficientes (operações atômicas por documento).

## Trade‑offs e limitações

- Tamanho do documento: limite de 16 MB. Embedding de coleções grandes pode exceder esse limite.
- Crescimento do documento: arrays embutidos que crescem indefinidamente podem causar relocations e queda de performance.
- Atualizações parciais: atualizações frequentes em subdocumentos grandes podem ser custosas.
- Indexação: é possível criar índices em campos embutidos (`campo.subcampo`), mas muitos índices ou arrays grandes afetam armazenamento e performance.

## Padrões comuns

- Embedded single object:
  - `user: { name, email, address: { street, city } }`
- Embedded array of subdocuments:
  - `post: { comments: [ {author, text, date}, ... ] }`
- Mix: embed dados essenciais, referenciar coleções grandes ou compartilhadas.

## Boas práticas

- Limite níveis de aninhamento (3–4 níveis preferíveis).
- Evite arrays que cresçam sem controle; se necessário, mova para coleção separada.
- Use `projection` para retornar só os campos necessários.
- Crie índices em campos embutidos usados em consultas frequentes.
- Monitore crescimento de documentos e relocations (profiler, métricas do Atlas/monitor).

## Exemplos PyMongo

```python
from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime

client = MongoClient()
db = client.exemplo
users = db.users
posts = db.posts

# Exemplo: embedding simples (endereço embutido)
users.insert_one({
    "nome": "Carla",
    "email": "carla@example.com",
    "endereco": {
        "rua": "Rua A",
        "cidade": "São Paulo",
        "cep": "01001-000"
    }
})

# Atualizar campo embutido
users.update_one({"email": "carla@example.com"}, {"$set": {"endereco.rua": "Rua B"}})

# Exemplo: array de subdocumentos (comentários)
post_id = posts.insert_one({
    "titulo": "Post sobre MongoDB",
    "conteudo": "...",
    "comentarios": [
        {"autor": "Ana", "texto": "Ótimo!", "data": datetime.utcnow()}
    ]
}).inserted_id

# Adicionar comentário sem duplicatas (usar $push ou $addToSet conforme necessidade)
posts.update_one({"_id": post_id}, {"$push": {"comentarios": {"autor": "Beto", "texto": "Bom post", "data": datetime.utcnow()}}})

# Atualizar primeiro comentário por posição
posts.update_one({"_id": post_id, "comentarios.autor": "Ana"}, {"$set": {"comentarios.$.texto": "Excelente!"}})

# Projetar apenas os dois primeiros comentários
doc = posts.find_one({"_id": post_id}, {"comentarios": {"$slice": 2}})

# Evitar arrays muito grandes: alternativa com coleção separada
# comments = db.comments
# comments.insert_one({"post_id": post_id, "autor": "C", "texto": "..."})
```

## Estratégias para crescimento e sharding

- Se um subdocumento/array tende a crescer muito, mova para coleção separada e use referência.
- Para workloads massivos de leitura/escrita, considere shard keys que evitem hotspots; embedding pode complicar shard choice se documentos crescerem desbalanceadamente.

## Considerações de consistência

- Atualizações por documento são atômicas; se precisar de atomicidade entre múltiplos documentos, use transações.
- Planeje estratégias de deleção/atualização para evitar inconsistências entre documentos referenciados.

## Resumo prático

- Embedding: ótimo para dados fortemente acoplados, leituras rápidas e simplicidade.
- Referência: escolha quando dados crescerão independentemente, forem compartilhados ou tiverem cardinalidade alta.
- Misture ambos quando necessário: embed para dados essenciais e referencie o que é volumoso ou compartilhado.