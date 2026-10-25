---
title: "PQ Hybrid ECIES-X25519-AEAD-Ratchet"
description: "Variante híbrida pós-quântica do protocolo de criptografia ECIES usando ML-KEM"
slug: "ecies-hybrid"
category: "Protocolos"
lastUpdated: "2026-04"
accurateFor: "0.9.69"
---

## Nota

Implementação, testes e lançamento em andamento nas várias implementações de router. Verifique a documentação dessas implementações para obter o status.

## Visão Geral

Esta é a variante PQ Hybrid do protocolo ECIES-X25519-AEAD-Ratchet [ECIES](/docs/specs/ecies/). É a primeira fase da proposta geral PQ [Prop169](/proposals/169-pq-crypto/) a ser aprovada. Consulte essa proposta para objetivos gerais, modelos de ameaças, análise, alternativas e informações adicionais.

Esta especificação contém apenas as diferenças do [ECIES](/docs/specs/ecies/) padrão e deve ser lida em conjunto com essa especificação.

## Design

Nós apoiamos o padrão NIST FIPS 203 [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf), que é baseado no CRYSTALS-Kyber, mas NÃO é compatível com ele.

Os handshakes híbridos são conforme especificado em [Noise-Hybrid](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf).

### Troca de Chaves

Definimos uma troca de chaves híbrida para Ratchet. PQ KEM fornece apenas chaves efêmeras e não suporta diretamente handshakes de chave estática como Noise IK.

Definimos as três variantes ML-KEM como em [FIPS203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf), para um total de 3 novos tipos de criptografia. Os tipos híbridos são definidos apenas em combinação com X25519.

Os novos tipos de criptografia são:

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Type</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Code</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM512_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">5</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM768_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">6</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM1024_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">7</td>
</tr>
</table>
A sobrecarga será substancial. Os tamanhos típicos das mensagens 1 e 2 (para IK) são atualmente em torno de 100 bytes (antes de qualquer payload adicional). Isso aumentará de 8x a 15x dependendo do algoritmo.

### Nova Criptografia Necessária

- ML-KEM (anteriormente CRYSTALS-Kyber) [FIPS203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf)
- SHA3-128 (anteriormente Keccak-256) [FIPS202](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.202.pdf) Usado apenas para SHAKE128
- SHA3-256 (anteriormente Keccak-512) [FIPS202](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.202.pdf)
- SHAKE128 e SHAKE256 (extensões XOF para SHA3-128 e SHA3-256)
  [FIPS202](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.202.pdf)

Vetores de teste para SHA3-256, SHAKE128, e SHAKE256 estão em [NIST-VECTORS](https://csrc.nist.gov/projects/cryptographic-standards-and-guidelines/example-values).

Note que a biblioteca Java bouncycastle suporta todos os itens acima. O suporte da biblioteca C++ está no OpenSSL 3.5 [OPENSSL](https://openssl-library.org/post/2025-02-04-release-announcement-3.5/).

## Especificação

### Estruturas Comuns

Veja a especificação de estruturas comuns [COMMON](/docs/specs/common-structures/) para comprimentos de chaves e identificadores.

### Padrões de Handshake

Os handshakes utilizam padrões de handshake [Noise](https://noiseprotocol.org/noise.html).

O seguinte mapeamento de letras é usado:

- e = chave efêmera de uso único
- s = chave estática
- p = carga útil da mensagem
- e1 = chave PQ efêmera de uso único, enviada de Alice para Bob
- ekem1 = o texto cifrado KEM, enviado de Bob para Alice

As seguintes modificações para XK e IK para sigilo direto híbrido (hfs) são conforme especificado em [Noise-Hybrid](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf) seção 5:

```
IK:                         IKhfs:
<- s                        <- s
...                         ...
-> e, es, s, ss, p          -> e, es, e1, s, ss, p
<- tag, e, ee, se, p        <- tag, e, ee, ekem1, se, p
<- p                        <- p
p ->                        p ->

e1 and ekem1 are encrypted. See pattern definitions below.
NOTE: e1 and ekem1 are different sizes (unlike X25519)
```
O padrão e1 é definido como segue, conforme especificado na seção 4 de [Noise-Hybrid](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf):

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
O padrão ekem1 é definido como segue, conforme especificado na seção 4 do [Noise-Hybrid](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf):

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
### Operações ML-KEM Definidas

Definimos as seguintes funções correspondentes aos blocos de construção criptográficos utilizados conforme definido em [FIPS203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf).

**(encap_key, decap_key) = PQ_KEYGEN()**

Alice cria as chaves de encapsulamento e desencapsulamento. A chave de encapsulamento é enviada na mensagem NS. Os tamanhos de encap_key e decap_key variam baseados na variante ML-KEM.

**(ciphertext, kem_shared_key) = ENCAPS(encap_key)**

Bob calcula o texto cifrado e a chave compartilhada, usando o texto cifrado recebido na mensagem NS. O texto cifrado é enviado na mensagem NSR. O tamanho do texto cifrado varia com base na variante ML-KEM. A kem_shared_key sempre tem 32 bytes.

**kem_shared_key = DECAPS(ciphertext, decap_key)**

Alice calcula a chave compartilhada, usando o texto cifrado recebido na mensagem NSR. A kem_shared_key sempre tem 32 bytes.

Note que tanto o encap_key quanto o ciphertext são criptografados dentro de blocos ChaCha/Poly nas mensagens 1 e 2 do handshake Noise. Eles serão descriptografados como parte do processo de handshake.

O kem_shared_key é misturado na chave de encadeamento com MixHash(). Veja abaixo para detalhes.

### KDF do Handshake Noise

#### Visão Geral

O handshake híbrido é definido em [Noise-Hybrid](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf). A primeira mensagem, de Alice para Bob, contém e1, a chave de encapsulamento, antes da carga útil da mensagem. Isso é tratado como uma chave estática adicional; chame EncryptAndHash() nela (como Alice) ou DecryptAndHash() (como Bob). Em seguida, processe a carga útil da mensagem como de costume.

A segunda mensagem, de Bob para Alice, contém ekem1, o texto cifrado, antes da carga útil da mensagem. Isso é tratado como uma chave estática adicional; chame EncryptAndHash() nela (como Bob) ou DecryptAndHash() (como Alice). Em seguida, calcule a kem_shared_key e chame MixKey(kem_shared_key). Depois processe a carga útil da mensagem como de costume.

#### Identificadores Noise

Estas são as strings de inicialização do Noise:

- "Noise_IKhfselg2_25519+MLKEM512_ChaChaPoly_SHA256"
- "Noise_IKhfselg2_25519+MLKEM768_ChaChaPoly_SHA256"
- "Noise_IKhfselg2_25519+MLKEM1024_ChaChaPoly_SHA256"

#### Alice KDF para Mensagem NS

Após o padrão de mensagem 'es' e antes do padrão de mensagem 's', adicione:

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

NOTE: For the next section (static key for IK),
the keydata and chain key remain the same, and n now equals 1
(instead of 0 for non-hybrid).
```
#### Bob KDF para Mensagem NS

Após o padrão de mensagem 'es' e antes do padrão de mensagem 's', adicione:

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

NOTE: For the next section (static key for IK),
the keydata and chain key remain the same, and n now equals 1
(instead of 0 for non-hybrid).
```
#### Bob KDF para Mensagem NSR

Após o padrão de mensagem 'ee' e antes do padrão de mensagem 'se', adicione:

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
```
#### Alice KDF para Mensagem NSR

Após o padrão de mensagem 'ee' e antes do padrão de mensagem 'ss', adicione:

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
```
#### KDF para split()

inalterado

### Formato de Mensagem

#### Formato NS

Mudanças: O ratchet atual continha a chave estática na primeira seção ChaCha, e a carga útil na segunda seção. Com ML-KEM, agora existem três seções. A primeira seção contém a chave pública PQ criptografada. A segunda seção contém a chave estática. A terceira seção contém a carga útil.

Formato criptografado:

```
+----+----+----+----+----+----+----+----+
|                                       |
+         New Session Ephemeral         +
|            Public Key                 |
+            32 bytes                   +
|      Encoded with Elligator2          |
+----+----+----+----+----+----+----+----+
|                                       |
+         ML-KEM encap_key              +
|       ChaCha20 encrypted data         |
+   (see table below for length)        +
|                                       |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|  Poly1305 Message Authentication Code |
+      (MAC) for encap_key Section      +
|              16 bytes                 |
+----+----+----+----+----+----+----+----+
|                                       |
+         X25519 Static Key             +
|       ChaCha20 encrypted data         |
+            32 bytes                   +
|                                       |
+----+----+----+----+----+----+----+----+
|  Poly1305 Message Authentication Code |
+     (MAC) for Static Key Section      +
|              16 bytes                 |
+----+----+----+----+----+----+----+----+
|                                       |
+          Payload Section              +
|       ChaCha20 encrypted data         |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|  Poly1305 Message Authentication Code |
+      (MAC) for Payload Section        +
|              16 bytes                 |
+----+----+----+----+----+----+----+----+
```
Formato descriptografado:

```
Payload Part 1:

+----+----+----+----+----+----+----+----+
|                                       |
+         ML-KEM encap_key              +
|                                       |
+   (see table below for length)        +
|                                       |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+

Payload Part 2:

+----+----+----+----+----+----+----+----+
|                                       |
+         X25519 Static Key             +
|            (32 bytes)                 |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+

Payload Part 3:

+----+----+----+----+----+----+----+----+
|                                       |
+          Payload Section              +
|                                       |
~                                       ~
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
```
Tamanhos:

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Type</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Type Code</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">X len</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">NS len</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">NS Enc len</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">NS Dec len</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">PQ key len</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">pl len</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">4</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">32</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">96+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">64+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">--</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">pl</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM512_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">32</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">912+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">880+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">800+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">800</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">pl</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM768_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">6</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">32</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1296+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1360+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1184+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1184</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">pl</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM1024_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">7</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">32</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1680+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1648+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1568+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1568</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">pl</td>
</tr>
</table>
Note que o payload deve conter um bloco DateTime, então o tamanho mínimo do payload é 7. Os tamanhos mínimos de NS podem ser calculados de acordo.

#### Formato NSR

Alterações: O ratchet atual tem uma carga útil vazia para a primeira seção ChaCha, e a carga útil na segunda seção. Com ML-KEM, agora há três seções. A primeira seção contém o texto cifrado PQ criptografado. A segunda seção tem uma carga útil vazia. A terceira seção contém a carga útil.

Formato criptografado:

```
+----+----+----+----+----+----+----+----+
|       Session Tag 8 bytes             |
+----+----+----+----+----+----+----+----+
|                                       |
+       Ephemeral Public Key            +
|            32 bytes                   |
+      Encoded with Elligator2          +
|                                       |
+----+----+----+----+----+----+----+----+
|                                       |
+         ML-KEM ciphertext             +
|       ChaCha20 encrypted data         |
+   (see table below for length)        +
|                                       |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|  Poly1305 Message Authentication Code |
+     (MAC) for ciphertext Section      +
|              16 bytes                 |
+----+----+----+----+----+----+----+----+
|  Poly1305 Message Authentication Code |
+   (MAC) for key Section (no data)     +
|              16 bytes                 |
+----+----+----+----+----+----+----+----+
|                                       |
+          Payload Section              +
|       ChaCha20 encrypted data         |
~                                       ~
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|  Poly1305 Message Authentication Code |
+      (MAC) for Payload Section        +
|              16 bytes                 |
+----+----+----+----+----+----+----+----+
```
Formato descriptografado:

```
Payload Part 1:

+----+----+----+----+----+----+----+----+
|                                       |
+         ML-KEM ciphertext             +
|                                       |
+   (see table below for length)        +
|                                       |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+

Payload Part 2:

empty

Payload Part 3:

+----+----+----+----+----+----+----+----+
|                                       |
+          Payload Section              +
|                                       |
~                                       ~
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
```
Tamanhos:

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Type</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Type Code</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Y len</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">NSR len</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">NSR Enc len</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">NSR Dec len</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">PQ CT len</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">opt len</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">4</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">32</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">72+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">32+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">--</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">pl</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM512_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">32</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">856+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">816+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">768+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">768</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">pl</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM768_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">6</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">32</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1176+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1136+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1088+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1088</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">pl</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM1024_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">7</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">32</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1656+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1616+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1568+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1568</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">pl</td>
</tr>
</table>
Note que embora o NSR normalmente tenha uma carga útil diferente de zero, a especificação do ratchet [ECIES](/docs/specs/ecies/) não exige isso, então o tamanho mínimo da carga útil é 0. Os tamanhos mínimos do NSR podem ser calculados de acordo.

## Análise de Sobrecarga

### Troca de Chaves

Aumento de tamanho (bytes):

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Type</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Pubkey (NS)</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Ciphertext (NSR)</th>
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
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM1024_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">+1584</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">+1584</td>
</tr>
</table>
Velocidade:

Velocidades conforme relatadas pela [CLOUDFLARE](https://blog.cloudflare.com/pq-2024/):

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Type</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Relative speed</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">X25519 DH/keygen</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">baseline</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM512</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">2.25x faster</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM768</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1.5x faster</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM1024</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1x (same)</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">XK</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">4x DH (keygen + 3 DH)</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM512_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">4x DH + 2x PQ (keygen + enc/dec) = 4.9x DH = 22% slower</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM768_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">4x DH + 2x PQ (keygen + enc/dec) = 5.3x DH = 32% slower</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM1024_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">4x DH + 2x PQ (keygen + enc/dec) = 6x DH = 50% slower</td>
</tr>
</table>
## Análise de Segurança

As categorias de segurança NIST são resumidas no [NIST-PQ-END](https://www.nccoe.nist.gov/sites/default/files/2023-08/pqc-light-at-the-end-of-the-tunnel-presentation.pdf) slide 10. Critérios preliminares: Nossa categoria mínima de segurança NIST deve ser 2 para protocolos híbridos e 3 para PQ-only.

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

Estes são todos protocolos híbridos. Provavelmente precisamos preferir MLKEM768; MLKEM512 não é seguro o suficiente.

Categorias de segurança NIST [FIPS203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf):

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
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM1024</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">5</td>
</tr>
</table>
## Preferências de Tipo

O tipo recomendado para suporte inicial, baseado na categoria de segurança e comprimento da chave, é:

MLKEM768_X25519 (tipo 6)

## Notas de Implementação

### Suporte de Biblioteca

As bibliotecas Bouncycastle, BoringSSL e WolfSSL agora suportam MLKEM. O suporte do OpenSSL está na versão 3.5 lançada em 8 de abril de 2025 [OPENSSL](https://openssl-library.org/post/2025-02-04-release-announcement-3.5/).

### Tunnels Compartilhados

A classificação/detecção automática de múltiplos protocolos nos mesmos túneis deve ser possível com base numa verificação do comprimento da mensagem 1 (New Session Message). Usando MLKEM512_X25519 como exemplo, o comprimento da mensagem 1 é 816 bytes maior que o protocolo ratchet atual, e o tamanho mínimo da mensagem 1 (com apenas um payload DateTime incluído) é 919 bytes. A maioria dos tamanhos da mensagem 1 com ratchet atual tem um payload inferior a 816 bytes, portanto podem ser classificados como ratchet não-híbrido. Mensagens grandes são provavelmente POSTs que são raros.

Portanto, a estratégia recomendada é:

- Se a mensagem 1 for menor que 919 bytes, é o protocolo ratchet atual.
- Se a mensagem 1 for maior ou igual a 919 bytes, provavelmente é MLKEM512_X25519. Tente MLKEM512_X25519 primeiro e, se falhar, tente o protocolo ratchet atual.

Isso deve nos permitir suportar eficientemente o ratchet padrão e o ratchet híbrido no mesmo destino, assim como anteriormente suportávamos ElGamal e ratchet no mesmo destino. Portanto, podemos migrar para o protocolo híbrido MLKEM muito mais rapidamente do que se não pudéssemos suportar protocolos duplos para o mesmo destino, porque podemos adicionar suporte MLKEM a destinos existentes.

As combinações suportadas obrigatórias são:

- X25519 + MLKEM512
- X25519 + MLKEM768
- X25519 + MLKEM1024

As seguintes combinações podem ser complexas e NÃO são obrigatórias de serem suportadas, mas podem ser, dependendo da implementação:

- Mais de um MLKEM
- ElG + um ou mais MLKEM
- X25519 + um ou mais MLKEM
- ElG + X25519 + um ou mais MLKEM

Não é obrigatório suportar múltiplos algoritmos MLKEM (por exemplo, MLKEM512_X25519 e MLKEM_768_X25519) no mesmo destino. Escolha apenas um. Dependente da implementação.

Não é necessário suportar três algoritmos (por exemplo X25519, MLKEM512_X25519, e MLKEM769_X25519) no mesmo destino. A classificação e estratégia de repetição podem ser muito complexas. A configuração e interface de configuração podem ser muito complexas. Dependente da implementação.

Não é necessário suportar algoritmos ElGamal e híbridos no mesmo destino. ElGamal é obsoleto, e ElGamal + híbrido apenas (sem X25519) não faz muito sentido. Além disso, as mensagens de nova sessão ElGamal e híbridas são ambas grandes, então as estratégias de classificação frequentemente teriam que tentar ambas as descriptografias, o que seria ineficiente. Dependente da implementação.

Os clientes podem usar as mesmas chaves estáticas X25519 ou chaves diferentes para os protocolos X25519 e híbrido nos mesmos túneis, dependendo da implementação.

### Sigilo de Encaminhamento

A especificação ECIES permite Garlic Messages no payload da New Session Message, o que permite a entrega 0-RTT do pacote de streaming inicial, geralmente um HTTP GET, juntamente com o leaseset do cliente. No entanto, o payload da New Session Message não possui forward secrecy. Como esta proposta está enfatizando forward secrecy aprimorado para ratchet, as implementações podem ou devem adiar a inclusão do payload de streaming, ou da mensagem de streaming completa, até a primeira Existing Session Message. Isso seria às custas da entrega 0-RTT. As estratégias também podem depender do tipo de tráfego ou tipo de tunnel, ou em GET vs. POST, por exemplo. Dependente da implementação.

### Tamanho da Nova Sessão

MLKEM aumentará dramaticamente o tamanho da New Session Message, conforme descrito acima. Isso pode diminuir significativamente a confiabilidade da entrega da New Session Message através de tunnels, onde elas devem ser fragmentadas em múltiplas mensagens de tunnel de 1024 bytes. O sucesso da entrega é proporcional ao número exponencial de fragmentos. As implementações podem usar várias estratégias para limitar o tamanho da mensagem, à custa da entrega 0-RTT. Dependente da implementação.

## Referências

- [CLOUDFLARE](https://blog.cloudflare.com/pq-2024/)
- [COMMON](/docs/specs/common-structures/)
- [ECIES](/docs/specs/ecies/)
- [FIPS202](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.202.pdf)
- [FIPS203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf)
- [FORUM](http://zzz.i2p/topics/3294)
- [NIST-PQ-END](https://www.nccoe.nist.gov/sites/default/files/2023-08/pqc-light-at-the-end-of-the-tunnel-presentation.pdf)
- [NIST-VECTORS](https://csrc.nist.gov/projects/cryptographic-standards-and-guidelines/example-values)
- [Noise](https://noiseprotocol.org/noise.html)
- [Noise-Hybrid](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf)
- [OPENSSL](https://openssl-library.org/post/2025-02-04-release-announcement-3.5/)
- [PQ-WIREGUARD](https://eprint.iacr.org/2020/379.pdf)
- [Prop169](/proposals/169-pq-crypto/)
