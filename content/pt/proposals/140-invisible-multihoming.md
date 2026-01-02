---
title: "Multihoming Invisível"
number: "140"
author: "str4d"
created: "2017-05-22"
lastupdated: "2017-07-04"
status: "Abrir"
thread: "http://zzz.i2p/topics/2335"
toc: true
---

## Visão Geral

Esta proposta descreve um design para um protocolo que permite a um cliente I2P, serviço ou processo balanceador externo gerenciar múltiplos routers de forma transparente hospedando um único [Destination](http://localhost:63465/docs/specs/common-structures/#destination).

A proposta atualmente não especifica uma implementação concreta. Poderia ser implementada como uma extensão para [I2CP](/docs/specs/i2cp/), ou como um novo protocolo.

## Motivação

Multihoming é onde múltiplos routers são utilizados para hospedar o mesmo Destination. A forma atual de fazer multihoming com I2P é executar o mesmo Destination em cada router independentemente; o router que é utilizado pelos clientes em qualquer momento específico é o último a publicar um leaseSet.

Isso é um hack e presumivelmente não funcionará para websites grandes em escala. Digamos que tivéssemos 100 routers de multihoming, cada um com 16 túneis. Isso são 1600 publicações de LeaseSet a cada 10 minutos, ou quase 3 por segundo. Os floodfills ficariam sobrecarregados e os limitadores entrariam em ação. E isso antes mesmo de mencionarmos o tráfego de consultas.

A Proposta 123 resolve este problema com um meta-LeaseSet, que lista os 100 hashes reais de LeaseSet. Uma consulta torna-se um processo de duas etapas: primeiro consultando o meta-LeaseSet, e depois um dos LeaseSets nomeados. Esta é uma boa solução para o problema de tráfego de consultas, mas por si só cria um vazamento significativo de privacidade: É possível determinar quais routers de multihoming estão online monitorando o meta-LeaseSet publicado, porque cada LeaseSet real corresponde a um único router.

Precisamos de uma forma para um cliente ou serviço I2P espalhar um único Destination por vários routers, de uma maneira que seja indistinguível de usar um único router (da perspectiva do próprio LeaseSet).

## Design

### Definitions

    User
        The person or organisation wanting to multihome their Destination(s). A
        single Destination is considered here without loss of generality (WLOG).

    Client
        The application or service running behind the Destination. It may be a
        client-side, server-side, or peer-to-peer application; we refer to it as
        a client in the sense that it connects to the I2P routers.

        The client consists of three parts, which may all be in the same process
        or may be split across processes or machines (in a multi-client setup):

        Balancer
            The part of the client that manages peer selection and tunnel
            building. There is a single balancer at any one time, and it
            communicates with all I2P routers. There may be failover balancers.

        Frontend
            The part of the client that can be operated in parallel. Each
            frontend communicates with a single I2P router.

        Backend
            The part of the client that is shared between all frontends. It has
            no direct communication with any I2P router.

    Router
        An I2P router run by the user that sits at the boundary between the I2P
        network and the user's network (akin to an edge device in corporate
        networks). It builds tunnels under the command of a balancer, and routes
        packets for a client or frontend.

### High-level overview

Imagine a seguinte configuração desejada:

- Uma aplicação cliente com um Destination.
- Quatro routers, cada um gerenciando três túneis de entrada.
- Todos os doze túneis devem ser publicados em um único LeaseSet.

### Single-client

```
                -{ [Tunnel 1]===\
                 |-{ [Tunnel 2]====[Router 1]-----
                 |-{ [Tunnel 3]===/               \
                 |                                 \
                 |-{ [Tunnel 4]===\                 \
  [Destination]  |-{ [Tunnel 5]====[Router 2]-----   \
    \            |-{ [Tunnel 6]===/               \   \
     [LeaseSet]--|                               [Client]
                 |-{ [Tunnel 7]===\               /   /
                 |-{ [Tunnel 8]====[Router 3]-----   /
                 |-{ [Tunnel 9]===/                 /
                 |                                 /
                 |-{ [Tunnel 10]==\               /
                 |-{ [Tunnel 11]===[Router 4]-----
                  -{ [Tunnel 12]==/
```
### Definições

```
                -{ [Tunnel 1]===\
                 |-{ [Tunnel 2]====[Router 1]---------[Frontend 1]
                 |-{ [Tunnel 3]===/          \                    \
                 |                            \                    \
                 |-{ [Tunnel 4]===\            \                    \
  [Destination]  |-{ [Tunnel 5]====[Router 2]---\-----[Frontend 2]   \
    \            |-{ [Tunnel 6]===/          \   \                \   \
     [LeaseSet]--|                         [Balancer]            [Backend]
                 |-{ [Tunnel 7]===\          /   /                /   /
                 |-{ [Tunnel 8]====[Router 3]---/-----[Frontend 3]   /
                 |-{ [Tunnel 9]===/            /                    /
                 |                            /                    /
                 |-{ [Tunnel 10]==\          /                    /
                 |-{ [Tunnel 11]===[Router 4]---------[Frontend 4]
                  -{ [Tunnel 12]==/
```
### Visão geral de alto nível

- Carregar ou gerar um Destination.

- Abrir uma sessão com cada router, vinculada ao Destination.

- Periodicamente (aproximadamente a cada dez minutos, mas mais ou menos baseado na vivacidade do tunnel):

- Obter o nível rápido de cada router.

- Utilizar o superconjunto de peers para construir tunnels de/para cada router.

    - By default, tunnels to/from a particular router will use peers from
      that router's fast tier, but this is not enforced by the protocol.

- Colete o conjunto de túneis de entrada ativos de todos os routers ativos e crie um LeaseSet.

- Publicar o LeaseSet através de um ou mais dos routers.

### Cliente único

Para criar e gerenciar esta configuração, o cliente precisa da seguinte funcionalidade nova além do que é atualmente fornecido pelo [I2CP](/docs/specs/i2cp/):

- Dizer a um router para construir túneis, sem criar um LeaseSet para eles.
- Obter uma lista dos túneis atuais no pool de entrada.

Além disso, a seguinte funcionalidade permitiria flexibilidade significativa na forma como o cliente gerencia seus tunnels:

- Obter o conteúdo da camada rápida de um router.
- Instruir um router a construir um túnel de entrada ou saída usando uma lista específica de
  peers.

### Multi-cliente

```
         Client                           Router

                    --------------------->  Create Session
   Session Status  <---------------------
                    --------------------->  Get Fast Tier
        Peer List  <---------------------
                    --------------------->  Create Tunnel
    Tunnel Status  <---------------------
                    --------------------->  Get Tunnel Pool
      Tunnel List  <---------------------
                    --------------------->  Publish LeaseSet
                    --------------------->  Send Packet
      Send Status  <---------------------
  Packet Received  <---------------------
```
### Processo geral do cliente

**Criar Sessão** - Criar uma sessão para o Destination especificado.

**Status da Sessão** - Confirmação de que a sessão foi configurada e o cliente agora pode começar a construir tunnels.

**Get Fast Tier** - Solicita uma lista dos peers que o router atualmente consideraria para construir túneis.

**Lista de Peers** - Uma lista de peers conhecidos pelo router.

**Criar Tunnel** - Solicita que o router construa um novo tunnel através dos peers especificados.

**Status do Tunnel** - O resultado de uma construção específica de tunnel, uma vez que esteja disponível.

**Get Tunnel Pool** - Solicita uma lista dos túneis atuais no pool de entrada ou saída para o Destination.

**Lista de Tunnels** - Uma lista de tunnels para o pool solicitado.

**Publicar LeaseSet** - Solicitar que o roteador publique o LeaseSet fornecido através de um dos túneis de saída para o Destino. Nenhum status de resposta é necessário; o roteador deve continuar tentando novamente até estar satisfeito que o LeaseSet foi publicado.

**Send Packet** - Um pacote de saída do cliente. Opcionalmente especifica um tunnel de saída através do qual o pacote deve (deveria?) ser enviado.

**Status de Envio** - Informa o cliente sobre o sucesso ou falha do envio de um pacote.

**Packet Received** - Um pacote de entrada para o cliente. Opcionalmente especifica o túnel de entrada através do qual o pacote foi recebido(?)

## Security implications

Do ponto de vista dos routers, este design é funcionalmente equivalente ao status quo. O router ainda constrói todos os túneis, mantém seus próprios perfis de pares e impõe separação entre operações de router e cliente. Na configuração padrão é completamente idêntica, porque os túneis para esse router são construídos a partir de sua própria camada rápida.

Da perspectiva do netDB, um único leaseSet criado através deste protocolo é idêntico ao status quo, porque aproveita funcionalidades pré-existentes. No entanto, para leaseSets maiores que se aproximam de 16 Leases, pode ser possível para um observador determinar que o leaseSet é multihomed:

- O tamanho máximo atual da camada rápida é de 75 peers. O Inbound Gateway
  (IBGW, o nó publicado em um Lease) é selecionado de uma fração da camada
  (particionado aleatoriamente por pool de túnel por hash, não por contagem):

      1 hop
          The whole fast tier

      2 hops
          Half of the fast tier
          (the default until mid-2014)

      3+ hops
          A quarter of the fast tier
          (3 being the current default)

Isso significa que, em média, os IBGWs serão de um conjunto de 20-30 peers.

- Em uma configuração single-homed, um LeaseSet completo de 16 túneis teria 16 IBGWs
  selecionados aleatoriamente de um conjunto de até (digamos) 20 peers.

- Numa configuração multihomed de 4 routers usando a configuração padrão, um
  LeaseSet completo de 16 túneis teria 16 IBGWs selecionados aleatoriamente de um conjunto de no máximo
  80 peers, embora seja provável que haja uma fração de peers comuns entre
  routers.

Assim, com a configuração padrão, pode ser possível através de análise estatística descobrir que um LeaseSet está sendo gerado por este protocolo. Também pode ser possível descobrir quantos routers existem, embora o efeito da rotatividade nas camadas rápidas reduziria a eficácia desta análise.

Como o cliente tem controle total sobre quais pares seleciona, este vazamento de informação poderia ser reduzido ou eliminado selecionando IBGWs de um conjunto reduzido de pares.

## Compatibility

Este design é completamente compatível com versões anteriores da rede, pois não há alterações no formato do LeaseSet. Todos os routers precisariam estar cientes do novo protocolo, mas isso não é uma preocupação, pois todos seriam controlados pela mesma entidade.

## Performance and scalability notes

O limite superior de 16 Leases por LeaseSet não é alterado por esta proposta. Para Destinations que requerem mais tunnels que isso, há duas possíveis modificações de rede:

- Aumentar o limite superior no tamanho dos LeaseSets. Esta seria a implementação mais simples (embora ainda exigisse suporte generalizado da rede antes de poder ser amplamente utilizada), mas poderia resultar em consultas mais lentas devido aos tamanhos maiores de pacotes. O tamanho máximo viável de LeaseSet é definido pelo MTU dos transportes subjacentes, e portanto está em torno de 16kB.

- Implementar a Proposta 123 para LeaseSets em camadas. Em combinação com esta proposta,
  os Destinations para os sub-LeaseSets poderiam ser distribuídos por múltiplos
  routers, efetivamente funcionando como múltiplos endereços IP para um serviço clearnet.

## Acknowledgements

Obrigado ao psi pela discussão que levou a esta proposta.
