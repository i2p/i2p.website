---
title: "Especificação de Criptografia do ECIES-X25519-AEAD-Ratchet"
description: "Esquema de Criptografia Integrada de Curvas Elípticas para o I2P (X25519 + AEAD (Criptografia Autenticada com Dados Associados))"
slug: "ecies"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
toc: true
---

## Visão geral

### Objetivo

ECIES-X25519-AEAD-Ratchet é o protocolo moderno de criptografia de ponta a ponta do I2P, substituindo o sistema legado ElGamal/AES+SessionTags. Ele fornece sigilo de encaminhamento (forward secrecy), criptografia autenticada e melhorias significativas em desempenho e segurança.

### Principais melhorias em relação a ElGamal/AES+SessionTags (etiquetas de sessão)

- **Chaves menores**: chaves de 32 bytes vs chaves públicas ElGamal de 256 bytes (redução de 87,5%)
- **Sigilo Direto**: alcançado por meio de DH ratcheting (mecanismo de "ratchet" Diffie-Hellman) (não disponível no protocolo legado)
- **Criptografia moderna**: X25519 DH, ChaCha20-Poly1305 AEAD, SHA-256
- **Criptografia autenticada**: autenticação integrada via construção AEAD
- **Protocolo bidirecional**: sessões de entrada/saída emparelhadas vs protocolo legado unidirecional
- **Tags eficientes**: tags de sessão de 8 bytes vs tags de 32 bytes (redução de 75%)
- **Ofuscação de tráfego**: a codificação Elligator2 torna os handshakes indistinguíveis de dados aleatórios

### Status de Implantação

- **Lançamento inicial**: Versão 0.9.46 (25 de maio de 2020)
- **Implantação na rede**: Concluída em 2020
- **Status atual**: Maduro, amplamente implantado (5+ anos em produção)
- **Suporte do router**: Requer a versão 0.9.46 ou superior
- **Requisitos de floodfill** (nós especializados que armazenam e propagam dados no netDb): Adoção próxima de 100% para consultas criptografadas

### Estado da Implementação

**Totalmente implementado:** - Mensagens New Session (NS) com associação - Mensagens New Session Reply (NSR) - Mensagens Existing Session (ES) - Mecanismo DH ratchet (mecanismo de catraca Diffie-Hellman) - Ratchets de Session tag e de chave simétrica - Blocos DateTime, NextKey, ACK, ACK Request, Garlic Clove (elemento de garlic encryption), e Padding

**Não implementado (até a versão 0.9.50):** - MessageNumbers block (bloco MessageNumbers) (tipo 6) - Options block (bloco Options) (tipo 5) - Termination block (bloco Termination) (tipo 4) - respostas automáticas na camada de protocolo - modo de chave estática zero - sessões multicast

**Observação**: O status de implementação para as versões 1.5.0 até 2.10.0 (2021-2025) requer verificação, pois alguns recursos podem ter sido adicionados.

---

## Fundamentos do Protocolo

### Noise Protocol Framework (estrutura de protocolos criptográficos Noise)

ECIES-X25519-AEAD-Ratchet é baseado no [Noise Protocol Framework](https://noiseprotocol.org/) (Revisão 34, 2018-07-11), especificamente no padrão de handshake **IK** (Interativo, chave estática remota conhecida) com extensões específicas do I2P.

### Identificador do Protocolo Noise

```
Noise_IKelg2+hs2_25519_ChaChaPoly_SHA256
```
**Componentes do identificador:** - `Noise` - Framework base - `IK` - Padrão de handshake (aperto de mão) interativo com chave estática remota conhecida - `elg2` - Codificação Elligator2 para chaves efêmeras (extensão do I2P) - `+hs2` - MixHash chamado antes da segunda mensagem para incorporar a tag (extensão do I2P) - `25519` - Função Diffie-Hellman X25519 - `ChaChaPoly` - Cifra AEAD ChaCha20-Poly1305 - `SHA256` - Função de hash SHA-256

### Padrão de Handshake do Noise

**Notação do padrão IK:**

```
<- s                    (Bob's static key known to Alice)
...
-> e, es, s, ss         (Alice sends ephemeral, DH es, static key, DH ss)
<- e, ee, se            (Bob sends ephemeral, DH ee, DH se)
```
**Significados dos tokens:** - `e` - Transmissão de chave efêmera - `s` - Transmissão de chave estática - `es` - DH entre a chave efêmera de Alice e a chave estática de Bob - `ss` - DH entre a chave estática de Alice e a chave estática de Bob - `ee` - DH entre a chave efêmera de Alice e a chave efêmera de Bob - `se` - DH entre a chave estática de Bob e a chave efêmera de Alice

### Propriedades de Segurança do Noise

Usando a terminologia do Noise, o padrão IK fornece:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Message</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Authentication Level</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Confidentiality Level</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Message&nbsp;1 (NS)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Level&nbsp;1 (sender auth, KCI vulnerable)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Level&nbsp;2 (weak forward secrecy)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Message&nbsp;2 (NSR)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Level&nbsp;2 (mutual auth)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Level&nbsp;4 (weak forward secrecy)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Transport (ES)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Level&nbsp;2 (mutual auth)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Level&nbsp;5 (strong forward secrecy)</td>
    </tr>
  </tbody>
</table>
**Níveis de autenticação:** - **Nível 1**: A carga útil é autenticada como pertencente ao proprietário da chave estática do remetente, mas é vulnerável a Key Compromise Impersonation (KCI, impersonação por comprometimento de chave) - **Nível 2**: Resistente a ataques de KCI após NSR

**Níveis de confidencialidade:** - **Nível 2**: Forward secrecy (sigilo futuro) se a chave estática do remetente for posteriormente comprometida - **Nível 4**: Forward secrecy se a chave efêmera do remetente for posteriormente comprometida - **Nível 5**: Forward secrecy total após a exclusão de ambas as chaves efêmeras

### Diferenças entre IK e XK

O padrão IK difere do padrão XK usado no NTCP2 e no SSU2:

1. **Quatro operações DH**: IK usa 4 operações DH (es, ss, ee, se) vs 3 para XK
2. **Autenticação imediata**: Alice é autenticada na primeira mensagem (Nível de autenticação 1)
3. **Sigilo futuro mais rápido**: Sigilo futuro completo (Nível 5) atingido após a segunda mensagem (1-RTT)
4. **Compromisso**: A carga útil da primeira mensagem não possui sigilo futuro (vs XK onde todas as cargas úteis possuem sigilo futuro)

**Resumo**: IK permite a entrega em 1-RTT da resposta de Bob com forward secrecy (sigilo futuro) total, ao custo de a requisição inicial não possuir forward secrecy.

### Conceitos do Signal Double Ratchet (algoritmo de catraca dupla)

ECIES (Esquema Integrado de Criptografia com Curvas Elípticas) incorpora conceitos do [Signal Double Ratchet Algorithm](https://signal.org/docs/specifications/doubleratchet/):

- **DH Ratchet**: (ratchet: mecanismo de atualização irreversível) Fornece sigilo futuro ao trocar periodicamente novas chaves DH
- **Symmetric Key Ratchet**: Deriva novas chaves de sessão para cada mensagem
- **Session Tag Ratchet**: Gera tags de sessão de uso único de forma determinística

**Principais diferenças em relação ao Signal:** - **Ratcheting (mecanismo de avanço do estado criptográfico) menos frequente**: O I2P aplica o ratcheting apenas quando necessário (perto da exaustão de tags (identificadores de sessão) ou por política) - **Tags de sessão em vez de criptografia do cabeçalho**: Usa tags determinísticas em vez de cabeçalhos criptografados - **ACKs (confirmações de recebimento) explícitos**: Usa blocos de ACK em banda em vez de depender apenas do tráfego de retorno - **Ratcheting de tag e de chave separados**: Mais eficiente para o receptor (pode adiar o cálculo da chave)

### Extensões do I2P para o Noise (estrutura de protocolos criptográficos)

1. **Codificação Elligator2**: Chaves efêmeras codificadas para serem indistinguíveis de dados aleatórios
2. **Tag anteposta ao NSR**: Tag de sessão adicionada antes da mensagem NSR para correlação
3. **Formato de payload definido**: Estrutura de payload baseada em blocos para todos os tipos de mensagem
4. **Encapsulamento I2NP**: Todas as mensagens encapsuladas em cabeçalhos I2NP Garlic Message (tipo de mensagem "garlic" do I2P)
5. **Fase de dados separada**: Mensagens de transporte (ES) divergem da fase de dados padrão do Noise

---

## Primitivas Criptográficas

### Diffie-Hellman X25519

**Especificação**: [RFC 7748](https://tools.ietf.org/html/rfc7748)

**Propriedades da chave:** - **Tamanho da chave privada**: 32 bytes - **Tamanho da chave pública**: 32 bytes - **Tamanho do segredo compartilhado**: 32 bytes - **Endianidade**: Little-endian - **Curva**: Curve25519

**Operações:**

### X25519 GENERATE_PRIVATE()

Gera uma chave privada aleatória de 32 bytes:

```
privkey = CSRNG(32)
```
### X25519 DERIVE_PUBLIC(privkey)

Deriva a chave pública correspondente:

```
pubkey = curve25519_scalarmult_base(privkey)
```
Retorna uma chave pública de 32 bytes em little-endian (ordem de bytes do menos significativo para o mais significativo).

### X25519 DH(privkey, pubkey)

Realiza o acordo de chaves Diffie-Hellman:

```
sharedSecret = curve25519_scalarmult(privkey, pubkey)
```
Retorna um segredo compartilhado de 32 bytes.

**Nota de segurança**: Implementadores devem validar que o segredo compartilhado não seja composto apenas por zeros (chave fraca). Rejeite e aborte o handshake (negociação inicial) se isso ocorrer.

### ChaCha20-Poly1305 AEAD (Criptografia Autenticada com Dados Associados)

**Especificação**: [RFC 7539](https://tools.ietf.org/html/rfc7539) seção 2.8

**Parâmetros:** - **Tamanho da Chave**: 32 bytes (256 bits) - **Tamanho do Nonce**: 12 bytes (96 bits) - **Tamanho do MAC**: 16 bytes (128 bits) - **Tamanho do Bloco**: 64 bytes (interno)

**Formato de Nonce (número usado uma vez):**

```
Byte 0-3:   0x00 0x00 0x00 0x00  (always zero)
Byte 4-11:  Little-endian counter (message number N)
```
**Construção de AEAD (Cifra Autenticada com Dados Associados):**

O AEAD (criptografia autenticada com dados associados) combina a cifra de fluxo ChaCha20 com o MAC Poly1305:

1. Gerar o fluxo de chave ChaCha20 a partir da chave e do nonce (número usado uma vez)
2. Cifrar o texto plano via XOR com o fluxo de chave
3. Calcular o MAC Poly1305 sobre (dados associados || texto cifrado)
4. Anexar o MAC de 16 bytes ao texto cifrado

### ChaCha20-Poly1305 ENCRYPT(k, n, plaintext, ad)

Criptografa o texto em claro com autenticação:

```python
# Inputs
k = 32-byte cipher key
n = 12-byte nonce (first 4 bytes zero, last 8 bytes = message number)
plaintext = data to encrypt (0 to 65519 bytes)
ad = associated data (optional, used in MAC calculation)

# Output
ciphertext = chacha20_encrypt(k, n, plaintext)
mac = poly1305(ad || ciphertext, poly1305_key_gen(k, n))
return ciphertext || mac  # Total length = len(plaintext) + 16
```
**Propriedades:** - O texto cifrado tem o mesmo tamanho que o texto em claro (cifra de fluxo) - A saída é plaintext_length + 16 bytes (inclui MAC) - Toda a saída é indistinguível de dados aleatórios se a chave for secreta - O MAC autentica tanto os dados associados quanto o texto cifrado

### ChaCha20-Poly1305 DECRYPT(k, n, ciphertext, ad)

Descriptografa e verifica a autenticação:

```python
# Split ciphertext and MAC
ct_without_mac = ciphertext[0:-16]
received_mac = ciphertext[-16:]

# Verify MAC
expected_mac = poly1305(ad || ct_without_mac, poly1305_key_gen(k, n))
if not constant_time_compare(received_mac, expected_mac):
    raise AuthenticationError("MAC verification failed")

# Decrypt
plaintext = chacha20_decrypt(k, n, ct_without_mac)
return plaintext
```
**Requisitos Críticos de Segurança:** - Nonces (números de uso único) DEVEM ser únicos para cada mensagem com a mesma chave - Nonces NÃO DEVEM ser reutilizados (falha catastrófica se reutilizados) - A verificação do MAC DEVE usar comparação em tempo constante para impedir ataques de temporização - Falha na verificação do MAC DEVE resultar na rejeição completa da mensagem (sem descriptografia parcial)

### Função de hash SHA-256

**Especificação**: NIST FIPS 180-4

**Propriedades:** - **Tamanho de saída**: 32 bytes (256 bits) - **Tamanho do bloco**: 64 bytes (512 bits) - **Nível de segurança**: 128 bits (resistência a colisões)

**Operações:**

### SHA-256 H(p, d)

Hash SHA-256 com string de personalização:

```
H(p, d) := SHA256(p || d)
```
Onde `||` denota concatenação, `p` é a string de personalização e `d` representa os dados.

### SHA-256 MixHash(d)

Atualiza o hash incremental com novos dados:

```
h = SHA256(h || d)
```
Usado ao longo do handshake do Noise para manter o hash da transcrição.

### Derivação de Chaves com HKDF (função de derivação de chaves baseada em hash)

**Especificação**: [RFC 5869](https://tools.ietf.org/html/rfc5869)

**Descrição**: Função de derivação de chaves baseada em HMAC usando SHA-256

**Parâmetros:** - **Função de hash**: HMAC-SHA256 - **Comprimento do salt**: Até 32 bytes (tamanho da saída do SHA-256) - **Comprimento da saída**: Variável (até 255 * 32 bytes)

**Função HKDF (função de derivação de chaves baseada em HMAC):**

```python
def HKDF(salt, ikm, info, length):
    """
    Args:
        salt: Salt value (32 bytes max for SHA-256)
        ikm: Input key material (any length)
        info: Context-specific info string
        length: Desired output length in bytes
    
    Returns:
        output: Derived key material (length bytes)
    """
    # Extract phase
    prk = HMAC-SHA256(salt, ikm)
    
    # Expand phase
    n = ceil(length / 32)
    t = b''
    okm = b''
    for i in range(1, n + 1):
        t = HMAC-SHA256(prk, t || info || byte(i))
        okm = okm || t
    
    return okm[0:length]
```
**Padrões comuns de uso:**

```python
# Generate two keys (64 bytes total)
keydata = HKDF(chainKey, sharedSecret, "KDFDHRatchetStep", 64)
nextRootKey = keydata[0:31]
chainKey = keydata[32:63]

# Generate session tag (8 bytes)
tagdata = HKDF(chainKey, CONSTANT, "SessionTagKeyGen", 64)
nextChainKey = tagdata[0:31]
sessionTag = tagdata[32:39]

# Generate symmetric key (32 bytes)
keydata = HKDF(chainKey, ZEROLEN, "SymmetricRatchet", 64)
nextChainKey = keydata[0:31]
sessionKey = keydata[32:63]
```
**Strings de informação usadas no ECIES:** - `"KDFDHRatchetStep"` - derivação de chave do ratchet (mecanismo de avanço criptográfico) DH - `"TagAndKeyGenKeys"` - inicializar as chaves de tag e da cadeia de chaves - `"STInitialization"` - inicialização do ratchet de tags de sessão - `"SessionTagKeyGen"` - geração de tags de sessão - `"SymmetricRatchet"` - geração de chave simétrica - `"XDHRatchetTagSet"` - chave do conjunto de tags do ratchet DH - `"SessionReplyTags"` - geração do conjunto de tags NSR - `"AttachPayloadKDF"` - derivação da chave da carga útil do NSR

### Codificação Elligator2 (método de mapeamento de curvas elípticas que torna pontos indistinguíveis de dados aleatórios)

**Objetivo**: Codificar chaves públicas X25519 de modo que sejam indistinguíveis de cadeias aleatórias uniformes de 32 bytes.

**Especificação**: [Artigo Elligator2](https://elligator.cr.yp.to/elligator-20130828.pdf)

**Problema**: As chaves públicas X25519 padrão têm uma estrutura reconhecível. Um observador pode identificar mensagens de handshake (negociação inicial) ao detectar essas chaves, mesmo que o conteúdo esteja criptografado.

**Solução**: Elligator2 fornece um mapeamento bijetivo entre ~50% das chaves públicas X25519 válidas e sequências de 254 bits com aparência aleatória.

**Geração de chaves com Elligator2:**

### Elligator2 GENERATE_PRIVATE_ELG2()

Gera uma chave privada que corresponde a uma chave pública codificável pelo Elligator2:

```python
while True:
    privkey = CSRNG(32)
    pubkey = DERIVE_PUBLIC(privkey)
    
    # Test if public key is Elligator2-encodable
    try:
        encoded = ENCODE_ELG2(pubkey)
        # Success - this key pair is suitable
        return privkey
    except NotEncodableError:
        # Try again with new random key
        continue
```
**Importante**: Aproximadamente 50% das chaves privadas geradas aleatoriamente produzirão chaves públicas não codificáveis. Essas devem ser descartadas e deve-se tentar a regeneração.

**Otimização de Desempenho**: Gere chaves antecipadamente em uma thread de segundo plano para manter um pool de pares de chaves adequados, evitando atrasos durante o handshake (negociação inicial).

### Elligator2 ENCODE_ELG2(pubkey)

Codifica uma chave pública em 32 bytes com aparência aleatória:

```python
def ENCODE_ELG2(pubkey):
    """
    Encodes X25519 public key using Elligator2.
    
    Args:
        pubkey: 32-byte X25519 public key (little-endian)
    
    Returns:
        encoded: 32-byte encoded key indistinguishable from random
    
    Raises:
        NotEncodableError: If pubkey cannot be encoded
    """
    # Perform Elligator2 representative calculation
    # Returns 254-bit value (31.75 bytes)
    encodedKey = elligator2_encode(pubkey)
    
    # Add 2 random bits to MSB to make full 32 bytes
    randomByte = CSRNG(1)
    encodedKey[31] |= (randomByte & 0xc0)
    
    return encodedKey
```
**Detalhes de codificação:** - Elligator2 (método para mapear pontos de curvas elípticas para bytes indistinguíveis de aleatórios) produz 254 bits (não os 256 completos) - Os 2 bits superiores do byte 31 são preenchimento aleatório - O resultado é distribuído uniformemente no espaço de 32 bytes - Codifica com sucesso aproximadamente 50% das chaves públicas X25519 (algoritmo de acordo de chaves baseado em curva elíptica) válidas

### Elligator2 DECODE_ELG2(encodedKey)

Decodifica de volta para a chave pública original:

```python
def DECODE_ELG2(encodedKey):
    """
    Decodes Elligator2-encoded key back to X25519 public key.
    
    Args:
        encodedKey: 32-byte encoded key
    
    Returns:
        pubkey: 32-byte X25519 public key (little-endian)
    """
    # Mask out 2 random padding bits from MSB
    encodedKey[31] &= 0x3f
    
    # Perform Elligator2 representative inversion
    pubkey = elligator2_decode(encodedKey)
    
    return pubkey
```
**Propriedades de Segurança:** - Chaves codificadas são indistinguíveis computacionalmente de bytes aleatórios - Nenhum teste estatístico pode detectar de forma confiável chaves codificadas com Elligator2 - A decodificação é determinística (a mesma chave codificada sempre produz a mesma chave pública) - A codificação é bijetiva para ~50% das chaves no subconjunto codificável

**Notas de implementação:** - Armazene as chaves codificadas na fase de geração para evitar recodificação durante o handshake - Chaves inadequadas da geração pelo Elligator2 (método que torna chaves públicas indistinguíveis de dados aleatórios) podem ser usadas para NTCP2 (que não requer Elligator2) - A geração de chaves em segundo plano é essencial para o desempenho - O tempo médio de geração dobra devido à taxa de rejeição de 50%

---

## Formatos de Mensagem

### Visão geral

ECIES define três tipos de mensagem:

1. **Nova Sessão (NS)**: Mensagem inicial de handshake (negociação inicial) de Alice para Bob
2. **Resposta de Nova Sessão (NSR)**: Resposta de handshake de Bob para Alice
3. **Sessão Existente (ES)**: Todas as mensagens subsequentes em ambas as direções

Todas as mensagens são encapsuladas no formato I2NP Garlic Message (formato de mensagem "garlic" do I2NP) com camadas adicionais de criptografia.

### Contêiner de Mensagem Garlic do I2NP

Todas as mensagens ECIES são encapsuladas em cabeçalhos padrão de I2NP Garlic Message (mensagem "garlic"):

```
+----+----+----+----+----+----+----+----+
|type|      msg_id       |  expiration   |
+----+----+----+----+----+----+----+----+
                         |  size   |chks|
+----+----+----+----+----+----+----+----+
|      length       |                   |
+----+----+----+----+                   +
|          encrypted data               |
~                                       ~
```
**Campos:** - `type`: 0x26 (Garlic Message, tipo de mensagem do I2NP) - `msg_id`: ID de mensagem do I2NP de 4 bytes - `expiration`: carimbo de tempo Unix de 8 bytes (milissegundos) - `size`: tamanho da carga útil de 2 bytes - `chks`: soma de verificação de 1 byte - `length`: comprimento dos dados criptografados de 4 bytes - `encrypted data`: carga útil criptografada com ECIES

**Finalidade**: Fornece identificação e roteamento de mensagens na camada I2NP. O campo `length` permite que os receptores saibam o tamanho total da carga útil criptografada.

### Mensagem de Nova Sessão (NS)

A mensagem de Nova Sessão inicia uma nova sessão de Alice para Bob. Ela tem três variantes:

1. **Com Vinculação** (1b): Inclui a chave estática de Alice para comunicação bidirecional
2. **Sem Vinculação** (1c): Omite a chave estática para comunicação unidirecional
3. **De Uso Único** (1d): Modo de mensagem única sem estabelecimento de sessão

### Mensagem NS com Vinculação (Tipo 1b)

**Caso de uso**: streaming, datagramas com suporte a resposta, qualquer protocolo que exija respostas

**Comprimento total**: 96 + payload_length bytes

**Formato**:

```
+----+----+----+----+----+----+----+----+
|                                       |
+                                       +
|   New Session Ephemeral Public Key    |
+             32 bytes                  +
|     Encoded with Elligator2           |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|                                       |
+         Static Key Section            +
|       ChaCha20 encrypted data         |
+            32 bytes                   +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|  Poly1305 Message Authentication Code |
+    (MAC) for Static Key Section       +
|             16 bytes                  |
+----+----+----+----+----+----+----+----+
|                                       |
+            Payload Section            +
|       ChaCha20 encrypted data         |
~          Variable length              ~
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|  Poly1305 Message Authentication Code |
+         (MAC) for Payload Section     +
|             16 bytes                  |
+----+----+----+----+----+----+----+----+
```
**Detalhes do Campo:**

**Chave Pública Efêmera** (32 bytes, texto claro): - Chave pública X25519 de uso único de Alice - Codificada com Elligator2 (indistinguível de dados aleatórios) - Gerada novamente para cada mensagem NS (nunca reutilizada) - Formato little-endian

**Seção de Chave Estática** (32 bytes criptografados, 48 bytes com MAC): - Contém a chave pública estática X25519 de Alice (32 bytes) - Criptografada com ChaCha20 - Autenticada com MAC Poly1305 (16 bytes) - Usada por Bob para vincular a sessão ao destino de Alice

**Seção de carga útil** (criptografada de comprimento variável, +16 bytes MAC): - Contém garlic cloves (submensagens do esquema garlic) e outros blocos - Deve incluir o bloco DateTime como primeiro bloco - Geralmente inclui blocos Garlic Clove com dados da aplicação - Pode incluir o bloco NextKey para ratchet imediato (mecanismo de avanço criptográfico) - Criptografada com ChaCha20 - Autenticada com MAC Poly1305 (16 bytes)

**Propriedades de Segurança:** - Chave efêmera fornece componente de sigilo direto - Chave estática autentica Alice (vinculação ao destino) - Ambas as seções têm MACs separados para separação de domínios - O handshake total realiza 2 operações de DH (es, ss)

### Mensagem NS sem Vinculação (Tipo 1c)

**Caso de uso**: Datagramas brutos em que não se espera nem se deseja resposta

**Comprimento total**: 96 + payload_length bytes

**Formato**:

```
+----+----+----+----+----+----+----+----+
|                                       |
+                                       +
|   New Session Ephemeral Public Key    |
+             32 bytes                  +
|     Encoded with Elligator2           |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|                                       |
+           Flags Section               +
|       ChaCha20 encrypted data         |
+            32 bytes                   +
|           All zeros                   |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|  Poly1305 Message Authentication Code |
+         (MAC) for above section       +
|             16 bytes                  |
+----+----+----+----+----+----+----+----+
|                                       |
+            Payload Section            +
|       ChaCha20 encrypted data         |
~          Variable length              ~
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|  Poly1305 Message Authentication Code |
+         (MAC) for Payload Section     +
|             16 bytes                  |
+----+----+----+----+----+----+----+----+
```
**Diferença principal**: A seção Flags contém 32 bytes de zero em vez de uma chave estática.

**Detecção**: Bob determina o tipo de mensagem descriptografando a seção de 32 bytes e verificando se todos os bytes estão em zero: - Todos em zero → Sessão não vinculada (tipo 1c) - Diferente de zero → Sessão vinculada com chave estática (tipo 1b)

**Propriedades:** - Sem chave estática, não há associação ao destino de Alice - Bob não pode enviar respostas (nenhum destino conhecido) - Executa apenas 1 operação de DH (es) - Segue o padrão "N" do Noise em vez de "IK" - Mais eficiente quando respostas nunca são necessárias

**Seção de Flags** (reservado para uso futuro): Atualmente, todos são zeros. Pode ser usada para negociação de funcionalidades em versões futuras.

### Mensagem NS de uso único (Tipo 1d)

**Caso de uso**: Mensagem anônima única sem sessão ou resposta esperada

**Comprimento total**: 96 + payload_length bytes

**Formato**: Idêntico a NS sem vinculação (tipo 1c)

**Distinção**:  - O Tipo 1c pode enviar várias mensagens na mesma sessão (ES messages (mensagens ES) subsequentes) - O Tipo 1d envia exatamente uma mensagem sem estabelecimento de sessão - Na prática, as implementações podem tratar ambos de forma idêntica inicialmente

**Propriedades:** - Anonimato máximo (sem chave estática, sem sessão) - Nenhuma das partes mantém estado de sessão - Segue o padrão "N" do Noise - Uma única operação DH

### Mensagem de Resposta de Nova Sessão (NSR)

Bob envia uma ou mais mensagens NSR em resposta à mensagem NS de Alice. O NSR conclui o aperto de mão Noise IK e estabelece uma sessão bidirecional.

**Comprimento total**: 72 + payload_length bytes

**Formato**:

```
+----+----+----+----+----+----+----+----+
|       Session Tag   8 bytes           |
+----+----+----+----+----+----+----+----+
|                                       |
+        Ephemeral Public Key           +
|                                       |
+            32 bytes                   +
|     Encoded with Elligator2           |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|  Poly1305 Message Authentication Code |
+  (MAC) for Key Section (empty)        +
|             16 bytes                  |
+----+----+----+----+----+----+----+----+
|                                       |
+            Payload Section            +
|       ChaCha20 encrypted data         |
~          Variable length              ~
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|  Poly1305 Message Authentication Code |
+         (MAC) for Payload Section     +
|             16 bytes                  |
+----+----+----+----+----+----+----+----+
```
**Detalhes do campo:**

**Tag de Sessão** (8 bytes, em claro): - Gerado a partir do conjunto de tags NSR (consulte as seções de KDF) - Correlaciona esta resposta com a mensagem NS de Alice - Permite que Alice identifique a qual NS este NSR responde - Uso único (nunca reutilizado)

**Chave Pública Efêmera** (32 bytes, em claro): - Chave pública X25519 de uso único de Bob - Codificada com Elligator2 (técnica de codificação para curvas elípticas) - Gerada novamente para cada mensagem NSR - Deve ser diferente para cada NSR enviada

**Key Section MAC** (MAC da seção de chave) (16 bytes): - Autentica dados vazios (ZEROLEN) - Parte do protocolo Noise IK (padrão se) - Usa o hash da transcrição como dados associados - Crítico para vincular NSR a NS

**Seção de Carga Útil** (comprimento variável): - Contém garlic cloves (submensagens "garlic") e blocos - Geralmente inclui respostas na camada de aplicação - Pode estar vazia (ACK-only NSR) - Tamanho máximo: 65519 bytes (65535 - MAC de 16 bytes)

**Múltiplas mensagens NSR:**

Bob pode enviar várias mensagens NSR em resposta a uma NS: - Cada NSR tem uma chave efêmera exclusiva - Cada NSR tem uma tag de sessão exclusiva - Alice usa a primeira NSR recebida para concluir o handshake (negociação inicial) - As outras NSR servem como redundância (em caso de perda de pacotes)

**Temporização Crítica:** - Alice deve receber um NSR antes de enviar mensagens ES - Bob deve receber uma mensagem ES antes de enviar mensagens ES - NSR estabelece chaves de sessão bidirecionais por meio da operação split()

**Propriedades de Segurança:** - Conclui o Noise IK handshake (handshake do protocolo Noise no padrão IK) - Realiza 2 operações DH adicionais (ee, se) - Total de 4 operações DH em NS+NSR - Alcança autenticação mútua (Nível 2) - Fornece sigilo futuro fraco (Nível 4) para a carga útil do NSR

### Mensagem de Sessão Existente (ES)

Todas as mensagens após o handshake NS/NSR usam o formato de Sessão Existente. As mensagens ES são usadas bidirecionalmente por Alice e Bob.

**Comprimento total**: 8 + payload_length + 16 bytes (mínimo 24 bytes)

**Formato**:

```
+----+----+----+----+----+----+----+----+
|       Session Tag   8 bytes           |
+----+----+----+----+----+----+----+----+
|                                       |
+            Payload Section            +
|       ChaCha20 encrypted data         |
~          Variable length              ~
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|  Poly1305 Message Authentication Code |
+              (MAC)                    +
|             16 bytes                  |
+----+----+----+----+----+----+----+----+
```
**Detalhes do campo:**

**Tag de sessão** (8 bytes, em claro): - Gerada a partir do conjunto de tags de saída atual - Identifica a sessão e o número da mensagem - O receptor consulta a tag para encontrar a chave de sessão e o nonce (valor de uso único) - Uso único (cada tag é usada exatamente uma vez) - Formato: primeiros 8 bytes da saída do HKDF

**Seção de carga útil** (comprimento variável): - Contém garlic cloves (submensagens do I2P) e blocos - Sem blocos obrigatórios (pode estar vazio) - Blocos comuns: Garlic Clove, NextKey, ACK, ACK Request, Padding - Tamanho máximo: 65519 bytes (65535 - MAC de 16 bytes)

**MAC** (16 bytes): - Tag de autenticação Poly1305 - Calculada sobre toda a carga útil - Dados associados: a tag de sessão de 8 bytes - Deve ser verificada corretamente ou a mensagem é rejeitada

**Processo de Consulta de Tags:**

1. O receptor extrai a tag de 8 bytes
2. Procura a tag em todos os conjuntos de tags de entrada atuais
3. Recupera a chave de sessão associada e o número da mensagem N
4. Constrói o nonce (número único): `[0x00, 0x00, 0x00, 0x00, N (8 bytes little-endian)]`
5. Descriptografa a carga útil usando AEAD com a tag como dados associados
6. Remove a tag do conjunto de tags (uso único)
7. Processa os blocos descriptografados

**Session Tag (etiqueta de sessão) não encontrada:**

Se a tag não for encontrada em nenhum tagset (conjunto de tags): - Pode ser uma mensagem NS (New Session, nova sessão) → tentar a descriptografia de NS - Pode ser uma mensagem NSR (New Session Reply, resposta de nova sessão) → tentar a descriptografia de NSR - Pode ser ES fora de ordem (ElGamal Session, sessão ElGamal) → aguardar brevemente a atualização do tagset - Pode ser um ataque de repetição → rejeitar - Podem ser dados corrompidos → rejeitar

**Carga útil vazia:**

Mensagens ES podem ter cargas úteis vazias (0 bytes): - Serve como ACK (confirmação) explícito quando um ACK Request (solicitação de confirmação) foi recebido - Fornece uma resposta na camada de protocolo sem dados da aplicação - Ainda consome uma session tag (rótulo de sessão) - Útil quando a camada superior não tem dados imediatos para enviar

**Propriedades de Segurança:** - Sigilo direto completo (Nível 5) após o recebimento do NSR - Criptografia autenticada com dados associados (AEAD) - A tag atua como dados associados adicionais - Máximo de 65535 mensagens por tagset (conjunto de tags) antes de ser necessário o ratchet (mecanismo de avanço criptográfico)

---

## Funções de Derivação de Chaves

Esta seção documenta todas as operações de KDF (função de derivação de chaves) usadas no ECIES (Esquema de Criptografia de Curva Elíptica Integrado), mostrando as derivações criptográficas completas.

### Notação e Constantes

**Constantes:** - `ZEROLEN` - Array de bytes de comprimento zero (string vazia) - `||` - Operador de concatenação

**Variáveis:** - `h` - Hash acumulado do transcrito (32 bytes) - `chainKey` - Chave de encadeamento para HKDF (32 bytes) - `k` - Chave de cifra simétrica (32 bytes) - `n` - Nonce (número único aleatório) / número da mensagem

**Chaves:** - `ask` / `apk` - Chave privada/pública estática de Alice - `aesk` / `aepk` - Chave privada/pública efêmera de Alice - `bsk` / `bpk` - Chave privada/pública estática de Bob - `besk` / `bepk` - Chave privada/pública efêmera de Bob

### KDFs da Mensagem NS

### KDF (função de derivação de chaves) 1: Chave de Cadeia Inicial

Executado uma vez na inicialização do protocolo (pode ser pré-calculado):

```python
# Protocol name (40 bytes, ASCII, no null termination)
protocol_name = "Noise_IKelg2+hs2_25519_ChaChaPoly_SHA256"

# Initialize hash
h = SHA256(protocol_name)

# Initialize chaining key
chainKey = h

# MixHash with empty prologue
h = SHA256(h)

# State: chainKey and h initialized
# Can be precalculated for all outbound sessions
```
**Resultado:** - `chainKey` = Chave de encadeamento inicial para todas as KDFs (funções de derivação de chaves) subsequentes - `h` = Hash de transcrição inicial

### KDF (função de derivação de chaves) 2: Mistura da chave estática de Bob

Bob executa isso uma vez (pode ser pré-calculado para todas as sessões de entrada):

```python
# Bob's static keys (published in LeaseSet)
bsk = GENERATE_PRIVATE()
bpk = DERIVE_PUBLIC(bsk)

# Mix Bob's public key into hash
h = SHA256(h || bpk)

# State: h updated with Bob's identity
# Can be precalculated by Bob for all inbound sessions
```
### KDF 3: Geração da Chave Efêmera de Alice

Alice gera chaves novas para cada mensagem NS:

```python
# Generate ephemeral key pair suitable for Elligator2
aesk = GENERATE_PRIVATE_ELG2()
aepk = DERIVE_PUBLIC(aesk)

# Mix ephemeral public key into hash
h = SHA256(h || aepk)

# Elligator2 encode for transmission
elg2_aepk = ENCODE_ELG2(aepk)

# State: h updated with Alice's ephemeral key
# Send elg2_aepk as first 32 bytes of NS message
```
### KDF 4: Seção de Chave Estática NS (es DH)

Deriva chaves para criptografar a chave estática de Alice:

```python
# Perform first DH (ephemeral-static)
sharedSecret = DH(aesk, bpk)  # Alice computes
# Equivalent: sharedSecret = DH(bsk, aepk)  # Bob computes

# Derive cipher key from shared secret
keydata = HKDF(chainKey, sharedSecret, "", 64)
chainKey = keydata[0:31]
k = keydata[32:63]

# AEAD encryption parameters
nonce = 0
associated_data = h  # Current hash transcript

# Encrypt static key section
if binding_requested:
    plaintext = apk  # Alice's static public key (32 bytes)
else:
    plaintext = bytes(32)  # All zeros for unbound

ciphertext = ENCRYPT(k, nonce, plaintext, associated_data)
# ciphertext = 32 bytes encrypted + 16 bytes MAC = 48 bytes

# Mix ciphertext into hash
h = SHA256(h || ciphertext)

# State: Static key section encrypted, h updated
# Send ciphertext (48 bytes) as next part of NS message
```
### KDF 5: Seção de carga útil NS (ss DH (Diffie-Hellman estático-estático), apenas vinculado)

Para sessões vinculadas, execute um segundo DH (Diffie-Hellman, protocolo de troca de chaves) para a criptografia da carga útil:

```python
if binding_requested:
    # Alice's static keys
    ask = GENERATE_PRIVATE()  # Alice's long-term key
    apk = DERIVE_PUBLIC(ask)
    
    # Perform second DH (static-static)
    sharedSecret = DH(ask, bpk)  # Alice computes
    # Equivalent: sharedSecret = DH(bsk, apk)  # Bob computes
    
    # Derive cipher key
    keydata = HKDF(chainKey, sharedSecret, "", 64)
    chainKey = keydata[0:31]
    k = keydata[32:63]
    
    nonce = 0
    associated_data = h
else:
    # Unbound: reuse keys from static key section
    # chainKey and k unchanged
    nonce = 1  # Increment nonce (reusing same key)
    associated_data = h

# Encrypt payload
payload = build_payload()  # DateTime + Garlic Cloves + etc.
ciphertext = ENCRYPT(k, nonce, payload, associated_data)

# Mix ciphertext into hash
h = SHA256(h || ciphertext)

# State: Payload encrypted, h contains complete NS transcript
# Save chainKey and h for NSR processing
# Send ciphertext as final part of NS message
```
**Notas importantes:**

1. **Vinculado vs Não vinculado**: 
   - Vinculado realiza 2 operações DH (es + ss)
   - Não vinculado realiza 1 operação DH (apenas es)
   - Não vinculado incrementa o nonce (número aleatório de uso único) em vez de derivar uma nova chave

2. **Segurança contra reutilização de chaves**:
   - Nonces (nonce: número usado uma vez) diferentes (0 vs 1) evitam a reutilização de chave/nonce
   - Dados associados diferentes (h é diferente) fornecem separação de domínios

3. **Transcrição de Hash**:
   - `h` agora contém: protocol_name, prólogo vazio, bpk, aepk, static_key_ciphertext, payload_ciphertext
   - Esta transcrição vincula todas as partes da mensagem NS entre si

### KDF (função de derivação de chaves) do conjunto de tags de resposta NSR

Bob gera tags para mensagens NSR (um tipo de mensagem):

```python
# Chain key from NS payload section
# chainKey = final chainKey from NS KDF

# Generate tagset key
tagsetKey = HKDF(chainKey, ZEROLEN, "SessionReplyTags", 32)

# Initialize NSR tagset (see DH_INITIALIZE below)
tagset_nsr = DH_INITIALIZE(chainKey, tagsetKey)

# Get tag for this NSR
tagsetEntry = tagset_nsr.GET_NEXT_ENTRY()
tag = tagsetEntry.SESSION_TAG  # 8 bytes

# State: tag available for NSR message
# Send tag as first 8 bytes of NSR
```
### KDFs (funções de derivação de chaves) de mensagens NSR

### KDF 6: Geração de Chaves Efêmeras do NSR

Bob gera uma nova chave efêmera para cada NSR:

```python
# Mix tag into hash (I2P extension to Noise)
h = SHA256(h || tag)

# Generate ephemeral key pair
besk = GENERATE_PRIVATE_ELG2()
bepk = DERIVE_PUBLIC(besk)

# Mix ephemeral public key into hash
h = SHA256(h || bepk)

# Elligator2 encode for transmission
elg2_bepk = ENCODE_ELG2(bepk)

# State: h updated with tag and Bob's ephemeral key
# Send elg2_bepk as bytes 9-40 of NSR message
```
### KDF 7: Seção de Chaves NSR (ee e se DH)

Deriva chaves para a seção de chaves NSR:

```python
# Perform third DH (ephemeral-ephemeral)
sharedSecret_ee = DH(aesk, bepk)  # Alice computes
# Equivalent: sharedSecret_ee = DH(besk, aepk)  # Bob computes

# Mix ee into chain
keydata = HKDF(chainKey, sharedSecret_ee, "", 32)
chainKey = keydata[0:31]

# Perform fourth DH (static-ephemeral)
sharedSecret_se = DH(ask, bepk)  # Alice computes
# Equivalent: sharedSecret_se = DH(besk, apk)  # Bob computes

# Derive cipher key from se
keydata = HKDF(chainKey, sharedSecret_se, "", 64)
chainKey = keydata[0:31]
k = keydata[32:63]

# AEAD encryption of empty data (key section has no payload)
nonce = 0
associated_data = h
ciphertext = ENCRYPT(k, nonce, ZEROLEN, associated_data)
# ciphertext = 16 bytes (MAC only, no plaintext)

# Mix ciphertext into hash
h = SHA256(h || ciphertext)

# State: Key section encrypted, chainKey contains all 4 DH results
# Send ciphertext (16 bytes MAC) as bytes 41-56 of NSR
```
**Crítico**: Isto conclui o handshake IK do Noise. `chainKey` agora contém contribuições de todas as quatro operações DH (es, ss, ee, se).

### KDF 8: Seção de Carga Útil do NSR

Deriva chaves para a criptografia da carga útil do NSR:

```python
# Split chainKey into bidirectional keys
keydata = HKDF(chainKey, ZEROLEN, "", 64)
k_ab = keydata[0:31]   # Alice → Bob key
k_ba = keydata[32:63]  # Bob → Alice key

# Initialize ES tagsets for both directions
tagset_ab = DH_INITIALIZE(chainKey, k_ab)  # Alice → Bob
tagset_ba = DH_INITIALIZE(chainKey, k_ba)  # Bob → Alice

# Derive NSR payload key (Bob → Alice)
k_nsr = HKDF(k_ba, ZEROLEN, "AttachPayloadKDF", 32)

# Encrypt NSR payload
nonce = 0
associated_data = h  # Binds payload to entire NSR
payload = build_payload()  # Usually application reply
ciphertext = ENCRYPT(k_nsr, nonce, payload, associated_data)

# State: Bidirectional ES sessions established
# tagset_ab and tagset_ba ready for ES messages
# Send ciphertext as bytes 57+ of NSR message
```
**Notas importantes:**

1. **Operação de separação**: 
   - Cria chaves independentes para cada direção
   - Evita a reutilização de chaves entre Alice→Bob e Bob→Alice

2. **Vinculação de Carga Útil NSR**:
   - Usa `h` como dados associados para vincular a carga útil ao handshake
   - Uma KDF ("AttachPayloadKDF") separada fornece separação de domínios

3. **Prontidão para ES**:
   - Após o NSR, ambas as partes podem enviar mensagens ES
   - Alice deve receber o NSR antes de enviar ES
   - Bob deve receber ES antes de enviar ES

### KDFs (funções de derivação de chaves) para Mensagens ES

As mensagens ES usam chaves de sessão pré-geradas provenientes de tagsets (conjuntos de tags):

```python
# Sender gets next tag and key
tagsetEntry = outbound_tagset.GET_NEXT_ENTRY()
tag = tagsetEntry.SESSION_TAG     # 8 bytes
k = tagsetEntry.SESSION_KEY       # 32 bytes
N = tagsetEntry.INDEX             # Message number

# Construct nonce (12 bytes)
nonce = [0x00, 0x00, 0x00, 0x00] + little_endian_8_bytes(N)

# AEAD encryption
associated_data = tag  # Tag is associated data
payload = build_payload()
ciphertext = ENCRYPT(k, nonce, payload, associated_data)

# Send: tag || ciphertext (8 + len(ciphertext) bytes)
```
**Processo do receptor:**

```python
# Extract tag
tag = message[0:8]

# Look up tag in inbound tagsets
tagsetEntry = inbound_tagset.GET_SESSION_KEY(tag)
if tagsetEntry is None:
    # Not an ES message, try NS/NSR decryption
    return try_handshake_decryption(message)

k = tagsetEntry.SESSION_KEY
N = tagsetEntry.INDEX

# Construct nonce
nonce = [0x00, 0x00, 0x00, 0x00] + little_endian_8_bytes(N)

# AEAD decryption
associated_data = tag
ciphertext = message[8:]
try:
    payload = DECRYPT(k, nonce, ciphertext, associated_data)
except AuthenticationError:
    # MAC verification failed, reject message
    return reject_message()

# Process payload blocks
process_payload(payload)

# Remove tag from tagset (one-time use)
inbound_tagset.remove(tag)
```
### Função DH_INITIALIZE

Cria um conjunto de tags para uma única direção:

```python
def DH_INITIALIZE(rootKey, k):
    """
    Initializes a tagset with session tag and symmetric key ratchets.
    
    Args:
        rootKey: Chain key from previous DH ratchet (32 bytes)
        k: Key material from split() or DH ratchet (32 bytes)
    
    Returns:
        tagset: Initialized tagset object
    """
    # Derive next root key and chain key
    keydata = HKDF(rootKey, k, "KDFDHRatchetStep", 64)
    nextRootKey = keydata[0:31]
    chainKey_tagset = keydata[32:63]
    
    # Derive separate chain keys for tags and keys
    keydata = HKDF(chainKey_tagset, ZEROLEN, "TagAndKeyGenKeys", 64)
    sessTag_ck = keydata[0:31]   # Session tag chain key
    symmKey_ck = keydata[32:63]  # Symmetric key chain key
    
    # Create tagset object
    tagset = Tagset()
    tagset.nextRootKey = nextRootKey
    tagset.sessTag_chainKey = sessTag_ck
    tagset.symmKey_chainKey = symmKey_ck
    tagset.lastIndex = -1
    
    return tagset
```
**Contextos de uso:**

1. **NSR Tagset (conjunto de etiquetas)**: `DH_INITIALIZE(chainKey_from_NS, tagsetKey_NSR)`
2. **ES Tagsets**: `DH_INITIALIZE(chainKey_from_NSR, k_ab or k_ba)`
3. **Ratcheted Tagsets**: `DH_INITIALIZE(nextRootKey_from_previous, tagsetKey_from_DH)`

---

## Mecanismos de catraca

ECIES usa três mecanismos ratchet (mecanismos de avanço criptográfico) sincronizados para fornecer sigilo futuro e gerenciamento eficiente de sessões.

### Visão geral do Ratchet

**Três tipos de Ratchet (mecanismo de catraca criptográfica):**

1. **DH Ratchet** (mecanismo de catraca Diffie-Hellman): Realiza trocas de chaves Diffie-Hellman para gerar novas chaves raiz
2. **Session Tag Ratchet** (mecanismo de catraca para tags de sessão): Deriva tags de sessão de uso único de forma determinística
3. **Symmetric Key Ratchet** (mecanismo de catraca para chaves simétricas): Deriva chaves de sessão para a criptografia de mensagens

**Relação:**

```
DH Ratchet (periodic)
    ↓
Creates new tagset
    ↓
Session Tag Ratchet (per message) ← synchronized → Symmetric Key Ratchet (per message)
    ↓                                                      ↓
Session Tags (8 bytes each)                      Session Keys (32 bytes each)
```
**Propriedades principais:**

- **Remetente**: Gera tags e chaves sob demanda (sem necessidade de armazenamento)
- **Receptor**: Pré-gera tags para a janela look-ahead (requer armazenamento)
- **Sincronização**: O índice da tag determina o índice da chave (N_tag = N_key)
- **Sigilo Futuro**: Obtido por meio de DH ratchet (mecanismo de avanço de Diffie-Hellman)
- **Eficiência**: O receptor pode adiar o cálculo da chave até que a tag seja recebida

### DH Ratchet (mecanismo de atualização contínua de chaves com Diffie-Hellman)

O DH ratchet (mecanismo de catraca Diffie-Hellman) proporciona sigilo futuro ao trocar periodicamente novas chaves efêmeras.

### Frequência do DH Ratchet (mecanismo de catraca Diffie-Hellman)

**Condições necessárias de Ratchet (mecanismo de atualização progressiva de chaves):** - Conjunto de tags aproximando-se da exaustão (a tag 65535 é o máximo) - Políticas específicas da implementação:   - Limite de contagem de mensagens (por exemplo, a cada 4096 mensagens)   - Limite de tempo (por exemplo, a cada 10 minutos)   - Limite de volume de dados (por exemplo, a cada 100 MB)

**Primeiro Ratchet recomendado (mecanismo de avanço de chaves)**: Por volta do número de tag 4096 para evitar atingir o limite

**Valores máximos:** - **ID máximo do conjunto de tags**: 65535 - **ID máximo de chave**: 32767 - **Máximo de mensagens por conjunto de tags**: 65535 - **Máximo teórico de dados por sessão**: ~6,9 TB (64K conjuntos de tags × 64K mensagens × 1730 bytes em média)

### IDs de Tag e de Chave do DH Ratchet (catraca Diffie–Hellman)

**Conjunto Inicial de Tags** (pós-handshake (negociação inicial)): - ID do conjunto de tags: 0 - Nenhum bloco NextKey (próxima chave) foi enviado ainda - Nenhum ID de chave atribuído

**Após o primeiro Ratchet (mecanismo de catraca de chaves)**: - ID do conjunto de tags: 1 = (1 + ID da chave da Alice + ID da chave do Bob) = (1 + 0 + 0) - Alice envia NextKey (mensagem de próxima chave) com ID da chave 0 - Bob responde com NextKey com ID da chave 0

**Conjuntos de tags subsequentes**: - ID do conjunto de tags = 1 + ID da chave do remetente + ID da chave do destinatário - Exemplo: Conjunto de tags 5 = (1 + sender_key_2 + receiver_key_2)

**Tabela de progressão do conjunto de tags:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Tag Set ID</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Sender Key ID</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Receiver Key ID</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">n/a</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">n/a</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Initial tag set (post-NSR)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">0 *</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">0 *</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">First ratchet (both generate new keys)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">2</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">1 *</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Sender generates new key</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">3</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">1 *</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Receiver generates new key</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">4</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">2 *</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Sender generates new key</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">5</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">2</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">2 *</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Receiver generates new key</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">...</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">...</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">...</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Pattern repeats</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">65534</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">32767 *</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">32766</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Second-to-last tag set</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">65535</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">32767</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">32767 *</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Final tag set</td>
    </tr>
  </tbody>
</table>
\* = Nova chave gerada neste ciclo do ratchet (mecanismo de avanço criptográfico)

**Regras de ID da chave:** - Os IDs são sequenciais a partir de 0 - Os IDs só aumentam quando uma nova chave é gerada - O ID de chave máximo é 32767 (15 bits) - Após o ID de chave 32767, é necessária uma nova sessão

### Fluxo de Mensagens do DH Ratchet (mecanismo de avanço criptográfico)

**Papéis:** - **Tag Sender** (Remetente de tags): Possui o conjunto de tags de saída, envia mensagens - **Tag Receiver** (Receptor de tags): Possui o conjunto de tags de entrada, recebe mensagens

**Padrão:** O remetente de tags inicia o ratchet (mecanismo de atualização de chaves) quando o conjunto de tags está quase esgotado.

**Diagrama de Fluxo de Mensagens:**

```
Tag Sender                         Tag Receiver

       ... using tag set #0 ...

(Tag set #0 approaching exhaustion)
(Generate new key #0)

NextKey forward, request reverse, with key #0  -------->
(Repeat until NextKey ACK received)
                                   (Generate new key #0)
                                   (Perform DH: sender_key_0 × receiver_key_0)
                                   (Create inbound tag set #1)

        <---------------           NextKey reverse, with key #0
                                   (Repeat until tag from tag set #1 received)

(Receive NextKey with key #0)
(Perform DH: sender_key_0 × receiver_key_0)
(Create outbound tag set #1)


       ... using tag set #1 ...


(Tag set #1 approaching exhaustion)
(Generate new key #1)

NextKey forward, with key #1        -------->
(Repeat until NextKey ACK received)
                                   (Reuse existing key #0)
                                   (Perform DH: sender_key_1 × receiver_key_0)
                                   (Create inbound tag set #2)

        <--------------            NextKey reverse, id 0 (ACK)
                                   (Repeat until tag from tag set #2 received)

(Receive NextKey with id 0)
(Perform DH: sender_key_1 × receiver_key_0)
(Create outbound tag set #2)


       ... using tag set #2 ...


(Tag set #2 approaching exhaustion)
(Reuse existing key #1)

NextKey forward, request reverse, id 1  -------->
(Repeat until NextKey received)
                                   (Generate new key #1)
                                   (Perform DH: sender_key_1 × receiver_key_1)
                                   (Create inbound tag set #3)

        <--------------            NextKey reverse, with key #1

(Receive NextKey with key #1)
(Perform DH: sender_key_1 × receiver_key_1)
(Create outbound tag set #3)


       ... using tag set #3 ...

       (Pattern repeats: even-numbered tag sets
        use forward key, odd-numbered use reverse key)
```
**Padrões de Ratchet (mecanismo de atualização de chaves):**

**Criando conjuntos de tags com numeração par** (2, 4, 6, ...): 1. O remetente gera uma nova chave 2. O remetente envia o NextKey block (bloco NextKey) com a nova chave 3. O receptor envia o NextKey block com o ID da chave antiga (ACK, confirmação) 4. Ambos realizam DH (Diffie-Hellman) com (nova chave do remetente × chave antiga do receptor)

**Criando conjuntos de tags com contagem ímpar** (3, 5, 7, ...): 1. O Remetente solicita a chave de retorno (envia NextKey com a flag de solicitação) 2. O Receptor gera uma nova chave 3. O Receptor envia um bloco NextKey com a nova chave 4. Ambos executam DH (Diffie-Hellman, troca de chaves) com (chave antiga do remetente × nova chave do receptor)

### Formato do bloco NextKey (próxima chave)

Consulte a seção Payload Format para obter a especificação detalhada do bloco NextKey.

**Elementos-chave:** - **Byte de flags**:   - Bit 0: Chave presente (1) ou apenas ID (0)   - Bit 1: Chave reversa (1) ou chave direta (0)   - Bit 2: Solicitar chave reversa (1) ou sem solicitação (0) - **ID da chave**: 2 bytes, big-endian (mais significativo primeiro) (0-32767) - **Chave pública**: 32 bytes X25519 (se o bit 0 = 1)

**Exemplos de NextKey Blocks (blocos NextKey):**

```python
# Sender initiates ratchet with new key (key ID 0, tag set 1)
NextKey(flags=0x01, key_id=0, pubkey=sender_key_0)

# Receiver replies with new key (key ID 0, tag set 1)
NextKey(flags=0x03, key_id=0, pubkey=receiver_key_0)

# Sender ratchets again with new key (key ID 1, tag set 2)
NextKey(flags=0x01, key_id=1, pubkey=sender_key_1)

# Receiver ACKs with old key ID (tag set 2)
NextKey(flags=0x02, key_id=0)

# Sender requests reverse key (tag set 3)
NextKey(flags=0x04, key_id=1)

# Receiver sends new reverse key (key ID 1, tag set 3)
NextKey(flags=0x03, key_id=1, pubkey=receiver_key_1)
```
### KDF do DH Ratchet (catraca Diffie-Hellman)

Quando novas chaves são trocadas:

```python
# Tag sender generates or reuses key
if generating_new:
    sender_sk = GENERATE_PRIVATE()
    sender_pk = DERIVE_PUBLIC(sender_sk)
else:
    # Reuse existing key pair
    sender_pk = existing_sender_pk

# Tag receiver generates or reuses key
if generating_new:
    receiver_sk = GENERATE_PRIVATE()
    receiver_pk = DERIVE_PUBLIC(receiver_sk)
else:
    # Reuse existing key pair
    receiver_pk = existing_receiver_pk

# Both parties perform DH
sharedSecret = DH(sender_sk, receiver_pk)

# Derive tagset key
tagsetKey = HKDF(sharedSecret, ZEROLEN, "XDHRatchetTagSet", 32)

# Get next root key from previous tagset
rootKey = previous_tagset.nextRootKey

# Initialize new tagset
new_tagset = DH_INITIALIZE(rootKey, tagsetKey)

# Tag sender: outbound tagset
# Tag receiver: inbound tagset
```
**Temporização Crítica:**

**Remetente de Tags:** - Cria um novo conjunto de tags de saída imediatamente - Passa a usar as novas tags imediatamente - Exclui o antigo conjunto de tags de saída

**Receptor de tags:** - Cria novo conjunto de tags de entrada - Mantém o conjunto de tags de entrada antigo por um período de carência (3 minutos) - Aceita tags de ambos os conjuntos (antigo e novo) durante o período de carência - Exclui o conjunto de tags de entrada antigo após o período de carência

### Gerenciamento de estado do DH Ratchet (mecanismo de avanço Diffie-Hellman)

**Estado do remetente:** - Conjunto de tags de saída atual - ID do conjunto de tags e IDs de chaves - Próxima chave raiz (para o próximo ratchet (mecanismo de avanço de chaves)) - Número de mensagens no conjunto de tags atual

**Estado do receptor:** - Conjunto(s) de tags de entrada em uso (pode haver 2 durante o período de carência) - Números de mensagens anteriores (PN) para detecção de lacunas - Janela de antecipação de tags pré-geradas - Próxima chave raiz (para a próxima ratchet (mecanismo de avanço criptográfico))

**Regras de Transição de Estado:**

1. **Antes do primeiro ratchet (mecanismo de avanço criptográfico)**:
   - Usando o conjunto de tags 0 (do NSR)
   - Nenhum ID de chave atribuído

2. **Iniciando Ratchet (mecanismo de catraca criptográfica)**:
   - Gerar nova chave (se o remetente estiver gerando nesta rodada)
   - Enviar o bloco NextKey na mensagem ES
   - Aguardar a resposta NextKey antes de criar um novo conjunto de tags de saída

3. **Recebendo Ratchet Request (pedido de ratchet)**:
   - Gerar nova chave (se o receptor estiver gerando nesta rodada)
   - Executar DH com a chave recebida
   - Criar novo conjunto de tags de entrada
   - Enviar resposta NextKey
   - Reter o conjunto de tags de entrada antigo por um período de carência

4. **Concluindo o Ratchet (mecanismo de catraca criptográfica)**:
   - Receber a resposta NextKey
   - Executar DH
   - Criar novo conjunto de tags de saída
   - Começar a usar as novas tags

### Ratchet de Tag de Sessão (mecanismo de avanço criptográfico)

O session tag ratchet (mecanismo de avanço de tags de sessão) gera tags de sessão de uso único de 8 bytes de forma determinística.

### Finalidade do Session Tag Ratchet (mecanismo de avanço das tags de sessão)

- Substitui a transmissão explícita de tags (ElGamal enviava tags de 32 bytes)
- Permite ao receptor pré-gerar tags para uma janela de antecipação
- O emissor gera sob demanda (sem necessidade de armazenamento)
- Sincroniza com o symmetric key ratchet (mecanismo de avanço de chaves simétricas) via índice

### Fórmula do Ratchet (mecanismo de avanço) de Tags de Sessão

**Inicialização:**

```python
# From DH_INITIALIZE
sessTag_ck = initial_chain_key  # 32 bytes

# Initialize session tag ratchet
keydata = HKDF(sessTag_ck, ZEROLEN, "STInitialization", 64)
sessTag_chainKey = keydata[0:31]    # First chain key
SESSTAG_CONSTANT = keydata[32:63]   # Constant for all tags in this tagset
```
**Geração de tag (para a tag N):**

```python
# Generate tag N
keydata = HKDF(sessTag_chainKey_(N-1), SESSTAG_CONSTANT, "SessionTagKeyGen", 64)
sessTag_chainKey_N = keydata[0:31]  # Chain key for next tag
tag_N = keydata[32:39]              # Session tag (8 bytes)

# Chain continues for each tag
# tag_0, tag_1, tag_2, ..., tag_65535
```
**Sequência completa:**

```python
# Tag 0
keydata_0 = HKDF(sessTag_chainKey, SESSTAG_CONSTANT, "SessionTagKeyGen", 64)
sessTag_chainKey_0 = keydata_0[0:31]
tag_0 = keydata_0[32:39]

# Tag 1
keydata_1 = HKDF(sessTag_chainKey_0, SESSTAG_CONSTANT, "SessionTagKeyGen", 64)
sessTag_chainKey_1 = keydata_1[0:31]
tag_1 = keydata_1[32:39]

# Tag N
keydata_N = HKDF(sessTag_chainKey_(N-1), SESSTAG_CONSTANT, "SessionTagKeyGen", 64)
sessTag_chainKey_N = keydata_N[0:31]
tag_N = keydata_N[32:39]
```
### Implementação do Remetente do Session Tag Ratchet (mecanismo de atualização progressiva de tags de sessão)

```python
class OutboundTagset:
    def __init__(self, sessTag_ck):
        # Initialize
        keydata = HKDF(sessTag_ck, ZEROLEN, "STInitialization", 64)
        self.chainKey = keydata[0:31]
        self.constant = keydata[32:63]
        self.index = -1
    
    def get_next_tag(self):
        # Increment index
        self.index += 1
        
        if self.index > 65535:
            raise TagsetExhausted("Ratchet required")
        
        # Generate tag
        keydata = HKDF(self.chainKey, self.constant, "SessionTagKeyGen", 64)
        self.chainKey = keydata[0:31]
        tag = keydata[32:39]
        
        return (tag, self.index)
```
**Processo do Remetente:** 1. Chame `get_next_tag()` para cada mensagem 2. Use a tag retornada na ES message (mensagem ES) 3. Armazene o índice N para possível rastreamento de ACK (confirmação) 4. Não é necessário armazenar tags (geradas sob demanda)

### Implementação do receptor do Session Tag Ratchet (mecanismo de catraca de tags de sessão)

```python
class InboundTagset:
    def __init__(self, sessTag_ck, look_ahead=32):
        # Initialize
        keydata = HKDF(sessTag_ck, ZEROLEN, "STInitialization", 64)
        self.chainKey = keydata[0:31]
        self.constant = keydata[32:63]
        self.index = -1
        self.look_ahead = look_ahead
        self.tags = {}  # Dictionary: tag -> index
        
        # Pre-generate initial tags
        self.extend(look_ahead)
    
    def extend(self, count):
        """Generate 'count' more tags"""
        for _ in range(count):
            self.index += 1
            
            if self.index > 65535:
                return  # Cannot exceed maximum
            
            # Generate tag
            keydata = HKDF(self.chainKey, self.constant, "SessionTagKeyGen", 64)
            self.chainKey = keydata[0:31]
            tag = keydata[32:39]
            
            # Store tag
            self.tags[tag] = self.index
    
    def lookup_tag(self, tag):
        """Look up tag and return index"""
        if tag in self.tags:
            index = self.tags[tag]
            # Remove tag (one-time use)
            del self.tags[tag]
            return index
        return None
    
    def check_and_extend(self):
        """Extend if tag count is low"""
        current_count = len(self.tags)
        if current_count < self.look_ahead // 2:
            # Extend to restore window
            self.extend(self.look_ahead - current_count)
```
**Processo do receptor:** 1. Pré-gerar tags para a look-ahead window (janela de antecipação) (por exemplo, 32 tags) 2. Armazenar as tags em uma tabela hash ou dicionário 3. Quando a mensagem chegar, consultar a tag para obter o índice N 4. Remover a tag do armazenamento (uso único) 5. Estender a janela se a contagem de tags cair abaixo do limiar

### Estratégia de antecipação de tags de sessão

**Objetivo**: Equilibrar o uso de memória vs. o tratamento de mensagens fora de ordem

**Tamanhos de Look-Ahead (antecipação) recomendados:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Tagset Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Initial Size</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Maximum Size</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">NSR tagset</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">12</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">12</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Short-lived</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ES tagset 0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">24</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">160</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Initial ES tagset</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ES tagset 1+</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">160</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">160</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Ratcheted tagsets</td>
    </tr>
  </tbody>
</table>
**Antecipação Adaptativa:**

```python
# Dynamic look-ahead based on highest tag received
look_ahead = min(tsmax, tsmin + N // 4)

# Example:
# tsmin = 24, tsmax = 160
# N = 0:   look_ahead = min(160, 24 + 0/4) = 24
# N = 100: look_ahead = min(160, 24 + 100/4) = 49
# N = 500: look_ahead = min(160, 24 + 500/4) = 149
# N = 544: look_ahead = min(160, 24 + 544/4) = 160
```
**Aparar por trás:**

```python
# Trim tags far behind highest received
trim_behind = look_ahead // 2

# If highest received tag is N=100, trim tags below N=50
```
**Cálculo de memória:**

```python
# Per tag: 8 bytes (tag) + 2 bytes (index) + overhead ≈ 16 bytes
# Look-ahead of 160 tags ≈ 2.5 KB per inbound tagset

# With multiple sessions:
# 100 inbound sessions × 2.5 KB = 250 KB total
```
### Tratamento de Session Tag (tag de sessão) fora de ordem

**Cenário**: Mensagens chegam fora de ordem

```
Expected: tag_5, tag_6, tag_7, tag_8
Received: tag_5, tag_7, tag_6, tag_8
```
**Comportamento do receptor:**

1. Receber tag_5:
   - Consultar: encontrado no índice 5
   - Processar mensagem
   - Remover tag_5
   - Maior recebido: 5

2. Receber tag_7 (fora de ordem):
   - Consultar: encontrado no índice 7
   - Processar mensagem
   - Remover tag_7
   - Maior recebido: 7
   - Observação: tag_6 ainda armazenado (ainda não recebido)

3. Receber tag_6 (atrasado):
   - Consultar: encontrado no índice 6
   - Processar mensagem
   - Remover tag_6
   - Maior recebido: 7 (inalterado)

4. Receber tag_8:
   - Consultar: encontrado no índice 8
   - Processar a mensagem
   - Remover tag_8
   - Maior recebido: 8

**Manutenção da Janela:** - Acompanhar o maior índice recebido - Manter lista de índices ausentes (gaps, lacunas) - Estender a janela com base no maior índice - Opcional: Expirar gaps antigos após o tempo limite

### Catraca de Chave Simétrica

O symmetric key ratchet (mecanismo de atualização progressiva de chaves simétricas) gera chaves de criptografia de 32 bytes sincronizadas com tags de sessão.

### Finalidade do Symmetric Key Ratchet (mecanismo de avanço criptográfico com chave simétrica)

- Fornece uma chave de criptografia exclusiva para cada mensagem
- Sincronizada com o session tag ratchet (mecanismo de catraca para tags de sessão; mesmo índice)
- O remetente pode gerar sob demanda
- O destinatário pode adiar a geração até que a tag seja recebida

### Fórmula do Symmetric Key Ratchet (mecanismo de catraca de chave simétrica)

**Inicialização:**

```python
# From DH_INITIALIZE
symmKey_ck = initial_chain_key  # 32 bytes

# No additional initialization needed
# Unlike session tag ratchet, no constant is derived
```
**Geração de chave (para a chave N):**

```python
# Generate key N
SYMMKEY_CONSTANT = ZEROLEN  # Empty string
keydata = HKDF(symmKey_chainKey_(N-1), SYMMKEY_CONSTANT, "SymmetricRatchet", 64)
symmKey_chainKey_N = keydata[0:31]  # Chain key for next key
key_N = keydata[32:63]              # Session key (32 bytes)
```
**Sequência Completa:**

```python
# Key 0
keydata_0 = HKDF(symmKey_ck, ZEROLEN, "SymmetricRatchet", 64)
symmKey_chainKey_0 = keydata_0[0:31]
key_0 = keydata_0[32:63]

# Key 1
keydata_1 = HKDF(symmKey_chainKey_0, ZEROLEN, "SymmetricRatchet", 64)
symmKey_chainKey_1 = keydata_1[0:31]
key_1 = keydata_1[32:63]

# Key N
keydata_N = HKDF(symmKey_chainKey_(N-1), ZEROLEN, "SymmetricRatchet", 64)
symmKey_chainKey_N = keydata_N[0:31]
key_N = keydata_N[32:63]
```
### Implementação do remetente do Symmetric Key Ratchet (mecanismo de catraca de chave simétrica)

```python
class OutboundKeyRatchet:
    def __init__(self, symmKey_ck):
        self.chainKey = symmKey_ck
        self.index = -1
    
    def get_key(self, index):
        """Generate key for specific index"""
        # Fast-forward to desired index if needed
        while self.index < index:
            self.index += 1
            keydata = HKDF(self.chainKey, ZEROLEN, "SymmetricRatchet", 64)
            self.chainKey = keydata[0:31]
            if self.index == index:
                return keydata[32:63]
        
        # Should not reach here if called correctly
        raise ValueError("Key already generated")
```
**Processo do Remetente:** 1. Obter a próxima tag e seu índice N 2. Gerar a chave para o índice N 3. Usar a chave para criptografar a mensagem 4. Não é necessário armazenar a chave

### Implementação do Receptor do Symmetric Key Ratchet (mecanismo de avanço de chave simétrica)

**Estratégia 1: Geração Adiada (Recomendado)**

```python
class InboundKeyRatchet:
    def __init__(self, symmKey_ck):
        self.chainKey = symmKey_ck
        self.index = -1
        self.cache = {}  # Optional: cache recently used keys
    
    def get_key(self, index):
        """Generate key for specific index"""
        # Check cache first (optional optimization)
        if index in self.cache:
            key = self.cache[index]
            del self.cache[index]
            return key
        
        # Fast-forward to desired index
        while self.index < index:
            self.index += 1
            keydata = HKDF(self.chainKey, ZEROLEN, "SymmetricRatchet", 64)
            self.chainKey = keydata[0:31]
            
            if self.index == index:
                return keydata[32:63]
        
        raise ValueError("Index already passed")
```
**Processo de Geração Diferida:** 1. Receber mensagem ES com tag 2. Consultar a tag para obter o índice N 3. Gerar as chaves de 0 a N (se ainda não tiverem sido geradas) 4. Usar a chave N para descriptografar a mensagem 5. chain key (chave da cadeia) agora posicionada no índice N

**Vantagens:** - Uso mínimo de memória - Chaves geradas apenas quando necessário - Implementação simples

**Desvantagens:** - Deve gerar todas as chaves de 0 a N no primeiro uso - Não consegue lidar com mensagens fora de ordem sem armazenamento em cache

**Estratégia 2: Pré-geração com janela de tags (Alternativa)**

```python
class InboundKeyRatchet:
    def __init__(self, symmKey_ck):
        self.chainKey = symmKey_ck
        self.index = -1
        self.keys = {}  # Dictionary: index -> key
    
    def extend(self, count):
        """Pre-generate 'count' more keys"""
        for _ in range(count):
            self.index += 1
            keydata = HKDF(self.chainKey, ZEROLEN, "SymmetricRatchet", 64)
            self.chainKey = keydata[0:31]
            key = keydata[32:63]
            self.keys[self.index] = key
    
    def get_key(self, index):
        """Retrieve pre-generated key"""
        if index in self.keys:
            key = self.keys[index]
            del self.keys[index]
            return key
        return None
```
**Processo de pré-geração:** 1. Pré-gerar chaves que correspondam à janela de tags (por exemplo, 32 chaves) 2. Armazenar chaves indexadas pelo número da mensagem 3. Quando a tag for recebida, procurar a chave correspondente 4. Estender a janela à medida que as tags forem usadas

**Vantagens:** - Lida naturalmente com mensagens fora de ordem - Recuperação rápida de chaves (sem atraso de geração)

**Desvantagens:** - Maior uso de memória (32 bytes por chave vs 8 bytes por tag) - Deve manter as chaves sincronizadas com as tags

**Comparação de memória:**

```python
# Look-ahead of 160:
# Tags only:  160 × 16 bytes = 2.5 KB
# Tags+Keys:  160 × (16 + 32) bytes = 7.5 KB
# 
# For 100 sessions:
# Tags only:  250 KB
# Tags+Keys:  750 KB
```
### Sincronização do Ratchet (mecanismo de avanço criptográfico) simétrico com tags de sessão

**Requisito Crítico**: O índice da tag de sessão DEVE ser igual ao índice da chave simétrica

```python
# Sender
tag, index = outbound_tagset.get_next_tag()
key = outbound_keyratchet.get_key(index)  # Same index
nonce = construct_nonce(index)
ciphertext = ENCRYPT(key, nonce, payload, tag)

# Receiver
index = inbound_tagset.lookup_tag(tag)
key = inbound_keyratchet.get_key(index)  # Same index
nonce = construct_nonce(index)
plaintext = DECRYPT(key, nonce, ciphertext, tag)
```
**Modos de falha:**

Se a sincronização falhar: - Chave incorreta usada para descriptografia - Falha na verificação do MAC - Mensagem rejeitada

**Prevenção:** - Sempre use o mesmo índice para a tag e a chave - Nunca pule índices em nenhum dos ratchets (mecanismo de catraca criptográfica) - Trate mensagens fora de ordem com cuidado

### Construção do Nonce do Ratchet Simétrico (mecanismo de catraca criptográfica)

Nonce (número usado uma vez) é derivado do número da mensagem:

```python
def construct_nonce(index):
    """
    Construct 12-byte nonce for ChaCha20-Poly1305
    
    Args:
        index: Message number (0-65535)
    
    Returns:
        nonce: 12-byte nonce
    """
    # First 4 bytes are always zero
    nonce = bytearray(12)
    nonce[0:4] = b'\x00\x00\x00\x00'
    
    # Last 8 bytes are little-endian message number
    nonce[4:12] = index.to_bytes(8, byteorder='little')
    
    return bytes(nonce)
```
**Exemplos:**

```python
index = 0:     nonce = 0x00000000 0000000000000000
index = 1:     nonce = 0x00000000 0100000000000000
index = 255:   nonce = 0x00000000 FF00000000000000
index = 256:   nonce = 0x00000000 0001000000000000
index = 65535: nonce = 0x00000000 FFFF000000000000
```
**Propriedades Importantes:** - Nonces (valores únicos usados uma vez) são exclusivos para cada mensagem em um tagset (conjunto de tags) - Nonces nunca se repetem (tags de uso único garantem isso) - Um contador de 8 bytes permite 2^64 mensagens (nós só usamos 2^16) - O formato do Nonce corresponde à construção baseada em contador da RFC 7539

---

## Gerenciamento de Sessões

### Contexto da Sessão

Todas as sessões de entrada e de saída devem pertencer a um contexto específico:

1. **Contexto do Router**: Sessões para o próprio router
2. **Contexto de Destino**: Sessões para um destino local específico (aplicação cliente)

**Regra Crítica**: As sessões NÃO DEVEM ser compartilhadas entre contextos para evitar ataques de correlação.

**Implementação:**

```python
class SessionKeyManager:
    """Context for managing sessions (router or destination)"""
    def __init__(self, context_id):
        self.context_id = context_id
        self.inbound_sessions = {}   # far_end_dest -> [sessions]
        self.outbound_sessions = {}  # far_end_dest -> session
        self.static_keypair = generate_keypair()  # Context's identity
    
    def get_outbound_session(self, destination):
        """Get or create outbound session to destination"""
        if destination not in self.outbound_sessions:
            self.outbound_sessions[destination] = create_outbound_session(destination)
        return self.outbound_sessions[destination]
    
    def add_inbound_session(self, session, destination=None):
        """Add inbound session, optionally bound to destination"""
        if destination:
            if destination not in self.inbound_sessions:
                self.inbound_sessions[destination] = []
            self.inbound_sessions[destination].append(session)
        else:
            # Unbound session
            self.inbound_sessions[None].append(session)
```
**Implementação do I2P em Java:**

No I2P em Java, a classe `SessionKeyManager` fornece esta funcionalidade: - Um `SessionKeyManager` por router - Um `SessionKeyManager` por destino local - Gerenciamento separado das sessões ECIES e ElGamal em cada contexto

### Vinculação de Sessão

**Binding** (vinculação) associa uma sessão a um destino remoto específico.

### Sessões Vinculadas

**Características:** - Incluir a chave estática do remetente na NS message (mensagem NS) - O destinatário pode identificar o destino do remetente - Permite comunicação bidirecional - Uma única sessão de saída por destino - Pode haver várias sessões de entrada (durante transições)

**Casos de uso:** - Conexões de streaming (semelhantes ao TCP) - Datagramas com suporte a resposta - Qualquer protocolo que exija requisição/resposta

**Processo de associação:**

```python
# Alice creates bound outbound session
outbound_session = OutboundSession(
    destination=bob_destination,
    static_key=alice_static_key,
    bound=True
)

# Alice sends NS with static key
ns_message = build_ns_message(
    ephemeral_key=alice_ephemeral_key,
    static_key=alice_static_key,  # Included for binding
    payload=data
)

# Bob receives NS
bob_receives_ns(ns_message)
# Bob extracts Alice's static key
alice_static_key = decrypt_static_key_section(ns_message)

# Bob looks up Alice's destination (from bundled LeaseSet)
alice_destination = lookup_destination_by_static_key(alice_static_key)

# Bob creates bound inbound session
inbound_session = InboundSession(
    destination=alice_destination,
    bound=True
)

# Bob pairs with outbound session
outbound_session = OutboundSession(
    destination=alice_destination,
    bound=True
)
```
**Benefícios:** 1. **DH Efêmero-Efêmero**: A resposta usa ee DH (sigilo de encaminhamento perfeito) 2. **Continuidade de sessão**: Ratchets (mecanismo de avanço criptográfico) mantêm o vínculo com o mesmo destino 3. **Segurança**: Impede sequestro de sessão (autenticado por chave estática) 4. **Eficiência**: Uma única sessão por destino (sem duplicação)

### Sessões não vinculadas

**Características:** - Sem chave estática na mensagem NS (a seção de flags contém apenas zeros) - O destinatário não pode identificar o remetente - Comunicação apenas unidirecional - Várias sessões para o mesmo destino são permitidas

**Casos de uso:** - Datagramas brutos (fire-and-forget, enviar e não esperar resposta) - Publicação anônima - Mensagens no estilo broadcast

**Propriedades:** - Mais anônimo (sem identificação do remetente) - Mais eficiente (1 DH vs 2 DH no handshake) - Não é possível responder (o destinatário não sabe para onde responder) - Sem ratcheting de sessão (mecanismo de atualização progressiva de chaves; uso único ou limitado)

### Emparelhamento de Sessão

**Emparelhamento** conecta uma sessão de entrada com uma sessão de saída para comunicação bidirecional.

### Criando Sessões Emparelhadas

**Perspectiva de Alice (iniciadora):**

```python
# Create outbound session to Bob
outbound_session = create_outbound_session(bob_destination)

# Create paired inbound session
inbound_session = create_inbound_session(
    paired_with=outbound_session,
    bound_to=bob_destination
)

# Link them
outbound_session.paired_inbound = inbound_session
inbound_session.paired_outbound = outbound_session

# Send NS message
send_ns_message(outbound_session, payload)
```
**Perspectiva de Bob (respondente):**

```python
# Receive NS message
ns_message = receive_ns_message()

# Create inbound session
inbound_session = create_inbound_session_from_ns(ns_message)

# If NS contains static key (bound):
if ns_message.has_static_key():
    alice_destination = extract_destination(ns_message)
    inbound_session.bind_to(alice_destination)
    
    # Create paired outbound session
    outbound_session = create_outbound_session(alice_destination)
    
    # Link them
    outbound_session.paired_inbound = inbound_session
    inbound_session.paired_outbound = outbound_session

# Send NSR
send_nsr_message(inbound_session, outbound_session, payload)
```
### Benefícios do Emparelhamento de Sessão

1. **ACKs no próprio canal**: Pode confirmar mensagens sem um clove separado (submensagem no esquema garlic)
2. **Ratcheting eficiente (mecanismo de avanço de chaves)**: Ambas as direções avançam em conjunto
3. **Controle de fluxo**: Pode implementar back-pressure (propagação de pressão/limitação de origem) entre sessões emparelhadas
4. **Consistência de estado**: Mais fácil manter o estado sincronizado

### Regras de Emparelhamento de Sessão

- A sessão de saída pode estar desemparelhada (NS sem vínculo; 'NS' mantido em inglês como termo técnico)
- A sessão de entrada para NS vinculado deve ser pareada
- O pareamento ocorre na criação da sessão, não depois
- Sessões pareadas têm o mesmo vínculo de destino
- Ratchets ocorrem de forma independente, mas são coordenados (ratchets: mecanismo de atualização criptográfica)

### Ciclo de vida da sessão

### Ciclo de vida da sessão: fase de criação

**Criação da sessão de saída (Alice):**

```python
def create_outbound_session(destination, bound=True):
    session = OutboundSession()
    session.destination = destination
    session.bound = bound
    session.state = SessionState.NEW
    session.created_time = now()
    
    # Generate keys for NS message
    session.ephemeral_keypair = generate_elg2_keypair()
    if bound:
        session.static_key = context.static_keypair.public_key
    
    # Will be populated after NSR received
    session.outbound_tagset = None
    session.inbound_tagset = None
    
    return session
```
**Criação de Sessão de Entrada (Bob):**

```python
def create_inbound_session_from_ns(ns_message):
    session = InboundSession()
    session.state = SessionState.ESTABLISHED
    session.created_time = now()
    
    # Extract from NS
    session.remote_ephemeral_key = ns_message.ephemeral_key
    session.remote_static_key = ns_message.static_key
    
    if session.remote_static_key:
        session.bound = True
        session.destination = lookup_destination(session.remote_static_key)
    else:
        session.bound = False
        session.destination = None
    
    # Generate keys for NSR
    session.ephemeral_keypair = generate_elg2_keypair()
    
    # Create tagsets from KDF
    session.inbound_tagset = create_tagset_from_nsr()
    session.outbound_tagset = create_tagset_from_nsr()
    
    return session
```
### Ciclo de Vida da Sessão: Fase Ativa

**Transições de Estado:**

```
NEW (outbound only)
  ↓
  NS sent
  ↓
PENDING_REPLY (outbound only)
  ↓
  NSR received
  ↓
ESTABLISHED
  ↓
  ES messages exchanged
  ↓
ESTABLISHED (ongoing)
  ↓
  (optional) RATCHETING
  ↓
ESTABLISHED
```
**Manutenção de Sessões Ativas:**

```python
def maintain_active_session(session):
    # Update last activity time
    session.last_activity = now()
    
    # Check for ratchet needed
    if session.outbound_tagset.needs_ratchet():
        initiate_ratchet(session)
    
    # Check for incoming ratchet
    if received_nextkey_block():
        process_ratchet(session)
    
    # Trim old tags from inbound tagset
    session.inbound_tagset.expire_old_tags()
    
    # Check session health
    if session.idle_time() > SESSION_TIMEOUT:
        mark_session_idle(session)
```
### Ciclo de Vida da Sessão: Fase de Expiração

**Valores de tempo limite da sessão:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Session Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Sender Timeout</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Receiver Timeout</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">NSR tagset</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">N/A</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3 minutes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Short-lived</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ES tagset 0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">8 minutes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">10 minutes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Initial</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ES tagset 1+</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">8 minutes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">10 minutes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Ratcheted</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Old tagset</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">N/A</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3 minutes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">After ratchet</td>
    </tr>
  </tbody>
</table>
**Lógica de expiração:**

```python
def check_session_expiration():
    for session in active_sessions:
        # Outbound session expiration (sender)
        if session.is_outbound():
            if session.idle_time() > 8 * 60:  # 8 minutes
                expire_outbound_session(session)
        
        # Inbound session expiration (receiver)
        else:
            if session.idle_time() > 10 * 60:  # 10 minutes
                expire_inbound_session(session)
    
    # Old tagsets (after ratchet)
    for tagset in old_tagsets:
        if tagset.age() > 3 * 60:  # 3 minutes
            delete_tagset(tagset)
```
**Regra Crítica**: As sessões de saída DEVEM expirar antes das sessões de entrada para evitar dessincronização.

**Finalização ordenada:**

```python
def terminate_session(session, reason=0):
    # Send Termination block (if implemented)
    send_termination_block(session, reason)
    
    # Mark session for deletion
    session.state = SessionState.TERMINATED
    
    # Keep session briefly for final messages
    schedule_deletion(session, delay=30)  # 30 seconds
    
    # Notify paired session
    if session.paired_session:
        session.paired_session.mark_remote_terminated()
```
### Múltiplas mensagens NS

**Cenário**: A mensagem NS de Alice se perde ou a resposta NSR se perde.

**Comportamento de Alice:**

```python
class OutboundSession:
    def __init__(self):
        self.ns_messages_sent = []
        self.ns_timer = None
        self.max_ns_attempts = 5
    
    def send_ns_message(self, payload):
        # Generate new ephemeral key for each NS
        ephemeral_key = generate_elg2_keypair()
        
        ns_message = build_ns_message(
            ephemeral_key=ephemeral_key,
            static_key=self.static_key,
            payload=payload
        )
        
        # Store state for this NS
        ns_state = {
            'ephemeral_key': ephemeral_key,
            'chainkey': compute_chainkey(ns_message),
            'hash': compute_hash(ns_message),
            'tagset': derive_nsr_tagset(ns_message),
            'sent_time': now()
        }
        self.ns_messages_sent.append(ns_state)
        
        # Send message
        send_message(ns_message)
        
        # Set timer for retry
        if not self.ns_timer:
            self.ns_timer = set_timer(1.0, self.on_ns_timeout)
    
    def on_ns_timeout(self):
        if len(self.ns_messages_sent) >= self.max_ns_attempts:
            # Give up
            fail_session("No NSR received after {self.max_ns_attempts} attempts")
            return
        
        # Retry with new NS message
        send_ns_message(self.payload)
    
    def on_nsr_received(self, nsr_message):
        # Cancel timer
        cancel_timer(self.ns_timer)
        
        # Find which NS this NSR responds to
        tag = nsr_message.tag
        for ns_state in self.ns_messages_sent:
            if tag in ns_state['tagset']:
                # This NSR corresponds to this NS
                self.active_ns_state = ns_state
                break
        
        # Process NSR and complete handshake
        complete_handshake(nsr_message, self.active_ns_state)
        
        # Discard other NS states
        self.ns_messages_sent = []
```
**Propriedades importantes:**

1. **Chaves Efêmeras Exclusivas**: Cada NS utiliza uma chave efêmera diferente
2. **Handshakes (negociação) Independentes**: Cada NS cria um estado de handshake separado
3. **Correlação NSR**: A tag NSR identifica a qual NS ela responde
4. **Limpeza de Estado**: Estados de NS não utilizados são descartados após uma NSR bem-sucedida

**Prevenção de ataques:**

Para evitar o esgotamento de recursos:

```python
# Limit NS sending rate
max_ns_rate = 5 per 10 seconds per destination

# Limit total NS attempts
max_ns_attempts = 5

# Limit total pending NS states
max_pending_ns = 10 per context
```
### Múltiplas mensagens NSR

**Cenário**: Bob envia múltiplas NSRs (por exemplo, dados de resposta divididos em várias mensagens).

**Comportamento de Bob:**

```python
class InboundSession:
    def send_nsr_replies(self, payload_chunks):
        # One NS received, multiple NSRs to send
        for chunk in payload_chunks:
            # Generate new ephemeral key for each NSR
            ephemeral_key = generate_elg2_keypair()
            
            # Get next tag from NSR tagset
            tag = self.nsr_tagset.get_next_tag()
            
            nsr_message = build_nsr_message(
                tag=tag,
                ephemeral_key=ephemeral_key,
                payload=chunk
            )
            
            send_message(nsr_message)
        
        # Wait for ES message from Alice
        self.state = SessionState.AWAITING_ES
```
**Comportamento de Alice:**

```python
class OutboundSession:
    def on_nsr_received(self, nsr_message):
        if self.state == SessionState.PENDING_REPLY:
            # First NSR received
            complete_handshake(nsr_message)
            self.state = SessionState.ESTABLISHED
            
            # Create ES sessions
            self.es_outbound_tagset = derive_es_outbound_tagset()
            self.es_inbound_tagset = derive_es_inbound_tagset()
            
            # Send ES message (ACK)
            send_es_message(empty_payload)
        
        elif self.state == SessionState.ESTABLISHED:
            # Additional NSR received
            # Decrypt and process payload
            payload = decrypt_nsr_payload(nsr_message)
            process_payload(payload)
            
            # These NSRs are from other NS attempts, ignore handshake
```
**Limpeza de Bob:**

```python
class InboundSession:
    def on_es_received(self, es_message):
        # First ES received from Alice
        # This confirms which NSR Alice used
        
        # Clean up other handshake states
        for other_ns_state in self.pending_ns_states:
            if other_ns_state != self.active_ns_state:
                delete_ns_state(other_ns_state)
        
        # Delete unused NSR tagsets
        for tagset in self.nsr_tagsets:
            if tagset != self.active_nsr_tagset:
                delete_tagset(tagset)
        
        self.state = SessionState.ESTABLISHED
```
**Propriedades importantes:**

1. **Múltiplos NSRs permitidos**: Bob pode enviar vários NSRs para cada NS
2. **Chaves efêmeras diferentes**: Cada NSR deve usar uma chave efêmera exclusiva
3. **Mesmo tagset (conjunto de tags) do NSR**: Todos os NSRs para um NS usam o mesmo tagset
4. **O primeiro ES vence**: O primeiro ES de Alice determina qual NSR foi bem-sucedido
5. **Limpeza após ES**: Bob descarta estados não utilizados após o recebimento do ES

### Máquina de estados da sessão

**Diagrama de Estados Completo:**

```
                    Outbound Session                    Inbound Session

                         NEW
                          |
                     send NS
                          |
                   PENDING_REPLY -------------------- receive NS ---> ESTABLISHED
                          |                                                |
                   receive NSR                                        send NSR
                          |                                                |
                    ESTABLISHED <---------- receive ES ------------- AWAITING_ES
                          |                     |                          |
                    ┌─────┴─────┐               |                    receive ES
                    |           |               |                          |
              send ES      receive ES           |                    ESTABLISHED
                    |           |               |                          |
                    └─────┬─────┘               |                ┌─────────┴─────────┐
                          |                     |                |                   |
                          |                     |          send ES              receive ES
                          |                     |                |                   |
                          |                     |                └─────────┬─────────┘
                          |                     |                          |
                          └─────────────────────┴──────────────────────────┘
                                              ACTIVE
                                                |
                                         idle timeout
                                                |
                                             EXPIRED
```
**Descrições dos estados:**

- **NEW**: Sessão de saída criada, nenhum NS enviado ainda
- **PENDING_REPLY**: NS enviado, aguardando NSR
- **AWAITING_ES**: NSR enviado, aguardando o primeiro ES de Alice
- **ESTABLISHED**: Handshake concluído, pode enviar/receber ES
- **ACTIVE**: Trocando ativamente mensagens ES
- **RATCHETING**: DH ratchet (mecanismo de avanço de chaves Diffie-Hellman) em andamento (subconjunto de ACTIVE)
- **EXPIRED**: Sessão expirada, aguardando exclusão
- **TERMINATED**: Sessão encerrada explicitamente

---

## Formato da Carga Útil

A seção de carga útil de todas as mensagens ECIES (NS, NSR, ES) usa um formato baseado em blocos semelhante ao NTCP2.

### Estrutura de Blocos

**Formato geral:**

```
+----+----+----+----+----+----+----+----+
|blk |  size   |       data             |
+----+----+----+                        +
|                                       |
~               ...                     ~
|                                       |
+----+----+----+----+----+----+----+----+
|blk |  size   |       data             |
+----+----+----+                        +
|                                       |
~               ...                     ~
|                                       |
+----+----+----+----+----+----+----+----+
```
**Campos:**

- `blk`: 1 byte - Número do tipo de bloco
- `size`: 2 bytes - Tamanho, em big-endian, do campo de dados (0-65516)
- `data`: Tamanho variável - Dados específicos do bloco

**Restrições:**

- Quadro ChaChaPoly (algoritmo AEAD ChaCha20-Poly1305) máximo: 65535 bytes
- Poly1305 MAC (código de autenticação de mensagem): 16 bytes
- Máximo total de blocos: 65519 bytes (65535 - 16)
- Tamanho máximo de um único bloco: 65519 bytes (incluindo cabeçalho de 3 bytes)
- Tamanho máximo de dados de um único bloco: 65516 bytes

### Tipos de Bloco

**Tipos de Blocos Definidos:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Name</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Size</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Status</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Usage</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">DateTime</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">7 bytes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Implemented</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Required in NS</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1-3</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">-</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">-</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Future use</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Termination</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">9+ bytes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Unimplemented</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Session termination</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">5</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Options</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">21+ bytes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Unimplemented</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Session options</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">6</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">MessageNumbers</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">5 bytes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Unimplemented</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">PN value</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">7</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">NextKey</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">3 or 35 bytes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Implemented</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">DH ratchet</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">8</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ACK</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">4+ bytes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Implemented</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Message acknowledgment</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">9</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ACK Request</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">3 bytes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Implemented</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Request ACK</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">10</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">-</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">-</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Future use</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">11</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Garlic Clove</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Variable</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Implemented</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Application data</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">12-223</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">-</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">-</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Future use</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">224-253</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Experimental</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Variable</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">-</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Testing features</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">254</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Padding</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Variable</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Implemented</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Traffic shaping</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">255</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">-</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">-</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Future extension</td>
    </tr>
  </tbody>
</table>
**Tratamento de blocos desconhecidos:**

As implementações DEVEM ignorar blocos com números de tipo desconhecido e tratá-los como preenchimento. Isso garante compatibilidade futura.

### Regras de Ordenação de Blocos

### Ordenação de mensagens NS

**Obrigatório:** - O bloco DateTime DEVE ser o primeiro

**Permitidos:** - Garlic Clove (tipo 11) - Opções (tipo 5) - se implementado - Preenchimento (tipo 254)

**Proibidos:** - NextKey, ACK, ACK Request, Termination, MessageNumbers

**Exemplo de carga útil NS válida:**

```
DateTime (0) | Garlic Clove (11) | Garlic Clove (11) | Padding (254)
```
### Ordenação de mensagens do NSR

**Obrigatório:** - Nenhum (a carga útil pode estar vazia)

**Permitidos:** - Garlic Clove (unidade de mensagem do garlic encryption) (tipo 11) - Opções (tipo 5) - se implementado - Preenchimento (tipo 254)

**Proibidos:** - DateTime, NextKey, ACK, ACK Request, Termination, MessageNumbers

**Exemplo de carga útil NSR válida:**

```
Garlic Clove (11) | Garlic Clove (11) | Padding (254)
```
ou

```
(empty - ACK only)
```
### Ordenação de mensagens ES

**Obrigatório:** - Nenhum (a carga útil pode estar vazia)

**Permitidos (em qualquer ordem):** - Garlic Clove (submensagem do garlic encryption) (tipo 11) - NextKey (tipo 7) - ACK (tipo 8) - ACK Request (tipo 9) - Termination (tipo 4) - se implementado - MessageNumbers (tipo 6) - se implementado - Options (tipo 5) - se implementado - Padding (tipo 254)

**Regras Especiais:** - Termination DEVE ser o último bloco (exceto Padding) - Padding DEVE ser o último bloco - Múltiplos Garlic Cloves (submensagens) permitidos - Até 2 blocos NextKey permitidos (direto e reverso) - Múltiplos blocos Padding NÃO são permitidos

**Exemplos válidos de cargas úteis ES:**

```
Garlic Clove (11) | ACK (8) | Padding (254)
```
```
NextKey (7) | Garlic Clove (11) | Garlic Clove (11)
```
```
NextKey (7) forward | NextKey (7) reverse | Garlic Clove (11)
```
```
ACK Request (9) | Garlic Clove (11) | Termination (4) | Padding (254)
```
### DateTime Block (bloco de data e hora) (Tipo 0)

**Finalidade**: Carimbo de data/hora para prevenção de repetição e validação do desvio do relógio

**Tamanho**: 7 bytes (3 bytes de cabeçalho + 4 bytes de dados)

**Formato:**

```
+----+----+----+----+----+----+----+
| 0  |    4    |     timestamp     |
+----+----+----+----+----+----+----+
```
**Campos:**

- `blk`: 0
- `size`: 4 (big-endian, ordem de bytes com o mais significativo primeiro)
- `timestamp`: 4 bytes - carimbo de tempo Unix em segundos (sem sinal, big-endian)

**Formato do carimbo de data e hora:**

```python
timestamp = int(time.time())  # Seconds since 1970-01-01 00:00:00 UTC
# Wraps around in year 2106 (4-byte unsigned maximum)
```
**Regras de validação:**

```python
MAX_CLOCK_SKEW_PAST = 5 * 60      # 5 minutes
MAX_CLOCK_SKEW_FUTURE = 2 * 60    # 2 minutes

def validate_datetime(timestamp):
    now = int(time.time())
    age = now - timestamp
    
    if age < -MAX_CLOCK_SKEW_FUTURE:
        return False  # Too far in future
    
    if age > MAX_CLOCK_SKEW_PAST:
        return False  # Too old
    
    return True
```
**Prevenção de Repetição:**

```python
class ReplayFilter:
    def __init__(self, duration=5*60):
        self.duration = duration  # 5 minutes
        self.seen_messages = BloomFilter(size=100000, false_positive_rate=0.001)
        self.cleanup_timer = RepeatTimer(60, self.cleanup)
    
    def check_replay(self, ephemeral_key, timestamp):
        # Check timestamp validity
        if not validate_datetime(timestamp):
            return False
        
        # Check if ephemeral key seen recently
        if ephemeral_key in self.seen_messages:
            return False  # Replay attack
        
        # Add to seen messages
        self.seen_messages.add(ephemeral_key)
        return True
    
    def cleanup(self):
        # Expire old entries (Bloom filter automatically ages out)
        pass
```
**Notas de Implementação:**

1. **Mensagens NS**: DateTime DEVE ser o primeiro bloco
2. **Mensagens NSR/ES**: Normalmente, o DateTime não é incluído
3. **Janela de Replay**: 5 minutos é o mínimo recomendado
4. **Filtro de Bloom**: Recomendado para detecção eficiente de replay
5. **Desvio do Relógio**: Permitir 5 minutos no passado, 2 minutos no futuro

### Bloco de Dente de Alho (Tipo 11)

**Objetivo**: Encapsula mensagens I2NP para entrega

**Formato:**

```
+----+----+----+----+----+----+----+----+
| 11 |  size   |                        |
+----+----+----+                        +
|      Delivery Instructions            |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|type|  Message_ID       | Expiration  |
+----+----+----+----+----+----+----+----+
     |      I2NP Message body           |
+----+                                  +
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
```
**Campos:**

- `blk`: 11
- `size`: Tamanho total do clove (submensagem no I2P; variável)
- `Delivery Instructions`: Conforme a especificação do I2NP
- `type`: Tipo de mensagem I2NP (1 byte)
- `Message_ID`: ID da mensagem I2NP (4 bytes)
- `Expiration`: Timestamp Unix em segundos (4 bytes)
- `I2NP Message body`: Dados da mensagem de comprimento variável

**Formatos de instruções de entrega:**

**Entrega local** (1 byte):

```
+----+
|0x00|
+----+
```
**Entrega ao Destino** (33 bytes):

```
+----+----+----+----+----+----+----+----+
|0x01|                                  |
+----+        Destination Hash         +
|              32 bytes                 |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
```
**Entrega ao Router** (33 bytes):

```
+----+----+----+----+----+----+----+----+
|0x02|                                  |
+----+         Router Hash              +
|              32 bytes                 |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
```
**Entrega via Tunnel** (37 bytes):

```
+----+----+----+----+----+----+----+----+
|0x03|         Tunnel ID                |
+----+----+----+----+----+              +
|           Router Hash                 |
+              32 bytes                 +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
```
**Cabeçalho de Mensagem do I2NP** (9 bytes no total):

```
+----+----+----+----+----+----+----+----+
|type|      msg_id       |  expiration   |
+----+----+----+----+----+----+----+----+
     |                                   |
```
- `type`: tipo de mensagem I2NP (Database Store, Database Lookup, Data, etc.)
- `msg_id`: identificador de mensagem de 4 bytes
- `expiration`: timestamp Unix de 4 bytes (segundos)

**Diferenças importantes em relação ao ElGamal Clove Format (formato Clove do ElGamal):**

1. **Sem Certificado**: campo Certificate omitido (não utilizado em ElGamal)
2. **Sem Clove ID**: Clove ID omitido (Clove = submensagem em uma mensagem de garlic encryption; sempre foi 0)
3. **Sem Clove Expiration**: usa a expiração da mensagem I2NP em vez disso
4. **Cabeçalho compacto**: cabeçalho I2NP de 9 bytes em comparação com o formato ElGamal maior
5. **Cada Clove é um bloco separado**: sem a estrutura CloveSet

**Múltiplos Cloves (dentes de alho):**

```python
# Multiple Garlic Cloves in one message
payload = [
    build_datetime_block(),
    build_garlic_clove(i2np_message_1),
    build_garlic_clove(i2np_message_2),
    build_garlic_clove(i2np_message_3),
    build_padding_block()
]
```
**Tipos comuns de mensagens I2NP em Cloves (submensagens em garlic encryption):**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Name</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Usage</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">DatabaseStore</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Publishing LeaseSet</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">DatabaseLookup</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Requesting LeaseSet</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">5</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">DeliveryStatus</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ACK (legacy, avoid in ECIES)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">20</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Data</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Streaming data</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">21</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Garlic</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Nested garlic messages</td>
    </tr>
  </tbody>
</table>
**Processamento de Clove (submensagem dentro de uma mensagem de garlic encryption):**

```python
def process_garlic_clove(clove_data):
    # Parse delivery instructions
    delivery_type = clove_data[0]
    
    if delivery_type == 0x00:
        # Local delivery
        offset = 1
    elif delivery_type == 0x01:
        # Destination delivery
        dest_hash = clove_data[1:33]
        offset = 33
    elif delivery_type == 0x02:
        # Router delivery
        router_hash = clove_data[1:33]
        offset = 33
    elif delivery_type == 0x03:
        # Tunnel delivery
        tunnel_id = struct.unpack('>I', clove_data[1:5])[0]
        router_hash = clove_data[5:37]
        offset = 37
    
    # Parse I2NP header
    i2np_type = clove_data[offset]
    msg_id = struct.unpack('>I', clove_data[offset+1:offset+5])[0]
    expiration = struct.unpack('>I', clove_data[offset+5:offset+9])[0]
    
    # Extract I2NP body
    i2np_body = clove_data[offset+9:]
    
    # Process message
    process_i2np_message(i2np_type, msg_id, expiration, i2np_body)
```
### Bloco NextKey (chave seguinte) (Tipo 7)

**Objetivo**: troca de chaves via DH ratchet (mecanismo de avanço de Diffie-Hellman)

**Formato (Chave presente - 38 bytes):**

```
+----+----+----+----+----+----+----+----+
| 7  |   35    |flag|  key ID |         |
+----+----+----+----+----+----+         +
|                                       |
+     Next DH Ratchet Public Key        +
|              32 bytes                 |
+                                       +
|                                       |
+                             +----+----+
|                             |
+----+----+----+----+----+----+
```
**Formato (apenas ID da chave - 6 bytes):**

```
+----+----+----+----+----+----+
| 7  |    3    |flag|  key ID |
+----+----+----+----+----+----+
```
**Campos:**

- `blk`: 7
- `size`: 3 (apenas ID) ou 35 (com chave)
- `flag`: 1 byte - Bits de flag
- `key ID`: 2 bytes - Identificador de chave Big-endian (0-32767)
- `Public Key`: 32 bytes - Chave pública X25519 (little-endian), se o bit 0 de flag = 1

**Bits de sinalização:**

```
Bit 7 6 5 4 3 2 1 0
    | | | | | | | |
    | | | | | | | +-- Bit 0: Key present (1) or ID only (0)
    | | | | | | +---- Bit 1: Reverse key (1) or forward key (0)
    | | | | | +------ Bit 2: Request reverse key (1) or no request (0)
    | | | | |
    +-+-+-+-+-------- Bits 3-7: Reserved (set to 0)
```
**Exemplos de flags:**

```python
# Forward key present
flags = 0x01  # Binary: 00000001

# Reverse key present
flags = 0x03  # Binary: 00000011

# Forward key ID only (ACK)
flags = 0x00  # Binary: 00000000

# Reverse key ID only (ACK)
flags = 0x02  # Binary: 00000010

# Forward key ID with reverse request
flags = 0x04  # Binary: 00000100
```
**Regras de ID da chave:**

- IDs são sequenciais: 0, 1, 2, ..., 32767
- O ID só incrementa quando uma nova chave é gerada
- O mesmo ID é usado para várias mensagens até o próximo ratchet (mecanismo de avanço)
- O ID máximo é 32767 (é necessário iniciar uma nova sessão depois)

**Exemplos de uso:**

```python
# Initiating ratchet (sender generates new key)
nextkey = NextKeyBlock(
    flags=0x01,           # Key present, forward
    key_id=0,
    public_key=sender_new_pk
)

# Replying to ratchet (receiver generates new key)
nextkey = NextKeyBlock(
    flags=0x03,           # Key present, reverse
    key_id=0,
    public_key=receiver_new_pk
)

# Acknowledging ratchet (no new key from sender)
nextkey = NextKeyBlock(
    flags=0x02,           # ID only, reverse
    key_id=0
)

# Requesting reverse ratchet
nextkey = NextKeyBlock(
    flags=0x04,           # Request reverse, forward ID
    key_id=1
)
```
**Lógica de processamento:**

```python
def process_nextkey_block(block):
    flags = block.flags
    key_id = block.key_id
    
    key_present = (flags & 0x01) != 0
    is_reverse = (flags & 0x02) != 0
    request_reverse = (flags & 0x04) != 0
    
    if key_present:
        public_key = block.public_key
        
        if is_reverse:
            # Reverse key received
            perform_dh_ratchet(receiver_key=public_key, key_id=key_id)
            # Sender should ACK with own key ID
        else:
            # Forward key received
            perform_dh_ratchet(sender_key=public_key, key_id=key_id)
            # Receiver should reply with reverse key
            send_reverse_key(generate_new_key())
    
    else:
        # Key ID only (ACK)
        if is_reverse:
            # Reverse key ACK
            confirm_reverse_ratchet(key_id)
        else:
            # Forward key ACK
            confirm_forward_ratchet(key_id)
    
    if request_reverse:
        # Sender requests receiver to generate new key
        send_reverse_key(generate_new_key())
```
**Múltiplos NextKey Blocks:**

Uma única ES message (mensagem do tipo ES) pode conter até 2 NextKey blocks (blocos NextKey) quando ambas as direções estiverem realizando ratcheting (avanço de chaves) simultaneamente:

```python
# Both directions ratcheting
payload = [
    NextKeyBlock(flags=0x01, key_id=2, public_key=forward_key),  # Forward
    NextKeyBlock(flags=0x03, key_id=1, public_key=reverse_key),  # Reverse
    build_garlic_clove(data)
]
```
### Bloco ACK (Tipo 8)

**Objetivo**: Acusar o recebimento de mensagens no mesmo canal

**Formato (ACK único - 7 bytes):**

```
+----+----+----+----+----+----+----+
| 8  |    4    |tagsetid |   N     |
+----+----+----+----+----+----+----+
```
**Formato (múltiplos ACKs):**

```
+----+----+----+----+----+----+----+----+
| 8  |  size   |tagsetid |   N     |    |
+----+----+----+----+----+----+----+    +
|            more ACKs                  |
~               ...                     ~
|                                       |
+----+----+----+----+----+----+----+----+
```
**Campos:**

- `blk`: 8
- `size`: 4 * número de ACKs (mínimo 4)
- Para cada ACK:
  - `tagsetid`: 2 bytes - ID do conjunto de tags em big-endian (0-65535)
  - `N`: 2 bytes - número da mensagem em big-endian (0-65535)

**Determinação do ID do conjunto de tags:**

```python
# Tag set 0 (initial, after NSR)
tagset_id = 0

# After first ratchet (tag set 1)
# Both Alice and Bob sent key ID 0
tagset_id = 1 + 0 + 0 = 1

# After second ratchet (tag set 2)
# Alice sent key ID 1, Bob still using key ID 0
tagset_id = 1 + 1 + 0 = 2

# After third ratchet (tag set 3)
# Alice still using key ID 1, Bob sent key ID 1
tagset_id = 1 + 1 + 1 = 3
```
**Exemplo de ACK (confirmação) único:**

```python
# ACK message from tag set 5, message number 127
ack_block = ACKBlock(
    tagset_id=5,
    message_number=127
)

# Wire format (7 bytes):
# 08 00 04 00 05 00 7F
# |  |  |  |  |  |  |
# |  |  |  |  |  |  +-- N (127)
# |  |  |  |  +--------- N high byte
# |  |  |  +------------ tagset_id (5)
# |  |  +--------------- tagset_id high byte
# |  +------------------ size (4)
# +--------------------- type (8)
```
**Exemplo de múltiplos ACKs (confirmações):**

```python
# ACK three messages
ack_block = ACKBlock([
    (tagset_id=3, N=42),
    (tagset_id=3, N=43),
    (tagset_id=4, N=0)
])

# Wire format (15 bytes):
# 08 00 0C 00 03 00 2A 00 03 00 2B 00 04 00 00
#                (ts=3, N=42) (ts=3, N=43) (ts=4, N=0)
```
**Processamento:**

```python
def process_ack_block(block):
    num_acks = block.size // 4
    
    for i in range(num_acks):
        offset = i * 4
        tagset_id = struct.unpack('>H', block.data[offset:offset+2])[0]
        message_num = struct.unpack('>H', block.data[offset+2:offset+4])[0]
        
        # Mark message as acknowledged
        mark_acked(tagset_id, message_num)
        
        # May trigger retransmission timeout cancellation
        cancel_retransmit_timer(tagset_id, message_num)
```
**Quando enviar ACKs (confirmações):**

1. **Solicitação explícita de ACK**: Sempre responder ao bloco de Solicitação de ACK
2. **Entrega de LeaseSet**: Quando o remetente inclui o LeaseSet na mensagem
3. **Estabelecimento de sessão**: Pode enviar ACK de NS/NSR (embora o protocolo prefira ACK implícito via ES)
4. **Confirmação do ratchet (mecanismo de avanço criptográfico)**: Pode enviar ACK do recebimento de NextKey
5. **Camada de aplicação**: Conforme exigido pelo protocolo da camada superior (por exemplo, Streaming)

**Temporização de ACK:**

```python
class ACKManager:
    def __init__(self):
        self.pending_acks = []
        self.ack_timer = None
    
    def request_ack(self, tagset_id, message_num):
        self.pending_acks.append((tagset_id, message_num))
        
        if not self.ack_timer:
            # Delay ACK briefly to allow higher layer to respond
            self.ack_timer = set_timer(0.1, self.send_acks)  # 100ms
    
    def send_acks(self):
        if self.pending_acks and not has_outbound_data():
            # No higher layer data, send explicit ACK
            send_es_message(build_ack_block(self.pending_acks))
        
        # Otherwise, ACK will piggyback on next ES message
        self.pending_acks = []
        self.ack_timer = None
```
### Bloco de Solicitação de ACK (Tipo 9)

**Finalidade**: Solicitar confirmação em banda do recebimento da mensagem atual

**Formato:**

```
+----+----+----+----+
| 9  |    1    |flg |
+----+----+----+----+
```
**Campos:**

- `blk`: 9
- `size`: 1
- `flg`: 1 byte - Sinalizadores (todos os bits atualmente não utilizados, definidos como 0)

**Uso:**

```python
# Request ACK for this message
payload = [
    build_ack_request_block(),
    build_garlic_clove(important_data)
]
```
**Resposta do receptor:**

Quando um ACK Request (pedido de ACK) é recebido:

1. **Com dados imediatos**: Incluir bloco ACK na resposta imediata
2. **Sem dados imediatos**: Iniciar um temporizador (por exemplo, 100 ms) e enviar ES vazio com ACK se o temporizador expirar
3. **Tag Set ID**: Usar o ID do conjunto de tags de entrada atual
4. **Número da mensagem**: Usar o número da mensagem associado à tag de sessão recebida

**Processamento:**

```python
def process_ack_request(message):
    # Extract message identification
    tagset_id = message.tagset_id
    message_num = message.message_num
    
    # Schedule ACK
    schedule_ack(tagset_id, message_num)
    
    # If no data to send immediately, start timer
    if not has_pending_data():
        set_timer(0.1, lambda: send_ack_only(tagset_id, message_num))
```
**Quando usar o ACK Request:**

1. **Mensagens Críticas**: Mensagens que devem ser confirmadas
2. **Entrega de LeaseSet**: Ao agrupar um LeaseSet
3. **Session Ratchet (mecanismo de avanço da sessão)**: Após enviar o bloco NextKey
4. **Fim da Transmissão**: Quando o remetente não tem mais dados para enviar, mas deseja confirmação

**Quando NÃO usar:**

1. **Protocolo de Streaming**: A camada de streaming lida com ACKs (confirmações)
2. **Mensagens de alta frequência**: Evite solicitação de ACK em cada mensagem (sobrecarga)
3. **Datagramas sem importância**: Datagramas brutos normalmente não precisam de ACKs

### Bloco de Terminação (Tipo 4)

**Estado**: NÃO IMPLEMENTADO

**Finalidade**: Encerrar a sessão de forma limpa

**Formato:**

```
+----+----+----+----+----+----+----+----+
| 4  |  size   | rsn|     addl data     |
+----+----+----+----+                   +
~               ...                     ~
+----+----+----+----+----+----+----+----+
```
**Campos:**

- `blk`: 4
- `size`: 1 ou mais bytes
- `rsn`: 1 byte - código do motivo
- `addl data`: Dados adicionais opcionais (o formato depende do motivo)

**Códigos de motivo:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Code</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Meaning</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Additional Data</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Normal close / unspecified</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">None</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Termination received</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">None</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Idle timeout</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">None (implementation-specific)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Resource exhaustion</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">None (implementation-specific)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4+</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Implementation-specific</td>
    </tr>
  </tbody>
</table>
**Uso (quando estiver implementado):**

```python
# Normal session close
termination = TerminationBlock(
    reason=0,
    additional_data=b''
)

# Session termination due to received termination
termination = TerminationBlock(
    reason=1,
    additional_data=b''
)
```
**Regras:**

- DEVE ser o último bloco, exceto por Padding (preenchimento)
- Padding DEVE seguir Termination (finalização) se presente
- Não é permitido em mensagens NS ou NSR
- Apenas é permitido em mensagens ES

### Bloco de Opções (Tipo 5)

**Status**: NÃO IMPLEMENTADO

**Objetivo**: Negociar parâmetros de sessão

**Formato:**

```
+----+----+----+----+----+----+----+----+
| 5  |  size   |ver |flg |STL |STimeout |
+----+----+----+----+----+----+----+----+
|  SOTW   |  RITW   |tmin|tmax|rmin|rmax|
+----+----+----+----+----+----+----+----+
|  tdmy   |  rdmy   |  tdelay |  rdelay |
+----+----+----+----+----+----+----+----+
|              more_options             |
~               ...                     ~
|                                       |
+----+----+----+----+----+----+----+----+
```
**Campos:**

- `blk`: 5
- `size`: 21 bytes ou mais
- `ver`: 1 byte - Versão do protocolo (deve ser 0)
- `flg`: 1 byte - Flags (todos os bits atualmente não utilizados)
- `STL`: 1 byte - Comprimento da tag de sessão (deve ser 8)
- `STimeout`: 2 bytes - Tempo limite de inatividade da sessão em segundos (big-endian)
- `SOTW`: 2 bytes - Janela de Tags de Saída do Remetente (big-endian)
- `RITW`: 2 bytes - Janela de Tags de Entrada do Receptor (big-endian)
- `tmin`, `tmax`, `rmin`, `rmax`: 1 byte cada - Parâmetros de preenchimento (ponto fixo 4.4)
- `tdmy`: 2 bytes - Tráfego fictício máximo que está disposto a enviar (bytes/sec, big-endian)
- `rdmy`: 2 bytes - Tráfego fictício solicitado (bytes/sec, big-endian)
- `tdelay`: 2 bytes - Atraso intra-mensagem máximo que está disposto a inserir (msec, big-endian)
- `rdelay`: 2 bytes - Atraso intra-mensagem solicitado (msec, big-endian)
- `more_options`: Variável - Extensões futuras

**Parâmetros de Preenchimento (4.4 em ponto fixo):**

```python
def encode_padding_ratio(ratio):
    """
    Encode padding ratio as 4.4 fixed-point
    
    ratio: 0.0 to 15.9375
    returns: 0x00 to 0xFF
    """
    return int(ratio * 16)

def decode_padding_ratio(encoded):
    """
    Decode 4.4 fixed-point to ratio
    
    encoded: 0x00 to 0xFF
    returns: 0.0 to 15.9375
    """
    return encoded / 16.0

# Examples:
# 0x00 = 0.0 (no padding)
# 0x01 = 0.0625 (6.25% padding)
# 0x10 = 1.0 (100% padding - double traffic)
# 0x80 = 8.0 (800% padding - 9x traffic)
# 0xFF = 15.9375 (1593.75% padding)
```
**Negociação da Janela de Tags:**

```python
# SOTW: Sender's recommendation for receiver's inbound window
# RITW: Sender's declaration of own inbound window

# Receiver calculates actual inbound window:
inbound_window = calculate_window(
    sender_suggestion=SOTW,
    own_constraints=MAX_INBOUND_TAGS,
    own_resources=available_memory()
)

# Sender uses:
# - RITW to know how far ahead receiver will accept
# - Own SOTW to hint optimal window size
```
**Valores padrão (quando as opções não são negociadas):**

```python
DEFAULT_OPTIONS = {
    'version': 0,
    'session_tag_length': 8,
    'session_timeout': 600,  # 10 minutes
    'sender_outbound_tag_window': 160,
    'receiver_inbound_tag_window': 160,
    'tmin': 0x00,  # No minimum padding
    'tmax': 0x10,  # Up to 100% padding
    'rmin': 0x00,  # No minimum requested
    'rmax': 0x10,  # Up to 100% requested
    'tdmy': 0,     # No dummy traffic
    'rdmy': 0,     # No dummy traffic requested
    'tdelay': 0,   # No delay
    'rdelay': 0    # No delay requested
}
```
### Bloco de Números de Mensagem (Tipo 6)

**Status**: NÃO IMPLEMENTADO

**Objetivo**: Indicar a última mensagem enviada no conjunto de tags anterior (permite detecção de lacunas)

**Formato:**

```
+----+----+----+----+----+
| 6  |    2    |  PN    |
+----+----+----+----+----+
```
**Campos:**

- `blk`: 6
- `size`: 2
- `PN`: 2 bytes - Número da última mensagem do conjunto de tags anterior (big-endian (ordem de bytes com o mais significativo primeiro), 0-65535)

**Definição de PN (Previous Number, número anterior):**

PN é o índice da última tag enviada no conjunto de tags anterior.

**Uso (quando implementado):**

```python
# After ratcheting to new tag set
# Old tag set: sent messages 0-4095
# New tag set: sending first message

payload = [
    MessageNumbersBlock(PN=4095),
    build_garlic_clove(data)
]
```
**Benefícios para o receptor:**

```python
def process_message_numbers(pn_value):
    # Receiver can now:
    
    # 1. Determine if any messages were skipped
    highest_received_in_old_tagset = 4090
    if pn_value > highest_received_in_old_tagset:
        missing_count = pn_value - highest_received_in_old_tagset
        # 5 messages were never received
    
    # 2. Delete tags higher than PN from old tagset
    for tag_index in range(pn_value + 1, MAX_TAG_INDEX):
        delete_tag(old_tagset, tag_index)
    
    # 3. Expire tags ≤ PN after grace period (e.g., 2 minutes)
    schedule_deletion(old_tagset, delay=120)
```
**Regras:**

- NÃO DEVE ser enviado no tag set (conjunto de tags) 0 (sem tag set anterior)
- Enviado apenas em ES messages (mensagens ES)
- Enviado apenas nas primeiras mensagens de um novo tag set
- PN value (valor PN) é do ponto de vista do remetente (último tag (etiqueta) enviado pelo remetente)

**Relação com o Signal:**

No Signal Double Ratchet (protocolo de troca de chaves Double Ratchet do Signal), o PN está no cabeçalho da mensagem. No ECIES (Esquema de Criptografia Integrada baseado em Curvas Elípticas), o PN fica na carga útil criptografada e é opcional.

### Bloco de preenchimento (Tipo 254)

**Objetivo**: Resistência à análise de tráfego e ofuscação do tamanho das mensagens

**Formato:**

```
+----+----+----+----+----+----+----+----+
|254 |  size   |      padding           |
+----+----+----+                        +
|                                       |
~               ...                     ~
|                                       |
+----+----+----+----+----+----+----+----+
```
**Campos:**

- `blk`: 254
- `size`: 0-65516 bytes (big-endian, ordem de bytes com o mais significativo primeiro)
- `padding`: Dados aleatórios ou zerados

**Regras:**

- DEVE ser o último bloco na mensagem
- Múltiplos blocos de preenchimento NÃO são permitidos
- Pode ter comprimento zero (apenas cabeçalho de 3 bytes)
- Os dados de preenchimento podem ser zeros ou bytes aleatórios

**Preenchimento padrão:**

```python
DEFAULT_PADDING_MIN = 0
DEFAULT_PADDING_MAX = 15

def generate_default_padding():
    size = random.randint(DEFAULT_PADDING_MIN, DEFAULT_PADDING_MAX)
    data = random.bytes(size)  # or zeros
    return PaddingBlock(size, data)
```
**Estratégias de resistência à análise de tráfego:**

**Estratégia 1: Tamanho aleatório (Padrão)**

```python
# Add 0-15 bytes random padding to each message
padding_size = random.randint(0, 15)
padding_block = PaddingBlock(padding_size, random.bytes(padding_size))
```
**Estratégia 2: Arredondar para um múltiplo**

```python
# Round total message size to next multiple of 64
target_size = ((message_size + 63) // 64) * 64
padding_size = target_size - message_size - 3  # -3 for block header
padding_block = PaddingBlock(padding_size, random.bytes(padding_size))
```
**Estratégia 3: Tamanhos Fixos de Mensagens**

```python
# Always send 1KB messages
TARGET_MESSAGE_SIZE = 1024
padding_size = TARGET_MESSAGE_SIZE - message_size - 3
padding_block = PaddingBlock(padding_size, random.bytes(padding_size))
```
**Estratégia 4: Preenchimento Negociado (bloco de opções)**

```python
# Calculate padding based on negotiated parameters
# tmin, tmax from Options block
min_padding = int(payload_size * tmin_ratio)
max_padding = int(payload_size * tmax_ratio)
padding_size = random.randint(min_padding, max_padding)
padding_block = PaddingBlock(padding_size, random.bytes(padding_size))
```
**Mensagens apenas de preenchimento:**

As mensagens podem consistir inteiramente de preenchimento (sem dados de aplicação):

```python
# Dummy traffic message
payload = [
    PaddingBlock(random.randint(100, 500), random.bytes(...))
]
```
**Notas de implementação:**

1. **Preenchimento com zeros**: Aceitável (será criptografado por ChaCha20)
2. **Preenchimento aleatório**: Não oferece segurança adicional após a criptografia, mas usa mais entropia
3. **Desempenho**: A geração de preenchimento aleatório pode ser custosa; considere usar zeros
4. **Memória**: Blocos grandes de preenchimento consomem largura de banda; seja cauteloso com o tamanho máximo

---

## Guia de Implementação

### Pré-requisitos

**Bibliotecas criptográficas:**

- **X25519**: libsodium, NaCl ou Bouncy Castle
- **ChaCha20-Poly1305**: libsodium, OpenSSL 1.1.0+ ou Bouncy Castle
- **SHA-256**: OpenSSL, Bouncy Castle ou suporte nativo da linguagem
- **Elligator2** (técnica para ocultar pontos de curva elíptica): Suporte limitado em bibliotecas; pode exigir implementação personalizada

**Implementação do Elligator2 (técnica criptográfica para mapear pontos de curva elíptica para dados indistinguíveis de aleatórios):**

O Elligator2 (método criptográfico para camuflar chaves públicas como dados aleatórios) não é amplamente implementado. Opções:

1. **OBFS4**: O transporte plugável obfs4 do Tor inclui uma implementação do Elligator2 (técnica para disfarçar chaves públicas em curvas elípticas)
2. **Implementação personalizada**: Baseada no [artigo Elligator2](https://elligator.cr.yp.to/elligator-20130828.pdf)
3. **kleshni/Elligator**: Implementação de referência no GitHub

**Nota do Java I2P:** O Java I2P usa a biblioteca net.i2p.crypto.eddsa com adições personalizadas de Elligator2 (técnica de hashing para curvas elípticas).

### Ordem de Implementação Recomendada

**Fase 1: Criptografia Essencial** 1. geração e troca de chaves DH X25519 2. cifragem/decifragem AEAD ChaCha20-Poly1305 3. hash SHA-256 e MixHash (operação de mistura de hash) 4. derivação de chaves HKDF 5. codificação/decodificação Elligator2 (pode usar vetores de teste inicialmente)

**Fase 2: Formatos de Mensagem** 1. Mensagem NS (não vinculada) - formato mais simples 2. Mensagem NS (vinculada) - adiciona chave estática 3. Mensagem NSR 4. Mensagem ES 5. Análise e geração de blocos

**Fase 3: Gerenciamento de Sessão** 1. Criação e armazenamento da sessão 2. Gerenciamento do conjunto de tags (remetente e destinatário) 3. Ratchet de tag de sessão (mecanismo de avanço criptográfico) 4. Ratchet de chave simétrica 5. Busca de tags e gerenciamento de janela

**Fase 4: DH Ratcheting (mecanismo de catraca DH)** 1. Tratamento do bloco NextKey 2. KDF do DH ratchet 3. Criação do conjunto de tags após a catraca 4. Gerenciamento de múltiplos conjuntos de tags

**Fase 5: Lógica do Protocolo** 1. Máquina de estados NS/NSR/ES 2. Prevenção de replay (DateTime, filtro de Bloom) 3. Lógica de retransmissão (múltiplos NS/NSR) 4. Tratamento de ACK

**Fase 6: Integração** 1. Processamento de I2NP Garlic Clove (dente de alho no contexto do I2P) 2. Empacotamento de LeaseSet 3. Integração do protocolo de streaming 4. Integração do protocolo de datagrama

### Implementação do Remetente

**Ciclo de Vida da Sessão de Saída:**

```python
class OutboundSession:
    def __init__(self, destination, bound=True):
        self.destination = destination
        self.bound = bound
        self.state = SessionState.NEW
        
        # Keys for NS message
        self.ephemeral_keypair = generate_elg2_keypair()
        if bound:
            self.static_key = context.static_keypair
        
        # Will be populated after NSR
        self.outbound_tagset = None
        self.outbound_keyratchet = None
        self.inbound_tagset = None
        self.inbound_keyratchet = None
        
        # Timing
        self.created_time = now()
        self.last_activity = now()
        
        # Retransmission
        self.ns_attempts = []
        self.ns_timer = None
    
    def send_initial_message(self, payload):
        """Send NS message"""
        # Build NS message
        ns_message = self.build_ns_message(payload)
        
        # Send
        send_to_network(self.destination, ns_message)
        
        # Track for retransmission
        self.ns_attempts.append({
            'message': ns_message,
            'time': now(),
            'ephemeral_key': self.ephemeral_keypair,
            'kdf_state': self.save_kdf_state()
        })
        
        # Start timer
        self.ns_timer = set_timer(1.0, self.on_ns_timeout)
        self.state = SessionState.PENDING_REPLY
    
    def build_ns_message(self, payload):
        """Construct NS message"""
        # KDF initialization
        chainKey, h = self.initialize_kdf()
        
        # Ephemeral key section
        elg2_ephemeral = ENCODE_ELG2(self.ephemeral_keypair.public_key)
        h = SHA256(h || self.destination.static_key)
        h = SHA256(h || self.ephemeral_keypair.public_key)
        
        # es DH
        es_shared = DH(self.ephemeral_keypair.private_key, 
                       self.destination.static_key)
        keydata = HKDF(chainKey, es_shared, "", 64)
        chainKey = keydata[0:31]
        k_static = keydata[32:63]
        
        # Encrypt static key section
        if self.bound:
            static_section = self.static_key.public_key
        else:
            static_section = bytes(32)
        
        static_ciphertext = ENCRYPT(k_static, 0, static_section, h)
        h = SHA256(h || static_ciphertext)
        
        # ss DH (if bound)
        if self.bound:
            ss_shared = DH(self.static_key.private_key, 
                          self.destination.static_key)
            keydata = HKDF(chainKey, ss_shared, "", 64)
            chainKey = keydata[0:31]
            k_payload = keydata[32:63]
            nonce = 0
        else:
            k_payload = k_static
            nonce = 1
        
        # Build payload blocks
        payload_data = self.build_ns_payload(payload)
        
        # Encrypt payload
        payload_ciphertext = ENCRYPT(k_payload, nonce, payload_data, h)
        h = SHA256(h || payload_ciphertext)
        
        # Save KDF state for NSR processing
        self.ns_chainkey = chainKey
        self.ns_hash = h
        
        # Assemble message
        return elg2_ephemeral + static_ciphertext + payload_ciphertext
    
    def build_ns_payload(self, application_data):
        """Build NS payload blocks"""
        blocks = []
        
        # DateTime block (required, first)
        blocks.append(build_datetime_block())
        
        # Garlic Clove(s) with application data
        blocks.append(build_garlic_clove(application_data))
        
        # Optionally bundle LeaseSet
        if should_send_leaseset():
            blocks.append(build_garlic_clove(build_leaseset_store()))
        
        # Padding
        blocks.append(build_padding_block(random.randint(0, 15)))
        
        return encode_blocks(blocks)
    
    def on_nsr_received(self, nsr_message):
        """Process NSR and establish ES session"""
        # Cancel retransmission timer
        cancel_timer(self.ns_timer)
        
        # Parse NSR
        tag = nsr_message[0:8]
        elg2_bob_ephemeral = nsr_message[8:40]
        key_section_mac = nsr_message[40:56]
        payload_ciphertext = nsr_message[56:]
        
        # Find corresponding NS attempt
        ns_state = self.find_ns_by_tag(tag)
        if not ns_state:
            raise ValueError("NSR tag doesn't match any NS")
        
        # Restore KDF state
        chainKey = ns_state['chainkey']
        h = ns_state['hash']
        
        # Decode Bob's ephemeral key
        bob_ephemeral = DECODE_ELG2(elg2_bob_ephemeral)
        
        # Mix tag and Bob's ephemeral into hash
        h = SHA256(h || tag)
        h = SHA256(h || bob_ephemeral)
        
        # ee DH
        ee_shared = DH(self.ephemeral_keypair.private_key, bob_ephemeral)
        keydata = HKDF(chainKey, ee_shared, "", 32)
        chainKey = keydata[0:31]
        
        # se DH
        se_shared = DH(self.static_key.private_key, bob_ephemeral)
        keydata = HKDF(chainKey, se_shared, "", 64)
        chainKey = keydata[0:31]
        k_key_section = keydata[32:63]
        
        # Verify key section MAC
        try:
            DECRYPT(k_key_section, 0, key_section_mac, h)
        except AuthenticationError:
            raise ValueError("NSR key section MAC verification failed")
        
        h = SHA256(h || key_section_mac)
        
        # Split for bidirectional ES
        keydata = HKDF(chainKey, ZEROLEN, "", 64)
        k_ab = keydata[0:31]  # Alice → Bob
        k_ba = keydata[32:63]  # Bob → Alice
        
        # Initialize ES tagsets
        self.outbound_tagset = DH_INITIALIZE(chainKey, k_ab)
        self.inbound_tagset = DH_INITIALIZE(chainKey, k_ba)
        
        # Decrypt NSR payload
        k_nsr = HKDF(k_ba, ZEROLEN, "AttachPayloadKDF", 32)
        try:
            payload = DECRYPT(k_nsr, 0, payload_ciphertext, h)
        except AuthenticationError:
            raise ValueError("NSR payload MAC verification failed")
        
        # Process NSR payload blocks
        self.process_payload_blocks(payload)
        
        # Session established
        self.state = SessionState.ESTABLISHED
        self.last_activity = now()
        
        # Send ES message (implicit ACK)
        self.send_es_ack()
    
    def send_es_message(self, payload):
        """Send ES message"""
        if self.state != SessionState.ESTABLISHED:
            raise ValueError("Session not established")
        
        # Get next tag and key
        tag, index = self.outbound_tagset.get_next_tag()
        key = self.outbound_keyratchet.get_key(index)
        
        # Construct nonce
        nonce = construct_nonce(index)
        
        # Build payload blocks
        payload_data = self.build_es_payload(payload)
        
        # AEAD encryption
        ciphertext = ENCRYPT(key, nonce, payload_data, tag)
        
        # Assemble message
        es_message = tag + ciphertext
        
        # Send
        send_to_network(self.destination, es_message)
        
        # Update activity
        self.last_activity = now()
        
        # Check if ratchet needed
        if self.outbound_tagset.should_ratchet():
            self.initiate_ratchet()
```
### Implementação do receptor

**Ciclo de Vida da Sessão de Entrada:**

```python
class InboundSession:
    def __init__(self):
        self.state = None
        self.bound = False
        self.destination = None
        
        # Keys
        self.remote_ephemeral_key = None
        self.remote_static_key = None
        self.ephemeral_keypair = None
        
        # Tagsets
        self.inbound_tagset = None
        self.outbound_tagset = None
        
        # Timing
        self.created_time = None
        self.last_activity = None
        
        # Paired session
        self.paired_outbound = None
    
    @staticmethod
    def try_decrypt_ns(message):
        """Attempt to decrypt as NS message"""
        # Parse NS structure
        elg2_ephemeral = message[0:32]
        static_ciphertext = message[32:80]  # 32 + 16
        payload_ciphertext = message[80:]
        
        # Decode ephemeral key
        try:
            alice_ephemeral = DECODE_ELG2(elg2_ephemeral)
        except:
            return None  # Not a valid Elligator2 encoding
        
        # Check replay
        if is_replay(alice_ephemeral):
            return None
        
        # KDF initialization
        chainKey, h = initialize_kdf()
        
        # Mix keys
        h = SHA256(h || context.static_keypair.public_key)
        h = SHA256(h || alice_ephemeral)
        
        # es DH
        es_shared = DH(context.static_keypair.private_key, alice_ephemeral)
        keydata = HKDF(chainKey, es_shared, "", 64)
        chainKey = keydata[0:31]
        k_static = keydata[32:63]
        
        # Decrypt static key section
        try:
            static_data = DECRYPT(k_static, 0, static_ciphertext, h)
        except AuthenticationError:
            return None  # Not a valid NS message
        
        h = SHA256(h || static_ciphertext)
        
        # Check if bound or unbound
        if static_data == bytes(32):
            # Unbound
            alice_static_key = None
            k_payload = k_static
            nonce = 1
        else:
            # Bound - perform ss DH
            alice_static_key = static_data
            ss_shared = DH(context.static_keypair.private_key, alice_static_key)
            keydata = HKDF(chainKey, ss_shared, "", 64)
            chainKey = keydata[0:31]
            k_payload = keydata[32:63]
            nonce = 0
        
        # Decrypt payload
        try:
            payload = DECRYPT(k_payload, nonce, payload_ciphertext, h)
        except AuthenticationError:
            return None
        
        h = SHA256(h || payload_ciphertext)
        
        # Create session
        session = InboundSession()
        session.state = SessionState.ESTABLISHED
        session.created_time = now()
        session.last_activity = now()
        session.remote_ephemeral_key = alice_ephemeral
        session.remote_static_key = alice_static_key
        session.bound = (alice_static_key is not None)
        session.ns_chainkey = chainKey
        session.ns_hash = h
        
        # Extract destination if bound
        if session.bound:
            session.destination = extract_destination_from_payload(payload)
        
        # Process payload
        session.process_payload_blocks(payload)
        
        return session
    
    def send_nsr_reply(self, reply_payload):
        """Send NSR message"""
        # Generate NSR tagset
        tagsetKey = HKDF(self.ns_chainkey, ZEROLEN, "SessionReplyTags", 32)
        nsr_tagset = DH_INITIALIZE(self.ns_chainkey, tagsetKey)
        
        # Get tag
        tag, _ = nsr_tagset.get_next_tag()
        
        # Mix tag into hash
        h = SHA256(self.ns_hash || tag)
        
        # Generate ephemeral key
        self.ephemeral_keypair = generate_elg2_keypair()
        bob_ephemeral = self.ephemeral_keypair.public_key
        elg2_bob_ephemeral = ENCODE_ELG2(bob_ephemeral)
        
        # Mix ephemeral key
        h = SHA256(h || bob_ephemeral)
        
        chainKey = self.ns_chainkey
        
        # ee DH
        ee_shared = DH(self.ephemeral_keypair.private_key, 
                      self.remote_ephemeral_key)
        keydata = HKDF(chainKey, ee_shared, "", 32)
        chainKey = keydata[0:31]
        
        # se DH
        se_shared = DH(context.static_keypair.private_key, 
                      self.remote_ephemeral_key)
        keydata = HKDF(chainKey, se_shared, "", 64)
        chainKey = keydata[0:31]
        k_key_section = keydata[32:63]
        
        # Encrypt key section (empty)
        key_section_ciphertext = ENCRYPT(k_key_section, 0, ZEROLEN, h)
        h = SHA256(h || key_section_ciphertext)
        
        # Split for bidirectional ES
        keydata = HKDF(chainKey, ZEROLEN, "", 64)
        k_ab = keydata[0:31]  # Alice → Bob
        k_ba = keydata[32:63]  # Bob → Alice
        
        # Initialize ES tagsets
        self.inbound_tagset = DH_INITIALIZE(chainKey, k_ab)
        self.outbound_tagset = DH_INITIALIZE(chainKey, k_ba)
        
        # Build reply payload
        payload_data = build_payload_blocks(reply_payload)
        
        # Encrypt payload
        k_nsr = HKDF(k_ba, ZEROLEN, "AttachPayloadKDF", 32)
        payload_ciphertext = ENCRYPT(k_nsr, 0, payload_data, h)
        
        # Assemble NSR
        nsr_message = tag + elg2_bob_ephemeral + key_section_ciphertext + payload_ciphertext
        
        # Send
        send_to_network(self.destination, nsr_message)
        
        # Wait for ES
        self.state = SessionState.AWAITING_ES
        self.last_activity = now()
    
    def on_es_received(self, es_message):
        """Process first ES message"""
        if self.state == SessionState.AWAITING_ES:
            # First ES received, confirms session
            self.state = SessionState.ESTABLISHED
        
        # Process ES message
        self.process_es_message(es_message)
    
    def process_es_message(self, es_message):
        """Decrypt and process ES message"""
        # Extract tag
        tag = es_message[0:8]
        ciphertext = es_message[8:]
        
        # Look up tag
        index = self.inbound_tagset.lookup_tag(tag)
        if index is None:
            raise ValueError("Tag not found")
        
        # Get key
        key = self.inbound_keyratchet.get_key(index)
        
        # Construct nonce
        nonce = construct_nonce(index)
        
        # Decrypt
        try:
            payload = DECRYPT(key, nonce, ciphertext, tag)
        except AuthenticationError:
            raise ValueError("ES MAC verification failed")
        
        # Process blocks
        self.process_payload_blocks(payload)
        
        # Update activity
        self.last_activity = now()
```
### Classificação de mensagens

**Diferenciando Tipos de Mensagem:**

```python
def classify_message(message):
    """Determine message type"""
    
    # Minimum lengths
    if len(message) < 24:
        return None  # Too short
    
    # Check for session tag (8 bytes)
    tag = message[0:8]
    
    # Try ES decryption first (most common)
    session = lookup_session_by_tag(tag)
    if session:
        return ('ES', session)
    
    # Try NSR decryption (tag + Elligator2 key)
    if len(message) >= 72:
        # Check if bytes 8-40 are valid Elligator2
        try:
            nsr_ephemeral = DECODE_ELG2(message[8:40])
            nsr_session = find_pending_nsr_by_tag(tag)
            if nsr_session:
                return ('NSR', nsr_session)
        except:
            pass
    
    # Try NS decryption (starts with Elligator2 key)
    if len(message) >= 96:
        try:
            ns_ephemeral = DECODE_ELG2(message[0:32])
            ns_session = InboundSession.try_decrypt_ns(message)
            if ns_session:
                return ('NS', ns_session)
        except:
            pass
    
    # Check ElGamal/AES (for dual-key compatibility)
    if len(message) >= 514:
        if (len(message) - 2) % 16 == 0:
            # Might be ElGamal NS
            return ('ELGAMAL_NS', None)
        elif len(message) % 16 == 0:
            # Might be ElGamal ES
            return ('ELGAMAL_ES', None)
    
    return None  # Unknown message type
```
### Boas práticas de gerenciamento de sessões

**Armazenamento de sessão:**

```python
class SessionKeyManager:
    def __init__(self):
        # Outbound sessions (one per destination)
        self.outbound_sessions = {}  # destination -> OutboundSession
        
        # Inbound sessions (multiple per destination during transition)
        self.inbound_sessions = []  # [InboundSession]
        
        # Session tag lookup (fast path for ES messages)
        self.tag_to_session = {}  # tag -> InboundSession
        
        # Limits
        self.max_inbound_sessions = 1000
        self.max_tags_per_session = 160
    
    def get_outbound_session(self, destination):
        """Get or create outbound session"""
        if destination not in self.outbound_sessions:
            session = OutboundSession(destination)
            self.outbound_sessions[destination] = session
        return self.outbound_sessions[destination]
    
    def add_inbound_session(self, session):
        """Add new inbound session"""
        # Check limits
        if len(self.inbound_sessions) >= self.max_inbound_sessions:
            self.expire_oldest_session()
        
        self.inbound_sessions.append(session)
        
        # Add tags to lookup table
        self.register_session_tags(session)
    
    def register_session_tags(self, session):
        """Register session's tags in lookup table"""
        for tag in session.inbound_tagset.get_all_tags():
            self.tag_to_session[tag] = session
    
    def lookup_tag(self, tag):
        """Fast tag lookup"""
        return self.tag_to_session.get(tag)
    
    def expire_sessions(self):
        """Periodic session expiration"""
        now_time = now()
        
        # Expire outbound sessions
        for dest, session in list(self.outbound_sessions.items()):
            if session.idle_time(now_time) > 8 * 60:
                del self.outbound_sessions[dest]
        
        # Expire inbound sessions
        expired = []
        for session in self.inbound_sessions:
            if session.idle_time(now_time) > 10 * 60:
                expired.append(session)
        
        for session in expired:
            self.remove_inbound_session(session)
    
    def remove_inbound_session(self, session):
        """Remove inbound session and clean up tags"""
        self.inbound_sessions.remove(session)
        
        # Remove tags from lookup
        for tag in session.inbound_tagset.get_all_tags():
            if tag in self.tag_to_session:
                del self.tag_to_session[tag]
```
**Gerenciamento de memória:**

```python
class TagMemoryManager:
    def __init__(self, max_memory_kb=10240):  # 10 MB default
        self.max_memory = max_memory_kb * 1024
        self.current_memory = 0
        self.max_tags_per_session = 160
        self.min_tags_per_session = 32
    
    def calculate_tag_memory(self, session):
        """Calculate memory used by session tags"""
        tag_count = len(session.inbound_tagset.tags)
        # Each tag: 8 bytes (tag) + 2 bytes (index) + 32 bytes (key, optional)
        # + overhead
        bytes_per_tag = 16 if session.defer_keys else 48
        return tag_count * bytes_per_tag
    
    def check_pressure(self):
        """Check if under memory pressure"""
        return self.current_memory > (self.max_memory * 0.9)
    
    def handle_pressure(self):
        """Reduce memory usage when under pressure"""
        if not self.check_pressure():
            return
        
        # Strategy 1: Reduce look-ahead windows
        for session in all_sessions:
            if session.look_ahead > self.min_tags_per_session:
                session.reduce_look_ahead(self.min_tags_per_session)
        
        # Strategy 2: Trim old tags aggressively
        for session in all_sessions:
            session.inbound_tagset.trim_behind(aggressive=True)
        
        # Strategy 3: Refuse new ratchets
        for session in all_sessions:
            if session.outbound_tagset.should_ratchet():
                session.defer_ratchet = True
        
        # Strategy 4: Expire idle sessions early
        expire_idle_sessions(threshold=5*60)  # 5 min instead of 10
```
### Estratégias de Teste

**Testes unitários:**

```python
def test_x25519_dh():
    """Test X25519 key exchange"""
    alice_sk = GENERATE_PRIVATE()
    alice_pk = DERIVE_PUBLIC(alice_sk)
    
    bob_sk = GENERATE_PRIVATE()
    bob_pk = DERIVE_PUBLIC(bob_sk)
    
    # Both sides compute same shared secret
    alice_shared = DH(alice_sk, bob_pk)
    bob_shared = DH(bob_sk, alice_pk)
    
    assert alice_shared == bob_shared

def test_elligator2_encode_decode():
    """Test Elligator2 roundtrip"""
    sk = GENERATE_PRIVATE_ELG2()
    pk = DERIVE_PUBLIC(sk)
    
    encoded = ENCODE_ELG2(pk)
    decoded = DECODE_ELG2(encoded)
    
    assert decoded == pk

def test_chacha_poly_encrypt_decrypt():
    """Test ChaCha20-Poly1305 AEAD"""
    key = CSRNG(32)
    nonce = construct_nonce(42)
    plaintext = b"Hello, I2P!"
    ad = b"associated_data"
    
    ciphertext = ENCRYPT(key, nonce, plaintext, ad)
    decrypted = DECRYPT(key, nonce, ciphertext, ad)
    
    assert decrypted == plaintext

def test_session_tag_ratchet():
    """Test session tag generation"""
    sessTag_ck = CSRNG(32)
    tagset = SessionTagRatchet(sessTag_ck)
    
    # Generate 100 tags
    tags = [tagset.get_next_tag() for _ in range(100)]
    
    # All tags should be unique
    assert len(set(tags)) == 100
    
    # Each tag should be 8 bytes
    for tag in tags:
        assert len(tag) == 8
```
**Testes de Integração:**

```python
def test_ns_nsr_handshake():
    """Test NS/NSR handshake"""
    # Alice creates outbound session
    alice_session = OutboundSession(bob_destination, bound=True)
    
    # Alice sends NS
    ns_message = alice_session.build_ns_message(b"Hello Bob")
    
    # Bob receives NS
    bob_session = InboundSession.try_decrypt_ns(ns_message)
    assert bob_session is not None
    assert bob_session.bound == True
    
    # Bob sends NSR
    nsr_message = bob_session.build_nsr_message(b"Hello Alice")
    
    # Alice receives NSR
    alice_session.on_nsr_received(nsr_message)
    assert alice_session.state == SessionState.ESTABLISHED
    
    # Both should have matching ES tagsets
    # (Cannot directly compare, but can test by sending ES messages)

def test_es_bidirectional():
    """Test ES messages in both directions"""
    # (After NS/NSR handshake)
    
    # Alice sends ES to Bob
    es_alice_to_bob = alice_session.send_es_message(b"Data from Alice")
    
    # Bob receives ES
    bob_session.process_es_message(es_alice_to_bob)
    
    # Bob sends ES to Alice
    es_bob_to_alice = bob_session.send_es_message(b"Data from Bob")
    
    # Alice receives ES
    alice_session.process_es_message(es_bob_to_alice)

def test_dh_ratchet():
    """Test DH ratchet"""
    # (After established session)
    
    # Alice initiates ratchet
    alice_session.initiate_ratchet()
    nextkey_alice = build_nextkey_block(
        flags=0x01,
        key_id=0,
        public_key=alice_new_key
    )
    
    # Send to Bob
    bob_session.process_nextkey_block(nextkey_alice)
    
    # Bob replies
    nextkey_bob = build_nextkey_block(
        flags=0x03,
        key_id=0,
        public_key=bob_new_key
    )
    
    # Send to Alice
    alice_session.process_nextkey_block(nextkey_bob)
    
    # Both should now be using new tagsets
    assert alice_session.outbound_tagset.id == 1
    assert bob_session.inbound_tagset.id == 1
```
**Vetores de teste:**

Implementar vetores de teste da especificação:

1. **Noise IK Handshake** (padrão de handshake IK do protocolo Noise): Use vetores de teste padronizados do Noise
2. **HKDF** (função de derivação de chaves baseada em HMAC): Use vetores de teste da RFC 5869
3. **ChaCha20-Poly1305** (cifra AEAD que combina ChaCha20 e Poly1305): Use vetores de teste da RFC 7539
4. **Elligator2** (técnica de mapeamento para ofuscação de chaves públicas): Use vetores de teste do artigo do Elligator2 ou do OBFS4

**Testes de interoperabilidade:**

1. **Java I2P**: Testar contra a implementação de referência do Java I2P
2. **i2pd**: Testar contra a implementação do i2pd em C++
3. **Capturas de pacotes**: Usar o dissector do Wireshark (se disponível) para verificar os formatos de mensagem
4. **Entre implementações**: Criar um test harness (infraestrutura de testes) que possa enviar/receber entre implementações

### Considerações de Desempenho

**Geração de Chaves:**

A geração de chaves Elligator2 (técnica criptográfica que torna chaves públicas indistinguíveis de dados aleatórios) é dispendiosa (taxa de rejeição de 50%):

```python
class KeyPool:
    """Pre-generate keys in background thread"""
    def __init__(self, pool_size=10):
        self.pool = Queue(maxsize=pool_size)
        self.generator_thread = Thread(target=self.generate_keys, daemon=True)
        self.generator_thread.start()
    
    def generate_keys(self):
        while True:
            if not self.pool.full():
                keypair = generate_elg2_keypair()
                # Also compute encoded form
                encoded = ENCODE_ELG2(keypair.public_key)
                self.pool.put((keypair, encoded))
            else:
                sleep(0.1)
    
    def get_keypair(self):
        try:
            return self.pool.get(timeout=1.0)
        except Empty:
            # Pool exhausted, generate inline
            return generate_elg2_keypair()
```
**Consulta de tags:**

Use tabelas hash para busca de tags em O(1):

```python
class FastTagLookup:
    def __init__(self):
        self.tag_to_session = {}  # Python dict is hash table
    
    def add_tag(self, tag, session, index):
        # 8-byte tag as bytes is hashable
        self.tag_to_session[tag] = (session, index)
    
    def lookup_tag(self, tag):
        return self.tag_to_session.get(tag)
```
**Otimização de Memória:**

Adiar a geração de chave simétrica:

```python
class DeferredKeyRatchet:
    """Only generate keys when needed"""
    def __init__(self, symmKey_ck):
        self.chainKey = symmKey_ck
        self.index = -1
        self.cache = LRUCache(maxsize=32)  # Cache recent keys
    
    def get_key(self, index):
        # Check cache first
        if index in self.cache:
            return self.cache[index]
        
        # Generate keys up to index
        while self.index < index:
            self.index += 1
            keydata = HKDF(self.chainKey, ZEROLEN, "SymmetricRatchet", 64)
            self.chainKey = keydata[0:31]
            
            if self.index == index:
                key = keydata[32:63]
                self.cache[index] = key
                return key
```
**Processamento em lote:**

Processar várias mensagens em lote:

```python
def process_message_batch(messages):
    """Process multiple messages efficiently"""
    results = []
    
    # Group by type
    ns_messages = []
    nsr_messages = []
    es_messages = []
    
    for msg in messages:
        msg_type = classify_message(msg)
        if msg_type[0] == 'NS':
            ns_messages.append(msg)
        elif msg_type[0] == 'NSR':
            nsr_messages.append(msg)
        elif msg_type[0] == 'ES':
            es_messages.append(msg)
    
    # Process in batches
    # ES messages are most common, process first
    for msg in es_messages:
        results.append(process_es_message(msg))
    
    for msg in nsr_messages:
        results.append(process_nsr_message(msg))
    
    for msg in ns_messages:
        results.append(process_ns_message(msg))
    
    return results
```
---

## Considerações de Segurança

### Modelo de Ameaça

**Capacidades do Adversário:**

1. **Observador Passivo**: Pode observar todo o tráfego da rede
2. **Atacante Ativo**: Pode injetar, modificar, descartar, repetir mensagens
3. **Nó Comprometido**: Pode comprometer um router ou destino
4. **Análise de Tráfego**: Pode realizar análise estatística dos padrões de tráfego

**Objetivos de segurança:**

1. **Confidencialidade**: Conteúdo das mensagens oculto para observadores
2. **Autenticação**: Identidade do remetente verificada (para sessões vinculadas)
3. **Forward Secrecy (sigilo direto)**: Mensagens anteriores permanecem secretas mesmo que as chaves sejam comprometidas
4. **Prevenção de Repetição**: Não é possível repetir mensagens antigas
5. **Ofuscação de Tráfego**: Negociações iniciais indistinguíveis de dados aleatórios

### Pressupostos criptográficos

**Hipóteses de dureza:**

1. **X25519 CDH**: O problema Diffie-Hellman computacional é difícil na Curve25519
2. **ChaCha20 PRF**: ChaCha20 é uma função pseudorrandômica
3. **Poly1305 MAC**: Poly1305 é inforjável sob ataque de mensagem escolhida
4. **SHA-256 CR**: SHA-256 é resistente a colisões
5. **HKDF Security**: HKDF extrai e expande chaves distribuídas uniformemente

**Níveis de segurança:**

- **X25519**: ~128 bits de segurança (ordem da curva 2^252)
- **ChaCha20**: chaves de 256 bits, segurança de 256 bits
- **Poly1305**: segurança de 128 bits (probabilidade de colisão)
- **SHA-256**: resistência a colisões de 128 bits, resistência à pré-imagem de 256 bits

### Gerenciamento de Chaves

**Geração de Chaves:**

```python
# CRITICAL: Use cryptographically secure RNG
def CSRNG(length):
    # GOOD: os.urandom, secrets.token_bytes (Python)
    # GOOD: /dev/urandom (Linux)
    # GOOD: BCryptGenRandom (Windows)
    # BAD: random.random(), Math.random() (NOT cryptographically secure)
    return os.urandom(length)

# CRITICAL: Validate keys
def validate_x25519_key(pubkey):
    # Check for weak keys (all zeros, small order points)
    if pubkey == bytes(32):
        raise WeakKeyError("All-zero public key")
    
    # Perform DH to check for weak shared secrets
    test_shared = DH(test_private_key, pubkey)
    if test_shared == bytes(32):
        raise WeakKeyError("Results in zero shared secret")
```
**Armazenamento de chaves:**

```python
# CRITICAL: Protect private keys
class SecureKeyStorage:
    def __init__(self):
        # Store in memory with protection
        self.keys = {}
        
        # Option 1: Memory locking (prevent swapping to disk)
        # mlock(self.keys)
        
        # Option 2: Encrypted storage
        # self.encryption_key = derive_from_password()
    
    def store_key(self, key_id, private_key):
        # Option: Encrypt before storage
        # encrypted = encrypt(private_key, self.encryption_key)
        # self.keys[key_id] = encrypted
        self.keys[key_id] = private_key
    
    def delete_key(self, key_id):
        # Securely wipe memory
        if key_id in self.keys:
            key = self.keys[key_id]
            # Overwrite with zeros before deletion
            for i in range(len(key)):
                key[i] = 0
            del self.keys[key_id]
```
**Rotação de chaves:**

```python
# CRITICAL: Rotate keys regularly
class KeyRotationPolicy:
    def __init__(self):
        self.max_messages_per_tagset = 4096  # Ratchet before 65535
        self.max_tagset_age = 10 * 60       # 10 minutes
        self.max_session_age = 60 * 60      # 1 hour
    
    def should_ratchet(self, tagset):
        return (tagset.messages_sent >= self.max_messages_per_tagset or
                tagset.age() >= self.max_tagset_age)
    
    def should_replace_session(self, session):
        return session.age() >= self.max_session_age
```
### Mitigações de ataques

### Mitigações de Ataques de Repetição

**Validação de data e hora:**

```python
MAX_CLOCK_SKEW_PAST = 5 * 60
MAX_CLOCK_SKEW_FUTURE = 2 * 60

def validate_datetime(timestamp):
    now = int(time.time())
    age = now - timestamp
    
    if age < -MAX_CLOCK_SKEW_FUTURE:
        raise ReplayError("Timestamp too far in future")
    
    if age > MAX_CLOCK_SKEW_PAST:
        raise ReplayError("Timestamp too old")
    
    return True
```
**Filtro de Bloom para mensagens NS:**

```python
class ReplayFilter:
    def __init__(self, capacity=100000, error_rate=0.001, duration=5*60):
        self.bloom = BloomFilter(capacity=capacity, error_rate=error_rate)
        self.duration = duration
        self.entries = []  # (timestamp, ephemeral_key)
    
    def check_replay(self, ephemeral_key, timestamp):
        # Validate timestamp
        if not validate_datetime(timestamp):
            return False
        
        # Check Bloom filter
        if ephemeral_key in self.bloom:
            # Potential replay (or false positive)
            # Check exact match in entries
            for ts, key in self.entries:
                if key == ephemeral_key:
                    return False  # Definite replay
        
        # Add to filter
        self.bloom.add(ephemeral_key)
        self.entries.append((timestamp, ephemeral_key))
        
        # Expire old entries
        self.expire_old_entries()
        
        return True
    
    def expire_old_entries(self):
        now = int(time.time())
        self.entries = [(ts, key) for ts, key in self.entries
                       if now - ts < self.duration]
```
**Uso único do Session Tag (etiqueta de sessão):**

```python
def process_session_tag(tag):
    # Look up tag
    entry = tagset.lookup_tag(tag)
    if entry is None:
        raise ValueError("Invalid session tag")
    
    # CRITICAL: Remove tag immediately (one-time use)
    tagset.remove_tag(tag)
    
    # Use associated key
    return entry.key, entry.index
```
### Mitigações contra Impersonação por Comprometimento de Chave (KCI)

**Problema**: a autenticação de mensagens do NS é vulnerável a KCI (Key Compromise Impersonation, personificação por comprometimento de chave) (Nível de Autenticação 1)

**Mitigação**:

1. Migre para NSR (Nível de Autenticação 2) o mais rapidamente possível
2. Não confie na carga útil de NS para operações críticas de segurança
3. Aguarde a confirmação de NSR antes de realizar ações irreversíveis

```python
def process_ns_message(ns_message):
    # NS authenticated at Level 1 (KCI vulnerable)
    # Do NOT perform security-critical operations yet
    
    # Extract sender's static key
    sender_key = ns_message.static_key
    
    # Mark session as pending Level 2 authentication
    session.auth_level = 1
    session.sender_key = sender_key
    
    # Send NSR
    send_nsr_reply(session)

def process_first_es_message(es_message):
    # Now we have Level 2 authentication (KCI resistant)
    session.auth_level = 2
    
    # Safe to perform security-critical operations
    process_security_critical_operation(es_message)
```
### Mitigações contra ataques de negação de serviço

**Proteção contra inundação de NS:**

```python
class NSFloodProtection:
    def __init__(self):
        self.ns_count = defaultdict(int)  # source -> count
        self.ns_timestamps = defaultdict(list)  # source -> [timestamps]
        
        self.max_ns_per_source = 5
        self.rate_window = 10  # seconds
        self.max_concurrent_ns = 100
    
    def check_ns_allowed(self, source):
        # Global limit
        total_pending = sum(self.ns_count.values())
        if total_pending >= self.max_concurrent_ns:
            return False
        
        # Per-source rate limit
        now = time.time()
        timestamps = self.ns_timestamps[source]
        
        # Remove old timestamps
        timestamps = [ts for ts in timestamps if now - ts < self.rate_window]
        self.ns_timestamps[source] = timestamps
        
        # Check rate
        if len(timestamps) >= self.max_ns_per_source:
            return False
        
        # Allow NS
        timestamps.append(now)
        self.ns_count[source] += 1
        return True
    
    def on_session_established(self, source):
        # Decrease pending count
        if self.ns_count[source] > 0:
            self.ns_count[source] -= 1
```
**Limites de armazenamento de tags:**

```python
class TagStorageLimit:
    def __init__(self, max_tags=1000000):
        self.max_tags = max_tags
        self.current_tags = 0
    
    def can_create_session(self, look_ahead):
        if self.current_tags + look_ahead > self.max_tags:
            return False
        return True
    
    def add_tags(self, count):
        self.current_tags += count
    
    def remove_tags(self, count):
        self.current_tags -= count
```
**Gerenciamento de Recursos Adaptativo:**

```python
class AdaptiveResourceManager:
    def __init__(self):
        self.load_level = 0  # 0 = low, 1 = medium, 2 = high, 3 = critical
    
    def adjust_parameters(self):
        if self.load_level == 0:
            # Normal operation
            return {
                'max_look_ahead': 160,
                'max_sessions': 1000,
                'session_timeout': 10 * 60
            }
        
        elif self.load_level == 1:
            # Moderate load
            return {
                'max_look_ahead': 80,
                'max_sessions': 800,
                'session_timeout': 8 * 60
            }
        
        elif self.load_level == 2:
            # High load
            return {
                'max_look_ahead': 32,
                'max_sessions': 500,
                'session_timeout': 5 * 60
            }
        
        else:  # load_level == 3
            # Critical load
            return {
                'max_look_ahead': 16,
                'max_sessions': 200,
                'session_timeout': 3 * 60
            }
```
### Resistência à Análise de Tráfego

**Codificação Elligator2:**

Garante que mensagens de handshake (negociação inicial) sejam indistinguíveis de dados aleatórios:

```python
# NS and NSR start with Elligator2-encoded ephemeral keys
# Observer cannot distinguish from random 32-byte string
```
**Estratégias de Preenchimento:**

```python
# Resist message size fingerprinting
def add_padding(payload, strategy='random'):
    if strategy == 'random':
        # Random padding 0-15 bytes
        size = random.randint(0, 15)
    
    elif strategy == 'round':
        # Round to next 64-byte boundary
        target = ((len(payload) + 63) // 64) * 64
        size = target - len(payload) - 3  # -3 for block header
    
    elif strategy == 'fixed':
        # Always 1KB messages
        size = 1024 - len(payload) - 3
    
    return build_padding_block(size)
```
**Ataques de temporização:**

```python
# CRITICAL: Use constant-time operations
def constant_time_compare(a, b):
    """Constant-time byte string comparison"""
    if len(a) != len(b):
        return False
    
    result = 0
    for x, y in zip(a, b):
        result |= x ^ y
    
    return result == 0

# CRITICAL: Constant-time MAC verification
def verify_mac(computed_mac, received_mac):
    if not constant_time_compare(computed_mac, received_mac):
        # Always take same time regardless of where comparison fails
        raise AuthenticationError("MAC verification failed")
```
### Armadilhas na Implementação

**Erros comuns:**

1. **Reutilização de Nonce (número usado uma vez)**: NUNCA reutilize pares (key, nonce)
   ```python
   # BAD: Reusing nonce with same key
   ciphertext1 = ENCRYPT(key, nonce, plaintext1, ad1)
   ciphertext2 = ENCRYPT(key, nonce, plaintext2, ad2)  # CATASTROPHIC

# CORRETO: nonce (número usado uma vez) exclusivo para cada mensagem    ciphertext1 = ENCRYPT(key, nonce1, plaintext1, ad1)    ciphertext2 = ENCRYPT(key, nonce2, plaintext2, ad2)

   ```

2. **Ephemeral Key Reuse**: Generate fresh ephemeral key for each NS/NSR
   ```python
# RUIM: Reutilizando chave efêmera    ephemeral_key = generate_elg2_keypair()    send_ns_message(ephemeral_key)    send_ns_message(ephemeral_key)  # RUIM

# CORRETO: Nova chave para cada mensagem    send_ns_message(generate_elg2_keypair())    send_ns_message(generate_elg2_keypair())

   ```

3. **Weak RNG**: Use cryptographically secure random number generator
   ```python
# RUIM: Gerador de números aleatórios não criptográfico    import random    key = bytes([random.randint(0, 255) for _ in range(32)])  # INSEGURO

# BOM: Gerador de números aleatórios criptograficamente seguro    import os    key = os.urandom(32)

   ```

4. **Timing Attacks**: Use constant-time comparisons
   ```python
# RUIM: Comparação com saída antecipada    if computed_mac == received_mac:  # Vazamento de temporização

       pass
   
# BOM: Comparação em tempo constante    if constant_time_compare(computed_mac, received_mac):

       pass
   ```

5. **Incomplete MAC Verification**: Always verify before using data
   ```python
# RUIM: Descriptografando antes da verificação    plaintext = chacha20_decrypt(key, nonce, ciphertext)    mac_ok = verify_mac(mac, plaintext)  # TARDE DEMAIS    if not mac_ok:

       return error
   
# CORRETO: AEAD verifica antes de decifrar    try:

       plaintext = DECRYPT(key, nonce, ciphertext, ad)  # Verifies MAC first
except AuthenticationError:

       return error
   ```

6. **Key Deletion**: Securely wipe keys from memory
   ```python
# RUIM: Exclusão simples    del private_key  # Ainda na memória

# CORRETO: Sobrescrever antes da exclusão    for i in range(len(private_key)):

       private_key[i] = 0
del private_key

   ```

### Security Audits

**Recommended Audits:**

1. **Cryptographic Review**: Expert review of KDF chains and DH operations
2. **Implementation Audit**: Code review for timing attacks, key management, RNG usage
3. **Protocol Analysis**: Formal verification of handshake security properties
4. **Side-Channel Analysis**: Timing, power, and cache attacks
5. **Fuzzing**: Random input testing for parser robustness

**Test Cases:**

```python
# Casos de teste críticos para a segurança

def test_nonce_uniqueness():

    """Ensure nonces are never reused"""
    nonces = set()
    for i in range(10000):
        nonce = construct_nonce(i)
        assert nonce not in nonces
        nonces.add(nonce)

def test_key_isolation():

    """Ensure sessions don't share keys"""
    session1 = create_session(destination1)
    session2 = create_session(destination2)
    
    assert session1.key != session2.key

def test_replay_prevention():

    """Ensure replay attacks are detected"""
    ns_message = create_ns_message()
    
    # First delivery succeeds
    assert process_ns_message(ns_message) == True
    
    # Replay fails
    assert process_ns_message(ns_message) == False

def test_mac_verification():

    """Ensure MAC verification is enforced"""
    key = CSRNG(32)
    nonce = construct_nonce(0)
    plaintext = b"test"
    ad = b"test_ad"
    
    ciphertext = ENCRYPT(key, nonce, plaintext, ad)
    
    # Correct MAC verifies
    assert DECRYPT(key, nonce, ciphertext, ad) == plaintext
    
    # Corrupted MAC fails
    corrupted = ciphertext[:-1] + bytes([ciphertext[-1] ^ 0xFF])
    with pytest.raises(AuthenticationError):
        DECRYPT(key, nonce, corrupted, ad)
```

---

## Configuration and Deployment

### I2CP Configuration

**Enable ECIES Encryption:**

```properties
# Somente ECIES (recomendado para novas implantações)

i2cp.leaseSetEncType=4

# Chave dupla (ECIES + ElGamal para compatibilidade)

i2cp.leaseSetEncType=4,0

# Somente ElGamal (legado, não recomendado)

i2cp.leaseSetEncType=0

```

**LeaseSet Type:**

```properties
# LS2 padrão (mais comum)

i2cp.leaseSetType=3

# LS2 criptografado (blinded destinations — destinos cegos)

i2cp.leaseSetType=5

# Meta LS2 (múltiplos destinos; versão 2 de leaseSet)

i2cp.leaseSetType=7

```

**Additional Options:**

```properties
# Chave estática para ECIES (esquema de criptografia integrada de curva elíptica) (opcional, gerada automaticamente se não for especificada)

# Chave pública X25519 de 32 bytes, codificada em base64

i2cp.leaseSetPrivateKey=<base64-encoded-key>

# Tipo de assinatura (para LeaseSet)

i2cp.leaseSetSigningPrivateKey=<base64-encoded-key> i2cp.leaseSetSigningType=7  # Ed25519

```

### Java I2P Configuration

**router.config:**

```properties
# ECIES de router para router

i2p.router.useECIES=true

```

**Build Properties:**

```java
// Para clientes I2CP (Java) Properties props = new Properties(); props.setProperty("i2cp.leaseSetEncType", "4"); props.setProperty("i2cp.leaseSetType", "3");

I2PSession session = i2pClient.createSession(props);

```

### i2pd Configuration

**i2pd.conf:**

```ini
[limites]

# Limite de memória das sessões de ECIES (Esquema Integrado de Criptografia com Curvas Elípticas)

ecies.memory = 128M

[ecies]

# Ativar ECIES (Esquema de Criptografia Integrada de Curvas Elípticas)

enabled = true

# Apenas ECIES (esquema integrado de criptografia com curvas elípticas) ou dual-key (chave dupla)

compatibility = true  # true = chave dupla, false = apenas ECIES

```

**Tunnels Configuration:**

```ini
[my-service] type = http host = 127.0.0.1 port = 8080 keys = my-service-keys.dat

# Apenas ECIES (Esquema Integrado de Criptografia com Curvas Elípticas)

ecies = true

```

### Compatibility Matrix

**Router Version Support:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Version</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">ECIES Support</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">LS2 Support</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Dual-Key</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">&lt; 0.9.38</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">❌ No</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">❌ No</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">N/A</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Legacy only</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.38-0.9.45</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">❌ No</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">✅ Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">N/A</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">LS2 only</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.46-0.9.50</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">✅ Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">✅ Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">✅ Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Initial ECIES</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">1.5.0+</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">✅ Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">✅ Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">✅ Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">2.0.0+</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">✅ Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">✅ Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">✅ Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
  </tbody>
</table>

**Destination Compatibility:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Destination Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Can Connect To</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ECIES-only</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ECIES-only, Dual-key</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Requires 0.9.46+ routers</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Dual-key</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Any</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Maximum compatibility</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ElGamal-only</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ElGamal-only, Dual-key</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Legacy</td>
    </tr>
  </tbody>
</table>

**FloodFill Requirements:**

- **ECIES-only destinations**: Require majority of floodfills on 0.9.46+ for encrypted lookups
- **Dual-key destinations**: Work with any floodfill version
- **Current status**: Near 100% floodfill adoption as of 2025

### Migration Guide

**Migrating from ElGamal to ECIES:**

**Step 1: Enable Dual-Key Mode**

```properties
# Adicionar ECIES (Esquema de Criptografia Integrado de Curvas Elípticas) mantendo ElGamal (esquema de criptografia de chave pública ElGamal)

i2cp.leaseSetEncType=4,0

```

**Step 2: Monitor Connections**

```bash
# Verifique os tipos de conexão

i2prouter.exe status

# ou

http://127.0.0.1:7657/peers

```

**Step 3: Switch to ECIES-Only (after testing)**

```properties
# Remover ElGamal

i2cp.leaseSetEncType=4

```

**Step 4: Restart Application**

```bash
# Reinicie o I2P router ou o aplicativo

systemctl restart i2p

# ou

i2prouter.exe restart

```

**Rollback Plan:**

```properties
# Reverter para apenas ElGamal em caso de problemas

i2cp.leaseSetEncType=0

```

### Performance Tuning

**Session Limits:**

```properties
# Número máximo de sessões de entrada

i2p.router.maxInboundSessions=1000

# Máximo de sessões de saída

i2p.router.maxOutboundSessions=1000

# Tempo limite da sessão (segundos)

i2p.router.sessionTimeout=600

```

**Memory Limits:**

```properties
# Limite de armazenamento de tags (KB)

i2p.ecies.maxTagMemory=10240  # 10 MB

# Janela de antecipação

i2p.ecies.tagLookAhead=160 i2p.ecies.tagLookAheadMin=32

```

**Ratchet Policy:**

```properties
# Mensagens anteriores ao ratchet (mecanismo de catraca criptográfica)

i2p.ecies.ratchetThreshold=4096

# Tempo antes do ratchet (mecanismo de avanço de chaves) (segundos)

i2p.ecies.ratchetTimeout=600  # 10 minutos

```

### Monitoring and Debugging

**Logging:**

```properties
# Ativar o registro de depuração do ECIES (esquema de criptografia integrada de curvas elípticas)

logger.i2p.router.transport.ecies=DEBUG

```

**Metrics:**

Monitor these metrics:

1. **NS Success Rate**: Percentage of NS messages receiving NSR
2. **Session Establishment Time**: Time from NS to first ES
3. **Tag Storage Usage**: Current memory usage for tags
4. **Ratchet Frequency**: How often sessions ratchet
5. **Session Lifetime**: Average session duration

**Common Issues:**

1. **NS Timeout**: No NSR received
   - Check destination is online
   - Check floodfill availability
   - Verify LeaseSet published correctly

2. **High Memory Usage**: Too many tags stored
   - Reduce look-ahead window
   - Decrease session timeout
   - Implement aggressive expiration

3. **Frequent Ratchets**: Sessions ratcheting too often
   - Increase ratchet threshold
   - Check for retransmissions

4. **Session Failures**: ES messages failing to decrypt
   - Verify tag synchronization
   - Check for replay attacks
   - Validate nonce construction

---

## References

### Specifications

1. **ECIES Proposal**: [Proposal 144](/proposals/144-ecies-x25519-aead-ratchet/)
2. **I2NP**: [I2NP Specification](/docs/specs/i2np/)
3. **Common Structures**: [Common Structures Specification](/docs/specs/common-structures/)
4. **NTCP2**: [NTCP2 Specification](/docs/specs/ntcp2/)
5. **SSU2**: [SSU2 Specification](/docs/specs/ssu2/)
6. **I2CP**: [I2CP Specification](/docs/specs/i2cp/)
7. **ElGamal/AES+SessionTags**: [ElGamal/AES Specification](/docs/legacy/elgamal-aes/)

### Cryptographic Standards

1. **Noise Protocol Framework**: [Noise Specification](https://noiseprotocol.org/noise.html) (Revision 34, 2018-07-11)
2. **Signal Double Ratchet**: [Signal Specification](https://signal.org/docs/specifications/doubleratchet/)
3. **RFC 7748**: [Elliptic Curves for Security (X25519)](https://tools.ietf.org/html/rfc7748)
4. **RFC 7539**: [ChaCha20 and Poly1305 for IETF Protocols](https://tools.ietf.org/html/rfc7539)
5. **RFC 5869**: [HKDF (HMAC-based Key Derivation Function)](https://tools.ietf.org/html/rfc5869)
6. **RFC 2104**: [HMAC: Keyed-Hashing for Message Authentication](https://tools.ietf.org/html/rfc2104)
7. **Elligator2**: [Elligator Paper](https://elligator.cr.yp.to/elligator-20130828.pdf)

### Implementation Resources

1. **Java I2P**: [i2p.i2p Repository](https://github.com/i2p/i2p.i2p)
2. **i2pd (C++)**: [i2pd Repository](https://github.com/PurpleI2P/i2pd)
3. **OBFS4 (Elligator2)**: [obfs4proxy Repository](https://gitlab.com/yawning/obfs4)

### Additional Information

1. **I2P Website**: [/](/)
2. **I2P Forum**: [https://i2pforum.net](https://i2pforum.net)
3. **I2P Wiki**: [https://wiki.i2p-projekt.de](https://wiki.i2p-projekt.de)

---

## Appendix A: KDF Summary

**All KDF Operations in ECIES:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Operation</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Input</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Info String</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Output</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">NS Initial ChainKey</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">protocol_name</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">(none - SHA256)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">h, chainKey</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">NS Static Key Section</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">chainKey, es_shared</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">""</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">chainKey, k</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">NS Payload Section (bound)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">chainKey, ss_shared</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">""</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">chainKey, k</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">NSR Tagset</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">chainKey</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">"SessionReplyTags"</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">tagsetKey</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">NSR ee DH</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">chainKey, ee_shared</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">""</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">chainKey</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">NSR se DH</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">chainKey, se_shared</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">""</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">chainKey, k</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">NSR Split</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">chainKey</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">""</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">k_ab, k_ba</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">NSR Payload</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">k_ba</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">"AttachPayloadKDF"</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">k_nsr</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">DH Initialize</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">rootKey, k</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">"KDFDHRatchetStep"</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">nextRootKey, chainKey</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Tag and Key Chain Keys</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">chainKey</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">"TagAndKeyGenKeys"</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">sessTag_ck, symmKey_ck</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Session Tag Init</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">sessTag_ck</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">"STInitialization"</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">chainKey, CONSTANT</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Session Tag Gen</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">chainKey, CONSTANT</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">"SessionTagKeyGen"</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">chainKey, tag</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Symmetric Key Gen</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">chainKey</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">"SymmetricRatchet"</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">chainKey, key</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">DH Ratchet</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">sharedSecret</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">"XDHRatchetTagSet"</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">tagsetKey</td>
    </tr>
  </tbody>
</table>

---

## Appendix B: Message Size Calculator

**Calculate message sizes for capacity planning:**

```python
def calculate_ns_size(payload_size, bound=True):

    """Calculate New Session message size"""
    ephemeral_key = 32
    static_section = 32 + 16  # encrypted + MAC
    payload_encrypted = payload_size + 16  # + MAC
    
    return ephemeral_key + static_section + payload_encrypted

def calculate_nsr_size(payload_size):

    """Calculate New Session Reply message size"""
    tag = 8
    ephemeral_key = 32
    key_section_mac = 16
    payload_encrypted = payload_size + 16  # + MAC
    
    return tag + ephemeral_key + key_section_mac + payload_encrypted

def calculate_es_size(payload_size):

    """Calculate Existing Session message size"""
    tag = 8
    payload_encrypted = payload_size + 16  # + MAC
    
    return tag + payload_encrypted

# Exemplos

print("NS (bound, 1KB payload):", calculate_ns_size(1024, bound=True), "bytes")

# Saída: 1120 bytes

print("NSR (1KB payload):", calculate_nsr_size(1024), "bytes")

# Saída: 1096 bytes

print("ES (carga útil de 1KB):", calculate_es_size(1024), "bytes")

# Saída: 1048 bytes

```

---

## Appendix C: Glossary

**AEAD**: Authenticated Encryption with Associated Data - encryption mode that provides both confidentiality and authenticity

**Authentication Level**: Noise protocol security property indicating strength of sender identity verification

**Binding**: Association of a session with a specific far-end destination

**ChaCha20**: Stream cipher designed by Daniel J. Bernstein

**ChainKey**: Cryptographic key used in HKDF chains to derive subsequent keys

**Confidentiality Level**: Noise protocol security property indicating strength of forward secrecy

**DH**: Diffie-Hellman key agreement protocol

**Elligator2**: Encoding technique to make elliptic curve points indistinguishable from random

**Ephemeral Key**: Short-lived key used only for a single handshake

**ES**: Existing Session message (used after handshake completion)

**Forward Secrecy**: Property ensuring past communications remain secure if keys are compromised

**Garlic Clove**: I2NP message container for end-to-end delivery

**HKDF**: HMAC-based Key Derivation Function

**IK Pattern**: Noise handshake pattern where initiator sends static key immediately

**KCI**: Key Compromise Impersonation attack

**KDF**: Key Derivation Function - cryptographic function for generating keys from other keys

**LeaseSet**: I2P structure containing a destination's public keys and tunnel information

**LS2**: LeaseSet version 2 with encryption type support

**MAC**: Message Authentication Code - cryptographic checksum proving authenticity

**MixHash**: Noise protocol function for maintaining running hash transcript

**NS**: New Session message (initiates new session)

**NSR**: New Session Reply message (response to NS)

**Nonce**: Number used once - ensures unique encryption even with same key

**Pairing**: Linking an inbound session with an outbound session for bidirectional communication

**Poly1305**: Message authentication code designed by Daniel J. Bernstein

**Ratchet**: Cryptographic mechanism for deriving sequential keys

**Session Tag**: 8-byte one-time identifier for existing session messages

**Static Key**: Long-term key associated with a destination's identity

**Tag Set**: Collection of session tags derived from a common root

**X25519**: Elliptic curve Diffie-Hellman key agreement using Curve25519

---