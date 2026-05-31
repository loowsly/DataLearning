# Modelo de documento no MongoDB

> MongoDB troca a rigidez de tabelas por documentos flexíveis e bem mais próximos de estruturas reais de aplicação.

## Mapa mental

| Conceito | Ideia |
| --- | --- |
| Collection | agrupamento lógico |
| Document | unidade principal de armazenamento |
| JSON | formato de leitura humana |
| BSON | formato binário interno do MongoDB |
| Schema flexível | cada documento pode variar |

## Visão geral

O MongoDB organiza dados em coleções e documentos. A coleção é o agrupamento lógico, e o documento é a unidade principal de armazenamento.

```mermaid
flowchart TB
	Collection[Collection]
	Doc1[Documento 1]
	Doc2[Documento 2]
	Doc3[Documento 3]

	Collection --> Doc1
	Collection --> Doc2
	Collection --> Doc3
```

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

## Modelagem prática

Em vez de pensar só em campos fixos, pense em:

- O que é comum entre os documentos.
- O que pode variar.
- O que deve ser aninhado em objetos.
- O que faz sentido virar array.

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

## Quando usar BSON mentalmente

Você não escreve BSON manualmente no dia a dia, mas precisa saber que o MongoDB entende tipos que JSON puro não cobre com tanta naturalidade.

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

Esse modelo é comum em MongoDB porque a coleção não exige que todos os documentos tenham exatamente os mesmos campos.

## Limitações

Apesar da flexibilidade, há limitações e pontos de atenção a considerar:

- Tamanho máximo de documento: um documento BSON não pode exceder 16 MB.
- Profundidade de aninhamento: níveis muito profundos tornam consultas e atualizações lentas e difíceis de manter.
- Indexação em campos aninhados e arrays: suportada via dot notation e índices multichave, porém indexar muitos campos heterogêneos pode degradar performance.
- Operações atômicas: atualizações são atômicas por documento; alterações que envolvam vários documentos podem precisar de transações.
- Consultas sobre arrays: operadores como `$elemMatch`, `$size` e `$slice` são necessários para consultas e projeções em arrays.
- Joins (`$lookup`): existem, mas são mais pesados que embedding; prefira embedding quando os dados tiverem coesão forte e cardinalidade baixa.

## Níveis de aninhamento (nesting)

Nesting (aninhamento) é a prática de colocar documentos dentro de documentos — criar "layers" de dados. Ajuda a modelar relações 1:1 ou 1:pequenos e reduz leituras necessárias.

Exemplo simples de camadas (layers):

```json
{
	"nome": "Ana",
	"enderecos": [
		{
			"tipo": "residencial",
			"rua": "Rua A",
			"coords": { "lat": -23.5, "lon": -46.6 }
		}
	],
	"habilidades": ["Python", "MongoDB"]
}
```

Consultas e atualizações em campos aninhados:

- Buscar por campo aninhado: `db.usuarios.find({ "enderecos.tipo": "residencial" })`
- Atualizar campo aninhado (dot notation): `db.usuarios.updateOne({ _id: id }, { $set: { "enderecos.0.rua": "Nova Rua" } })`
- Atualizar elemento de array por posição (operador posicional): `db.usuarios.updateOne({ "enderecos.tipo": "residencial" }, { $set: { "enderecos.$.rua": "Rua X" } })`
- Adicionar item a array: `db.usuarios.updateOne({ _id: id }, { $push: { habilidades: "Docker" } })`

Boas práticas de nesting:

- Embed quando os dados forem fortemente acoplados e não crescerem indefinidamente (ex.: endereços de um usuário).
- Use referência (guardar `_id` de outro documento) quando houver cardinalidade grande, crescimento independente ou necessidade de compartilhar o mesmo subdocumento entre muitos pais.
- Prefira consultar e projetar apenas os campos necessários para reduzir transferência de dados.

## Exemplo de documento

```json
{
	"nome": "Ana",
	"idade": 28,
	"endereco": {
		"cidade": "Sao Paulo",
		"uf": "SP"
	},
	"habilidades": ["Python", "SQL", "MongoDB"]
}
```