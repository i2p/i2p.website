---
title: "Especificação de Criação de Tunnel (ECIES-X25519)"
description: "Criptografia de mensagem Tunnel Build usando primitivas criptográficas ECIES-X25519 para sigilo direto."
slug: "tunnel-creation-ecies"
aliases:
  - "/pt/docs/specs/tunnel-creation-ecies-spec"
  - "/pt/docs/specs/tunnel-creation-ecies-spec/"
category: "Protocolos"
lastUpdated: "2025-06"
accurateFor: "0.9.66"
---

## Visão Geral

Este documento especifica a criptografia de mensagens Tunnel Build usando primitivas criptográficas introduzidas por [ECIES-X25519](/docs/specs/ecies/). É uma parte da proposta geral [Prop156](/proposals/156/) para converter routers de chaves ElGamal para ECIES-X25519.

Existem duas versões especificadas. A primeira usa as mensagens de construção existentes e o tamanho de registro de construção atual, para compatibilidade com roteadores ElGamal. Esta especificação foi implementada a partir da versão 0.9.48 e agora está obsoleta. A segunda usa duas novas mensagens de construção e um tamanho de registro de construção menor, e só pode ser usada com roteadores ECIES. Esta especificação está implementada a partir da versão 0.9.51.

Para os propósitos de transição da rede de ElGamal + AES256 para ECIES + ChaCha20, tunnels com routers ElGamal e ECIES mistos são necessários. Especificações para lidar com hops de tunnel mistos são fornecidas. Nenhuma mudança será feita no formato, processamento ou criptografia de hops ElGamal. Este formato mantém o mesmo tamanho para registros de construção de tunnel, conforme necessário para compatibilidade.

Criadores de tunnel ElGamal irão gerar pares de chaves X25519 efêmeros por salto, e seguir esta especificação para criar tunnels contendo saltos ECIES.

Este documento especifica a Construção de Tunnel ECIES-X25519. Para uma visão geral de todas as mudanças necessárias para routers ECIES, veja a proposta 156 [Prop156](/proposals/156/). Para informações adicionais sobre o desenvolvimento da especificação de registro longo, veja a proposta 152 [Prop152](/proposals/152/). Para informações adicionais sobre o desenvolvimento da especificação de registro curto, veja a proposta 157 [Prop157](/proposals/157/).

### Primitivas Criptográficas

Os primitivos necessários para implementar esta especificação são:

- AES-256-CBC como em [Cryptography](/docs/specs/cryptography/)
- Funções STREAM ChaCha20: ENCRYPT(k, iv, plaintext) e DECRYPT(k, iv, ciphertext) - como em [EncryptedLeaseSet](/docs/specs/encryptedleaseset/) e [RFC-7539](https://tools.ietf.org/html/rfc7539)
- Funções STREAM ChaCha20/Poly1305: ENCRYPT(k, n, plaintext, ad) e DECRYPT(k, n, ciphertext, ad) - como em [NTCP2](/docs/specs/ntcp2/), [ECIES-X25519](/docs/specs/ecies/), e [RFC-7539](https://tools.ietf.org/html/rfc7539)
- Funções X25519 DH - como em [NTCP2](/docs/specs/ntcp2/) e [ECIES-X25519](/docs/specs/ecies/)
- HKDF(salt, ikm, info, n) - como em [NTCP2](/docs/specs/ntcp2/) e [ECIES-X25519](/docs/specs/ecies/)

Outras funções Noise definidas em outros locais:

- MixHash(d) - como em [NTCP2](/docs/specs/ntcp2/) e [ECIES-X25519](/docs/specs/ecies/)
- MixKey(d) - como em [NTCP2](/docs/specs/ntcp2/) e [ECIES-X25519](/docs/specs/ecies/)

## Design

### Noise Protocol Framework

Esta especificação fornece os requisitos baseados no Noise Protocol Framework [NOISE](https://noiseprotocol.org/noise.html) (Revisão 34, 2018-07-11). Na terminologia do Noise, Alice é o iniciador, e Bob é o respondedor.

É baseado no protocolo Noise Noise_N_25519_ChaChaPoly_SHA256. Este protocolo Noise usa as seguintes primitivas:

- Padrão de Handshake Unidirecional: N - Alice não transmite sua chave estática para Bob (N)
- Função DH: X25519 - X25519 DH com um comprimento de chave de 32 bytes conforme especificado em [RFC-7748](https://tools.ietf.org/html/rfc7748)
- Função de Cifra: ChaChaPoly - AEAD_CHACHA20_POLY1305 conforme especificado em [RFC-7539](https://tools.ietf.org/html/rfc7539) seção 2.8. Nonce de 12 bytes, com os primeiros 4 bytes definidos como zero. Idêntico ao usado em [NTCP2](/docs/specs/ntcp2/)
- Função Hash: SHA256 - Hash padrão de 32 bytes, já usado extensivamente no I2P

### Padrões de Handshake

Os handshakes usam padrões de handshake [Noise](https://noiseprotocol.org/noise.html).

O seguinte mapeamento de letras é utilizado:

- e = chave efêmera de uso único
- s = chave estática
- p = carga útil da mensagem

A solicitação de construção é idêntica ao padrão Noise N. Isso também é idêntico à primeira mensagem (Solicitação de Sessão) no padrão XK usado em [NTCP2](/docs/specs/ntcp2/).

```
<- s
  ...
  e es p ->
```
### Criptografia de Solicitação

Os registros de solicitação de construção são criados pelo criador do tunnel e criptografados assimetricamente para o hop individual. Esta criptografia assimétrica dos registros de solicitação é atualmente ElGamal conforme definido em [Cryptography](/docs/specs/cryptography/) e contém uma soma de verificação SHA-256. Este design não possui sigilo futuro.

O design ECIES usa o padrão Noise unidirecional "N" com DH efêmero-estático ECIES-X25519, com um HKDF, e ChaCha20/Poly1305 AEAD para sigilo progressivo, integridade e autenticação. Alice é o solicitante da construção do tunnel. Cada salto no tunnel é um Bob.

### Criptografia de Resposta

Os registros de resposta de build são criados pelo criador dos hops e criptografados simetricamente para o criador. Esta criptografia simétrica dos registros de resposta ElGamal é AES com uma soma de verificação SHA-256 prefixada. Este design não possui sigilo futuro.

As respostas ECIES usam ChaCha20/Poly1305 AEAD para integridade e autenticação.

## Especificação de Registro Longo

NOTA: Descontinuado, obsoleto. Use o formato Short Record especificado abaixo.

### Registros de Solicitação de Construção

BuildRequestRecords criptografados têm 528 bytes tanto para ElGamal quanto para ECIES, para compatibilidade.

#### Registro de Solicitação Não Criptografado

Esta é a especificação do BuildRequestRecord de tunnel para routers ECIES-X25519. Resumo das alterações:

- Remover hash do router de 32 bytes não utilizado
- Alterar tempo de solicitação de horas para minutos
- Adicionar campo de expiração para tempo de tunnel variável futuro
- Adicionar mais espaço para flags
- Adicionar Mapeamento para opções de construção adicionais
- Chave de resposta AES-256 e IV não são utilizados para o próprio registro de resposta do hop
- Registro não criptografado é mais longo porque há menos sobrecarga de criptografia

O registro de solicitação não contém nenhuma chave de resposta ChaCha. Essas chaves são derivadas de uma KDF. Veja abaixo.

Todos os campos estão em big-endian.

Tamanho não criptografado: 464 bytes

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
<thead>
<tr>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Bytes</th>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contents</th>
</tr>
</thead>
<tbody>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">0-3</td><td style="border:1px solid var(--color-border); padding:0.6rem;">tunnel ID to receive messages as, nonzero</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">4-7</td><td style="border:1px solid var(--color-border); padding:0.6rem;">next tunnel ID, nonzero</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">8-39</td><td style="border:1px solid var(--color-border); padding:0.6rem;">next router identity hash</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">40-71</td><td style="border:1px solid var(--color-border); padding:0.6rem;">AES-256 tunnel layer key</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">72-103</td><td style="border:1px solid var(--color-border); padding:0.6rem;">AES-256 tunnel IV key</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">104-135</td><td style="border:1px solid var(--color-border); padding:0.6rem;">AES-256 reply key</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">136-151</td><td style="border:1px solid var(--color-border); padding:0.6rem;">AES-256 reply IV</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">152</td><td style="border:1px solid var(--color-border); padding:0.6rem;">flags</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">153-155</td><td style="border:1px solid var(--color-border); padding:0.6rem;">more flags, unused, set to 0 for compatibility</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">156-159</td><td style="border:1px solid var(--color-border); padding:0.6rem;">request time (in minutes since the epoch, rounded down)</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">160-163</td><td style="border:1px solid var(--color-border); padding:0.6rem;">request expiration (in seconds since creation)</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">164-167</td><td style="border:1px solid var(--color-border); padding:0.6rem;">next message ID</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">168-x</td><td style="border:1px solid var(--color-border); padding:0.6rem;">tunnel build options (Mapping)</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">x-x</td><td style="border:1px solid var(--color-border); padding:0.6rem;">other data as implied by flags or options</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">x-463</td><td style="border:1px solid var(--color-border); padding:0.6rem;">random padding</td></tr>
</tbody>
</table>
O campo flags é o mesmo definido em [Tunnel-Creation](/docs/specs/tunnel-creation/) e contém o seguinte:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
<thead>
<tr>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Bit</th>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Description</th>
</tr>
</thead>
<tbody>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;" colspan="2"><em>Bit order: 76543210 (bit 7 is MSB)</em></td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">7</td><td style="border:1px solid var(--color-border); padding:0.6rem;">if set, allow messages from anyone</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">6</td><td style="border:1px solid var(--color-border); padding:0.6rem;">if set, allow messages to anyone, and send the reply to the specified next hop in a Tunnel Build Reply Message</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">5-0</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Undefined, must set to 0 for compatibility with future options</td></tr>
</tbody>
</table>
O bit 7 indica que o salto será um gateway de entrada (IBGW). O bit 6 indica que o salto será um endpoint de saída (OBEP). Se nenhum bit estiver definido, o salto será um participante intermediário. Ambos não podem ser definidos ao mesmo tempo.

A expiração da solicitação é para duração variável futura do tunnel. Por enquanto, o único valor suportado é 600 (10 minutos).

As opções de construção de tunnel é uma estrutura Mapping conforme definido em [Common](/docs/specs/common-structures/). As únicas opções atualmente definidas são para parâmetros de largura de banda, a partir da API 0.9.65, veja abaixo para detalhes. Se a estrutura Mapping estiver vazia, isso são dois bytes 0x00 0x00. O tamanho máximo do Mapping (incluindo o campo de comprimento) é 296 bytes, e o valor máximo do campo de comprimento do Mapping é 294.

#### Registro de Solicitação Criptografado

Todos os campos estão em big-endian, exceto a chave pública efêmera que está em little-endian.

Tamanho criptografado: 528 bytes

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
<thead>
<tr>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Bytes</th>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contents</th>
</tr>
</thead>
<tbody>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">0-15</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Hop's truncated identity hash</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">16-47</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Sender's ephemeral X25519 public key</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">48-511</td><td style="border:1px solid var(--color-border); padding:0.6rem;">ChaCha20 encrypted BuildRequestRecord</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">512-527</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Poly1305 MAC</td></tr>
</tbody>
</table>
### Construir Registros de Resposta

BuildReplyRecords encriptados têm 528 bytes tanto para ElGamal quanto para ECIES, para compatibilidade.

#### Registro de Resposta Não Criptografado

Esta é a especificação do BuildReplyRecord do tunnel para routers ECIES-X25519. Resumo das mudanças:

- Adicionar Mapeamento para opções de resposta de construção
- Registro não criptografado é mais longo porque há menos sobrecarga de criptografia

Respostas ECIES são criptografadas com ChaCha20/Poly1305.

Todos os campos estão em big-endian.

Tamanho não criptografado: 512 bytes

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
<thead>
<tr>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Bytes</th>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contents</th>
</tr>
</thead>
<tbody>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">0-x</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Tunnel Build Reply Options (Mapping)</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">x-x</td><td style="border:1px solid var(--color-border); padding:0.6rem;">other data as implied by options</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">x-510</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Random padding</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">511</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Reply byte</td></tr>
</tbody>
</table>
As opções de resposta de construção de tunnel são uma estrutura Mapping conforme definido em [Common](/docs/specs/common-structures/). As únicas opções atualmente definidas são para parâmetros de largura de banda, a partir da API 0.9.65, veja abaixo para detalhes. Se a estrutura Mapping estiver vazia, são dois bytes 0x00 0x00. O tamanho máximo do Mapping (incluindo o campo de comprimento) é 511 bytes, e o valor máximo do campo de comprimento do Mapping é 509.

O byte de resposta é um dos seguintes valores conforme definido em [Tunnel-Creation](/docs/specs/tunnel-creation/) para evitar fingerprinting:

- 0x00 (aceitar)
- 30 (TUNNEL_REJECT_BANDWIDTH)

#### Registro de Resposta Criptografado

Tamanho criptografado: 528 bytes

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
<thead>
<tr>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Bytes</th>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contents</th>
</tr>
</thead>
<tbody>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">0-511</td><td style="border:1px solid var(--color-border); padding:0.6rem;">ChaCha20 encrypted BuildReplyRecord</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">512-527</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Poly1305 MAC</td></tr>
</tbody>
</table>
Após a transição completa para registros ECIES, as regras de padding intervalado são as mesmas que para registros de solicitação.

### Criptografia Simétrica de Registros

Túneis mistos são permitidos, e necessários, para a transição do ElGamal para ECIES. Durante o período de transição, um número crescente de roteadores será configurado com chaves ECIES.

O pré-processamento de criptografia simétrica será executado da mesma forma:

- "encryption":
  - cipher executado em modo de descriptografia
  - registros de solicitação descriptografados preventivamente no pré-processamento (ocultando registros de solicitação criptografados)
- "decryption":
  - cipher executado em modo de criptografia
  - registros de solicitação criptografados (revelando próximo registro de solicitação em texto simples) pelos hops participantes
- ChaCha20 não possui "modos", então é simplesmente executado três vezes:
  - uma vez no pré-processamento
  - uma vez pelo hop
  - uma vez no processamento final da resposta

Quando tunnels mistos são usados, os criadores de tunnel precisarão basear a criptografia simétrica do BuildRequestRecord no tipo de criptografia do hop atual e do anterior.

Cada hop utilizará seu próprio tipo de criptografia para criptografar BuildReplyRecords e os outros registros no VariableTunnelBuildMessage (VTBM).

No caminho de resposta, o endpoint (remetente) precisará desfazer a [Multiple-Encryption](https://en.wikipedia.org/wiki/Multiple_encryption), usando a chave de resposta de cada hop.

Como exemplo esclarecedor, vamos analisar um tunnel de saída com ECIES rodeado por ElGamal:

- Remetente (OBGW) -> ElGamal (H1) -> ECIES (H2) -> ElGamal (H3)

Todos os BuildRequestRecords estão em seu estado criptografado (usando ElGamal ou ECIES).

A cifra AES256/CBC, quando usada, ainda é utilizada para cada registro, sem encadeamento entre múltiplos registros.

Da mesma forma, ChaCha20 será usado para criptografar cada registro, não transmitindo por todo o VTBM.

Os registros de solicitação são pré-processados pelo Remetente (OBGW):

- O registro de H3 é "criptografado" usando:
  - A chave de resposta de H2 (ChaCha20)
  - A chave de resposta de H1 (AES256/CBC)
- O registro de H2 é "criptografado" usando:
  - A chave de resposta de H1 (AES256/CBC)
- O registro de H1 é enviado sem criptografia simétrica

Apenas o H2 verifica a flag de criptografia de resposta, e vê que é seguida por AES256/CBC.

Após serem processados por cada salto, os registros ficam em um estado "descriptografado":

- O registro do H3 é "descriptografado" usando:
  - Chave de resposta do H3 (AES256/CBC)
- O registro do H2 é "descriptografado" usando:
  - Chave de resposta do H3 (AES256/CBC)
  - Chave de resposta do H2 (ChaCha20-Poly1305)
- O registro do H1 é "descriptografado" usando:
  - Chave de resposta do H3 (AES256/CBC)
  - Chave de resposta do H2 (ChaCha20)
  - Chave de resposta do H1 (AES256/CBC)

O criador do tunnel, também conhecido como Inbound Endpoint (IBEP), pós-processa a resposta:

- O registro do H3 é "criptografado" usando:
  - Chave de resposta do H3 (AES256/CBC)
- O registro do H2 é "criptografado" usando:
  - Chave de resposta do H3 (AES256/CBC)
  - Chave de resposta do H2 (ChaCha20-Poly1305)
- O registro do H1 é "criptografado" usando:
  - Chave de resposta do H3 (AES256/CBC)
  - Chave de resposta do H2 (ChaCha20)
  - Chave de resposta do H1 (AES256/CBC)

### Chaves de Registro de Solicitação

Essas chaves são explicitamente incluídas nos ElGamal BuildRequestRecords. Para ECIES BuildRequestRecords, as chaves de túnel e chaves de resposta AES são incluídas, mas as chaves de resposta ChaCha são derivadas da troca DH. Veja [Prop156](/proposals/156/) para detalhes das chaves ECIES estáticas do router.

Abaixo está uma descrição de como derivar as chaves previamente transmitidas nos registros de solicitação.

#### KDF para ck e h Iniciais

Este é o [NOISE](https://noiseprotocol.org/noise.html) padrão para o padrão "N" com um nome de protocolo padrão.

```
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
#### KDF para Registro de Solicitação

Criadores de tunnel ElGamal geram um par de chaves X25519 efêmero para cada hop ECIES no tunnel, e usam o esquema acima para criptografar seu BuildRequestRecord. Criadores de tunnel ElGamal usarão o esquema anterior a esta especificação para criptografar para hops ElGamal.

Os criadores de tunnel ECIES precisarão criptografar para cada chave pública do salto ElGamal usando o esquema definido em [Tunnel-Creation](/docs/specs/tunnel-creation/). Os criadores de tunnel ECIES usarão o esquema acima para criptografar para saltos ECIES.

Isso significa que os saltos do tunnel só verão registros criptografados do mesmo tipo de criptografia.

Para criadores de tunnel ElGamal e ECIES, eles irão gerar pares de chaves efêmeras X25519 únicos por salto para criptografar para saltos ECIES.

**IMPORTANTE**: As chaves efêmeras devem ser únicas por hop ECIES e por registro de construção. Falhar em usar chaves únicas abre um vetor de ataque para hops em conluio confirmarem que estão no mesmo tunnel.

```
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
`replyKey`, `layerKey` e `layerIV` ainda devem ser incluídos dentro dos registros ElGamal, e podem ser gerados aleatoriamente.

### Criptografia de Registro de Resposta

O registro de resposta é criptografado com ChaCha20/Poly1305.

```
// AEAD parameters
k = chainkey from build request
n = 0
plaintext = 512 byte build reply record
ad = h from build request

ciphertext = ENCRYPT(k, n, plaintext, ad)
```
## Especificação de Registro Curto

Esta especificação usa duas novas mensagens I2NP de construção de tunnel, Short Tunnel Build Message (tipo 25) e Outbound Tunnel Build Reply Message (tipo 26).

O criador do tunnel e todos os hops no tunnel criado devem suportar ECIES-X25519, e pelo menos a versão 0.9.51. Os hops no tunnel de resposta (para uma construção outbound) ou o tunnel outbound (para uma construção inbound) não têm nenhum requisito.

Registros de solicitação e resposta criptografados terão 218 bytes, comparado a 528 bytes para todas as outras mensagens de construção.

Os registros de solicitação em texto simples terão 154 bytes, comparados a 222 bytes para registros ElGamal, e 464 bytes para registros ECIES conforme definido acima.

Os registros de resposta em texto simples terão 202 bytes, comparado a 496 bytes para registros ElGamal, e 512 bytes para registros ECIES conforme definido acima.

A criptografia de resposta será ChaCha20/Poly1305 para o registro do próprio salto, e ChaCha20 (NÃO ChaCha20/Poly1305) para os outros registros na mensagem de construção.

Os registos de solicitação serão tornados menores usando HKDF para criar as chaves de camada e resposta, para que não sejam explicitamente incluídos na solicitação.

### Fluxo de Mensagens

```
STBM: Short tunnel build message (type 25)
OTBRM: Outbound tunnel build reply message (type 26)

Outbound Build A-B-C
Reply through existing inbound D-E-F


                New Tunnel
         STBM      STBM      STBM
Creator ------> A ------> B ------> C ---\
                                   OBEP   \
                                          | Garlic wrapped (optional)
                                          | OTBRM
                                          | (TUNNEL delivery)
                                          | from OBEP to
                                          | creator
              Existing Tunnel             /
Creator <-------F---------E-------- D <--/
                                   IBGW



Inbound Build D-E-F
Sent through existing outbound A-B-C


              Existing Tunnel
Creator ------> A ------> B ------> C ---\
                                  OBEP    \
                                          | Garlic wrapped (optional)
                                          | STBM
                                          | (ROUTER delivery)
                                          | from creator
                New Tunnel                | to IBGW
          STBM      STBM      STBM        /
Creator <------ F <------ E <------ D <--/
                                   IBGW
```
#### Notas

O envolvimento garlic das mensagens as oculta do OBEP (para uma construção de entrada) ou do IBGW (para uma construção de saída). Isso é recomendado, mas não obrigatório. Se o OBEP e o IBGW forem o mesmo router, não é necessário.

### Registos de Solicitação de Construção Curtos

BuildRequestRecords criptografados curtos têm 218 bytes.

#### Registro de Solicitação Curta Não Criptografado

Resumo das mudanças dos registros longos:

- Alterar comprimento não criptografado de 464 para 154 bytes
- Alterar comprimento criptografado de 528 para 218 bytes
- Remover chaves de camada e resposta e IVs, elas serão geradas a partir de um KDF

O registro de solicitação não contém nenhuma chave de resposta ChaCha. Essas chaves são derivadas de uma KDF. Veja abaixo.

Todos os campos são big-endian.

Tamanho não criptografado: 154 bytes.

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
<thead>
<tr>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Bytes</th>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contents</th>
</tr>
</thead>
<tbody>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">0-3</td><td style="border:1px solid var(--color-border); padding:0.6rem;">tunnel ID to receive messages as, nonzero</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">4-7</td><td style="border:1px solid var(--color-border); padding:0.6rem;">next tunnel ID, nonzero</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">8-39</td><td style="border:1px solid var(--color-border); padding:0.6rem;">next router identity hash</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">40</td><td style="border:1px solid var(--color-border); padding:0.6rem;">flags</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">41-42</td><td style="border:1px solid var(--color-border); padding:0.6rem;">more flags, unused, set to 0 for compatibility</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">43</td><td style="border:1px solid var(--color-border); padding:0.6rem;">layer encryption type</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">44-47</td><td style="border:1px solid var(--color-border); padding:0.6rem;">request time (in minutes since the epoch, rounded down)</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">48-51</td><td style="border:1px solid var(--color-border); padding:0.6rem;">request expiration (in seconds since creation)</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">52-55</td><td style="border:1px solid var(--color-border); padding:0.6rem;">next message ID</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">56-x</td><td style="border:1px solid var(--color-border); padding:0.6rem;">tunnel build options (Mapping)</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">x-x</td><td style="border:1px solid var(--color-border); padding:0.6rem;">other data as implied by flags or options</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">x-153</td><td style="border:1px solid var(--color-border); padding:0.6rem;">random padding (see below)</td></tr>
</tbody>
</table>
O campo flags é o mesmo definido em [Tunnel-Creation](/docs/specs/tunnel-creation/) e contém o seguinte:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
<thead>
<tr>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Bit</th>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Description</th>
</tr>
</thead>
<tbody>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;" colspan="2"><em>Bit order: 76543210 (bit 7 is MSB)</em></td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">7</td><td style="border:1px solid var(--color-border); padding:0.6rem;">if set, allow messages from anyone</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">6</td><td style="border:1px solid var(--color-border); padding:0.6rem;">if set, allow messages to anyone, and send the reply to the specified next hop in a Tunnel Build Reply Message</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">5-0</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Undefined, must set to 0 for compatibility with future options</td></tr>
</tbody>
</table>
O bit 7 indica que o hop será um gateway de entrada (IBGW). O bit 6 indica que o hop será um endpoint de saída (OBEP). Se nenhum bit estiver definido, o hop será um participante intermediário. Ambos não podem estar definidos ao mesmo tempo.

Tipo de criptografia de camada: 0 para AES (como nos túneis atuais); 1 para futuro (ChaCha?)

A expiração da solicitação é para duração variável de tunnel no futuro. Por enquanto, o único valor suportado é 600 (10 minutos).

A chave pública efêmera do criador é uma chave ECIES, big-endian. É usada para o KDF para a camada IBGW e chaves e IVs de resposta. Isso é incluído apenas no registro de texto simples em uma mensagem Inbound Tunnel Build. É necessário porque não há DH nesta camada para o registro de construção.

As opções de construção de tunnel são uma estrutura de Mapping conforme definido em [Common](/docs/specs/common-structures/). As únicas opções atualmente definidas são para parâmetros de largura de banda, a partir da API 0.9.65, veja abaixo para detalhes. Se a estrutura de Mapping estiver vazia, são dois bytes 0x00 0x00. O tamanho máximo do Mapping (incluindo o campo de comprimento) é 98 bytes, e o valor máximo do campo de comprimento do Mapping é 96.

#### Registro de Solicitação Curta Criptografado

Todos os campos estão em big-endian, exceto a chave pública efêmera que está em little-endian.

Tamanho criptografado: 218 bytes

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
<thead>
<tr>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Bytes</th>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contents</th>
</tr>
</thead>
<tbody>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">0-15</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Hop's truncated identity hash</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">16-47</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Sender's ephemeral X25519 public key</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">48-201</td><td style="border:1px solid var(--color-border); padding:0.6rem;">ChaCha20 encrypted ShortBuildRequestRecord</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">202-217</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Poly1305 MAC</td></tr>
</tbody>
</table>
### Registros de Resposta de Construção Curta

BuildReplyRecords criptografados curtos têm 218 bytes.

#### Registro de Resposta Curta Não Criptografado

Resumo das alterações dos registros longos:

- Alterar comprimento não criptografado de 512 para 202 bytes
- Alterar comprimento criptografado de 528 para 218 bytes

As respostas ECIES são criptografadas com ChaCha20/Poly1305.

Todos os campos estão em big-endian.

Tamanho não criptografado: 202 bytes.

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
<thead>
<tr>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Bytes</th>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contents</th>
</tr>
</thead>
<tbody>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">0-x</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Tunnel Build Reply Options (Mapping)</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">x-x</td><td style="border:1px solid var(--color-border); padding:0.6rem;">other data as implied by options</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">x-200</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Random padding (see below)</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">201</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Reply byte</td></tr>
</tbody>
</table>
As opções de resposta de construção de tunnel são uma estrutura Mapping conforme definido em [Common](/docs/specs/common-structures/). As únicas opções atualmente definidas são para parâmetros de largura de banda, a partir da API 0.9.65, veja abaixo para detalhes. Se a estrutura Mapping estiver vazia, isso são dois bytes 0x00 0x00. O tamanho máximo do Mapping (incluindo o campo de comprimento) é 201 bytes, e o valor máximo do campo de comprimento do Mapping é 199.

O byte de resposta é um dos seguintes valores conforme definido em [Tunnel-Creation](/docs/specs/tunnel-creation/) para evitar fingerprinting:

- 0x00 (aceitar)
- 30 (TUNNEL_REJECT_BANDWIDTH)

Um valor de resposta adicional pode ser definido no futuro para representar rejeição para opções não suportadas.

#### Registro de Resposta Curta Criptografado

Tamanho criptografado: 218 bytes

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
<thead>
<tr>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Bytes</th>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contents</th>
</tr>
</thead>
<tbody>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">0-201</td><td style="border:1px solid var(--color-border); padding:0.6rem;">ChaCha20 encrypted ShortBuildReplyRecord</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">202-217</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Poly1305 MAC</td></tr>
</tbody>
</table>
### KDF

Usamos a chave de encadeamento (ck) do estado Noise após a criptografia/descriptografia do registro de construção do tunnel para derivar as seguintes chaves: chave de resposta, chave da camada AES, chave IV AES e chave/tag de resposta garlic para o OBEP.

Chaves de resposta: Note que o KDF é ligeiramente diferente para os hops OBEP e não-OBEP. Ao contrário dos registros longos, não podemos usar a parte esquerda do ck para a chave de resposta, porque não é o último e será usado posteriormente. A chave de resposta é usada para criptografar a resposta desse registro usando AEAD/ChaCha20/Poly1305 e ChaCha20 para responder outros registros. Ambos usam a mesma chave. O nonce é a posição do registro na mensagem começando do 0. Veja abaixo para detalhes.

```
keydata = HKDF(ck, ZEROLEN, "SMTunnelReplyKey", 64)
replyKey = keydata[32:63]
ck = keydata[0:31]

AES Layer key:
keydata = HKDF(ck, ZEROLEN, "SMTunnelLayerKey", 64)
layerKey = keydata[32:63]

IV key for non-OBEP record:
ivKey = keydata[0:31]
because it's last

IV key for OBEP record:
ck = keydata[0:31]
keydata = HKDF(ck, ZEROLEN, "TunnelLayerIVKey", 64)
ivKey = keydata[32:63]
ck = keydata[0:31]

OBEP garlic reply key/tag:
keydata = HKDF(ck, ZEROLEN, "RGarlicKeyAndTag", 64)
garlicReplyKey = keydata[32:63]
garlicReplyTag = keydata[0:7]
```
Nota: O KDF para a chave IV no OBEP é diferente daquele para os outros saltos, mesmo se a resposta não estiver criptografada com garlic encryption.

#### Criptografia de Registros

O registro de resposta do próprio hop é criptografado com ChaCha20/Poly1305. Isso é o mesmo que para a especificação de registro longo acima, EXCETO que 'n' é o número do registro 0-7, em vez de sempre ser 0. Veja [RFC-7539](https://tools.ietf.org/html/rfc7539).

```
// AEAD parameters
k = replyKey from KDF above
n = record number 0-7
plaintext = 202 byte build reply record
ad = h from build request

ciphertext = ENCRYPT(k, n, plaintext, ad)
```
Os outros registros são iterativamente e simetricamente criptografados em cada salto com ChaCha20 (NÃO ChaCha20/Poly1305). Isso é diferente da especificação de registro longo acima, que usa AES e não utiliza o número do registro.

O número do registro é colocado no IV no byte 4, porque o ChaCha20 usa um IV de 12 bytes com um nonce little-endian nos bytes 4-11. Veja [RFC-7539](https://tools.ietf.org/html/rfc7539).

```
// Parameters
k = replyKey from KDF above
n = record number 0-7
iv = 12 bytes, all zeros except iv[4] = n
plaintext = 218 byte encrypted record

ciphertext = ENCRYPT(k, iv, plaintext)
```
#### Garlic Encryption

O encapsulamento garlic das mensagens as oculta do OBEP (para uma construção de entrada) ou do IBGW (para uma construção de saída). Isso é recomendado mas não obrigatório. Se o OBEP e IBGW forem o mesmo router, não é necessário.

Garlic encryption de uma mensagem inbound Short Tunnel Build Message, pelo criador, criptografada para o ECIES IBGW, usa criptografia Noise 'N', conforme definido em [ECIES-ROUTERS](/docs/specs/ecies-routers/).

Garlic encryption de uma Mensagem de Resposta de Construção de Tunnel de Saída, pelo OBEP, criptografada para o criador, usa mensagens de Sessão Existente com a chave de resposta garlic de 32 bytes e a tag de resposta garlic de 8 bytes do KDF acima. O formato é conforme especificado para respostas a Consultas de Banco de Dados em [I2NP](/docs/specs/i2np/), [ECIES-ROUTERS](/docs/specs/ecies-routers/), e [ECIES-X25519](/docs/specs/ecies/).

#### Criptografia de Camada

Esta especificação inclui um campo de tipo de criptografia de camada no registro de solicitação de construção. O único tipo de criptografia de camada atualmente suportado é o tipo 0, que é AES. Isso não mudou em relação às especificações anteriores, exceto que a chave de camada e a chave IV são derivadas do KDF acima em vez de serem incluídas no registro de solicitação de construção.

Adicionar novos tipos de criptografia de camada, por exemplo ChaCha20, é um tópico para pesquisa adicional, e atualmente não faz parte desta especificação.

## Notas de Implementação

- Routers mais antigos não verificam o tipo de criptografia do salto e enviarão registros criptografados com ElGamal. Alguns routers recentes têm bugs e enviarão vários tipos de registros malformados. Os implementadores devem detectar e rejeitar esses registros antes da operação DH, se possível, para reduzir o uso da CPU.

### Registros de Construção

A ordem dos registros de construção deve ser randomizada, para que os hops intermediários não saibam sua localização dentro do tunnel.

O número mínimo recomendado de registros de construção é 4. Se houver mais registros de construção do que saltos, registros "falsos" devem ser adicionados, contendo dados aleatórios ou específicos da implementação. Para construções de tunnel de entrada, deve sempre haver um registro "falso" para o router de origem, com o prefixo hash de 16 bytes correto e uma chave efêmera X25519 real, caso contrário o salto mais próximo saberá que o próximo salto é o originador.

O restante do registro "falso" pode ser dados aleatórios, ou pode estar criptografado em qualquer formato para que o originador envie dados para si mesmo sobre a construção, talvez para reduzir os requisitos de armazenamento para construções pendentes.

Os originadores de tunnels de entrada devem usar algum método para validar que seu registro "falso" não foi modificado pelo hop anterior, pois isso também pode ser usado para desanonimização. O originador pode armazenar e verificar um checksum do registro, ou incluir o checksum no registro, ou usar uma função de criptografia/descriptografia AEAD, dependendo da implementação. Se o prefixo hash de 16 bytes ou outros conteúdos do registro de construção foram modificados, o router deve descartar o tunnel.

Registros falsos para túneis de saída, e registros falsos adicionais para túneis de entrada, não têm esses requisitos, e podem ser dados completamente aleatórios, já que nunca serão visíveis para nenhum hop. Ainda pode ser desejável para o originador validar que não foram modificados.

## Parâmetros de Largura de Banda do Tunnel

### Visão Geral

À medida que aumentamos o desempenho da rede ao longo dos últimos anos com novos protocolos, tipos de criptografia e melhorias no controle de congestionamento, aplicações mais rápidas como streaming de vídeo estão se tornando possíveis. Essas aplicações requerem alta largura de banda em cada salto em seus tunnels cliente.

Os routers participantes, no entanto, não têm qualquer informação sobre quanta largura de banda um tunnel irá usar quando recebem uma mensagem de construção de tunnel. Eles só podem aceitar ou rejeitar um tunnel com base na largura de banda total atual usada por todos os tunnels participantes e no limite total de largura de banda para tunnels participantes.

Os routers solicitantes também não têm qualquer informação sobre quanta largura de banda está disponível em cada salto.

Além disso, os routers atualmente não têm como limitar o tráfego de entrada em um tunnel. Isso seria bastante útil durante períodos de sobrecarga ou ataques DDoS a um serviço.

Os parâmetros de largura de banda do tunnel nas mensagens de solicitação e resposta de construção do tunnel adicionam suporte para essas funcionalidades. Consulte [Prop168](/proposals/168/) para informações adicionais. Esses parâmetros são definidos a partir da API 0.9.65, mas o suporte pode variar por implementação. Eles são suportados tanto para registros de construção ECIES longos quanto curtos.

### Opções de Solicitação de Construção

As três opções seguintes podem ser definidas no campo de mapeamento de opções de construção de tunnel do registro: Um router solicitante pode incluir qualquer uma, todas ou nenhuma.

- m := largura de banda mínima necessária para este tunnel (KBps inteiro positivo como string)
- r := largura de banda solicitada para este tunnel (KBps inteiro positivo como string)
- l := largura de banda limite para este tunnel; enviado apenas para IBGW (KBps inteiro positivo como string)

Restrição: m <= r <= l

O router participante deve rejeitar o tunnel se "m" for especificado e não conseguir fornecer pelo menos essa quantidade de largura de banda.

As opções de solicitação são enviadas para cada participante no registro de solicitação de construção criptografado correspondente, e não são visíveis para outros participantes.

### Opção de Resposta de Construção

A seguinte opção pode ser definida no campo de mapeamento de opções da resposta de construção do tunnel do registro, quando a resposta é ACCEPTED:

- b := largura de banda disponível para este tunnel (número inteiro positivo em KBps como string)

Restrição: b >= m

O router participante deve incluir isso se "m" ou "r" foi especificado na solicitação de construção. O valor deve ser pelo menos o do valor "m" se especificado, mas pode ser menor ou maior que o valor "r" se especificado.

O router participante deve tentar reservar e fornecer pelo menos essa quantidade de largura de banda para o tunnel, porém isso não é garantido. Os routers não podem prever condições 10 minutos no futuro, e o tráfego participante tem prioridade menor que o próprio tráfego e tunnels do router.

Os routers também podem alocar mais largura de banda do que a disponível, se necessário, e isso é provavelmente desejável, já que outros saltos no tunnel podem rejeitá-lo.

Por estas razões, a resposta do router participante deve ser tratada como um compromisso de melhor esforço, mas não uma garantia.

As opções de resposta são enviadas ao router solicitante no registro de resposta de construção criptografado correspondente, e não são visíveis para outros participantes.

### Notas de Implementação

Os parâmetros de largura de banda são vistos nos routers participantes na camada do tunnel, ou seja, o número de mensagens de tunnel de tamanho fixo de 1 KB por segundo. A sobrecarga de transporte (NTCP2 ou SSU2) não está incluída.

Esta largura de banda pode ser muito maior ou menor que a largura de banda vista no cliente. As mensagens de tunnel contêm uma sobrecarga substancial, incluindo sobrecarga de camadas superiores incluindo ratchet e streaming. Mensagens pequenas intermitentes, como acks de streaming, serão expandidas para 1 KB cada. No entanto, a compressão gzip na camada I2CP pode reduzir substancialmente a largura de banda.

A implementação mais simples no router solicitante é usar as larguras de banda média, mínima e/ou máxima dos tunnels atuais no pool para calcular os valores a serem colocados na solicitação. Algoritmos mais complexos são possíveis e ficam a critério do implementador.

Não há opções I2CP ou SAM atuais definidas para o cliente informar ao router qual largura de banda é necessária, e nenhuma nova opção é proposta aqui. Opções podem ser definidas posteriormente se necessário.

As implementações podem usar a largura de banda disponível ou quaisquer outros dados, algoritmo, política local ou configuração local para calcular o valor de largura de banda retornado na resposta de construção.

## Referências

- [Comum](/docs/specs/common-structures/)
- [Criptografia](/docs/specs/cryptography/)
- [ECIES-ROUTERS](/docs/specs/ecies-routers/)
- [ECIES-X25519](/docs/specs/ecies/)
- [EncryptedLeaseSet](/docs/specs/encryptedleaseset/)
- [I2NP](/docs/specs/i2np/)
- [Criptografia Múltipla](https://en.wikipedia.org/wiki/Multiple_encryption)
- [NOISE](https://noiseprotocol.org/noise.html)
- [NTCP2](/docs/specs/ntcp2/)
- [Prop119](/proposals/119/)
- [Prop143](/proposals/143/)
- [Prop152](/proposals/152/)
- [Prop153](/proposals/153/)
- [Prop156](/proposals/156/)
- [Prop157](/proposals/157/)
- [Prop168](/proposals/168/)
- [RFC-7539](https://tools.ietf.org/html/rfc7539)
- [RFC-7748](https://tools.ietf.org/html/rfc7748)
- [Criação de Tunnel](/docs/specs/tunnel-creation/)
