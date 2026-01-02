---
title: "ECIES-X25519-AEAD-Ratchet Criptografia Híbrida"
description: "Variante híbrida pós-quântica do protocolo de criptografia ECIES (Esquema de Criptografia Integrada por Curvas Elípticas) usando ML-KEM (mecanismo de encapsulamento de chaves baseado em reticulados modulares)"
slug: "ecies-hybrid"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

## Status da Implementação

**Implantação atual:** - **i2pd (implementação em C++)**: Totalmente implementado na versão 2.58.0 (setembro de 2025) com suporte a ML-KEM-512, ML-KEM-768 e ML-KEM-1024. Criptografia de ponta a ponta pós-quântica habilitada por padrão quando o OpenSSL 3.5.0 ou posterior estiver disponível. - **Java I2P**: Ainda não implementado nas versões 0.9.67 / 2.10.0 (setembro de 2025). Especificação aprovada e implementação planejada para versões futuras.

Esta especificação descreve a funcionalidade aprovada que está atualmente implantada no i2pd e planejada para implementações em Java do I2P.

## Visão geral

Esta é a variante híbrida pós-quântica do protocolo ECIES-X25519-AEAD-Ratchet [ECIES](/docs/specs/ecies/). Ela representa a primeira fase da Proposta 169 [Prop169](/proposals/169-pq-crypto/) a ser aprovada. Consulte essa proposta para objetivos gerais, modelos de ameaça, análise, alternativas e informações adicionais.

Status da Proposta 169: **Aberta** (primeira fase aprovada para implementação híbrida de ECIES).

Esta especificação contém apenas as diferenças em relação ao [ECIES](/docs/specs/ecies/) padrão e deve ser lida em conjunto com aquela especificação.

## Projeto

Utilizamos o padrão NIST FIPS 203 [FIPS203](https://csrc.nist.gov/pubs/fips/203/final), que se baseia em, mas não é compatível com, o CRYSTALS-Kyber (versões 3.1, 3 e anteriores).

Handshakes híbridos combinam X25519 Diffie-Hellman clássico com mecanismos de encapsulamento de chaves pós-quânticos ML-KEM. Essa abordagem baseia-se em conceitos de sigilo futuro híbrido (hybrid forward secrecy) documentados na pesquisa PQNoise e em implementações semelhantes no TLS 1.3, IKEv2 e WireGuard.

### Troca de Chaves

Definimos uma troca de chaves híbrida para o Ratchet (mecanismo de avanço criptográfico). O KEM pós-quântico fornece apenas chaves efêmeras e não oferece suporte direto a handshakes de chave estática, como o Noise IK.

Definimos as três variantes de ML-KEM (mecanismo de encapsulamento de chaves baseado em reticulados modulares) conforme especificado em [FIPS203](https://csrc.nist.gov/pubs/fips/203/final), totalizando 3 novos tipos de criptografia. Os tipos híbridos só são definidos em combinação com X25519.

Os novos tipos de criptografia são:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Code</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Security Level</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">ML-KEM Variant</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM512_X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">5</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">NIST Category 1 (AES-128 equivalent)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ML-KEM-512</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM768_X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">6</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">NIST Category 3 (AES-192 equivalent)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ML-KEM-768 (Recommended)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM1024_X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">7</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">NIST Category 5 (AES-256 equivalent)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ML-KEM-1024</td>
    </tr>
  </tbody>
</table>
**Nota:** MLKEM768_X25519 (Type 6) é a variante padrão recomendada, oferecendo forte segurança pós-quântica com sobrecarga razoável.

A sobrecarga é substancial em comparação com a criptografia somente com X25519. Os tamanhos típicos das mensagens 1 e 2 (para o IK pattern (padrão IK do Noise)) estão atualmente em torno de 96-103 bytes (antes da carga útil adicional). Isso aumentará aproximadamente 9-12x para MLKEM512 (KEM pós-quântico ML-KEM), 13-16x para MLKEM768 e 17-23x para MLKEM1024, dependendo do tipo de mensagem.

### Nova criptografia necessária

- **ML-KEM** (anteriormente CRYSTALS-Kyber) [FIPS203](https://csrc.nist.gov/pubs/fips/203/final) - Padrão de Mecanismo de Encapsulamento de Chaves baseado em reticulados de módulos
- **SHA3-256** (anteriormente Keccak-512) [FIPS202](https://csrc.nist.gov/pubs/fips/202/final) - Parte do Padrão SHA-3
- **SHAKE128 e SHAKE256** (extensões XOF ao SHA3) [FIPS202](https://csrc.nist.gov/pubs/fips/202/final) - Funções de Saída Extensível

Vetores de teste para SHA3-256, SHAKE128 e SHAKE256 estão disponíveis no [NIST Cryptographic Algorithm Validation Program](https://csrc.nist.gov/Projects/cryptographic-algorithm-validation-program).

**Suporte de bibliotecas:** - Java: a biblioteca Bouncycastle versão 1.79 e posteriores oferece suporte a todas as variantes de ML-KEM (mecanismo de encapsulamento de chaves pós-quântico) e às funções SHA3/SHAKE (algoritmos SHA-3 e SHAKE) - C++: OpenSSL 3.5 e posteriores incluem suporte completo a ML-KEM (lançado em abril de 2025) - Go: Várias bibliotecas disponíveis para implementação de ML-KEM e SHA3

## Especificação

### Estruturas Comuns

Consulte a [Especificação de Estruturas Comuns](/docs/specs/common-structures/) para comprimentos de chaves e identificadores.

### Padrões de Handshake

Os handshakes usam padrões de handshake do [Noise Protocol Framework](https://noiseprotocol.org/noise.html) (framework de protocolo Noise) com adaptações específicas do I2P para segurança pós-quântica híbrida.

O seguinte mapeamento de letras é utilizado:

- **e** = chave efêmera de uso único (X25519)
- **s** = chave estática
- **p** = carga útil da mensagem
- **e1** = chave PQ (pós-quântica) efêmera de uso único, enviada de Alice para Bob (token específico do I2P)
- **ekem1** = o texto cifrado do KEM (mecanismo de encapsulamento de chaves), enviado de Bob para Alice (token específico do I2P)

**Nota importante:** Os nomes de padrão "IKhfs" e "IKhfselg2" e os tokens "e1" e "ekem1" são adaptações específicas do I2P não documentadas na especificação oficial do Noise Protocol Framework. Elas representam definições personalizadas para integrar o ML-KEM ao padrão Noise IK. Embora a abordagem híbrida X25519 + ML-KEM seja amplamente reconhecida na pesquisa em criptografia pós-quântica e em outros protocolos, a nomenclatura específica usada aqui é própria do I2P.

As seguintes modificações ao IK (padrão de aperto de mão do Noise) para sigilo de encaminhamento híbrido são aplicadas:

```
Standard IK:              I2P IKhfs (Hybrid):
<- s                      <- s
...                       ...
-> e, es, s, ss, p        -> e, es, e1, s, ss, p
<- e, ee, se, p           <- e, ee, ekem1, se, p
<- p                      <- p
p ->                      p ->

Note: e1 and ekem1 are encrypted within ChaCha20-Poly1305 AEAD blocks.
Note: e1 (ML-KEM public key) and ekem1 (ML-KEM ciphertext) have different sizes.
```
O padrão **e1** é definido da seguinte forma:

```
For Alice (sender):
(encap_key, decap_key) = PQ_KEYGEN()

// EncryptAndHash(encap_key)
ciphertext = ENCRYPT(k, n, encap_key, ad)
n++
MixHash(ciphertext)

For Bob (receiver):
// DecryptAndHash(ciphertext)
encap_key = DECRYPT(k, n, ciphertext, ad)
n++
MixHash(ciphertext)
```
O padrão **ekem1** é definido da seguinte forma:

```
For Bob (receiver of encap_key):
(kem_ciphertext, kem_shared_key) = ENCAPS(encap_key)

// EncryptAndHash(kem_ciphertext)
ciphertext = ENCRYPT(k, n, kem_ciphertext, ad)
MixHash(ciphertext)

// MixKey
MixKey(kem_shared_key)

For Alice (sender of encap_key):
// DecryptAndHash(ciphertext)
kem_ciphertext = DECRYPT(k, n, ciphertext, ad)
MixHash(ciphertext)

// MixKey
kem_shared_key = DECAPS(kem_ciphertext, decap_key)
MixKey(kem_shared_key)
```
### Operações Definidas do ML-KEM

Definimos as seguintes funções correspondentes às primitivas criptográficas, conforme especificado em [FIPS203](https://csrc.nist.gov/pubs/fips/203/final).

**(encap_key, decap_key) = PQ_KEYGEN()** : Alice cria as chaves de encapsulamento e desencapsulamento. A chave de encapsulamento é enviada na mensagem NS. Tamanhos das chaves:   - ML-KEM-512: encap_key = 800 bytes, decap_key = 1632 bytes   - ML-KEM-768: encap_key = 1184 bytes, decap_key = 2400 bytes   - ML-KEM-1024: encap_key = 1568 bytes, decap_key = 3168 bytes

**(ciphertext, kem_shared_key) = ENCAPS(encap_key)** : Bob calcula o texto cifrado e a chave compartilhada usando a chave de encapsulação recebida na mensagem NS. O texto cifrado é enviado na mensagem NSR. Tamanhos do texto cifrado:   - ML-KEM-512: 768 bytes   - ML-KEM-768: 1088 bytes   - ML-KEM-1024: 1568 bytes

O kem_shared_key tem sempre **32 bytes** em todas as três variantes.

**kem_shared_key = DECAPS(ciphertext, decap_key)** : Alice calcula a chave compartilhada usando o ciphertext recebido na mensagem NSR. O kem_shared_key é sempre **32 bytes**.

**Importante:** Tanto o encap_key quanto o texto cifrado são criptografados dentro de blocos ChaCha20-Poly1305 nas mensagens 1 e 2 do handshake (aperto de mão) Noise. Ambos serão descriptografados como parte do processo de handshake.

O kem_shared_key é integrado à chave de encadeamento com MixKey(). Veja abaixo para mais detalhes.

### KDF (função de derivação de chave) do Noise Handshake

#### Visão geral

O handshake híbrido combina o X25519 ECDH clássico com o ML-KEM pós-quântico. A primeira mensagem, de Alice para Bob, contém e1 (a chave de encapsulamento do ML-KEM) antes da carga útil da mensagem. Isso é tratado como material de chave adicional; aplique EncryptAndHash() a e1 (como Alice) ou DecryptAndHash() (como Bob). Em seguida, processe a carga útil da mensagem como de costume.

A segunda mensagem, de Bob para Alice, contém ekem1 (o texto cifrado ML-KEM) antes da carga útil da mensagem. Isso é tratado como material de chave adicional; chame EncryptAndHash() nele (como Bob) ou DecryptAndHash() (como Alice). Em seguida, calcule kem_shared_key e chame MixKey(kem_shared_key). Depois, processe a carga útil da mensagem como de costume.

#### Identificadores do Noise (framework de protocolos criptográficos)

Estas são as strings de inicialização do Noise (específicas do I2P):

- `Noise_IKhfselg2_25519+MLKEM512_ChaChaPoly_SHA256`
- `Noise_IKhfselg2_25519+MLKEM768_ChaChaPoly_SHA256`
- `Noise_IKhfselg2_25519+MLKEM1024_ChaChaPoly_SHA256`

#### KDF (função de derivação de chaves) de Alice para a mensagem NS

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

NOTE: For the next section (payload for XK or static key for IK),
the keydata and chain key remain the same,
and n now equals 1 (instead of 0 for non-hybrid).
```
#### KDF de Bob para a Mensagem NS

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

NOTE: For the next section (payload for XK or static key for IK),
the keydata and chain key remain the same,
and n now equals 1 (instead of 0 for non-hybrid).
```
#### KDF de Bob para a Mensagem NSR

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
#### Função de derivação de chaves (KDF) de Alice para a mensagem NSR

Depois do padrão de mensagem 'ee' e antes do padrão de mensagem 'ss', adicione:

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

A função split() permanece inalterada em relação à especificação padrão do ECIES. Após a conclusão do handshake (negociação inicial):

```
keydata = HKDF(chainKey, ZEROLEN, "", 64)
k_ab = keydata[0:31]
k_ba = keydata[32:63]
```
Estas são as chaves de sessão bidirecionais para a comunicação em andamento.

### Formato da Mensagem

#### Formato NS (New Session - nova sessão)

**Alterações:** O ratchet (mecanismo de avanço) atual contém a chave estática na primeira seção ChaCha20-Poly1305 e a carga útil na segunda seção. Com o ML-KEM, agora há três seções. A primeira seção contém a chave pública do ML-KEM criptografada (encap_key). A segunda seção contém a chave estática. A terceira seção contém a carga útil.

**Tamanhos de mensagens:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Type Code</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">X25519 len</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">NS len</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">NS Enc len</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">NS Dec len</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">PQ key len</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">pl len</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">4</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">96+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">64+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">--</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">pl</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM512_X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">5</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">912+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">880+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">800+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">800</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">pl</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM768_X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">6</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1296+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1264+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1184+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1184</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">pl</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM1024_X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">7</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1680+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1648+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1568+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1568</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">pl</td>
    </tr>
  </tbody>
</table>
**Nota:** A carga útil deve conter um bloco DateTime (bloco de data e hora) (mínimo de 7 bytes: tipo de 1 byte, tamanho de 2 bytes, carimbo de data/hora de 4 bytes). Os tamanhos mínimos de NS podem ser calculados de acordo. O tamanho mínimo prático de NS é, portanto, de 103 bytes para X25519 e varia de 919 a 1687 bytes para variantes híbridas.

Os aumentos de tamanho de 816, 1200 e 1584 bytes para as três variantes de ML-KEM (mecanismo de encapsulamento de chaves) devem-se à chave pública do ML-KEM mais um MAC Poly1305 de 16 bytes para criptografia autenticada.

#### Formato do NSR (New Session Reply, resposta de nova sessão)

**Alterações:** O ratchet (mecanismo de avanço) atual tem uma carga útil vazia para a primeira seção de ChaCha20-Poly1305 e a carga útil na segunda seção. Com o ML-KEM, agora há três seções. A primeira seção contém o texto cifrado do ML-KEM. A segunda seção tem uma carga útil vazia. A terceira seção contém a carga útil.

**Tamanhos de mensagens:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Type Code</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">X25519 len</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">NSR len</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">NSR Enc len</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">NSR Dec len</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">PQ ct len</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">pl len</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">4</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">72+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">40+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">--</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">pl</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM512_X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">5</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">856+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">824+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">784+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">768</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">pl</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM768_X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">6</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1176+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1144+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1104+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1088</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">pl</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM1024_X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">7</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1656+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1624+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1584+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1568</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">pl</td>
    </tr>
  </tbody>
</table>
Os aumentos de tamanho de 784, 1104 e 1584 bytes para as três variantes do ML-KEM (mecanismo de encapsulamento de chaves baseado em reticulados modulares) devem-se ao texto cifrado do ML-KEM mais um MAC Poly1305 de 16 bytes para criptografia autenticada.

## Análise de Sobrecarga

### Troca de chaves

A sobrecarga da criptografia híbrida é substancial em comparação com o uso somente de X25519:

- **MLKEM512_X25519**: Aproximadamente 9-12x de aumento no tamanho da mensagem de handshake (aperto de mão) (NS: 9,5x, NSR: 11,9x)
- **MLKEM768_X25519**: Aproximadamente 13-16x de aumento no tamanho da mensagem de handshake (NS: 13,5x, NSR: 16,3x)
- **MLKEM1024_X25519**: Aproximadamente 17-23x de aumento no tamanho da mensagem de handshake (NS: 17,5x, NSR: 23x)

Essa sobrecarga é aceitável pelos benefícios adicionais de segurança pós-quântica. Os multiplicadores variam conforme o tipo de mensagem porque os tamanhos base das mensagens diferem (NS mínimo 96 bytes, NSR mínimo 72 bytes).

### Considerações sobre largura de banda

Para um estabelecimento de sessão típico com cargas úteis mínimas: - Apenas X25519: ~200 bytes no total (NS + NSR) - MLKEM512_X25519: ~1,800 bytes no total (aumento de 9x) - MLKEM768_X25519: ~2,500 bytes no total (aumento de 12.5x) - MLKEM1024_X25519: ~3,400 bytes no total (aumento de 17x)

Após o estabelecimento da sessão, a criptografia contínua das mensagens utiliza o mesmo formato de transporte de dados que as sessões que usam apenas X25519, de modo que não há sobrecarga para as mensagens subsequentes.

## Análise de segurança

### Apertos de mão

O handshake (procedimento inicial de negociação) híbrido fornece segurança clássica (X25519) e pós-quântica (ML-KEM). Um atacante deve quebrar **ambos** o ECDH clássico e o KEM (Mecanismo de Encapsulamento de Chaves) pós-quântico para comprometer as chaves de sessão.

Isso oferece: - **Segurança atual**: X25519 ECDH fornece segurança contra atacantes clássicos (nível de segurança de 128 bits) - **Segurança futura**: ML-KEM fornece segurança contra atacantes quânticos (varia conforme o conjunto de parâmetros) - **Segurança híbrida**: Ambos devem ser quebrados para comprometer a sessão (nível de segurança = máximo entre os dois componentes)

### Níveis de segurança

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Variant</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">NIST Category</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Classical Security</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">PQ Security</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Hybrid Security</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM512_X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Category 1</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">128-bit (X25519)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">AES-128 equivalent</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">128-bit</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM768_X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Category 3</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">128-bit (X25519)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">AES-192 equivalent</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">128-bit</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM1024_X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Category 5</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">128-bit (X25519)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">AES-256 equivalent</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">128-bit</td>
    </tr>
  </tbody>
</table>
**Nota:** O nível de segurança híbrido é limitado pelo mais fraco dos dois componentes. Em todos os casos, X25519 oferece segurança clássica de 128 bits. Se um computador quântico criptograficamente relevante se tornar disponível, o nível de segurança dependerá do conjunto de parâmetros ML-KEM escolhido.

### Sigilo Direto

A abordagem híbrida mantém as propriedades de sigilo direto (forward secrecy). As chaves de sessão são derivadas a partir de ambas as trocas de chaves efêmeras X25519 e ML-KEM. Se as chaves privadas efêmeras X25519 ou ML-KEM forem destruídas após o handshake (negociação inicial), sessões anteriores não poderão ser descriptografadas mesmo que as chaves estáticas de longo prazo sejam comprometidas.

O padrão IK fornece sigilo de encaminhamento completo (Confidencialidade do Noise nível 5) após a segunda mensagem (NSR) ser enviada.

## Preferências de Tipo

As implementações devem oferecer suporte a vários tipos híbridos e negociar a variante mutuamente suportada mais forte. A ordem de preferência deve ser:

1. **MLKEM768_X25519** (Tipo 6) - Padrão recomendado, melhor equilíbrio entre segurança e desempenho
2. **MLKEM1024_X25519** (Tipo 7) - Máxima segurança para aplicações sensíveis
3. **MLKEM512_X25519** (Tipo 5) - Segurança pós-quântica básica para cenários com recursos limitados
4. **X25519** (Tipo 4) - Apenas clássico, alternativa para compatibilidade

**Justificativa:** MLKEM768_X25519 é recomendado como padrão porque fornece segurança de Categoria 3 do NIST (equivalente ao AES-192), o que é considerado proteção suficiente contra computadores quânticos, mantendo tamanhos de mensagem razoáveis. MLKEM1024_X25519 oferece segurança superior, porém com uma sobrecarga substancialmente maior.

## Notas de Implementação

### Suporte a bibliotecas

- **Java**: A partir da versão 1.79 (agosto de 2024), a biblioteca Bouncycastle oferece suporte a todas as variantes necessárias de ML-KEM e às funções SHA3/SHAKE. Use `org.bouncycastle.pqc.crypto.mlkem.MLKEMEngine` para conformidade com a FIPS 203.
- **C++**: OpenSSL 3.5 (abril de 2025) e versões posteriores incluem suporte a ML-KEM por meio da interface EVP_KEM. Esta é uma versão Long Term Support (suporte de longo prazo) mantida até abril de 2030.
- **Go**: Várias bibliotecas de terceiros estão disponíveis para ML-KEM e SHA3, incluindo a biblioteca CIRCL da Cloudflare.

### Estratégia de Migração

Implementações devem: 1. Suportar tanto a variante apenas X25519 (algoritmo de acordo de chaves de curva elíptica) quanto as variantes híbridas ML-KEM (mecanismo de encapsulamento de chaves baseado em reticulados de módulo) durante o período de transição 2. Preferir as variantes híbridas quando ambos os pares as suportarem 3. Manter fallback para apenas X25519 para compatibilidade com versões anteriores 4. Considerar as restrições de largura de banda da rede ao selecionar a variante padrão

### Tunnels Compartilhados

O aumento dos tamanhos de mensagem pode impactar o uso de tunnel compartilhado. As implementações devem considerar: - Agrupar handshakes quando possível para amortizar a sobrecarga - Usar tempos de expiração mais curtos para sessões híbridas a fim de reduzir o estado armazenado - Monitorar o uso de largura de banda e ajustar os parâmetros conforme necessário - Implementar controle de congestionamento para o tráfego de estabelecimento de sessão

### Considerações sobre o tamanho de novas sessões

Devido ao maior tamanho das mensagens de handshake, as implementações podem precisar de: - Aumentar os tamanhos de buffer para a negociação de sessão (mínimo de 4KB recomendado) - Ajustar os valores de tempo limite para conexões mais lentas (considerar mensagens ~3-17x maiores) - Considerar compressão para os dados de carga útil em mensagens NS/NSR - Implementar tratamento de fragmentação se exigido pela camada de transporte

### Testes e Validação

As implementações devem verificar: - Geração correta de chaves ML-KEM, encapsulamento e decapsulamento - Integração adequada de kem_shared_key no Noise KDF - Cálculos do tamanho da mensagem em conformidade com a especificação - Interoperabilidade com outras implementações de I2P router - Comportamento de fallback (mecanismo de contingência) quando ML-KEM não estiver disponível

Vetores de teste para operações de ML-KEM (mecanismo de encapsulamento de chaves) estão disponíveis no [Programa de Validação de Algoritmos Criptográficos](https://csrc.nist.gov/Projects/cryptographic-algorithm-validation-program) do NIST.

## Compatibilidade de Versões

**Numeração de versões do I2P:** O I2P mantém dois números de versão paralelos: - **Versão de lançamento do Router**: formato 2.x.x (por exemplo, 2.10.0 lançado em setembro de 2025) - **Versão da API/protocolo**: formato 0.9.x (por exemplo, 0.9.67 corresponde ao router 2.10.0)

Esta especificação faz referência à versão do protocolo 0.9.67, que corresponde à versão 2.10.0 do router e posteriores.

**Matriz de compatibilidade:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Implementation</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Version</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">ML-KEM Support</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Status</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">i2pd</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.58.0+</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Full (512/768/1024)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deployed September 2025</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Java I2P</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.67 / 2.10.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Not yet</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Planned for future release</td>
    </tr>
  </tbody>
</table>
## Referências

- **[ECIES]**: [Especificação ECIES-X25519-AEAD-Ratchet](/docs/specs/ecies/)
- **[Prop169]**: [Proposta 169: Criptografia Pós-Quântica](/proposals/169-pq-crypto/)
- **[FIPS203]**: [NIST FIPS 203 - Padrão ML-KEM](https://csrc.nist.gov/pubs/fips/203/final)
- **[FIPS202]**: [NIST FIPS 202 - Padrão SHA-3](https://csrc.nist.gov/pubs/fips/202/final)
- **[Noise]**: [Framework do Protocolo Noise](https://noiseprotocol.org/noise.html)
- **[COMMON]**: [Especificação de Estruturas Comuns](/docs/specs/common-structures/)
- **[RFC7539]**: [RFC 7539 - ChaCha20 e Poly1305](https://www.rfc-editor.org/rfc/rfc7539)
- **[RFC5869]**: [RFC 5869 - HKDF](https://www.rfc-editor.org/rfc/rfc5869)
- **[OpenSSL]**: [Documentação do OpenSSL 3.5 - ML-KEM](https://docs.openssl.org/3.5/man7/EVP_KEM-ML-KEM/)
- **[Bouncycastle]**: [Biblioteca de Criptografia Java Bouncycastle](https://www.bouncycastle.org/)

---
