---
title: "Modelo de Ameaças do I2P"
description: "Análise dos ataques considerados no design do I2P e as mitigações implementadas"
slug: "threat-model"
aliases:
  - "/pt/how_threatmodel"
  - "/pt/how_threatmodel/"
lastUpdated: "2010-11"
accurateFor: "0.8.1"
---

## O Que Queremos Dizer com "Anônimo"?

O seu nível de anonimato pode ser descrito como "quão difícil é para alguém descobrir informações que você não quer que saibam" — quem você é, onde está localizado, com quem se comunica, ou até mesmo quando se comunica. Anonimato "perfeito" não é um conceito útil aqui — o software não o tornará indistinguível de pessoas que não usam computadores ou que não estão na Internet. Em vez disso, estamos trabalhando para fornecer anonimato suficiente para atender às necessidades reais de quem pudermos — desde aqueles que simplesmente navegam em sites, até aqueles que trocam dados, até aqueles que temem ser descobertos por organizações ou estados poderosos.

A questão de saber se o I2P fornece anonimato suficiente para suas necessidades específicas é difícil, mas esta página esperançosamente ajudará a responder essa questão explorando como o I2P opera sob vários ataques para que você possa decidir se atende às suas necessidades.

Acolhemos mais pesquisa e análise sobre a resistência do I2P às ameaças descritas abaixo. É necessária mais revisão da literatura existente (grande parte focada no Tor) e trabalho original focado no I2P.

---

## Resumo da Topologia da Rede

O I2P baseia-se nas ideias de muitos [outros](/docs/overview/comparison/) sistemas, mas alguns pontos-chave devem ser mantidos em mente ao revisar a literatura relacionada:

- **I2P é uma mixnet de rota livre** — o criador da mensagem define explicitamente o caminho que as mensagens serão enviadas (o tunnel de saída), e o destinatário da mensagem define explicitamente o caminho que as mensagens serão recebidas (o tunnel de entrada).
- **I2P não possui pontos oficiais de entrada e saída** — todos os pares participam totalmente da mistura, e não há proxies de entrada ou saída na camada de rede (no entanto, na camada de aplicação, alguns proxies existem).
- **I2P é totalmente distribuído** — não há controles centrais ou autoridades. Alguém poderia modificar alguns routers para operar cascatas de mistura (construindo tunnels e fornecendo as chaves necessárias para controlar o encaminhamento no ponto final do tunnel) ou perfil baseado em diretório e seleção, tudo sem quebrar a compatibilidade com o resto da rede, mas fazer isso obviamente não é necessário (e pode até prejudicar o anonimato).

Temos planos documentados para implementar atrasos não triviais e estratégias de agrupamento cuja existência é conhecida apenas pelo hop específico ou gateway do tunnel que recebe a mensagem, permitindo que uma mixnet de baixa latência forneça tráfego de cobertura para comunicação de alta latência (por exemplo, email). No entanto, estamos cientes de que atrasos significativos são necessários para fornecer proteção significativa, e que a implementação de tais atrasos será um desafio considerável. Não está claro neste momento se realmente implementaremos essas funcionalidades de atraso.

Em teoria, os routers ao longo do caminho da mensagem podem injetar um número arbitrário de saltos antes de encaminhar a mensagem para o próximo peer, embora a implementação atual não o faça.

---

## O Modelo de Ameaças

O design do I2P começou em 2003, pouco depois do advento do [Onion Routing](http://www.onion-router.net), [Freenet](http://freenetproject.org/), e [Tor](https://www.torproject.org/). Nosso design se beneficia substancialmente da pesquisa publicada naquela época. O I2P usa várias técnicas de onion routing (roteamento cebola), então continuamos a nos beneficiar do significativo interesse acadêmico no Tor.

Com base nos ataques e análises apresentados na [literatura sobre anonimato](http://freehaven.net/anonbib/topic.html) (principalmente [Traffic Analysis: Protocols, Attacks, Design Issues and Open Problems](http://citeseer.ist.psu.edu/454354.html)), o seguinte descreve brevemente uma ampla variedade de ataques, bem como muitas das defesas do I2P. Atualizamos esta lista para incluir novos ataques conforme são identificados.

Incluídos estão alguns ataques que podem ser únicos ao I2P. Não temos boas respostas para todos esses ataques, porém continuamos fazendo pesquisa e melhorando nossas defesas.

Além disso, muitos desses ataques são significativamente mais fáceis do que deveriam ser, devido ao tamanho modesto da rede atual. Embora estejamos cientes de algumas limitações que precisam ser abordadas, o I2P foi projetado para suportar centenas de milhares, ou milhões, de participantes. Conforme continuamos a divulgar e expandir a rede, esses ataques se tornarão muito mais difíceis.

As páginas de [comparações de rede](/docs/overview/comparison/) e [terminologia "garlic"](/docs/overview/garlic-routing/) também podem ser úteis para revisar.

### Ataques de Força Bruta

Um ataque de força bruta pode ser montado por um adversário passivo ou ativo global, observando todas as mensagens que passam entre todos os nós e tentando correlacionar qual mensagem segue qual caminho. Montar esse ataque contra o I2P deve ser não trivial, pois todos os peers na rede estão frequentemente enviando mensagens (tanto de ponta a ponta quanto mensagens de manutenção da rede), além de uma mensagem de ponta a ponta mudar de tamanho e dados ao longo de seu caminho. Além disso, o adversário externo não tem acesso às mensagens também, pois a comunicação entre routers é tanto criptografada quanto transmitida em fluxo (tornando duas mensagens de 1024 bytes indistinguíveis de uma mensagem de 2048 bytes).

No entanto, um atacante poderoso pode usar força bruta para detectar tendências — se eles conseguirem enviar 5GB para um destino I2P e monitorar a conexão de rede de todos, podem eliminar todos os pares que não receberam 5GB de dados. Técnicas para derrotar esse ataque existem, mas podem ser proibitivamente caras (veja: os mímicos do [Tarzan](http://citeseer.ist.psu.edu/freedman02tarzan.html) ou tráfego de taxa constante). A maioria dos usuários não se preocupa com esse ataque, pois o custo de executá-lo é extremo (e frequentemente requer atividade ilegal). No entanto, o ataque ainda é possível, por exemplo por um observador em um grande provedor de internet ou em um ponto de troca de internet. Aqueles que querem se defender contra isso devem tomar contramedidas apropriadas, como definir limites baixos de largura de banda, e usar leasesets não publicados ou criptografados para Sites I2P. Outras contramedidas, como atrasos não triviais e rotas restritas, não estão implementadas atualmente.

Como defesa parcial contra um único router ou grupo de routers tentando rotear todo o tráfego da rede, os routers contêm limites quanto a quantos túneis podem ser roteados através de um único peer. À medida que a rede cresce, esses limites estão sujeitos a ajustes adicionais. Outros mecanismos para classificação, seleção e prevenção de peers são discutidos na página de seleção de peers.

### Ataques de Temporização

As mensagens do I2P são unidirecionais e não implicam necessariamente que uma resposta será enviada. No entanto, aplicações em cima do I2P muito provavelmente terão padrões reconhecíveis na frequência de suas mensagens — por exemplo, uma requisição HTTP será uma mensagem pequena com uma grande sequência de mensagens de resposta contendo a resposta HTTP. Usando esses dados bem como uma visão ampla da topologia da rede, um atacante pode ser capaz de desqualificar alguns links por serem muito lentos para ter transmitido a mensagem.

Este tipo de ataque é poderoso, mas sua aplicabilidade ao I2P não é óbvia, já que a variação nos atrasos das mensagens devido ao enfileiramento, processamento de mensagens e limitação de taxa frequentemente atenderá ou excederá o tempo de passagem de uma mensagem ao longo de um único link — mesmo quando o atacante sabe que uma resposta será enviada assim que a mensagem for recebida. Há alguns cenários que irão expor respostas bastante automáticas, no entanto — a biblioteca de streaming faz isso (com o SYN+ACK) assim como o modo de mensagem de entrega garantida (com o DataMessage+DeliveryStatusMessage).

Sem limpeza de protocolo ou latência mais alta, adversários ativos globais podem obter informações substanciais. Como tal, pessoas preocupadas com esses ataques poderiam aumentar a latência (usando atrasos não triviais ou estratégias de agrupamento), incluir limpeza de protocolo, ou outras técnicas avançadas de roteamento de tunnel, mas estas não estão implementadas no I2P.

Referências: [Low-Resource Routing Attacks Against Anonymous Systems](http://www.cs.colorado.edu/department/publications/reports/docs/CU-CS-1025-07.pdf)

### Ataques de Interseção

Ataques de interseção contra sistemas de baixa latência são extremamente poderosos — fazem contato periódico com o alvo e mantêm registro de quais peers estão na rede. Com o tempo, conforme ocorre a rotatividade de nós, o atacante obterá informações significativas sobre o alvo simplesmente intersectando os conjuntos de peers que estão online quando uma mensagem passa com sucesso. O custo deste ataque é significativo conforme a rede cresce, mas pode ser viável em alguns cenários.

Em resumo, se um atacante estiver em ambas as extremidades do seu tunnel ao mesmo tempo, ele pode ser bem-sucedido. O I2P não possui uma defesa completa contra isso para comunicação de baixa latência. Esta é uma fraqueza inerente do roteamento onion de baixa latência. O Tor fornece um [aviso similar](https://trac.torproject.org/projects/tor/wiki/TheOnionRouter/TorFAQ#Whatattacksremainagainstonionrouting).

Defesas parciais implementadas no I2P:

- [Ordenação rigorosa](/docs/specs/tunnel-implementation/#ordering) de peers
- Criação de perfil e seleção de peers a partir de um pequeno grupo que muda lentamente
- Limites no número de tunnels roteados através de um único peer
- Prevenção de peers da mesma faixa IP /16 de serem membros de um único tunnel
- Para Sites I2P ou outros serviços hospedados, suportamos hospedagem simultânea em múltiplos routers, ou multihoming

Mesmo em conjunto, essas defesas não são uma solução completa. Além disso, fizemos algumas escolhas de design que podem aumentar significativamente nossa vulnerabilidade:

- Não usamos "guard nodes" de baixa largura de banda
- Usamos pools de tunnel compostos por vários tunnels, e o tráfego pode mudar de tunnel para tunnel.
- Tunnels não têm longa duração; novos tunnels são construídos a cada 10 minutos.
- Os comprimentos dos tunnels são configuráveis. Embora tunnels de 3 saltos sejam recomendados para proteção total, várias aplicações e serviços usam tunnels de 2 saltos por padrão.

No futuro, poderia ser possível para peers que podem suportar atrasos significativos (por atrasos não triviais e estratégias de batching). Além disso, isso só é relevante para destinos que outras pessoas conhecem — um grupo privado cujo destino é conhecido apenas por peers confiáveis não precisa se preocupar, pois um adversário não pode fazer "ping" neles para montar o ataque.

Referência: [One Cell Enough](http://blog.torproject.org/blog/one-cell-enough)

### Ataques de Negação de Serviço

Há uma grande variedade de ataques de negação de serviço disponíveis contra I2P, cada um com diferentes custos e consequências:

**Ataque de usuário ganancioso:** Isso é simplesmente pessoas tentando consumir significativamente mais recursos do que estão dispostas a contribuir. A defesa contra isso é:

- Definir padrões para que a maioria dos usuários forneça recursos para a rede. No I2P, os usuários roteiam tráfego por padrão. Em nítido contraste com [outras redes](/docs/overview/comparison/), mais de 95% dos usuários do I2P retransmitem tráfego para outros.
- Fornecer opções de configuração fáceis para que os usuários possam aumentar sua contribuição (percentual de compartilhamento) para a rede. Exibir métricas fáceis de entender, como "taxa de compartilhamento", para que os usuários possam ver o que estão contribuindo.
- Manter uma comunidade forte com blogs, fóruns, IRC e outros meios de comunicação.

**Ataque de privação:** Um usuário hostil pode tentar prejudicar a rede criando um número significativo de peers na rede que não são identificados como estando sob controle da mesma entidade (como no caso do Sybil). Esses nós então decidem não fornecer recursos para a rede, fazendo com que os peers existentes tenham que procurar através de uma base de dados de rede maior ou solicitar mais tunnels do que deveria ser necessário. Alternativamente, os nós podem fornecer serviço intermitente, periodicamente descartando tráfego selecionado ou recusando conexões para determinados peers. Este comportamento pode ser indistinguível do de um nó sobrecarregado ou falhando. O I2P aborda essas questões mantendo perfis dos peers, tentando identificar aqueles com baixo desempenho e simplesmente os ignorando, ou os usando raramente. Melhoramos significativamente a capacidade de reconhecer e evitar peers problemáticos; no entanto, ainda são necessários esforços significativos nesta área.

**Ataque de flooding:** Um usuário hostil pode tentar fazer flooding da rede, de um peer, de um destino ou de um tunnel. O flooding de rede e peer é possível, e o I2P não faz nada para prevenir flooding padrão da camada IP. O flooding de um destino com mensagens enviando um grande número para os vários gateways de tunnel de entrada do alvo é possível, mas o destino saberá disso tanto pelo conteúdo da mensagem quanto porque os testes do tunnel irão falhar. O mesmo vale para fazer flooding de apenas um único tunnel. O I2P não tem defesas para um ataque de flooding de rede. Para um ataque de flooding de destino e tunnel, o alvo identifica quais tunnels não estão respondendo e constrói novos. Novo código também poderia ser escrito para adicionar ainda mais tunnels se o cliente desejar lidar com a carga maior. Se, por outro lado, a carga for mais do que o cliente pode lidar, eles podem instruir os tunnels a limitar o número de mensagens ou bytes que devem passar adiante (uma vez que a operação avançada de tunnel for implementada).

**Ataque de carga de CPU:** Atualmente existem alguns métodos para que pessoas solicitem remotamente que um peer execute alguma operação criptograficamente cara, e um atacante hostil poderia usar isso para inundar esse peer com um grande número dessas operações numa tentativa de sobrecarregar a CPU. Tanto o uso de boas práticas de engenharia quanto potencialmente exigir certificados não triviais (por exemplo, HashCash) anexados a essas solicitações caras devem mitigar o problema, embora possa haver espaço para um atacante explorar vários bugs na implementação.

**Ataque DOS floodfill:** Um usuário hostil pode tentar prejudicar a rede ao se tornar um router floodfill. As defesas atuais contra routers floodfill não confiáveis, intermitentes ou maliciosos são fracas. Um router floodfill pode fornecer respostas ruins ou nenhuma resposta às consultas, e também pode interferir na comunicação entre floodfills. Algumas defesas e criação de perfis de pares estão implementadas, no entanto há muito mais a ser feito. Para mais informações, consulte a [página da base de dados da rede](/docs/specs/common-structures/).

### Ataques de Marcação

Ataques de marcação — modificar uma mensagem para que possa ser identificada posteriormente ao longo do caminho — são por si só impossíveis no I2P, pois as mensagens passadas através de tunnels são assinadas. No entanto, se um atacante é o gateway do tunnel de entrada, bem como um participante mais adiante nesse tunnel, com conluio eles podem identificar o fato de que estão no mesmo tunnel (e antes da adição de hop ids únicos e outras atualizações, pares em conluio dentro do mesmo tunnel podem reconhecer esse fato sem qualquer esforço). Um atacante em um tunnel de saída e qualquer parte de um tunnel de entrada não podem conspirar, no entanto, pois a criptografia do tunnel preenche e modifica os dados separadamente para os tunnels de entrada e saída. Atacantes externos não podem fazer nada, pois os links são criptografados e as mensagens assinadas.

### Ataques de Particionamento

Ataques de particionamento — encontrar maneiras de segregar (técnica ou analiticamente) os peers numa rede — são importantes de se ter em mente ao lidar com um adversário poderoso, já que o tamanho da rede desempenha um papel fundamental na determinação do seu anonimato. O particionamento técnico através do corte de ligações entre peers para criar redes fragmentadas é abordado pela base de dados de rede integrada do I2P, que mantém estatísticas sobre vários peers de modo a permitir que quaisquer conexões existentes para outras seções fragmentadas sejam exploradas para curar a rede. No entanto, se o atacante desconectar todas as ligações para peers não controlados, essencialmente isolando o alvo, nenhuma quantidade de cura da base de dados de rede irá corrigi-lo. Nesse ponto, a única coisa que o router pode esperar fazer é notar que um número significativo de peers anteriormente confiáveis ficaram indisponíveis e alertar o cliente de que está temporariamente desconectado (este código de detecção não está implementado no momento).

Particionar a rede analiticamente procurando por diferenças em como routers e destinos se comportam e agrupando-os de acordo também é um ataque muito poderoso. Por exemplo, um atacante [coletando](#harvesting-attacks) a base de dados da rede saberá quando um destino específico tem 5 túneis de entrada em seu leaseSet enquanto outros têm apenas 2 ou 3, permitindo ao adversário potencialmente particionar clientes pelo número de túneis selecionados. Outra partição é possível ao lidar com atrasos não triviais e estratégias de agrupamento, já que os gateways de túnel e os saltos específicos com atrasos diferentes de zero provavelmente se destacarão. No entanto, esses dados são expostos apenas àqueles saltos específicos, então para particionar efetivamente nesse aspecto, o atacante precisaria controlar uma porção significativa da rede (e ainda assim seria apenas uma partição probabilística, já que eles não saberiam quais outros túneis ou mensagens têm esses atrasos).

Também discutido na [página da base de dados de rede](/docs/specs/common-structures/) (ataque de bootstrap).

### Ataques de Predecessor

O ataque predecessor consiste em coletar estatísticas passivamente na tentativa de ver quais peers estão 'próximos' ao destino, participando em seus tunnels e rastreando o salto anterior ou seguinte (para tunnels de saída ou entrada, respectivamente). Com o tempo, usando uma amostra perfeitamente aleatória de peers e ordenação aleatória, um atacante seria capaz de ver qual peer aparece como 'mais próximo' estatisticamente mais do que os demais, e esse peer seria onde o alvo está localizado.

O I2P evita isso de quatro maneiras: primeiro, os peers selecionados para participar em tunnels não são amostrados aleatoriamente por toda a rede — eles são derivados do algoritmo de seleção de peers que os divide em camadas. Segundo, com [ordenação rigorosa](/docs/specs/tunnel-implementation/#ordering) de peers em um tunnel, o fato de um peer aparecer com mais frequência não significa que ele seja a origem. Terceiro, com comprimento de tunnel permutado (não habilitado por padrão), até mesmo tunnels de 0 saltos podem fornecer negação plausível, pois a variação ocasional do gateway parecerá com tunnels normais. Quarto, com rotas restritas (não implementadas), apenas o peer com uma conexão restrita ao alvo jamais contatará o alvo, enquanto atacantes apenas se depararão com esse gateway.

O método atual de construção de tunnel foi especificamente projetado para combater o ataque predecessor. Veja também [o ataque de interseção](#intersection-attacks).

Referências: [Wright et al. 2008](http://forensics.umass.edu/pubs/wright.tissec.2008.pdf), que é uma atualização do [artigo predecessor de ataque de 2004](http://forensics.umass.edu/pubs/wright-tissec.pdf).

### Ataques de Coleta

"Harvesting" significa compilar uma lista de usuários executando I2P. Pode ser usado para ataques legais e para auxiliar outros ataques simplesmente executando um peer, vendo a quem ele se conecta, e coletando quaisquer referências a outros peers que conseguir encontrar.

O próprio I2P não foi projetado com defesas eficazes contra este ataque, uma vez que existe a base de dados distribuída da rede contendo exatamente esta informação. Os seguintes fatores tornam o ataque um pouco mais difícil na prática:

- O crescimento da rede tornará mais difícil obter uma determinada proporção da rede
- Routers floodfill implementam limites de consulta como proteção contra DOS
- O "modo oculto", que impede um router de publicar suas informações no netDb, (mas também o impede de retransmitir dados) não é amplamente usado agora, mas poderia ser.

Em implementações futuras, rotas restritas básicas e abrangentes reduziriam o poder deste ataque, pois os pares "ocultos" não publicam seus endereços de contato na base de dados da rede — apenas os túneis através dos quais podem ser alcançados (bem como suas chaves públicas, etc).

No futuro, os routers poderiam usar GeoIP para identificar se estão em um país específico onde a identificação como um nó I2P seria arriscada. Nesse caso, o router poderia automaticamente habilitar o modo oculto, ou implementar outros métodos de roteamento restritivos.

### Identificação Através de Análise de Tráfego

Ao inspecionar o tráfego de entrada e saída de um router, um ISP malicioso ou firewall de nível estatal poderia identificar que um computador está executando I2P. Como discutido [acima](#harvesting-attacks), o I2P não foi especificamente projetado para ocultar que um computador está executando I2P. No entanto, várias decisões de design tomadas no projeto da camada de transporte e protocolos tornam um tanto difícil identificar o tráfego I2P:

- Seleção aleatória de porta
- Criptografia Ponto-a-Ponto de todo o tráfego
- Troca de chaves DH sem bytes de protocolo ou outros campos constantes não criptografados
- Uso simultâneo de transportes TCP e UDP. UDP pode ser muito mais difícil para alguns equipamentos de Inspeção Profunda de Pacotes (DPI) rastrearem.

No futuro próximo, planejamos abordar diretamente as questões de análise de tráfego através de maior ofuscação dos protocolos de transporte I2P, possivelmente incluindo:

- Padding na camada de transporte para comprimentos aleatórios, especialmente durante o handshake de conexão
- Estudo das assinaturas de distribuição de tamanho de pacotes e padding adicional conforme necessário
- Desenvolvimento de métodos de transporte adicionais que imitam SSL ou outros protocolos comuns
- Revisão das estratégias de padding em camadas superiores para ver como afetam os tamanhos de pacotes na camada de transporte
- Revisão dos métodos implementados por vários firewalls de nível estatal para bloquear Tor
- Trabalho direto com especialistas em DPI e ofuscação

Referência: [Breaking and Improving Protocol Obfuscation](http://www.iis.se/docs/hjelmvik_breaking.pdf)

### Ataques Sybil

Sybil descreve uma categoria de ataques onde o adversário cria números arbitrariamente grandes de nodes coludindo e usa o aumento de números para ajudar a montar outros ataques. Por exemplo, se um atacante está em uma rede onde peers são selecionados aleatoriamente e eles querem 80% de chance de ser um desses peers, eles simplesmente criam cinco vezes o número de nodes que estão na rede e jogam os dados. Quando identidade é gratuita, Sybil pode ser uma técnica muito potente para um adversário poderoso. A técnica principal para lidar com isso é simplesmente tornar a identidade 'não gratuita' — [Tarzan](http://www.pdos.lcs.mit.edu/tarzan/) (entre outros) usa o fato de que endereços IP são limitados, enquanto IIP usou [HashCash](http://www.hashcash.org/) para 'cobrar' pela criação de uma nova identidade. Atualmente não implementamos nenhuma técnica particular para lidar com Sybil, mas incluímos certificados placeholder nas estruturas de dados do router e do destino que podem conter um certificado HashCash de valor apropriado quando necessário (ou algum outro certificado provando escassez).

Exigir Certificados HashCash em vários locais tem dois problemas principais:

- Manter compatibilidade com versões anteriores
- O problema clássico do HashCash — selecionar valores HashCash que sejam provas de trabalho significativas em máquinas de alta performance, enquanto ainda sejam viáveis em máquinas de baixa performance como dispositivos móveis.

Várias limitações no número de routers em um determinado intervalo de IP restringem a vulnerabilidade a atacantes que não têm a capacidade de colocar máquinas em vários blocos de IP. No entanto, esta não é uma defesa significativa contra um adversário poderoso.

Consulte a [página da base de dados da rede](/docs/specs/common-structures/) para mais discussão sobre Sybil.

### Ataques de Esgotamento de Buddy

(Referência: [In Search of an Anonymous and Secure Lookup](http://www.eecs.berkeley.edu/~pmittal/publications/nisan-torsk-ccs10.pdf) Seção 5.2)

Ao recusar aceitar ou encaminhar solicitações de construção de tunnel, exceto para um peer cúmplice, um router poderia garantir que um tunnel seja formado inteiramente a partir de seu conjunto de routers cúmplices. As chances de sucesso são aumentadas se houver um grande número de routers cúmplices, ou seja, um [ataque Sybil](#sybil-attacks). Isso é parcialmente mitigado por nossos métodos de criação de perfis de peers usados para monitorar o desempenho dos peers. No entanto, este é um ataque poderoso conforme o número de routers se aproxima de *f* = 0,2, ou 20% de nós maliciosos, conforme especificado no artigo. Os routers maliciosos também poderiam manter conexões com o router alvo e fornecer excelente largura de banda de encaminhamento para tráfego através dessas conexões, numa tentativa de manipular os perfis gerenciados pelo alvo e parecer atraentes. Pesquisas adicionais e defesas podem ser necessárias.

### Ataques Criptográficos

Utilizamos criptografia forte com chaves longas e assumimos a segurança das primitivas criptográficas padrão da indústria usadas no I2P. Os recursos de segurança incluem a detecção imediata de mensagens alteradas ao longo do caminho, a incapacidade de descriptografar mensagens não endereçadas a você e defesa contra ataques man-in-the-middle. Os tamanhos de chave escolhidos em 2003 eram bastante conservadores na época e ainda são mais longos que aqueles usados em [outras redes de anonimato](https://torproject.org/). Não achamos que os comprimentos de chave atuais sejam nossa maior fraqueza, especialmente para adversários tradicionais, não estatais; bugs e o pequeno tamanho da rede são muito mais preocupantes. É claro que todos os algoritmos criptográficos eventualmente se tornam obsoletos devido ao advento de processadores mais rápidos, pesquisa criptográfica e avanços em métodos como rainbow tables, clusters de hardware de videogame, etc. Infelizmente, o I2P não foi projetado com mecanismos fáceis para aumentar chaves ou alterar valores de segredo compartilhado mantendo compatibilidade com versões anteriores.

A atualização das várias estruturas de dados e protocolos para suportar chaves mais longas terá que ser enfrentada eventualmente, e esta será uma tarefa importante, assim como será para [outros](https://torproject.org/). Esperançosamente, através de planejamento cuidadoso, podemos minimizar a interrupção e implementar mecanismos para facilitar futuras transições.

No futuro, vários protocolos I2P e estruturas de dados suportarão o preenchimento seguro de mensagens para tamanhos arbitrários, para que as mensagens possam ter tamanho constante ou as garlic messages possam ser modificadas aleatoriamente para que alguns cloves pareçam conter mais subcloves do que realmente contêm. No momento, entretanto, as garlic messages, tunnel e mensagens ponta a ponta incluem preenchimento aleatório simples.

### Ataques de Anonimato Floodfill

Além dos ataques DOS contra floodfill descritos [acima](#denial-of-service-attacks), os roteadores floodfill estão em uma posição única para aprender sobre os participantes da rede, devido ao seu papel no netDb e à alta frequência de comunicação com esses participantes. Isso é parcialmente mitigado porque os roteadores floodfill gerenciam apenas uma porção do keyspace total, e o keyspace roda diariamente, conforme explicado na [página da base de dados da rede](/docs/specs/common-structures/). Os mecanismos específicos pelos quais os roteadores se comunicam com floodfills foram cuidadosamente projetados. No entanto, essas ameaças devem ser estudadas mais profundamente. As ameaças potenciais específicas e as defesas correspondentes são um tópico para pesquisas futuras.

### Outros Ataques à Base de Dados da Rede

Um usuário hostil pode tentar prejudicar a rede criando um ou mais roteadores floodfill e configurando-os para oferecer respostas ruins, lentas ou nenhuma resposta. Vários cenários são discutidos na [página da base de dados da rede](/docs/specs/common-structures/).

### Ataques a Recursos Centrais

Existem alguns recursos centralizados ou limitados (alguns dentro do I2P, outros não) que podem ser atacados ou usados como vetor para ataques. A ausência de jrandom a partir de novembro de 2007, seguida pela perda do serviço de hospedagem i2p.net em janeiro de 2008, destacou numerosos recursos centralizados no desenvolvimento e operação da rede I2P, a maioria dos quais agora está distribuída. Ataques a recursos acessíveis externamente afetam principalmente a capacidade de novos usuários nos encontrarem, não a operação da rede em si.

- O site é espelhado e usa DNS round-robin para acesso público externo.
- Os routers agora suportam [múltiplas localizações externas de reseed](/docs/overview/faq/#reseed), no entanto mais hosts de reseed podem ser necessários, e o manuseio de hosts de reseed não confiáveis ou maliciosos pode precisar de melhorias.
- Os routers agora suportam múltiplas localizações de arquivos de atualização. Um host de atualização malicioso poderia fornecer um arquivo enorme; é necessário limitar o tamanho.
- Os routers agora suportam múltiplos assinantes confiáveis de atualização padrão.
- Os routers agora lidam melhor com múltiplos peers floodfill não confiáveis. floodfills maliciosos precisam de mais estudo.
- O código agora é armazenado em um sistema de controle de fonte distribuído.
- Os routers dependem de um único host de notícias, mas há uma URL de backup codificada apontando para um host diferente. Um host de notícias malicioso poderia fornecer um arquivo enorme; é necessário limitar o tamanho.
- [Serviços do sistema de nomenclatura](/docs/overview/naming/), incluindo provedores de assinatura de catálogo de endereços, serviços de adição de hosts e serviços de salto, podem ser maliciosos. Proteções substanciais para assinaturas foram implementadas na versão 0.6.1.31, com melhorias adicionais nas versões subsequentes. No entanto, todos os serviços de nomenclatura exigem alguma medida de confiança; consulte [a página de nomenclatura](/docs/overview/naming/) para detalhes.
- Continuamos dependentes do serviço DNS para i2p2.de; perder isso causaria uma interrupção substancial em nossa capacidade de atrair novos usuários, e reduziria a rede (a curto e médio prazo), assim como a perda de i2p.net fez.

### Ataques de Desenvolvimento

Estes ataques não são diretamente contra a rede, mas sim direcionados à sua equipe de desenvolvimento, seja introduzindo obstáculos legais para qualquer pessoa que contribua com o desenvolvimento do software, ou usando qualquer meio disponível para fazer com que os desenvolvedores subvertam o software. Medidas técnicas tradicionais não podem derrotar estes ataques, e se alguém ameaçasse a vida ou o sustento de um desenvolvedor (ou mesmo apenas emitisse uma ordem judicial acompanhada de uma ordem de silêncio, sob ameaça de prisão), teríamos um grande problema.

No entanto, duas técnicas ajudam a defender contra esses ataques:

- Todos os componentes da rede devem ser de código aberto para permitir inspeção, verificação, modificação e melhoria. Se um desenvolvedor for comprometido, uma vez que isso seja percebido, a comunidade deve exigir explicações e deixar de aceitar o trabalho desse desenvolvedor. Todos os commits para nosso sistema de controle de código distribuído são assinados criptograficamente, e os empacotadores de versões usam um sistema de lista de confiança para restringir modificações apenas àquelas previamente aprovadas.
- Desenvolvimento através da própria rede, permitindo que os desenvolvedores permaneçam anônimos mas ainda assim protejam o processo de desenvolvimento. Todo desenvolvimento I2P pode ocorrer através do I2P — usando um sistema de controle de código distribuído, chat IRC, servidores web públicos, fóruns de discussão (forum.i2p), e os sites de distribuição de software, todos disponíveis dentro do I2P.

Também mantemos relacionamentos com várias organizações que oferecem aconselhamento jurídico, caso qualquer defesa seja necessária.

### Ataques de Implementação (Bugs)

Por mais que tentemos, a maioria das aplicações não triviais inclui erros no design ou implementação, e o I2P não é exceção. Pode haver bugs que poderiam ser explorados para atacar o anonimato ou segurança da comunicação executada sobre I2P de formas inesperadas. Para ajudar a resistir a ataques contra o design ou protocolos em uso, publicamos todos os designs e documentação e solicitamos revisão e críticas na esperança de que muitos olhos melhorem o sistema. Não acreditamos em segurança através da obscuridade.

Além disso, o código está sendo tratado da mesma forma, com pouca aversão a refazer ou descartar algo que não esteja atendendo às necessidades do sistema de software (incluindo a facilidade de modificação). A documentação para o design e implementação da rede e dos componentes de software é uma parte essencial da segurança, pois sem ela é improvável que os desenvolvedores estejam dispostos a gastar tempo para aprender o software o suficiente para identificar deficiências e bugs.

O nosso software provavelmente contém, em particular, bugs relacionados a negação de serviço através de erros de falta de memória (OOMs), problemas de cross-site-scripting (XSS) no console do router, e outras vulnerabilidades a entradas não padronizadas através dos vários protocolos.

O I2P ainda é uma rede pequena com uma pequena comunidade de desenvolvimento e quase nenhum interesse de grupos acadêmicos ou de pesquisa. Portanto, nos falta a análise que [outras redes de anonimato](https://torproject.org/) podem ter recebido. Continuamos a recrutar pessoas para [se envolver](/get-involved/) e ajudar.

---

## Outras Defesas

### Listas de Bloqueio

Até certo ponto, o I2P poderia ser aprimorado para evitar peers operando em endereços IP listados em uma lista de bloqueio. Várias listas de bloqueio estão comumente disponíveis em formatos padrão, listando organizações anti-P2P, potenciais adversários a nível estatal e outros.

Na medida em que peers ativos realmente aparecem na blocklist atual, bloquear apenas um subconjunto de peers tenderia a segmentar a rede, agravar problemas de alcançabilidade e diminuir a confiabilidade geral. Portanto, gostaríamos de concordar com uma blocklist específica e habilitá-la por padrão.

As listas de bloqueio são apenas uma parte (talvez uma pequena parte) de um conjunto de defesas contra malícia. Em grande parte, o sistema de criação de perfis faz um bom trabalho ao medir o comportamento do router para que não precisemos confiar em nada no netDb. No entanto, há mais que pode ser feito. Para cada uma das áreas na lista acima, há melhorias que podemos fazer na detecção de atividade maliciosa.

Se uma lista de bloqueio estiver hospedada em uma localização central com atualizações automáticas, a rede fica vulnerável a um [ataque de recurso central](#central-resource-attacks). A assinatura automática de uma lista dá ao provedor da lista o poder de desligar completamente a rede I2P.

Atualmente, uma blocklist padrão é distribuída com nosso software, listando apenas os IPs de fontes de DOS anteriores. Não há mecanismo de atualização automática. Caso uma faixa de IP específica implemente ataques sérios na rede I2P, teríamos que pedir às pessoas para atualizarem sua blocklist manualmente através de mecanismos fora da banda, como fóruns, blogs, etc.
