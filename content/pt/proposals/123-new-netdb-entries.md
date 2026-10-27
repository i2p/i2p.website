---
title: "Novas Entradas netDB"
number: "123"
author: "zzz, str4d, orignal"
created: "2016-01-16"
lastupdated: "2020-07-18"
status: "Abrir"
thread: "http://zzz.i2p/topics/2051"
supercedes: "110, 120, 121, 122"
toc: true
---

## Status

Partes desta proposta estão completas e implementadas nas versões 0.9.38 e 0.9.39.   As Estruturas Comuns, I2CP, I2NP e outras especificações   agora estão atualizadas para refletir as mudanças que são suportadas atualmente.

As partes concluídas ainda estão sujeitas a revisões menores.   Outras partes desta proposta ainda estão em desenvolvimento   e sujeitas a revisões substanciais.

A Pesquisa de Serviço (tipos 9 e 11) tem baixa prioridade,   não está agendada e pode ser separada em uma proposta distinta.

## Visão Geral

Esta é uma atualização e agregação das seguintes 4 propostas:

- 110 LS2
- 120 Meta LS2 para multihoming massivo
- 121 LS2 Criptografado
- 122 Pesquisa de serviço não autenticada (anycasting)

Essas propostas são principalmente independentes, mas, por coerência, definimos e usamos um   formato comum para várias delas.

As seguintes propostas são parcialmente relacionadas:

- 140 Multihoming Invisível (incompatível com esta proposta)
- 142 Novo Modelo de Criptografia (para nova criptografia simétrica)
- 144 ECIES-X25519-AEAD-Ratchet
- 145 ECIES-P256
- 146 Red25519
- 148 EdDSA-BLAKE2b-Ed25519
- 149 B32 para LS2 Criptografado
- 150 Protocolo Garlic Farm
- 151 ECDSA Blinding

## Proposta

Esta proposta define 5 novos tipos de DatabaseEntry e o processo para   armazená-los e recuperá-los do banco de dados da rede,   bem como o método para assiná-los e verificar essas assinaturas.

### Objetivos

- Compatibilidade com versões anteriores
- LS2 utilizável com multihoming no estilo antigo
- Nenhuma nova criptografia ou primitivas necessárias para suporte
- Manter o desacoplamento entre criptografia e assinatura; suportar todas as versões atuais e futuras
- Habilitar chaves de assinatura offline opcionais
- Reduzir a precisão dos timestamps para reduzir fingerprinting
- Habilitar nova criptografia para destinos
- Habilitar multihoming massivo
- Corrigir múltiplos problemas com o LS criptografado existente
- Ofuscação opcional para reduzir a visibilidade pelos floodfills
- Criptografado suporta tanto chave única quanto múltiplas chaves revogáveis
- Pesquisa de serviço para facilitar a busca de outproxies, bootstrap de DHT de aplicação,  
  e outros usos
- Não quebrar nada que dependa de hashes binários de destino de 32 bytes, por exemplo, bittorrent
- Adicionar flexibilidade aos leasesets via propriedades, como temos em routerinfos.
- Colocar o timestamp de publicação e expiração variável no cabeçalho, para funcionar mesmo  
  se o conteúdo estiver criptografado (não derivar timestamp da lease mais antiga)
- Todos os novos tipos residem no mesmo espaço DHT e nas mesmas localizações dos leasesets existentes,  
  para que os usuários possam migrar do LS antigo para o LS2,  
  ou mudar entre LS2, Meta e Criptografado,  
  sem alterar o Destino ou o hash.
- Um Destino existente pode ser convertido para usar chaves offline,  
  ou voltar para chaves online, sem alterar o Destino ou o hash.

### Não-Objetivos / Fora do Escopo

- Novo algoritmo de rotação DHT ou geração de número aleatório compartilhado
- O tipo específico de nova criptografia e esquema de criptografia ponta a ponta  
  para usar esse novo tipo estaria em uma proposta separada.  
  Nenhuma nova criptografia é especificada ou discutida aqui.
- Nova criptografia para RIs ou construção de túneis.  
  Isso estaria em uma proposta separada.
- Métodos de criptografia, transmissão e recepção de mensagens I2NP DLM / DSM / DSRM.  
  Não será alterado.
- Como gerar e suportar Meta, incluindo comunicação inter-roteadores, gerenciamento, failover e coordenação.  
  O suporte pode ser adicionado ao I2CP, ou i2pcontrol, ou um novo protocolo.  
  Isso pode ou não ser padronizado.
- Como realmente implementar e gerenciar túneis com expiração mais longa, ou cancelar túneis existentes.  
  Isso é extremamente difícil, e sem isso, você não pode ter um desligamento gracioso razoável.
- Mudanças no modelo de ameaça
- Formato de armazenamento offline, ou métodos para armazenar/recuperar/compartilhar os dados.
- Detalhes de implementação não são discutidos aqui e são deixados a cada projeto.

### Justificativa

LS2 adiciona campos para alterar o tipo de criptografia e para futuras mudanças de protocolo.

LS2 Criptografado corrige vários problemas de segurança com o LS criptografado existente ao   usar criptografia assimétrica de todo o conjunto de leases.

Meta LS2 fornece multihoming flexível, eficiente, eficaz e em larga escala.

Registro de Serviço e Lista de Serviço fornecem serviços anycast como pesquisa de nomes   e bootstrap de DHT.

### Tipos de Dados NetDB

Os números de tipo são usados nas Mensagens I2NP de Pesquisa/Armazenamento no Banco de Dados.

A coluna ponta a ponta refere-se a se consultas/respostas são enviadas a um Destino em uma Mensagem de Alho.

Tipos existentes:

| NetDB Data | Tipo de Pesquisa | Tipo de Armazenamento |
|------------|------------------|-----------------------|
| any        | 0                | any                   |
| LS         | 1                | 1                     |
| RI         | 2                | 0                     |
| exploratory| 3                | DSRM                  |
Novos tipos:

| NetDB Data     | Tipo de Pesquisa | Tipo de Armazenamento | Cabeçalho LS2 Padrão? | Enviado ponta a ponta? |
|----------------|------------------|------------------------|------------------------|------------------------|
| LS2            | 1                | 3                      | sim                    | sim                    |
| LS2 Criptografado  | 1                | 5                      | não                    | não                    |
| Meta LS2       | 1                | 7                      | sim                    | não                    |
| Registro de Serviço | n/a         | 9                      | sim                    | não                    |
| Lista de Serviço   | 4                | 11                     | não                    | não                    |
### Notas

- Os tipos de pesquisa atualmente usam os bits 3-2 na Mensagem de Pesquisa no Banco de Dados.  
  Quaisquer tipos adicionais exigiriam o uso do bit 4.

- Todos os tipos de armazenamento são ímpares, pois os bits superiores no campo de tipo da Mensagem de Armazenamento no Banco de Dados  
  são ignorados por roteadores antigos.  
  Preferimos que a análise falhe como um LS do que como um RI comprimido.

- O tipo deve ser explícito, implícito ou nenhum nos dados cobertos pela assinatura?

### Processo de Pesquisa/Armazenamento

Os tipos 3, 5 e 7 podem ser retornados em resposta a uma pesquisa padrão de leaseset (tipo 1).   O tipo 9 nunca é retornado em resposta a uma pesquisa.   O tipo 11 é retornado em resposta a um novo tipo de pesquisa de serviço (tipo 11).

Apenas o tipo 3 pode ser enviado em uma mensagem de Alho cliente-cliente.

### Formato

Os tipos 3, 7 e 9 têm um formato comum::

```text
Standard LS2 Header
- as defined below

Type-Specific Part
- as defined below in each part

Standard LS2 Signature:
- Length as implied by sig type of signing key
```
Cabeçalho Padrão LS2

Parte Específica do Tipo

### Considerações de Privacidade/Segurança

Assinatura Padrão LS2:

## Cabeçalho LS2 Padrão

O tipo 5 (Criptografado) não começa com um Destino e tem um   formato diferente. Veja abaixo.

### Formato

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
### Justificativa

  - conforme definido abaixo

  - conforme definido abaixo em cada parte

  - Comprimento conforme implicado pelo tipo de assinatura da chave de assinatura

- Não publicado/publicado: Para uso ao enviar um armazenamento de banco de dados ponta a ponta,  
  o roteador remetente pode desejar indicar que este leaseset não deve ser  
  enviado a outros. Atualmente usamos heurísticas para manter esse estado.

### Problemas

- Publicado: Substitui a lógica complexa necessária para determinar a 'versão' do  
  leaseset. Atualmente, a versão é a expiração da lease com expiração mais longa, e um roteador publicador deve incrementar essa expiração em pelo menos 1ms ao  
  publicar um leaseset que apenas remove uma lease mais antiga.

- Expira: Permite que a expiração de uma entrada netdb seja anterior à  
  de sua lease com expiração mais longa. Pode não ser útil para LS2, onde os leasesets  
  são esperados para permanecer com uma expiração máxima de 11 minutos, mas  
  para outros novos tipos, é necessário (veja Meta LS e Registro de Serviço abaixo).

- Chaves offline são opcionais, para reduzir a complexidade inicial/obrigatória de implementação.

### Notas

- Poderia reduzir ainda mais a precisão do timestamp (10 minutos?) mas teria que adicionar  
  número de versão. Isso poderia quebrar multihoming, a menos que tivéssemos criptografia que preserva ordem?  
  Provavelmente não é possível sem timestamps.

- Alternativa: timestamp de 3 bytes (época / 10 minutos), versão de 1 byte, expiração de 2 bytes

- O tipo é explícito ou implícito nos dados/assinatura? Constantes "Domínio" para assinatura?

## Novos tipos DatabaseEntry

### LeaseSet 2

O tipo 11 (Lista de Serviço) é uma agregação de vários Registros de Serviço e tem um   formato diferente. Veja abaixo.

- Roteadores não devem publicar um LS mais de uma vez por segundo.  
  Se fizerem, devem artificialmente incrementar o timestamp de publicação em 1  
  em relação ao LS publicado anteriormente.

TBD

    Standard LS flag (1)
Os tipos 3, 7 e 9 usam o cabeçalho LS2 padrão, especificado abaixo:

    Standard LS2 type (3)
Mudanças do LeaseSet existente:

    Hash of destination
    This hash is then used to generate the daily "routing key", as in LS1
Pesquisa com

    10 minutes, as in a regular LS.
Armazenar com

    Destination

### Formato

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
### Justificativa

- Implementações de roteadores poderiam armazenar em cache as chaves e assinatura transitórias para  
  evitar verificação toda vez. Em particular, floodfills e roteadores nas  
  extremidades de conexões de longa duração poderiam se beneficiar disso.

- Chaves e assinatura offline são apropriadas apenas para destinos de longa duração,  
  ou seja, servidores, não clientes.

### Discussão

Armazenar em

Expiração típica

Publicado por

- Adicionar timestamp de publicação, timestamp de expiração, flags e propriedades
- Adicionar tipo de criptografia
- Remover chave de revogação

Esta proposta continua a usar a chave pública no leaseset para a   chave de criptografia ponta a ponta, e deixa o campo de chave pública no   Destino não utilizado, como está agora. O tipo de criptografia não é especificado   no certificado de chave do Destino, permanecerá 0.

- Propriedades: Expansão futura e flexibilidade.  
  Colocadas primeiro caso sejam necessárias para análise dos dados restantes.

### Novos Problemas de Criptografia

Uma alternativa rejeitada é especificar o tipo de criptografia no certificado de chave do Destino,   usar a chave pública no Destino, e não usar a chave pública   no leaseset. Não temos planos de fazer isso.

- Múltiplos pares tipo de criptografia/chave pública são  
  para facilitar a transição para novos tipos de criptografia. A outra maneira de fazer isso  
  é publicar múltiplos leasesets, possivelmente usando os mesmos túneis,  
  como fazemos agora para destinos DSA e EdDSA.  
  A identificação do tipo de criptografia de entrada em um túnel  
  pode ser feita com o mecanismo existente de tag de sessão,  
  e/ou descriptografia por tentativa usando cada chave. Os comprimentos das mensagens  
  de entrada também podem fornecer uma pista.

- Localização da chave pública real não muda.
- Tipo de criptografia ou chave pública pode mudar sem alterar o Destino.
- Remove o campo de revogação não utilizado
- Compatibilidade básica com outros tipos DatabaseEntry nesta proposta
- Permite múltiplos tipos de criptografia

- Localização da chave pública e tipo de criptografia difere do RouterInfo
- Mantém a chave pública não utilizada no leaseset
- Requer implementação em toda a rede; na alternativa, tipos experimentais de criptografia podem ser usados, se permitidos pelos floodfills  
  (mas veja propostas relacionadas 136 e 137 sobre suporte para tipos de assinatura experimentais).  
  A proposta alternativa poderia ser mais fácil de implementar e testar para tipos experimentais de criptografia.

### Notas

- O tipo de criptografia representa a combinação  
  de curva, comprimento da chave e esquema ponta a ponta,  
  incluindo KDF e MAC, se houver.

- Incluímos um campo de comprimento da chave, para que o LS2 seja  
  analisável e verificável pelo floodfill mesmo para tipos de criptografia desconhecidos.

- O primeiro novo tipo de criptografia a ser proposto provavelmente será  
  ECIES/X25519. Como ele é usado ponta a ponta  
  (ou uma versão ligeiramente modificada de ElGamal/AES+SessionTag  
  ou algo completamente novo, por exemplo, ChaCha/Poly) será especificado  
  em uma ou mais propostas separadas.  
  Veja também as propostas ECIES 144 e 145.

### LS2 Criptografado

Benefícios do LS2:

- Expiração de 8 bytes nas leases mudada para 4 bytes.

Desvantagens do LS2:

Alguns pontos estão fora do escopo desta proposta,   mas estamos colocando notas aqui por enquanto, pois ainda não temos   uma proposta de criptografia separada.   Veja também as propostas ECIES 144 e 145.

- Se implementarmos revogação no futuro, podemos fazê-lo com um campo de expiração zero,  
  ou leases zero, ou ambos. Não há necessidade de uma chave de revogação separada.

Objetivos:

    Standard LS flag (1)
LS2 Criptografado nunca é enviado em uma mensagem de alho ponta a ponta.   Use o LS2 padrão conforme acima.

    Encrypted LS2 type (5)
Mudanças do LeaseSet Criptografado existente:

    Hash of blinded sig type and blinded public key
    Two byte sig type (big endian, e.g. 0x000b) || blinded public key
    This hash is then used to generate the daily "routing key", as in LS1
Pesquisa com

    10 minutes, as in a regular LS, or hours, as in a meta LS.
Armazenar com

    Destination


### Definições

Armazenar em

Expiração típica

    n-byte output from a cryptographically-secure random number generator.

    In addition to the requirement of CSRNG being cryptographically-secure (and thus
    suitable for generating key material), it MUST be safe
    for some n-byte output to be used for key material when the byte sequences immediately
    preceding and following it are exposed on the network (such as in a salt, or encrypted
    padding). Implementations that rely on a potentially-untrustworthy source should hash
    any output that is to be exposed on the network. See [PRNG references](http://projectbullrun.org/dual-ec/ext-rand.html) and [Tor dev discussion](https://lists.torproject.org/pipermail/tor-dev/2015-November/009954.html).

Publicado por

    SHA-256 hash function that takes a personalization string p and data d, and
    produces an output of length 32 bytes.

    Use SHA-256 as follows::

        H(p, d) := SHA-256(p || d)

Definimos as seguintes funções correspondentes aos blocos criptográficos usados   para LS2 Criptografado:

    The ChaCha20 stream cipher as specified in [RFC 7539 Section 2.4](https://tools.ietf.org/html/rfc7539#section-2.4), with the initial counter
    set to 1. S_KEY_LEN = 32 and S_IV_LEN = 12.

    ENCRYPT(k, iv, plaintext)
        Encrypts plaintext using the cipher key k, and nonce iv which MUST be unique for
        the key k. Returns a ciphertext that is the same size as the plaintext.

        The entire ciphertext must be indistinguishable from random if the key is secret.

    DECRYPT(k, iv, ciphertext)
        Decrypts ciphertext using the cipher key k, and nonce iv. Returns the plaintext.


CSRNG(n)

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

H(p, d)

    X25519 public key agreement system. Private keys of 32 bytes, public keys of 32
    bytes, produces outputs of 32 bytes. It has the following
    functions:

    GENERATE_PRIVATE()
        Generates a new private key.

    DERIVE_PUBLIC(privkey)
        Returns the public key corresponding to the given private key.

    DH(privkey, pubkey)
        Generates a shared secret from the given private and public keys.

STREAM

    A cryptographic key derivation function which takes some input key material ikm (which
    should have good entropy but is not required to be a uniformly random string), a salt
    of length 32 bytes, and a context-specific 'info' value, and produces an output
    of n bytes suitable for use as key material.

    Use HKDF as specified in [RFC 5869](https://tools.ietf.org/html/rfc5869), using the HMAC hash function SHA-256
    as specified in [RFC 2104](https://tools.ietf.org/html/rfc2104). This means that SALT_LEN is 32 bytes max.


### Formato

SIG

- As chaves de criptografia estão em ordem de preferência do servidor, a mais preferida primeiro.  
  O comportamento padrão do cliente é selecionar a primeira chave com  
  um tipo de criptografia suportado. Os clientes podem usar outros algoritmos de seleção  
  com base no suporte à criptografia, desempenho relativo e outros fatores.

DH

    Layer 0 data + Enc(layer 1 data + Enc(layer 2 data)) + Signature

HKDF(salt, ikm, info, n)

O formato LS2 criptografado consiste em três camadas aninhadas:

#### Camada 0 (externa)

O formato geral é::

    1 byte

    Not actually in header, but part of data covered by signature.
    Take from field in Database Store Message.

Observe que o LS2 criptografado é ofuscado. O Destino não está no cabeçalho.   A localização de armazenamento DHT é SHA-256(tipo de assinatura || chave pública ofuscada), e rotacionada diariamente.

    2 bytes, big endian
    This will always be type 11, identifying a Red25519 blinded key.

NÃO usa o cabeçalho LS2 padrão especificado acima.

    Length as implied by sig type

Tipo

    4 bytes, big endian

    Seconds since epoch, rolls over in 2106

Tipo de Assinatura da Chave Pública Ofuscada

    2 bytes, big endian

    Offset from published timestamp in seconds, 18.2 hours max

Chave Pública Ofuscada

    2 bytes

    Bit order: 15 14 ... 3 2 1 0

    Bit 0: If 0, no offline keys; if 1, offline keys

    Other bits: set to 0 for compatibility with future uses

Timestamp de publicação

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

Expira

    2 bytes, big endian

Flags

    lenOuterCiphertext bytes

    Encrypted layer 1 data. See below for key derivation and encryption algorithms.

Dados da chave transitória

    Length as implied by sig type of the signing key used

    The signature is of everything above.

    If the flag indicates offline keys, the signature is verified with the transient
    public key. Otherwise, the signature is verified with the blinded public key.


#### Camada 1 (intermediária)

lenOuterCiphertext

    1 byte
    
    Bit order: 76543210

    Bit 0: 0 for everybody, 1 for per-client, auth section to follow

    Bits 3-1: Authentication scheme, only if bit 0 is set to 1 for per-client, otherwise 000
              000: DH client authentication (or no per-client authentication)
              001: PSK client authentication

    Bits 7-4: Unused, set to 0 for future compatibility

outerCiphertext

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

Assinatura

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


Flags

    Length implied by lenOuterCiphertext (whatever data remains)

    Encrypted layer 2 data. See below for key derivation and encryption algorithms.


#### Camada 2 (interna)

Dados de autenticação de cliente DH

    1 byte

    Either 3 (LS2) or 7 (Meta LS2)

Dados de autenticação de cliente PSK

    LeaseSet2 data for the given type.

    Includes the header and signature.


### Derivação de Chave Ofuscada

innerCiphertext

Tipo

#### Objetivos

- Adicionar ofuscação
- Permitir múltiplos tipos de assinatura
- Não exigir nenhuma nova primitiva de criptografia
- Opcionalmente criptografar para cada destinatário, revogável
- Suportar criptografia apenas de LS2 Padrão e Meta LS2

#### Segurança

Dados

#### Definições

Usamos o seguinte esquema para ofuscação de chave,   baseado em Ed25519 e [ZCash RedDSA](https://github.com/zcash/zips/tree/master/protocol/protocol.pdf).   As assinaturas Re25519 são sobre a curva Ed25519, usando SHA-512 para o hash.

    The Ed25519 base point (generator) 2^255 - 19 as in [Ed25519](http://cr.yp.to/papers.html#ed25519)

Não usamos [Tor's rend-spec-v3.txt appendix A.2](https://spec.torproject.org/rend-spec-v3),   que tem objetivos de design semelhantes, porque suas chaves públicas ofuscadas   podem estar fora do subgrupo de ordem prima, com implicações de segurança desconhecidas.

    The Ed25519 order 2^252 + 27742317777372353535851937790883648493
    as in [Ed25519](http://cr.yp.to/papers.html#ed25519)

A segurança de um esquema de ofuscação requer que a   distribuição de alpha seja a mesma das chaves privadas não ofuscadas.   No entanto, quando ofuscamos uma chave privada Ed25519 (tipo de assinatura 7)   para uma chave privada Red25519 (tipo de assinatura 11), a distribuição é diferente.   Para atender aos requisitos da [zcash seção 4.1.6.1](https://github.com/zcash/zips/tree/master/protocol/protocol.pdf),   Red25519 (tipo de assinatura 11) deve ser usado também para as chaves não ofuscadas, para que   "a combinação de uma chave pública re-randomizada e assinatura(s)   sob essa chave não revele a chave da qual foi re-randomizada."   Permitimos o tipo 7 para destinos existentes, mas recomendamos   o tipo 11 para novos destinos que serão criptografados.

    Convert a private key to public, as in Ed25519 (mulitply by G)

B

    A 32-byte random number known to those who know the destination.

L

    Generate alpha for the current date, for those who know the destination and the secret.
    The result must be identically distributed as Ed25519 private keys.

DERIVE_PUBLIC(a)

    The unblinded 32-byte EdDSA or RedDSA signing private key used to sign the destination

alpha

    The unblinded 32-byte EdDSA or RedDSA signing public key in the destination,
    = DERIVE_PUBLIC(a), as in Ed25519

GENERATE_ALPHA(destination, date, secret)

    The blinded 32-byte EdDSA signing private key used to sign the encrypted leaseset
    This is a valid EdDSA private key.

a

    The blinded 32-byte EdDSA signing public key in the Destination,
    may be generated with DERIVE_PUBLIC(a'), or from A and alpha.
    This is a valid EdDSA public key, on the curve and on the prime-order subgroup.

A

    Flip the order of the input bytes to little-endian

a'

    32 bytes = (LEOS2IP(SHA512(x))) mod B, same as in Ed25519 hash-and-reduce


#### Cálculos de Ofuscação

A'

LEOS2IP(x)

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
H*(x)

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
Uma nova chave secreta alpha e chaves ofuscadas devem ser geradas a cada dia (UTC).   A chave secreta alpha e as chaves ofuscadas são calculadas da seguinte forma.

```text
// BLIND_PUBKEY()

  alpha = GENERATE_ALPHA(destination, date, secret)
  A = destination's signing public key
  // Addition using group elements (points on the curve)
  blinded public key = A' = BLIND_PUBKEY(A, alpha) = A + DERIVE_PUBLIC(alpha)
```
GENERATE_ALPHA(destination, date, secret), para todas as partes:

#### Assinatura

BLIND_PRIVKEY(), para o proprietário publicando o leaseset:

BLIND_PUBKEY(), para os clientes recuperando o leaseset:

Ambos os métodos de cálculo de A' produzem o mesmo resultado, conforme exigido.

O leaseset não ofuscado é assinado pela chave privada de assinatura Ed25519 ou Red25519 não ofuscada   e verificado com a chave pública de assinatura Ed25519 ou Red25519 não ofuscada (tipos de assinatura 7 ou 11) conforme o usual.

#### Cálculos de Assinatura/Verificação

Se a chave pública de assinatura estiver offline,   o leaseset não ofuscado é assinado pela chave privada de assinatura transitória Ed25519 ou Red25519 não ofuscada   e verificado com a chave pública de assinatura transitória Ed25519 ou Red25519 não ofuscada (tipos de assinatura 7 ou 11) conforme o usual.   Veja abaixo para notas adicionais sobre chaves offline para leasesets criptografados.

Para assinatura do leaseset criptografado, usamos Red25519, baseado em [RedDSA](https://github.com/zcash/zips/tree/master/protocol/protocol.pdf)   para assinar e verificar com chaves ofuscadas.   As assinaturas Red25519 são sobre a curva Ed25519, usando SHA-512 para o hash.

Red25519 é idêntico ao Ed25519 padrão, exceto conforme especificado abaixo.

A parte externa do leaseset criptografado usa chaves e assinaturas Red25519.

Red25519 é quase idêntico ao Ed25519. Existem duas diferenças:

```text
T = 80 random bytes
  r = H*(T || publickey || message)
  // rest is the same as in Ed25519
```
Chaves privadas Red25519 são geradas a partir de números aleatórios e então devem ser reduzidas mod L, onde L é definido acima.   Chaves privadas Ed25519 são geradas a partir de números aleatórios e então "ajustadas" usando   máscara bit a bit para os bytes 0 e 31. Isso não é feito para Red25519.   As funções GENERATE_ALPHA() e BLIND_PRIVKEY() definidas acima geram chaves privadas Red25519 adequadas usando mod L.

```text
// same as in Ed25519
```
### Criptografia e processamento

#### Derivação de subcredenciais

Em Red25519, o cálculo de r para assinatura usa dados aleatórios adicionais,   e usa o valor da chave pública em vez do hash da chave privada.   Por causa dos dados aleatórios, cada assinatura Red25519 é diferente, mesmo   ao assinar os mesmos dados com a mesma chave.

```text
A = destination's signing public key
  stA = signature type of A, 2 bytes big endian (0x0007 or 0x000b)
  stA' = signature type of A', 2 bytes big endian (0x000b)
  keydata = A || stA || stA'
  credential = H("credential", keydata)
```
Assinatura:

Verificação:

```text
subcredential = H("subcredential", credential || blindedPublicKey)
```
Como parte do processo de ofuscação, precisamos garantir que um LS2 criptografado só possa ser   descriptografado por alguém que conheça a chave pública de assinatura do Destino correspondente.   O Destino completo não é necessário.   Para alcançar isso, derivamos uma credencial a partir da chave pública de assinatura:

#### Criptografia da Camada 1

A string de personalização garante que a credencial não colida com nenhum hash usado   como chave de pesquisa DHT, como o hash simples do Destino.

```text
outerInput = subcredential || publishedTimestamp
```
Para uma chave ofuscada dada, podemos então derivar uma subcredencial:

```text
outerSalt = CSRNG(32)
```
A subcredencial é incluída nos processos de derivação de chave abaixo, o que vincula essas   chaves ao conhecimento da chave pública de assinatura do Destino.

```text
keys = HKDF(outerSalt, outerInput, "ELS2_L1K", 44)
  outerKey = keys[0:31]
  outerIV = keys[32:43]
```
Primeiro, a entrada para o processo de derivação de chave é preparada:

```text
outerCiphertext = outerSalt || ENCRYPT(outerKey, outerIV, outerPlaintext)
```
#### Descriptografia da Camada 1

Em seguida, um sal aleatório é gerado:

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
Finalmente, o texto claro da camada 1 é criptografado e serializado:

```text
outerPlaintext = DECRYPT(outerKey, outerIV, outerCiphertext[32:end])
```
#### Criptografia da Camada 2

O sal é analisado a partir do texto cifrado da camada 1:

Então a chave usada para criptografar a camada 1 é derivada:

```text
innerInput = authCookie || subcredential || publishedTimestamp
  innerSalt = CSRNG(32)
  keys = HKDF(innerSalt, innerInput, "ELS2_L2K", 44)
  innerKey = keys[0:31]
  innerIV = keys[32:43]
  innerCiphertext = innerSalt || ENCRYPT(innerKey, innerIV, innerPlaintext)
```
#### Descriptografia da Camada 2

Finalmente, o texto cifrado da camada 1 é descriptografado:

Quando a autorização do cliente está habilitada, ``authCookie`` é calculado conforme descrito abaixo.   Quando a autorização do cliente está desabilitada, ``authCookie`` é o array de bytes de comprimento zero.

```text
innerInput = authCookie || subcredential || publishedTimestamp
  innerSalt = innerCiphertext[0:31]
  keys = HKDF(innerSalt, innerInput, "ELS2_L2K", 44)
  innerKey = keys[0:31]
  innerIV = keys[32:43]
  innerPlaintext = DECRYPT(innerKey, innerIV, innerCiphertext[32:end])
```
### Autorização por cliente

A criptografia prossegue de forma semelhante à camada 1:

Quando a autorização do cliente está habilitada, ``authCookie`` é calculado conforme descrito abaixo.   Quando a autorização do cliente está desabilitada, ``authCookie`` é o array de bytes de comprimento zero.

#### Autorização de cliente DH

A descriptografia prossegue de forma semelhante à camada 1:

Quando a autorização do cliente está habilitada para um Destino, o servidor mantém uma lista de   clientes que estão autorizados a descriptografar os dados do LS2 criptografado. Os dados armazenados por cliente   dependem do mecanismo de autorização e incluem alguma forma de material de chave que cada   cliente gera e envia ao servidor por um mecanismo seguro fora da banda.

```text
authCookie = CSRNG(32)
  esk = GENERATE_PRIVATE()
  epk = DERIVE_PUBLIC(esk)
```
Existem duas alternativas para implementar a autorização por cliente:

```text
sharedSecret = DH(esk, cpk_i)
  authInput = sharedSecret || cpk_i || subcredential || publishedTimestamp
  okm = HKDF(epk, authInput, "ELS2_XCA", 52)
  clientKey_i = okm[0:31]
  clientIV_i = okm[32:43]
  clientID_i = okm[44:51]
  clientCookie_i = ENCRYPT(clientKey_i, clientIV_i, authCookie)
```
Cada cliente gera um par de chaves DH ``[csk_i, cpk_i]``, e envia a chave pública ``cpk_i``   ao servidor.

Processamento do servidor   ^^^^^^^^^^^^^^^^^ O servidor gera um novo ``authCookie`` e um par de chaves DH efêmero:

```text
sharedSecret = DH(csk_i, epk)
  authInput = sharedSecret || cpk_i || subcredential || publishedTimestamp
  okm = HKDF(epk, authInput, "ELS2_XCA", 52)
  clientKey_i = okm[0:31]
  clientIV_i = okm[32:43]
  clientID_i = okm[44:51]
```
Então, para cada cliente autorizado, o servidor criptografa ``authCookie`` para sua chave pública:

```text
authCookie = DECRYPT(clientKey_i, clientIV_i, clientCookie_i)
```
#### Autorização de cliente com chave pré-compartilhada

O servidor coloca cada tupla ``[clientID_i, clientCookie_i]`` na   camada 1 do LS2 criptografado, junto com ``epk``.

Processamento do cliente   ^^^^^^^^^^^^^^^^^ O cliente usa sua chave privada para derivar seu identificador de cliente esperado ``clientID_i``,   chave de criptografia ``clientKey_i`` e IV de criptografia ``clientIV_i``:

```text
authCookie = CSRNG(32)
  authSalt = CSRNG(32)
```
Então o cliente procura nos dados de autorização da camada 1 uma entrada que contenha   ``clientID_i``. Se uma entrada correspondente existir, o cliente a descriptografa para obter   ``authCookie``:

```text
authInput = psk_i || subcredential || publishedTimestamp
  okm = HKDF(authSalt, authInput, "ELS2PSKA", 52)
  clientKey_i = okm[0:31]
  clientIV_i = okm[32:43]
  clientID_i = okm[44:51]
  clientCookie_i = ENCRYPT(clientKey_i, clientIV_i, authCookie)
```
Cada cliente gera uma chave secreta de 32 bytes ``psk_i``, e a envia ao servidor.   Alternativamente, o servidor pode gerar a chave secreta e enviá-la a um ou mais clientes.

Processamento do servidor   ^^^^^^^^^^^^^^^^^ O servidor gera um novo ``authCookie`` e sal:

```text
authInput = psk_i || subcredential || publishedTimestamp
  okm = HKDF(authSalt, authInput, "ELS2PSKA", 52)
  clientKey_i = okm[0:31]
  clientIV_i = okm[32:43]
  clientID_i = okm[44:51]
```
Então, para cada cliente autorizado, o servidor criptografa ``authCookie`` para sua chave pré-compartilhada:

```text
authCookie = DECRYPT(clientKey_i, clientIV_i, clientCookie_i)
```
#### Considerações de segurança

O servidor coloca cada tupla ``[clientID_i, clientCookie_i]`` na   camada 1 do LS2 criptografado, junto com ``authSalt``.

Processamento do cliente   ^^^^^^^^^^^^^^^^^ O cliente usa sua chave pré-compartilhada para derivar seu identificador de cliente esperado ``clientID_i``,   chave de criptografia ``clientKey_i`` e IV de criptografia ``clientIV_i``:

Então o cliente procura nos dados de autorização da camada 1 uma entrada que contenha   ``clientID_i``. Se uma entrada correspondente existir, o cliente a descriptografa para obter   ``authCookie``:

Ambos os mecanismos de autorização de cliente acima fornecem privacidade para a associação de clientes.   Uma entidade que conhece apenas o Destino pode ver quantos clientes estão inscritos em um determinado   momento, mas não pode rastrear quais clientes estão sendo adicionados ou revogados.

- Criptografar tudo por segurança
- Criptografar com segurança, não apenas com AES.
- Criptografar para cada destinatário

Os servidores DEVEM embaralhar a ordem dos clientes cada vez que geram um LS2 criptografado, para   impedir que os clientes descubram sua posição na lista e infiram quando outros clientes foram adicionados ou revogados.

- Uma camada externa contendo as informações em texto claro necessárias para armazenamento e recuperação.
- Uma camada intermediária que lida com autenticação do cliente.
- Uma camada interna que contém os dados reais do LS2.

Um servidor PODE optar por ocultar o número de clientes inscritos inserindo entradas aleatórias na   lista de dados de autorização.

- A chave pública de assinatura no destino não ofuscado deve ser  
  Ed25519 (tipo de assinatura 7) ou Red25519 (tipo de assinatura 11);  
  nenhum outro tipo de assinatura é suportado  
- Se a chave pública de assinatura estiver offline, a chave pública de assinatura transitória também deve ser Ed25519  
- Ofuscação é computacionalmente simples  
- Usar primitivas criptográficas existentes  
- Chaves públicas ofuscadas não podem ser desofuscadas  
- Chaves públicas ofuscadas devem estar na curva Ed25519 e no subgrupo de ordem prima  
- Deve-se conhecer a chave pública de assinatura do destino  
  (destino completo não necessário) para derivar a chave pública ofuscada  
- Opcionalmente fornecer um segredo adicional necessário para derivar a chave pública ofuscada

Vantagens da autorização de cliente DH   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- A segurança do esquema não depende exclusivamente da troca fora da banda do material de chave do cliente. A chave privada do cliente nunca precisa sair de seu dispositivo, e assim um  
  adversário que consiga interceptar a troca fora da banda, mas não consiga quebrar o algoritmo DH,  
  não poderá descriptografar o LS2 criptografado, nem determinar por quanto tempo o cliente tem acesso.

### LS Criptografado com Endereços Base 32

Desvantagens da autorização de cliente DH   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Vantagens da autorização de cliente PSK   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

### LS Criptografado com Chaves Offline

Desvantagens da autorização de cliente PSK   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Veja a proposta 149.

Você não pode usar um LS2 criptografado para bittorrent, por causa das respostas compactas de anúncio que têm 32 bytes.   Os 32 bytes contêm apenas o hash. Não há espaço para indicar que o   leaseset está criptografado, ou os tipos de assinatura.

### Notas

- Requer N + 1 operações DH no lado do servidor para N clientes.
- Requer uma operação DH no lado do cliente.
- Requer que o cliente gere a chave secreta.

- Não requer operações DH.
- Permite que o servidor gere a chave secreta.
- Permite que o servidor compartilhe a mesma chave com vários clientes, se desejado.

- A segurança do esquema depende criticamente da troca fora da banda do material de chave do cliente. Um adversário que intercepte a troca para um cliente específico pode descriptografar  
  qualquer LS2 criptografado subsequente para o qual esse cliente esteja autorizado, bem como determinar  
  quando o acesso do cliente é revogado.

- Um serviço usando leasesets criptografados publicaria a versão criptografada nos  
  floodfills. No entanto, por eficiência, enviaria leasesets não criptografados aos  
  clientes na mensagem de alho encapsulada, uma vez autenticado (via lista branca, por  
  exemplo).

- Floodfills podem limitar o tamanho máximo a um valor razoável para evitar abusos.

### Meta LS2

Para leasesets criptografados com chaves offline, as chaves privadas ofuscadas também devem ser geradas offline,   uma para cada dia.

Como o bloco opcional de assinatura offline está na parte em texto claro do leaseset criptografado,   qualquer pessoa que colete dados dos floodfills poderia usar isso para rastrear o leaseset (mas não descriptografá-lo)   por vários dias.   Para evitar isso, o proprietário das chaves deve gerar novas chaves transitórias   para cada dia também.   Ambas as chaves transitórias e ofuscadas podem ser geradas com antecedência e entregues ao roteador   em lote.

Não há formato de arquivo definido nesta proposta para empacotar múltiplas chaves transitórias e   ofuscadas e fornecê-las ao cliente ou roteador.   Não há melhoria no protocolo I2CP definida nesta proposta para suportar   leasesets criptografados com chaves offline.

Isso é usado para substituir multihoming. Como qualquer leaseset, isso é assinado pelo   criador. É uma lista autenticada de hashes de destino.

O Meta LS2 é o topo de, e possivelmente nós intermediários de,   uma estrutura em árvore.   Contém vários registros, cada um apontando para um LS, LS2 ou outro Meta LS2   para suportar multihoming massivo.   Um Meta LS2 pode conter uma mistura de entradas LS, LS2 e Meta LS2.   As folhas da árvore são sempre um LS ou LS2.   A árvore é um DAG; loops são proibidos; clientes que fazem pesquisas devem detectar e   recusar-se a seguir loops.

Um Meta LS2 pode ter uma expiração muito mais longa que um LS ou LS2 padrão.   O nível superior pode ter uma expiração várias horas após a data de publicação.   O tempo máximo de expiração será imposto por floodfills e clientes, e é TBD.

O caso de uso para Meta LS2 é multihoming massivo, mas sem mais   proteção contra correlação de roteadores com leasesets (na reinicialização do roteador) do que   é fornecida atualmente com LS ou LS2.   Isso é equivalente ao caso de uso "facebook", que provavelmente não precisa   de proteção contra correlação. Este caso de uso provavelmente precisa de chaves offline,   que são fornecidas no cabeçalho padrão em cada nó da árvore.

O protocolo de back-end para coordenação entre os roteadores folha, signatários intermediários e mestres do Meta LS   não é especificado aqui. Os requisitos são extremamente simples - apenas verificar se o peer está ativo,   e publicar um novo LS a cada poucas horas. A única complexidade é para escolher novos   publicadores para os Meta LS de nível superior ou intermediário em caso de falha.

Leasesets mistos onde leases de múltiplos roteadores são combinados, assinados e publicados   em um único leaseset são documentados na proposta 140, "multihoming invisível".   Esta proposta é inviável como escrita, porque conexões de streaming não seriam   "aderentes" a um único roteador, veja http://zzz.i2p/topics/2335 .

O protocolo de back-end, e a interação com os componentes internos do roteador e cliente, seria   muito complexo para multihoming invisível.

    Standard LS flag (1)
Para evitar sobrecarregar o floodfill para o Meta LS de nível superior, a expiração deve   ser de várias horas no mínimo. Os clientes devem armazenar em cache o Meta LS de nível superior e mantê-lo   entre reinicializações se não expirado.

    Meta LS2 type (7)
Precisamos definir algum algoritmo para os clientes percorrerem a árvore, incluindo fallbacks,   para que o uso seja disperso. Alguma função de distância de hash, custo e aleatoriedade.   Se um nó tiver tanto LS ou LS2 quanto Meta LS, precisamos saber quando é permitido   usar esses leasesets, e quando continuar percorrendo a árvore.

    Hash of destination
    This hash is then used to generate the daily "routing key", as in LS1
Pesquisa com

    Hours. Max 18.2 hours (65535 seconds)
Armazenar com

    "master" Destination or coordinator, or intermediate coordinators

### Formato

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
Armazenar em

### Notas

- Após a descriptografia, várias verificações devem ser feitas, incluindo que  
  o timestamp interno e a expiração correspondam aos do nível superior.

- ChaCha20 foi selecionado em vez de AES. Embora as velocidades sejam semelhantes se o  
  suporte de hardware AES estiver disponível, ChaCha20 é 2,5-3 vezes mais rápido quando  
  o suporte de hardware AES não está disponível, como em dispositivos ARM de baixo desempenho.

- Não nos preocupamos o suficiente com velocidade para usar BLAKE2b com chave. Ele tem um tamanho de saída  
  grande o suficiente para acomodar o maior n que exigimos (ou podemos chamá-lo uma vez por  
  chave desejada com um argumento contador). BLAKE2b é muito mais rápido que SHA-256, e  
  BLAKE2b com chave reduziria o número total de chamadas à função hash.  
  No entanto, veja a proposta 148, onde é proposto que mudemos para BLAKE2b por outros motivos.  
  Veja [Secure key derivation performance](https://www.lvh.io/posts/secure-key-derivation-performance.html).

### Registro de Serviço

Expiração típica

Publicado por

Flags e propriedades: para uso futuro

    n/a, see Service List
Este é um registro individual dizendo que um destino está participando de um   serviço. É enviado do participante para o floodfill. Nunca é enviado   individualmente por um floodfill, mas apenas como parte de uma Lista de Serviço. O Registro de Serviço também é usado para revogar a participação em um serviço, definindo a   expiração como zero.

    Service Record type (9)
Isso não é um LS2, mas usa o formato padrão de cabeçalho e assinatura LS2.

    Hash of service name
    This hash is then used to generate the daily "routing key", as in LS1
Pesquisa com

    Hours. Max 18.2 hours (65535 seconds)
Armazenar com

    Destination

### Formato

```
Standard LS2 Header as specified above

  Service Record Type-Specific Part
  - Port (2 bytes, big endian) (0 if unspecified)
  - Hash of service name (32 bytes)

  Standard LS2 Signature:
  - Signature (40+ bytes)
    The signature is of everything above.
```
### Notas

- Um serviço distribuído usando isso teria um ou mais "mestres" com a  
  chave privada do destino do serviço. Eles (fora da banda) determinariam a  
  lista atual de destinos ativos e publicariam o Meta LS2. Para  
  redundância, múltiplos mestres poderiam multihoming (ou seja, publicar simultaneamente) o  
  Meta LS2.

- Um serviço distribuído poderia começar com um único destino ou usar multihoming no estilo antigo,  
  então migrar para um Meta LS2. Uma pesquisa LS padrão poderia retornar  
  qualquer um de LS, LS2 ou Meta LS2.

- Quando um serviço usa um Meta LS2, ele não tem túneis (leases).

### Lista de Serviço

Armazenar em

Expiração típica

Publicado por

Isso não é nada parecido com um LS2 e usa um formato diferente.

A lista de serviço é criada e assinada pelo floodfill. É não autenticada   no sentido de que qualquer pessoa pode participar de um serviço publicando um Registro de Serviço para um   floodfill.

Uma Lista de Serviço contém Registros de Serviço Curto, não Registros de Serviço completos. Estes   contêm assinaturas, mas apenas hashes, não destinos completos, então não podem ser   verificados sem o destino completo.

    Service List lookup type (11)
A segurança, se houver, e a desejabilidade das listas de serviço são TBD.   Floodfills poderiam limitar publicação e pesquisas a uma lista branca de serviços,   mas essa lista branca pode variar com base na implementação ou preferência do operador.   Pode não ser possível alcançar consenso sobre uma lista branca comum e básica   entre implementações.

    Service List type (11)
Se o nome do serviço estiver incluído no registro de serviço acima,   então operadores de floodfill podem objetar; se apenas o hash estiver incluído,   não há verificação, e um registro de serviço poderia "entrar" antes de   qualquer outro tipo netdb e ser armazenado no floodfill.

    Hash of service name
    This hash is then used to generate the daily "routing key", as in LS1
Pesquisa com

    Hours, not specified in the list itself, up to local policy
Armazenar com

    Nobody, never sent to floodfill, never flooded.

### Formato

Armazenar em

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
Expiração típica

- Se expira for todo zero, o floodfill deve revogar o registro e não incluí-lo mais  
  na lista de serviço.

Publicado por

- Armazenamento: O floodfill pode limitar estritamente o armazenamento desses registros e  
  limitar o número de registros armazenados por hash e sua expiração. Uma lista branca  
  de hashes também pode ser usada.

NÃO usa o cabeçalho LS2 padrão especificado acima.

- Qualquer outro tipo netdb no mesmo hash tem prioridade, então um registro de serviço nunca pode  
  sobrescrever um LS/RI, mas um LS/RI sobrescreverá todos os registros de serviço nesse hash.

### Notas

- pré-anexar o hash do nome do serviço
- remover o hash do criador
- Verificar assinatura do conteúdo modificado

- Buscar destino
- Verificar assinatura de (timestamp de publicação + expira + flags + porta + Hash do  
  nome do serviço)

- Buscar destino
- Verificar assinatura de (timestamp de publicação + 4 bytes zero + flags + porta + Hash  
  do nome do serviço)

## Alterações Necessárias na Especificação de Estruturas Comuns

### Certificados de Chave

Para verificar a assinatura da Lista de Serviço:

### Novas Estruturas Intermediárias

Para verificar a assinatura de cada Registro de Serviço Curto:

### Novos Tipos de NetDB

Para verificar a assinatura de cada Registro de Revogação:

### Novo Tipo de Assinatura

Adicionar RedDSA_SHA512_Ed25519 Tipo 11. A chave pública tem 32 bytes; a chave privada tem 32 bytes; o hash tem 64 bytes; a assinatura tem 64 bytes.

## Alterações necessárias na especificação de criptografia

Fora do escopo desta proposta. Ver propostas 144 e 145.

## Alterações necessárias no I2NP

Adicionar nota: LS2 só pode ser publicado para floodfills com uma versão mínima.

### Mensagem de consulta ao banco de dados

Adicione o tipo de consulta da lista de serviços.

### Alterações

```
Flags byte: Lookup type field, currently bits 3-2, expands to bits 4-2.
  Lookup type 0x04 is defined as the service list lookup.

  Add note: Service list loookup may only be sent to floodfills with a minimum version.
  Minimum version is 0.9.38.
```
### Mensagem Database Store

Adicione todos os novos tipos de armazenamento.

### Alterações

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
## Alterações necessárias no I2CP

### Opções do I2CP

Novas opções interpretadas no lado do router, enviadas no SessionConfig Mapping:

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
Novas opções interpretadas no lado do cliente:

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
### Configuração de Sessão

Observe que, para assinaturas offline, as opções i2cp.leaseSetOfflineExpiration, i2cp.leaseSetTransientPublicKey e i2cp.leaseSetOfflineSignature são obrigatórias, e a assinatura é feita pela chave privada de assinatura transitória.

### Mensagem de Solicitação de LeaseSet

Do router para o cliente. Sem alterações. Os leases são enviados com timestamps de 8 bytes, mesmo que o leaseset retornado seja um LS2 com timestamps de 4 bytes. Observe que a resposta pode ser uma mensagem Create Leaseset ou Create Leaseset2.

### Mensagem de solicitação de leaseSet variável

Do router para o cliente. Sem alterações. Os leases são enviados com timestamps de 8 bytes, mesmo que o leaseset retornado seja um LS2 com timestamps de 4 bytes. Observe que a resposta pode ser uma mensagem Create Leaseset ou Create Leaseset2.

### Criar Mensagem Leaseset2

Cliente para router. Nova mensagem, para usar no lugar de Create Leaseset Message.

### Justificativa

- Usamos comprimento da assinatura em vez de tipo de assinatura para suportar tipos de assinatura desconhecidos.

- Não há expiração de uma lista de serviço, os destinatários podem tomar sua própria  
  decisão com base na política ou na expiração dos registros individuais.

- Listas de Serviço não são inundadas, apenas Registros de Serviço individuais são. Cada  
  floodfill cria, assina e armazena em cache uma Lista de Serviço. O floodfill usa sua  
  própria política para tempo de cache e número máximo de registros de serviço e revogação.

### Tipo de Mensagem

O tipo de mensagem para a Create Leaseset2 Message é 41.

### Formato

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
### Notas

- A versão mínima do router é 0.9.39.
- A versão preliminar com tipo de mensagem 40 estava na 0.9.38, mas o formato foi alterado.
  O tipo 40 foi abandonado e não é suportado.

### Problemas

- São necessárias mais alterações para suportar LS criptografados e meta LS.

### Mensagem de Informações de Blinding

Cliente para router. Nova mensagem.

### Justificativa

- O router precisa saber se um destination está blinded.
  Se estiver blinded e usar autenticação secreta ou por cliente,
  também precisa ter essa informação.

- Uma Host Lookup de um endereço b32 de novo formato ("b33")
  informa ao router que o endereço está blinded, mas não há mecanismo para
  passar a chave secreta ou privada ao router na mensagem Host Lookup.
  Embora pudéssemos estender a mensagem Host Lookup para adicionar essa informação,
  é mais limpo definir uma nova mensagem.

- Precisamos de uma forma programática para o client informar o router.
  Caso contrário, o usuário teria que configurar manualmente cada destination.

### Uso

Antes que um cliente envie uma mensagem para um destino cegado, ele deve consultar o "b33" em uma mensagem Host Lookup ou enviar uma mensagem Blinding Info. Se o destino cegado exigir um segredo ou autenticação por cliente, o cliente deverá enviar uma mensagem Blinding Info.

O router não envia uma resposta a esta mensagem.

### Tipo de Mensagem

O tipo de mensagem da Blinding Info Message é 42.

### Formato

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
### Notas

- A versão mínima do router é 0.9.43

### Problemas

### Mensagem de Resposta do Host (enc)

Para oferecer suporte a consultas de nomes de host "b33" e retornar uma indicação caso o router não tenha as informações necessárias, definimos códigos de resultado adicionais para a Host Reply Message, conforme segue:

```
2: Lookup password required
   3: Private key required
   4: Lookup password and private key required
   5: Leaseset decryption failure
```
Os valores 1-255 já estão definidos como erros, portanto não há problema de compatibilidade com versões anteriores.

### Mensagem de redirecionamento Meta

Do router para o cliente. Nova mensagem.

### Justificativa

Um cliente não sabe a priori que um determinado Hash será resolvido para um Meta LS.

Se uma consulta de leaseset para um Destination retornar um Meta LS, o router fará a resolução recursiva. Para datagramas, o lado do cliente não precisa saber; no entanto, para streaming, em que o protocolo verifica o destino no SYN ACK, ele precisa saber qual é o destino "real". Portanto, precisamos de uma nova mensagem.

### Uso

O router mantém um cache para o destino real usado a partir de um meta LS. Quando o cliente envia uma mensagem para um destino que resolve para um meta LS, o router verifica no cache o último destino real usado. Se o cache estiver vazio, o router seleciona um destino do meta LS e consulta o leaseset. Se a consulta ao leaseset for bem-sucedida, o router adiciona esse destino ao cache e envia ao cliente uma Meta Redirect Message. Isso é feito apenas uma vez, a menos que o destino expire e precise ser alterado. O cliente também deve armazenar as informações em cache, se necessário. A Meta Redirect Message NÃO é enviada em resposta a cada SendMessage.

O router só envia esta mensagem para clientes com versão 0.9.47 ou superior.

O cliente não envia uma resposta a esta mensagem.

### Tipo de Mensagem

O tipo de mensagem da Meta Redirect Message é 43.

### Formato

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
### Alterações para suporte à Meta

Como gerar e suportar Meta, incluindo comunicação e coordenação entre routers, está fora do escopo desta proposta. Ver proposta relacionada 150.

### Alterações para suportar chaves offline

Assinaturas offline não podem ser verificadas em streaming ou datagramas repliable. Consulte as seções abaixo.

## Alterações necessárias no arquivo de chave privada

O formato do arquivo de chave privada (eepPriv.dat) não é uma parte oficial das nossas especificações, mas está documentado nos [javadocs do Java I2P](http://idk.i2p/javadoc-i2p/net/i2p/data/PrivateKeyFile.html) e outras implementações oferecem suporte a ele. Isso possibilita a portabilidade das chaves privadas entre diferentes implementações.

São necessárias alterações para armazenar a chave pública transitória e as informações de assinatura offline.

### Alterações

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
### Alterações Necessárias no CLI do Arquivo de Chave Privada

Adicionar suporte para as seguintes opções:

```
-d days              (specify expiration in days of offline sig, default 365)
      -o offlinedestfile   (generate the online key file,
                            using the offline key file specified)
      -r sigtype           (specify sig type of transient key, default Ed25519)
```
## Alterações de streaming necessárias

Atualmente, não é possível verificar assinaturas offline em streaming. A alteração abaixo adiciona o bloco de assinatura offline às opções. Isso evita ter que recuperar essa informação via I2CP.

### Alterações

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
### Notas

- A alternativa é apenas adicionar um flag e recuperar a chave pública transitória via I2CP
  (Ver as seções Host Lookup / Host Reply Message acima)

## Alterações necessárias em datagramas com resposta

Assinaturas offline não podem ser verificadas no processamento de datagramas replicáveis. É necessária uma flag para indicar que foram assinados offline, mas não há onde colocar essa flag. Será necessário um número de protocolo e um formato completamente novos.

### Alterações

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
### Notas

- A alternativa é apenas adicionar um flag e recuperar a chave pública transitória via I2CP
  (Ver as seções Host Lookup / Host Reply Message acima)
- Alguma outra opção que devemos adicionar agora que temos bytes de flag?

## Alterações Necessárias no SAM V3

O SAM deve ser aprimorado para suportar assinaturas offline no DESTINATION em base 64.

### Alterações

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
Observe que as assinaturas offline são suportadas apenas para STREAM e RAW, não para DATAGRAM (até que definamos um novo protocolo DATAGRAM).

Observe que o SESSION STATUS retornará uma Signing Private Key com todos os zeros e os dados de Offline Signature exatamente como fornecidos no SESSION CREATE.

Observe que DEST GENERATE e SESSION CREATE DESTINATION=TRANSIENT não podem ser usados para criar um destino assinado offline.

### Problemas

Incrementar a versão para 3.4 ou mantê-la em 3.1/3.2/3.3 para que possa ser adicionado sem exigir todas as dependências das versões 3.2/3.3?

Outras alterações a definir. Consulte a seção I2CP Host Reply Message acima.

## Alterações necessárias no BOB

O BOB precisaria ser aprimorado para oferecer suporte a assinaturas offline e/ou Meta LS. Isso é de baixa prioridade e provavelmente nunca será especificado ou implementado. O SAM V3 é a interface preferida.

## Publicação, Migração, Compatibilidade

O LS2 (exceto o LS2 criptografado) é publicado na mesma localização da DHT que o LS1. Não há forma de publicar tanto um LS1 como um LS2, a menos que o LS2 estivesse numa localização diferente.

O LS2 criptografado é publicado no hash do tipo de chave cegada e dos dados da chave. Esse hash é então usado para gerar a "chave de roteamento" diária, como no LS1.

O LS2 só seria usado quando novos recursos forem necessários (nova criptografia, LS criptografado, meta, etc.). O LS2 só pode ser publicado para floodfills de uma versão especificada ou superior.

Os servidores que publicam LS2 saberiam que quaisquer clientes que se conectem suportam LS2. Eles poderiam enviar LS2 no garlic.

Os clientes enviariam LS2 em garlics somente se estivessem usando novo crypto. Clientes compartilhados usariam LS1 indefinidamente? TODO: Como ter clientes compartilhados que suportam tanto o antigo quanto o novo crypto?

## Implantação

A versão 0.9.38 contém suporte a floodfill para LS2 padrão, incluindo chaves offline.

0.9.39 contém suporte do I2CP para LS2 e Encrypted LS2, assinatura/verificação com sig type 11, suporte a floodfill para Encrypted LS2 (tipos de sig 7 e 11, sem chaves offline) e criptografia/descriptografia de LS2 (sem autorização por cliente).

O 0.9.40 está previsto para incluir suporte à criptografia/descriptografia de LS2 com autorização por cliente, suporte de floodfill e I2CP para Meta LS2, suporte a LS2 criptografado com chaves offline e suporte a b32 para LS2 criptografado.

## Agradecimentos

O design criptografado do LS2 é fortemente influenciado pelos [descritores de serviços ocultos v3 do Tor](https://spec.torproject.org/rend-spec-v3), que tinham objetivos de design semelhantes.

## Referências

* ["High-speed high-security signatures" por Daniel J. Bernstein, Niels Duif, Tanja Lange, Peter Schwabe e Bo-Yin Yang](https://ed25519.cr.yp.to/)
* [KEYBLIND-PROOF](https://lists.torproject.org/pipermail/tor-dev/2013-December/005943.html)
* [KEYBLIND-REFS](https://gitlab.torproject.org/tpo/core/tor/-/issues/8106)
* [PRNG-REFS](http://projectbullrun.org/dual-ec/ext-rand.html)
* [RFC-2104](https://tools.ietf.org/html/rfc2104)
* [RFC-4880-S5.1](https://tools.ietf.org/html/rfc4880#section-5.1)
* [RFC-5869](https://tools.ietf.org/html/rfc5869)
* [RFC-7539-S2.4](https://tools.ietf.org/html/rfc7539#section-2.4)
* [TOR-REND-SPEC-V3](https://spec.torproject.org/rend-spec-v3)
* [UNSCIENTIFIC-KDF-SPEEDS](https://www.lvh.io/posts/secure-key-derivation-performance.html)
* [ZCASH](https://github.com/zcash/zips/tree/master/protocol/protocol.pdf)
