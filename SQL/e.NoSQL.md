# NoSQL

- São dividos em key-values, graphs, documents ou column-family
- São eficientes para OLTPs que exigem grande volume de informações e baixa latência e análises de dados semiestruturados
- Não tem um padrão especifico de modelo, visto que podem ser analisados em várias formas, como key-values, docs, graphs e etc
- Bancos NoSQL fornecem as propriedades BASE(Basicamente acessível, Estado Flexível, Consistência Eventual), de maneira flexível ao contrário do SQL, ou seja a consistência aqui é eventual(depende da escolha de arquitetura), apesar de que alguns bancos NoSQL podem oferecer ACID até certo ponto
- Performance aqui é relacionada ao hardware também, mas além disso, à latência da rede e à própria aplicação
- Pode ser escalado ao ser particionado, horizontalmente, distribuindo cópias pela arquitetura
- APIs baseadas em objetos que podem enviar e receber diretamente da memória, ou pares de chaves que controlam dados de documentos semiestruturados(sem tabelas fixas), ex:
```
{
  "nome": "Carlos",
  "idade": 30,
  "hobbies": ["futebol", "leitura"]
}
```
- Além de poderem oferecer linguagens prórpias de query e leitura de json