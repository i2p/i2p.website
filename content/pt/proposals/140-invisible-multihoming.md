---
title: "Multihoming Invisível"
number: "140"
author: "str4d"
created: "2017-05-22"
lastupdated: "2017-07-04"
status: "Open"
thread: "http://zzz.i2p/topics/2335"
---

## Visão Geral

Esta proposta descreve um design para um protocolo que permite a um cliente, serviço ou processo externo de balanceamento do I2P gerenciar múltiplos roteadores que hospedam de forma transparente um único [Destino](http://localhost:63465/en/docs/specs/common-structures/#destination).

A proposta atualmente não especifica uma implementação concreta. Ela poderia ser implementada como uma extensão ao [I2CP](/en/docs/specs/i2cp/), ou como um novo protocolo.

## Motivação

Multihoming é quando vários roteadores são usados para hospedar o mesmo Destino. A maneira atual de fazer multihoming com o I2P é executar o mesmo Destino em cada roteador de forma independente; o roteador que é usado pelos clientes em qualquer momento é o último que publica um [LeaseSet](http://localhost:63465/en/docs/specs/common-structures/#leaseset).

Isso é um improviso e presumivelmente não funcionará para grandes sites em escala. Suponha que tivéssemos 100 roteadores multihoming cada um com 16 túneis. São 1600 publicações de LeaseSet a cada 10 minutos, ou quase 3 por segundo. Os floodfills ficariam sobrecarregados e os controles de limitação entrariam em ação. E isso antes mesmo de mencionarmos o tráfego de procura.

[Proposal 123](/en/proposals/123-new-netdb-entries/) resolve este problema com um meta-LeaseSet, que lista os 100 hashes reais de LeaseSet. Uma consulta torna-se um processo de duas etapas: primeiro procurando o meta-LeaseSet, e depois um dos LeaseSets nomeados. Esta é uma boa solução para o problema de tráfego de consulta, mas por si só cria um vazamento significativo de privacidade: é possível determinar quais roteadores multihoming estão online ao monitorar o meta-LeaseSet publicado, porque cada LeaseSet real corresponde a um único roteador.

Precisamos de uma maneira para que um cliente ou serviço do I2P espalhe um único Destino por vários roteadores, de uma forma que seja indistinguível do uso de um único roteador (do ponto de vista do próprio LeaseSet).

## Design

### Definições

    Usuário
        A pessoa ou organização que deseja multihomear seu(s) Destino(s). Um único Destino é considerado aqui sem perda de generalidade (WLOG).

    Cliente
        A aplicação ou serviço executando por trás do Destino. Pode ser uma aplicação do lado do cliente, do lado do servidor ou peer-to-peer; nos referimos a ela como um cliente no sentido de que se conecta aos roteadores do I2P.

        O cliente consiste em três partes, que podem estar todas no mesmo processo ou podem ser separadas por processos ou máquinas (em uma configuração de múltiplos clientes):

        Balanceador
            A parte do cliente que gerencia a seleção de pares e a construção de túneis. Há um único balanceador em qualquer momento, e ele se comunica com todos os roteadores I2P. Podem haver balanceadores de failover.

        Frontend
            A parte do cliente que pode ser operada em paralelo. Cada frontend se comunica com um único roteador I2P.

        Backend
            A parte do cliente que é compartilhada entre todos os frontends. Não tem comunicação direta com nenhum roteador I2P.

    Roteador
        Um roteador I2P operado pelo usuário que fica na fronteira entre a rede I2P e a rede do usuário (semelhante a um dispositivo de borda em redes corporativas). Ele constrói túneis sob o comando de um balanceador, e encaminha pacotes para um cliente ou frontend.

### Visão geral de alto nível

Imagine a seguinte configuração desejada:

- Uma aplicação cliente com um Destino.
- Quatro roteadores, cada um gerenciando três túneis de entrada.
- Todos os doze túneis devem ser publicados em um único LeaseSet.

Cliente único

```
                -{ [Túnel 1]===\
                 |-{ [Túnel 2]====[Roteador 1]-----
                 |-{ [Túnel 3]===/               \
                 |                                 \
                 |-{ [Túnel 4]===\                 \
  [Destino]      |-{ [Túnel 5]====[Roteador 2]-----   \
    \            |-{ [Túnel 6]===/               \   \
     [LeaseSet]--|                               [Cliente]
                 |-{ [Túnel 7]===\               /   /
                 |-{ [Túnel 8]====[Roteador 3]-----   /
                 |-{ [Túnel 9]===/                 /
                 |                                 /
                 |-{ [Túnel 10]==\               /
                 |-{ [Túnel 11]===[Roteador 4]-----
                  -{ [Túnel 12]==/

Multi-cliente

```
                -{ [Túnel 1]===\
                 |-{ [Túnel 2]====[Roteador 1]---------[Frontend 1]
                 |-{ [Túnel 3]===/          \                    \
                 |                            \                    \
                 |-{ [Túnel 4]===\            \                    \
  [Destino]      |-{ [Túnel 5]====[Roteador 2]---\-----[Frontend 2]   \
    \            |-{ [Túnel 6]===/          \   \                \   \
     [LeaseSet]--|                         [Balanceador]        [Backend]
                 |-{ [Túnel 7]===\          /   /                /   /
                 |-{ [Túnel 8]====[Roteador 3]---/-----[Frontend 3]   /
                 |-{ [Túnel 9]===/            /                    /
                 |                            /                    /
                 |-{ [Túnel 10]==\          /                    /
                 |-{ [Túnel 11]===[Roteador 4]---------[Frontend 4]
                  -{ [Túnel 12]==/

### Processo geral do cliente
- Carregar ou gerar um Destino.

- Abrir uma sessão com cada roteador, vinculada ao Destino.

- Periodicamente (cerca de a cada dez minutos, mas mais ou menos com base na vitalidade dos túneis):

  - Obter o nível rápido de cada roteador.

  - Usar o superconjunto de pares para construir túneis de/para cada roteador.

    - Por padrão, túneis de/para um roteador específico usarão pares do nível rápido desse roteador, mas isso não é imposto pelo protocolo.

  - Coletar o conjunto de túneis de entrada ativos de todos os roteadores ativos e criar um LeaseSet.

  - Publicar o LeaseSet através de um ou mais dos roteadores.

### Diferenças para o I2CP
Para criar e gerenciar essa configuração, o cliente precisa da seguinte nova funcionalidade além do que é atualmente fornecido pelo [I2CP](/en/docs/specs/i2cp/):

- Informar a um roteador para construir túneis, sem criar um LeaseSet para eles.
- Obter uma lista dos túneis atuais no pool de entrada.

Além disso, a seguinte funcionalidade permitiria flexibilidade significativa em como o cliente gerencia seus túneis:

- Obter o conteúdo do nível rápido de um roteador.
- Informar a um roteador para construir um túnel de entrada ou saída usando uma lista especificada de pares.

### Resumo do protocolo

```
         Cliente                           Roteador

                    --------------------->  Criar Sessão
   Status da Sessão <---------------------
                    --------------------->  Obter Nível Rápido
        Lista de Pares  <---------------------
                    --------------------->  Criar Túnel
    Status do Túnel  <---------------------
                    --------------------->  Obter Pool de Túneis
      Lista de Túneis  <---------------------
                    --------------------->  Publicar LeaseSet
                    --------------------->  Enviar Pacote
      Status de Envio  <---------------------
  Pacote Recebido  <---------------------

### Mensagens
    Criar Sessão
        Criar uma sessão para o Destino dado.

    Status da Sessão
        Confirmação de que a sessão foi configurada, e o cliente pode agora começar a construir túneis.

    Obter Nível Rápido
        Solicitar uma lista dos pares que o roteador atualmente consideraria construir túneis.

    Lista de Pares
        Uma lista de pares conhecidos pelo roteador.

    Criar Túnel
        Solicitar que o roteador construa um novo túnel através dos pares especificados.

    Status do Túnel
        O resultado de uma construção específica de túnel, uma vez que esteja disponível.

    Obter Pool de Túneis
        Solicitar uma lista dos túneis atuais no pool de entrada ou saída para o Destino.

    Lista de Túneis
        Uma lista de túneis para o pool solicitado.

    Publicar LeaseSet
        Solicitar que o roteador publique o LeaseSet fornecido através de um dos túneis de saída para o Destino. Nenhum status de resposta é necessário; o roteador deve continuar tentando até que esteja satisfeito de que o LeaseSet foi publicado.

    Enviar Pacote
        Um pacote de saída do cliente. Opcionalmente especifica um túnel de saída através do qual o pacote deve (deveria?) ser enviado.

    Status de Envio
        Informa o cliente sobre o sucesso ou falha ao enviar um pacote.

    Pacote Recebido
        Um pacote de entrada para o cliente. Opcionalmente especifica o túnel de entrada através do qual o pacote foi recebido(?)

## Implicações de segurança

Do ponto de vista dos roteadores, este design é funcionalmente equivalente ao status quo. O roteador ainda constrói todos os túneis, mantém seus próprios perfis de pares e impõe a separação entre as operações do roteador e do cliente. Na configuração padrão é completamente idêntico, porque os túneis para esse roteador são construídos a partir de seu próprio nível rápido.

Do ponto de vista do netDB, um único LeaseSet criado via este protocolo é idêntico ao status quo, porque aproveita funcionalidades pré-existentes. No entanto, para LeaseSets maiores que se aproximam de 16 Leases, pode ser possível para um observador determinar que o LeaseSet é multihomed:

- O tamanho máximo atual do nível rápido é de 75 pares. O Gateway de Entrada (IBGW, o nó publicado em um Lease) é selecionado a partir de uma fração do nível (particionado aleatoriamente por pool de túneis por hash, não por contagem):

      1 hop
          O nível rápido inteiro

      2 hops
          Metade do nível rápido
          (o padrão até meados de 2014)

      3+ hops
          Um quarto do nível rápido
          (3 sendo o padrão atual)

  Isso significa que, em média, os IBGWs serão de um conjunto de 20-30 pares.

- Em uma configuração de hospedeiro único, um LeaseSet completo de 16 túneis teria 16 IBGWs selecionados aleatoriamente de um conjunto de até (digamos) 20 pares.

- Em uma configuração multihomed de 4 roteadores usando a configuração padrão, um LeaseSet completo de 16 túneis teria 16 IBGWs selecionados aleatoriamente de um conjunto de no máximo 80 pares, embora seja provável que haja uma fração de pares comuns entre os roteadores.

Assim, com a configuração padrão, pode ser possível através de análise estatística descobrir que um LeaseSet está sendo gerado por este protocolo. Também pode ser possível descobrir quantos roteadores existem, embora o efeito de churn nos níveis rápidos reduza a eficácia dessa análise.

Como o cliente tem controle total sobre quais pares seleciona, esse vazamento de informações pode ser reduzido ou eliminado selecionando IBGWs de um conjunto reduzido de pares.

## Compatibilidade

Este design é completamente compatível com versões anteriores da rede, porque não há alterações no formato do [LeaseSet](http://localhost:63465/en/docs/specs/common-structures/#leaseset). Todos os roteadores precisariam estar cientes do novo protocolo, mas isso não é uma preocupação, já que eles seriam todos controlados pela mesma entidade.

## Notas de desempenho e escalabilidade

O limite superior de 16 [Lease](http://localhost:63465/en/docs/specs/common-structures/#lease) por LeaseSet não é alterado por esta proposta. Para Destinos que exigem mais túneis do que isso, há duas modificações de rede possíveis:

- Aumentar o limite superior no tamanho do LeaseSets. Isso seria o mais simples de implementar (embora ainda exigisse suporte generalizado na rede antes de ser amplamente usado), mas poderia resultar em buscas mais lentas devido aos tamanhos de pacote maiores. O tamanho máximo viável do LeaseSet é definido pelo MTU dos transportes subjacentes, e é, portanto, em torno de 16kB.

- Implementar [Proposal 123](/en/proposals/123-new-netdb-entries/) para LeaseSets em camadas. Em combinação com esta proposta, os Destinos para os sub-LeaseSets poderiam ser espalhados por vários roteadores, agindo efetivamente como múltiplos endereços IP para um serviço clearnet.

## Agradecimentos

Agradecimentos ao psi pela discussão que levou a esta proposta.
