---
title: "ECIES-X25519-AEAD-Ratchet"
number: "144"
author: "zzz, chisana, orignal"
created: "2018-11-22"
lastupdated: "2025-03-05"
status: "Closed"
thread: "http://zzz.i2p/topics/2639"
target: "0.9.46"
implementedin: "0.9.46"
---

## Nota
Implantação e teste de rede em andamento.
Sujeito a pequenas revisões.
Veja [SPEC]_ para a especificação oficial.

As seguintes funcionalidades não estão implementadas na versão 0.9.46:

- Blocos MessageNumbers, Options e Termination
- Respostas de camada de protocolo
- Chave estática zero
- Multicast


## Visão Geral

Esta é uma proposta para o primeiro novo tipo de criptografia de ponta a ponta desde o início do I2P, para substituir o ElGamal/AES+SessionTags [Elg-AES]_.

Ela se baseia nos trabalhos anteriores da seguinte forma:

- Especificação de estruturas comuns [Common]_
- Especificação [I2NP]_ incluindo LS2
- ElGamal/AES+Session Tags [Elg-AES]_
- http://zzz.i2p/topics/1768 visão geral da nova criptografia assimétrica
- Visão geral de criptografia de baixo nível [CRYPTO-ELG]_
- ECIES http://zzz.i2p/topics/2418
- [NTCP2]_ [Prop111]_
- 123 Novas entradas netDB
- 142 Novo modelo de criptografia
- Protocolo [Noise]_
- Algoritmo de catraca dupla [Signal]_

O objetivo é suportar nova criptografia para comunicação de ponta a ponta, destino a destino.

O design usará um aperto de mão Noise e fase de dados incorporando a catraca dupla do Signal.

Todas as referências ao Signal e Noise nesta proposta são apenas para informação de fundo. Não é necessário conhecimento dos protocolos Signal e Noise para entender ou implementar esta proposta.


### Usos atuais do ElGamal

Como uma revisão,
as chaves públicas do ElGamal de 256 bytes podem ser encontradas nas seguintes estruturas de dados.
Consulte a especificação de estruturas comuns.

- Em uma Identidade de Roteador
  Esta é a chave de criptografia do roteador.

- Em um Destino
  A chave pública do destino foi usada para a criptografia antiga i2cp-to-i2cp
  que foi desabilitada na versão 0.6, ela está atualmente inutilizada, exceto
  para o IV para criptografia do LeaseSet, que está obsoleta.
  A chave pública no LeaseSet é usada em seu lugar.

- Em um LeaseSet
  Esta é a chave de criptografia do destino.

- Em um LS2
  Esta é a chave de criptografia do destino.



### EncTypes em Key Certs

Como uma revisão,
adicionamos suporte para tipos de criptografia quando adicionamos suporte para tipos de assinatura.
O campo do tipo de criptografia é sempre zero, tanto em Destinations quanto em RouterIdentities.
Se algum dia mudar isso é TBD.
Consulte a especificação de estruturas comuns [Common]_.




### Usos de Criptografia Assimétrica

Como uma revisão, usamos ElGamal para:

1) Mensagens de construção de túnel (a chave está em RouterIdentity)
   A substituição não está coberta nesta proposta.
   Veja a proposta 152 [Prop152]_.

2) Criptografia de roteador para roteador de netdb e outras mensagens I2NP (a chave está em RouterIdentity)
   Depende desta proposta.
   Requer uma proposta para 1) também, ou colocar a chave nas opções RI.

3) ElGamal+AES/SessionTag de ponta a ponta do cliente (a chave está em LeaseSet, a chave de Destination está inutilizada)
   A substituição ESTÁ coberta nesta proposta.

4) DH Efêmero para NTCP1 e SSU
   A substituição não está coberta nesta proposta.
   Veja a proposta 111 para NTCP2.
   Nenhuma proposta atual para SSU2.


### Objetivos

- Compatível com versões anteriores
- Requer e se baseia no LS2 (proposta 123)
- Aproveitar nova criptografia ou primitivas adicionadas para NTCP2 (proposta 111)
- Não são necessárias novas criptografias ou primitivas para suporte
- Manter o desacoplamento da criptografia e assinatura; suportar todas as versões atuais e futuras
- Permitir nova criptografia para destinos
- Permitir nova criptografia para roteadores, mas apenas para mensagens de alho - a construção de túneis seria uma proposta separada
- Não quebrar nada que dependa de hashes binários de destino de 32 bytes, por exemplo, bittorrent
- Manter entrega de mensagem 0-RTT usando DH estático efêmero
- Não requerer bufferização/encaminhamento de mensagens nesta camada de protocolo; continuar a suportar entrega ilimitada de mensagens em ambas as direções sem esperar por uma resposta
- Atualizar para DH efêmero-efêmero após 1 RTT
- Manter o tratamento de mensagens fora de ordem
- Manter segurança de 256 bits
- Adicionar segredo futuro
- Adicionar autenticação (AEAD)
- Muito mais eficiente em termos de CPU do que ElGamal
- Não depender do jbigi Java para tornar DH eficiente
- Minimizar operações DH
- Muito mais eficiente em termos de largura de banda do que ElGamal (bloco ElGamal de 514 bytes)
- Suportar nova e antiga criptografia no mesmo túnel, se desejado
- O destinatário é capaz de distinguir eficientemente entre nova e antiga criptografia vindo do mesmo túnel
- Outros não podem distinguir entre nova, antiga ou futura criptografia
- Eliminar a classificação de comprimento de nova vs. sessão existente (suporte a padding)
- Nenhuma nova mensagem I2NP necessária
- Substituir checksum SHA-256 no payload AES por AEAD
- Suportar ligação de sessões de transmissão e recepção para que reconhecimentos possam ocorrer dentro do protocolo, em vez de apenas fora da banda.
  Isso também permitirá que respostas tenham segredo futuro imediatamente.
- Habilitar criptografia de ponta a ponta de certas mensagens (armazenamentos de RouterInfo) que atualmente não fazemos devido a sobrecarga de CPU.
- Não mudar o formato da Mensagem de Alho I2NP ou das Instruções de Entrega de Mensagens de Alho.
- Eliminar campos não utilizados ou redundantes no Garlic Clove Set e nos formatos de Clove.

Eliminar vários problemas com tags de sessão, incluindo:

- Incapacidade de usar AES até a primeira resposta
- Confiabilidade e atrasos se a entrega da tag for assumida
- Ineficiente em termos de largura de banda, especialmente na primeira entrega
- Enorme ineficiência de espaço para armazenar tags
- Grande sobrecarga de largura de banda para entregar tags
- Altamente complexo, difícil de implementar
- Difícil de ajustar para vários casos de uso (streaming vs. datagramas, servidor vs. cliente, alta vs. baixa largura de banda)
- Vulnerabilidades de exaustão de memória devido à entrega de tags


### Não-Objetivos / Fora do escopo

- Mudanças de formato LS2 (a proposta 123 está concluída)
- Novo algoritmo de rotação DHT ou geração aleatória compartilhada
- Nova criptografia para construção de túneis. Veja a proposta 152 [Prop152]_.
- Nova criptografia para criptografia em camada de túnel. Veja a proposta 153 [Prop153]_.
- Métodos de criptografia, transmissão e recepção de mensagens I2NP DLM / DSM / DSRM. Sem mudanças.
- Nenhuma comunicação LS1-to-LS2 ou ElGamal/AES-para-esta-proposta é suportada. Esta proposta é um protocolo bidirecional. Destinations podem lidar com compatibilidade retroativa publicando dois leasesets usando os mesmos túneis, ou colocando ambos os tipos de criptografia no LS2.
- Mudanças no modelo de ameaça
- Detalhes de implementação não são discutidos aqui e são deixados para cada projeto.
- (Otimista) Adicionar extensões ou ganchos para suportar multicast



### Justificativa

ElGamal/AES+SessionTag tem sido nosso único protocolo de ponta a ponta por cerca de 15 anos, essencialmente sem modificações no protocolo. Agora, existem primitivas criptográficas que são mais rápidas. Precisamos melhorar a segurança do protocolo. Também desenvolvemos estratégias heurísticas e soluções alternativas para minimizar a sobrecarga de memória e largura de banda do protocolo, mas essas estratégias são frágeis, difíceis de ajustar e tornam o protocolo ainda mais propenso a falhas, causando a queda da sessão.

Por quase o mesmo período, a especificação ElGamal/AES+SessionTag e a documentação relacionada descreveram o quão caro em termos de largura de banda é entregar tags de sessão, e propuseram substituir a entrega de tags de sessão por um "PRNG sincronizado". Um PRNG sincronizado gera deterministicamente as mesmas tags em ambas as extremidades, derivadas de uma semente comum. Um PRNG sincronizado também pode ser denominado "catraca". Esta proposta (finalmente) especifica esse mecanismo de catraca e elimina a entrega de tags.

Ao usar uma catraca (um PRNG sincronizado) para gerar as tags de sessão, eliminamos a sobrecarga do envio de tags de sessão na mensagem de Nova Sessão e em mensagens subsequentes quando necessário. Para um conjunto típico de 32 tags, são 1KB. Isso também elimina o armazenamento de tags de sessão no lado do remetente, reduzindo assim pela metade os requisitos de armazenamento.

Um aperto de mão completo de duas vias, semelhante ao padrão Noise IK, é necessário para evitar ataques de Key Compromise Impersonation (KCI). Veja a tabela de "Propriedades de Segurança de Payload" do Noise em [NOISE]_. Para mais informações sobre KCI, veja o artigo https://www.usenix.org/system/files/conference/woot15/woot15-paper-hlauschek.pdf



### Modelo de Ameaça

O modelo de ameaça é algo diferente do para NTCP2 (proposta 111). Os nós MitM são o OBEP e IBGW e devem ter uma visão completa do NetDB global atual ou histórico, ao coludirem com floodfills.

O objetivo é impedir que esses MitMs classifiquem o tráfego como mensagens de Nova e Sessão Existente, ou como nova criptografia vs. velha criptografia.



## Proposta Detalhada

Esta proposta define um novo protocolo de ponta a ponta para substituir ElGamal/AES+SessionTags. O design usará um aperto de mão Noise e fase de dados incorporando a catraca dupla do Signal.


### Resumo do Design Criptográfico

Existem cinco partes do protocolo a serem redesenhadas:


- 1) Os formatos de contêiner de Nova e Sessão Existente são substituídos por novos formatos.
- 2) ElGamal (chaves públicas de 256 bytes, chaves privadas de 128 bytes) será substituído por ECIES-X25519 (chaves públicas e privadas de 32 bytes)
- 3) AES será substituído por AEAD_ChaCha20_Poly1305 (abreviado como ChaChaPoly abaixo)
- 4) SessionTags serão substituídos por catracas, que são essencialmente um PRNG criptográfico, sincronizado.
- 5) O payload AES, conforme definido na especificação ElGamal/AES+SessionTags, é substituído por um formato de bloco semelhante ao no NTCP2.

Cada uma das cinco alterações tem sua própria seção abaixo.


### Novas Primitivas Criptográficas para I2P

As implementações dos roteadores I2P existentes exigirão implementações para as seguintes primitivas criptográficas padrão, que não são necessárias para protocolos I2P atuais:

- ECIES (mas isso é essencialmente X25519)
- Elligator2

Implementações de roteadores I2P existentes que ainda não implementaram [NTCP2]_ ([Prop111]_)
também exigirão implementações para:

- Geração de chave X25519 e DH
- AEAD_ChaCha20_Poly1305 (abreviado como ChaChaPoly abaixo)
- HKDF


### Tipo de Cripto

O tipo de criptografia (usado no LS2) é 4. Isso indica uma chave pública X25519 de 32 bytes em little-endian, e o protocolo de ponta a ponta especificado aqui.

O tipo de criptografia 0 é ElGamal. Os tipos de criptografia 1-3 são reservados para ECIES-ECDH-AES-SessionTag, consulte a proposta 145 [Prop145]_.


### Estrutura do Protocolo Noise

Esta proposta fornece os requisitos com base na Estrutura do Protocolo Noise [NOISE]_ (Revisão 34, 2018-07-11). Noise tem propriedades semelhantes ao protocolo Station-To-Station [STS]_, que é a base para o protocolo [SSU]_. Na terminologia Noise, Alice é a iniciadora, e Bob é o receptor.

Esta proposta baseia-se no protocolo Noise Noise_IK_25519_ChaChaPoly_SHA256. (O identificador real para a função inicial de derivação de chave é "Noise_IKelg2_25519_ChaChaPoly_SHA256" para indicar extensões do I2P - veja a seção KDF 1 abaixo) Este protocolo Noise utiliza as seguintes primitivas:

- Padrão de Aperto de Mão Interativo: IK
  Alice imediatamente transmite sua chave estática para Bob (I)
  Alice já conhece a chave estática de Bob (K)

- Padrão de Aperto de Mão Unilateral: N
  Alice não transmite sua chave estática para Bob (N)

- Função DH: X25519
  X25519 DH com um comprimento de chave de 32 bytes conforme especificado em [RFC-7748]_.

- Função de Cifra: ChaChaPoly
  AEAD_CHACHA20_POLY1305 conforme especificado em [RFC-7539]_ seção 2.8.
  Nonce de 12 bytes, com os primeiros 4 bytes definidos como zero.
  Idêntico ao em [NTCP2]_.

- Função Hash: SHA256
  Hash padrão de 32 bytes, já usado extensivamente no I2P.


Adições à Estrutura
``````````````````````````````````

Esta proposta define as seguintes melhorias para
Noise_IK_25519_ChaChaPoly_SHA256. Estas geralmente seguem as diretrizes na
seção 13 de [NOISE]_.

1) As chaves efêmeras de texto claro são codificadas com [Elligator2]_.

2) A resposta é prefixada com uma tag em texto claro.

3) O formato do payload é definido para mensagens 1, 2 e na fase de dados. Claro, isso não é definido no Noise.

Todas as mensagens incluem um cabeçalho de Mensagem de Alho [I2NP]_. A fase de dados usa criptografia semelhante, mas não compatível, à fase de dados do Noise.


### Padrões de Apertos de Mão

Apertos de mãos usam padrões de aperto de mão [Noise]_.

A seguinte mapeamento de letras é usado:

- e = chave efêmera de uso único
- s = chave estática
- p = payload da mensagem

As sessões de Uso Único e Não Vínculadas são semelhantes ao padrão N do Noise.

.. raw:: html

  {% highlight lang='dataspec' %}
<- s
  ...
  e es p ->

{% endhighlight %}

As sessões vinculadas são semelhantes ao padrão IK do Noise.

.. raw:: html

  {% highlight lang='dataspec' %}
<- s
  ...
  e es s ss p ->
  <- tag e ee se
  <- p
  p ->

{% endhighlight %}


### Sessões

O protocolo atual ElGamal/AES+SessionTag é unidirecional. Nesta camada, o receptor não sabe de onde a mensagem é. Sessões de saída e entrada não estão associadas. Os reconhecimentos são fora da banda usando uma DeliveryStatus Message (encapsulada em um GarlicMessage) no cravo.

Há uma ineficiência substancial em um protocolo unidirecional. Qualquer resposta deve também usar uma mensagem 'Nova Sessão' cara. Isso causa maior uso de largura de banda, CPU e memória.

Também existem fraquezas de segurança em um protocolo unidirecional. Todas as sessões são baseadas em DH estático efêmero. Sem um caminho de retorno, não há como Bob "catracar" sua chave estática para uma chave efêmera. Sem saber de onde uma mensagem é, não há como usar a chave efêmera recebida para mensagens de saída, assim, a resposta inicial também usa DH estático efêmero.

Para esta proposta, definimos dois mecanismos para criar um protocolo bidirecional - "pareamento" e "vinculação". Esses mecanismos fornecem maior eficiência e segurança.


Contexto de Sessão
````````````````````

Como com ElGamal/AES+SessionTags, toda sessão de entrada e saída deve estar em um determinado contexto, seja o contexto do roteador ou o contexto para um destino local específico. No Java I2P, esse contexto é chamado de Gerenciador de Chave de Sessão.

As sessões não devem ser compartilhadas entre contextos, pois isso permitiria essa correlação entre os vários destinos locais, ou entre um destino local e um roteador.

Quando um determinado destino suporta tanto ElGamal/AES+SessionTags quanto esta proposta, ambos os tipos de sessões podem compartilhar um contexto. Ver seção 1c) abaixo.



Pareamento de Sessões de Entrada e Saída
``````````````````````````````````````````

Quando uma sessão de saída é criada no originador (Alice), uma nova sessão de entrada é criada e pareada com a sessão de saída, a menos que nenhuma resposta seja esperada (por exemplo, datagramas brutos).

Uma nova sessão de entrada é sempre pareada com uma nova sessão de saída, a menos que nenhuma resposta seja solicitada (por exemplo, datagramas brutos).

Se uma resposta for solicitada e vinculada a um destino ou roteador de extremidade final, essa nova sessão de saída é vinculada a esse destino ou roteador, e substitui qualquer sessão de saída anterior para esse destino ou roteador.

Ao parear sessões de entrada e saída, fornecemos um protocolo bidirecional com a capacidade de catracar as chaves DH.



Vinculando Sessões e Destinos
``````````````````````````````````

Só há uma sessão de saída para um determinado destino ou roteador. Pode haver várias sessões de entrada atuais de um determinado destino ou roteador. Geralmente, quando uma nova sessão de entrada é criada, e o tráfego é recebido nessa sessão (o que serve como um ACK), qualquer outra será marcada para expirar relativamente rápido, dentro de um minuto ou mais. O valor das mensagens enviadas anteriormente (PN) é verificado, e se não houver mensagens não recebidas (dentro do tamanho da janela) na sessão de entrada anterior, a sessão anterior pode ser excluída imediatamente.


Quando uma sessão de saída é criada no originador (Alice), ela é vinculada ao Destino de extremidade final (Bob), e qualquer sessão de entrada pareada também será vinculada ao Destino de extremidade final. À medida que as sessões avançam, elas continuam vinculadas ao Destino de extremidade final.

Quando uma sessão de entrada é criada no receptor (Bob), ela pode ser vinculada ao Destino de extremidade final (Alice), à opção de Alice. Se Alice incluir informações de vinculação (sua chave estática) na mensagem de Nova Sessão, a sessão será vinculada a esse destino, e uma sessão de saída será criada e vinculada ao mesmo Destino. À medida que as sessões avançam, elas continuam vinculadas ao Destino de extremidade final.


Benefícios da Vinculação e Pareamento
``````````````````````````````````````

Para o caso comum, de streaming, esperamos que Alice e Bob usem o protocolo da seguinte forma:

- Alice pareia sua nova sessão de saída para uma nova sessão de entrada, ambas vinculadas ao destino de extremidade final (Bob).
- Alice inclui as informações de vinculação e assinatura, e uma solicitação de resposta, na mensagem de Nova Sessão enviada para Bob.
- Bob pareia sua nova sessão de entrada para uma nova sessão de saída, ambas vinculadas ao destino de extremidade final (Alice).
- Bob envia uma resposta (ack) para Alice na sessão pareada, com uma catraca para uma nova chave DH.
- Alice catraca para uma nova sessão de saída com a nova chave de Bob, pareada com a sessão de entrada existente.

Ao vincular uma sessão de entrada a um Destino de extremidade final, e pareando a sessão de entrada com uma sessão de saída vinculada ao mesmo Destino, alcançamos dois benefícios principais:

1) A resposta inicial de Bob para Alice usa DH efêmero-efêmero

2) Depois que Alice recebe a resposta de Bob e catraca, todas as mensagens subsequentes de Alice para Bob usam DH efêmero-efêmero.


ACKs de Mensagens
``````````````

Em ElGamal/AES+SessionTags, quando um LeaseSet é agrupado como um bloco de alho, ou tags são entregues, o roteador de envio solicita um ACK. Este é um bloco de alho separado contendo uma DeliveryStatus Message. Para segurança adicional, a DeliveryStatus Message é encapsulada em um Garlic Message. Esse mecanismo é fora da banda do ponto de vista do protocolo.

No novo protocolo, uma vez que as sessões de entrada e saída são pareadas, podemos ter ACKs na banda. Nenhum bloco de alho separado é necessário.

Um ACK explícito é simplesmente uma mensagem de Sessão Existente sem bloco I2NP. No entanto, na maioria dos casos, um ACK explícito pode ser evitado, pois há tráfego reverso. Pode ser desejável para implementações esperar um curto período de tempo (talvez cem ms) antes de enviar um ACK explícito, para dar à camada de streaming ou de aplicação tempo para responder.

As implementações também precisarão adiar qualquer envio de ACK até após o processamento do bloco I2NP, pois a Garlic Message pode conter uma Database Store Message com um lease set. Um lease set recente será necessário para rotear o ACK, e o destino de extremidade final (contido no lease set) será necessário para verificar a chave estática de vinculação.


Timers de Sessão
````````````````

Sessões de saída devem sempre expirar antes das sessões de entrada. Uma vez que uma sessão de saída expira, e uma nova é criada, uma nova sessão de entrada pareada também será criada. Se houvesse uma sessão de entrada anterior, ela será permitida a expirar.


### Multicast

TBD


### Definições
Definimos as seguintes funções correspondentes às bloco de construção criptográficas usadas.

ZEROLEN
    Array de bytes de comprimento zero

CSRNG(n)
    Saída de n bytes de um gerador de número aleatório criptograficamente seguro.

H(p, d)
    Função hash SHA-256 que usa uma string de personalização p e dados d, e produz uma saída de comprimento de 32 bytes.
    Conforme definido em [NOISE]_.
    || abaixo significa concatenar.

    Usar SHA-256 da seguinte forma::

        H(p, d) := SHA-256(p || d)

MixHash(d)
    Função hash SHA-256 que usa um hash anterior h e novos dados d e produz uma saída de comprimento de 32 bytes.
    || abaixo significa concatenar.

    Usar SHA-256 da seguinte forma::

        MixHash(d) := h = SHA-256(h || d)

STREAM
    O AEAD ChaCha20/Poly1305 conforme especificado em [RFC-7539]_.
    S_KEY_LEN = 32 e S_IV_LEN = 12.

    ENCRYPT(k, n, plaintext, ad)
        Criptografa o texto simples usando a chave de cifra k e um nonce n, que DEVE ser único para a chave k. Dados associados ad são opcionais. Retorna um texto cifrado que é do tamanho do texto simples + 16 bytes para o HMAC.

        O texto cifrado inteiro deve ser indistinguível do aleatório se a chave for secreta.

    DECRYPT(k, n, texto cifrado, ad)
        Descriptografa o texto cifrado usando a chave de cifra k and nonce n. Dados associados ad são opcionais. Retorna o texto simples.

DH
    Sistema de acordo de chave pública X25519. Chaves privadas de 32 bytes, chaves públicas de 32 bytes, produz saídas de 32 bytes. Tem as seguintes funções:

    GENERATE_PRIVATE()
        Gera uma nova chave privada.

    DERIVE_PUBLIC(privkey)
        Retorna a chave pública correspondente à chave privada dada.

    GENERATE_PRIVATE_ELG2()
        Gera uma nova chave privada que mapeia para uma chave pública adequada para codificação Elligator2.
        Observe que metade das chaves privadas geradas aleatoriamente não serão adequadas e devem ser descartadas.

    ENCODE_ELG2(pubkey)
        Retorna a chave pública codificada Elligator2 correspondente à chave pública fornecida (mapeamento inverso).
        As chaves codificadas são little endian.
        A chave codificada deve ser 256 bits indistinguíveis de dados aleatórios.
        Veja a seção Elligator2 abaixo para especificação.

    DECODE_ELG2(pubkey)
        Retorna a chave pública correspondente à chave pública codificada Elligator2 dada.
        Veja a seção Elligator2 abaixo para especificação.

    DH(privkey, pubkey)
        Gera um segredo compartilhado a partir das chaves privada e pública dadas.

HKDF(salt, ikm, info, n)
    Uma função criptográfica de derivação de chave que recebe algum material de entrada de chave ikm (que deve ter boa entropia, mas não é necessário ser uma string aleatória uniforme), um sal de comprimento 32 bytes, e um valor de 'info' específico do contexto, e produz uma saída de n bytes, adequada para uso como material de chave.

    Usa HKDF conforme especificado em [RFC-5869]_, usando a função hash HMAC SHA-256 conforme especificado em [RFC-2104]_. Isso significa que SALT_LEN é 32 bytes no máximo.

MixKey(d)
    Usa HKDF() com uma cadeia de chave anterior e novos dados d, e define a nova cadeia de chave e k.
    Conforme definido em [NOISE]_.

    Usa HKDF da seguinte forma::

        MixKey(d) := output = HKDF(chainKey, d, "", 64)
                     chainKey = output[0:31]
                     k = output[32:63]



### 1) Formato da mensagem

Revisão do Formato Atual da Mensagem
````````````````````````````````````

A Mensagem de Alho, conforme especificado em [I2NP]_, é a seguinte. Como um objetivo de design é que os hops intermediários não possam distinguir entre nova e antiga criptografia, esse formato não pode mudar, mesmo que o campo de comprimento seja redundante. O formato é mostrado com o cabeçalho completo de 16 bytes, embora o cabeçalho real possa estar em um formato diferente, dependendo do transporte usado.

Quando descriptografado, os dados contêm uma série de Garlic Cloves e dados adicionais, também conhecidos como um Clove Set.

Veja [I2NP]_ para detalhes e uma especificação completa.


.. raw:: html

  {% highlight lang='dataspec' %}
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

{% endhighlight %}


Revisão do Formato de Dados Criptográficos
````````````````````````````````````````````

O formato da mensagem atual, usado por mais de 15 anos, é ElGamal/AES+SessionTags. Em ElGamal/AES+SessionTags, existem dois formatos de mensagem:

1) Nova sessão:
- bloco ElGamal de 514 bytes
- bloco AES (128 bytes mínimo, múltiplo de 16)

2) Sessão existente:
- Etiqueta de Sessão de 32 bytes
- bloco AES (128 bytes mínimo, múltiplo de 16)

O padding mínimo para 128 é como implementado em Java I2P mas não é aplicado na recepção.

Essas mensagens são encapsuladas em uma mensagem de alho I2NP, que contém um campo de comprimento, então o comprimento é conhecido.

Observe que não há padding definido para um comprimento não-módulo-16, então a Nova Sessão é sempre (mod 16 == 2), e uma Sessão Existente é sempre (mod 16 == 0). Precisamos consertar isso.

O receptor primeiro tenta procurar os primeiros 32 bytes como uma Etiqueta de Sessão. Se encontrado, ele descriptografa o bloco AES. Se não for encontrado, e os dados tiverem pelo menos 514+16 de comprimento, ele tenta descriptografar o bloco ElGamal, e se bem-sucedido, descriptografa o bloco AES.


Novas Etiquetas de Sessão e Comparação ao Signal
`````````````````````````````````````````````````

No Signal Double Ratchet, o cabeçalho contém:

- DH: Chave pública de catraca atual
- PN: Comprimento da mensagem de cadeia anterior
- N: Número da Mensagem

As "correntes de envio" do Signal são aproximadamente equivalentes aos nossos conjuntos de tags. Usando uma etiqueta de sessão, podemos eliminar a maioria disso.

Na Nova Sessão, colocamos apenas a chave pública no cabeçalho não criptografado.

Na Sessão Existente, usamos uma etiqueta de sessão para o cabeçalho. A etiqueta de sessão está associada à chave pública de catraca atual e ao número da mensagem.

Tanto na nova quanto na Sessão Existente, PN e N estão no corpo criptografado.

No Signal, as coisas estão constantemente avançando. Uma nova chave pública DH exige que o receptor avance e envie uma nova chave pública de volta, que também serve como reconhecimento para a chave pública recebida. Isso seria operações de DH demasiadas para nós. Então, separamos o reconhecimento da chave recebida e a transmissão de uma nova chave. Qualquer mensagem usando uma etiqueta de sessão gerada a partir da nova chave DH constitui um ACK. Só transmitimos uma nova chave quando desejamos reformar.

O número máximo de mensagens antes que o DH deva reformar é 65535.

Ao entregar uma sessão de chave, derivamos o "Conjunto de Tags" a partir dela, em vez de ter que entregar também as etiquetas de sessão. Um Conjunto de Tags pode ter até 65536 tags. No entanto, os receptores devem implementar uma estratégia de "antevisão", em vez de gerar todas as tags possíveis de uma só vez. Só gerem no máximo N tags além da última tag boa recebida. N pode ser no máximo 128, mas 32 ou até menos pode ser uma escolha melhor.



### 1a) Novo formato de sessão

Nova Sessão Chave Pública Efêmera (32 bytes) Dados criptografados e MAC (bytes restantes)

A mensagem de Nova Sessão pode ou não conter a chave pública estática do remetente. Se ela for incluída, a sessão reversa será vinculada a essa chave. A chave estática deve ser incluída se respostas forem esperadas, por exemplo, para streaming e datagramas repliáveis. Ela não deve ser incluída para datagramas brutos.

A mensagem de Nova Sessão é semelhante ao padrão de uma via [NOISE]_, padrão "N" (se a chave estática não for enviada), ou ao padrão de duas vias "IK" (se a chave estática for enviada).



### 1b) Novo formato de sessão (com vinculação)

O comprimento é 96 + comprimento do payload. Formato criptografado:

.. raw:: html

  {% highlight lang='dataspec' %}
+----+----+----+----+----+----+----+----+
  |                                      |
  +                                       +
  |   Nova Sessão Chave Pública Efêmera   |
  +             32 bytes                  +
  |     Codificada com Elligator2         |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +         Chave Estática                +
  |       Dados criptografados ChaCha20   |
  +            32 bytes                   +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |  Poly1305 Código de Autenticação da Mensagem |
  +    (MAC) para o Segmento da Chave Estática   +
  |             16 bytes                  |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +            Segmento de Payload        +
  |       Dados criptografados ChaCha20   |
  ~                                       ~
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |  Poly1305 Código de Autenticação da Mensagem |
  +         (MAC) para o Segmento de Payload     +
  |             16 bytes                  |
  +----+----+----+----+----+----+----+----+

  Chave Pública :: 32 bytes, little endian, Elligator2, texto claro

  Dados criptografados da Chave Estática :: 32 bytes

  Dados criptografados do Segmento de Payload :: dados restantes menos 16 bytes

  MAC :: Código de autenticação da mensagem Poly1305, 16 bytes

{% endhighlight %}


Nova Sessão Chave Efêmera
`````````````````````````

A chave efêmera tem 32 bytes, codificada com Elligator2. Esta chave nunca é reutilizada; uma nova chave é gerada com cada mensagem, incluindo retransmissões.

Chave Estática
``````````````

Quando descriptografada, a chave estática X25519 de Alice, 32 bytes.


Payload
```````

O comprimento criptografado é o restante dos dados. O comprimento descriptografado é 16 menos que o comprimento criptografado. O payload deve conter um bloco DateTime e geralmente conterá um ou mais blocos Garlic Clove. Veja a seção de payload abaixo para formato e requisitos adicionais.



### 1c) Novo formato de sessão (sem vinculação)

Se nenhuma resposta for necessária, nenhuma chave estática é enviada.

O comprimento é 96 + comprimento do payload. Formato criptografado:

.. raw:: html

  {% highlight lang='dataspec' %}
+----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |   Nova Sessão Chave Pública Efêmera   |
  +             32 bytes                  +
  |     Codificada com Elligator2         |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +         Segmento de Flags             +
  |       Dados criptografados ChaCha20   +
  +            32 bytes                   +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |  Poly1305 Código de Autenticação da Mensagem |
  +         (MAC) para o segmento acima   +
  |             16 bytes                  |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +            Segmento de Payload        +
  |       Dados criptografados ChaCha20   |
  ~                                       ~
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |  Poly1305 Código de Autenticação da Mensagem |
  +         (MAC) para o Segmento de Payload     +
  |             16 bytes                  |
  +----+----+----+----+----+----+----+----+

  Chave Pública :: 32 bytes, little endian, Elligator2, texto claro

  Dados criptografados do Segmento de Flags :: 32 bytes

  Dados criptografados do Segmento de Payload :: dados restantes menos 16 bytes

  MAC :: Código de autenticação da mensagem Poly1305, 16 bytes

{% endhighlight %}

Nova Sessão Chave Efêmera
`````````````````````````

A chave efêmera de Alice. A chave efêmera tem 32 bytes, codificada com Elligator2, little endian. Esta chave nunca é reutilizada; uma nova chave é gerada com cada mensagem, incluindo retransmissões.


Dados descriptografados do Segmento de Flags
``````````````````````````````````````

O segmento de flags não contém nada. Ele tem sempre 32 bytes, porque deve ser do mesmo comprimento que a chave estática para mensagens de Nova Sessão com vinculação. Bob determina se é uma chave estática ou um segmento de flags testando se os 32 bytes são todos zeros.

TODO há alguma flag necessária aqui?

Payload
```````

O comprimento criptografado é o restante dos dados. O comprimento descriptografado é 16 menos que o comprimento criptografado. O payload deve conter um bloco DateTime e geralmente conterá um ou mais blocos Garlic Clove. Veja a seção de payload abaixo para formato e requisitos adicionais.




### 1d) Formato de uso único (sem vinculação ou sessão)

Se apenas uma única mensagem for esperada ser enviada, não é necessária configuração de sessão ou chave estática.

O comprimento é 96 + comprimento do payload. Formato criptografado:

.. raw:: html

  {% highlight lang='dataspec' %}
+----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |         Chave pública efêmera         |
  +             32 bytes                  +
  |     Codificada com Elligator2         |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +         Segmento de Flags             +
  |       Dados criptografados ChaCha20   +
  +            32 bytes                   +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |  Poly1305 Código de Autenticação da Mensagem |
  +         (MAC) para o segmento acima   +
  |             16 bytes                  |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +            Segmento de Payload        +
  |       Dados criptografados ChaCha20   |
  ~                                       ~
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |  Poly1305 Código de Autenticação da Mensagem |
  +         (MAC) para o Segmento de Payload     +
  |             16 bytes                  |
  +----+----+----+----+----+----+----+----+

  Chave Pública :: 32 bytes, little endian, Elligator2, texto claro

  Dados criptografados do Segmento de Flags :: 32 bytes

  Dados criptografados do Segmento de Payload :: dados restantes menos 16 bytes

  MAC :: Código de autenticação da mensagem Poly1305, 16 bytes

{% endhighlight %}


Nova Sessão Chave de Uso Único
`````````````````````````````

A chave de uso único tem 32 bytes, codificada com Elligator2, little endian. Esta chave nunca é reutilizada; uma nova chave é gerada com cada mensagem, incluindo retransmissões.


Dados descriptografados do Segmento de Flags
````````````````````````````````

O segmento de flags não contém nada. Ele tem sempre 32 bytes, porque deve ser do mesmo comprimento que a chave estática para mensagens de Nova Sessão com vinculação. Bob determina se é uma chave estática ou um segmento de flags testando se os 32 bytes são todos zeros.

TODO há alguma flag necessária aqui?

.. raw:: html

  {% highlight lang='dataspec' %}
+----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |                                       |
  +             Todos zeros               +
  |              32 bytes                 |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+

  zeros:: Todos zeros, 32 bytes.

{% endhighlight %}


Payload
```````

O comprimento criptografado é o restante dei dados. O comprimento descriptografado é 16 menos que o comprimento criptografado. O payload deve conter um bloco DateTime e geralmente conterá um ou mais blocos Garlic Clove. Veja a seção de payload abaixo para formato e requisitos adicionais.



### 1f) KDFs para Mensagem de Nova Sessão

KDF para Cadeia Inicial
````````````````````````

Isso é padrão [NOISE]_ para IK com um nome de protocolo modificado. Observe que usamos o mesmo inicializador para ambos, o padrão IK (sessões vinculadas) e para o padrão N (sessões não vinculadas).

O nome do protocolo é modificado por dois motivos. Primeiro, para indicar que as chaves efêmeras são codificadas com Elligator2, e segundo, para indicar que MixHash() é chamado antes da segunda mensagem para misturar o valor da tag.

.. raw:: html

  {% highlight lang='text' %}
Esta é a definição do padrão "e" de mensagens:

  // Define protocol_name.
  Defina protocol_name = "Noise_IKelg2+hs2_25519_ChaChaPoly_SHA256"
   (40 bytes, US-ASCII codificado, sem terminação NULL).

  // Define Hash h = 32 bytes
  h = SHA256(protocol_name);

  Defina ck = 32 byte de encadeamento. Copie os dados de h em ck.
  Defina chainKey = h

  // MixHash(null prologue)
  h = SHA256(h);

  // até agora, tudo pode ser pré-calculado por Alice para todas as conexões de saída

{% endhighlight %}


KDF para Conteúdos Criptografados da Seção de Flags/Chave Estática
```````````````````````````````````````````````````

.. raw:: html

  {% highlight lang='text' %}
Esta é a definição do padrão "e" de mensagens:

  // Chaves estáticas X25519 de Bob
  // bpk é publicado no leaseset
  bsk = GENERATE_PRIVATE()
  bpk = DERIVE_PUBLIC(bsk)

  // Chave pública estática de Bob
  // MixHash(bpk)
  // || abaixo significa concatenar
  h = SHA256(h || bpk);

  // até agora, tudo pode ser pré-calculado por Bob para todas as conexões de entrada

  // Chaves efêmeras X25519 de Alice
  aesk = GENERATE_PRIVATE_ELG2()
  aepk = DERIVE_PUBLIC(aesk)

  // Chave pública efêmera de Alice
  // MixHash(aepk)
  // || abaixo significa concatenar
  h = SHA256(h || aepk);

  // h é usado como os dados associados para o AEAD na Mensagem de Nova Sessão
  // Retenha o Hash h para o KDF de Resposta de Nova Sessão
  // eapk é enviada em texto claro no
  // início da mensagem de Nova Sessão
  elg2_aepk = ENCODE_ELG2(aepk)
  // Como decodificado por Bob
  aepk = DECODE_ELG2(elg2_aepk)

  Fim do padrão de mensagens "e".

  Este é o padrão "es" de mensagens:

  // Noise es
  sharedSecret = DH(aesk, bpk) = DH(bsk, aepk)

  // MixKey(DH())
  //[chainKey, k] = MixKey(sharedSecret)
  // Parâmetros ChaChaPoly para criptografar/descriptografar
  keydata = HKDF(chainKey, sharedSecret, "", 64)
  chainKey = keydata[0:31]

  // Parâmetros AEAD
  k = keydata[32:63]
  n = 0
  ad = h
  ciphertext = ENCRYPT(k, n, seção de flags/chave estática, ad)

  Fim do padrão "es" de mensagens.

  Este é o padrão "s" de mensagens:

  // MixHash(ciphertext)
  // Salve para o KDF do Section de Payload
  h = SHA256(h || ciphertext)

  // Chaves estáticas X25519 de Alice
  ask = GENERATE_PRIVATE()
  apk = DERIVE_PUBLIC(ask)

  Fim do padrão "s" de mensagens.


{% endhighlight %}



KDF para Seção de Payload (com chave estática de Alice)
```````````````````````````````````````````````````````

.. raw:: html

  {% highlight lang='text' %}
Este é o padrão "ss" de mensagens:

  // Noise ss
  sharedSecret = DH(ask, bpk) = DH(bsk, apk)

  // MixKey(DH())
  //[chainKey, k] = MixKey(sharedSecret)
  // Parâmetros ChaChaPoly para criptografar/descriptografar
  // chainKey da Seção de Chave Estática
  Define sharedSecret = resultado DH X25519
  keydata = HKDF(chainKey, sharedSecret, "", 64)
  chainKey = keydata[0:31]

  // Parâmetros AEAD
  k = keydata[32:63]
  n = 0
  ad = h
  ciphertext = ENCRYPT(k, n, payload, ad)

  Fim do padrão "ss" de mensagens.

  // MixHash(ciphertext)
  // Salve para o KDF de Resposta de Nova Sessão
  h = SHA256(h || ciphertext)

{% endhighlight %}


KDF para Seção de Payload (sem chave estática de Alice)
``````````````````````````````````````````````````````

Observe que este é um padrão "N" do Noise, mas usamos o mesmo inicializador "IK" que para sessões vinculadas.

As mensagens de Nova Sessão não podem ser identificadas como contendo ou não a chave estática de Alice até que a chave estática seja descriptografada e inspecionada para determinar se contém todos os zeros. Portanto, o receptor deve usar a máquina de estado "IK" para todas as mensagens de Nova Sessão. Se a chave estática for toda de zeros, o padrão de mensagens "ss" deve ser ignorado.



.. raw:: html

  {% highlight lang='text' %}
chainKey = da Seção de Chave Flags/Estática
  k = da Seção de Chave Flags/Estática
  n = 1
  ad = h da Seção de Chave Flags/Estática
  ciphertext = ENCRYPT(k, n, payload, ad)

{% endhighlight %}



### 1g) Formato de Resposta de Nova Sessão

Uma ou mais Respostas de Nova Sessão podem ser enviadas em resposta a uma única mensagem de Nova Sessão. Cada resposta é prefixada por uma tag, que é gerada a partir de um Conjunto de Tags para a sessão.

A Resposta de Nova Sessão está em duas partes. A primeira parte é a conclusão do aperto de mão Noise IK com uma tag prefixada. O comprimento da primeira parte é 56 bytes. A segunda parte é o payload da fase de dados. O comprimento da segunda parte é 16 + comprimento do payload.

Comprimento total é 72 + comprimento do payload. Formato criptografado:

.. raw:: html

  {% highlight lang='dataspec' %}
+----+----+----+----+----+----+----+----+
  |       Etiqueta de Sessão   8 bytes    |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +        Chave Pública Efêmera          +
  |                                       |
  +            32 bytes                   +
  |     Codificada com Elligator2         |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |  Poly1305 Código de Autenticação da Mensagem |
  +  (MAC) para Seção de Chave (sem dados)     +
  |             16 bytes                  |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +            Seção de Payload           +
  |       Dados criptografados ChaCha20   |
  ~                                       ~
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |  Poly1305 Código de Autenticação da Mensagem |
  +         (MAC) para Seção de Payload         +
  |             16 bytes                  |
  +----+----+----+----+----+----+----+----+

  Tag :: 8 bytes, texto claro

  Chave Pública :: 32 bytes, little endian, Elligator2, texto claro

  MAC :: Código de autenticação da mensagem Poly1305, 16 bytes
         Nota: Os dados de texto simples ChaCha20 são vazios (ZEROLEN)

  Dados criptografados da Seção de Payload :: dados restantes menos 16 bytes

  MAC :: Código de autenticação da mensagem Poly1305, 16 bytes

{% endhighlight %}

Etiqueta de Sessão
```````````
A tag é gerada no KDF das Etiquetas de Sessão, como inicializado no DH Initialization KDF abaixo. Isso correlaciona a resposta à sessão. A chave de sessão do DH Initialization não é usada.


Resposta de Nova Sessão Chave Efêmera
````````````````````````````````````

Chave efêmera de Bob. A chave efêmera é de 32 bytes, codificada com Elligator2, little endian. Esta chave nunca é reutilizada; uma nova chave é gerada com cada mensagem, incluindo retransmissões.


Payload
```````
O comprimento criptografado é o restante dos dados. O comprimento descriptografado é 16 menos que o comprimento criptografado. O payload geralmente conterá um ou mais blocos de Garlic Clove. Veja a seção de payload abaixo para formato e requisitos adicionais.


KDF para Conjunto de Etiquetas de Resposta
````````````````````````````````

Uma ou mais etiquetas são criadas a partir do Conjunto de Tags, que é inicializado usando o KDF abaixo, utilizando a chainKey da mensagem de Nova Sessão.

.. raw:: html

  {% highlight lang='text' %}
// Gerar conjunto de etiquetas
  tagsetKey = HKDF(chainKey, ZEROLEN, "SessionReplyTags", 32)
  tagset_nsr = DH_INITIALIZE(chainKey, tagsetKey)

{% endhighlight %}


KDF para Conteúdos Criptografados da Seção de Chave de Resposta
````````````````````````````````````````````

.. raw:: html

  {% highlight lang='text' %}
// Chaves da mensagem de Nova Sessão
  // Chaves X25519 de Alice
  // apk e aepk são enviadas na mensagem de Nova Sessão original
  // ask = chave privada estática de Alice
  // apk = chave pública estática de Alice
  // aesk = chave privada efêmera de Alice
  // aepk = chave pública efêmera de Alice
  // Chaves estáticas X25519 de Bob
  // bsk = chave privada estática de Bob
  // bpk = chave pública estática de Bob

  // Gerar a tag
  tagsetEntry = tagset_nsr.GET_NEXT_ENTRY()
  tag = tagsetEntry.SESSION_TAG

  // MixHash(tag)
  h = SHA256(h || tag)

  Este é o padrão de mensagens "e":

  // Chaves efêmeras X25519 de Bob
  besk = GENERATE_PRIVATE_ELG2()
  bepk = DERIVE_PUBLIC(besk)

  // Chave pública efêmera de Bob
  // MixHash(bepk)
  // || abaixo significa concatenar
  h = SHA256(h || bepk);

  // elg2_bepk é enviado em texto claro no
  // início da mensagem de Nova Sessão
  elg2_bepk = ENCODE_ELG2(bepk)
  // Como decodificado por Bob
  bepk = DECODE_ELG2(elg2_bepk)

  Fim do padrão de mensagens "e".

  Este é o padrão de mensagens "ee":

  // MixKey(DH())
  //[chainKey, k] = MixKey(sharedSecret)
  // Parâmetros ChaChaPoly para criptografar/descriptografar
  // chainKey da Seção de Payload de Nova Sessão original
  sharedSecret = DH(aesk, bepk) = DH(besk, aepk)
  keydata = HKDF(chainKey, sharedSecret, "", 32)
  chainKey = keydata[0:31]

  Fim do padrão de mensagens "ee".

  Este é o padrão de mensagens "se":

  // MixKey(DH())
  //[chainKey, k] = MixKey(sharedSecret)
  sharedSecret = DH(ask, bepk) = DH(besk, apk)
  keydata = HKDF(chainKey, sharedSecret, "", 64)
  chainKey = keydata[0:31]

  // Parâmetros AEAD
  k = keydata[32:63]
  n = 0
  ad = h
  ciphertext = ENCRYPT(k, n, ZEROLEN, ad)

  Fim do padrão de mensagens "se".

  // MixHash(ciphertext)
  h = SHA256(h || ciphertext)

  chainKey é usado na catraca abaixo.

{% endhighlight %}


KDF para Conteúdos Criptografados da Seção de Payload
``````````````````````````````````````````

Este é como a primeira mensagem de Sessão Existente, pós-divisão, mas sem uma tag separada. Além disso, usamos o hash acima para vincular o payload à mensagem NSR.


.. raw:: html

  {% highlight lang='text' %}
// split()
  keydata = HKDF(chainKey, ZEROLEN, "", 64)
  k_ab = keydata[0:31]
  k_ba = keydata[32:63]
  tagset_ab = DH_INITIALIZE(chainKey, k_ab)
  tagset_ba = DH_INITIALIZE(chainKey, k_ba)

  // Parâmetros AEAD para payload de Resposta de Nova Sessão
  k = HKDF(k_ba, ZEROLEN, "AttachPayloadKDF", 32)
  n = 0
  ad = h
  ciphertext = ENCRYPT(k, n, payload, ad)
{% endhighlight %}


### Notas

Múltiplas mensagens NSR podem ser enviadas em resposta, cada uma com chaves efêmeras únicas, dependendo do tamanho da resposta.

Alice e Bob são obrigados a usar novas chaves efêmeras para cada mensagem NS e NSR.

Alice deve receber uma das mensagens NSR de Bob antes de enviar mensagens de Sessão Existente (ES), e Bob deve receber uma mensagem ES de Alice antes de enviar mensagens ES.

Os ``chainKey`` e ``k`` da Seção de Payload de Bob no NSR são usados como entradas para as Catracas DH iniciais ES (ambas as direções, ver DH Ratchet KDF).

Bob deve reter apenas Sessões Existentes para as mensagens ES recebidas de Alice. Qualquer outra sessão de entrada e saída criada (para múltiplos NSRs) deve ser destruída imediatamente após a recepção da primeira mensagem ES de Alice para uma determinada sessão.



### 1h) Formato de Sessão Existente

Tag de sessão (8 bytes) Dados criptografados e MAC (ver seção 3 abaixo)


Formato
``````
Criptografado:

.. raw:: html

  {% highlight lang='dataspec' %}
+----+----+----+----+----+----+----+----+
  |       Sessão Tag                      |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +            Seção de Payload            +
  |       Dados criptografados ChaCha20   |
  ~                                       ~
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |  Poly1305 Código de Autenticação da Mensagem |
  +              (MAC)                     +
  |             16 bytes                  |
  +----+----+----+----+----+----+----+----+

  Sessão Tag :: 8 bytes, texto claro

  Dados criptografados da Seção de Payload :: dados restantes menos 16 bytes

  MAC :: Código de autenticação da mensagem Poly1305, 16 bytes

{% endhighlight %}


Payload
```````
O comprimento criptografado é o restante dos dados. O comprimento descriptografado é 16 menos que o comprimento criptografado. Veja a seção de payload abaixo para formato e requisitos.


KDF
```

.. raw:: html

  {% highlight lang='text' %}
Veja seção AEAD abaixo.

  // Parâmetros AEAD para payload de Sessão Existente
  k = A chave de sessão de 32 bytes associada a esta tag de sessão
  n = O número da mensagem N na cadeia atual, conforme recuperado da tag de sessão associada.
  ad = A tag da sessão, 8 bytes
  ciphertext = ENCRYPT(k, n, payload, ad)
{% endhighlight %}



### 2) ECIES-X25519


Formato: 32-byte chaves públicas e privadas, little-endian.

Justificação: Usado em [NTCP2]_.



### 2a) Elligator2

Em apertos de mão padrão do Noise, as mensagens de aperto de mão inicial em cada direção começam com chaves efêmeras que são transmitidas em texto claro. Como as chaves válidas X25519 são distinguíveis do aleatório, um homem no meio pode distinguir essas mensagens de mensagens de Sessão Existente que começam com tags de sessão aleatórias. No [NTCP2]_ ([Prop111]_), usamos uma função XOR de baixo custo usando a chave estática fora da banda para ofuscar a chave. No entanto, o modelo de ameaça aqui é diferente; não queremos permitir que qualquer MitM use qualquer meio para confirmar o destino do tráfego ou distinguir as mensagens de aperto de mão inicial das mensagens de Sessão Existente.

Portanto, [Elligator2]_ é usado para transformar as chaves efêmeras nas mensagens de Nova Sessão e Resposta de Nova Sessão para que sejam indistinguíveis de strings aleatórias uniformes.



Formato
``````

32-byte chaves públicas e privadas. Chaves codificadas são little endian.

Conforme definido em [Elligator2]_, as chaves codificadas são indistinguíveis de 254 bits aleatórios. Exigimos 256 bits aleatórios (32 bytes). Portanto, a codificação e decodificação são definidas da seguinte forma:

Codificação:

.. raw:: html

  {% highlight lang='text' %}
Definição de ENCODE_ELG2()

  // Encode conforme definido na especificação Elligator2
  encodedKey = encode(pubkey)
  // Ou em 2 bits aleatórios para MSB
  randomByte = CSRNG(1)
  encodedKey[31] |= (randomByte & 0xc0)
{% endhighlight %}


Decodificação:

.. raw:: html

  {% highlight lang='text' %}
Definição de DECODE_ELG2()

  // Mascarar 2 bits aleatórios do MSB
  encodedKey[31] &= 0x3f
  // Decode conforme definido na especificação Elligator2
  pubkey = decode(encodedKey)
{% endhighlight %}




Justificação
`````````````

Requerido para evitar que o OBEP e IBGW classifiquem o tráfego.


Notas
`````

Elligator2 dobra o tempo médio para a geração de chaves, pois metade das chaves privadas resulta em chaves públicas que são inadequadas para codificação com Elligator2. Além disso, o tempo de geração de chaves não tem limite superior com uma distribuição exponencial, pois o gerador deve continuar tentando até encontrar um par de chaves adequado.

Essa sobrecarga pode ser administrada gerando chaves com antecedência, em uma thread separada, para manter um pool de chaves adequadas.

O gerador faz a função ENCODE_ELG2() para determinar adequação. Portanto, o gerador deve armazenar o resultado de ENCODE_ELG2() para que não seja necessário calcular novamente.

Além disso, as chaves inadequadas podem ser adicionadas ao pool de chaves usadas para [NTCP2]_, onde Elligator2 não é usado. As questões de segurança ao fazer isso são TBD.




### 3) AEAD (ChaChaPoly)

AEAD usando ChaCha20 e Poly1305, assim como em [NTCP2]_. Isso corresponde a [RFC-7539]_, que também é usado de forma semelhante no TLS [RFC-7905]_.



Entradas de Nova Sessão e Resposta de Nova Sessão
``````````````````````````````````````````

Entradas para as funções de criptografia/descriptografia para um bloco AEAD em uma mensagem de Nova Sessão:

.. raw:: html

  {% highlight lang='dataspec' %}
k :: 32 byte chave de cifra
       Veja os KDFs de Nova Sessão e Resposta de Nova Sessão acima.

  n :: Nonce baseado em contador, 12 bytes.
       n = 0

  ad :: Dados associados, 32 bytes.
        O hash SHA256 dos dados anteriores, conforme saída de mixHash()

  data :: Dados de texto simples, 0 ou mais bytes

{% endhighlight %}


Entradas de Sessão Existente
```````````````````````````````

Entradas para as funções de criptografia/descriptografia para um bloco AEAD em uma mensagem de Sessão Existente:

.. raw:: html

  {% highlight lang='dataspec' %}
k :: 32 byte chave de sessão
       Conforme procurado a partir da tag de sessão acompanhante.

  n :: Nonce baseado em contador, 12 bytes.
       O valor como procurado a partir da tag de sessão acompanhante.
       Para o emissor, o valor
       como procurado a partir da tag de sessão acompanhante.
       Os primeiros quatro bytes são sempre zero.
       Os últimos oito bytes são o número da mensagem (n), codificados em little-endian.
       O valor máximo é 65535.
       A sessão deve ser catracada quando N atingir esse valor.
       Valores mais altos nunca devem ser usados.

  ad :: Dados associados
        A tag de sessão

  data :: Dados de texto simples, 0 ou mais bytes

{% endhighlight %}


Formato Criptografado
``````````````````

Saída da função de criptografia, entrada para a função de descriptografia:

.. raw:: html

  {% highlight lang='dataspec' %}
+----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |       Dados criptografados ChaCha20   |
  ~               .   .   .               ~
  |                                       |
  +----+----+----+----+----+----+----+----+
  |  Poly1305 Código de Autenticação da Mensagem |
  +              (MAC)                    +
  |             16 bytes                  |
  +----+----+----+----+----+----+----+----+

  dados criptografados :: Mesmo tamanho do texto simples, 0 - 65519 bytes

  MAC :: Código de autenticação da mensagem Poly1305, 16 bytes

{% endhighlight %}

Notas
`````
- Como ChaCha20 é uma cifra de fluxo, os textos simples não precisam ser preenchidos.
  Bytes adicionais da chave do fluxo são descartados.

- A chave para a cifra (256 bits) é acordada por meio do SHA256 KDF.
  Os detalhes do KDF para cada mensagem estão em seções separadas abaixo.

- Frames ChaChaPoly são de tamanho conhecido, pois são encapsulados na mensagem de dados I2NP.

- Para todas as mensagens,
  padding é dentro do dado autenticado
  do frame.


Manuseio de Erros AEAD
```````````````````````

Todos os dados recebidos que falharem na verificação AEAD devem ser descartados.
Nenhuma resposta é retornada.


Justificação
`````````````

Usado em [NTCP2]_.



### 4) Catracas

Ainda usamos tags de sessão, como antes, mas usamos catracas para gerá-las. Tags de sessão também tinham uma opção de rekey que nós nunca implementamos. Portanto, é como uma catraca dupla, mas nunca fizemos a segunda.

Aqui definimos algo semelhante à Catraca Dupla do Signal. As tags de sessão são geradas de forma determinística e idêntica nos lados do receptor e transmissor.

Usando uma catraca de chave/tag simétrica, eliminamos o uso de memória para armazenar tags de sessão no lado do transmissor. Também eliminamos o consumo de largura de banda ao enviar conjuntos de tags. O uso do lado do receptor ainda é significativo, mas podemos reduzi-lo ainda mais à medida que reduzimos a tag de sessão de 32 para 8 bytes.

Não usamos criptografia de cabeçalho conforme especificado (e opcional) no Signal, usamos tags de sessão em vez disso.

Usando uma catraca DH, alcançamos segredo futuro, que nunca foi implementado em ElGamal/AES+SessionTags.

Nota: A chave pública de uso único da Nova Sessão não é parte da catraca, sua única função é criptografar a chave inicial de catraca DH de Alice.


Números de Mensagens
`````````````````````

A Catraca Dupla lida com mensagens perdidas ou fora de ordem incluindo em cada cabeçalho de mensagem uma tag. O receptor olha para o índice da tag, este é o número da mensagem N. Se a mensagem contém um bloco de Número de Mensagens com um valor PN, o receptor pode excluir todas as tags maiores que aquele valor no conjunto de tags anterior, enquanto retém tags puladas do conjunto de tags anterior caso as mensagens puladas cheguem depois.


Implementação de Exemplo
````````````````````````

Definimos as seguintes estruturas de dados e funções para implementar essas catracas.

TAGSET_ENTRY
    Uma única entrada em um TAGSET.

    INDEX
        Um índice inteiro, começando com 0

    SESSION_TAG
        Um identificador para enviar na rede, 8 bytes

    SESSION_KEY
        Uma chave simétrica, nunca enviada na rede, 32 bytes

TAGSET
    Uma coleção de TAGSET_ENTRIES.

    CREATE(key, n)
        Gera um novo TAGSET usando um material criptográfico de chave inicial de 32 bytes. O identificador da sessão associada é fornecido. O número inicial de tags a serem criadas é especificado; isso geralmente é 0 ou 1 para uma sessão de saída. LAST_INDEX = -1. EXTEND(n) é chamado.

    EXTEND(n)
        Gera n mais TAGSET_ENTRIES chamando EXTEND() n vezes.

    EXTEND()
        Gera uma TAGSET_ENTRY a mais, a menos que o número máximo de SESSION_TAGS já tenha sido gerado. Se LAST_INDEX for maior ou igual a 65535, retorne. ++ LAST_INDEX. Cria uma nova TAGSET_ENTRY com o valor LAST_INDEX e a SESSION_TAG calculada. Chama RATCHET_TAG() e (opcionalmente) RATCHET_KEY(). Para sessões de entrada, o cálculo da SESSION_KEY pode ser adiado e calculado em GET_SESSION_KEY(). Chama EXPIRE()

    EXPIRE()
        Remove tags e chaves que são muito velhas, ou se o tamanho do TAGSET exceder algum limite.

    RATCHET_TAG()
        Calcula a próxima SESSION_TAG com base na última SESSION_TAG.

    RATCHET_KEY()
        Calcula a próxima SESSION_KEY com base na última SESSION_KEY.

    SESSION
        A sessão associada.

    CREATION_TIME
        Quando o TAGSET foi criado.

    LAST_INDEX
        O último TAGSET_ENTRY INDEX gerado por EXTEND().

    GET_NEXT_ENTRY()
        Usado apenas para sessões de saída. EXTEND(1) é chamado se não houver restos TAGSET_ENTRIES restantes. Se EXTEND(1) não fez nada, o máximo de 65535 TAGSETS foi usado, e retorne um erro. Retorna o próximo TAGSET_ENTRY não utilizado.

    GET_SESSION_KEY(sessionTag)
        Usado apenas para sessões de entrada. Retorna o TAGSET_ENTRY contendo a sessionTag. Se encontrado, o TAGSET_ENTRY é removido. Se o cálculo de SESSION_KEY foi adiado, ele é calculado agora. Se houver poucas TAGSET_ENTRIES restantes, EXTEND(n) é chamado.




4a) Catraca DH
``````````````

Catracas mas não tão rápido quanto o Signal faz. Separamos o ack da chave recebida da geração da nova chave. No uso típico, Alice e Bob avançam (duas vezes) imediatamente em uma Nova Sessão, mas não avançam novamente.

Observe que uma catraca é para uma única direção e gera uma cadeia de catraca de tag de mensagem/nova sessão para essa direção. Para gerar chaves para ambas as direções, você deve avançar duas vezes.

Você deve avançar cada vez que você gerar e enviar uma nova chave. Você deve avançar cada vez que receber uma nova chave.

Alice avança uma vez ao criar uma sessão de saída não vinculada, ela não cria uma sessão de entrada (não vinculada é não repliável).

Bob avança uma vez ao criar uma sessão de entrada não vinculada e não cria uma sessão de saída correspondente (não vinculada é não repliável).

Alice continua enviando mensagens de Nova Sessão (NS) para Bob até receber uma das mensagens de Resposta de Nova Sessão (NSR) de Bob. Ela então usa os resultados do KDF da Seção de Payload do NSR como entradas para as catracas de sessão (veja DH Ratchet KDF) e começa a enviar mensagens de Sessão Existente (ES).

Para cada mensagem NS recebida, Bob cria uma nova sessão de entrada, usando os resultados do KDF da seção de resposta para entradas para a nova catraca de DH de entrada e saída ES.

Para cada resposta necessária, Bob envia para Alice uma mensagem NSR com a resposta no payload. É necessário que Bob use novas chaves efêmeras para cada NSR.

Bob deve receber uma mensagem ES de Alice em uma das sessões de entrada, antes de criar e enviar mensagens ES na sessão de saída correspondente.

Alice deve usar um temporizador para receber uma mensagem de NSR de Bob. Se o temporizador expirar, a sessão deve ser removida.

Para evitar um ataque de KCI e/ou exaustão de recursos, onde um atacante descarta as respostas NSR de Bob para manter Alice enviando mensagens NS, Alice deve evitar iniciar Novas Sessões para Bob após um certo número de tentativas devido ao tempo de espera expirar.

Alice e Bob cada um fazem uma catraca DH para cada bloco NextKey recebido.

Alice e Bob cada um geram novas catracas de conjuntos de tags e duas catracas de chaves simétricas depois de cada catraca DH. Para cada nova mensagem ES em uma dada direção, Alice e Bob avançam as catracas de tags de sessão e de chaves simétricas.

A frequência de catracas DH após
