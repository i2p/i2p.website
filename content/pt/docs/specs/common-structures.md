---
title: "Estruturas Comuns"
description: "Tipos de dados compartilhados e formatos de serialização utilizados nas especificações do I2P"
slug: "common-structures"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

## Visão geral

Este documento especifica as estruturas de dados fundamentais usadas em todos os protocolos do I2P, incluindo [I2NP](/docs/specs/i2np/), [I2CP](/docs/specs/i2cp/), [SSU2](/docs/specs/ssu2/), [NTCP2](/docs/specs/ntcp2/), entre outros. Essas estruturas comuns garantem a interoperabilidade entre diferentes implementações do I2P e camadas de protocolo.

### Principais mudanças desde 0.9.58

- ElGamal e DSA-SHA1 marcados como obsoletos para Identidades do Router (use X25519 + EdDSA)
- Suporte a ML-KEM pós-quântico em testes beta (opt-in a partir da versão 2.10.0)
- Opções de registros de serviço padronizadas ([Proposal 167](/proposals/167-service-records/), implementado na versão 0.9.66)
- Especificações de preenchimento comprimível finalizadas ([Proposal 161](/pt/proposals/161-ri-dest-padding/), implementado na versão 0.9.57)

---

## Especificações de Tipos Comuns

### Inteiro

**Descrição:** Representa um inteiro não negativo em ordem de bytes de rede (big-endian, mais significativo primeiro).

**Conteúdo:** 1 a 8 bytes representando um inteiro sem sinal.

**Uso:** Comprimentos de campos, contagens, identificadores de tipo e valores numéricos em todos os protocolos do I2P.

---

### Data

**Descrição:** Carimbo de data/hora representando milissegundos desde a época Unix (1º de janeiro de 1970 00:00:00 GMT).

**Conteúdo:** Inteiro de 8 bytes (unsigned long)

**Valores especiais:** - `0` = Data indefinida ou nula - Valor máximo: `0xFFFFFFFFFFFFFFFF` (ano 584,942,417,355)

**Notas de Implementação:** - Sempre no fuso horário UTC/GMT - Precisão em milissegundos obrigatória - Usado para expiração de lease (entrada temporária em um leaseSet do I2P), publicação de RouterInfo e validação de carimbo de data/hora

---

### Cadeia de caracteres

**Descrição:** Cadeia de caracteres codificada em UTF-8 com prefixo de tamanho.

**Formato:**

```
+----+----+----+----+----+----+
|len | UTF-8 encoded data...   |
+----+----+----+----+----+----+

len :: Integer (1 byte)
       Value: 0-255 (string length in bytes, NOT characters)

data :: UTF-8 encoded bytes
        Length: 0-255 bytes
```
**Restrições:** - Comprimento máximo: 255 bytes (não caracteres - sequências UTF-8 de múltiplos bytes contam como vários bytes) - O comprimento pode ser zero (string vazia) - Terminador nulo NÃO incluído - A string NÃO possui terminador nulo

**Importante:** Sequências UTF-8 podem usar vários bytes por caractere. Uma string com 100 caracteres pode exceder o limite de 255 bytes se usar caracteres de múltiplos bytes.

---

## Estruturas de Chaves Criptográficas

### Chave pública

**Descrição:** Chave pública para criptografia assimétrica. O tipo e o tamanho da chave dependem do contexto ou são especificados em um Certificado de Chave.

**Tipo padrão:** ElGamal (obsoleto para Router Identities a partir da versão 0.9.58)

**Tipos suportados:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Code</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Length (bytes)</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Since</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Endianness</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Usage</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Status</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ElGamal</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">256</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Destinations only (unused field)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated for RIs</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">P256</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">64</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">See Proposal 145</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">P384</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">96</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">See Proposal 145</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">P521</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">132</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">See Proposal 145</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">X25519</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.38</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Little</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Current standard</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Recommended</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MLKEM512_X25519</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">5</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Mixed</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Hybrid PQ, LeaseSets only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Beta</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MLKEM768_X25519</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">6</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Mixed</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Hybrid PQ, LeaseSets only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Beta</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MLKEM1024_X25519</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">7</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Mixed</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Hybrid PQ, LeaseSets only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Beta</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MLKEM512</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">800</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshakes only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Beta</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MLKEM768</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1184</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshakes only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Beta</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MLKEM1024</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1568</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshakes only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Beta</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MLKEM512_CT</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">768</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshakes only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Beta</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MLKEM768_CT</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1088</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshakes only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Beta</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MLKEM1024_CT</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1568</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshakes only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Beta</td></tr>
  </tbody>
</table>
**Requisitos de Implementação:**

1. **X25519 (Tipo 4) - Padrão atual:**
   - Usado para criptografia ECIES-X25519-AEAD-Ratchet
   - Obrigatório para Identidades do router desde a versão 0.9.48
   - Codificação little-endian (ordem de bytes do menos significativo para o mais significativo; ao contrário de outros tipos)
   - Consulte [ECIES](/docs/specs/ecies/) e [ECIES-ROUTERS](/docs/specs/ecies/#routers)

2. **ElGamal (Tipo 0) - Legado:**
   - Descontinuado para Identidades de router desde a versão 0.9.58
   - Ainda válido para Destinos (campo não utilizado desde 0.6/2005)
   - Usa primos constantes definidos na [especificação ElGamal](/docs/specs/cryptography/)
   - Suporte mantido para compatibilidade com versões anteriores

3. **MLKEM (Pós-Quântico) - Beta:**
   - A abordagem híbrida combina ML-KEM com X25519
   - NÃO está habilitado por padrão na 2.10.0
   - Requer ativação manual via Hidden Service Manager (Gerenciador de Serviços Ocultos)
   - Consulte [ECIES-HYBRID](/docs/specs/ecies/#hybrid) e [Proposal 169](/proposals/169-pq-crypto/)
   - Códigos de tipo e especificações estão sujeitos a alterações

**JavaDoc:** [PublicKey](http://docs.i2p-projekt.de/javadoc/net/i2p/data/PublicKey.html)

---

### Chave privada

**Descrição:** Chave privada para descriptografia assimétrica, correspondente aos tipos PublicKey.

**Armazenamento:** Tipo e comprimento inferidos a partir do contexto ou armazenados separadamente em estruturas de dados/arquivos de chave.

**Tipos suportados:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Code</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Length (bytes)</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Since</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Endianness</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Usage</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Status</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ElGamal</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">256</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Destinations only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated for RIs</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">P256</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">See Proposal 145</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">P384</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">48</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">See Proposal 145</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">P521</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">66</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">See Proposal 145</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">X25519</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.38</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Little</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Current standard</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Recommended</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MLKEM512_X25519</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">5</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Mixed</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Hybrid PQ, LeaseSets only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Beta</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MLKEM768_X25519</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">6</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Mixed</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Hybrid PQ, LeaseSets only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Beta</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MLKEM1024_X25519</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">7</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Mixed</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Hybrid PQ, LeaseSets only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Beta</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MLKEM512</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1632</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshakes only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Beta</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MLKEM768</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2400</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshakes only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Beta</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MLKEM1024</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3168</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshakes only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Beta</td></tr>
  </tbody>
</table>
**Notas de segurança:** - Chaves privadas DEVEM ser geradas usando geradores de números aleatórios criptograficamente seguros - Chaves privadas X25519 usam "scalar clamping" (ajuste do escalar) conforme definido na RFC 7748 - O material de chave DEVE ser apagado de forma segura da memória quando não for mais necessário

**JavaDoc:** [PrivateKey](http://docs.i2p-projekt.de/javadoc/net/i2p/data/PrivateKey.html)

---

### Chave de sessão

**Descrição:** Chave simétrica para criptografia e descriptografia AES-256 no tunnel e na garlic encryption do I2P.

**Conteúdo:** 32 bytes (256 bits)

**Uso:** - Criptografia na camada de tunnel (AES-256/CBC com IV) - Criptografia de mensagens Garlic - Criptografia de sessão ponta a ponta

**Geração:** DEVE usar gerador de números aleatórios criptograficamente seguro.

**JavaDoc:** [SessionKey](http://docs.i2p-projekt.de/javadoc/net/i2p/data/SessionKey.html)

---

### SigningPublicKey

**Descrição:** Chave pública para verificação de assinatura. Tipo e tamanho especificados no Certificado de Chave do Destino ou inferidos a partir do contexto.

**Tipo padrão:** DSA_SHA1 (obsoleto a partir da 0.9.58)

**Tipos suportados:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Code</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Length (bytes)</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Since</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Endianness</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Usage</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Status</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">DSA_SHA1</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">128</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Legacy only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA_SHA256_P256</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">64</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Older Destinations</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA_SHA384_P384</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">96</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Rare</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA_SHA512_P521</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">132</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Rare</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RSA_SHA256_2048</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">256</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Offline signing only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RSA_SHA384_3072</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">5</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">384</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Offline signing only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RSA_SHA512_4096</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">6</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">512</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Offline signing only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Recommended for SU3</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">EdDSA_SHA512_Ed25519</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">7</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.15</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Little</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Current standard</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Recommended</strong></td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">EdDSA_SHA512_Ed25519ph</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">8</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.25</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Little</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Offline signing only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Rare</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RedDSA_SHA512_Ed25519</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">11</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.39</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Little</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Encrypted leasesets only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Specialized</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved (GOST)</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">9</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">64</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Proposal 134</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved (GOST)</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">10</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">128</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Proposal 134</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved (MLDSA)</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">12-20</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Proposal 169</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Experimental</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">65280-65534</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Varies</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Varies</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Testing only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Never production</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">65535</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Future expansion</td><td style="border:1px solid var(--color-border); padding:0.5rem;">-</td></tr>
  </tbody>
</table>
**Requisitos de Implementação:**

1. **EdDSA_SHA512_Ed25519 (Type 7) - Padrão atual:**
   - Padrão para todas as novas Identidades do Router e Destinos desde o final de 2015
   - Usa a curva Ed25519 com hash SHA-512
   - Chaves públicas de 32 bytes, assinaturas de 64 bytes
   - Codificação little-endian (ao contrário da maioria dos outros tipos)
   - Alto desempenho e segurança

2. **RedDSA_SHA512_Ed25519 (Type 11) - Especializado:**
   - Usado APENAS para leasesets criptografados e cegamento
   - Nunca usado para Identidades de Router ou Destinos padrão
   - Principais diferenças em relação ao EdDSA:
     - Chaves privadas via redução modular (não clamping (ajuste de bits))
     - Assinaturas incluem 80 bytes de dados aleatórios
     - Usa chaves públicas diretamente (não hashes de chaves privadas)
   - Consulte a [especificação Red25519](//docs/specs/red25519-signature-scheme/

3. **DSA_SHA1 (Tipo 0) - Legado:**
   - Descontinuado para Identidades de router a partir da versão 0.9.58
   - Não recomendado para novos Destinos
   - DSA de 1024 bits com SHA-1 (vulnerabilidades conhecidas)
   - Suporte mantido apenas para compatibilidade

4. **Chaves multi-elemento:**
   - Quando composta por dois elementos (por exemplo, pontos ECDSA X,Y)
   - Cada elemento preenchido até length/2 com zeros à esquerda
   - Exemplo: chave ECDSA de 64 bytes = 32 bytes de X + 32 bytes de Y

**JavaDoc:** [SigningPublicKey](http://docs.i2p-projekt.de/javadoc/net/i2p/data/SigningPublicKey.html)

---

### SigningPrivateKey

**Descrição:** Chave privada para criar assinaturas, correspondente aos tipos de SigningPublicKey (chave pública de assinatura).

**Armazenamento:** Tipo e tamanho especificados no momento da criação.

**Tipos suportados:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Code</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Length (bytes)</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Since</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Endianness</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Usage</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Status</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">DSA_SHA1</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">20</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Legacy only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA_SHA256_P256</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Older Destinations</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA_SHA384_P384</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">48</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Rare</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA_SHA512_P521</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">66</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Rare</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RSA_SHA256_2048</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">512</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Offline signing only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RSA_SHA384_3072</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">5</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">768</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Offline signing only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RSA_SHA512_4096</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">6</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1024</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Offline signing only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Recommended for SU3</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">EdDSA_SHA512_Ed25519</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">7</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.15</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Little</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Current standard</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Recommended</strong></td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">EdDSA_SHA512_Ed25519ph</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">8</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.25</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Little</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Offline signing only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Rare</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RedDSA_SHA512_Ed25519</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">11</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.39</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Little</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Encrypted leasesets only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Specialized</td></tr>
  </tbody>
</table>
**Requisitos de Segurança:** - Gerar usando uma fonte de aleatoriedade criptograficamente segura - Proteger com controles de acesso apropriados - Apagar com segurança da memória quando terminar - Para EdDSA: semente de 32 bytes submetida a hash com SHA-512, os primeiros 32 bytes tornam-se o escalar (clamped: ajuste de bits conforme a especificação) - Para RedDSA: geração de chave diferente (redução modular em vez de clamping)

**JavaDoc:** [SigningPrivateKey](http://docs.i2p-projekt.de/javadoc/net/i2p/data/SigningPrivateKey.html)

---

### Assinatura

**Descrição:** Assinatura criptográfica sobre os dados, usando o algoritmo de assinatura correspondente ao tipo SigningPrivateKey.

**Tipo e Comprimento:** Inferidos a partir do tipo de chave usado para assinar.

**Tipos suportados:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Code</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Length (bytes)</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Since</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Endianness</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Usage</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Status</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">DSA_SHA1</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">40</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Legacy only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA_SHA256_P256</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">64</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Older Destinations</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA_SHA384_P384</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">96</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Rare</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA_SHA512_P521</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">132</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Rare</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RSA_SHA256_2048</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">256</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Offline signing only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RSA_SHA384_3072</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">5</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">384</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Offline signing only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RSA_SHA512_4096</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">6</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">512</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Offline signing only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Current for SU3</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">EdDSA_SHA512_Ed25519</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">7</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">64</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.15</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Little</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Current standard</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Recommended</strong></td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">EdDSA_SHA512_Ed25519ph</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">8</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">64</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.25</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Little</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Offline signing only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Rare</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RedDSA_SHA512_Ed25519</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">11</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">64</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.39</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Little</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Encrypted leasesets only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Specialized</td></tr>
  </tbody>
</table>
**Notas de Formato:** - Assinaturas com múltiplos elementos (por exemplo, valores R,S de ECDSA) são preenchidas até length/2 para cada elemento com zeros à esquerda - EdDSA e RedDSA usam codificação little-endian - Todos os outros tipos usam codificação big-endian

**Verificação:** - Use a SigningPublicKey (chave pública de assinatura) correspondente - Siga as especificações do algoritmo de assinatura para o tipo de chave - Verifique se o tamanho da assinatura corresponde ao tamanho esperado para o tipo de chave

**JavaDoc:** [Signature](http://docs.i2p-projekt.de/javadoc/net/i2p/data/Signature.html)

---

### Hash

**Descrição:** Hash SHA-256 de dados, usado em todo o I2P para verificação de integridade e identificação.

**Conteúdo:** 32 bytes (256 bits)

**Uso:** - hashes de Identidade do Router (chaves do banco de dados da rede) - hashes de Destino (chaves do banco de dados da rede) - identificação do gateway de Tunnel em Leases - verificação da integridade dos dados - geração de ID de Tunnel

**Algoritmo:** SHA-256 como definido no FIPS 180-4

**JavaDoc:** [Hash](http://docs.i2p-projekt.de/javadoc/net/i2p/data/Hash.html)

---

### Tag de sessão

**Descrição:** Número aleatório usado para identificação de sessão e criptografia baseada em tags.

**Importante:** O tamanho do Session Tag (etiqueta de sessão) varia conforme o tipo de criptografia: - **ElGamal/AES+SessionTag:** 32 bytes (legado) - **ECIES-X25519:** 8 bytes (padrão atual)

**Padrão atual (ECIES):**

```
Contents: 8 bytes
Usage: Ratchet-based encryption for Destinations and Routers
```
Consulte [ECIES](/docs/specs/ecies/) e [ECIES-ROUTERS](/docs/specs/ecies/#routers) para especificações detalhadas.

**Legado (ElGamal/AES):**

```
Contents: 32 bytes
Usage: Deprecated encryption scheme
```
**Geração:** DEVE usar um gerador de números aleatórios criptograficamente seguro.

**JavaDoc:** [SessionTag](http://docs.i2p-projekt.de/javadoc/net/i2p/data/SessionTag.html)

---

### TunnelId

**Descrição:** Identificador único da posição de um router em um tunnel. Cada salto em um tunnel tem seu próprio TunnelId.

**Formato:**

```
Contents: 4-byte Integer (unsigned 32-bit)
Range: Generally > 0 (zero reserved for special cases)
```
**Uso:** - Identifica conexões de tunnel de entrada/saída em cada router - TunnelId diferente em cada salto na cadeia de tunnels - Usado em estruturas Lease (estrutura de concessão temporária) para identificar tunnels de gateway

**Valores Especiais:** - `0` = Reservado para usos especiais do protocolo (evite durante a operação normal) - TunnelIds (identificadores de tunnel) são localmente significativos para cada router

**JavaDoc:** [TunnelId](http://docs.i2p-projekt.de/javadoc/net/i2p/data/TunnelId.html)

---

## Especificações de Certificados

### Certificado

**Descrição:** Contêiner para recibos, prova de trabalho ou metadados criptográficos usados em todo o I2P.

**Formato:**

```
+----+----+----+----+----+----+-//
|type| length  | payload
+----+----+----+----+----+----+-//

type :: Integer (1 byte)
        Values: 0-5 (see types below)

length :: Integer (2 bytes, big-endian)
          Size of payload in bytes

payload :: data
           length -> $length bytes
```
**Tamanho total:** 3 bytes no mínimo (NULL certificate; certificado vazio), até 65538 bytes no máximo

### Tipos de Certificado

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Code</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Payload Length</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Total Size</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Status</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Usage</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">NULL</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem;">3</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Default/empty certificate</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">HASHCASH</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Varies</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Varies</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Unused (was for proof-of-work)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">HIDDEN</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem;">3</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Unused (hidden routers don't advertise)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">SIGNED</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td><td style="border:1px solid var(--color-border); padding:0.5rem;">40 or 72</td><td style="border:1px solid var(--color-border); padding:0.5rem;">43 or 75</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Unused (DSA signature ± destination hash)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MULTIPLE</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Varies</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Varies</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Unused (multiple certificates)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">KEY</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">5</td><td style="border:1px solid var(--color-border); padding:0.5rem;">4+</td><td style="border:1px solid var(--color-border); padding:0.5rem;">7+</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Current</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Specifies key types (see below)</td></tr>
  </tbody>
</table>
### Certificado de Chave (Tipo 5)

**Introdução:** Versão 0.9.12 (Dezembro de 2013)

**Objetivo:** Especifica tipos de chave não padrão e armazena dados de chave excedentes além da estrutura KeysAndCert padrão de 384 bytes.

**Estrutura da carga útil:**

```
+----+----+----+----+----+----+----+----+-//
|SPKtype|CPKtype| Excess SPK data     |
+----+----+----+----+----+----+----+----+-//
              | Excess CPK data...    |
+----+----+----+----+----+----+----+----+

SPKtype :: Signing Public Key Type (2 bytes)
           See SigningPublicKey table above

CPKtype :: Crypto Public Key Type (2 bytes)
           See PublicKey table above

Excess SPK data :: Signing key bytes beyond 128 bytes
                   Length: 0 to 65531 bytes

Excess CPK data :: Crypto key bytes beyond 256 bytes
                   Length: 0 to remaining space
```
**Notas Críticas de Implementação:**

1. **Ordem dos tipos de chave:**
   - **AVISO:** tipo de chave de assinatura vem ANTES do tipo de chave criptográfica
   - Isso é contraintuitivo, mas é mantido por compatibilidade
   - Ordem: SPKtype, CPKtype (não CPKtype, SPKtype)

2. **Disposição dos dados de chave em KeysAndCert (estrutura de dados):**
   ```
   [Crypto Public Key (partial/complete)]
   [Padding (if total key lengths < 384)]
   [Signing Public Key (partial/complete)]
   [Certificate Header (3 bytes)]
   [Key Certificate (4+ bytes)]
   [Excess Signing Key Data]
   [Excess Crypto Key Data]
   ```

3. **Calculando dados de chave excedentes:**
   - Se Crypto Key > 256 bytes: Excess = (Crypto Length - 256)
   - Se Signing Key > 128 bytes: Excess = (Signing Length - 128)
   - Padding = max(0, 384 - Crypto Length - Signing Length)

**Exemplos (chave criptográfica ElGamal):**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Signing Key Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Total SPK Length</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Padding</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Excess in Cert</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Total Structure Size</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">DSA_SHA1</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">128</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem;">387 + 7 = 394</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA_P256</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">64</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">64</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem;">387 + 7 = 394</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA_P384</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">96</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem;">387 + 7 = 394</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA_P521</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">132</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4</td><td style="border:1px solid var(--color-border); padding:0.5rem;">387 + 11 = 398</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RSA_2048</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">256</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">128</td><td style="border:1px solid var(--color-border); padding:0.5rem;">387 + 135 = 522</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RSA_4096</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">512</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">384</td><td style="border:1px solid var(--color-border); padding:0.5rem;">387 + 391 = 778</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">EdDSA</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">96</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem;">387 + 7 = 394</td></tr>
  </tbody>
</table>
**Requisitos de Identidade do Router:** - Certificado NULL usado até a versão 0.9.15 - Certificado de Chave obrigatório para tipos de chave não padrão desde a versão 0.9.16 - Chaves de criptografia X25519 suportadas desde a versão 0.9.48

**Requisitos do Destino:** - certificado NULL OU Key Certificate (certificado de chave) (conforme necessário) - Key Certificate obrigatório para tipos de chave de assinatura não padrão desde 0.9.12 - Campo de chave pública criptográfica não utilizado desde 0.6 (2005), mas ainda deve estar presente

**Avisos Importantes:**

1. **NULL vs KEY Certificate (NULL = certificado vazio; KEY = certificado com informações de chave):**
   - Um certificado KEY com tipos (0,0) especificando ElGamal+DSA_SHA1 é permitido, mas não é recomendado
   - Use sempre certificado NULL para ElGamal+DSA_SHA1 (representação canônica)
   - Um certificado KEY com (0,0) é 4 bytes mais longo e pode causar problemas de compatibilidade
   - Algumas implementações podem não lidar corretamente com certificados KEY (0,0)

2. **Validação de Excesso de Dados:**
   - As implementações DEVEM verificar se o comprimento do certificado corresponde ao comprimento esperado para cada tipo de chave
   - Rejeitar certificados com dados em excesso que não correspondam aos tipos de chave
   - Proibir dados lixo ao final de uma estrutura de certificado válida

**JavaDoc:** [Certificate](http://docs.i2p-projekt.de/javadoc/net/i2p/data/Certificate.html)

---

### Mapeamento

**Descrição:** Coleção de propriedades chave-valor utilizada para configuração e metadados.

**Formato:**

```
+----+----+----+----+----+----+----+----+
|  size   | key_string (len + data)| =  |
+----+----+----+----+----+----+----+----+
| val_string (len + data)     | ;  | ...
+----+----+----+----+----+----+----+

size :: Integer (2 bytes, big-endian)
        Total number of bytes that follow (not including size field)
        Range: 0 to 65535

key_string :: String
              Format: 1-byte length + UTF-8 data
              Length: 0-255 bytes

= :: Single byte (0x3D, '=' character)

val_string :: String
              Format: 1-byte length + UTF-8 data
              Length: 0-255 bytes

; :: Single byte (0x3B, ';' character)

[Repeat key_string = val_string ; for additional entries]
```
**Limites de tamanho:** - Comprimento da chave: 0-255 bytes (+ 1 byte de comprimento) - Comprimento do valor: 0-255 bytes (+ 1 byte de comprimento) - Tamanho total do mapeamento: 0-65535 bytes (+ 2 bytes do campo de tamanho) - Tamanho máximo da estrutura: 65537 bytes

**Requisito crítico de ordenação:**

Quando mapeamentos aparecem em **estruturas assinadas** (RouterInfo, RouterAddress, propriedades de Destination, I2CP SessionConfig), as entradas DEVEM ser ordenadas pela chave para garantir a invariância da assinatura:

1. **Método de ordenação:** Ordenação lexicográfica usando valores de ponto de código Unicode (equivalente a Java String.compareTo())
2. **Sensibilidade a maiúsculas/minúsculas:** Chaves e valores são geralmente sensíveis a maiúsculas/minúsculas (dependente da aplicação)
3. **Chaves duplicadas:** NÃO são permitidas em estruturas assinadas (causarão falha na verificação da assinatura)
4. **Codificação de caracteres:** Comparação em nível de byte em UTF-8

**Por que a ordenação importa:** - As assinaturas são calculadas sobre a representação em bytes - Diferentes ordens de chaves produzem assinaturas diferentes - Mapeamentos não assinados não exigem ordenação, mas devem seguir a mesma convenção

**Notas de implementação:**

1. **Redundância de codificação:**
   - Tanto os delimitadores `=` e `;` quanto os bytes de comprimento da string (cadeia de caracteres) estão presentes
   - Isso é ineficiente, mas é mantido por compatibilidade
   - Os bytes de comprimento prevalecem; os delimitadores são obrigatórios, mas redundantes

2. **Suporte a caracteres:**
   - Apesar da documentação, `=` e `;` SÃO suportados dentro de strings (os bytes de comprimento tratam disso)
   - A codificação UTF-8 suporta todo o Unicode
   - **Aviso:** I2CP usa UTF-8, mas historicamente o I2NP não tratava UTF-8 corretamente
   - Use ASCII para os mapeamentos do I2NP quando possível, para máxima compatibilidade

3. **Contextos Especiais:**
   - **RouterInfo/RouterAddress:** DEVE ser ordenado, sem duplicados
   - **I2CP SessionConfig:** DEVE ser ordenado, sem duplicados  
   - **Mapeamentos de aplicações:** Ordenação recomendada, mas nem sempre obrigatória

**Exemplo (opções de RouterInfo):**

```
Mapping size: 45 bytes
Sorted entries:
  caps=L       (capabilities)
  netId=2      (network ID)
  router.version=0.9.67
```
**JavaDoc:** [DataHelper](http://docs.i2p-projekt.de/javadoc/net/i2p/data/DataHelper.html)

---

## Especificação da Estrutura Comum

### Chaves e Certificado

**Descrição:** Estrutura fundamental que combina a chave de criptografia, a chave de assinatura e o certificado. Usada tanto como RouterIdentity quanto como Destination.

**Estrutura:**

```
+----+----+----+----+----+----+----+----+
| public_key                            |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| padding (optional)                    |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| signing_key                           |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| certificate                           |
+----+----+----+-//

public_key :: PublicKey (partial or full)
              Default: 256 bytes (ElGamal)
              Other sizes: As specified in Key Certificate

padding :: Random data
           Length: 0 bytes or as needed
           CONSTRAINT: public_key + padding + signing_key = 384 bytes

signing_key :: SigningPublicKey (partial or full)
               Default: 128 bytes (DSA_SHA1)
               Other sizes: As specified in Key Certificate

certificate :: Certificate
               Minimum: 3 bytes (NULL certificate)
               Common: 7 bytes (Key Certificate with default keys)

TOTAL LENGTH: 387+ bytes (never assume exactly 387!)
```
**Alinhamento de Chaves:** - **Chave Pública Criptográfica:** Alinhada no início (byte 0) - **Preenchimento:** No meio (se necessário) - **Chave Pública de Assinatura:** Alinhada no final (do byte 256 ao byte 383) - **Certificado:** Começa no byte 384

**Cálculo do tamanho:**

```
Total size = 384 + 3 + key_certificate_length

For NULL certificate (ElGamal + DSA_SHA1):
  Total = 384 + 3 = 387 bytes

For Key Certificate (EdDSA + X25519):
  Total = 384 + 3 + 4 = 391 bytes

For larger keys (e.g., RSA_4096):
  Total = 384 + 3 + 4 + excess_key_data_length
```
### Diretrizes para Geração de Preenchimento ([Proposta 161](/pt/proposals/161-ri-dest-padding/))

**Versão da implementação:** 0.9.57 (janeiro de 2023, lançamento 2.1.0)

**Contexto:** - Para chaves que não sejam ElGamal+DSA, o preenchimento está presente na estrutura fixa de 384 bytes - Para Destinos, o campo de chave pública de 256 bytes não é usado desde a versão 0.6 (2005) - O preenchimento deve ser gerado de forma a ser compressível, mantendo-se seguro

**Requisitos:**

1. **Dados Aleatórios Mínimos:**
   - Use pelo menos 32 bytes de dados aleatórios criptograficamente seguros
   - Isso fornece entropia suficiente para a segurança

2. **Estratégia de compressão:**
   - Repetir os 32 bytes ao longo de todo o campo de padding/chave pública
   - Protocolos como I2NP Database Store, Streaming SYN e o handshake do SSU2 usam compressão
   - Economia significativa de largura de banda sem comprometer a segurança

3. **Exemplos:**

**Identidade do Router (X25519 + EdDSA):**

```
Structure:
- 32 bytes X25519 public key
- 320 bytes padding (10 copies of 32-byte random data)
- 32 bytes EdDSA public key
- 7 bytes Key Certificate

Compression savings: ~288 bytes when compressed
```
**Destino (ElGamal-unused + EdDSA):**

```
Structure:
- 256 bytes unused ElGamal field (11 copies of 32-byte random data, truncated to 256)
- 96 bytes padding (3 copies of 32-byte random data)
- 32 bytes EdDSA public key  
- 7 bytes Key Certificate

Compression savings: ~320 bytes when compressed
```
4. **Por que isso funciona:**
   - O hash SHA-256 da estrutura completa ainda inclui toda a entropia
   - A distribuição na DHT do banco de dados da rede depende apenas do hash
   - A chave de assinatura (32 bytes EdDSA/X25519) fornece 256 bits de entropia
   - 32 bytes adicionais de dados aleatórios repetidos = 512 bits de entropia total
   - Mais do que suficiente para força criptográfica

5. **Notas de Implementação:**
   - DEVE armazenar e transmitir a estrutura completa de 387+ bytes
   - hash SHA-256 calculado sobre a estrutura completa não compactada
   - Compressão aplicada na camada de protocolo (I2NP, Streaming, SSU2)
   - Retrocompatível com todas as versões desde a 0.6 (2005)

**JavaDoc:** [KeysAndCert](http://docs.i2p-projekt.de/javadoc/net/i2p/data/KeysAndCert.html)

---

### Identidade do router

**Descrição:** Identifica de forma exclusiva um router na rede I2P. Estrutura idêntica a KeysAndCert.

**Formato:** Consulte a estrutura KeysAndCert acima

**Requisitos atuais (a partir da versão 0.9.58):**

1. **Tipos de chave obrigatórios:**
   - **Criptografia:** X25519 (tipo 4, 32 bytes)
   - **Assinatura:** EdDSA_SHA512_Ed25519 (tipo 7, 32 bytes)
   - **Certificado:** Certificado de chave (tipo 5)

2. **Tipos de chave descontinuados:**
   - ElGamal (tipo 0) descontinuado para Identidades de Router a partir da versão 0.9.58
   - DSA_SHA1 (tipo 0) descontinuado para Identidades de Router a partir da versão 0.9.58
   - Estes não devem ser usados em novos routers

3. **Tamanho típico:**
   - X25519 + EdDSA com certificado de chave = 391 bytes
   - 32 bytes de chave pública X25519
   - 320 bytes de preenchimento (compressível conforme [Proposal 161](/pt/proposals/161-ri-dest-padding/))
   - 32 bytes de chave pública EdDSA
   - 7 bytes de certificado (cabeçalho de 3 bytes + 4 bytes de tipos de chave)

**Evolução histórica:** - Pré-0.9.16: Sempre certificado NULL (ElGamal + DSA_SHA1) - 0.9.16-0.9.47: Suporte a certificado de chave adicionado - 0.9.48+: Chaves de criptografia X25519 suportadas - 0.9.58+: ElGamal e DSA_SHA1 obsoletos

**Chave do Banco de Dados da Rede:** - RouterInfo (registro de informações do router) indexado pelo hash SHA-256 da RouterIdentity (identidade criptográfica do router) completa - Hash calculada sobre toda a estrutura de 391+ bytes (incluindo preenchimento)

**Consulte também:** - Diretrizes para geração de preenchimento ([Proposal 161](/pt/proposals/161-ri-dest-padding/)) - Especificação do Certificado de Chave acima

**JavaDoc:** [RouterIdentity](http://docs.i2p-projekt.de/javadoc/net/i2p/data/router/RouterIdentity.html)

---

### Destino

**Descrição:** Identificador de ponto de extremidade para a entrega segura de mensagens. Estruturalmente idêntico a KeysAndCert, mas com semântica de uso diferente.

**Formato:** Consulte a estrutura KeysAndCert acima

**Diferença crítica em relação ao RouterIdentity:** - **O campo de chave pública NÃO É UTILIZADO e pode conter dados aleatórios** - Este campo não é usado desde a versão 0.6 (2005) - Originalmente era para a antiga criptografia I2CP-para-I2CP (desativada) - Atualmente, só é usado como IV para a criptografia de LeaseSet descontinuada

**Recomendações atuais:**

1. **Chave de assinatura:**
   - **Recomendado:** EdDSA_SHA512_Ed25519 (tipo 7, 32 bytes)
   - Alternativa: tipos ECDSA para compatibilidade com versões mais antigas
   - Evitar: DSA_SHA1 (obsoleto, desaconselhado)

2. **Chave de criptografia:**
   - O campo não é utilizado, mas deve estar presente
   - **Recomendado:** Preencher com dados aleatórios conforme [Proposta 161](/pt/proposals/161-ri-dest-padding/) (compressível)
   - Tamanho: Sempre 256 bytes (slot do ElGamal, embora não seja utilizado para ElGamal)

3. **Certificado:**
   - Certificado NULL para ElGamal + DSA_SHA1 (apenas legado)
   - Certificado de chave para todos os outros tipos de chave de assinatura

**Destino moderno típico:**

```
Structure:
- 256 bytes unused field (random data, compressible)
- 96 bytes padding (random data, compressible)
- 32 bytes EdDSA signing public key
- 7 bytes Key Certificate

Total: 391 bytes
Compression savings: ~320 bytes
```
**Chave de criptografia efetiva:** - A chave de criptografia para o Destination (destino no I2P) está no **LeaseSet**, não no Destination - O LeaseSet contém as chaves públicas de criptografia atuais - Consulte a especificação LeaseSet2 para o tratamento de chaves de criptografia

**Chave do Banco de Dados da Rede:** - LeaseSet indexado pelo hash SHA-256 da Destination (destino no I2P) completa - Hash calculado sobre a estrutura completa de 387+ bytes

**JavaDoc:** [Destination](http://docs.i2p-projekt.de/javadoc/net/i2p/data/Destination.html)

---

## Estruturas do Banco de Dados de Rede

### Lease (descritor temporário de túnel)

**Descrição:** Autoriza um tunnel específico a receber mensagens para um Destino. Parte do formato original de LeaseSet (tipo 1).

**Formato:**

```
+----+----+----+----+----+----+----+----+
| tunnel_gw                             |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|     tunnel_id     |      end_date
+----+----+----+----+----+----+----+----+
                    |
+----+----+----+----+

tunnel_gw :: Hash (32 bytes)
             SHA-256 hash of the gateway RouterIdentity

tunnel_id :: TunnelId (4 bytes)
             Tunnel identifier at the gateway router

end_date :: Date (8 bytes)
            Expiration timestamp in milliseconds since epoch
```
**Tamanho total:** 44 bytes

**Uso:** - Usado apenas no LeaseSet original (tipo 1, obsoleto) - Para o LeaseSet2 e variantes posteriores, use o Lease2 em vez disso

**JavaDoc:** [Lease](http://docs.i2p-projekt.de/javadoc/net/i2p/data/Lease.html)

---

### LeaseSet (Tipo 1)

**Descrição:** Formato LeaseSet original. Contém tunnels autorizados e chaves para um Destino. Armazenado no banco de dados da rede. **Status: Obsoleto** (use LeaseSet2 em vez disso).

**Estrutura:**

```
+----+----+----+----+----+----+----+----+
| destination                           |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| encryption_key                        |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| signing_key                           |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| num| Lease 0                          |
+----+                                  +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| Lease 1                               |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| Lease ($num-1)                        |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| signature                             |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+

destination :: Destination
               Length: 387+ bytes

encryption_key :: PublicKey (256 bytes, ElGamal)
                  Used for end-to-end ElGamal/AES+SessionTag encryption
                  Generated anew at each router startup (not persistent)

signing_key :: SigningPublicKey (128+ bytes)
               Same type as Destination signing key
               Used for LeaseSet revocation (unimplemented)
               Generated anew at each router startup (not persistent)

num :: Integer (1 byte)
       Number of Leases to follow
       Range: 0-16

leases :: Array of Lease structures
          Length: $num × 44 bytes
          Each Lease is 44 bytes

signature :: Signature (40+ bytes)
             Length determined by Destination signing key type
             Signed by Destination's SigningPrivateKey
```
**Armazenamento do banco de dados:** - **Tipo de banco de dados:** 1 - **Chave:** hash SHA-256 do Destino - **Valor:** Estrutura completa de LeaseSet (estrutura I2P que descreve os túneis de entrada de um Destino)

**Notas importantes:**

1. **Chave pública do Destino não utilizada:**
   - O campo de chave pública de criptografia no Destino não é utilizado
   - A chave de criptografia no LeaseSet é a chave de criptografia efetiva

2. **Chaves temporárias:**
   - `encryption_key` é temporária (regenerada na inicialização do router)
   - `signing_key` é temporária (regenerada na inicialização do router)
   - Nenhuma das chaves é persistente entre reinicializações

3. **Revogação (Não implementada):**
   - Pretendia-se usar `signing_key` para a revogação de LeaseSet
   - O mecanismo de revogação nunca foi implementado
   - LeaseSet com zero leases (leases: entradas temporárias de túnel) estava previsto para revogação, mas não é utilizado

4. **Versionamento/Carimbo de data/hora:**
   - LeaseSet não possui um campo de carimbo de data/hora `published` explícito
   - A versão é a data de expiração mais cedo entre todos os leases
   - Um novo LeaseSet deve ter uma data de expiração mais cedo dos leases para ser aceito

5. **Publicação da expiração de lease (entrada de túnel):**
   - Pré-0.9.7: Todos os leases publicados com a mesma expiração (a mais próxima)
   - 0.9.7+: Expirações individuais reais de lease publicadas
   - Isto é um detalhe de implementação, não faz parte da especificação

6. **Zero Leases:**
   - LeaseSet com zero leases é tecnicamente permitido
   - Destinado à revogação (não implementada)
   - Não usado na prática
   - As variantes de LeaseSet2 exigem pelo menos um Lease

**Descontinuação:** LeaseSet tipo 1 está obsoleto. Novas implementações devem usar **LeaseSet2 (tipo 3)** que oferece: - Campo de carimbo de data/hora de publicação (melhor versionamento) - Suporte a múltiplas chaves de criptografia - Capacidade de assinatura offline - Expirações de leases (períodos de concessão) de 4 bytes (vs 8 bytes) - Opções mais flexíveis

**JavaDoc:** [LeaseSet](http://docs.i2p-projekt.de/javadoc/net/i2p/data/LeaseSet.html)

---

## Variantes de LeaseSet

### Lease2

**Descrição:** Formato de lease (concessão) aprimorado com expiração de 4 bytes. Usado em LeaseSet2 (tipo 3) e MetaLeaseSet (tipo 7).

**Introdução:** Versão 0.9.38 (consulte [Proposta 123](/proposals/123-new-netdb-entries/))

**Formato:**

```
+----+----+----+----+----+----+----+----+
| tunnel_gw                             |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|     tunnel_id     |      end_date     |
+----+----+----+----+----+----+----+----+

tunnel_gw :: Hash (32 bytes)
             SHA-256 hash of gateway RouterIdentity

tunnel_id :: TunnelId (4 bytes)
             Tunnel identifier at gateway

end_date :: 4-byte timestamp (seconds since epoch)
            Rolls over in year 2106
```
**Tamanho total:** 40 bytes (4 bytes menor do que o Lease original)

**Comparação com o Lease (entrada do leaseSet) original:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Feature</th>
      <th style="border:1pxsolid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Lease (Type&nbsp;1)</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Lease2 (Type&nbsp;3+)</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Size</td><td style="border:1px solid var(--color-border); padding:0.5rem;">44 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">40 bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Expiration Size</td><td style="border:1px solid var(--color-border); padding:0.5rem;">8 bytes (ms)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">4 bytes (seconds)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Precision</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Millisecond</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Second</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Rollover</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Year&nbsp;292,277,026,596</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Year&nbsp;2106</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Used In</td><td style="border:1px solid var(--color-border); padding:0.5rem;">LeaseSet (deprecated)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">LeaseSet2, MetaLeaseSet</td></tr>
  </tbody>
</table>
**JavaDoc:** [Lease2](http://docs.i2p-projekt.de/javadoc/net/i2p/data/Lease2.html)

---

### OfflineSignature (assinatura offline)

**Descrição:** Estrutura opcional para chaves efêmeras pré-assinadas, permitindo a publicação de LeaseSet sem acesso online à chave privada de assinatura do Destino.

**Introdução:** Versão 0.9.38 (consulte [Proposta 123](/proposals/123-new-netdb-entries/))

**Formato:**

```
+----+----+----+----+----+----+----+----+
|     expires       | sigtype |         |
+----+----+----+----+----+----+         +
|       transient_public_key            |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|           signature                   |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+

expires :: 4-byte timestamp (seconds since epoch)
           Expiration of transient key validity
           Rolls over in year 2106

sigtype :: 2-byte signature type
           Type of transient_public_key (see SigningPublicKey types)

transient_public_key :: SigningPublicKey
                        Length determined by sigtype
                        Temporary signing key for LeaseSet

signature :: Signature
             Length determined by Destination's signing key type
             Signature of (expires || sigtype || transient_public_key)
             Signed by Destination's permanent SigningPrivateKey
```
**Finalidade:** - Permite a geração offline de LeaseSet - Protege a chave mestra do Destination (identidade de serviço no I2P) contra exposição online - A chave transitória pode ser revogada ao publicar um novo LeaseSet sem assinatura offline

**Cenários de uso:**

1. **Destinos de Alta Segurança:**
   - Chave mestra de assinatura armazenada offline (HSM (módulo de segurança de hardware), armazenamento a frio)
   - Chaves temporárias geradas offline por períodos limitados
   - Uma chave temporária comprometida não expõe a chave mestra

2. **Publicação de LeaseSet criptografado:**
   - EncryptedLeaseSet pode incluir assinatura offline
   - Chave pública cega + assinatura offline fornecem segurança adicional

**Considerações de Segurança:**

1. **Gerenciamento de expiração:**
   - Defina um prazo de expiração razoável (de dias a semanas, não anos)
   - Gere novas chaves temporárias antes da expiração
   - Expiração mais curta = melhor segurança, mais manutenção

2. **Geração de Chaves:**
   - Gerar chaves transitórias offline em ambiente seguro
   - Assinar com a chave mestra offline
   - Transferir apenas a chave transitória assinada + a assinatura para o router online

3. **Revogação:**
   - Publicar novo LeaseSet sem assinatura offline para revogar implicitamente
   - Ou publicar novo LeaseSet com chave transitória diferente

**Verificação de Assinatura:**

```
Data to sign: expires (4 bytes) || sigtype (2 bytes) || transient_public_key

Verification:
1. Extract Destination from LeaseSet
2. Get Destination's SigningPublicKey
3. Verify signature over (expires || sigtype || transient_public_key)
4. Check that current time < expires
5. If valid, use transient_public_key to verify LeaseSet signature
```
**Notas de implementação:** - O tamanho total varia com base no sigtype e no tipo de chave de assinatura da Destination (destino no I2P) - Tamanho mínimo: 4 + 2 + 32 (chave EdDSA) + 64 (assinatura EdDSA) = 102 bytes - Tamanho máximo prático: ~600 bytes (chave efêmera RSA-4096 + assinatura RSA-4096)

**Compatível com:** - LeaseSet2 (tipo 3) - EncryptedLeaseSet (tipo 5) - MetaLeaseSet (tipo 7)

**Veja também:** [Proposta 123](/proposals/123-new-netdb-entries/) para um protocolo de assinatura offline detalhado.

---

### LeaseSet2Header (cabeçalho do LeaseSet2)

**Descrição:** Estrutura de cabeçalho comum para LeaseSet2 (tipo 3) e MetaLeaseSet (tipo 7).

**Introdução:** Versão 0.9.38 (consulte [Proposta 123](/proposals/123-new-netdb-entries/))

**Formato:**

```
+----+----+----+----+----+----+----+----+
| destination                           |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|     published     | expires |  flags  |
+----+----+----+----+----+----+----+----+
| offline_signature (optional)          |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+

destination :: Destination
               Length: 387+ bytes

published :: 4-byte timestamp (seconds since epoch)
             Publication time of this LeaseSet
             Rolls over in year 2106

expires :: 2-byte offset (seconds)
           Offset from published timestamp
           Maximum: 65535 seconds (18.2 hours)

flags :: 2 bytes (bit flags)
         See flag definitions below

offline_signature :: OfflineSignature (optional)
                     Present only if flags bit 0 is set
                     Variable length
```
**Tamanho total mínimo:** 395 bytes (sem assinatura offline)

**Definições de flags (ordem dos bits: 15 14 ... 3 2 1 0):**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Bit</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Name</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Offline Keys</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0 = No offline keys, 1 = Offline signature present</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Unpublished</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0 = Standard published, 1 = Unpublished (client-side only)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Blinded</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0 = Standard, 1 = Will be blinded when published</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3-15</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Must be 0 for compatibility</td></tr>
  </tbody>
</table>
**Detalhes da flag:**

**Bit 0 - Chaves offline:** - `0`: Sem assinatura offline, use a chave de assinatura do Destino para verificar a assinatura do LeaseSet - `1`: A estrutura OfflineSignature (estrutura de assinatura offline) vem após o campo de flags

**Bit 1 - Não publicado:** - `0`: LeaseSet publicado padrão, deve ser propagado aos floodfills - `1`: LeaseSet não publicado (somente no lado do cliente)   - NÃO deve ser propagado, publicado ou enviado em resposta a consultas   - Se expirar, NÃO consultar o netdb para substituição (a menos que o bit 2 também esteja definido)   - Usado para tunnels locais ou testes

**Bit 2 - Ofuscado (desde 0.9.42):** - `0`: LeaseSet padrão - `1`: Este LeaseSet não criptografado será ofuscado e criptografado quando publicado   - A versão publicada será EncryptedLeaseSet (tipo 5)   - Se expirar, consulte a **blinded location** (localização ofuscada) em netdb para substituição   - Também deve definir o bit 1 como 1 (não publicado + ofuscado)   - Usado para serviços ocultos criptografados

**Limites de Expiração:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">LeaseSet Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Maximum Expires Value</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Maximum Actual Time</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">LeaseSet2 (type 3)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈660 seconds</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈11 minutes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MetaLeaseSet (type 7)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">65,535 seconds</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈18.2 hours</td></tr>
  </tbody>
</table>
**Requisitos do carimbo de data/hora de publicação:**

LeaseSet (tipo 1) não tinha um campo published, o que exigia buscar a expiração de lease (concessão) mais antiga para versionamento. LeaseSet2 adiciona um carimbo de data/hora `published` explícito com resolução de 1 segundo.

**Nota crítica de implementação:** - Routers DEVEM limitar a taxa de publicação de LeaseSet a **muito mais lenta do que uma vez por segundo** por Destino - Se publicar mais rapidamente, garanta que cada novo LeaseSet tenha `published` time pelo menos 1 segundo depois - Floodfills rejeitarão o LeaseSet se o `published` time não for mais recente do que a versão atual - Intervalo mínimo recomendado: 10-60 segundos entre publicações

**Exemplos de cálculo:**

**LeaseSet2 (máximo de 11 minutos):**

```
published = 1704067200 (2024-01-01 00:00:00 UTC)
expires = 660 (seconds)
Actual expiration = 1704067200 + 660 = 1704067860 (2024-01-01 00:11:00 UTC)
```
**MetaLeaseSet (máximo de 18,2 horas):**

```
published = 1704067200 (2024-01-01 00:00:00 UTC)
expires = 65535 (seconds)
Actual expiration = 1704067200 + 65535 = 1704132735 (2024-01-01 18:12:15 UTC)
```
**Versionamento:** - LeaseSet é considerado "mais recente" se o carimbo de data/hora `published` for maior - Floodfills armazenam e disseminam apenas a versão mais recente - Tenha cuidado quando a Lease (alocação temporária de túnel) mais antiga corresponder à Lease mais antiga do LeaseSet anterior

---

### LeaseSet2 (Tipo 3)

**Descrição:** Formato moderno de LeaseSet com múltiplas chaves de criptografia, assinaturas offline e registros de serviço. Padrão atual para serviços ocultos no I2P.

**Introdução:** Versão 0.9.38 (ver [Proposta 123](/proposals/123-new-netdb-entries/))

**Estrutura:**

```
+----+----+----+----+----+----+----+----+
|         ls2_header                    |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|          options                      |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|numk| keytype0| keylen0 |              |
+----+----+----+----+----+              +
|          encryption_key_0             |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| keytypen| keylenn |                   |
+----+----+----+----+                   +
|          encryption_key_n             |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| num| Lease2 0                         |
+----+                                  +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| Lease2($num-1)                        |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| signature                             |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+

ls2header :: LeaseSet2Header
             Length: 395+ bytes (varies with offline signature)

options :: Mapping
           Key-value pairs for service records and metadata
           Length: 2+ bytes (size field + data)

numk :: Integer (1 byte)
        Number of encryption keys
        Range: 1 to (implementation-defined maximum, typically 8)

keytype :: 2-byte encryption type
           See PublicKey type table

keylen :: 2-byte key length
          Must match keytype specification

encryption_key :: PublicKey
                  Length: keylen bytes
                  Type: keytype

[Repeat keytype/keylen/encryption_key for each key]

num :: Integer (1 byte)
       Number of Lease2s
       Range: 1-16 (at least one required)

leases :: Array of Lease2 structures
          Length: $num × 40 bytes

signature :: Signature
             Length determined by signing key type
             Signed over entire structure including database type prefix
```
**Armazenamento do banco de dados:** - **Tipo de banco de dados:** 3 - **Chave:** hash SHA-256 de Destination (destino I2P) - **Valor:** estrutura LeaseSet2 completa

**Cálculo da Assinatura:**

```
Data to sign: database_type (1 byte, value=3) || complete LeaseSet2 data

Verification:
1. Prepend database type byte (0x03) to LeaseSet2 data
2. If offline signature present:
   - Verify offline signature against Destination key
   - Verify LeaseSet2 signature against transient key
3. Else:
   - Verify LeaseSet2 signature against Destination key
```
### Ordem de preferência de chaves de criptografia

**Para LeaseSet Publicado (Servidor):** - Chaves listadas em ordem de preferência do servidor (mais preferidas primeiro) - Clientes que suportam vários tipos DEVERIAM respeitar a preferência do servidor - Selecione o primeiro tipo suportado da lista - Em geral, tipos de chaves com numeração mais alta (mais novos) são mais seguros/eficientes - Ordem recomendada: Liste as chaves em ordem inversa pelo código do tipo (as mais novas primeiro)

**Exemplo de Preferência do Servidor:**

```
numk = 2
Key 0: X25519 (type 4, 32 bytes)         [Most preferred]
Key 1: ElGamal (type 0, 256 bytes)       [Legacy compatibility]
```
**Para LeaseSet não publicado (cliente):** - A ordem das chaves efetivamente não importa (raramente são feitas tentativas de conexão a clientes) - Siga a mesma convenção para manter a consistência

**Seleção de chave do cliente:** - Respeitar a preferência do servidor (selecionar o primeiro tipo suportado) - Ou usar preferência definida pela implementação - Ou determinar uma preferência combinada com base nas capacidades de ambas as partes

### Mapeamento de Opções

**Requisitos:** - As opções DEVEM ser ordenadas por chave (lexicográfica, ordem de bytes UTF-8) - A ordenação garante a invariância da assinatura - Chaves duplicadas NÃO são permitidas

**Formato Padrão ([Proposta 167](/proposals/167-service-records/)):**

A partir da API 0.9.66 (junho de 2025, versão 2.9.0), as opções de service record (registro de serviço) seguem um formato padronizado. Consulte [Proposta 167](/proposals/167-service-records/) para a especificação completa.

**Formato da Opção de Registro de Serviço:**

```
Key: _service._proto
Value: record_type ttl [priority weight] port target [appoptions]

service :: Symbolic name of service (lowercase, [a-z0-9-])
           Examples: smtp, http, irc, mumble
           Use standard identifiers from IANA Service Name Registry
           or Linux /etc/services when available

proto :: Transport protocol (lowercase, [a-z0-9-])
         "tcp" = streaming protocol
         "udp" = repliable datagrams
         Protocol indicators for raw datagrams may be defined later

record_type :: "0" (self-reference) or "1" (SRV record)

ttl :: Time to live in seconds (positive integer)
       Recommended minimum: 86400 (one day)
       Prevents frequent re-queries

For record_type = 0 (self-reference):
  port :: I2CP port number (non-negative integer)
  appoptions :: Optional application-specific data (no spaces or commas)

For record_type = 1 (SRV record):
  priority :: Lower value = more preferred (non-negative integer)
  weight :: Relative weight for same priority, higher = more likely (non-negative)
  port :: I2CP port number (non-negative integer)
  target :: Hostname or b32 of destination (lowercase)
            Format: "example.i2p" or "aaaaa...aaaa.b32.i2p"
            Recommend b32 unless hostname is "well known"
  appoptions :: Optional application-specific data (no spaces or commas)
```
**Exemplos de Registros de Serviço:**

**1. Servidor SMTP autorreferenciado:**

```
Destination: aaaa...aaaa.b32.i2p (this LeaseSet)
Option: "_smtp._tcp" = "0 999999 25"

Meaning: This destination provides SMTP service on I2CP port 25
```
**2. Servidor SMTP Externo Único:**

```
Destination: aaaa...aaaa.b32.i2p (this LeaseSet)
Option: "_smtp._tcp" = "1 86400 0 0 25 bbbb...bbbb.b32.i2p"

Meaning: SMTP service provided by bbbb...bbbb on port 25
         TTL = 1 day, single server (priority=0, weight=0)
```
**3. Vários servidores SMTP (balanceamento de carga):**

```
Destination: aaaa...aaaa.b32.i2p (this LeaseSet)
Option: "_smtp._tcp" = "1 86400 0 0 25 bbbb...bbbb.b32.i2p,1 86400 1 0 25 cccc...cccc.b32.i2p"

Meaning: Two SMTP servers
         bbbb...bbbb (priority=0, preferred)
         cccc...cccc (priority=1, backup)
```
**4. Serviço HTTP com Opções do Aplicativo:**

```
Option: "_http._tcp" = "0 86400 80 tls=1.3;cert=ed25519"

Meaning: HTTP on port 80 with TLS 1.3 and EdDSA certificates
```
**Recomendações de TTL (tempo de vida):** - Mínimo: 86400 segundos (1 dia) - TTL mais longo reduz a carga de consultas no netdb - Equilíbrio entre a redução de consultas e a propagação de atualizações do serviço - Para serviços estáveis: 604800 (7 dias) ou mais

**Notas de Implementação:**

1. **Chaves de criptografia (a partir da versão 0.9.44):**
   - ElGamal (tipo 0, 256 bytes): compatibilidade com versões antigas
   - X25519 (tipo 4, 32 bytes): padrão atual
   - Variantes MLKEM: pós-quânticas (beta, não finalizadas)

2. **Validação do Comprimento da Chave:**
   - Floodfills e clientes DEVEM ser capazes de analisar tipos de chave desconhecidos
   - Use o campo keylen para ignorar chaves desconhecidas
   - Não falhe ao analisar se o tipo de chave for desconhecido

3. **Carimbo de data/hora de publicação:**
   - Consulte as notas do LeaseSet2Header sobre limitação de taxa
   - Incremento mínimo de 1 segundo entre publicações
   - Recomendado: 10-60 segundos entre publicações

4. **Migração do tipo de criptografia:**
   - Múltiplas chaves permitem migração gradual
   - Liste as chaves antigas e as novas durante o período de transição
   - Remova a chave antiga após um período suficiente para atualização dos clientes

**JavaDoc:** [LeaseSet2](http://docs.i2p-projekt.de/javadoc/net/i2p/data/LeaseSet2.html)

---

### MetaLease (termo específico do I2P sem tradução estabelecida)

**Descrição:** Estrutura de Lease para MetaLeaseSet que pode referenciar outros LeaseSets em vez de tunnels. Usado para balanceamento de carga e redundância.

**Introdução:** Versão 0.9.38, funcionamento previsto para a 0.9.40 (veja [Proposta 123](/proposals/123-new-netdb-entries/))

**Formato:**

```
+----+----+----+----+----+----+----+----+
| tunnel_gw                             |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|    flags     |cost|      end_date     |
+----+----+----+----+----+----+----+----+

tunnel_gw :: Hash (32 bytes)
             SHA-256 hash of:
             - Gateway RouterIdentity (for type 1), OR
             - Another MetaLeaseSet destination (for type 3/5/7)

flags :: 3 bytes
         Bit order: 23 22 ... 3 2 1 0
         Bits 3-0: Entry type (see table below)
         Bits 23-4: Reserved (must be 0)

cost :: 1 byte (0-255)
        Lower value = higher priority
        Used for load balancing

end_date :: 4-byte timestamp (seconds since epoch)
            Expiration time
            Rolls over in year 2106
```
**Tamanho total:** 40 bytes

**Tipo de entrada (bits de flags 3-0):**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Code</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Unknown</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Unknown/invalid entry</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">LeaseSet</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Points to LeaseSet (type 1, deprecated)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">LeaseSet2</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Points to LeaseSet2 (type 3)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">EncryptedLeaseSet</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">5</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Points to EncryptedLeaseSet (type 5)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MetaLeaseSet</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align-center?">7</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Points to another MetaLeaseSet (type 7)</td></tr>
  </tbody>
</table>
**Cenários de uso:**

1. **Balanceamento de carga:**
   - MetaLeaseSet (estrutura que referencia vários LeaseSet2) com várias entradas MetaLease
   - Cada entrada aponta para um LeaseSet2 diferente
   - Os clientes selecionam com base no campo cost

2. **Redundância:**
   - Múltiplas entradas apontando para LeaseSets de backup
   - Alternativa caso o LeaseSet principal esteja indisponível

3. **Migração de Serviço:**
   - MetaLeaseSet aponta para um novo LeaseSet
   - Permite uma transição suave entre destinos

**Uso do Campo de Custo:** - Custo mais baixo = prioridade mais alta - Custo 0 = prioridade máxima - Custo 255 = prioridade mínima - Os clientes DEVERIAM preferir entradas de menor custo - Entradas de custo igual podem ser balanceadas aleatoriamente

**Comparação com Lease2:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Feature</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Lease2</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">MetaLease</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Size</td><td style="border:1px solid var(--color-border); padding:0.5rem;">40 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">40 bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Tunnel ID</td><td style="border:1px solid var(--color-border); padding:0.5rem;">4 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Replaced by flags (3 bytes) + cost (1 byte)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Points To</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Specific tunnel</td><td style="border:1px solid var(--color-border); padding:0.5rem;">LeaseSet or MetaLeaseSet</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Usage</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Direct tunnel reference</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Indirection/load balancing</td></tr>
  </tbody>
</table>
**JavaDoc:** [MetaLease](http://docs.i2p-projekt.de/javadoc/net/i2p/data/MetaLease.html)

---

### MetaLeaseSet (Tipo 7)

**Descrição:** Variante de LeaseSet que contém entradas MetaLease, fornecendo indireção para outros LeaseSets. Utilizado para balanceamento de carga, redundância e migração de serviço.

**Introdução:** Definido na 0.9.38, funcionamento previsto para a 0.9.40 (ver [Proposta 123](/proposals/123-new-netdb-entries/))

**Status:** Especificação concluída. O status de implantação em produção deve ser verificado em relação às versões atuais do I2P.

**Estrutura:**

```
+----+----+----+----+----+----+----+----+
|         ls2_header                    |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|          options                      |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| num| MetaLease 0                      |
+----+                                  +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| MetaLease($num-1)                     |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|numr|                                  |
+----+                                  +
|          revocation_0                 |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|          revocation_n                 |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| signature                             |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+

ls2header :: LeaseSet2Header
             Length: 395+ bytes

options :: Mapping
           Length: 2+ bytes (size + data)
           MUST be sorted by key

num :: Integer (1 byte)
       Number of MetaLease entries
       Range: 1 to (implementation-defined, recommend 1-16)

metaleases :: Array of MetaLease structures
              Length: $num × 40 bytes

numr :: Integer (1 byte)
        Number of revocation hashes
        Range: 0 to (implementation-defined, recommend 0-16)

revocations :: Array of Hash structures
               Length: $numr × 32 bytes
               SHA-256 hashes of revoked LeaseSet Destinations
```
**Armazenamento de banco de dados:** - **Tipo de banco de dados:** 7 - **Chave:** hash SHA-256 do Destination (destino no I2P) - **Valor:** estrutura MetaLeaseSet completa

**Cálculo da assinatura:**

```
Data to sign: database_type (1 byte, value=7) || complete MetaLeaseSet data

Verification:
1. Prepend database type byte (0x07) to MetaLeaseSet data
2. If offline signature present in header:
   - Verify offline signature against Destination key
   - Verify MetaLeaseSet signature against transient key
3. Else:
   - Verify MetaLeaseSet signature against Destination key
```
**Cenários de uso:**

**1. Balanceamento de carga:**

```
MetaLeaseSet for primary.i2p:
  MetaLease 0: cost=0, points to server1.i2p LeaseSet2
  MetaLease 1: cost=0, points to server2.i2p LeaseSet2
  MetaLease 2: cost=0, points to server3.i2p LeaseSet2

Clients randomly select among equal-cost entries
```
**2. Comutação por falha:**

```
MetaLeaseSet for service.i2p:
  MetaLease 0: cost=0, points to primary.i2p LeaseSet2
  MetaLease 1: cost=100, points to backup.i2p LeaseSet2

Clients prefer cost=0 (primary), fall back to cost=100 (backup)
```
**3. Migração de Serviço:**

```
MetaLeaseSet for old-domain.i2p:
  MetaLease 0: cost=0, points to new-domain.i2p LeaseSet2

Transparently redirects clients from old to new destination
```
**4. Arquitetura Multicamadas:**

```
MetaLeaseSet for service.i2p:
  MetaLease 0: cost=0, points to region1-meta.i2p (another MetaLeaseSet)
  MetaLease 1: cost=0, points to region2-meta.i2p (another MetaLeaseSet)

Each region MetaLeaseSet points to regional servers
Allows hierarchical load balancing
```
**Lista de Revogação:**

A lista de revogação permite que o MetaLeaseSet (termo técnico do I2P) revogue explicitamente LeaseSets publicados anteriormente:

- **Finalidade:** Marcar determinadas Destinations (identificadores de destino no I2P) como não mais válidas
- **Conteúdo:** Hashes SHA-256 de estruturas de Destination revogadas
- **Uso:** Clientes NÃO DEVEM usar LeaseSets cujo hash de Destination conste na lista de revogação
- **Valor típico:** Vazio (numr=0) na maioria das implantações

**Exemplo de Revogação:**

```
Service migrates from dest-v1.i2p to dest-v2.i2p:
  MetaLease 0: points to dest-v2.i2p
  Revocations: [hash(dest-v1.i2p)]

Clients will use v2 and ignore v1 even if cached
```
**Tratamento de expiração:**

MetaLeaseSet usa LeaseSet2Header com expires=65535 seconds no máximo (~18,2 horas):

- Muito mais longo que o LeaseSet2 (estrutura que anuncia como alcançar um destino no I2P; versão 2) (máx. ~11 minutos)
- Adequado para indirecionamento relativamente estático
- LeaseSets referenciados podem ter expiração mais curta
- Os clientes devem verificar a expiração tanto do MetaLeaseSet (um LeaseSet que aponta para outros LeaseSets) E dos LeaseSets referenciados

**Mapeamento de Opções:**

- Use o mesmo formato das opções de LeaseSet2
- Pode incluir registros de serviço ([Proposta 167](/proposals/167-service-records/))
- DEVE ser ordenado por chave
- Registros de serviço normalmente descrevem o serviço final, não a estrutura de indireção

**Notas de Implementação do Cliente:**

1. **Processo de resolução:**
   ```
   1. Query netdb for MetaLeaseSet using SHA-256(Destination)
   2. Parse MetaLeaseSet, extract MetaLease entries
   3. Sort entries by cost (lower = better)
   4. For each entry in cost order:
      a. Extract LeaseSet hash from tunnel_gw field
      b. Determine entry type from flags
      c. Query netdb for referenced LeaseSet (may be another MetaLeaseSet)
      d. Check revocation list
      e. Check expiration
      f. If valid, use the LeaseSet; else try next entry
   ```

2. **Armazenamento em cache:**
   - Armazene em cache tanto o MetaLeaseSet (estrutura de metadados que referencia LeaseSets) quanto os LeaseSets referenciados
   - Verifique a expiração de ambos os níveis
   - Monitore a publicação atualizada do MetaLeaseSet

3. **Failover (comutação por falha):**
   - Se a entrada preferida falhar, tente a próxima opção de menor custo
   - Considere marcar as entradas com falha como temporariamente indisponíveis
   - Verifique novamente periodicamente para detectar recuperação

**Estado da implementação:**

[Proposal 123](/proposals/123-new-netdb-entries/) observa que algumas partes ainda estão "em desenvolvimento". Implementadores devem:
- Verificar a prontidão para produção na versão alvo do I2P
- Testar o suporte a MetaLeaseSet (tipo de LeaseSet com metadados) antes da implantação
- Verificar se há especificações atualizadas em versões mais recentes do I2P

**JavaDoc:** [MetaLeaseSet](http://docs.i2p-projekt.de/javadoc/net/i2p/data/MetaLeaseSet.html)

---

### EncryptedLeaseSet (Tipo 5)

**Descrição:** LeaseSet criptografado e cegado para privacidade aprimorada. Somente a chave pública cegada e os metadados são visíveis; os leases (entradas do LeaseSet) reais e as chaves de criptografia estão criptografados.

**Introdução:** Definido na 0.9.38, operacional a partir da 0.9.39 (ver [Proposta 123](/proposals/123-new-netdb-entries/))

**Estrutura:**

```
+----+----+----+----+----+----+----+----+
| sigtype |                             |
+----+----+                             +
|        blinded_public_key             |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|     published     | expires |  flags  |
+----+----+----+----+----+----+----+----+
| offline_signature (optional)          |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|  len    |                             |
+----+----+                             +
|         encrypted_data                |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| signature                             |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+

sigtype :: 2-byte signature type
           Type of blinded_public_key
           MUST be RedDSA_SHA512_Ed25519 (type 11)

blinded_public_key :: SigningPublicKey (32 bytes for RedDSA)
                      Blinded version of Destination signing key
                      Used to verify signature on EncryptedLeaseSet

published :: 4-byte timestamp (seconds since epoch)
             Publication time
             Rolls over in year 2106

expires :: 2-byte offset (seconds)
           Offset from published
           Maximum: 65535 seconds (18.2 hours)
           Practical maximum for LeaseSet data: ~660 seconds (~11 min)

flags :: 2 bytes
         Bit 0: Offline signature present (0=no, 1=yes)
         Bit 1: Unpublished (0=published, 1=client-side only)
         Bits 15-2: Reserved (must be 0)

offline_signature :: OfflineSignature (optional)
                     Present only if flags bit 0 = 1
                     Variable length

len :: 2-byte integer
       Length of encrypted_data
       Range: 1 to 65535

encrypted_data :: Encrypted payload
                  Length: len bytes
                  Contains encrypted LeaseSet2 or MetaLeaseSet

signature :: Signature (64 bytes for RedDSA)
             Length determined by sigtype
             Signed by blinded_public_key or transient key
```
**Armazenamento de banco de dados:** - **Tipo de banco de dados:** 5 - **Chave:** Hash SHA-256 da **Destination ofuscada** (não da Destination original) - **Valor:** Estrutura completa de EncryptedLeaseSet

**Diferenças cruciais em relação ao LeaseSet2:**

1. **NÃO usa a estrutura LeaseSet2Header** (tem campos semelhantes, mas disposição diferente)
2. **Chave pública ofuscada** em vez da Destination (identidade criptográfica do I2P) completa
3. **Carga útil cifrada** em vez de leases e chaves em claro
4. **A chave de base de dados é o hash da Destination ofuscada**, não da Destination original

**Cálculo da Assinatura:**

```
Data to sign: database_type (1 byte, value=5) || complete EncryptedLeaseSet data

Verification:
1. Prepend database type byte (0x05) to EncryptedLeaseSet data
2. If offline signature present (flags bit 0 = 1):
   - Verify offline signature against blinded public key
   - Verify EncryptedLeaseSet signature against transient key
3. Else:
   - Verify EncryptedLeaseSet signature against blinded public key
```
**Requisito do tipo de assinatura:**

**DEVE usar RedDSA_SHA512_Ed25519 (tipo 11):** - Chaves públicas cegadas de 32 bytes - Assinaturas de 64 bytes - Necessário para as propriedades de segurança do cegamento - Consulte [especificação Red25519](//docs/specs/red25519-signature-scheme/

**Principais diferenças em relação ao EdDSA:** - Chaves privadas por redução modular (não por clamping (mascaramento de bits)) - Assinaturas incluem 80 bytes de dados aleatórios - Usa chaves públicas diretamente (sem hashes) - Permite operação de blinding (cegamento) segura

**Cegamento e Criptografia:**

Consulte a [especificação do EncryptedLeaseSet](/docs/specs/encryptedleaseset/) (leaseSet criptografado) para detalhes completos:

**1. Cegamento de Chave:**

```
Blinding process (daily rotation):
  secret = HKDF(original_signing_private_key, date_string, "i2pblinding1")
  alpha = SHA-256(secret) mod L (where L is Ed25519 group order)
  blinded_private_key = alpha * original_private_key
  blinded_public_key = alpha * original_public_key
```
**2. Localização da base de dados:**

```
Client publishes to:
  Key = SHA-256(blinded_destination)
  
Where blinded_destination uses:
  - Blinded public key (signing key)
  - Same unused public key field (random)
  - Same certificate structure
```
**3. Camadas de Criptografia (Três Camadas):**

**Camada 1 - Camada de Autenticação (Acesso do Cliente):** - Criptografia: cifra de fluxo ChaCha20 - Derivação de chaves: HKDF com segredos específicos de cada cliente - Clientes autenticados podem descriptografar a camada externa

**Camada 2 - Camada de Criptografia:** - Criptografia: ChaCha20 - Chave: derivada do DH (Diffie-Hellman) entre cliente e servidor - Contém o LeaseSet2 ou o MetaLeaseSet propriamente dito

**Camada 3 - LeaseSet Interno (descritor de destino do I2P):** - LeaseSet2 (formato mais recente de LeaseSet) completo ou MetaLeaseSet (LeaseSet que referencia outros LeaseSets) - Inclui todos os tunnels, chaves de criptografia, opções - Apenas acessível após descriptografia bem-sucedida

**Derivação de Chave de Criptografia:**

```
Client has: ephemeral_client_private_key
Server has: ephemeral_server_public_key (in encrypted_data)

Shared secret = X25519(client_private, server_public)
Encryption key = HKDF(shared_secret, context_info, "i2pblinding2")
```
**Processo de descoberta:**

**Para clientes autorizados:**

```
1. Client knows original Destination
2. Client computes current blinded Destination (based on current date)
3. Client computes database key: SHA-256(blinded_destination)
4. Client queries netdb for EncryptedLeaseSet using blinded key
5. Client decrypts layer 1 using authorization credentials
6. Client decrypts layer 2 using DH shared secret
7. Client extracts inner LeaseSet2/MetaLeaseSet
8. Client uses tunnels from inner LeaseSet for communication
```
**Para clientes não autorizados:** - Não podem descriptografar mesmo que encontrem o EncryptedLeaseSet - Não podem determinar o Destination original a partir da versão blinded (cegamento) - Não podem vincular EncryptedLeaseSets entre diferentes períodos de blinding (rotação diária)

**Prazos de expiração:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Content Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Maximum Expires</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">EncryptedLeaseSet (outer)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">65,535 sec (≈18.2 hr)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Full 2-byte expires field</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Inner LeaseSet2</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈660 sec (≈11 min)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Actual lease data practical maximum</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Inner MetaLeaseSet</td><td style="border:1px solid var(--color-border); padding:0.5rem;">65,535 sec (≈18.2 hr)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Indirection can be longer-lived</td></tr>
  </tbody>
</table>
**Carimbo de data/hora da publicação:**

Mesmos requisitos que o LeaseSet2Header: - Deve aumentar em pelo menos 1 segundo entre publicações - Os Floodfills rejeitam se não for mais recente do que a versão atual - Recomendado: 10-60 segundos entre publicações

**Assinaturas offline com Encrypted LeaseSets:**

Considerações especiais ao usar assinaturas offline: - A chave pública cegada é rotacionada diariamente - A assinatura offline deve ser regenerada diariamente com uma nova chave cegada - OU use a assinatura offline no LeaseSet interno, não no EncryptedLeaseSet externo - Veja as notas da [Proposta 123](/proposals/123-new-netdb-entries/)

**Notas de Implementação:**

1. **Autorização de clientes:**
   - Vários clientes podem ser autorizados com chaves diferentes
   - Cada cliente autorizado possui credenciais de descriptografia exclusivas
   - Revogue um cliente alterando as chaves de autorização

2. **Rotação Diária de Chaves:**
   - Blinded keys (chaves cegadas) mudam à meia-noite UTC
   - Os clientes devem recalcular diariamente o Destino cegado
   - EncryptedLeaseSets antigos deixam de poder ser descobertos após a rotação

3. **Propriedades de Privacidade:**
   - Floodfills não podem determinar o Destino original
   - Clientes não autorizados não podem acessar o serviço
   - Períodos de blinding (ofuscação) diferentes não podem ser vinculados
   - Sem metadados em claro além dos tempos de expiração

4. **Desempenho:**
   - Clientes devem realizar o cálculo de cegamento diário
   - A criptografia em três camadas adiciona sobrecarga computacional
   - Considere armazenar em cache o LeaseSet (estrutura de metadados que descreve um destino no I2P) interno descriptografado

**Considerações de Segurança:**

1. **Gerenciamento de chaves de autorização:**
   - Distribua com segurança as credenciais de autorização do cliente
   - Use credenciais exclusivas por cliente para revogação granular
   - Rotacione as chaves de autorização periodicamente

2. **Sincronização do relógio:**
   - O blinding (cegamento criptográfico) diário depende de datas UTC sincronizadas
   - O desvio de relógio pode causar falhas de consulta
   - Considere oferecer suporte ao blinding do dia anterior/seguinte para tolerância

3. **Vazamento de metadados:**
   - Os campos Published e expires estão em texto claro
   - A análise de padrões pode revelar características do serviço
   - Aleatorize os intervalos de publicação, se for motivo de preocupação

**JavaDoc:** [EncryptedLeaseSet](http://docs.i2p-projekt.de/javadoc/net/i2p/data/EncryptedLeaseSet.html)

---

## Estruturas do Router

### RouterAddress

**Descrição:** Define as informações de conexão para um router por meio de um protocolo de transporte específico.

**Formato:**

```
+----+----+----+----+----+----+----+----+
|cost|           expiration
+----+----+----+----+----+----+----+----+
     |        transport_style           |
+----+----+----+----+-//-+----+----+----+
|                                       |
+                                       +
|               options                 |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+

cost :: Integer (1 byte)
        Relative cost, 0=free, 255=expensive
        Typical values:
          5-6: SSU2
          10-11: NTCP2

expiration :: Date (8 bytes)
              MUST BE ALL ZEROS (see critical note below)

transport_style :: String (1-256 bytes)
                   Transport protocol name
                   Current values: "SSU2", "NTCP2"
                   Legacy: "SSU", "NTCP" (removed)

options :: Mapping
           Transport-specific configuration
           Common options: "host", "port"
           Transport-specific options vary
```
**CRÍTICO - Campo de Expiração:**

⚠️ **O campo de expiração DEVE ser definido para todos os zeros (8 bytes com valor zero).**

- **Motivo:** Desde a versão 0.9.3, expiração diferente de zero causa falha na verificação da assinatura
- **Histórico:** A expiração originalmente não era usada, sempre nula
- **Estado atual:** O campo voltou a ser reconhecido a partir da 0.9.12, mas é necessário aguardar uma atualização da rede
- **Implementação:** Sempre definir como 0x0000000000000000

Qualquer valor de expiração diferente de zero fará com que a assinatura do RouterInfo falhe na validação.

### Protocolos de Transporte

**Protocolos atuais (a partir da versão 2.10.0):**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Protocol</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Status</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Introduced</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Removed</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>SSU2</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.54 (May 2022)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Default since 0.9.56</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>NTCP2</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.36 (Aug 2018)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">NTCP</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Removed</td><td style="border:1px solid var(--color-border); padding:0.5rem;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.50 (May 2021)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Use NTCP2</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">SSU</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Removed</td><td style="border:1px solid var(--color-border); padding:0.5rem;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem;">2.4.0 (Dec 2023)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Use SSU2</td></tr>
  </tbody>
</table>
**Valores do estilo de transporte:** - `"SSU2"`: Transporte atual baseado em UDP - `"NTCP2"`: Transporte atual baseado em TCP - `"NTCP"`: Legado, removido (não usar) - `"SSU"`: Legado, removido (não usar)

### Opções comuns

Todos os transportes normalmente incluem:

```
"host" = IPv4 or IPv6 address or hostname
"port" = Port number (1-65535)
```
### Opções específicas do SSU2

Consulte a [especificação SSU2](/docs/specs/ssu2/) (protocolo de transporte do I2P) para detalhes completos.

**Opções obrigatórias:**

```
"host" = IP address (IPv4 or IPv6)
"port" = UDP port number
"s" = Static X25519 public key (Base64, 44 characters = 32 bytes)
"i" = Introduction key X25519 (Base64, 44 characters = 32 bytes)
"v" = "2" (protocol version)
```
**Opções opcionais:**

```
"caps" = Capability string (e.g., "B" for bandwidth tier)
"ihost0", "ihost1", ... = Introducer IP addresses
"iport0", "iport1", ... = Introducer ports  
"ikey0", "ikey1", ... = Introducer static keys (Base64, 44 chars)
"itag0", "itag1", ... = Introducer relay tags
"iexp0", "iexp1", ... = Introducer expiration timestamps
"mtu" = Maximum transmission unit (default 1500, min 1280)
"mtu6" = IPv6 MTU (if different from IPv4)
```
**Exemplo SSU2 RouterAddress:**

```
cost: 5
expiration: 0x0000000000000000
transport_style: "SSU2"
options:
  host=198.51.100.42
  port=12345
  s=SGVsbG8gV29ybGQhIFRoaXMgaXMgYSBzYW1wbGUga2V5IQ==
  i=QW5vdGhlciBTYW1wbGUgS2V5IGZvciBJbnRyb2R1Y3Rpb24=
  v=2
  caps=BC
  mtu=1472
```
### Opções Específicas do NTCP2

Consulte a [especificação do NTCP2](/docs/specs/ntcp2/) para obter detalhes completos.

**Opções obrigatórias:**

```
"host" = IP address (IPv4 or IPv6)
"port" = TCP port number
"s" = Static X25519 public key (Base64, 44 characters = 32 bytes)
"i" = Initialization vector (Base64, 24 characters = 16 bytes)
"v" = "2" (protocol version)
```
**Opções opcionais (desde 0.9.50):**

```
"caps" = Capability string
```
**Exemplo de NTCP2 RouterAddress:**

```
cost: 10
expiration: 0x0000000000000000
transport_style: "NTCP2"
options:
  host=198.51.100.42
  port=23456
  s=SGVsbG8gV29ybGQhIFRoaXMgaXMgYSBzYW1wbGUga2V5IQ==
  i=U2FtcGxlIElWIGhlcmU=
  v=2
```
### Notas de Implementação

1. **Valores de custo:**
   - UDP (SSU2) normalmente tem custo menor (5-6) devido à eficiência
   - TCP (NTCP2) normalmente tem custo mais alto (10-11) devido à sobrecarga
   - Menor custo = transporte preferido

2. **Múltiplos Endereços:**
   - Routers podem publicar múltiplas entradas de RouterAddress (estrutura de endereço do router)
   - Diferentes transportes (SSU2 e NTCP2)
   - Diferentes versões de IP (IPv4 e IPv6)
   - Os clientes selecionam com base em custo e capacidades

3. **Nome de host vs IP:**
   - Endereços IP são preferidos para melhor desempenho
   - Nomes de host são suportados, mas adicionam sobrecarga de resolução de DNS
   - Considere usar IP para RouterInfos publicados (metadados do router no I2P)

4. **Codificação Base64:**
   - Todas as chaves e os dados binários codificados em Base64
   - Base64 padrão (RFC 4648)
   - Sem preenchimento ou caracteres não padrão

**JavaDoc:** [RouterAddress](http://docs.i2p-projekt.de/javadoc/net/i2p/data/router/RouterAddress.html)

---

### RouterInfo (informações do router)

**Descrição:** Informações publicadas completas sobre um router, armazenadas no banco de dados da rede. Contém identidade, endereços e capacidades.

**Formato:**

```
+----+----+----+----+----+----+----+----+
| router_ident                          |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| published                             |
+----+----+----+----+----+----+----+----+
|size| RouterAddress 0                  |
+----+                                  +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| RouterAddress 1                       |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| RouterAddress ($size-1)               |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+-//-+----+----+----+
|psiz| options                          |
+----+----+----+----+-//-+----+----+----+
| signature                             |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+

router_ident :: RouterIdentity
                Length: 387+ bytes (typically 391 for X25519+EdDSA)

published :: Date (8 bytes)
             Publication timestamp (milliseconds since epoch)

size :: Integer (1 byte)
        Number of RouterAddress entries
        Range: 0-255

addresses :: Array of RouterAddress
             Variable length
             Each RouterAddress has variable size

peer_size :: Integer (1 byte)
             Number of peer hashes (ALWAYS 0)
             Historical, unused feature

options :: Mapping
           Router capabilities and metadata
           MUST be sorted by key

signature :: Signature
             Length determined by router_ident signing key type
             Typically 64 bytes (EdDSA)
             Signed by router_ident's SigningPrivateKey
```
**Armazenamento do banco de dados:** - **Tipo de banco de dados:** 0 - **Chave:** hash SHA-256 de RouterIdentity (identidade do roteador) - **Valor:** estrutura RouterInfo (informações do roteador) completa

**Carimbo de tempo publicado:** - Data de 8 bytes (milissegundos desde a época Unix) - Usado para controle de versão do RouterInfo - Routers publicam novo RouterInfo periodicamente - Floodfills mantêm a versão mais recente com base no carimbo de tempo publicado

**Ordenação de endereços:** - **Histórico:** routers muito antigos exigiam endereços ordenados pelo SHA-256 de seus dados - **Atual:** Ordenação NÃO é necessária, não vale a pena implementar por compatibilidade - Os endereços podem estar em qualquer ordem

**Campo Tamanho de Par (Histórico):** - **Sempre 0** no I2P moderno - Era destinado a rotas restritas (não implementado) - Se implementado, seria seguido por esse número de Router Hashes - Algumas implementações antigas podem ter exigido uma lista de pares ordenada

**Mapeamento de Opções:**

As opções DEVEM ser ordenadas por chave. As opções padrão incluem:

**Opções de capacidade:**

```
"caps" = Capability string
         Common values:
           f = Floodfill (network database)
           L or M or N or O = Bandwidth tier (L=lowest, O=highest)
           R = Reachable
           U = Unreachable/firewalled
           Example: "fLRU" = Floodfill, Low bandwidth, Reachable, Unreachable
```
**Opções de Rede:**

```
"netId" = Network ID (default "2" for main I2P network)
          Different values for test networks

"router.version" = I2P version string
                   Example: "0.9.67" or "2.10.0"
```
**Opções estatísticas:**

```
"stat_uptime" = Uptime in milliseconds
"coreVersion" = Core I2P version
"router.version" = Full router version string
```
Consulte a [documentação do RouterInfo do Banco de Dados da Rede](/docs/specs/common-structures/#routerInfo) para a lista completa de opções padrão.

**Cálculo da Assinatura:**

```
Data to sign: Complete RouterInfo structure from router_ident through options

Verification:
1. Extract RouterIdentity from RouterInfo
2. Get SigningPublicKey from RouterIdentity (type determines algorithm)
3. Verify signature over all data preceding signature field
4. Signature must match signing key type and length
```
**RouterInfo moderno típico (estrutura de informações do router):**

```
RouterIdentity: 391 bytes (X25519+EdDSA with Key Certificate)
Published: 8 bytes
Size: 1 byte (typically 1-4 addresses)
RouterAddress × N: Variable (typically 200-500 bytes each)
Peer Size: 1 byte (value=0)
Options: Variable (typically 50-200 bytes)
Signature: 64 bytes (EdDSA)

Total: ~1000-2500 bytes typical
```
**Notas de implementação:**

1. **Vários endereços:**
   - Routers normalmente publicam 1-4 endereços
   - Variantes IPv4 e IPv6
   - Transportes SSU2 e/ou NTCP2
   - Cada endereço é independente

2. **Versionamento:**
   - Um RouterInfo (metadados do router) mais recente tem carimbo de data/hora `published` posterior
   - Routers republicam a cada ~2 horas ou quando os endereços mudam
   - Floodfills armazenam e difundem apenas a versão mais recente

3. **Validação:**
   - Verifique a assinatura antes de aceitar o RouterInfo (informações do router)
   - Verifique se o campo de expiração é composto apenas por zeros em cada RouterAddress (endereço do router)
   - Valide se o mapeamento de opções está ordenado por chave
   - Verifique se os tipos de certificado e de chave são conhecidos/suportados

4. **Base de Dados da Rede:**
   - Os floodfills armazenam RouterInfo indexados por Hash(RouterIdentity)
   - Armazenados por ~2 dias após a última publicação
   - Routers consultam os floodfills para descobrir outros Routers

**JavaDoc:** [RouterInfo](http://docs.i2p-projekt.de/javadoc/net/i2p/data/router/RouterInfo.html)

---

## Notas de Implementação

### Ordem de bytes (Endianness)

**Padrão: Big-Endian (ordem de bytes de rede)**

A maioria das estruturas do I2P usa ordem de bytes big-endian (byte mais significativo primeiro): - Todos os tipos inteiros (1-8 bytes) - Carimbos de data e hora - TunnelId - Prefixo de tamanho de String - Tipos e comprimentos de certificado - Códigos de tipo de chave - Campos de tamanho de mapeamento

**Exceção: Little-Endian (ordem de bytes onde o menos significativo vem primeiro)**

Os seguintes tipos de chave usam codificação **little-endian**: - **X25519** chaves de criptografia (tipo 4) - **EdDSA_SHA512_Ed25519** chaves de assinatura (tipo 7) - **EdDSA_SHA512_Ed25519ph** chaves de assinatura (tipo 8) - **RedDSA_SHA512_Ed25519** chaves de assinatura (tipo 11)

**Implementação:**

```java
// Big-endian (most structures)
int value = ((bytes[0] & 0xFF) << 24) | 
            ((bytes[1] & 0xFF) << 16) |
            ((bytes[2] & 0xFF) << 8) | 
            (bytes[3] & 0xFF);

// Little-endian (X25519, EdDSA, RedDSA)
int value = (bytes[0] & 0xFF) | 
            ((bytes[1] & 0xFF) << 8) |
            ((bytes[2] & 0xFF) << 16) | 
            ((bytes[3] & 0xFF) << 24);
```
### Versionamento de Estruturas

**Nunca presuma tamanhos fixos:**

Muitas estruturas têm tamanho variável: - RouterIdentity: 387+ bytes (nem sempre é 387) - Destination: 387+ bytes (nem sempre é 387) - LeaseSet2: Varia significativamente - Certificate: 3+ bytes

**Sempre leia os campos de tamanho:** - Tamanho do certificado nos bytes 1-2 - Tamanho do mapeamento no início - KeysAndCert sempre é calculado como 384 + 3 + certificate_length

**Verifique se há dados em excesso:** - Proibir dados residuais após estruturas válidas - Validar se os comprimentos dos certificados correspondem aos tipos de chave - Impor os comprimentos exatos esperados para tipos de tamanho fixo

### Recomendações atuais (outubro de 2025)

**Para novas identidades de router:**

```
Encryption: X25519 (type 4, 32 bytes)
Signing: EdDSA_SHA512_Ed25519 (type 7, 32 bytes)
Certificate: Key Certificate (type 5)
Total Size: 391 bytes
Padding: Compressible per [Proposal 161](/pt/proposals/161-ri-dest-padding/)
```
**Para novos destinos:**

```
Unused Public Key Field: 256 bytes random (compressible)
Signing: EdDSA_SHA512_Ed25519 (type 7, 32 bytes)
Certificate: Key Certificate (type 5)
Total Size: 391 bytes
Padding: Compressible per [Proposal 161](/pt/proposals/161-ri-dest-padding/)
```
**Para novos LeaseSets:**

```
Type: LeaseSet2 (type 3)
Encryption Keys: X25519 (type 4, 32 bytes)
Leases: At least 1, typically 3-5
Options: Include service records per [Proposal 167](/proposals/167-service-records/)
Signature: EdDSA (64 bytes)
```
**Para serviços criptografados:**

```
Type: EncryptedLeaseSet (type 5)
Blinding: RedDSA_SHA512_Ed25519 (type 11)
Inner LeaseSet: LeaseSet2 (type 3)
Rotation: Daily blinding key rotation
Authorization: Per-client encryption keys
```
### Funcionalidades obsoletas - Não utilizar

**Criptografia obsoleta:** - ElGamal (tipo 0) para Identidades de Router (obsoleto desde 0.9.58) - Criptografia ElGamal/AES+SessionTag (rótulo de sessão) (use ECIES-X25519)

**Assinaturas descontinuadas:** - DSA_SHA1 (tipo 0) para Identidades do Router (descontinuado em 0.9.58) - Variantes ECDSA (tipos 1-3) para novas implementações - Variantes RSA (tipos 4-6) exceto para arquivos SU3

**Formatos de Rede Obsoletos:** - LeaseSet tipo 1 (use LeaseSet2) - Lease (44 bytes, use Lease2) - Formato Original de Expiração do Lease

**Transportes obsoletos:** - NTCP (removido na versão 0.9.50) - SSU (removido na versão 2.4.0)

**Certificados obsoletos:** - HASHCASH (tipo 1) - HIDDEN (tipo 2) - SIGNED (tipo 3) - MULTIPLE (tipo 4)

### Considerações de Segurança

**Geração de Chaves:** - Use sempre geradores de números aleatórios criptograficamente seguros - Nunca reutilize chaves em diferentes contextos - Proteja as chaves privadas com controles de acesso apropriados - Apague com segurança o material das chaves da memória quando terminar

**Verificação de Assinaturas:** - Sempre verifique as assinaturas antes de confiar nos dados - Verifique se o tamanho da assinatura corresponde ao tipo de chave - Valide se os dados assinados incluem os campos esperados - Para mapeamentos ordenados, verifique a ordem de classificação antes de assinar/verificar

**Validação de carimbo de data/hora:** - Verifique se as datas/horários publicados são razoáveis (não muito no futuro) - Valide se as expirações dos leases (alocações temporárias de túnel) não estão vencidas - Considere a tolerância ao desvio de relógio (±30 segundos típico)

**Network Database:** - Validar todas as estruturas antes de armazenar - Aplicar limites de tamanho para evitar DoS - Limitar a taxa de consultas e publicações - Verificar se as chaves do banco de dados correspondem aos hashes das estruturas

### Notas de Compatibilidade

**Compatibilidade com versões anteriores:** - ElGamal e DSA_SHA1 ainda são suportados para routers legados - Tipos de chave obsoletos continuam funcionais, mas são desaconselhados - Preenchimento compressível ([Proposal 161](/pt/proposals/161-ri-dest-padding/)) é retrocompatível até a versão 0.6

**Compatibilidade futura:** - Tipos de chave desconhecidos podem ser analisados usando campos de comprimento - Tipos de certificado desconhecidos podem ser ignorados usando o comprimento - Tipos de assinatura desconhecidos devem ser tratados de forma adequada - Implementadores não devem falhar diante de recursos opcionais desconhecidos

**Estratégias de migração:** - Suportar tanto tipos de chave antigos quanto novos durante a transição - LeaseSet2 pode listar várias chaves de criptografia - Assinaturas offline permitem rotação segura de chaves - MetaLeaseSet permite migração transparente de serviços

### Testes e Validação

**Validação da Estrutura:** - Verifique se todos os campos de tamanho estão dentro dos intervalos esperados - Verifique se estruturas de tamanho variável são analisadas corretamente - Valide se as assinaturas são verificadas com sucesso - Teste com estruturas de tamanho mínimo e máximo

**Casos limite:** - Strings de comprimento zero - Mapeamentos vazios - Número mínimo e máximo de leases (descritor de túnel de entrada do I2P) - Certificado com carga útil de comprimento zero - Estruturas muito grandes (próximas aos tamanhos máximos)

**Interoperabilidade:** - Testar contra a implementação oficial do I2P em Java - Verificar a compatibilidade com i2pd - Testar com vários conteúdos do banco de dados da rede - Validar contra vetores de teste conhecidos como válidos

---

## Referências

### Especificações

- [Protocolo I2NP](/docs/specs/i2np/)
- [Protocolo I2CP](/docs/specs/i2cp/)
- [Transporte SSU2](/docs/specs/ssu2/)
- [Transporte NTCP2](/docs/specs/ntcp2/)
- [Protocolo de Tunnel](/docs/specs/implementation/)
- [Protocolo de Datagramas](/docs/api/datagrams/)

### Criptografia

- [Visão geral da criptografia](/docs/specs/cryptography/)
- [Criptografia ElGamal/AES](/docs/legacy/elgamal-aes/)
- [Criptografia ECIES-X25519](/docs/specs/ecies/)
- [ECIES para Routers](/docs/specs/ecies/#routers)
- [ECIES híbrido (pós-quântico)](/docs/specs/ecies/#hybrid)
- [Assinaturas Red25519](/docs/specs/red25519-signature-scheme/)
- [LeaseSet criptografado](/docs/specs/encryptedleaseset/)

### Propostas

- [Proposta 123: Novas entradas no netDB](/proposals/123-new-netdb-entries/)
- [Proposta 134: Tipos de assinatura GOST](/proposals/134-gost/)
- [Proposta 136: Tipos de assinatura experimentais](/proposals/136-experimental-sigtypes/)
- [Proposta 145: ECIES-P256](/proposals/145-ecies/)
- [Proposta 156: ECIES Routers](/proposals/156-ecies-routers/)
- [Proposta 161: Geração de Padding (preenchimento)](/pt/proposals/161-ri-dest-padding/)
- [Proposta 167: Registros de serviço](/proposals/167-service-records/)
- [Proposta 169: Criptografia pós-quântica](/proposals/169-pq-crypto/)
- [Índice de todas as propostas](/proposals/)

### Banco de Dados da Rede

- [Visão geral do banco de dados da rede](/docs/specs/common-structures/)
- [Opções padrão do RouterInfo](/docs/specs/common-structures/#routerInfo)

### Referência da API do JavaDoc

- [Pacote de dados do núcleo](http://docs.i2p-projekt.de/javadoc/net/i2p/data/)
- [PublicKey](http://docs.i2p-projekt.de/javadoc/net/i2p/data/PublicKey.html)
- [PrivateKey](http://docs.i2p-projekt.de/javadoc/net/i2p/data/PrivateKey.html)
- [SessionKey](http://docs.i2p-projekt.de/javadoc/net/i2p/data/SessionKey.html)
- [SigningPublicKey](http://docs.i2p-projekt.de/javadoc/net/i2p/data/SigningPublicKey.html)
- [SigningPrivateKey](http://docs.i2p-projekt.de/javadoc/net/i2p/data/SigningPrivateKey.html)
- [Signature](http://docs.i2p-projekt.de/javadoc/net/i2p/data/Signature.html)
- [Hash](http://docs.i2p-projekt.de/javadoc/net/i2p/data/Hash.html)
- [SessionTag](http://docs.i2p-projekt.de/javadoc/net/i2p/data/SessionTag.html)
- [TunnelId](http://docs.i2p-projekt.de/javadoc/net/i2p/data/TunnelId.html)
- [Certificate](http://docs.i2p-projekt.de/javadoc/net/i2p/data/Certificate.html)
- [DataHelper](http://docs.i2p-projekt.de/javadoc/net/i2p/data/DataHelper.html)
- [KeysAndCert](http://docs.i2p-projekt.de/javadoc/net/i2p/data/KeysAndCert.html)
- [RouterIdentity](http://docs.i2p-projekt.de/javadoc/net/i2p/data/router/RouterIdentity.html)
- [Destination](http://docs.i2p-projekt.de/javadoc/net/i2p/data/Destination.html)
- [Lease](http://docs.i2p-projekt.de/javadoc/net/i2p/data/Lease.html)
- [LeaseSet](http://docs.i2p-projekt.de/javadoc/net/i2p/data/LeaseSet.html)
- [Lease2](http://docs.i2p-projekt.de/javadoc/net/i2p/data/Lease2.html)
- [LeaseSet2](http://docs.i2p-projekt.de/javadoc/net/i2p/data/LeaseSet2.html)
- [MetaLease](http://docs.i2p-projekt.de/javadoc/net/i2p/data/MetaLease.html)
- [MetaLeaseSet](http://docs.i2p-projekt.de/javadoc/net/i2p/data/MetaLeaseSet.html)
- [EncryptedLeaseSet](http://docs.i2p-projekt.de/javadoc/net/i2p/data/EncryptedLeaseSet.html)
- [RouterAddress](http://docs.i2p-projekt.de/javadoc/net/i2p/data/router/RouterAddress.html)
- [RouterInfo](http://docs.i2p-projekt.de/javadoc/net/i2p/data/router/RouterInfo.html)

### Padrões Externos

- **RFC 7748 (X25519):** Curvas elípticas para segurança
- **RFC 7539 (ChaCha20):** ChaCha20 e Poly1305 para protocolos da IETF
- **RFC 4648 (Base64):** As codificações de dados Base16, Base32 e Base64
- **FIPS 180-4 (SHA-256):** Padrão de Hash Seguro
- **FIPS 204 (ML-DSA):** Padrão de Assinatura Digital baseado em reticulados modulares
- [Registro de Serviços da IANA](http://www.dns-sd.org/ServiceTypes.html)

### Recursos da comunidade

- [Site do I2P](/)
- [Fórum do I2P](https://i2pforum.net)
- [GitLab do I2P](https://i2pgit.org/I2P_Developers/i2p.i2p)
- [Espelho do I2P no GitHub](https://github.com/i2p/i2p.i2p)
- [Índice da Documentação Técnica](/docs/)

### Informações de lançamento

- [Lançamento do I2P 2.10.0](/pt/blog/2025/09/08/i2p-2.10.0-release/)
- [Histórico de lançamentos](https://github.com/i2p/i2p.i2p/blob/master/history.txt)
- [Registro de alterações](https://github.com/i2p/i2p.i2p/blob/master/debian/changelog)

---

## Apêndice: Tabelas de Referência Rápida

### Referência Rápida de Tipos de Chave

**Padrão atual (recomendado para todas as novas implementações):** - **Criptografia:** X25519 (tipo 4, 32 bytes, little-endian) - **Assinatura:** EdDSA_SHA512_Ed25519 (tipo 7, 32 bytes, little-endian)

**Legado (suportado, mas obsoleto):** - **Criptografia:** ElGamal (tipo 0, 256 bytes, big-endian) - **Assinatura:** DSA_SHA1 (tipo 0, 20 bytes (privada) / 128 bytes (pública), big-endian)

**Especializado:** - **Assinatura (LeaseSet criptografado):** RedDSA_SHA512_Ed25519 (tipo 11, 32 bytes, little-endian)

**Pós-quântico (Beta, não finalizado):** - **Criptografia híbrida:** variantes MLKEM_X25519 (tipos 5-7) - **Criptografia pós-quântica pura:** variantes MLKEM (ainda sem códigos de tipo atribuídos)

### Referência rápida de tamanhos de estruturas

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Structure</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Minimum Size</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Typical Size</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Maximum Size</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Integer</td><td style="border:1px solid var(--color-border); padding:0.5rem;">1 byte</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Varies</td><td style="border:1px solid var(--color-border); padding:0.5rem;">8 bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Date</td><td style="border:1px solid var(--color-border); padding:0.5rem;">8 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">8 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">8 bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">String</td><td style="border:1px solid var(--color-border); padding:0.5rem;">1 byte</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Varies</td><td style="border:1px solid var(--color-border); padding:0.5rem;">256 bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">SessionKey</td><td style="border:1px solid var(--color-border); padding:0.5rem;">32 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">32 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">32 bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Hash</td><td style="border:1px solid var(--color-border); padding:0.5rem;">32 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">32 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">32 bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">TunnelId</td><td style="border:1px solid var(--color-border); padding:0.5rem;">4 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">4 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">4 bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Certificate</td><td style="border:1px solid var(--color-border); padding:0.5rem;">3 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">7 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">65,538 bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">KeysAndCert</td><td style="border:1px solid var(--color-border); padding:0.5rem;">387 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">391 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈1000+ bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RouterIdentity</td><td style="border:1px solid var(--color-border); padding:0.5rem;">387 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">391 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈1000+ bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Destination</td><td style="border:1px solid var(--color-border); padding:0.5rem;">387 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">391 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈1000+ bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Lease</td><td style="border:1px solid var(--color-border); padding:0.5rem;">44 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">44 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">44 bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Lease2</td><td style="border:1px solid var(--color-border); padding:0.5rem;">40 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">40 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">40 bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">LeaseSet</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈1000 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈1200 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈2000+ bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">LeaseSet2</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈500 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈800 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈2000+ bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">EncryptedLeaseSet</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈600 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈1000 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈3000+ bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RouterAddress</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈150 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈300 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈600 bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RouterInfo</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈1000 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈1500 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈3000+ bytes</td></tr>
  </tbody>
</table>
### Referência rápida de tipos de banco de dados

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Structure</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Status</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem;">RouterInfo</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Stored under Hash(RouterIdentity)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td><td style="border:1px solid var(--color-border); padding:0.5rem;">LeaseSet</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Use LeaseSet2 instead</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td><td style="border:1px solid var(--color-border); padding:0.5rem;">LeaseSet2</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Stored under Hash(Destination)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">5</td><td style="border:1px solid var(--color-border); padding:0.5rem;">EncryptedLeaseSet</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Stored under Hash(Blinded Destination)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">7</td><td style="border:1px solid var(--color-border); padding:0.5rem;">MetaLeaseSet</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Defined</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Verify production status</td></tr>
  </tbody>
</table>
### Referência Rápida do Protocolo de Transporte

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Protocol</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Status</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Port Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Since</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">SSU2</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td><td style="border:1px solid var(--color-border); padding:0.5rem;">UDP</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.54</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Default since 0.9.56</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">NTCP2</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td><td style="border:1px solid var(--color-border); padding:0.5rem;">TCP</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.36</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">SSU</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Removed</td><td style="border:1px solid var(--color-border); padding:0.5rem;">UDP</td><td style="border:1px solid var(--color-border); padding:0.5rem;">-</td><td style="border:1pxsolid var(--color-border); padding:0.5rem;">Removed in 2.4.0</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">NTCP</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Removed</td><td style="border:1px solid var(--color-border); padding:0.5rem;">TCP</td><td style="border:1px solid var(--color-border); padding:0.5rem;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Removed in 0.9.50</td></tr>
  </tbody>
</table>
### Referência rápida de marcos de versão

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Version</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">API</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Date</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Key Changes</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">0.6</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.6.x</td><td style="border:1px solid var(--color-border); padding:0.5rem;">2005</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Destination encryption disabled</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Dec 2013</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Key Certificates introduced</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.15</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.15</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Sep 2015</td><td style="border:1px solid var(--color-border); padding:0.5rem;">EdDSA support added</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.16</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.16</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Nov 2015</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Router Key Certificates</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.36</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.36</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Aug 2018</td><td style="border:1px solid var(--color-border); padding:0.5rem;">NTCP2 introduced</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.38</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.38</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Nov 2018</td><td style="border:1px solid var(--color-border); padding:0.5rem;">LeaseSet2, X25519 for Destinations</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.39</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.39</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Dec 2018</td><td style="border:1px solid var(--color-border); padding:0.5rem;">EncryptedLeaseSet working</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.48</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.48</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Jul 2020</td><td style="border:1px solid var(--color-border); padding:0.5rem;">X25519 for Router Identities</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.50</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.50</td><td style="border:1px solid var(--color-border); padding:0.5rem;">May 2021</td><td style="border:1px solid var(--color-border); padding:0.5rem;">NTCP removed</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.54</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.54</td><td style="border:1px solid var(--color-border); padding:0.5rem;">May 2022</td><td style="border:1px solid var(--color-border); padding:0.5rem;">SSU2 testing</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.57</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.57</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Jan 2023</td><td style="border:1px solid var(--color-border); padding:0.5rem;">[Proposal 161](/pt/proposals/161-ri-dest-padding/) padding (release 2.1.0)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.58</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.58</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Mar 2023</td><td style="border:1px solid var(--color-border); padding:0.5rem;">ElGamal/DSA deprecated for RIs (2.2.0)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.66</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.66</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Jun 2025</td><td style="border:1px solid var(--color-border); padding:0.5rem;">[Proposal 167](/proposals/167-service-records/) service records (2.9.0)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Sep 2025</td><td style="border:1px solid var(--color-border); padding:0.5rem;">ML-KEM beta support (2.10.0)</td></tr>
  </tbody>
</table>
---
