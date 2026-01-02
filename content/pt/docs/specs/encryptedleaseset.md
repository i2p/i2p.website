---
title: "LeaseSet criptografado"
description: "Formato de LeaseSet com controle de acesso para Destinations (destinos no I2P) privadas"
slug: "encryptedleaseset"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

## Visão geral

Este documento especifica o blinding (cegamento criptográfico), a criptografia e a descriptografia de LeaseSet2 (LS2) criptografado. LeaseSets criptografados fornecem a publicação com controle de acesso de informações de serviços ocultos no banco de dados de rede do I2P.

**Principais recursos:** - Rotação diária de chaves para sigilo futuro - Autorização de clientes em dois níveis (baseada em DH e em PSK) - Criptografia ChaCha20 para desempenho em dispositivos sem hardware AES - Assinaturas Red25519 com cegamento de chaves - Associação de clientes com preservação de privacidade

**Documentação relacionada:** - [Especificação de Estruturas Comuns](/docs/specs/common-structures/) - Estrutura de LeaseSet (conjunto de informações de roteamento de entrada) criptografado - [Proposta 123: Novas entradas no netDB (banco de dados da rede)](/proposals/123-new-netdb-entries/) - Contexto sobre LeaseSets criptografados - [Documentação do NetDB](/docs/specs/common-structures/) - Uso do NetDB

---

## Histórico de versões e status de implementação

### Linha do tempo do desenvolvimento do protocolo

**Nota importante sobre a numeração de versões:**   O I2P usa dois esquemas distintos de numeração de versões: - **Versão da API/Router:** série 0.9.x (usada nas especificações técnicas) - **Versão de Lançamento do Produto:** série 2.x.x (usada para lançamentos públicos)

As especificações técnicas fazem referência às versões da API (por exemplo, 0.9.41), enquanto os utilizadores finais veem as versões do produto (por exemplo, 2.10.0).

### Marcos de Implementação

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Version</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Release Date</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Features</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.38</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">January 2019</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Floodfill support for standard LS2, offline keys</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.39</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">March 2019</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Full encrypted LS2 support, Red25519 (sig type&nbsp;11)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.40</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">May 2019</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Per-client authorization, encrypted LS2 with offline keys, B32 support</strong></td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.41</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">June 2019</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Protocol finalized as stable</strong></td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>2.10.0</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">September 2025</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Latest Java implementation (API version 0.9.61)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>i2pd 2.58.0</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">September 2025</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Full C++ implementation compatibility</td></tr>
  </tbody>
</table>
### Estado atual

- ✅ **Status do protocolo:** Estável e inalterado desde junho de 2019
- ✅ **Java I2P:** Totalmente implementado a partir da versão 0.9.40+
- ✅ **i2pd (C++):** Totalmente implementado a partir da versão 2.58.0+
- ✅ **Interoperabilidade:** Completa entre as implementações
- ✅ **Implantação na rede:** Pronta para produção, com mais de 6 anos de experiência operacional

---

## Definições Criptográficas

### Notação e Convenções

- `||` denota concatenação
- `mod L` denota a redução modular pela ordem do Ed25519
- Todos os arrays de bytes estão em ordem de bytes de rede (big-endian), a menos que especificado de outra forma
- Valores little-endian são indicados explicitamente

### gerador de números aleatórios criptograficamente seguro (CSRNG)(n)

**Gerador de números aleatórios criptograficamente seguro**

Produz `n` bytes de dados aleatórios criptograficamente seguros, adequados para a geração de material de chave.

**Requisitos de Segurança:** - Deve ser criptograficamente seguro (adequado para a geração de chaves) - Deve ser seguro quando sequências de bytes adjacentes são expostas na rede - As implementações deveriam aplicar hash na saída proveniente de fontes potencialmente não confiáveis

**Referências:** - [Considerações de segurança sobre PRNG](http://projectbullrun.org/dual-ec/ext-rand.html) - [Discussão dos desenvolvedores do Tor](https://lists.torproject.org/pipermail/tor-dev/2015-November/009954.html)

### H(p, d)

**Hash SHA-256 com personalização**

Função de hash com separação de domínios que recebe: - `p`: string de personalização (fornece separação de domínios) - `d`: dados a serem processados pelo hash

**Implementação:**

```
H(p, d) := SHA-256(p || d)
```
**Uso:** Fornece separação de domínios criptográfica para evitar ataques de colisão entre diferentes utilizações do SHA-256 em protocolos.

### FLUXO: ChaCha20

**Cifra de fluxo: ChaCha20 conforme especificado na RFC 7539 Seção 2.4**

**Parâmetros:** - `S_KEY_LEN = 32` (chave de 256 bits) - `S_IV_LEN = 12` (nonce de 96 bits) - Contador inicial: `1` (A RFC 7539 permite 0 ou 1; 1 é recomendado para contextos AEAD (criptografia autenticada com dados associados))

**CIFRAR(k, iv, plaintext)**

Cifra o texto em claro usando: - `k`: chave de cifra de 32 bytes - `iv`: nonce (valor único usado uma vez) de 12 bytes (DEVE ser único para cada chave) - Retorna texto cifrado do mesmo tamanho que o texto em claro

**Propriedade de segurança:** Todo o texto cifrado deve ser indistinguível de dados aleatórios se a chave for secreta.

**DECIFRAR(k, iv, ciphertext)**

Descriptografa o texto cifrado usando: - `k`: chave de cifra de 32 bytes - `iv`: nonce (número usado uma vez) de 12 bytes - Retorna o texto em claro

**Justificativa de design:** ChaCha20 foi escolhido em vez de AES porque: - 2.5-3x mais rápido que AES em dispositivos sem aceleração por hardware - Implementação em tempo constante mais fácil de obter - Segurança e velocidade comparáveis quando o AES-NI está disponível

**Referências:** - [RFC 7539](https://datatracker.ietf.org/doc/html/rfc7539) - ChaCha20 e Poly1305 para Protocolos do IETF

### Assinatura: Red25519 (variante do Ed25519 usando o esquema RedDSA)

**Esquema de Assinatura: Red25519 (SigType 11) com Cegamento de Chave**

Red25519 é baseado em assinaturas Ed25519 sobre a curva Ed25519, usando SHA-512 para hash, com suporte a key blinding (cegamento de chave) conforme especificado em ZCash RedDSA.

**Funções:**

#### DERIVE_PUBLIC(privkey)

Retorna a chave pública correspondente à chave privada fornecida. - Usa a multiplicação escalar padrão do Ed25519 pelo ponto base

#### SIGN(privkey, m)

Retorna uma assinatura da mensagem `m` gerada pela chave privada `privkey`.

**Diferenças de assinatura do Red25519 em relação ao Ed25519:** 1. **Nonce aleatório:** Usa 80 bytes de dados aleatórios adicionais

   ```
   T = CSRNG(80)  // 80 random bytes
   r = H*(T || publickey || message)
   ```
Isso torna cada assinatura Red25519 única, mesmo para a mesma mensagem e chave.

2. **Geração de chaves privadas:** chaves privadas Red25519 são geradas a partir de números aleatórios e reduzidas `mod L`, em vez de usar a abordagem de "bit-clamping" (fixação de bits) do Ed25519.

#### VERIFY(pubkey, m, sig)

Verifica a assinatura `sig` contra a chave pública `pubkey` e a mensagem `m`. - Retorna `true` se a assinatura for válida, `false` caso contrário - A verificação é idêntica à de Ed25519

**Operações de Cegamento de Chaves:**

#### GENERATE_ALPHA(data, secret)

Gera alpha para cegamento de chave. - `data`: Normalmente contém a chave pública de assinatura e os tipos de assinatura - `secret`: Segredo adicional opcional (comprimento zero se não for usado) - O resultado é distribuído de forma idêntica às chaves privadas Ed25519 (após a redução módulo L)

#### BLIND_PRIVKEY(privkey, alpha)

Aplica cegamento a uma chave privada utilizando o segredo `alpha`. - Implementação: `blinded_privkey = (privkey + alpha) mod L` - Usa aritmética escalar no campo

#### BLIND_PUBKEY(pubkey, alpha)

Cega uma chave pública usando o segredo `alpha`. - Implementação: `blinded_pubkey = pubkey + DERIVE_PUBLIC(alpha)` - Usa a adição de elementos do grupo (ponto) na curva

**Propriedade crítica:**

```
BLIND_PUBKEY(pubkey, alpha) == DERIVE_PUBLIC(BLIND_PRIVKEY(privkey, alpha))
```
**Considerações de segurança:**

Da Seção 5.4.6.1 da Especificação do Protocolo ZCash: Por segurança, alpha deve ter distribuição idêntica à das chaves privadas sem cegamento. Isso garante que "a combinação de uma chave pública re-randomizada e assinatura(s) sob essa chave não revela a chave a partir da qual ela foi re-randomizada."

**Tipos de assinatura suportados:** - **Tipo 7 (Ed25519):** Suportado para destinos existentes (compatibilidade com versões anteriores) - **Tipo 11 (Red25519):** Recomendado para novos destinos que usam criptografia - **Blinded keys (chaves cegas):** Sempre use o tipo 11 (Red25519)

**Referências:** - [Especificação do Protocolo ZCash](https://zips.z.cash/protocol/protocol.pdf) - Seção 5.4.6 RedDSA - [Especificação Red25519 do I2P](/docs/specs/red25519-signature-scheme/)

### DH: X25519

**Diffie-Hellman de Curva Elíptica: X25519**

Sistema de acordo de chaves públicas baseado na Curve25519 (curva elíptica).

**Parâmetros:** - Chaves privadas: 32 bytes - Chaves públicas: 32 bytes - Saída do segredo compartilhado: 32 bytes

**Funções:**

#### GENERATE_PRIVATE()

Gera uma nova chave privada de 32 bytes usando CSRNG (gerador de números aleatórios criptograficamente seguro).

#### DERIVE_PUBLIC(privkey)

Deriva a chave pública de 32 bytes a partir da chave privada fornecida. - Utiliza multiplicação escalar na Curve25519 (uma curva elíptica)

#### DH(privkey, pubkey)

Realiza o acordo de chaves Diffie-Hellman. - `privkey`: Chave privada local de 32 bytes - `pubkey`: Chave pública remota de 32 bytes - Retorna: Segredo compartilhado de 32 bytes

**Propriedades de Segurança:** - Hipótese de Diffie-Hellman computacional na Curve25519 - Sigilo de encaminhamento quando chaves efêmeras são usadas - Implementação em tempo constante necessária para prevenir ataques de temporização

**Referências:** - [RFC 7748](https://datatracker.ietf.org/doc/html/rfc7748) - Curvas Elípticas para Segurança

### HKDF (função de derivação de chaves baseada em HMAC)

**Função de Derivação de Chaves baseada em HMAC**

Extrai e expande o material de chave a partir do material de chave de entrada.

**Parâmetros:** - `salt`: máximo de 32 bytes (normalmente 32 bytes para SHA-256) - `ikm`: material de chave de entrada (qualquer comprimento, deve ter boa entropia) - `info`: informação específica do contexto (separação de domínios) - `n`: comprimento da saída em bytes

**Implementação:**

Utiliza HKDF (função de derivação de chaves baseada em HMAC) conforme especificado na RFC 5869 com: - **Função de hash:** SHA-256 - **HMAC:** Conforme especificado na RFC 2104 - **Comprimento do sal:** Máximo de 32 bytes (HashLen para SHA-256)

**Padrão de uso:**

```
keys = HKDF(salt, ikm, info, n)
```
**Separação de domínios:** O parâmetro `info` fornece separação de domínios criptográfica entre diferentes usos do HKDF (função de derivação de chaves baseada em HMAC) no protocolo.

**Valores de Informações Verificados:** - `"ELS2_L1K"` - criptografia da camada 1 (externa) - `"ELS2_L2K"` - criptografia da camada 2 (interna) - `"ELS2_XCA"` - autorização do cliente DH - `"ELS2PSKA"` - autorização do cliente PSK - `"i2pblinding1"` - geração alfa

**Referências:** - [RFC 5869](https://datatracker.ietf.org/doc/html/rfc5869) - Especificação do HKDF - [RFC 2104](https://datatracker.ietf.org/doc/html/rfc2104) - Especificação do HMAC

---

## Especificação de Formato

LS2 criptografado consiste em três camadas aninhadas:

1. **Camada 0 (Externa):** Informações em texto claro para armazenamento e recuperação
2. **Camada 1 (Intermediária):** Dados de autenticação do cliente (criptografados)
3. **Camada 2 (Interna):** Dados efetivos do LeaseSet2 (criptografados)

**Estrutura geral:**

```
Layer 0 data + Enc(layer 1 data + Enc(layer 2 data)) + Signature
```
**Importante:** O LS2 criptografado usa chaves cegadas. A Destination não está no cabeçalho. O local de armazenamento na DHT é `SHA-256(sig type || blinded public key)`, com rotação diária.

### Camada 0 (Externa) - Texto em claro

A Camada 0 NÃO usa o cabeçalho LS2 padrão. Ela tem um formato personalizado otimizado para chaves cegadas.

**Estrutura:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Field</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Size</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Type</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1 byte</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Not in header, from DatabaseStore message field</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Blinded Public Key Sig Type</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big endian, always <code>0x000b</code> (Red25519 type 11)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Blinded Public Key</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Red25519 blinded public key</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Published Timestamp</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big endian, seconds since epoch (rolls over in 2106)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Expires</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big endian, offset from published in seconds (max 65,535 &asymp; 18.2 hours)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Flags</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Bit flags (see below)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">[Optional] Transient Key Data</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Variable</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Present if flag bit&nbsp;0 is set</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">lenOuterCiphertext</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big endian, length of outer ciphertext</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">outerCiphertext</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">lenOuterCiphertext</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Encrypted Layer&nbsp;1 data</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Signature</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">64 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Red25519 signature over all preceding data</td></tr>
  </tbody>
</table>
**Campo de Flags (2 bytes, bits 15-0):** - **Bit 0:** indicador de chaves offline   - `0` = Sem chaves offline   - `1` = Chaves offline presentes (dados de chaves transitórios a seguir) - **Bits 1-15:** Reservados, devem ser 0 para compatibilidade futura

**Dados de chave transitória (presente se o bit de flag 0 = 1):**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Field</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Size</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Expires Timestamp</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big endian, seconds since epoch</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Transient Sig Type</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big endian, signature type</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Transient Signing Public Key</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Variable</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Length implied by signature type</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Signature</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">64 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Signed by blinded public key; covers expires timestamp, transient sig type, and transient public key</td></tr>
  </tbody>
</table>
**Verificação de assinatura:** - **Sem chaves offline:** Verifique com chave pública cega - **Com chaves offline:** Verifique com chave pública temporária

A assinatura abrange todos os dados de Type até outerCiphertext (inclusive).

### Camada 1 (Intermediária) - Autorização do Cliente

**Descriptografia:** Consulte a seção [Criptografia da Camada 1](#layer-1-encryption).

**Estrutura:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Field</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Size</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Flags</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1 byte</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Authorization flags (see below)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">[Optional] Auth Data</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Variable</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Present based on flags</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">innerCiphertext</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Variable</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Encrypted Layer&nbsp;2 data (remainder)</td></tr>
  </tbody>
</table>
**Campo de flags (1 byte, bits 7-0):** - **Bit 0:** Modo de autorização   - `0` = Sem autorização por cliente (todos)   - `1` = Autorização por cliente (a seção de autenticação vem a seguir) - **Bits 3-1:** Esquema de autenticação (somente se o bit 0 = 1)   - `000` = autenticação de cliente DH   - `001` = autenticação de cliente PSK   - Outros reservados - **Bits 7-4:** Não utilizados, devem ser 0

**Dados de Autorização do Cliente DH (flags = 0x01, bits 3-1 = 000):**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Field</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Size</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ephemeralPublicKey</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Server's ephemeral X25519 public key</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">clients</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big endian, number of client entries</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">authClient[]</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">40 bytes each</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Array of client authorization entries</td></tr>
  </tbody>
</table>
**Entrada authClient (40 bytes):** - `clientID_i`: 8 bytes - `clientCookie_i`: 32 bytes (authCookie criptografado)

**Dados de Autorização do Cliente com PSK (flags = 0x03, bits 3-1 = 001):**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Field</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Size</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">authSalt</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Salt for PSK key derivation</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">clients</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big endian, number of client entries</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">authClient[]</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">40 bytes each</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Array of client authorization entries</td></tr>
  </tbody>
</table>
**Entrada authClient (40 bytes):** - `clientID_i`: 8 bytes - `clientCookie_i`: 32 bytes (authCookie criptografado)

### Camada 2 (Interna) - Dados do LeaseSet

**Descriptografia:** Consulte a seção [Criptografia da Camada 2](#layer-2-encryption).

**Estrutura:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Field</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Size</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Type</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1 byte</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>3</code> (LS2) or <code>7</code> (Meta LS2)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Data</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Variable</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Complete LeaseSet2 or MetaLeaseSet2</td></tr>
  </tbody>
</table>
A camada interna contém a estrutura completa do LeaseSet2, incluindo: - cabeçalho LS2 - informações de Lease (registro de um tunnel com expiração no I2P) - assinatura LS2

**Requisitos de Verificação:** Após a descriptografia, as implementações devem verificar: 1. O carimbo de data/hora interno corresponde ao carimbo de data/hora externo publicado 2. A expiração interna corresponde à expiração externa 3. A assinatura do LS2 (versão 2 do LeaseSet) é válida 4. Os dados de Lease estão bem formados

**Referências:** - [Especificação de Estruturas Comuns](/docs/specs/common-structures/) - detalhes do formato do LeaseSet2

---

## Derivação da Chave de Cegamento

### Visão geral

I2P usa um esquema aditivo de cegamento de chaves baseado em Ed25519 e ZCash RedDSA. As chaves cegadas são rotacionadas diariamente (à meia-noite UTC) para garantir sigilo perfeito futuro.

**Justificativa de Design:**

O I2P optou explicitamente por NÃO usar a abordagem do Apêndice A.2 do rend-spec-v3.txt do Tor. De acordo com a especificação:

> "Não usamos o apêndice A.2 do rend-spec-v3.txt do Tor, que tem objetivos de projeto semelhantes, porque, nele, as chaves públicas cegas podem estar fora do subgrupo de ordem prima, com implicações de segurança desconhecidas."

O cegamento aditivo do I2P garante que as chaves cegadas permaneçam no subgrupo de ordem prima da curva Ed25519.

### Definições Matemáticas

**Parâmetros do Ed25519:** - `B`: ponto base do Ed25519 (gerador) = `2^255 - 19` - `L`: ordem do Ed25519 = `2^252 + 27742317777372353535851937790883648493`

**Variáveis-chave:** - `A`: Chave pública de assinatura de 32 bytes não cegada (em Destination) - `a`: Chave privada de assinatura de 32 bytes não cegada - `A'`: Chave pública de assinatura de 32 bytes cegada (usada em LeaseSet criptografado) - `a'`: Chave privada de assinatura de 32 bytes cegada - `alpha`: Fator de cegamento de 32 bytes (secreto)

**Funções auxiliares:**

#### LEOS2IP(x)

"Cadeia de octetos Little-Endian (ordem de bytes do menos significativo primeiro) para inteiro"

Converte um array de bytes em little-endian para representação inteira.

#### H*(x)

"Hash e Redução"

```
H*(x) = (LEOS2IP(SHA512(x))) mod L
```
Mesma operação que na geração de chaves Ed25519.

### Geração Alfa

**Rotação diária:** Um novo alpha e chaves cegadas DEVEM ser gerados todos os dias à meia-noite UTC (00:00:00 UTC).

**GENERATE_ALPHA(destination, date, secret) Algoritmo:**

```python
# Input parameters
A = destination's signing public key (32 bytes)
stA = signature type of A (2 bytes, big endian)
     # 0x0007 for Ed25519 or 0x000b for Red25519
stA' = signature type of blinded key A' (2 bytes, big endian) 
     # Always 0x000b (Red25519)
datestring = "YYYYMMDD" (8 bytes ASCII from current UTC date)
secret = optional UTF-8 encoded string (zero-length if not used)

# Computation
keydata = A || stA || stA'  # 36 bytes total
seed = HKDF(
    salt=H("I2PGenerateAlpha", keydata),
    ikm=datestring || secret,
    info="i2pblinding1",
    n=64
)

# Treat seed as 64-byte little-endian integer and reduce
alpha = seed mod L
```
**Parâmetros verificados:** - Personalização do salt: "I2PGenerateAlpha" - Parâmetro info do HKDF (campo de contexto): "i2pblinding1" - Saída: 64 bytes antes da redução - Distribuição de Alpha: Idêntica à das chaves privadas Ed25519 após `mod L`

### Cegamento de chave privada

**Algoritmo BLIND_PRIVKEY(a, alpha):**

Para o proprietário do destino ao publicar o LeaseSet criptografado:

```python
# For Ed25519 private key (type 7)
if sigtype == 7:
    seed = destination's signing private key (32 bytes)
    a = left_half(SHA512(seed))  # 32 bytes
    a = clamp(a)  # Ed25519 clamping
    
# For Red25519 private key (type 11)
elif sigtype == 11:
    a = destination's signing private key (32 bytes)
    # No clamping for Red25519

# Additive blinding using scalar arithmetic
blinded_privkey = a' = (a + alpha) mod L

# Derive blinded public key
blinded_pubkey = A' = DERIVE_PUBLIC(a')
```
**Crítico:** A redução `mod L` é essencial para manter a relação algébrica correta entre a chave privada e a chave pública.

### Cegamento de Chave Pública

**Algoritmo BLIND_PUBKEY(A, alpha):**

Para clientes que recuperam e verificam o LeaseSet criptografado:

```python
alpha = GENERATE_ALPHA(destination, date, secret)
A = destination's signing public key (32 bytes)

# Additive blinding using group elements (curve points)
blinded_pubkey = A' = A + DERIVE_PUBLIC(alpha)
```
**Equivalência Matemática:**

Ambos os métodos produzem resultados idênticos:

```
BLIND_PUBKEY(A, alpha) == DERIVE_PUBLIC(BLIND_PRIVKEY(a, alpha))
```
Isso ocorre porque:

```
A' = A + [alpha]B
   = [a]B + [alpha]B
   = [a + alpha]B  (group operation)
   = DERIVE_PUBLIC(a + alpha mod L)
```
### Assinatura com Chaves Cegadas

**Assinatura de LeaseSet sem cegamento:**

O LeaseSet não cegado (enviado diretamente a clientes autenticados) é assinado usando: - Assinatura Ed25519 padrão (tipo 7) ou Red25519 (tipo 11) - Chave privada de assinatura não cegada - Verificado com a chave pública não cegada

**Com chaves offline:** - Assinado com chave privada transitória sem cegamento - Verificado com chave pública transitória sem cegamento - Ambas devem ser do tipo 7 ou 11

**Assinatura do LeaseSet criptografado:**

A parte externa do LeaseSet criptografado usa assinaturas Red25519 (variante aleatorizada do Ed25519) com chaves cegadas.

**Algoritmo de Assinatura Red25519:**

```python
# Generate per-signature random nonce
T = CSRNG(80)  # 80 random bytes

# Calculate r (differs from Ed25519)
r = H*(T || blinded_pubkey || message)

# Rest is same as Ed25519
R = [r]B
S = (r + H(R || A' || message) * a') mod L
signature = R || S  # 64 bytes total
```
**Principais diferenças em relação ao Ed25519:** 1. Usa 80 bytes de dados aleatórios `T` (não o hash da chave privada) 2. Usa o valor da chave pública diretamente (não o hash da chave privada) 3. Cada assinatura é única mesmo para a mesma mensagem e chave

**Verificação:**

Igual a Ed25519 (algoritmo de assinatura digital baseado em curva elíptica):

```python
# Parse signature
R = signature[0:32]
S = signature[32:64]

# Verify equation: [S]B = R + [H(R || A' || message)]A'
return [S]B == R + [H(R || A' || message)]A'
```
### Considerações de Segurança

**Distribuição Alfa:**

Por motivos de segurança, alpha deve ter a mesma distribuição que as chaves privadas não cegadas. Ao aplicar cegamento de Ed25519 (tipo 7) para Red25519 (tipo 11), as distribuições diferem ligeiramente.

**Recomendação:** Use Red25519 (tipo 11) para chaves descegadas e cegadas a fim de atender aos requisitos do ZCash: "a combinação de uma chave pública re-aleatorizada e de assinatura(s) sob essa chave não revela a chave a partir da qual foi re-aleatorizada."

**Suporte ao Tipo 7:** Ed25519 (algoritmo de assinatura EdDSA) é suportado para manter compatibilidade com versões anteriores em destinos existentes, mas o tipo 11 é recomendado para novos destinos criptografados.

**Benefícios da Rotação Diária:** - Sigilo futuro (forward secrecy): Comprometer a blinded key (chave cegada) de hoje não revela a de ontem - Não vinculabilidade: A rotação diária evita o rastreamento de longo prazo via DHT (tabela hash distribuída) - Separação de chaves: Chaves diferentes para períodos de tempo diferentes

**Referências:** - [Especificação do Protocolo ZCash](https://zips.z.cash/protocol/protocol.pdf) - Seção 5.4.6.1 - [Discussão sobre cegamento de chaves no Tor](https://lists.torproject.org/pipermail/tor-dev/2013-December/005943.html) - [Ticket do Tor nº 8106](https://trac.torproject.org/projects/tor/ticket/8106)

---

## Criptografia e Processamento

### Derivação de Subcredencial

Antes da criptografia, derivamos uma credencial e uma subcredencial para vincular as camadas criptografadas ao conhecimento da chave pública de assinatura do Destino.

**Objetivo:** Garantir que apenas aqueles que conhecem a chave pública de assinatura do Destino possam descriptografar o LeaseSet criptografado. O Destino completo não é necessário.

#### Cálculo de Credenciais

```python
A = destination's signing public key (32 bytes)
stA = signature type of A (2 bytes big endian)
     # 0x0007 for Ed25519 or 0x000b for Red25519
stA' = signature type of blinded key A' (2 bytes big endian)
     # Always 0x000b (Red25519)

keydata = A || stA || stA'  # 36 bytes

credential = H("credential", keydata)  # 32 bytes
```
**Separação de domínios:** A string de personalização `"credential"` garante que este hash não colida com quaisquer chaves de consulta da DHT ou outros usos do protocolo.

#### Cálculo da Subcredencial

```python
blindedPublicKey = A' (32 bytes, from blinding process)

subcredential = H("subcredential", credential || blindedPublicKey)  # 32 bytes
```
**Finalidade:** A subcredencial vincula o LeaseSet criptografado a: 1. A Destination (destino no I2P) específica (via credential) 2. A chave cegada específica (via blindedPublicKey) 3. O dia específico (via rotação diária de blindedPublicKey)

Isso impede ataques de repetição e vinculação entre dias.

### Criptografia da Camada 1

**Contexto:** A Camada 1 contém dados de autorização do cliente e é criptografada com uma chave derivada da subcredential (subcredencial).

#### Algoritmo de Criptografia

```python
# Prepare input
outerInput = subcredential || publishedTimestamp
# publishedTimestamp: 4 bytes from Layer 0

# Generate random salt
outerSalt = CSRNG(32)  # 32 bytes

# Derive encryption key and IV
keys = HKDF(
    salt=outerSalt,
    ikm=outerInput,
    info="ELS2_L1K",  # Domain separation
    n=44  # 32 bytes key + 12 bytes IV
)

outerKey = keys[0:31]    # 32 bytes (indices 0-31 inclusive)
outerIV = keys[32:43]    # 12 bytes (indices 32-43 inclusive)

# Encrypt and prepend salt
outerPlaintext = [Layer 1 data]
outerCiphertext = outerSalt || ENCRYPT(outerKey, outerIV, outerPlaintext)
```
**Saída:** `outerCiphertext` é de `32 + len(outerPlaintext)` bytes.

**Propriedades de Segurança:** - O salt garante pares exclusivos de chave/IV (vetor de inicialização) mesmo com a mesma subcredencial - A string de contexto `"ELS2_L1K"` fornece separação de domínios - ChaCha20 fornece segurança semântica (texto cifrado indistinguível de dados aleatórios)

#### Algoritmo de Descriptografia

```python
# Parse salt from ciphertext
outerSalt = outerCiphertext[0:31]  # First 32 bytes

# Derive decryption key and IV (same process as encryption)
outerInput = subcredential || publishedTimestamp
keys = HKDF(
    salt=outerSalt,
    ikm=outerInput,
    info="ELS2_L1K",
    n=44
)

outerKey = keys[0:31]    # 32 bytes
outerIV = keys[32:43]    # 12 bytes

# Decrypt (skip salt bytes)
outerPlaintext = DECRYPT(outerKey, outerIV, outerCiphertext[32:end])
```
**Verificação:** Após a descriptografia, verifique se a estrutura da Camada 1 está bem formada antes de prosseguir para a Camada 2.

### Criptografia da Camada 2

**Contexto:** A Camada 2 contém os dados efetivos de LeaseSet2 e é criptografada com uma chave derivada do authCookie (se a autenticação por cliente estiver ativada) ou uma string vazia (se não estiver).

#### Algoritmo de criptografia

```python
# Determine authCookie based on authorization mode
if per_client_auth_enabled:
    authCookie = [32-byte cookie from client authorization process]
else:
    authCookie = b''  # Zero-length byte array

# Prepare input
innerInput = authCookie || subcredential || publishedTimestamp

# Generate random salt
innerSalt = CSRNG(32)  # 32 bytes

# Derive encryption key and IV
keys = HKDF(
    salt=innerSalt,
    ikm=innerInput,
    info="ELS2_L2K",  # Domain separation
    n=44  # 32 bytes key + 12 bytes IV
)

innerKey = keys[0:31]    # 32 bytes
innerIV = keys[32:43]    # 12 bytes

# Encrypt and prepend salt
innerPlaintext = [Layer 2 data: LS2 type byte + LeaseSet2 data]
innerCiphertext = innerSalt || ENCRYPT(innerKey, innerIV, innerPlaintext)
```
**Saída:** `innerCiphertext` tem `32 + len(innerPlaintext)` bytes.

**Vinculação de chave:** - Se não houver autenticação do cliente: Vinculada apenas à subcredencial e ao carimbo de data/hora - Se a autenticação do cliente estiver ativada: Além disso vinculada a authCookie (diferente para cada cliente autorizado)

#### Algoritmo de descriptografia

```python
# Determine authCookie (same as encryption)
if per_client_auth_enabled:
    authCookie = [32-byte cookie from client authorization process]
else:
    authCookie = b''  # Zero-length byte array

# Parse salt from ciphertext
innerSalt = innerCiphertext[0:31]  # First 32 bytes

# Derive decryption key and IV
innerInput = authCookie || subcredential || publishedTimestamp
keys = HKDF(
    salt=innerSalt,
    ikm=innerInput,
    info="ELS2_L2K",
    n=44
)

innerKey = keys[0:31]    # 32 bytes
innerIV = keys[32:43]    # 12 bytes

# Decrypt (skip salt bytes)
innerPlaintext = DECRYPT(innerKey, innerIV, innerCiphertext[32:end])
```
**Verificação:** Após a descriptografia: 1. Verifique se o byte de tipo do LS2 é válido (3 ou 7) 2. Analisar a estrutura LeaseSet2 3. Verifique se o carimbo de data/hora interno corresponde ao carimbo de data/hora de publicação externo 4. Verifique se a expiração interna corresponde à expiração externa 5. Verifique a assinatura do LeaseSet2

### Resumo da Camada de Criptografia

```
┌─────────────────────────────────────────────────┐
│ Layer 0 (Plaintext)                             │
│ - Blinded public key                            │
│ - Timestamps                                    │
│ - Signature                                     │
│                                                 │
│  ┌─────────────────────────────────────────┐   │
│  │ Layer 1 (Encrypted with subcredential)  │   │
│  │ - Authorization flags                   │   │
│  │ - Client auth data (if enabled)         │   │
│  │                                          │   │
│  │  ┌────────────────────────────────┐     │   │
│  │  │ Layer 2 (Encrypted with        │     │   │
│  │  │          authCookie + subcred) │     │   │
│  │  │ - LeaseSet2 type               │     │   │
│  │  │ - LeaseSet2 data               │     │   │
│  │  │ - Leases                       │     │   │
│  │  │ - LS2 signature                │     │   │
│  │  └────────────────────────────────┘     │   │
│  └─────────────────────────────────────────┘   │
└─────────────────────────────────────────────────┘
```
**Fluxo de Descriptografia:** 1. Verifique a assinatura da Camada 0 com a chave pública cegada 2. Descriptografe a Camada 1 usando subcredential (subcredencial) 3. Processe os dados de autorização (se presentes) para obter o authCookie (cookie de autenticação) 4. Descriptografe a Camada 2 usando o authCookie e a subcredential 5. Verifique e analise o LeaseSet2

---

## Autorização por Cliente

### Visão geral

Quando a autorização por cliente está ativada, o servidor mantém uma lista de clientes autorizados. Cada cliente possui material de chave que deve ser transmitido com segurança fora de banda.

**Dois mecanismos de autorização:** 1. **Autorização de cliente DH (Diffie-Hellman):** Mais segura, usa acordo de chaves X25519 2. **Autorização por PSK (Pre-Shared Key, chave pré-compartilhada):** Mais simples, usa chaves simétricas

**Propriedades de Segurança Comuns:** - Privacidade de associação de clientes: observadores veem a contagem de clientes, mas não podem identificar clientes específicos - Adição/revogação anônima de clientes: não é possível rastrear quando clientes específicos são adicionados ou removidos - Probabilidade de colisão do identificador de cliente de 8 bytes: ~1 em 18 quintilhões (desprezível)

### Autorização de Cliente DH (Diffie-Hellman)

**Visão geral:** Cada cliente gera um par de chaves X25519 e envia sua chave pública ao servidor por meio de um canal seguro fora de banda. O servidor usa Diffie-Hellman efêmero para criptografar um authCookie exclusivo para cada cliente.

#### Geração de chaves do cliente

```python
# Client generates keypair
csk_i = GENERATE_PRIVATE()  # 32-byte X25519 private key
cpk_i = DERIVE_PUBLIC(csk_i)  # 32-byte X25519 public key

# Client sends cpk_i to server via secure out-of-band channel
# Client KEEPS csk_i secret (never transmitted)
```
**Vantagem de segurança:** A chave privada do cliente nunca deixa o dispositivo. Um adversário que intercepte a transmissão fora de banda não pode descriptografar futuros LeaseSets criptografados sem quebrar o X25519 DH.

#### Processamento do Servidor

```python
# Server generates new auth cookie and ephemeral keypair
authCookie = CSRNG(32)  # 32-byte cookie

esk = GENERATE_PRIVATE()  # 32-byte ephemeral private key
epk = DERIVE_PUBLIC(esk)  # 32-byte ephemeral public key

# For each authorized client i
for cpk_i in authorized_clients:
    # Perform DH key agreement
    sharedSecret = DH(esk, cpk_i)  # 32 bytes
    
    # Derive client-specific encryption key
    authInput = sharedSecret || cpk_i || subcredential || publishedTimestamp
    okm = HKDF(
        salt=epk,  # Ephemeral public key as salt
        ikm=authInput,
        info="ELS2_XCA",  # Domain separation
        n=52  # 32 key + 12 IV + 8 ID
    )
    
    # Extract components
    clientKey_i = okm[0:31]    # 32 bytes
    clientIV_i = okm[32:43]    # 12 bytes
    clientID_i = okm[44:51]    # 8 bytes
    
    # Encrypt authCookie for this client
    clientCookie_i = ENCRYPT(clientKey_i, clientIV_i, authCookie)
    
    # Store [clientID_i, clientCookie_i] entry in Layer 1
```
**Estrutura de Dados da Camada 1:**

```
ephemeralPublicKey (32 bytes)
clients (2 bytes) = N
[clientID_1 (8 bytes) || clientCookie_1 (32 bytes)]
[clientID_2 (8 bytes) || clientCookie_2 (32 bytes)]
...
[clientID_N (8 bytes) || clientCookie_N (32 bytes)]
```
**Recomendações para o servidor:** - Gerar um novo par de chaves efêmero para cada LeaseSet criptografado publicado - Aleatorizar a ordem dos clientes para evitar rastreamento baseado em posição - Considerar adicionar entradas falsas para ocultar o número real de clientes

#### Processamento do Cliente

```python
# Client has: csk_i (their private key), destination, date, secret
# Client receives: encrypted LeaseSet with epk in Layer 1

# Perform DH key agreement with server's ephemeral public key
sharedSecret = DH(csk_i, epk)  # 32 bytes

# Derive expected client identifier and decryption key
cpk_i = DERIVE_PUBLIC(csk_i)  # Client's own public key
authInput = sharedSecret || cpk_i || subcredential || publishedTimestamp

okm = HKDF(
    salt=epk,
    ikm=authInput,
    info="ELS2_XCA",
    n=52
)

clientKey_i = okm[0:31]    # 32 bytes
clientIV_i = okm[32:43]    # 12 bytes
clientID_i = okm[44:51]    # 8 bytes

# Search Layer 1 authorization data for clientID_i
for (clientID, clientCookie) in layer1_auth_entries:
    if clientID == clientID_i:
        # Found matching entry, decrypt authCookie
        authCookie = DECRYPT(clientKey_i, clientIV_i, clientCookie)
        # Use authCookie to decrypt Layer 2
        break
else:
    # No matching entry - client not authorized or revoked
    raise AuthorizationError("Client not authorized")
```
**Tratamento de erros do cliente:** - Se `clientID_i` não for encontrado: O cliente foi revogado ou nunca foi autorizado - Se a descriptografia falhar: Dados corrompidos ou chaves incorretas (extremamente raro) - Os clientes devem efetuar nova busca periodicamente para detectar revogação

### Autorização do Cliente com PSK

**Visão geral:** Cada cliente possui uma chave simétrica pré-compartilhada de 32 bytes. O servidor criptografa o mesmo authCookie usando a PSK (chave pré-compartilhada) de cada cliente.

#### Geração de Chaves

```python
# Option 1: Client generates key
psk_i = CSRNG(32)  # 32-byte pre-shared key
# Client sends psk_i to server via secure out-of-band channel

# Option 2: Server generates key
psk_i = CSRNG(32)  # 32-byte pre-shared key
# Server sends psk_i to one or more clients via secure out-of-band channel
```
**Nota de segurança:** A mesma PSK (chave pré-compartilhada) pode ser compartilhada entre múltiplos clientes, se desejado (cria uma autorização "de grupo").

#### Processamento do servidor

```python
# Server generates new auth cookie and salt
authCookie = CSRNG(32)  # 32-byte cookie
authSalt = CSRNG(32)     # 32-byte salt

# For each authorized client i
for psk_i in authorized_clients:
    # Derive client-specific encryption key
    authInput = psk_i || subcredential || publishedTimestamp
    
    okm = HKDF(
        salt=authSalt,
        ikm=authInput,
        info="ELS2PSKA",  # Domain separation
        n=52  # 32 key + 12 IV + 8 ID
    )
    
    # Extract components
    clientKey_i = okm[0:31]    # 32 bytes
    clientIV_i = okm[32:43]    # 12 bytes
    clientID_i = okm[44:51]    # 8 bytes
    
    # Encrypt authCookie for this client
    clientCookie_i = ENCRYPT(clientKey_i, clientIV_i, authCookie)
    
    # Store [clientID_i, clientCookie_i] entry in Layer 1
```
**Estrutura de Dados da Camada 1:**

```
authSalt (32 bytes)
clients (2 bytes) = N
[clientID_1 (8 bytes) || clientCookie_1 (32 bytes)]
[clientID_2 (8 bytes) || clientCookie_2 (32 bytes)]
...
[clientID_N (8 bytes) || clientCookie_N (32 bytes)]
```
#### Processamento do cliente

```python
# Client has: psk_i (their pre-shared key), destination, date, secret
# Client receives: encrypted LeaseSet with authSalt in Layer 1

# Derive expected client identifier and decryption key
authInput = psk_i || subcredential || publishedTimestamp

okm = HKDF(
    salt=authSalt,
    ikm=authInput,
    info="ELS2PSKA",
    n=52
)

clientKey_i = okm[0:31]    # 32 bytes
clientIV_i = okm[32:43]    # 12 bytes
clientID_i = okm[44:51]    # 8 bytes

# Search Layer 1 authorization data for clientID_i
for (clientID, clientCookie) in layer1_auth_entries:
    if clientID == clientID_i:
        # Found matching entry, decrypt authCookie
        authCookie = DECRYPT(clientKey_i, clientIV_i, clientCookie)
        # Use authCookie to decrypt Layer 2
        break
else:
    # No matching entry - client not authorized or revoked
    raise AuthorizationError("Client not authorized")
```
### Comparação e Recomendações

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Feature</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">DH Authorization</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">PSK Authorization</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Key Exchange</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Asymmetric (X25519)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Symmetric (shared secret)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Security</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Higher (forward secrecy)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Lower (depends on PSK secrecy)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Client Privacy</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Private key never transmitted</td><td style="border:1px solid var(--color-border); padding:0.5rem;">PSK must be transmitted securely</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Performance</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">N+1 DH operations</td><td style="border:1px solid var(--color-border); padding:0.5rem;">No DH operations</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Key Sharing</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">One key per client</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Can share key among multiple clients</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Revocation Detection</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Adversary cannot tell when revoked</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Adversary can track revocation if PSK intercepted</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Use Case</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">High security requirements</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Performance-critical or group access</td></tr>
  </tbody>
</table>
**Recomendação:** - **Use a autorização DH (Diffie-Hellman)** para aplicações de alta segurança em que o sigilo futuro (forward secrecy) é importante - **Use a autorização por PSK (chave pré-compartilhada)** quando o desempenho for crítico ou ao gerenciar grupos de clientes - **Nunca reutilize PSKs** entre serviços diferentes ou em períodos de tempo distintos - **Sempre use canais seguros** para a distribuição de chaves (por exemplo, Signal, OTR, PGP)

### Considerações de segurança

**Privacidade da filiação do cliente:**

Ambos os mecanismos fornecem privacidade para a associação de clientes por meio de: 1. **Identificadores de cliente criptografados:** clientID de 8 bytes derivado da saída do HKDF (função de derivação de chaves baseada em HMAC) 2. **Cookies indistinguíveis:** Todos os valores clientCookie de 32 bytes parecem aleatórios 3. **Sem metadados específicos do cliente:** Não há como identificar qual entrada pertence a qual cliente

Um observador pode ver: - Número de clientes autorizados (do campo `clients`) - Mudanças na contagem de clientes ao longo do tempo

Um observador NÃO PODE ver: - Quais clientes específicos estão autorizados - Quando clientes específicos são adicionados ou removidos (se a contagem permanecer a mesma) - Qualquer informação que identifique clientes

**Recomendações de Aleatorização:**

Servidores DEVERIAM aleatorizar a ordem dos clientes sempre que gerarem um LeaseSet criptografado:

```python
import random

# Before serializing
auth_entries = [(clientID_i, clientCookie_i) for each client]
random.shuffle(auth_entries)
# Now serialize in randomized order
```
**Benefícios:** - Impede que os clientes saibam sua posição na lista - Evita ataques de inferência com base em mudanças de posição - Torna indistinguível a adição/revogação de clientes

**Ocultando a contagem de clientes:**

Servidores PODEM inserir entradas fictícias aleatórias:

```python
# Add dummy entries
num_dummies = random.randint(0, max_dummies)
for _ in range(num_dummies):
    dummy_id = CSRNG(8)
    dummy_cookie = CSRNG(32)
    auth_entries.append((dummy_id, dummy_cookie))

# Randomize all entries (real + dummy)
random.shuffle(auth_entries)
```
**Custo:** Entradas fictícias aumentam o tamanho do LeaseSet criptografado (40 bytes cada).

**Rotação do AuthCookie (cookie de autenticação):**

Os servidores DEVERIAM gerar um novo authCookie: - Cada vez que um LeaseSet criptografado for publicado (a cada poucas horas, tipicamente) - Imediatamente após revogar a autorização de um cliente - Em um cronograma regular (por exemplo, diariamente), mesmo que não haja alterações de clientes

**Benefícios:** - Limita a exposição se o authCookie for comprometido - Garante que clientes revogados percam o acesso rapidamente - Fornece sigilo de encaminhamento para a Camada 2

---

## Endereçamento Base32 para LeaseSets Criptografados

### Visão geral

Endereços base32 tradicionais do I2P contêm apenas o hash do Destination (destino no I2P) (32 bytes → 52 caracteres). Isso é insuficiente para LeaseSets criptografados porque:

1. Os clientes precisam da **chave pública não cegada** para derivar a chave pública cegada
2. Os clientes precisam dos **tipos de assinatura** (não cegada e cegada) para a derivação correta da chave
3. O hash por si só não fornece essa informação

**Solução:** Um novo formato base32 que inclui a chave pública e os tipos de assinatura.

### Especificação do Formato de Endereço

**Estrutura decodificada (35 bytes):**

```
┌─────────────────────────────────────────────────────┐
│ Byte 0   │ Byte 1  │ Byte 2  │ Bytes 3-34          │
│ Flags    │ Unblind │ Blinded │ Public Key          │
│ (XOR)    │ SigType │ SigType │ (32 bytes)          │
│          │ (XOR)   │ (XOR)   │                     │
└─────────────────────────────────────────────────────┘
```
**Primeiros 3 bytes (XOR com checksum):**

Os 3 primeiros bytes contêm metadados combinados via XOR com partes de uma soma de verificação CRC-32:

```python
# Data structure before XOR
flags = 0x00           # 1 byte (reserved for future use)
unblinded_sigtype = 0x07 or 0x0b  # 1 byte (7 or 11)
blinded_sigtype = 0x0b  # 1 byte (always 11)

# Compute CRC-32 checksum of public key
checksum = crc32(pubkey)  # 4-byte CRC-32 of bytes 3-34

# XOR first 3 bytes with parts of checksum
data[0] = flags XOR (checksum >> 24) & 0xFF
data[1] = unblinded_sigtype XOR (checksum >> 16) & 0xFF  
data[2] = blinded_sigtype XOR (checksum >> 8) & 0xFF

# Bytes 3-34 contain the unmodified 32-byte public key
data[3:34] = pubkey
```
**Propriedades da soma de verificação:** - Usa o polinômio padrão CRC-32 - Taxa de falsos negativos: ~1 em 16 milhões - Fornece detecção de erros de digitação em endereços - Não pode ser usado como autenticação (não é criptograficamente seguro)

**Formato codificado:**

```
Base32Encode(35 bytes) || ".b32.i2p"
```
**Características:** - Total de caracteres: 56 (35 bytes × 8 bits ÷ 5 bits por caractere) - Sufixo: ".b32.i2p" (igual ao base32 tradicional) - Comprimento total: 56 + 8 = 64 caracteres (excluindo o terminador nulo)

**Codificação Base32:** - Alfabeto: `abcdefghijklmnopqrstuvwxyz234567` (padrão RFC 4648) - 5 bits não utilizados no final DEVEM ser 0 - Não diferencia maiúsculas de minúsculas (por convenção, minúsculas)

### Geração de Endereços

```python
import struct
from zlib import crc32
import base64

def generate_encrypted_b32_address(pubkey, unblinded_sigtype, blinded_sigtype):
    """
    Generate base32 address for encrypted LeaseSet.
    
    Args:
        pubkey: 32-byte public key (bytes)
        unblinded_sigtype: Unblinded signature type (7 or 11)
        blinded_sigtype: Blinded signature type (always 11)
    
    Returns:
        String address ending in .b32.i2p
    """
    # Verify inputs
    assert len(pubkey) == 32, "Public key must be 32 bytes"
    assert unblinded_sigtype in [7, 11], "Unblinded sigtype must be 7 or 11"
    assert blinded_sigtype == 11, "Blinded sigtype must be 11"
    
    # Compute CRC-32 of public key
    checksum = crc32(pubkey) & 0xFFFFFFFF  # Ensure 32-bit unsigned
    
    # Prepare metadata bytes
    flags = 0x00
    
    # XOR metadata with checksum parts
    byte0 = flags ^ ((checksum >> 24) & 0xFF)
    byte1 = unblinded_sigtype ^ ((checksum >> 16) & 0xFF)
    byte2 = blinded_sigtype ^ ((checksum >> 8) & 0xFF)
    
    # Construct 35-byte data
    data = bytes([byte0, byte1, byte2]) + pubkey
    
    # Base32 encode (standard alphabet)
    # Python's base64 module uses uppercase by default
    b32 = base64.b32encode(data).decode('ascii').lower().rstrip('=')
    
    # Construct full address
    address = b32 + ".b32.i2p"
    
    return address
```
### Análise de Endereços

```python
import struct
from zlib import crc32
import base64

def parse_encrypted_b32_address(address):
    """
    Parse base32 address for encrypted LeaseSet.
    
    Args:
        address: String address ending in .b32.i2p
    
    Returns:
        Tuple of (pubkey, unblinded_sigtype, blinded_sigtype)
    
    Raises:
        ValueError: If address is invalid or checksum fails
    """
    # Remove suffix
    if not address.endswith('.b32.i2p'):
        raise ValueError("Invalid address suffix")
    
    b32 = address[:-8]  # Remove ".b32.i2p"
    
    # Verify length (56 characters for 35 bytes)
    if len(b32) != 56:
        raise ValueError(f"Invalid length: {len(b32)} (expected 56)")
    
    # Base32 decode
    # Add padding if needed
    padding_needed = (8 - (len(b32) % 8)) % 8
    b32_padded = b32.upper() + '=' * padding_needed
    
    try:
        data = base64.b32decode(b32_padded)
    except Exception as e:
        raise ValueError(f"Invalid base32 encoding: {e}")
    
    # Verify decoded length
    if len(data) != 35:
        raise ValueError(f"Invalid decoded length: {len(data)} (expected 35)")
    
    # Extract public key
    pubkey = data[3:35]
    
    # Compute CRC-32 for verification
    checksum = crc32(pubkey) & 0xFFFFFFFF
    
    # Un-XOR metadata bytes
    flags = data[0] ^ ((checksum >> 24) & 0xFF)
    unblinded_sigtype = data[1] ^ ((checksum >> 16) & 0xFF)
    blinded_sigtype = data[2] ^ ((checksum >> 8) & 0xFF)
    
    # Verify expected values
    if flags != 0x00:
        raise ValueError(f"Invalid flags: {flags:#x} (expected 0x00)")
    
    if unblinded_sigtype not in [7, 11]:
        raise ValueError(f"Invalid unblinded sigtype: {unblinded_sigtype} (expected 7 or 11)")
    
    if blinded_sigtype != 11:
        raise ValueError(f"Invalid blinded sigtype: {blinded_sigtype} (expected 11)")
    
    return pubkey, unblinded_sigtype, blinded_sigtype
```
### Comparação com o Base32 tradicional

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Feature</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Traditional B32</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Encrypted LS2 B32</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Content</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">SHA-256 hash of Destination</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Public key + signature types</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Decoded Size</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">32 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">35 bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Encoded Length</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">52 characters</td><td style="border:1px solid var(--color-border); padding:0.5rem;">56 characters</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Suffix</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">.b32.i2p</td><td style="border:1px solid var(--color-border); padding:0.5rem;">.b32.i2p</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Total Length</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">60 chars</td><td style="border:1px solid var(--color-border); padding:0.5rem;">64 chars</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Checksum</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">None</td><td style="border:1px solid var(--color-border); padding:0.5rem;">CRC-32 (XOR'd into first 3 bytes)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Use Case</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Regular destinations</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Encrypted LeaseSet destinations</td></tr>
  </tbody>
</table>
### Restrições de Uso

**Incompatibilidade com BitTorrent:**

Endereços LS2 criptografados NÃO PODEM ser usados com as respostas compactas de announce do BitTorrent:

```
Compact announce reply format:
┌────────────────────────────┐
│ 32-byte destination hash   │  ← Only hash, no signature types
│ 2-byte port                │
└────────────────────────────┘
```
**Problema:** O formato compacto contém apenas o hash (32 bytes), sem espaço para tipos de assinatura ou informações da chave pública.

**Solução:** Utilize respostas completas de announce ou rastreadores baseados em HTTP que suportem endereços completos.

### Integração com o Livro de Endereços

Se um cliente tiver o Destination (identificador de destino no I2P) completo em um livro de endereços:

1. Armazenar Destination completo (Destino no I2P, inclui a chave pública)
2. Suportar consulta reversa por hash
3. Quando um LS2 criptografado for encontrado, recuperar a chave pública do livro de endereços
4. Não há necessidade de um novo formato base32 se o Destination completo já for conhecido

**Formatos de livro de endereços que suportam LS2 criptografado (LeaseSet v2, termo do I2P para um conjunto de informações de destino):** - hosts.txt com cadeias de caracteres de destino completas - bancos de dados SQLite com coluna de destino - formatos JSON/XML com dados de destino completos

### Exemplos de Implementação

**Exemplo 1: Gerar endereço**

```python
# Ed25519 destination example
pubkey = bytes.fromhex('a' * 64)  # 32-byte public key
unblinded_type = 7   # Ed25519
blinded_type = 11    # Red25519 (always)

address = generate_encrypted_b32_address(pubkey, unblinded_type, blinded_type)
print(f"Address: {address}")
# Output: 56 base32 characters + .b32.i2p
```
**Exemplo 2: Analisar e Validar**

```python
address = "abc...xyz.b32.i2p"  # 56 chars + suffix

try:
    pubkey, unblinded, blinded = parse_encrypted_b32_address(address)
    print(f"Public Key: {pubkey.hex()}")
    print(f"Unblinded SigType: {unblinded}")
    print(f"Blinded SigType: {blinded}")
except ValueError as e:
    print(f"Invalid address: {e}")
```
**Exemplo 3: Converter a partir de Destination (destino do I2P)**

```python
def destination_to_encrypted_b32(destination):
    """
    Convert full Destination to encrypted LS2 base32 address.
    
    Args:
        destination: I2P Destination object
    
    Returns:
        Base32 address string
    """
    # Extract public key and signature type from destination
    pubkey = destination.signing_public_key  # 32 bytes
    sigtype = destination.sig_type  # 7 or 11
    
    # Blinded type is always 11 (Red25519)
    blinded_type = 11
    
    # Generate address
    return generate_encrypted_b32_address(pubkey, sigtype, blinded_type)
```
### Considerações de Segurança

**Privacidade:** - O endereço Base32 revela a chave pública - Isso é intencional e necessário para o protocolo - NÃO revela a chave privada nem compromete a segurança - Chaves públicas são, por definição, informações públicas

**Resistência a colisões:** - CRC-32 fornece apenas 32 bits de resistência a colisões - Não é criptograficamente seguro (use apenas para detecção de erros) - NÃO confie no checksum para autenticação - A verificação completa do destino ainda é necessária

**Validação de Endereço:** - Sempre valide a soma de verificação antes do uso - Rejeite endereços com tipos de assinatura inválidos - Verifique se a chave pública está na curva (específico da implementação)

**Referências:** - [Proposta 149: B32 para LS2 (versão 2 do leaseSet) criptografado](/proposals/149-b32-encrypted-ls2/) - [Especificação de Endereçamento B32](/docs/specs/b32-for-encrypted-leasesets/) - [Especificação de Nomes do I2P](/docs/overview/naming/)

---

## Suporte a Chaves Offline

### Visão geral

Chaves offline permitem que a chave de assinatura principal permaneça offline (armazenamento a frio) enquanto uma chave de assinatura transitória é usada nas operações do dia a dia. Isso é fundamental para serviços de alta segurança.

**Requisitos Específicos do LS2 criptografado:** - Chaves transitórias devem ser geradas offline - Chaves privadas cegadas devem ser pré-geradas (uma por dia) - Tanto as chaves transitórias quanto as cegadas devem ser entregues em lotes - Ainda não há um formato de arquivo padronizado definido (TODO na especificação)

### Estrutura de Chave Offline

**Dados de Chave Transitória da Camada 0 (quando o bit 0 do flag = 1):**

```
┌───────────────────────────────────────────────────┐
│ Expires Timestamp       │ 4 bytes (seconds)       │
│ Transient Sig Type      │ 2 bytes (big endian)    │
│ Transient Signing Pubkey│ Variable (sigtype len)  │
│ Signature (by blinded)  │ 64 bytes (Red25519)     │
└───────────────────────────────────────────────────┘
```
**Cobertura da Assinatura:** A assinatura no bloco de chave offline cobre: - Carimbo de data/hora de expiração (4 bytes) - Tipo de assinatura transitória (2 bytes)   - Chave pública de assinatura transitória (variável)

Esta assinatura é verificada com a **chave pública cegada**, provando que a entidade com a chave privada cegada autorizou esta chave temporária.

### Processo de Geração de Chaves

**Para LeaseSet criptografado com chaves offline:**

1. **Gerar pares de chaves efêmeros** (offline, em armazenamento a frio):
   ```python
   # For each day in future
   for date in future_dates:
       # Generate daily transient keypair
       transient_privkey = generate_red25519_privkey()  # Type 11
       transient_pubkey = derive_public(transient_privkey)

       # Store for later delivery
       keys[date] = (transient_privkey, transient_pubkey)
   ```

2. **Generate daily blinded keypairs** (offline, in cold storage):
   ```python
# Para cada dia    for date in future_dates:

       # Derive alpha for this date
       datestring = date.strftime("%Y%m%d")  # "YYYYMMDD"
       alpha = GENERATE_ALPHA(destination, datestring, secret)
       
       # Blind the signing private key
       a = destination_signing_privkey  # Type 7 or 11
       blinded_privkey = BLIND_PRIVKEY(a, alpha)  # Result is type 11
       blinded_pubkey = DERIVE_PUBLIC(blinded_privkey)
       
       # Store for later delivery
       blinded_keys[date] = (blinded_privkey, blinded_pubkey)
   ```

3. **Sign transient keys with blinded keys** (offline):
   ```python
for date in future_dates:

       transient_pubkey = keys[date][1]
       blinded_privkey = blinded_keys[date][0]
       
       # Create signature data
       expires = int((date + timedelta(days=1)).timestamp())
       sig_data = struct.pack('>I', expires)  # 4 bytes
       sig_data += struct.pack('>H', 11)     # Transient type (Red25519)
       sig_data += transient_pubkey          # 32 bytes
       
       # Sign with blinded private key
       signature = RED25519_SIGN(blinded_privkey, sig_data)
       
       # Package for delivery
       offline_sig_blocks[date] = {
           'expires': expires,
           'transient_type': 11,
           'transient_pubkey': transient_pubkey,
           'signature': signature
       }
   ```

4. **Package for delivery to router:**
   ```python
# Para cada data    delivery_package[date] = {

       'transient_privkey': keys[date][0],
       'transient_pubkey': keys[date][1],
       'blinded_privkey': blinded_keys[date][0],
       'blinded_pubkey': blinded_keys[date][1],
       'offline_sig_block': offline_sig_blocks[date]
}

   ```

### Router Usage

**Daily Key Loading:**

```python
# À meia-noite UTC (ou antes da publicação)

date = datetime.utcnow().date()

# Carregar as chaves de hoje

today_keys = load_delivery_package(date)

transient_privkey = today_keys['transient_privkey'] transient_pubkey = today_keys['transient_pubkey'] blinded_privkey = today_keys['blinded_privkey'] blinded_pubkey = today_keys['blinded_pubkey'] offline_sig_block = today_keys['offline_sig_block']

# Use estas chaves para o LeaseSet criptografado de hoje

```

**Publishing Process:**

```python
# 1. Criar LeaseSet2 interno

inner_ls2 = create_leaseset2(

    destinations, leases, expires, 
    signing_key=transient_privkey  # Use transient key
)

# 2. Criptografar a Camada 2

layer2_ciphertext = encrypt_layer2(inner_ls2, authCookie, subcredential, timestamp)

# 3. Crie a Camada 1 com dados de autorização

layer1_plaintext = create_layer1(authorization_data, layer2_ciphertext)

# 4. Criptografar a Camada 1

layer1_ciphertext = encrypt_layer1(layer1_plaintext, subcredential, timestamp)

# 5. Crie a Camada 0 com um bloco de assinatura offline

layer0 = create_layer0(

    blinded_pubkey,
    timestamp,
    expires,
    flags=0x0001,  # Bit 0 set (offline keys present)
    offline_sig_block=offline_sig_block,
    layer1_ciphertext=layer1_ciphertext
)

# 6. Assine a Camada 0 com uma chave privada transitória

signature = RED25519_SIGN(transient_privkey, layer0)

# 7. Anexar a assinatura e publicar

encrypted_leaseset = layer0 + signature publish_to_netdb(encrypted_leaseset)

```

### Security Considerations

**Tracking via Offline Signature Block:**

The offline signature block is in plaintext (Layer 0). An adversary scraping floodfills could:
- Track the same encrypted LeaseSet across multiple days
- Correlate encrypted LeaseSets even though blinded keys change daily

**Mitigation:** Generate new transient keys daily (in addition to blinded keys):

```python
# Gerar tanto novas chaves temporárias quanto novas chaves cegadas todos os dias

for date in future_dates:

    # New transient keypair for this day
    transient_privkey = generate_red25519_privkey()
    transient_pubkey = derive_public(transient_privkey)
    
    # New blinded keypair for this day
    alpha = GENERATE_ALPHA(destination, datestring, secret)
    blinded_privkey = BLIND_PRIVKEY(signing_privkey, alpha)
    blinded_pubkey = DERIVE_PUBLIC(blinded_privkey)
    
    # Sign new transient key with new blinded key
    sig = RED25519_SIGN(blinded_privkey, transient_pubkey || metadata)
    
    # Now offline sig block changes daily
```

**Benefits:**
- Prevents tracking across days via offline signature block
- Provides same security as encrypted LS2 without offline keys
- Each day appears completely independent

**Cost:**
- More keys to generate and store
- More complex key management

### File Format (TODO)

**Current Status:** No standardized file format defined for batch key delivery.

**Requirements for Future Format:**

1. **Must support multiple dates:**
   - Batch delivery of 30+ days worth of keys
   - Clear date association for each key set

2. **Must include all necessary data:**
   - Transient private key
   - Transient public key
   - Blinded private key
   - Blinded public key
   - Pre-computed offline signature block
   - Expiration timestamps

3. **Should be tamper-evident:**
   - Checksums or signatures over entire file
   - Integrity verification before loading

4. **Should be encrypted:**
   - Keys are sensitive material
   - Encrypt file with router's key or passphrase

**Proposed Format Example (JSON, encrypted):**

```json
{   "version": 1,   "destination_hash": "base64...",   "keys": [

    {
      "date": "2025-10-15",
      "transient": {
        "type": 11,
        "privkey": "base64...",
        "pubkey": "base64..."
      },
      "blinded": {
        "privkey": "base64...",
        "pubkey": "base64..."
      },
      "offline_sig_block": {
        "expires": 1729123200,
        "signature": "base64..."
      }
    }
],   "signature": "base64..."  // Signature over entire structure }

```

### I2CP Protocol Enhancement (TODO)

**Current Status:** No I2CP protocol enhancement defined for offline keys with encrypted LeaseSet.

**Requirements:**

1. **Key delivery mechanism:**
   - Upload batch of keys from client to router
   - Acknowledgment of successful key loading

2. **Key expiration notification:**
   - Router notifies client when keys running low
   - Client can generate and upload new batch

3. **Key revocation:**
   - Emergency revocation of future keys if compromise suspected

**Proposed I2CP Messages:**

```
UPLOAD_OFFLINE_KEYS   - Lote de material de chave criptografado   - Intervalo de datas abrangido

OFFLINE_KEY_STATUS   - Número de dias restantes   - Data de expiração da próxima chave

REVOKE_OFFLINE_KEYS     - Intervalo de datas a revogar   - Novas chaves para substituir (opcional)

```

### Implementation Status

**Java I2P:**
- ✅ Offline keys for standard LS2: Fully supported (since 0.9.38)
- ⚠️ Offline keys for encrypted LS2: Implemented (since 0.9.40)
- ❌ File format: Not standardized
- ❌ I2CP protocol: Not enhanced

**i2pd (C++):**
- ✅ Offline keys for standard LS2: Fully supported
- ✅ Offline keys for encrypted LS2: Fully supported (since 2.58.0)
- ❌ File format: Not standardized
- ❌ I2CP protocol: Not enhanced

**References:**
- [Offline Signatures Proposal](/proposals/123-new-netdb-entries/)
- [I2CP Specification](/docs/specs/i2cp/)

---

## Security Considerations

### Cryptographic Security

**Algorithm Selection:**

All cryptographic primitives are based on well-studied algorithms:
- **ChaCha20:** Modern stream cipher, constant-time, no timing attacks
- **SHA-256:** NIST-approved hash, 128-bit security level
- **HKDF:** RFC 5869 standard, proven security bounds
- **Ed25519/Red25519:** Curve25519-based, ~128-bit security level
- **X25519:** Diffie-Hellman over Curve25519, ~128-bit security level

**Key Sizes:**
- All symmetric keys: 256 bits (32 bytes)
- All public/private keys: 256 bits (32 bytes)
- All nonces/IVs: 96 bits (12 bytes)
- All signatures: 512 bits (64 bytes)

These sizes provide adequate security margins against current and near-future attacks.

### Forward Secrecy

**Daily Key Rotation:**

Encrypted LeaseSets rotate keys daily (UTC midnight):
- New blinded public/private key pair
- New storage location in DHT
- New encryption keys for both layers

**Benefits:**
- Compromising today's blinded key doesn't reveal yesterday's
- Limits exposure window to 24 hours
- Prevents long-term tracking via DHT

**Enhanced with Ephemeral Keys:**

DH client authorization uses ephemeral keys:
- Server generates new ephemeral DH keypair for each publication
- Compromising ephemeral key only affects that publication
- True forward secrecy even if long-term keys compromised

### Privacy Properties

**Destination Blinding:**

The blinded public key:
- Is unlinkable to the original destination (without knowing the secret)
- Changes daily, preventing long-term correlation
- Cannot be reversed to find the original public key

**Client Membership Privacy:**

Per-client authorization provides:
- **Anonymity:** No way to identify which clients are authorized
- **Untraceability:** Cannot track when specific clients added/revoked
- **Size obfuscation:** Can add dummy entries to hide true count

**DHT Privacy:**

Storage location rotates daily:
```
location = SHA-256(sig_type || blinded_public_key)

```

This prevents:
- Correlation across days via DHT lookups
- Long-term monitoring of service availability
- Traffic analysis of DHT queries

### Threat Model

**Adversary Capabilities:**

1. **Network Adversary:**
   - Can monitor all DHT traffic
   - Can observe encrypted LeaseSet publications
   - Cannot decrypt without proper keys

2. **Floodfill Adversary:**
   - Can store and analyze all encrypted LeaseSets
   - Can track publication patterns over time
   - Cannot decrypt Layer 1 or Layer 2
   - Can see client count (but not identities)

3. **Authorized Client Adversary:**
   - Can decrypt specific encrypted LeaseSets
   - Can access inner LeaseSet2 data
   - Cannot determine other clients' identities
   - Cannot decrypt past LeaseSets (with ephemeral keys)

**Out of Scope:**

- Malicious router implementations
- Compromised router host systems
- Side-channel attacks (timing, power analysis)
- Physical access to keys
- Social engineering attacks

### Attack Scenarios

**1. Offline Keys Tracking Attack:**

**Attack:** Adversary tracks encrypted LeaseSets via unchanging offline signature block.

**Mitigation:** Generate new transient keys daily (in addition to blinded keys).

**Status:** Documented recommendation, implementation-specific.

**2. Client Position Inference Attack:**

**Attack:** If client order is static, clients can infer their position and detect when other clients added/removed.

**Mitigation:** Randomize client order in authorization list for each publication.

**Status:** Documented recommendation in specification.

**3. Client Count Analysis Attack:**

**Attack:** Adversary monitors client count changes over time to infer service popularity or client churn.

**Mitigation:** Add random dummy entries to authorization list.

**Status:** Optional feature, deployment-specific trade-off (size vs. privacy).

**4. PSK Interception Attack:**

**Attack:** Adversary intercepts PSK during out-of-band exchange and can decrypt all future encrypted LeaseSets.

**Mitigation:** Use DH client authorization instead, or ensure secure key exchange (Signal, OTR, PGP).

**Status:** Known limitation of PSK approach, documented in specification.

**5. Timing Correlation Attack:**

**Attack:** Adversary correlates publication times across days to link encrypted LeaseSets.

**Mitigation:** Randomize publication times, use delayed publishing.

**Status:** Implementation-specific, not addressed in core specification.

**6. Long-term Secret Compromise:**

**Attack:** Adversary compromises the blinding secret and can compute all past and future blinded keys.

**Mitigation:** 
- Use optional secret parameter (not empty)
- Rotate secret periodically
- Use different secrets for different services

**Status:** Secret parameter is optional; using it is highly recommended.

### Operational Security

**Key Management:**

1. **Signing Private Key:**
   - Store offline in cold storage
   - Use only for generating blinded keys (batch process)
   - Never expose to online router

2. **Blinded Private Keys:**
   - Generate offline, deliver in batches
   - Rotate daily automatically
   - Delete after use (forward secrecy)

3. **Transient Private Keys (with offline keys):**
   - Generate offline, deliver in batches
   - Can be longer-lived (days/weeks)
   - Rotate regularly for enhanced privacy

4. **Client Authorization Keys:**
   - DH: Client private keys never leave client device
   - PSK: Use unique keys per client, secure exchange
   - Revoke immediately upon client removal

**Secret Management:**

The optional secret parameter in `GENERATE_ALPHA`:
- SHOULD be used for high-security services
- MUST be transmitted securely to authorized clients
- SHOULD be rotated periodically (e.g., monthly)
- CAN be different for different client groups

**Monitoring and Auditing:**

1. **Publication Monitoring:**
   - Verify encrypted LeaseSets published successfully
   - Monitor floodfill acceptance rates
   - Alert on publication failures

2. **Client Access Monitoring:**
   - Log client authorization attempts (without identifying clients)
   - Monitor for unusual patterns
   - Detect potential attacks early

3. **Key Rotation Auditing:**
   - Verify daily key rotation occurs
   - Check blinded key changes daily
   - Ensure old keys are deleted

### Implementation Security

**Constant-Time Operations:**

Implementations MUST use constant-time operations for:
- All scalar arithmetic (mod L operations)
- Private key comparisons
- Signature verification
- DH key agreement

**Memory Security:**

- Zero sensitive key material after use
- Use secure memory allocation for keys
- Prevent keys from being paged to disk
- Clear stack variables containing key material

**Random Number Generation:**

- Use cryptographically secure RNG (CSRNG)
- Properly seed RNG from OS entropy source
- Do not use predictable RNGs for key material
- Verify RNG output quality periodically

**Input Validation:**

- Validate all public keys are on the curve
- Check all signature types are supported
- Verify all lengths before parsing
- Reject malformed encrypted LeaseSets early

**Error Handling:**

- Do not leak information via error messages
- Use constant-time comparison for authentication
- Do not expose timing differences in decryption
- Log security-relevant events properly

### Recommendations

**For Service Operators:**

1. ✅ **Use Red25519 (type 11)** for new destinations
2. ✅ **Use DH client authorization** for high-security services
3. ✅ **Generate new transient keys daily** when using offline keys
4. ✅ **Use the optional secret parameter** in GENERATE_ALPHA
5. ✅ **Randomize client order** in authorization lists
6. ✅ **Monitor publication success** and investigate failures
7. ⚠️ **Consider dummy entries** to hide client count (size trade-off)

**For Client Implementers:**

1. ✅ **Validate blinded public keys** are on prime-order subgroup
2. ✅ **Verify all signatures** before trusting data
3. ✅ **Use constant-time operations** for cryptographic primitives
4. ✅ **Zero key material** immediately after use
5. ✅ **Implement proper error handling** without information leaks
6. ✅ **Support both Ed25519 and Red25519** destination types

**For Network Operators:**

1. ✅ **Accept encrypted LeaseSets** in floodfill routers
2. ✅ **Enforce reasonable size limits** to prevent abuse
3. ✅ **Monitor for anomalous patterns** (extremely large, frequent updates)
4. ⚠️ **Consider rate limiting** encrypted LeaseSet publications

---

## Implementation Notes

### Java I2P Implementation

**Repository:** https://github.com/i2p/i2p.i2p

**Key Classes:**
- `net.i2p.data.LeaseSet2` - LeaseSet2 structure
- `net.i2p.data.EncryptedLeaseSet` - Encrypted LS2 implementation
- `net.i2p.crypto.eddsa.EdDSAEngine` - Ed25519/Red25519 signatures
- `net.i2p.crypto.HKDF` - HKDF implementation
- `net.i2p.crypto.ChaCha20` - ChaCha20 cipher

**Configuration:**

Enable encrypted LeaseSet in `clients.config`:
```properties
# Ativar LeaseSet criptografado

i2cp.encryptLeaseSet=true

# Opcional: Ativar a autorização do cliente

i2cp.enableAccessList=true

# Opcional: Use a autorização DH (Diffie-Hellman) (o padrão é PSK (chave pré-compartilhada))

i2cp.accessListType=0

# Opcional: Blinding secret (segredo de cegamento) (altamente recomendado)

i2cp.blindingSecret=seu-segredo-aqui

```

**API Usage Example:**

```java
// Crie um LeaseSet criptografado EncryptedLeaseSet els = new EncryptedLeaseSet();

// Defina o destino els.setDestination(destination);

// Ativar autorização por cliente els.setAuthorizationEnabled(true); els.setAuthType(EncryptedLeaseSet.AUTH_DH);

// Adicionar clientes autorizados (chaves públicas DH) for (byte[] clientPubKey : authorizedClients) {

    els.addClient(clientPubKey);
}

// Defina os parâmetros de cegamento els.setBlindingSecret("your-secret");

// Assine e publique els.sign(signingPrivateKey); netDb.publish(els);

```

### i2pd (C++) Implementation

**Repository:** https://github.com/PurpleI2P/i2pd

**Key Files:**
- `libi2pd/LeaseSet.h/cpp` - LeaseSet implementations
- `libi2pd/Crypto.h/cpp` - Cryptographic primitives
- `libi2pd/Ed25519.h/cpp` - Ed25519/Red25519 signatures
- `libi2pd/ChaCha20.h/cpp` - ChaCha20 cipher

**Configuration:**

Enable in tunnel configuration (`tunnels.conf`):
```ini
[my-hidden-service] type = http host = 127.0.0.1 port = 8080 keys = my-service-keys.dat

# Ativar LeaseSet criptografado

encryptleaseset = true

# Opcional: Tipo de autorização do cliente (0=DH, 1=PSK)

authtype = 0

# Opcional: Blinding secret (segredo de cegamento)

secret = seu-segredo-aqui

# Opcional: Clientes autorizados (um por linha, chaves públicas codificadas em Base64)

client.1 = base64-encoded-client-pubkey-1 client.2 = base64-encoded-client-pubkey-2

```

**API Usage Example:**

```cpp
// Criar LeaseSet criptografado
auto encryptedLS = std::make_shared<i2p::data::EncryptedLeaseSet>(

    destination,
    blindingSecret
);

// Habilitar a autorização por cliente encryptedLS->SetAuthType(i2p::data::AUTH_TYPE_DH);

// Adicionar clientes autorizados
for (const auto& clientPubKey : authorizedClients) {

    encryptedLS->AddClient(clientPubKey);
}

// Assinar e publicar encryptedLS->Sign(signingPrivKey); netdb.Publish(encryptedLS);

```

### Testing and Debugging

**Test Vectors:**

Generate test vectors for implementation verification:

```python
# Vetor de teste 1: Cegamento de chave

destination_pubkey = bytes.fromhex('a' * 64) sigtype = 7 blinded_sigtype = 11 date = "20251015" secret = ""

alpha = generate_alpha(destination_pubkey, sigtype, blinded_sigtype, date, secret) print(f"Alpha: {alpha.hex()}")

# Esperado: (verificar em relação à implementação de referência)

```

**Unit Tests:**

Key areas to test:
1. HKDF derivation with various inputs
2. ChaCha20 encryption/decryption
3. Red25519 signature generation and verification
4. Key blinding (private and public)
5. Layer 1/2 encryption/decryption
6. Client authorization (DH and PSK)
7. Base32 address generation and parsing

**Integration Tests:**

1. Publish encrypted LeaseSet to test network
2. Retrieve and decrypt from client
3. Verify daily key rotation
4. Test client authorization (add/remove clients)
5. Test offline keys (if supported)

**Common Implementation Errors:**

1. **Incorrect mod L reduction:** Must use proper modular arithmetic
2. **Endianness errors:** Most fields are big-endian, but some crypto uses little-endian
3. **Off-by-one in array slicing:** Verify indices are inclusive/exclusive as needed
4. **Missing constant-time comparisons:** Use constant-time for all sensitive comparisons
5. **Not zeroing key material:** Always zero keys after use

### Performance Considerations

**Computational Costs:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Operation</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Cost</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Key blinding (server)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">1 scalar mult</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Per publication</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Key blinding (client)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">1 point add + 1 scalar mult</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Per retrieval</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Layer 1 encryption</td><td style="border:1px solid var(--color-border); padding:0.5rem;">1 HKDF + 1 ChaCha20</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Fast</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Layer 2 encryption</td><td style="border:1px solid var(--color-border); padding:0.5rem;">1 HKDF + 1 ChaCha20</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Fast</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">DH client auth (server)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">N+1 X25519 ops</td><td style="border:1px solid var(--color-border); padding:0.5rem;">N = number of clients</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">DH client auth (client)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">1 X25519 op</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Per retrieval</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">PSK client auth</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0 DH ops</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Only HKDF + ChaCha20</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Signature (Red25519)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">1 signature op</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Similar cost to Ed25519</td></tr>
  </tbody>
</table>

**Size Overhead:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Component</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Size</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Frequency</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Blinded public key</td><td style="border:1px solid var(--color-border); padding:0.5rem;">32 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Per LeaseSet</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Layer 1 encryption overhead</td><td style="border:1px solid var(--color-border); padding:0.5rem;">32 bytes (salt)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Per LeaseSet</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Layer 2 encryption overhead</td><td style="border:1px solid var(--color-border); padding:0.5rem;">32 bytes (salt)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Per LeaseSet</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">DH auth per client</td><td style="border:1px solid var(--color-border); padding:0.5rem;">40 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Per client per LeaseSet</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">DH ephemeral pubkey</td><td style="border:1px solid var(--color-border); padding:0.5rem;">32 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Per LeaseSet (if DH auth)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">PSK auth per client</td><td style="border:1px solid var(--color-border); padding:0.5rem;">40 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Per client per LeaseSet</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">PSK salt</td><td style="border:1px solid var(--color-border); padding:0.5rem;">32 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Per LeaseSet (if PSK auth)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Signature</td><td style="border:1px solid var(--color-border); padding:0.5rem;">64 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Per LeaseSet</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Offline sig block</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈100 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Per LeaseSet (if offline keys)</td></tr>
  </tbody>
</table>

**Typical Sizes:**

- **No client auth:** ~200 bytes overhead
- **With 10 DH clients:** ~600 bytes overhead
- **With 100 DH clients:** ~4200 bytes overhead

**Optimization Tips:**

1. **Batch key generation:** Generate blinded keys for multiple days in advance
2. **Cache subcredentials:** Compute once per day, reuse for all publications
3. **Reuse ephemeral keys:** Can reuse ephemeral DH key for short period (minutes)
4. **Parallel client encryption:** Encrypt client cookies in parallel
5. **Fast path for no auth:** Skip authorization layer entirely when disabled

### Compatibility

**Backward Compatibility:**

- Ed25519 (type 7) destinations supported for unblinded keys
- Red25519 (type 11) required for blinded keys
- Traditional LeaseSets still fully supported
- Encrypted LeaseSets do not break existing network

**Forward Compatibility:**

- Reserved flag bits for future features
- Extensible authorization scheme (3 bits allow 8 types)
- Version field in various structures

**Interoperability:**

- Java I2P and i2pd fully interoperable since:
  - Java I2P 0.9.40 (May 2019)
  - i2pd 2.58.0 (September 2025)
- Encrypted LeaseSets work across implementations
- Client authorization works across implementations

---

## References

### IETF RFCs

- **[RFC 2104](https://datatracker.ietf.org/doc/html/rfc2104)** - HMAC: Keyed-Hashing for Message Authentication (February 1997)
- **[RFC 5869](https://datatracker.ietf.org/doc/html/rfc5869)** - HMAC-based Extract-and-Expand Key Derivation Function (HKDF) (May 2010)
- **[RFC 7539](https://datatracker.ietf.org/doc/html/rfc7539)** - ChaCha20 and Poly1305 for IETF Protocols (May 2015)
- **[RFC 7748](https://datatracker.ietf.org/doc/html/rfc7748)** - Elliptic Curves for Security (January 2016)

### I2P Specifications

- **[Common Structures Specification](/docs/specs/common-structures/)** - LeaseSet2 and EncryptedLeaseSet structures
- **[Proposal 123: New netDB Entries](/proposals/123-new-netdb-entries/)** - Background and design of LeaseSet2
- **[Proposal 146: Red25519](/proposals/146-red25519/)** - Red25519 signature scheme specification
- **[Proposal 149: B32 for Encrypted LS2](/proposals/149-b32-encrypted-ls2/)** - Base32 addressing for encrypted LeaseSets
- **[Red25519 Specification](/docs/specs/red25519-signature-scheme/)** - Detailed Red25519 implementation
- **[B32 Addressing Specification](/docs/specs/b32-for-encrypted-leasesets/)** - Base32 address format
- **[Network Database Documentation](/docs/specs/common-structures/)** - NetDB usage and operations
- **[I2CP Specification](/docs/specs/i2cp/)** - I2P Client Protocol

### Cryptographic References

- **[Ed25519 Paper](http://cr.yp.to/papers.html#ed25519)** - "High-speed high-security signatures" by Bernstein et al.
- **[ZCash Protocol Specification](https://zips.z.cash/protocol/protocol.pdf)** - Section 5.4.6: RedDSA signature scheme
- **[Tor Rendezvous Specification v3](https://spec.torproject.org/rend-spec)** - Tor's onion service specification (for comparison)

### Security References

- **[Key Blinding Security Discussion](https://lists.torproject.org/pipermail/tor-dev/2013-December/005943.html)** - Tor Project mailing list discussion
- **[Tor Ticket #8106](https://trac.torproject.org/projects/tor/ticket/8106)** - Key blinding implementation discussion
- **[PRNG Security](http://projectbullrun.org/dual-ec/ext-rand.html)** - Random number generator security considerations
- **[Tor PRNG Discussion](https://lists.torproject.org/pipermail/tor-dev/2015-November/009954.html)** - Discussion of PRNG usage in Tor

### Implementation References

- **[Java I2P Repository](https://github.com/i2p/i2p.i2p)** - Official Java implementation
- **[i2pd Repository](https://github.com/PurpleI2P/i2pd)** - C++ implementation
- **[I2P Website](/)** - Official I2P project website
- **[I2P Specifications](/docs/specs/)** - Complete specification index

### Version History

- **[I2P Release Notes](/en/blog)** - Official release announcements
- **[Java I2P Releases](https://github.com/i2p/i2p.i2p/releases)** - GitHub release history
- **[i2pd Releases](https://github.com/PurpleI2P/i2pd/releases)** - GitHub release history

---

## Appendix A: Cryptographic Constants

### Ed25519 / Red25519 Constants

```python
# Ponto base (gerador) do Ed25519

B = 2**255 - 19

# Ordem do Ed25519 (tamanho do campo escalar)

L = 2**252 + 27742317777372353535851937790883648493

# Valores de tipos de assinatura

SIGTYPE_ED25519 = 7    # 0x0007 SIGTYPE_RED25519 = 11  # 0x000b

# Tamanhos de chave

PRIVKEY_SIZE = 32  # bytes PUBKEY_SIZE = 32   # bytes SIGNATURE_SIZE = 64  # bytes

```

### ChaCha20 Constants

```python
# Parâmetros do ChaCha20

CHACHA20_KEY_SIZE = 32   # bytes (256 bits) CHACHA20_NONCE_SIZE = 12  # bytes (96 bits) CHACHA20_INITIAL_COUNTER = 1  # RFC 7539 permite 0 ou 1

```

### HKDF Constants

```python
# Parâmetros do HKDF (função de derivação de chaves baseada em HMAC)

HKDF_HASH = "SHA-256" HKDF_SALT_MAX = 32  # bytes (HashLen)

# Strings do parâmetro info do HKDF (separação de domínios)

HKDF_INFO_ALPHA = b"i2pblinding1" HKDF_INFO_LAYER1 = b"ELS2_L1K" HKDF_INFO_LAYER2 = b"ELS2_L2K" HKDF_INFO_DH_AUTH = b"ELS2_XCA" HKDF_INFO_PSK_AUTH = b"ELS2PSKA"

```

### Hash Personalization Strings

```python
# Strings de personalização do SHA-256

HASH_PERS_ALPHA = b"I2PGenerateAlpha" HASH_PERS_RED25519 = b"I2P_Red25519H(x)" HASH_PERS_CREDENTIAL = b"credential" HASH_PERS_SUBCREDENTIAL = b"subcredential"

```

### Structure Sizes

```python
# Tamanhos da Camada 0 (externa)

BLINDED_SIGTYPE_SIZE = 2   # bytes BLINDED_PUBKEY_SIZE = 32   # bytes (para Red25519) PUBLISHED_TS_SIZE = 4      # bytes EXPIRES_SIZE = 2           # bytes FLAGS_SIZE = 2             # bytes LEN_OUTER_CIPHER_SIZE = 2  # bytes SIGNATURE_SIZE = 64        # bytes (Red25519)

# Tamanhos dos blocos de chaves offline

OFFLINE_EXPIRES_SIZE = 4   # bytes OFFLINE_SIGTYPE_SIZE = 2   # bytes OFFLINE_SIGNATURE_SIZE = 64  # bytes

# Tamanhos da camada 1 (intermediária)

AUTH_FLAGS_SIZE = 1        # byte EPHEMERAL_PUBKEY_SIZE = 32  # bytes (autenticação DH) AUTH_SALT_SIZE = 32        # bytes (autenticação PSK) NUM_CLIENTS_SIZE = 2       # bytes CLIENT_ID_SIZE = 8         # bytes CLIENT_COOKIE_SIZE = 32    # bytes AUTH_CLIENT_ENTRY_SIZE = 40  # bytes (CLIENT_ID + CLIENT_COOKIE)

# Sobrecarga de criptografia

SALT_SIZE = 32  # bytes (anteposto a cada camada criptografada)

# Endereço Base32

B32_ENCRYPTED_DECODED_SIZE = 35  # bytes B32_ENCRYPTED_ENCODED_LEN = 56   # caracteres B32_SUFFIX = ".b32.i2p"

```

---

## Appendix B: Test Vectors

### Test Vector 1: Alpha Generation

**Input:**
```python
# Chave pública de destino (Ed25519)

A = bytes.fromhex('aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa') stA = 0x0007  # Ed25519 stA_prime = 0x000b  # Red25519 date = "20251015" secret = ""  # Segredo vazio

```

**Computation:**
```python
keydata = A || bytes([0x00, 0x07]) || bytes([0x00, 0x0b])

# keydata = 36 bytes

salt = SHA256(b"I2PGenerateAlpha" + keydata) ikm = b"20251015" info = b"i2pblinding1"

seed = HKDF(salt, ikm, info, 64) alpha = LEOS2IP(seed) mod L

```

**Expected Output:**
```
(Verifique contra a implementação de referência) alpha = [valor hexadecimal de 64 bytes]

```

### Test Vector 2: ChaCha20 Encryption

**Input:**
```python
key = bytes([i for i in range(32)])  # 0x00..0x1f nonce = bytes([i for i in range(12)])  # 0x00..0x0b plaintext = b"Hello, I2P!"

```

**Computation:**
```python
ciphertext = ChaCha20_Encrypt(key, nonce, plaintext, counter=1)

```

**Expected Output:**
```
ciphertext = [verificar contra os vetores de teste da RFC 7539]

```

### Test Vector 3: HKDF

**Input:**
```python
salt = bytes(32)  # All zeros ikm = b"test input keying material" info = b"ELS2_L1K" n = 44

```

**Computation:**
```python
keys = HKDF(salt, ikm, info, n)

```

**Expected Output:**
```
keys = [valor hexadecimal de 44 bytes]

```

### Test Vector 4: Base32 Address

**Input:**
```python
pubkey = bytes.fromhex('bbbb' + 'bb' * 30)  # 32 bytes unblinded_sigtype = 11  # Red25519 blinded_sigtype = 11    # Red25519

```

**Computation:**
```python
address = generate_encrypted_b32_address(pubkey, unblinded_sigtype, blinded_sigtype)

```

**Expected Output:**
```
address = [56 caracteres base32].b32.i2p

# Verifique se a soma de verificação é validada corretamente

```

---

## Appendix C: Glossary

**Alpha (α):** The secret blinding factor used to blind public and private keys. Generated from the destination, date, and optional secret.

**AuthCookie:** A 32-byte random value encrypted for each authorized client, used as input to Layer 2 encryption.

**B (Base Point):** The generator point for the Ed25519 elliptic curve.

**Blinded Key:** A public or private key that has been transformed using the alpha blinding factor. Blinded keys cannot be linked to the original keys without knowing alpha.

**ChaCha20:** A stream cipher providing fast, secure encryption without requiring AES hardware support.

**ClientID:** An 8-byte identifier derived from HKDF output, used to identify authorization entries for clients.

**ClientCookie:** A 32-byte encrypted value containing the authCookie for a specific client.

**Credential:** A 32-byte value derived from the destination's public key and signature types, binding encryption to knowledge of the destination.

**CSRNG:** Cryptographically Secure Random Number Generator. Must provide unpredictable output suitable for key generation.

**DH (Diffie-Hellman):** A cryptographic protocol for securely establishing shared secrets. I2P uses X25519.

**Ed25519:** An elliptic curve signature scheme providing fast signatures with 128-bit security level.

**Ephemeral Key:** A short-lived cryptographic key, typically used once and then discarded.

**Floodfill:** I2P routers that store and serve network database entries, including encrypted LeaseSets.

**HKDF:** HMAC-based Key Derivation Function, used to derive multiple cryptographic keys from a single source.

**L (Order):** The order of the Ed25519 scalar field (approximately 2^252).

**Layer 0 (Outer):** The plaintext portion of an encrypted LeaseSet, containing blinded key and metadata.

**Layer 1 (Middle):** The first encrypted layer, containing client authorization data.

**Layer 2 (Inner):** The innermost encrypted layer, containing the actual LeaseSet2 data.

**LeaseSet2 (LS2):** Second version of I2P's network database entry format, introducing encrypted variants.

**NetDB:** The I2P network database, a distributed hash table storing router and destination information.

**Offline Keys:** A feature allowing the main signing key to remain in cold storage while a transient key handles daily operations.

**PSK (Pre-Shared Key):** A symmetric key shared in advance between two parties, used for PSK client authorization.

**Red25519:** An Ed25519-based signature scheme with key blinding support, based on ZCash RedDSA.

**Salt:** Random data used as input to key derivation functions to ensure unique outputs.

**SigType:** A numeric identifier for signature algorithms (e.g., 7 = Ed25519, 11 = Red25519).

**Subcredential:** A 32-byte value derived from the credential and blinded public key, binding encryption to a specific encrypted LeaseSet.

**Transient Key:** A temporary signing key used with offline keys, with a limited validity period.

**X25519:** An elliptic curve Diffie-Hellman protocol over Curve25519, providing key agreement.

---

## Document Information

**Status:** This document represents the current stable encrypted LeaseSet specification as implemented in I2P since June 2019. The protocol is mature and widely deployed.

**Contributing:** For corrections or improvements to this documentation, please submit issues or pull requests to the I2P specifications repository.

**Support:** For questions about implementing encrypted LeaseSets:
- I2P Forum: https://i2pforum.net/
- IRC: #i2p-dev on OFTC
- Matrix: #i2p-dev:matrix.org

**Acknowledgments:** This specification builds on work by the I2P development team, ZCash cryptography research, and Tor Project's key blinding research.