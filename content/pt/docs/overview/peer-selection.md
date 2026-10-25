---
title: "Criação de Perfil e Seleção de Peers"
description: "Como os routers I2P perfilam e selecionam peers para construir túneis"
slug: "peer-selection"
aliases:
  - "/pt/how_peerselection"
  - "/pt/how_peerselection/"
lastUpdated: "2024-02"
accurateFor: "0.9.62"
---

## Nota

Esta página descreve a implementação Java I2P de criação de perfis e seleção de pares a partir de 2010. Embora ainda seja amplamente precisa, alguns detalhes podem não estar mais corretos. Continuamos a evoluir estratégias de banimento, bloqueio e seleção para lidar com ameaças, ataques e condições de rede mais recentes. A rede atual possui múltiplas implementações de router com várias versões. Outras implementações I2P podem ter estratégias de criação de perfis e seleção completamente diferentes, ou podem não usar criação de perfis de forma alguma.

## Visão Geral {#overview}

### Perfil de Peers {#profiling}

**Peer profiling** é o processo de coleta de dados baseado na performance **observada** de outros routers ou peers, e classificação desses peers em grupos. O profiling **não** usa nenhum dado de performance alegado publicado pelo próprio peer na [base de dados da rede](/docs/overview/network-database).

Os perfis são usados para dois propósitos:

1. Selecionando peers para retransmitir nosso tráfego, que é discutido abaixo
2. Escolhendo peers do conjunto de roteadores floodfill para usar no armazenamento e consultas da base de dados de rede,
   que é discutido na página da [base de dados de rede](/docs/overview/network-database)

### Seleção de Peers {#selection}

**Seleção de peers** é o processo de escolher quais routers na rede queremos que retransmitam nossas mensagens (quais peers vamos pedir para se juntarem aos nossos tunnels). Para realizar isso, mantemos controle de como cada peer se comporta (o "perfil" do peer) e usamos esses dados para estimar quão rápidos eles são, com que frequência conseguirão aceitar nossos pedidos, e se parecem estar sobrecarregados ou de outra forma incapazes de executar confivelmente o que concordam em fazer.

Ao contrário de algumas outras redes anônimas, no I2P, a largura de banda declarada não é confiável e é **apenas** usada para evitar aqueles peers que anunciam largura de banda muito baixa, insuficiente para roteamento de tunnels. Toda seleção de peers é feita através de profiling. Isso previne ataques simples baseados em peers que alegam alta largura de banda para capturar grandes números de tunnels. Também torna [ataques de temporização](/docs/overview/threat-model#timing) mais difíceis.

A seleção de peers é feita com bastante frequência, pois um router pode manter um grande número de túneis de cliente e exploratórios, e o tempo de vida de um tunnel é de apenas 10 minutos.

### Informações Adicionais {#further-info}

Para mais informações consulte o artigo [Peer Profiling and Selection in the I2P Anonymous Network](/pdf/I2P-PET-CON-2009.1.pdf) apresentado na [PET-CON 2009.1](http://web.archive.org/web/20100413184504/http://www.pet-con.org/index.php/PET_Convention_2009.1). Veja [abaixo](#notes) as notas sobre pequenas mudanças desde que o artigo foi publicado.

## Perfis {#profiles}

Cada peer tem um conjunto de pontos de dados coletados sobre eles, incluindo estatísticas sobre quanto tempo levam para responder a uma consulta da base de dados da rede, com que frequência seus túneis falham, e quantos novos peers eles conseguem nos apresentar, além de pontos de dados simples como quando ouvimos deles pela última vez ou quando ocorreu o último erro de comunicação.

Os perfis são bastante pequenos, alguns KB. Para controlar o uso de memória, o tempo de expiração do perfil diminui conforme o número de perfis aumenta. Os perfis são mantidos na memória até o desligamento do router, quando são escritos no disco. Na inicialização, os perfis são lidos para que o router não precise reinicializar todos os perfis, permitindo assim que um router se reintegre rapidamente à rede após a inicialização.

## Resumos de Peers {#summaries}

Embora os perfis em si possam ser considerados um resumo do desempenho de um peer, para permitir uma seleção eficaz de peers, dividimos cada resumo em quatro valores simples, representando a velocidade do peer, sua capacidade, quão bem integrado na rede ele está, e se está falhando.

### Velocidade {#speed}

O cálculo de velocidade simplesmente percorre o perfil e estima quanta quantidade de dados podemos enviar ou receber em um único tunnel através do peer em um minuto. Para esta estimativa, ele apenas observa o desempenho no minuto anterior.

### Capacidade {#capacity}

O cálculo de capacidade simplesmente percorre o perfil e estima quantos tunnels o peer concordaria em participar durante um determinado período de tempo. Para esta estimativa, analisa quantas solicitações de construção de tunnel o peer aceitou, rejeitou e descartou, e quantos dos tunnels acordados falharam posteriormente. Embora o cálculo seja ponderado por tempo para que a atividade recente conte mais que a atividade posterior, estatísticas de até 48 horas podem ser incluídas.

Reconhecer e evitar peers não confiáveis e inacessíveis é de importância crítica. Infelizmente, como a construção e teste de túneis requerem a participação de vários peers, é difícil identificar positivamente a causa de uma solicitação de construção descartada ou falha de teste. O router atribui uma probabilidade de falha a cada um dos peers e usa essa probabilidade no cálculo de capacidade. Descartes e falhas de teste têm peso muito maior que rejeições.

## Organização de Peers {#organization}

Como mencionado acima, analisamos minuciosamente o perfil de cada peer para chegar a alguns cálculos-chave e, com base neles, organizamos cada peer em três grupos - rápido, alta capacidade e padrão.

Os agrupamentos não são mutuamente exclusivos, nem são independentes:

- Um peer é considerado "alta capacidade" se seu cálculo de capacidade atender ou
  exceder a mediana de todos os peers.
- Um peer é considerado "rápido" se já for de "alta capacidade" e seu
  cálculo de velocidade atender ou exceder a mediana de todos os peers.
- Um peer é considerado "padrão" se não for de "alta capacidade"

### Limites do Tamanho do Grupo {#group-limits}

O tamanho dos grupos pode ser limitado.

- O grupo rápido é limitado a 30 peers.
  Se houvesse mais, apenas aqueles com a classificação de velocidade mais alta são colocados no grupo.
- O grupo de alta capacidade é limitado a 75 peers (incluindo o grupo rápido).
  Se houvesse mais, apenas aqueles com a classificação de capacidade mais alta são colocados no grupo.
- O grupo padrão não tem limite fixo, mas é um pouco menor que o número de RouterInfos
  armazenados na base de dados de rede local.
  Em um router ativo na rede atual, pode haver cerca de 1000 RouterInfos e 500 perfis de peer
  (incluindo aqueles nos grupos rápido e de alta capacidade).

## Recálculo e Estabilidade {#recalculation}

Os resumos são recalculados e os peers são reorganizados em grupos a cada 45 segundos.

Os grupos tendem a ser bastante estáveis, ou seja, não há muito "turnover" nas classificações a cada recálculo. Os peers nos grupos de alta velocidade e alta capacidade recebem mais túneis construídos através deles, o que aumenta suas classificações de velocidade e capacidade, reforçando sua presença no grupo.

## Seleção de Peers {#peer-selection}

O router seleciona peers dos grupos acima para construir tunnels através deles.

### Seleção de Pares para Tunnels de Cliente {#client-tunnels}

Os tunnels de cliente são usados para tráfego de aplicações, como para proxies HTTP e servidores web.

Para reduzir a suscetibilidade a [alguns ataques](http://blog.torproject.org/blog/one-cell-enough) e aumentar o desempenho, os peers para construção de tunnels de cliente são escolhidos aleatoriamente do menor grupo, que é o grupo "rápido". Não há tendência para selecionar peers que foram previamente participantes em um tunnel para o mesmo cliente.

### Seleção de Peers para Tunnels Exploratórios {#exploratory-tunnels}

Os tunnels exploratórios são usados para fins administrativos do router, como tráfego da base de dados de rede e teste de tunnels de cliente. Os tunnels exploratórios também são usados para contactar routers anteriormente não conectados, razão pela qual são chamados de "exploratórios". Estes tunnels são geralmente de baixa largura de banda.

Os peers para construir tunnels exploratórios são geralmente escolhidos aleatoriamente do grupo padrão. Se a taxa de sucesso dessas tentativas de construção for baixa comparada à taxa de sucesso de construção de tunnels de cliente, o router selecionará uma média ponderada de peers aleatoriamente do grupo de alta capacidade. Isso ajuda a manter uma taxa de sucesso de construção satisfatória mesmo quando o desempenho da rede está ruim. Não há tendência para selecionar peers que foram anteriormente participantes em um tunnel exploratório.

Como o grupo padrão inclui um subconjunto muito grande de todos os peers que o router conhece, tunnels exploratórios são essencialmente construídos através de uma seleção aleatória de todos os peers, até que a taxa de sucesso de construção se torne muito baixa.

### Restrições {#restrictions}

Para prevenir alguns ataques simples e por questões de desempenho, existem as seguintes restrições:

- Dois peers do mesmo espaço IP /16 não podem estar no mesmo tunnel.
- Um peer pode participar em no máximo 33% de todos os tunnels criados pelo router.
- Peers com largura de banda extremamente baixa não são utilizados.
- Peers para os quais uma tentativa de conexão recente falhou não são utilizados.

### Ordenação de Peers em Tunnels {#ordering}

Os peers são ordenados dentro dos tunnels para lidar com o [ataque do predecessor](http://forensics.umass.edu/pubs/wright-tissec.pdf) ([atualização de 2008](http://forensics.umass.edu/pubs/wright.tissec.2008.pdf)). Mais informações estão na [página de tunnel](/docs/specs/tunnel-implementation#ordering).

## Trabalho Futuro {#future}

- Continuar a analisar e ajustar os cálculos de velocidade e capacidade conforme necessário
- Implementar uma estratégia de ejeção mais agressiva se necessário para controlar o uso de memória à medida que a rede cresce
- Avaliar os limites de tamanho do grupo
- Usar dados GeoIP para incluir ou excluir certos peers, se configurado

## Notas {#notes}

Para aqueles que estão lendo o artigo [Peer Profiling and Selection in the I2P Anonymous Network](/pdf/I2P-PET-CON-2009.1.pdf), por favor tenham em mente as seguintes pequenas mudanças no I2P desde a publicação do artigo:

- O cálculo de Integração ainda não é usado
- No artigo, "grupos" são chamados de "níveis"
- O nível "Com Falhas" não é mais usado
- O nível "Sem Falhas" agora é chamado de "Padrão"

## Referências {#references}

- [Peer Profiling and Selection in the I2P Anonymous Network](/pdf/I2P-PET-CON-2009.1.pdf)
- [One Cell Enough](http://blog.torproject.org/blog/one-cell-enough)
- [Tor Entry Guards](https://wiki.torproject.org/noreply/TheOnionRouter/TorFAQ#EntryGuards)
- [Murdoch 2007 Paper](http://freehaven.net/anonbib/#murdoch-pet2007)
- [Tune-up for Tor](http://www.crhc.uiuc.edu/~nikita/papers/tuneup-cr.pdf)
- [Low-resource Routing Attacks Against Tor](http://cs.gmu.edu/~mccoy/papers/wpes25-bauer.pdf)
