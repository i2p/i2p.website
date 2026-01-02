---
title: "Entrega OBEP para Túneis de 1-em-N ou N-em-N"
number: "125"
author: "zzz, str4d"
created: "2016-03-10"
lastupdated: "2017-04-07"
status: "Open"
thread: "http://zzz.i2p/topics/2099"
toc: true
---

## Visão Geral

Esta proposta abrange duas melhorias para aprimorar o desempenho da rede:

- Delegar a seleção do IBGW para o OBEP, fornecendo a ele uma lista de
  alternativas em vez de uma única opção.

- Habilitar o roteamento de pacotes multicast no OBEP.


## Motivação

No caso de conexão direta, a ideia é reduzir a congestão de conexão, dando
flexibilidade ao OBEP em como ele se conecta aos IBGWs. A capacidade de especificar
múltiplos túneis também nos permite implementar multicast no OBEP (entregando a
mensagem para todos os túneis especificados).

Uma alternativa à parte de delegação desta proposta seria enviar através de um
hash [LeaseSet](http://localhost:63465/docs/specs/common-structures/#leaseset), semelhante à habilidade existente de especificar um hash
[RouterIdentity](http://localhost:63465/docs/specs/common-structures/#common-structure-specification) de destino. Isso resultaria em uma mensagem menor e em
potencialmente um LeaseSet mais recente. No entanto:

1. Isso forçaria o OBEP a fazer uma busca

2. O LeaseSet pode não ser publicado em um floodfill, então a busca falharia.

3. O LeaseSet pode estar criptografado, então o OBEP não conseguiria obter os
   leases.

4. Especificar um LeaseSet revela ao OBEP o [Destination](/docs/specs/common-structures/#destination) da mensagem,
   que ele poderia descobrir apenas vasculhando todos os LeaseSets na rede e
   procurando por uma correspondência de Lease.


## Design

O originador (OBGW) colocaria alguns (todos?) dos [Leases](http://localhost:63465/docs/specs/common-structures/#lease) de destino nas
instruções de entrega [TUNNEL-DELIVERY](/docs/specs/i2np/#tunnel-message-delivery-instructions) em vez de escolher apenas um.

O OBEP selecionaria um desses para entregar. O OBEP selecionaria, se
disponível, um ao qual ele já está conectado, ou já conhece. Isso faria o
caminho OBEP-IBGW mais rápido e mais confiável, e reduziria as conexões de
rede totais.

Temos um tipo de entrega não utilizado (0x03) e dois bits restantes (0 e 1) nos
flags para [TUNNEL-DELIVERY](/docs/specs/i2np/#tunnel-message-delivery-instructions), que podemos aproveitar para implementar esses
recursos.


## Implicações de Segurança

Esta proposta não altera a quantidade de informações vazadas sobre o destino
alvo do OBGW ou sua visão do NetDB:

- Um adversário que controla o OBEP e está coletando LeaseSets do NetDB já pode
  determinar se uma mensagem está sendo enviada para um Destino específico,
  buscando o par [TunnelId](http://localhost:63465/docs/specs/common-structures/#tunnelid) / [RouterIdentity](http://localhost:63465/docs/specs/common-structures/#common-structure-specification). Na pior das hipóteses, a
  presença de vários Leases no TMDI pode tornar mais rápido encontrar uma
  correspondência no banco de dados do adversário.

- Um adversário que está operando um Destino malicioso já pode obter
  informações sobre a visão de NetDB de uma vítima conectada, publicando
  LeaseSets contendo diferentes túneis de entrada para diferentes floodfills, e
  observando por quais túneis o OBGW conecta. Do ponto de vista deles, o OBEP
  selecionando qual túnel usar é funcionalmente idêntico ao OBGW fazendo a
  seleção.

O flag de multicast vaza o fato de que o OBGW está fazendo multicast para os
OBEPs. Isso cria uma troca entre desempenho e privacidade que deve ser
considerada ao implementar protocolos de nível mais alto. Sendo um flag
opcional, os usuários podem tomar a decisão apropriada para sua aplicação. Podem
haver benefícios de isso ser o comportamento padrão para aplicações compatíveis,
contudo, como o uso generalizado por uma variedade de aplicações reduziria o
vazamento de informações sobre de qual aplicação específica uma mensagem vem.


## Especificação

As Instruções de Entrega do Primeiro Fragmento [TUNNEL-DELIVERY](/docs/specs/i2np/#tunnel-message-delivery-instructions) seriam
modificadas da seguinte forma:

```
+----+----+----+----+----+----+----+----+
|flag|  Tunnel ID (opt)  |              |
+----+----+----+----+----+              +
|                                       |
+                                       +
|         To Hash (optional)            |
+                                       +
|                                       |
+                        +----+----+----+
|                        |dly | Message  
+----+----+----+----+----+----+----+----+
 ID (opt) |extended opts (opt)|cnt | (o)
+----+----+----+----+----+----+----+----+
 Tunnel ID N   |                        |
+----+----+----+                        +
|                                       |
+                                       +
|         To Hash N (optional)          |
+                                       +
|                                       |
+              +----+----+----+----+----+
|              | Tunnel ID N+1 (o) |    |
+----+----+----+----+----+----+----+    +
|                                       |
+                                       +
|         To Hash N+1 (optional)        |
+                                       +
|                                       |
+                                  +----+
|                                  | sz
+----+----+----+----+----+----+----+----+
     |
+----+

flag ::
       1 byte
       Ordem dos bits: 76543210
       bits 6-5: tipo de entrega
                 0x03 = TUNNELS
       bit 0: multicast? Se 0, entregar para um dos túneis
                         Se 1, entregar para todos os túneis
                         Definir para 0 para compatibilidade com usos
                         futuros se o tipo de entrega não for TUNNELS

Count ::
       1 byte
       Opcional, presente se o tipo de entrega for TUNNELS
       2-255 - Número de pares id/hash a seguir

Tunnel ID :: `TunnelId`
To Hash ::
       36 bytes cada
       Opcional, presente se o tipo de entrega é TUNNELS
       pares id/hash

Comprimento total: O comprimento típico é:
       75 bytes para entrega TUNNELS com contagem 2 (mensagem de túnel
       não fragmentada);
       79 bytes para entrega TUNNELS com contagem 2 (primeiro fragmento)

Resto das instruções de entrega inalterado
```


## Compatibilidade

Os únicos pares que precisam entender a nova especificação são os OBGWs e os
OBEPs. Portanto, podemos tornar esta mudança compatível com a rede existente
tornando seu uso condicional na versão I2P alvo [VERSIONS](/docs/specs/i2np/#protocol-versions):

* Os OBGWs devem selecionar OBEPs compatíveis ao construir túneis de saída,
  com base na versão I2P anunciada em seu [RouterInfo](http://localhost:63465/docs/specs/common-structures/#routerinfo).

* Pares que anunciam a versão alvo devem suportar a análise dos novos flags,
  e não devem rejeitar as instruções como inválidas.

