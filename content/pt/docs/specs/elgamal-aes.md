---
title: "Criptografia ElGamal/AES + SessionTag"
description: "Criptografia end-to-end legada combinando ElGamal, AES, SHA-256 e tags de sessão únicas"
slug: "elgamal-aes"
aliases:
  - "/pt/how_elgamalaes"
  - "/pt/how_elgamalaes/"
lastUpdated: "2020-04"
accurateFor: "0.9.46"
---

## Visão Geral

ElGamal/AES+SessionTags é usado para criptografia ponta a ponta.

Como um sistema não confiável, desordenado e baseado em mensagens, o I2P usa uma combinação simples de algoritmos de criptografia assimétrica e simétrica para fornecer confidencialidade e integridade dos dados às garlic messages. Como um todo, a combinação é referida como ElGamal/AES+SessionTags, mas essa é uma forma excessivamente verbosa de descrever o uso de ElGamal de 2048bit, AES256, SHA256 e nonces de 32 bytes.

Na primeira vez que um router quer criptografar uma mensagem garlic para outro router, eles criptografam o material de chaveamento para uma chave de sessão AES256 com ElGamal e anexam o payload criptografado AES256/CBC após esse bloco ElGamal criptografado. Além do payload criptografado, a seção criptografada AES contém o comprimento do payload, o hash SHA256 do payload não criptografado, bem como um número de "session tags" - nonces aleatórios de 32 bytes. Na próxima vez que o remetente quiser criptografar uma mensagem garlic para outro router, em vez de criptografar ElGamal uma nova chave de sessão, eles simplesmente escolhem uma das session tags previamente entregues e criptografam AES o payload como antes, usando a chave de sessão usada com essa session tag, precedida pela própria session tag. Quando um router recebe uma mensagem criptografada garlic, eles verificam os primeiros 32 bytes para ver se correspondem a uma session tag disponível - se corresponder, eles simplesmente descriptografam AES a mensagem, mas se não corresponder, eles descriptografam ElGamal o primeiro bloco.

Cada tag de sessão pode ser usada apenas uma vez para evitar que adversários internos correlacionem desnecessariamente diferentes mensagens como sendo entre os mesmos routers. O remetente de uma mensagem criptografada ElGamal/AES+SessionTag escolhe quando e quantas tags entregar, abastecendo previamente o destinatário com tags suficientes para cobrir uma rajada de mensagens. As mensagens garlic podem detectar a entrega bem-sucedida da tag agrupando uma pequena mensagem adicional como um cravo (uma "mensagem de status de entrega") - quando a mensagem garlic chega ao destinatário pretendido e é descriptografada com sucesso, esta pequena mensagem de status de entrega é um dos cravos expostos e tem instruções para o destinatário enviar o cravo de volta ao remetente original (através de um tunnel de entrada, é claro). Quando o remetente original recebe esta mensagem de status de entrega, ele sabe que as tags de sessão agrupadas na mensagem garlic foram entregues com sucesso.

As próprias session tags têm um tempo de vida curto, após o qual são descartadas se não forem usadas. Além disso, a quantidade armazenada para cada chave é limitada, assim como o número das próprias chaves - se muitas chegarem, mensagens novas ou antigas podem ser descartadas. O remetente controla se as mensagens que usam session tags estão sendo entregues, e se não houver comunicação suficiente, ele pode descartar aquelas anteriormente consideradas como devidamente entregues, revertendo para a criptografia ElGamal completa e custosa. Uma sessão continuará a existir até que todas as suas tags sejam esgotadas ou expirem.

As sessões são unidirecionais. As tags são entregues de Alice para Bob, e Alice então usa as tags, uma por uma, nas mensagens subsequentes para Bob.

As sessões podem ser estabelecidas entre Destinations, entre routers, ou entre um router e um Destination. Cada router e Destination mantém seu próprio Session Key Manager para acompanhar as Session Keys e Session Tags. Session Key Managers separados impedem a correlação de múltiplos Destinations entre si ou com um router por adversários.

## Recepção de Mensagens

Cada mensagem recebida tem uma de duas condições possíveis:

1. É parte de uma sessão existente e contém uma Session Tag e um bloco criptografado AES
2. É para uma nova sessão e contém blocos criptografados ElGamal e AES

Quando um router recebe uma mensagem, ele primeiro assume que ela é de uma sessão existente e tenta localizar a Session Tag e descriptografar os dados seguintes usando AES. Se isso falhar, ele assume que é para uma nova sessão e tenta descriptografá-la usando ElGamal.

## Especificação da Mensagem de Nova Sessão {#new}

Uma mensagem ElGamal de nova sessão contém duas partes: um bloco ElGamal criptografado e um bloco AES criptografado.

A mensagem criptografada contém:

```
   +----+----+----+----+----+----+----+----+
   |                                       |
   +                                       +
   |       ElGamal Encrypted Block         |
   ~                                       ~
   |                                       |
   +         +----+----+----+----+----+----+
   |         |                             |
   +----+----+                             +
   |                                       |
   +                                       +
   |         AES Encrypted Block           |
   ~                                       ~
   |                                       |
   +         +----+----+----+----+----+----+
   |         +
   +----+----+
```
### Bloco ElGamal

O Bloco ElGamal criptografado tem sempre 514 bytes de comprimento.

Os dados ElGamal não criptografados têm 222 bytes de comprimento, contendo:

```
   +----+----+----+----+----+----+----+----+
   |                                       |
   +                                       +
   |           Session Key                 |
   +                                       +
   |                                       |
   +                                       +
   |                                       |
   +----+----+----+----+----+----+----+----+
   |                                       |
   +                                       +
   |              Pre-IV                   |
   +                                       +
   |                                       |
   +                                       +
   |                                       |
   +----+----+----+----+----+----+----+----+
   +                                       +
   |                                       |
   +                                       +
   |       158 bytes random padding        |
   ~                                       ~
   |                                       |
   +                             +----+----+
   |                             |
   +----+----+----+----+----+----+
```
A [Session Key](/docs/specs/common-structures#type_SessionKey) de 32 bytes é o identificador da sessão. O Pre-IV de 32 bytes será usado para gerar o IV para o bloco AES que se segue; o IV são os primeiros 16 bytes do Hash SHA-256 do Pre-IV.

O payload de 222 bytes é criptografado [usando ElGamal](/docs/specs/cryptography#elgamal) e o bloco criptografado tem 514 bytes de comprimento.

### Bloco AES {#aes}

Os dados não criptografados no bloco AES contêm o seguinte:

```
   +----+----+----+----+----+----+----+----+
   |tag count|                             |
   +----+----+                             +
   |                                       |
   +                                       +
   |          Session Tags                 |
   ~                                       ~
   |                                       |
   +                                       +
   |                                       |
   +         +----+----+----+----+----+----+
   |         |    payload size   |         |
   +----+----+----+----+----+----+         +
   |                                       |
   +                                       +
   |          Payload Hash                 |
   +                                       +
   |                                       |
   +                             +----+----+
   |                             |flag|    |
   +----+----+----+----+----+----+----+    +
   |                                       |
   +                                       +
   |          New Session Key (opt.)       |
   +                                       +
   |                                       |
   +                                  +----+
   |                                  |    |
   +----+----+----+----+----+----+----+    +
   |                                       |
   +                                       +
   |           Payload                     |
   ~                                       ~
   |                                       |
   +                        +----//---+----+
   |                        |              |
   +----+----+----//---+----+              +
   |          Padding to 16 bytes          |
   +----+----+----+----+----+----+----+----+
```
#### Definição

```
tag count:
    2-byte Integer, 0-200

Session Tags:
    That many 32-byte SessionTags

payload size:
    4-byte Integer

Payload Hash:
    The 32-byte SHA256 Hash of the payload

flag:
    A one-byte value. Normally == 0. If == 0x01, a Session Key follows

New Session Key:
    A 32-byte SessionKey,
    to replace the old key, and is only present if preceding flag is 0x01

Payload:
    the data

Padding:
    Random data to a multiple of 16 bytes for the total length.
    May contain more than the minimum required padding.
```
Comprimento mínimo: 48 bytes

Os dados são então [criptografados com AES](/docs/specs/cryptography), usando a chave de sessão e IV (calculado a partir do pre-IV) da seção ElGamal. O comprimento do bloco AES criptografado é variável, mas sempre é um múltiplo de 16 bytes.

#### Notas

- O comprimento máximo real da carga útil e o comprimento máximo do bloco é inferior a 64 KB; consulte a [Visão Geral do I2NP](/docs/protocol/i2np).
- Nova Session Key está atualmente não utilizada e nunca está presente.

## Especificação de Mensagem de Sessão Existente {#existing}

As session tags entregues com sucesso são lembradas por um breve período (15 minutos atualmente) até serem usadas ou descartadas. Uma tag é usada ao empacotá-la numa Existing Session Message que contém apenas um bloco criptografado AES, e não é precedida por um bloco ElGamal.

A mensagem de sessão existente é a seguinte:

```
   +----+----+----+----+----+----+----+----+
   |                                       |
   +                                       +
   |            Session Tag                |
   +                                       +
   |                                       |
   +                                       +
   |                                       |
   +----+----+----+----+----+----+----+----+
   |                                       |
   +                                       +
   |         AES Encrypted Block           |
   ~                                       ~
   |                                       |
   +                                       +
   |                                       |
   +----+----+----+----+----+----+----+----+
```
#### Definição

```
Session Tag:
    A 32-byte SessionTag
    previously delivered in an AES block

AES Encrypted Block:
    As specified above.
```
A tag de sessão também serve como pré-IV. O IV são os primeiros 16 bytes do Hash SHA-256 da sessionTag.

Para decodificar uma mensagem de uma sessão existente, um router procura a Session Tag para encontrar uma Session Key associada. Se a Session Tag for encontrada, o bloco AES é descriptografado usando a Session Key associada. Se a tag não for encontrada, a mensagem é considerada uma [New Session Message](#new).

## Opções de Configuração de Session Tag {#config}

A partir da versão 0.9.2, o cliente pode configurar o número padrão de Session Tags a enviar e o limite mínimo de tags para a sessão atual. Para conexões de streaming breves ou datagramas, essas opções podem ser usadas para reduzir significativamente a largura de banda. Consulte a [especificação de opções I2CP](/docs/protocol/i2cp#options) para detalhes. As configurações de sessão também podem ser substituídas por mensagem individual. Consulte a [especificação I2CP Send Message Expires](/docs/specs/i2cp#msg_SendMessageExpires) para detalhes.

## Trabalho Futuro {#future}

**Nota:** ElGamal/AES+SessionTags está sendo substituído por ECIES-X25519-AEAD-Ratchet (Proposta 144). Os problemas e ideias referenciados abaixo foram incorporados no design do novo protocolo. Os itens a seguir não serão abordados no ElGamal/AES+SessionTags.

Há muitas áreas possíveis para ajustar os algoritmos do Gerenciador de Chaves de Sessão; algumas podem interagir com o comportamento da biblioteca de streaming, ou ter impacto significativo no desempenho geral.

- O número de tags entregues pode depender do tamanho da mensagem, tendo em mente
  o preenchimento eventual para 1KB na camada de mensagem do tunnel.

- Os clientes poderiam enviar uma estimativa do tempo de vida da sessão para o router, como um conselho sobre o número de tags necessárias.

- A entrega de poucas tags faz com que o router recorra a uma criptografia ElGamal custosa.

- O router pode assumir a entrega das Session Tags, ou aguardar confirmação antes de usá-las;
  existem compensações para cada estratégia.

- Para mensagens muito breves, quase todos os 222 bytes dos campos de pré-IV e preenchimento no bloco ElGamal poderiam ser usados para toda a mensagem, em vez de estabelecer uma sessão.

- Avaliar estratégia de padding; atualmente fazemos padding para um mínimo de 128 bytes.
  Seria melhor adicionar algumas tags a mensagens pequenas do que fazer padding.

- Talvez as coisas pudessem ser mais eficientes se o sistema de Session Tag fosse bidirecional,
  para que as tags entregues no caminho 'direto' pudessem ser usadas no caminho 'reverso',
  evitando assim ElGamal na resposta inicial.
  O router atualmente usa alguns truques como este ao enviar
  mensagens de teste de tunnel para si mesmo.

- Mudança de Session Tags para
  [um PRNG sincronizado](/docs/overview/performance#future#prng).

- Várias dessas ideias podem exigir um novo tipo de mensagem I2NP, ou
  definir uma flag nas
  [Instruções de Entrega](/docs/specs/tunnel-message#struct_TunnelMessageDeliveryInstructions),
  ou definir um número mágico nos primeiros bytes do campo Session Key
  e aceitar um pequeno risco da Session Key aleatória corresponder ao número mágico.
