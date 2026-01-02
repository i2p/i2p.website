---
title: "ECIES-X25519-AEAD-Ratchet"
number: "144"
author: "zzz, chisana, orignal"
created: "2018-11-22"
lastupdated: "2025-03-05"
status: "Fechado"
thread: "http://zzz.i2p/topics/2639"
target: "0.9.46"
implementedin: "0.9.46"
toc: true
---

## Nota

Implantação e teste de rede em andamento. Sujeito a pequenas revisões. Consulte [SPEC](/docs/specs/ecies/) para a especificação oficial.

As seguintes funcionalidades não estão implementadas a partir da versão 0.9.46:

- Blocos MessageNumbers, Options e Termination
- Respostas da camada de protocolo
- Chave estática zero
- Multicast

## Visão Geral

Esta é uma proposta para o primeiro novo tipo de criptografia ponta a ponta desde o início do I2P, para substituir ElGamal/AES+SessionTags [Elg-AES](/docs/legacy/elgamal-aes/).

Baseia-se no trabalho anterior da seguinte forma:

- Especificação de estruturas comuns [Common Structures](/docs/specs/common-structures/)
- Especificação [I2NP](/docs/specs/i2np/) incluindo LS2
- ElGamal/AES+Session Tags [Elg-AES](/docs/legacy/elgamal-aes/)
- [http://zzz.i2p/topics/1768](http://zzz.i2p/topics/1768) visão geral da nova criptografia assimétrica
- Visão geral da criptografia de baixo nível [CRYPTO-ELG](/docs/specs/cryptography/)
- ECIES [http://zzz.i2p/topics/2418](http://zzz.i2p/topics/2418)
- [NTCP2](/docs/specs/ntcp2/) [Proposta 111](/proposals/111-ntcp-2/)
- 123 Novas Entradas netDB
- 142 Novo Modelo de Criptografia
- Protocolo [Noise](https://noiseprotocol.org/noise.html)
- Algoritmo double ratchet do [Signal](https://signal.org/docs/)

O objetivo é suportar nova encriptação para comunicação ponto a ponto, de destino para destino.

O design usará um handshake Noise e uma fase de dados incorporando o double ratchet do Signal.

Todas as referências ao Signal e Noise nesta proposta são apenas para informação de contexto. O conhecimento dos protocolos Signal e Noise não é necessário para entender ou implementar esta proposta.

### Current ElGamal Uses

Para revisão, chaves públicas ElGamal de 256 bytes podem ser encontradas nas seguintes estruturas de dados. Consulte a especificação de estruturas comuns.

- Em uma Router Identity
  Esta é a chave de criptografia do router.

- Em um Destination
  A chave pública do destination foi usada para a antiga criptografia i2cp-to-i2cp
  que foi desabilitada na versão 0.6, atualmente não é utilizada exceto para
  o IV para criptografia LeaseSet, que está obsoleta.
  A chave pública no LeaseSet é usada em seu lugar.

- Em um LeaseSet
  Esta é a chave de criptografia do destino.

- Em um LS2
  Esta é a chave de criptografia do destino.

### EncTypes in Key Certs

Como revisão, adicionamos suporte para tipos de criptografia quando adicionamos suporte para tipos de assinatura. O campo do tipo de criptografia é sempre zero, tanto em Destinations quanto em RouterIdentities. Se isso deve ser alterado algum dia está por ser determinado (TBD). Consulte a especificação de estruturas comuns [Common Structures](/docs/specs/common-structures/).

### Usos Atuais do ElGamal

Como revisão, usamos ElGamal para:

1) Mensagens de construção de tunnel (chave está na RouterIdentity)    A substituição não é coberta nesta proposta.    Veja a proposta 152 [Proposta 152](/proposals/152-ecies-tunnels).

2) Criptografia router-para-router de netDb e outras mensagens I2NP (Chave está na RouterIdentity)    Depende desta proposta.    Requer uma proposta para 1) também, ou colocar a chave nas opções RI.

3) Cliente End-to-end ElGamal+AES/SessionTag (chave está no LeaseSet, a chave de Destino não é usada)    A substituição ESTÁ coberta nesta proposta.

4) DH Efêmero para NTCP1 e SSU    A substituição não está coberta nesta proposta.    Veja a proposta 111 para NTCP2.    Nenhuma proposta atual para SSU2.

### EncTypes em Key Certs

- Compatível com versões anteriores
- Requer e baseia-se no LS2 (proposta 123)
- Aproveita nova criptografia ou primitivas adicionadas para NTCP2 (proposta 111)
- Nenhuma nova criptografia ou primitivas necessárias para suporte
- Manter desacoplamento de criptografia e assinatura; suportar todas as versões atuais e futuras
- Habilitar nova criptografia para destinos
- Habilitar nova criptografia para routers, mas apenas para mensagens garlic - construção de túnel seria
  uma proposta separada
- Não quebrar nada que dependa de hashes de destino binários de 32 bytes, por exemplo, bittorrent
- Manter entrega de mensagem 0-RTT usando DH ephemeral-static
- Não exigir buffering / enfileiramento de mensagens nesta camada de protocolo;
  continuar suportando entrega ilimitada de mensagens em ambas as direções sem aguardar resposta
- Atualizar para DH ephemeral-ephemeral após 1 RTT
- Manter manipulação de mensagens fora de ordem
- Manter segurança de 256 bits
- Adicionar forward secrecy
- Adicionar autenticação (AEAD)
- Muito mais eficiente em CPU que ElGamal
- Não depender do Java jbigi para tornar DH eficiente
- Minimizar operações DH
- Muito mais eficiente em largura de banda que ElGamal (bloco ElGamal de 514 bytes)
- Suportar criptografia nova e antiga no mesmo túnel se desejado
- Destinatário consegue distinguir eficientemente criptografia nova da antiga chegando pelo
  mesmo túnel
- Outros não podem distinguir criptografia nova da antiga ou futura
- Eliminar classificação de comprimento de Sessão nova vs. Existente (suportar padding)
- Nenhuma nova mensagem I2NP necessária
- Substituir checksum SHA-256 no payload AES por AEAD
- Suportar vinculação de sessões de transmissão e recepção para que
  confirmações possam acontecer dentro do protocolo, ao invés de somente fora de banda.
  Isso também permitirá que respostas tenham forward secrecy imediatamente.
- Habilitar criptografia ponta a ponta de certas mensagens (armazenamentos RouterInfo)
  que atualmente não fazemos devido ao overhead de CPU.
- Não alterar a I2NP Garlic Message
  ou formato de Garlic Message Delivery Instructions.
- Eliminar campos não utilizados ou redundantes nos formatos Garlic Clove Set e Clove.

Elimina vários problemas com session tags, incluindo:

- Incapacidade de usar AES até a primeira resposta
- Não confiabilidade e travamentos se a entrega de tag for assumida
- Ineficiente em largura de banda, especialmente na primeira entrega
- Enorme ineficiência de espaço para armazenar tags
- Enorme sobrecarga de largura de banda para entregar tags
- Altamente complexo, difícil de implementar
- Difícil de ajustar para vários casos de uso
  (streaming vs. datagramas, servidor vs. cliente, alta vs. baixa largura de banda)
- Vulnerabilidades de esgotamento de memória devido à entrega de tags

### Usos de Criptografia Assimétrica

- Mudanças no formato LS2 (proposta 123 está concluída)
- Novo algoritmo de rotação DHT ou geração aleatória compartilhada
- Nova criptografia para construção de túneis.
  Veja a proposta 152 [Proposal 152](/proposals/152-ecies-tunnels).
- Nova criptografia para criptografia de camada de túnel.
  Veja a proposta 153 [Proposal 153](/proposals/153-chacha20-layer-encryption).
- Métodos de criptografia, transmissão e recepção de mensagens I2NP DLM / DSM / DSRM.
  Não alterando.
- Nenhuma comunicação LS1-para-LS2 ou ElGamal/AES-para-esta-proposta é suportada.
  Esta proposta é um protocolo bidirecional.
  Destinos podem lidar com compatibilidade retroativa publicando dois leasesets
  usando os mesmos túneis, ou colocar ambos os tipos de criptografia no LS2.
- Mudanças no modelo de ameaça
- Detalhes de implementação não são discutidos aqui e são deixados para cada projeto.
- (Otimista) Adicionar extensões ou ganchos para suportar multicast

### Objetivos

ElGamal/AES+SessionTag tem sido nosso único protocolo end-to-end por cerca de 15 anos, essencialmente sem modificações no protocolo. Existem agora primitivas criptográficas que são mais rápidas. Precisamos aprimorar a segurança do protocolo. Também desenvolvemos estratégias heurísticas e soluções alternativas para minimizar o overhead de memória e largura de banda do protocolo, mas essas estratégias são frágeis, difíceis de ajustar e tornam o protocolo ainda mais propenso a falhas, causando a queda da sessão.

Por aproximadamente o mesmo período de tempo, a especificação ElGamal/AES+SessionTag e a documentação relacionada descreveram como é custoso em termos de largura de banda entregar session tags, e propuseram substituir a entrega de session tag por um "PRNG sincronizado". Um PRNG sincronizado gera deterministicamente as mesmas tags em ambas as extremidades, derivadas de uma semente comum. Um PRNG sincronizado também pode ser denominado um "ratchet". Esta proposta (finalmente) especifica esse mecanismo ratchet e elimina a entrega de tags.

Ao usar um ratchet (um PRNG sincronizado) para gerar as session tags, eliminamos a sobrecarga de enviar session tags na mensagem New Session e mensagens subsequentes quando necessário. Para um conjunto típico de 32 tags, isso representa 1KB. Isso também elimina o armazenamento de session tags no lado do remetente, reduzindo assim os requisitos de armazenamento pela metade.

Um handshake bidirecional completo, semelhante ao padrão Noise IK, é necessário para evitar ataques de Personificação por Comprometimento de Chave (KCI). Veja a tabela "Payload Security Properties" do Noise em [NOISE](https://noiseprotocol.org/noise.html). Para mais informações sobre KCI, consulte o artigo https://www.usenix.org/system/files/conference/woot15/woot15-paper-hlauschek.pdf

### Não-objetivos / Fora do escopo

O modelo de ameaça é um pouco diferente do que para NTCP2 (proposta 111). Os nós MitM são o OBEP e IBGW e presume-se que tenham visão completa do netDb global atual ou histórico, através de conluio com floodfills.

O objetivo é impedir que esses MitMs classifiquem o tráfego como mensagens de Nova Sessão e Sessão Existente, ou como nova criptografia versus criptografia antiga.

## Detailed Proposal

Esta proposta define um novo protocolo fim-a-fim para substituir ElGamal/AES+SessionTags. O design utilizará um handshake Noise e uma fase de dados incorporando o double ratchet do Signal.

### Justificativa

Existem cinco partes do protocolo a serem reprojetadas:

- 1) Os formatos de contêiner de Sessão nova e Existente
  são substituídos por novos formatos.
- 2) ElGamal (chaves públicas de 256 bytes, chaves privadas de 128 bytes) é substituído
  por ECIES-X25519 (chaves públicas e privadas de 32 bytes)
- 3) AES é substituído por
  AEAD_ChaCha20_Poly1305 (abreviado como ChaChaPoly abaixo)
- 4) SessionTags serão substituídas por ratchets,
  que é essencialmente um PRNG criptográfico e sincronizado.
- 5) O payload AES, conforme definido na especificação ElGamal/AES+SessionTags,
  é substituído por um formato de bloco similar ao do NTCP2.

Cada uma das cinco mudanças tem sua própria seção abaixo.

### Modelo de Ameaças

As implementações existentes de router I2P exigirão implementações para as seguintes primitivas criptográficas padrão, que não são necessárias para os protocolos I2P atuais:

- ECIES (mas isso é essencialmente X25519)
- Elligator2

As implementações existentes de roteadores I2P que ainda não implementaram [NTCP2](/docs/specs/ntcp2/) ([Proposta 111](/proposals/111-ntcp-2/)) também exigirão implementações para:

- Geração de chaves X25519 e DH
- AEAD_ChaCha20_Poly1305 (abreviado como ChaChaPoly abaixo)
- HKDF

### Crypto Type

O tipo de criptografia (usado no LS2) é 4. Isso indica uma chave pública X25519 de 32 bytes little-endian, e o protocolo ponta-a-ponta especificado aqui.

O tipo de criptografia 0 é ElGamal. Os tipos de criptografia 1-3 são reservados para ECIES-ECDH-AES-SessionTag, veja a proposta 145 [Proposal 145](/proposals/145-ecies).

### Resumo do Design Criptográfico

Esta proposta fornece os requisitos baseados no Noise Protocol Framework [NOISE](https://noiseprotocol.org/noise.html) (Revisão 34, 2018-07-11). O Noise tem propriedades similares ao protocolo Station-To-Station [STS](https://en.wikipedia.org/wiki/Station-to-Station_protocol), que é a base para o protocolo [SSU](/docs/legacy/ssu/). Na terminologia do Noise, Alice é a iniciadora e Bob é o respondedor.

Esta proposta é baseada no protocolo Noise Noise_IK_25519_ChaChaPoly_SHA256. (O identificador real para a função de derivação de chave inicial é "Noise_IKelg2_25519_ChaChaPoly_SHA256" para indicar extensões I2P - veja a seção KDF 1 abaixo) Este protocolo Noise usa as seguintes primitivas:

- Padrão de Handshake Interativo: IK
  Alice transmite imediatamente sua chave estática para Bob (I)
  Alice já conhece a chave estática de Bob (K)

- One-Way Handshake Pattern: N
  Alice não transmite sua chave estática para Bob (N)

- Função DH: X25519
  X25519 DH com comprimento de chave de 32 bytes conforme especificado na [RFC-7748](https://tools.ietf.org/html/rfc7748).

- Função de Cifra: ChaChaPoly
  AEAD_CHACHA20_POLY1305 conforme especificado na [RFC-7539](https://tools.ietf.org/html/rfc7539) seção 2.8.
  Nonce de 12 bytes, com os primeiros 4 bytes definidos como zero.
  Idêntica à do [NTCP2](/docs/specs/ntcp2/).

- Função de Hash: SHA256
  Hash padrão de 32 bytes, já usado extensivamente no I2P.

### Novas Primitivas Criptográficas para I2P

Esta proposta define as seguintes melhorias para Noise_IK_25519_ChaChaPoly_SHA256. Estas geralmente seguem as diretrizes na seção 13 do [NOISE](https://noiseprotocol.org/noise.html).

1) Chaves efêmeras em texto simples são codificadas com [Elligator2](https://elligator.cr.yp.to/).

2) A resposta é prefixada com uma tag de texto claro.

3) O formato da carga útil é definido para as mensagens 1, 2, e a fase de dados. Claro, isso não é definido no Noise.

Todas as mensagens incluem um cabeçalho de [I2NP](/docs/specs/i2np/) Garlic Message. A fase de dados usa criptografia similar, mas não compatível com a fase de dados do Noise.

### Tipo de Criptografia

Os handshakes utilizam padrões de handshake [Noise](https://noiseprotocol.org/noise.html).

O seguinte mapeamento de letras é usado:

- e = chave efêmera de uso único
- s = chave estática
- p = carga útil da mensagem

Sessões One-time e Unbound são similares ao padrão Noise N.

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
### Estrutura do Protocolo Noise

O protocolo ElGamal/AES+SessionTag atual é unidirecional. Nesta camada, o receptor não sabe de onde vem uma mensagem. As sessões de saída e entrada não estão associadas. As confirmações são fora de banda usando uma DeliveryStatusMessage (encapsulada em uma GarlicMessage) no cravo.

Há uma ineficiência substancial em um protocolo unidirecional. Qualquer resposta também deve usar uma mensagem custosa de 'Nova Sessão'. Isso causa maior uso de largura de banda, CPU e memória.

Também há fraquezas de segurança em um protocolo unidirecional. Todas as sessões são baseadas em DH ephemeral-static. Sem um caminho de retorno, não há maneira de Bob "ratchet" sua chave estática para uma chave ephemeral. Sem saber de onde uma mensagem vem, não há maneira de usar a chave ephemeral recebida para mensagens de saída, então a resposta inicial também usa DH ephemeral-static.

Para esta proposta, definimos dois mecanismos para criar um protocolo bidirecional - "pairing" e "binding". Estes mecanismos proporcionam maior eficiência e segurança.

### Adições ao Framework

Assim como com ElGamal/AES+SessionTags, todas as sessões de entrada e saída devem estar em um contexto específico, seja o contexto do router ou o contexto para um destino local particular. No Java I2P, este contexto é chamado de Session Key Manager.

As sessões não devem ser compartilhadas entre contextos, pois isso permitiria a correlação entre os vários destinos locais, ou entre um destino local e um router.

Quando um determinado destino suporta tanto ElGamal/AES+SessionTags quanto esta proposta, ambos os tipos de sessões podem compartilhar um contexto. Veja a seção 1c) abaixo.

### Padrões de Handshake

Quando uma sessão de saída é criada no originador (Alice), uma nova sessão de entrada é criada e emparelhada com a sessão de saída, a menos que nenhuma resposta seja esperada (por exemplo, datagramas brutos).

Uma nova sessão de entrada é sempre emparelhada com uma nova sessão de saída, a menos que nenhuma resposta seja solicitada (por exemplo, datagramas brutos).

Se uma resposta for solicitada e vinculada a um destino ou router de extremidade distante, essa nova sessão de saída é vinculada a esse destino ou router, e substitui qualquer sessão de saída anterior para esse destino ou router.

O emparelhamento de sessões de entrada e saída fornece um protocolo bidirecional com a capacidade de rotacionar as chaves DH.

### Sessões

Existe apenas uma sessão de saída para um determinado destino ou router. Pode haver várias sessões de entrada atuais de um determinado destino ou router. Geralmente, quando uma nova sessão de entrada é criada e o tráfego é recebido nessa sessão (o que serve como um ACK), quaisquer outras serão marcadas para expirar relativamente rapidamente, dentro de um minuto ou mais. O valor das mensagens anteriores enviadas (PN) é verificado e, se não houver mensagens não recebidas (dentro do tamanho da janela) na sessão de entrada anterior, a sessão anterior pode ser excluída imediatamente.

Quando uma sessão de saída é criada no originador (Alice), ela é vinculada ao Destination de destino (Bob), e qualquer sessão de entrada emparelhada também será vinculada ao Destination de destino. Conforme as sessões evoluem, elas continuam vinculadas ao Destination de destino.

Quando uma sessão de entrada é criada no receptor (Bob), ela pode ser vinculada ao Destination remoto (Alice), conforme opção da Alice. Se Alice incluir informações de vinculação (sua chave estática) na mensagem New Session, a sessão será vinculada a esse destination, e uma sessão de saída será criada e vinculada ao mesmo Destination. À medida que as sessões fazem ratchet, elas continuam vinculadas ao Destination remoto.

### Contexto da Sessão

Para o caso comum de streaming, esperamos que Alice e Bob usem o protocolo da seguinte forma:

- Alice emparelha sua nova sessão de saída com uma nova sessão de entrada, ambas vinculadas ao destino remoto (Bob).
- Alice inclui as informações de vinculação e assinatura, e uma solicitação de resposta, na
  mensagem New Session enviada para Bob.
- Bob emparelha sua nova sessão de entrada com uma nova sessão de saída, ambas vinculadas ao destino remoto (Alice).
- Bob envia uma resposta (ack) para Alice na sessão emparelhada, com um ratchet para uma nova chave DH.
- Alice executa ratchet para uma nova sessão de saída com a nova chave de Bob, emparelhada à sessão de entrada existente.

Ao vincular uma sessão de entrada a um Destination de extremidade distante, e emparelhar a sessão de entrada com uma sessão de saída vinculada ao mesmo Destination, obtemos dois grandes benefícios:

1) A resposta inicial de Bob para Alice usa DH efêmero-efêmero

2) Após a Alice receber a resposta do Bob e realizar os ratchets, todas as mensagens subsequentes da Alice para o Bob usam DH efêmero-efêmero.

### Emparelhando Sessões de Entrada e Saída

Em ElGamal/AES+SessionTags, quando um LeaseSet é empacotado como um garlic clove, ou tags são entregues, o router remetente solicita um ACK. Este é um garlic clove separado contendo uma Mensagem DeliveryStatus. Para segurança adicional, a Mensagem DeliveryStatus é encapsulada em uma Mensagem Garlic. Este mecanismo é fora da banda da perspectiva do protocolo.

No novo protocolo, uma vez que as sessões de entrada e saída estão emparelhadas, podemos ter ACKs em banda. Nenhum clove separado é necessário.

Um ACK explícito é simplesmente uma mensagem de Sessão Existente sem bloco I2NP. No entanto, na maioria dos casos, um ACK explícito pode ser evitado, pois há tráfego reverso. Pode ser desejável que as implementações aguardem um curto período (talvez cem ms) antes de enviar um ACK explícito, para dar tempo à camada de streaming ou aplicação para responder.

As implementações também precisarão adiar o envio de qualquer ACK até após o bloco I2NP ser processado, pois a Garlic Message pode conter uma Database Store Message com um leaseSet. Um leaseSet recente será necessário para rotear o ACK, e o destino da extremidade distante (contido no leaseSet) será necessário para verificar a chave estática de vinculação.

### Vinculação de Sessões e Destinos

As sessões de saída devem sempre expirar antes das sessões de entrada. Quando uma sessão de saída expira e uma nova é criada, uma nova sessão de entrada emparelhada também será criada. Se havia uma sessão de entrada antiga, ela será permitida a expirar.

### Benefícios do Binding e Pairing

A ser definido

### ACKs de Mensagem

Definimos as seguintes funções correspondentes aos blocos de construção criptográficos utilizados.

ZEROLEN

    zero-length byte array

CSRNG(n)

    n-byte output from a cryptographically-secure random number generator.

H(p, d)

    SHA-256 hash function that takes a personalization string p and data d, and
    produces an output of length 32 bytes.
    As defined in [NOISE](https://noiseprotocol.org/noise.html).
    || below means append.

    Use SHA-256 as follows::

        H(p, d) := SHA-256(p || d)

MixHash(d)

    SHA-256 hash function that takes a previous hash h and new data d,
    and produces an output of length 32 bytes.
    || below means append.

    Use SHA-256 as follows::

        MixHash(d) := h = SHA-256(h || d)

STREAM

    The ChaCha20/Poly1305 AEAD as specified in [RFC-7539](https://tools.ietf.org/html/rfc7539).
    S_KEY_LEN = 32 and S_IV_LEN = 12.

    ENCRYPT(k, n, plaintext, ad)
        Encrypts plaintext using the cipher key k, and nonce n which MUST be unique for
        the key k.
        Associated data ad is optional.
        Returns a ciphertext that is the size of the plaintext + 16 bytes for the HMAC.

        The entire ciphertext must be indistinguishable from random if the key is secret.

    DECRYPT(k, n, ciphertext, ad)
        Decrypts ciphertext using the cipher key k, and nonce n.
        Associated data ad is optional.
        Returns the plaintext.

DH

    X25519 public key agreement system. Private keys of 32 bytes, public keys of 32
    bytes, produces outputs of 32 bytes. It has the following
    functions:

    GENERATE_PRIVATE()
        Generates a new private key.

    DERIVE_PUBLIC(privkey)
        Returns the public key corresponding to the given private key.

    GENERATE_PRIVATE_ELG2()
        Generates a new private key that maps to a public key suitable for Elligator2 encoding.
        Note that half of the randomly-generated private keys will not be suitable and must be discarded.

    ENCODE_ELG2(pubkey)
        Returns the Elligator2-encoded public key corresponding to the given public key (inverse mapping).
        Encoded keys are little endian.
        Encoded key must be 256 bits indistinguishable from random data.
        See Elligator2 section below for specification.

    DECODE_ELG2(pubkey)
        Returns the public key corresponding to the given Elligator2-encoded public key.
        See Elligator2 section below for specification.

    DH(privkey, pubkey)
        Generates a shared secret from the given private and public keys.

HKDF(salt, ikm, info, n)

    A cryptographic key derivation function which takes some input key material ikm (which
    should have good entropy but is not required to be a uniformly random string), a salt
    of length 32 bytes, and a context-specific 'info' value, and produces an output
    of n bytes suitable for use as key material.

    Use HKDF as specified in [RFC-5869](https://tools.ietf.org/html/rfc5869), using the HMAC hash function SHA-256
    as specified in [RFC-2104](https://tools.ietf.org/html/rfc2104). This means that SALT_LEN is 32 bytes max.

MixKey(d)

    Use HKDF() with a previous chainKey and new data d, and
    sets the new chainKey and k.
    As defined in [NOISE](https://noiseprotocol.org/noise.html).

    Use HKDF as follows::

        MixKey(d) := output = HKDF(chainKey, d, "", 64)
                     chainKey = output[0:31]
                     k = output[32:63]


### Timeouts de Sessão

### Multicast

A Mensagem Garlic conforme especificada em [I2NP](/docs/specs/i2np/) é a seguinte. Como um objetivo de design é que os saltos intermediários não possam distinguir criptografia nova da antiga, este formato não pode mudar, mesmo que o campo de comprimento seja redundante. O formato é mostrado com o cabeçalho completo de 16 bytes, embora o cabeçalho real possa estar em um formato diferente, dependendo do transporte usado.

Quando descriptografado, os dados contêm uma série de Garlic Cloves e dados adicionais, também conhecidos como um Clove Set.

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
### Definições

O formato de mensagem atual, usado por mais de 15 anos, é ElGamal/AES+SessionTags. No ElGamal/AES+SessionTags, há dois formatos de mensagem:

1) Nova sessão: - Bloco ElGamal de 514 bytes - Bloco AES (128 bytes mínimo, múltiplo de 16)

2) Sessão existente: - 32 byte Session Tag - Bloco AES (128 bytes mínimo, múltiplo de 16)

O preenchimento mínimo para 128 é como implementado no Java I2P, mas não é aplicado na recepção.

Essas mensagens são encapsuladas em uma mensagem I2NP garlic, que contém um campo de comprimento, portanto o comprimento é conhecido.

Observe que não há padding definido para um comprimento não-mod-16, então a New Session é sempre (mod 16 == 2), e uma Existing Session é sempre (mod 16 == 0). Precisamos corrigir isso.

O receptor primeiro tenta procurar os primeiros 32 bytes como uma Session Tag. Se encontrada, ele descriptografa o bloco AES. Se não encontrada, e os dados tiverem pelo menos (514+16) de comprimento, ele tenta descriptografar o bloco ElGamal, e se bem-sucedido, descriptografa o bloco AES.

### 1) Formato da mensagem

No Signal Double Ratchet, o cabeçalho contém:

- DH: Chave pública ratchet atual
- PN: Comprimento da mensagem da cadeia anterior
- N: Número da Mensagem

As "sending chains" do Signal são aproximadamente equivalentes aos nossos conjuntos de tags. Ao usar uma tag de sessão, podemos eliminar a maior parte disso.

Em New Session, colocamos apenas a chave pública no cabeçalho não criptografado.

Na Sessão Existente, usamos uma tag de sessão para o cabeçalho. A tag de sessão está associada à chave pública do ratchet atual e ao número da mensagem.

Tanto em Sessão nova quanto em Sessão Existente, PN e N estão no corpo criptografado.

No Signal, as coisas estão constantemente fazendo ratcheting. Uma nova chave pública DH requer que o receptor faça ratchet e envie uma nova chave pública de volta, o que também serve como o ack para a chave pública recebida. Isso seria muitas operações DH demais para nós. Então separamos o ack da chave recebida e a transmissão de uma nova chave pública. Qualquer mensagem usando uma session tag gerada a partir da nova chave pública DH constitui um ACK. Só transmitimos uma nova chave pública quando desejamos fazer rekey.

O número máximo de mensagens antes que o DH deve fazer ratchet é 65535.

Ao entregar uma chave de sessão, derivamos o "Tag Set" dela, em vez de ter que entregar session tags também. Um Tag Set pode ter até 65536 tags. No entanto, os receptores devem implementar uma estratégia de "look-ahead", em vez de gerar todas as tags possíveis de uma vez. Gere apenas no máximo N tags além da última tag válida recebida. N pode ser no máximo 128, mas 32 ou até menos pode ser uma escolha melhor.

### Revisão do Formato de Mensagem Atual

Chave Pública de Sessão Nova de Uso Único (32 bytes) Dados criptografados e MAC (bytes restantes)

A mensagem New Session pode ou não conter a chave pública estática do remetente. Se estiver incluída, a sessão reversa fica vinculada a essa chave. A chave estática deve ser incluída se respostas forem esperadas, ou seja, para streaming e datagramas que podem ser respondidos. Não deve ser incluída para datagramas brutos.

A mensagem New Session é semelhante ao padrão [NOISE](https://noiseprotocol.org/noise.html) unidirecional "N" (se a chave estática não for enviada), ou ao padrão bidirecional "IK" (se a chave estática for enviada).

### Revisão do Formato de Dados Criptografados

O comprimento é 96 + comprimento do payload. Formato criptografado:

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
### Novas Session Tags e Comparação com o Signal

A chave efêmera tem 32 bytes, codificada com Elligator2. Esta chave nunca é reutilizada; uma nova chave é gerada com cada mensagem, incluindo retransmissões.

### 1a) Novo formato de sessão

Quando decriptada, a chave estática X25519 de Alice, 32 bytes.

### 1b) Novo formato de sessão (com vinculação)

O comprimento criptografado é o restante dos dados. O comprimento descriptografado é 16 a menos que o comprimento criptografado. O payload deve conter um bloco DateTime e geralmente conterá um ou mais blocos Garlic Clove. Consulte a seção payload abaixo para formato e requisitos adicionais.

### Chave Efêmera de Nova Sessão

Se nenhuma resposta for necessária, nenhuma chave estática é enviada.

O comprimento é 96 + comprimento do payload. Formato criptografado:

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
### Chave Estática

Chave efêmera da Alice. A chave efêmera tem 32 bytes, codificada com Elligator2, little endian. Esta chave nunca é reutilizada; uma nova chave é gerada a cada mensagem, incluindo retransmissões.

### Payload

A seção Flags não contém nada. Ela sempre tem 32 bytes, porque deve ter o mesmo comprimento que a chave estática para mensagens New Session com binding. Bob determina se são 32 bytes de uma chave estática ou de uma seção flags testando se os 32 bytes são todos zeros.

TODO alguma flag necessária aqui?

### 1c) Novo formato de sessão (sem vinculação)

O comprimento criptografado é o restante dos dados. O comprimento descriptografado é 16 a menos que o comprimento criptografado. A carga útil deve conter um bloco DateTime e geralmente conterá um ou mais blocos Garlic Clove. Veja a seção de carga útil abaixo para formato e requisitos adicionais.

### Chave Efêmera de Nova Sessão

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
### Seção de Flags Dados descriptografados

A chave de uso único tem 32 bytes, codificada com Elligator2, little endian. Esta chave nunca é reutilizada; uma nova chave é gerada a cada mensagem, incluindo retransmissões.

### Payload

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
### 1d) Formato único (sem vinculação ou sessão)

O comprimento encriptado é o restante dos dados. O comprimento descriptografado é 16 a menos que o comprimento encriptado. A carga útil deve conter um bloco DateTime e geralmente conterá um ou mais blocos Garlic Clove. Consulte a seção de carga útil abaixo para formato e requisitos adicionais.

### Nova Chave de Sessão de Uso Único

### Seção de Flags Dados descriptografados

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
### Payload

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
### 1f) KDFs para Mensagem de Nova Sessão

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
### KDF para ChainKey Inicial

Note que este é um padrão Noise "N", mas usamos o mesmo inicializador "IK" que para sessões vinculadas.

As mensagens New Session não podem ser identificadas como contendo a chave estática da Alice ou não até que a chave estática seja descriptografada e inspecionada para determinar se contém todos os zeros. Portanto, o receptor deve usar a máquina de estados "IK" para todas as mensagens New Session. Se a chave estática for todos os zeros, o padrão de mensagem "ss" deve ser pulado.

```

chainKey = from Flags/Static key section
  k = from Flags/Static key section
  n = 1
  ad = h from Flags/Static key section
  ciphertext = ENCRYPT(k, n, payload, ad)

```
### KDF para Conteúdos Encriptados da Seção Flags/Static Key

Uma ou mais New Session Replies podem ser enviadas em resposta a uma única mensagem New Session. Cada resposta é precedida por uma tag, que é gerada a partir de um TagSet para a sessão.

A New Session Reply está em duas partes. A primeira parte é a conclusão do handshake Noise IK com uma tag anexada. O comprimento da primeira parte é de 56 bytes. A segunda parte é o payload da fase de dados. O comprimento da segunda parte é 16 + comprimento do payload.

O comprimento total é 72 + comprimento do payload. Formato criptografado:

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
### KDF para Seção de Payload (com chave estática da Alice)

A tag é gerada no Session Tags KDF, conforme inicializado no DH Initialization KDF abaixo. Isso correlaciona a resposta à sessão. A Session Key do DH Initialization não é utilizada.

### KDF para Seção de Payload (sem chave estática da Alice)

Chave efêmera do Bob. A chave efêmera tem 32 bytes, codificada com Elligator2, little endian. Esta chave nunca é reutilizada; uma nova chave é gerada a cada mensagem, incluindo retransmissões.

### 1g) Formato da Resposta de Nova Sessão

O comprimento criptografado é o restante dos dados. O comprimento descriptografado é 16 menos que o comprimento criptografado. O payload geralmente conterá um ou mais blocos Garlic Clove. Consulte a seção de payload abaixo para formato e requisitos adicionais.

### Session Tag

Uma ou mais tags são criadas a partir do TagSet, que é inicializado usando o KDF abaixo, usando a chainKey da mensagem New Session.

```

// Generate tagset
  tagsetKey = HKDF(chainKey, ZEROLEN, "SessionReplyTags", 32)
  tagset_nsr = DH_INITIALIZE(chainKey, tagsetKey)

```
### Resposta de Nova Sessão com Chave Efêmera

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
### Payload

Isso é como a primeira mensagem de Sessão Existente, pós-divisão, mas sem uma tag separada. Além disso, usamos o hash de cima para vincular o payload à mensagem NSR.

```

// split()
  keydata = HKDF(chainKey, ZEROLEN, "", 64)
  k_ab = keydata[0:31]
  k_ba = keydata[32:63]
  tagset_ab = DH_INITIALIZE(chainKey, k_ab)
  tagset_ba = DH_INITIALIZE(chainKey, k_ba)

  // AEAD parameters for New Session Reply payload
  k = HKDF(k_ba, ZEROLEN, "AttachPayloadKDF", 32)
  n = 0
  ad = h
  ciphertext = ENCRYPT(k, n, payload, ad)
```
### KDF para Reply TagSet

Múltiplas mensagens NSR podem ser enviadas em resposta, cada uma com chaves efêmeras únicas, dependendo do tamanho da resposta.

Alice e Bob são obrigados a usar novas chaves efêmeras para cada mensagem NS e NSR.

Alice deve receber uma das mensagens NSR de Bob antes de enviar mensagens de Sessão Existente (ES), e Bob deve receber uma mensagem ES de Alice antes de enviar mensagens ES.

O ``chainKey`` e ``k`` da Seção de Payload NSR do Bob são usados como entradas para os Ratchets ES DH iniciais (ambas as direções, veja DH Ratchet KDF).

Bob deve manter apenas as Sessões Existentes para as mensagens ES recebidas de Alice. Qualquer outra sessão de entrada e saída criada (para múltiplos NSRs) deve ser destruída imediatamente após receber a primeira mensagem ES de Alice para uma determinada sessão.

### KDF para Conteúdos Criptografados da Seção Reply Key

Tag da sessão (8 bytes) Dados criptografados e MAC (veja a seção 3 abaixo)

### KDF para Conteúdos Criptografados da Seção de Payload

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
### Notas

O comprimento criptografado é o restante dos dados. O comprimento descriptografado é 16 a menos que o comprimento criptografado. Veja a seção de payload abaixo para formato e requisitos.

KDF

```
See AEAD section below.

  // AEAD parameters for Existing Session payload
  k = The 32-byte session key associated with this session tag
  n = The message number N in the current chain, as retrieved from the associated Session Tag.
  ad = The session tag, 8 bytes
  ciphertext = ENCRYPT(k, n, payload, ad)
```
### 1h) Formato de sessão existente

Formato: Chaves públicas e privadas de 32 bytes, little-endian.

Justificativa: Usado em [NTCP2](/docs/specs/ntcp2/).

### Formato

Nos handshakes Noise padrão, as mensagens iniciais de handshake em cada direção começam com chaves efêmeras que são transmitidas em texto simples. Como chaves X25519 válidas são distinguíveis de dados aleatórios, um atacante man-in-the-middle pode distinguir essas mensagens das mensagens de Sessão Existente que começam com tags de sessão aleatórias. No [NTCP2](/docs/specs/ntcp2/) ([Proposta 111](/proposals/111-ntcp-2/)), usamos uma função XOR de baixo overhead usando a chave estática fora de banda para ofuscar a chave. No entanto, o modelo de ameaça aqui é diferente; não queremos permitir que qualquer MitM use qualquer meio para confirmar o destino do tráfego, ou para distinguir as mensagens iniciais de handshake das mensagens de Sessão Existente.

Portanto, [Elligator2](https://elligator.cr.yp.to/) é usado para transformar as chaves efêmeras nas mensagens New Session e New Session Reply de modo que sejam indistinguíveis de strings uniformemente aleatórias.

### Payload

Chaves públicas e privadas de 32 bytes. As chaves codificadas são little endian.

Como definido em [Elligator2](https://elligator.cr.yp.to/), as chaves codificadas são indistinguíveis de 254 bits aleatórios. Precisamos de 256 bits aleatórios (32 bytes). Portanto, a codificação e decodificação são definidas da seguinte forma:

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
### 2) ECIES-X25519

Necessário para impedir que o OBEP e o IBGW classifiquem o tráfego.

### 2a) Elligator2

Elligator2 dobra o tempo médio de geração de chaves, pois metade das chaves privadas resulta em chaves públicas inadequadas para codificação com Elligator2. Além disso, o tempo de geração de chaves é ilimitado com uma distribuição exponencial, pois o gerador deve continuar tentando até encontrar um par de chaves adequado.

Este overhead pode ser gerenciado fazendo a geração de chaves antecipadamente, em uma thread separada, para manter um pool de chaves adequadas.

O gerador executa a função ENCODE_ELG2() para determinar a adequação. Portanto, o gerador deve armazenar o resultado de ENCODE_ELG2() para que não precise ser calculado novamente.

Adicionalmente, as chaves inadequadas podem ser adicionadas ao conjunto de chaves usadas para [NTCP2](/docs/specs/ntcp2/), onde Elligator2 não é usado. As questões de segurança de fazê-lo ainda estão por ser determinadas.

### Formato

AEAD usando ChaCha20 e Poly1305, igual ao usado em [NTCP2](/docs/specs/ntcp2/). Isto corresponde à [RFC-7539](https://tools.ietf.org/html/rfc7539), que também é usado de forma similar no TLS [RFC-7905](https://tools.ietf.org/html/rfc7905).

### Justificativa

Entradas para as funções de criptografia/descriptografia para um bloco AEAD numa mensagem New Session:

```

k :: 32 byte cipher key
       See New Session and New Session Reply KDFs above.

  n :: Counter-based nonce, 12 bytes.
       n = 0

  ad :: Associated data, 32 bytes.
        The SHA256 hash of the preceding data, as output from mixHash()

  data :: Plaintext data, 0 or more bytes

```
### Notas

Entradas para as funções de criptografia/descriptografia para um bloco AEAD em uma mensagem de Sessão Existente:

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
### 3) AEAD (ChaChaPoly)

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
### Entradas de Nova Sessão e Resposta de Nova Sessão

- Como ChaCha20 é uma cifra de fluxo, os textos simples não precisam ser preenchidos.
  Bytes adicionais de keystream são descartados.

- A chave para a cifra (256 bits) é acordada por meio do SHA256 KDF.
  Os detalhes do KDF para cada mensagem estão em seções separadas abaixo.

- Os frames ChaChaPoly têm tamanho conhecido pois são encapsulados na mensagem de dados I2NP.

- Para todas as mensagens,
  o padding está dentro do quadro de
  dados autenticados.

### Entradas de Sessão Existentes

Todos os dados recebidos que falharem na verificação AEAD devem ser descartados. Nenhuma resposta é retornada.

### Formato Criptografado

Usado em [NTCP2](/docs/specs/ntcp2/).

### Notas

Ainda usamos session tags, como antes, mas usamos ratchets para gerá-las. Session tags também tinham uma opção de rekey que nunca implementamos. Então é como um double ratchet, mas nunca fizemos o segundo.

Aqui definimos algo similar ao Double Ratchet do Signal. As session tags são geradas de forma determinística e idêntica nos lados do receptor e do remetente.

Ao usar um ratchet de chave/tag simétrica, eliminamos o uso de memória para armazenar session tags no lado do remetente. Também eliminamos o consumo de largura de banda do envio de conjuntos de tags. O uso no lado do receptor ainda é significativo, mas podemos reduzi-lo ainda mais, pois iremos diminuir a session tag de 32 bytes para 8 bytes.

Não usamos criptografia de cabeçalho conforme especificado (e opcional) no Signal, usamos session tags em vez disso.

Ao usar um DH ratchet, alcançamos forward secrecy, que nunca foi implementado no ElGamal/AES+SessionTags.

Nota: A chave pública única da Nova Sessão não faz parte do ratchet, sua única função é criptografar a chave inicial do ratchet DH de Alice.

### Tratamento de Erros AEAD

O Double Ratchet lida com mensagens perdidas ou fora de ordem incluindo uma tag no cabeçalho de cada mensagem. O receptor procura o índice da tag, este é o número da mensagem N. Se a mensagem contém um bloco Message Number com um valor PN, o destinatário pode deletar quaisquer tags maiores que esse valor no conjunto de tags anterior, enquanto retém tags ignoradas do conjunto de tags anterior no caso das mensagens ignoradas chegarem mais tarde.

### Justificativa

Definimos as seguintes estruturas de dados e funções para implementar estes ratchets.

TAGSET_ENTRY

    A single entry in a TAGSET.

    INDEX
        An integer index, starting with 0

    SESSION_TAG
        An identifier to go out on the wire, 8 bytes

    SESSION_KEY
        A symmetric key, never goes on the wire, 32 bytes

TAGSET

    A collection of TAGSET_ENTRIES.

    CREATE(key, n)
        Generate a new TAGSET using initial cryptographic key material of 32 bytes.
        The associated session identifier is provided.
        The initial number of of tags to create is specified; this is generally 0 or 1
        for an outgoing session.
        LAST_INDEX = -1
        EXTEND(n) is called.

    EXTEND(n)
        Generate n more TAGSET_ENTRIES by calling EXTEND() n times.

    EXTEND()
        Generate one more TAGSET_ENTRY, unless the maximum number SESSION_TAGS have
        already been generated.
        If LAST_INDEX is greater than or equal to 65535, return.
        ++ LAST_INDEX
        Create a new TAGSET_ENTRY with the LAST_INDEX value and the calculated SESSION_TAG.
        Calls RATCHET_TAG() and (optionally) RATCHET_KEY().
        For inbound sessions, the calculation of the SESSION_KEY may
        be deferred and calculated in GET_SESSION_KEY().
        Calls EXPIRE()

    EXPIRE()
        Remove tags and keys that are too old, or if the TAGSET size exceeds some limit.

    RATCHET_TAG()
        Calculates the next SESSION_TAG based on the last SESSION_TAG.

    RATCHET_KEY()
        Calculates the next SESSION_KEY based on the last SESSION_KEY.

    SESSION
        The associated session.

    CREATION_TIME
        When the TAGSET was created.

    LAST_INDEX
        The last TAGSET_ENTRY INDEX generated by EXTEND().

    GET_NEXT_ENTRY()
        Used for outgoing sessions only.
        EXTEND(1) is called if there are no remaining TAGSET_ENTRIES.
        If EXTEND(1) did nothing, the max of 65535 TAGSETS have been used,
        and return an error.
        Returns the next unused TAGSET_ENTRY.

    GET_SESSION_KEY(sessionTag)
        Used for incoming sessions only.
        Returns the TAGSET_ENTRY containing the sessionTag.
        If found, the TAGSET_ENTRY is removed.
        If the SESSION_KEY calculation was deferred, it is calculated now.
        If there are few TAGSET_ENTRIES remaining, EXTEND(n) is called.


### 4) Ratchets

Ratchets mas não tão rápido quanto o Signal faz. Separamos o reconhecimento da chave recebida da geração da nova chave. No uso típico, Alice e Bob farão cada um ratchet (duas vezes) imediatamente em uma Nova Sessão, mas não farão ratchet novamente.

Note que um ratchet é para uma única direção, e gera uma cadeia de ratchet de tag de Nova Sessão / chave de mensagem para essa direção. Para gerar chaves para ambas as direções, você tem que fazer ratchet duas vezes.

Você faz ratchet toda vez que gera e envia uma nova chave. Você faz ratchet toda vez que recebe uma nova chave.

Alice executa um ratchet uma vez ao criar uma sessão outbound não vinculada, ela não cria uma sessão inbound (não vinculada significa não respondível).

Bob faz um ratchet uma vez ao criar uma sessão inbound não vinculada, e não cria uma sessão outbound correspondente (não vinculada é não respondível).

Alice continua enviando mensagens New Session (NS) para Bob até receber uma das mensagens New Session Reply (NSR) de Bob. Ela então usa os resultados do KDF da Seção de Payload do NSR como entradas para os ratchets da sessão (veja DH Ratchet KDF), e começa a enviar mensagens Existing Session (ES).

Para cada mensagem NS recebida, Bob cria uma nova sessão de entrada, usando os resultados do KDF da Seção de Payload de resposta como entradas para o novo Ratchet DH ES de entrada e saída.

Para cada resposta necessária, Bob envia a Alice uma mensagem NSR com a resposta no payload. É obrigatório que Bob use novas chaves efêmeras para cada NSR.

Bob deve receber uma mensagem ES de Alice numa das sessões de entrada, antes de criar e enviar mensagens ES na sessão de saída correspondente.

Alice deve usar um temporizador para receber uma mensagem NSR de Bob. Se o temporizador expirar, a sessão deve ser removida.

Para evitar um ataque KCI e/ou de exaustão de recursos, onde um atacante descarta as respostas NSR de Bob para manter Alice enviando mensagens NS, Alice deve evitar iniciar New Sessions para Bob após um certo número de tentativas devido à expiração do temporizador.

Alice e Bob fazem cada um um ratchet DH para cada bloco NextKey recebido.

Alice e Bob geram cada um novos ratchets de conjuntos de tags e dois ratchets de chaves simétricas após cada ratchet DH. Para cada nova mensagem ES em uma determinada direção, Alice e Bob avançam os ratchets de tag de sessão e chave simétrica.

A frequência dos ratchets DH após o handshake inicial depende da implementação. Embora o protocolo estabeleça um limite de 65535 mensagens antes que um ratchet seja obrigatório, ratcheting mais frequente (baseado na contagem de mensagens, tempo decorrido, ou ambos) pode fornecer segurança adicional.

Após o KDF final do handshake em sessões vinculadas, Bob e Alice devem executar a função Noise Split() no CipherState resultante para criar chaves simétricas e de cadeia de tags independentes para sessões de entrada e saída.

#### KEY AND TAG SET IDS

Os números de ID das chaves e conjuntos de tags são usados para identificar chaves e conjuntos de tags. Os IDs de chave são usados em blocos NextKey para identificar a chave enviada ou utilizada. Os IDs de conjunto de tags são usados (com o número da mensagem) em blocos ACK para identificar a mensagem que está sendo confirmada. Tanto os IDs de chave quanto os de conjunto de tags se aplicam aos conjuntos de tags para uma única direção. Os números de ID das chaves e conjuntos de tags devem ser sequenciais.

Nos primeiros conjuntos de tags utilizados para uma sessão em cada direção, o ID do conjunto de tags é 0. Nenhum bloco NextKey foi enviado, portanto não há IDs de chave.

Para iniciar um DH ratchet, o remetente transmite um novo bloco NextKey com um ID de chave de 0. O receptor responde com um novo bloco NextKey com um ID de chave de 0. O remetente então começa a usar um novo conjunto de tags com um ID de conjunto de tags de 1.

Os conjuntos de tags subsequentes são gerados de forma similar. Para todos os conjuntos de tags usados após as trocas NextKey, o número do conjunto de tags é (1 + ID da chave de Alice + ID da chave de Bob).

Os IDs de chave e conjunto de tags começam em 0 e incrementam sequencialmente. O ID máximo do conjunto de tags é 65535. O ID máximo da chave é 32767. Quando um conjunto de tags está quase esgotado, o remetente do conjunto de tags deve iniciar uma troca NextKey. Quando o conjunto de tags 65535 está quase esgotado, o remetente do conjunto de tags deve iniciar uma nova sessão enviando uma mensagem New Session.

Com um tamanho máximo de mensagem de streaming de 1730, e assumindo nenhuma retransmissão, a transferência máxima teórica de dados usando um único conjunto de tags é 1730 * 65536 ~= 108 MB. O máximo real será menor devido às retransmissões.

A transferência máxima teórica de dados com todos os 65536 conjuntos de tags disponíveis, antes que a sessão tenha que ser descartada e substituída, é 64K * 108 MB ~= 6,9 TB.

#### DH RATCHET MESSAGE FLOW

A próxima troca de chaves para um conjunto de tags deve ser iniciada pelo remetente dessas tags (o proprietário do conjunto de tags de saída). O receptor (proprietário do conjunto de tags de entrada) responderá. Para um tráfego HTTP GET típico na camada de aplicação, Bob enviará mais mensagens e fará o ratchet primeiro ao iniciar a troca de chaves; o diagrama abaixo mostra isso. Quando Alice faz o ratchet, a mesma coisa acontece em sentido inverso.

O primeiro conjunto de tags usado após o handshake NS/NSR é o conjunto de tags 0. Quando o conjunto de tags 0 está quase esgotado, novas chaves devem ser trocadas em ambas as direções para criar o conjunto de tags 1. Depois disso, uma nova chave é enviada apenas em uma direção.

Para criar o conjunto de tags 2, o remetente das tags envia uma nova chave e o receptor das tags envia o ID de sua chave antiga como confirmação. Ambos os lados fazem um DH.

Para criar o conjunto de tags 3, o remetente da tag envia o ID de sua chave antiga e solicita uma nova chave do destinatário da tag. Ambos os lados fazem um DH.

Os conjuntos de tags subsequentes são gerados como para os conjuntos de tags 2 e 3. O número do conjunto de tags é (1 + ID da chave do remetente + ID da chave do destinatário).

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
Após a conclusão do DH ratchet para um tagset de saída, e um novo tagset de saída ser criado, ele deve ser usado imediatamente, e o antigo tagset de saída pode ser excluído.

Depois que o DH ratchet estiver completo para um tagset de entrada, e um novo tagset de entrada for criado, o receptor deve escutar tags em ambos os tagsets, e deletar o tagset antigo após um tempo curto, cerca de 3 minutos.

Resumo da progressão do conjunto de tags e ID da chave está na tabela abaixo. * indica que uma nova chave é gerada.

| New Tag Set ID | Sender key ID | Rcvr key ID |
|----------------|---------------|-------------|
| 0              | n/a           | n/a         |
| 1              | 0 *           | 0 *         |
| 2              | 1 *           | 0           |
| 3              | 1             | 1 *         |
| 4              | 2 *           | 1           |
| 5              | 2             | 2 *         |
| ...            | ...           | ...         |
| 65534          | 32767 *       | 32766       |
| 65535          | 32767         | 32767 *     |
Os números de ID do conjunto de chaves e tags devem ser sequenciais.

#### DH INITIALIZATION KDF

Esta é a definição de DH_INITIALIZE(rootKey, k) para uma única direção. Ela cria um tagset e uma "próxima chave raiz" para ser usada em um ratchet DH subsequente, se necessário.

Usamos a inicialização DH em três lugares. Primeiro, a usamos para gerar um conjunto de tags para as New Session Replies. Segundo, a usamos para gerar dois conjuntos de tags, um para cada direção, para uso em mensagens Existing Session. Por último, a usamos após um DH Ratchet para gerar um novo conjunto de tags em uma única direção para mensagens Existing Session adicionais.

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
#### DH RATCHET KDF

Isto é usado após novas chaves DH serem trocadas em blocos NextKey, antes de um tagset ser esgotado.

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
### Números de Mensagem

Ratchets para cada mensagem, como no Signal. O ratchet de tag de sessão é sincronizado com o ratchet de chave simétrica, mas o ratchet de chave do receptor pode "ficar para trás" para economizar memória.

O transmissor executa ratchet uma vez para cada mensagem transmitida. Nenhuma tag adicional deve ser armazenada. O transmissor também deve manter um contador para 'N', o número da mensagem da mensagem na cadeia atual. O valor 'N' é incluído na mensagem enviada. Veja a definição do bloco Message Number.

O receptor deve avançar por ratchet pelo tamanho máximo da janela e armazenar as tags em um "conjunto de tags", que está associado à sessão. Uma vez recebida, a tag armazenada pode ser descartada, e se não houver tags anteriores não recebidas, a janela pode ser avançada. O receptor deve manter o valor 'N' associado a cada tag de sessão, e verificar se o número na mensagem enviada corresponde a este valor. Consulte a definição do bloco Message Number.

#### KDF

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
### Implementação de Exemplo

Ratchets para cada mensagem, como no Signal. Cada chave simétrica tem um número de mensagem associado e uma tag de sessão. O ratchet da chave de sessão é sincronizado com o ratchet da tag simétrica, mas o ratchet da chave do receptor pode "ficar para trás" para economizar memória.

Transmitter ratchets uma vez para cada mensagem transmitida. Nenhuma chave adicional precisa ser armazenada.

Quando o receptor recebe uma session tag, se ainda não tiver avançado o ratchet de chave simétrica até a chave associada, ele deve "alcançar" a chave associada. O receptor provavelmente armazenará em cache as chaves para quaisquer tags anteriores que ainda não foram recebidas. Uma vez recebidas, a chave armazenada pode ser descartada, e se não houver tags anteriores não recebidas, a janela pode ser avançada.

Para eficiência, os ratchets da session tag e da chave simétrica são separados, permitindo que o ratchet da session tag execute à frente do ratchet da chave simétrica. Isso também fornece segurança adicional, já que as session tags são transmitidas pela rede.

#### KDF

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
### 4a) DH Ratchet

Isso substitui o formato da seção AES definido na especificação ElGamal/AES+SessionTags.

Isto usa o mesmo formato de bloco conforme definido na especificação [NTCP2](/docs/specs/ntcp2/). Os tipos de blocos individuais são definidos de forma diferente.

Há preocupações de que encorajar implementadores a compartilhar código pode levar a problemas de parsing. Os implementadores devem considerar cuidadosamente os benefícios e riscos de compartilhar código, e garantir que as regras de ordenação e blocos válidos sejam diferentes para os dois contextos.

### Payload Section Decrypted data

O comprimento criptografado é o restante dos dados. O comprimento descriptografado é 16 a menos que o comprimento criptografado. Todos os tipos de bloco são suportados. O conteúdo típico inclui os seguintes blocos:

| Payload Block Type | Type Number | Block Length |
|--------------------|-------------|--------------|
| DateTime           | 0           | 7            |
| Termination (TBD)  | 4           | 9 typ.       |
| Options (TBD)      | 5           | 21+          |
| Message Number (TBD) | 6           | TBD          |
| Next Key           | 7           | 3 or 35      |
| ACK                | 8           | 4 typ.       |
| ACK Request        | 9           | 3            |
| Garlic Clove       | 11          | varies       |
| Padding            | 254         | varies       |
### Unencrypted data

Há zero ou mais blocos no frame criptografado. Cada bloco contém um identificador de um byte, um comprimento de dois bytes e zero ou mais bytes de dados.

Para extensibilidade, os receptores DEVEM ignorar blocos com números de tipo desconhecidos e tratá-los como preenchimento.

Os dados criptografados têm um máximo de 65535 bytes, incluindo um cabeçalho de autenticação de 16 bytes, portanto o máximo de dados não criptografados é de 65519 bytes.

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
### Block Ordering Rules

Na mensagem New Session, o bloco DateTime é obrigatório e deve ser o primeiro bloco.

Outros blocos permitidos:

- Garlic Clove (tipo 11)
- Opções (tipo 5)
- Preenchimento (tipo 254)

Na mensagem de Resposta de Nova Sessão, nenhum bloco é obrigatório.

Outros blocos permitidos:

- Garlic Clove (tipo 11)
- Opções (tipo 5)
- Preenchimento (tipo 254)

Nenhum outro bloco é permitido. O padding, se presente, deve ser o último bloco.

Na mensagem Existing Session, nenhum bloco é obrigatório, e a ordem não é especificada, exceto pelos seguintes requisitos:

A terminação, se presente, deve ser o último bloco exceto pelo Padding. O Padding, se presente, deve ser o último bloco.

Pode haver múltiplos blocos Garlic Clove em um único frame. Pode haver até dois blocos Next Key em um único frame. Múltiplos blocos Padding não são permitidos em um único frame. Outros tipos de bloco provavelmente não terão múltiplos blocos em um único frame, mas isso não é proibido.

### DateTime

Uma expiração. Auxilia na prevenção de respostas. Bob deve validar que a mensagem é recente, usando este timestamp. Bob deve implementar um filtro Bloom ou outro mecanismo para prevenir ataques de replay, se o tempo for válido. Geralmente incluído apenas em mensagens New Session.

```

+----+----+----+----+----+----+----+
  | 0  |    4    |     timestamp     |
  +----+----+----+----+----+----+----+

  blk :: 0
  size :: 2 bytes, big endian, value = 4
  timestamp :: Unix timestamp, unsigned seconds.
               Wraps around in 2106

```
### 4b) Session Tag Ratchet

Um único Garlic Clove descriptografado conforme especificado em [I2NP](/docs/specs/i2np/), com modificações para remover campos que não são utilizados ou são redundantes. Aviso: Este formato é significativamente diferente daquele para ElGamal/AES. Cada clove é um bloco de payload separado. Garlic Cloves não podem ser fragmentados entre blocos ou entre frames ChaChaPoly.

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
         the Garlic Clove section of [I2NP](/docs/specs/i2np/).
         Length varies but is typically 1, 33, or 37 bytes

  type :: I2NP message type

  Message_ID :: 4 byte `Integer` I2NP message ID

  Expiration :: 4 bytes, seconds since the epoch

```
Notas:

- Os implementadores devem garantir que ao ler um bloco,
  dados malformados ou maliciosos não causem leituras que
  ultrapassem o próximo bloco.

- O formato Clove Set especificado em [I2NP](/docs/specs/i2np/) não é usado.
  Cada clove está contido em seu próprio bloco.

- O cabeçalho da mensagem I2NP tem 9 bytes, com um formato idêntico
  ao usado no [NTCP2](/docs/specs/ntcp2/).

- O Certificate, Message ID e Expiration da
  definição de Garlic Message em [I2NP](/docs/specs/i2np/) não estão incluídos.

- O Certificate, Clove ID e Expiration da
  definição Garlic Clove em [I2NP](/docs/specs/i2np/) não estão incluídos.

Justificativa:

- Os certificados nunca foram usados.
- O ID de mensagem separado e os IDs de clove nunca foram usados.
- As expirações separadas nunca foram usadas.
- A economia geral em comparação com os formatos antigos Clove Set e Clove
  é de aproximadamente 35 bytes para 1 clove, 54 bytes para 2 cloves,
  e 73 bytes para 3 cloves.
- O formato de bloco é extensível e quaisquer novos campos podem ser adicionados
  como novos tipos de bloco.

### Termination

A implementação é opcional. Encerre a sessão. Este deve ser o último bloco não-padding no quadro. Nenhuma mensagem adicional será enviada nesta sessão.

Não permitido em NS ou NSR. Incluído apenas em mensagens de Sessão Existente.

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
### 4c) Ratchet de Chave Simétrica

NÃO IMPLEMENTADO, para estudo adicional. Passar opções atualizadas. As opções incluem vários parâmetros para a sessão. Consulte a seção Análise do Comprimento da Tag de Sessão abaixo para mais informações.

O bloco de opções pode ter comprimento variável, pois more_options pode estar presente.

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
SOTW é a recomendação do remetente para o destinatário sobre a janela de tag de entrada do destinatário (o lookahead máximo). RITW é a declaração do remetente da janela de tag de entrada (lookahead máximo) que ele planeja usar. Cada lado então define ou ajusta o lookahead com base em algum mínimo ou máximo ou outro cálculo.

Notas:

- O suporte para comprimento de tag de sessão não padrão
  esperamos que nunca seja necessário.
- A janela de tag é MAX_SKIP na documentação do Signal.

Problemas:

- A negociação de opções está por definir (TBD).
- Padrões por definir (TBD).
- As opções de padding e atraso são copiadas do NTCP2,
  mas essas opções não foram totalmente implementadas ou estudadas lá.

### Message Numbers

A implementação é opcional. O comprimento (número de mensagens enviadas) no conjunto de tags anterior (PN). O receptor pode imediatamente deletar tags maiores que PN do conjunto de tags anterior. O receptor pode expirar tags menores ou iguais a PN do conjunto de tags anterior após um curto período de tempo (ex.: 2 minutos).

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
  Isso é similar ao que o Signal faz, mas no Signal, PN e N estão no cabeçalho.
  Aqui, eles estão no corpo da mensagem criptografada.
- Não envie este bloco no conjunto de tags 0, pois não havia conjunto de tags anterior.

### 5) Payload

A próxima chave DH ratchet está no payload, e é opcional. Não fazemos ratchet toda vez. (Isso é diferente do Signal, onde ela está no cabeçalho e é enviada toda vez)

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
- Pode não ser estritamente necessário, mas é útil para debugging.
  O Signal não usa um key ID.
- O Key ID máximo é 32767.
- No caso raro em que os conjuntos de tags em ambas as direções estão fazendo ratcheting ao
  mesmo tempo, um frame conterá dois blocos Next Key, um para
  a chave forward e um para a chave reverse.
- Os números de ID de conjuntos de chaves e tags devem ser sequenciais.
- Veja a seção DH Ratchet acima para detalhes.

### Seção de Payload Dados descriptografados

Isso só é enviado se um bloco de solicitação de confirmação foi recebido. Várias confirmações podem estar presentes para confirmar múltiplas mensagens.

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

- O ID do conjunto de tags e N identificam unicamente a mensagem sendo confirmada.
- Nos primeiros conjuntos de tags usados para uma sessão em cada direção, o ID do conjunto de tags é 0.
- Nenhum bloco NextKey foi enviado, então não há IDs de chave.
- Para todos os conjuntos de tags usados após trocas NextKey, o número do conjunto de tags é (1 + ID da chave da Alice + ID da chave do Bob).

### Dados não criptografados

Solicitar um ack in-band. Para substituir a Mensagem DeliveryStatus out-of-band no Garlic Clove.

Se um ack explícito for solicitado, o ID do tagset atual e o número da mensagem (N) são retornados em um bloco de ack.

Não permitido em NS ou NSR. Incluído apenas em mensagens de Sessão Existente.

```

+----+----+----+----+
  |  9 |  size   |flg |
  +----+----+----+----+

  blk :: 9
  size :: 1
  flg :: 1 byte flags
         bits 7-0: Unused, set to 0 for future compatibility

```
### Regras de Ordenação de Blocos

Todo o padding está dentro dos frames AEAD. TODO O padding dentro do AEAD deve aderir aproximadamente aos parâmetros negociados. TODO Alice enviou seus parâmetros tx/rx min/max solicitados na mensagem NS. TODO Bob enviou seus parâmetros tx/rx min/max solicitados na mensagem NSR. Opções atualizadas podem ser enviadas durante a fase de dados. Veja as informações do bloco de opções acima.

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

- O preenchimento com zeros é aceitável, pois será criptografado.
- Estratégias de preenchimento a serem definidas.
- Frames apenas de preenchimento são permitidos.
- O padrão de preenchimento é 0-15 bytes.
- Consulte o bloco de opções para negociação do parâmetro de preenchimento
- Consulte o bloco de opções para parâmetros mínimo/máximo de preenchimento
- A resposta do router à violação do preenchimento negociado depende da implementação.

### DateTime

As implementações devem ignorar tipos de bloco desconhecidos para compatibilidade futura.

### Dente de Garlic

- O comprimento do preenchimento deve ser decidido por mensagem com base em estimativas da distribuição de comprimento, ou atrasos aleatórios devem ser adicionados. Essas contramedidas devem ser incluídas para resistir à DPI, pois os tamanhos das mensagens revelariam que o tráfego I2P está sendo transportado pelo protocolo de transporte. O esquema exato de preenchimento é uma área de trabalho futuro, o Apêndice A fornece mais informações sobre o tópico.

## Typical Usage Patterns

### Terminação

Este é o caso de uso mais típico, e a maioria dos casos de uso de streaming não-HTTP será idêntica a este caso de uso também. Uma pequena mensagem inicial é enviada, uma resposta segue, e mensagens adicionais são enviadas em ambas as direções.

Um HTTP GET geralmente cabe em uma única mensagem I2NP. Alice envia uma pequena requisição com uma única mensagem de Session nova, incluindo um reply leaseset. Alice inclui ratchet imediato para nova chave. Inclui sig para vincular ao destino. Nenhum ack solicitado.

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
### Opções

Alice tem três opções:

1) Enviar apenas a primeira mensagem (tamanho da janela = 1), como no HTTP GET. Não recomendado.

2) Enviar até a janela de streaming, mas usando a mesma chave pública em texto claro codificada com Elligator2. Todas as mensagens contêm a mesma próxima chave pública (ratchet). Isso será visível para OBGW/IBEP porque todas começam com o mesmo texto claro. As coisas prosseguem como em 1). Não recomendado.

3) Implementação recomendada. Enviar até a janela de streaming, mas usando uma chave pública de texto claro codificada em Elligator2 diferente (sessão) para cada uma. Todas as mensagens contêm a mesma próxima chave pública (ratchet). Isso não será visível para OBGW/IBEP porque todas começam com texto claro diferente. Bob deve reconhecer que todas contêm a mesma próxima chave pública, e responder a todas com o mesmo ratchet. Alice usa essa próxima chave pública e continua.

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
### Números de Mensagem

Uma única mensagem, com uma única resposta esperada. Mensagens ou respostas adicionais podem ser enviadas.

Semelhante ao HTTP GET, mas com opções menores para o tamanho da janela de tag de sessão e tempo de vida. Talvez não solicite um ratchet.

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
### Próxima Chave Pública DH Ratchet

Múltiplas mensagens anônimas, sem respostas esperadas.

Neste cenário, Alice solicita uma sessão, mas sem vinculação. Uma nova mensagem de sessão é enviada. Nenhum leaseSet de resposta é agrupado. Um DSM de resposta é agrupado (este é o único caso de uso que requer DSMs agrupados). Nenhuma próxima chave é incluída. Nenhuma resposta ou ratchet é solicitado. Nenhum ratchet é enviado. As opções definem a janela de session tags como zero.

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
### Confirmação

Uma única mensagem anônima, sem resposta esperada.

Uma mensagem única é enviada. Nenhum LS de resposta ou DSM são incluídos. Nenhuma próxima chave é incluída. Nenhuma resposta ou ratchet é solicitado. Nenhum ratchet é enviado. As opções definem a janela de session tags como zero.

```

Alice                           Bob

  One-Time Message (1d)   ------------------->
  with bundled message
  without bundled LS
  without bundled Delivery Status Message

```
### Solicitação de Ack

Sessões de longa duração podem executar ratchet, ou solicitar um ratchet, a qualquer momento, para manter o sigilo futuro a partir desse ponto no tempo. As sessões devem executar ratchet à medida que se aproximam do limite de mensagens enviadas por sessão (65535).

## Implementation Considerations

### Preenchimento

Assim como no protocolo ElGamal/AES+SessionTag existente, as implementações devem limitar o armazenamento de session tags e proteger contra ataques de esgotamento de memória.

Algumas estratégias recomendadas incluem:

- Limite rígido no número de tags de sessão armazenadas
- Expiração agressiva de sessões inbound inativas quando sob pressão de memória
- Limite no número de sessões inbound vinculadas a um único destino remoto
- Redução adaptativa da janela de tags de sessão e exclusão de tags antigas não utilizadas
  quando sob pressão de memória
- Recusa em fazer ratchet quando solicitado, se sob pressão de memória

### Outros tipos de blocos

Parâmetros recomendados e timeouts:

- Tamanho do tagset NSR: 12 tsmin e tsmax
- Tamanho do tagset ES 0: tsmin 24, tsmax 160
- Tamanho do tagset ES (1+): 160 tsmin e tsmax
- Timeout do tagset NSR: 3 minutos para o receptor
- Timeout do tagset ES: 8 minutos para o remetente, 10 minutos para o receptor
- Remover tagset ES anterior após: 3 minutos
- Antecipação do tagset da tag N: min(tsmax, tsmin + N/4)
- Corte do tagset atrás da tag N: min(tsmax, tsmin + N/4) / 2
- Enviar próxima chave na tag: TBD
- Enviar próxima chave após tempo de vida do tagset: TBD
- Substituir sessão se NS recebido após: 3 minutos
- Desvio máximo do relógio: -5 minutos a +2 minutos
- Duração do filtro de replay NS: 5 minutos
- Tamanho do padding: 0-15 bytes (outras estratégias TBD)

### Trabalho futuro

Seguem as recomendações para classificar mensagens recebidas.

### X25519 Only

Num túnel que é usado exclusivamente com este protocolo, faça a identificação como é feito atualmente com ElGamal/AES+SessionTags:

Primeiro, trate os dados iniciais como uma session tag e procure a session tag. Se encontrada, descriptografe usando os dados armazenados associados a essa session tag.

Se não encontrado, trate os dados iniciais como uma chave pública DH e nonce. Execute uma operação DH e o KDF especificado, e tente descriptografar os dados restantes.

### HTTP GET

Em um túnel que suporta tanto este protocolo quanto ElGamal/AES+SessionTags, classifique as mensagens recebidas da seguinte forma:

Devido a uma falha na especificação ElGamal/AES+SessionTags, o bloco AES não é preenchido com um comprimento aleatório não-mod-16. Portanto, o comprimento das mensagens Existing Session mod 16 é sempre 0, e o comprimento das mensagens New Session mod 16 é sempre 2 (já que o bloco ElGamal tem 514 bytes de comprimento).

Se o comprimento mod 16 não for 0 ou 2, trate os dados iniciais como uma session tag, e procure pela session tag. Se encontrada, descriptografe usando os dados armazenados associados a essa session tag.

Se não encontrado, e o comprimento mod 16 não for 0 ou 2, trate os dados iniciais como uma chave pública DH e nonce. Execute uma operação DH e o KDF especificado, e tente descriptografar os dados restantes. (baseado na mistura relativa de tráfego, e nos custos relativos das operações DH X25519 e ElGamal, este passo pode ser feito por último)

Caso contrário, se o comprimento mod 16 for 0, trate os dados iniciais como uma session tag ElGamal/AES, e procure pela session tag. Se encontrada, descriptografe usando os dados armazenados associados àquela session tag.

Se não for encontrado, e os dados tiverem pelo menos 642 (514 + 128) bytes de comprimento, e o comprimento mod 16 for 2, trate os dados iniciais como um bloco ElGamal. Tente descriptografar os dados restantes.

Note que se a especificação ElGamal/AES+SessionTag for atualizada para permitir padding não-mod-16, as coisas precisarão ser feitas de forma diferente.

### HTTP POST

As implementações iniciais dependem de tráfego bidirecional nas camadas superiores. Ou seja, as implementações assumem que o tráfego na direção oposta será transmitido em breve, o que forçará qualquer resposta necessária na camada ECIES.

No entanto, certo tráfego pode ser unidirecional ou de largura de banda muito baixa, de modo que não há tráfego de camada superior para gerar uma resposta oportuna.

O recebimento de mensagens NS e NSR requer uma resposta; o recebimento de blocos ACK Request e Next Key também requer uma resposta.

Uma implementação sofisticada pode iniciar um temporizador quando uma dessas mensagens é recebida e requer uma resposta, e gerar uma resposta "vazia" (sem bloco Garlic Clove) na camada ECIES se nenhum tráfego reverso for enviado em um período curto de tempo (por exemplo, 1 segundo).

Também pode ser apropriado usar um timeout ainda mais curto para respostas a mensagens NS e NSR, para direcionar o tráfego para as eficientes mensagens ES o mais rápido possível.

## Analysis

### Datagrama Replicável

A sobrecarga de mensagem para as duas primeiras mensagens em cada direção é a seguinte. Isto assume apenas uma mensagem em cada direção antes do ACK, ou que quaisquer mensagens adicionais sejam enviadas especulativamente como mensagens de Sessão Existente. Se não houver ACKs especulativos de session tags entregues, a sobrecarga do protocolo antigo é muito maior.

Nenhum preenchimento é assumido para análise do novo protocolo. Nenhum leaseSet agrupado é assumido.

### Múltiplos Datagramas Raw

Nova mensagem de sessão, igual para cada direção:

```

ElGamal block:
  514 bytes

  AES block:
  - 2 byte tag count
  - 1024 bytes of tags (32 typical)
  - 4 byte payload size
  - 32 byte hash of payload
  - 1 byte flags
  - 1 byte clove count
  - 33 byte Garlic deliv. inst.
  - 16 byte I2NP header
  - 15 byte clove cert, id, exp.
  - 15 byte msg cert, id, exp.
  - 0 byte padding assuming 1936 byte message
  1143 total

  Total:
  1657 bytes
```
Mensagens de sessão existentes, iguais em cada direção:

```

AES block:
  - 32 byte session tag
  - 2 byte tag count
  - 4 byte payload size
  - 32 byte hash of payload
  - 1 byte flags
  - 1 byte clove count
  - 33 byte Garlic deliv. inst.
  - 16 byte I2NP header
  - 15 byte msg cert, id, exp.
  - 15 byte clove cert, id, exp.
  - 0 byte padding assuming 1936 byte message
  151 total
```
```
Four message total (two each direction)
  3616 bytes overhead
```
### Datagrama Bruto Único

Mensagem de Nova Sessão Alice-para-Bob:

```

- 32 byte ephemeral public key
  - 32 byte static public key
  - 16 byte Poly1305 MAC
  - 7 byte DateTime block
  - 3 byte Garlic block overhead
  - 9 byte I2NP header
  - 33 byte Garlic deliv. inst.
  - 16 byte Poly1305 MAC

  Total:
  148 bytes overhead
```
Mensagem de Resposta de Nova Sessão de Bob-para-Alice:

```

- 8 byte session tag
  - 32 byte ephemeral public key
  - 16 byte Poly1305 MAC
  - 3 byte Garlic block overhead
  - 9 byte I2NP header
  - 33 byte Garlic deliv. inst.
  - 16 byte Poly1305 MAC

  Total:
  117 bytes overhead
```
Mensagens de sessão existentes, mesma em cada direção:

```

- 8 byte session tag
  - 3 byte Garlic block overhead
  - 9 byte I2NP header
  - 33 byte Garlic deliv. inst.
  - 16 byte Poly1305 MAC

  Total:
  69 bytes
```
### Sessões de Longa Duração

Quatro mensagens no total (duas em cada direção):

```

372 bytes
  90% (approx. 10x) reduction compared to ElGamal/AES+SessionTags
```
Apenas handshake:

```

ElGamal: 1657 + 1657 = 3314 bytes
  Ratchet: 148 _ 117 = 265 bytes
  92% (approx. 12x) reduction compared to ElGamal/AES+SessionTags
```
Total a longo prazo (ignorando handshakes):

```
ElGamal: 151 + 32 byte tag sent previously = 183 bytes
  Ratchet: 69 bytes
  64% (approx. 3x) reduction compared to ElGamal/AES+SessionTags
```
### CPU

TODO atualizar esta seção após a proposta estar estável.

As seguintes operações criptográficas são necessárias para cada parte trocar mensagens New Session e New Session Reply:

- HMAC-SHA256: 3 por HKDF, total TBD
- ChaChaPoly: 2 cada
- Geração de chave X25519: 2 Alice, 1 Bob
- X25519 DH: 3 cada
- Verificação de assinatura: 1 (Bob)

Alice calcula 5 ECDHs por sessão vinculada (mínimo), 2 para cada mensagem NS para Bob, e 3 para cada uma das mensagens NSR de Bob.

Bob também calcula 6 ECDHs por sessão vinculada, 3 para cada uma das mensagens NS de Alice, e 3 para cada uma de suas mensagens NSR.

As seguintes operações criptográficas são requeridas por cada parte para cada mensagem de Sessão Existente:

- HKDF: 2
- ChaChaPoly: 1

### Defesa

O comprimento atual da tag de sessão é de 32 bytes. Ainda não encontramos nenhuma justificativa para esse comprimento, mas continuamos pesquisando os arquivos. A proposta acima define o novo comprimento da tag como 8 bytes. A análise que justifica uma tag de 8 bytes é a seguinte:

O ratchet de session tag é assumido como gerador de tags aleatórias, uniformemente distribuídas. Não há razão criptográfica para um comprimento específico de session tag. O ratchet de session tag é sincronizado com, mas gera uma saída independente do, ratchet de chave simétrica. As saídas dos dois ratchets podem ter comprimentos diferentes.

Portanto, a única preocupação é a colisão de tags de sessão. Presume-se que as implementações não tentarão lidar com colisões tentando descriptografar com ambas as sessões; as implementações simplesmente associarão a tag com a sessão anterior ou nova, e qualquer mensagem recebida com essa tag na outra sessão será descartada após a falha na descriptografia.

O objetivo é selecionar um comprimento de session tag que seja grande o suficiente para minimizar o risco de colisões, mas pequeno o suficiente para minimizar o uso de memória.

Isso assume que as implementações limitam o armazenamento de session tags para prevenir ataques de exaustão de memória. Isso também reduzirá drasticamente as chances de um atacante criar colisões. Veja a seção Considerações de Implementação abaixo.

Para um caso pior, assuma um servidor movimentado com 64 novas sessões de entrada por segundo. Assuma um tempo de vida de session tag de entrada de 15 minutos (igual ao atual, provavelmente deveria ser reduzido). Assuma uma janela de session tag de entrada de 32. 64 * 15 * 60 * 32 = 1.843.200 tags O máximo atual de tags de entrada do Java I2P é 750.000 e nunca foi atingido pelo que sabemos.

Uma meta de 1 em um milhão (1e-6) de colisões de session tag provavelmente é suficiente. A probabilidade de descartar uma mensagem ao longo do caminho devido ao congestionamento é muito maior que isso.

Ref: https://en.wikipedia.org/wiki/Birthday_paradox Seção da tabela de probabilidades.

Com session tags de 32 bytes (256 bits), o espaço de session tag é 1.2e77. A probabilidade de uma colisão com probabilidade 1e-18 requer 4.8e29 entradas. A probabilidade de uma colisão com probabilidade 1e-6 requer 4.8e35 entradas. 1,8 milhão de tags de 32 bytes cada é cerca de 59 MB no total.

Com session tags de 16 bytes (128 bits), o espaço de session tags é de 3,4e38. A probabilidade de uma colisão com probabilidade 1e-18 requer 2,6e10 entradas. A probabilidade de uma colisão com probabilidade 1e-6 requer 2,6e16 entradas. 1,8 milhão de tags de 16 bytes cada uma totaliza cerca de 30 MB.

Com session tags de 8 bytes (64 bits), o espaço de session tags é 1,8e19. A probabilidade de uma colisão com probabilidade 1e-18 requer 6,1 entradas. A probabilidade de uma colisão com probabilidade 1e-6 requer 6,1e6 (6.100.000) entradas. 1,8 milhão de tags de 8 bytes cada uma totaliza cerca de 15 MB.

6,1 milhões de tags ativas é mais de 3x superior à nossa estimativa do pior caso de 1,8 milhões de tags. Portanto, a probabilidade de colisão seria inferior a uma em um milhão. Concluímos, portanto, que session tags de 8 bytes são suficientes. Isso resulta em uma redução de 4x do espaço de armazenamento, além da redução de 2x porque as tags de transmissão não são armazenadas. Assim, teremos uma redução de 8x no uso de memória de session tags comparado ao ElGamal/AES+SessionTags.

Para manter flexibilidade caso essas suposições estejam erradas, incluiremos um campo de comprimento de session tag nas opções, para que o comprimento padrão possa ser substituído por sessão. Não esperamos implementar negociação dinâmica de comprimento de tag a menos que seja absolutamente necessário.

As implementações devem, no mínimo, reconhecer colisões de session tag, tratá-las de forma elegante, e registrar ou contar o número de colisões. Embora ainda extremamente improváveis, elas serão muito mais prováveis do que eram para ElGamal/AES+SessionTags, e poderiam realmente acontecer.

### Parâmetros

Usando duas vezes as sessões por segundo (128) e duas vezes a janela de tag (64), temos 4 vezes as tags (7,4 milhões). O máximo para uma chance de colisão de um em um milhão é 6,1 milhões de tags. Tags de 12 bytes (ou até mesmo 10 bytes) adicionariam uma margem enorme.

No entanto, será que a chance de um em um milhão de colisão é um bom objetivo? Muito maior que a chance de ser descartado ao longo do caminho não é muito útil. O objetivo de falso-positivo para o DecayingBloomFilter do Java é aproximadamente 1 em 10.000, mas mesmo 1 em 1.000 não é motivo de grave preocupação. Ao reduzir o objetivo para 1 em 10.000, há uma margem abundante com tags de 8 bytes.

### Classificação

O remetente gera tags e chaves dinamicamente, portanto não há armazenamento. Isso reduz os requisitos gerais de armazenamento pela metade em comparação com ElGamal/AES. As tags ECIES têm 8 bytes em vez de 32 para ElGamal/AES. Isso reduz os requisitos gerais de armazenamento por outro fator de 4. As chaves de sessão por tag não são armazenadas no receptor, exceto para "lacunas", que são mínimas para taxas de perda razoáveis.

A redução de 33% no tempo de expiração das tags cria uma economia adicional de 33%, assumindo tempos de sessão curtos.

Portanto, a economia total de espaço vs. ElGamal/AES é um fator de 10,7, ou 92%.

## Related Changes

### Apenas X25519

Consultas de Banco de Dados a partir de Destinos ECIES: Consulte a [Proposta 154](/proposals/154-ecies-lookups), agora incorporada no [I2NP](/docs/specs/i2np/) para a versão 0.9.46.

Esta proposta requer suporte LS2 para publicar a chave pública X25519 com o leaseset. Nenhuma alteração é necessária nas especificações LS2 em [I2NP](/docs/specs/i2np/). Todo o suporte foi projetado, especificado e implementado na [Proposta 123](/proposals/123-new-netdb-entries) implementada na versão 0.9.38.

### X25519 Compartilhado com ElGamal/AES+SessionTags

Nenhuma. Esta proposta requer suporte a LS2 e uma propriedade a ser definida nas opções I2CP para ser habilitada. Não são necessárias alterações nas especificações do [I2CP](/docs/specs/i2cp/). Todo o suporte foi projetado, especificado e implementado na [Proposta 123](/proposals/123-new-netdb-entries) implementada na versão 0.9.38.

A opção necessária para habilitar ECIES é uma única propriedade I2CP para I2CP, BOB, SAM, ou i2ptunnel.

Os valores típicos são i2cp.leaseSetEncType=4 apenas para ECIES, ou i2cp.leaseSetEncType=4,0 para chaves duplas ECIES e ElGamal.

### Respostas da Camada de Protocolo

Esta seção é copiada da [Proposta 123](/proposals/123-new-netdb-entries).

Opção no Mapeamento SessionConfig:

```
  i2cp.leaseSetEncType=nnn[,nnn]  The encryption types to be used.
                                  0: ElGamal
                                  1-3: See proposal 145
                                  4: This proposal.
```
### Create Leaseset2 Message

Esta proposta requer LS2 que é suportado a partir da versão 0.9.38. Nenhuma alteração é necessária nas especificações do [I2CP](/docs/specs/i2cp/). Todo o suporte foi projetado, especificado e implementado na [Proposta 123](/proposals/123-new-netdb-entries) implementada na 0.9.38.

### Sobrecarga

Qualquer router que suporte LS2 com chaves duplas (0.9.38 ou superior) deve suportar conexão para destinos com chaves duplas.

Destinos apenas ECIES exigirão que a maioria dos floodfills seja atualizada para 0.9.46 para obter respostas de consulta criptografadas. Veja [Proposta 154](/proposals/154-ecies-lookups).

Destinos ECIES-only só podem conectar com outros destinos que sejam ECIES-only ou dual-key.
