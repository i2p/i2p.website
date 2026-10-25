---
title: "A Base de Dados da Rede"
description: "Compreendendo a base de dados de rede distribuída do I2P (netDb) - uma DHT especializada para informações de contato do router e pesquisas de destino"
slug: "network-database"
aliases:
  - "/pt/how_networkdatabase"
  - "/pt/how_networkdatabase/"
lastUpdated: "2025-03"
accurateFor: "0.9.65"
---

## Visão Geral

O netDb do I2P é um banco de dados distribuído especializado, contendo apenas dois tipos de dados - informações de contato do router (**RouterInfos**) e informações de contato de destino (**LeaseSets**). Cada pedaço de dados é assinado pela parte apropriada e verificado por qualquer pessoa que o use ou armazene. Além disso, os dados contêm informações de vitalidade, permitindo que entradas irrelevantes sejam descartadas, entradas mais novas substituam as mais antigas, e proteção contra certas classes de ataques.

O netDb é distribuído com uma técnica simples chamada "floodfill", onde um subconjunto de todos os routers, chamados "floodfill routers", mantém a base de dados distribuída.

---

## RouterInfo

Quando um router I2P quer contactar outro router, ele precisa conhecer algumas peças-chave de dados - todas elas são agrupadas e assinadas pelo router numa estrutura chamada "RouterInfo", que é distribuída com o SHA256 da identidade do router como chave. A estrutura em si contém:

- A identidade do router (uma chave de criptografia, uma chave de assinatura e um certificado)
- Os endereços de contato pelos quais pode ser alcançado
- Quando isto foi publicado
- Um conjunto de opções de texto arbitrárias
- A assinatura do acima, gerada pela chave de assinatura da identidade

### Opções Esperadas

As seguintes opções de texto, embora não sejam estritamente obrigatórias, espera-se que estejam presentes:

- **caps** (Flags de capacidades - usadas para indicar participação em floodfill, largura de banda aproximada e alcançabilidade percebida)
  - **D**: Congestionamento médio (a partir da versão 0.9.58)
  - **E**: Congestionamento alto (a partir da versão 0.9.58)
  - **f**: Floodfill
  - **G**: Rejeitando todos os tunnels (a partir da versão 0.9.58)
  - **H**: Oculto
  - **K**: Menos de 12 KBps de largura de banda compartilhada
  - **L**: 12 - 48 KBps de largura de banda compartilhada (padrão)
  - **M**: 48 - 64 KBps de largura de banda compartilhada
  - **N**: 64 - 128 KBps de largura de banda compartilhada
  - **O**: 128 - 256 KBps de largura de banda compartilhada
  - **P**: 256 - 2000 KBps de largura de banda compartilhada (a partir da versão 0.9.20, veja a nota abaixo)
  - **R**: Alcançável
  - **U**: Inalcançável
  - **X**: Mais de 2000 KBps de largura de banda compartilhada (a partir da versão 0.9.20, veja a nota abaixo)

"Largura de banda compartilhada" == (% de compartilhamento) * min(largura de banda entrada, largura de banda saída)

Para compatibilidade com routers mais antigos, um router pode publicar múltiplas letras de largura de banda, por exemplo "PO".

Nota: o limite entre as classes de largura de banda P e X pode ser 2000 ou 2048 KBps, à escolha do implementador.

- **netId** = 2 (Compatibilidade básica de rede - Um router recusará comunicar com um peer que tenha um netId diferente)
- **router.version** (Usado para determinar compatibilidade com recursos e mensagens mais recentes)

Notas sobre capacidades R/U: Um router geralmente deve publicar a capacidade R ou U, a menos que o estado de acessibilidade seja atualmente desconhecido. R significa que o router é diretamente acessível (não requer introducers, não está atrás de firewall) em pelo menos um endereço de transporte. U significa que o router NÃO é diretamente acessível em NENHUM endereço de transporte.

Opções descontinuadas: - ~~coreVersion~~ (Nunca usado, removido na versão 0.9.24) - ~~stat_uptime~~ = 90m (Não usado desde a versão 0.7.9, removido na versão 0.9.24)

Esses valores são usados por outros routers para decisões básicas. Devemos nos conectar a este router? Devemos tentar rotear um tunnel através deste router? A flag de capacidade de largura de banda, em particular, é usada apenas para determinar se o router atende a um limite mínimo para roteamento de tunnels. Acima do limite mínimo, a largura de banda anunciada não é usada ou confiável em nenhum lugar no router, exceto para exibição na interface do usuário e para depuração e análise de rede.

Números de NetID válidos:

| Uso | Número NetID |
|-------|--------------|
| Reservado | 0 |
| Reservado | 1 |
| Rede Atual (padrão) | 2 |
| Redes Futuras Reservadas | 3 - 15 |
| Forks e Redes de Teste | 16 - 254 |
| Reservado | 255 |
### Opções Adicionais

As opções de texto adicionais incluem um pequeno número de estatísticas sobre a saúde do router, que são agregadas por sites como [stats.i2p](http://stats.i2p/) para análise de desempenho da rede e depuração. Essas estatísticas foram escolhidas para fornecer dados cruciais aos desenvolvedores, como taxas de sucesso de construção de tunnel, equilibrando a necessidade desses dados com os efeitos colaterais que poderiam resultar da revelação dessas informações. As estatísticas atuais estão limitadas a:

- Taxas de sucesso, rejeição e timeout de construção de tunnel exploratório
- Número médio de tunnels participantes em 1 hora

Estas são opcionais, mas se incluídas, ajudam na análise do desempenho da rede como um todo. A partir da API 0.9.58, estas estatísticas são simplificadas e padronizadas, da seguinte forma:

- As chaves de opção são stat_(nomestat).(períodostat)
- Os valores de opção são separados por ';'
- Estatísticas para contagens de eventos ou percentagens normalizadas usam o 4º valor; os primeiros três valores não são usados mas devem estar presentes
- Estatísticas para valores médios usam o 1º valor, e não é necessário separador ';'
- Para ponderação igual de todos os routers na análise de estatísticas, e para anonimato adicional, os routers devem incluir estas estatísticas apenas após um tempo de funcionamento de uma hora ou mais, e apenas uma vez a cada 16 vezes que o RI é publicado.

Exemplo:

```
stat_tunnel.buildExploratoryExpire.60m = 0;0;0;53.14
stat_tunnel.buildExploratoryReject.60m = 0;0;0;15.51
stat_tunnel.buildExploratorySuccess.60m = 0;0;0;31.35
stat_tunnel.participatingTunnels.60m = 289.20
```
Os roteadores floodfill podem publicar dados adicionais sobre o número de entradas na sua base de dados de rede. Estes são opcionais, mas se incluídos, ajudam na análise do desempenho da rede como um todo.

As duas opções seguintes devem ser incluídas pelos routers floodfill em cada RI publicado:

- **netdb.knownLeaseSets**
- **netdb.knownRouters**

Exemplo:

```
netdb.knownLeaseSets = 158
netdb.knownRouters = 11374
```
Os dados publicados podem ser vistos na interface do usuário do router, mas não são usados ou confiáveis por nenhum outro router.

### Opções da Família

A partir da versão 0.9.24, os routers podem declarar que fazem parte de uma "família", operada pela mesma entidade. Múltiplos routers na mesma família não serão usados em um único tunnel.

As opções de família são:

- **family** (O nome da família)
- **family.key** O código do tipo de assinatura da [Chave Pública de Assinatura](/docs/specs/common-structures/#type_SigningPublicKey) da família (em dígitos ASCII) concatenado com ':' concatenado com a Chave Pública de Assinatura em base 64
- **family.sig** A assinatura de ((nome da família em UTF-8) concatenado com (hash do router de 32 bytes)) em base 64

### Expiração do RouterInfo

RouterInfos não têm tempo de expiração definido. Cada router é livre para manter sua própria política local para equilibrar a frequência de consultas de RouterInfo com uso de memória ou disco. Na implementação atual, existem as seguintes políticas gerais:

- Não há expiração durante a primeira hora de funcionamento, já que os dados persistentes armazenados podem estar desatualizados.
- Não há expiração se houver 25 ou menos RouterInfos.
- À medida que o número de RouterInfos locais aumenta, o tempo de expiração diminui, numa tentativa de manter um número razoável de RouterInfos. O tempo de expiração com menos de 120 routers é de 72 horas, enquanto o tempo de expiração com 300 routers é de cerca de 30 horas.
- RouterInfos contendo introducers [SSU](/docs/legacy/ssu/) expiram em cerca de uma hora, já que a lista de introducers expira aproximadamente nesse tempo.
- Floodfills usam um tempo de expiração curto (1 hora) para todos os RouterInfos locais, já que RouterInfos válidos serão republicados frequentemente para eles.

### Armazenamento Persistente do RouterInfo

RouterInfos são periodicamente gravados no disco para que estejam disponíveis após uma reinicialização.

Pode ser desejável armazenar persistentemente Meta LeaseSets com expirações longas. Isso depende da implementação.

### Veja Também

- [Especificação RouterInfo](/docs/specs/common-structures/#struct_RouterInfo)
- [RouterInfo Javadoc](http://idk.i2p/javadoc-i2p/net/i2p/data/router/RouterInfo.html)

---

## LeaseSet

O segundo tipo de dados distribuído no netDb é um "LeaseSet" - documentando um grupo de **pontos de entrada de tunnel (leases)** para um destino cliente específico. Cada um desses leases especifica as seguintes informações:

- O router gateway do tunnel (especificando sua identidade)
- O ID do tunnel nesse router para enviar mensagens (um número de 4 bytes)
- Quando esse tunnel irá expirar.

O próprio LeaseSet é armazenado no netDb sob a chave derivada do SHA256 do destino. Uma exceção é para Encrypted LeaseSets (LS2), a partir da versão 0.9.38. O SHA256 do byte de tipo (3) seguido da chave pública mascarada é usado para a chave DHT, e então rotacionado como usual. Veja a seção Métrica de Proximidade Kademlia abaixo.

Além desses leases, o LeaseSet inclui:

- O próprio destino (uma chave de criptografia, uma chave de assinatura e um certificado)
- Chave pública de criptografia adicional: usada para criptografia ponta a ponta de mensagens garlic
- Chave pública de assinatura adicional: destinada para revogação de LeaseSet, mas atualmente não é utilizada.
- Assinatura de todos os dados do LeaseSet, para garantir que o Destino publicou o LeaseSet.

- [Especificação de Lease](/docs/specs/common-structures/#struct_Lease)
- [Especificação de LeaseSet](/docs/specs/common-structures/#struct_LeaseSet)
- [Javadoc de Lease](http://idk.i2p/javadoc-i2p/net/i2p/data/Lease.html)
- [Javadoc de LeaseSet](http://idk.i2p/javadoc-i2p/net/i2p/data/LeaseSet.html)

A partir da versão 0.9.38, três novos tipos de LeaseSets são definidos; LeaseSet2, MetaLeaseSet e EncryptedLeaseSet. Veja abaixo.

### LeaseSets Não Publicados

Um leaseSet para um destino usado apenas para conexões de saída é *não publicado*. Ele nunca é enviado para publicação em um router floodfill. Túneis "cliente", como aqueles para navegação web e clientes IRC, são não publicados. Servidores ainda serão capazes de enviar mensagens de volta para esses destinos não publicados, devido às [mensagens de armazenamento I2NP](#leaseset-storage-to-peers).

### LeaseSets Revogados

Um LeaseSet pode ser *revogado* publicando um novo LeaseSet com zero leases. As revogações devem ser assinadas pela chave de assinatura adicional no LeaseSet. As revogações não estão totalmente implementadas, e não está claro se têm algum uso prático. Este é o único uso planejado para essa chave de assinatura, então ela está atualmente não utilizada.

### LeaseSet2 (LS2)

A partir da versão 0.9.38, os floodfills suportam uma nova estrutura LeaseSet2. Esta estrutura é muito similar à estrutura LeaseSet antiga e serve ao mesmo propósito. A nova estrutura fornece a flexibilidade necessária para suportar novos tipos de criptografia, múltiplos tipos de criptografia, opções, chaves de assinatura offline e outras funcionalidades. Consulte a proposta 123 para detalhes.

### Meta LeaseSet (LS2)

A partir da versão 0.9.38, os floodfills suportam uma nova estrutura Meta LeaseSet. Esta estrutura fornece uma estrutura semelhante a uma árvore no DHT, para referenciar outros LeaseSets. Usando Meta LeaseSets, um site pode implementar grandes serviços multihomed, onde vários Destinations diferentes são usados para fornecer um serviço comum. As entradas em um Meta LeaseSet são Destinations ou outros Meta LeaseSets, e podem ter expirações longas, até 18,2 horas. Usando esta facilidade, deve ser possível executar centenas ou milhares de Destinations hospedando um serviço comum. Veja a proposta 123 para detalhes.

### LeaseSets Criptografados (LS1)

Esta seção descreve o método antigo e inseguro de criptografar LeaseSets usando uma chave simétrica fixa. Veja abaixo a versão LS2 dos Encrypted LeaseSets.

Em um LeaseSet *criptografado*, todos os Leases são criptografados com uma chave separada. Os leases podem apenas ser decodificados, e assim o destino pode apenas ser contactado, por aqueles que possuem a chave. Não há nenhuma flag ou outra indicação direta de que o LeaseSet está criptografado. LeaseSets criptografados não são amplamente utilizados, e é um tópico para trabalho futuro pesquisar se a interface do usuário e implementação de LeaseSets criptografados poderiam ser melhoradas.

### LeaseSets Criptografados (LS2)

A partir da versão 0.9.38, floodfills suportam uma nova estrutura EncryptedLeaseSet. O Destination fica oculto, e apenas uma chave pública cegada e uma expiração ficam visíveis para o floodfill. Somente aqueles que possuem o Destination completo podem descriptografar a estrutura. A estrutura é armazenada em uma localização DHT baseada no hash da chave pública cegada, não no hash do Destination. Veja a proposta 123 para detalhes.

### Expiração do LeaseSet

Para LeaseSets regulares, a expiração é o tempo da expiração mais recente de suas leases. Para as novas estruturas de dados LeaseSet2, a expiração é especificada no cabeçalho. Para LeaseSet2, a expiração deve corresponder à expiração mais recente de suas leases. Para EncryptedLeaseSet e MetaLeaseSet, a expiração pode variar, e a expiração máxima pode ser aplicada, a ser determinada.

### Armazenamento Persistente de LeaseSet

Não é necessário armazenamento persistente de dados do LeaseSet, já que eles expiram muito rapidamente. No entanto, o armazenamento persistente de dados do EncryptedLeaseSet e MetaLeaseSet com expirações longas pode ser aconselhável.

### Seleção de Chave de Criptografia (LS2)

LeaseSet2 pode conter múltiplas chaves de encriptação. As chaves estão em ordem de preferência do servidor, sendo a mais preferida a primeira. O comportamento padrão do cliente é selecionar a primeira chave com um tipo de encriptação suportado. Os clientes podem usar outros algoritmos de seleção baseados no suporte de encriptação, desempenho relativo e outros fatores.

---

## Inicialização

O netDb é descentralizado, no entanto você precisa de pelo menos uma referência a um peer para que o processo de integração o conecte. Isso é realizado através do "reseeding" do seu router com o RouterInfo de um peer ativo - especificamente, recuperando o arquivo `routerInfo-$hash.dat` dele e armazenando-o no seu diretório `netDb/`. Qualquer pessoa pode fornecer esses arquivos - você pode até mesmo fornecê-los a outros expondo seu próprio diretório netDb. Para simplificar o processo, voluntários publicam seus diretórios netDb (ou um subconjunto) na rede regular (não-i2p), e as URLs desses diretórios são codificadas no I2P. Quando o router inicia pela primeira vez, ele automaticamente busca de uma dessas URLs, selecionada aleatoriamente.

---

## Floodfill

O floodfill netDb é um mecanismo de armazenamento distribuído simples. O algoritmo de armazenamento é simples: enviar os dados para o peer mais próximo que se anunciou como um floodfill router. Quando o peer no floodfill netDb recebe um armazenamento netDb de um peer que não está no floodfill netDb, ele envia para um subconjunto dos floodfill netDb-peers. Os peers selecionados são aqueles mais próximos (de acordo com a [métrica XOR](#kademlia-closeness-metric)) de uma chave específica.

Determinar quem faz parte do floodfill netDb é trivial - isso é exposto no routerInfo publicado de cada router como uma capacidade.

Os floodfills não têm autoridade central e não formam um "consenso" - eles apenas implementam uma sobreposição DHT simples.

### Participação Voluntária em Floodfill Router

Ao contrário do Tor, onde os servidores de diretório são codificados e confiáveis, e operados por entidades conhecidas, os membros do conjunto de peers floodfill do I2P não precisam ser confiáveis e mudam ao longo do tempo.

Para aumentar a confiabilidade do netDb e minimizar o impacto do tráfego netDb em um router, o floodfill é automaticamente habilitado apenas em routers que estão configurados com limites de largura de banda altos. Routers com limites de largura de banda altos (que devem ser configurados manualmente, já que o padrão é muito menor) são presumidos como estando em conexões de menor latência e têm maior probabilidade de estarem disponíveis 24/7. A largura de banda mínima atual de compartilhamento para um router floodfill é 128 KBytes/sec.

Além disso, um router deve passar por vários testes adicionais de saúde (tempo da fila de mensagens de saída, atraso de trabalhos, etc.) antes que a operação floodfill seja habilitada automaticamente.

Com as regras atuais para ativação automática, aproximadamente 6% dos routers na rede são floodfill routers.

Enquanto alguns peers são configurados manualmente para serem floodfill, outros são simplesmente routers de alta largura de banda que se voluntariam automaticamente quando o número de peers floodfill cai abaixo de um limite. Isso previne qualquer dano de longo prazo à rede por perder a maioria ou todos os floodfills em um ataque. Por sua vez, esses peers deixarão de ser floodfill quando houver muitos floodfills ativos.

### Funções do Router Floodfill

Os únicos serviços de um floodfill router que são adicionais aos dos roteadores não-floodfill são aceitar armazenamentos netDb e responder a consultas netDb. Como geralmente têm alta largura de banda, é mais provável que participem de um grande número de túneis (ou seja, sejam um "relay" para outros), mas isso não está diretamente relacionado aos seus serviços de base de dados distribuída.

---

## Métrica de Proximidade Kademlia

O netDb usa uma métrica XOR simples no estilo Kademlia para determinar proximidade. Para criar uma chave Kademlia, o hash SHA256 da RouterIdentity ou Destination é computado. Uma exceção são os Encrypted LeaseSets (LS2), a partir da versão 0.9.38. O SHA256 do byte de tipo (3) seguido da chave pública ofuscada é usado para a chave DHT, e então rotacionado como usual.

Uma modificação neste algoritmo é feita para aumentar os custos de [ataques Sybil](#sybil-attack-partial-keyspace). Em vez do hash SHA256 da chave que está sendo procurada ou armazenada, o hash SHA256 é calculado da chave de busca binária de 32 bytes anexada com a data UTC representada como uma string ASCII de 8 bytes yyyyMMdd, ou seja, SHA256(key + yyyyMMdd). Isso é chamado de "chave de roteamento", e ela muda todos os dias à meia-noite UTC. Apenas a chave de busca é modificada desta forma, não os hashes dos roteadores floodfill. A transformação diária do DHT às vezes é chamada de "rotação do keyspace", embora não seja estritamente uma rotação.

As chaves de roteamento nunca são enviadas pela rede em nenhuma mensagem I2NP, elas são usadas apenas localmente para determinação de distância.

---

## Segmentação da Base de Dados de Rede - Sub-Bases de Dados

Tradicionalmente, as DHT's no estilo Kademlia não se preocupam em preservar a não-linkabilidade das informações armazenadas em qualquer nó específico da DHT. Por exemplo, uma informação pode ser armazenada em um nó da DHT e então solicitada de volta desse nó incondicionalmente. Dentro do I2P e usando o netDb, esse não é o caso - informações armazenadas na DHT só podem ser compartilhadas sob certas circunstâncias conhecidas onde é "seguro" fazê-lo. Isso é para prevenir uma classe de ataques onde um ator malicioso pode tentar associar um tunnel de cliente com um router enviando um armazenamento para um tunnel de cliente, e então solicitando-o de volta diretamente do suposto "Host" do tunnel de cliente.

### Estrutura de Segmentação

Os routers I2P podem implementar defesas eficazes contra esta classe de ataques desde que algumas condições sejam atendidas. Uma implementação de base de dados de rede deve ser capaz de acompanhar se uma entrada da base de dados foi recebida através de um tunnel cliente ou diretamente. Se foi recebida através de um tunnel cliente, então deve também acompanhar através de qual tunnel cliente foi recebida, usando o destino local do cliente. Se a entrada foi recebida através de múltiplos tunnels cliente, então o netDb deve acompanhar todos os destinos onde a entrada foi observada. Deve também acompanhar se uma entrada foi recebida como resposta a uma consulta, ou como um armazenamento.

Tanto nas implementações Java quanto C++, isso é alcançado usando uma única netDb "Principal" para pesquisas diretas e operações floodfill primeiro. Esta netDb principal existe no contexto do router. Em seguida, cada cliente recebe sua própria versão da netDb, que é usada para capturar entradas de banco de dados enviadas para tunnels de cliente e responder a pesquisas enviadas através de tunnels de cliente. Chamamos essas de "Client Network Databases" ou "Sub-Databases" e elas existem no contexto do cliente. A netDb operada pelo cliente existe apenas durante o tempo de vida do cliente e contém apenas entradas que são comunicadas com os tunnels do cliente. Isso torna impossível que entradas enviadas através de tunnels de cliente se sobreponham com entradas enviadas diretamente para o router.

Além disso, cada netDb precisa ser capaz de lembrar se uma entrada de banco de dados foi recebida porque foi enviada para um dos nossos destinos, ou porque foi solicitada por nós como parte de uma consulta. Se uma entrada de banco de dados foi recebida como um armazenamento, ou seja, algum outro router a enviou para nós, então um netDb deve responder às solicitações da entrada quando outro router consultar a chave. No entanto, se foi recebida como uma resposta a uma consulta, então o netDb deve apenas responder a uma consulta pela entrada se a entrada já tivesse sido armazenada no mesmo destino. Um cliente nunca deve responder consultas com uma entrada do netDb principal, apenas seu próprio banco de dados de rede cliente.

Essas estratégias devem ser adotadas e usadas em combinação para que ambas sejam aplicadas. Em combinação, elas "Segmentam" o netDb e o protegem contra ataques.

---

## Mecânicas de Armazenamento, Verificação e Consulta

### Armazenamento de RouterInfo para Peers

[I2NP](/docs/specs/i2np/) DatabaseStoreMessages contendo o RouterInfo local são trocadas com pares como parte da inicialização de uma conexão de transporte [NTCP](/docs/specs/ntcp2/) ou [SSU](/docs/specs/ssu2/).

### Armazenamento de LeaseSet para Peers

[I2NP](/docs/specs/i2np/) DatabaseStoreMessages contendo o leaseSet local são periodicamente trocadas com peers ao agrupá-las em uma mensagem garlic junto com o tráfego normal do Destination relacionado. Isso permite que uma resposta inicial, e respostas posteriores, sejam enviadas para um Lease apropriado, sem exigir qualquer consulta de leaseSet, ou exigir que os Destinations comunicantes tenham publicado leaseSets.

### Seleção de Floodfill

A DatabaseStoreMessage deve ser enviada para o floodfill que está mais próximo da chave de roteamento atual para o RouterInfo ou LeaseSet que está sendo armazenado. Atualmente, o floodfill mais próximo é encontrado por uma busca na base de dados local. Mesmo que esse floodfill não seja realmente o mais próximo, ele irá inundá-lo "mais perto" enviando-o para vários outros floodfills. Isso fornece um alto grau de tolerância a falhas.

No Kademlia tradicional, um peer faria uma busca "find-closest" antes de inserir um item no DHT para o alvo mais próximo. Como a operação de verificação tenderá a descobrir floodfills mais próximos se estiverem presentes, um router melhorará rapidamente seu conhecimento da "vizinhança" DHT para o RouterInfo e LeaseSets que publica regularmente. Embora o I2NP não defina uma mensagem "find-closest", se se tornar necessário, um router pode simplesmente fazer uma busca iterativa por uma chave com o bit menos significativo invertido (ou seja, key ^ 0x01) até que não sejam recebidos peers mais próximos nas DatabaseSearchReplyMessages. Isso garante que o peer verdadeiramente mais próximo seja encontrado mesmo se um peer mais distante tivesse o item do netDb.

### Armazenamento de RouterInfo para Floodfills

Um router publica sua própria RouterInfo conectando-se diretamente a um router floodfill e enviando uma [I2NP](/docs/specs/i2np/) DatabaseStoreMessage com um Reply Token diferente de zero. A mensagem não é criptografada end-to-end com garlic encryption, pois esta é uma conexão direta, então não há routers intermediários (e não há necessidade de ocultar esses dados de qualquer forma). O router floodfill responde com uma [I2NP](/docs/specs/i2np/) DeliveryStatusMessage, com o Message ID definido para o valor do Reply Token.

Em algumas circunstâncias, um router também pode enviar a RouterInfo DatabaseStoreMessage através de um tunnel exploratório; por exemplo, devido a limites de conexão, incompatibilidade de conexão, ou um desejo de ocultar o IP real do floodfill. O floodfill pode não aceitar tal armazenamento em momentos de sobrecarga ou baseado em outros critérios; se deve-se declarar explicitamente ilegal o armazenamento não-direto de uma RouterInfo é um tópico para estudo futuro.

### Armazenamento de LeaseSet em Floodfills

O armazenamento de LeaseSets é muito mais sensível do que para RouterInfos, pois um router deve garantir que o LeaseSet não possa ser associado ao router.

Um router publica um leaseSet local enviando uma [I2NP](/docs/specs/i2np/) DatabaseStoreMessage com um Reply Token diferente de zero através de um túnel cliente de saída para esse Destination. A mensagem é criptografada garlic de ponta a ponta usando o Session Key Manager do Destination, para ocultar a mensagem do ponto final de saída do túnel. O router floodfill responde com uma [I2NP](/docs/specs/i2np/) DeliveryStatusMessage, com o Message ID definido para o valor do Reply Token. Esta mensagem é enviada de volta para um dos túneis de entrada do cliente.

### Flooding

Como qualquer router, um floodfill usa vários critérios para validar o LeaseSet ou RouterInfo antes de armazená-lo localmente. Esses critérios podem ser adaptativos e dependentes das condições atuais, incluindo carga atual, tamanho do netDb e outros fatores. Toda validação deve ser feita antes do flooding.

Depois que um router floodfill recebe uma DatabaseStoreMessage contendo um RouterInfo ou LeaseSet válido que é mais recente do que o anteriormente armazenado em sua NetDb local, ele o "inunda". Para inundar uma entrada da NetDb, ele procura vários (atualmente 3) routers floodfill mais próximos à chave de roteamento da entrada da NetDb. (A chave de roteamento é o Hash SHA256 da RouterIdentity ou Destination com a data (yyyyMMdd) anexada.) Ao inundar para aqueles mais próximos à chave, não mais próximos a si mesmo, o floodfill garante que o armazenamento chegue ao lugar certo, mesmo que o router armazenador não tivesse bom conhecimento da "vizinhança" DHT para a chave de roteamento.

O floodfill então se conecta diretamente a cada um desses peers e envia uma [I2NP](/docs/specs/i2np/) DatabaseStoreMessage com um Reply Token zero. A mensagem não é criptografada com garlic encryption de ponta a ponta, pois esta é uma conexão direta, então não há routers intermediários (e não há necessidade de ocultar esses dados de qualquer forma). Os outros routers não respondem ou re-transmitem, pois o Reply Token é zero.

Floodfills não devem fazer flood através de túneis; a DatabaseStoreMessage deve ser enviada através de uma conexão direta.

Floodfills nunca devem inundar um LeaseSet expirado ou um RouterInfo publicado há mais de uma hora.

### Consulta de RouterInfo e LeaseSet

O [I2NP](/docs/specs/i2np/) DatabaseLookupMessage é usado para solicitar uma entrada do netDb de um router floodfill. As consultas são enviadas através de um dos tunnels exploratórios de saída do router. As respostas são especificadas para retornar através de um dos tunnels exploratórios de entrada do router.

As consultas são geralmente enviadas para os dois roteadores floodfill "bons" (cuja conexão não falha) mais próximos da chave solicitada, em paralelo.

Se a chave for encontrada localmente pelo router floodfill, ele responde com uma [I2NP](/docs/specs/i2np/) DatabaseStoreMessage. Se a chave não for encontrada localmente pelo router floodfill, ele responde com uma [I2NP](/docs/specs/i2np/) DatabaseSearchReplyMessage contendo uma lista de outros routers floodfill próximos à chave.

As pesquisas de leaseSet são criptografadas com garlic encryption ponta a ponta a partir da versão 0.9.5. As pesquisas de RouterInfo não são criptografadas e, portanto, são vulneráveis ao monitoramento pelo endpoint de saída (OBEP) do túnel do cliente. Isso se deve ao custo da criptografia ElGamal. A criptografia de pesquisa de RouterInfo pode ser habilitada em uma versão futura.

A partir da versão 0.9.7, as respostas a uma consulta de LeaseSet (uma DatabaseStoreMessage ou DatabaseSearchReplyMessage) serão criptografadas incluindo a chave de sessão e tag na consulta. Isso oculta a resposta do gateway de entrada (IBGW) do tunnel de resposta. As respostas a consultas de RouterInfo serão criptografadas se habilitarmos a criptografia de consulta.

(Referência: [Hashing it out in Public](http://www-users.cs.umn.edu/~hopper/hashing_it_out.pdf) Seções 2.2-2.3 para termos abaixo em itálico)

Devido ao tamanho relativamente pequeno da rede e à redundância de flooding, as buscas são geralmente O(1) em vez de O(log n). Um router tem alta probabilidade de conhecer um router floodfill próximo o suficiente da chave para obter a resposta na primeira tentativa. Em versões anteriores à 0.8.9, os routers usavam uma redundância de busca de dois (ou seja, duas buscas eram realizadas em paralelo para peers diferentes), e nem roteamento *recursivo* nem *iterativo* para buscas foi implementado. As consultas eram enviadas através de *múltiplas rotas simultaneamente* para *reduzir a chance de falha na consulta*.

A partir da versão 0.8.9, *lookups iterativos* são implementados sem redundância de lookup. Este é um lookup mais eficiente e confiável que funcionará muito melhor quando nem todos os peers floodfill são conhecidos, e remove uma limitação séria ao crescimento da rede. À medida que a rede cresce e cada router conhece apenas um pequeno subconjunto dos peers floodfill, os lookups se tornarão O(log n). Mesmo se o peer não retornar referências mais próximas da chave, o lookup continua com o próximo peer mais próximo, para robustez adicional, e para prevenir que um floodfill malicioso crie um buraco negro em uma parte do espaço de chaves. Os lookups continuam até que um timeout total de lookup seja atingido, ou o número máximo de peers seja consultado.

*IDs de nó* são *verificáveis* pois usamos o hash do router diretamente tanto como ID do nó quanto como chave Kademlia. Respostas incorretas que não estão mais próximas da chave de busca são geralmente ignoradas. Dado o tamanho atual da rede, um router tem *conhecimento detalhado da vizinhança do espaço de IDs de destino*.

### Verificação de Armazenamento de RouterInfo

Nota: A verificação de RouterInfo está desabilitada desde a versão 0.9.7.1 para prevenir o ataque descrito no artigo [Practical Attacks Against the I2P Network](http://wwwcip.informatik.uni-erlangen.de/~spjsschl/i2p.pdf). Não está claro se a verificação pode ser redesenhada para ser feita com segurança.

Para verificar se um armazenamento foi bem-sucedido, um router simplesmente aguarda cerca de 10 segundos, depois envia uma consulta para outro router floodfill próximo à chave (mas não aquele para o qual o armazenamento foi enviado). As consultas são enviadas através de um dos tunnels exploratórios de saída do router. As consultas são criptografadas end-to-end com garlic encryption para prevenir espionagem pelo ponto final de saída (OBEP).

### Verificação de Armazenamento de LeaseSet

Para verificar se um armazenamento foi bem-sucedido, um router simplesmente espera cerca de 10 segundos, depois envia uma consulta para outro floodfill router próximo da chave (mas não aquele para o qual o armazenamento foi enviado). As consultas são enviadas por um dos tunnels de saída do cliente para o destino do LeaseSet que está sendo verificado. Para prevenir espionagem pelo OBEP do tunnel de saída, as consultas são criptografadas end-to-end com garlic encryption. As respostas são especificadas para retornar através de um dos tunnels de entrada do cliente.

A partir da versão 0.9.7, as respostas para consultas de RouterInfo e LeaseSet (uma DatabaseStoreMessage ou uma DatabaseSearchReplyMessage) serão criptografadas, para ocultar a resposta do gateway de entrada (IBGW) do tunnel de resposta.

### Exploração

*Exploration* é uma forma especial de lookup netdb, onde um router tenta conhecer novos routers. Ele faz isso enviando para um router floodfill uma [I2NP](/docs/specs/i2np/) DatabaseLookup Message, procurando por uma chave aleatória. Como essa lookup falhará, o floodfill normalmente responderia com uma [I2NP](/docs/specs/i2np/) DatabaseSearchReplyMessage contendo hashes de routers floodfill próximos à chave. Isso não seria útil, pois o router solicitante provavelmente já conhece esses floodfills, e seria impraticável adicionar todos os routers floodfill ao campo "don't include" da DatabaseLookup Message. Para uma consulta exploration, o router solicitante define uma flag especial na DatabaseLookup Message. O floodfill então responderá apenas com routers não-floodfill próximos à chave solicitada.

### Notas sobre Respostas de Consulta

A resposta a uma solicitação de busca é uma Database Store Message (em caso de sucesso) ou uma Database Search Reply Message (em caso de falha). A DSRM contém um campo de hash do router 'from' para indicar a origem da resposta; a DSM não contém. O campo 'from' da DSRM não é autenticado e pode ser falsificado ou inválido. Não há outras tags de resposta. Portanto, ao fazer múltiplas solicitações em paralelo, é difícil monitorar o desempenho dos vários roteadores floodfill.

---

## MultiHoming

Os destinos podem ser hospedados em múltiplos routers simultaneamente, usando as mesmas chaves privadas e públicas (tradicionalmente armazenadas em arquivos eepPriv.dat). Como ambas as instâncias publicarão periodicamente seus leaseSets assinados para os peers floodfill, o leaseSet mais recentemente publicado será retornado para um peer que solicitar uma consulta ao banco de dados. Como os leaseSets têm (no máximo) um tempo de vida de 10 minutos, caso uma instância específica falhe, a interrupção durará no máximo 10 minutos, e geralmente muito menos que isso. A função de multihoming foi verificada e está sendo utilizada por vários serviços na rede.

A partir da versão 0.9.38, os floodfills suportam uma nova estrutura Meta LeaseSet. Esta estrutura fornece uma estrutura semelhante a uma árvore no DHT, para referenciar outros LeaseSets. Usando Meta LeaseSets, um site pode implementar grandes serviços multihomed, onde vários Destinations diferentes são usados para fornecer um serviço comum. As entradas em um Meta LeaseSet são Destinations ou outros Meta LeaseSets, e podem ter expirações longas, até 18,2 horas. Usando esta facilidade, deve ser possível executar centenas ou milhares de Destinations hospedando um serviço comum. Veja a proposta 123 para detalhes.

---

## Análise de Ameaças

Também discutido na [página do modelo de ameaças](/docs/overview/threat-model/#floodfill).

Um usuário hostil pode tentar prejudicar a rede criando um ou mais roteadores floodfill e configurando-os para oferecer respostas ruins, lentas ou nenhuma resposta. Alguns cenários são discutidos abaixo.

### Mitigação Geral Através do Crescimento

Atualmente existem cerca de 1700 routers floodfill na rede. A maioria dos seguintes ataques se tornará mais difícil, ou terá menos impacto, conforme o tamanho da rede e o número de routers floodfill aumentarem.

### Mitigação Geral Através de Redundância

Via flooding, todas as entradas do netDb são armazenadas nos 3 roteadores floodfill mais próximos à chave.

### Falsificações

Todas as entradas do netDb são assinadas pelos seus criadores, portanto nenhum router pode falsificar um RouterInfo ou LeaseSet.

### Lento ou Sem Resposta

Cada router mantém um conjunto expandido de estatísticas no [perfil de peer](/docs/overview/peer-selection/) para cada router floodfill, cobrindo várias métricas de qualidade para esse peer. O conjunto inclui:

- Tempo médio de resposta
- Percentagem de consultas respondidas com os dados solicitados
- Percentagem de armazenamentos que foram verificados com sucesso
- Último armazenamento bem-sucedido
- Última consulta bem-sucedida
- Última resposta

Cada vez que um router precisa determinar qual floodfill router está mais próximo de uma chave, ele usa essas métricas para determinar quais floodfill routers são "bons". Os métodos e limites usados para determinar a "qualidade" são relativamente novos e estão sujeitos a análises e melhorias adicionais. Embora um router completamente não responsivo seja rapidamente identificado e evitado, routers que são apenas ocasionalmente maliciosos podem ser muito mais difíceis de lidar.

### Ataque Sybil (Keyspace Completo)

Um atacante pode montar um [ataque Sybil](https://www.freehaven.net/anonbib/cache/sybil.pdf) criando um grande número de floodfill routers espalhados por todo o keyspace.

(Em um exemplo relacionado, um pesquisador recentemente criou um [grande número de relays Tor](http://blog.torproject.org/blog/june-2010-progress-report).) Se bem-sucedido, isso poderia ser um ataque de negação de serviço (DOS) efetivo em toda a rede.

Se os floodfills não estão se comportando mal o suficiente para serem marcados como "ruins" usando as métricas de perfil de peers descritas acima, este é um cenário difícil de lidar. A resposta do Tor pode ser muito mais ágil no caso de relays, já que os relays suspeitos podem ser removidos manualmente do consenso. Algumas possíveis respostas para a rede I2P estão listadas abaixo, porém nenhuma delas é completamente satisfatória:

- Compilar uma lista de hashes de router ou IPs ruins, e anunciar a lista através de vários meios (notícias do console, website, fórum, etc.); os usuários teriam que baixar manualmente a lista e adicioná-la à sua "blacklist" local.
- Pedir a todos na rede para habilitar floodfill manualmente (combater Sybil com mais Sybil)
- Lançar uma nova versão de software que inclui a lista "ruim" codificada diretamente
- Lançar uma nova versão de software que melhora as métricas e limites do perfil de peers, numa tentativa de identificar automaticamente os peers "ruins".
- Adicionar software que desqualifica floodfills se muitos deles estiverem em um único bloco de IP
- Implementar uma blacklist automática baseada em assinatura controlada por um único indivíduo ou grupo. Isso essencialmente implementaria uma parte do modelo de "consenso" do Tor. Infelizmente também daria a um único indivíduo ou grupo o poder de bloquear a participação de qualquer router ou IP específico na rede, ou mesmo de desligar ou destruir completamente toda a rede.

Este ataque torna-se mais difícil à medida que o tamanho da rede aumenta.

### Ataque Sybil (Keyspace Parcial)

Um atacante pode montar um [ataque Sybil](https://www.freehaven.net/anonbib/cache/sybil.pdf) criando um pequeno número (8-15) de routers floodfill agrupados de forma próxima no keyspace, e distribuindo amplamente os RouterInfos desses routers. Então, todas as consultas e armazenamentos para uma chave nesse keyspace seriam direcionados para um dos routers do atacante. Se bem-sucedido, isso poderia ser um ataque DOS efetivo em um I2P Site específico, por exemplo.

Como o espaço de chaves é indexado pelo hash criptográfico (SHA256) da chave, um atacante deve usar um método de força bruta para gerar repetidamente hashes de router até ter o suficiente que estejam suficientemente próximos da chave. A quantidade de poder computacional necessária para isso, que depende do tamanho da rede, é desconhecida.

Como uma defesa parcial contra este ataque, o algoritmo usado para determinar a "proximidade" do Kademlia varia ao longo do tempo. Em vez de usar o Hash da chave (ou seja, H(k)) para determinar a proximidade, usamos o Hash da chave anexada com a string da data atual, ou seja, H(k + AAAAMMDD). Uma função chamada "gerador de chave de roteamento" faz isso, que transforma a chave original em uma "chave de roteamento". Em outras palavras, todo o espaço de chaves do netDb "rotaciona" todos os dias à meia-noite UTC. Qualquer ataque de espaço de chaves parcial teria que ser regenerado todos os dias, pois após a rotação, os routers atacantes não estariam mais próximos da chave alvo, ou uns dos outros.

Este ataque torna-se mais difícil à medida que o tamanho da rede cresce. No entanto, pesquisas recentes demonstram que a rotação do keyspace não é particularmente eficaz. Um atacante pode pré-computar numerosos hashes de router com antecedência, e apenas alguns routers são suficientes para "eclipsar" uma porção do keyspace dentro de meia hora após a rotação.

Uma consequência da rotação diária do espaço de chaves é que a base de dados de rede distribuída pode tornar-se não confiável por alguns minutos após a rotação -- as consultas falharão porque o novo router "mais próximo" ainda não recebeu um armazenamento. A extensão do problema e os métodos para mitigação (por exemplo, "transferências" de netDb à meia-noite) são um tópico para estudo futuro.

### Ataques de Bootstrap

Um atacante poderia tentar inicializar novos routers em uma rede isolada ou controlada pela maioria, assumindo o controle de um site de reseed, ou enganando os desenvolvedores para que adicionem seu site de reseed à lista codificada no router.

Várias defesas são possíveis, e a maioria delas está planejada:

- Não permitir fallback de HTTPS para HTTP para reseeding. Um atacante MITM poderia simplesmente bloquear HTTPS e então responder ao HTTP.
- Incluir dados de reseed no instalador

Defesas que são implementadas:

- Alterar a tarefa de reseed para buscar um subconjunto de RouterInfos de cada um de vários sites de reseed em vez de usar apenas um único site
- Criar um serviço de monitoramento de reseed fora da rede que verifica periodicamente os sites de reseed e confirma que os dados não estão desatualizados ou inconsistentes com outras visões da rede
- A partir da versão 0.9.14, os dados de reseed são agrupados em um arquivo zip assinado e a assinatura é verificada durante o download. Veja [a especificação su3](/docs/specs/updates/#su3) para detalhes.

### Captura de Consulta

Veja também [lookup](#routerinfo-and-leaseset-lookup) (Referência: [Hashing it out in Public](http://www-users.cs.umn.edu/~hopper/hashing_it_out.pdf) Seções 2.2-2.3 para os termos abaixo em itálico)

Similar a um ataque de bootstrap, um atacante usando um router floodfill poderia tentar "direcionar" peers para um subconjunto de routers controlados por ele ao retornar suas referências.

Isso é improvável de funcionar via exploração, porque a exploração é uma tarefa de baixa frequência. Os routers adquirem a maioria de suas referências de pares através da atividade normal de construção de tunnels. Os resultados de exploração são geralmente limitados a alguns hashes de router, e cada consulta de exploração é direcionada para um router floodfill aleatório.

A partir da versão 0.8.9, *pesquisas iterativas* são implementadas. Para referências de floodfill router retornadas em uma resposta DatabaseSearchReplyMessage [I2NP](/docs/specs/i2np/) a uma pesquisa, essas referências são seguidas se estiverem mais próximas (ou as próximas mais próximas) da chave de pesquisa. O router solicitante não confia que as referências estejam mais próximas da chave (ou seja, elas são *verificavelmente corretas*). A pesquisa também não para quando nenhuma chave mais próxima é encontrada, mas continua consultando o nó seguinte mais próximo, até que o timeout ou número máximo de consultas seja alcançado. Isso impede que um floodfill malicioso crie um buraco negro em parte do espaço de chaves. Além disso, a rotação diária do keyspace exige que um atacante regenere uma router info dentro da região do espaço de chaves desejada. Este design garante que o ataque de captura de consulta descrito em [Hashing it out in Public](http://www-users.cs.umn.edu/~hopper/hashing_it_out.pdf) seja muito mais difícil.

### Seleção de Relay Baseada em DHT

(Referência: [Hashing it out in Public](http://www-users.cs.umn.edu/~hopper/hashing_it_out.pdf) Seção 3)

Isso não tem muito a ver com floodfill, mas veja a [página de seleção de pares](/docs/overview/peer-selection/) para uma discussão sobre as vulnerabilidades da seleção de pares para tunnels.

### Vazamentos de Informação

(Referência: [In Search of an Anonymous and Secure Lookup](https://www.freehaven.net/anonbib/cache/ccs10-lookup.pdf) Seção 3)

Este artigo aborda fraquezas nas pesquisas DHT "Finger Table" usadas pelo Torsk e NISAN. À primeira vista, estas não parecem se aplicar ao I2P. Primeiro, o uso de DHT pelo Torsk e NISAN é significativamente diferente daquele no I2P. Segundo, as pesquisas de network database do I2P estão apenas vagamente correlacionadas aos processos de [seleção de peers](/docs/overview/peer-selection/) e [construção de tunnel](/docs/overview/tunnel-routing/); apenas peers conhecidos previamente são usados para tunnels. Além disso, a seleção de peers não está relacionada a qualquer noção de proximidade de chave DHT.

Parte disso pode ser mais interessante quando a rede I2P ficar muito maior. Atualmente, cada router conhece uma grande proporção da rede, então buscar uma Router Info específica no netDb não é um forte indicativo de uma intenção futura de usar esse router em um tunnel. Talvez quando a rede for 100 vezes maior, a busca possa ser mais correlativa. Claro, uma rede maior torna um ataque Sybil muito mais difícil.

No entanto, a questão geral do vazamento de informações da DHT no I2P precisa de mais investigação. Os routers floodfill estão em posição de observar consultas e reunir informações. Certamente, a um nível de *f* = 0,2 (20% de nós maliciosos, conforme especificado no artigo) esperamos que muitas das ameaças Sybil que descrevemos ([aqui](/docs/overview/threat-model/#sybil), [aqui](#sybil-attack-full-keyspace) e [aqui](#sybil-attack-partial-keyspace)) se tornem problemáticas por várias razões.

---

## Histórico

[Movido para a página de discussão do netdb](/docs/legacy/netdb/).

---

## Trabalho Futuro

Criptografia ponta a ponta de consultas e respostas adicionais do netDb.

Melhores métodos para rastrear respostas de consulta.
