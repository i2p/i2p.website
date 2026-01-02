---
title: "Transporte NTCP2"
description: "Transporte TCP baseado no Noise (framework de protocolos criptográficos) para links router-to-router"
slug: "ntcp2"
lastUpdated: "2025-10"
accurateFor: "0.9.66"
type: docs
---

## Visão geral

NTCP2 substitui o transporte NTCP legado por um aperto de mão baseado no Noise (framework de protocolos criptográficos) que resiste à impressão digital de tráfego, criptografa os campos de comprimento e oferece suporte a suítes criptográficas modernas. Routers podem executar NTCP2 juntamente com SSU2 como os dois protocolos de transporte obrigatórios na rede I2P. NTCP (versão 1) foi descontinuado na versão 0.9.40 (maio de 2019) e removido completamente na versão 0.9.50 (maio de 2021).

## Framework do Protocolo Noise

NTCP2 usa o Noise Protocol Framework [Revisão 33, 2017-10-04](https://noiseprotocol.org/noise.html) com extensões específicas do I2P:

- **Padrão**: `Noise_XK_25519_ChaChaPoly_SHA256`
- **Identificador estendido**: `Noise_XKaesobfse+hs2+hs3_25519_ChaChaPoly_SHA256` (para a inicialização do KDF (função de derivação de chaves))
- **Função DH**: X25519 (RFC 7748) - chaves de 32 bytes, codificação little-endian
- **Cifra**: AEAD_CHACHA20_POLY1305 (RFC 7539/RFC 8439)
  - nonce de 12 bytes: os primeiros 4 bytes iguais a zero, os últimos 8 bytes são um contador (little-endian)
  - Valor máximo do nonce: 2^64 - 2 (a conexão deve ser encerrada antes de atingir 2^64 - 1)
- **Função de hash**: SHA-256 (saída de 32 bytes)
- **MAC**: Poly1305 (tag de autenticação de 16 bytes)

### Extensões específicas do I2P

1. **Ofuscação AES**: Chaves efêmeras criptografadas com AES-256-CBC usando o hash do router de Bob e IV publicado
2. **Padding aleatório**: Padding em texto claro nas mensagens 1-2 (autenticado), padding AEAD a partir da mensagem 3 (criptografado)
3. **Ofuscação de comprimento com SipHash-2-4**: Comprimentos de frames de dois bytes são combinados por XOR com a saída do SipHash
4. **Estrutura de frames**: Frames com prefixo de comprimento para a fase de dados (compatibilidade com streaming TCP)
5. **Payloads baseados em blocos**: Formato de dados estruturado com blocos tipados

## Fluxo de Handshake (negociação inicial)

```
Alice (Initiator)             Bob (Responder)
SessionRequest  ──────────────────────►
                ◄────────────────────── SessionCreated
SessionConfirmed ──────────────────────►
```
### Handshake de três mensagens

1. **SessionRequest** - chave efêmera ofuscada de Alice, opções, indicações de preenchimento
2. **SessionCreated** - chave efêmera ofuscada de Bob, opções criptografadas, preenchimento
3. **SessionConfirmed** - chave estática criptografada de Alice e RouterInfo (dois quadros AEAD)

### Padrões de Mensagens do Noise

```
XK(s, rs):           Authentication   Confidentiality
  <- s               (Bob's static key known in advance)
  -> e, es                  0                2
  <- e, ee                  2                1
  -> s, se                  2                5
  <-                        2                5
```
**Níveis de autenticação:** - 0: Sem autenticação (qualquer parte poderia ter enviado) - 2: Autenticação do remetente resistente a key-compromise impersonation (impersonação por comprometimento de chave, KCI)

**Níveis de Confidencialidade:** - 1: Destinatário efêmero (sigilo direto, sem autenticação do destinatário) - 2: Destinatário conhecido, sigilo direto apenas no caso de comprometimento do remetente - 5: Sigilo direto forte (ephemeral-ephemeral + ephemeral-static DH)

## Especificações de Mensagens

### Notação de Chaves

- `RH_A` = Hash do router de Alice (32 bytes, SHA-256)
- `RH_B` = Hash do router de Bob (32 bytes, SHA-256)
- `||` = Operador de concatenação
- `byte(n)` = Um único byte com valor n
- Todos os inteiros de múltiplos bytes são **big-endian** (mais significativo primeiro), a menos que especificado em contrário
- As chaves X25519 são **little-endian** (menos significativo primeiro) (32 bytes)

### Criptografia autenticada (ChaCha20-Poly1305)

**Função de criptografia:**

```
AEAD_ChaCha20_Poly1305(key, nonce, associatedData, plaintext)
  → (ciphertext || MAC)
```
**Parâmetros:** - `key`: chave de cifra de 32 bytes proveniente da KDF (função de derivação de chaves) - `nonce`: 12 bytes (4 bytes nulos + contador de 8 bytes, little-endian) - `associatedData`: hash de 32 bytes na fase de handshake; comprimento zero na fase de dados - `plaintext`: Dados a cifrar (0+ bytes)

**Saída:** - Texto cifrado: Mesmo tamanho do texto em claro - MAC: 16 bytes (tag de autenticação Poly1305)

**Gerenciamento de nonce (número usado uma vez):** - O contador começa em 0 para cada instância de cifra - É incrementado a cada operação AEAD (Criptografia Autenticada com Dados Associados) naquela direção - Contadores separados para Alice→Bob e Bob→Alice na fase de dados - Deve encerrar a conexão antes que o contador atinja 2^64 - 1

## Mensagem 1: SessionRequest (solicitação de sessão)

Alice inicia uma conexão com Bob.

**Operações do Noise**: `e, es` (geração e troca de chaves efêmeras)

### Formato bruto

```
+----+----+----+----+----+----+----+----+
|                                       |
+    AES-256-CBC Encrypted X (32B)      +
|    Key: RH_B, IV: Bob's published IV  |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|                                       |
+    ChaChaPoly Frame (48 bytes)        +
|    Plaintext: 32B (X + options)       |
+    k from KDF-1, n=0, ad=h            +
|                                       |
+----+----+----+----+----+----+----+----+
|    Cleartext Padding (optional)       |
+    Length specified in options         +
|    0 to 65535 - 80 bytes              |
~           .   .   .                   ~
+----+----+----+----+----+----+----+----+
```
**Restrições de tamanho:** - Mínimo: 80 bytes (32 AES + 48 AEAD) - Máximo: 65535 bytes no total - **Caso especial**: Máx. 287 bytes ao conectar-se a endereços "NTCP" (detecção de versão)

### Conteúdo descriptografado

```
+----+----+----+----+----+----+----+----+
|                                       |
+    X (Alice ephemeral public key)     +
|    32 bytes, X25519, little-endian    |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|           Options Block               |
+             (16 bytes)                +
|                                       |
+----+----+----+----+----+----+----+----+
|    Cleartext Padding (optional)       |
~           .   .   .                   ~
+----+----+----+----+----+----+----+----+
```
### Bloco de Opções (16 bytes, big-endian (mais significativo primeiro))

```
+----+----+----+----+----+----+----+----+
| id | ver|  padLen | m3p2len | Rsvd(0) |
+----+----+----+----+----+----+----+----+
|        tsA        |   Reserved (0)    |
+----+----+----+----+----+----+----+----+

id      : 1 byte  - Network ID (2 for mainnet, 16-254 for testnets)
ver     : 1 byte  - Protocol version (currently 2)
padLen  : 2 bytes - Padding length in this message (0-65455)
m3p2len : 2 bytes - Length of SessionConfirmed part 2 frame
Rsvd    : 2 bytes - Reserved, set to 0
tsA     : 4 bytes - Unix timestamp (seconds since epoch)
Reserved: 4 bytes - Reserved, set to 0
```
**Campos críticos:** - **Network ID** (desde 0.9.42): Rejeição rápida de conexões entre redes - **m3p2len**: Tamanho exato da parte 2 da mensagem 3 (deve corresponder ao valor enviado)

### Função de Derivação de Chave (KDF-1)

**Inicializar protocolo:**

```
protocol_name = "Noise_XKaesobfse+hs2+hs3_25519_ChaChaPoly_SHA256"
h = SHA256(protocol_name)
ck = h  // Chaining key initialized to hash
```
**Operações de MixHash:**

```
h = SHA256(h)                    // Null prologue
h = SHA256(h || rs)              // Bob's static key (known)
h = SHA256(h || e.pubkey)        // Alice's ephemeral key X
// h is now the associated data for message 1 AEAD
```
**Operação MixKey (padrão es):**

```
dh_result = X25519(Alice.ephemeral_private, Bob.static_public)
temp_key = HMAC-SHA256(ck, dh_result)
ck = HMAC-SHA256(temp_key, byte(0x01))
k = HMAC-SHA256(temp_key, ck || byte(0x02))
// k is the cipher key for message 1
// ck is retained for message 2 KDF
```
### Notas de Implementação

1. **Ofuscação AES**: Usada apenas para resistência a DPI; qualquer pessoa com o hash do router do Bob e o IV pode descriptografar X
2. **Prevenção de repetição**: Bob deve armazenar em cache valores de X (ou equivalentes criptografados) por pelo menos 2*D segundos (D = desvio máximo de relógio)
3. **Validação do carimbo de tempo**: Bob deve rejeitar conexões com |tsA - current_time| > D (tipicamente D = 60 segundos)
4. **Validação da curva**: Bob deve verificar se X é um ponto X25519 válido
5. **Rejeição rápida**: Bob pode verificar X[31] & 0x80 == 0 antes da descriptografia (chaves X25519 válidas têm o bit mais significativo (MSB) limpo)
6. **Tratamento de erros**: Em qualquer falha, Bob fecha com TCP RST após um tempo limite aleatório e a leitura de um número aleatório de bytes
7. **Bufferização**: Alice deve enviar a mensagem inteira (incluindo o padding) de uma vez para eficiência

## Mensagem 2: SessionCreated (Sessão criada)

Bob responde a Alice.

**Operações do Noise**: `e, ee` (DH efêmero-efêmero)

### Formato bruto

```
+----+----+----+----+----+----+----+----+
|                                       |
+    AES-256-CBC Encrypted Y (32B)      +
|    Key: RH_B, IV: AES state from msg1 |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|                                       |
+    ChaChaPoly Frame (48 bytes)        +
|    Plaintext: 32B (Y + options)       |
+    k from KDF-2, n=0, ad=h            +
|                                       |
+----+----+----+----+----+----+----+----+
|    Cleartext Padding (optional)       |
+    Length specified in options         +
|    0 to 65535 - 80 bytes              |
~           .   .   .                   ~
+----+----+----+----+----+----+----+----+
```
### Conteúdo descriptografado

```
+----+----+----+----+----+----+----+----+
|                                       |
+    Y (Bob ephemeral public key)       +
|    32 bytes, X25519, little-endian    |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|           Options Block               |
+             (16 bytes)                +
|                                       |
+----+----+----+----+----+----+----+----+
|    Cleartext Padding (optional)       |
~           .   .   .                   ~
+----+----+----+----+----+----+----+----+
```
### Bloco de Opções (16 bytes, big-endian)

```
+----+----+----+----+----+----+----+----+
| Rsvd(0) | padLen  |   Reserved (0)    |
+----+----+----+----+----+----+----+----+
|        tsB        |   Reserved (0)    |
+----+----+----+----+----+----+----+----+

Rsvd    : 2 bytes - Reserved, set to 0
padLen  : 2 bytes - Padding length in this message
Reserved: 10 bytes - Reserved, set to 0
tsB     : 4 bytes - Unix timestamp (seconds since epoch)
```
### Função de Derivação de Chaves (KDF-2)

**Operações do MixHash:**

```
h = SHA256(h || encrypted_payload_msg1)  // 32-byte ciphertext
if (msg1_padding_length > 0):
    h = SHA256(h || padding_from_msg1)
h = SHA256(h || e.pubkey)                // Bob's ephemeral key Y
// h is now the associated data for message 2 AEAD
```
**MixKey Operation (operação de mistura de chave) (ee pattern):**

```
dh_result = X25519(Bob.ephemeral_private, Alice.ephemeral_public)
temp_key = HMAC-SHA256(ck, dh_result)
ck = HMAC-SHA256(temp_key, byte(0x01))
k = HMAC-SHA256(temp_key, ck || byte(0x02))
// k is the cipher key for message 2
// ck is retained for message 3 KDF
```
**Limpeza de memória:**

```
// Overwrite ephemeral keys after ee DH
Alice.ephemeral_public = zeros(32)
Alice.ephemeral_private = zeros(32)  // Bob side
Bob.received_ephemeral = zeros(32)    // Bob side
```
### Notas de implementação

1. **Encadeamento AES**: A criptografia de Y usa o estado do AES-CBC da mensagem 1 (não reinicializado)
2. **Prevenção de repetição (replay)**: Alice deve armazenar em cache os valores de Y por pelo menos 2*D segundos
3. **Validação do carimbo de data/hora**: Alice deve rejeitar |tsB - current_time| > D
4. **Validação da curva**: Alice deve verificar se Y é um ponto X25519 válido
5. **Tratamento de erros**: Alice encerra com TCP RST em qualquer falha
6. **Armazenamento em buffer**: Bob deve descarregar a mensagem inteira de uma só vez

## Mensagem 3: SessionConfirmed (confirmação de sessão)

Alice confirma a sessão e envia RouterInfo (informações do router).

**Operações do Noise**: `s, se` (revelação da chave estática e DH estático-efêmero)

### Estrutura em duas partes

A mensagem 3 consiste em **dois quadros AEAD separados**: (AEAD: criptografia autenticada com dados associados)

1. **Parte 1**: Quadro fixo de 48 bytes com a chave estática criptografada de Alice
2. **Parte 2**: Quadro de comprimento variável com RouterInfo (informações do router), opções e preenchimento

### Formato bruto

```
+----+----+----+----+----+----+----+----+
|    ChaChaPoly Frame 1 (48 bytes)      |
+    Plaintext: Alice static key (32B)  +
|    k from KDF-2, n=1, ad=h            |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|                                       |
+    ChaChaPoly Frame 2 (variable)      +
|    Length specified in msg1.m3p2len   |
+    k from KDF-3, n=0, ad=h            +
|    Plaintext: RouterInfo + padding    |
+                                       +
|                                       |
~           .   .   .                   ~
+----+----+----+----+----+----+----+----+
```
**Restrições de tamanho:** - Parte 1: Exatamente 48 bytes (32 de texto em claro + 16 MAC) - Parte 2: Comprimento especificado na mensagem 1 (campo m3p2len) - Máximo total: 65535 bytes (parte 1 máx. 48, então parte 2 máx. 65487)

### Conteúdo decifrado

**Parte 1:**

```
+----+----+----+----+----+----+----+----+
|                                       |
+    S (Alice static public key)        +
|    32 bytes, X25519, little-endian    |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
```
**Parte 2:**

```
+----+----+----+----+----+----+----+----+
|    Block: RouterInfo (required)       |
+    Type=2, contains Alice's RI         +
|                                       |
~           .   .   .                   ~
+----+----+----+----+----+----+----+----+
|    Block: Options (optional)          |
+    Type=1, padding parameters          +
|                                       |
+----+----+----+----+----+----+----+----+
|    Block: Padding (optional)          |
+    Type=254, random data               +
|    MUST be last block if present      |
~           .   .   .                   ~
+----+----+----+----+----+----+----+----+
```
### Função de Derivação de Chaves (KDF-3)

**Parte 1 (padrão s):**

```
h = SHA256(h || encrypted_payload_msg2)  // 32-byte ciphertext
if (msg2_padding_length > 0):
    h = SHA256(h || padding_from_msg2)

// Encrypt static key with message 2 cipher key
ciphertext = AEAD_ChaCha20_Poly1305(k_msg2, n=1, h, Alice.static_public)
h = SHA256(h || ciphertext)  // 48 bytes (32 + 16)
// h is now the associated data for message 3 part 2
```
**Parte 2 (padrão se):**

```
dh_result = X25519(Alice.static_private, Bob.ephemeral_public)
temp_key = HMAC-SHA256(ck, dh_result)
ck = HMAC-SHA256(temp_key, byte(0x01))
k = HMAC-SHA256(temp_key, ck || byte(0x02))
// k is the cipher key for message 3 part 2
// ck is retained for data phase KDF

ciphertext = AEAD_ChaCha20_Poly1305(k, n=0, h, payload)
h = SHA256(h || ciphertext)
// h is retained for SipHash KDF
```
**Limpeza de memória:**

```
// Overwrite Bob's ephemeral key after se DH
Alice.received_ephemeral = zeros(32)  // Alice side
Bob.ephemeral_public = zeros(32)       // Bob side
Bob.ephemeral_private = zeros(32)      // Bob side
```
### Notas de Implementação

1. **Validação do RouterInfo**: Bob deve verificar a assinatura, o carimbo de data e hora e a consistência da chave
2. **Correspondência de chave**: Bob deve verificar se a chave estática de Alice na parte 1 corresponde à chave em RouterInfo
3. **Local da chave estática**: Procure o parâmetro "s" correspondente em NTCP ou NTCP2 RouterAddress
4. **Ordem dos blocos**: RouterInfo deve vir primeiro, Options em segundo (se presente), Padding por último (se presente)
5. **Planejamento do tamanho**: Alice deve garantir que m3p2len na mensagem 1 corresponda exatamente ao tamanho da parte 2
6. **Armazenamento em buffer**: Alice deve enviar ambas as partes juntas em um único envio TCP
7. **Encadeamento opcional**: Alice pode anexar imediatamente um data phase frame (quadro da fase de dados) para eficiência

## Fase de Dados

Após a conclusão do handshake, todas as mensagens usam quadros AEAD (criptografia autenticada com dados associados) de comprimento variável com campos de comprimento ofuscados.

### Função de Derivação de Chaves (Fase de Dados)

**Função Split (Noise):**

```
// Generate transmit and receive keys
zerolen = ""  // Zero-length byte array
temp_key = HMAC-SHA256(ck, zerolen)

// Alice transmits to Bob
k_ab = HMAC-SHA256(temp_key, byte(0x01))

// Bob transmits to Alice  
k_ba = HMAC-SHA256(temp_key, k_ab || byte(0x02))

// Cleanup
ck = zeros(32)
temp_key = zeros(32)
```
**Derivação de chave com SipHash (função de hash autenticado com chave):**

```
// Generate additional symmetric key for SipHash
ask_master = HMAC-SHA256(temp_key, "ask" || byte(0x01))

// "siphash" is 7 bytes US-ASCII
temp_key2 = HMAC-SHA256(ask_master, h || "siphash")
sip_master = HMAC-SHA256(temp_key2, byte(0x01))

// Alice to Bob SipHash keys
temp_key3 = HMAC-SHA256(sip_master, zerolen)
sipkeys_ab = HMAC-SHA256(temp_key3, byte(0x01))
sipk1_ab = sipkeys_ab[0:7]   // 8 bytes, little-endian
sipk2_ab = sipkeys_ab[8:15]  // 8 bytes, little-endian
sipiv_ab = sipkeys_ab[16:23] // 8 bytes, IV

// Bob to Alice SipHash keys
sipkeys_ba = HMAC-SHA256(temp_key3, sipkeys_ab || byte(0x02))
sipk1_ba = sipkeys_ba[0:7]   // 8 bytes, little-endian
sipk2_ba = sipkeys_ba[8:15]  // 8 bytes, little-endian
sipiv_ba = sipkeys_ba[16:23] // 8 bytes, IV
```
### Estrutura do Quadro

```
+----+----+----+----+----+----+----+----+
|Obfs Len |                             |
+----+----+    ChaChaPoly Frame         +
|    Encrypted Block Data               |
+    k_ab (Alice→Bob) or k_ba (Bob→Alice)|
|    Nonce starts at 0, increments      |
+    No associated data (empty string)  +
|                                       |
~           .   .   .                   ~
|                                       |
+----+----+----+----+----+----+----+----+
|    Poly1305 MAC (16 bytes)            |
+----+----+----+----+----+----+----+----+
```
**Restrições de quadro:** - Mínimo: 18 bytes (2 de comprimento ofuscado + 0 em texto claro + 16 MAC) - Máximo: 65537 bytes (2 de comprimento ofuscado + 65535 do quadro) - Recomendado: Poucos KB por quadro (minimizar a latência do receptor)

### Ofuscação do Comprimento com SipHash

**Finalidade**: Impedir que a DPI (inspeção profunda de pacotes) identifique os limites de quadros

**Algoritmo:**

```
// Initialization (per direction)
IV[0] = sipiv  // From KDF

// For each frame:
IV[n] = SipHash-2-4(sipk1, sipk2, IV[n-1])
Mask[n] = IV[n][0:1]  // First 2 bytes of IV
ObfuscatedLength = ActualLength XOR Mask[n]

// Send 2-byte ObfuscatedLength, then ActualLength bytes
```
**Decodificação:**

```
// Receiver maintains identical IV chain
IV[n] = SipHash-2-4(sipk1, sipk2, IV[n-1])
Mask[n] = IV[n][0:1]
ActualLength = ObfuscatedLength XOR Mask[n]
// Read ActualLength bytes (includes 16-byte MAC)
```
**Notas:** - Separe cadeias de IV para cada direção (Alice→Bob e Bob→Alice) - Se SipHash retornar uint64, use os 2 bytes menos significativos como máscara - Converta o uint64 no próximo IV em bytes little-endian

### Formato de bloco

Cada quadro contém zero ou mais blocos:

```
+----+----+----+----+----+----+----+----+
|Type| Length  |       Data              |
+----+----+----+                        +
|                                       |
~           .   .   .                   ~
+----+----+----+----+----+----+----+----+

Type  : 1 byte  - Block type identifier
Length: 2 bytes - Big-endian, data size (0-65516)
Data  : Variable length payload
```
**Limites de tamanho:** - Quadro máximo: 65535 bytes (incluindo MAC) - Espaço máximo do bloco: 65519 bytes (quadro - MAC de 16 bytes) - Bloco único máximo: 65519 bytes (cabeçalho de 3 bytes + 65516 de dados)

### Tipos de Blocos

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Name</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem;">DateTime</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Time synchronization (4-byte timestamp)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Options</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Padding parameters, dummy traffic</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td><td style="border:1px solid var(--color-border); padding:0.5rem;">RouterInfo</td><td style="border:1px solid var(--color-border); padding:0.5rem;">RouterInfo delivery/flooding</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td><td style="border:1px solid var(--color-border); padding:0.5rem;">I2NP</td><td style="border:1px solid var(--color-border); padding:0.5rem;">I2NP message with shortened header</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Termination</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Explicit connection close</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">224-253</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Experimental features</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">254</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Padding</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Random padding (must be last)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">255</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Future extensions</td></tr>
  </tbody>
</table>
**Regras de Ordenação de Blocos:** - **Mensagem 3 parte 2**: RouterInfo, Options (opcional), Padding (opcional) - NENHUM outro tipo - **Fase de dados**: Qualquer ordem, exceto:   - Padding DEVE ser o último bloco, se presente   - Termination DEVE ser o último bloco (exceto Padding), se presente - Múltiplos blocos I2NP são permitidos por quadro - Múltiplos blocos Padding NÃO são permitidos por quadro

### Tipo de Bloco 0: DateTime

Sincronização de tempo para detecção de desvio do relógio.

```
+----+----+----+----+----+----+----+
| 0  |    4    |     timestamp     |
+----+----+----+----+----+----+----+

Type     : 0
Length   : 4 (big-endian)
Timestamp: 4 bytes, Unix seconds (big-endian)
```
**Implementação**: Arredonde para o segundo mais próximo para evitar o acúmulo de viés do relógio.

### Tipo de Bloco 1: Opções

Parâmetros de preenchimento e modelagem de tráfego.

```
+----+----+----+----+----+----+----+----+
| 1  |  size   |tmin|tmax|rmin|rmax|tdmy|
+----+----+----+----+----+----+----+----+
|tdmy|  rdmy   |  tdelay |  rdelay |    |
+----+----+----+----+----+----+----+    +
|         more_options (TBD)            |
~           .   .   .                   ~
+----+----+----+----+----+----+----+----+

Type  : 1
Length: 12+ bytes (big-endian)
```
**Proporções de preenchimento** (número de ponto fixo 4.4, valor/16.0): - `tmin`: Proporção mínima de preenchimento na transmissão (0.0 - 15.9375) - `tmax`: Proporção máxima de preenchimento na transmissão (0.0 - 15.9375) - `rmin`: Proporção mínima de preenchimento na recepção (0.0 - 15.9375) - `rmax`: Proporção máxima de preenchimento na recepção (0.0 - 15.9375)

**Exemplos:** - 0x00 = 0% de preenchimento - 0x01 = 6.25% de preenchimento - 0x10 = 100% de preenchimento (proporção de 1:1) - 0x80 = 800% de preenchimento (proporção de 8:1)

**Tráfego de preenchimento (dummy traffic):** - `tdmy`: Máximo que está disposto a enviar (2 bytes, média em bytes/seg) - `rdmy`: Solicitado para receber (2 bytes, média em bytes/seg)

**Inserção de atraso:** - `tdelay`: Máximo disposto a inserir (2 bytes, média em milissegundos) - `rdelay`: Atraso solicitado (2 bytes, média em milissegundos)

**Diretrizes:** - Valores mínimos indicam a resistência desejada à análise de tráfego - Valores máximos indicam restrições de largura de banda - O emissor deve respeitar o limite máximo do receptor - O emissor pode respeitar o mínimo do receptor dentro das restrições - Não há mecanismo de imposição; as implementações podem variar

### Tipo de bloco 2: RouterInfo (informações do router)

Entrega de RouterInfo (informações do router) para preenchimento e difusão do netdb.

```
+----+----+----+----+----+----+----+----+
| 2  |  size   |flg |    RouterInfo     |
+----+----+----+----+                   +
|                                       |
~           .   .   .                   ~
+----+----+----+----+----+----+----+----+

Type : 2
Length: Flag (1 byte) + RouterInfo size
Flag : Bit 0 = flood request (1) or local store (0)
       Bits 1-7 = Reserved, set to 0
```
**Uso:**

**Na Mensagem 3 Parte 2** (handshake): - Alice envia seu RouterInfo para Bob - Bit de Flood tipicamente 0 (armazenamento local) - RouterInfo NÃO comprimido com gzip

**Na Fase de Dados:** - Qualquer das partes pode enviar seu RouterInfo atualizado - Bit de flood = 1: Solicitar distribuição via floodfill (se o receptor for floodfill) - Bit de flood = 0: Apenas armazenamento local no netdb

**Requisitos de Validação:** 1. Verificar se o tipo de assinatura é suportado 2. Verificar a assinatura do RouterInfo (registro de informações do router no I2P) 3. Verificar se o carimbo de data/hora está dentro de limites aceitáveis 4. Para o handshake (negociação inicial): Verificar se a chave estática corresponde ao parâmetro "s" do endereço NTCP2 5. Para a fase de dados: Verificar se o hash do router corresponde ao par da sessão 6. Somente propague RouterInfos com endereços publicados

**Notas:** - Sem mecanismo de ACK (use I2NP DatabaseStore com token de resposta, se necessário) - Pode conter RouterInfos (informações do router) de terceiros (uso de floodfill) - NÃO compactado com gzip (ao contrário de I2NP DatabaseStore)

### Tipo de Bloco 3: Mensagem I2NP

Mensagem I2NP com cabeçalho reduzido de 9 bytes.

```
+----+----+----+----+----+----+----+----+
| 3  |  size   |type|    msg_id         |
+----+----+----+----+----+----+----+----+
|   expiration  |     I2NP payload      |
+----+----+----+                        +
|                                       |
~           .   .   .                   ~
+----+----+----+----+----+----+----+----+

Type      : 3
Length    : 9 + payload_size (big-endian)
Type      : 1 byte, I2NP message type
Msg_ID    : 4 bytes, big-endian, I2NP message ID
Expiration: 4 bytes, big-endian, Unix timestamp (seconds)
Payload   : I2NP message body (length = size - 9)
```
**Diferenças em relação ao NTCP1:** - Expiração: 4 bytes (segundos) vs 8 bytes (milissegundos) - Tamanho: Omitido (derivável a partir do tamanho do bloco) - Checksum: Omitido (AEAD fornece integridade) - Cabeçalho: 9 bytes vs 16 bytes (redução de 44%)

**Fragmentação:** - mensagens I2NP NÃO DEVEM ser fragmentadas entre blocos - mensagens I2NP NÃO DEVEM ser fragmentadas entre frames - Múltiplos blocos I2NP permitidos por frame

### Tipo de Bloco 4: Encerramento

Encerramento explícito da conexão com código de motivo.

```
+----+----+----+----+----+----+----+----+
| 4  |  size   |  valid_frames_recv    |
+----+----+----+----+----+----+----+----+
| (continued) |rsn |   additional_data   |
+----+----+----+----+                   +
|                                       |
~           .   .   .                   ~
+----+----+----+----+----+----+----+----+

Type            : 4
Length          : 9+ bytes (big-endian)
Valid_Frames_Recv: 8 bytes, big-endian (receive nonce value)
                  0 if error in handshake phase
Reason          : 1 byte (see table below)
Additional_Data : Optional (format unspecified, for debugging)
```
**Códigos de motivo:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Code</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Reason</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Phase</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Normal close / unspecified</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Any</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Termination received</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Data</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Idle timeout</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Data</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Router shutdown</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Data</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Data phase AEAD failure</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Data</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">5</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Incompatible options</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshake</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">6</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Incompatible signature type</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshake</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">7</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Clock skew</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshake</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">8</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Padding violation</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Any</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">9</td><td style="border:1px solid var(--color-border); padding:0.5rem;">AEAD framing error</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Data</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">10</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Payload format error</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Data</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">11</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Message 1 error</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshake</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Message 2 error</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshake</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">13</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Message 3 error</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshake</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">14</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Intra-frame read timeout</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Data</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">15</td><td style="border:1px solid var(--color-border); padding:0.5rem;">RouterInfo signature verification fail</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshake</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">16</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Static key parameter mismatch</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshake</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">17</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Banned</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Any</td></tr>
  </tbody>
</table>
**Regras:** - A terminação DEVE ser o último bloco não de preenchimento no quadro - No máximo um bloco de terminação por quadro - O emissor deveria fechar a conexão após o envio - O receptor deveria fechar a conexão após o recebimento

**Tratamento de erros:** - Erros de handshake: Normalmente encerrar com TCP RST (sem bloco de terminação) - Erros de AEAD (cifra autenticada com dados associados) na fase de dados: Tempo limite aleatório + leitura aleatória, em seguida, enviar a terminação - Veja a seção "AEAD Error Handling" para procedimentos de segurança

### Tipo de bloco 254: Preenchimento

Preenchimento aleatório para resistência à análise de tráfego.

```
+----+----+----+----+----+----+----+----+
|254 |  size   |     random_data       |
+----+----+----+                        +
|                                       |
~           .   .   .                   ~
+----+----+----+----+----+----+----+----+

Type: 254
Length: 0-65516 bytes (big-endian)
Data: Cryptographically random bytes
```
**Regras:** - O padding (preenchimento) DEVE ser o último bloco no quadro, se presente - Padding de comprimento zero é permitido - Apenas um bloco de padding por quadro - Quadros apenas de padding são permitidos - Deve respeitar os parâmetros negociados do bloco Options

**Preenchimento nas mensagens 1-2:** - Fora do quadro AEAD (criptografia autenticada com dados associados) (texto em claro) - Incluído na cadeia de hash da próxima mensagem (autenticado) - Manipulação detectada quando o AEAD da próxima mensagem falha

**Preenchimento em Message 3+ e Fase de Dados:** - Dentro do quadro AEAD (criptografado e autenticado) - Usado para modelagem de tráfego e ofuscação do tamanho

## Tratamento de erros de AEAD (criptografia autenticada com dados associados)

**Requisitos de Segurança Críticos:**

### Fase de Handshake (negociação inicial) (Mensagens 1-3)

**Tamanho de Mensagem Conhecido:** - Os tamanhos de mensagem são predefinidos ou especificados antecipadamente - A falha de autenticação em AEAD (autenticação e criptografia com dados associados) é inequívoca

**Resposta de Bob à falha na Mensagem 1:** 1. Definir tempo limite aleatório (faixa dependente da implementação, sugere-se 100-500ms) 2. Ler uma quantidade aleatória de bytes (faixa dependente da implementação, sugere-se 1KB-64KB) 3. Fechar a conexão com TCP RST (sem resposta) 4. Bloquear temporariamente o IP de origem 5. Registrar falhas repetidas para banimentos de longo prazo

**Resposta de Alice à falha da Mensagem 2:** 1. Fechar a conexão imediatamente com TCP RST 2. Nenhuma resposta para Bob

**Resposta de Bob à falha da Mensagem 3:** 1. Fechar a conexão imediatamente com TCP RST 2. Não responder a Alice

### Fase de dados

**Tamanho da Mensagem Ofuscado:** - O campo de comprimento é ofuscado com SipHash - Comprimento inválido ou falha de AEAD podem indicar:   - Sondagem por um atacante   - Corrupção na rede   - IV de SipHash dessincronizado   - Par malicioso

**Resposta a erro de AEAD (Autenticação e Criptografia com Dados Associados) ou Erro de Comprimento:** 1. Defina um tempo limite aleatório (sugestão: 100-500ms) 2. Leia um número aleatório de bytes (sugestão: 1KB-64KB) 3. Envie um bloco de término com código de motivo 4 (falha de AEAD) ou 9 (erro de enquadramento) 4. Feche a conexão

**Prevenção de Oráculo de Descriptografia:** - Nunca revele o tipo de erro ao par antes de um tempo limite aleatório - Nunca omita a validação do tamanho antes da verificação de AEAD (criptografia autenticada com dados associados) - Trate um tamanho inválido da mesma forma que uma falha de AEAD - Use um caminho de tratamento de erros idêntico para ambos os erros

**Considerações de Implementação:** - Algumas implementações podem continuar após erros de AEAD (criptografia autenticada com dados associados) se forem infrequentes - Encerrar após erros repetidos (limiar sugerido: 3-5 erros por hora) - Equilíbrio entre a recuperação de erros e a segurança

## RouterInfo (metadados do router no I2P) publicado

### Formato de Endereço do Router

O suporte a NTCP2 é anunciado por meio de entradas RouterAddress (endereço do router) publicadas com opções específicas.

**Estilo de Transporte:** - `"NTCP2"` - NTCP2 apenas nesta porta - `"NTCP"` - Tanto NTCP quanto NTCP2 nesta porta (detecção automática)   - **Nota**: suporte a NTCP (v1) removido na 0.9.50 (maio de 2021)   - o estilo "NTCP" agora está obsoleto; use "NTCP2"

### Opções obrigatórias

**Todos os endereços NTCP2 publicados:**

1. **`host`** - Endereço IP (IPv4 ou IPv6) ou nome do host
   - Formato: Notação IP padrão ou nome de domínio
   - Pode ser omitido em routers somente de saída ou ocultos

2. **`port`** - Número da porta TCP
   - Formato: Inteiro, 1-65535
   - Pode ser omitida para routers outbound-only (apenas de saída) ou ocultos

3. **`s`** - Chave pública estática (X25519)
   - Formato: codificado em Base64, 44 caracteres
   - Codificação: alfabeto Base64 do I2P
   - Origem: chave pública X25519 de 32 bytes, little-endian (ordem de bytes do menos significativo primeiro)

4. **`i`** - Vetor de inicialização (IV) para AES
   - Formato: codificado em Base64, 24 caracteres
   - Codificação: alfabeto Base64 do I2P
   - Origem: IV de 16 bytes, big-endian

5. **`v`** - Versão do protocolo
   - Formato: inteiro ou inteiros separados por vírgula
   - Atual: `"2"`
   - Futuro: `"2,3"` (deve estar em ordem numérica)

**Opções opcionais:**

6. **`caps`** - Capacidades (desde 0.9.50)
   - Formato: Cadeia de caracteres de capacidades
   - Valores:
     - `"4"` - Capacidade de saída IPv4
     - `"6"` - Capacidade de saída IPv6
     - `"46"` - Ambos IPv4 e IPv6 (ordem recomendada)
   - Não é necessário se `host` estiver publicado
   - Útil para routers ocultos/atrás de firewall

7. **`cost`** - Prioridade do endereço
   - Formato: inteiro, 0-255
   - Valores menores = prioridade mais alta
   - Sugerido: 5-10 para endereços normais
   - Sugerido: 14 para endereços não publicados

### Exemplos de entradas de RouterAddress

**Endereço IPv4 publicado:**

```
<Address cost="5">
  <transport_style>NTCP2</transport_style>
  <options>
    <host>192.0.2.1</host>
    <port>8887</port>
    <s>9EjeG7BZeznKbL9a2fXx8JBDPgLZbLmKbqY3QrNGJCo=</s>
    <i>MDEyMzQ1Njc4OUFCQ0RFRg==</i>
    <v>2</v>
  </options>
</Address>
```
**Router oculto (somente de saída):**

```
<Address cost="14">
  <transport_style>NTCP2</transport_style>
  <options>
    <s>9EjeG7BZeznKbL9a2fXx8JBDPgLZbLmKbqY3QrNGJCo=</s>
    <v>2</v>
    <caps>4</caps>
  </options>
</Address>
```
**Router Dual-Stack (pilha dupla):**

```
<!-- IPv4 Address -->
<Address cost="5">
  <transport_style>NTCP2</transport_style>
  <options>
    <host>192.0.2.1</host>
    <port>8887</port>
    <s>9EjeG7BZeznKbL9a2fXx8JBDPgLZbLmKbqY3QrNGJCo=</s>
    <i>MDEyMzQ1Njc4OUFCQ0RFRg==</i>
    <v>2</v>
  </options>
</Address>

<!-- IPv6 Address (same keys, same port) -->
<Address cost="5">
  <transport_style>NTCP2</transport_style>
  <options>
    <host>2001:db8::1</host>
    <port>8887</port>
    <s>9EjeG7BZeznKbL9a2fXx8JBDPgLZbLmKbqY3QrNGJCo=</s>
    <i>MDEyMzQ1Njc4OUFCQ0RFRg==</i>
    <v>2</v>
  </options>
</Address>
```
**Regras importantes:** - Vários endereços NTCP2 com a **mesma porta** DEVEM usar valores **idênticos** `s`, `i` e `v` - Portas diferentes podem usar chaves diferentes - Routers dual-stack (pilha dupla) devem publicar endereços IPv4 e IPv6 separados

### Endereço NTCP2 não publicado

**Para Routers somente de saída:**

Se um router não aceita conexões NTCP2 de entrada, mas inicia conexões de saída, ele DEVE ainda assim publicar um RouterAddress (estrutura de endereço do router) com:

```xml
<Address cost="14">
  <transport_style>NTCP2</transport_style>
  <options>
    <s>9EjeG7BZeznKbL9a2fXx8JBDPgLZbLmKbqY3QrNGJCo=</s>
    <v>2</v>
  </options>
</Address>
```
**Objetivo:** - Permite que Bob valide a chave estática de Alice durante o handshake (negociação inicial) - Necessária para a verificação de RouterInfo (informações do router) na mensagem 3, parte 2 - Não é necessário `i`, `host` ou `port` (somente saída)

**Alternativa:** - Adicione `s` e `v` ao endereço "NTCP" ou SSU já publicado

### Rotação da chave pública e do vetor de inicialização (IV)

**Política de Segurança Crítica:**

**Regras gerais:** 1. **Nunca realizar a rotação enquanto o router estiver em execução** 2. **Armazene de forma persistente a chave e o IV (vetor de inicialização)** entre reinicializações 3. **Acompanhe o tempo de inatividade anterior** para determinar a elegibilidade para rotação

**Tempo mínimo de inatividade antes da rotação:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Router Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Min Downtime</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Reason</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Published NTCP2 address</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>1 month</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Many routers cache RouterInfo</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Published SSU only (no NTCP2)</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>1 day</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Moderate caching</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">No published addresses (hidden)</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>2 hours</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Minimal impact</td></tr>
  </tbody>
</table>
**Gatilhos adicionais:** - Alteração do endereço IP local: Pode rotacionar independentemente do tempo de inatividade - Router "rekey" (novo Router Hash): Gera novas chaves

**Justificativa:** - Evita expor horários de reinício por meio de alterações de chave - Permite que RouterInfos (informações do router) em cache expirem naturalmente - Mantém a estabilidade da rede - Reduz tentativas de conexão malsucedidas

**Implementação:** 1. Armazenar de forma persistente a chave, o IV (vetor de inicialização) e o timestamp do último desligamento 2. Na inicialização, calcular downtime = current_time - last_shutdown 3. Se downtime > mínimo para o tipo de router, pode rotacionar 4. Se o IP mudou ou rekeying (troca de chaves), pode rotacionar 5. Caso contrário, reutilizar a chave anterior e o IV

**Rotação do IV:** - Sujeita às mesmas regras que a rotação de chaves - Presente apenas em endereços publicados (não em routers ocultos) - Recomenda-se alterar o IV sempre que a chave mudar

## Detecção de Versão

**Contexto:** Quando `transportStyle="NTCP"` (legado), Bob oferece suporte a NTCP v1 e v2 na mesma porta e deve detectar automaticamente a versão do protocolo.

**Algoritmo de detecção:**

```
1. Wait for at least 64 bytes (minimum NTCP2 message 1 size)

2. If received ≥ 288 bytes:
   → Connection is NTCP version 1 (NTCP1 message 1 is 288 bytes)

3. If received < 288 bytes:
   
   Option A (conservative, pre-NTCP2 majority):
   a. Wait additional short time (e.g., 100-500ms)
   b. If total received ≥ 288 bytes → NTCP1
   c. Otherwise → Attempt NTCP2 decode
   
   Option B (aggressive, post-NTCP2 majority):
   a. Attempt NTCP2 decode immediately:
      - Decrypt first 32 bytes (X key) with AES-256-CBC
      - Verify valid X25519 point (X[31] & 0x80 == 0)
      - Verify AEAD frame
   b. If decode succeeds → NTCP2
   c. If decode fails → Wait for more data or NTCP1
```
**Verificação rápida do MSB (bit mais significativo):** - Antes da descriptografia AES, verifique: `encrypted_X[31] & 0x80 == 0` - Chaves X25519 válidas têm o MSB limpo - Falha indica provável NTCP1 (ou ataque) - Implemente resistência a sondagens (tempo limite aleatório + leitura) em caso de falha

**Requisitos de Implementação:**

1. **Responsabilidade de Alice:**
   - Ao conectar-se ao endereço "NTCP", limitar a mensagem 1 a, no máximo, 287 bytes
   - Armazenar em buffer e enviar toda a mensagem 1 de uma vez
   - Aumenta a probabilidade de entrega em um único pacote TCP

2. **Responsabilidades de Bob:**
   - Armazenar em buffer os dados recebidos antes de decidir a versão
   - Implementar tratamento adequado de tempo limite (timeout)
   - Usar TCP_NODELAY para detecção rápida da versão
   - Armazenar em buffer e descarregar toda a mensagem 2 de uma vez após detectar a versão

**Considerações de Segurança:** - Ataques de segmentação: Bob deve ser resiliente à segmentação de TCP - Ataques de sondagem: Implementar atrasos aleatórios e leituras de bytes em caso de falhas - Prevenção de DoS: Limitar o número de conexões pendentes simultâneas - Tempos limite de leitura: Tanto por leitura quanto total (proteção contra "slowloris")

## Diretrizes sobre desvio de relógio

**Campos de carimbo de data/hora:** - Mensagem 1: `tsA` (carimbo de data/hora de Alice) - Mensagem 2: `tsB` (carimbo de data/hora de Bob) - Mensagem 3+: blocos DateTime (data e hora) opcionais

**Desvio Máximo (D):** - Típico: **±60 segundos** - Configurável conforme a implementação - Desvio > D é geralmente fatal

### Tratamento de Bob (Mensagem 1)

```
1. Receive tsA from Alice
2. skew = tsA - current_time
3. If |skew| > D:
   a. Still send message 2 (allows Alice to calculate skew)
   b. Include tsB in message 2
   c. Do NOT initiate handshake completion
   d. Optionally: Temporary ban Alice's IP
   e. After message 2 sent, close connection

4. If |skew| ≤ D:
   a. Continue handshake normally
```
**Justificativa:** Enviar a mensagem 2 mesmo em caso de defasagem do relógio permite que Alice diagnostique problemas de relógio.

### Tratamento de Alice (Mensagem 2)

```
1. Receive tsB from Bob
2. RTT = (current_time_now - tsA_sent)
3. adjusted_skew = (tsB - current_time_now) - (RTT / 2)
4. If |adjusted_skew| > D:
   a. Close connection immediately
   b. If local clock suspect: Adjust clock or use external time source
   c. If Bob's clock suspect: Temporary ban Bob
   d. Log for operator review
5. If |adjusted_skew| ≤ D:
   a. Continue handshake normally
   b. Optionally: Track skew for time synchronization
```
**Ajuste de RTT:** - Subtrair metade do RTT do desvio calculado - Leva em conta o atraso de propagação da rede - Estimativa de desvio mais precisa

### Processamento por Bob (Mensagem 3)

```
1. If message 3 received (unlikely if skew exceeded in message 1)
2. Recalculate skew = tsA_received - current_time
3. If |adjusted_skew| > D:
   a. Send termination block (reason code 7: clock skew)
   b. Close connection
   c. Ban Alice for period (e.g., 1-24 hours)
```
### Sincronização de Tempo

**Blocos DateTime (Fase de Dados):** - Enviar periodicamente o bloco DateTime (tipo 0) - O receptor pode usar para ajuste do relógio - Arredondar o carimbo de data/hora para o segundo mais próximo (evitar viés)

**Fontes Externas de Tempo:** - NTP (Protocolo de Tempo de Rede) - Sincronização do relógio do sistema - Tempo de consenso da rede I2P

**Estratégias de Ajuste do Relógio:** - Se o relógio local estiver incorreto: ajuste a hora do sistema ou use um offset (deslocamento) - Se os relógios dos peers (pares) estiverem consistentemente incorretos: sinalize o problema no peer - Acompanhe estatísticas de desvio para monitoramento da saúde da rede

## Propriedades de Segurança

### Sigilo Direto

**Obtido por meio de:** - Troca de chaves Diffie-Hellman efêmera (X25519) - Três operações DH: es, ee, se (padrão Noise XK) - Chaves efêmeras destruídas após a conclusão do handshake (negociação inicial)

**Progressão de Confidencialidade:** - Mensagem 1: Nível 2 (sigilo de encaminhamento em caso de comprometimento do remetente) - Mensagem 2: Nível 1 (destinatário efêmero) - Mensagem 3+: Nível 5 (sigilo de encaminhamento forte)

**Sigilo de Encaminhamento Perfeito:** - O comprometimento de chaves estáticas de longo prazo NÃO revela chaves de sessões passadas - Cada sessão usa chaves efêmeras exclusivas - As chaves privadas efêmeras nunca são reutilizadas - Limpeza de memória após o acordo de chaves

**Limitações:** - Mensagem 1 vulnerável se a chave estática de Bob for comprometida (mas há sigilo futuro (forward secrecy) em caso de comprometimento de Alice) - Ataques de repetição possíveis para a mensagem 1 (mitigados por carimbo de tempo e cache de repetição)

### Autenticação

**Autenticação Mútua:** - Alice autenticada por chave estática na mensagem 3 - Bob autenticado pela posse da chave privada estática (implícito a partir de handshake bem-sucedido)

**Resistência a Key Compromise Impersonation (KCI, impersonação por comprometimento de chave):** - Nível de autenticação 2 (resistente a KCI) - O atacante não pode se passar por Alice mesmo com a chave privada estática de Alice (sem a chave efêmera de Alice) - O atacante não pode se passar por Bob mesmo com a chave privada estática de Bob (sem a chave efêmera de Bob)

**Verificação de Chave Estática:** - Alice sabe a chave estática de Bob com antecedência (do RouterInfo (informações do router)) - Bob verifica se a chave estática de Alice corresponde ao RouterInfo na mensagem 3 - Evita ataques man-in-the-middle

### Resistência à Análise de Tráfego

**Contramedidas de DPI (Inspeção profunda de pacotes):** 1. **Ofuscação com AES:** Chaves efêmeras criptografadas; parece aleatório 2. **Ofuscação de comprimento com SipHash:** Comprimentos dos quadros não em claro 3. **Preenchimento aleatório:** Tamanhos de mensagem variáveis, sem padrões fixos 4. **Quadros criptografados:** Toda a carga útil criptografada com ChaCha20

**Prevenção contra ataques de repetição:** - Validação de carimbo de tempo (±60 segundos) - Cache de repetição de chaves efêmeras (tempo de vida 2*D) - Incrementos de nonce (número único de uso único) evitam a repetição de pacotes dentro da sessão

**Resistência a sondagens:** - Tempos limite aleatórios em falhas de AEAD - Leituras aleatórias de bytes antes do encerramento da conexão - Nenhuma resposta em falhas de handshake - Bloqueio de IP por falhas repetidas

**Diretrizes de preenchimento:** - Mensagens 1-2: preenchimento em texto claro (autenticado) - Mensagem 3+: preenchimento criptografado dentro de quadros AEAD - Parâmetros de preenchimento negociados (Options block – bloco de Opções) - Quadros somente de preenchimento permitidos

### Mitigação de Ataques de Negação de Serviço

**Limites de conexão:** - Máximo de conexões ativas (dependente da implementação) - Máximo de handshakes (negociação inicial) pendentes (por exemplo, 100-1000) - Limites de conexão por IP (por exemplo, 3-10 simultâneas)

**Proteção de Recursos:** - Operações DH com limitação de taxa (custosas) - Tempos limite de leitura por soquete e no total - Proteção contra "Slowloris" (limites de tempo totais) - Bloqueio de IP por abuso

**Rejeição rápida:** - Incompatibilidade de ID de rede → encerramento imediato - Ponto X25519 inválido → verificação rápida de MSB (bit mais significativo) antes da descriptografia - Carimbo de data e hora fora dos limites → encerrar sem processamento - Falha de AEAD (criptografia autenticada com dados associados) → sem resposta, atraso aleatório

**Resistência a sondagens:** - Tempo limite aleatório: 100-500ms (dependente da implementação) - Leitura aleatória: 1KB-64KB (dependente da implementação) - Nenhuma informação de erro para o atacante - Encerrar com TCP RST (sem handshake FIN)

### Segurança Criptográfica

**Algoritmos:** - **X25519**: segurança de 128 bits, DH de curva elíptica (Curve25519) - **ChaCha20**: cifra de fluxo com chave de 256 bits - **Poly1305**: MAC seguro do ponto de vista da teoria da informação - **SHA-256**: resistência a colisões de 128 bits, resistência à pré-imagem de 256 bits - **HMAC-SHA256**: função pseudorrandômica (PRF) para derivação de chaves

**Tamanhos de chave:** - Chaves estáticas: 32 bytes (256 bits) - Chaves efêmeras: 32 bytes (256 bits) - Chaves de cifra: 32 bytes (256 bits) - MAC: 16 bytes (128 bits)

**Problemas conhecidos:** - A reutilização de nonce (valor único não repetível) no ChaCha20 é catastrófica (evitada pelo incremento do contador) - X25519 tem problemas com subgrupos pequenos (mitigados pela validação da curva) - SHA-256 é teoricamente vulnerável à extensão de comprimento (não explorável em HMAC)

**Nenhuma vulnerabilidade conhecida (em outubro de 2025):** - Noise Protocol Framework amplamente analisado - ChaCha20-Poly1305 utilizado no TLS 1.3 - X25519 padrão em protocolos modernos - Sem ataques práticos à construção

## Referências

### Especificações Principais

- **[Especificação do NTCP2](/docs/specs/ntcp2/)** - Especificação oficial do I2P
- **[Proposta 111](/proposals/111-ntcp-2/)** - Documento de projeto original com fundamentação
- **[Noise Protocol Framework](https://noiseprotocol.org/noise.html)** - Revisão 33 (2017-10-04)

### Padrões criptográficos

- **[RFC 7748](https://www.rfc-editor.org/rfc/rfc7748)** - Curvas Elípticas para Segurança (X25519)
- **[RFC 7539](https://www.rfc-editor.org/rfc/rfc7539)** - ChaCha20 e Poly1305 para Protocolos da IETF
- **[RFC 8439](https://www.rfc-editor.org/rfc/rfc8439)** - ChaCha20-Poly1305 (torna o RFC 7539 obsoleto)
- **[RFC 2104](https://www.rfc-editor.org/rfc/rfc2104)** - HMAC: Hash com chave para autenticação de mensagens
- **[SipHash](https://www.131002.net/siphash/)** - SipHash-2-4 para aplicações de funções de hash

### Especificações relacionadas do I2P

- **[Especificação do I2NP](/docs/specs/i2np/)** - formato de mensagem do I2P Network Protocol (protocolo de rede do I2P)
- **[Estruturas Comuns](/docs/specs/common-structures/)** - formatos de RouterInfo e RouterAddress
- **[Transporte SSU](/docs/legacy/ssu/)** - transporte UDP (original, agora SSU2)
- **[Proposta 147](/proposals/147-transport-network-id-check/)** - Verificação do ID da rede de transporte (0.9.42)

### Referências de Implementação

- **[I2P Java](https://github.com/i2p/i2p.i2p)** - Implementação de referência (Java)
- **[i2pd](https://github.com/PurpleI2P/i2pd)** - Implementação em C++
- **[Notas de Lançamento do I2P](/blog/)** - Histórico de versões e atualizações

### Contexto histórico

- **[Station-To-Station Protocol (STS)](https://en.wikipedia.org/wiki/Station-to-Station_protocol)** - Inspiração para o Noise framework (estrutura para negociações de chaves criptográficas)
- **[obfs4](https://gitlab.com/yawning/obfs4)** - Transporte plugável (precedente de ofuscação do comprimento com SipHash)

## Diretrizes de Implementação

### Requisitos obrigatórios

**Para conformidade:**

1. **Implementar handshake completo:**
   - Suportar todas as três mensagens com cadeias KDF corretas
   - Validar todas as tags AEAD
   - Verificar se os pontos X25519 são válidos

2. **Implementar a Fase de Dados:**
   - Ofuscação do comprimento com SipHash (em ambas as direções)
   - Todos os tipos de bloco: 0 (DateTime), 1 (Options), 2 (RouterInfo), 3 (I2NP), 4 (Termination), 254 (Padding)
   - Gerenciamento adequado de nonce (número usado uma vez) (contadores separados)

3. **Recursos de segurança:**
   - Prevenção de replay (armazenar em cache chaves efêmeras por 2*D)
   - Validação de carimbo de tempo (±60 segundos por padrão)
   - Preenchimento aleatório nas mensagens 1-2
   - Tratamento de erros em AEAD (Authenticated Encryption with Associated Data — criptografia autenticada com dados associados) com tempos limite aleatórios

4. **Publicação do RouterInfo (metadados do router):**
   - Publicar chave estática ("s"), vetor de inicialização (IV) ("i") e versão ("v")
   - Rotacionar chaves conforme a política
   - Suportar o campo de capacidades ("caps") para routers ocultos

5. **Compatibilidade de rede:**
   - Suportar o campo de ID da rede (atualmente 2 para a rede principal)
   - Interoperar com as implementações existentes em Java e i2pd
   - Suportar IPv4 e IPv6

### Práticas Recomendadas

**Otimização de desempenho:**

1. **Estratégia de armazenamento em buffer:**
   - Descarregar mensagens inteiras de uma vez (mensagens 1, 2, 3)
   - Usar TCP_NODELAY para mensagens de handshake (negociação inicial)
   - Agrupar vários blocos de dados em um único quadro
   - Limitar o tamanho do quadro a poucos KB (minimizar a latência no receptor)

2. **Gerenciamento de conexões:**
   - Reutilize conexões quando possível
   - Implemente pool de conexões
   - Monitore a saúde da conexão (DateTime blocks, bloqueios de DateTime)

3. **Gerenciamento de memória:**
   - Zerar dados sensíveis após o uso (chaves efêmeras, resultados de DH (Diffie-Hellman))
   - Limitar handshakes simultâneos (prevenção de DoS)
   - Usar pools de memória para alocações frequentes

**Fortalecimento de segurança:**

1. **Resistência a sondagens:**
   - Tempos limite aleatórios: 100-500ms
   - Leituras aleatórias de bytes: 1KB-64KB
   - Bloqueio de IP por falhas repetidas
   - Sem detalhes de erro para os pares

2. **Limites de recursos:**
   - Máximo de conexões por IP: 3-10
   - Máximo de handshakes (negociações iniciais) pendentes: 100-1000
   - Tempo limite de leitura: 30-60 segundos por operação
   - Tempo limite total de conexão: 5 minutos para handshake

3. **Gerenciamento de chaves:**
   - Armazenamento persistente da chave estática e do vetor de inicialização (IV)
   - Geração aleatória segura (RNG criptográfico)
   - Cumprir rigorosamente as políticas de rotação
   - Nunca reutilizar chaves efêmeras

**Monitoramento e Diagnóstico:**

1. **Métricas:**
   - Taxas de sucesso/falha do handshake (negociação inicial)
   - Taxas de erro de AEAD
   - Distribuição do desvio de relógio
   - Estatísticas de duração da conexão

2. **Registro em log:**
   - Registrar falhas de handshake (negociação inicial) com códigos de motivo
   - Registrar eventos de desvio de relógio
   - Registrar IPs banidos
   - Nunca registrar material de chave sensível

3. **Testes:**
   - Testes de unidade para cadeias de KDF
   - Testes de integração com outras implementações
   - Fuzzing para tratamento de pacotes
   - Testes de carga para resistência a DoS

### Armadilhas comuns

**Erros críticos a evitar:**

1. **Reutilização de Nonce (número usado uma vez):**
   - Nunca redefina o contador de nonce no meio da sessão
   - Use contadores separados para cada direção
   - Encerre antes de atingir 2^64 - 1

2. **Rotação de chaves:**
   - Nunca rotacione chaves enquanto o router estiver em execução
   - Nunca reutilize chaves efêmeras entre sessões
   - Siga as regras de tempo mínimo de inatividade

3. **Manipulação de carimbos de data/hora:**
   - Nunca aceite carimbos de data/hora expirados
   - Sempre ajuste em função do RTT (tempo de ida e volta) ao calcular o desvio
   - Arredonde os carimbos de data/hora DateTime para segundos

4. **Erros de AEAD:**
   - Nunca revele o tipo de erro ao atacante
   - Sempre use um tempo limite aleatório antes de fechar
   - Trate um comprimento inválido da mesma forma que uma falha de AEAD

5. **Padding (preenchimento):**
   - Nunca enviar preenchimento fora dos limites negociados
   - Sempre colocar o bloco de preenchimento por último
   - Nunca múltiplos blocos de preenchimento por quadro

6. **RouterInfo:**
   - Sempre verifique se a chave estática corresponde ao RouterInfo
   - Nunca propague RouterInfos sem endereços publicados
   - Sempre valide as assinaturas

### Metodologia de Testes

**Testes unitários:**

1. **Primitivas criptográficas:**
   - Vetores de teste para X25519, ChaCha20, Poly1305, SHA-256
   - Vetores de teste de HMAC-SHA256
   - Vetores de teste de SipHash-2-4

2. **Cadeias KDF (função de derivação de chaves):**
   - Testes de resposta conhecida para todas as três mensagens
   - Verificar a propagação da chave de encadeamento
   - Testar a geração do IV (vetor de inicialização) do SipHash

3. **Análise de mensagens:**
   - Decodificação de mensagens válidas
   - Rejeição de mensagens inválidas
   - Condições de fronteira (vazio, tamanho máximo)

**Testes de Integração:**

1. **Aperto de mão:**
   - Troca de três mensagens bem-sucedida
   - Rejeição por desvio de relógio
   - Detecção de ataque de repetição
   - Rejeição de chave inválida

2. **Fase de Dados:**
   - Transferência de mensagens do I2NP
   - Troca de RouterInfo
   - Tratamento do preenchimento
   - Mensagens de encerramento

3. **Interoperabilidade:**
   - Testar com o Java I2P
   - Testar com o i2pd
   - Testar IPv4 e IPv6
   - Testar routers publicados e ocultos

**Testes de Segurança:**

1. **Testes Negativos:**
   - Tags AEAD inválidas
   - Mensagens repetidas
   - Ataques de desvio de relógio
   - Quadros malformados

2. **Testes de DoS:**
   - Inundação de conexões
   - Ataques Slowloris
   - Exaustão de CPU (DH excessivo)
   - Exaustão de memória

3. **Fuzzing (teste por mutação):**
   - Mensagens de handshake aleatórias
   - Quadros aleatórios da fase de dados
   - Tipos e tamanhos de blocos aleatórios
   - Valores criptográficos inválidos

### Migração do NTCP

**Para o suporte legado ao NTCP (um protocolo de transporte do I2P) (agora removido):**

NTCP (versão 1) foi removido na versão 0.9.50 do I2P (maio de 2021). Todas as implementações atuais devem oferecer suporte a NTCP2. Notas históricas:

1. **Período de Transição (2018-2021):**
   - 0.9.36: NTCP2 introduzido (desativado por padrão)
   - 0.9.37: NTCP2 ativado por padrão
   - 0.9.40: NTCP obsoleto
   - 0.9.50: NTCP removido

2. **Detecção de versão:**
   - "NTCP" transportStyle (estilo de transporte) indicava suporte a ambas as versões
   - "NTCP2" transportStyle indicava apenas NTCP2
   - Detecção automática via tamanho da mensagem (287 vs 288 bytes)

3. **Estado atual:**
   - Todos os routers devem suportar NTCP2
   - "NTCP" transportStyle está obsoleto
   - Use "NTCP2" transportStyle exclusivamente

## Apêndice A: Padrão Noise XK

**Padrão Noise XK Pattern (padrão de handshake do framework Noise):**

```
XK(s, rs):
  <- s
  ...
  -> e, es
  <- e, ee
  -> s, se
```
**Interpretação:**

- `<-` : Mensagem do respondente (Bob) para o iniciador (Alice)
- `->` : Mensagem do iniciador (Alice) para o respondente (Bob)
- `s` : Chave estática (chave de identidade de longo prazo)
- `rs` : Chave estática remota (chave estática do par, conhecida de antemão)
- `e` : Chave efêmera (específica da sessão, gerada sob demanda)
- `es` : DH Efêmero-Estático (efêmero de Alice × estático de Bob)
- `ee` : DH Efêmero-Efêmero (efêmero de Alice × efêmero de Bob)
- `se` : DH Estático-Efêmero (estático de Alice × efêmero de Bob)

**Sequência de Acordo de Chaves:**

1. **Pré-mensagem:** Alice conhece a chave pública estática de Bob (do RouterInfo, metadados do router)
2. **Mensagem 1:** Alice envia a chave efêmera, executa es DH
3. **Mensagem 2:** Bob envia a chave efêmera, executa ee DH
4. **Mensagem 3:** Alice revela a chave estática, executa se DH

**Propriedades de Segurança:**

- Alice autenticada: Sim (pela mensagem 3)
- Bob autenticado: Sim (por possuir a chave privada estática)
- Sigilo de encaminhamento: Sim (chaves efêmeras destruídas)
- KCI resistance (Key Compromise Impersonation - resistência a personificação após comprometimento de chave): Sim (nível de autenticação 2)

## Apêndice B: Codificação Base64

**Alfabeto Base64 do I2P:**

```
ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-~
```
**Diferenças em relação ao Base64 padrão:** - Caracteres 62-63: `-~` em vez de `+/` - Preenchimento: Igual (`=`) ou omitido dependendo do contexto

**Uso no NTCP2:** - Chave estática ("s"): 32 bytes → 44 caracteres (sem preenchimento) - IV ("i"): 16 bytes → 24 caracteres (sem preenchimento)

**Exemplo de codificação:**

```python
# 32-byte static key (hex): 
# f4489e1bb0597b39ca6cbf5ad9f5f1f09043e02d96cb9aa6a63742b3462429aa

# I2P Base64 encoded:
# 9EjeG7BZeznKbL9a2fXx8JBDPgLZbLmKbqY3QrNGJCo=
```
## Apêndice C: Análise de Captura de Pacotes

**Identificando o tráfego NTCP2:**

1. **Handshake TCP:**
   - SYN, SYN-ACK, ACK padrão do TCP
   - Porta de destino normalmente 8887 ou similar

2. **Mensagem 1 (SessionRequest - pedido de sessão):**
   - Primeiros dados da aplicação enviados por Alice
   - 80-65535 bytes (tipicamente algumas centenas)
   - Parece aleatório (chave efêmera criptografada com AES)
   - 287 bytes no máximo ao conectar-se a um endereço "NTCP"

3. **Mensagem 2 (SessionCreated):**
   - Resposta de Bob
   - 80-65535 bytes (tipicamente algumas centenas)
   - Também parece aleatório

4. **Mensagem 3 (SessionConfirmed — confirmação da sessão):**
   - De Alice
   - 48 bytes + variável (tamanho do RouterInfo (informações do router) + preenchimento)
   - Normalmente 1-4 KB

5. **Fase de Dados:**
   - Quadros de tamanho variável
   - Campo de comprimento ofuscado (parece aleatório)
   - Carga útil criptografada
   - Preenchimento torna o tamanho imprevisível

**Evasão de DPI (inspeção profunda de pacotes):** - Sem cabeçalhos em texto claro - Sem padrões fixos - Campos de comprimento ofuscados - Preenchimento aleatório quebra heurísticas baseadas em tamanho

**Comparação com NTCP:** - Mensagem 1 do NTCP tem sempre 288 bytes (identificável) - Mensagem 1 do NTCP2 tem tamanho variável (não identificável) - NTCP tinha padrões reconhecíveis - NTCP2 projetado para resistir à inspeção profunda de pacotes (DPI)

## Apêndice D: Histórico de versões

**Principais marcos:**

- **0.9.36** (23 de agosto de 2018): NTCP2 introduzido, desativado por padrão
- **0.9.37** (4 de outubro de 2018): NTCP2 ativado por padrão
- **0.9.40** (20 de maio de 2019): NTCP tornado obsoleto
- **0.9.42** (27 de agosto de 2019): campo Network ID adicionado (Proposta 147)
- **0.9.50** (17 de maio de 2021): NTCP removido, suporte a capacidades adicionado
- **2.10.0** (9 de setembro de 2025): Versão estável mais recente

**Estabilidade do Protocolo:** - Sem alterações incompatíveis desde 0.9.50 - Melhorias contínuas na resistência a sondagens - Foco em desempenho e confiabilidade - Criptografia pós-quântica em desenvolvimento (não ativada por padrão)

**Estado atual dos transportes:** - NTCP2: Transporte TCP obrigatório - SSU2: Transporte UDP obrigatório - NTCP (v1): Removido - SSU (v1): Removido
