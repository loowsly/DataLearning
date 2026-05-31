# Chaves e pares (Key‑Value) em documentos MongoDB

## Conceitos básicos

- Um documento é uma coleção de pares `chave: valor` (como um `dict` em Python).
- Chaves são strings UTF‑8 e são case‑sensitive.
- A ordem das chaves **não** é semanticamente relevante, embora seja preservada na representação interna.

## Restrições e caracteres proibidos

- Não use `\0` (null) em nomes de campo.
- Evite começar nomes de campo com `$` (reservado para operadores) ou conter `.` (ponto) quando não representar navegação por campos aninhados.
- Se precisar armazenar chaves com `.` ou `$`, encode/escape a chave ou use uma estrutura alternativa (por exemplo, array de pares).

## Boas práticas de nomenclatura

- Use `snake_case` ou `camelCase` consistentemente conforme seu estilo de projeto.
- Prefira nomes curtos, descritivos e estáveis (mudar nomes de campo requer migração lógica).
- Evite campos dinâmicos ilimitados que poluam índices.

## Chaves e índices

- Índices são definidos por nomes de campo; criar índices em muitas chaves heterogêneas aumenta custo de armazenamento e manutenção.
- Use índices parciais e índices compostos quando apropriado.

## Exemplo PyMongo

```python
from pymongo import MongoClient

client = MongoClient()
db = client.exemplo
col = db.usuarios

doc = {
    "nome": "Lucas",
    "email": "lucas@example.com",
    "perfil_ativo": True
}

col.insert_one(doc)

# Acessar valor em Python
u = col.find_one({"email": "lucas@example.com"})
print(u["nome"])  # Lucas
```

## Quando usar pares dinâmicos

- Útil para metadados extensíveis (ex.: tags, atributos customizados), mas idealmente limite com um subdocumento específico ou array de pares para evitar explosão de índices.
