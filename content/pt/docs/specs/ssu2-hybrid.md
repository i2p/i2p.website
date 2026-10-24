---
title: "PQ Hybrid SSU2"
description: "Variante híbrida pós-quântica do protocolo de transporte SSU2 usando ML-KEM"
slug: "ssu2-hybrid"
lastupdated: "2026-10"
category: "Transportes"
accurateFor: "0.9.71"
---

### Status

Beta Q2 2026, lançamento Q3 2026

## Visão Geral

Esta é a variante híbrida pós-quântica do protocolo de transporte SSU2, conforme projetado na Proposta 169. Consulte essa proposta para informações adicionais.

O PQ Hybrid SSU2 é definido apenas no mesmo endereço e porta que o SSU2 padrão. A operação em uma porta diferente, ou sem suporte ao SSU2 padrão, não é permitida, e não o será por vários anos, até que o SSU2 padrão seja descontinuado.

Esta especificação documenta apenas as alterações necessárias ao SSU2 padrão para suportar PQ Hybrid. Consulte a especificação SSU2 para os detalhes de implementação da linha de base.

## Design

Suportamos os padrões NIST FIPS 203 e 204 [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf) [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf) que são baseados em, mas NÃO compatíveis com, CRYSTALS-Kyber e CRYSTALS-Dilithium (versões 3.1, 3 e anteriores).

### Troca de Chaves

PQ KEM fornece apenas chaves efêmeras e não suporta diretamente handshakes de chave estática, como Noise XK e IK. Os tipos de criptografia são os mesmos utilizados no PQ Hybrid Ratchet e estão definidos no documento de estruturas comuns [/docs/specs/common-structures/](/docs/specs/common-structures/), como em [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf), os tipos Híbridos são definidos apenas em combinação com X25519.

Os tipos de criptografia são:

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Type</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Code</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">SSU2 Version</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM512_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">3</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM768_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">6</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">4</td>
</tr>
</table>
### Combinações Legais

Os novos tipos de criptografia são indicados nos RouterAddresses. O tipo de criptografia no certificado de chave continuará sendo o tipo 4.

## Especificação

### Padrões de Handshake

Os handshakes utilizam padrões de handshake do [Protocolo Noise](https://noiseprotocol.org/noise.html).

O seguinte mapeamento de letras é utilizado:

- e = chave efêmera de uso único
- s = chave estática
- p = carga útil da mensagem
- e1 = chave PQ efêmera de uso único, enviada de Alice para Bob
- ekem1 = o texto cifrado KEM, enviado de Bob para Alice

As seguintes modificações em XK e IK para sigilo encaminhado híbrido (hfs) são especificadas conforme a seção 5 da [especificação Noise HFS](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf):

```
XK:                       XKhfs:
  <- s                      <- s
  ...                       ...
  -> e, es, p               -> e, es, e1, p
  <- e, ee, p               <- e, ee, ekem1, p
  -> s, se                  -> s, se
  <- p                      <- p
  p ->                      p ->


  e1 and ekem1 are encrypted. See pattern definitions below.
  NOTE: e1 and ekem1 are different sizes (unlike X25519)
```
O padrão e1 é definido da seguinte forma, conforme especificado na seção 4 do [Noise HFS spec](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf):

```
For Alice:
  (encap_key, decap_key) = PQ_KEYGEN()

  // EncryptAndHash(encap_key)
  ciphertext = ENCRYPT(k, n, encap_key, ad)
  n++
  MixHash(ciphertext)

  For Bob:

  // DecryptAndHash(ciphertext)
  encap_key = DECRYPT(k, n, ciphertext, ad)
  n++
  MixHash(ciphertext)
```
O padrão ekem1 é definido da seguinte forma, conforme especificado na seção 4 do [Noise HFS spec](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf):

```
For Bob:

  (kem_ciphertext, kem_shared_key) = ENCAPS(encap_key)

  // EncryptAndHash(kem_ciphertext)
  ciphertext = ENCRYPT(k, n, kem_ciphertext, ad)
  MixHash(ciphertext)

  // MixKey
  MixKey(kem_shared_key)


  For Alice:

  // DecryptAndHash(ciphertext)
  kem_ciphertext = DECRYPT(k, n, ciphertext, ad)
  MixHash(ciphertext)

  // MixKey
  kem_shared_key = DECAPS(kem_ciphertext, decap_key)
  MixKey(kem_shared_key)
```
### KDF do Handshake Noise

#### Visão Geral

O handshake híbrido é definido na [especificação Noise HFS](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf). A primeira mensagem, de Alice para Bob, contém e1, a chave de encapsulamento, antes do payload da mensagem. Isso é tratado como uma chave estática adicional; chame EncryptAndHash() sobre ela (como Alice) ou DecryptAndHash() (como Bob). Em seguida, processe o payload da mensagem normalmente.

A segunda mensagem, de Bob para Alice, contém ekem1, o texto cifrado, antes do payload da mensagem. Isso é tratado como uma chave estática adicional; chame EncryptAndHash() sobre ela (como Bob) ou DecryptAndHash() (como Alice). Em seguida, calcule o kem_shared_key e chame MixKey(kem_shared_key). Depois, processe o payload da mensagem normalmente.

#### Operações ML-KEM Definidas

Definimos as seguintes funções correspondentes aos blocos de construção criptográficos utilizados conforme definido em [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf).

(encap_key, decap_key) = PQ_KEYGEN()

    Alice creates the encapsulation and decapsulation keys
    The encapsulation key is sent in message 1.
    encap_key and decap_key sizes vary based on ML-KEM variant.

(ciphertext, kem_shared_key) = ENCAPS(encap_key)

    Bob calculates the ciphertext and shared key,
    using the ciphertext received in message 1.
    The ciphertext is sent in message 2.
    ciphertext size varies based on ML-KEM variant.
    The kem_shared_key is always 32 bytes.

kem_shared_key = DECAPS(ciphertext, decap_key)

    Alice calculates the shared key,
    using the ciphertext received in message 2.
    The kem_shared_key is always 32 bytes.

Note que tanto o encap_key quanto o ciphertext são cifrados dentro de blocos ChaCha/Poly nas mensagens de handshake Noise 1 e 2. Eles serão decifrados como parte do processo de handshake.

O kem_shared_key é misturado na chave de encadeamento com MixHash(). Veja abaixo para mais detalhes.

#### KDF de Alice para a Mensagem 1

Após o padrão de mensagem 'es' e antes do payload, adicione:

```
This is the "e1" message pattern:
  (encap_key, decap_key) = PQ_KEYGEN()

  // EncryptAndHash(encap_key)
  // AEAD parameters
  k = keydata[32:63]
  n = 0
  ad = h
  ciphertext = ENCRYPT(k, n, encap_key, ad)
  n++

  // MixHash(ciphertext)
  h = SHA256(h || ciphertext)


  End of "e1" message pattern.

  NOTE: For the next section (payload for XK or static key for IK),
  the keydata and chain key remain the same,
  and n now equals 1 (instead of 0 for non-hybrid).
```
#### KDF de Bob para a Mensagem 1

Após o padrão de mensagem 'es' e antes do payload, adicione:

```
This is the "e1" message pattern:

  // DecryptAndHash(encap_key_section)
  // AEAD parameters
  k = keydata[32:63]
  n = 0
  ad = h
  encap_key = DECRYPT(k, n, encap_key_section, ad)
  n++

  // MixHash(encap_key_section)
  h = SHA256(h || encap_key_section)

  End of "e1" message pattern.

  NOTE: For the next section (payload for XK or static key for IK),
  the keydata and chain key remain the same,
  and n now equals 1 (instead of 0 for non-hybrid).
```
#### KDF de Bob para Mensagem 2

Para XK: Após o padrão de mensagem 'ee' e antes do payload, adicione:

```
This is the "ekem1" message pattern:

  (kem_ciphertext, kem_shared_key) = ENCAPS(encap_key)

  // EncryptAndHash(kem_ciphertext)
  // AEAD parameters
  k = keydata[32:63]
  n = 0
  ad = h
  ciphertext = ENCRYPT(k, n, kem_ciphertext, ad)

  // MixHash(ciphertext)
  h = SHA256(h || ciphertext)

  // MixKey(kem_shared_key)
  keydata = HKDF(chainKey, kem_shared_key, "", 64)
  chainKey = keydata[0:31]

  End of "ekem1" message pattern.

  // AEAD parameters for payload section
  ... as in standard SSU2 ...
  k = keydata[32:63]
  ...

```
#### KDF de Alice para a Mensagem 2

Após o padrão de mensagem 'ee', adicione:

```
This is the "ekem1" message pattern:

  // DecryptAndHash(kem_ciphertext_section)
  // AEAD parameters
  k = keydata[32:63]
  n = 0
  ad = h
  kem_ciphertext = DECRYPT(k, n, kem_ciphertext_section, ad)

  // MixHash(kem_ciphertext_section)
  h = SHA256(h || kem_ciphertext_section)

  // MixKey(kem_shared_key)
  kem_shared_key = DECAPS(kem_ciphertext, decap_key)
  keydata = HKDF(chainKey, kem_shared_key, "", 64)
  chainKey = keydata[0:31]

  End of "ekem1" message pattern.

  // AEAD parameters for payload section
  ... as in standard SSU2 ...
  k = keydata[32:63]
  ...

```
#### KDF para Mensagem 3

inalterado

#### KDF para split()

inalterado

### Detalhes do Handshake

#### Identificadores Noise

- "Noise_XKhfschaobfse+hs1+hs2+hs3_25519+MLKEM512_ChaChaPoly_SHA256"
- "Noise_XKhfschaobfse+hs1+hs2+hs3_25519+MLKEM768_ChaChaPoly_SHA256"

Note que MLKEM-1024 NÃO é suportado para SSU2, pois as chaves são grandes demais para caber em um datagrama padrão de 1500 bytes.

#### Cabeçalho Longo

O cabeçalho longo tem 32 bytes. É utilizado antes de uma sessão ser criada, para Token Request, SessionRequest, SessionCreated e Retry. Também é utilizado para mensagens Peer Test e Hole Punch fora de sessão.

Nas seguintes mensagens, defina o campo ver (versão) no cabeçalho longo como 3 ou 4, para indicar MLKEM-512 ou MLKEM-768.

- (0) Solicitação de Sessão
- (1) Sessão Criada
- (9) Tentar Novamente
- (10) Solicitação de Token
- (11) Hole Punch

Nas mensagens a seguir, defina o campo ver (versão) no cabeçalho longo como 2, como de costume, mesmo que MLKEM-512 ou MLKEM-768 seja suportado. As implementações também podem definir o valor como 3 ou 4, se a outra extremidade suportar, mas isso não é necessário. As implementações devem aceitar qualquer valor de 2 a 4.

- (7) Teste de Par (mensagens fora de sessão 5-7)

Discussão: Definir o campo de versão como 3 ou 4 pode não ser estritamente necessário para todos os tipos de mensagem, mas fazê-lo auxilia na detecção precoce de falhas em conexões pós-quânticas não suportadas. Mensagens Token Request e Retry (tipos 9 e 10) devem ter as versões 3/4 por consistência. Mensagens Hole Punch (tipo 11) podem não exigir esse tratamento, mas seguiremos o mesmo padrão por uniformidade. Mensagens Peer Test (tipo 7) estão fora de sessão e não indicam intenção de iniciar uma sessão.

- Solicitação de Relay
- Resposta de Relay
- Introdução de Relay
- Teste de Par

Antes da criptografia do cabeçalho:

Antes da criptografia do cabeçalho:

```

  +----+----+----+----+----+----+----+----+
  |      Destination Connection ID        |
  +----+----+----+----+----+----+----+----+
  |   Packet Number   |type| ver| id |flag|
  +----+----+----+----+----+----+----+----+
  |        Source Connection ID           |
  +----+----+----+----+----+----+----+----+
  |                 Token                 |
  +----+----+----+----+----+----+----+----+

  Destination Connection ID :: 8 bytes, unsigned big endian integer

  Packet Number :: 4 bytes, unsigned big endian integer

  type :: The message type = 0, 1, 7, 9, 10, or 11

  ver :: The protocol version = 2, 3, or 4 for non-PQ, MLKEM512, MLKEM768

  id :: 1 byte, the network ID (currently 2, except for test networks)

  flag :: 1 byte, unused, set to 0 for future compatibility

  Source Connection ID :: 8 bytes, unsigned big endian integer

  Token :: 8 bytes, unsigned big endian integer

```
#### Cabeçalho Curto

inalterado

#### SessionRequest (Tipo 0)

Alterações: O SSU2 atual contém apenas os dados do bloco na seção ChaCha. Com ML-KEM, a seção ChaCha também conterá a chave pública PQ criptografada.

Mudança no KDF para Proteção contra Spoofing: Para resolver os problemas levantados na Proposta 165 [Prop165]_, mas com uma solução diferente, modificamos o KDF para Session Request. Isso se aplica apenas a sessões PQ. O KDF para sessões não-PQ permanece inalterado.

```

// End of KDF for initial chain key (unchanged)
  // Bob static key
  // MixHash(bpk)
  h = SHA256(h || bpk);

  // Start of KDF for session request
  // NEW for PQ only
  // bhash = Bob router hash (32 bytes)
  // MixHash(bhash)
  h = SHA256(h || bhash);

  // Rest of KDF for session request, unchanged, as in SSU2 spec
  // MixHash(header)
  h = SHA256(h || header)

  ...

```
Conteúdo bruto:

```
  +----+----+----+----+----+----+----+----+
  |  Long Header bytes 0-15, ChaCha20     |
  +  encrypted with Bob intro key         +
  |    See Header Encryption KDF          |
  +----+----+----+----+----+----+----+----+
  |  Long Header bytes 16-31, ChaCha20    |
  +  encrypted with Bob intro key n=0     +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +       X, ChaCha20 encrypted           +
  |       with Bob intro key n=0          |
  +              (32 bytes)               +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |   ChaCha20 encrypted data (MLKEM)     |
  +          (length varies)              +
  |  k defined in KDF for Session Request |
  +  n = 0                                +
  |  see KDF for associated data          |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +        Poly1305 MAC (16 bytes)        +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |   ChaCha20 encrypted data (payload)   |
  +          (length varies)              +
  |  k defined in KDF for Session Request |
  +  n = 1                                +
  |  see KDF for associated data          |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +        Poly1305 MAC (16 bytes)        +
  |                                       |
  +----+----+----+----+----+----+----+----+


```
Dados não criptografados (tag de autenticação Poly1305 não exibida):

```
  +----+----+----+----+----+----+----+----+
  |      Destination Connection ID        |
  +----+----+----+----+----+----+----+----+
  |   Packet Number   |type| ver| id |flag|
  +----+----+----+----+----+----+----+----+
  |        Source Connection ID           |
  +----+----+----+----+----+----+----+----+
  |                 Token                 |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |                   X                   |
  +              (32 bytes)               +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |           ML-KEM encap_key            |
  +      (see table below for length)     +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |     Noise payload (block data)        |
  +          (length varies)              +
  |     see below for allowed blocks      |
  +----+----+----+----+----+----+----+----+
```
Tamanhos, sem incluir a sobrecarga de IP:

| Tipo | Código do Tipo | Comprimento X | Comprimento Msg 1 | Comprimento Enc Msg 1 | Comprimento Dec Msg 1 | Comprimento chave PQ | Comprimento pl |
|------|----------------|---------------|-------------------|-----------------------|-----------------------|----------------------|----------------|
| X25519 | 4 | 32 | 80+pl | 16+pl | pl | -- | pl |
| MLKEM512_X25519 | 5 | 32 | 896+pl | 832+pl | 800+pl | 800 | pl |
| MLKEM768_X25519 | 6 | 32 | 1280+pl | 1216+pl | 1184+pl | 1184 | pl |
| MLKEM1024_X25519 | 7 | n/a | muito grande | | | | |
Nota: Os códigos de tipo são apenas para uso interno. Os routers permanecerão do tipo 4, e o suporte será indicado nos endereços do router.

MTU mínimo para MLKEM768_X25519: 1318 para IPv4 e 1338 para IPv6. Veja abaixo.

Alterações: o SSU2 atual contém apenas o payload em uma única seção ChaCha. Com o ML-KEM, haverá uma nova seção ChaCha antes do payload, contendo o ciphertext PQ criptografado.

#### SessionCreated (Tipo 1)

Alterações: o SSU2 atual contém apenas o payload em uma única seção ChaCha. Com o ML-KEM, haverá uma nova seção ChaCha antes do payload, contendo o ciphertext PQ criptografado.

Conteúdo bruto:

```
  +----+----+----+----+----+----+----+----+
  |  Long Header bytes 0-15, ChaCha20     |
  +  encrypted with Bob intro key and     +
  | derived key, see Header Encryption KDF|
  +----+----+----+----+----+----+----+----+
  |  Long Header bytes 16-31, ChaCha20    |
  +  encrypted with derived key n=0       +
  |  See Header Encryption KDF            |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +       Y, ChaCha20 encrypted           +
  |       with derived key n=0            |
  +              (32 bytes)               +
  |       See Header Encryption KDF       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |   ChaCha20 data (MLKEM)               |
  +   Encrypted and authenticated data    +
  |  length varies                        |
  +  k defined in KDF for Session Created +
  |  (before mixKey)                      |
  +  n = 0; see KDF for associated data   +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +        Poly1305 MAC (16 bytes)        +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |   ChaCha20 data (payload)             |
  +   Encrypted and authenticated data    +
  |  length varies                        |
  +  k defined in KDF for Session Created +
  |  (after mixKey)                       |
  +  n = 0; see KDF for associated data   +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +        Poly1305 MAC (16 bytes)        +
  |                                       |
  +----+----+----+----+----+----+----+----+


```
Dados não criptografados (tag de autenticação Poly1305 não exibida):

```
  +----+----+----+----+----+----+----+----+
  |      Destination Connection ID        |
  +----+----+----+----+----+----+----+----+
  |   Packet Number   |type| ver| id |flag|
  +----+----+----+----+----+----+----+----+
  |        Source Connection ID           |
  +----+----+----+----+----+----+----+----+
  |                 Token                 |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |                  Y                    |
  +              (32 bytes)               +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |           ML-KEM Ciphertext           |
  +      (see table below for length)     +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |     Noise payload (block data)        |
  +          (length varies)              +
  |      see below for allowed blocks     |
  +----+----+----+----+----+----+----+----+
```
Tamanhos, sem incluir a sobrecarga de IP:

| Tipo | Código do Tipo | len Y | len Msg 2 | len Msg 2 Enc | len Msg 2 Dec | len PQ CT | len pl |
|------|-----------|-------|-----------|---------------|---------------|-----------|--------|
| X25519 | 4 | 32 | 80+pl | 16+pl | pl | -- | pl |
| MLKEM512_X25519 | 5 | 32 | 864+pl | 800+pl | 768+pl | 768 | pl |
| MLKEM768_X25519 | 6 | 32 | 1184+pl | 1120+pl | 1088+pl | 1088 | pl |
| MLKEM1024_X25519 | 7 | n/a | muito grande | | | | |
Nota: Os códigos de tipo são apenas para uso interno. Os routers permanecerão do tipo 4, e o suporte será indicado nos endereços do router.

MTU mínimo para MLKEM768_X25519: 1318 para IPv4 e 1338 para IPv6. Veja abaixo.

Tamanho máximo: Alice ainda não possui o RouterInfo de Bob e não conhece seu MTU publicado. Para esta mensagem, utilize um MTU temporário da seguinte forma. Para MLKEM512_X25519, use o maior valor entre 1280 ou o tamanho do SessionRequest recebido como MTU. Para MLKEM768_X25519, use o maior valor entre (1318 para IPv4 ou 1338 para IPv6) ou o tamanho do SessionRequest recebido como MTU. A sobrecarga do SessionCreated é menor que a do SessionRequest, porque o texto cifrado MLKEM é menor que a chave pública MLKEM. Isso permite uma variedade de tamanhos de preenchimento no SessionCreated, mesmo que tenha havido pouco ou nenhum preenchimento no SessionRequest.

#### SessionConfirmed (Tipo 2)

inalterado

#### KDF para a fase de dados

inalterado

#### Relay e Teste de Pares

Os seguintes blocos contêm campos de versão. Eles permanecerão na versão 2 (para compatibilidade com um Bob não-PQ) e não serão alterados para a versão 3/4 para PQ.

* [CABFORUM](https://cabforum.org/2024/10/10/2024-10-10-minutes-of-the-code-signing-certificate-working-group/)
* [Choosing-Hash](https://kerkour.com/fast-secure-hash-function-sha256-sha512-sha3-blake3)
* [CLOUDFLARE](https://blog.cloudflare.com/pq-2024/)
* [COMMON](/docs/specs/common-structures/)
* [COMPOSITE-SIGS](https://datatracker.ietf.org/doc/draft-ietf-lamps-pq-composite-sigs/)
* [ECIES](/docs/specs/ecies/)
* [FORUM](http://zzz.i2p/topics/3294)
* [FIPS202](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.202.pdf)
* [FIPS203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf)
* [FIPS204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf)
* [FIPS205](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.205.pdf)
* [MLDSA-OIDS](https://datatracker.ietf.org/doc/draft-ietf-lamps-dilithium-certificates/)
* [NIST-PQ](https://www.nist.gov/news-events/news/2024/08/nist-releases-first-3-finalized-post-quantum-encryption-standards)
* [NIST-PQ-UPDATE](https://csrc.nist.gov/csrc/media/Presentations/2022/update-on-post-quantum-encryption-and-cryptographi/Day%202%20-%20230pm%20Chen%20PQC%20ISPAB.pdf)
* [NIST-PQ-END](https://www.nccoe.nist.gov/sites/default/files/2023-08/pqc-light-at-the-end-of-the-tunnel-presentation.pdf)
* [NIST-VECTORS](https://csrc.nist.gov/projects/cryptographic-standards-and-guidelines/example-values)
* [Noise](https://noiseprotocol.org/noise.html)
* [Noise-Hybrid](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf)
* [NSA-PQ](https://media.defense.gov/2022/Sep/07/2003071836/-1/-1/0/CSI_CNSA_2.0_FAQ_.PDF)
* [NTCP2](/docs/specs/ntcp2/)
* [OPENSSL](https://openssl-library.org/post/2025-02-04-release-announcement-3.5/)
* [Prop165](/docs/proposals/165/)
* [PQ-WIREGUARD](https://eprint.iacr.org/2020/379.pdf)
* [RFC-2104](https://tools.ietf.org/html/rfc2104)
* [Rosenpass](https://rosenpass.eu/)
* [Rosenpass-Whitepaper](https://raw.githubusercontent.com/rosenpass/rosenpass/papers-pdf/whitepaper.pdf)
* [SSH-HYBRID](https://datatracker.ietf.org/doc/draft-ietf-sshm-mlkem-hybrid-kex/)
* [SSU2](/docs/specs/ssu2/)
* [TLS-HYBRID](https://datatracker.ietf.org/doc/draft-ietf-tls-hybrid-design/)

#### Endereços Publicados

Em todos os casos, use o nome de transporte SSU2 como de costume. MLKEM-1024 não é suportado.

Use o mesmo endereço/porta que o não-PQ, sem firewall. Uma ou ambas as variantes PQ são suportadas. No endereço do router, publique v=2 (como de costume) e o novo parâmetro pq=[3|4|3,4|4,3] para indicar MLKEM 512/768/ambos. Routers com MTU inferior ao mínimo especificado abaixo não devem publicar um parâmetro "pq" contendo "4". Publique 4,3 para indicar preferência por MLKEM-768 ou 3,4 para indicar preferência por MLKEM-512. A versão efetiva fica a critério do iniciador, e a preferência pode não ser respeitada. Routers com MTU inferior ao mínimo especificado abaixo não devem conectar-se usando MLKEM768. Routers mais antigos ignorarão o parâmetro pq e conectar-se-ão sem PQ como de costume.

Endereço/porta diferente como não-PQ, ou somente PQ, sem firewall NÃO é suportado. Isso não será implementado até que o SSU2 não-PQ seja desativado, o que ocorrerá daqui a vários anos. Quando o não-PQ for desativado, uma ou ambas as variantes PQ serão suportadas. No endereço do router, publique v=[3|4|3,4|4,3] para indicar MLKEM 512/768/ambos. Routers mais antigos verificarão o parâmetro v e ignorarão este endereço por não ser suportado.

Endereços com firewall (sem IP publicado): No endereço do router, publicar v=2 (como de costume). O parâmetro pq DEVE ser publicado em endereços com firewall, para suportar relay (retransmissão).

Alice pode conectar-se a um Bob PQ usando a variante PQ que Bob publica, independentemente de Alice anunciar suporte a PQ em suas informações de router, ou se ela anuncia a mesma variante.

#### MTU

Tenha cuidado para não exceder o MTU com MLKEM768. O MTU mínimo para MLKEM768_X25519 é 1318 para IPv4 e 1338 para IPv6 (assumindo um payload mínimo de 10 bytes com um bloco DateTime e um bloco Padding ou RelayTagRequest). O MTU mínimo para SSU2 em geral é 1280, portanto nem todos os peers poderão usar MLKEM768. Não publique nem use MLKEM768 se o MTU real for inferior ao mínimo, seja localmente ou conforme anunciado pelo peer. Tome cuidado para não incluir um tamanho de padding tal que a mensagem 1 ou 2 exceda o MTU local ou remoto.

## Análise de Sobrecarga

### Troca de Chaves

Aumento de tamanho (bytes):

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Type</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Pubkey (Msg 1)</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Ciphertext (Msg 2)</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM512_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">+816</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">+784</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM768_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">+1200</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">+1104</td>
</tr>
</table>
## Análise de Segurança

As categorias de segurança do NIST são resumidas no [slide 10 da apresentação do NIST](https://www.nccoe.nist.gov/sites/default/files/2023-08/pqc-light-at-the-end-of-the-tunnel-presentation.pdf). Critérios preliminares: Nossa categoria mínima de segurança do NIST deve ser 2 para protocolos híbridos e 3 para protocolos somente PQ (pós-quânticos).

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Category</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">As Secure As</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">AES128</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">2</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">SHA256</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">3</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">AES192</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">4</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">SHA384</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">AES256</td>
</tr>
</table>
### Handshakes

Todos estes são protocolos híbridos. As implementações devem preferir MLKEM768; MLKEM512 não é suficientemente seguro.

Categorias de segurança NIST [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf):

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Algorithm</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Security Category</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM512</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM768</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">3</td>
</tr>
</table>
## Notas de Implementação

### Suporte de Biblioteca

As bibliotecas Bouncycastle, BoringSSL e WolfSSL já suportam MLKEM e MLDSA. O suporte do OpenSSL está previsto para a versão 3.5, lançada em 8 de abril de 2025 [OpenSSL](https://openssl-library.org/post/2025-02-04-release-announcement-3.5/).

### Identificação de Tráfego de Entrada

Definimos o MSB (bit mais significativo) da chave efêmera (key[31] & 0x80) na solicitação de sessão para indicar que esta é uma conexão híbrida. Isso nos permite executar tanto o NTCP padrão quanto o NTCP híbrido na mesma porta. Apenas uma variante híbrida é suportada para entrada (inbound) e anunciada no endereço do router. Por exemplo, pq=3 ou pq=4.

## Compatibilidade do Router

### Nomes de Transporte

Como Alice, para uma conexão PQ, antes da ofuscação, defina X[31] |= 0x80. Isso torna X uma chave pública X25519 inválida. Após a ofuscação, o AES-CBC irá aleatorizar. O MSB de X será aleatório após a ofuscação.

## Referências

* [CLOUDFLARE](https://blog.cloudflare.com/pq-2024/)
* [COMMON](/docs/specs/common-structures/)
* [ECIES](/docs/specs/ecies/)
* [FORUM](http://zzz.i2p/topics/3294)
* [FIPS202](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.202.pdf)
* [FIPS203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf)
* [NIST-PQ](https://www.nist.gov/news-events/news/2024/08/nist-releases-first-3-finalized-post-quantum-encryption-standards)
* [NIST-PQ-UPDATE](https://csrc.nist.gov/csrc/media/Presentations/2022/update-on-post-quantum-encryption-and-cryptographi/Day%202%20-%20230pm%20Chen%20PQC%20ISPAB.pdf)
* [NIST-PQ-END](https://www.nccoe.nist.gov/sites/default/files/2023-08/pqc-light-at-the-end-of-the-tunnel-presentation.pdf)
* [NIST-VECTORS](https://csrc.nist.gov/projects/cryptographic-standards-and-guidelines/example-values)
* [Noise](https://noiseprotocol.org/noise.html)
* [Noise-Hybrid](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf)
* [NSA-PQ](https://media.defense.gov/2022/Sep/07/2003071836/-1/-1/0/CSI_CNSA_2.0_FAQ_.PDF)
* [OPENSSL](https://openssl-library.org/post/2025-02-04-release-announcement-3.5/)
* [Prop165](/docs/proposals/165/)
* [PQ-WIREGUARD](https://eprint.iacr.org/2020/379.pdf)
* [RFC-2104](https://tools.ietf.org/html/rfc2104)
* [Rosenpass](https://rosenpass.eu/)
* [Rosenpass-Whitepaper](https://raw.githubusercontent.com/rosenpass/rosenpass/papers-pdf/whitepaper.pdf)
* [SSH-HYBRID](https://datatracker.ietf.org/doc/draft-ietf-sshm-mlkem-hybrid-kex/)
* [SSU2](/docs/specs/ssu2/)
* [TLS-HYBRID](https://datatracker.ietf.org/doc/draft-ietf-tls-hybrid-design/)
