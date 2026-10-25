---
title: "SSU (Secure Semireliable UDP)"
description: "Especificação original do protocolo de transporte UDP (descontinuado, substituído pelo SSU2)"
slug: "ssu"
aliases:
  - "/pt/docs/transport/ssu"
  - "/pt/docs/transport/ssu/"
  - "/pt/docs/transports/ssu"
  - "/pt/docs/transports/ssu/"
  - "/pt/docs/specs/ssu-spec"
  - "/pt/docs/specs/ssu-spec/"
  - "/pt/udp_spec"
  - "/pt/udp_spec/"
category: "Transportes"
lastUpdated: "2024-01"
accurateFor: "0.9.61"
---

## Visão Geral

DESCONTINUADO - SSU foi substituído por SSU2. O suporte para SSU foi removido do i2pd na versão 2.44.0 (API 0.9.56) 2022-11. O suporte para SSU foi removido do Java I2P na versão 2.4.0 (API 0.9.61) 2023-12.

Consulte a [visão geral do SSU](/docs/transport/ssu/) para mais informações.

## Troca de Chaves DH {#dh}

A troca inicial de chaves DH de 2048 bits está descrita na [página de Chaves SSU](/docs/transport/ssu/#keys). Esta troca usa o mesmo primo compartilhado usado para a [criptografia ElGamal](/docs/specs/cryptography/#elgamal) do I2P.

## Cabeçalho da Mensagem {#header}

Todos os datagramas UDP começam com um MAC (Message Authentication Code) de 16 bytes e um IV (Initialization Vector) de 16 bytes seguidos por uma carga útil de tamanho variável criptografada com a chave apropriada. O MAC usado é HMAC-MD5, truncado para 16 bytes, enquanto a chave é uma chave AES256 completa de 32 bytes. A construção específica do MAC são os primeiros 16 bytes de:

```
HMAC-MD5(encryptedPayload + IV + (payloadLength ^ protocolVersion ^ ((netid - 2) << 8)), macKey)
```
onde '+' significa anexar e '^' significa ou-exclusivo.

O IV é gerado aleatoriamente para cada pacote. O encryptedPayload é a versão criptografada da mensagem começando com o byte de flag (encrypt-then-MAC). O payloadLength usado no MAC é um inteiro sem sinal de 2 bytes, big endian. Note que protocolVersion é 0, então o exclusive-or é um no-op. A macKey é ou a chave de introdução ou é construída a partir da chave DH trocada (veja detalhes abaixo), conforme especificado para cada mensagem abaixo.

**AVISO** - o HMAC-MD5-128 usado aqui não é padrão, consulte [detalhes do HMAC](/docs/specs/cryptography/#udp) para mais informações.

O payload em si (isto é, a mensagem começando com o byte de flag) é criptografado com AES256/CBC usando o IV e a sessionKey, com prevenção de replay abordada dentro do seu corpo, explicado abaixo.

O protocolVersion é um inteiro sem sinal de 2 bytes, big endian, e está atualmente definido como 0. Peers que usam uma versão de protocolo diferente não conseguirão se comunicar com este peer, embora versões anteriores que não usam esta flag consigam.

O OR exclusivo de ((netid - 2) << 8) é usado para identificar rapidamente conexões entre redes. O netid é um inteiro sem sinal de 2 bytes, big endian, e está atualmente definido como 2. A partir da versão 0.9.42. Consulte a proposta 147 para mais informações. Como o ID de rede atual é 2, isto é uma operação sem efeito para a rede atual e é compatível com versões anteriores. Quaisquer conexões de redes de teste devem ter um ID diferente e falharão no HMAC.

### Especificação HMAC

- Preenchimento interno: 0x36...
- Preenchimento externo: 0x5C...
- Chave: 32 bytes
- Função de digest hash: MD5, 16 bytes
- Tamanho do bloco: 64 bytes
- Tamanho do MAC: 16 bytes
- Implementações C de exemplo:
  - hmac.h em [i2pd](https://github.com/PurpleI2P/i2pd)
  - I2PHMAC.cpp em [i2pcpp](http://git.repo.i2p/w/i2pcpp.git)
- Implementação Java de exemplo:
  - I2PHMac.java em [I2P](https://github.com/i2p/i2p.i2p)

### Detalhes da Chave de Sessão

A chave de sessão de 32 bytes é criada da seguinte forma:

1. Pegue a chave DH trocada, representada como um array de bytes BigInteger de comprimento mínimo positivo (complemento de dois big-endian)
2. Se o bit mais significativo for 1 (ou seja, array[0] & 0x80 != 0), adicione um byte 0x00 no início, como na representação BigInteger.toByteArray() do Java
3. Se o array de bytes for maior ou igual a 32 bytes, use os primeiros (mais significativos) 32 bytes
4. Se o array de bytes for menor que 32 bytes, adicione bytes 0x00 ao final para estender para 32 bytes. *Muito improvável - Veja nota abaixo.*

### Detalhes da Chave MAC

A chave MAC de 32 bytes é criada da seguinte forma:

1. Pegue o array de bytes da chave DH trocada, precedido por um byte 0x00 se
   necessário, do passo 2 nos Detalhes da Chave de Sessão acima.
2. Se esse array de bytes for maior ou igual a 64 bytes, a chave MAC
   são os bytes 33-64 desse array de bytes.
3. Se esse array de bytes for menor que 64 bytes, a chave MAC é o
   Hash SHA-256 desse array de bytes. *A partir da versão 0.9.8. Veja nota abaixo.*

#### Nota importante

O código anterior ao lançamento 0.9.8 estava com defeito e não tratava corretamente arrays de bytes de chaves DH entre 32 e 63 bytes (passos 3 e 4 acima) e a conexão falharia. Como esses casos nunca funcionaram, eles foram redefinidos conforme descrito acima para o lançamento 0.9.8, e o caso de 0-32 bytes também foi redefinido. Uma vez que a chave DH trocada nominal é de 256 bytes, as chances da representação mínima ser menor que 64 bytes são extremamente pequenas.

### Formato do Cabeçalho

Dentro do payload criptografado AES, há uma estrutura comum mínima para as várias mensagens - uma flag de um byte e um timestamp de envio de quatro bytes (segundos desde a época unix).

O formato do cabeçalho é:

```
Header: 37+ bytes
  Encryption starts with the flag byte.
  +----+----+----+----+----+----+----+----+
  |                  MAC                  |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                   IV                  |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |flag|        time       |              |
  +----+----+----+----+----+              +
  | keying material (optional)            |
  +                                       +
  |                                       |
  ~                                       ~
  |                                       |
  +                        +----+----+----+
  |                        |#opt|         |
  +----+----+----+----+----+----+         +
  | #opt extended option bytes (optional) |
  ~                                       ~
  ~                                       ~
  +----+----+----+----+----+----+----+----+
```
O byte de flag contém os seguintes campos de bits:

```
Bit order: 76543210 (bit 7 is MSB)

  bits 7-4: payload type
     bit 3: If 1, rekey data is included. Always 0, unimplemented
     bit 2: If 1, extended options are included. Always 0 before release
            0.9.24.
  bits 1-0: reserved, set to 0 for compatibility with future uses
```
Sem rekeying e opções estendidas, o tamanho do cabeçalho é de 37 bytes.

### Rekeying {#rekey}

Se a flag de rekey estiver definida, 64 bytes de material de chave seguem o timestamp.

Ao regerar chaves, os primeiros 32 bytes do material de chaveamento são fornecidos a um SHA256 para produzir a nova chave MAC, e os próximos 32 bytes são fornecidos a um SHA256 para produzir a nova chave de sessão, embora as chaves não sejam usadas imediatamente. O outro lado também deve responder com a flag de regeração de chaves definida e esse mesmo material de chaveamento. Uma vez que ambos os lados tenham enviado e recebido esses valores, as novas chaves devem ser usadas e as chaves anteriores descartadas. Pode ser útil manter as chaves antigas por um breve período, para lidar com perda de pacotes e reordenação.

NOTA: A regeneração de chaves não está implementada atualmente.

### Opções Estendidas {#extend}

Se a flag de opções estendidas estiver definida, um valor de tamanho de opção de um byte é anexado, seguido por essa quantidade de bytes de opções estendidas. As opções estendidas sempre fizeram parte da especificação, mas não foram implementadas até a versão 0.9.24. Quando presentes, o formato da opção é específico para o tipo de mensagem. Consulte a documentação da mensagem abaixo sobre se opções estendidas são esperadas para a mensagem em questão, e o formato especificado. Embora os routers Java sempre tenham reconhecido a flag e o comprimento das opções, outras implementações não o fizeram. Portanto, não envie opções estendidas para routers anteriores à versão 0.9.24.

## Preenchimento

Todas as mensagens contêm 0 ou mais bytes de preenchimento. Cada mensagem deve ser preenchida para um limite de 16 bytes, conforme exigido pela [camada de criptografia AES256](/docs/specs/cryptography/#AES).

Até a versão 0.9.7, as mensagens eram preenchidas apenas até o próximo limite de 16 bytes, e mensagens que não fossem múltiplas de 16 bytes poderiam ser inválidas.

A partir da versão 0.9.7, as mensagens podem ser preenchidas com qualquer comprimento, desde que a MTU atual seja respeitada. Quaisquer bytes de preenchimento extras de 1-15 além do último bloco de 16 bytes não podem ser criptografados ou descriptografados e serão ignorados. No entanto, o comprimento total e todo o preenchimento são incluídos no cálculo do MAC.

A partir da versão 0.9.8, as mensagens transmitidas não são necessariamente um múltiplo de 16 bytes. A mensagem SessionConfirmed é uma exceção, veja abaixo.

## Chaves

As assinaturas nas mensagens SessionCreated e SessionConfirmed são geradas usando a [SigningPublicKey](/docs/specs/common-structures/#signingpublickey) da [RouterIdentity](/docs/specs/common-structures/#routeridentity) que é distribuída fora da banda através da publicação na base de dados da rede, e a [SigningPrivateKey](/docs/specs/common-structures/#signingprivatekey) associada.

Até a versão 0.9.15, o algoritmo de assinatura era sempre DSA, com uma assinatura de 40 bytes.

A partir da versão 0.9.16, o algoritmo de assinatura pode ser especificado por um [KeyCertificate](/docs/specs/common-structures/#key-certificates) na [RouterIdentity](/docs/specs/common-structures/#routeridentity) do Bob.

Tanto as chaves de introdução quanto as chaves de sessão têm 32 bytes e são definidas pela especificação de estruturas comuns [SessionKey](/docs/specs/common-structures/#sessionkey). A chave usada para o MAC e criptografia é especificada para cada mensagem abaixo.

As chaves de introdução são entregues através de um canal externo (a base de dados da rede), onde tradicionalmente eram idênticas ao Hash do router até a versão 0.9.47, mas podem ser aleatórias a partir da versão 0.9.48.

## Notas

### IPv6

A especificação do protocolo permite tanto endereços IPv4 de 4 bytes quanto endereços IPv6 de 16 bytes. SSU-over-IPv6 é suportado a partir da versão 0.9.8. Consulte a documentação de mensagens individuais abaixo para detalhes sobre o suporte IPv6.

### Carimbos de Tempo {#time}

Embora a maior parte do I2P use timestamps de [Date](/docs/specs/common-structures/#date) de 8 bytes com resolução de milissegundos, o SSU usa timestamps de números inteiros não assinados de 4 bytes com resolução de um segundo. Como esses valores são não assinados, eles não farão rollover até fevereiro de 2106.

## Mensagens

Existem 10 mensagens (tipos de payload) definidas:

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Type</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Message</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Notes</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#sessionrequest">SessionRequest</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#sessioncreated">SessionCreated</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">2</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#sessionconfirmed">SessionConfirmed</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">3</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#relayrequest">RelayRequest</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">4</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#relayresponse">RelayResponse</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#relayintro">RelayIntro</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">6</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#data">Data</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">7</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#peertest">PeerTest</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">8</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#sessiondestroyed">SessionDestroyed</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Implemented as of 0.8.9</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">n/a</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#holepunch">HolePunch</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
</table>
### SessionRequest (tipo 0) {#sessionrequest}

Esta é a primeira mensagem enviada para estabelecer uma sessão.

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Peer:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Alice to Bob</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Data:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">256 byte X, to begin the DH agreement; 1 byte IP address size; that many bytes representation of Bob's IP address; N bytes, currently uninterpreted</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Crypto Key used:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Bob's introKey, as retrieved from the network database</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>MAC Key used:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Bob's introKey, as retrieved from the network database</td>
</tr>
</table>
Formato da mensagem:

```
+----+----+----+----+----+----+----+----+
|         X, as calculated from DH      |
~                .  .  .                ~
|                                       |
+----+----+----+----+----+----+----+----+
|size| that many byte IP address (4-16) |
+----+----+----+----+----+----+----+----+
| arbitrary amount of uninterpreted data|
~                .  .  .                ~
```
Tamanho típico incluindo cabeçalho, na implementação atual: 304 (IPv4) ou 320 (IPv6) bytes (antes do preenchimento não-mod-16)

#### Opções estendidas

Nota: Implementado na versão 0.9.24.

- Comprimento mínimo: 3 (byte de comprimento da opção + 2 bytes)
- Comprimento da opção: 2 mínimo
- 2 bytes de flags:

```
Bit order: 15...76543210 (bit 15 is MSB)

      bit 0: 1 for Alice to request a relay tag from Bob in the
             SessionCreated response, 0 if Alice does not need a relay tag.
             Note that "1" is the default if no extended options are present
  bits 15-1: unused, set to 0 for compatibility with future uses
```
#### Notas

- Endereços IPv4 e IPv6 são suportados.
- Os dados não interpretados poderiam possivelmente ser usados no futuro para desafios.

### SessionCreated (tipo 1) {#sessioncreated}

Esta é a resposta a uma [SessionRequest](#sessionrequest).

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Peer:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Bob to Alice</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Data:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">256 byte Y, to complete the DH agreement; 1 byte IP address size; that many bytes representation of Alice's IP address; 2 byte Alice's port number; 4 byte relay (introduction) tag which Alice can publish (else 0x00000000); 4 byte timestamp (seconds from the epoch) for use in the DSA signature; Bob's <a href="/docs/specs/common-structures/#signature">Signature</a> of the critical exchanged data (X + Y + Alice's IP + Alice's port + Bob's IP + Bob's port + Alice's new relay tag + Bob's signed on time), encrypted with another layer of encryption using the negotiated sessionKey. The IV is reused here. See notes for length information.; 0-15 bytes of padding of the signature, using random data, to a multiple of 16 bytes, so that the signature + padding may be encrypted with an additional layer of encryption using the negotiated session key as part of the DSA block.; N bytes, currently uninterpreted</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Crypto Key used:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Bob's introKey, with an additional layer of encryption over the 40 byte signature and the following 8 bytes padding.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>MAC Key used:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Bob's introKey</td>
</tr>
</table>
Formato da mensagem:

```
+----+----+----+----+----+----+----+----+
|         Y, as calculated from DH      |
~                .  .  .                ~
|                                       |
+----+----+----+----+----+----+----+----+
|size| that many byte IP address (4-16) |
+----+----+----+----+----+----+----+----+
| Port (A)| public relay tag  |  signed
+----+----+----+----+----+----+----+----+
  on time |                             |
+----+----+                             +
|                                       |
+                                       +
|             signature                 |
+                                       +
|                                       |
+                                       +
|                                       |
+         +----+----+----+----+----+----+
|         |   (0-15 bytes of padding) 
+----+----+----+----+----+----+----+----+
          |                             |
+----+----+                             +
|           arbitrary amount            |
~        of uninterpreted data          ~
~                .  .  .                ~
```
Tamanho típico incluindo cabeçalho, na implementação atual: 368 bytes (IPv4 ou IPv6) (antes do preenchimento não-mod-16)

#### Notas

- Endereços IPv4 e IPv6 são suportados.
- Se a tag de relay for diferente de zero, Bob está se oferecendo para atuar como introducer para
  Alice. Alice pode subsequentemente publicar o endereço de Bob e a tag de relay na
  base de dados da rede.
- Para a assinatura, Bob deve usar sua porta externa, pois é isso que Alice usará
  para verificar. Se o NAT/firewall de Bob mapeou sua porta interna para uma
  porta externa diferente, e Bob não tem conhecimento disso, a verificação por Alice
  falhará.
- Veja a seção [Keys](#keys) acima para detalhes sobre assinaturas. Alice já possui
  a chave pública de assinatura de Bob, da base de dados da rede.
- Até a versão 0.9.15, a assinatura era sempre uma assinatura DSA de 40 bytes e
  o padding era sempre de 8 bytes. A partir da versão 0.9.16, o tipo e
  comprimento da assinatura são implícitos pelo tipo da [SigningPublicKey](/docs/specs/common-structures/#signingpublickey) na
  [RouterIdentity](/docs/specs/common-structures/#routeridentity) de Bob. O padding é conforme necessário para um múltiplo de 16 bytes.
- Esta é a única mensagem que usa a chave de introdução do remetente. Todas as outras usam a
  chave de introdução do receptor ou a chave de sessão estabelecida.
- O tempo de assinatura parece não ser usado ou não verificado na implementação
  atual.
- Os dados não interpretados poderiam possivelmente ser usados no futuro para desafios.
- Opções estendidas no cabeçalho: Não esperadas, indefinidas.

### SessionConfirmed (tipo 2) {#sessionconfirmed}

Esta é a resposta a uma mensagem [SessionCreated](#sessioncreated) e o último passo no estabelecimento de uma sessão. Pode ser necessário múltiplas mensagens SessionConfirmed se a Router Identity precisar ser fragmentada.

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Peer:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Alice to Bob</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Data:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1 byte identity fragment info (bits 7-4: current identity fragment # 0-14; bits 3-0: total identity fragments (F) 1-15); 2 byte size of the current identity fragment; that many byte fragment of Alice's <a href="/docs/specs/common-structures/#routeridentity">RouterIdentity</a>; After the last identity fragment only: 4 byte signed-on time; N bytes padding, currently uninterpreted; After the last identity fragment only: The remaining bytes contain Alice's <a href="/docs/specs/common-structures/#signature">Signature</a> of the critical exchanged data (X + Y + Alice's IP + Alice's port + Bob's IP + Bob's port + Alice's new relay tag + Alice's signed on time). See notes for length information.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Crypto Key used:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Alice/Bob sessionKey, as generated from the DH exchange</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>MAC Key used:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Alice/Bob MAC Key, as generated from the DH exchange</td>
</tr>
</table>
**Fragmento 0 até F-2** (apenas se F > 1; atualmente não utilizado, veja as notas abaixo):

```
+----+----+----+----+----+----+----+----+
|info| cursize |                        |
+----+----+----+                        +
|      fragment of Alice's full         |
~            Router Identity            ~
~                .  .  .                ~
|                                       |
+----+----+----+----+----+----+----+----+
| arbitrary amount of uninterpreted data|
~                .  .  .                ~
```
**Fragmento F-1 (último ou único fragmento):**

```
+----+----+----+----+----+----+----+----+
|info| cursize |                        |
+----+----+----+                        +
|     last fragment of Alice's full     |
~            Router Identity            ~
~                .  .  .                ~
|                                       |
+----+----+----+----+----+----+----+----+
|  signed on time   |                   |
+----+----+----+----+                   +
|  arbitrary amount of uninterpreted    |
~      data, until the signature at     ~
~       end of the current packet       ~
|  Packet length must be mult. of 16    |
+----+----+----+----+----+----+----+----+
+                                       +
|                                       |
+                                       +
|             signature                 |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
```
Tamanho típico incluindo cabeçalho, na implementação atual: 512 bytes (com assinatura Ed25519) ou 480 bytes (com assinatura DSA-SHA1) (antes do preenchimento não-mod-16)

#### Notas

- Na implementação atual, o tamanho máximo do fragmento é 512 bytes. Isso
  deve ser estendido para que assinaturas mais longas funcionem sem fragmentação.
  A implementação atual não processa corretamente assinaturas divididas entre
  dois fragmentos.
- A [RouterIdentity](/docs/specs/common-structures/#routeridentity) típica tem 387 bytes, então nunca é
  necessária fragmentação. Se nova criptografia estender o tamanho da RouterIdentity, o
  esquema de fragmentação deve ser testado cuidadosamente.
- Não há mecanismo para solicitar ou reenviar fragmentos perdidos.
- O campo de total de fragmentos F deve ser definido identicamente em todos os fragmentos.
- Veja a seção [Keys](#keys) acima para detalhes sobre assinaturas DSA.
- O tempo de assinatura parece ser não usado ou não verificado na
  implementação atual.
- Como a assinatura está no final, o padding no último ou único pacote
  deve preencher o pacote total para um múltiplo de 16 bytes, ou a assinatura não
  será descriptografada corretamente. Isso é diferente de todos os outros tipos
  de mensagem, onde o padding está no final.
- Até a versão 0.9.15, a assinatura era sempre uma assinatura DSA de 40 bytes. A
  partir da versão 0.9.16, o tipo e comprimento da assinatura são implícitos pelo tipo da
  [SigningPublicKey](/docs/specs/common-structures/#signingpublickey) na [RouterIdentity](/docs/specs/common-structures/#routeridentity) de Alice. O padding é conforme
  necessário para um múltiplo de 16 bytes.
- Opções estendidas no cabeçalho: Não esperadas, indefinidas.

### SessionDestroyed (tipo 8) {#sessiondestroyed}

A mensagem SessionDestroyed foi implementada (apenas recepção) na versão 0.8.1, e é enviada a partir da versão 0.8.9.

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Peer:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Alice to Bob or Bob to Alice</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Data:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">none</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Crypto Key used:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Alice/Bob sessionKey</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>MAC Key used:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Alice/Bob MAC Key</td>
</tr>
</table>
Esta mensagem não contém dados. Tamanho típico incluindo cabeçalho, na implementação atual: 48 bytes (antes do preenchimento não-mod-16)

#### Notas

- Mensagens de destruição recebidas com a chave de introdução do remetente ou do destinatário serão ignoradas.
- Opções estendidas no cabeçalho: Não esperadas, indefinidas.

### RelayRequest (tipo 3) {#relayrequest}

Esta é a primeira mensagem enviada de Alice para Bob para solicitar uma apresentação a Charlie.

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Peer:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Alice to Bob</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Data:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">4 byte relay (introduction) tag, nonzero, as received by Alice in the SessionCreated message from Bob; 1 byte IP address size; that many byte representation of Alice's IP address; 2 byte port number (of Alice); 1 byte challenge size; that many bytes to be relayed to Charlie in the intro; Alice's 32-byte introduction key (so Bob can reply with Charlie's info); 4 byte nonce of Alice's relay request; N bytes, currently uninterpreted</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Crypto Key used:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Bob's introKey, as retrieved from the network database (or Alice/Bob sessionKey, if established)</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>MAC Key used:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Bob's introKey, as retrieved from the network database (or Alice/Bob MAC Key, if established)</td>
</tr>
</table>
Formato da mensagem:

```
+----+----+----+----+----+----+----+----+
|      relay tag    |size| Alice IP addr
+----+----+----+----+----+----+----+----+
     | Port (A)|size| challenge bytes   |
+----+----+----+----+                   +
|      to be delivered to Charlie       |
+----+----+----+----+----+----+----+----+
| Alice's intro key                     |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|       nonce       |                   |
+----+----+----+----+                   +
| arbitrary amount of uninterpreted data|
~                .  .  .                ~
```
Tamanho típico incluindo cabeçalho, na implementação atual: 96 bytes (IP de Alice não incluído) ou 112 bytes (IP de Alice de 4 bytes incluído) (antes do preenchimento não-múltiplo-de-16)

#### Notas

- O endereço IP só é incluído se for diferente do endereço de origem e porta do pacote.
- Esta mensagem pode ser enviada via IPv4 ou IPv6.
  Se a mensagem for via IPv6 para uma introdução IPv4,
  ou (a partir da versão 0.9.50) via IPv4 para uma introdução IPv6,
  Alice deve incluir seu endereço e porta de introdução.
  Isto é suportado a partir da versão 0.9.50.
- Se Alice incluir seu endereço/porta, Bob pode realizar validação adicional
  antes de continuar.
  - Antes da versão 0.9.24, o Java I2P rejeitava qualquer endereço ou porta que fosse
    diferente da conexão.
- Challenge não está implementado, o tamanho do challenge é sempre zero
- Retransmissão para IPv6 é suportada a partir da versão 0.9.50.
- Antes da versão 0.9.12, a chave de introdução de Bob era sempre usada. A partir da versão
  0.9.12, a chave de sessão é usada se houver uma sessão estabelecida entre
  Alice e Bob. Na prática, deve haver uma sessão estabelecida, pois Alice
  só obterá o nonce (tag de introdução) da mensagem de sessão criada,
  e Bob marcará o tag de introdução como inválido quando a sessão for destruída.
- Opções estendidas no cabeçalho: Não esperadas, indefinidas.

### RelayResponse (tipo 4) {#relayresponse}

Esta é a resposta a um [RelayRequest](#relayrequest) e é enviada do Bob para Alice.

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Peer:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Bob to Alice</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Data:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1 byte IP address size; that many byte representation of Charlie's IP address; 2 byte Charlie's port number; 1 byte IP address size; that many byte representation of Alice's IP address; 2 byte Alice's port number; 4 byte nonce sent by Alice; N bytes, currently uninterpreted</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Crypto Key used:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Alice's introKey, as received in the Relay Request (or Alice/Bob sessionKey, if established)</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>MAC Key used:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Alice's introKey, as received in the Relay Request (or Alice/Bob MAC Key, if established)</td>
</tr>
</table>
Formato da mensagem:

```
+----+----+----+----+----+----+----+----+
|size|    Charlie IP     | Port (C)|size|
+----+----+----+----+----+----+----+----+
|    Alice IP       | Port (A)|  nonce
+----+----+----+----+----+----+----+----+
          |   arbitrary amount of       |
+----+----+                             +
|          uninterpreted data           |
~                .  .  .                ~
```
Tamanho típico incluindo cabeçalho, na implementação atual: 64 (Alice IPv4) ou 80 (Alice IPv6) bytes (antes do preenchimento não-mod-16)

#### Notas

- Esta mensagem pode ser enviada via IPv4 ou IPv6.
- O endereço IP/porta da Alice são o IP/porta aparente que Bob recebeu o
  RelayRequest (não necessariamente o IP que Alice incluiu no RelayRequest),
  e podem ser IPv4 ou IPv6. Alice atualmente ignora estes no recebimento.
- O endereço IP do Charlie pode ser IPv4, ou, a partir da versão 0.9.50, IPv6,
  pois este é o endereço para o qual Alice enviará
  o SessionRequest após o Hole Punch.
- O relay para IPv6 é suportado a partir da versão 0.9.50.
- Antes da versão 0.9.12, a chave de introdução da Alice era sempre usada. A partir da versão
  0.9.12, a chave de sessão é usada se há uma sessão estabelecida entre
  Alice e Bob.
- Opções estendidas no cabeçalho: Não esperadas, indefinidas.

### RelayIntro (tipo 5) {#relayintro}

Esta é a apresentação de Alice, que é enviada do Bob para o Charlie.

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Peer:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Bob to Charlie</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Data:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1 byte IP address size; that many byte representation of Alice's IP address; 2 byte port number (of Alice); 1 byte challenge size; that many bytes relayed from Alice; N bytes, currently uninterpreted</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Crypto Key used:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Bob/Charlie sessionKey</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>MAC Key used:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Bob/Charlie MAC Key</td>
</tr>
</table>
Formato da mensagem:

```
+----+----+----+----+----+----+----+----+
|size|     Alice IP      | Port (A)|size|
+----+----+----+----+----+----+----+----+
|      that many bytes of challenge     |
+                                       +
|        data relayed from Alice        |
+----+----+----+----+----+----+----+----+
| arbitrary amount of uninterpreted data|
~                .  .  .                ~
```
Tamanho típico incluindo cabeçalho, na implementação atual: 48 bytes (antes do preenchimento não-mod-16)

#### Notas

- Para IPv4, o endereço IP da Alice é sempre 4 bytes, porque Alice está tentando se conectar ao Charlie via IPv4.
  A partir da versão 0.9.50, IPv6 é suportado, e o endereço IP da Alice pode ser 16 bytes.
- Para IPv4, esta mensagem deve ser enviada via uma conexão IPv4 estabelecida,
  pois essa é a única maneira de Bob saber o endereço IPv4 do Charlie para retornar à Alice no RelayResponse.
  A partir da versão 0.9.50, IPv6 é suportado, e esta mensagem pode ser enviada via uma conexão IPv6 estabelecida.
- A partir da versão 0.9.50, qualquer endereço SSU publicado com introducers deve conter "4" ou "6" na opção "caps".
- Challenge não está implementado, o tamanho do challenge é sempre zero
- Opções estendidas no cabeçalho: Não esperadas, indefinidas.

### Dados (tipo 6) {#data}

Esta mensagem é usada para transporte de dados e confirmação.

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Peer:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Any</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Crypto Key used:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Alice/Bob sessionKey</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>MAC Key used:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Alice/Bob MAC Key</td>
</tr>
</table>
**Dados:** 1 byte de flags (veja abaixo); se ACKs explícitos estão incluídos: 1 byte com número de ACKs, essa quantidade de MessageIds de 4 bytes sendo totalmente confirmados; se campos de bits ACK estão incluídos: 1 byte com número de campos de bits ACK, essa quantidade de MessageIds de 4 bytes + um campo de bits ACK de 1 ou mais bytes (veja notas); Se dados estendidos incluídos: 1 byte de tamanho de dados, essa quantidade de bytes de dados estendidos (atualmente não interpretados); 1 byte com número de fragmentos (pode ser zero); Se não-zero, essa quantidade de fragmentos de mensagem.

```
Flags byte:
  Bit order: 76543210 (bit 7 is MSB)
  bit 7: explicit ACKs included
  bit 6: ACK bitfields included
  bit 5: reserved
  bit 4: explicit congestion notification (ECN)
  bit 3: request previous ACKs
  bit 2: want reply
  bit 1: extended data included (unused, never set)
  bit 0: reserved
```
Cada fragmento contém: - 4 bytes messageId - 3 bytes de informação do fragmento:   - bits 23-17: fragmento # 0 - 127   - bit 16: isLast (1 = verdadeiro)   - bits 15-14: não utilizados, definidos como 0 para compatibilidade com usos futuros   - bits 13-0: tamanho do fragmento 0 - 16383 - essa quantidade de bytes de dados do fragmento

Formato da mensagem:

```
+----+----+----+----+----+----+----+----+
|flag| (additional headers, determined  |
+----+                                  +
~ by the flags, such as ACKs or         ~
| bitfields                             |
+----+----+----+----+----+----+----+----+
|#frg|     messageId     |   frag info  |
+----+----+----+----+----+----+----+----+
| that many bytes of fragment data      |
~                .  .  .                ~
|                                       |
+----+----+----+----+----+----+----+----+
|     messageId     |   frag info  |    |
+----+----+----+----+----+----+----+    +
| that many bytes of fragment data      |
~                .  .  .                ~
|                                       |
+----+----+----+----+----+----+----+----+
|     messageId     |   frag info  |    |
+----+----+----+----+----+----+----+    +
| that many bytes of fragment data      |
~                .  .  .                ~
|                                       |
+----+----+----+----+----+----+----+----+
| arbitrary amount of uninterpreted data|
~                .  .  .                ~
```
#### Notas do Campo de Bits ACK

O bitfield usa os 7 bits baixos de cada byte, com o bit alto especificando se um byte de bitfield adicional o segue (1 = verdadeiro, 0 = o byte de bitfield atual é o último). Essa sequência de arrays de 7 bits representa se um fragmento foi recebido - se um bit for 1, o fragmento foi recebido. Para esclarecer, assumindo que os fragmentos 0, 2, 5 e 9 foram recebidos, os bytes do bitfield seriam os seguintes:

```
byte 0:
   Bit order: 76543210 (bit 7 is MSB)
   bit 7: 1 (further bitfield bytes follow)
   bit 6: 0 (fragment 6 not received)
   bit 5: 1 (fragment 5 received)
   bit 4: 0 (fragment 4 not received)
   bit 3: 0 (fragment 3 not received)
   bit 2: 1 (fragment 2 received)
   bit 1: 0 (fragment 1 not received)
   bit 0: 1 (fragment 0 received)
byte 1:
   Bit order: 76543210 (bit 7 is MSB)
   bit 7: 0 (no further bitfield bytes)
   bit 6: 0 (fragment 13 not received)
   bit 5: 0 (fragment 12 not received)
   bit 4: 0 (fragment 11 not received)
   bit 3: 0 (fragment 10 not received)
   bit 2: 1 (fragment 9 received)
   bit 1: 0 (fragment 8 not received)
   bit 0: 0 (fragment 7 not received)
```
#### Notas

- A implementação atual adiciona um número limitado de acks duplicados para
  mensagens previamente reconhecidas, se houver espaço disponível.
- Se o número de fragmentos for zero, esta é uma mensagem somente de ack ou keepalive.
- O recurso ECN não está implementado, e o bit nunca é definido.
- Na implementação atual, o bit want reply é definido quando o número de
  fragmentos é maior que zero, e não é definido quando não há fragmentos.
- Dados estendidos não estão implementados e nunca estão presentes.
- A recepção de múltiplos fragmentos é suportada em todas as versões. A transmissão de
  múltiplos fragmentos está implementada na versão 0.9.16.
- Como atualmente implementado, o máximo de fragmentos é 64 (número máximo de fragmento = 63).
- Como atualmente implementado, o tamanho máximo do fragmento é, é claro, menor que o MTU.
- Tenha cuidado para não exceder o MTU máximo mesmo se houver um grande número de
  ACKs para enviar.
- O protocolo permite fragmentos de tamanho zero, mas não há razão para enviá-los.
- No SSU, os dados usam um cabeçalho I2NP curto de 5 bytes seguido pela carga útil da
  mensagem I2NP em vez do cabeçalho I2NP padrão de 16 bytes. O cabeçalho I2NP curto
  consiste apenas do tipo I2NP de um byte e expiração de 4 bytes em
  segundos. O ID da mensagem I2NP é usado como ID da mensagem para o fragmento. O
  tamanho I2NP é montado a partir dos tamanhos dos fragmentos. O checksum I2NP não é
  necessário pois a integridade da mensagem UDP é garantida pela descriptografia.
- IDs de mensagem não são números de sequência e não são consecutivos. O SSU não
  garante entrega em ordem. Embora usemos o ID da mensagem I2NP como o
  ID da mensagem SSU, do ponto de vista do protocolo SSU, eles são números aleatórios. Na verdade,
  como o router usa um único filtro Bloom para todos os pares, o ID da mensagem
  deve ser um número verdadeiramente aleatório.
- Como não há números de sequência, não há forma de ter certeza de que um ACK foi
  recebido. A implementação atual rotineiramente envia uma grande quantidade de
  ACKs duplicados. ACKs duplicados não devem ser interpretados como uma indicação de
  congestionamento.
- Notas do campo de bits ACK: O receptor de um pacote de dados não sabe quantos
  fragmentos estão na mensagem a menos que tenha recebido o último fragmento.
  Portanto, o número de bytes do campo de bits enviados em resposta pode ser menor ou maior
  que o número de fragmentos dividido por 7. Por exemplo, se o fragmento mais alto
  que o receptor viu é o número 4, apenas um byte é necessário para ser
  enviado, mesmo que possa haver 13 fragmentos no total. Até 10 bytes (ou seja, (64 / 7)
  + 1) podem ser incluídos para cada ID de mensagem reconhecido.
- Opções estendidas no cabeçalho: Não esperadas, indefinidas.

### PeerTest (tipo 7) {#peertest}

Consulte [SSU Peer Testing](/docs/transport/ssu/#peerTesting) para detalhes. Nota: O teste de peers IPv6 é suportado a partir da versão 0.9.27.

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Peer:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Any</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Data:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">4 byte nonce; 1 byte IP address size (may be zero); that many byte representation of Alice's IP address, if size > 0; 2 byte Alice's port number; Alice's or Charlie's 32-byte introduction key; N bytes, currently uninterpreted</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Crypto Key used:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">See notes below</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>MAC Key used:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">See notes below</td>
</tr>
</table>
Chave Criptográfica usada (listada em ordem de ocorrência): 1. Quando enviada de Alice para Bob: sessionKey Alice/Bob 2. Quando enviada de Bob para Charlie: sessionKey Bob/Charlie 3. Quando enviada de Charlie para Bob: sessionKey Bob/Charlie 4. Quando enviada de Bob para Alice: sessionKey Alice/Bob (ou para Bob anterior à versão 0.9.52, introKey de Alice) 5. Quando enviada de Charlie para Alice: introKey de Alice, conforme recebida na mensagem PeerTest de Bob 6. Quando enviada de Alice para Charlie: introKey de Charlie, conforme recebida na mensagem PeerTest de Charlie

Chave MAC utilizada (listada por ordem de ocorrência): 1. Quando enviado de Alice para Bob: Chave MAC Alice/Bob 2. Quando enviado de Bob para Charlie: Chave MAC Bob/Charlie 3. Quando enviado de Charlie para Bob: Chave MAC Bob/Charlie 4. Quando enviado de Bob para Alice: introKey de Alice, conforme recebido na mensagem PeerTest de Alice 5. Quando enviado de Charlie para Alice: introKey de Alice, conforme recebido na mensagem PeerTest de Bob 6. Quando enviado de Alice para Charlie: introKey de Charlie, conforme recebido na mensagem PeerTest de Charlie

Formato da mensagem:

```
+----+----+----+----+----+----+----+----+
|    test nonce     |size| Alice IP addr
+----+----+----+----+----+----+----+----+
     | Port (A)|                        |
+----+----+----+                        +
| Alice or Charlie's                    |
+ introduction key (Alice's is sent to  +
| Bob and Charlie, while Charlie's is   |
+ sent to Alice)                        +
|                                       |
+              +----+----+----+----+----+
|              | arbitrary amount of    |
+----+----+----+                        |
| uninterpreted data                    |
~                .  .  .                ~
```
Tamanho típico incluindo cabeçalho, na implementação atual: 80 bytes (antes do preenchimento não-mod-16)

#### Notas

- Quando enviado por Alice, o tamanho do endereço IP é 0, o endereço IP não está presente, e a porta
  é 0, já que Bob e Charlie não usam os dados; o objetivo é determinar
  o verdadeiro endereço IP/porta de Alice e informar Alice; Bob e Charlie não se importam com o que
  Alice pensa que seu endereço é.
- Quando enviado por Bob ou Charlie, IP e porta estão presentes, e o endereço IP tem
  4 ou 16 bytes. Teste IPv6 é suportado a partir da versão 0.9.27.
- Quando enviado por Charlie para Alice, o IP e porta são os seguintes:
  Primeira vez (mensagem 5): IP e porta solicitados por Alice conforme recebidos na mensagem 2.
  Segunda vez (mensagem 7): IP e porta reais de Alice de onde a mensagem 6 foi recebida.
- Notas IPv6: Até a versão 0.9.26, apenas teste de endereços IPv4 é suportado. Portanto, toda
  comunicação Alice-Bob e Alice-Charlie deve ser via IPv4. Comunicação Bob-Charlie,
  no entanto, pode ser via IPv4 ou IPv6. O endereço de Alice, quando
  especificado na mensagem PeerTest, deve ter 4 bytes.
  A partir da versão 0.9.27, teste de endereços IPv6 é suportado,
  e comunicação Alice-Bob e Alice-Charlie pode ser via IPv6,
  se Bob e Charlie indicarem suporte com uma capacidade 'B' em seu endereço IPv6 publicado.
  Veja a Proposta 126 para detalhes.
- Alice envia a solicitação para Bob usando uma sessão existente sobre o transporte (IPv4 ou IPv6) que ela deseja testar.
  Quando Bob recebe uma solicitação de Alice via IPv4, Bob deve selecionar um Charlie que anuncie um endereço IPv4.
  Quando Bob recebe uma solicitação de Alice via IPv6, Bob deve selecionar um Charlie que anuncie um endereço IPv6.
  A comunicação real Bob-Charlie pode ser via IPv4 ou IPv6 (ou seja, independente do tipo de endereço de Alice).
- Um peer deve manter uma tabela de estados de teste ativos (nonces). No recebimento de
  uma mensagem PeerTest, procure o nonce na tabela. Se encontrado, é um
  teste existente e você conhece seu papel (Alice, Bob, ou Charlie). Caso contrário, se
  o IP não estiver presente e a porta for 0, este é um novo teste e você é Bob.
  Caso contrário, este é um novo teste e você é Charlie.
- A partir da versão 0.9.15, Alice deve ter uma sessão estabelecida com Bob e usar
  a chave de sessão.
- Antes da versão API 0.9.52, em algumas implementações, Bob respondia para Alice usando
  a chave de introdução de Alice em vez da chave de sessão Alice/Bob, mesmo que
  Alice e Bob tenham uma sessão estabelecida (desde 0.9.15).
  A partir da versão API 0.9.52, Bob usará corretamente a chave de sessão em todas
  as implementações, e Alice deve rejeitar uma mensagem recebida de Bob
  com a chave de introdução de Alice se Bob for versão API 0.9.52 ou superior.
- Opções estendidas no cabeçalho: Não esperadas, indefinidas.

### HolePunch {#holepunch}

Um HolePunch é simplesmente um pacote UDP sem dados. Não é autenticado nem criptografado. Não contém um cabeçalho SSU, então não possui um número de tipo de mensagem. É enviado de Charlie para Alice como parte da sequência de Introduction.

## Datagramas de Exemplo {#sampledatagrams}

### Mensagem de dados mínima

- sem fragmentos, sem ACKs, sem NACKs, etc
- Tamanho: 39 bytes

```
+----+----+----+----+----+----+----+----+
|                  MAC                  |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|                   IV                  |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|flag|        time       |flag|#frg|    |
+----+----+----+----+----+----+----+    +
|  padding to fit a full AES256 block   |
+----+----+----+----+----+----+----+----+
```
### Mensagem de dados mínima com payload

- Tamanho: 46+fragmentSize bytes

```
+----+----+----+----+----+----+----+----+
|                  MAC                  |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|                   IV                  |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|flag|        time       |flag|#frg|
+----+----+----+----+----+----+----+----+
  messageId    |   frag info  |         |
----+----+----+----+----+----+         +
| that many bytes of fragment data      |
~                .  .  .                ~
|                                       |
+----+----+----+----+----+----+----+----+
```
## Referências

- [Criptografia AES](/docs/specs/cryptography/#AES)
- [Especificação de Estruturas Comuns](/docs/specs/common-structures/)
- [Data](/docs/specs/common-structures/#date)
- [Criptografia ElGamal](/docs/specs/cryptography/#elgamal)
- [Detalhes HMAC](/docs/specs/cryptography/#udp)
- [Código-fonte I2P](https://github.com/i2p/i2p.i2p)
- [Código-fonte i2pd](https://github.com/PurpleI2P/i2pd)
- [KeyCertificate](/docs/specs/common-structures/#key-certificates)
- [RouterIdentity](/docs/specs/common-structures/#routeridentity)
- [SessionKey](/docs/specs/common-structures/#sessionkey)
- [Signature](/docs/specs/common-structures/#signature)
- [SigningPrivateKey](/docs/specs/common-structures/#signingprivatekey)
- [SigningPublicKey](/docs/specs/common-structures/#signingpublickey)
- [Visão Geral SSU](/docs/transport/ssu/)
- [Chaves SSU](/docs/transport/ssu/#keys)
- [Teste de Peers SSU](/docs/transport/ssu/#peerTesting)
