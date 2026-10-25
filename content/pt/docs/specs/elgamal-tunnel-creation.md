---
title: "Especificação de Criação de Tunnel (ElGamal)"
description: "Especificação legada de construção de túnel baseada em ElGamal, substituída por X25519"
slug: "elgamal-tunnel-creation"
aliases:
  - "/pt/tunnel-alt-creation"
  - "/pt/tunnel-alt-creation/"
lastUpdated: "2025-05"
accurateFor: "0.9.66"
---

## Visão geral {#tunnelcreate-overview}

NOTA: OBSOLETO - Esta é a especificação de construção de tunnel ElGamal. Consulte a [especificação de construção de tunnel X25519](/docs/specs/tunnel-creation-ecies) para o método atual.

Este documento especifica os detalhes das mensagens criptografadas de construção de tunnel usadas para criar tunnels usando um método de "telescoping não-interativo". Consulte o documento de construção de tunnel [TUNNEL-IMPL](/docs/specs/tunnel-implementation) para uma visão geral do processo, incluindo métodos de seleção e ordenação de peers.

A criação do tunnel é realizada por uma única mensagem passada ao longo do caminho dos peers no tunnel, reescrita no local e transmitida de volta ao criador do tunnel. Esta única mensagem de tunnel é composta por um número variável de registros (até 8) - um para cada peer potencial no tunnel. Os registros individuais são criptografados assimetricamente (ElGamal [CRYPTO-ELG](/docs/specs/cryptography#elgamal)) para serem lidos apenas por um peer específico ao longo do caminho, enquanto uma camada adicional de criptografia simétrica (AES [CRYPTO-AES](/docs/specs/cryptography#AES)) é adicionada a cada salto de forma a expor o registro criptografado assimetricamente apenas no momento apropriado.

### Número de Registros {#number}

Nem todos os registros precisam conter dados válidos. A mensagem de construção para um tunnel de 3 saltos, por exemplo, pode conter mais registros para ocultar o comprimento real do tunnel dos participantes. Existem dois tipos de mensagens de construção. A Tunnel Build Message ([TBM](/docs/specs/i2np#msg-tunnelbuild)) original contém 8 registros, que é mais do que suficiente para qualquer comprimento prático de tunnel. A Variable Tunnel Build Message ([VTBM](/docs/specs/i2np#msg-variabletunnelbuild)) mais recente contém de 1 a 8 registros. O originador pode equilibrar o tamanho da mensagem com a quantidade desejada de ofuscação do comprimento do tunnel.

Na rede atual, a maioria dos tunnels têm 2 ou 3 saltos de comprimento. A implementação atual usa um VTBM de 5 registros para construir tunnels de 4 saltos ou menos, e o TBM de 8 registros para tunnels mais longos. O VTBM de 5 registros (que, quando fragmentado, cabe em três mensagens de tunnel de 1KB) reduz o tráfego de rede e aumenta a taxa de sucesso de construção, porque mensagens menores têm menos probabilidade de serem descartadas.

A mensagem de resposta deve ser do mesmo tipo e comprimento que a mensagem de construção.

### Especificação de Registro de Solicitação {#tunnelcreate-requestrecord}

Também especificado na Especificação I2NP [BRR](/docs/specs/i2np#struct-buildrequestrecord).

Texto em claro do registro, visível apenas ao hop que está sendo consultado:

```
bytes     0-3: tunnel ID to receive messages as, nonzero
bytes    4-35: local router identity hash
bytes   36-39: next tunnel ID, nonzero
bytes   40-71: next router identity hash
bytes  72-103: AES-256 tunnel layer key
bytes 104-135: AES-256 tunnel IV key
bytes 136-167: AES-256 reply key
bytes 168-183: AES-256 reply IV
byte      184: flags
bytes 185-188: request time (in hours since the epoch, rounded down)
bytes 189-192: next message ID
bytes 193-221: uninterpreted / random padding
```
Os campos de próximo ID do tunnel e hash de identidade do próximo router são usados para especificar o próximo salto no tunnel, embora para um endpoint de tunnel de saída, eles especifiquem para onde a mensagem de resposta de criação de tunnel reescrita deve ser enviada. Além disso, o próximo ID de mensagem especifica o ID da mensagem que a mensagem (ou resposta) deve usar.

A chave da camada tunnel, chave IV do tunnel, chave de resposta e IV de resposta são cada uma valores aleatórios de 32 bytes gerados pelo criador, para uso apenas neste registro de solicitação de construção.

O campo flags contém o seguinte:

```
Bit order: 76543210 (bit 7 is MSB)
bit 7: if set, allow messages from anyone
bit 6: if set, allow messages to anyone, and send the reply to the
       specified next hop in a Tunnel Build Reply Message
bits 5-0: Undefined, must set to 0 for compatibility with future options
```
O Bit 7 indica que o hop será um gateway de entrada (IBGW). O Bit 6 indica que o hop será um endpoint de saída (OBEP). Se nenhum bit estiver definido, o hop será um participante intermediário. Ambos não podem estar definidos ao mesmo tempo.

#### Criação de Registro de Solicitação

Cada salto recebe um Tunnel ID aleatório, diferente de zero. Os Tunnel IDs do salto atual e do próximo salto são preenchidos. Cada registro recebe uma chave IV de tunnel aleatória, IV de resposta, chave de camada e chave de resposta.

#### Criptografia de Registro de Solicitação {#encryption}

Esse registro em texto simples é criptografado com ElGamal 2048 [CRYPTO-ELG](/docs/specs/cryptography#elgamal) usando a chave pública de criptografia do salto e formatado em um registro de 528 bytes:

```
bytes   0-15: First 16 bytes of the SHA-256 of the current hop's router identity
bytes 16-527: ElGamal-2048 encrypted request record
```
No registro criptografado de 512 bytes, os dados ElGamal contêm os bytes 1-256 e 258-513 do bloco criptografado ElGamal de 514 bytes [CRYPTO-ELG](/docs/specs/cryptography#elgamal). Os dois bytes de preenchimento do bloco (os bytes zero nas posições 0 e 257) são removidos.

Como o texto não cifrado usa o campo completo, não há necessidade de preenchimento adicional além de `SHA256(cleartext) + cleartext`.

Cada registro de 528 bytes é então criptografado iterativamente (usando descriptografia AES, com a chave de resposta e IV de resposta para cada salto) de modo que a identidade do router só esteja em texto claro para o salto em questão.

### Processamento de Hop e Criptografia {#tunnelcreate-hopprocessing}

Quando um hop recebe uma TunnelBuildMessage, ele procura através dos registros contidos nela por um que comece com seu próprio hash de identidade (cortado para 16 bytes). Em seguida, descriptografa o bloco ElGamal desse registro e recupera o texto claro protegido. Nesse ponto, eles garantem que a solicitação de tunnel não seja uma duplicata alimentando a chave de resposta AES-256 em um filtro Bloom. Duplicatas ou solicitações inválidas são descartadas. Registros que não estão marcados com a hora atual, ou a hora anterior se logo após o início da hora, devem ser descartados. Por exemplo, pegue a hora no timestamp, converta para um tempo completo, então se estiver mais de 65 minutos atrasado ou 5 minutos adiantado em relação ao tempo atual, é inválido. O filtro Bloom deve ter uma duração de pelo menos uma hora (mais alguns minutos, para permitir desvio de relógio), para que registros duplicados na hora atual que não sejam rejeitados pela verificação do timestamp da hora no registro, sejam rejeitados pelo filtro.

Após decidir se concordam ou não em participar do tunnel, eles substituem o registro que continha a solicitação por um bloco de resposta criptografado. Todos os outros registros são criptografados AES-256 [CRYPTO-AES](/docs/specs/cryptography#AES) com a chave de resposta e IV incluídos. Cada um é criptografado AES/CBC separadamente com a mesma chave de resposta e IV de resposta. O modo CBC não é continuado (encadeado) entre os registros.

Cada hop conhece apenas sua própria resposta. Se concordar, manterá o tunnel até a expiração, mesmo que não seja usado, pois não pode saber se todos os outros hops concordaram.

#### Especificação do Registro de Resposta {#tunnelcreate-replyrecord}

Depois que o hop atual lê seu registro, ele o substitui por um registro de resposta informando se concorda ou não em participar do tunnel, e se não concorda, ele classifica sua razão para a rejeição. Este é simplesmente um valor de 1 byte, com 0x0 significando que concorda em participar no tunnel, e valores mais altos significando níveis mais altos de rejeição.

Os seguintes códigos de rejeição estão definidos:

- TUNNEL_REJECT_PROBABALISTIC_REJECT = 10
- TUNNEL_REJECT_TRANSIENT_OVERLOAD = 20
- TUNNEL_REJECT_BANDWIDTH = 30
- TUNNEL_REJECT_CRIT = 50

Para ocultar outras causas, como desligamento do router, dos pares, a implementação atual usa TUNNEL_REJECT_BANDWIDTH para quase todas as rejeições.

A resposta é criptografada com a chave de sessão AES entregue a ela no bloco criptografado, preenchida com 495 bytes de dados aleatórios para atingir o tamanho completo do registro. O preenchimento é colocado antes do byte de status:

```
AES-256-CBC(SHA-256(padding+status) + padding + status, key, IV)

bytes   0-31 : SHA-256 of bytes 32-527
bytes 32-526 : Random padding
byte 527     : Reply value
```
Isso também é descrito na especificação I2NP [BRR](/docs/specs/i2np#struct-buildrequestrecord).

### Preparação da Mensagem de Construção de Tunnel {#tunnelcreate-requestpreparation}

Ao construir uma nova Tunnel Build Message, todos os Build Request Records devem primeiro ser construídos e criptografados assimetricamente usando ElGamal [CRYPTO-ELG](/docs/specs/cryptography#elgamal). Cada registro é então descriptografado preventivamente com as chaves de resposta e IVs dos saltos anteriores no caminho, usando AES [CRYPTO-AES](/docs/specs/cryptography#AES). Essa descriptografia deve ser executada em ordem reversa para que os dados criptografados assimetricamente apareçam em texto limpo no salto correto após seu predecessor criptografá-los.

Os registros excedentes não necessários para solicitações individuais são simplesmente preenchidos com dados aleatórios pelo criador.

### Entrega de Mensagem de Construção de Tunnel {#tunnelcreate-requestdelivery}

Para tunnels de saída, a entrega é feita diretamente do criador do tunnel para o primeiro salto, empacotando a TunnelBuildMessage como se o criador fosse apenas outro salto no tunnel. Para tunnels de entrada, a entrega é feita através de um tunnel de saída existente. O tunnel de saída é geralmente do mesmo pool que o novo tunnel sendo construído. Se nenhum tunnel de saída estiver disponível nesse pool, um tunnel exploratório de saída é usado. Na inicialização, quando ainda não existe nenhum tunnel exploratório de saída, um tunnel de saída falso de 0 saltos é usado.

### Manipulação de Endpoint de Mensagem de Construção de Tunnel {#tunnelcreate-endpointhandling}

Para a criação de um tunnel de saída, quando a solicitação atinge um endpoint de saída (conforme determinado pela flag 'permitir mensagens para qualquer um'), o hop é processado normalmente, criptografando uma resposta no lugar do registro e criptografando todos os outros registros, mas como não há um 'próximo hop' para encaminhar a TunnelBuildMessage, ele coloca os registros de resposta criptografados em uma TunnelBuildReplyMessage ([TBRM](/docs/specs/i2np#msg-tunnelbuildreply)) ou VariableTunnelBuildReplyMessage ([VTBRM](/docs/specs/i2np#msg-variabletunnelbuildreply)) (o tipo de mensagem e número de registros deve corresponder ao da solicitação) e a entrega ao tunnel de resposta especificado dentro do registro da solicitação. Esse tunnel de resposta encaminha a Tunnel Build Reply Message de volta ao criador do tunnel, assim como para qualquer outra mensagem [TUNNEL-OP](/docs/specs/tunnel-implementation#tunnel.operation). O criador do tunnel então a processa, conforme descrito abaixo.

O tunnel de resposta foi selecionado pelo criador da seguinte forma: Geralmente é um tunnel de entrada do mesmo pool que o novo tunnel de saída sendo construído. Se nenhum tunnel de entrada estiver disponível nesse pool, um tunnel exploratório de entrada é usado. Na inicialização, quando ainda não existe nenhum tunnel exploratório de entrada, um tunnel de entrada falso de 0 saltos é usado.

Para a criação de um tunnel de entrada, quando a solicitação atinge o endpoint de entrada (também conhecido como criador do tunnel), não há necessidade de gerar uma Mensagem de Resposta de Construção de Tunnel explícita, e o router processa cada uma das respostas, conforme descrito abaixo.

### Processamento de Mensagem de Resposta de Construção de Tunnel {#tunnelcreate-replyprocessing}

Para processar os registros de resposta, o criador simplesmente tem que descriptografar AES cada registro individualmente, usando a chave de resposta e IV de cada hop no tunnel após o peer (em ordem reversa). Isso então expõe a resposta especificando se eles concordam em participar no tunnel ou por que eles recusam. Se todos concordarem, o tunnel é considerado criado e pode ser usado imediatamente, mas se alguém recusar, o tunnel é descartado.

Os acordos e rejeições são anotados no perfil de cada peer [PEER-SELECTION](/docs/overview/peer-selection), para serem usados em avaliações futuras da capacidade de tunnel do peer.

## Histórico e Notas {#tunnelcreate-notes}

Esta estratégia surgiu durante uma discussão na lista de email do I2P entre Michael Rogers, Matthew Toseland (toad) e jrandom sobre o ataque predecessor. Veja [TUNBUILD-SUMMARY](http://zzz.i2p/archive/2005-10/msg00138.html), [TUNBUILD-REASONING](http://zzz.i2p/archive/2005-10/msg00129.html). Foi introduzida na versão 0.6.1.10 em 16/02/2006, que foi a última vez que uma mudança não compatível com versões anteriores foi feita no I2P.

Notas:

- Este design não impede que dois peers hostis dentro de um tunnel marquem um ou mais registros de solicitação ou resposta para detectar que estão dentro do mesmo tunnel, mas fazer isso pode ser detectado pelo criador do tunnel ao ler a resposta, fazendo com que o tunnel seja marcado como inválido.

- Este design não inclui uma prova de trabalho na seção criptografada assimetricamente, embora o hash de identidade de 16 bytes possa ser reduzido pela metade com a última parte sendo substituída por uma função hashcash de até 2^64 de custo.

- Este design por si só não impede que dois pares hostis dentro de um tunnel usem informações de temporização para determinar se estão no mesmo tunnel. O uso de entrega de solicitações em lote e sincronizada poderia ajudar (agrupando solicitações e enviando-as no minuto (sincronizado por ntp)). No entanto, fazer isso permite que os pares 'marquem' as solicitações atrasando-as e detectando o atraso mais tarde no tunnel, embora talvez descartar solicitações não entregues em uma pequena janela funcionaria (embora fazer isso exigiria um alto grau de sincronização de relógio). Alternativamente, talvez saltos individuais poderiam injetar um atraso aleatório antes de encaminhar a solicitação?

- Existem métodos não fatais de marcar a solicitação?

- O timestamp com resolução de uma hora é usado para prevenção de replay. A restrição não foi aplicada até a versão 0.9.16.

## Trabalho Futuro {#future}

- Na implementação atual, o originador deixa um registro vazio
  para si mesmo. Assim, uma mensagem de n registros só pode construir um tunnel de n-1 saltos.
  Isso parece ser necessário para tunnels de entrada (onde o penúltimo salto
  pode ver o prefixo hash para o próximo salto), mas não para tunnels de saída.
  Isso deve ser pesquisado e verificado. Se for possível usar o
  registro restante sem comprometer o anonimato, devemos fazê-lo.

- Análise adicional de possíveis ataques de marcação e temporização descritos nas notas acima.

- Use apenas VTBM; não selecione peers antigos que não o suportam.

- O Build Request Record não especifica um tempo de vida ou expiração do tunnel;
  cada hop expira o tunnel após 10 minutos, que é uma constante hardcoded de toda a rede. Poderíamos usar um bit no campo de flag e tirar 4 (ou 8)
  bytes do padding para especificar um tempo de vida ou expiração. O solicitante
  só especificaria esta opção se todos os participantes a suportassem.

## Referências {#ref}

- [BRR](/docs/specs/i2np#struct-buildrequestrecord) - Build Request Record
- [CRYPTO-AES](/docs/specs/cryptography#AES) - AES Encryption
- [CRYPTO-ELG](/docs/specs/cryptography#elgamal) - ElGamal Encryption
- [HASHING-IT-OUT](http://www-users.cs.umn.edu/~hopper/hashing_it_out.pdf) - Hashing It Out Paper
- [PEER-SELECTION](/docs/overview/peer-selection) - Peer Selection
- [PREDECESSOR](http://forensics.umass.edu/pubs/wright-tissec.pdf) - Predecessor Attack Paper
- [PREDECESSOR-2008](http://forensics.umass.edu/pubs/wright.tissec.2008.pdf) - Predecessor Attack Paper (2008)
- [TBM](/docs/specs/i2np#msg-tunnelbuild) - Tunnel Build Message
- [TBRM](/docs/specs/i2np#msg-tunnelbuildreply) - Tunnel Build Reply Message
- [TUNBUILD-REASONING](http://zzz.i2p/archive/2005-10/msg00129.html) - Tunnel Build Reasoning
- [TUNBUILD-SUMMARY](http://zzz.i2p/archive/2005-10/msg00138.html) - Tunnel Build Summary
- [TUNNEL-IMPL](/docs/specs/tunnel-implementation) - Tunnel Implementation
- [TUNNEL-OP](/docs/specs/tunnel-implementation#tunnel.operation) - Tunnel Operation
- [VTBM](/docs/specs/i2np#msg-variabletunnelbuild) - Variable Tunnel Build Message
- [VTBRM](/docs/specs/i2np#msg-variabletunnelbuildreply) - Variable Tunnel Build Reply Message
