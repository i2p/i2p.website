---
title: "ECIES-X25519-AEAD-Ratchet"
description: "Esquema de Criptografia Integrada de Curva Elíptica para criptografia ponta-a-ponta I2P"
slug: "ecies"
aliases:
  - "/pt/docs/specs/ecies-x25519-aead-ratchet"
  - "/pt/docs/specs/ecies-x25519-aead-ratchet/"
category: "Protocolos"
lastUpdated: "2025-06"
accurateFor: "0.9.67"
---

## Nota

Implantação da rede concluída. Sujeita a pequenas revisões. Consulte [Prop144](/proposals/144-ecies-x25519/) para a proposta original, incluindo discussão de contexto e informações adicionais.

As seguintes funcionalidades não estão implementadas a partir da versão 0.9.66:

- Blocos MessageNumbers, Options e Termination
- Respostas da camada de protocolo
- Chave estática zero
- Multicast

Para a versão MLKEM PQ Hybrid deste protocolo, consulte [ECIES-HYBRID](/docs/specs/ecies-hybrid/).

## Visão Geral

Este é o novo protocolo de criptografia ponta-a-ponta para substituir ElGamal/AES+SessionTags [ElG-AES](/docs/specs/elgamal-aes/).

Baseia-se em trabalhos anteriores da seguinte forma:

- Especificação de estruturas comuns [Common](/docs/specs/common-structures/)
- Especificação [I2NP](/docs/specs/i2np/) incluindo LS2
- ElGamal/AES+Session Tags [Elg-AES](/docs/specs/elgamal-aes/)
- <http://zzz.i2p/topics/1768> visão geral da nova criptografia assimétrica
- Visão geral de criptografia de baixo nível [CRYPTO-ELG](/docs/specs/cryptography/#elgamal)
- ECIES <http://zzz.i2p/topics/2418>
- [NTCP2](/docs/specs/ntcp2/) [Prop111](/proposals/111-ntcp2/)
- 123 Novas Entradas netDB
- 142 Novo Modelo de Criptografia
- Protocolo [Noise](https://noiseprotocol.org/noise.html)
- Algoritmo double ratchet do [Signal](https://signal.org/docs/specifications/doubleratchet/)

Suporta nova criptografia para comunicação ponto a ponto, destination-to-destination.

O design usa um handshake Noise e uma fase de dados que incorpora o double ratchet do Signal.

Todas as referências ao Signal e Noise nesta especificação são apenas para informação de contexto. O conhecimento dos protocolos Signal e Noise não é necessário para entender ou implementar esta especificação.

Esta especificação é suportada a partir da versão 0.9.46.

## Especificação

O design usa um handshake Noise e uma fase de dados incorporando o double ratchet do Signal.

### Resumo do Design Criptográfico

Existem cinco partes do protocolo que precisam ser redesenhadas:

- 1\) Os novos formatos de contêiner de Sessão nova e Existente são substituídos por
  novos formatos.
- 2\) ElGamal (chaves públicas de 256 bytes, chaves privadas de 128 bytes) é
  substituído por ECIES-X25519 (chaves públicas e privadas de 32 bytes)
- 3\) AES é substituído por AEAD_ChaCha20_Poly1305 (abreviado como
  ChaChaPoly abaixo)
- 4\) SessionTags serão substituídas por ratchets, que é essencialmente um
  PRNG criptográfico e sincronizado.
- 5\) O payload AES, conforme definido na especificação
  ElGamal/AES+SessionTags, é substituído por um formato de bloco similar ao do
  NTCP2.

Cada uma das cinco mudanças tem sua própria seção abaixo.

### Tipo de Criptografia

O tipo de criptografia (usado no LS2) é 4. Isso indica uma chave pública X25519 de 32 bytes little-endian, e o protocolo ponto-a-ponto especificado aqui.

Tipo de criptografia 0 é ElGamal. Tipos de criptografia 1-3 são reservados para ECIES-ECDH-AES-SessionTag, veja proposta 145 [Prop145](/proposals/145-ecies-ecdh-aes/).

### Framework do Protocolo Noise

Este protocolo fornece os requisitos baseados no Noise Protocol Framework [NOISE](https://noiseprotocol.org/noise.html) (Revisão 34, 2018-07-11). O Noise tem propriedades similares ao protocolo Station-To-Station [STS](https://en.wikipedia.org/wiki/Station-to-Station_protocol), que é a base para o protocolo [SSU](/docs/transport/ssu/). Na terminologia do Noise, Alice é o iniciador e Bob é o respondente.

Esta especificação é baseada no protocolo Noise Noise_IK_25519_ChaChaPoly_SHA256. (O identificador real para a função inicial de derivação de chaves é "Noise_IKelg2_25519_ChaChaPoly_SHA256" para indicar extensões I2P - veja a seção KDF 1 abaixo) Este protocolo Noise usa as seguintes primitivas:

- Padrão de Handshake Interativo: IK Alice transmite imediatamente sua
  chave estática para Bob (I) Alice já conhece a chave estática de Bob (K)
- Padrão de Handshake Unidirecional: N Alice não transmite sua chave estática para
  Bob (N)
- Função DH: X25519 X25519 DH com um comprimento de chave de 32 bytes conforme
  especificado em [RFC-7748](https://tools.ietf.org/html/rfc7748).
- Função de Cifra: ChaChaPoly AEAD_CHACHA20_POLY1305 conforme especificado em
  [RFC-7539](https://tools.ietf.org/html/rfc7539) seção 2.8. Nonce de 12 bytes, com
  os primeiros 4 bytes definidos como zero. Idêntico ao usado em
  [NTCP2](/docs/specs/ntcp2/).
- Função Hash: SHA256 Hash padrão de 32 bytes, já usado extensivamente
  no I2P.

#### Adições ao Framework

Esta especificação define as seguintes melhorias para Noise_IK_25519_ChaChaPoly_SHA256. Estas geralmente seguem as diretrizes na seção 13 do [NOISE](https://noiseprotocol.org/noise.html).

1)  Chaves efêmeras em texto claro são codificadas com

    [Elligator2](https://elligator.cr.yp.to/elligator-20130828.pdf).
2) A resposta é prefixada com uma tag em texto claro. 3) O formato do payload é definido para as mensagens 1, 2 e a fase de dados.

    Of course, this is not defined in Noise.

Todas as mensagens incluem um cabeçalho [I2NP](/docs/specs/i2np/) Garlic Message. A fase de dados usa criptografia similar, mas não compatível, com a fase de dados do Noise.

### Padrões de Handshake

Os handshakes usam padrões de handshake [Noise](https://noiseprotocol.org/noise.html).

O seguinte mapeamento de letras é utilizado:

- e = chave efêmera de uso único
- s = chave estática
- p = carga útil da mensagem

Sessões One-time e Unbound são semelhantes ao padrão Noise N.

```
<- s
...
e es p ->
```
Sessões vinculadas são similares ao padrão Noise IK.

```
<- s
...
e es s ss p ->
<- tag e ee se
<- p
p ->
```
#### Propriedades de Segurança

Usando a terminologia Noise, a sequência de estabelecimento e dados é a seguinte: (Propriedades de Segurança do Payload de [Noise](https://noiseprotocol.org/noise.html) )

```
IK(s, rs):           Authentication   Confidentiality
  <- s
  ...
  -> e, es, s, ss           1                2
  <- e, ee, se              2                4
  ->                        2                5
  <-                        2                5
```
#### Diferenças do XK

Handshakes IK têm várias diferenças dos handshakes XK usados em [NTCP2](/docs/specs/ntcp2/) e [SSU2](/docs/specs/ssu2/).

- Quatro operações DH totais comparadas a três para XK
- Autenticação do remetente na primeira mensagem: A carga útil é autenticada
  como pertencente ao proprietário da chave pública do remetente, embora a
  chave possa ter sido comprometida (Autenticação 1) XK requer outro
  round trip antes de Alice ser autenticada.
- Sigilo direto total (Confidencialidade 5) após a segunda mensagem. Bob
  pode enviar uma carga útil imediatamente após a segunda mensagem com sigilo
  direto total. XK requer outro round trip para sigilo direto total.

Em resumo, o IK permite entrega 1-RTT da carga útil de resposta de Bob para Alice com sigilo futuro completo, no entanto a carga útil de solicitação não possui sigilo futuro.

### Sessões

O protocolo ElGamal/AES+SessionTag é unidirecional. Nesta camada, o receptor não sabe de onde vem uma mensagem. As sessões de saída e entrada não estão associadas. As confirmações são fora de banda usando uma DeliveryStatusMessage (embrulhada em uma GarlicMessage) no cravo.

Para esta especificação, definimos dois mecanismos para criar um protocolo bidirecional - "emparelhamento" e "vinculação". Esses mecanismos fornecem maior eficiência e segurança.

#### Contexto da Sessão

Assim como com ElGamal/AES+SessionTags, todas as sessões de entrada e saída devem estar em um determinado contexto, seja o contexto do router ou o contexto para um destino local específico. No Java I2P, este contexto é chamado de Session Key Manager.

As sessões não devem ser compartilhadas entre contextos, pois isso permitiria correlação entre os vários destinos locais, ou entre um destino local e um router.

Quando um destino específico suporta tanto ElGamal/AES+SessionTags quanto esta especificação, ambos os tipos de sessões podem compartilhar um contexto. Veja a seção 1c) abaixo.

#### Emparelhando Sessões de Entrada e Saída

Quando uma sessão de saída é criada no originador (Alice), uma nova sessão de entrada é criada e emparelhada com a sessão de saída, a menos que nenhuma resposta seja esperada (ex: datagramas brutos).

Uma nova sessão de entrada é sempre emparelhada com uma nova sessão de saída, a menos que nenhuma resposta seja solicitada (por exemplo, datagramas brutos).

Se uma resposta for solicitada e vinculada a um destino ou router de extremidade distante, essa nova sessão de saída é vinculada a esse destino ou router, e substitui qualquer sessão de saída anterior para esse destino ou router.

Emparelhar sessões de entrada e saída fornece um protocolo bidirecional com a capacidade de rotacionar as chaves DH.

#### Vinculando Sessões e Destinos

Há apenas uma sessão de saída para um determinado destino ou router. Pode haver várias sessões de entrada atuais de um determinado destino ou router. Geralmente, quando uma nova sessão de entrada é criada, e o tráfego é recebido nessa sessão (que serve como um ACK), quaisquer outras serão marcadas para expirar relativamente rápido, dentro de um minuto ou mais. O valor das mensagens anteriores enviadas (PN) é verificado, e se não há mensagens não recebidas (dentro do tamanho da janela) na sessão de entrada anterior, a sessão anterior pode ser deletada imediatamente.

Quando uma sessão de saída é criada no originador (Alice), ela fica vinculada ao Destination da extremidade remota (Bob), e qualquer sessão de entrada emparelhada também ficará vinculada ao Destination da extremidade remota. À medida que as sessões evoluem, elas continuam vinculadas ao Destination da extremidade remota.

Quando uma sessão de entrada é criada no receptor (Bob), ela pode ser vinculada ao Destination de extremidade distante (Alice), a critério de Alice. Se Alice incluir informações de vinculação (sua chave estática) na mensagem New Session, a sessão será vinculada a esse destination, e uma sessão de saída será criada e vinculada ao mesmo Destination. À medida que as sessões fazem o ratchet, elas continuam vinculadas ao Destination de extremidade distante.

#### Benefícios da Vinculação e Emparelhamento

Para o caso comum de streaming, esperamos que Alice e Bob usem o protocolo da seguinte forma:

- Alice emparelha sua nova sessão de saída com uma nova sessão de entrada, ambas
  vinculadas ao destino final (Bob).
- Alice inclui as informações de vinculação e assinatura, e uma solicitação
  de resposta, na mensagem New Session enviada para Bob.
- Bob emparelha sua nova sessão de entrada com uma nova sessão de saída, ambas
  vinculadas ao destino final (Alice).
- Bob envia uma resposta (ack) para Alice na sessão emparelhada, com um ratchet
  para uma nova chave DH.
- Alice executa ratchet para uma nova sessão de saída com a nova chave de Bob, emparelhada
  à sessão de entrada existente.

Ao vincular uma sessão de entrada a um Destination remoto e emparelhar a sessão de entrada com uma sessão de saída vinculada ao mesmo Destination, obtemos dois grandes benefícios:

1)  A resposta inicial de Bob para Alice usa DH efêmero-efêmero

2\) Depois que Alice recebe a resposta de Bob e faz o ratchet, todas as mensagens subsequentes de Alice para Bob usam DH efêmero-efêmero.

#### ACKs de Mensagem

No ElGamal/AES+SessionTags, quando um leaseSet é empacotado como um garlic clove, ou tags são entregues, o router remetente solicita um ACK. Este é um garlic clove separado contendo uma Mensagem DeliveryStatus. Para segurança adicional, a Mensagem DeliveryStatus é envolvida em uma Mensagem Garlic. Este mecanismo é out-of-band da perspectiva do protocolo.

No novo protocolo, como as sessões de entrada e saída estão emparelhadas, podemos ter ACKs in-band. Nenhum clove separado é necessário.

Um ACK explícito é simplesmente uma mensagem de Sessão Existente sem bloco I2NP. No entanto, na maioria dos casos, um ACK explícito pode ser evitado, pois há tráfego reverso. Pode ser desejável que as implementações aguardem um tempo curto (talvez cem ms) antes de enviar um ACK explícito, para dar tempo à camada de streaming ou aplicação para responder.

As implementações também precisarão adiar o envio de qualquer ACK até depois que o bloco I2NP seja processado, pois a Garlic Message pode conter uma Database Store Message com um leaseSet. Um leaseSet recente será necessário para rotear o ACK, e o destino remoto (contido no leaseSet) será necessário para verificar a chave estática de vinculação.

#### Timeouts de Sessão

Sessões de saída devem sempre expirar antes das sessões de entrada. Uma vez que uma sessão de saída expire e uma nova seja criada, uma nova sessão de entrada pareada também será criada. Se havia uma sessão de entrada antiga, ela será permitida expirar.

### Multicast

A definir

### Definições

Definimos as seguintes funções correspondentes aos blocos de construção criptográficos utilizados.

ZEROLEN

array de bytes de comprimento zero

CSRNG(n)

saída de n bytes de um número aleatório criptograficamente seguro

    generator.

H(p, d)

Função hash SHA-256 que recebe uma string de personalização p e dados

    d, and produces an output of length 32 bytes. As defined in
    [NOISE](https://noiseprotocol.org/noise.html). || below means append.

    Use SHA-256 as follows:

        H(p, d) := SHA-256(p || d)

MixHash(d)

Função de hash SHA-256 que recebe um hash anterior h e novos dados d,

    and produces an output of length 32 bytes. || below means append.

    Use SHA-256 as follows:

        MixHash(d) := h = SHA-256(h || d)

STREAM

O ChaCha20/Poly1305 AEAD conforme especificado em

    [RFC-7539](https://tools.ietf.org/html/rfc7539). S_KEY_LEN = 32 and S_IV_LEN =
    12.

    ENCRYPT(k, n, plaintext, ad)

    :   Encrypts plaintext using the cipher key k, and nonce n which
        MUST be unique for the key k. Associated data ad is optional.
        Returns a ciphertext that is the size of the plaintext + 16
        bytes for the HMAC.

        The entire ciphertext must be indistinguishable from random if
        the key is secret.

    DECRYPT(k, n, ciphertext, ad)

    :   Decrypts ciphertext using the cipher key k, and nonce n.
        Associated data ad is optional. Returns the plaintext.

DH

Sistema de acordo de chave pública X25519. Chaves privadas de 32 bytes, pública

    keys of 32 bytes, produces outputs of 32 bytes. It has the following
    functions:

    GENERATE_PRIVATE()

    :   Generates a new private key.

    DERIVE_PUBLIC(privkey)

    :   Returns the public key corresponding to the given private key.

    GENERATE_PRIVATE_ELG2()

    :   Generates a new private key that maps to a public key suitable
        for Elligator2 encoding. Note that half of the
        randomly-generated private keys will not be suitable and must be
        discarded.

    ENCODE_ELG2(pubkey)

    :   Returns the Elligator2-encoded public key corresponding to the
        given public key (inverse mapping). Encoded keys are little
        endian. Encoded key must be 256 bits indistinguishable from
        random data. See Elligator2 section below for specification.

    DECODE_ELG2(pubkey)

    :   Returns the public key corresponding to the given
        Elligator2-encoded public key. See Elligator2 section below for
        specification.

    DH(privkey, pubkey)

    :   Generates a shared secret from the given private and public
        keys.

HKDF(salt, ikm, info, n)

Uma função de derivação de chave criptográfica que recebe alguma chave de entrada

    material ikm (which should have good entropy but is not required to
    be a uniformly random string), a salt of length 32 bytes, and a
    context-specific 'info' value, and produces an output of n bytes
    suitable for use as key material.

    Use HKDF as specified in [RFC-5869](https://tools.ietf.org/html/rfc5869), using
    the HMAC hash function SHA-256 as specified in
    [RFC-2104](https://tools.ietf.org/html/rfc2104). This means that SALT_LEN is 32
    bytes max.

MixKey(d)

Use HKDF() com um chainKey anterior e novos dados d, e define o novo

    chainKey and k. As defined in [NOISE](https://noiseprotocol.org/noise.html).

    Use HKDF as follows:

        MixKey(d) := output = HKDF(chainKey, d, "", 64)
                     chainKey = output[0:31]
                     k = output[32:63]

### 1) Formato da mensagem

#### Revisão do Formato de Mensagem Atual

A Garlic Message conforme especificado em [I2NP](/docs/specs/i2np/) é a seguinte. Como um objetivo de design é que os saltos intermediários não possam distinguir criptografia nova de antiga, este formato não pode mudar, mesmo que o campo de comprimento seja redundante. O formato é mostrado com o cabeçalho completo de 16 bytes, embora o cabeçalho real possa estar em um formato diferente, dependendo do transporte utilizado.

Quando descriptografados, os dados contêm uma série de Garlic Cloves e dados adicionais, também conhecidos como Clove Set.

Veja [I2NP](/docs/specs/i2np/) para detalhes e especificação completa.

```
+----+----+----+----+----+----+----+----+
|type|      msg_id       |  expiration
+----+----+----+----+----+----+----+----+
                         |  size   |chks|
+----+----+----+----+----+----+----+----+
|      length       |                   |
+----+----+----+----+                   +
|          encrypted data               |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
```
#### Revisão do Formato de Dados Criptografados

No ElGamal/AES+SessionTags, existem dois formatos de mensagem:

1\) Nova sessão: - bloco ElGamal de 514 bytes - bloco AES (128 bytes mínimo, múltiplo de 16)

2\) Sessão existente: - 32 bytes Session Tag - bloco AES (128 bytes mínimo, múltiplo de 16)

Essas mensagens são encapsuladas em uma mensagem I2NP garlic, que contém um campo de comprimento, então o comprimento é conhecido.

O receptor primeiro tenta procurar os primeiros 32 bytes como uma Session Tag. Se encontrada, ele descriptografa o bloco AES. Se não for encontrada, e os dados tiverem pelo menos (514+16) de comprimento, ele tenta descriptografar o bloco ElGamal, e se bem-sucedido, descriptografa o bloco AES.

#### Novas Tags de Sessão e Comparação com Signal

No Signal Double Ratchet, o cabeçalho contém:

- DH: Chave pública atual do ratchet
- PN: Comprimento da mensagem da cadeia anterior
- N: Número da Mensagem

As "sending chains" do Signal são aproximadamente equivalentes aos nossos conjuntos de tags. Ao usar uma tag de sessão, podemos eliminar a maior parte disso.

Em New Session, colocamos apenas a chave pública no cabeçalho não criptografado.

Em Sessão Existente, usamos uma tag de sessão para o cabeçalho. A tag de sessão está associada à chave pública ratchet atual e ao número da mensagem.

Tanto em sessões novas quanto existentes, PN e N estão no corpo criptografado.

No Signal, as coisas estão constantemente em rotação. Uma nova chave pública DH exige que o receptor faça a rotação e envie uma nova chave pública de volta, que também serve como confirmação para a chave pública recebida. Isso seria muitas operações DH demais para nós. Então separamos a confirmação da chave recebida e a transmissão de uma nova chave pública. Qualquer mensagem usando uma session tag gerada a partir da nova chave pública DH constitui uma confirmação. Só transmitimos uma nova chave pública quando desejamos recriar as chaves.

O número máximo de mensagens antes que o DH deve fazer ratchet é 65535.

Ao entregar uma chave de sessão, derivamos o "Tag Set" dela, em vez de ter que entregar tags de sessão também. Um Tag Set pode ter até 65536 tags. No entanto, os receptores devem implementar uma estratégia de "look-ahead", em vez de gerar todas as tags possíveis de uma vez. Gere apenas no máximo N tags além da última tag válida recebida. N pode ser no máximo 128, mas 32 ou até menos pode ser uma escolha melhor.

### 1a) Novo formato de sessão

Nova Chave Pública de Uso Único da Sessão (32 bytes) Dados criptografados e MAC (bytes restantes)

A mensagem New Session pode ou não conter a chave pública estática do remetente. Se estiver incluída, a sessão reversa fica vinculada a essa chave. A chave estática deve ser incluída se respostas são esperadas, ou seja, para streaming e datagramas que podem ser respondidos. Não deve ser incluída para datagramas brutos.

A mensagem New Session é semelhante ao padrão [NOISE](https://noiseprotocol.org/noise.html) unidirecional "N" (se a chave estática não for enviada), ou ao padrão bidirecional "IK" (se a chave estática for enviada).

### 1b) Novo formato de sessão (com vinculação)

O comprimento é 96 + comprimento da carga útil. Formato criptografado:

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
+         Static Key                    +
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
~                                       ~
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|  Poly1305 Message Authentication Code |
+         (MAC) for Payload Section     +
|             16 bytes                  |
+----+----+----+----+----+----+----+----+

Public Key :: 32 bytes, little endian, Elligator2, cleartext

Static Key encrypted data :: 32 bytes

Payload Section encrypted data :: remaining data minus 16 bytes

MAC :: Poly1305 message authentication code, 16 bytes
```
#### Nova Chave Efêmera de Sessão

A chave efêmera tem 32 bytes, codificada com Elligator2. Esta chave nunca é reutilizada; uma nova chave é gerada a cada mensagem, incluindo retransmissões.

#### Chave Estática

Quando descriptografada, a chave estática X25519 de Alice, 32 bytes.

#### Payload

O comprimento criptografado é o restante dos dados. O comprimento descriptografado é 16 a menos que o comprimento criptografado. A carga útil deve conter um bloco DateTime e geralmente conterá um ou mais blocos Garlic Clove. Consulte a seção de carga útil abaixo para formato e requisitos adicionais.

### 1c) Novo formato de sessão (sem vinculação)

Se não for necessária resposta, nenhuma chave estática é enviada.

O comprimento é 96 + comprimento da carga útil. Formato criptografado:

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
|                                       |
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
~                                       ~
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|  Poly1305 Message Authentication Code |
+         (MAC) for Payload Section     +
|             16 bytes                  |
+----+----+----+----+----+----+----+----+

Public Key :: 32 bytes, little endian, Elligator2, cleartext

Flags Section encrypted data :: 32 bytes

Payload Section encrypted data :: remaining data minus 16 bytes

MAC :: Poly1305 message authentication code, 16 bytes
```
#### Nova Chave Efêmera de Sessão

Chave efêmera de Alice. A chave efêmera tem 32 bytes, codificada com Elligator2, little endian. Esta chave nunca é reutilizada; uma nova chave é gerada a cada mensagem, incluindo retransmissões.

#### Seção de Flags Dados descriptografados

A seção Flags não contém nada. Ela sempre tem 32 bytes, porque deve ter o mesmo comprimento que a chave estática para mensagens de Nova Sessão com vinculação. Bob determina se são 32 bytes de uma chave estática ou uma seção de flags testando se os 32 bytes são todos zeros.

TODO alguma flag necessária aqui?

#### Carga útil

O comprimento criptografado é o restante dos dados. O comprimento descriptografado é 16 menor que o comprimento criptografado. A carga útil deve conter um bloco DateTime e geralmente conterá um ou mais blocos Garlic Clove. Consulte a seção de carga útil abaixo para formato e requisitos adicionais.

### 1d) Formato único (sem vinculação ou sessão)

Se apenas uma única mensagem for esperada para ser enviada, nenhuma configuração de sessão ou chave estática é necessária.

O comprimento é 96 + comprimento do payload. Formato criptografado:

```
+----+----+----+----+----+----+----+----+
|                                       |
+                                       +
|       Ephemeral Public Key            |
+             32 bytes                  +
|     Encoded with Elligator2           |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|                                       |
+           Flags Section               +
|       ChaCha20 encrypted data         |
+            32 bytes                   +
|                                       |
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
~                                       ~
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|  Poly1305 Message Authentication Code |
+         (MAC) for Payload Section     +
|             16 bytes                  |
+----+----+----+----+----+----+----+----+

Public Key :: 32 bytes, little endian, Elligator2, cleartext

Flags Section encrypted data :: 32 bytes

Payload Section encrypted data :: remaining data minus 16 bytes

MAC :: Poly1305 message authentication code, 16 bytes
```
#### Nova Chave de Sessão de Uso Único

A chave única é de 32 bytes, codificada com Elligator2, little endian. Esta chave nunca é reutilizada; uma nova chave é gerada com cada mensagem, incluindo retransmissões.

#### Seção de Flags Dados descriptografados

A seção Flags não contém nada. Ela sempre tem 32 bytes, porque deve ter o mesmo comprimento que a chave estática para mensagens New Session com binding. Bob determina se são 32 bytes de uma chave estática ou uma seção de flags testando se os 32 bytes são todos zeros.

TODO alguma flag necessária aqui?

```
+----+----+----+----+----+----+----+----+
|                                       |
+                                       +
|                                       |
+             All zeros                 +
|              32 bytes                 |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+

zeros:: All zeros, 32 bytes.
```
#### Payload

O comprimento criptografado é o restante dos dados. O comprimento descriptografado é 16 menos que o comprimento criptografado. O payload deve conter um bloco DateTime e geralmente conterá um ou mais blocos Garlic Clove. Veja a seção de payload abaixo para formato e requisitos adicionais.

### 1f) KDFs para Mensagem de Nova Sessão

#### KDF para ChainKey Inicial

Este é o [NOISE](https://noiseprotocol.org/noise.html) padrão para IK com um nome de protocolo modificado. Note que usamos o mesmo inicializador tanto para o padrão IK (sessões vinculadas) quanto para o padrão N (sessões não vinculadas).

O nome do protocolo é modificado por duas razões. Primeiro, para indicar que as chaves efêmeras são codificadas com Elligator2, e segundo, para indicar que MixHash() é chamado antes da segunda mensagem para misturar o valor da tag.

```
This is the "e" message pattern:

// Define protocol_name.
Set protocol_name = "Noise_IKelg2+hs2_25519_ChaChaPoly_SHA256"
 (40 bytes, US-ASCII encoded, no NULL termination).

// Define Hash h = 32 bytes
h = SHA256(protocol_name);

Define ck = 32 byte chaining key. Copy the h data to ck.
Set chainKey = h

// MixHash(null prologue)
h = SHA256(h);

// up until here, can all be precalculated by Alice for all outgoing connections
```
#### KDF para Conteúdo Criptografado da Seção Flags/Static Key

```
This is the "e" message pattern:

// Bob's X25519 static keys
// bpk is published in leaseset
bsk = GENERATE_PRIVATE()
bpk = DERIVE_PUBLIC(bsk)

// Bob static public key
// MixHash(bpk)
// || below means append
h = SHA256(h || bpk);

// up until here, can all be precalculated by Bob for all incoming connections

// Alice's X25519 ephemeral keys
aesk = GENERATE_PRIVATE_ELG2()
aepk = DERIVE_PUBLIC(aesk)

// Alice ephemeral public key
// MixHash(aepk)
// || below means append
h = SHA256(h || aepk);

// h is used as the associated data for the AEAD in the New Session Message
// Retain the Hash h for the New Session Reply KDF
// eapk is sent in cleartext in the
// beginning of the New Session message
elg2_aepk = ENCODE_ELG2(aepk)
// As decoded by Bob
aepk = DECODE_ELG2(elg2_aepk)

End of "e" message pattern.

This is the "es" message pattern:

// Noise es
sharedSecret = DH(aesk, bpk) = DH(bsk, aepk)

// MixKey(DH())
//[chainKey, k] = MixKey(sharedSecret)
// ChaChaPoly parameters to encrypt/decrypt
keydata = HKDF(chainKey, sharedSecret, "", 64)
chainKey = keydata[0:31]

// AEAD parameters
k = keydata[32:63]
n = 0
ad = h
ciphertext = ENCRYPT(k, n, flags/static key section, ad)

End of "es" message pattern.

This is the "s" message pattern:

// MixHash(ciphertext)
// Save for Payload section KDF
h = SHA256(h || ciphertext)

// Alice's X25519 static keys
ask = GENERATE_PRIVATE()
apk = DERIVE_PUBLIC(ask)

End of "s" message pattern.
```
#### KDF para Seção de Payload (com chave estática de Alice)

```
This is the "ss" message pattern:

// Noise ss
sharedSecret = DH(ask, bpk) = DH(bsk, apk)

// MixKey(DH())
//[chainKey, k] = MixKey(sharedSecret)
// ChaChaPoly parameters to encrypt/decrypt
// chainKey from Static Key Section
Set sharedSecret = X25519 DH result
keydata = HKDF(chainKey, sharedSecret, "", 64)
chainKey = keydata[0:31]

// AEAD parameters
k = keydata[32:63]
n = 0
ad = h
ciphertext = ENCRYPT(k, n, payload, ad)

End of "ss" message pattern.

// MixHash(ciphertext)
// Save for New Session Reply KDF
h = SHA256(h || ciphertext)
```
#### KDF para Seção de Payload (sem chave estática da Alice)

Note que este é um padrão Noise "N", mas usamos o mesmo inicializador "IK" como para sessões vinculadas.

Mensagens de Nova Sessão não podem ser identificadas como contendo a chave estática da Alice ou não até que a chave estática seja descriptografada e inspecionada para determinar se contém todos zeros. Portanto, o receptor deve usar a máquina de estados "IK" para todas as mensagens de Nova Sessão. Se a chave estática for todos zeros, o padrão de mensagem "ss" deve ser ignorado.

```
chainKey = from Flags/Static key section
k = from Flags/Static key section
n = 1
ad = h from Flags/Static key section
ciphertext = ENCRYPT(k, n, payload, ad)
```
### 1g) Formato de Resposta de Nova Sessão

Uma ou mais Respostas de Nova Sessão podem ser enviadas em resposta a uma única mensagem de Nova Sessão. Cada resposta é precedida por uma tag, que é gerada a partir de um TagSet para a sessão.

A New Session Reply está dividida em duas partes. A primeira parte é a conclusão do handshake Noise IK com uma tag prefixada. O comprimento da primeira parte é de 56 bytes. A segunda parte é o payload da fase de dados. O comprimento da segunda parte é 16 + comprimento do payload.

O comprimento total é 72 + comprimento da carga útil. Formato criptografado:

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
+  (MAC) for Key Section (no data)      +
|             16 bytes                  |
+----+----+----+----+----+----+----+----+
|                                       |
+            Payload Section            +
|       ChaCha20 encrypted data         |
~                                       ~
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|  Poly1305 Message Authentication Code |
+         (MAC) for Payload Section     +
|             16 bytes                  |
+----+----+----+----+----+----+----+----+

Tag :: 8 bytes, cleartext

Public Key :: 32 bytes, little endian, Elligator2, cleartext

MAC :: Poly1305 message authentication code, 16 bytes
       Note: The ChaCha20 plaintext data is empty (ZEROLEN)

Payload Section encrypted data :: remaining data minus 16 bytes

MAC :: Poly1305 message authentication code, 16 bytes
```
#### Tag de Sessão

A tag é gerada no Session Tags KDF, conforme inicializado no DH Initialization KDF abaixo. Isso correlaciona a resposta à sessão. A Session Key do DH Initialization não é utilizada.

#### Chave Efêmera de Resposta de Nova Sessão

Chave efêmera do Bob. A chave efêmera tem 32 bytes, codificada com Elligator2, little endian. Esta chave nunca é reutilizada; uma nova chave é gerada com cada mensagem, incluindo retransmissões.

#### Carga Útil

O comprimento criptografado é o restante dos dados. O comprimento descriptografado é 16 a menos que o comprimento criptografado. A carga útil geralmente conterá um ou mais blocos Garlic Clove. Consulte a seção de carga útil abaixo para formato e requisitos adicionais.

#### KDF para Reply TagSet

Uma ou mais tags são criadas a partir do TagSet, que é inicializado usando o KDF abaixo, utilizando a chainKey da mensagem New Session.

```
// Generate tagset

tagsetKey = HKDF(chainKey, ZEROLEN, "SessionReplyTags", 32)
    tagset_nsr = DH_INITIALIZE(chainKey, tagsetKey)

```
#### KDF para Conteúdos Criptografados da Seção de Chave de Resposta

```
// Keys from the New Session message
// Alice's X25519 keys
// apk and aepk are sent in original New Session message
// ask = Alice private static key
// apk = Alice public static key
// aesk = Alice ephemeral private key
// aepk = Alice ephemeral public key
// Bob's X25519 static keys
// bsk = Bob private static key
// bpk = Bob public static key

// Generate the tag
tagsetEntry = tagset_nsr.GET_NEXT_ENTRY()
tag = tagsetEntry.SESSION_TAG

// MixHash(tag)
h = SHA256(h || tag)

This is the "e" message pattern:

// Bob's X25519 ephemeral keys
besk = GENERATE_PRIVATE_ELG2()
bepk = DERIVE_PUBLIC(besk)

// Bob's ephemeral public key
// MixHash(bepk)
// || below means append
h = SHA256(h || bepk);

// elg2_bepk is sent in cleartext in the
// beginning of the New Session message
elg2_bepk = ENCODE_ELG2(bepk)
// As decoded by Bob
bepk = DECODE_ELG2(elg2_bepk)

End of "e" message pattern.

This is the "ee" message pattern:

// MixKey(DH())
//[chainKey, k] = MixKey(sharedSecret)
// ChaChaPoly parameters to encrypt/decrypt
// chainKey from original New Session Payload Section
sharedSecret = DH(aesk, bepk) = DH(besk, aepk)
keydata = HKDF(chainKey, sharedSecret, "", 32)
chainKey = keydata[0:31]

End of "ee" message pattern.

This is the "se" message pattern:

// MixKey(DH())
//[chainKey, k] = MixKey(sharedSecret)
sharedSecret = DH(ask, bepk) = DH(besk, apk)
keydata = HKDF(chainKey, sharedSecret, "", 64)
chainKey = keydata[0:31]

// AEAD parameters
k = keydata[32:63]
n = 0
ad = h
ciphertext = ENCRYPT(k, n, ZEROLEN, ad)

End of "se" message pattern.

// MixHash(ciphertext)
h = SHA256(h || ciphertext)

chainKey is used in the ratchet below.
```
#### KDF para Conteúdos Criptografados da Seção de Payload

Isto é como a primeira mensagem de Sessão Existente, pós-divisão, mas sem uma tag separada. Além disso, usamos o hash de cima para vincular a carga útil à mensagem NSR.

```
This is the "ss" message pattern:

// Noise ss
sharedSecret = DH(ask, bpk) = DH(bsk, apk)

// MixKey(DH())
//[chainKey, k] = MixKey(sharedSecret)
// ChaChaPoly parameters to encrypt/decrypt
// chainKey from Static Key Section
Set sharedSecret = X25519 DH result
keydata = HKDF(chainKey, sharedSecret, "", 64)
chainKey = keydata[0:31]

// AEAD parameters
k = keydata[32:63]
n = 0
ad = h
ciphertext = ENCRYPT(k, n, payload, ad)

End of "ss" message pattern.

// MixHash(ciphertext)
// Save for New Session Reply KDF
h = SHA256(h || ciphertext)
```
### Notas

Várias mensagens NSR podem ser enviadas em resposta, cada uma com chaves efêmeras únicas, dependendo do tamanho da resposta.

Alice e Bob são obrigados a usar novas chaves efêmeras para cada mensagem NS e NSR.

Alice deve receber uma das mensagens NSR de Bob antes de enviar mensagens de Sessão Existente (ES), e Bob deve receber uma mensagem ES de Alice antes de enviar mensagens ES.

A `chainKey` e `k` da Seção de Payload NSR de Bob são usadas como entradas para os DH Ratchets ES iniciais (ambas as direções, veja DH Ratchet KDF).

Bob deve manter apenas as Sessões Existentes para as mensagens ES recebidas de Alice. Quaisquer outras sessões de entrada e saída criadas (para múltiplos NSRs) devem ser destruídas imediatamente após receber a primeira mensagem ES de Alice para uma determinada sessão.

### 1h) Formato de sessão existente

Tag de sessão (8 bytes) Dados criptografados e MAC (veja seção 3 abaixo)

#### Formato

Criptografado:

```
+----+----+----+----+----+----+----+----+
|       Session Tag                     |
+----+----+----+----+----+----+----+----+
|                                       |
+            Payload Section            +
|       ChaCha20 encrypted data         |
~                                       ~
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|  Poly1305 Message Authentication Code |
+              (MAC)                    +
|             16 bytes                  |
+----+----+----+----+----+----+----+----+

Session Tag :: 8 bytes, cleartext

Payload Section encrypted data :: remaining data minus 16 bytes

MAC :: Poly1305 message authentication code, 16 bytes
```
#### Payload

O comprimento criptografado é o restante dos dados. O comprimento descriptografado é 16 a menos que o comprimento criptografado. Veja a seção de payload abaixo para formato e requisitos.

#### KDF

```
See AEAD section below.

// AEAD parameters for Existing Session payload
k = The 32-byte session key associated with this session tag
n = The message number N in the current chain, as retrieved from the associated Session Tag.
ad = The session tag, 8 bytes
ciphertext = ENCRYPT(k, n, payload, ad)
```
### 2) ECIES-X25519

Formato: chaves públicas e privadas de 32 bytes, little-endian.

### 2a) Elligator2

Nos handshakes Noise padrão, as mensagens iniciais do handshake em cada direção começam com chaves efêmeras que são transmitidas em texto plano. Como chaves X25519 válidas são distinguíveis de dados aleatórios, um atacante man-in-the-middle pode distinguir essas mensagens das mensagens de Sessão Existente que começam com tags de sessão aleatórias. No [NTCP2](/docs/specs/ntcp2/) ([Prop111](/proposals/111-ntcp2/)), usamos uma função XOR de baixo overhead usando a chave estática fora-da-banda para ofuscar a chave. Contudo, o modelo de ameaça aqui é diferente; não queremos permitir que qualquer MitM use qualquer meio para confirmar o destino do tráfego, ou para distinguir as mensagens iniciais do handshake das mensagens de Sessão Existente.

Portanto, [Elligator2](https://elligator.cr.yp.to/elligator-20130828.pdf) é usado para transformar as chaves efêmeras nas mensagens New Session e New Session Reply de modo que sejam indistinguíveis de strings aleatórias uniformes.

#### Formato

Chaves públicas e privadas de 32 bytes. As chaves codificadas estão em little endian.

Como definido em [Elligator2](https://elligator.cr.yp.to/elligator-20130828.pdf), as chaves codificadas são indistinguíveis de 254 bits aleatórios. Precisamos de 256 bits aleatórios (32 bytes). Portanto, a codificação e decodificação são definidas da seguinte forma:

Codificação:

```
ENCODE_ELG2() Definition

// Encode as defined in Elligator2 specification
encodedKey = encode(pubkey)
// OR in 2 random bits to MSB
randomByte = CSRNG(1)
encodedKey[31] |= (randomByte & 0xc0)
```
Decodificação:

```
DECODE_ELG2() Definition

// Mask out 2 random bits from MSB
encodedKey[31] &= 0x3f
// Decode as defined in Elligator2 specification
pubkey = decode(encodedKey)
```
#### Notas

O Elligator2 duplica em média o tempo de geração de chaves, pois metade das chaves privadas resulta em chaves públicas inadequadas para codificação com Elligator2. Além disso, o tempo de geração de chaves é ilimitado com uma distribuição exponencial, já que o gerador deve continuar tentando até que um par de chaves adequado seja encontrado.

Esta sobrecarga pode ser gerenciada fazendo a geração de chaves com antecedência, em uma thread separada, para manter um pool de chaves adequadas.

O gerador executa a função ENCODE_ELG2() para determinar a adequação. Portanto, o gerador deve armazenar o resultado de ENCODE_ELG2() para que não precise ser calculado novamente.

Além disso, as chaves inadequadas podem ser adicionadas ao conjunto de chaves usadas para [NTCP2](/docs/specs/ntcp2/), onde Elligator2 não é usado. As questões de segurança de fazer isso estão por definir.

### 3) AEAD (ChaChaPoly)

AEAD usando ChaCha20 e Poly1305, igual ao [NTCP2](/docs/specs/ntcp2/). Isso corresponde ao [RFC-7539](https://tools.ietf.org/html/rfc7539), que também é usado de forma similar no TLS [RFC-7905](https://tools.ietf.org/html/rfc7905).

#### Entradas de Nova Sessão e Resposta de Nova Sessão

Entradas para as funções de criptografia/descriptografia para um bloco AEAD em uma mensagem New Session:

```
k :: 32 byte cipher key
     See New Session and New Session Reply KDFs above.

n :: Counter-based nonce, 12 bytes.
     n = 0

ad :: Associated data, 32 bytes.
      The SHA256 hash of the preceding data, as output from mixHash()

data :: Plaintext data, 0 or more bytes
```
#### Entradas de Sessão Existentes

Entradas para as funções de criptografia/descriptografia para um bloco AEAD numa mensagem de Sessão Existente:

```
k :: 32 byte session key
     As looked up from the accompanying session tag.

n :: Counter-based nonce, 12 bytes.
     Starts at 0 and incremented for each message when transmitting.
     For the receiver, the value
     as looked up from the accompanying session tag.
     First four bytes are always zero.
     Last eight bytes are the message number (n), little-endian encoded.
     Maximum value is 65535.
     Session must be ratcheted when N reaches that value.
     Higher values must never be used.

ad :: Associated data
      The session tag

data :: Plaintext data, 0 or more bytes
```
#### Formato Criptografado

Saída da função de criptografia, entrada da função de descriptografia:

```
+----+----+----+----+----+----+----+----+
|                                       |
+                                       +
|       ChaCha20 encrypted data         |
~               .   .   .               ~
|                                       |
+----+----+----+----+----+----+----+----+
|  Poly1305 Message Authentication Code |
+              (MAC)                    +
|             16 bytes                  |
+----+----+----+----+----+----+----+----+

encrypted data :: Same size as plaintext data, 0 - 65519 bytes

MAC :: Poly1305 message authentication code, 16 bytes
```
#### Notas

- Como ChaCha20 é uma cifra de fluxo, os textos simples não precisam ser preenchidos.
  Bytes adicionais do fluxo de chaves são descartados.
- A chave para a cifra (256 bits) é acordada por meio do
  SHA256 KDF. Os detalhes do KDF para cada mensagem estão em seções
  separadas abaixo.
- Os frames ChaChaPoly têm tamanho conhecido pois são encapsulados na
  mensagem de dados I2NP.
- Para todas as mensagens, o preenchimento está dentro do frame de dados autenticados.

#### Tratamento de Erros AEAD

Todos os dados recebidos que falham na verificação AEAD devem ser descartados. Nenhuma resposta é retornada.

### 4) Ratchets

Ainda usamos session tags, como antes, mas usamos ratchets para gerá-las. Session tags também tinham uma opção de rekey que nunca implementamos. Então é como um double ratchet, mas nunca fizemos o segundo.

Aqui definimos algo semelhante ao Double Ratchet do Signal. As tags de sessão são geradas de forma determinística e idêntica tanto no lado do receptor quanto do remetente.

Ao usar uma chave simétrica/ratchet de tag, eliminamos o uso de memória para armazenar session tags no lado do remetente. Também eliminamos o consumo de largura de banda do envio de conjuntos de tags. O uso do lado do receptor ainda é significativo, mas podemos reduzi-lo ainda mais, pois iremos reduzir a session tag de 32 bytes para 8 bytes.

Não utilizamos criptografia de cabeçalho conforme especificado (e opcional) no Signal, utilizamos tags de sessão em vez disso.

Ao usar um ratchet DH, alcançamos sigilo futuro (forward secrecy), que nunca foi implementado no ElGamal/AES+SessionTags.

Nota: A chave pública única da Nova Sessão não faz parte do ratchet, sua única função é criptografar a chave inicial do ratchet DH de Alice.

#### Números de Mensagem

O Double Ratchet lida com mensagens perdidas ou fora de ordem incluindo uma tag no cabeçalho de cada mensagem. O receptor procura o índice da tag, que é o número da mensagem N. Se a mensagem contém um bloco de Número da Mensagem com um valor PN, o destinatário pode deletar quaisquer tags superiores a esse valor no conjunto de tags anterior, enquanto mantém as tags ignoradas do conjunto de tags anterior caso as mensagens ignoradas cheguem mais tarde.

#### Implementação de Exemplo

Definimos as seguintes estruturas de dados e funções para implementar esses ratchets.

TAGSET_ENTRY

Uma única entrada em um TAGSET.

    INDEX

    :   An integer index, starting with 0

    SESSION_TAG

    :   An identifier to go out on the wire, 8 bytes

    SESSION_KEY

    :   A symmetric key, never goes on the wire, 32 bytes

TAGSET

Uma coleção de TAGSET_ENTRIES.

    CREATE(key, n)

    :   Generate a new TAGSET using initial cryptographic key material
        of 32 bytes. The associated session identifier is provided. The
        initial number of of tags to create is specified; this is
        generally 0 or 1 for an outgoing session. LAST_INDEX = -1
        EXTEND(n) is called.

    EXTEND(n)

    :   Generate n more TAGSET_ENTRIES by calling EXTEND() n times.

    EXTEND()

    :   Generate one more TAGSET_ENTRY, unless the maximum number
        SESSION_TAGS have already been generated. If LAST_INDEX is
        greater than or equal to 65535, return. ++ LAST_INDEX Create a
        new TAGSET_ENTRY with the LAST_INDEX value and the calculated
        SESSION_TAG. Calls RATCHET_TAG() and (optionally) RATCHET_KEY().
        For inbound sessions, the calculation of the SESSION_KEY may be
        deferred and calculated in GET_SESSION_KEY(). Calls EXPIRE()

    EXPIRE()

    :   Remove tags and keys that are too old, or if the TAGSET size
        exceeds some limit.

    RATCHET_TAG()

    :   Calculates the next SESSION_TAG based on the last SESSION_TAG.

    RATCHET_KEY()

    :   Calculates the next SESSION_KEY based on the last SESSION_KEY.

    SESSION

    :   The associated session.

    CREATION_TIME

    :   When the TAGSET was created.

    LAST_INDEX

    :   The last TAGSET_ENTRY INDEX generated by EXTEND().

    GET_NEXT_ENTRY()

    :   Used for outgoing sessions only. EXTEND(1) is called if there
        are no remaining TAGSET_ENTRIES. If EXTEND(1) did nothing, the
        max of 65535 TAGSETS have been used, and return an error.
        Returns the next unused TAGSET_ENTRY.

    GET_SESSION_KEY(sessionTag)

    :   Used for incoming sessions only. Returns the TAGSET_ENTRY
        containing the sessionTag. If found, the TAGSET_ENTRY is
        removed. If the SESSION_KEY calculation was deferred, it is
        calculated now. If there are few TAGSET_ENTRIES remaining,
        EXTEND(n) is called.

#### 4a) DH Ratchet

Ratchets mas não tão rápido quanto o Signal faz. Separamos o reconhecimento da chave recebida da geração da nova chave. No uso típico, Alice e Bob irão cada um fazer ratchet (duas vezes) imediatamente em uma Nova Sessão, mas não farão ratchet novamente.

Note que um ratchet é para uma única direção, e gera uma cadeia de ratchet de tag de Nova Sessão / chave de mensagem para essa direção. Para gerar chaves para ambas as direções, você deve fazer o ratchet duas vezes.

Você faz um ratchet toda vez que gera e envia uma nova chave. Você faz um ratchet toda vez que recebe uma nova chave.

Alice executa um ratchet uma vez ao criar uma sessão de saída não vinculada, ela não cria uma sessão de entrada (não vinculada é não respondível).

Bob faz um ratchet uma vez ao criar uma sessão inbound não vinculada, e não cria uma sessão outbound correspondente (não vinculada significa não respondível).

Alice continua enviando mensagens New Session (NS) para Bob até receber uma das mensagens New Session Reply (NSR) de Bob. Ela então usa os resultados do KDF da Seção de Payload do NSR como entradas para os ratchets da sessão (veja DH Ratchet KDF), e começa a enviar mensagens Existing Session (ES).

Para cada mensagem NS recebida, Bob cria uma nova sessão de entrada, usando os resultados do KDF da Seção de Payload da resposta como entradas para o novo DH Ratchet ES de entrada e saída.

Para cada resposta necessária, Bob envia a Alice uma mensagem NSR com a resposta no payload. É obrigatório que Bob use novas chaves efêmeras para cada NSR.

Bob deve receber uma mensagem ES de Alice em uma das sessões de entrada, antes de criar e enviar mensagens ES na sessão de saída correspondente.

Alice deve usar um temporizador para receber uma mensagem NSR de Bob. Se o temporizador expirar, a sessão deve ser removida.

Para evitar um ataque KCI e/ou de esgotamento de recursos, onde um atacante descarta as respostas NSR de Bob para manter Alice enviando mensagens NS, Alice deve evitar iniciar Novas Sessões com Bob após um certo número de tentativas devido ao tempo limite expirar.

Alice e Bob fazem cada um um ratchet DH para cada bloco NextKey recebido.

Alice e Bob geram novos ratchets de conjuntos de tags e dois ratchets de chaves simétricas após cada ratchet DH. Para cada nova mensagem ES em uma determinada direção, Alice e Bob avançam os ratchets de tag de sessão e chave simétrica.

A frequência dos ratchets DH após o handshake inicial depende da implementação. Embora o protocolo estabeleça um limite de 65535 mensagens antes que um ratchet seja necessário, ratcheting mais frequente (baseado na contagem de mensagens, tempo decorrido, ou ambos) pode fornecer segurança adicional.

Após o KDF final de handshake em sessões vinculadas, Bob e Alice devem executar a função Split() do Noise no CipherState resultante para criar chaves simétricas e de cadeia de tag independentes para sessões de entrada e saída.

##### IDS DE CONJUNTOS DE CHAVES E TAGS

Os números de ID de chave e conjunto de tags são usados para identificar chaves e conjuntos de tags. Os IDs de chave são usados em blocos NextKey para identificar a chave enviada ou usada. Os IDs de conjunto de tags são usados (com o número da mensagem) em blocos ACK para identificar a mensagem sendo confirmada. Tanto os IDs de chave quanto os de conjunto de tags se aplicam aos conjuntos de tags para uma única direção. Os números de ID de chave e conjunto de tags devem ser sequenciais.

Nos primeiros conjuntos de tags usados para uma sessão em cada direção, o ID do conjunto de tags é 0. Nenhum bloco NextKey foi enviado, então não há IDs de chave.

Para iniciar um DH ratchet, o remetente transmite um novo bloco NextKey com um ID de chave 0. O receptor responde com um novo bloco NextKey com um ID de chave 0. O remetente então começa a usar um novo conjunto de tags com um ID de conjunto de tags 1.

Conjuntos de tags subsequentes são gerados de forma similar. Para todos os conjuntos de tags usados após trocas NextKey, o número do conjunto de tags é (1 + ID da chave da Alice + ID da chave do Bob).

Os IDs do conjunto de chaves e tags começam em 0 e incrementam sequencialmente. O ID máximo do conjunto de tags é 65535. O ID máximo da chave é 32767. Quando um conjunto de tags está quase esgotado, o remetente do conjunto de tags deve iniciar uma troca NextKey. Quando o conjunto de tags 65535 está quase esgotado, o remetente do conjunto de tags deve iniciar uma nova sessão enviando uma mensagem New Session.

Com um tamanho máximo de mensagem de streaming de 1730, e assumindo nenhuma retransmissão, a transferência máxima teórica de dados usando um único conjunto de tags é 1730 * 65536 ~= 108 MB. O máximo real será menor devido às retransmissões.

O máximo teórico de transferência de dados com todos os 65536 conjuntos de tags disponíveis, antes que a sessão teria que ser descartada e substituída, é 64K * 108 MB ~= 6,9 TB.

##### FLUXO DE MENSAGENS DO DH RATCHET

A próxima troca de chaves para um conjunto de tags deve ser iniciada pelo remetente dessas tags (o proprietário do conjunto de tags de saída). O receptor (proprietário do conjunto de tags de entrada) irá responder. Para um tráfego típico de HTTP GET na camada de aplicação, Bob enviará mais mensagens e fará o ratchet primeiro ao iniciar a troca de chaves; o diagrama abaixo mostra isso. Quando Alice faz o ratchet, a mesma coisa acontece no sentido inverso.

O primeiro conjunto de tags usado após o handshake NS/NSR é o conjunto de tags 0. Quando o conjunto de tags 0 está quase esgotado, novas chaves devem ser trocadas em ambas as direções para criar o conjunto de tags 1. Depois disso, uma nova chave é enviada apenas em uma direção.

Para criar o conjunto de tags 2, o remetente de tag envia uma nova chave e o receptor de tag envia o ID de sua chave antiga como confirmação. Ambos os lados fazem um DH.

Para criar o conjunto de tags 3, o remetente de tags envia o ID de sua chave antiga e solicita uma nova chave do receptor de tags. Ambos os lados fazem um DH.

Os conjuntos de tags subsequentes são gerados da mesma forma que os conjuntos de tags 2 e 3. O número do conjunto de tags é (1 + ID da chave do remetente + ID da chave do destinatário).

```
Tag Sender                    Tag Receiver

                 ... use tag set #0 ...


(Tagset #0 almost empty)
(generate new key #0)

Next Key, forward, request reverse, with key #0  -------->
(repeat until next key received)

                            (generate new key #0, do DH, create IB Tagset #1)

        <-------------      Next Key, reverse, with key #0
                            (repeat until tag received on new tagset)

(do DH, create OB Tagset #1)


                 ... use tag set #1 ...


(Tagset #1 almost empty)
(generate new key #1)

Next Key, forward, with key #1        -------->
(repeat until next key received)

                            (reuse key #0, do DH, create IB Tagset #2)

        <--------------     Next Key, reverse, id 0
                            (repeat until tag received on new tagset)

(do DH, create OB Tagset #2)


                 ... use tag set #2 ...


(Tagset #2 almost empty)
(reuse key #1)

Next Key, forward, request reverse, id 1  -------->
(repeat until next key received)

                            (generate new key #1, do DH, create IB Tagset #3)

        <--------------     Next Key, reverse, with key #1

(do DH, create OB Tagset #3)
(reuse key #1, do DH, create IB Tagset #3)



                 ... use tag set #3 ...



     After tag set 3, repeat the above
     patterns as shown for tag sets 2 and 3.

     To create a new even-numbered tag set, the sender sends a new key
     to the receiver. The receiver sends his old key ID
     back as an acknowledgement.

     To create a new odd-numbered tag set, the sender sends a reverse request
     to the receiver. The receiver sends a new reverse key to the sender.
```
Após o DH ratchet estar completo para um tagset de saída, e um novo tagset de saída ser criado, ele deve ser usado imediatamente, e o tagset de saída antigo pode ser excluído.

Após o DH ratchet estar completo para um tagset de entrada, e um novo tagset de entrada ser criado, o receptor deve escutar por tags em ambos os tagsets, e deletar o tagset antigo após um curto período, cerca de 3 minutos.

Um resumo da progressão do conjunto de tags e ID da chave está na tabela abaixo. * indica que uma nova chave é gerada.

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">New Tag Set ID</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Sender key ID</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Rcvr key ID</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">n/a</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">n/a</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0 *</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0 *</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">2</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1 *</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">3</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1 *</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">4</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">2 *</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">2</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">2 *</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">...</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">...</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">...</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">65534</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">32767 *</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">32766</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">65535</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">32767</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">32767 *</td>
</tr>
</table>
Os números de ID do conjunto de chaves e tags devem ser sequenciais.

##### INICIALIZAÇÃO DH KDF

Esta é a definição de DH_INITIALIZE(rootKey, k) para uma única direção. Ela cria um tagset e uma "próxima chave raiz" para ser usada em um ratchet DH subsequente, se necessário.

Usamos a inicialização DH em três lugares. Primeiro, usamo-la para gerar um conjunto de tags para as New Session Replies. Segundo, usamo-la para gerar dois conjuntos de tags, um para cada direção, para uso em mensagens Existing Session. Por último, usamo-la após um DH Ratchet para gerar um novo conjunto de tags numa única direção para mensagens Existing Session adicionais.

```
Inputs:
1) rootKey = chainKey from Payload Section
2) k from the New Session KDF or split()

// KDF_RK(rk, dh_out)
keydata = HKDF(rootKey, k, "KDFDHRatchetStep", 64)

// Output 1: The next Root Key (KDF input for the next DH ratchet)
nextRootKey = keydata[0:31]
// Output 2: The chain key to initialize the new
// session tag and symmetric key ratchets
// for the tag set
ck = keydata[32:63]

// session tag and symmetric key chain keys
keydata = HKDF(ck, ZEROLEN, "TagAndKeyGenKeys", 64)
sessTag_ck = keydata[0:31]
symmKey_ck = keydata[32:63]
```
##### DH RATCHET KDF

Isso é usado após novas chaves DH serem trocadas em blocos NextKey, antes que um tagset seja esgotado.

```
// Tag sender generates new X25519 ephemeral keys
// and sends rapk to tag receiver in a NextKey block
rask = GENERATE_PRIVATE()
rapk = DERIVE_PUBLIC(rask)

// Tag receiver generates new X25519 ephemeral keys
// and sends rbpk to Tag sender in a NextKey block
rbsk = GENERATE_PRIVATE()
rbpk = DERIVE_PUBLIC(rbsk)

sharedSecret = DH(rask, rbpk) = DH(rbsk, rapk)
tagsetKey = HKDF(sharedSecret, ZEROLEN, "XDHRatchetTagSet", 32)
rootKey = nextRootKey // from previous tagset in this direction
newTagSet = DH_INITIALIZE(rootKey, tagsetKey)
```
#### 4b) Session Tag Ratchet

Ratchets para cada mensagem, como no Signal. O ratchet de tag de sessão é sincronizado com o ratchet de chave simétrica, mas o ratchet de chave do receptor pode "ficar para trás" para economizar memória.

O transmissor avança o ratchet uma vez para cada mensagem transmitida. Nenhuma tag adicional deve ser armazenada. O transmissor também deve manter um contador para 'N', o número da mensagem na cadeia atual. O valor 'N' é incluído na mensagem enviada. Consulte a definição do bloco Message Number.

O receptor deve avançar o ratchet pelo tamanho máximo da janela e armazenar as tags em um "conjunto de tags", que está associado à sessão. Uma vez recebida, a tag armazenada pode ser descartada, e se não houver tags anteriores não recebidas, a janela pode ser avançada. O receptor deve manter o valor 'N' associado a cada tag de sessão e verificar se o número na mensagem enviada corresponde a este valor. Veja a definição do bloco Message Number.

##### KDF

Esta é a definição de RATCHET_TAG().

```
Inputs:
1) Session Tag Chain key sessTag_ck
   First time: output from DH ratchet
   Subsequent times: output from previous session tag ratchet

Generated:
2) input_key_material = SESSTAG_CONSTANT
   Must be unique for this tag set (generated from chain key),
   so that the sequence isn't predictable, since session tags
   go out on the wire in plaintext.

Outputs:
1) N (the current session tag number)
2) the session tag (and symmetric key, probably)
3) the next Session Tag Chain Key (KDF input for the next session tag ratchet)

Initialization:
keydata = HKDF(sessTag_ck, ZEROLEN, "STInitialization", 64)
// Output 1: Next chain key
sessTag_chainKey = keydata[0:31]
// Output 2: The constant
SESSTAG_CONSTANT = keydata[32:63]

// KDF_ST(ck, constant)
keydata_0 = HKDF(sessTag_chainkey, SESSTAG_CONSTANT, "SessionTagKeyGen", 64)
// Output 1: Next chain key
sessTag_chainKey_0 = keydata_0[0:31]
// Output 2: The session tag
// or more if tag is longer than 8 bytes
tag_0 = keydata_0[32:39]

// repeat as necessary to get to tag_n
keydata_n = HKDF(sessTag_chainKey_(n-1), SESSTAG_CONSTANT, "SessionTagKeyGen", 64)
// Output 1: Next chain key
sessTag_chainKey_n = keydata_n[0:31]
// Output 2: The session tag
// or more if tag is longer than 8 bytes
tag_n = keydata_n[32:39]
```
#### 4c) Ratchet de Chave Simétrica

Ratchets para cada mensagem, como no Signal. Cada chave simétrica tem um número de mensagem associado e uma session tag. O ratchet da chave de sessão é sincronizado com o ratchet da tag simétrica, mas o ratchet da chave do receptor pode "ficar para trás" para economizar memória.

O transmissor avança o ratchet uma vez para cada mensagem transmitida. Nenhuma chave adicional precisa ser armazenada.

Quando o receptor recebe uma session tag, se ainda não tiver avançado o ratchet de chave simétrica até a chave associada, deve "alcançar" a chave associada. O receptor provavelmente armazenará em cache as chaves para quaisquer tags anteriores que ainda não foram recebidas. Uma vez recebidas, a chave armazenada pode ser descartada, e se não houver tags anteriores não recebidas, a janela pode ser avançada.

Para eficiência, os ratchets de session tag e chave simétrica são separados para que o ratchet de session tag possa avançar à frente do ratchet de chave simétrica. Isso também fornece alguma segurança adicional, já que os session tags são enviados pela rede.

##### KDF

Esta é a definição de RATCHET_KEY().

```
Inputs:
1) Symmetric Key Chain key symmKey_ck
   First time: output from DH ratchet
   Subsequent times: output from previous symmetric key ratchet

Generated:
2) input_key_material = SYMMKEY_CONSTANT = ZEROLEN
   No need for uniqueness. Symmetric keys never go out on the wire.
   TODO: Set a constant anyway?

Outputs:
1) N (the current session key number)
2) the session key
3) the next Symmetric Key Chain Key (KDF input for the next symmetric key ratchet)

// KDF_CK(ck, constant)
SYMMKEY_CONSTANT = ZEROLEN
// Output 1: Next chain key
keydata_0 = HKDF(symmKey_ck, SYMMKEY_CONSTANT, "SymmetricRatchet", 64)
symmKey_chainKey_0 = keydata_0[0:31]
// Output 2: The symmetric key
k_0 = keydata_0[32:63]

// repeat as necessary to get to k[n]
keydata_n = HKDF(symmKey_chainKey_(n-1), SYMMKEY_CONSTANT, "SymmetricRatchet", 64)
// Output 1: Next chain key
symmKey_chainKey_n = keydata_n[0:31]
// Output 2: The symmetric key
k_n = keydata_n[32:63]
```
### 5) Carga útil

Isso substitui o formato da seção AES definido na especificação ElGamal/AES+SessionTags.

Isto usa o mesmo formato de bloco definido na especificação [NTCP2](/docs/specs/ntcp2/). Os tipos de blocos individuais são definidos de forma diferente.

Existem preocupações de que encorajar os implementadores a compartilhar código pode levar a problemas de análise. Os implementadores devem considerar cuidadosamente os benefícios e riscos de compartilhar código, e garantir que as regras de ordenação e blocos válidos sejam diferentes para os dois contextos.

#### Seção de Payload Dados descriptografados

O comprimento criptografado é o restante dos dados. O comprimento descriptografado é 16 menor que o comprimento criptografado. Todos os tipos de bloco são suportados. O conteúdo típico inclui os seguintes blocos:

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Payload Block Type</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Type Number</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Block Length</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">DateTime</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">7</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">Termination (TBD)</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">4</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">9 typ.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">Options (TBD)</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">21+</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">Message Number (TBD)</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">6</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">TBD</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">Next Key</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">7</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">3 or 35</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">ACK</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">8</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">4 typ.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">ACK Request</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">9</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">3</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">Garlic Clove</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">11</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">varies</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">Padding</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">254</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">varies</td>
</tr>
</table>
#### Dados não criptografados

Há zero ou mais blocos no quadro criptografado. Cada bloco contém um identificador de um byte, um comprimento de dois bytes e zero ou mais bytes de dados.

Para extensibilidade, os receptores DEVEM ignorar blocos com números de tipo desconhecidos e tratá-los como preenchimento.

Os dados criptografados têm no máximo 65535 bytes, incluindo um cabeçalho de autenticação de 16 bytes, então os dados não criptografados têm no máximo 65519 bytes.

(Tag de autenticação Poly1305 não mostrada):

```
+----+----+----+----+----+----+----+----+
|blk |  size   |       data             |
+----+----+----+                        +
|                                       |
~               .   .   .               ~
|                                       |
+----+----+----+----+----+----+----+----+
|blk |  size   |       data             |
+----+----+----+                        +
|                                       |
~               .   .   .               ~
|                                       |
+----+----+----+----+----+----+----+----+
~               .   .   .               ~

blk :: 1 byte
       0 datetime
       1-3 reserved
       4 termination
       5 options
       6 previous message number
       7 next session key
       8 ack
       9 ack request
       10 reserved
       11 Garlic Clove
       224-253 reserved for experimental features
       254 for padding
       255 reserved for future extension
size :: 2 bytes, big endian, size of data to follow, 0 - 65516
data :: the data

Maximum ChaChaPoly frame is 65535 bytes.
Poly1305 tag is 16 bytes
Maximum total block size is 65519 bytes
Maximum single block size is 65519 bytes
Block type is 1 byte
Block length is 2 bytes
Maximum single block data size is 65516 bytes.
```
#### Regras de Ordenação de Blocos

Na mensagem New Session, o bloco DateTime é obrigatório e deve ser o primeiro bloco.

Outros blocos permitidos:

- Garlic Clove (tipo 11)
- Opções (tipo 5)
- Preenchimento (tipo 254)

Na mensagem New Session Reply, nenhum bloco é necessário.

Outros blocos permitidos:

- Garlic Clove (tipo 11)
- Opções (tipo 5)
- Preenchimento (tipo 254)

Nenhum outro bloco é permitido. O preenchimento, se presente, deve ser o último bloco.

Na mensagem de Sessão Existente, nenhum bloco é obrigatório, e a ordem não é especificada, exceto pelos seguintes requisitos:

Termination, se presente, deve ser o último bloco exceto por Padding. Padding, se presente, deve ser o último bloco.

Pode haver múltiplos blocos Garlic Clove em um único quadro. Pode haver até dois blocos Next Key em um único quadro. Múltiplos blocos Padding não são permitidos em um único quadro. Outros tipos de blocos provavelmente não terão múltiplos blocos em um único quadro, mas isso não é proibido.

#### DataHora

Uma expiração. Auxilia na prevenção de replay. Bob deve validar que a mensagem é recente, usando este timestamp. Bob deve implementar um filtro Bloom ou outro mecanismo para prevenir ataques de replay, se o tempo for válido. Bob também pode usar uma verificação anterior de detecção de replay para uma chave efêmera duplicada (antes ou depois da decodificação Elligator2) para detectar e descartar mensagens NS duplicadas recentes antes da descriptografia. Geralmente incluído apenas em mensagens New Session.

```
+----+----+----+----+----+----+----+
| 0  |    4    |     timestamp     |
+----+----+----+----+----+----+----+

blk :: 0
size :: 2 bytes, big endian, value = 4
timestamp :: Unix timestamp, unsigned seconds.
             Wraps around in 2106
```
#### Garlic Clove

Um único Garlic Clove descriptografado conforme especificado em [I2NP](/docs/specs/i2np/), com modificações para remover campos que não são utilizados ou são redundantes. Aviso: Este formato é significativamente diferente daquele para ElGamal/AES. Cada clove é um bloco de payload separado. Garlic Cloves não podem ser fragmentados entre blocos ou entre quadros ChaChaPoly.

```
+----+----+----+----+----+----+----+----+
| 11 |  size   |                        |
+----+----+----+                        +
|      Delivery Instructions            |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|type|  Message_ID       | Expiration   
+----+----+----+----+----+----+----+----+
     |      I2NP Message body           |
+----+                                  +
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+

size :: size of all data to follow

Delivery Instructions :: As specified in
       the Garlic Clove section of [I2NP]_.
       Length varies but is typically 1, 33, or 37 bytes

type :: I2NP message type

Message_ID :: 4 byte `Integer` I2NP message ID

Expiration :: 4 bytes, seconds since the epoch
```
Notas:

- Os implementadores devem garantir que, ao ler um bloco, dados malformados ou
  maliciosos não causem leituras que ultrapassem para o próximo bloco.
- O formato Clove Set especificado em [I2NP](/docs/specs/i2np/) não é
  usado. Cada clove está contido em seu próprio bloco.
- O cabeçalho da mensagem I2NP tem 9 bytes, com formato idêntico ao
  usado em [NTCP2](/docs/specs/ntcp2/).
- O Certificate, Message ID e Expiration da definição de Garlic Message
  em [I2NP](/docs/specs/i2np/) não são incluídos.
- O Certificate, Clove ID e Expiration da definição de Garlic Clove
  em [I2NP](/docs/specs/i2np/) não são incluídos.

#### Término

A implementação é opcional. Encerre a sessão. Este deve ser o último bloco não-preenchimento no quadro. Nenhuma mensagem adicional será enviada nesta sessão.

Não permitido em NS ou NSR. Apenas incluído em mensagens de Sessão Existente.

```
+----+----+----+----+----+----+----+----+
| 4  |  size   | rsn|     addl data     |
+----+----+----+----+                   +
~               .   .   .               ~
+----+----+----+----+----+----+----+----+

blk :: 4
size :: 2 bytes, big endian, value = 1 or more
rsn :: reason, 1 byte:
       0: normal close or unspecified
       1: termination received
       others: optional, impementation-specific
addl data :: optional, 0 or more bytes, for future expansion, debugging,
             or reason text.
             Format unspecified and may vary based on reason code.
```
#### Opções

NÃO IMPLEMENTADO, para estudo futuro. Passa opções atualizadas. As opções incluem vários parâmetros para a sessão. Consulte a seção Análise do Comprimento da Tag de Sessão abaixo para mais informações.

O bloco de opções pode ter comprimento variável, pois more_options podem estar presentes.

```
+----+----+----+----+----+----+----+----+
| 5  |  size   |ver |flg |STL |STimeout |
+----+----+----+----+----+----+----+----+
|  SOTW   |  RITW   |tmin|tmax|rmin|rmax|
+----+----+----+----+----+----+----+----+
|  tdmy   |  rdmy   |  tdelay |  rdelay |
+----+----+----+----+----+----+----+----+
|              more_options             |
~               .   .   .               ~
|                                       |
+----+----+----+----+----+----+----+----+

blk :: 5
size :: 2 bytes, big endian, size of options to follow, 21 bytes minimum
ver :: Protocol version, must be 0
flg :: 1 byte flags
       bits 7-0: Unused, set to 0 for future compatibility
STL :: Session tag length (must be 8), other values unimplemented
STimeout :: Session idle timeout (seconds), big endian
SOTW :: Sender Outbound Tag Window, 2 bytes big endian
RITW :: Receiver Inbound Tag Window 2 bytes big endian

tmin, tmax, rmin, rmax :: requested padding limits
    tmin and rmin are for desired resistance to traffic analysis.
    tmax and rmax are for bandwidth limits.
    tmin and tmax are the transmit limits for the router sending this options block.
    rmin and rmax are the receive limits for the router sending this options block.
    Each is a 4.4 fixed-point float representing 0 to 15.9375
    (or think of it as an unsigned 8-bit integer divided by 16.0).
    This is the ratio of padding to data. Examples:
    Value of 0x00 means no padding
    Value of 0x01 means add 6 percent padding
    Value of 0x10 means add 100 percent padding
    Value of 0x80 means add 800 percent (8x) padding
    Alice and Bob will negotiate the minimum and maximum in each direction.
    These are guidelines, there is no enforcement.
    Sender should honor receiver's maximum.
    Sender may or may not honor receiver's minimum, within bandwidth constraints.

tdmy: Max dummy traffic willing to send, 2 bytes big endian, bytes/sec average
rdmy: Requested dummy traffic, 2 bytes big endian, bytes/sec average
tdelay: Max intra-message delay willing to insert, 2 bytes big endian, msec average
rdelay: Requested intra-message delay, 2 bytes big endian, msec average

more_options :: Format undefined, for future use
```
SOTW é a recomendação do remetente para o destinatário sobre a janela de tags de entrada do destinatário (o máximo de antecipação). RITW é a declaração do remetente sobre a janela de tags de entrada (máximo de antecipação) que ele planeja usar. Cada lado então define ou ajusta a antecipação com base em algum mínimo ou máximo ou outro cálculo.

Notas:

- O suporte para comprimento de tag de sessão não padrão esperançosamente nunca será
  necessário.
- A janela de tag é MAX_SKIP na documentação do Signal.

Problemas:

- A negociação de opções está TBD.
- Padrões TBD.
- As opções de padding e atraso são copiadas do NTCP2, mas essas opções
  não foram totalmente implementadas ou estudadas lá.

#### Números de Mensagem

A implementação é opcional. O comprimento (número de mensagens enviadas) no conjunto de tags anterior (PN). O receptor pode deletar imediatamente tags maiores que PN do conjunto de tags anterior. O receptor pode expirar tags menores ou iguais a PN do conjunto de tags anterior após um curto período de tempo (por exemplo, 2 minutos).

```
+----+----+----+----+----+
| 6  |  size   |  PN    |
+----+----+----+----+----+

blk :: 6
size :: 2
PN :: 2 bytes big endian. The index of the last tag sent in the previous tag set.
```
Notas:

- O PN máximo é 65535.
- As definições de PN são iguais à definição do Signal, menos uma.
  Isso é similar ao que o Signal faz, mas no Signal, PN e N estão no
  cabeçalho. Aqui, eles estão no corpo da mensagem criptografada.
- Não envie este bloco no conjunto de tags 0, porque não havia conjunto de tags
  anterior.

#### Próxima Chave Pública DH Ratchet

A próxima chave de ratchet DH está no payload, e é opcional. Não fazemos ratchet toda vez. (Isto é diferente do Signal, onde está no cabeçalho e é enviada sempre)

Para o primeiro ratchet, Key ID = 0.

Não permitido em NS ou NSR. Incluído apenas em mensagens de Sessão Existente.

```
+----+----+----+----+----+----+----+----+
| 7  |  size   |flag|  key ID |         |
+----+----+----+----+----+----+         +
|                                       |
+                                       +
|     Next DH Ratchet Public Key        |
+                                       +
|                                       |
+                             +----+----+
|                             |
+----+----+----+----+----+----+

blk :: 7
size :: 3 or 35
flag :: 1 byte flags
        bit order: 76543210
        bit 0: 1 for key present, 0 for no key present
        bit 1: 1 for reverse key, 0 for forward key
        bit 2: 1 to request reverse key, 0 for no request
               only set if bit 1 is 0
        bits 7-2: Unused, set to 0 for future compatibility
key ID :: The key ID of this key. 2 bytes, big endian
          0 - 32767
Public Key :: The next X25519 public key, 32 bytes, little endian
              Only if bit 0 is 1
```
Notas:

- O Key ID é um contador incremental para a chave local usada para esse conjunto de tags, começando em 0.
- O ID não deve mudar a menos que a chave mude.
- Pode não ser estritamente necessário, mas é útil para depuração. O Signal não usa um key ID.
- O Key ID máximo é 32767.
- No caso raro em que os conjuntos de tags em ambas as direções estão fazendo ratcheting ao mesmo tempo, um frame conterá dois blocos Next Key, um para a chave direta e um para a chave reversa.
- Os números de ID do conjunto de chaves e tags devem ser sequenciais.
- Consulte a seção DH Ratchet acima para detalhes.

#### Confirmação

Isso só é enviado se um bloco de solicitação de ack foi recebido. Múltiplos acks podem estar presentes para confirmar múltiplas mensagens.

Não permitido em NS ou NSR. Incluído apenas em mensagens de Sessão Existente.

```
+----+----+----+----+----+----+----+----+
| 8  |  size   |tagsetid |   N     |    |
+----+----+----+----+----+----+----+    +
|             more acks                 |
~               .   .   .               ~
|                                       |
+----+----+----+----+----+----+----+----+

blk :: 8
size :: 4 * number of acks to follow, minimum 1 ack
for each ack:
tagsetid :: 2 bytes, big endian, from the message being acked
N :: 2 bytes, big endian, from the message being acked
```
Notas:

- O ID do conjunto de tags e N identificam exclusivamente a mensagem sendo confirmada.
- Nos primeiros conjuntos de tags usados para uma sessão em cada direção, o
  ID do conjunto de tags é 0.
- Nenhum bloco NextKey foi enviado, então não há IDs de chave.
- Para todos os conjuntos de tags usados após trocas NextKey, o número do conjunto de tags é
  (1 + ID da chave da Alice + ID da chave do Bob).

#### Solicitação de Confirmação

Solicitar um ack in-band. Para substituir a Mensagem DeliveryStatus out-of-band no Garlic Clove.

Se um ack explícito for solicitado, o ID do tagset atual e o número da mensagem (N) são retornados em um bloco de ack.

Não permitido em NS ou NSR. Apenas incluído em mensagens de Sessão Existente.

```
+----+----+----+----+
|  9 |  size   |flg |
+----+----+----+----+

blk :: 9
size :: 1
flg :: 1 byte flags
       bits 7-0: Unused, set to 0 for future compatibility
```
#### Preenchimento

Todo o preenchimento está dentro dos frames AEAD. TODO O preenchimento dentro do AEAD deve aderir aproximadamente aos parâmetros negociados. TODO Alice enviou seus parâmetros mín/máx tx/rx solicitados na mensagem NS. TODO Bob enviou seus parâmetros mín/máx tx/rx solicitados na mensagem NSR. Opções atualizadas podem ser enviadas durante a fase de dados. Veja as informações do bloco de opções acima.

Se presente, este deve ser o último bloco no quadro.

```
+----+----+----+----+----+----+----+----+
|254 |  size   |      padding           |
+----+----+----+                        +
|                                       |
~               .   .   .               ~
|                                       |
+----+----+----+----+----+----+----+----+

blk :: 254
size :: 2 bytes, big endian, 0-65516
padding :: zeros or random data
```
Notas:

- Preenchimento com todos zeros é adequado, pois será criptografado.
- Estratégias de preenchimento a definir.
- Frames somente de preenchimento são permitidos.
- Preenchimento padrão é 0-15 bytes.
- Veja bloco de opções para negociação de parâmetros de preenchimento
- Veja bloco de opções para parâmetros mín/máx de preenchimento
- Resposta do router em caso de violação do preenchimento negociado é
  dependente da implementação.

#### Outros tipos de blocos

As implementações devem ignorar tipos de blocos desconhecidos para compatibilidade futura.

#### Trabalho futuro

- O comprimento do preenchimento deve ser decidido por mensagem e
  estimativas da distribuição de comprimento, ou atrasos aleatórios devem ser
  adicionados. Essas contramedidas devem ser incluídas para resistir à DPI, pois
  os tamanhos das mensagens revelariam que o tráfego I2P está sendo transportado
  pelo protocolo de transporte. O esquema exato de preenchimento é uma área de
  trabalho futuro, o Apêndice A fornece mais informações sobre o tópico.

## Padrões de Uso Típicos

### HTTP GET

Este é o caso de uso mais típico, e a maioria dos casos de uso de streaming não-HTTP será idêntica a este caso também. Uma pequena mensagem inicial é enviada, uma resposta segue, e mensagens adicionais são enviadas em ambas as direções.

Um HTTP GET geralmente cabe em uma única mensagem I2NP. Alice envia uma pequena solicitação com uma única mensagem de Sessão nova, agrupando um leaseSet de resposta. Alice inclui ratchet imediato para nova chave. Inclui assinatura para vincular ao destino. Nenhuma confirmação solicitada.

Bob executa o ratchet imediatamente.

Alice faz o ratchet imediatamente.

Continua com essas sessões.

```
Alice                           Bob

  New Session (1b)     ------------------->
  with ephemeral key 1
  with static key for binding
  with next key
  with bundled HTTP GET
  with bundled LS
  without bundled Delivery Status Message

  any retransmissions, same as above

  following messages may arrive in any order:

  <--------------     New Session Reply (1g)
                      with Bob ephemeral key 1
                      with bundled HTTP reply part 1

  <--------------     New Session Reply (1g)
                      with Bob ephemeral key 2
                      with bundled HTTP reply part 2

  <--------------     New Session Reply (1g)
                      with Bob ephemeral key 3
                      with bundled HTTP reply part 3

  After reception of any of these messages,
  Alice switches to use Existing Session messages,
  creates a new inbound + outbound session pair,
  and ratchets.


  Existing Session     ------------------->
  with bundled streaming ack


  Existing Session     ------------------->
  with bundled streaming ack


  After reception of any of these messages,
  Bob switches to use Existing Session messages.


  <--------------     Existing Session
                      with bundled HTTP reply part 4


  Existing Session     ------------------->
  with bundled streaming ack

  <--------------     Existing Session
                      with bundled HTTP reply part 5
```
### HTTP POST

Alice tem três opções:

1)  Enviar apenas a primeira mensagem (tamanho da janela = 1), como no HTTP GET. Não

    recommended.
2)  Enviar até a janela de streaming, mas usando a mesma codificação Elligator2

    cleartext public key. All messages contain same next public key
    (ratchet). This will be visible to OBGW/IBEP because they all start
    with the same cleartext. Things proceed as in 1). Not recommended.
3)  Implementação recomendada. Enviar até a janela de streaming, mas usando uma

    different Elligator2-encoded cleartext public key (session) for
    each. All messages contain same next public key (ratchet). This will
    not be visible to OBGW/IBEP because they all start with different
    cleartext. Bob must recognize that they all contain the same next
    public key, and respond to all with the same ratchet. Alice uses
    that next public key and continues.

Fluxo de mensagens da Opção 3:

```
Alice                           Bob

  New Session (1b)     ------------------->
  with ephemeral key 1
  with static key for binding
  with bundled HTTP POST part 1
  with bundled LS
  without bundled Delivery Status Message


  New Session (1b)     ------------------->
  with ephemeral key 2
  with static key for binding
  with bundled HTTP POST part 2
  with bundled LS
  without bundled Delivery Status Message


  New Session (1b)     ------------------->
  with ephemeral key 3
  with static key for binding
  with bundled HTTP POST part 3
  with bundled LS
  without bundled Delivery Status Message


  following messages can arrive in any order:

  <--------------     New Session Reply (1g)
                      with Bob ephemeral key 1
                      with bundled streaming ack

  <--------------     New Session Reply (1g)
                      with Bob ephemeral key 2
                      with bundled streaming ack

  After reception of any of these messages,
  Alice switches to use Existing Session messages,
  creates a new inbound + outbound session pair,
  and ratchets.


  following messages can arrive in any order:


  Existing Session     ------------------->
  with bundled HTTP POST part 4

  Existing Session     ------------------->
  with next key
  with bundled HTTP POST part 5


  After reception of any of these messages,
  Bob switches to use Existing Session messages.


  <--------------     Existing Session
                      with bundled streaming ack

  After reception of any of this message,
  Alice switches to use Existing Session messages,
  and Alice ratchets.


  Existing Session     ------------------->
  with next key
  with bundled HTTP POST part 4

  after reception of this message, Bob ratchets

  Existing Session     ------------------->
  with next key
  with bundled HTTP POST part 5

  <--------------     Existing Session
                      with bundled streaming ack
```
### Datagrama Replicável

Uma única mensagem, com uma única resposta esperada. Mensagens ou respostas adicionais podem ser enviadas.

Semelhante ao HTTP GET, mas com opções menores para tamanho da janela de tag de sessão e tempo de vida. Talvez não solicite um ratchet.

```
Alice                           Bob

  New Session (1b)     ------------------->
  with static key for binding
  with next key
  with bundled repliable datagram
  with bundled LS
  without bundled Delivery Status Message


  <--------------     New Session Reply (1g)
                      with Bob ephemeral key
                      with bundled reply part 1

  <--------------     New Session Reply (1g)
                      with Bob ephemeral key
                      with bundled reply part 2

  After reception of either message,
  Alice switches to use Existing Session messages,
  and ratchets.

  If the Existing Session message arrives first,
  Alice ratchets on the existing inbound and outbound
  sessions.

  When the New Session Reply arrives, Alice
  sets the existing inbound session to expire,
  creates a new inbound and outbound session,
  and sends Existing Session messages on
  the new outbound session.

  Alice keeps the expiring inbound session
  around for a while to process the Existing Session
  message sent to Alice.
  If all expected original Existing Session message replies
  have been processed, Alice can expire the original
  inbound session immediately.

  if there are any other messages:

  Existing Session     ------------------->
  with bundled message

  Existing Session     ------------------->
  with bundled streaming ack

  <--------------     Existing Session
                      with bundled message
```
### Múltiplos Datagramas Raw

Múltiplas mensagens anônimas, sem respostas esperadas.

Neste cenário, Alice solicita uma sessão, mas sem vinculação. Uma nova mensagem de sessão é enviada. Nenhum leaseSet de resposta é incluído. Um DSM de resposta é incluído (este é o único caso de uso que requer DSMs incluídos). Nenhuma próxima chave é incluída. Nenhuma resposta ou ratchet é solicitado. Nenhum ratchet é enviado. As opções definem a janela de tags da sessão como zero.

```
Alice                           Bob

  New Session (1c)     ------------------->
  with bundled message
  without bundled LS
  with bundled Delivery Status Message 1

  New Session (1c)     ------------------->
  with bundled message
  without bundled LS
  with bundled Delivery Status Message 2

  New Session (1c)     ------------------->
  with bundled message
  without bundled LS
  with bundled Delivery Status Message 3
 
  following messages can arrive in any order:

  <--------------     Delivery Status Message 1

  <--------------     Delivery Status Message 2

  <--------------     Delivery Status Message 3

  After reception of any of these messages,
  Alice switches to use Existing Session messages.

  Existing Session     ------------------->

  Existing Session     ------------------->

  Existing Session     ------------------->
```
### Datagrama Bruto Único

Uma única mensagem anônima, sem resposta esperada.

Mensagem única é enviada. Nenhum LS de resposta ou DSM é incluído. Nenhuma próxima chave é incluída. Nenhuma resposta ou ratchet é solicitado. Nenhum ratchet é enviado. Opções definem a janela de tags de sessão como zero.

```
Alice                           Bob

  One-Time Message (1d)   ------------------->
  with bundled message
  without bundled LS
  without bundled Delivery Status Message
```
### Sessões de Longa Duração

Sessões de longa duração podem fazer ratchet, ou solicitar um ratchet, a qualquer momento, para manter o sigilo futuro a partir desse ponto no tempo. As sessões devem fazer ratchet quando se aproximam do limite de mensagens enviadas por sessão (65535).

## Considerações de Implementação

### Defesa

Assim como no protocolo ElGamal/AES+SessionTag existente, as implementações devem limitar o armazenamento de session tags e proteger contra ataques de esgotamento de memória.

Algumas estratégias recomendadas incluem:

- Limite rígido no número de session tags armazenadas
- Expiração agressiva de sessões inbound inativas quando sob pressão de memória
- Limite no número de sessões inbound vinculadas a um único destino remoto
- Redução adaptativa da janela de session tag e exclusão de tags antigas não utilizadas quando sob pressão de memória
- Recusa em fazer ratchet quando solicitado, se sob pressão de memória

### Parâmetros

Parâmetros e timeouts recomendados:

- Tamanho do tagset NSR: 12 tsmin e tsmax
- Tamanho do tagset ES 0: tsmin 24, tsmax 160
- Tamanho do tagset ES (1+): 160 tsmin e tsmax
- Timeout do tagset NSR: 3 minutos para receptor
- Timeout do tagset ES: 8 minutos para remetente, 10 minutos para receptor
- Remover tagset ES anterior após: 3 minutos
- Antecipação do tagset da tag N: min(tsmax, tsmin + N/4)
- Aparar tagset atrás da tag N: min(tsmax, tsmin + N/4) / 2
- Enviar próxima chave na tag: 4096
- Enviar próxima chave após tempo de vida do tagset: A definir
- Substituir sessão se NS recebido após: 3 minutos
- Desvio máximo de relógio: -5 minutos a +2 minutos
- Duração do filtro de replay NS: 5 minutos
- Tamanho do padding: 0-15 bytes (outras estratégias a definir)

### Classificação

A seguir estão as recomendações para classificar mensagens recebidas.

#### Apenas X25519

Em um tunnel que é usado exclusivamente com este protocolo, faça a identificação como é feito atualmente com ElGamal/AES+SessionTags:

Primeiro, trate os dados iniciais como uma tag de sessão e procure pela tag de sessão. Se encontrada, descriptografe usando os dados armazenados associados a essa tag de sessão.

Se não for encontrado, trate os dados iniciais como uma chave pública DH e nonce. Execute uma operação DH e o KDF especificado, e tente descriptografar os dados restantes.

#### X25519 Compartilhado com ElGamal/AES+SessionTags

Em um tunnel que suporta tanto este protocolo quanto ElGamal/AES+SessionTags, classifique as mensagens recebidas da seguinte forma:

Devido a uma falha na especificação ElGamal/AES+SessionTags, o bloco AES não é preenchido para um comprimento aleatório não-mod-16. Portanto, o comprimento das mensagens de Sessão Existente mod 16 é sempre 0, e o comprimento das mensagens de Nova Sessão mod 16 é sempre 2 (já que o bloco ElGamal tem 514 bytes de comprimento).

Se o comprimento mod 16 não for 0 ou 2, trate os dados iniciais como uma session tag e procure pela session tag. Se encontrada, descriptografe usando os dados armazenados associados a essa session tag.

Se não encontrado, e o comprimento mod 16 não for 0 ou 2, trate os dados iniciais como uma chave pública DH e nonce. Execute uma operação DH e o KDF especificado, e tente descriptografar os dados restantes. (com base na mistura de tráfego relativa e nos custos relativos das operações DH X25519 e ElGamal, este passo pode ser feito por último)

Caso contrário, se o comprimento mod 16 for 0, trate os dados iniciais como uma session tag ElGamal/AES e procure pela session tag. Se encontrada, descriptografe usando os dados armazenados associados a essa session tag.

Se não encontrado, e os dados têm pelo menos 642 (514 + 128) bytes de comprimento, e o comprimento mod 16 é 2, trate os dados iniciais como um bloco ElGamal. Tente descriptografar os dados restantes.

Note que se a especificação ElGamal/AES+SessionTag for atualizada para permitir preenchimento não-mod-16, as coisas precisarão ser feitas de forma diferente.

### Retransmissões e Transições de Estado

A camada ratchet não faz retransmissões e, com duas exceções, não usa temporizadores para transmissões. Temporizadores também são necessários para timeout de tagset.

Os timers de transmissão são usados apenas para enviar NSR e para responder com um ES quando um ES recebido contém uma solicitação ACK. O timeout recomendado é de um segundo. Na maioria dos casos, a camada superior (datagrama ou streaming) irá responder, forçando um NSR ou ES, e o timer pode ser cancelado. Se o timer disparar, envie um payload vazio com o NSR ou ES.

#### Respostas da Camada Ratchet

As implementações iniciais dependem de tráfego bidirecional nas camadas superiores. Ou seja, as implementações assumem que o tráfego na direção oposta será transmitido em breve, o que forçará qualquer resposta necessária na camada ECIES.

No entanto, certo tráfego pode ser unidirecional ou de largura de banda muito baixa, de tal forma que não há tráfego de camada superior para gerar uma resposta em tempo hábil.

O recebimento de mensagens NS e NSR requer uma resposta; o recebimento de blocos ACK Request e Next Key também requer uma resposta.

As implementações devem iniciar um temporizador quando uma dessas mensagens que requer resposta é recebida, e gerar uma resposta "vazia" (sem bloco Garlic Clove) na camada ECIES se nenhum tráfego reverso for enviado em um curto período de tempo (por exemplo, 1 segundo).

Também pode ser apropriado um timeout ainda mais curto para respostas a mensagens NS e NSR, para transferir o tráfego para as mensagens ES eficientes o mais rápido possível.

#### Vinculação NS Para NSR

Na camada ratchet, como Bob, Alice é conhecida apenas pela chave estática. A mensagem NS é autenticada ([Noise](https://noiseprotocol.org/noise.html) IK sender authentication 1). No entanto, isso não é suficiente para a camada ratchet ser capaz de enviar qualquer coisa para Alice, pois o roteamento de rede requer um Destination completo.

Antes que o NSR possa ser enviado, o Destination completo de Alice deve ser descoberto pela camada ratchet ou por um protocolo de camada superior que permita resposta, seja [Datagrams](/docs/specs/datagrams/) com resposta ou [Streaming](/docs/specs/streaming/). Após encontrar o Leaseset para esse Destination, esse Leaseset conterá a mesma chave estática contida no NS.

Tipicamente, a camada superior irá responder, forçando uma consulta de base de dados de rede do Leaseset de Alice pelo Hash de Destino de Alice. Esse Leaseset quase sempre será encontrado localmente, porque o NS continha um bloco Garlic Clove, contendo uma mensagem Database Store, contendo o Leaseset de Alice.

Para que Bob esteja preparado para enviar um NSR da camada ratchet e vincular a sessão pendente ao Destination de Alice, Bob deve "capturar" o Destination enquanto processa o payload NS. Se uma mensagem Database Store for encontrada contendo um Leaseset com uma chave que corresponde à chave estática no NS, a sessão pendente agora está vinculada àquele Destination, e Bob sabe onde enviar qualquer NSR se o temporizador de resposta expirar. Esta é a implementação recomendada.

Um design alternativo é manter um cache ou banco de dados onde a chave estática é mapeada para um Destination. A segurança e praticidade desta abordagem é um tópico para estudo posterior.

Nem esta especificação nem outras exigem estritamente que cada NS contenha o Leaseset da Alice. No entanto, na prática, deveria conter. O timeout recomendado do remetente do tagset ES (8 minutos) é menor que o timeout máximo do Leaseset (10 minutos), então poderia haver uma pequena janela onde a sessão anterior expirou, Alice pensa que Bob ainda tem seu Leaseset válido, e não envia um novo Leaseset com o novo NS. Este é um tópico para estudo adicional.

#### Múltiplas Mensagens NS

Se nenhuma resposta NSR for recebida antes que a camada superior (datagrama ou streaming) envie mais dados, possivelmente como uma retransmissão, Alice deve compor um novo NS, usando uma nova chave efêmera. Não reutilize a chave efêmera de qualquer NS anterior. Alice deve manter o estado de handshake adicional e o conjunto de tags de recebimento derivado, para receber mensagens NSR em resposta a qualquer NSR que foi enviado.

As implementações podem limitar o número total de mensagens NS enviadas, ou a taxa de envio de mensagens NS, seja enfileirando ou descartando mensagens de camadas superiores antes de serem enviadas.

Em certas situações, quando sob alta carga, ou sob certos cenários de ataque, pode ser apropriado para Bob enfileirar, descartar ou limitar mensagens NS aparentes sem tentar descriptografar, para evitar um ataque de esgotamento de recursos.

Para cada NS recebido, Bob gera um tagset outbound NSR, envia um NSR, faz um split(), e gera os tagsets ES inbound e outbound. No entanto, Bob não envia nenhuma mensagem ES até que a primeira mensagem ES no tagset inbound correspondente seja recebida. Depois disso, Bob pode descartar todos os estados de handshake e tagsets para qualquer outro NS recebido ou NSR enviado, ou permitir que expirem em breve. Não use tagsets NSR para mensagens ES.

É um tópico para estudos futuros se Bob pode escolher enviar especulativamente mensagens ES imediatamente após o NSR, mesmo antes de receber o primeiro ES de Alice. Em determinados cenários e padrões de tráfego, isso poderia economizar largura de banda e CPU substanciais. Esta estratégia pode ser baseada em heurísticas como padrões de tráfego, porcentagem de ESs recebidos no tagset da primeira sessão, ou outros dados.

#### Múltiplas Mensagens NSR

Para cada mensagem NS recebida, até que uma mensagem ES seja recebida, Bob deve responder com um novo NSR, seja devido ao tráfego de camada superior sendo enviado, ou expiração do timer de envio NSR.

Cada NSR usa o estado de handshake e conjunto de tags correspondente ao NS recebido. Bob deve manter o estado de handshake e conjunto de tags para todas as mensagens NS recebidas, até que uma mensagem ES seja recebida.

As implementações podem limitar o número total de mensagens NSR enviadas, ou a taxa de envio de mensagens NSR, seja enfileirando ou descartando mensagens de camadas superiores antes que sejam enviadas. Essas podem ser limitadas tanto quando causadas por mensagens NS recebidas, quanto por tráfego adicional de saída de camadas superiores.

Em certas situações, quando sob alta carga, ou sob certos cenários de ataque, pode ser apropriado para Alice enfileirar, descartar, ou limitar mensagens NSR sem tentar descriptografar, para evitar um ataque de esgotamento de recursos. Esses limites podem ser tanto totais em todas as sessões, por sessão, ou ambos.

Uma vez que Alice recebe um NSR, Alice faz um split() para derivar as chaves de sessão ES. Alice deve configurar um temporizador e enviar uma mensagem ES vazia se a camada superior não enviar nenhum tráfego, tipicamente dentro de um segundo.

Os outros tagsets NSR de entrada podem ser removidos em breve ou podem expirar, mas Alice deve mantê-los por um curto período, para descriptografar quaisquer outras mensagens NSR que sejam recebidas.

### Prevenção de Replay

Bob deve implementar um filtro Bloom ou outro mecanismo para prevenir ataques de replay NS, se o DateTime incluído for recente, e rejeitar mensagens NS onde o DateTime for muito antigo. Bob também pode usar uma verificação anterior de detecção de replay para uma chave efêmera duplicada (seja pré ou pós-decodificação Elligator2) para detectar e descartar mensagens NS duplicadas recentes antes da descriptografia.

Mensagens NSR e ES têm prevenção de replay inerente porque a etiqueta de sessão é de uso único.

Mensagens garlic também possuem prevenção contra replay se o router implementar um filtro Bloom ao nível do router baseado no ID da mensagem I2NP.

## Mudanças Relacionadas

Consultas de Banco de Dados de Destinos ECIES: Consulte [Prop154](/proposals/154-ratchet/), agora incorporada em [I2NP](/docs/specs/i2np/) para a versão 0.9.46.

Esta especificação requer suporte LS2 para publicar a chave pública X25519 com o leaseset. Nenhuma alteração é necessária nas especificações LS2 em [I2NP](/docs/specs/i2np/). Todo o suporte foi projetado, especificado e implementado na [Prop123](/proposals/123-new-netdb-entries/) implementada na versão 0.9.38.

Esta especificação requer que uma propriedade seja definida nas opções I2CP para ser habilitada. Todo o suporte foi projetado, especificado e implementado em [Prop123](/proposals/123-new-netdb-entries/) implementado na versão 0.9.38.

A opção necessária para habilitar ECIES é uma única propriedade I2CP para I2CP, BOB, SAM, ou i2ptunnel.

Valores típicos são i2cp.leaseSetEncType=4 apenas para ECIES, ou i2cp.leaseSetEncType=4,0 para chaves duplas ECIES e ElGamal.

## Compatibilidade

Qualquer router que suporte LS2 com chaves duplas (0.9.38 ou superior) deve suportar conexão a destinos com chaves duplas.

Destinos somente ECIES requerem que a maioria dos floodfills seja atualizada para 0.9.46 para receber respostas de consulta criptografadas. Veja [Prop154](/proposals/154-ratchet/).

Destinos somente ECIES só podem conectar com outros destinos que sejam somente ECIES ou de chave dupla.

## Referências

- [Common](/docs/specs/common-structures/)
- [CRYPTO-ELG](/docs/specs/cryptography/#elgamal)
- [Datagrams](/docs/specs/datagrams/)
- [ECIES-HYBRID](/docs/specs/ecies-hybrid/)
- [ElG-AES](/docs/specs/elgamal-aes/)
- [Elligator2](https://elligator.cr.yp.to/elligator-20130828.pdf) - Veja também [artigo sobre Elligator](https://www.imperialviolet.org/2013/12/25/elligator.html) e código OBFS4
- [GARLICSPEC](/docs/overview/garlic-routing/)
- [I2CP](/docs/specs/i2cp/)
- [I2NP](/docs/specs/i2np/)
- [NOISE](https://noiseprotocol.org/noise.html)
- [NTCP2](/docs/specs/ntcp2/)
- [Prop111](/proposals/111-ntcp2/)
- [Prop123](/proposals/123-new-netdb-entries/)
- [Prop142](/proposals/142-ecies-template/)
- [Prop144](/proposals/144-ecies-x25519/)
- [Prop145](/proposals/145-ecies-ecdh-aes/)
- [Prop152](/proposals/152-ecies-config/)
- [Prop153](/proposals/153-chacha20-layer/)
- [Prop154](/proposals/154-ratchet/)
- [RFC-2104](https://tools.ietf.org/html/rfc2104)
- [RFC-4880-S5.1](https://tools.ietf.org/html/rfc4880#section-5.1)
- [RFC-5869](https://tools.ietf.org/html/rfc5869)
- [RFC-7539](https://tools.ietf.org/html/rfc7539)
- [RFC-7748](https://tools.ietf.org/html/rfc7748)
- [RFC-7905](https://tools.ietf.org/html/rfc7905)
- [Signal](https://signal.org/docs/specifications/doubleratchet/)
- [SSU](/docs/transport/ssu/)
- [SSU2](/docs/specs/ssu2/)
- [STS](https://en.wikipedia.org/wiki/Station-to-Station_protocol) - Diffie, W.; van Oorschot P. C.; Wiener M. J., Authentication and Authenticated Key Exchanges
- [Streaming](/docs/specs/streaming/)
