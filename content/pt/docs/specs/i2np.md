---
title: "Especificação I2NP"
description: "Formatos de mensagem do Protocolo de Rede I2P (I2NP), prioridades e estruturas comuns para comunicação entre routers."
slug: "i2np"
aliases:
  - "/pt/spec/i2np"
  - "/pt/spec/i2np/"
category: "Protocolos"
lastUpdated: "2026-03"
accurateFor: "0.9.69"
---

## Visão Geral

O I2P Network Protocol (I2NP) é a camada acima dos protocolos de transporte I2P. É um protocolo router-para-router. É usado para consultas e respostas da base de dados da rede, para criar tunnels, e para mensagens de dados encriptadas de router e cliente. As mensagens I2NP podem ser enviadas ponto-a-ponto para outro router, ou enviadas anonimamente através de tunnels para esse router.

## Versões do Protocolo {#versions}

Todos os routers devem publicar sua versão do protocolo I2NP no campo "router.version" nas propriedades do RouterInfo. Este campo de versão é a versão da API, indicando o nível de suporte para várias funcionalidades do protocolo I2NP, e não é necessariamente a versão real do router.

Se routers alternativos (não-Java) desejarem publicar qualquer informação de versão sobre a implementação real do router, eles devem fazê-lo em outra propriedade. Versões diferentes daquelas listadas abaixo são permitidas. O suporte será determinado através de uma comparação numérica; por exemplo, 0.9.13 implica suporte para recursos da versão 0.9.12. Note que a propriedade "coreVersion" não é mais publicada nas informações do router, e nunca foi usada para determinação da versão do protocolo I2NP.

Um resumo básico das versões do protocolo I2NP é o seguinte. Para detalhes, veja abaixo.

<table style="border-collapse: collapse; width: 100%;">
<thead>
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px; text-align: left;">API Version</th>
<th style="border: 1px solid var(--color-border); padding: 8px; text-align: left;">Required I2NP Features</th>
</tr>
</thead>
<tbody>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.68</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Tunnel testing required</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.66</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">LeaseSet2 service record options (see proposal 167)</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.65</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Tunnel build bandwidth parameters (see proposal 168)</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.62</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Minimum peers will build tunnels through, as of 0.9.68<br>Minimum floodfill peers will send DSM to, as of 0.9.68</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.59</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Minimum peers will build tunnels through, as of 0.9.63<br>Minimum floodfill peers will send DSM to, as of 0.9.63</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.58</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Minimum peers will build tunnels through, as of 0.9.62<br>ElGamal Routers deprecated</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.55</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">SSU2 transport support (if published in router info)</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.51</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Short tunnel build messages for ECIES-X25519 routers<br>Minimum peers will build tunnels through, as of 0.9.58<br>Minimum floodfill peers will send DSM to, as of 0.9.58</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.49</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Garlic messages to ECIES-X25519 routers</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.48</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">ECIES-X25519 Routers<br>ECIES-X25519 Build Request/Response records</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.46</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">DatabaseLookup flag bit 4 for AEAD reply</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.44</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">ECIES-X25519 keys in LeaseSet2</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.40</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">MetaLeaseSet may be sent in a DSM</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.39</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">EncryptedLeaseSet may be sent in a DSM<br>RedDSA_SHA512_Ed25519 signature type supported for destinations and leasesets</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.38</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">DSM type bits 3-0 now contain the type; LeaseSet2 may be sent in a DSM</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.36</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">NTCP2 transport support (if published in router info)<br>Minimum peers will build tunnels through, as of 0.9.46</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.28</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">RSA sig types disallowed<br>Minimum floodfill peers will send DSM to, as of 0.9.34</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.18</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">DSM type bits 7-1 ignored</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.16</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">RI key certs / ECDSA and EdDSA sig types<br>Note: RSA sig types also supported as of this version, but currently unused<br>DLM lookup types (DLM flag bits 3-2)<br>Minimum version compatible with vast majority of current network, since routers are now using the EdDSA sig type.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.15</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Dest/LS key certs w/ EdDSA Ed25519 sig type (if floodfill)</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.12</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Dest/LS key certs w/ ECDSA P-256, P-384, and P-521 sig types (if floodfill)<br>Note: RSA sig types also supported as of this version, but currently unused<br>Nonzero expiration allowed in RouterAddress</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.7</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Encrypted DSM/DSRM replies supported (DLM flag bit 1) (if floodfill)</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.6</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Nonzero DLM flag bits 7-1 allowed</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.3</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Requires zero expiration in RouterAddress</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Supports up to 16 leases in a DSM LS store (6 previously)</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.7.12</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">VTBM and VTBRM message support</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.7.10</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Floodfill supports encrypted DSM stores</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.7.9 or lower</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">All messages and features not listed above</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.6.1.10</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">TBM and TBRM messages introduced<br>Minimum version compatible with current network</td>
</tr>
</tbody>
</table>
Note que também existem funcionalidades relacionadas ao transporte e problemas de compatibilidade; consulte a documentação dos transportes NTCP e SSU para detalhes.

## Estruturas Comuns {#structures}

As seguintes estruturas são elementos de múltiplas mensagens I2NP. Elas não são mensagens completas.

### Cabeçalho da Mensagem I2NP {#struct-I2NPMessageHeader}

#### Descrição

Cabeçalho comum a todas as mensagens I2NP, que contém informações importantes como uma soma de verificação, data de expiração, etc.

#### Conteúdo

Existem três formatos separados utilizados, dependendo do contexto; um formato padrão e dois formatos curtos.

O formato padrão de 16 bytes contém 1 byte [Integer](/docs/specs/common-structures/#integer) especificando o tipo desta mensagem, seguido por um [Integer](/docs/specs/common-structures/#integer) de 4 bytes especificando o message-id. Após isso, há uma [Date](/docs/specs/common-structures/#date) de expiração, seguida por um [Integer](/docs/specs/common-structures/#integer) de 2 bytes especificando o comprimento do payload da mensagem, seguido por um [Hash](/docs/specs/common-structures/#hash), que é truncado para o primeiro byte. Após isso seguem os dados reais da mensagem.

Os formatos curtos usam uma expiração de 4 bytes em segundos em vez de uma expiração de 8 bytes em milissegundos. Os formatos curtos não contêm um checksum ou tamanho, estes são fornecidos pelos encapsulamentos, dependendo do contexto.

```
Standard (16 bytes):

+----+----+----+----+----+----+----+----+
|type|      msg_id       |  expiration
+----+----+----+----+----+----+----+----+
                         |  size   |chks|
+----+----+----+----+----+----+----+----+

Short (SSU, 5 bytes) (obsolete):

+----+----+----+----+----+
|type| short_expiration  |
+----+----+----+----+----+

Short (NTCP2, SSU2, and ECIES-Ratchet Garlic Cloves, 9 bytes):

+----+----+----+----+----+----+----+----+
|type|      msg_id       | short_expira-
+----+----+----+----+----+----+----+----+
 tion|
+----+

type :: Integer
        length -> 1 byte
        purpose -> identifies the message type (see table below)

msg_id :: Integer
          length -> 4 bytes
          purpose -> uniquely identifies this message (for some time at least)
                     This is usually a locally-generated random number, but
                     for outgoing tunnel build messages it may be derived from
                     the incoming message. See below.

expiration :: Date
              8 bytes
              date this message will expire

short_expiration :: Integer
                    4 bytes
                    date this message will expire (seconds since the epoch)

size :: Integer
        length -> 2 bytes
        purpose -> length of the payload

chks :: Integer
        length -> 1 byte
        purpose -> checksum of the payload
                   SHA256 hash truncated to the first byte

data ::
        length -> $size bytes
        purpose -> actual message contents
```
#### Notas

- Quando transmitida por [SSU](/docs/transports/ssu/), o cabeçalho padrão de 16 bytes não é usado. Apenas um tipo de 1 byte e uma expiração de 4 bytes em segundos são incluídos. O id da mensagem e o tamanho são incorporados no formato do pacote de dados SSU. O checksum não é necessário, pois os erros são detectados na descriptografia.

- Quando transmitido por [NTCP2](/docs/specs/ntcp2/) ou [SSU2](/docs/specs/ssu2/), o cabeçalho padrão de 16 bytes não é usado. Apenas um tipo de 1 byte, id da mensagem de 4 bytes e uma expiração de 4 bytes em segundos são incluídos. O tamanho é incorporado nos formatos de pacote de dados NTCP2 e SSU2. O checksum não é necessário, pois os erros são detectados na descriptografia.

- O cabeçalho padrão também é obrigatório para mensagens I2NP contidas em outras mensagens e estruturas (Data, TunnelData, TunnelGateway e GarlicClove). A partir da versão 0.8.12, para reduzir a sobrecarga, a verificação de checksum está desabilitada em alguns pontos da pilha de protocolos. No entanto, para compatibilidade com versões mais antigas, a geração de checksum ainda é obrigatória. É um tópico para pesquisa futura determinar pontos na pilha de protocolos onde a versão do router de destino é conhecida e a geração de checksum pode ser desabilitada.

- A expiração curta é não assinada e irá reiniciar em 7 de fevereiro de 2106. A partir dessa data, um deslocamento deve ser adicionado para obter o tempo correto.

- As implementações podem rejeitar mensagens com expirações muito distantes no futuro. A expiração máxima recomendada é de 60s no futuro.

### BuildRequestRecord {#struct-BuildRequestRecord}

DEPRECIADO, apenas usado na rede atual quando um tunnel contém um router ElGamal. Ver [Criação de Tunnel ECIES](/docs/specs/tunnel-creation-ecies/).

#### Descrição

Um Record em um conjunto de múltiplos records para solicitar a criação de um hop no tunnel. Para mais detalhes, consulte a [visão geral do tunnel](/docs/specs/tunnel-implementation/) e a [especificação de criação de tunnel ElGamal](/docs/specs/tunnel-creation/).

Para BuildRequestRecords ECIES-X25519, consulte [Criação de Túnel ECIES](/docs/specs/tunnel-creation-ecies/).

#### Conteúdo (ElGamal)

[TunnelId](/docs/specs/common-structures/#tunnelid) para receber mensagens, seguido pelo [Hash](/docs/specs/common-structures/#hash) da nossa [RouterIdentity](/docs/specs/common-structures/#routeridentity). Depois disso seguem o [TunnelId](/docs/specs/common-structures/#tunnelid) e o [Hash](/docs/specs/common-structures/#hash) da [RouterIdentity](/docs/specs/common-structures/#routeridentity) do próximo router.

Criptografado com ElGamal e AES:

```
+----+----+----+----+----+----+----+----+
| encrypted data...                     |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+

encrypted_data :: ElGamal and AES encrypted data
                  length -> 528

total length: 528
```
Criptografado com ElGamal:

```
+----+----+----+----+----+----+----+----+
| toPeer                                |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
| encrypted data...                     |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+

toPeer :: First 16 bytes of the SHA-256 Hash of the peer's RouterIdentity
          length -> 16 bytes

encrypted_data :: ElGamal-2048 encrypted data (see notes)
                  length -> 512

total length: 528
```
Texto em claro:

```
+----+----+----+----+----+----+----+----+
| receive_tunnel    | our_ident         |
+----+----+----+----+                   +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+                   +----+----+----+----+
|                   | next_tunnel       |
+----+----+----+----+----+----+----+----+
| next_ident                            |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
| layer_key                             |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
| iv_key                                |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
| reply_key                             |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
| reply_iv                              |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|flag| request_time      | send_msg_id
+----+----+----+----+----+----+----+----+
     |                                  |
+----+                                  +
|         29 bytes padding              |
+                                       +
|                                       |
+                             +----+----+
|                             |
+----+----+----+----+----+----+

receive_tunnel :: TunnelId
                  length -> 4 bytes
                  nonzero

our_ident :: Hash
             length -> 32 bytes

next_tunnel :: TunnelId
               length -> 4 bytes
               nonzero

next_ident :: Hash
              length -> 32 bytes

layer_key :: SessionKey
             length -> 32 bytes

iv_key :: SessionKey
          length -> 32 bytes

reply_key :: SessionKey
             length -> 32 bytes

reply_iv :: data
            length -> 16 bytes

flag :: Integer
        length -> 1 byte

request_time :: Integer
                length -> 4 bytes
                Hours since the epoch, i.e. current time / 3600

send_message_id :: Integer
                   length -> 4 bytes

padding :: Data
           length -> 29 bytes
           source -> random

total length: 222
```
#### Notas

- No registro criptografado de 512 bytes, os dados ElGamal contêm os bytes 1-256 e 258-513 do bloco criptografado ElGamal de 514 bytes [CRYPTO-ELG](/docs/specs/cryptography/#elgamal). Os dois bytes de preenchimento do bloco (os bytes zero nas posições 0 e 257) são removidos.

- Veja a [especificação de criação de tunnel](/docs/specs/tunnel-creation/) para detalhes sobre o conteúdo dos campos.

### BuildResponseRecord {#struct-BuildResponseRecord}

DESCONTINUADO, usado apenas na rede atual quando um tunnel contém um router ElGamal. Consulte [ECIES Tunnel Creation](/docs/specs/tunnel-creation-ecies/).

#### Descrição

Um registro em um conjunto de múltiplos registros com respostas a uma solicitação de construção. Para mais detalhes, consulte a [visão geral do tunnel](/docs/specs/tunnel-implementation/) e a [especificação de criação de tunnel ElGamal](/docs/specs/tunnel-creation/).

Para BuildResponseRecords ECIES-X25519, consulte [Criação de Túnel ECIES](/docs/specs/tunnel-creation-ecies/).

#### Conteúdo (ElGamal)

```
Encrypted:

bytes 0-527 :: AES-encrypted record (note: same size as BuildRequestRecord)

Unencrypted:

+----+----+----+----+----+----+----+----+
|                                       |
+                                       +
|                                       |
+   SHA-256 Hash of following bytes     +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
| random data...                        |
~                                       ~
|                                       |
+                                  +----+
|                                  | ret|
+----+----+----+----+----+----+----+----+

bytes 0-31   :: SHA-256 Hash of bytes 32-527
bytes 32-526 :: random data
byte  527    :: reply

total length: 528
```
#### Notas

- O campo de dados aleatórios poderia, no futuro, ser usado para retornar informações de congestionamento ou conectividade de peer de volta ao solicitante.

- Veja a [especificação de criação de tunnel](/docs/specs/tunnel-creation/) para detalhes sobre o campo de resposta.

### ShortBuildRequestRecord {#struct-ShortBuildRequestRecord}

Apenas para routers ECIES-X25519, a partir da versão da API 0.9.51. 218 bytes quando criptografado. Veja [Criação de Tunnel ECIES](/docs/specs/tunnel-creation-ecies/).

### ShortBuildResponseRecord {#struct-ShortBuildResponseRecord}

Apenas para routers ECIES-X25519, a partir da versão da API 0.9.51. 218 bytes quando criptografado. Veja [Criação de Tunnel ECIES](/docs/specs/tunnel-creation-ecies/).

### GarlicClove {#struct-GarlicClove}

Aviso: Este é o formato usado para dentes de garlic encryption dentro de mensagens garlic encryption criptografadas com ElGamal [CRYPTO-ELG](/docs/specs/cryptography/#elgamal). O formato para mensagens garlic encryption e dentes garlic encryption ECIES-AEAD-X25519-Ratchet é significativamente diferente; consulte [ECIES](/docs/specs/ecies/) para a especificação.

```
Unencrypted:

+----+----+----+----+----+----+----+----+
| Delivery Instructions                 |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| I2NP Message                          |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|    Clove ID       |     Expiration
+----+----+----+----+----+----+----+----+
                    | Certificate  |
+----+----+----+----+----+----+----+

Delivery Instructions :: as defined below
       Length varies but is typically 1, 33, or 37 bytes

I2NP Message :: Any I2NP Message

Clove ID :: 4 byte Integer

Expiration :: Date (8 bytes)

Certificate :: Always NULL in the current implementation (3 bytes total, all zeroes)
```
#### Notas

- Cloves nunca são fragmentados. Quando usados em um Garlic Clove, o primeiro bit do byte de flag das Instruções de Entrega especifica encriptação. Se este bit for 0, o clove não está encriptado. Se for 1, o clove está encriptado, e uma Session Key de 32 bytes segue imediatamente após o byte de flag. A encriptação de clove não está totalmente implementada.

- Veja também a [especificação de roteamento garlic](/docs/overview/garlic-routing/).

- O comprimento máximo é uma função do comprimento total de todos os dentes e do comprimento máximo da GarlicMessage.

- No futuro, o certificado poderia possivelmente ser usado para um HashCash para "pagar" pelo roteamento.

- A mensagem pode ser qualquer mensagem I2NP (incluindo uma GarlicMessage, embora isso não seja usado na prática). As mensagens usadas na prática são DataMessage, DeliveryStatusMessage e DatabaseStoreMessage.

- O ID do Clove é geralmente definido como um número aleatório na transmissão e é verificado para duplicatas no recebimento (mesmo espaço de ID de mensagem que os IDs de Mensagem de nível superior)

### Instruções de Entrega de Garlic Clove {#struct-GarlicCloveDeliveryInstructions}

Este é o formato usado tanto para dentes de garlic encryption criptografados com ElGamal [CRYPTO-ELG](/docs/specs/cryptography/#elgamal) quanto para aqueles criptografados com ECIES-AEAD-X25519-Ratchet [ECIES](/docs/specs/ecies/).

Esta especificação é apenas para Instruções de Entrega dentro de Garlic Cloves. Note que "Instruções de Entrega" também são usadas dentro de Mensagens de Túnel, onde o formato é significativamente diferente. Consulte a [documentação de Mensagem de Túnel](/docs/legacy/tunnel-message/#tunnel-message-delivery-instructions) para detalhes. NÃO use a especificação a seguir para Instruções de Entrega de Mensagem de Túnel!

A chave de sessão e o atraso não são utilizados e nunca estão presentes, então os três comprimentos possíveis são 1 (LOCAL), 33 (ROUTER e DESTINATION), e 37 (TUNNEL) bytes.

```
+----+----+----+----+----+----+----+----+
|flag|                                  |
+----+                                  +
|                                       |
+       Session Key (optional)          +
|                                       |
+                                       +
|                                       |
+    +----+----+----+----+--------------+
|    |                                  |
+----+                                  +
|                                       |
+         To Hash (optional)            +
|                                       |
+                                       +
|                                       |
+    +----+----+----+----+--------------+
|    |  Tunnel ID (opt)  |  Delay (opt)
+----+----+----+----+----+----+----+----+
     |
+----+

flag ::
       1 byte
       Bit order: 76543210
       bit 7: encrypted? Unimplemented, always 0
                If 1, a 32-byte encryption session key is included
       bits 6-5: delivery type
                0x0 = LOCAL, 0x01 = DESTINATION, 0x02 = ROUTER, 0x03 = TUNNEL
       bit 4: delay included?  Not fully implemented, always 0
                If 1, four delay bytes are included
       bits 3-0: reserved, set to 0 for compatibility with future uses

Session Key ::
       32 bytes
       Optional, present if encrypt flag bit is set.
       Unimplemented, never set, never present.

To Hash ::
       32 bytes
       Optional, present if delivery type is DESTINATION, ROUTER, or TUNNEL
          If DESTINATION, the SHA256 Hash of the destination
          If ROUTER, the SHA256 Hash of the router
          If TUNNEL, the SHA256 Hash of the gateway router

Tunnel ID :: TunnelId
       4 bytes
       Optional, present if delivery type is TUNNEL
       The destination tunnel ID, nonzero

Delay :: Integer
       4 bytes
       Optional, present if delay included flag is set
       Not fully implemented. Specifies the delay in seconds.

Total length: Typical length is:
       1 byte for LOCAL delivery;
       33 bytes for ROUTER / DESTINATION delivery;
       37 bytes for TUNNEL delivery
```
## Mensagens

<table style="border-collapse: collapse; width: 100%;">
<thead>
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px; text-align: left;">Message</th>
<th style="border: 1px solid var(--color-border); padding: 8px; text-align: center;">Type</th>
<th style="border: 1px solid var(--color-border); padding: 8px; text-align: left;">Since</th>
</tr>
</thead>
<tbody>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#msg-DatabaseStore">DatabaseStore</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: center;">1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#msg-DatabaseLookup">DatabaseLookup</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: center;">2</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#msg-DatabaseSearchReply">DatabaseSearchReply</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: center;">3</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#msg-DeliveryStatus">DeliveryStatus</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: center;">10</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#msg-Garlic">Garlic</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: center;">11</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#msg-TunnelData">TunnelData</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: center;">18</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#msg-TunnelGateway">TunnelGateway</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: center;">19</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#msg-Data">Data</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: center;">20</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#msg-TunnelBuild">TunnelBuild</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: center;">21</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">deprecated</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#msg-TunnelBuildReply">TunnelBuildReply</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: center;">22</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">deprecated</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#msg-VariableTunnelBuild">VariableTunnelBuild</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: center;">23</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.7.12</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#msg-VariableTunnelBuildReply">VariableTunnelBuildReply</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: center;">24</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.7.12</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#msg-ShortTunnelBuild">ShortTunnelBuild</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: center;">25</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.51</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#msg-OutboundTunnelBuildReply">OutboundTunnelBuildReply</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: center;">26</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.51</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">Reserved</td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: center;">0</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">Reserved for experimental messages</td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: center;">224-254</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">Reserved for future expansion</td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: center;">255</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
</tbody>
</table>
### DatabaseStore {#msg-DatabaseStore}

#### Descrição

Um armazenamento de banco de dados não solicitado, ou a resposta a uma [DatabaseLookup](#msg-DatabaseLookup) Message bem-sucedida

#### Conteúdo

Um LeaseSet descomprimido, LeaseSet2, MetaLeaseSet, ou EncryptedLeaseset, ou um RouterInfo comprimido

```
with reply token:
+----+----+----+----+----+----+----+----+
| SHA256 Hash as key                    |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|type| reply token       | reply_tunnelId
+----+----+----+----+----+----+----+----+
     | SHA256 of the gateway RouterInfo |
+----+                                  +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+    +----+----+----+----+----+----+----+
|    | data ...
+----+-//

with reply token == 0:
+----+----+----+----+----+----+----+----+
| SHA256 Hash as key                    |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|type|         0         | data ...
+----+----+----+----+----+-//

key ::
    32 bytes
    SHA256 hash

type ::
     1 byte
     type identifier
     bit 0:
             0    RouterInfo
             1    LeaseSet or variants listed below
     bits 3-1:
            Through release 0.9.17, must be 0
            As of release 0.9.18, ignored, reserved for future options, set to 0 for compatibility
            As of release 0.9.38, the remainder of the type identifier:
            0: RouterInfo or LeaseSet (types 0 or 1)
            1: LeaseSet2 (type 3)
            2: EncryptedLeaseSet (type 5)
            3: MetaLeaseSet (type 7)
            4-7: Unsupported, invalid
     bits 7-4:
            Through release 0.9.17, must be 0
            As of release 0.9.18, ignored, reserved for future options, set to 0 for compatibility

reply token ::
            4 bytes
            If greater than zero, a DeliveryStatusMessage
            is requested with the Message ID set to the value of the Reply Token.
            A floodfill router is also expected to flood the data to the closest floodfill peers
            if the token is greater than zero.

reply_tunnelId ::
               4 byte TunnelId
               Only included if reply token > 0
               This is the TunnelId of the inbound gateway of the tunnel the response should be sent to
               If $reply_tunnelId is zero, the reply is sent directy to the reply gateway router.

reply gateway ::
              32 bytes
              Hash of the RouterInfo entry to reach the gateway
              Only included if reply token > 0
              If $reply_tunnelId is nonzero, this is the router hash of the inbound gateway
              of the tunnel the response should be sent to.
              If $reply_tunnelId is zero, this is the router hash the response should be sent to.

data ::
     If type == 0, data is a 2-byte Integer specifying the number of bytes that follow,
                   followed by a gzip-compressed RouterInfo. See note below.
     If type == 1, data is an uncompressed LeaseSet.
     If type == 3, data is an uncompressed LeaseSet2.
     If type == 5, data is an uncompressed EncryptedLeaseSet.
     If type == 7, data is an uncompressed MetaLeaseSet.
```
#### Notas

- Por segurança, os campos de resposta são ignorados se a mensagem for recebida através de um tunnel.

- A chave é o hash "real" do RouterIdentity ou Destination, NÃO a chave de roteamento.

- Tipos 3, 5 e 7 são a partir da versão 0.9.38. Veja a proposta 123 para mais informações. Estes tipos devem ser enviados apenas para routers com versão 0.9.38 ou superior.

- Como uma otimização para reduzir conexões, se o tipo for um LeaseSet, o token de resposta estiver incluído, o ID do tunnel de resposta for diferente de zero, e o par gateway/tunnelID de resposta for encontrado no LeaseSet como um lease, o destinatário pode redirecionar a resposta para qualquer outro lease no LeaseSet.

- Para ocultar o OS do router e a implementação, corresponder à implementação do router Java do gzip definindo o tempo de modificação para 0 e o byte do OS para 0xFF, e definir XFL para 0x02 (compressão máxima, algoritmo mais lento). Veja RFC 1952. Os primeiros 10 bytes das informações comprimidas do router serão (hex): 1F 8B 08 00 00 00 00 00 02 FF

### DatabaseLookup {#msg-DatabaseLookup}

#### Descrição

Uma solicitação para procurar um item na base de dados da rede. A resposta é ou um [DatabaseStore](#msg-DatabaseStore) ou um [DatabaseSearchReply](#msg-DatabaseSearchReply).

#### Conteúdo

```
+----+----+----+----+----+----+----+----+
| SHA256 hash as the key to look up     |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
| SHA256 hash of the routerInfo         |
+ who is asking or the gateway to       +
| send the reply to                     |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|flag| reply_tunnelId    | size    |    |
+----+----+----+----+----+----+----+    +
| SHA256 of key1 to exclude             |
+                                       +
|                                       |
+                                       +
|                                       |
+                                  +----+
|                                  |    |
+----+----+----+----+----+----+----+    +
| SHA256 of key2 to exclude             |
+                                       +
~                                       ~
+                                  +----+
|                                  |    |
+----+----+----+----+----+----+----+    +
|                                       |
+                                       +
|   Session key if reply encryption     |
+   was requested                       +
|                                       |
+                                  +----+
|                                  |tags|
+----+----+----+----+----+----+----+----+
|                                       |
+                                       +
|   Session tags if reply encryption    |
+   was requested                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+

key ::
    32 bytes
    SHA256 hash of the object to lookup

from ::
     32 bytes
     if deliveryFlag == 0, the SHA256 hash of the routerInfo entry this
                           request came from (to which the reply should be
                           sent)
     if deliveryFlag == 1, the SHA256 hash of the reply tunnel gateway (to
                           which the reply should be sent)

flags ::
     1 byte
     bit order: 76543210
     bit 0: deliveryFlag
             0  => send reply directly
             1  => send reply to some tunnel
     bit 1: encryptionFlag
             through release 0.9.5, must be set to 0
             as of release 0.9.6, ignored
             as of release 0.9.7:
             0  => send unencrypted reply
             1  => send AES encrypted reply using enclosed key and tag
     bits 3-2: lookup type flags
             through release 0.9.5, must be set to 00
             as of release 0.9.6, ignored
             as of release 0.9.16:
             00  => ANY lookup, return RouterInfo or LeaseSet or
                    DatabaseSearchReplyMessage. DEPRECATED.
                    Use LS or RI lookup as of 0.9.16.
             01  => LS lookup, return LeaseSet or
                    DatabaseSearchReplyMessage
                    As of release 0.9.38, may also return a
                    LeaseSet2, MetaLeaseSet, or EncryptedLeaseSet.
             10  => RI lookup, return RouterInfo or
                    DatabaseSearchReplyMessage
             11  => exploration lookup, return RouterInfo or
                    DatabaseSearchReplyMessage containing
                    non-floodfill routers only (replaces an
                    excludedPeer of all zeroes)
     bit 4: ECIESFlag
             before release 0.9.46 ignored
             as of release 0.9.46:
             0  => send unencrypted or ElGamal reply
             1  => send ChaCha/Poly encrypted reply using enclosed key
                   (whether tag is enclosed depends on bit 1)
     bits 7-5:
             through release 0.9.5, must be set to 0
             as of release 0.9.6, ignored, set to 0 for compatibility with
             future uses and with older routers

reply_tunnelId ::
               4 byte TunnelID
               only included if deliveryFlag == 1
               tunnelId of the tunnel to send the reply to, nonzero

size ::
     2 byte Integer
     valid range: 0-512
     number of peers to exclude from the DatabaseSearchReplyMessage

excludedPeers ::
              $size SHA256 hashes of 32 bytes each (total $size*32 bytes)
              if the lookup fails, these peers are requested to be excluded
              from the list in the DatabaseSearchReplyMessage.
              if excludedPeers includes a hash of all zeroes, the request is
              exploratory, and the DatabaseSearchReplyMessage is requested
              to list non-floodfill routers only.

reply_key ::
     32 byte key
     see below

tags ::
     1 byte Integer
     valid range: 1-32 (typically 1)
     the number of reply tags that follow
     see below

reply_tags ::
     one or more 8 or 32 byte session tags (typically one)
     see below
```
#### Criptografia de Resposta

NOTA: Routers ElGamal estão obsoletos a partir da API 0.9.58. Como a versão mínima recomendada de floodfill para consulta é agora 0.9.58, as implementações não precisam implementar criptografia para routers floodfill ElGamal. Destinos ElGamal ainda são suportados.

O bit 4 da flag é usado em combinação com o bit 1 para determinar o modo de criptografia da resposta. O bit 4 da flag deve ser definido apenas ao enviar para routers com versão 0.9.46 ou superior. Veja as propostas 154 e 156 para detalhes.

Na tabela abaixo, "DH n/a" significa que a resposta não está criptografada. "DH no" significa que as chaves de resposta estão incluídas na solicitação. "DH yes" significa que as chaves de resposta são derivadas da operação DH.

<table style="border-collapse: collapse; width: 100%;">
<thead>
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px; text-align: left;">Flag bits 4,1</th>
<th style="border: 1px solid var(--color-border); padding: 8px; text-align: left;">From</th>
<th style="border: 1px solid var(--color-border); padding: 8px; text-align: left;">To Router</th>
<th style="border: 1px solid var(--color-border); padding: 8px; text-align: left;">Reply</th>
<th style="border: 1px solid var(--color-border); padding: 8px; text-align: left;">DH?</th>
<th style="border: 1px solid var(--color-border); padding: 8px; text-align: left;">notes</th>
</tr>
</thead>
<tbody>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0 0</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Any</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Any</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">no enc</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">n/a</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">no encryption</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0 1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">ElG</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">ElG</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">AES</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">no</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">As of 0.9.7</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">1 0</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">ECIES</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">ElG</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">AEAD</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">no</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">As of 0.9.46</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">1 0</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">ECIES</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">ECIES</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">AEAD</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">no</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">As of 0.9.49</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">1 1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">ElG</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">ECIES</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">AES</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">yes</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">TBD</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">1 1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">ECIES</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">ECIES</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">AEAD</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">yes</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">TBD</td>
</tr>
</tbody>
</table>
#### Sem Criptografia

reply_key, tags e reply_tags não estão presentes.

#### ElG para ElG

Suportado a partir da versão 0.9.7. Descontinuado a partir da versão 0.9.58. Destino ElG envia uma consulta para um router ElG.

Geração de chave do solicitante:

```
reply_key :: CSRNG(32) 32 bytes random data
reply_tags :: Each is CSRNG(32) 32 bytes random data
```
Formato da mensagem:

```
reply_key ::
     32 byte SessionKey big-endian
     only included if encryptionFlag == 1 AND ECIESFlag == 0, only as of release 0.9.7

tags ::
     1 byte Integer
     valid range: 1-32 (typically 1)
     the number of reply tags that follow
     only included if encryptionFlag == 1 AND ECIESFlag == 0, only as of release 0.9.7

reply_tags ::
     one or more 32 byte SessionTags (typically one)
     only included if encryptionFlag == 1 AND ECIESFlag == 0, only as of release 0.9.7
```
#### ECIES para ElG

Suportado a partir da versão 0.9.46. Descontinuado a partir da versão 0.9.58. O destino ECIES envia uma consulta para um router ElG. Os campos reply_key e reply_tags são redefinidos para uma resposta criptografada com ECIES.

Geração de chave do solicitante:

```
reply_key :: CSRNG(32) 32 bytes random data
reply_tags :: Each is CSRNG(8) 8 bytes random data
```
Formato da mensagem: Redefina os campos reply_key e reply_tags como segue:

```
reply_key ::
     32 byte ECIES SessionKey big-endian
     only included if encryptionFlag == 0 AND ECIESFlag == 1, only as of release 0.9.46

tags ::
     1 byte Integer
     required value: 1
     the number of reply tags that follow
     only included if encryptionFlag == 0 AND ECIESFlag == 1, only as of release 0.9.46

reply_tags ::
     an 8 byte ECIES SessionTag
     only included if encryptionFlag == 0 AND ECIESFlag == 1, only as of release 0.9.46
```
A resposta é uma mensagem ECIES Existing Session, conforme definido em [ECIES](/docs/specs/ecies/).

#### Formato de resposta

Esta é a mensagem de sessão existente, igual à do [ECIES](/docs/specs/ecies/), copiada abaixo para referência.

```
+----+----+----+----+----+----+----+----+
|       Session Tag                     |
+----+----+----+----+----+----+----+----+
|                                       |
+            Payload Section            +
|       ChaCha20 encrypted data         |
~                                       ~
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|  Poly1305 Message Authentication Code |
+              (MAC)                    +
|             16 bytes                  |
+----+----+----+----+----+----+----+----+

Session Tag :: 8 bytes, cleartext

Payload Section encrypted data :: remaining data minus 16 bytes

MAC :: Poly1305 message authentication code, 16 bytes
```
Parâmetros AEAD:

```
tag :: 8 byte reply_tag

k :: 32 byte session key
   The reply_key.

n :: 0

ad :: The 8 byte reply_tag

payload :: Plaintext data, the DSM or DSRM.

ciphertext = ENCRYPT(k, n, payload, ad)
```
#### ECIES para ECIES (0.9.49)

Destino ECIES ou router envia uma consulta para um router ECIES. Suportado a partir da versão 0.9.49.

Os routers ECIES foram introduzidos na versão 0.9.48, veja a [Proposta 156](/proposals/156/). Os destinos e routers ECIES podem usar o mesmo formato da seção "ECIES para ElG" acima, com chaves de resposta incluídas na solicitação. A criptografia da mensagem de consulta é especificada em [ECIES-ROUTERS](/docs/specs/ecies-routers/). O solicitante é anônimo.

#### ECIES para ECIES (futuro)

Esta opção ainda não está completamente definida. Consulte a [Proposta 156](/proposals/156/).

#### Notas

- Antes da versão 0.9.16, a chave pode ser para um RouterInfo ou LeaseSet, pois eles estão no mesmo espaço de chaves, e não havia uma flag para solicitar apenas um tipo específico de dados.

- Flag de encriptação, chave de resposta e tags de resposta a partir da versão 0.9.7.

- Respostas criptografadas são úteis apenas quando a resposta é através de um tunnel.

- O número de tags incluídas poderia ser maior que um se estratégias alternativas de busca DHT (por exemplo, buscas recursivas) forem implementadas.

- A chave de busca e as chaves de exclusão são os hashes "reais", NÃO chaves de roteamento.

- Os tipos 3, 5 e 7 podem ser retornados a partir da versão 0.9.38. Consulte a proposta 123 para mais informações.

- Notas de busca exploratória: Uma busca exploratória é definida para retornar uma lista de hashes não-floodfill próximos à chave. No entanto, veja as notas importantes para DatabaseSearchReply para variantes de implementação. Além disso, esta especificação nunca deixou claro se o receptor deve buscar a chave de pesquisa para um RI e retornar um DatabaseStore em vez de um DSRM se presente. O Java faz a busca; o i2pd não faz. Portanto, não é recomendado usar uma busca exploratória para hashes recebidos anteriormente.

### DatabaseSearchReply {#msg-DatabaseSearchReply}

#### Descrição

A resposta para uma Mensagem [DatabaseLookup](#msg-DatabaseLookup) que falhou

#### Conteúdo

Uma lista de hashes de router mais próximos da chave solicitada

```
+----+----+----+----+----+----+----+----+
| SHA256 hash as query key              |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
| num| peer_hashes                      |
+----+                                  +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+    +----+----+----+----+----+----+----+
|    | from                             |
+----+                                  +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+    +----+----+----+----+----+----+----+
|    |
+----+

key ::
    32 bytes
    SHA256 of the object being searched

num ::
    1 byte Integer
    number of peer hashes that follow, 0-255

peer_hashes ::
          $num SHA256 hashes of 32 bytes each (total $num*32 bytes)
          SHA256 of the RouterIdentity that the other router thinks is close
          to the key

from ::
     32 bytes
     SHA256 of the RouterInfo of the router this reply was sent from
```
#### Notas

- O hash 'from' não é autenticado e não pode ser confiável.

- Os hashes de peer retornados não são necessariamente mais próximos da chave do que o router sendo consultado. Para respostas a buscas regulares, isso facilita a descoberta de novos floodfills e busca "para trás" (mais distante da chave) para robustez.

- A chave para uma consulta de exploração é geralmente gerada aleatoriamente. Portanto, os peer_hashes não-floodfill da resposta podem ser selecionados usando um algoritmo otimizado, como fornecer peers que estão próximos à chave, mas não necessariamente os mais próximos em toda a base de dados de rede local, para evitar uma ordenação ou busca ineficiente de toda a base de dados local. Outras estratégias como cache também podem ser apropriadas. Isso depende da implementação.

- Número típico de hashes retornados: 3

- Número máximo recomendado de hashes a retornar: 16

- A chave de pesquisa, hashes de peers, e hash de origem são hashes "reais", NÃO chaves de roteamento.

### DeliveryStatus {#msg-DeliveryStatus}

#### Descrição

Um simples reconhecimento de mensagem. Geralmente criado pelo originador da mensagem e encapsulado numa Garlic Message junto com a própria mensagem, para ser retornado pelo destino.

Esta mensagem também é usada para teste de túnel, no qual o originador a envia por meio de um túnel de saída, para um túnel de entrada, de volta para si mesmo. Nessa aplicação, ela também é normalmente encapsulada com alho (Garlic wrapped). O teste de túnel é obrigatório a partir da versão 0.9.68 da API, em 2026-02, pois os roteadores podem descartar túneis participantes que não tenham recebido qualquer tráfego após os primeiros dois minutos.

#### Conteúdo

O ID da mensagem entregue e a hora de criação ou chegada.

```
+----+----+----+----+----+----+----+----+----+----+----+----+
| msg_id            |           time_stamp                  |
+----+----+----+----+----+----+----+----+----+----+----+----+

msg_id :: Integer
       4 bytes
       unique ID of the message we deliver the DeliveryStatus for (see
       I2NPMessageHeader for details)

time_stamp :: Date
             8 bytes
             time the message was successfully created or delivered
```
#### Notas

- Parece que o carimbo de tempo é sempre definido pelo criador para o tempo atual. No entanto, há vários usos disso no código, e mais podem ser adicionados no futuro.

- Esta mensagem também é usada como confirmação de sessão estabelecida no SSU [SSU-ED](/docs/transports/ssu/#establishDirect). Neste caso, o ID da mensagem é definido para um número aleatório, e o "tempo de chegada" é definido para o ID atual de toda a rede, que é 2 (ou seja, 0x0000000000000002).

### Garlic {#msg-Garlic}

Aviso: Este é o formato usado para mensagens de alho criptografadas com ElGamal [CRYPTO-ELG](/docs/specs/cryptography/#elgamal). O formato para mensagens de alho e favos de alho criptografados com ECIES-AEAD-X25519-Ratchet é significativamente diferente; veja [ECIES](/docs/specs/ecies/) para a especificação.

#### Descrição

Usado para agrupar múltiplas mensagens I2NP criptografadas

#### Conteúdo

Quando descriptografado, uma série de [Dentes de Alho](#struct-GarlicClove) e dados adicionais, também conhecidos como Conjunto de Dentes (Clove Set).

Criptografado:

```
+----+----+----+----+----+----+----+----+
|      length       | data              |
+----+----+----+----+                   +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+

length ::
       4 byte Integer
       number of bytes that follow 0 - 64 KB

data ::
     $length bytes
     ElGamal encrypted data
```
Dados descriptografados, também conhecidos como Conjunto de Clove:

```
+----+----+----+----+----+----+----+----+
| num|  clove 1                         |
+----+                                  +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|         clove 2 ...                   |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| Certificate  |   Message_ID      |
+----+----+----+----+----+----+----+----+
          Expiration               |
+----+----+----+----+----+----+----+

num ::
     1 byte Integer number of GarlicCloves to follow

clove ::  a GarlicClove

Certificate :: always NULL in the current implementation (3 bytes total, all zeroes)

Message_ID :: 4 byte Integer

Expiration :: Date (8 bytes)
```
#### Notas

- Quando não criptografado, os dados contêm um ou mais [Garlic Cloves](#struct-GarlicClove).

- O bloco criptografado AES é preenchido para um mínimo de 128 bytes; com a Session Tag de 32 bytes, o tamanho mínimo da mensagem criptografada é de 160 bytes; com os 4 bytes de comprimento, o tamanho mínimo da Garlic Message é de 164 bytes.

- O comprimento máximo real é menor que 64 KB; veja [I2NP](/docs/protocol/i2np/).

- Veja também a [especificação ElGamal/AES](/docs/specs/elgamal-aes/).

- Veja também a [especificação de garlic routing](/docs/overview/garlic-routing/).

- O tamanho mínimo de 128 bytes do bloco criptografado AES não é atualmente configurável, no entanto o tamanho mínimo de uma DataMessage em um GarlicClove em uma GarlicMessage, com overhead, é de 128 bytes mesmo assim. Uma opção configurável para aumentar o tamanho mínimo pode ser adicionada no futuro.

- O ID da mensagem é geralmente definido como um número aleatório na transmissão e parece ser ignorado no recebimento.

- No futuro, o certificado poderia possivelmente ser usado para um HashCash para "pagar" pelo roteamento.

### TunnelData {#msg-TunnelData}

#### Descrição

Uma mensagem enviada do gateway ou participante de um túnel para o próximo participante ou ponto final. Os dados têm comprimento fixo e contêm mensagens I2NP que são fragmentadas, agrupadas, preenchidas e criptografadas.

#### Conteúdo

```
+----+----+----+----+----+----+----+----+
|     tunnnelID     | data              |
+----+----+----+----+                   |
|                                       |
~                                       ~
~                                       ~
|                                       |
+                   +----+----+----+----+
|                   |
+----+----+----+----+

tunnelId ::
         4 byte TunnelId
         identifies the tunnel this message is directed at
         nonzero

data ::
     1024 bytes
     payload data.. fixed to 1024 bytes
```
#### Notas

- O ID da mensagem I2NP para esta mensagem é definido como um novo número aleatório a cada salto.

- Veja também a [Especificação de Mensagem de Tunnel](/docs/legacy/tunnel-message/)

### TunnelGateway {#msg-TunnelGateway}

#### Descrição

Envolve outra mensagem I2NP para ser enviada a um túnel no gateway de entrada do túnel.

#### Conteúdo

```
+----+----+----+----+----+----+----+-//
| tunnelId          | length  | data...
+----+----+----+----+----+----+----+-//

tunnelId ::
         4 byte TunnelId
         identifies the tunnel this message is directed at
         nonzero

length ::
       2 byte Integer
       length of the payload

data ::
     $length bytes
     actual payload of this message
```
#### Notas

- O payload é uma mensagem I2NP com um cabeçalho padrão de 16 bytes.

### Data {#msg-Data}

#### Descrição

Usado por Mensagens de Alho e Pedaços de Alho para encapsular dados arbitrários.

#### Conteúdo

Um inteiro de comprimento, seguido por dados opacos.

```
+----+----+----+----+----+-//-+
| length            | data... |
+----+----+----+----+----+-//-+

length ::
       4 bytes
       length of the payload

data ::
     $length bytes
     actual payload of this message
```
#### Notas

- Esta mensagem não contém informações de roteamento e nunca será enviada "desembrulhada". É usada apenas dentro de mensagens `Garlic`.

### TunnelBuild {#msg-TunnelBuild}

OBSOLETO, use [VariableTunnelBuild](#msg-VariableTunnelBuild)

```
+----+----+----+----+----+----+----+----+
| Record 0 ...                          |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| Record 1 ...                          |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| Record 7 ...                          |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+

Just 8 BuildRequestRecords attached together
record size: 528 bytes
total size: 8*528 = 4224 bytes
```
#### Notas

- A partir da versão 0.9.48, pode também conter ECIES-X25519 BuildRequestRecords, veja [ECIES Tunnel Creation](/docs/specs/tunnel-creation-ecies/).

- Veja também a [especificação de criação de tunnel](/docs/specs/tunnel-creation/).

- O ID da mensagem I2NP para esta mensagem deve ser definido de acordo com a especificação de criação de tunnel.

- Embora esta mensagem seja raramente vista na rede atual, tendo sido substituída pela mensagem `VariableTunnelBuild`, ainda pode ser usada para tunnels muito longos, e não foi descontinuada. Routers devem implementar.

### TunnelBuildReply {#msg-TunnelBuildReply}

OBSOLETO, use [VariableTunnelBuildReply](#msg-VariableTunnelBuildReply)

```
Same format as TunnelBuildMessage, with BuildResponseRecords
```
#### Notas

- A partir da versão 0.9.48, também pode conter ECIES-X25519 BuildResponseRecords, consulte [ECIES Tunnel Creation](/docs/specs/tunnel-creation-ecies/).

- Veja também a [especificação de criação de tunnel](/docs/specs/tunnel-creation/).

- O ID da mensagem I2NP para esta mensagem deve ser definido de acordo com a especificação de criação de tunnel.

- Embora esta mensagem seja raramente vista na rede atual, tendo sido substituída pela mensagem `VariableTunnelBuildReply`, ainda pode ser usada para tunnels muito longos e não foi depreciada. Os routers devem implementar.

### VariableTunnelBuild {#msg-VariableTunnelBuild}

```
+----+----+----+----+----+----+----+----+
| num| BuildRequestRecords...
+----+----+----+----+----+----+----+----+

Same format as TunnelBuildMessage, except for the addition of a $num field
in front and $num number of BuildRequestRecords instead of 8

num ::
       1 byte Integer
       Valid values: 1-8

record size: 528 bytes
total size: 1+$num*528
```
#### Notas

- A partir de 0.9.48, pode também conter BuildRequestRecords ECIES-X25519, consulte [ECIES Tunnel Creation](/docs/specs/tunnel-creation-ecies/).

- Esta mensagem foi introduzida na versão 0.7.12 do router, e pode não ser enviada para participantes de tunnel anteriores a essa versão.

- Veja também a [especificação de criação de tunnel](/docs/specs/tunnel-creation/).

- O ID da mensagem I2NP para esta mensagem deve ser definido de acordo com a especificação de criação de tunnel.

- O número típico de registros na rede atual é 4, para um tamanho total de 2113.

### VariableTunnelBuildReply {#msg-VariableTunnelBuildReply}

```
+----+----+----+----+----+----+----+----+
| num| BuildResponseRecords...
+----+----+----+----+----+----+----+----+

Same format as VariableTunnelBuildMessage, with BuildResponseRecords.
```
#### Notas

- A partir da versão 0.9.48, também pode conter BuildResponseRecords ECIES-X25519, consulte [ECIES Tunnel Creation](/docs/specs/tunnel-creation-ecies/).

- Esta mensagem foi introduzida na versão 0.7.12 do router, e pode não ser enviada para participantes de tunnel anteriores a essa versão.

- Veja também a [especificação de criação de tunnel](/docs/specs/tunnel-creation/).

- O ID da mensagem I2NP para esta mensagem deve ser definido de acordo com a especificação de criação de tunnel.

- O número típico de registros na rede atual é 4, para um tamanho total de 2113.

### ShortTunnelBuild {#msg-ShortTunnelBuild}

#### Descrição

A partir da versão da API 0.9.51, apenas para roteadores ECIES-X25519.

```
+----+----+----+----+----+----+----+----+
| num| ShortBuildRequestRecords...
+----+----+----+----+----+----+----+----+

Same format as VariableTunnelBuildMessage,
except that the record size is 218 bytes instead of 528

num ::
       1 byte Integer
       Valid values: 1-8

record size: 218 bytes
total size: 1+$num*218
```
#### Notas

- A partir da versão 0.9.51. Veja [Criação de Tunnel ECIES](/docs/specs/tunnel-creation-ecies/).

- Esta mensagem foi introduzida na versão 0.9.51 do router e pode não ser enviada para participantes do tunnel em versões anteriores.

- O número típico de registros na rede atual é 4, para um tamanho total de 873.

### OutboundTunnelBuildReply {#msg-OutboundTunnelBuildReply}

#### Descrição

Enviado do ponto de extremidade de saída de um novo túnel para o originador. A partir da versão da API 0.9.51, apenas para roteadores ECIES-X25519.

```
+----+----+----+----+----+----+----+----+
| num| ShortBuildResponseRecords...
+----+----+----+----+----+----+----+----+

Same format as ShortTunnelBuildMessage, with ShortBuildResponseRecords.
```
#### Notas

- A partir da versão 0.9.51. Consulte [Criação de Tunnel ECIES](/docs/specs/tunnel-creation-ecies/).

- O número típico de registros na rede atual é 4, para um tamanho total de 873.

## Referências

- **[CRYPTO-ELG]** [Criptografia - ElGamal](/docs/specs/cryptography/#elgamal)
- **[Date]** [Estruturas Comuns - Data](/docs/specs/common-structures/#date)
- **[ECIES]** [Especificação ECIES](/docs/specs/ecies/)
- **[ECIES-ROUTERS]** [Especificação de routers ECIES](/docs/specs/ecies-routers/)
- **[ElG-AES]** [ElGamal/AES](/docs/specs/elgamal-aes/)
- **[GARLICSPEC]** [Garlic Routing](/docs/overview/garlic-routing/)
- **[Hash]** [Estruturas Comuns - Hash](/docs/specs/common-structures/#hash)
- **[I2NP]** [Protocolo I2NP](/docs/protocol/i2np/)
- **[Integer]** [Estruturas Comuns - Integer](/docs/specs/common-structures/#integer)
- **[NTCP2]** [Especificação NTCP2](/docs/specs/ntcp2/)
- **[Prop156]** [Proposta 156](/proposals/156/)
- **[Prop157]** [Proposta 157](/proposals/157/)
- **[RouterIdentity]** [Estruturas Comuns - RouterIdentity](/docs/specs/common-structures/#routeridentity)
- **[SSU]** [Transporte SSU](/docs/transports/ssu/)
- **[SSU-ED]** [Transporte SSU - Establish Direct](/docs/transports/ssu/#establishDirect)
- **[SSU2]** [Especificação SSU2](/docs/specs/ssu2/)
- **[TMDI]** [Instruções de Entrega de Mensagem tunnel](/docs/legacy/tunnel-message/#tunnel-message-delivery-instructions)
- **[TUNNEL-CREATION]** [Especificação de Criação de tunnel](/docs/specs/tunnel-creation/)
- **[TUNNEL-CREATION-ECIES]** [Criação de tunnel ECIES](/docs/specs/tunnel-creation-ecies/)
- **[TUNNEL-IMPL]** [Implementação de tunnel](/docs/specs/tunnel-implementation/)
- **[TUNNEL-MSG]** [Especificação de Mensagem tunnel](/docs/legacy/tunnel-message/)
- **[TunnelId]** [Estruturas Comuns - TunnelId](/docs/specs/common-structures/#tunnelid)
