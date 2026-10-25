---
title: "NTCP (TCP baseado em NIO)"
description: "Transporte TCP baseado em Java NIO legado para I2P, substituído pelo NTCP2"
slug: "ntcp"
aliases:
  - "/pt/docs/transport/ntcp"
  - "/pt/docs/transport/ntcp/"
  - "/pt/docs/ntcp"
  - "/pt/docs/ntcp/"
  - "/pt/ntcp"
  - "/pt/ntcp/"
lastUpdated: "2021-10"
accurateFor: "0.9.52"
---

DESCONTINUADO, NÃO MAIS SUPORTADO. Desabilitado por padrão a partir de 0.9.40 2019-05. Suporte removido a partir de 0.9.50 2021-05. Substituído por [NTCP2](/docs/specs/ntcp2). NTCP é um transporte baseado em Java NIO introduzido na versão 0.6.1.22 do I2P. Java NIO (new I/O) não sofre dos problemas de 1 thread por conexão do antigo transporte TCP. NTCP-over-IPv6 é suportado a partir da versão 0.9.8.

Por padrão, NTCP usa o IP/Porta auto-detectados pelo SSU. Quando habilitado no config.jsp, SSU irá notificar/reiniciar NTCP quando o endereço externo mudar ou quando o status do firewall mudar. Agora você pode habilitar TCP de entrada sem um IP estático ou serviço dyndns.

O código NTCP dentro do I2P é relativamente leve (1/4 do tamanho do código SSU) porque usa o transporte TCP Java subjacente para entrega confiável.

## Especificação de Endereço do Router {#ra}

As seguintes propriedades são armazenadas na base de dados da rede.

- **Nome do transporte:** NTCP
- **host:** IP (IPv4 ou IPv6).
  Endereços IPv6 abreviados (com "::") são permitidos.
  Nomes de host eram anteriormente permitidos, mas estão obsoletos a partir da versão 0.9.32. Ver proposta 141.
- **port:** 1024 - 65535

## Especificação do Protocolo NTCP

### Formato de Mensagem Padrão

Após o estabelecimento, o transporte NTCP envia mensagens I2NP individuais, com um checksum simples. A mensagem não criptografada é codificada da seguinte forma:

```
+-------+-------+-------+-------+-------+-------+-------+-------+
| sizeof(data)  |                                               |
+-------+-------+                                               +
|                            data                               |
~                                                               ~
|                                                               |
+                                       +-------+-------+-------+
|                                       |        padding
+-------+-------+-------+-------+-------+-------+-------+-------+
                                | Adler checksum of sz+data+pad |
+-------+-------+-------+-------+-------+-------+-------+-------+
```
Os dados são então criptografados com AES/256/CBC. A chave de sessão para a criptografia é negociada durante o estabelecimento (usando Diffie-Hellman 2048 bit). O estabelecimento entre dois routers é implementado na classe EstablishState e detalhado abaixo. O IV para criptografia AES/256/CBC são os últimos 16 bytes da mensagem criptografada anterior.

São necessários de 0 a 15 bytes de preenchimento para fazer com que o comprimento total da mensagem (incluindo os seis bytes de tamanho e checksum) seja um múltiplo de 16. O tamanho máximo da mensagem é atualmente de 16 KB. Portanto, o tamanho máximo de dados é atualmente de 16 KB - 6, ou 16378 bytes. O tamanho mínimo de dados é 1.

### Formato da Mensagem de Sincronização de Tempo

Um caso especial é uma mensagem de metadados onde o sizeof(data) é 0. Nesse caso, a mensagem não criptografada é codificada como:

```
+-------+-------+-------+-------+-------+-------+-------+-------+
|       0       |      timestamp in seconds     | uninterpreted
+-------+-------+-------+-------+-------+-------+-------+-------+
        uninterpreted           | Adler checksum of bytes 0-11  |
+-------+-------+-------+-------+-------+-------+-------+-------+
```
Comprimento total: 16 bytes. A mensagem de sincronização de tempo é enviada em intervalos de aproximadamente 15 minutos. A mensagem é criptografada da mesma forma que as mensagens padrão.

### Checksums

As mensagens padrão e de sincronização de tempo usam o checksum Adler-32 conforme definido na [Especificação ZLIB](http://tools.ietf.org/html/rfc1950).

### Timeout de Inatividade

O timeout de inatividade e o fechamento de conexão ficam a critério de cada endpoint e podem variar. A implementação atual diminui o timeout conforme o número de conexões se aproxima do máximo configurado, e aumenta o timeout quando a contagem de conexões está baixa. O timeout mínimo recomendado é de dois minutos ou mais, e o timeout máximo recomendado é de dez minutos ou mais.

### Troca de RouterInfo

Após o estabelecimento, e a cada 30-60 minutos depois disso, os dois routers devem geralmente trocar RouterInfos usando uma DatabaseStoreMessage. No entanto, Alice deve verificar se a primeira mensagem na fila é uma DatabaseStoreMessage para não enviar uma mensagem duplicada; isso frequentemente acontece ao conectar-se a um router floodfill.

### Sequência de Estabelecimento

No estado de estabelecimento, há uma sequência de mensagens de 4 fases para trocar chaves DH e assinaturas. Nas duas primeiras mensagens há uma troca Diffie Hellman de 2048 bits. Em seguida, assinaturas dos dados críticos são trocadas para confirmar a conexão.

```
Alice                   contacts                      Bob
=========================================================
 X+(H(X) xor Bob.identHash)----------------------------->
 <----------------------------------------Y+E(H(X+Y)+tsB+padding, sk, Y[239:255])
 E(sz+Alice.identity+tsA+padding+S(X+Y+Bob.identHash+tsA+tsB), sk, hX_xor_Bob.identHash[16:31])--->
 <----------------------E(S(X+Y+Alice.identHash+tsA+tsB)+padding, sk, prev)
```
```
  Legend:
    X, Y: 256 byte DH public keys
    H(): 32 byte SHA256 Hash
    E(data, session key, IV): AES256 Encrypt
    S(): Signature
    tsA, tsB: timestamps (4 bytes, seconds since epoch)
    sk: 32 byte Session key
    sz: 2 byte size of Alice identity to follow
```
#### Troca de Chaves DH {#DH}

A troca de chaves DH inicial de 2048 bits usa o mesmo número primo compartilhado (p) e gerador (g) que é usado para a [criptografia ElGamal](/docs/specs/cryptography#elgamal) do I2P.

O intercâmbio de chaves DH consiste em várias etapas, exibidas abaixo. O mapeamento entre essas etapas e as mensagens enviadas entre routers I2P está marcado em negrito.

1. Alice gera um inteiro secreto x. Ela então calcula `X = g^x mod p`.
2. Alice envia X para Bob **(Mensagem 1)**.
3. Bob gera um inteiro secreto y. Ele então calcula `Y = g^y mod p`.
4. Bob envia Y para Alice. **(Mensagem 2)**
5. Alice pode agora calcular `sessionKey = Y^x mod p`.
6. Bob pode agora calcular `sessionKey = X^y mod p`.
7. Tanto Alice quanto Bob agora têm uma chave compartilhada `sessionKey = g^(x*y) mod p`.

A sessionKey é então usada para trocar identidades na **Mensagem 3** e **Mensagem 4**. O comprimento do expoente (x e y) para a troca DH está documentado na [página de criptografia](/docs/specs/cryptography#exponent).

#### Detalhes da Chave de Sessão

A chave de sessão de 32 bytes é criada da seguinte forma:

1. Pegue a chave DH trocada, representada como um array de bytes BigInteger de comprimento mínimo positivo (complemento de dois big-endian)
2. Se o bit mais significativo for 1 (ou seja, array[0] & 0x80 != 0), adicione um byte 0x00 no início, como na representação Java's BigInteger.toByteArray()
3. Se esse array de bytes for maior ou igual a 32 bytes, use os primeiros (mais significativos) 32 bytes
4. Se esse array de bytes for menor que 32 bytes, adicione bytes 0x00 no final para estender até 32 bytes. *(extremamente improvável)*

#### Mensagem 1 (Solicitação de Sessão)

Esta é a solicitação DH. Alice já possui a [Router Identity](/docs/specs/common-structures#struct_RouterIdentity), endereço IP e porta de Bob, conforme contido em seu [Router Info](/docs/specs/common-structures#struct_RouterInfo), que foi publicado no [network database](/docs/overview/network-database). Alice envia para Bob:

```
 X+(H(X) xor Bob.identHash)----------------------------->

    Size: 288 bytes
```
Conteúdo:

```
 +----+----+----+----+----+----+----+----+
 |         X, as calculated from DH      |
 +                                       +
 |                                       |
 ~               .   .   .               ~
 |                                       |
 +----+----+----+----+----+----+----+----+
 |                                       |
 +                                       +
 |              HXxorHI                  |
 +                                       +
 |                                       |
 +                                       +
 |                                       |
 +----+----+----+----+----+----+----+----+

  X :: 256 byte X from Diffie Hellman

  HXxorHI :: SHA256 Hash(X) xored with SHA256 Hash(Bob's RouterIdentity)
             (32 bytes)
```
**Notas:**

- Bob verifica HXxorHI usando seu próprio hash do router. Se não verificar, Alice contatou o router errado, e Bob encerra a conexão.

#### Mensagem 2 (Sessão Criada)

Esta é a resposta DH. Bob envia para Alice:

```
 <----------------------------------------Y+E(H(X+Y)+tsB+padding, sk, Y[239:255])

    Size: 304 bytes
```
Conteúdos Não Criptografados:

```
 +----+----+----+----+----+----+----+----+
 |         Y as calculated from DH       |
 +                                       +
 |                                       |
 ~               .   .   .               ~
 |                                       |
 +----+----+----+----+----+----+----+----+
 |                                       |
 +                                       +
 |              HXY                      |
 +                                       +
 |                                       |
 +                                       +
 |                                       |
 +----+----+----+----+----+----+----+----+
 |        tsB        |     padding       |
 +----+----+----+----+                   +
 |                                       |
 +----+----+----+----+----+----+----+----+

  Y :: 256 byte Y from Diffie Hellman

  HXY :: SHA256 Hash(X concatenated with Y)
         (32 bytes)

  tsB :: 4 byte timestamp (seconds since the epoch)

  padding :: 12 bytes random data
```
Conteúdos Criptografados:

```
 +----+----+----+----+----+----+----+----+
 |         Y as calculated from DH       |
 +                                       +
 |                                       |
 ~               .   .   .               ~
 |                                       |
 +----+----+----+----+----+----+----+----+
 |                                       |
 +                                       +
 |             encrypted data            |
 +                                       +
 |                                       |
 +                                       +
 |                                       |
 +                                       +
 |                                       |
 +                                       +
 |                                       |
 +----+----+----+----+----+----+----+----+

  Y: 256 byte Y from Diffie Hellman

  encrypted data: 48 bytes AES encrypted using the DH session key and
                  the last 16 bytes of Y as the IV
```
**Notas:**

- Alice pode descartar a conexão se a diferença de relógio com Bob for muito alta conforme calculado usando tsB.

#### Mensagem 3 (Confirmação de Sessão A)

Isso contém a identidade do router da Alice e uma assinatura dos dados críticos. Alice envia para Bob:

```
 E(sz+Alice.identity+tsA+padding+S(X+Y+Bob.identHash+tsA+tsB), sk, hX_xor_Bob.identHash[16:31])--->

    Size: 448 bytes (typ. for 387 byte identity and DSA signature), see notes below
```
Conteúdos Não Criptografados:

```
 +----+----+----+----+----+----+----+----+
 |   sz    | Alice's Router Identity     |
 +----+----+                             +
 |                                       |
 ~               .   .   .               ~
 |                                       |
 +                        +----+----+----+
 |                        |     tsA
 +----+----+----+----+----+----+----+----+
      |             padding              |
 +----+                                  +
 |                                       |
 +----+----+----+----+----+----+----+----+
 |                                       |
 +                                       +
 |              signature                |
 +                                       +
 |                                       |
 +                                       +
 |                                       |
 +                                       +
 |                                       |
 +----+----+----+----+----+----+----+----+

  sz :: 2 byte size of Alice's router identity to follow (387+)

  ident :: Alice's 387+ byte RouterIdentity

  tsA :: 4 byte timestamp (seconds since the epoch)

  padding :: 0-15 bytes random data

  signature :: the Signature of the following concatenated data:
               X, Y, Bob's RouterIdentity, tsA, tsB.
               Alice signs it with the SigningPrivateKey associated with
               the SigningPublicKey in her RouterIdentity
```
Conteúdos Criptografados:

```
 +----+----+----+----+----+----+----+----+
 |                                       |
 +                                       +
 |             encrypted data            |
 ~               .   .   .               ~
 |                                       |
 +----+----+----+----+----+----+----+----+

  encrypted data: 448 bytes AES encrypted using the DH session key and
                  the last 16 bytes of HXxorHI (i.e., the last 16 bytes
                  of message #1) as the IV
                  448 is the typical length, but it could be longer, see below.
```
**Notas:**

- Bob verifica a assinatura e, em caso de falha, descarta a conexão.
- Bob pode descartar a conexão se o desvio de relógio com Alice for muito alto conforme calculado usando tsA.
- Alice usará os últimos 16 bytes do conteúdo criptografado desta mensagem como o IV para a próxima mensagem.
- Até o lançamento 0.9.15, a router identity sempre tinha 387 bytes, a assinatura sempre era uma assinatura DSA de 40 bytes, e o padding sempre era de 15 bytes. A partir do lançamento 0.9.16, a router identity pode ser maior que 387 bytes, e o tipo e comprimento da assinatura são implícitos pelo tipo da [Signing Public Key](/docs/specs/common-structures#type_SigningPublicKey) na [Router Identity](/docs/specs/common-structures#struct_RouterIdentity) de Alice. O padding é conforme necessário para um múltiplo de 16 bytes para todo o conteúdo não criptografado.
- O comprimento total da mensagem não pode ser determinado sem descriptografá-la parcialmente para ler a Router Identity. Como o comprimento mínimo da Router Identity é 387 bytes, e o comprimento mínimo da Signature é 40 (para DSA), o tamanho mínimo total da mensagem é 2 + 387 + 4 + (comprimento da assinatura) + (padding para 16 bytes), ou 2 + 387 + 4 + 40 + 15 = 448 para DSA. O receptor poderia ler essa quantidade mínima antes de descriptografar para determinar o comprimento real da Router Identity. Para Certificates pequenos na Router Identity, isso provavelmente será a mensagem inteira, e não haverá mais bytes na mensagem que requeiram uma operação adicional de descriptografia.

#### Mensagem 4 (Confirmação de Sessão B)

Esta é uma assinatura dos dados críticos. Bob envia para Alice:

```
 <----------------------E(S(X+Y+Alice.identHash+tsA+tsB)+padding, sk, prev)

    Size: 48 bytes (typ. for DSA signature), see notes below
```
Conteúdo não criptografado:

```
 +----+----+----+----+----+----+----+----+
 |                                       |
 +                                       +
 |              signature                |
 +                                       +
 |                                       |
 +                                       +
 |                                       |
 +                                       +
 |                                       |
 +----+----+----+----+----+----+----+----+
 |               padding                 |
 +----+----+----+----+----+----+----+----+

  signature :: the Signature of the following concatenated data:
               X, Y, Alice's RouterIdentity, tsA, tsB.
               Bob signs it with the SigningPrivateKey associated with
               the SigningPublicKey in his RouterIdentity

  padding :: 0-15 bytes random data
```
Conteúdos Criptografados:

```
 +----+----+----+----+----+----+----+----+
 |                                       |
 +                                       +
 |             encrypted data            |
 ~               .   .   .               ~
 |                                       |
 +----+----+----+----+----+----+----+----+

  encrypted data: Data AES encrypted using the DH session key and
                  the last 16 bytes of the encrypted contents of message #2 as the IV
                  48 bytes for a DSA signature, may vary for other signature types
```
**Notas:**

- Alice verifica a assinatura e, em caso de falha, encerra a conexão.
- Bob usará os últimos 16 bytes do conteúdo criptografado desta mensagem como o IV para a próxima mensagem.
- Até a versão 0.9.15, a assinatura era sempre uma assinatura DSA de 40 bytes e o preenchimento era sempre de 8 bytes. A partir da versão 0.9.16, o tipo e comprimento da assinatura são implícitos pelo tipo da [Signing Public Key](/docs/specs/common-structures#type_SigningPublicKey) na [Router Identity](/docs/specs/common-structures#struct_RouterIdentity) de Bob. O preenchimento é conforme necessário para um múltiplo de 16 bytes para todo o conteúdo não criptografado.

#### Após o Estabelecimento

A conexão é estabelecida e mensagens padrão ou de sincronização de tempo podem ser trocadas. Todas as mensagens subsequentes são criptografadas com AES usando a chave de sessão DH negociada. Alice usará os últimos 16 bytes do conteúdo criptografado da mensagem #3 como o próximo IV. Bob usará os últimos 16 bytes do conteúdo criptografado da mensagem #4 como o próximo IV.

### Verificar Mensagem de Conexão

Alternativamente, quando Bob recebe uma conexão, pode ser uma conexão de verificação (talvez solicitada por Bob pedindo para alguém verificar seu ouvinte). Check Connection não é usado atualmente. No entanto, para registro, as conexões de verificação são formatadas da seguinte forma. Uma conexão de informação de verificação receberá 256 bytes contendo:

- 32 bytes de dados não interpretados, ignorados
- 1 byte de tamanho
- essa quantidade de bytes compondo o endereço IP do router local (conforme alcançado pelo lado remoto)
- número de porta de 2 bytes no qual o router local foi alcançado
- tempo de rede i2p de 4 bytes conforme conhecido pelo lado remoto (segundos desde a época)
- dados de preenchimento não interpretados, até o byte 223
- xor do hash de identidade do router local e o SHA256 dos bytes 32 até os bytes 223

A verificação de conexão está completamente desabilitada a partir da versão 0.9.12.

## Discussão

Agora na [Página de Discussão NTCP](/docs/discussions/ntcp).

## Trabalho Futuro {#future}

- O tamanho máximo da mensagem deve ser aumentado para aproximadamente 32 KB.

- Um conjunto de tamanhos fixos de pacotes pode ser apropriado para ocultar ainda mais a fragmentação de dados de adversários externos, mas o preenchimento do tunnel, garlic e ponto a ponto deve ser suficiente para a maioria das necessidades até então.
  No entanto, atualmente não há provisão para preenchimento além do próximo limite de 16 bytes,
  para criar um número limitado de tamanhos de mensagem.

- A utilização de memória (incluindo a do kernel) para NTCP deve ser comparada com a do SSU.

- As mensagens de estabelecimento podem ser preenchidas aleatoriamente de alguma forma, para frustrar a identificação do tráfego I2P baseada nos tamanhos dos pacotes iniciais?
