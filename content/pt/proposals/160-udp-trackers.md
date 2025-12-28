---
title: "Rastreadores UDP"
number: "160"
author: "zzz"
created: "2022-01-03"
lastupdated: "2025-06-25"
status: "Fechado"
thread: "http://zzz.i2p/topics/1634"
target: "0.9.67"
toc: true
---

## Status

Aprovado na revisão de 24-06-2025. A especificação está em [UDP specification](/docs/specs/udp-bittorrent-announces/). Implementado no zzzot 0.20.0-beta2. Implementado no i2psnark a partir da API 0.9.67. Verifique a documentação de outras implementações para o status.

## Visão Geral

Esta proposta é para implementação de rastreadores UDP no I2P.

### Change History

Uma proposta preliminar para rastreadores UDP no I2P foi publicada em nossa [página de especificação bittorrent](/docs/applications/bittorrent/) em maio de 2014; isso antecedeu nosso processo formal de propostas, e nunca foi implementada. Esta proposta foi criada no início de 2022 e simplifica a versão de 2014.

Como esta proposta depende de datagramas replicáveis, foi colocada em espera quando começamos a trabalhar na [proposta Datagram2](/proposals/163-datagram2/) no início de 2023. Essa proposta foi aprovada em abril de 2025.

A versão de 2023 desta proposta especificou dois modos, "compatibilidade" e "rápido". Uma análise mais aprofundada revelou que o modo rápido seria inseguro, e também seria ineficiente para clientes com um grande número de torrents. Além disso, o BiglyBT indicou uma preferência pelo modo de compatibilidade. Este modo será mais fácil de implementar para qualquer tracker ou cliente que suporte o [BEP 15](http://www.bittorrent.org/beps/bep_0015.html) padrão.

Embora o modo de compatibilidade seja mais complexo de implementar do zero no lado do cliente, temos código preliminar para isso iniciado em 2023.

Portanto, a versão atual aqui é ainda mais simplificada para remover o modo rápido e remover o termo "compatibilidade". A versão atual muda para o novo formato Datagram2 e adiciona referências ao protocolo de extensão UDP announce [BEP 41](http://www.bittorrent.org/beps/bep_0041.html).

Além disso, um campo de tempo de vida do ID de conexão é adicionado à resposta de conexão, para estender os ganhos de eficiência deste protocolo.

## Motivation

À medida que a base de usuários em geral e o número de usuários de bittorrent especificamente continua a crescer, precisamos tornar os trackers e anúncios mais eficientes para que os trackers não sejam sobrecarregados.

O Bittorrent propôs trackers UDP no BEP 15 [BEP 15](http://www.bittorrent.org/beps/bep_0015.html) em 2008, e a grande maioria dos trackers na clearnet agora são apenas UDP.

É difícil calcular as economias de largura de banda dos datagramas vs. protocolo de streaming. Uma solicitação respondível tem aproximadamente o mesmo tamanho de um SYN de streaming, mas o payload é cerca de 500 bytes menor porque o HTTP GET tem uma enorme string de parâmetros de URL de 600 bytes. A resposta bruta é muito menor que um SYN ACK de streaming, proporcionando redução significativa para o tráfego de saída de um tracker.

Além disso, devem haver reduções de memória específicas da implementação, já que datagramas requerem muito menos estado na memória do que uma conexão de streaming.

A criptografia e assinaturas pós-quânticas como previstas em [/proposals/169-pq-crypto/](/proposals/169-pq-crypto/) aumentarão substancialmente a sobrecarga das estruturas criptografadas e assinadas, incluindo destinations, leasesets, streaming SYN e SYN ACK. É importante minimizar essa sobrecarga sempre que possível antes que a criptografia pós-quântica seja adotada no I2P.

## Motivação

Esta proposta usa repliable datagram2, repliable datagram3, e raw datagrams, conforme definido em [/docs/api/datagrams/](/docs/api/datagrams/). Datagram2 e Datagram3 são novas variantes de repliable datagrams, definidas na Proposta 163 [/proposals/163-datagram2/](/proposals/163-datagram2/). Datagram2 adiciona resistência a replay e suporte a assinatura offline. Datagram3 é menor que o formato antigo de datagrama, mas sem autenticação.

### BEP 15

Para referência, o fluxo de mensagens definido no [BEP 15](http://www.bittorrent.org/beps/bep_0015.html) é o seguinte:

```
Client                        Tracker
    Connect Req. ------------->
      <-------------- Connect Resp.
    Announce Req. ------------->
      <-------------- Announce Resp.
    Announce Req. ------------->
      <-------------- Announce Resp.
```
A fase de conexão é obrigatória para prevenir a falsificação de endereços IP. O tracker retorna um ID de conexão que o cliente usa em anúncios subsequentes. Este ID de conexão expira por padrão em um minuto no cliente, e em dois minutos no tracker.

O I2P usará o mesmo fluxo de mensagens do BEP 15, para facilitar a adoção em bases de código de clientes existentes capazes de UDP: por eficiência e pelas razões de segurança discutidas abaixo:

```
Client                        Tracker
    Connect Req. ------------->       (Repliable Datagram2)
      <-------------- Connect Resp.   (Raw)
    Announce Req. ------------->      (Repliable Datagram3)
      <-------------- Announce Resp.  (Raw)
    Announce Req. ------------->      (Repliable Datagram3)
      <-------------- Announce Resp.  (Raw)
             ...
```
Isso potencialmente proporciona uma grande economia de largura de banda em relação aos anúncios de streaming (TCP). Embora o Datagram2 tenha aproximadamente o mesmo tamanho de um SYN de streaming, a resposta raw é muito menor que o SYN ACK de streaming. As solicitações subsequentes usam Datagram3, e as respostas subsequentes são raw.

As solicitações de anúncio são Datagram3 para que o tracker não precise manter uma grande tabela de mapeamento de IDs de conexão para destino de anúncio ou hash. Em vez disso, o tracker pode gerar IDs de conexão criptograficamente a partir do hash do remetente, do timestamp atual (baseado em algum intervalo), e de um valor secreto. Quando uma solicitação de anúncio é recebida, o tracker valida o ID de conexão, e então usa o hash do remetente Datagram3 como o alvo de envio.

### Histórico de Alterações

Para uma aplicação integrada (router e cliente em um processo, por exemplo i2psnark, e o plugin Java ZzzOT), ou para uma aplicação baseada em I2CP (por exemplo BiglyBT), deve ser direto implementar e rotear o tráfego de streaming e datagrama separadamente. ZzzOT e i2psnark são esperados para serem o primeiro tracker e cliente a implementar esta proposta.

Trackers e clientes não integrados são discutidos abaixo.

#### Trackers

Existem quatro implementações conhecidas de tracker I2P:

- zzzot, um plugin integrado para router Java, executando em opentracker.dg2.i2p e vários outros
- tracker2.postman.i2p, executando presumivelmente atrás de um router Java e túnel HTTP Server
- O antigo opentracker em C, portado pelo zzz, com suporte UDP comentado
- O novo opentracker em C, portado pelo r4sas, executando em opentracker.r4sas.i2p e possivelmente outros,
  executando presumivelmente atrás de um router i2pd e túnel HTTP Server

Para uma aplicação de tracker externa que atualmente usa um túnel de servidor HTTP para receber solicitações de anúncio, a implementação poderia ser bastante difícil. Um túnel especializado poderia ser desenvolvido para traduzir datagramas em solicitações/respostas HTTP locais. Ou, um túnel especializado que manipula tanto solicitações HTTP quanto datagramas poderia ser projetado para encaminhar os datagramas para o processo externo. Essas decisões de design dependerão fortemente das implementações específicas do router e do tracker, e estão fora do escopo desta proposta.

#### Clients

Clientes de torrent externos baseados em SAM, como qbittorrent e outros clientes baseados em libtorrent, exigiriam [SAM v3.3](/docs/api/samv3/) que não é suportado pelo i2pd. Isso também é necessário para suporte a DHT, e é complexo o suficiente para que nenhum cliente de torrent SAM conhecido o tenha implementado. Não são esperadas implementações baseadas em SAM desta proposta em breve.

### Connection Lifetime

[BEP 15](http://www.bittorrent.org/beps/bep_0015.html) especifica que o ID de conexão expira em um minuto no cliente, e em dois minutos no tracker. Não é configurável. Isso limita os potenciais ganhos de eficiência, a menos que os clientes agrupem anúncios para fazer todos eles dentro de uma janela de um minuto. O i2psnark atualmente não agrupa anúncios; ele os espalha, para evitar rajadas de tráfego. Usuários avançados são relatados executando milhares de torrents de uma vez, e concentrar tantos anúncios em um minuto não é realista.

Aqui, propomos estender a resposta de conexão para adicionar um campo opcional de tempo de vida da conexão. O padrão, se não estiver presente, é um minuto. Caso contrário, o tempo de vida especificado em segundos deverá ser usado pelo cliente, e o tracker manterá o ID da conexão por mais um minuto.

### Compatibility with BEP 15

Este design mantém compatibilidade com [BEP 15](http://www.bittorrent.org/beps/bep_0015.html) tanto quanto possível para limitar as mudanças necessárias em clientes e trackers existentes.

A única mudança necessária é o formato das informações do peer na resposta de anúncio. A adição do campo lifetime na resposta de conexão não é obrigatória, mas é fortemente recomendada por eficiência, como explicado acima.

### BEP 15

Um objetivo importante de um protocolo de anúncio UDP é prevenir a falsificação de endereços. O cliente deve realmente existir e incluir um leaseset real. Ele deve ter túneis de entrada para receber a Resposta de Conexão. Esses túneis poderiam ser de zero saltos e construídos instantaneamente, mas isso exporia o criador. Este protocolo cumpre esse objetivo.

### Suporte a Tracker/Cliente

- Esta proposta não suporta destinos cegos,
  mas pode ser estendida para fazê-lo. Veja abaixo.

## Design

### Protocols and Ports

Repliable Datagram2 usa protocolo I2CP 19; repliable Datagram3 usa protocolo I2CP 20; datagramas brutos usam protocolo I2CP 18. As requisições podem ser Datagram2 ou Datagram3. As respostas são sempre brutas. O formato mais antigo de datagrama repliable ("Datagram1") usando protocolo I2CP 17 NÃO DEVE ser usado para requisições ou respostas; estes devem ser descartados se recebidos nas portas de requisição/resposta. Note que o protocolo Datagram1 17 ainda é usado para o protocolo DHT.

As requisições usam a "porta de destino" I2CP da URL de anúncio; veja abaixo. A "porta de origem" da requisição é escolhida pelo cliente, mas deve ser diferente de zero e uma porta diferente daquelas usadas pelo DHT, para que as respostas possam ser facilmente classificadas. Os trackers devem rejeitar requisições recebidas na porta errada.

As respostas usam a "porta de destino" I2CP da solicitação. A "porta de origem" da solicitação é a "porta de destino" da solicitação.

### Announce URL

O formato da URL de announce não é especificado em [BEP 15](http://www.bittorrent.org/beps/bep_0015.html), mas como na clearnet, URLs de announce UDP são da forma "udp://host:port/path". O path é ignorado e pode estar vazio, mas normalmente é "/announce" na clearnet. A parte :port deve sempre estar presente, no entanto, se a parte ":port" for omitida, use uma porta I2CP padrão de 6969, já que essa é a porta comum na clearnet. Também pode haver parâmetros cgi &a=b&c=d anexados, esses podem ser processados e fornecidos na solicitação de announce, veja [BEP 41](http://www.bittorrent.org/beps/bep_0041.html). Se não houver parâmetros ou path, a barra final / também pode ser omitida, como implícito em [BEP 41](http://www.bittorrent.org/beps/bep_0041.html).

### Duração da Conexão

Todos os valores são enviados em ordem de bytes de rede (big endian). Não espere que os pacotes tenham exatamente um determinado tamanho. Extensões futuras podem aumentar o tamanho dos pacotes.

#### Connect Request

Cliente para tracker. 16 bytes. Deve ser um Datagram2 com resposta possível. O mesmo que em [BEP 15](http://www.bittorrent.org/beps/bep_0015.html). Sem alterações.

```
Offset  Size            Name            Value
  0       64-bit integer  protocol_id     0x41727101980 // magic constant
  8       32-bit integer  action          0 // connect
  12      32-bit integer  transaction_id
```
#### Connect Response

Tracker para cliente. 16 ou 18 bytes. Deve ser bruto. Igual ao [BEP 15](http://www.bittorrent.org/beps/bep_0015.html) exceto conforme observado abaixo.

```
Offset  Size            Name            Value
  0       32-bit integer  action          0 // connect
  4       32-bit integer  transaction_id
  8       64-bit integer  connection_id
  16      16-bit integer  lifetime        optional  // Change from BEP 15
```
A resposta DEVE ser enviada para a "porta de destino" I2CP que foi recebida como a "porta de origem" da solicitação.

O campo lifetime é opcional e indica o tempo de vida do connection_id do cliente em segundos. O padrão é 60, e o mínimo se especificado é 60. O máximo é 65535 ou cerca de 18 horas. O tracker deve manter o connection_id por 60 segundos a mais que o tempo de vida do cliente.

#### Announce Request

Cliente para tracker. 98 bytes mínimo. Deve ser um Datagram3 que permite resposta. Igual ao [BEP 15](http://www.bittorrent.org/beps/bep_0015.html) exceto conforme observado abaixo.

O connection_id é como recebido na resposta de conexão.

```
Offset  Size            Name            Value
  0       64-bit integer  connection_id
  8       32-bit integer  action          1     // announce
  12      32-bit integer  transaction_id
  16      20-byte string  info_hash
  36      20-byte string  peer_id
  56      64-bit integer  downloaded
  64      64-bit integer  left
  72      64-bit integer  uploaded
  80      32-bit integer  event           0     // 0: none; 1: completed; 2: started; 3: stopped
  84      32-bit integer  IP address      0     // default
  88      32-bit integer  key
  92      32-bit integer  num_want        -1    // default
  96      16-bit integer  port
  98      varies          options     optional  // As specified in BEP 41
```
Mudanças da [BEP 15](http://www.bittorrent.org/beps/bep_0015.html):

- key é ignorada
- port é provavelmente ignorada
- A seção options, se presente, é conforme definida em [BEP 41](http://www.bittorrent.org/beps/bep_0041.html)

A resposta DEVE ser enviada para a "porta de destino" I2CP que foi recebida como "porta de origem" da solicitação. Não use a porta da solicitação de anúncio.

#### Announce Response

Tracker para cliente. 20 bytes mínimo. Deve ser raw. Igual ao [BEP 15](http://www.bittorrent.org/beps/bep_0015.html) exceto como indicado abaixo.

```
Offset  Size            Name            Value
  0           32-bit integer  action          1 // announce
  4           32-bit integer  transaction_id
  8           32-bit integer  interval
  12          32-bit integer  leechers
  16          32-bit integer  seeders
  20   32 * n 32-byte hash    binary hashes     // Change from BEP 15
  ...                                           // Change from BEP 15
```
Mudanças de [BEP 15](http://www.bittorrent.org/beps/bep_0015.html):

- Em vez de IPv4+porta de 6 bytes ou IPv6+porta de 18 bytes, retornamos
  um múltiplo de "respostas compactas" de 32 bytes com os hashes binários SHA-256 dos peers.
  Como nas respostas compactas TCP, não incluímos uma porta.

A resposta DEVE ser enviada para a "porta de destino" I2CP que foi recebida como "porta de origem" da solicitação. Não use a porta da solicitação de anúncio.

Os datagramas I2P têm um tamanho máximo muito grande de cerca de 64 KB; no entanto, para entrega confiável, datagramas maiores que 4 KB devem ser evitados. Para eficiência de largura de banda, os trackers provavelmente deveriam limitar o máximo de peers para cerca de 50, o que corresponde a cerca de um pacote de 1600 bytes antes do overhead em várias camadas, e deveria estar dentro de um limite de payload de duas mensagens de tunnel após a fragmentação.

Como no BEP 15, não há contagem incluída do número de endereços de peers (IP/porta para BEP 15, hashes aqui) a seguir. Embora não contemplado no BEP 15, um marcador de fim de peers com todos zeros poderia ser definido para indicar que a informação do peer está completa e alguns dados de extensão seguem.

Para que a extensão seja possível no futuro, os clientes devem ignorar um hash de 32 bytes com todos zeros, e quaisquer dados que o seguem. Os trackers devem rejeitar anúncios de um hash com todos zeros, embora esse hash já seja banido pelos roteadores Java.

#### Scrape

A solicitação/resposta de scrape do [BEP 15](http://www.bittorrent.org/beps/bep_0015.html) não é exigida por esta proposta, mas pode ser implementada se desejado, nenhuma alteração necessária. O cliente deve adquirir um ID de conexão primeiro. A solicitação de scrape é sempre um Datagram3 que pode ser respondido. A resposta de scrape é sempre raw.

#### Rastreadores

Tracker para cliente. 8 bytes mínimo (se a mensagem estiver vazia). Deve ser raw. Igual ao [BEP 15](http://www.bittorrent.org/beps/bep_0015.html). Sem alterações.

```
Offset  Size            Name            Value
  0       32-bit integer  action          3 // error
  4       32-bit integer  transaction_id
  8       string          message
```
## Extensions

Bits de extensão ou um campo de versão não são incluídos. Clientes e trackers não devem assumir que os pacotes tenham um tamanho específico. Desta forma, campos adicionais podem ser adicionados sem quebrar a compatibilidade. O formato de extensões definido na [BEP 41](http://www.bittorrent.org/beps/bep_0041.html) é recomendado se necessário.

A resposta de conexão é modificada para adicionar um tempo de vida opcional do ID de conexão.

Se o suporte a destino blinded for necessário, podemos adicionar o endereço blinded de 35 bytes ao final da solicitação de anúncio, ou solicitar hashes blinded nas respostas, usando o formato [BEP 41](http://www.bittorrent.org/beps/bep_0041.html) (parâmetros a serem definidos). O conjunto de endereços peer blinded de 35 bytes poderia ser adicionado ao final da resposta de anúncio, após um hash de 32 bytes com todos zeros.

## Implementation guidelines

Consulte a seção de design acima para uma discussão dos desafios para clientes e trackers não integrados e não-I2CP.

### Compatibilidade com BEP 15

Para um determinado hostname de tracker, um cliente deve preferir URLs UDP em vez de HTTP, e não deve anunciar para ambos.

Clientes com suporte BEP 15 existente devem exigir apenas pequenas modificações.

Se um cliente suporta DHT ou outros protocolos de datagrama, ele provavelmente deveria selecionar uma porta diferente como a "porta de origem" da solicitação para que as respostas retornem para essa porta e não sejam misturadas com mensagens DHT. O cliente apenas recebe datagramas brutos como respostas. Os trackers nunca enviarão um datagrama2 com resposta possível para o cliente.

Os clientes com uma lista padrão de opentrackers devem atualizar a lista para adicionar URLs UDP após os opentrackers conhecidos serem reconhecidos como suportando UDP.

Os clientes podem ou não implementar retransmissão de solicitações. Retransmissões, se implementadas, devem usar um timeout inicial de pelo menos 15 segundos, e dobrar o timeout para cada retransmissão (backoff exponencial).

Os clientes devem recuar após receber uma resposta de erro.

### Análise de Segurança

Trackers com suporte BEP 15 existente devem exigir apenas pequenas modificações. Esta proposta difere da proposta de 2014, pois o tracker deve suportar a recepção de datagram2 e datagram3 com resposta na mesma porta.

Para minimizar os requisitos de recursos do tracker, este protocolo foi projetado para eliminar qualquer requisito de que o tracker armazene mapeamentos de hashes de clientes para IDs de conexão para validação posterior. Isso é possível porque o pacote de solicitação de anúncio é um pacote Datagram3 com resposta, então ele contém o hash do remetente.

Uma implementação recomendada é:

- Definir a época atual como o tempo atual com uma resolução do tempo de vida da conexão,
  ``epoch = now / lifetime``.
- Definir uma função de hash criptográfica ``H(secret, clienthash, epoch)`` que gera
  uma saída de 8 bytes.
- Gerar o segredo constante aleatório usado para todas as conexões.
- Para respostas de conexão, gerar ``connection_id = H(secret,  clienthash, epoch)``
- Para solicitações de anúncio, validar o ID de conexão recebido na época atual verificando
  ``connection_id == H(secret, clienthash, epoch) || connection_id == H(secret, clienthash, epoch - 1)``

## Migration

Os clientes existentes não suportam URLs de anúncio UDP e as ignoram.

Os trackers existentes não suportam a recepção de datagramas com resposta ou datagramas brutos, eles serão descartados.

Esta proposta é completamente opcional. Nem clientes nem trackers são obrigatórios a implementá-la em qualquer momento.

## Rollout

As primeiras implementações são esperadas no ZzzOT e i2psnark. Elas serão usadas para teste e verificação desta proposta.

Outras implementações seguirão conforme desejado após a conclusão dos testes e verificação.
