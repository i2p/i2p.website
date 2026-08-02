---
title: "Transporte NTCP2"
description: "Transporte TCP baseado em Noise para conexões router-to-router"
slug: "ntcp2"
category: "Transportes"
lastUpdated: "2026-07"
accurateFor: "0.9.70"
---

## Visão Geral

NTCP2 é um protocolo de acordo de chaves autenticado que melhora a resistência do [NTCP](/docs/transport/ntcp) a várias formas de identificação automatizada e ataques.

NTCP2 é projetado para flexibilidade e coexistência com NTCP. Pode ser suportado na mesma porta que NTCP, ou numa porta diferente, ou até sem suporte simultâneo de NTCP. Consulte a seção Informações do Router Publicado abaixo para detalhes.

Assim como outros transportes I2P, o NTCP2 é definido exclusivamente para transporte ponto-a-ponto (router-para-router) de mensagens I2NP. Não é um canal de dados de propósito geral.

NTCP2 é suportado a partir da versão 0.9.36. Veja [Prop111](/proposals/111-ntcp-2) para a proposta original, incluindo discussão de contexto e informações adicionais.

## Framework de Protocolo Noise

NTCP2 usa o Noise Protocol Framework [NOISE](https://noiseprotocol.org/noise.html) (Revisão 33, 2017-10-04). Noise tem propriedades similares ao protocolo Station-To-Station [STS](#references), que é a base para o protocolo [SSU](/docs/transport/ssu). Na terminologia do Noise, Alice é a iniciadora, e Bob é o respondedor.

NTCP2 é baseado no protocolo Noise Noise_XK_25519_ChaChaPoly_SHA256. (O identificador real para a função inicial de derivação de chave é "Noise_XKaesobfse+hs2+hs3_25519_ChaChaPoly_SHA256" para indicar extensões I2P - veja a seção KDF 1 abaixo) Este protocolo Noise usa as seguintes primitivas:

- Padrão de Handshake: XK Alice transmite sua chave para Bob (X) Alice já conhece a chave estática de Bob (K)
- Função DH: X25519 X25519 DH com um comprimento de chave de 32 bytes conforme especificado na [RFC-7748](https://tools.ietf.org/html/rfc7748).
- Função de Cifra: ChaChaPoly AEAD_CHACHA20_POLY1305 conforme especificado na [RFC-7539](https://tools.ietf.org/html/rfc7539) seção 2.8. Nonce de 12 bytes, com os primeiros 4 bytes definidos como zero.
- Função de Hash: SHA256 Hash padrão de 32 bytes, já usado extensivamente no I2P.

## Adições ao Framework

NTCP2 define as seguintes melhorias para Noise_XK_25519_ChaChaPoly_SHA256. Estas geralmente seguem as diretrizes na seção 13 do [NOISE](https://noiseprotocol.org/noise.html).

1) Chaves efêmeras em texto simples são ofuscadas com criptografia AES usando uma chave e IV conhecidos. 2) Preenchimento aleatório em texto simples é adicionado às mensagens 1 e 2. O preenchimento em texto simples é incluído no cálculo do hash do handshake (MixHash). Consulte as seções KDF abaixo para a mensagem 2 e mensagem 3 parte 1. Preenchimento AEAD aleatório é adicionado à mensagem 3 e mensagens da fase de dados. 3) Um campo de comprimento de quadro de dois bytes é adicionado, conforme necessário para Noise sobre TCP, e como no obfs4. Isso é usado apenas nas mensagens da fase de dados. Os quadros AEAD das mensagens 1 e 2 têm comprimento fixo. O quadro AEAD da mensagem 3 parte 1 tem comprimento fixo. O comprimento do quadro AEAD da mensagem 3 parte 2 é especificado na mensagem 1. 4) O campo de comprimento de quadro de dois bytes é ofuscado com SipHash-2-4, como no obfs4. 5) O formato de payload é definido para as mensagens 1,2,3, e a fase de dados. É claro que estes não são definidos no framework.

## Mensagens

Todas as mensagens NTCP2 têm 65537 bytes ou menos de comprimento. O formato da mensagem é baseado nas mensagens Noise, com modificações para enquadramento e indistinguibilidade. Implementações que usam bibliotecas Noise padrão podem precisar pré-processar as mensagens recebidas de/para o formato de mensagem Noise. Todos os campos criptografados são textos cifrados AEAD.

A sequência de estabelecimento é a seguinte:

```
Alice                           Bob

SessionRequest ------------------->
<------------------- SessionCreated
SessionConfirmed ----------------->
```
Usando a terminologia do Noise, a sequência de estabelecimento e dados é a seguinte: (Propriedades de Segurança do Payload de [Noise](https://noiseprotocol.org/noise.html) )

```
XK(s, rs):           Authentication   Confidentiality
  <- s
  ...
  -> e, es                  0                2
  <- e, ee                  2                1
  -> s, se                  2                5
  <-                        2                5
```
Uma vez estabelecida uma sessão, Alice e Bob podem trocar mensagens de dados.

Todos os tipos de mensagem (SessionRequest, SessionCreated, SessionConfirmed, Data e TimeSync) são especificados nesta seção.

Algumas notações:

    - RH_A = Router Hash for Alice (32 bytes)
    - RH_B = Router Hash for Bob (32 bytes)

### Criptografia Autenticada

Existem três instâncias separadas de criptografia autenticada (CipherStates). Uma durante a fase de handshake, e duas (transmitir e receber) para a fase de dados. Cada uma tem sua própria chave de um KDF.

Dados criptografados/autenticados serão representados como

```
+----+----+----+----+----+----+----+----+
|                                       |
+                                       +
|   Encrypted and authenticated data    |
~               .   .   .               ~
|                                       |
+----+----+----+----+----+----+----+----+
```
#### ChaCha20/Poly1305

Formato de dados criptografado e autenticado.

Entradas para as funções de criptografia/descriptografia:

```
k :: 32 byte cipher key, as generated from KDF

nonce :: Counter-based nonce, 12 bytes.
         Starts at 0 and incremented for each message.
         First four bytes are always zero.
         Last eight bytes are the counter, little-endian encoded.
         Maximum value is 2**64 - 2.
         Connection must be dropped and restarted after
         it reaches that value.
         The value 2**64 - 1 must never be sent.

ad :: In handshake phase:
      Associated data, 32 bytes.
      The SHA256 hash of all preceding data.
      In data phase:
      Zero bytes

data :: Plaintext data, 0 or more bytes
```
Saída da função de criptografia, entrada da função de descriptografia:

```
+----+----+----+----+----+----+----+----+
|Obfs Len |                             |
+----+----+                             +
|       ChaCha20 encrypted data         |
~               .   .   .               ~
|                                       |
+----+----+----+----+----+----+----+----+
|  Poly1305 Message Authentication Code |
+              (MAC)                    +
|             16 bytes                  |
+----+----+----+----+----+----+----+----+

Obfs Len :: Length of (encrypted data + MAC) to follow, 16 - 65535
            Obfuscation using SipHash (see below)
            Not used in message 1 or 2, or message 3 part 1, where the length is fixed
            Not used in message 3 part 1, as the length is specified in message 1

encrypted data :: Same size as plaintext data, 0 - 65519 bytes

MAC :: Poly1305 message authentication code, 16 bytes
```
Para ChaCha20, o que é descrito aqui corresponde à [RFC-7539](https://tools.ietf.org/html/rfc7539), que também é usada de forma similar no TLS [RFC-7905](https://tools.ietf.org/html/rfc7905).

#### Notas

- Como ChaCha20 é uma cifra de fluxo, os textos simples não precisam ser preenchidos. Bytes adicionais do fluxo de chaves são descartados.
- A chave para a cifra (256 bits) é acordada por meio do SHA256 KDF. Os detalhes do KDF para cada mensagem estão em seções separadas abaixo.
- Os frames ChaChaPoly para as mensagens 1, 2 e a primeira parte da mensagem 3 são de tamanho conhecido. A partir da segunda parte da mensagem 3, os frames são de tamanho variável. O tamanho da parte 1 da mensagem 3 é especificado na mensagem 1. A partir da fase de dados, os frames são precedidos por um comprimento de dois bytes ofuscado com SipHash como no obfs4.
- O preenchimento está fora do frame de dados autenticado para as mensagens 1 e 2. O preenchimento é usado no KDF para a próxima mensagem, então a adulteração será detectada. A partir da mensagem 3, o preenchimento está dentro do frame de dados autenticado.

#### Tratamento de Erros AEAD

- Nas mensagens 1, 2 e partes 1 e 2 da mensagem 3, o tamanho da mensagem AEAD é conhecido antecipadamente. Em caso de falha de autenticação AEAD, o destinatário deve interromper o processamento adicional de mensagens e fechar a conexão sem responder. Isso deve ser um fechamento anormal (TCP RST).
- Para resistência a sondagem, na mensagem 1, após uma falha AEAD, Bob deve definir um timeout aleatório (intervalo a ser determinado) e então ler um número aleatório de bytes (intervalo a ser determinado) antes de fechar o socket. Bob deve manter uma lista negra de IPs com falhas repetidas.
- Na fase de dados, o tamanho da mensagem AEAD é "criptografado" (ofuscado) com SipHash. Deve-se ter cuidado para evitar criar um oráculo de descriptografia. Em caso de falha de autenticação AEAD na fase de dados, o destinatário deve definir um timeout aleatório (intervalo a ser determinado) e então ler um número aleatório de bytes (intervalo a ser determinado). Após a leitura, ou em timeout de leitura, o destinatário deve enviar um payload com um bloco de terminação contendo um código de razão "falha AEAD" e fechar a conexão.
- Tome a mesma ação de erro para um valor de campo de comprimento inválido na fase de dados.

### Função de Derivação de Chave (KDF) (para mensagem de handshake 1)

O KDF gera uma chave de cifra da fase de handshake k a partir do resultado DH, usando HMAC-SHA256(key, data) conforme definido na [RFC-2104](https://tools.ietf.org/html/rfc2104). Estas são as funções InitializeSymmetric(), MixHash() e MixKey(), exatamente como definidas na especificação Noise.

```
This is the "e" message pattern:

// Define protocol_name.
Set protocol_name = "Noise_XKaesobfse+hs2+hs3_25519_ChaChaPoly_SHA256"
 (48 bytes, US-ASCII encoded, no NULL termination).

// Define Hash h = 32 bytes
h = SHA256(protocol_name);

Define ck = 32 byte chaining key. Copy the h data to ck.
Set ck = h

Define rs = Bob's 32-byte static key as published in the RouterInfo

// MixHash(null prologue)
h = SHA256(h);

// up until here, can all be precalculated by Alice for all outgoing connections

// Alice must validate that Bob's static key is a valid point on the curve here.

// Bob static key
// MixHash(rs)
// || below means append
h = SHA256(h || rs);

// up until here, can all be precalculated by Bob for all incoming connections

This is the "e" message pattern:

Alice generates her ephemeral DH key pair e.

// Alice ephemeral key X
// MixHash(e.pubkey)
// || below means append
h = SHA256(h || e.pubkey);

// h is used as the associated data for the AEAD in message 1
// Retain the Hash h for the message 2 KDF


End of "e" message pattern.

This is the "es" message pattern:

// DH(e, rs) == DH(s, re)
Define input_key_material = 32 byte DH result of Alice's ephemeral key and Bob's static key
Set input_key_material = X25519 DH result

// MixKey(DH())

Define temp_key = 32 bytes
Define HMAC-SHA256(key, data) as in [RFC-2104]_
// Generate a temp key from the chaining key and DH result
// ck is the chaining key, defined above
temp_key = HMAC-SHA256(ck, input_key_material)
// overwrite the DH result in memory, no longer needed
input_key_material = (all zeros)

// Output 1
// Set a new chaining key from the temp key
// byte() below means a single byte
ck =       HMAC-SHA256(temp_key, byte(0x01)).

// Output 2
// Generate the cipher key k
Define k = 32 bytes
// || below means append
// byte() below means a single byte
k =        HMAC-SHA256(temp_key, ck || byte(0x02)).
// overwrite the temp_key in memory, no longer needed
temp_key = (all zeros)

// retain the chaining key ck for message 2 KDF


End of "es" message pattern.
```
### 1) SessionRequest

Alice envia para Bob.

Conteúdo Noise: chave efêmera X da Alice Payload Noise: bloco de opção de 16 bytes Payload não-noise: Preenchimento aleatório

(Propriedades de Segurança da Carga Útil de [Noise](https://noiseprotocol.org/noise.html) )

```
XK(s, rs):           Authentication   Confidentiality
  -> e, es                  0                2

  Authentication: None (0).
  This payload may have been sent by any party, including an active attacker.

  Confidentiality: 2.
  Encryption to a known recipient, forward secrecy for sender compromise
  only, vulnerable to replay.  This payload is encrypted based only on DHs
  involving the recipient's static key pair.  If the recipient's static
  private key is compromised, even at a later date, this payload can be
  decrypted.  This message can also be replayed, since there's no ephemeral
  contribution from the recipient.

  "e": Alice generates a new ephemeral key pair and stores it in the e
       variable, writes the ephemeral public key as cleartext into the
       message buffer, and hashes the public key along with the old h to
       derive a new h.

  "es": A DH is performed between the Alice's ephemeral key pair and the
        Bob's static key pair.  The result is hashed along with the old ck to
        derive a new ck and k, and n is set to zero.
```
O valor X é criptografado para garantir indistinguibilidade e singularidade do payload, que são contramedidas DPI necessárias. Usamos criptografia AES para conseguir isso, em vez de alternativas mais complexas e lentas como elligator2. Criptografia assimétrica para a chave pública do router do Bob seria muito lenta. A criptografia AES usa o hash do router do Bob como chave e o IV do Bob conforme publicado no netDb.

A criptografia AES é apenas para resistência a DPI. Qualquer parte que conheça o hash do router do Bob e o IV, que são publicados na base de dados da rede, pode descriptografar o valor X nesta mensagem.

O preenchimento não é criptografado por Alice. Pode ser necessário que Bob descriptografe o preenchimento, para inibir ataques de temporização.

Conteúdo bruto:

```
+----+----+----+----+----+----+----+----+
|                                       |
+        obfuscated with RH_B           +
|       AES-CBC-256 encrypted X         |
+             (32 bytes)                +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|   ChaChaPoly encrypted data           |
+             (16 bytes)                +
|   k defined in KDF for message 1      |
+   n = 0                               +
|   see KDF for associated data         |
+----+----+----+----+----+----+----+----+
|                                       |
+        Poly1305 MAC (16 bytes)        +
|                                       |
+----+----+----+----+----+----+----+----+
|     unencrypted authenticated         |
~         padding (optional)            ~
|     length defined in options block   |
+----+----+----+----+----+----+----+----+

X :: 32 bytes, AES-256-CBC encrypted X25519 ephemeral key, little endian
        key: RH_B
        iv: As published in Bobs network database entry

padding :: Random data, 0 or more bytes.
           Total message length must be 65535 bytes or less.
           Total message length must be 287 bytes or less if
           Bob is publishing his address as NTCP
           (see Version Detection section below).
           Alice and Bob will use the padding data in the KDF for message 2.
           It is authenticated so that any tampering will cause the
           next message to fail.
```
Dados não criptografados (tag de autenticação Poly1305 não mostrada):

```
+----+----+----+----+----+----+----+----+
|                                       |
+                                       +
|                   X                   |
+              (32 bytes)               +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|               options                 |
+              (16 bytes)               +
|                                       |
+----+----+----+----+----+----+----+----+
|     unencrypted authenticated         |
+         padding (optional)            +
|     length defined in options block   |
~               .   .   .               ~
|                                       |
+----+----+----+----+----+----+----+----+

X :: 32 bytes, X25519 ephemeral key, little endian

options :: options block, 16 bytes, see below

padding :: Random data, 0 or more bytes.
           Total message length must be 65535 bytes or less.
           Total message length must be 287 bytes or less if
           Bob is publishing his address as "NTCP"
           (see Version Detection section below)
           Alice and Bob will use the padding data in the KDF for message 2.
           It is authenticated so that any tampering will cause the
           next message to fail.
```
Bloco de opções: Nota: Todos os campos estão em big-endian.

```
+----+----+----+----+----+----+----+----+
| id | ver|  padLen | m3p2len | Rsvd(0) |
+----+----+----+----+----+----+----+----+
|        tsA        |   Reserved (0)    |
+----+----+----+----+----+----+----+----+

id :: 1 byte, the network ID (currently 2, except for test networks)
      As of 0.9.42. See proposal 147.

ver :: 1 byte, protocol version (currently 2)

padLen :: 2 bytes, length of the padding, 0 or more
          See below for max guidelines. Random size from 0 to 64 bytes minimum is recommended.
          (Distribution is implementation-dependent)

m3p2Len :: 2 bytes, length of the the second AEAD frame in SessionConfirmed
           (message 3 part 2) See notes below

Rsvd :: 2 bytes, set to 0 for compatibility with future options

tsA :: 4 bytes, Unix timestamp, unsigned seconds.
       Wraps around in 2106

Reserved :: 4 bytes, set to 0 for compatibility with future options
```
#### Notas

- Quando o endereço publicado é "NTCP", Bob suporta tanto NTCP quanto NTCP2 na mesma porta. Para compatibilidade, ao iniciar uma conexão para um endereço publicado como "NTCP", Alice deve limitar o tamanho máximo desta mensagem, incluindo padding, a 287 bytes ou menos. Isso facilita a identificação automática de protocolo por Bob. Quando publicado como "NTCP2", não há restrição de tamanho. Veja as seções Endereços Publicados e Detecção de Versão abaixo.

- O valor único X no bloco AES inicial garante que o texto cifrado seja diferente para cada sessão.

- Bob deve rejeitar conexões onde o valor do timestamp está muito distante do horário atual. Chame o delta máximo de tempo de "D". Bob deve manter um cache local de valores de handshake usados anteriormente e rejeitar duplicatas, para prevenir ataques de replay. Os valores no cache devem ter uma vida útil de pelo menos 2*D. Os valores do cache são dependentes da implementação, no entanto o valor X de 32 bytes (ou seu equivalente criptografado) pode ser usado.

- As chaves efêmeras Diffie-Hellman nunca podem ser reutilizadas, para prevenir ataques criptográficos, e a reutilização será rejeitada como um ataque de replay.

- As opções "KE" e "auth" devem ser compatíveis, ou seja, o segredo compartilhado K deve ter o tamanho apropriado. Se mais opções "auth" forem adicionadas, isso poderia implicitamente alterar o significado da flag "KE" para usar um KDF diferente ou um tamanho de truncamento diferente.

- Bob deve validar que a chave efêmera de Alice é um ponto válido na curva aqui.

- O padding deve ser limitado a uma quantidade razoável. Bob pode rejeitar conexões com padding excessivo. Bob especificará suas opções de padding na mensagem 2. Diretrizes de mín/máx a serem definidas. Tamanho aleatório de 0 a 31 bytes no mínimo? (A distribuição depende da implementação) As implementações Java atualmente limitam o padding a 256 bytes no máximo.

- Em qualquer erro, incluindo AEAD, DH, timestamp, replay aparente, ou falha na validação de chave, Bob deve interromper o processamento adicional de mensagens e fechar a conexão sem responder. Este deve ser um fechamento anormal (TCP RST). Para resistência a sondagem, após uma falha AEAD, Bob deve definir um timeout aleatório (intervalo a ser determinado) e então ler um número aleatório de bytes (intervalo a ser determinado), antes de fechar o socket.

- Bob pode fazer uma verificação rápida do MSB para uma chave válida (X[31] & 0x80 == 0) antes de tentar a descriptografia. Se o bit alto estiver definido, implemente resistência a sondagem como para falhas AEAD.

- Mitigação de DoS: DH é uma operação relativamente cara. Como com o protocolo NTCP anterior, os routers devem tomar todas as medidas necessárias para prevenir esgotamento de CPU ou conexão. Estabeleça limites no máximo de conexões ativas e máximo de configurações de conexão em progresso. Aplique timeouts de leitura (tanto por leitura quanto total para "slowloris"). Limite conexões repetidas ou simultâneas da mesma fonte. Mantenha listas negras para fontes que falham repetidamente. Não responda a falha AEAD.

- Para facilitar a detecção rápida de versão e handshaking, as implementações devem garantir que Alice armazene em buffer e então descarregue todo o conteúdo da primeira mensagem de uma vez, incluindo o padding. Isso aumenta a probabilidade de que os dados sejam contidos em um único pacote TCP (a menos que sejam segmentados pelo SO ou middleboxes), e recebidos de uma só vez por Bob. Além disso, as implementações devem garantir que Bob armazene em buffer e então descarregue todo o conteúdo da segunda mensagem de uma vez, incluindo o padding, e que Bob armazene em buffer e então descarregue todo o conteúdo da terceira mensagem de uma vez. Isso também é para eficiência e para garantir a efetividade do padding aleatório.

- campo "ver": O protocolo Noise geral, extensões e protocolo NTCP incluindo especificações de payload, indicando NTCP2. Este campo pode ser usado para indicar suporte para mudanças futuras.

- Comprimento da parte 2 da mensagem 3: Este é o tamanho do segundo frame AEAD (incluindo MAC de 16 bytes) contendo o Router Info de Alice e preenchimento opcional que será enviado na mensagem SessionConfirmed. Como os routers regeneram periodicamente e republicam seu Router Info, o tamanho do Router Info atual pode mudar antes da mensagem 3 ser enviada. As implementações devem escolher uma das duas estratégias:

a\) salvar as informações atuais do Router para serem enviadas na mensagem 3, para que o tamanho seja conhecido, e opcionalmente adicionar espaço para padding;

b\) aumentar o tamanho especificado o suficiente para permitir um possível aumento no tamanho do Router Info, e sempre adicionar preenchimento quando a mensagem 3 for efetivamente enviada. Em qualquer caso, o comprimento "m3p2len" incluído na mensagem 1 deve ser exatamente o tamanho desse frame quando enviado na mensagem 3.

- Bob deve falhar a conexão se algum dado de entrada permanecer após validar a mensagem 1 e ler o padding. Não deve haver dados extras de Alice, já que Bob ainda não respondeu com a mensagem 2.

- O campo ID da rede é usado para identificar rapidamente conexões entre redes diferentes. Se este campo for diferente de zero e não corresponder ao ID da rede do Bob, o Bob deve desconectar e bloquear conexões futuras. Quaisquer conexões de redes de teste devem ter um ID diferente e falharão no teste. A partir da versão 0.9.42. Consulte a proposta 147 para mais informações.

- Até a API 0.9.68 (versão 2.11.0), o Java I2P implementava um máximo de 256 bytes de padding para conexões não-PQ, porém isso não havia sido documentado anteriormente.
  A partir da API 0.9.69 (versão 2.12.0), o Java I2P implementa o mesmo padding máximo para conexões não-PQ que para MLKEM-512. O padding máximo é de 880 bytes.

### Função de Derivação de Chave (KDF) (para mensagem 2 do handshake e parte 1 da mensagem 3)

```
// take h saved from message 1 KDF
// MixHash(ciphertext)
h = SHA256(h || 32 byte encrypted payload from message 1)

// MixHash(padding)
// Only if padding length is nonzero
h = SHA256(h || random padding from message 1)

This is the "e" message pattern:

Bob generates his ephemeral DH key pair e.

// h is from KDF for handshake message 1
// Bob ephemeral key Y
// MixHash(e.pubkey)
// || below means append
h = SHA256(h || e.pubkey);

// h is used as the associated data for the AEAD in message 2
// Retain the Hash h for the message 3 KDF

End of "e" message pattern.

This is the "ee" message pattern:

// DH(e, re)
Define input_key_material = 32 byte DH result of Alice's ephemeral key and Bob's ephemeral key
Set input_key_material = X25519 DH result
// overwrite Alice's ephemeral key in memory, no longer needed
// Alice:
e(public and private) = (all zeros)
// Bob:
re = (all zeros)

// MixKey(DH())

Define temp_key = 32 bytes
Define HMAC-SHA256(key, data) as in [RFC-2104]_
// Generate a temp key from the chaining key and DH result
// ck is the chaining key, from the KDF for handshake message 1
temp_key = HMAC-SHA256(ck, input_key_material)
// overwrite the DH result in memory, no longer needed
input_key_material = (all zeros)

// Output 1
// Set a new chaining key from the temp key
// byte() below means a single byte
ck =       HMAC-SHA256(temp_key, byte(0x01)).

// Output 2
// Generate the cipher key k
Define k = 32 bytes
// || below means append
// byte() below means a single byte
k =        HMAC-SHA256(temp_key, ck || byte(0x02)).
// overwrite the temp_key in memory, no longer needed
temp_key = (all zeros)

// retain the chaining key ck for message 3 KDF

End of "ee" message pattern.
```
### 2) SessionCreated

Bob envia para Alice.

Conteúdo Noise: chave efêmera Y do Bob Payload Noise: bloco de opção de 16 bytes Payload não-noise: preenchimento aleatório

(Propriedades de Segurança do Payload de [Noise](https://noiseprotocol.org/noise.html) )

```
XK(s, rs):           Authentication   Confidentiality
  <- e, ee                  2                1

  Authentication: 2.
  Sender authentication resistant to key-compromise impersonation (KCI).
  The sender authentication is based on an ephemeral-static DH ("es" or "se")
  between the sender's static key pair and the recipient's ephemeral key pair.
  Assuming the corresponding private keys are secure, this authentication cannot be forged.

  Confidentiality: 1.
  Encryption to an ephemeral recipient.
  This payload has forward secrecy, since encryption involves an ephemeral-ephemeral DH ("ee").
  However, the sender has not authenticated the recipient,
  so this payload might be sent to any party, including an active attacker.


  "e": Bob generates a new ephemeral key pair and stores it in the e variable,
  writes the ephemeral public key as cleartext into the message buffer,
  and hashes the public key along with the old h to derive a new h.

  "ee": A DH is performed between the Bob's ephemeral key pair and the Alice's ephemeral key pair.
  The result is hashed along with the old ck to derive a new ck and k, and n is set to zero.
```
O valor Y é criptografado para garantir indistinguibilidade e unicidade da carga útil, que são contramedidas DPI necessárias. Usamos criptografia AES para alcançar isso, em vez de alternativas mais complexas e lentas como elligator2. Criptografia assimétrica para a chave pública do router de Alice seria muito lenta. A criptografia AES usa o hash do router de Bob como chave e o estado AES da mensagem 1 (que foi inicializado com o IV de Bob conforme publicado no network database).

A criptografia AES é apenas para resistência à DPI. Qualquer parte que conheça o hash do router de Bob e o IV, que são publicados na base de dados da rede, e capturou os primeiros 32 bytes da mensagem 1, pode descriptografar o valor Y nesta mensagem.

Conteúdo bruto:

```
+----+----+----+----+----+----+----+----+
|                                       |
+        obfuscated with RH_B           +
|       AES-CBC-256 encrypted Y         |
+              (32 bytes)               +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|   ChaChaPoly encrypted data (options) |
+   16 bytes                            +
|   k defined in KDF for message 2      |
+   n = 0; see KDF for associated data  +
|                                       |
+----+----+----+----+----+----+----+----+
|                                       |
+        Poly1305 MAC (16 bytes)        +
|                                       |
+----+----+----+----+----+----+----+----+
|     unencrypted authenticated         |
+         padding (optional)            +
|     length defined in options block   |
~               .   .   .               ~
|                                       |
+----+----+----+----+----+----+----+----+

Y :: 32 bytes, AES-256-CBC encrypted X25519 ephemeral key, little endian
        key: RH_B
        iv: Using AES state from message 1
```
Dados não criptografados (tag de autenticação Poly1305 não mostrada):

```
+----+----+----+----+----+----+----+----+
|                                       |
+                                       +
|                  Y                    |
+              (32 bytes)               +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|               options                 |
+              (16 bytes)               +
|                                       |
+----+----+----+----+----+----+----+----+
|     unencrypted authenticated         |
+         padding (optional)            +
|     length defined in options block   |
~               .   .   .               ~
|                                       |
+----+----+----+----+----+----+----+----+

Y :: 32 bytes, X25519 ephemeral key, little endian

options :: options block, 16 bytes, see below

padding :: Random data, 0 or more bytes.
           Total message length must be 65535 bytes or less.
           Alice and Bob will use the padding data in the KDF for message 3 part 1.
           It is authenticated so that any tampering will cause the
           next message to fail.
```
#### Notas

- Alice deve validar que a chave efêmera de Bob é um ponto válido na curva aqui.
- O padding deve ser limitado a uma quantidade razoável. Alice pode rejeitar conexões com padding excessivo. Alice especificará suas opções de padding na mensagem 3. Diretrizes mín/máx a serem definidas. Tamanho aleatório de 0 a 31 bytes no mínimo? (A distribuição depende da implementação)
- Em qualquer erro, incluindo AEAD, DH, timestamp, aparente replay, ou falha na validação de chave, Alice deve interromper o processamento adicional de mensagens e fechar a conexão sem responder. Isso deve ser um fechamento anormal (TCP RST).
- Para facilitar o handshake rápido, as implementações devem garantir que Bob armazene em buffer e então descarregue todo o conteúdo da primeira mensagem de uma vez, incluindo o padding. Isso aumenta a probabilidade de que os dados sejam contidos em um único pacote TCP (a menos que sejam segmentados pelo SO ou middleboxes), e recebidos todos de uma vez por Alice. Isso também é para eficiência e para garantir a eficácia do padding aleatório.
- Alice deve falhar a conexão se algum dado de entrada permanecer após validar a mensagem 2 e ler o padding. Não deve haver dados extras de Bob, pois Alice ainda não respondeu com a mensagem 3.

Bloco de opções: Nota: Todos os campos são big-endian.

```
+----+----+----+----+----+----+----+----+
| Rsvd(0) | padLen  |   Reserved (0)    |
+----+----+----+----+----+----+----+----+
|        tsB        |   Reserved (0)    |
+----+----+----+----+----+----+----+----+

Reserved :: 10 bytes total, set to 0 for compatibility with future options

padLen :: 2 bytes, big endian, length of the padding, 0 or more
          See below for max guidelines. Random size from 0 to 64 bytes minimum is recommended.
          (Distribution is implementation-dependent)

tsB :: 4 bytes, big endian, Unix timestamp, unsigned seconds.
       Wraps around in 2106
```
#### Notas

- Alice deve rejeitar conexões onde o valor do timestamp está muito distante do tempo atual. Chame o delta de tempo máximo de "D". Alice deve manter um cache local de valores de handshake previamente utilizados e rejeitar duplicatas, para prevenir ataques de replay. Valores no cache devem ter um tempo de vida de pelo menos 2*D. Os valores do cache dependem da implementação, porém o valor Y de 32 bytes (ou seu equivalente criptografado) pode ser usado.

- Através da API 0.9.68 (release 2.11.0), o Java I2P implementava um máximo de 256 bytes de padding para conexões não-PQ, porém isto
  não estava documentado anteriormente.
  A partir da API 0.9.69 (release 2.12.0), o Java I2P implementa o mesmo padding máximo para conexões não-PQ
  como para MLKEM-512. O padding máximo é de 848 bytes.

#### Problemas

- Incluir opções de padding mínimo/máximo aqui?

### Criptografia para a parte 1 da mensagem 3 do handshake, usando o KDF da mensagem 2)

```
// take h saved from message 2 KDF
// MixHash(ciphertext)
h = SHA256(h || 24 byte encrypted payload from message 2)

// MixHash(padding)
// Only if padding length is nonzero
h = SHA256(h || random padding from message 2)
// h is used as the associated data for the AEAD in message 3 part 1, below

This is the "s" message pattern:

Define s = Alice's static public key, 32 bytes

// EncryptAndHash(s.publickey)
// EncryptWithAd(h, s.publickey)
// AEAD_ChaCha20_Poly1305(key, nonce, associatedData, data)
// k is from handshake message 1
// n is 1
ciphertext = AEAD_ChaCha20_Poly1305(k, n++, h, s.publickey)
// MixHash(ciphertext)
// || below means append
h = SHA256(h || ciphertext);

// h is used as the associated data for the AEAD in message 3 part 2

End of "s" message pattern.
```
### Função de Derivação de Chave (KDF) (para a mensagem de handshake 3 parte 2)

```
This is the "se" message pattern:

// DH(s, re) == DH(e, rs)
Define input_key_material = 32 byte DH result of Alice's static key and Bob's ephemeral key
Set input_key_material = X25519 DH result
// overwrite Bob's ephemeral key in memory, no longer needed
// Alice:
re = (all zeros)
// Bob:
e(public and private) = (all zeros)

// MixKey(DH())

Define temp_key = 32 bytes
Define HMAC-SHA256(key, data) as in [RFC-2104]_
// Generate a temp key from the chaining key and DH result
// ck is the chaining key, from the KDF for handshake message 1
temp_key = HMAC-SHA256(ck, input_key_material)
// overwrite the DH result in memory, no longer needed
input_key_material = (all zeros)

// Output 1
// Set a new chaining key from the temp key
// byte() below means a single byte
ck =       HMAC-SHA256(temp_key, byte(0x01)).

// Output 2
// Generate the cipher key k
Define k = 32 bytes
// || below means append
// byte() below means a single byte
k =        HMAC-SHA256(temp_key, ck || byte(0x02)).

// h from message 3 part 1 is used as the associated data for the AEAD in message 3 part 2

// EncryptAndHash(payload)
// EncryptWithAd(h, payload)
// AEAD_ChaCha20_Poly1305(key, nonce, associatedData, data)
// n is 0
ciphertext = AEAD_ChaCha20_Poly1305(k, n++, h, payload)
// MixHash(ciphertext)
// || below means append
h = SHA256(h || ciphertext);

// retain the chaining key ck for the data phase KDF
// retain the hash h for the data phase Additional Symmetric Key (SipHash) KDF

End of "se" message pattern.

// overwrite the temp_key in memory, no longer needed
temp_key = (all zeros)
```
### 3) SessionConfirmed

Alice envia para Bob.

Conteúdo Noise: chave estática da Alice Payload Noise: RouterInfo da Alice e padding aleatório Payload não-noise: nenhum

(Propriedades de Segurança de Payload do [Noise](https://noiseprotocol.org/noise.html) )

```
XK(s, rs):           Authentication   Confidentiality
  -> s, se                  2                5

  Authentication: 2.
  Sender authentication resistant to key-compromise impersonation (KCI).  The
  sender authentication is based on an ephemeral-static DH ("es" or "se")
  between the sender's static key pair and the recipient's ephemeral key
  pair.  Assuming the corresponding private keys are secure, this
  authentication cannot be forged.

  Confidentiality: 5.
  Encryption to a known recipient, strong forward secrecy.  This payload is
  encrypted based on an ephemeral-ephemeral DH as well as an ephemeral-static
  DH with the recipient's static key pair.  Assuming the ephemeral private
  keys are secure, and the recipient is not being actively impersonated by an
  attacker that has stolen its static private key, this payload cannot be
  decrypted.

  "s": Alice writes her static public key from the s variable into the
  message buffer, encrypting it, and hashes the output along with the old h
  to derive a new h.

  "se": A DH is performed between the Alice's static key pair and the Bob's
  ephemeral key pair.  The result is hashed along with the old ck to derive a
  new ck and k, and n is set to zero.
```
Isto contém dois frames ChaChaPoly. O primeiro é a chave pública estática criptografada de Alice. O segundo é o payload Noise: o RouterInfo criptografado de Alice, opções opcionais e padding opcional. Eles usam chaves diferentes, porque a função MixKey() é chamada entre eles.

Conteúdo bruto:

```
+----+----+----+----+----+----+----+----+
|                                       |
+   ChaCha20 encrypted data (32 bytes)  +
|   Alice static key S                  |
+     k defined in KDF for message 2    +
|   n = 1 see KDF for associated data   |
+----+----+----+----+----+----+----+----+
|                                       |
+        Poly1305 MAC (16 bytes)        +
|                                       |
+----+----+----+----+----+----+----+----+
|                                       |
+   ChaCha20 encrypted data             +
|     Length specified in message 1     |
+     (including 16 byte MAC to follow) +
|                                       |
+       Alice RouterInfo                +
|       using block format 2            |
+       Alice Options (optional)        +
|       using block format 1            |
+       Arbitrary padding               +
|       using block format 254          |
+                                       +
| k defined in KDF for message 3 part 2 |
+     n = 0                             +
|     see KDF for associated data       |
~               .   .   .               ~
|                                       |
+----+----+----+----+----+----+----+----+
|                                       |
+        Poly1305 MAC (16 bytes)        +
|                                       |
+----+----+----+----+----+----+----+----+

S :: 32 bytes, ChaChaPoly encrypted Alice's X25519 static key, little endian
     inside 48 byte ChaChaPoly frame
```
Dados não criptografados (tags de autenticação Poly1305 não mostradas):

```
+----+----+----+----+----+----+----+----+
|                                       |
+                                       +
|              S                        |
+       Alice static key                +
|          (32 bytes)                   |
+                                       +
|                                       |
+                                       +
+----+----+----+----+----+----+----+----+
|                                       |
+                                       +
|                                       |
+                                       +
|       Alice RouterInfo block          |
~               .   .   .               ~
|                                       |
+----+----+----+----+----+----+----+----+
|                                       |
+       Optional Options block          +
|                                       |
~               .   .   .               ~
|                                       |
+----+----+----+----+----+----+----+----+
|                                       |
+       Optional Padding block          +
|                                       |
~               .   .   .               ~
|                                       |
+----+----+----+----+----+----+----+----+

S :: 32 bytes, Alice's X25519 static key, little endian
```
#### Notas

- Bob deve realizar a validação usual do Router Info. Garantir que o tipo de assinatura é suportado, verificar a assinatura, verificar se o timestamp está dentro dos limites, e quaisquer outras verificações necessárias.

- Bob deve verificar se a chave estática de Alice recebida no primeiro quadro corresponde à chave estática no Router Info. Bob deve primeiro buscar no Router Info por um Router Address NTCP ou NTCP2 com uma opção de versão (v) correspondente. Veja as seções Published Router Info e Unpublished Router Info abaixo.

- Se Bob tem uma versão mais antiga do RouterInfo de Alice em seu netdb, verificar se a chave estática nas informações do router é a mesma em ambas, se presente, e se a versão mais antiga tem menos de XXX (veja o tempo de rotação de chave abaixo)

- Bob deve validar que a chave estática de Alice é um ponto válido na curva aqui.

- As opções devem ser incluídas, para especificar parâmetros de preenchimento.

- Em qualquer erro, incluindo falha de validação AEAD, RI, DH, timestamp ou chave, Bob deve interromper o processamento adicional de mensagens e fechar a conexão sem responder. Isso deve ser um fechamento anormal (TCP RST).

- Para facilitar o handshaking rápido, as implementações devem garantir que Alice armazene em buffer e então descarregue todo o conteúdo da terceira mensagem de uma só vez, incluindo ambos os frames AEAD. Isso aumenta a probabilidade de que os dados sejam contidos em um único pacote TCP (a menos que sejam segmentados pelo SO ou middleboxes), e recebidos de uma só vez pelo Bob. Isso também é para eficiência e para garantir a eficácia do padding aleatório.

- Comprimento do quadro da parte 2 da mensagem 3: O comprimento deste quadro (incluindo MAC) é enviado por Alice na mensagem 1. Consulte essa mensagem para observações importantes sobre permitir espaço suficiente para preenchimento.

- Conteúdo do quadro da parte 2 da mensagem 3: O formato deste quadro é o mesmo que o formato dos quadros da fase de dados, exceto que o comprimento do quadro é enviado por Alice na mensagem 1. Veja abaixo o formato do quadro da fase de dados. O quadro deve conter de 1 a 3 blocos na seguinte ordem:

1)  Bloco de Informações do Router da Alice (obrigatório)   2)  Bloco de Opções (opcional)

3\) Bloco de preenchimento (opcional) Este frame nunca deve conter qualquer outro tipo de bloco.

- O preenchimento da parte 2 da mensagem 3 não é necessário se Alice anexar um quadro de fase de dados (opcionalmente contendo preenchimento) ao final da mensagem 3 e enviar ambos de uma vez, pois aparecerá como um grande fluxo de bytes para um observador. Como Alice geralmente, mas nem sempre, terá uma mensagem I2NP para enviar para Bob (é por isso que ela se conectou a ele), esta é a implementação recomendada, por eficiência e para garantir a eficácia do preenchimento aleatório.

- O comprimento máximo teórico total de ambos os quadros AEAD da Mensagem 3 (partes 1 e 2) é de 65535 bytes; a parte 1 tem 48 bytes, portanto o comprimento máximo do quadro da parte 2 é de 65487; o comprimento máximo de texto claro da parte 2, excluindo o MAC, é de 65471.
  AVISO: Algumas implementações impõem comprimentos muito menores. O Java I2P atualmente limita o comprimento total a 4096 bytes. Não adicione preenchimento excessivo.

### Função de Derivação de Chave (KDF) (para fase de dados)

A fase de dados usa uma entrada de dados associados de comprimento zero.

O KDF gera duas chaves de cifra k_ab e k_ba a partir da chaining key ck, usando HMAC-SHA256(key, data) conforme definido em [RFC-2104](https://tools.ietf.org/html/rfc2104). Esta é a função Split(), exatamente como definida na especificação Noise.

```
ck = from handshake phase

// k_ab, k_ba = HKDF(ck, zerolen)
// ask_master = HKDF(ck, zerolen, info="ask")

// zerolen is a zero-length byte array
temp_key = HMAC-SHA256(ck, zerolen)
// overwrite the chaining key in memory, no longer needed
ck = (all zeros)

// Output 1
// cipher key, for Alice transmits to Bob (Noise doesn't make clear which is which, but Java code does)
k_ab =   HMAC-SHA256(temp_key, byte(0x01)).

// Output 2
// cipher key, for Bob transmits to Alice (Noise doesn't make clear which is which, but Java code does)
k_ba =   HMAC-SHA256(temp_key, k_ab || byte(0x02)).


KDF for SipHash for length field:
Generate an Additional Symmetric Key (ask) for SipHash
SipHash uses two 8-byte keys (big endian) and 8 byte IV for first data.

// "ask" is 3 bytes, US-ASCII, no null termination
ask_master = HMAC-SHA256(temp_key, "ask" || byte(0x01))
// sip_master = HKDF(ask_master, h || "siphash")
// "siphash" is 7 bytes, US-ASCII, no null termination
// overwrite previous temp_key in memory
// h is from KDF for message 3 part 2
temp_key = HMAC-SHA256(ask_master, h || "siphash")
// overwrite ask_master in memory, no longer needed
ask_master = (all zeros)
sip_master = HMAC-SHA256(temp_key, byte(0x01))

Alice to Bob SipHash k1, k2, IV:
// sipkeys_ab, sipkeys_ba = HKDF(sip_master, zerolen)
// overwrite previous temp_key in memory
temp_key = HMAC-SHA256(sip_master, zerolen)
// overwrite sip_master in memory, no longer needed
sip_master = (all zeros)

sipkeys_ab = HMAC-SHA256(temp_key, byte(0x01)).
sipk1_ab = sipkeys_ab[0:7], little endian
sipk2_ab = sipkeys_ab[8:15], little endian
sipiv_ab = sipkeys_ab[16:23]

Bob to Alice SipHash k1, k2, IV:

sipkeys_ba = HMAC-SHA256(temp_key, sipkeys_ab || byte(0x02)).
sipk1_ba = sipkeys_ba[0:7], little endian
sipk2_ba = sipkeys_ba[8:15], little endian
sipiv_ba = sipkeys_ba[16:23]

// overwrite the temp_key in memory, no longer needed
temp_key = (all zeros)
```
### 4) Fase de Dados

Payload de ruído: Como definido abaixo, incluindo preenchimento aleatório Payload sem ruído: nenhum

Começando com a 2ª parte da mensagem 3, todas as mensagens estão dentro de um "frame" ChaChaPoly autenticado e criptografado com um comprimento ofuscado de dois bytes anexado. Todo o preenchimento está dentro do frame. Dentro do frame há um formato padrão com zero ou mais "blocos". Cada bloco tem um tipo de um byte e um comprimento de dois bytes. Os tipos incluem data/hora, mensagem I2NP, opções, terminação e preenchimento.

Nota: Bob pode, mas não é obrigatório, enviar seu RouterInfo para Alice como sua primeira mensagem para Alice na fase de dados.

(Propriedades de Segurança de Payload do [Noise](https://noiseprotocol.org/noise.html) )

```
XK(s, rs):           Authentication   Confidentiality
  <-                        2                5
  ->                        2                5

  Authentication: 2.
  Sender authentication resistant to key-compromise impersonation (KCI).
  The sender authentication is based on an ephemeral-static DH ("es" or "se")
  between the sender's static key pair and the recipient's ephemeral key pair.
  Assuming the corresponding private keys are secure, this authentication cannot be forged.

  Confidentiality: 5.
  Encryption to a known recipient, strong forward secrecy.
  This payload is encrypted based on an ephemeral-ephemeral DH as well as
  an ephemeral-static DH with the recipient's static key pair.
  Assuming the ephemeral private keys are secure, and the recipient is not being actively impersonated
  by an attacker that has stolen its static private key, this payload cannot be decrypted.
```
#### Notas

- Para eficiência e para minimizar a identificação do campo de comprimento, as implementações devem garantir que o remetente faça buffer e então envie todo o conteúdo das mensagens de dados de uma vez, incluindo o campo de comprimento e o quadro AEAD. Isso aumenta a probabilidade de que os dados sejam contidos em um único pacote TCP (a menos que sejam segmentados pelo SO ou middleboxes), e recebidos de uma vez pela outra parte. Isso também é para eficiência e para garantir a eficácia do preenchimento aleatório.
- O router pode escolher terminar a sessão em caso de erro AEAD, ou pode continuar a tentar comunicações. Se continuar, o router deve terminar após erros repetidos.

#### Comprimento ofuscado SipHash

Referência: [SipHash](https://www.131002.net/siphash/)

Uma vez que ambos os lados tenham completado o handshake, eles transferem payloads que são então criptografados e autenticados em "frames" ChaChaPoly.

Cada frame é precedido por um comprimento de dois bytes, big endian. Este comprimento especifica o número de bytes de frame criptografados que se seguem, incluindo o MAC. Para evitar transmitir campos de comprimento identificáveis no stream, o comprimento do frame é ofuscado através de XOR com uma máscara derivada do SipHash, conforme inicializado a partir do KDF da fase de dados. Note que as duas direções têm chaves SipHash e IVs únicos do KDF.

```
    sipk1, sipk2 = The SipHash keys from the KDF.  (two 8-byte long integers)
    IV[0] = sipiv = The SipHash IV from the KDF. (8 bytes)
    length is big endian.
    For each frame:
      IV[n] = SipHash-2-4(sipk1, sipk2, IV[n-1])
      Mask[n] = First 2 bytes of IV[n]
      obfuscatedLength = length ^ Mask[n]

    The first length output will be XORed with with IV[1].
```
O receptor possui as mesmas chaves SipHash e IV. A decodificação do comprimento é feita derivando a máscara usada para ofuscar o comprimento e aplicando XOR ao digest truncado para obter o comprimento do quadro. O comprimento do quadro é o comprimento total do quadro criptografado incluindo o MAC.

#### Notas

- Se você usar uma função de biblioteca SipHash que retorna um inteiro longo sem sinal, use os dois bytes menos significativos como a Máscara. Converta o inteiro longo para o próximo IV como little endian.

#### Conteúdo bruto

```
+----+----+----+----+----+----+----+----+
|obf size |                             |
+----+----+                             +
|                                       |
+   ChaChaPoly frame                    +
|   Encrypted and authenticated         |
+   key is k_ab for Alice to Bob        +
|   key is k_ba for Bob to Alice        |
+   as defined in KDF for data phase    +
|   n starts at 0 and increments        |
+   for each frame in that direction    +
|   no associated data                  |
+   16 bytes minimum                    +
|                                       |
~               .   .   .               ~
|                                       |
+----+----+----+----+----+----+----+----+

obf size :: 2 bytes length obfuscated with SipHash
            when de-obfuscated: 16 - 65535

Minimum size including length field is 18 bytes.
Maximum size including length field is 65537 bytes.
Obfuscated length is 2 bytes.
Maximum ChaChaPoly frame is 65535 bytes.
```
#### Notas

- Como o receptor deve obter o quadro inteiro para verificar o MAC, é recomendado que o remetente limite os quadros a alguns KB em vez de maximizar o tamanho do quadro. Isso minimizará a latência no receptor.

#### Dados não criptografados

Existem zero ou mais blocos no quadro criptografado. Cada bloco contém um identificador de um byte, um comprimento de dois bytes e zero ou mais bytes de dados.

Para extensibilidade, os receptores devem ignorar blocos com identificadores desconhecidos e tratá-los como preenchimento.

Os dados criptografados têm no máximo 65535 bytes, incluindo um cabeçalho de autenticação de 16 bytes, então o máximo de dados não criptografados é de 65519 bytes.

(Tag de autenticação Poly1305 não mostrada):

```
+----+----+----+----+----+----+----+----+
|blk |  size   |       data             |
+----+----+----+                        +
|                                       |
~               .   .   .               ~
|                                       |
+----+----+----+----+----+----+----+----+
|blk |  size   |       data             |
+----+----+----+                        +
|                                       |
~               .   .   .               ~
|                                       |
+----+----+----+----+----+----+----+----+
~               .   .   .               ~

blk :: 1 byte
       0 for datetime
       1 for options
       2 for RouterInfo
       3 for I2NP message
       4 for termination
       224-253 reserved for experimental features
       254 for padding
       255 reserved for future extension
size :: 2 bytes, big endian, size of data to follow, 0 - 65516
data :: the data

Maximum ChaChaPoly frame is 65535 bytes.
Poly1305 tag is 16 bytes
Maximum total block size is 65519 bytes
Maximum single block size is 65519 bytes
Block type is 1 byte
Block length is 2 bytes
Maximum single block data size is 65516 bytes.
```
#### Regras de Ordenação de Blocos

Na mensagem de handshake 3 parte 2, a ordem deve ser: RouterInfo, seguido por Options se presente, seguido por Padding se presente. Nenhum outro bloco é permitido.

Na fase de dados, a ordem não é especificada, exceto pelos seguintes requisitos: Padding, se presente, deve ser o último bloco. Termination, se presente, deve ser o último bloco exceto pelo Padding.

Pode haver múltiplos blocos I2NP em um único quadro. Múltiplos blocos de Padding não são permitidos em um único quadro. Outros tipos de blocos provavelmente não terão múltiplos blocos em um único quadro, mas isso não é proibido.

#### DataHora

Caso especial para sincronização de tempo:

```
+----+----+----+----+----+----+----+
| 0  |    4    |     timestamp     |
+----+----+----+----+----+----+----+

blk :: 0
size :: 2 bytes, big endian, value = 4
timestamp :: Unix timestamp, unsigned seconds.
             Wraps around in 2106
```
NOTA: As implementações devem arredondar para o segundo mais próximo para evitar desvio de relógio na rede.

#### Opções

Passe opções atualizadas. As opções incluem: Preenchimento mínimo e máximo.

O bloco de opções terá comprimento variável.

```
+----+----+----+----+----+----+----+----+
| 1  |  size   |tmin|tmax|rmin|rmax|tdmy|
+----+----+----+----+----+----+----+----+
|tdmy|  rdmy   |  tdelay |  rdelay |    |
~----+----+----+----+----+----+----+    ~
|              more_options             |
~               .   .   .               ~
|                                       |
+----+----+----+----+----+----+----+----+

blk :: 1
size :: 2 bytes, big endian, size of options to follow, 12 bytes minimum

tmin, tmax, rmin, rmax :: requested padding limits
    tmin and rmin are for desired resistance to traffic analysis.
    tmax and rmax are for bandwidth limits.
    tmin and tmax are the transmit limits for the router sending this options block.
    rmin and rmax are the receive limits for the router sending this options block.
    Each is a 4.4 fixed-point float representing 0 to 15.9375
    (or think of it as an unsigned 8-bit integer divided by 16.0).
    This is the ratio of padding to data. Examples:
    Value of 0x00 means no padding
    Value of 0x01 means add 6 percent padding
    Value of 0x10 means add 100 percent padding
    Value of 0x80 means add 800 percent (8x) padding
    Alice and Bob will negotiate the minimum and maximum in each direction.
    These are guidelines, there is no enforcement.
    Sender should honor receiver's maximum.
    Sender may or may not honor receiver's minimum, within bandwidth constraints.

tdmy: Max dummy traffic willing to send, 2 bytes big endian, bytes/sec average
rdmy: Requested dummy traffic, 2 bytes big endian, bytes/sec average
tdelay: Max intra-message delay willing to insert, 2 bytes big endian, msec average
rdelay: Requested intra-message delay, 2 bytes big endian, msec average

Padding distribution specified as additional parameters?
Random delay specified as additional parameters?

more_options :: Format TBD
```
#### Problemas de Opções

- O formato das opções está a ser definido.
- A negociação de opções está a ser definida.

#### RouterInfo

Passa o RouterInfo da Alice para o Bob. Usado na mensagem de handshake 3 parte 2. Passa o RouterInfo da Alice para o Bob, ou o do Bob para a Alice. Usado opcionalmente na fase de dados.

```
+----+----+----+----+----+----+----+----+
| 2  |  size   |flg |    RouterInfo     |
+----+----+----+----+                   +
| (Alice RI in handshake msg 3 part 2)  |
~ (Alice, Bob, or third-party           ~
|  RI in data phase)                    |
~               .   .   .               ~
|                                       |
+----+----+----+----+----+----+----+----+

blk :: 2
size :: 2 bytes, big endian, size of flag + router info to follow
flg :: 1 byte flags
       bit order: 76543210
       bit 0: 0 for local store, 1 for flood request
       bits 7-1: Unused, set to 0 for future compatibility
routerinfo :: Alice's or Bob's RouterInfo
```
#### Notas

- Quando usado na fase de dados, o receptor (Alice ou Bob) deve validar que é o mesmo Router Hash como originalmente enviado (para Alice) ou enviado para (para Bob). Então, trate-o como uma Mensagem I2NP DatabaseStore local. Valide a assinatura, valide timestamp mais recente, e armazene no netdb local. Se o bit de flag 0 for 1, e a parte receptora for floodfill, trate-o como uma Mensagem DatabaseStore com um token de resposta não-zero, e inunde para os floodfills mais próximos.
- O Router Info NÃO é comprimido com gzip (diferentemente de uma Mensagem DatabaseStore, onde é)
- Flooding não deve ser solicitado a menos que existam RouterAddresses publicados no RouterInfo. O router receptor não deve fazer flood do RouterInfo a menos que existam RouterAddresses publicados nele.
- Implementadores devem garantir que ao ler um bloco, dados malformados ou maliciosos não causem leituras que ultrapassem para o próximo bloco.
- Este protocolo não fornece uma confirmação de que o RouterInfo foi recebido, armazenado, ou inundado (seja na fase de handshake ou de dados). Se confirmação for desejada, e o receptor for floodfill, o remetente deve em vez disso enviar uma DatabaseStoreMessage I2NP padrão com um token de resposta.

#### Problemas

- Também poderia ser usado na fase de dados, em vez de uma I2NP DatabaseStoreMessage. Por exemplo, Bob poderia usá-lo para iniciar a fase de dados.
- É permitido que isso contenha o RI para routers diferentes do originador, como uma substituição geral para DatabaseStoreMessages, por exemplo, para flooding por floodfills?

#### Mensagem I2NP

Uma única mensagem I2NP com um cabeçalho modificado. As mensagens I2NP não podem ser fragmentadas entre blocos ou entre frames ChaChaPoly.

Isso usa os primeiros 9 bytes do cabeçalho I2NP NTCP padrão, e remove os últimos 7 bytes do cabeçalho, da seguinte forma: encurtar a expiração de 8 para 4 bytes (segundos em vez de milissegundos, igual ao SSU), remover o comprimento de 2 bytes (usar o tamanho do bloco - 9), e remover o checksum SHA256 de um byte.

```
+----+----+----+----+----+----+----+----+
| 3  |  size   |type|    msg id         |
+----+----+----+----+----+----+----+----+
|   short exp       |     message       |
+----+----+----+----+                   +
|                                       |
~               .   .   .               ~
|                                       |
+----+----+----+----+----+----+----+----+

blk :: 3
size :: 2 bytes, big endian, size of type + msg id + exp + message to follow
        I2NP message body size is (size - 9).
type :: 1 byte, I2NP msg type, see I2NP spec
msg id :: 4 bytes, big endian, I2NP message ID
short exp :: 4 bytes, big endian, I2NP message expiration, Unix timestamp, unsigned seconds.
             Wraps around in 2106
message :: I2NP message body
```
#### Notas

- Os implementadores devem garantir que ao ler um bloco, dados malformados ou maliciosos não causem leituras que excedam os limites para o próximo bloco.

#### Terminação

O Noise recomenda uma mensagem de terminação explícita. O NTCP original não tem uma. Encerre a conexão. Este deve ser o último bloco sem preenchimento no quadro.

```
+----+----+----+----+----+----+----+----+
| 4  |  size   |    valid data frames   |
+----+----+----+----+----+----+----+----+
    received   | rsn|     addl data     |
+----+----+----+----+                   +
~               .   .   .               ~
+----+----+----+----+----+----+----+----+

blk :: 4
size :: 2 bytes, big endian, value = 9 or more
valid data frames received :: The number of valid AEAD data phase frames received
                              (current receive nonce value)
                              0 if error occurs in handshake phase
                              8 bytes, big endian
rsn :: reason, 1 byte:
       0: normal close or unspecified
       1: termination received
       2: idle timeout
       3: router shutdown
       4: data phase AEAD failure
       5: incompatible options
       6: incompatible signature type
       7: clock skew
       8: padding violation
       9: AEAD framing error
       10: payload format error
       11: message 1 error
       12: message 2 error
       13: message 3 error
       14: intra-frame read timeout
       15: RI signature verification fail
       16: s parameter missing, invalid, or mismatched in RouterInfo
       17: banned
addl data :: optional, 0 or more bytes, for future expansion, debugging,
             or reason text.
             Format unspecified and may vary based on reason code.
```
#### Notas

Nem todos os motivos podem ser realmente utilizados, dependendo da implementação. Falhas de handshake geralmente resultarão em um fechamento com TCP RST. Veja as notas nas seções de mensagem de handshake acima. Motivos adicionais listados são para consistência, logging, depuração, ou se a política mudar.

#### Preenchimento

Isto é para preenchimento dentro de quadros AEAD. O preenchimento para mensagens 1 e 2 está fora dos quadros AEAD. Todo o preenchimento para a mensagem 3 e a fase de dados está dentro dos quadros AEAD.

O preenchimento dentro do AEAD deve aderir aproximadamente aos parâmetros negociados. Bob enviou seus parâmetros tx/rx mín/máx solicitados na mensagem 2. Alice enviou seus parâmetros tx/rx mín/máx solicitados na mensagem 3. Opções atualizadas podem ser enviadas durante a fase de dados. Veja as informações do bloco de opções acima.

Se presente, este deve ser o último bloco no quadro.

```
+----+----+----+----+----+----+----+----+
|254 |  size   |      padding           |
+----+----+----+                        +
|                                       |
~               .   .   .               ~
|                                       |
+----+----+----+----+----+----+----+----+

blk :: 254
size :: 2 bytes, big endian, size of padding to follow
padding :: random data
```
#### Notas

- Tamanho = 0 é permitido.
- Estratégias de padding TBD.
- Padding mínimo TBD.
- Frames apenas com padding são permitidos.
- Padrões de padding TBD.
- Veja o bloco de opções para negociação de parâmetros de padding
- Veja o bloco de opções para parâmetros de padding mín/máx
- O Noise limita mensagens a 64KB. Se mais padding for necessário, envie múltiplos frames.
- A resposta do router em caso de violação do padding negociado depende da implementação.

#### Outros tipos de blocos

As implementações devem ignorar tipos de bloco desconhecidos para compatibilidade futura, exceto na parte 2 da mensagem 3, onde blocos desconhecidos não são permitidos.

#### Trabalho futuro

- O comprimento do padding deve ser decidido caso a caso com base em estimativas da distribuição de comprimento, ou atrasos aleatórios devem ser adicionados. Essas contramedidas devem ser incluídas para resistir à DPI, já que os tamanhos das mensagens revelariam que o tráfego I2P está sendo transportado pelo protocolo de transporte. O esquema exato de padding é uma área de trabalho futuro.

### 5) Rescisão

As conexões podem ser encerradas via fechamento normal ou anormal do socket TCP, ou, como o Noise recomenda, uma mensagem de encerramento explícita. A mensagem de encerramento explícita é definida na fase de dados acima.

Após qualquer terminação normal ou anormal, os routers devem zerar todos os dados efêmeros em memória, incluindo chaves efêmeras de handshake, chaves de criptografia simétricas e informações relacionadas.

## Informações do Router Publicadas

### Capacidades

A partir da versão 0.9.50, a opção "caps" é suportada em endereços NTCP2, similar ao SSU. Uma ou mais capacidades podem ser publicadas na opção "caps". As capacidades podem estar em qualquer ordem, mas "46" é a ordem recomendada, para consistência entre implementações. Existem duas capacidades definidas:

4: Indica capacidade IPv4 de saída. Se um IP é publicado no campo host, esta capacidade não é necessária. Se o router está oculto, ou NTCP2 é apenas de saída, '4' e '6' podem ser combinados em um único endereço.

6: Indica capacidade IPv6 de saída. Se um IP for publicado no campo host, esta capacidade não é necessária. Se o router estiver oculto, ou se NTCP2 for apenas de saída, '4' e '6' podem ser combinados em um único endereço.

### Endereços Publicados

O RouterAddress publicado (parte do RouterInfo) terá um identificador de protocolo de "NTCP" ou "NTCP2".

O RouterAddress deve conter opções "host" e "port", como no protocolo NTCP atual.

O RouterAddress deve conter três opções para indicar suporte NTCP2:

- s=(Chave Base64) A chave pública estática Noise atual (s) para este RouterAddress. Codificada em Base 64 usando o alfabeto I2P Base 64 padrão. 32 bytes em binário, 44 bytes codificados em Base 64, chave pública X25519 little-endian.
- i=(IV Base64) O IV atual para criptografar o valor X na mensagem 1 para este RouterAddress. Codificado em Base 64 usando o alfabeto I2P Base 64 padrão. 16 bytes em binário, 24 bytes codificados em Base 64, big-endian.
- v=2 A versão atual (2). Quando publicado como "NTCP", suporte adicional para versão 1 está implícito. Suporte para versões futuras será com valores separados por vírgula, ex: v=2,3 A implementação deve verificar compatibilidade, incluindo múltiplas versões se uma vírgula estiver presente. Versões separadas por vírgula devem estar em ordem numérica.

Alice deve verificar que todas as três opções estão presentes e válidas antes de conectar usando o protocolo NTCP2.

Quando publicado como "NTCP" com as opções "s", "i" e "v", o router deve aceitar conexões de entrada nesse host e porta para os protocolos NTCP e NTCP2, e detectar automaticamente a versão do protocolo.

Quando publicado como "NTCP2" com as opções "s", "i" e "v", o router aceita conexões de entrada nesse host e porta apenas para o protocolo NTCP2.

Se um router suporta conexões NTCP1 e NTCP2 mas não implementa detecção automática de versão para conexões de entrada, ele deve anunciar endereços "NTCP" e "NTCP2", e incluir as opções NTCP2 apenas no endereço "NTCP2". O router deve definir um valor de custo mais baixo (prioridade mais alta) no endereço "NTCP2" do que no endereço "NTCP", para que NTCP2 seja preferido.

Se múltiplos NTCP2 RouterAddresses (seja como "NTCP" ou "NTCP2") forem publicados no mesmo RouterInfo (para endereços IP ou portas adicionais), todos os endereços especificando a mesma porta devem conter as opções e valores NTCP2 idênticos. Em particular, todos devem conter a mesma chave estática e iv.

### Endereço NTCP2 Não Publicado

Se Alice não publicar seu endereço NTCP2 (como "NTCP" ou "NTCP2") para conexões de entrada, ela deve publicar um endereço de router "NTCP2" contendo apenas sua chave estática e versão NTCP2, para que Bob possa validar a chave após receber o RouterInfo de Alice na parte 2 da mensagem 3.

- s=(chave Base64) Como definido acima para endereços publicados.
- v=2 Como definido acima para endereços publicados.

Este endereço de router não conterá as opções "i", "host" ou "port", pois estas não são necessárias para conexões NTCP2 de saída. O custo publicado para este endereço não importa estritamente, já que é apenas de entrada; no entanto, pode ser útil para outros routers se o custo for definido mais alto (prioridade mais baixa) do que outros endereços. O valor sugerido é 14.

Alice também pode simplesmente adicionar as opções "s" e "v" a um endereço "NTCP" publicado existente.

### Rotação de Chave Pública e IV

Devido ao cache de RouterInfos, os routers não devem rotacionar a chave pública estática ou IV enquanto o router estiver ativo, seja em um endereço publicado ou não. Os routers devem armazenar persistentemente esta chave e IV para reutilização após uma reinicialização imediata, para que as conexões de entrada continuem funcionando, e os tempos de reinicialização não sejam expostos. Os routers devem armazenar persistentemente, ou de outra forma determinar, o tempo do último desligamento, para que o tempo de inatividade anterior possa ser calculado na inicialização.

Sujeitos a preocupações sobre expor horários de reinicialização, os routers podem rotacionar esta chave ou IV na inicialização se o router estava previamente inativo por algum tempo (pelo menos algumas horas).

Se o router tem RouterAddresses NTCP2 publicados (como NTCP ou NTCP2), o tempo mínimo de inatividade antes da rotação deve ser muito maior, por exemplo um mês, a menos que o endereço IP local tenha mudado ou o router "rekeys".

Se o router tiver algum RouterAddresses SSU publicado, mas não NTCP2 (como NTCP ou NTCP2), o tempo mínimo de inatividade antes da rotação deve ser maior, por exemplo um dia, a menos que o endereço IP local tenha mudado ou o router "rekeys". Isso se aplica mesmo se o endereço SSU publicado tiver introducers.

Se o router não tiver RouterAddresses publicados (NTCP, NTCP2 ou SSU), o tempo mínimo de inatividade antes da rotação pode ser de apenas duas horas, mesmo se o endereço IP mudar, a menos que o router faça "rekeys".

Se o router "rekeys" para um Router Hash diferente, ele também deve gerar uma nova chave noise e IV.

As implementações devem estar cientes de que alterar a chave pública estática ou o IV impedirá conexões NTCP2 de entrada de routers que tenham em cache um RouterInfo mais antigo. A publicação do RouterInfo, seleção de pares de tunnel (incluindo tanto OBGW quanto o hop mais próximo IB), seleção de tunnel de zero-hop, seleção de transporte e outras estratégias de implementação devem levar isso em conta.

A rotação de IV está sujeita às mesmas regras da rotação de chaves, exceto que os IVs não estão presentes exceto em RouterAddresses publicados, então não há IV para routers ocultos ou protegidos por firewall. Se qualquer coisa mudar (versão, chave, opções?) é recomendado que o IV também mude.

Nota: O tempo mínimo de inatividade antes da recriação de chaves pode ser modificado para garantir a saúde da rede e para prevenir a ressemeadura por um router inativo por um período moderado de tempo.

## Detecção de Versão

Quando publicado como "NTCP", o router deve detectar automaticamente a versão do protocolo para conexões de entrada.

Esta detecção depende da implementação, mas aqui estão algumas orientações gerais.

Para detectar a versão de uma conexão NTCP recebida, Bob procede da seguinte forma:

- Aguarde pelo menos 64 bytes (tamanho mínimo da mensagem 1 NTCP2)

- Se os dados iniciais recebidos têm 288 ou mais bytes, a conexão de entrada é versão 1.

- Se menos de 288 bytes, então

> - Aguardar um curto período por mais dados (boa estratégia antes da adoção generalizada do NTCP2) se pelo menos 288 foram recebidos no total, é NTCP 1.   >   > - Tentar os primeiros estágios de decodificação como versão 2, se falhar, aguardar um curto período por mais dados (boa estratégia após a adoção generalizada do NTCP2)   >   >   > - Descriptografar os primeiros 32 bytes (a chave X) do pacote SessionRequest usando AES-256 com chave RH_B.   >   > - Verificar um ponto válido na curva. Se falhar, aguardar um curto período por mais dados para NTCP 1   >   > - Verificar o frame AEAD. Se falhar, aguardar um curto período por mais dados para NTCP 1

Note que mudanças ou estratégias adicionais podem ser recomendadas se detectarmos ataques ativos de segmentação TCP no NTCP 1.

Para facilitar a detecção rápida de versão e handshaking, as implementações devem garantir que Alice armazene em buffer e então despeje todo o conteúdo da primeira mensagem de uma vez, incluindo o padding. Isso aumenta a probabilidade de que os dados sejam contidos em um único pacote TCP (a menos que sejam segmentados pelo SO ou middleboxes), e recebidos de uma só vez por Bob. Isso também é para eficiência e para garantir a efetividade do padding aleatório. Isso se aplica tanto aos handshakes NTCP quanto NTCP2.

## Variantes, Fallbacks e Questões Gerais

- Se Alice e Bob suportam NTCP2, Alice deve conectar com NTCP2.
- Se Alice falhar ao conectar com Bob usando NTCP2 por qualquer motivo, a conexão falha. Alice não pode tentar novamente usando NTCP 1.

## Diretrizes de Desvio de Relógio

Os timestamps dos peers são incluídos nas duas primeiras mensagens de handshake, Session Request e Session Created. Uma diferença de relógio entre dois peers superior a +/- 60 segundos é geralmente fatal. Se Bob acha que seu relógio local está incorreto, ele pode ajustar seu relógio usando a diferença calculada, ou alguma fonte externa. Caso contrário, Bob deve responder com um Session Created mesmo se a diferença máxima for excedida, ao invés de simplesmente fechar a conexão. Isso permite que Alice obtenha o timestamp de Bob e calcule a diferença, tomando medidas se necessário. Bob não possui a identidade do router de Alice neste ponto, mas para conservar recursos, pode ser desejável que Bob bloqueie conexões de entrada do IP de Alice por algum período de tempo, ou após tentativas repetidas de conexão com diferença excessiva.

Alice deve ajustar o desvio de relógio calculado subtraindo metade do RTT. Se Alice achar que seu relógio local está com problemas, ela pode ajustar seu relógio usando o desvio calculado, ou alguma fonte externa. Se Alice achar que o relógio de Bob está com problemas, ela pode banir Bob por algum período de tempo. Em qualquer caso, Alice deve fechar a conexão.

Se Alice responder com Session Confirmed (provavelmente porque o desvio está muito próximo do limite de 60s, e os cálculos de Alice e Bob não são exatamente os mesmos devido ao RTT), Bob deve ajustar o desvio de relógio calculado subtraindo metade do RTT. Se o desvio de relógio ajustado exceder o máximo, Bob deve então responder com uma mensagem Disconnect contendo um código de motivo de desvio de relógio, e fechar a conexão. Neste ponto, Bob tem a identidade do router de Alice, e pode banir Alice por algum período de tempo.

## Referências

- [Estruturas Comuns](/docs/specs/common-structures)
- [I2NP](/docs/specs/i2np)
- [Base de Dados de Rede](/docs/overview/network-database)
- [NOISE - Framework de Protocolo Noise](https://noiseprotocol.org/noise.html)
- [NTCP](/docs/transport/ntcp)
- [Prop104](/proposals/104-tls-transport)
- [Prop109](/proposals/109-pt-transport)
- [Prop111](/proposals/111-ntcp-2)
- [RFC-2104 - HMAC](https://tools.ietf.org/html/rfc2104)
- [RFC-3526 - Grupos DH](https://tools.ietf.org/html/rfc3526)
- [RFC-6151](https://tools.ietf.org/html/rfc6151)
- [RFC-7539 - ChaCha20-Poly1305](https://tools.ietf.org/html/rfc7539)
- [RFC-7748 - X25519](https://tools.ietf.org/html/rfc7748)
- [RFC-7905](https://tools.ietf.org/html/rfc7905)
- [SipHash](https://www.131002.net/siphash/)
- [SSU](/docs/transport/ssu)
- **[STS]** Diffie, W.; van Oorschot P. C.; Wiener M. J., Autenticação e Trocas de Chaves Autenticadas
