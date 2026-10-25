---
title: "Especificação de Mensagem de Tunnel"
description: "Especificação para o formato de mensagens de tunnel no I2P"
slug: "tunnel-message"
aliases:
  - "/pt/docs/legacy/tunnel-message"
  - "/pt/docs/legacy/tunnel-message/"
  - "/pt/tunnel_message_spec"
  - "/pt/tunnel_message_spec/"
category: "Design"
lastUpdated: "2021-01"
accurateFor: "0.9.49"
---

## Visão Geral

Este documento especifica o formato das mensagens de tunnel. Para informações gerais sobre tunnels veja a [documentação de tunnel](/docs/specs/tunnel-implementation).

## Pré-processamento de Mensagens

Um *tunnel gateway* é a entrada, ou primeiro salto, de um tunnel. Para um tunnel de saída, o gateway é o criador do tunnel. Para um tunnel de entrada, o gateway está na extremidade oposta ao criador do tunnel.

Um gateway *pré-processa* mensagens [I2NP](/docs/specs/i2np) fragmentando-as e combinando-as em mensagens de tunnel.

Embora as mensagens I2NP tenham tamanho variável de 0 a quase 64 KB, as mensagens de tunnel têm tamanho fixo, aproximadamente 1 KB. O tamanho fixo da mensagem restringe vários tipos de ataques que são possíveis através da observação do tamanho da mensagem.

Após as mensagens do tunnel serem criadas, elas são criptografadas conforme descrito na [documentação do tunnel](/docs/specs/tunnel-implementation).

### Mensagem de Tunnel (Criptografada)

Estes são os conteúdos de uma mensagem de dados de tunnel após a criptografia.

```
+----+----+----+----+----+----+----+----+
|    Tunnel ID      |       IV          |
+----+----+----+----+                   +
|                                       |
+                   +----+----+----+----+
|                   |                   |
+----+----+----+----+                   +
|                                       |
+           Encrypted Data              +
~                                       ~
|                                       |
+                   +-------------------+
|                   |
+----+----+----+----+
```
**ID do Tunnel** :: [TunnelId](/docs/specs/common-structures#tunnelid) : 4 bytes. O ID do próximo salto, diferente de zero.

**IV** :: : 16 bytes. O vetor de inicialização.

**Dados Criptografados** :: : 1008 bytes. A mensagem de tunnel criptografada.

**Tamanho total: 1028 bytes**

### Mensagem de Tunnel (Descriptografada)

Estes são os conteúdos de uma mensagem de dados de tunnel quando descriptografada.

```
+----+----+----+----+----+----+----+----+
|    Tunnel ID      |       IV          |
+----+----+----+----+                   +
|                                       |
+                   +----+----+----+----+
|                   |     Checksum      |
+----+----+----+----+----+----+----+----+
|          nonzero padding...           |
~                                       ~
|                                       |
+                                  +----+
|                                  |zero|
+----+----+----+----+----+----+----+----+
|                                       |
|       Delivery Instructions  1        |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|                                       |
+       I2NP Message Fragment 1         +
|                                       |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|                                       |
|       Delivery Instructions 2...      |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|                                       |
+       I2NP Message Fragment 2...      +
|                                       |
~                                       ~
|                                       |
+                   +-------------------+
|                   |
+----+----+----+----+
```
**ID do Tunnel** :: [TunnelId](/docs/specs/common-structures#tunnelid) : 4 bytes. O ID do próximo salto, diferente de zero.

**IV** :: : 16 bytes. O vetor de inicialização.

**Checksum** :: : 4 bytes. Os primeiros 4 bytes do hash SHA256 de (o conteúdo da mensagem (após o byte zero) + IV).

**Preenchimento não-zero** :: : 0 ou mais bytes. Dados aleatórios não-zero para preenchimento.

**Zero** :: : 1 byte. O valor 0x00.

**Instruções de Entrega** :: TunnelMessageDeliveryInstructions : O comprimento varia, mas normalmente é 7, 39, 43 ou 47 bytes. Indica o fragmento e o roteamento para o fragmento.

**Fragmento de Mensagem** :: : 1 a 996 bytes, o máximo real depende do tamanho da instrução de entrega. Uma Mensagem I2NP parcial ou completa.

**Tamanho total: 1028 bytes**

#### Notas

- O preenchimento, se houver, deve estar antes dos pares instrução/mensagem. Não há provisão para preenchimento no final.
- O checksum NÃO cobre o preenchimento ou o byte zero. Pegue a mensagem começando nas primeiras instruções de entrega, concatene o IV e calcule o Hash disso.

## Instruções de Entrega de Mensagens do Tunnel

As instruções são codificadas com um único byte de controle, seguido por qualquer informação adicional necessária. O primeiro bit (MSB) nesse byte de controle determina como o restante do cabeçalho é interpretado - se não estiver definido, a mensagem não está fragmentada ou este é o primeiro fragmento da mensagem. Se estiver definido, este é um fragmento subsequente.

Esta especificação é apenas para Instruções de Entrega dentro de Mensagens de Tunnel. Note que "Instruções de Entrega" também são usadas dentro de Garlic Cloves, onde o formato é significativamente diferente. Consulte a [documentação I2NP](/docs/specs/i2np#garlicclovedeliveryinstructions) para detalhes. NÃO use a especificação a seguir para Instruções de Entrega de Garlic Clove!

### Instruções de Entrega do Primeiro Fragmento

Se o MSB do primeiro byte for 0, este é um fragmento inicial de mensagem I2NP, ou uma mensagem I2NP completa (não fragmentada), e as instruções são:

```
+----+----+----+----+----+----+----+----+
|flag|  Tunnel ID (opt)  |              |
+----+----+----+----+----+              +
|                                       |
+                                       +
|         To Hash (optional)            |
+                                       +
|                                       |
+                        +--------------+
|                        |dly | Message
+----+----+----+----+----+----+----+----+
 ID (opt) |extended opts (opt)|  size   |
+----+----+----+----+----+----+----+----+
```
**flag** :: : 1 byte. Ordem dos bits: 76543210   - bit 7: 0 para especificar um fragmento inicial ou uma mensagem não fragmentada   - bits 6-5: tipo de entrega

    - 0x0 = LOCAL
    - 0x01 = TUNNEL
    - 0x02 = ROUTER
    - 0x03 = unused, invalid
    - Note: LOCAL is used for inbound tunnels only, unimplemented for outbound tunnels
- bit 4: delay incluído? Não implementado, sempre 0. Se 1, um byte de delay é incluído.
  - bit 3: fragmentado? Se 0, a mensagem não está fragmentada, o que segue é a mensagem inteira. Se 1, a mensagem está fragmentada, e as instruções contêm um Message ID.
  - bit 2: opções estendidas? Não implementado, sempre 0. Se 1, opções estendidas são incluídas.
  - bits 1-0: reservados, definidos como 0 para compatibilidade com usos futuros

**Tunnel ID** :: [TunnelId](/docs/specs/common-structures#tunnelid) : 4 bytes. Opcional, presente se o tipo de entrega for TUNNEL. O ID do tunnel de destino, diferente de zero.

**To Hash** :: : 32 bytes. Opcional, presente se o tipo de entrega for ROUTER ou TUNNEL. Se ROUTER, o Hash SHA256 do router. Se TUNNEL, o Hash SHA256 do router de gateway.

**Delay** :: : 1 byte. Opcional, presente se a flag de delay incluído estiver definida. Em mensagens de tunnel: Não implementado, nunca presente; especificação original: bit 7: tipo (0 = rigoroso, 1 = aleatório), bits 6-0: expoente de delay (2^valor minutos).

**ID da Mensagem** :: : 4 bytes. Opcional, presente se esta mensagem for o primeiro de 2 ou mais fragmentos (ou seja, se o bit fragmentado for 1). Um ID que identifica unicamente todos os fragmentos como pertencentes a uma única mensagem (a implementação atual usa I2NPMessageHeader.msg_id).

**Opções Estendidas** :: : 2 ou mais bytes. Opcional, presente se a flag de opções estendidas estiver definida. Não implementado, nunca presente; especificação original: Um byte de comprimento e então essa quantidade de bytes.

**size** :: : 2 bytes. O comprimento do fragmento que segue. Valores válidos: 1 a aproximadamente 960 numa mensagem de tunnel.

**Comprimento total:** O comprimento típico é: - 3 bytes para entrega LOCAL (mensagem de tunnel) - 35 bytes para entrega ROUTER ou 39 bytes para entrega TUNNEL (mensagem de tunnel não fragmentada) - 39 bytes para entrega ROUTER ou 43 bytes para entrega TUNNEL (primeiro fragmento)

### Instruções de Entrega de Fragmentos Subsequentes

Se o MSB do primeiro byte for 1, este é um fragmento de continuação, e as instruções são:

```
+----+----+----+----+----+----+----+
|frag|     Message ID    |  size   |
+----+----+----+----+----+----+----+
```
**frag** :: : 1 byte. Ordem dos bits: 76543210. Binário 1nnnnnnd:   - bit 7: 1 para indicar que este é um fragmento de continuação   - bits 6-1: nnnnnn é o número do fragmento de 6 bits de 1 a 63   - bit 0: d é 1 para indicar o último fragmento, 0 caso contrário

**Message ID** :: : 4 bytes. Identifica a sequência de fragmentos à qual este fragmento pertence. Este corresponderá ao message ID de um fragmento inicial (um fragmento com o bit 7 da flag definido como 0 e o bit 3 da flag definido como 1).

**size** :: : 2 bytes. O comprimento do fragmento que segue. Valores válidos: 1 a 996.

**Comprimento total: 7 bytes**

## Notas

### Tamanho Máximo da Mensagem I2NP

Embora o tamanho máximo da mensagem I2NP seja nominalmente de 64 KB, o tamanho é ainda mais restringido pelo método de fragmentar mensagens I2NP em múltiplas mensagens de tunnel de 1 KB. O número máximo de fragmentos é 64, e o fragmento inicial pode não estar perfeitamente alinhado no início de uma mensagem de tunnel. Portanto, a mensagem deve nominalmente caber em 63 fragmentos.

O tamanho máximo de um fragmento inicial é 956 bytes (assumindo modo de entrega TUNNEL); o tamanho máximo de um fragmento subsequente é 996 bytes. Portanto, o tamanho máximo é aproximadamente 956 + (62 * 996) = 62708 bytes, ou 61,2 KB.

### Ordenação, Agrupamento, Empacotamento

As mensagens de tunnel podem ser descartadas ou reordenadas. O gateway do tunnel, que cria as mensagens de tunnel, tem liberdade para implementar qualquer estratégia de agrupamento, mistura ou reordenação para fragmentar mensagens I2NP e empacotar eficientemente os fragmentos em mensagens de tunnel. Em geral, um empacotamento ótimo não é possível (o "problema de empacotamento"). Os gateways podem implementar várias estratégias de atraso e reordenação.

### Tráfego de Cobertura

Mensagens de tunnel podem conter apenas preenchimento (ou seja, nenhuma instrução de entrega ou fragmentos de mensagem) para tráfego de cobertura. Isso não está implementado.

## Referências

- **[I2NP]** [Protocolo I2NP](/docs/specs/i2np)
- **[I2NP-GC]** [GarlicClove](/docs/specs/i2np#garlicclove)
- **[I2NP-GCDI]** [GarlicCloveDeliveryInstructions](/docs/specs/i2np#garlicclovedeliveryinstructions)
- **[TUNNEL-IMPL]** [Implementação de Tunnel](/docs/specs/tunnel-implementation)
