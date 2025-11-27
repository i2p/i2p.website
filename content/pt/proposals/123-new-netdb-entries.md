---
title: "Novas Entradas netDB"
number: "123"
author: "zzz, str4d, orignal"
created: "2016-01-16"
lastupdated: "2020-07-18"
status: "Abrir"
thread: "http://zzz.i2p/topics/2051"
supercedes: "110, 120, 121, 122"
---

## Status

Partes desta proposta estão completas e implementadas na versão 0.9.38 e 0.9.39. As especificações de Common Structures, I2CP, I2NP e outras agora estão atualizadas para refletir as mudanças que são suportadas atualmente.

As partes concluídas ainda estão sujeitas a revisões menores. Outras partes desta proposta ainda estão em desenvolvimento e sujeitas a revisões substanciais.

Service Lookup (tipos 9 e 11) são de baixa prioridade e não programados, e podem ser separados para uma proposta distinta.

## Visão Geral

Esta é uma atualização e agregação das seguintes 4 propostas:

- 110 LS2
- 120 Meta LS2 para multihoming massivo
- 121 LS2 Criptografado
- 122 Busca de serviço não autenticada (anycasting)

Essas propostas são em sua maioria independentes, mas para manter a coerência definimos e usamos um formato comum para várias delas.

As seguintes propostas estão de certa forma relacionadas:

- 140 Invisible Multihoming (incompatível com esta proposta)
- 142 New Crypto Template (para nova criptografia simétrica)
- 144 ECIES-X25519-AEAD-Ratchet
- 145 ECIES-P256
- 146 Red25519
- 148 EdDSA-BLAKE2b-Ed25519
- 149 B32 para LS2 Criptografado
- 150 Garlic Farm Protocol
- 151 ECDSA Blinding

## Proposta

Esta proposta define 5 novos tipos de DatabaseEntry e o processo para armazená-los e recuperá-los da base de dados da rede, bem como o método para assiná-los e verificar essas assinaturas.

### Goals

- Compatível com versões anteriores
- LS2 utilizável com multihoming de estilo antigo
- Nenhuma nova criptografia ou primitivas necessárias para suporte
- Manter desacoplamento de criptografia e assinatura; suportar todas as versões atuais e futuras
- Habilitar chaves de assinatura offline opcionais
- Reduzir precisão de timestamps para reduzir fingerprinting
- Habilitar nova criptografia para destinos
- Habilitar multihoming massivo
- Corrigir múltiplos problemas com LS criptografado existente
- Blinding opcional para reduzir visibilidade por floodfills
- Criptografado suporta tanto chave única quanto múltiplas chaves revogáveis
- Busca de serviços para facilitar busca de outproxies, bootstrap de DHT de aplicação,
  e outros usos
- Não quebrar nada que dependa de hashes de destino binários de 32 bytes, ex. bittorrent
- Adicionar flexibilidade aos leasesets via propriedades, como temos nos routerinfos.
- Colocar timestamp publicado e expiração variável no cabeçalho, para que funcione mesmo
  se o conteúdo estiver criptografado (não derivar timestamp do lease mais antigo)
- Todos os novos tipos vivem no mesmo espaço DHT e mesmas localizações dos leasesets existentes,
  para que usuários possam migrar do LS antigo para LS2,
  ou mudar entre LS2, Meta e Encrypted,
  sem alterar o Destination ou hash.
- Um Destination existente pode ser convertido para usar chaves offline,
  ou voltar para chaves online, sem alterar o Destination ou hash.

### Non-Goals / Out-of-scope

- Novo algoritmo de rotação DHT ou geração aleatória compartilhada
- O tipo específico de nova criptografia e esquema de criptografia ponta-a-ponta
  para usar esse novo tipo estaria em uma proposta separada.
  Nenhuma nova criptografia é especificada ou discutida aqui.
- Nova criptografia para RIs ou construção de tunnel.
  Isso estaria em uma proposta separada.
- Métodos de criptografia, transmissão e recepção de mensagens I2NP DLM / DSM / DSRM.
  Não está mudando.
- Como gerar e suportar Meta, incluindo comunicação inter-router de backend, gerenciamento, failover e coordenação.
  O suporte pode ser adicionado ao I2CP, ou i2pcontrol, ou um novo protocolo.
  Isso pode ou não ser padronizado.
- Como realmente implementar e gerenciar tunnels com expiração mais longa, ou cancelar tunnels existentes.
  Isso é extremamente difícil, e sem isso, você não pode ter um desligamento gracioso razoável.
- Mudanças no modelo de ameaças
- Formato de armazenamento offline, ou métodos para armazenar/recuperar/compartilhar os dados.
- Detalhes de implementação não são discutidos aqui e ficam a cargo de cada projeto.

### Justification

LS2 adiciona campos para alterar o tipo de criptografia e para futuras mudanças de protocolo.

LS2 criptografado corrige várias questões de segurança do LS criptografado existente ao usar criptografia assimétrica de todo o conjunto de leases.

Meta LS2 oferece multihoming flexível, eficiente, eficaz e em larga escala.

Service Record e Service List fornecem serviços anycast como consulta de nomes e inicialização de DHT.

### Objetivos

Os números de tipo são usados nas Mensagens I2NP Database Lookup/Store.

A coluna end-to-end refere-se a se as consultas/respostas são enviadas para um Destination em uma Garlic Message.

Tipos existentes:

| NetDB Data | Lookup Type | Store Type |
|------------|-------------|------------|
| any        | 0           | any        |
| LS         | 1           | 1          |
| RI         | 2           | 0          |
| exploratory| 3           | DSRM       |
Novos tipos:

| NetDB Data     | Lookup Type | Store Type | Std. LS2 Header? | Sent end-to-end? |
|----------------|-------------|------------|------------------|------------------|
| LS2            | 1           | 3          | yes              | yes              |
| Encrypted LS2  | 1           | 5          | no               | no               |
| Meta LS2       | 1           | 7          | yes              | no               |
| Service Record | n/a         | 9          | yes              | no               |
| Service List   | 4           | 11         | no               | no               |
### Não-Objetivos / Fora de escopo

- Os tipos de lookup são atualmente os bits 3-2 na Database Lookup Message.
  Quaisquer tipos adicionais exigiriam o uso do bit 4.

- Todos os tipos de armazenamento são ímpares, pois os bits superiores no campo
  de tipo da Database Store Message são ignorados pelos roteadores antigos.
  Preferimos que a análise falhe como um LS do que como um RI comprimido.

- O tipo deve ser explícito ou implícito ou nenhum dos dois nos dados cobertos pela assinatura?

### Justificativa

Os tipos 3, 5 e 7 podem ser retornados em resposta a uma consulta de leaseset padrão (tipo 1). O tipo 9 nunca é retornado em resposta a uma consulta. O tipo 11 é retornado em resposta a um novo tipo de consulta de serviço (tipo 11).

Apenas o tipo 3 pode ser enviado em uma mensagem Garlic client-to-client.

### Tipos de Dados NetDB

Os tipos 3, 7 e 9 têm todos um formato comum::

Cabeçalho LS2 Padrão - conforme definido abaixo

Parte Específica do Tipo   - conforme definido abaixo em cada parte

Assinatura LS2 Padrão:   - Comprimento conforme implícito pelo tipo de assinatura da chave de assinatura

Tipo 5 (Criptografado) não começa com um Destination e tem um formato diferente. Veja abaixo.

Tipo 11 (Lista de Serviços) é uma agregação de vários Registros de Serviço e tem um formato diferente. Veja abaixo.

### Notas

TBD

## Standard LS2 Header

Os tipos 3, 7 e 9 usam o cabeçalho LS2 padrão, especificado abaixo:

### Processo de Lookup/Store

```
Standard LS2 Header:
  - Type (1 byte)
    Not actually in header, but part of data covered by signature.
    Take from field in Database Store Message.
  - Destination (387+ bytes)
  - Published timestamp (4 bytes, big endian, seconds since epoch, rolls over in 2106)
  - Expires (2 bytes, big endian) (offset from published timestamp in seconds, 18.2 hours max)
  - Flags (2 bytes)
    Bit order: 15 14 ... 3 2 1 0
    Bit 0: If 0, no offline keys; if 1, offline keys
    Bit 1: If 0, a standard published leaseset.
           If 1, an unpublished leaseset. Should not be flooded, published, or
           sent in response to a query. If this leaseset expires, do not query the
           netdb for a new one, unless bit 2 is set.
    Bit 2: If 0, a standard published leaseset.
           If 1, this unencrypted leaseset will be blinded and encrypted when published.
           If this leaseset expires, query the blinded location in the netdb for a new one.
           If this bit is set to 1, set bit 1 to 1 also.
           As of release 0.9.42.
    Bits 3-15: set to 0 for compatibility with future uses
  - If flag indicates offline keys, the offline signature section:
    Expires timestamp (4 bytes, big endian, seconds since epoch, rolls over in 2106)
    Transient sig type (2 bytes, big endian)
    Transient signing public key (length as implied by sig type)
    Signature of expires timestamp, transient sig type, and public key,
    by the destination public key,
    length as implied by destination public key sig type.
    This section can, and should, be generated offline.
```
### Formato

- Unpublished/published: Para uso ao enviar um database store ponto-a-ponto,
  o router remetente pode desejar indicar que este leaseset não deve ser
  enviado para outros. Atualmente usamos heurísticas para manter este estado.

- Published: Substitui a lógica complexa necessária para determinar a 'versão' do
  leaseset. Atualmente, a versão é a expiração do lease que expira por último,
  e um router de publicação deve incrementar essa expiração em pelo menos 1ms ao
  publicar um leaseset que apenas remove um lease mais antigo.

- Expires: Permite que uma entrada netDb expire antes da expiração do seu leaseSet com expiração mais tardia. Pode não ser útil para LS2, onde os leaseSets devem manter uma expiração máxima de 11 minutos, mas para outros tipos novos, é necessário (veja Meta LS e Service Record abaixo).

- As chaves offline são opcionais, para reduzir a complexidade inicial/necessária de implementação.

### Considerações de Privacidade/Segurança

- Poderia reduzir ainda mais a precisão do timestamp (10 minutos?) mas teria que adicionar
  número de versão. Isso poderia quebrar o multihoming, a menos que tenhamos criptografia que preserva ordem?
  Provavelmente não conseguimos fazer sem timestamps completamente.

- Alternativa: timestamp de 3 bytes (época / 10 minutos), versão de 1 byte, expira em 2 bytes

- O tipo é explícito ou implícito nos dados / assinatura? Constantes de "Domain" para assinatura?

### Notes

- Os routers não devem publicar um LS mais de uma vez por segundo.
  Se o fizerem, devem incrementar artificialmente o timestamp publicado em 1
  sobre o LS publicado anteriormente.

- As implementações de router podem armazenar em cache as chaves transitórias e assinatura para
  evitar verificação a cada vez. Em particular, floodfills e routers em
  ambas as extremidades de conexões de longa duração poderiam se beneficiar disso.

- Chaves offline e assinatura são apropriadas apenas para destinos de longa duração,
  ou seja, servidores, não clientes.

## New DatabaseEntry types

### Formato

Alterações do LeaseSet existente:

- Adicionar timestamp de publicação, timestamp de expiração, flags e propriedades
- Adicionar tipo de encriptação
- Remover chave de revogação

Consultar com

    Standard LS flag (1)
Armazenar com

    Standard LS2 type (3)
Armazenar em

    Hash of destination
    This hash is then used to generate the daily "routing key", as in LS1
Expiração típica

    10 minutes, as in a regular LS.
Publicado por

    Destination

### Justificação

```
Standard LS2 Header as specified above

  Standard LS2 Type-Specific Part
  - Properties (Mapping as specified in common structures spec, 2 zero bytes if none)
  - Number of key sections to follow (1 byte, max TBD)
  - Key sections:
    - Encryption type (2 bytes, big endian)
    - Encryption key length (2 bytes, big endian)
      This is explicit, so floodfills can parse LS2 with unknown encryption types.
    - Encryption key (number of bytes specified)
  - Number of lease2s (1 byte)
  - Lease2s (40 bytes each)
    These are leases, but with a 4-byte instead of an 8-byte expiration,
    seconds since the epoch (rolls over in 2106)

  Standard LS2 Signature:
  - Signature
    If flag indicates offline keys, this is signed by the transient pubkey,
    otherwise, by the destination pubkey
    Length as implied by sig type of signing key
    The signature is of everything above.
```
### Problemas

- Properties: Expansão futura e flexibilidade.
  Colocado primeiro caso seja necessário para análise dos dados restantes.

- Vários pares de tipo de criptografia/chave pública são
  para facilitar a transição para novos tipos de criptografia. A outra maneira de fazer isso
  é publicar vários leaseSets, possivelmente usando os mesmos túneis,
  como fazemos agora para destinos DSA e EdDSA.
  A identificação do tipo de criptografia recebida em um túnel
  pode ser feita com o mecanismo de session tag existente,
  e/ou descriptografia de teste usando cada chave. Os comprimentos das mensagens
  recebidas também podem fornecer uma pista.

### Notas

Esta proposta continua a usar a chave pública no leaseset para a chave de encriptação ponta-a-ponta, e deixa o campo de chave pública no Destination não utilizado, como está agora. O tipo de encriptação não é especificado no certificado de chave do Destination, permanecerá 0.

Uma alternativa rejeitada é especificar o tipo de criptografia no certificado de chave de Destination, usar a chave pública no Destination, e não usar a chave pública no leaseset. Não planejamos fazer isso.

Benefícios do LS2:

- A localização da chave pública real não muda.
- O tipo de criptografia, ou chave pública, pode mudar sem alterar o Destination.
- Remove o campo de revogação não utilizado
- Compatibilidade básica com outros tipos de DatabaseEntry nesta proposta
- Permite múltiplos tipos de criptografia

Desvantagens do LS2:

- Localização da chave pública e tipo de criptografia difere do RouterInfo
- Mantém chave pública não utilizada no leaseset
- Requer implementação em toda a rede; como alternativa, tipos experimentais
  de criptografia podem ser usados, se permitido pelos floodfills
  (mas veja as propostas relacionadas 136 e 137 sobre suporte para tipos de assinatura experimentais).
  A proposta alternativa pode ser mais fácil de implementar e testar para tipos de criptografia experimentais.

### New Encryption Issues

Parte disso está fora do escopo desta proposta, mas colocando notas aqui por enquanto, já que ainda não temos uma proposta de criptografia separada. Veja também as propostas ECIES 144 e 145.

- O tipo de criptografia representa a combinação
  de curva, comprimento da chave e esquema ponta a ponta,
  incluindo KDF e MAC, se houver.

- Incluímos um campo de comprimento de chave, para que o LS2 seja
  analisável e verificável pelo floodfill mesmo para tipos de criptografia desconhecidos.

- O primeiro novo tipo de criptografia a ser proposto será
  provavelmente ECIES/X25519. Como será usado end-to-end
  (seja uma versão ligeiramente modificada do ElGamal/AES+SessionTag
  ou algo completamente novo, por exemplo ChaCha/Poly) será especificado
  em uma ou mais propostas separadas.
  Veja também as propostas ECIES 144 e 145.

### LeaseSet 2

- Expiração de 8 bytes em leases alterada para 4 bytes.

- Se algum dia implementarmos revogação, podemos fazê-lo com um campo expires de zero,
  ou zero leases, ou ambos. Não há necessidade de uma chave de revogação separada.

- As chaves de encriptação estão ordenadas por preferência do servidor, a mais preferida primeiro.
  O comportamento padrão do cliente é selecionar a primeira chave com
  um tipo de encriptação suportado. Os clientes podem usar outros algoritmos de seleção
  baseados no suporte de encriptação, desempenho relativo e outros fatores.

### Formato

Objetivos:

- Adicionar blinding
- Permitir múltiplos tipos de assinatura
- Não exigir quaisquer primitivos criptográficos novos
- Opcionalmente criptografar para cada destinatário, revogável
- Suportar criptografia apenas de Standard LS2 e Meta LS2

LS2 criptografado nunca é enviado em uma mensagem garlic ponto-a-ponto. Use o LS2 padrão conforme descrito acima.

Mudanças do LeaseSet criptografado existente:

- Criptografar tudo por segurança
- Criptografar de forma segura, não apenas com AES
- Criptografar para cada destinatário

Consultar com

    Standard LS flag (1)
Armazenar com

    Encrypted LS2 type (5)
Armazenar em

    Hash of blinded sig type and blinded public key
    Two byte sig type (big endian, e.g. 0x000b) || blinded public key
    This hash is then used to generate the daily "routing key", as in LS1
Expiração típica

    10 minutes, as in a regular LS, or hours, as in a meta LS.
Publicado por

    Destination


### Justificação

Definimos as seguintes funções correspondentes aos blocos de construção criptográficos utilizados para LS2 criptografado:

CSRNG(n)

    n-byte output from a cryptographically-secure random number generator.

    In addition to the requirement of CSRNG being cryptographically-secure (and thus
    suitable for generating key material), it MUST be safe
    for some n-byte output to be used for key material when the byte sequences immediately
    preceding and following it are exposed on the network (such as in a salt, or encrypted
    padding). Implementations that rely on a potentially-untrustworthy source should hash
    any output that is to be exposed on the network. See [PRNG references](http://projectbullrun.org/dual-ec/ext-rand.html) and [Tor dev discussion](https://lists.torproject.org/pipermail/tor-dev/2015-November/009954.html).

H(p, d)

    SHA-256 hash function that takes a personalization string p and data d, and
    produces an output of length 32 bytes.

    Use SHA-256 as follows::

        H(p, d) := SHA-256(p || d)

STREAM

    The ChaCha20 stream cipher as specified in [RFC 7539 Section 2.4](https://tools.ietf.org/html/rfc7539#section-2.4), with the initial counter
    set to 1. S_KEY_LEN = 32 and S_IV_LEN = 12.

    ENCRYPT(k, iv, plaintext)
        Encrypts plaintext using the cipher key k, and nonce iv which MUST be unique for
        the key k. Returns a ciphertext that is the same size as the plaintext.

        The entire ciphertext must be indistinguishable from random if the key is secret.

    DECRYPT(k, iv, ciphertext)
        Decrypts ciphertext using the cipher key k, and nonce iv. Returns the plaintext.


SIG

    The RedDSA signature scheme (corresponding to SigType 11) with key blinding.
    It has the following functions:

    DERIVE_PUBLIC(privkey)
        Returns the public key corresponding to the given private key.

    SIGN(privkey, m)
        Returns a signature by the private key privkey over the given message m.

    VERIFY(pubkey, m, sig)
        Verifies the signature sig against the public key pubkey and message m. Returns
        true if the signature is valid, false otherwise.

    It must also support the following key blinding operations:

    GENERATE_ALPHA(data, secret)
        Generate alpha for those who know the data and an optional secret.
        The result must be identically distributed as the private keys.

    BLIND_PRIVKEY(privkey, alpha)
        Blinds a private key, using a secret alpha.

    BLIND_PUBKEY(pubkey, alpha)
        Blinds a public key, using a secret alpha.
        For a given keypair (privkey, pubkey) the following relationship holds::

            BLIND_PUBKEY(pubkey, alpha) ==
            DERIVE_PUBLIC(BLIND_PRIVKEY(privkey, alpha))

DH

    X25519 public key agreement system. Private keys of 32 bytes, public keys of 32
    bytes, produces outputs of 32 bytes. It has the following
    functions:

    GENERATE_PRIVATE()
        Generates a new private key.

    DERIVE_PUBLIC(privkey)
        Returns the public key corresponding to the given private key.

    DH(privkey, pubkey)
        Generates a shared secret from the given private and public keys.

HKDF(salt, ikm, info, n)

    A cryptographic key derivation function which takes some input key material ikm (which
    should have good entropy but is not required to be a uniformly random string), a salt
    of length 32 bytes, and a context-specific 'info' value, and produces an output
    of n bytes suitable for use as key material.

    Use HKDF as specified in [RFC 5869](https://tools.ietf.org/html/rfc5869), using the HMAC hash function SHA-256
    as specified in [RFC 2104](https://tools.ietf.org/html/rfc2104). This means that SALT_LEN is 32 bytes max.


### Discussão

O formato LS2 criptografado consiste em três camadas aninhadas:

- Uma camada externa contendo as informações de texto simples necessárias para armazenamento e recuperação.
- Uma camada intermediária que gerencia a autenticação do cliente.
- Uma camada interna que contém os dados reais do LS2.

O formato geral é semelhante a::

    Layer 0 data + Enc(layer 1 data + Enc(layer 2 data)) + Signature

Note que LS2 criptografado é ofuscado. O Destination não está no cabeçalho. A localização de armazenamento DHT é SHA-256(tipo de assinatura || chave pública ofuscada), e rotacionada diariamente.

NÃO usa o cabeçalho LS2 padrão especificado acima.

#### Layer 0 (outer)

Tipo

    1 byte

    Not actually in header, but part of data covered by signature.
    Take from field in Database Store Message.

Tipo de Assinatura de Chave Pública Cega

    2 bytes, big endian
    This will always be type 11, identifying a Red25519 blinded key.

Chave Pública Cega

    Length as implied by sig type

Carimbo de data/hora de publicação

    4 bytes, big endian

    Seconds since epoch, rolls over in 2106

Expira

    2 bytes, big endian

    Offset from published timestamp in seconds, 18.2 hours max

Flags

    2 bytes

    Bit order: 15 14 ... 3 2 1 0

    Bit 0: If 0, no offline keys; if 1, offline keys

    Other bits: set to 0 for compatibility with future uses

Dados de chave transitória

    Present if flag indicates offline keys

    Expires timestamp
        4 bytes, big endian

        Seconds since epoch, rolls over in 2106

    Transient sig type
        2 bytes, big endian

    Transient signing public key
        Length as implied by sig type

    Signature
        Length as implied by blinded public key sig type

        Over expires timestamp, transient sig type, and transient public key.

        Verified with the blinded public key.

lenOuterCiphertext

    2 bytes, big endian

outerCiphertext

    lenOuterCiphertext bytes

    Encrypted layer 1 data. See below for key derivation and encryption algorithms.

Assinatura

    Length as implied by sig type of the signing key used

    The signature is of everything above.

    If the flag indicates offline keys, the signature is verified with the transient
    public key. Otherwise, the signature is verified with the blinded public key.


#### Layer 1 (middle)

Bandeiras

    1 byte
    
    Bit order: 76543210

    Bit 0: 0 for everybody, 1 for per-client, auth section to follow

    Bits 3-1: Authentication scheme, only if bit 0 is set to 1 for per-client, otherwise 000
              000: DH client authentication (or no per-client authentication)
              001: PSK client authentication

    Bits 7-4: Unused, set to 0 for future compatibility

Dados de autenticação do cliente DH

    Present if flag bit 0 is set to 1 and flag bits 3-1 are set to 000.

    ephemeralPublicKey
        32 bytes

    clients
        2 bytes, big endian

        Number of authClient entries to follow, 40 bytes each

    authClient
        Authorization data for a single client.
        See below for the per-client authorization algorithm.

        clientID_i
            8 bytes

        clientCookie_i
            32 bytes

Dados de autenticação de cliente PSK

    Present if flag bit 0 is set to 1 and flag bits 3-1 are set to 001.

    authSalt
        32 bytes

    clients
        2 bytes, big endian

        Number of authClient entries to follow, 40 bytes each

    authClient
        Authorization data for a single client.
        See below for the per-client authorization algorithm.

        clientID_i
            8 bytes

        clientCookie_i
            32 bytes


innerCiphertext

    Length implied by lenOuterCiphertext (whatever data remains)

    Encrypted layer 2 data. See below for key derivation and encryption algorithms.


#### Layer 2 (inner)

Tipo

    1 byte

    Either 3 (LS2) or 7 (Meta LS2)

Dados

    LeaseSet2 data for the given type.

    Includes the header and signature.


### Novos Problemas de Criptografia

Utilizamos o seguinte esquema para key blinding, baseado em Ed25519 e [ZCash RedDSA](https://github.com/zcash/zips/tree/master/protocol/protocol.pdf). As assinaturas Re25519 são sobre a curva Ed25519, usando SHA-512 para o hash.

Não utilizamos o [Tor's rend-spec-v3.txt appendix A.2](https://spec.torproject.org/rend-spec-v3), que tem objetivos de design similares, porque suas chaves públicas cegas podem estar fora do subgrupo de ordem prima, com implicações de segurança desconhecidas.

#### Goals

- A chave pública de assinatura no destino não cegado deve ser
  Ed25519 (tipo de assinatura 7) ou Red25519 (tipo de assinatura 11);
  nenhum outro tipo de assinatura é suportado
- Se a chave pública de assinatura estiver offline, a chave pública de assinatura transitória também deve ser Ed25519
- O cegamento é computacionalmente simples
- Usar primitivas criptográficas existentes
- Chaves públicas cegadas não podem ser descegadas
- Chaves públicas cegadas devem estar na curva Ed25519 e subgrupo de ordem prima
- Deve conhecer a chave pública de assinatura do destino
  (destino completo não é necessário) para derivar a chave pública cegada
- Opcionalmente fornecer um segredo adicional necessário para derivar a chave pública cegada

#### Security

A segurança de um esquema de blinding requer que a distribuição de alpha seja a mesma das chaves privadas não blindadas. No entanto, quando blindamos uma chave privada Ed25519 (sig type 7) para uma chave privada Red25519 (sig type 11), a distribuição é diferente. Para atender aos requisitos da [seção 4.1.6.1 do zcash](https://github.com/zcash/zips/tree/master/protocol/protocol.pdf), Red25519 (sig type 11) deveria ser usado também para as chaves não blindadas, de modo que "a combinação de uma chave pública re-randomizada e assinatura(s) sob essa chave não revelem a chave da qual foi re-randomizada." Permitimos o tipo 7 para destinos existentes, mas recomendamos o tipo 11 para novos destinos que serão criptografados.

#### Definitions

B

    The Ed25519 base point (generator) 2^255 - 19 as in [Ed25519](http://cr.yp.to/papers.html#ed25519)

L

    The Ed25519 order 2^252 + 27742317777372353535851937790883648493
    as in [Ed25519](http://cr.yp.to/papers.html#ed25519)

DERIVE_PUBLIC(a)

    Convert a private key to public, as in Ed25519 (mulitply by G)

alpha

    A 32-byte random number known to those who know the destination.

GENERATE_ALPHA(destination, date, secret)

    Generate alpha for the current date, for those who know the destination and the secret.
    The result must be identically distributed as Ed25519 private keys.

a

    The unblinded 32-byte EdDSA or RedDSA signing private key used to sign the destination

A

    The unblinded 32-byte EdDSA or RedDSA signing public key in the destination,
    = DERIVE_PUBLIC(a), as in Ed25519

a'

    The blinded 32-byte EdDSA signing private key used to sign the encrypted leaseset
    This is a valid EdDSA private key.

A'

    The blinded 32-byte EdDSA signing public key in the Destination,
    may be generated with DERIVE_PUBLIC(a'), or from A and alpha.
    This is a valid EdDSA public key, on the curve and on the prime-order subgroup.

LEOS2IP(x)

    Flip the order of the input bytes to little-endian

H*(x)

    32 bytes = (LEOS2IP(SHA512(x))) mod B, same as in Ed25519 hash-and-reduce


#### Blinding Calculations

Uma nova chave secreta alpha e chaves cegas devem ser geradas a cada dia (UTC). A chave secreta alpha e as chaves cegas são calculadas da seguinte forma.

GENERATE_ALPHA(destination, date, secret), para todas as partes:

```text
// GENERATE_ALPHA(destination, date, secret)

  // secret is optional, else zero-length
  A = destination's signing public key
  stA = signature type of A, 2 bytes big endian (0x0007 or 0x000b)
  stA' = signature type of blinded public key A', 2 bytes big endian (0x000b)
  keydata = A || stA || stA'
  datestring = 8 bytes ASCII YYYYMMDD from the current date UTC
  secret = UTF-8 encoded string
  seed = HKDF(H("I2PGenerateAlpha", keydata), datestring || secret, "i2pblinding1", 64)
  // treat seed as a 64 byte little-endian value
  alpha = seed mod L
```
BLIND_PRIVKEY(), para o proprietário publicando o leaseSet:

```text
// BLIND_PRIVKEY()

  alpha = GENERATE_ALPHA(destination, date, secret)
  // If for a Ed25519 private key (type 7)
  seed = destination's signing private key
  a = left half of SHA512(seed) and clamped as usual for Ed25519
  // else, for a Red25519 private key (type 11)
  a = destination's signing private key
  // Addition using scalar arithmentic
  blinded signing private key = a' = BLIND_PRIVKEY(a, alpha) = (a + alpha) mod L
  blinded signing public key = A' = DERIVE_PUBLIC(a')
```
BLIND_PUBKEY(), para os clientes que recuperam o leaseset:

```text
// BLIND_PUBKEY()

  alpha = GENERATE_ALPHA(destination, date, secret)
  A = destination's signing public key
  // Addition using group elements (points on the curve)
  blinded public key = A' = BLIND_PUBKEY(A, alpha) = A + DERIVE_PUBLIC(alpha)
```
Ambos os métodos de calcular A' produzem o mesmo resultado, conforme necessário.

#### Signing

O leaseset não-cego é assinado pela chave privada de assinatura Ed25519 ou Red25519 não-cega e verificado com a chave pública de assinatura Ed25519 ou Red25519 não-cega (tipos de assinatura 7 ou 11) como de costume.

Se a chave pública de assinatura estiver offline, o leaseset não ofuscado é assinado pela chave privada de assinatura transitória Ed25519 ou Red25519 não ofuscada e verificado com a chave pública de assinatura transitória Ed25519 ou Red25519 não ofuscada (tipos de assinatura 7 ou 11) como de costume. Veja abaixo as notas adicionais sobre chaves offline para leasesets criptografados.

Para a assinatura do leaseset criptografado, usamos Red25519, baseado em [RedDSA](https://github.com/zcash/zips/tree/master/protocol/protocol.pdf) para assinar e verificar com chaves ofuscadas. As assinaturas Red25519 são sobre a curva Ed25519, usando SHA-512 para o hash.

Red25519 é idêntico ao Ed25519 padrão, exceto conforme especificado abaixo.

#### Sign/Verify Calculations

A porção externa do leaseset criptografado usa chaves e assinaturas Red25519.

Red25519 é quase idêntico ao Ed25519. Existem duas diferenças:

As chaves privadas Red25519 são geradas a partir de números aleatórios e depois devem ser reduzidas mod L, onde L é definido acima. As chaves privadas Ed25519 são geradas a partir de números aleatórios e depois "fixadas" usando mascaramento bitwise nos bytes 0 e 31. Isso não é feito para Red25519. As funções GENERATE_ALPHA() e BLIND_PRIVKEY() definidas acima geram chaves privadas Red25519 adequadas usando mod L.

No Red25519, o cálculo de r para assinatura usa dados aleatórios adicionais e utiliza o valor da chave pública em vez do hash da chave privada. Devido aos dados aleatórios, cada assinatura Red25519 é diferente, mesmo ao assinar os mesmos dados com a mesma chave.

Assinatura:

```text
T = 80 random bytes
  r = H*(T || publickey || message)
  // rest is the same as in Ed25519
```
Verificação:

```text
// same as in Ed25519
```
### Notas

#### Derivation of subcredentials

Como parte do processo de blinding, precisamos garantir que um LS2 criptografado só possa ser descriptografado por alguém que conheça a chave pública de assinatura da Destination correspondente. A Destination completa não é necessária. Para conseguir isso, derivamos uma credencial da chave pública de assinatura:

```text
A = destination's signing public key
  stA = signature type of A, 2 bytes big endian (0x0007 or 0x000b)
  stA' = signature type of A', 2 bytes big endian (0x000b)
  keydata = A || stA || stA'
  credential = H("credential", keydata)
```
A string de personalização garante que a credencial não colida com qualquer hash usado como chave de busca DHT, como o hash de Destination simples.

Para uma determinada chave ofuscada, podemos então derivar uma subcredencial:

```text
subcredential = H("subcredential", credential || blindedPublicKey)
```
A subcredencial é incluída nos processos de derivação de chave abaixo, o que vincula essas chaves ao conhecimento da chave pública de assinatura do Destination.

#### Layer 1 encryption

Primeiro, a entrada para o processo de derivação de chave é preparada:

```text
outerInput = subcredential || publishedTimestamp
```
Em seguida, um salt aleatório é gerado:

```text
outerSalt = CSRNG(32)
```
Então a chave usada para criptografar a camada 1 é derivada:

```text
keys = HKDF(outerSalt, outerInput, "ELS2_L1K", 44)
  outerKey = keys[0:31]
  outerIV = keys[32:43]
```
Finalmente, o texto simples da camada 1 é criptografado e serializado:

```text
outerCiphertext = outerSalt || ENCRYPT(outerKey, outerIV, outerPlaintext)
```
#### Layer 1 decryption

O salt é analisado a partir do texto cifrado da camada 1:

```text
outerSalt = outerCiphertext[0:31]
```
Então a chave usada para criptografar a camada 1 é derivada:

```text
outerInput = subcredential || publishedTimestamp
  keys = HKDF(outerSalt, outerInput, "ELS2_L1K", 44)
  outerKey = keys[0:31]
  outerIV = keys[32:43]
```
Finalmente, o texto cifrado da camada 1 é descriptografado:

```text
outerPlaintext = DECRYPT(outerKey, outerIV, outerCiphertext[32:end])
```
#### Layer 2 encryption

Quando a autorização de cliente está habilitada, ``authCookie`` é calculado conforme descrito abaixo. Quando a autorização de cliente está desabilitada, ``authCookie`` é o array de bytes de comprimento zero.

A criptografia procede de forma similar à camada 1:

```text
innerInput = authCookie || subcredential || publishedTimestamp
  innerSalt = CSRNG(32)
  keys = HKDF(innerSalt, innerInput, "ELS2_L2K", 44)
  innerKey = keys[0:31]
  innerIV = keys[32:43]
  innerCiphertext = innerSalt || ENCRYPT(innerKey, innerIV, innerPlaintext)
```
#### Layer 2 decryption

Quando a autorização de cliente está habilitada, ``authCookie`` é calculado como descrito abaixo. Quando a autorização de cliente está desabilitada, ``authCookie`` é o array de bytes de comprimento zero.

A descriptografia procede de maneira similar à camada 1:

```text
innerInput = authCookie || subcredential || publishedTimestamp
  innerSalt = innerCiphertext[0:31]
  keys = HKDF(innerSalt, innerInput, "ELS2_L2K", 44)
  innerKey = keys[0:31]
  innerIV = keys[32:43]
  innerPlaintext = DECRYPT(innerKey, innerIV, innerCiphertext[32:end])
```
### LS2 Criptografado

Quando a autorização de cliente está habilitada para um Destination, o servidor mantém uma lista de clientes que estão sendo autorizados a descriptografar os dados LS2 criptografados. Os dados armazenados por cliente dependem do mecanismo de autorização e incluem alguma forma de material de chave que cada cliente gera e envia para o servidor através de um mecanismo seguro fora da banda.

Existem duas alternativas para implementar autorização por cliente:

#### DH client authorization

Cada cliente gera um par de chaves DH ``[csk_i, cpk_i]``, e envia a chave pública ``cpk_i`` para o servidor.

Processamento do servidor
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

O servidor gera um novo ``authCookie`` e um par de chaves DH efêmero:

```text
authCookie = CSRNG(32)
  esk = GENERATE_PRIVATE()
  epk = DERIVE_PUBLIC(esk)
```
Então, para cada cliente autorizado, o servidor criptografa ``authCookie`` para sua chave pública:

```text
sharedSecret = DH(esk, cpk_i)
  authInput = sharedSecret || cpk_i || subcredential || publishedTimestamp
  okm = HKDF(epk, authInput, "ELS2_XCA", 52)
  clientKey_i = okm[0:31]
  clientIV_i = okm[32:43]
  clientID_i = okm[44:51]
  clientCookie_i = ENCRYPT(clientKey_i, clientIV_i, authCookie)
```
O servidor coloca cada tupla ``[clientID_i, clientCookie_i]`` na camada 1 do LS2 criptografado, junto com ``epk``.

Processamento do cliente
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

O cliente utiliza sua chave privada para derivar seu identificador de cliente esperado ``clientID_i``, chave de criptografia ``clientKey_i``, e IV de criptografia ``clientIV_i``:

```text
sharedSecret = DH(csk_i, epk)
  authInput = sharedSecret || cpk_i || subcredential || publishedTimestamp
  okm = HKDF(epk, authInput, "ELS2_XCA", 52)
  clientKey_i = okm[0:31]
  clientIV_i = okm[32:43]
  clientID_i = okm[44:51]
```
Em seguida, o cliente busca nos dados de autorização da camada 1 por uma entrada que contenha ``clientID_i``. Se uma entrada correspondente existir, o cliente a descriptografa para obter ``authCookie``:

```text
authCookie = DECRYPT(clientKey_i, clientIV_i, clientCookie_i)
```
#### Pre-shared key client authorization

Cada cliente gera uma chave secreta de 32 bytes ``psk_i``, e a envia para o servidor. Alternativamente, o servidor pode gerar a chave secreta, e enviá-la para um ou mais clientes.

Processamento do servidor
^^^^^^^^^^^^^^^^^^^^^

O servidor gera um novo ``authCookie`` e salt:

```text
authCookie = CSRNG(32)
  authSalt = CSRNG(32)
```
Em seguida, para cada cliente autorizado, o servidor criptografa ``authCookie`` com sua chave pré-compartilhada:

```text
authInput = psk_i || subcredential || publishedTimestamp
  okm = HKDF(authSalt, authInput, "ELS2PSKA", 52)
  clientKey_i = okm[0:31]
  clientIV_i = okm[32:43]
  clientID_i = okm[44:51]
  clientCookie_i = ENCRYPT(clientKey_i, clientIV_i, authCookie)
```
O servidor coloca cada tupla ``[clientID_i, clientCookie_i]`` na camada 1 do LS2 criptografado, juntamente com ``authSalt``.

Processamento do cliente ^^^^^^^^^^^^^^^^^^^^^

O cliente usa sua chave pré-compartilhada para derivar seu identificador de cliente esperado ``clientID_i``, chave de criptografia ``clientKey_i``, e IV de criptografia ``clientIV_i``:

```text
authInput = psk_i || subcredential || publishedTimestamp
  okm = HKDF(authSalt, authInput, "ELS2PSKA", 52)
  clientKey_i = okm[0:31]
  clientIV_i = okm[32:43]
  clientID_i = okm[44:51]
```
Em seguida, o cliente procura nos dados de autorização da camada 1 por uma entrada que contenha ``clientID_i``. Se uma entrada correspondente existir, o cliente a descriptografa para obter ``authCookie``:

```text
authCookie = DECRYPT(clientKey_i, clientIV_i, clientCookie_i)
```
#### Security considerations

Ambos os mecanismos de autorização de cliente acima fornecem privacidade para a associação de clientes. Uma entidade que conhece apenas o Destination pode ver quantos clientes estão inscritos a qualquer momento, mas não pode rastrear quais clientes estão sendo adicionados ou revogados.

Os servidores DEVEM randomizar a ordem dos clientes a cada vez que geram um LS2 criptografado, para evitar que os clientes descubram sua posição na lista e infiram quando outros clientes foram adicionados ou revogados.

Um servidor PODE escolher ocultar o número de clientes que estão inscritos inserindo entradas aleatórias na lista de dados de autorização.

Vantagens da autorização de cliente DH
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- A segurança do esquema não depende exclusivamente da troca fora de banda do material
  da chave do cliente. A chave privada do cliente nunca precisa sair do seu dispositivo,
  e assim um adversário que consegue interceptar a troca fora de banda, mas não consegue
  quebrar o algoritmo DH, não pode descriptografar o LS2 criptografado, ou determinar
  por quanto tempo o cliente tem acesso concedido.

Desvantagens da autorização de cliente DH
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Requer N + 1 operações DH no lado do servidor para N clientes.
- Requer uma operação DH no lado do cliente.
- Requer que o cliente gere a chave secreta.

Vantagens da autorização de cliente PSK
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Não requer operações DH.
- Permite ao servidor gerar a chave secreta.
- Permite ao servidor compartilhar a mesma chave com múltiplos clientes, se desejado.

Desvantagens da autorização de cliente PSK
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- A segurança do esquema depende criticamente da troca fora de banda do material de chave do cliente. Um adversário que intercepte a troca para um cliente específico pode descriptografar qualquer LS2 criptografado subsequente para o qual esse cliente esteja autorizado, bem como determinar quando o acesso do cliente é revogado.

### Definições

Veja a proposta 149.

Você não pode usar um LS2 criptografado para bittorrent, devido às respostas de announce compactas que têm 32 bytes. Os 32 bytes contêm apenas o hash. Não há espaço para uma indicação de que o leaseset está criptografado, ou os tipos de assinatura.

### Formato

Para leaseSets criptografados com chaves offline, as chaves privadas ofuscadas também devem ser geradas offline, uma para cada dia.

Como o bloco de assinatura offline opcional está na parte de texto limpo do leaseset criptografado, qualquer pessoa coletando dados dos floodfills poderia usar isso para rastrear o leaseset (mas não descriptografá-lo) ao longo de vários dias. Para evitar isso, o proprietário das chaves também deveria gerar novas chaves transitórias para cada dia. Tanto as chaves transitórias quanto as chaves cegas podem ser geradas com antecedência e entregues ao router em lote.

Não há formato de arquivo definido nesta proposta para empacotar múltiplas chaves transitórias e cegas e fornecê-las ao cliente ou router. Não há melhoria do protocolo I2CP definida nesta proposta para suportar leasesets criptografados com chaves offline.

### Notes

- Um serviço usando leaseSets criptografados publicaria a versão criptografada para os
  floodfills. No entanto, por eficiência, enviaria leaseSets não criptografados para
  os clientes na mensagem garlic encapsulada, uma vez autenticados (via whitelist, por
  exemplo).

- Os floodfills podem limitar o tamanho máximo para um valor razoável para prevenir abuso.

- Após a descriptografia, várias verificações devem ser feitas, incluindo que
  o timestamp interno e a expiração coincidam com aqueles no nível superior.

- ChaCha20 foi selecionado em vez de AES. Embora as velocidades sejam similares quando há suporte de hardware AES disponível, ChaCha20 é 2,5-3x mais rápido quando o suporte de hardware AES não está disponível, como em dispositivos ARM de baixo desempenho.

- Não nos importamos o suficiente com a velocidade para usar BLAKE2b com chave. Tem um
  tamanho de saída grande o suficiente para acomodar o maior n que necessitamos (ou podemos chamá-lo uma vez por
  chave desejada com um argumento contador). BLAKE2b é muito mais rápido que SHA-256, e
  BLAKE2b com chave reduziria o número total de chamadas de função hash.
  No entanto, veja a proposta 148, onde é proposto que mudemos para BLAKE2b por outras razões.
  Veja [Secure key derivation performance](https://www.lvh.io/posts/secure-key-derivation-performance.html).

### Meta LS2

Isso é usado para substituir multihoming. Como qualquer leaseset, isso é assinado pelo criador. Esta é uma lista autenticada de hashes de destino.

O Meta LS2 é o topo de, e possivelmente nós intermediários de, uma estrutura de árvore. Ele contém um número de entradas, cada uma apontando para um LS, LS2, ou outro Meta LS2 para suportar multihoming massivo. Um Meta LS2 pode conter uma mistura de entradas LS, LS2 e Meta LS2. As folhas da árvore são sempre um LS ou LS2. A árvore é um DAG; loops são proibidos; clientes fazendo consultas devem detectar e se recusar a seguir loops.

Um Meta LS2 pode ter uma expiração muito mais longa que um LS ou LS2 padrão. O nível superior pode ter uma expiração várias horas após a data de publicação. O tempo máximo de expiração será aplicado pelos floodfills e clientes, e ainda está por definir.

O caso de uso para Meta LS2 é multihoming massivo, mas sem mais proteção para correlação de roteadores com leaseSets (no momento de reinicialização do router) do que é fornecido agora com LS ou LS2. Isso é equivalente ao caso de uso "facebook", que provavelmente não precisa de proteção contra correlação. Este caso de uso provavelmente precisa de chaves offline, que são fornecidas no cabeçalho padrão em cada nó da árvore.

O protocolo de back-end para coordenação entre os routers folha, signatários Meta LS intermediários e mestres não está especificado aqui. Os requisitos são extremamente simples - apenas verificar se o peer está ativo e publicar um novo LS a cada poucas horas. A única complexidade é escolher novos publicadores para os Meta LSes de nível superior ou intermediário em caso de falha.

Mix-and-match leasesets onde leases de múltiplos routers são combinados, assinados e publicados em um único leaseset está documentado na proposta 140, "invisible multihoming". Esta proposta é insustentável como escrita, porque conexões streaming não seriam "sticky" a um único router, veja http://zzz.i2p/topics/2335 .

O protocolo de back-end, e a interação com os componentes internos do router e cliente, seria bastante complexa para multihoming invisível.

Para evitar sobrecarregar o floodfill para o Meta LS de nível superior, a expiração deve ser de pelo menos várias horas. Os clientes devem fazer cache do Meta LS de nível superior e persistir através de reinicializações se não estiver expirado.

Precisamos definir algum algoritmo para os clientes percorrerem a árvore, incluindo alternativas de fallback, para que o uso seja disperso. Alguma função de distância de hash, custo e aleatoriedade. Se um nó tem tanto LS ou LS2 quanto Meta LS, precisamos saber quando é permitido usar esses leaseSets e quando continuar percorrendo a árvore.

Consultar com

    Standard LS flag (1)
Armazenar com

    Meta LS2 type (7)
Armazenar em

    Hash of destination
    This hash is then used to generate the daily "routing key", as in LS1
Expiração típica

    Hours. Max 18.2 hours (65535 seconds)
Publicado por

    "master" Destination or coordinator, or intermediate coordinators

### Format

```
Standard LS2 Header as specified above

  Meta LS2 Type-Specific Part
  - Properties (Mapping as specified in common structures spec, 2 zero bytes if none)
  - Number of entries (1 byte) Maximum TBD
  - Entries. Each entry contains: (40 bytes)
    - Hash (32 bytes)
    - Flags (2 bytes)
      TBD. Set all to zero for compatibility with future uses.
    - Type (1 byte) The type of LS it is referencing;
      1 for LS, 3 for LS2, 5 for encrypted, 7 for meta, 0 for unknown.
    - Cost (priority) (1 byte)
    - Expires (4 bytes) (4 bytes, big endian, seconds since epoch, rolls over in 2106)
  - Number of revocations (1 byte) Maximum TBD
  - Revocations: Each revocation contains: (32 bytes)
    - Hash (32 bytes)

  Standard LS2 Signature:
  - Signature (40+ bytes)
    The signature is of everything above.
```
Flags e propriedades: para uso futuro

### Derivação de Chave de Ofuscação

- Um serviço distribuído usando isto teria um ou mais "mestres" com a
  chave privada do destino do serviço. Eles determinariam (fora de banda) a
  lista atual de destinos ativos e publicariam o Meta LS2. Para redundância,
  múltiplos mestres poderiam fazer multihome (ou seja, publicar simultaneamente) o
  Meta LS2.

- Um serviço distribuído pode começar com um único destino ou usar 
  multihoming de estilo antigo, depois fazer a transição para um Meta LS2. Uma 
  consulta LS padrão pode retornar qualquer um entre um LS, LS2, ou Meta LS2.

- Quando um serviço usa um Meta LS2, ele não tem túneis (leases).

### Service Record

Este é um registro individual que indica que um destino está participando de um serviço. É enviado do participante para o floodfill. Nunca é enviado individualmente por um floodfill, mas apenas como parte de uma Lista de Serviços. O Registro de Serviço também é usado para revogar a participação em um serviço, definindo a expiração como zero.

Isso não é um LS2, mas usa o formato padrão de cabeçalho e assinatura LS2.

Consultar com

    n/a, see Service List
Armazenar com

    Service Record type (9)
Armazenar em

    Hash of service name
    This hash is then used to generate the daily "routing key", as in LS1
Expiração típica

    Hours. Max 18.2 hours (65535 seconds)
Publicado por

    Destination

### Format

```
Standard LS2 Header as specified above

  Service Record Type-Specific Part
  - Port (2 bytes, big endian) (0 if unspecified)
  - Hash of service name (32 bytes)

  Standard LS2 Signature:
  - Signature (40+ bytes)
    The signature is of everything above.
```
### Notes

- Se expires for todos zeros, o floodfill deve revogar o registro e não mais
  incluí-lo na lista de serviços.

- Armazenamento: O floodfill pode restringir rigorosamente o armazenamento desses registros e
  limitar o número de registros armazenados por hash e sua expiração. Uma lista de permissões
  de hashes também pode ser utilizada.

- Qualquer outro tipo de netDb no mesmo hash tem prioridade, portanto um registro de serviço nunca pode
  substituir um LS/RI, mas um LS/RI irá substituir todos os registros de serviço nesse hash.

### Service List

Isso não se parece em nada com um LS2 e usa um formato diferente.

A lista de serviços é criada e assinada pelo floodfill. É não autenticada no sentido de que qualquer pessoa pode ingressar em um serviço publicando um Service Record para um floodfill.

Uma Lista de Serviços contém Registros de Serviço Curtos, não Registros de Serviço completos. Estes contêm assinaturas mas apenas hashes, não destinos completos, portanto não podem ser verificados sem o destino completo.

A segurança, se houver, e a conveniência das listas de serviços ainda está por ser determinada (TBD). Os floodfills poderiam limitar a publicação e as consultas a uma lista de permissões de serviços, mas essa lista pode variar com base na implementação ou preferência do operador. Pode não ser possível alcançar consenso sobre uma lista de permissões comum e básica entre as implementações.

Se o nome do serviço estiver incluído no registo de serviço acima, então os operadores de floodfill podem objetar; se apenas o hash estiver incluído, não há verificação, e um registo de serviço pode "entrar" à frente de qualquer outro tipo de netDb e ser armazenado no floodfill.

Consultar com

    Service List lookup type (11)
Armazenar com

    Service List type (11)
Armazenar em

    Hash of service name
    This hash is then used to generate the daily "routing key", as in LS1
Expiração típica

    Hours, not specified in the list itself, up to local policy
Publicado por

    Nobody, never sent to floodfill, never flooded.

### Format

NÃO usa o cabeçalho LS2 padrão especificado acima.

```
- Type (1 byte)
    Not actually in header, but part of data covered by signature.
    Take from field in Database Store Message.
  - Hash of the service name (implicit, in the Database Store message)
  - Hash of the Creator (floodfill) (32 bytes)
  - Published timestamp (8 bytes, big endian)

  - Number of Short Service Records (1 byte)
  - List of Short Service Records:
    Each Short Service Record contains (90+ bytes)
    - Dest hash (32 bytes)
    - Published timestamp (8 bytes, big endian)
    - Expires (4 bytes, big endian) (offset from published in ms)
    - Flags (2 bytes)
    - Port (2 bytes, big endian)
    - Sig length (2 bytes, big endian)
    - Signature of dest (40+ bytes)

  - Number of Revocation Records (1 byte)
  - List of Revocation Records:
    Each Revocation Record contains (86+ bytes)
    - Dest hash (32 bytes)
    - Published timestamp (8 bytes, big endian)
    - Flags (2 bytes)
    - Port (2 bytes, big endian)
    - Sig length (2 bytes, big endian)
    - Signature of dest (40+ bytes)

  - Signature of floodfill (40+ bytes)
    The signature is of everything above.
```
Para verificar a assinatura da Lista de Serviços:

- anexar o hash do nome do serviço
- remover o hash do criador
- Verificar assinatura dos conteúdos modificados

Para verificar a assinatura de cada Short Service Record:

- Buscar destino
- Verificar assinatura de (timestamp publicado + expira + flags + porta + Hash do
  nome do serviço)

Para verificar a assinatura de cada Registro de Revogação:

- Buscar destino
- Verificar assinatura de (timestamp publicado + 4 bytes zero + flags + porta + Hash
  do nome do serviço)

### Notes

- Usamos o comprimento da assinatura em vez do tipo de assinatura para que possamos suportar tipos de assinatura desconhecidos.

- Não há expiração de uma lista de serviços, os destinatários podem tomar sua própria decisão baseada na política ou na expiração dos registros individuais.

- As Listas de Serviço não são inundadas, apenas os Registros de Serviço individuais são. Cada
  floodfill cria, assina e armazena em cache uma Lista de Serviço. O floodfill usa sua
  própria política para tempo de cache e o número máximo de registros de serviço e revogação.

## Common Structures Spec Changes Required

### Criptografia e processamento

Fora do escopo desta proposta. Adicionar às propostas ECIES 144 e 145.

### New Intermediate Structures

Adicionar novas estruturas para Lease2, MetaLease, LeaseSet2Header e OfflineSignature. Efetivo a partir da versão 0.9.38.

### New NetDB Types

Adicionar estruturas para cada novo tipo de leaseSet, incorporadas do acima. Para LeaseSet2, EncryptedLeaseSet e MetaLeaseSet, efetivo a partir da versão 0.9.38. Para Service Record e Service List, preliminar e não agendado.

### New Signature Type

Adicionar RedDSA_SHA512_Ed25519 Tipo 11. Chave pública tem 32 bytes; chave privada tem 32 bytes; hash tem 64 bytes; assinatura tem 64 bytes.

## Encryption Spec Changes Required

Fora do escopo desta proposta. Consulte as propostas 144 e 145.

## I2NP Changes Required

Adicionar nota: LS2 só pode ser publicado em floodfills com uma versão mínima.

### Database Lookup Message

Adicionar o tipo de busca da lista de serviços.

### Changes

```
Flags byte: Lookup type field, currently bits 3-2, expands to bits 4-2.
  Lookup type 0x04 is defined as the service list lookup.

  Add note: Service list loookup may only be sent to floodfills with a minimum version.
  Minimum version is 0.9.38.
```
### Autorização por cliente

Adicione todos os novos tipos de armazenamento.

### Changes

```
Type byte: Type field, currently bit 0, expands to bits 3-0.
  Type 3 is defined as a LS2 store.
  Type 5 is defined as a encrypted LS2 store.
  Type 7 is defined as a meta LS2 store.
  Type 9 is defined as a service record store.
  Type 11 is defined as a service list store.
  Other types are undefined and invalid.

  Add note: All new types may only be published to floodfills with a minimum version.
  Minimum version is 0.9.38.
```
## I2CP Changes Required

### I2CP Options

Novas opções interpretadas no lado do router, enviadas no Mapeamento SessionConfig:

```

  i2cp.leaseSetType=nnn       The type of leaseset to be sent in the Create Leaseset Message
                              Value is the same as the netdb store type in the table above.
                              Interpreted client-side, but also passed to the router in the
                              SessionConfig, to declare intent and check support.

  i2cp.leaseSetEncType=nnn[,nnn]  The encryption types to be used.
                                  Interpreted client-side, but also passed to the router in
                                  the SessionConfig, to declare intent and check support.
                                  See proposals 144 and 145.

  i2cp.leaseSetOfflineExpiration=nnn  The expiration of the offline signature, ASCII,
                                      seconds since the epoch.

  i2cp.leaseSetTransientPublicKey=[type:]b64  The base 64 of the transient private key,
                                              prefixed by an optional sig type number
                                              or name, default DSA_SHA1.
                                              Length as inferred from the sig type

  i2cp.leaseSetOfflineSignature=b64   The base 64 of the offline signature.
                                      Length as inferred from the destination
                                      signing public key type

  i2cp.leaseSetSecret=b64     The base 64 of a secret used to blind the
                              address of the leaseset, default ""

  i2cp.leaseSetAuthType=nnn   The type of authentication for encrypted LS2.
                              0 for no per-client authentication (the default)
                              1 for DH per-client authentication
                              2 for PSK per-client authentication

  i2cp.leaseSetPrivKey=b64    A base 64 private key for the router to use to
                              decrypt the encrypted LS2,
                              only if per-client authentication is enabled
```
Novas opções interpretadas do lado do cliente:

```

  i2cp.leaseSetType=nnn     The type of leaseset to be sent in the Create Leaseset Message
                            Value is the same as the netdb store type in the table above.
                            Interpreted client-side, but also passed to the router in the
                            SessionConfig, to declare intent and check support.

  i2cp.leaseSetEncType=nnn[,nnn]  The encryption types to be used.
                                  Interpreted client-side, but also passed to the router in
                                  the SessionConfig, to declare intent and check support.
                                  See proposals 144 and 145.

  i2cp.leaseSetSecret=b64     The base 64 of a secret used to blind the
                              address of the leaseset, default ""

  i2cp.leaseSetAuthType=nnn       The type of authentication for encrypted LS2.
                                  0 for no per-client authentication (the default)
                                  1 for DH per-client authentication
                                  2 for PSK per-client authentication

  i2cp.leaseSetBlindedType=nnn   The sig type of the blinded key for encrypted LS2.
                                 Default depends on the destination sig type.

  i2cp.leaseSetClient.dh.nnn=b64name:b64pubkey   The base 64 of the client name (ignored, UI use only),
                                                 followed by a ':', followed by the base 64 of the public
                                                 key to use for DH per-client auth. nnn starts with 0

  i2cp.leaseSetClient.psk.nnn=b64name:b64privkey   The base 64 of the client name (ignored, UI use only),
                                                   followed by a ':', followed by the base 64 of the private
                                                   key to use for PSK per-client auth. nnn starts with 0
```
### Session Config

Note que para assinaturas offline, as opções i2cp.leaseSetOfflineExpiration, i2cp.leaseSetTransientPublicKey, e i2cp.leaseSetOfflineSignature são obrigatórias, e a assinatura é feita pela chave privada de assinatura transiente.

### Encrypted LS com Endereços Base 32

Router para cliente. Sem alterações. Os leases são enviados com timestamps de 8 bytes, mesmo se o leaseset retornado for um LS2 com timestamps de 4 bytes. Note que a resposta pode ser uma mensagem Create Leaseset ou Create Leaseset2.

### LS Criptografada com Chaves Offline

Router para cliente. Sem alterações. Os leases são enviados com timestamps de 8 bytes, mesmo que o leaseset retornado seja um LS2 com timestamps de 4 bytes. Note que a resposta pode ser uma mensagem Create Leaseset ou Create Leaseset2.

### Notas

Cliente para router. Nova mensagem, para usar no lugar da Mensagem Create Leaseset.

### Meta LS2

- Para que o router analise o tipo de armazenamento, o tipo deve estar na mensagem,
  a menos que seja passado para o router previamente na configuração da sessão.
  Para código de análise comum, é mais fácil tê-lo na própria mensagem.

- Para que o router saiba o tipo e comprimento da chave privada,
  ela deve estar após o lease set, a menos que o parser conheça o tipo antecipadamente
  na configuração da sessão.
  Para código de parsing comum, é mais fácil saber isso da própria mensagem.

- A chave privada de assinatura, previamente definida para revogação e não utilizada,
  não está presente no LS2.

### Formato

O tipo de mensagem para a Mensagem Create Leaseset2 é 41.

### Notas

```
Session ID
  Type byte: Type of lease set to follow
             Type 1 is a LS
             Type 3 is a LS2
             Type 5 is a encrypted LS2
             Type 7 is a meta LS2
  LeaseSet: type specified above
  Number of private keys to follow (1 byte)
  Encryption Private Keys: For each public key in the lease set,
                           in the same order
                           (Not present for Meta LS2)
                           - Encryption type (2 bytes, big endian)
                           - Encryption key length (2 bytes, big endian)
                           - Encryption key (number of bytes specified)
```
### Registro de Serviço

- A versão mínima do router é 0.9.39.
- A versão preliminar com tipo de mensagem 40 estava na 0.9.38, mas o formato foi alterado.
  O tipo 40 foi abandonado e não é suportado.

### Formato

- Mais alterações são necessárias para suportar LS criptografado e meta.

### Notas

Cliente para roteador. Nova mensagem.

### Lista de Serviços

- O router precisa saber se um destino está ofuscado.
  Se estiver ofuscado e usar uma autenticação secreta ou por cliente,
  ele precisa ter essa informação também.

- Uma Host Lookup de um endereço b32 de novo formato ("b33")
  informa ao router que o endereço é ofuscado, mas não há mecanismo para
  passar a chave secreta ou privada para o router na mensagem Host Lookup.
  Embora pudéssemos estender a mensagem Host Lookup para adicionar essa informação,
  é mais limpo definir uma nova mensagem.

- Precisamos de uma forma programática para o cliente informar o router.
  Caso contrário, o usuário teria que configurar manualmente cada destino.

### Formato

Antes de um cliente enviar uma mensagem para um destino blindado, ele deve procurar o "b33" em uma mensagem Host Lookup, ou enviar uma mensagem Blinding Info. Se o destino blindado requer uma autenticação secreta ou por cliente, o cliente deve enviar uma mensagem Blinding Info.

O router não envia uma resposta para esta mensagem.

### Notas

O tipo de mensagem para a Blinding Info Message é 42.

### Format

```
Session ID
  Flags:       1 byte
               Bit order: 76543210
               Bit 0: 0 for everybody, 1 for per-client
               Bits 3-1: Authentication scheme, if bit 0 is set to 1 for per-client, otherwise 000
                         000: DH client authentication (or no per-client authentication)
                         001: PSK client authentication
               Bit 4: 1 if secret required, 0 if no secret required
               Bits 7-5: Unused, set to 0 for future compatibility
  Type byte:   Endpoint type to follow
               Type 0 is a Hash
               Type 1 is a host name String
               Type 2 is a Destination
               Type 3 is a Sig Type and Signing Public Key
  Blind Type:  2 byte blinded sig type (big endian)
  Expiration:  4 bytes, big endian, seconds since epoch
  Endpoint:    Data as specified above
               For type 0: 32 byte binary hash
               For type 1: host name String
               For type 2: binary Destination
               For type 3: 2 byte sig type (big endian)
                           Signing Public Key (length as implied by sig type)
  Private Key: Only if flag bit 0 is set to 1
               A 32-byte ECIES_X25519 private key
  Secret:      Only if flag bit 4 is set to 1
               A secret String
```
### Certificados de Chave

- A versão mínima do router é 0.9.43

### Novas Estruturas Intermediárias

### Novos Tipos de NetDB

Para suportar consultas de nomes de host "b33" e retornar uma indicação se o router não tiver a informação necessária, definimos códigos de resultado adicionais para a Mensagem de Resposta de Host, como segue:

```
2: Lookup password required
   3: Private key required
   4: Lookup password and private key required
   5: Leaseset decryption failure
```
Os valores 1-255 já estão definidos como erros, portanto não há problema de compatibilidade com versões anteriores.

### Novo Tipo de Assinatura

Router para cliente. Nova mensagem.

### Justification

Um cliente não sabe a priori que um determinado Hash será resolvido para um Meta LS.

Se uma consulta de leaseset para um Destination retornar um Meta LS, o router fará a resolução recursiva. Para datagramas, o lado cliente não precisa saber; no entanto, para streaming, onde o protocolo verifica o destino no SYN ACK, ele deve saber qual é o destino "real". Portanto, precisamos de uma nova mensagem.

### Usage

O router mantém um cache para o destino real que é usado de um meta LS. Quando o cliente envia uma mensagem para um destino que resolve para um meta LS, o router verifica o cache para o destino real usado pela última vez. Se o cache estiver vazio, o router seleciona um destino do meta LS e procura o leaseset. Se a busca do leaseset for bem-sucedida, o router adiciona esse destino ao cache e envia ao cliente uma Meta Redirect Message. Isso é feito apenas uma vez, a menos que o destino expire e precise ser alterado. O cliente também deve fazer cache da informação se necessário. A Meta Redirect Message NÃO é enviada em resposta a cada SendMessage.

O router apenas envia esta mensagem para clientes com versão 0.9.47 ou superior.

O cliente não envia uma resposta para esta mensagem.

### Mensagem de Consulta de Base de Dados

O tipo de mensagem para a Meta Redirect Message é 43.

### Alterações

```
Session ID (2 bytes) The value from the Send Message.
  Message ID generated by the router (4 bytes)
  4 byte nonce previously generated by the client
               (the value from the Send Message, may be zero)
  Flags:       2 bytes, bit order 15...0
               Unused, set to 0 for future compatibility
               Bit 0: 0 - the destination is no longer meta
                      1 - the destination is now meta
               Bits 15-1: Unused, set to 0 for future compatibility
  Original Destination (387+ bytes)
  (following fields only present if flags bit 0 is 1)
  MFlags:      2 bytes
               Unused, set to 0 for future compatibility
               From the Meta Lease for the actual Destination
  Expiration:  4 bytes, big endian, seconds since epoch
               From the Meta Lease for the actual Destination
  Cost (priority) 1 byte
               From the Meta Lease for the actual Destination
  Actual (real) Destination (387+ bytes)
```
### Mensagem de Armazenamento de Base de Dados

Como gerar e suportar Meta, incluindo comunicação e coordenação entre routers, está fora do escopo desta proposta. Veja a proposta relacionada 150.

### Alterações

Assinaturas offline não podem ser verificadas em streaming ou datagramas respondíveis. Veja as seções abaixo.

## Private Key File Changes Required

O formato do arquivo de chave privada (eepPriv.dat) não é uma parte oficial de nossas especificações, mas está documentado nos [javadocs do Java I2P](http://idk.i2p/javadoc-i2p/net/i2p/data/PrivateKeyFile.html) e outras implementações o suportam. Isso permite a portabilidade de chaves privadas para diferentes implementações.

São necessárias alterações para armazenar a chave pública transitória e as informações de assinatura offline.

### Changes

```
If the signing private key is all zeros, the offline information section follows:

  - Expires timestamp
    (4 bytes, big endian, seconds since epoch, rolls over in 2106)
  - Sig type of transient Signing Public Key (2 bytes, big endian)
  - Transient Signing Public key
    (length as specified by transient sig type)
  - Signature of above three fields by offline key
    (length as specified by destination sig type)
  - Transient Signing Private key
    (length as specified by transient sig type)
```
### Opções I2CP

Adicione suporte para as seguintes opções:

```
-d days              (specify expiration in days of offline sig, default 365)
      -o offlinedestfile   (generate the online key file,
                            using the offline key file specified)
      -r sigtype           (specify sig type of transient key, default Ed25519)
```
## Streaming Changes Required

Assinaturas offline não podem ser verificadas atualmente no streaming. A alteração abaixo adiciona o bloco de assinatura offline às opções. Isso evita ter que recuperar essas informações via I2CP.

### Configuração de Sessão

```
Add new option:
  Bit:          11
  Flag:         OFFLINE_SIGNATURE
  Option order: 4
  Option data:  Variable bytes
  Function:     Contains the offline signature section from LS2.
                FROM_INCLUDED must also be set.
                Expires timestamp
                (4 bytes, big endian, seconds since epoch, rolls over in 2106)
                Transient sig type (2 bytes, big endian)
                Transient signing public key (length as implied by sig type)
                Signature of expires timestamp, transient sig type,
                and public key, by the destination public key,
                length as implied by destination public key sig type.

  Change option:
  Bit:          3
  Flag:         SIGNATURE_INCLUDED
  Option order: Change from 4 to 5

  Add information about transient keys to the
  Variable Length Signature Notes section:
  The offline signature option does not needed to be added for a CLOSE packet if
  a SYN packet containing the option was previously acked.
  More info TODO
```
### Mensagem de Solicitação de LeaseSet

- A alternativa é apenas adicionar uma flag e recuperar a chave pública transiente via I2CP
  (Veja as seções Host Lookup / Host Reply Message acima)

## Cabeçalho LS2 Padrão

As assinaturas offline não podem ser verificadas no processamento de datagrama repliable. Precisa de uma flag para indicar assinado offline, mas não há lugar para colocar uma flag. Exigirá um número de protocolo e formato completamente novos.

### Mensagem de Solicitação de Leaseset de Variável

```
Define new protocol 19 - Repliable datagram with options?
  - Destination (387+ bytes)
  - Flags (2 bytes)
    Bit order: 15 14 ... 3 2 1 0
    Bit 0: If 0, no offline keys; if 1, offline keys
    Bits 1-15: set to 0 for compatibility with future uses
  - If flag indicates offline keys, the offline signature section:
    Expires timestamp
    (4 bytes, big endian, seconds since epoch, rolls over in 2106)
    Transient sig type (2 bytes, big endian)
    Transient signing public key (length as implied by sig type)
    Signature of expires timestamp, transient sig type,
    and public key, by the destination public key,
    length as implied by destination public key sig type.
    This section can, and should, be generated offline.
  - Data
```
### Criar Mensagem Leaseset2

- Alternativa é apenas adicionar uma flag e recuperar a chave pública transitória via I2CP
  (Ver seções Host Lookup / Host Reply Message acima)
- Quaisquer outras opções que deveríamos adicionar agora que temos bytes de flag?

## SAM V3 Changes Required

SAM deve ser aprimorado para suportar assinaturas offline no DESTINATION base 64.

### Justificativa

```
Note that in the SESSION CREATE DESTINATION=$privkey,
  the $privkey raw data (before base64 conversion)
  may be optionally followed by the Offline Signature as specified in the
  Common Structures Specification.

  If the signing private key is all zeros, the offline information section follows:

  - Expires timestamp
    (4 bytes, big endian, seconds since epoch, rolls over in 2106)
  - Sig type of transient Signing Public Key (2 bytes, big endian)
  - Transient Signing Public key
    (length as specified by transient sig type)
  - Signature of above three fields by offline key
    (length as specified by destination sig type)
  - Transient Signing Private key (length as specified by transient sig type)
```
Note que assinaturas offline são suportadas apenas para STREAM e RAW, não para DATAGRAM (até que definamos um novo protocolo DATAGRAM).

Note que o SESSION STATUS retornará uma Signing Private Key de todos zeros e os dados de Offline Signature exatamente como fornecidos no SESSION CREATE.

Observe que DEST GENERATE e SESSION CREATE DESTINATION=TRANSIENT não podem ser usados para criar um destino assinado offline.

### Tipo de Mensagem

Aumentar a versão para 3.4, ou deixá-la em 3.1/3.2/3.3 para que possa ser adicionada sem exigir todas as funcionalidades da 3.2/3.3?

Outras mudanças a definir. Veja a seção I2CP Host Reply Message acima.

## BOB Changes Required

BOB teria que ser aprimorado para suportar assinaturas offline e/ou Meta LS. Esta é uma prioridade baixa e provavelmente nunca será especificada ou implementada. SAM V3 é a interface preferida.

## Publishing, Migration, Compatibility

LS2 (exceto LS2 criptografado) é publicado no mesmo local DHT que LS1. Não há maneira de publicar tanto um LS1 quanto um LS2, a menos que LS2 esteja em um local diferente.

O LS2 criptografado é publicado no hash do tipo de chave ofuscada e dados da chave. Este hash é então usado para gerar a "chave de roteamento" diária, como no LS1.

LS2 seria usado apenas quando novos recursos são necessários (nova criptografia, LS criptografado, meta, etc.). LS2 só pode ser publicado para floodfills de uma versão especificada ou superior.

Servidores que publicam LS2 saberiam que quaisquer clientes conectando suportam LS2. Eles poderiam enviar LS2 no garlic.

Os clientes enviariam LS2 em garlics apenas se estivessem usando nova criptografia. Clientes compartilhados usariam LS1 indefinidamente? TODO: Como ter clientes compartilhados que suportem tanto criptografia antiga quanto nova?

## Rollout

0.9.38 contém suporte floodfill para LS2 padrão, incluindo chaves offline.

A versão 0.9.39 contém suporte I2CP para LS2 e Encrypted LS2, assinatura/verificação do tipo de assinatura 11, suporte floodfill para Encrypted LS2 (tipos de assinatura 7 e 11, sem chaves offline), e criptografia/descriptografia LS2 (sem autorização por cliente).

A versão 0.9.40 está programada para incluir suporte para criptografar/descriptografar LS2 com autorização por cliente, suporte floodfill e I2CP para Meta LS2, suporte para LS2 criptografado com chaves offline, e suporte b32 para LS2 criptografado.

## Novos tipos de DatabaseEntry

O design criptografado do LS2 é fortemente influenciado pelos [descritores de serviços ocultos v3 do Tor](https://spec.torproject.org/rend-spec-v3), que tinham objetivos de design similares.
