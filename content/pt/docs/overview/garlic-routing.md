---
title: "Garlic Routing"
description: "Entendendo a terminologia, arquitetura e implementação do garlic routing no I2P"
slug: "garlic-routing"
aliases:
  - "/pt/how_garlicrouting"
  - "/pt/how_garlicrouting/"
lastUpdated: "2025-10"
accurateFor: "0.9.12"
---

## Garlic Routing e Terminologia "Garlic"

Os termos "garlic routing" e "garlic encryption" são frequentemente usados de forma imprecisa ao se referir à tecnologia do I2P. Aqui, explicamos a história dos termos, os vários significados e o uso dos métodos "garlic" no I2P.

"Garlic routing" foi cunhado pela primeira vez por [Michael J. Freedman](https://www.cs.princeton.edu/~mfreed/) na [tese de mestrado](https://www.freehaven.net/papers.html) de Roger Dingledine sobre Free Haven, Seção 8.1.1 (junho de 2000), como derivado do [Onion Routing](https://www.onion-router.net/).

"Garlic" pode ter sido usado originalmente pelos desenvolvedores do I2P porque o I2P implementa uma forma de agrupamento como Freedman descreve, ou simplesmente para enfatizar as diferenças gerais do Tor. O raciocínio específico pode ter se perdido na história. Geralmente, ao se referir ao I2P, o termo "garlic" pode significar uma de três coisas:

1. Criptografia em Camadas
2. Agrupamento de múltiplas mensagens juntas
3. Criptografia ElGamal/AES

Infelizmente, o uso da terminologia "garlic" pelo I2P ao longo dos anos nem sempre foi preciso; portanto, o leitor deve ter cautela ao encontrar o termo. Esperamos que a explicação abaixo torne as coisas claras.

### Criptografia em Camadas

O roteamento onion é uma técnica para construir caminhos, ou túneis, através de uma série de pares, e depois usar esse tunnel. As mensagens são criptografadas repetidamente pelo originador e então descriptografadas por cada salto. Durante a fase de construção, apenas as instruções de roteamento para o próximo salto são expostas a cada par. Durante a fase operacional, as mensagens são passadas através do tunnel, e a mensagem e suas instruções de roteamento são expostas apenas ao ponto final do tunnel.

Isto é semelhante à forma como o Mixmaster (veja [comparações de rede](/docs/overview/comparison/)) envia mensagens - pegando uma mensagem, criptografando-a com a chave pública do destinatário, pegando essa mensagem criptografada e criptografando-a (junto com instruções especificando o próximo salto), e então pegando essa mensagem criptografada resultante e assim por diante, até ter uma camada de criptografia por salto ao longo do caminho.

Neste sentido, "garlic routing" como conceito geral é idêntico ao "onion routing". Como implementado no I2P, é claro, existem várias diferenças da implementação no Tor; veja abaixo. Mesmo assim, há semelhanças substanciais de modo que o I2P se beneficia de uma [grande quantidade de pesquisa acadêmica sobre onion routing](https://www.onion-router.net/Publications.html), [Tor, e mixnets similares](https://freehaven.net/anonbib/topic.html).

### Agrupamento de Múltiplas Mensagens

Michael Freedman definiu "garlic routing" como uma extensão do onion routing, na qual múltiplas mensagens são agrupadas juntas. Ele chamou cada mensagem de "bulbo". Todas as mensagens, cada uma com suas próprias instruções de entrega, são expostas no endpoint. Isso permite o agrupamento eficiente de um "reply block" de onion routing com a mensagem original.

Este conceito é implementado no I2P, conforme descrito abaixo. Nosso termo para "bulbos" de garlic encryption são "dentes". Qualquer número de mensagens pode ser contido, em vez de apenas uma única mensagem. Esta é uma distinção significativa do onion routing implementado no Tor. No entanto, é apenas uma das muitas diferenças arquitetônicas principais entre I2P e Tor; talvez não seja, por si só, suficiente para justificar uma mudança na terminologia.

Outra diferença do método descrito por Freedman é que o caminho é unidirecional - não há "ponto de virada" como visto no roteamento onion ou nos blocos de resposta mixmaster, o que simplifica muito o algoritmo e permite uma entrega mais flexível e confiável.

### Criptografia ElGamal/AES

Em alguns casos, "garlic encryption" pode simplesmente significar criptografia [ElGamal/AES+SessionTag](/docs/specs/elgamal-aes/) (sem múltiplas camadas).

---

## Métodos "Garlic" no I2P

Agora que definimos vários termos "garlic", podemos dizer que o I2P usa garlic routing, agrupamento e criptografia em três lugares:

1. Para construir e rotear através de tunnels (criptografia em camadas)
2. Para determinar o sucesso ou falha da entrega de mensagens ponto a ponto (agrupamento)
3. Para publicar algumas entradas da base de dados da rede (reduzindo a probabilidade de um ataque bem-sucedido de análise de tráfego) (ElGamal/AES)

Também existem maneiras significativas pelas quais esta técnica pode ser usada para melhorar o desempenho da rede, explorando trade-offs entre latência/throughput de transporte, e ramificando dados através de caminhos redundantes para aumentar a confiabilidade.

### Construção e Roteamento de Tunnel

No I2P, os tunnels são unidirecionais. Cada parte constrói dois tunnels, um para tráfego de saída e um para tráfego de entrada. Portanto, quatro tunnels são necessários para uma única mensagem de ida e volta e resposta.

Tunnels são construídos e depois utilizados com criptografia em camadas. Isso é descrito na [página de implementação de tunnel](/docs/specs/tunnel-implementation/). Usamos [ElGamal/AES+SessionTag](/docs/specs/elgamal-aes/) para a criptografia.

Tunnels são um mecanismo de propósito geral para transportar todas as [mensagens I2NP](/docs/specs/i2np/), e as Garlic Messages não são usadas para construir tunnels. Não agrupamos múltiplas mensagens I2NP em uma única Garlic Message para desempacotamento no endpoint do tunnel de saída; a criptografia do tunnel é suficiente.

### Agrupamento de Mensagens de Ponta a Ponta

Na camada acima dos tunnels, o I2P entrega mensagens ponta-a-ponta entre [Destinations](/docs/specs/common-structures/). Assim como dentro de um único tunnel, usamos [ElGamal/AES+SessionTag](/docs/specs/elgamal-aes/) para a criptografia. Cada mensagem do cliente entregue ao router através da [interface I2CP](/docs/api/i2cp/) torna-se um único Garlic Clove com suas próprias Delivery Instructions, dentro de uma Garlic Message. As Delivery Instructions podem especificar um Destination, Router ou Tunnel.

Geralmente, uma Garlic Message conterá apenas um clove. No entanto, o router irá periodicamente agrupar dois cloves adicionais na Garlic Message:

![Garlic Message Cloves](/images/garliccloves.svg)

1. **Uma Mensagem de Status de Entrega**, com Instruções de Entrega especificando que ela deve ser enviada de volta ao router originário como uma confirmação. Isso é similar ao "bloco de resposta" ou "cebola de resposta" descrita nas referências. É usada para determinar o sucesso ou falha da entrega de mensagem de ponta a ponta. O router originário pode, ao falhar em receber a Mensagem de Status de Entrega dentro do período de tempo esperado, modificar o roteamento para o Destination de destino final, ou tomar outras ações.

2. **Uma Mensagem Database Store**, contendo um LeaseSet para o Destino de origem, com Instruções de Entrega especificando o router do destino remoto. Ao incluir periodicamente um LeaseSet, o router garante que a extremidade remota será capaz de manter as comunicações. Caso contrário, a extremidade remota teria que consultar um router floodfill para a entrada da base de dados da rede, e todos os LeaseSets teriam que ser publicados na base de dados da rede, conforme explicado na [página da base de dados da rede](/docs/specs/common-structures/).

Por padrão, as mensagens de Status de Entrega e Armazenamento de Base de Dados são agrupadas quando o LeaseSet local muda, quando Session Tags adicionais são entregues, ou se as mensagens não foram agrupadas no minuto anterior.

Obviamente, as mensagens adicionais são atualmente agrupadas para propósitos específicos, e não fazem parte de um esquema de roteamento de uso geral.

A partir da versão 0.9.12, a Mensagem de Status de Entrega é envolvida em outra Mensagem Garlic pelo originador, de modo que o conteúdo seja criptografado e não visível aos routers no caminho de retorno.

### Armazenamento na Base de Dados da Rede Floodfill

Conforme explicado na [página da base de dados da rede](/docs/specs/common-structures/), os LeaseSets locais são enviados para roteadores floodfill em uma Database Store Message envolvida em uma Garlic Message para que não seja visível ao gateway de saída do túnel.

---

## Trabalho Futuro

O mecanismo de Garlic Message é muito flexível e fornece uma estrutura para implementar muitos tipos de métodos de entrega de mixnet. Juntamente com a opção de atraso não utilizada nas Instruções de Entrega da mensagem do tunnel, um amplo espectro de estratégias de agrupamento, atraso, mistura e roteamento são possíveis.

Em particular, há potencial para muito mais flexibilidade no ponto final do tunnel de saída. As mensagens poderiam possivelmente ser roteadas de lá para um de vários tunnels (minimizando assim as conexões ponto-a-ponto), ou enviadas por multicast para vários tunnels para redundância, ou para streaming de áudio e vídeo.

Tais experimentos podem entrar em conflito com a necessidade de garantir segurança e anonimato, como limitar certas rotas de roteamento, restringir os tipos de mensagens I2NP que podem ser encaminhadas ao longo de vários caminhos e impor certos tempos de expiração de mensagem.

Como parte da criptografia ElGamal/AES, uma mensagem garlic contém uma quantidade de dados de preenchimento especificada pelo remetente, permitindo que o remetente tome contramedidas ativas contra análise de tráfego. Isso não é usado atualmente, além da exigência de preencher para um múltiplo de 16 bytes.

Criptografia de mensagens adicionais para e dos [floodfill routers](/docs/specs/common-structures/).

---

## Referências

- O termo garlic routing foi cunhado pela primeira vez na [tese de mestrado](https://www.freehaven.net/papers.html) de Roger Dingledine no Free Haven (junho de 2000), veja a Seção 8.1.1 escrita por [Michael J. Freedman](https://www.cs.princeton.edu/~mfreed/).
- [Publicações do Onion Router](https://www.onion-router.net/Publications.html)
- [Onion Routing (Wikipedia)](https://en.wikipedia.org/wiki/Onion_routing)
- [Garlic Routing (Wikipedia)](https://en.wikipedia.org/wiki/Garlic_routing)
- [Projeto Tor](https://www.torproject.org/)
- [Free Haven Anonbib](https://freehaven.net/anonbib/topic.html)
- O onion routing foi descrito pela primeira vez em [Hiding Routing Information](https://www.onion-router.net/Publications/IH-1996.pdf) por David M. Goldschlag, Michael G. Reed, e Paul F. Syverson em 1996.
