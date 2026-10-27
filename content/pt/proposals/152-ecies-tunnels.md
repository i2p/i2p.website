---
title: "Túneis ECIES"
aliases:
  - "/pt/proposals/152-ecies-config"
  - "/pt/proposals/152-ecies-config/"
  - "/pt/proposals/152"
  - "/pt/proposals/152/"
number: "152"
author: "chisana, zzz, orignal"
created: "2019-07-04"
lastupdated: "2025-03-05"
status: "Fechado"
thread: "http://zzz.i2p/topics/2737"
target: "0.9.48"
implementedin: "0.9.48"
toc: true
---

## Nota

Implantação e testes da rede em andamento. Sujeito a revisões menores. Consulte [SPEC](/docs/specs/tunnel-implementation/) para a especificação oficial.

## Visão Geral

Este documento propõe mudanças na criptografia de mensagens Tunnel Build usando primitivas criptográficas introduzidas pelo [ECIES-X25519](/docs/specs/ecies/). É uma parte da proposta geral [Proposta 156](/proposals/156-ecies-routers) para converter routers de chaves ElGamal para ECIES-X25519.

Para fins de transição da rede de ElGamal + AES256 para ECIES + ChaCha20, tunnels com roteadores ElGamal e ECIES mistos são necessários. Especificações para o tratamento de saltos de tunnel mistos são fornecidas. Nenhuma alteração será feita no formato, processamento ou criptografia dos saltos ElGamal.

Os criadores de túneis ElGamal precisarão criar pares de chaves X25519 efêmeros por salto e seguir esta especificação para criar túneis contendo saltos ECIES.

Esta proposta especifica as mudanças necessárias para Tunnel Building ECIES-X25519. Para uma visão geral de todas as mudanças necessárias para routers ECIES, veja a proposta 156 [Proposal 156](/proposals/156-ecies-routers).

Esta proposta mantém o mesmo tamanho para os registros de construção de tunnel, conforme necessário para compatibilidade. Registros de construção e mensagens menores serão implementados posteriormente - consulte a [Proposta 157](/proposals/157-new-tbm).

### Cryptographic Primitives

Nenhuma primitiva criptográfica nova é introduzida. As primitivas necessárias para implementar esta proposta são:

- AES-256-CBC como em [Cryptography](/docs/specs/cryptography/)
- Funções STREAM ChaCha20/Poly1305:
  ENCRYPT(k, n, plaintext, ad) e DECRYPT(k, n, ciphertext, ad) - como em [NTCP2](/docs/specs/ntcp2/) [ECIES-X25519](/docs/specs/ecies/) e [RFC-7539](https://tools.ietf.org/html/rfc7539)
- Funções X25519 DH - como em [NTCP2](/docs/specs/ntcp2/) e [ECIES-X25519](/docs/specs/ecies/)
- HKDF(salt, ikm, info, n) - como em [NTCP2](/docs/specs/ntcp2/) e [ECIES-X25519](/docs/specs/ecies/)

Outras funções Noise definidas em outro lugar:

- MixHash(d) - como em [NTCP2](/docs/specs/ntcp2/) e [ECIES-X25519](/docs/specs/ecies/)
- MixKey(d) - como em [NTCP2](/docs/specs/ntcp2/) e [ECIES-X25519](/docs/specs/ecies/)

### Goals

- Aumentar a velocidade das operações criptográficas
- Substituir ElGamal + AES256/CBC por primitivas ECIES para BuildRequestRecords e BuildReplyRecords de túnel.
- Nenhuma alteração no tamanho dos BuildRequestRecords e BuildReplyRecords criptografados (528 bytes) para compatibilidade
- Nenhuma nova mensagem I2NP
- Manter o tamanho do registro de construção criptografado para compatibilidade
- Adicionar forward secrecy para Tunnel Build Messages.
- Adicionar criptografia autenticada
- Detectar hops reordenando BuildRequestRecords
- Aumentar a resolução do timestamp para que o tamanho do filtro Bloom possa ser reduzido
- Adicionar campo para expiração de túnel para que diferentes tempos de vida de túnel sejam possíveis (apenas túneis totalmente ECIES)
- Adicionar campo de opções extensível para recursos futuros
- Reutilizar primitivas criptográficas existentes
- Melhorar a segurança das mensagens de construção de túnel onde possível, mantendo a compatibilidade
- Suportar túneis com peers ElGamal/ECIES mistos
- Melhorar as defesas contra ataques de "tagging" em mensagens de construção
- Hops não precisam conhecer o tipo de criptografia do próximo hop antes de processar a mensagem de construção,
  pois podem não ter o RI do próximo hop naquele momento
- Maximizar a compatibilidade com a rede atual
- Nenhuma alteração na criptografia AES de solicitação/resposta de construção de túnel para routers ElGamal
- Nenhuma alteração na criptografia de "camada" AES de túnel, para isso veja a [Proposta 153](/proposals/153-chacha20-layer-encryption)
- Continuar suportando tanto TBM/TBRM de 8 registros quanto VTBM/VTBRM de tamanho variável
- Não exigir atualização de "dia da bandeira" para toda a rede

### Primitivas Criptográficas

- Reformulação completa das mensagens de construção de tunnel exigindo um "flag day".
- Redução das mensagens de construção de tunnel (requer hops totalmente ECIES e uma nova proposta)
- Uso de opções de construção de tunnel conforme definido na [Proposta 143](/proposals/143-build-message-options), necessário apenas para mensagens pequenas
- Tunnels bidirecionais - para isso veja a [Proposta 119](/proposals/119-bidirectional-tunnels)
- Mensagens de construção de tunnel menores - para isso veja a [Proposta 157](/proposals/157-new-tbm)

## Threat Model

### Objetivos

- Nenhum hop é capaz de determinar o originador do tunnel.

- Os hops intermediários não devem conseguir determinar a direção do tunnel
  ou sua posição no tunnel.

- Nenhum hop pode ler qualquer conteúdo de outros registros de solicitação ou resposta, exceto
  pelo hash do router truncado e chave efêmera para o próximo hop

- Nenhum membro do reply tunnel para build de saída pode ler qualquer registro de resposta.

- Nenhum membro do túnel de saída para construção de entrada pode ler qualquer registro de solicitação,
  exceto que o OBEP pode ver o hash do router truncado e a chave efêmera para o IBGW

### Não-Objetivos

Um objetivo principal do design de construção de túnel é tornar mais difícil para routers coludentes X e Y saberem que estão em um único túnel. Se o router X está no salto m e o router Y está no salto m+1, eles obviamente saberão. Mas se o router X está no salto m e o router Y está no salto m+n para n>1, isso deve ser muito mais difícil.

Ataques de marcação são onde o router X do salto intermediário altera a mensagem de construção do tunnel de tal forma que o router Y pode detectar a alteração quando a mensagem de construção chega lá. O objetivo é que qualquer mensagem alterada seja descartada por um router entre X e Y antes de chegar ao router Y. Para modificações que não são descartadas antes do router Y, o criador do tunnel deve detectar a corrupção na resposta e descartar o tunnel.

Possíveis ataques:

- Alterar um registro de build
- Substituir um registro de build
- Adicionar ou remover um registro de build
- Reordenar os registros de build

TODO: O design atual previne todos esses ataques?

## Design

### Noise Protocol Framework

Esta proposta fornece os requisitos baseados no Noise Protocol Framework [NOISE](https://noiseprotocol.org/noise.html) (Revisão 34, 2018-07-11). Na terminologia do Noise, Alice é o iniciador, e Bob é o respondedor.

Esta proposta é baseada no protocolo Noise Noise_N_25519_ChaChaPoly_SHA256. Este protocolo Noise utiliza as seguintes primitivas:

- One-Way Handshake Pattern: N
  Alice não transmite sua chave estática para Bob (N)

- Função DH: X25519
  X25519 DH com um comprimento de chave de 32 bytes conforme especificado na [RFC-7748](https://tools.ietf.org/html/rfc7748).

- Cipher Function: ChaChaPoly
  AEAD_CHACHA20_POLY1305 conforme especificado na [RFC-7539](https://tools.ietf.org/html/rfc7539) seção 2.8.
  Nonce de 12 bytes, com os primeiros 4 bytes definidos como zero.
  Idêntico ao usado no [NTCP2](/docs/specs/ntcp2/).

- Função Hash: SHA256
  Hash padrão de 32 bytes, já amplamente utilizado no I2P.

#### Additions to the Framework

Nenhum.

### Objetivos de Design

Os handshakes utilizam padrões de handshake [Noise](https://noiseprotocol.org/noise.html).

O seguinte mapeamento de letras é usado:

- e = chave efêmera de uso único
- s = chave estática
- p = carga útil da mensagem

A requisição de construção é idêntica ao padrão Noise N. Isso também é idêntico à primeira mensagem (Session Request) no padrão XK usado em [NTCP2](/docs/specs/ntcp2/).

```text
<- s
  ...
  e es p ->
```
### Ataques de Marcação

Os registros de solicitação de construção são criados pelo criador do tunnel e criptografados assimetricamente para o hop individual. Esta criptografia assimétrica dos registros de solicitação é atualmente ElGamal conforme definido em [Cryptography](/docs/specs/cryptography/) e contém um checksum SHA-256. Este design não é forward-secret.

O novo design utilizará o padrão Noise unidirecional "N" com ECIES-X25519 ephemeral-static DH, com um HKDF, e ChaCha20/Poly1305 AEAD para forward secrecy, integridade e autenticação. Alice é o solicitante de construção do tunnel. Cada salto no tunnel é um Bob.

(Propriedades de Segurança do Payload)

```text
N:                      Authentication   Confidentiality
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
### Reply encryption

Os registros de resposta de construção são criados pelo criador dos hops e criptografados simetricamente para o criador. Esta criptografia simétrica dos registros de resposta é atualmente AES com uma soma de verificação SHA-256 prefixada e contém uma soma de verificação SHA-256. Este design não é forward-secret.

O novo design usará ChaCha20/Poly1305 AEAD para integridade e autenticação.

### Framework de Protocolo Noise

A chave pública efêmera na solicitação não precisa ser ofuscada com AES ou Elligator2. O salto anterior é o único que pode vê-la, e esse salto sabe que o próximo salto é ECIES.

Os registros de resposta não precisam de criptografia assimétrica completa com outro DH.

## Specification

### Build Request Records

Os BuildRequestRecords criptografados têm 528 bytes tanto para ElGamal quanto para ECIES, por compatibilidade.

#### Request Record Unencrypted (ElGamal)

Para referência, esta é a especificação atual do BuildRequestRecord do tunnel para routers ElGamal, retirada de [I2NP](/docs/specs/i2np/). Os dados não criptografados são precedidos por um byte diferente de zero e o hash SHA-256 dos dados antes da criptografia, conforme definido em [Cryptography](/docs/specs/cryptography/).

Todos os campos estão em big-endian.

Tamanho não criptografado: 222 bytes

```text
bytes     0-3: tunnel ID to receive messages as, nonzero
  bytes    4-35: local router identity hash
  bytes   36-39: next tunnel ID, nonzero
  bytes   40-71: next router identity hash
  bytes  72-103: AES-256 tunnel layer key
  bytes 104-135: AES-256 tunnel IV key
  bytes 136-167: AES-256 reply key
  bytes 168-183: AES-256 reply IV
  byte      184: flags
  bytes 185-188: request time (in hours since the epoch, rounded down)
  bytes 189-192: next message ID
  bytes 193-221: uninterpreted / random padding
```
#### Request Record Encrypted (ElGamal)

Para referência, esta é a especificação atual do BuildRequestRecord de túnel para roteadores ElGamal, retirada de [I2NP](/docs/specs/i2np/).

Tamanho criptografado: 528 bytes

```text
bytes    0-15: Hop's truncated identity hash
  bytes  16-528: ElGamal encrypted BuildRequestRecord
```
#### Request Record Unencrypted (ECIES)

Esta é a especificação proposta do BuildRequestRecord de tunnel para routers ECIES-X25519. Resumo das alterações:

- Remover hash do router de 32 bytes não utilizado
- Alterar tempo de solicitação de horas para minutos
- Adicionar campo de expiração para tempo variável de túnel futuro
- Adicionar mais espaço para flags
- Adicionar Mapeamento para opções de construção adicionais
- Chave de resposta AES-256 e IV não são utilizados para o registro de resposta do próprio hop
- Registro não criptografado é mais longo porque há menos sobrecarga de criptografia

O registro de solicitação não contém nenhuma chave de resposta ChaCha. Essas chaves são derivadas de uma KDF. Veja abaixo.

Todos os campos são big-endian.

Tamanho não criptografado: 464 bytes

```text
bytes     0-3: tunnel ID to receive messages as, nonzero
  bytes     4-7: next tunnel ID, nonzero
  bytes    8-39: next router identity hash
  bytes   40-71: AES-256 tunnel layer key
  bytes  72-103: AES-256 tunnel IV key
  bytes 104-135: AES-256 reply key
  bytes 136-151: AES-256 reply IV
  byte      152: flags
  bytes 153-155: more flags, unused, set to 0 for compatibility
  bytes 156-159: request time (in minutes since the epoch, rounded down)
  bytes 160-163: request expiration (in seconds since creation)
  bytes 164-167: next message ID
  bytes   168-x: tunnel build options (Mapping)
  bytes     x-x: other data as implied by flags or options
  bytes   x-463: random padding
```
O campo flags é o mesmo definido em [Tunnel Creation](/docs/specs/tunnel-implementation/) e contém o seguinte::

```text
Bit order: 76543210 (bit 7 is MSB)
bit 7: if set, allow messages from anyone
bit 6: if set, allow messages to anyone, and send the reply to the
       specified next hop in a Tunnel Build Reply Message
bits 5-0: Undefined, must set to 0 for compatibility with future options
```
Ordem dos bits: 76543210 (bit 7 é MSB)  bit 7: se definido, permite mensagens de qualquer um  bit 6: se definido, permite mensagens para qualquer um, e envia a resposta para o

bits 5-0: Indefinido, deve ser definido como 0 para compatibilidade com opções futuras

O bit 7 indica que o hop será um gateway de entrada (IBGW). O bit 6 indica que o hop será um endpoint de saída (OBEP). Se nenhum bit estiver definido, o hop será um participante intermediário. Ambos não podem estar definidos ao mesmo tempo.

#### Request Record Encrypted (ECIES)

A expiração da solicitação é para duração variável de túnel futura. Por enquanto, o único valor suportado é 600 (10 minutos).

As opções de construção do tunnel são uma estrutura Mapping conforme definido em [Common Structures](/docs/specs/common-structures/). Isto é para uso futuro. Nenhuma opção está atualmente definida. Se a estrutura Mapping estiver vazia, isto são dois bytes 0x00 0x00. O tamanho máximo do Mapping (incluindo o campo de comprimento) é de 296 bytes, e o valor máximo do campo de comprimento do Mapping é 294.

```text
bytes    0-15: Hop's truncated identity hash
  bytes   16-47: Sender's ephemeral X25519 public key
  bytes  48-511: ChaCha20 encrypted BuildRequestRecord
  bytes 512-527: Poly1305 MAC
```
### Padrões de Handshake

Todos os campos são big-endian exceto para a chave pública efêmera que é little-endian.

#### Reply Record Unencrypted (ElGamal)

Tamanho criptografado: 528 bytes

Os BuildReplyRecords criptografados têm 528 bytes tanto para ElGamal quanto para ECIES, para compatibilidade.

As respostas ElGamal são criptografadas com AES.

```text
bytes   0-31: SHA-256 Hash of bytes 32-527
  bytes 32-526: random data
  byte     527: reply

  total length: 528
```
#### Reply Record Unencrypted (ECIES)

Todos os campos são big-endian.

- Adicionar Mapeamento para opções de resposta de construção
- Registro não criptografado é mais longo porque há menos sobrecarga de criptografia

Tamanho não criptografado: 528 bytes

Esta é a especificação proposta do BuildReplyRecord de tunnel para routers ECIES-X25519. Resumo das mudanças:

As respostas ECIES são criptografadas com ChaCha20/Poly1305.

```text
bytes    0-x: Tunnel Build Reply Options (Mapping)
  bytes    x-x: other data as implied by options
  bytes  x-510: Random padding
  byte     511: Reply byte
```
Todos os campos estão em big-endian.

Tamanho não criptografado: 512 bytes

- 0x00 (aceitar)
- 30 (TUNNEL_REJECT_BANDWIDTH)

#### Reply Record Encrypted (ECIES)

As opções de resposta de construção de tunnel são uma estrutura Mapping conforme definida em [Common Structures](/docs/specs/common-structures/). Isto é para uso futuro. Nenhuma opção está atualmente definida. Se a estrutura Mapping estiver vazia, são dois bytes 0x00 0x00. O tamanho máximo do Mapping (incluindo o campo de comprimento) é de 511 bytes, e o valor máximo do campo de comprimento do Mapping é 509.

```text
bytes   0-511: ChaCha20 encrypted BuildReplyRecord
  bytes 512-527: Poly1305 MAC
```
O byte de resposta é um dos seguintes valores conforme definido em [Tunnel Creation](/docs/specs/tunnel-implementation/) para evitar fingerprinting:

### Criptografia de solicitação

Tamanho criptografado: 528 bytes

Após a transição completa para registros ECIES, as regras de preenchimento por intervalos são as mesmas dos registros de solicitação.

- "encryption":

- cifra executada em modo de descriptografia
- registros de solicitação descriptografados preventivamente no pré-processamento (ocultando registros de solicitação criptografados)

- "decryption":

- cipher executado em modo de encriptação
- registros de solicitação encriptados (revelando o próximo registro de solicitação em texto plano) por saltos de participantes

- ChaCha20 não possui "modos", então é simplesmente executado três vezes:

- uma vez no pré-processamento
- uma vez pelo hop
- uma vez no processamento final da resposta

Túneis mistos são permitidos, e necessários, para a transição do ElGamal para ECIES. Durante o período de transição, um número crescente de routers será configurado com chaves ECIES.

O pré-processamento de criptografia simétrica será executado da mesma forma:

Quando túneis mistos são utilizados, os criadores de túnel precisarão basear a criptografia simétrica do BuildRequestRecord no tipo de criptografia do hop atual e anterior.

Cada hop usará seu próprio tipo de criptografia para criptografar BuildReplyRecords, e os outros registros no VariableTunnelBuildMessage (VTBM).

- Remetente (OBGW) -> ElGamal (H1) -> ECIES (H2) -> ElGamal (H3)

No caminho de resposta, o endpoint (remetente) precisará desfazer a [Multiple Encryption](https://en.wikipedia.org/wiki/Multiple_encryption), usando a chave de resposta de cada hop.

Como exemplo esclarecedor, vamos ver um tunnel de saída com ECIES cercado por ElGamal:

Todos os BuildRequestRecords estão no seu estado criptografado (usando ElGamal ou ECIES).

A cifra AES256/CBC, quando utilizada, ainda é usada para cada registro, sem encadeamento através de múltiplos registros.

- O registro do H3 é "criptografado" usando:

- Chave de resposta do H2 (ChaCha20)
- Chave de resposta do H1 (AES256/CBC)

- O registro do H2 é "criptografado" usando:

- Chave de resposta do H1 (AES256/CBC)

- O registro H1 sai sem criptografia simétrica

Da mesma forma, o ChaCha20 será usado para criptografar cada registro, não transmitindo em streaming através de todo o VTBM.

Os registros de solicitação são pré-processados pelo Remetente (OBGW):

- O registro do H3 é "decriptado" usando:

- Chave de resposta do H3 (AES256/CBC)

- O registro do H2 é "descriptografado" usando:

- Chave de resposta do H3 (AES256/CBC)
- Chave de resposta do H2 (ChaCha20-Poly1305)

- O registro H1 é "descriptografado" usando:

- Chave de resposta do H3 (AES256/CBC)
- Chave de resposta do H2 (ChaCha20)
- Chave de resposta do H1 (AES256/CBC)

Apenas H2 verifica a flag de criptografia da resposta, e vê que é seguida por AES256/CBC.

- O registro do H3 é "criptografado" usando:

- Chave de resposta do H3 (AES256/CBC)

- O registro do H2 é "criptografado" usando:

- Chave de resposta do H3 (AES256/CBC)
- Chave de resposta do H2 (ChaCha20-Poly1305)

- O registro do H1 é "criptografado" usando:

- Chave de resposta do H3 (AES256/CBC)
- Chave de resposta do H2 (ChaCha20)
- Chave de resposta do H1 (AES256/CBC)

### Criptografia de resposta

Após serem processados por cada salto, os registros ficam em um estado "descriptografado":

O criador do tunnel, também conhecido como Inbound Endpoint (IBEP), pós-processa a resposta:

#### KDF for Initial ck and h

Essas chaves são explicitamente incluídas nos ElGamal BuildRequestRecords. Para ECIES BuildRequestRecords, as chaves de túnel e chaves de resposta AES são incluídas, mas as chaves de resposta ChaCha são derivadas da troca DH. Veja a [Proposta 156](/proposals/156-ecies-routers) para detalhes das chaves ECIES estáticas do router.

```text
This is the "e" message pattern:

  // Define protocol_name.
  Set protocol_name = "Noise_N_25519_ChaChaPoly_SHA256"
  (31 bytes, US-ASCII encoded, no NULL termination).

  // Define Hash h = 32 bytes
  // Pad to 32 bytes. Do NOT hash it, because it is not more than 32 bytes.
  h = protocol_name || 0

  Define ck = 32 byte chaining key. Copy the h data to ck.
  Set chainKey = h

  // MixHash(null prologue)
  h = SHA256(h);

  // up until here, can all be precalculated by all routers.
```
#### KDF for Request Record

Abaixo está uma descrição de como derivar as chaves previamente transmitidas nos registros de solicitação.

Este é o [NOISE](https://noiseprotocol.org/noise.html) padrão para o padrão "N" com um nome de protocolo padrão.

Os criadores de tunnel ElGamal geram um par de chaves X25519 efêmero para cada hop ECIES no tunnel, e usam o esquema acima para criptografar seu BuildRequestRecord. Os criadores de tunnel ElGamal usarão o esquema anterior a esta especificação para criptografar para hops ElGamal.

Os criadores de túneis ECIES precisarão criptografar para cada chave pública do hop ElGamal usando o esquema definido em [Tunnel Creation](/docs/specs/tunnel-implementation/). Os criadores de túneis ECIES usarão o esquema acima para criptografar para hops ECIES.

Isso significa que os saltos do tunnel só verão registros criptografados do mesmo tipo de criptografia.

```text
// Each hop's X25519 static keypair (hesk, hepk) from the Router Identity
  hesk = GENERATE_PRIVATE()
  hepk = DERIVE_PUBLIC(hesk)

  // MixHash(hepk)
  // || below means append
  h = SHA256(h || hepk);

  // up until here, can all be precalculated by each router
  // for all incoming build requests

  // Sender generates an X25519 ephemeral keypair per ECIES hop in the VTBM (sesk, sepk)
  sesk = GENERATE_PRIVATE()
  sepk = DERIVE_PUBLIC(sesk)

  // MixHash(sepk)
  h = SHA256(h || sepk);

  End of "e" message pattern.

  This is the "es" message pattern:

  // Noise es
  // Sender performs an X25519 DH with Hop's static public key.
  // Each Hop, finds the record w/ their truncated identity hash,
  // and extracts the Sender's ephemeral key preceding the encrypted record.
  sharedSecret = DH(sesk, hepk) = DH(hesk, sepk)

  // MixKey(DH())
  //[chainKey, k] = MixKey(sharedSecret)
  // ChaChaPoly parameters to encrypt/decrypt
  keydata = HKDF(chainKey, sharedSecret, "", 64)
  // Save for Reply Record KDF
  chainKey = keydata[0:31]

  // AEAD parameters
  k = keydata[32:63]
  n = 0
  plaintext = 464 byte build request record
  ad = h
  ciphertext = ENCRYPT(k, n, plaintext, ad)

  End of "es" message pattern.

  // MixHash(ciphertext)
  // Save for Reply Record KDF
  h = SHA256(h || ciphertext)
```
Para criadores de túneis ElGamal e ECIES, eles irão gerar pares de chaves X25519 efêmeras únicas por salto para criptografar para saltos ECIES.

### Justificação

**IMPORTANTE**: As chaves efêmeras devem ser únicas por hop ECIES e por registro de construção. Falhar em usar chaves únicas abre um vetor de ataque para hops coludentes confirmarem que estão no mesmo túnel.

### Reply Record Encryption (ECIES)

``replyKey``, ``layerKey`` e ``layerIV`` ainda devem ser incluídos dentro dos registros ElGamal, e podem ser gerados aleatoriamente.

```text
// AEAD parameters
  k = chainkey from build request
  n = 0
  plaintext = 512 byte build reply record
  ad = h from build request

  ciphertext = ENCRYPT(k, n, plaintext, ad)
```
### Registros de Solicitação de Build

Conforme definido em [Tunnel Creation](/docs/specs/tunnel-implementation/). Não há alterações na criptografia para hops ElGamal.

### Security Analysis

O registro de resposta é criptografado com ChaCha20/Poly1305.

Como definido em [Tunnel Creation](/docs/specs/tunnel-implementation/). Não há mudanças na criptografia para hops ElGamal.

ElGamal não oferece sigilo futuro para Mensagens de Construção de Tunnel.

AES256/CBC está em uma situação ligeiramente melhor, sendo vulnerável apenas a um enfraquecimento teórico de um ataque de `biclique` com texto simples conhecido.

O único ataque prático conhecido contra AES256/CBC é um ataque de oráculo de preenchimento, quando o IV é conhecido pelo atacante.

Um atacante precisaria quebrar a criptografia ElGamal do próximo salto para obter as informações da chave AES256/CBC (chave de resposta e IV).

ElGamal é significativamente mais intensivo em CPU do que ECIES, levando a um potencial esgotamento de recursos.

## Modelo de Ameaças

ECIES, usado com novas chaves efêmeras por-BuildRequestRecord ou VariableTunnelBuildMessage, fornece forward-secrecy.

## Implementation Notes

* Routers mais antigos não verificam o tipo de encriptação do hop e enviarão registros
  encriptados com ElGamal. Alguns routers recentes têm bugs e enviarão vários tipos de registros
  malformados. Os implementadores devem detectar e rejeitar esses registros antes da operação
  DH, se possível, para reduzir o uso da CPU.

## Issues

## Projeto

ChaCha20Poly1305 fornece criptografia AEAD, permitindo que o destinatário verifique a integridade da mensagem antes de tentar a descriptografia.

## Referências

* [Comum](/docs/specs/common-structures/)
* [Criptografia](/docs/specs/cryptography/)
* [ECIES-X25519](/docs/specs/ecies/)
* [I2NP](/docs/specs/i2np/)
* [NOISE](https://noiseprotocol.org/noise.html)
* [NTCP2](/docs/specs/ntcp2/)
* [Prop119](/proposals/119-bidirectional-tunnels/)
* [Prop143](/proposals/143-build-message-options/)
* [Prop153](/proposals/153-chacha20-layer-encryption/)
* [Prop156](/proposals/156-ecies-routers/)
* [Prop157](/proposals/157-new-tbm/)
* [SPEC](/docs/specs/tunnel-implementation/#tunnel-creation-ecies)
* [Criação de Tunnel](/docs/specs/tunnel-implementation/#tunnel-creation-ecies)
* [Criptografia Múltipla](https://en.wikipedia.org/wiki/Multiple_encryption)
* [RFC-7539](https://tools.ietf.org/html/rfc7539)
* [RFC-7748](https://tools.ietf.org/html/rfc7748)
