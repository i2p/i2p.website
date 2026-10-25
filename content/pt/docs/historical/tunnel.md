---
title: "Discussão sobre Tunnels"
description: "Exploração histórica de estratégias de preenchimento, fragmentação e construção de tunnels"
slug: "tunnel"
aliases:
  - "/pt/docs/discussions/tunnel"
  - "/pt/docs/discussions/tunnel/"
  - "/pt/tunnel_discussion"
  - "/pt/tunnel_discussion/"
lastUpdated: "2019-07"
accurateFor: "0.9.41"
---

Nota: Este documento contém informações mais antigas sobre alternativas à implementação atual de tunnel no I2P, e especulações sobre possibilidades futuras. Para informações atuais consulte [a página de tunnel](/docs/specs/tunnel-implementation).

Essa página documenta a implementação atual de construção de tunnel a partir da versão 0.6.1.10. O método antigo de construção de tunnel, usado antes da versão 0.6.1.10, está documentado na [página antiga de tunnel](/docs/historical/tunnel-alt).

### Alternativas de Configuração {#config}

Além do comprimento, pode haver parâmetros configuráveis adicionais para cada tunnel que podem ser utilizados, como uma limitação na frequência de mensagens entregues, como o padding deve ser usado, por quanto tempo um tunnel deve permanecer em operação, se deve injetar mensagens chaff, e quais estratégias de batching, se houver, devem ser empregadas. Nenhuma dessas funcionalidades está atualmente implementada.

### Alternativas de Padding {#tunnel.padding}

Várias estratégias de preenchimento de tunnel são possíveis, cada uma com seus próprios méritos:

- Sem padding
- Padding para um tamanho aleatório
- Padding para um tamanho fixo
- Padding para o KB mais próximo
- Padding para o tamanho exponencial mais próximo (2^n bytes)

Essas estratégias de preenchimento podem ser usadas em vários níveis, abordando a exposição de informações sobre o tamanho da mensagem para diferentes adversários. Após coletar e revisar algumas estatísticas da rede 0.4, bem como explorar as compensações de anonimato, estamos começando com um tamanho fixo de mensagem de tunnel de 1024 bytes. Dentro disso, porém, as mensagens fragmentadas em si não são preenchidas pelo tunnel de forma alguma (embora para mensagens ponto a ponto, elas possam ser preenchidas como parte do empacotamento garlic).

### Alternativas de Fragmentação {#tunnel.fragmentation}

Para prevenir que adversários marquem as mensagens ao longo do caminho ajustando o tamanho da mensagem, todas as mensagens de tunnel têm um tamanho fixo de 1024 bytes. Para acomodar mensagens I2NP maiores, bem como para suportar as menores de forma mais eficiente, o gateway divide as mensagens I2NP maiores em fragmentos contidos dentro de cada mensagem de tunnel. O endpoint tentará reconstruir a mensagem I2NP a partir dos fragmentos por um curto período de tempo, mas os descartará conforme necessário.

Os routers têm muita flexibilidade quanto à forma como os fragmentos são organizados, seja se são empacotados de forma ineficiente como unidades discretas, agrupados por um breve período para caber mais payload nas mensagens de túnel de 1024 bytes, ou oportunisticamente preenchidos com outras mensagens que o gateway queria enviar.

### Mais Alternativas {#tunnel.alternatives}

#### Ajustar Processamento de Tunnel em Tempo Real {#tunnel.reroute}

Embora o algoritmo simples de roteamento de tunnel deva ser suficiente para a maioria dos casos, existem três alternativas que podem ser exploradas:

- Fazer com que um peer diferente do endpoint atue temporariamente como o ponto de terminação de um tunnel ajustando a criptografia usada no gateway para fornecer a eles o texto simples das mensagens I2NP pré-processadas. Cada peer poderia verificar se tinha o texto simples, processando a mensagem quando recebida como se tivesse.
- Permitir que routers participantes em um tunnel remixem a mensagem antes de encaminhá-la - fazendo-a saltar através de um dos próprios tunnels de saída daquele peer, portando instruções para entrega ao próximo salto.
- Implementar código para o criador do tunnel redefinir o "próximo salto" de um peer no tunnel, permitindo redirecionamento dinâmico adicional.

#### Use Tunnels Bidirecionais {#tunnel.bidirectional}

A estratégia atual de usar dois tunnels separados para comunicação de entrada e saída não é a única técnica disponível, e tem implicações de anonimato. Do lado positivo, ao usar tunnels separados, isso reduz os dados de tráfego expostos para análise aos participantes em um tunnel - por exemplo, peers em um tunnel de saída de um navegador web veriam apenas o tráfego de um HTTP GET, enquanto os peers em um tunnel de entrada veriam a carga útil entregue ao longo do tunnel. Com tunnels bidirecionais, todos os participantes teriam acesso ao fato de que, por exemplo, 1KB foi enviado em uma direção, depois 100KB na outra. Do lado negativo, usar tunnels unidirecionais significa que há dois conjuntos de peers que precisam ser perfilados e considerados, e cuidado adicional deve ser tomado para abordar a velocidade aumentada de ataques predecessores. O processo de pooling e construção de tunnel descrito abaixo deve minimizar as preocupações do ataque predecessor, embora se fosse desejado, não seria muito trabalho construir tanto os tunnels de entrada quanto os de saída ao longo dos mesmos peers.

#### Comunicação de Canal Secundário {#tunnel.backchannel}

No momento, os valores de IV utilizados são valores aleatórios. No entanto, é possível que esse valor de 16 bytes seja usado para enviar mensagens de controle do gateway para o endpoint, ou em tunnels de saída, do gateway para qualquer um dos peers. O gateway de entrada poderia codificar certos valores no IV uma vez, que o endpoint seria capaz de recuperar (já que sabe que o endpoint também é o criador). Para tunnels de saída, o criador poderia entregar certos valores aos participantes durante a criação do tunnel (por exemplo, "se você vir 0x0 como o IV, isso significa X", "0x1 significa Y", etc). Como o gateway no tunnel de saída também é o criador, eles podem construir um IV de modo que qualquer um dos peers receba o valor correto. O criador do tunnel poderia até mesmo fornecer ao gateway do tunnel de entrada uma série de valores de IV que esse gateway poderia usar para se comunicar com participantes individuais exatamente uma vez (embora isso teria problemas relacionados à detecção de conluio).

Esta técnica poderia ser usada posteriormente para entregar mensagens no meio do fluxo, ou para permitir que o gateway de entrada informe ao endpoint que está sofrendo um ataque DoS ou que irá falhar em breve. No momento, não há planos para explorar este canal de retorno.

#### Mensagens de Tunnel de Tamanho Variável {#tunnel.variablesize}

Embora a camada de transporte possa ter seu próprio tamanho de mensagem fixo ou variável, usando sua própria fragmentação, a camada de tunnel pode em vez disso usar mensagens de tunnel de tamanho variável. A diferença é uma questão de modelos de ameaça - um tamanho fixo na camada de transporte ajuda a reduzir as informações expostas a adversários externos (embora a análise geral de fluxo ainda funcione), mas para adversários internos (ou seja, participantes do tunnel) o tamanho da mensagem fica exposto. Mensagens de tunnel de tamanho fixo ajudam a reduzir as informações expostas aos participantes do tunnel, mas não esconde as informações expostas aos endpoints e gateways do tunnel. Mensagens fim-a-fim de tamanho fixo escondem as informações expostas a todos os pares na rede.

Como sempre, é uma questão de contra quem o I2P está tentando proteger. Mensagens de tunnel de tamanho variável são perigosas, pois permitem que os participantes usem o próprio tamanho da mensagem como um canal secundário para outros participantes - por exemplo, se você vê uma mensagem de 1337 bytes, você está no mesmo tunnel que outro peer coludindo. Mesmo com um conjunto fixo de tamanhos permitidos (1024, 2048, 4096, etc), esse canal secundário ainda existe, pois os peers poderiam usar a frequência de cada tamanho como portadora (por exemplo, duas mensagens de 1024 bytes seguidas de uma de 8192). Mensagens menores incorrem na sobrecarga dos cabeçalhos (IV, ID do tunnel, porção do hash, etc), mas mensagens maiores de tamanho fixo aumentam a latência (devido ao agrupamento) ou aumentam drasticamente a sobrecarga (devido ao preenchimento). A fragmentação ajuda a amortizar a sobrecarga, ao custo de potencial perda de mensagens devido a fragmentos perdidos.

Ataques de temporização também são relevantes ao analisar a eficácia de mensagens de tamanho fixo, embora exijam uma visão substancial dos padrões de atividade da rede para serem eficazes. Atrasos artificiais excessivos no tunnel serão detectados pelo criador do tunnel, devido a testes periódicos, fazendo com que todo o tunnel seja descartado e os perfis dos peers dentro dele sejam ajustados.

### Construindo Alternativas {#tunnel.building.alternatives}

Referência: [Hashing it out in Public](http://www-users.cs.umn.edu/~hopper/hashing_it_out.pdf)

#### Método Antigo de Construção de Tunnel {#tunnel.building.old}

O método antigo de construção de tunnel, usado antes da versão 0.6.1.10, está documentado na [página antiga de tunnel](/docs/historical/tunnel-alt). Este era um método "tudo de uma vez" ou "paralelo", onde mensagens eram enviadas em paralelo para cada um dos participantes.

#### Construção Telescópica de Uma Vez {#tunnel.building.oneshot}

NOTA: Este é o método atual.

Uma questão que surgiu em relação ao uso dos tunnels exploratórios para enviar e receber mensagens de criação de tunnel é como isso impacta a vulnerabilidade do tunnel a ataques de predecessor. Embora os pontos finais e gateways desses tunnels sejam distribuídos aleatoriamente pela rede (talvez até incluindo o criador do tunnel nesse conjunto), uma alternativa é usar os próprios caminhos do tunnel para passar a solicitação e resposta, como é feito no [Tor](https://www.torproject.org/). Isso, no entanto, pode levar a vazamentos durante a criação do tunnel, permitindo que peers descubram quantos saltos existem mais adiante no tunnel monitorando o tempo ou contagem de pacotes conforme o tunnel é construído.

#### Construção Telescópica "Interativa" {#tunnel.building.telescoping}

Construa os hops um de cada vez com uma mensagem através da parte existente do tunnel para cada um. Tem grandes problemas pois os peers podem contar as mensagens para determinar sua localização no tunnel.

#### Tunnels Não-Exploratórios para Gestão {#tunnel.building.nonexploratory}

Uma segunda alternativa ao processo de construção de túnel é fornecer ao router um conjunto adicional de pools de entrada e saída não exploratórios, usando-os para a solicitação e resposta do túnel. Assumindo que o router tenha uma visão bem integrada da rede, isso não deveria ser necessário, mas se o router estivesse particionado de alguma forma, usar pools não exploratórios para gerenciamento de túnel reduziria o vazamento de informações sobre quais peers estão na partição do router.

#### Entrega de Solicitação Exploratória {#tunnel.building.exploratory}

Uma terceira alternativa, usada até o I2P 0.6.1.10, utiliza garlic encryption para criptografar mensagens individuais de solicitação de tunnel e as entrega aos hops individualmente, transmitindo-as através de tunnels exploratórios com sua resposta retornando em um tunnel exploratório separado. Esta estratégia foi abandonada em favor da descrita acima.

#### Mais História e Discussão {#history}

Antes da introdução da Variable Tunnel Build Message, havia pelo menos dois problemas:

1. O tamanho das mensagens (causado por um máximo de 8 saltos, quando o comprimento típico do tunnel é de 2 ou 3 saltos...
   e pesquisas atuais indicam que mais de 3 saltos não melhora o anonimato);
2. A alta taxa de falha na construção, especialmente para tunnels longos (e exploratórios), já que todos os saltos devem concordar ou o tunnel é descartado.

O VTBM corrigiu o #1 e melhorou o #2.

Welterde propôs modificações no método paralelo para permitir reconfiguração. Sponge propôs usar 'tokens' de algum tipo.

Qualquer estudante de construção de tunnel deve estudar o registro histórico que levou ao método atual, especialmente as várias vulnerabilidades de anonimato que podem existir em vários métodos. Os arquivos de correio de outubro de 2005 são particularmente úteis. Como declarado na [especificação de criação de tunnel](/docs/specs/tunnel-creation), a estratégia atual surgiu durante uma discussão na lista de correio I2P entre Michael Rogers, Matthew Toseland (toad) e jrandom sobre o ataque predecessor.

#### Alternativas de Ordenação de Peers {#ordering}

Uma ordenação menos rigorosa também é possível, assegurando que embora o salto após A possa ser B, B nunca pode vir antes de A. Outras opções de configuração incluem a capacidade de apenas os gateways de tunnel de entrada e os endpoints de tunnel de saída serem fixos, ou rotacionados a uma taxa MTBF.

## Mistura/Loteamento {#tunnel.mixing}

Que estratégias devem ser usadas no gateway e em cada hop para atrasar, reordenar, redirecionar ou adicionar padding às mensagens? Em que medida isso deve ser feito automaticamente, quanto deve ser configurado como uma definição por tunnel ou por hop, e como o criador do tunnel (e por sua vez, o usuário) deve controlar essa operação? Tudo isso permanece como desconhecido, para ser resolvido em uma versão futura.
