---
title: "Implementação de Tunnel"
description: "Especificação da operação, construção e processamento de mensagens dos tunnels I2P"
slug: "tunnel-implementation"
aliases:
  - "/pt/docs/specs/implementation"
  - "/pt/docs/specs/implementation/"
lastUpdated: "2019-07"
accurateFor: "0.9.41"
---

Esta página documenta a implementação atual de tunnel.

## Visão Geral dos Tunnels {#tunnel.overview}

Dentro do I2P, as mensagens são passadas em uma direção através de um tunnel virtual de pares, usando qualquer meio disponível para passar a mensagem para o próximo salto. As mensagens chegam ao *gateway* do tunnel, são agrupadas e/ou fragmentadas em mensagens de tunnel de tamanho fixo, e são encaminhadas para o próximo salto no tunnel, que processa e verifica a validade da mensagem e a envia para o próximo salto, e assim por diante, até atingir o endpoint do tunnel. Esse *endpoint* pega as mensagens agrupadas pelo gateway e as encaminha conforme instruído - seja para outro router, para outro tunnel em outro router, ou localmente.

Todos os tunnels funcionam da mesma forma, mas podem ser segmentados em dois grupos diferentes - tunnels de entrada e tunnels de saída. Os tunnels de entrada têm um gateway não confiável que passa mensagens para baixo em direção ao criador do tunnel, que serve como o ponto final do tunnel. Para tunnels de saída, o criador do tunnel serve como o gateway, passando mensagens para o ponto final remoto.

O criador do tunnel seleciona exatamente quais peers irão participar no tunnel, e fornece a cada um os dados de configuração necessários. Eles podem ter qualquer número de saltos. A intenção é tornar difícil tanto para os participantes quanto para terceiros determinarem o comprimento de um tunnel, ou mesmo para participantes em conluio determinarem se fazem parte do mesmo tunnel (exceto na situação onde peers em conluio estão um ao lado do outro no tunnel).

Na prática, uma série de pools de tunnel são usados para diferentes propósitos - cada destino de cliente local tem seu próprio conjunto de tunnels de entrada e tunnels de saída, configurados para atender às suas necessidades de anonimato e desempenho. Além disso, o próprio router mantém uma série de pools para participar da network database e para gerenciar os próprios tunnels.

I2P é uma rede inerentemente comutada por pacotes, mesmo com esses tunnels, permitindo que aproveite múltiplos tunnels executando em paralelo, aumentando a resiliência e balanceando a carga. Fora da camada central do I2P, há uma biblioteca de streaming fim-a-fim opcional disponível para aplicações cliente, expondo operação semelhante ao TCP, incluindo reordenamento de mensagens, retransmissão, controle de congestionamento, etc.

Uma visão geral da terminologia de tunnel do I2P está [na página de visão geral de tunnels](/docs/overview/tunnel-routing).

## Operação de Tunnel (Processamento de Mensagens) {#tunnel.operation}

### Visão Geral

Após um tunnel ser construído, [mensagens I2NP](/docs/specs/i2np) são processadas e passadas através dele. A operação do tunnel possui quatro processos distintos, executados por vários peers no tunnel.

1. Primeiro, o gateway do tunnel acumula um número
   de mensagens I2NP e as pré-processa em mensagens de tunnel para
   entrega.
2. Em seguida, esse gateway criptografa esses dados pré-processados, então
   os encaminha para o primeiro salto.
3. Esse peer, e subsequentes
   participantes do tunnel, removem uma camada da criptografia, verificando que não é
   uma duplicata, então a encaminham para o próximo peer.
4. Eventualmente, as mensagens de tunnel chegam ao endpoint onde as mensagens I2NP
   originalmente agrupadas pelo gateway são remontadas e encaminhadas conforme
   solicitado.

Os participantes intermediários do tunnel não sabem se estão em um tunnel de entrada ou de saída; eles sempre "criptografam" para o próximo salto. Portanto, aproveitamos a criptografia AES simétrica para "descriptografar" no gateway do tunnel de saída, de modo que o texto simples seja revelado no endpoint de saída.

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Role</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Preprocessing</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Encryption Operation</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Postprocessing</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Outbound Gateway (Creator)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Fragment, Batch, and Pad</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Iteratively encrypt (using decryption operations)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Forward to next hop</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Participant</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Decrypt (using an encryption operation)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Forward to next hop</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Outbound Endpoint</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Decrypt (using an encryption operation) to reveal plaintext tunnel message</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reassemble Fragments, Forward as instructed to Inbound Gateway or Router</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;" colspan="4"></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Inbound Gateway</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Fragment, Batch, and Pad</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Encrypt</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Forward to next hop</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Participant</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Encrypt</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Forward to next hop</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Inbound Endpoint (Creator)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Iteratively decrypt to reveal plaintext tunnel message</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reassemble Fragments, Receive data</td>
    </tr>
  </tbody>
</table>
### Processamento do Gateway {#tunnel.gateway}

#### Pré-processamento de Mensagens {#tunnel.preprocessing}

A função de um gateway de túnel é fragmentar e empacotar [mensagens I2NP](/docs/specs/i2np) em [mensagens de túnel](/docs/specs/tunnel-message) de tamanho fixo e criptografar as mensagens de túnel. As mensagens de túnel contêm o seguinte:

- Um Tunnel ID de 4 bytes
- Um IV (vetor de inicialização) de 16 bytes
- Um checksum
- Padding, se necessário
- Um ou mais pares { instrução de entrega, fragmento de mensagem I2NP }

Os IDs de tunnel são números de 4 bytes usados em cada salto - os participantes sabem qual ID de tunnel devem escutar para mensagens e qual ID de tunnel devem usar para encaminhar ao próximo salto, sendo que cada salto escolhe o ID de tunnel no qual recebe mensagens. Os tunnels em si têm vida curta (10 minutos). Mesmo que tunnels subsequentes sejam construídos usando a mesma sequência de pares, o ID de tunnel de cada salto será alterado.

Para evitar que adversários marquem as mensagens ao longo do caminho ajustando o tamanho das mensagens, todas as mensagens de tunnel têm um tamanho fixo de 1024 bytes. Para acomodar mensagens I2NP maiores, bem como para suportar mensagens menores de forma mais eficiente, o gateway divide as mensagens I2NP maiores em fragmentos contidos dentro de cada mensagem de tunnel. O endpoint tentará reconstruir a mensagem I2NP a partir dos fragmentos por um curto período de tempo, mas os descartará conforme necessário.

Os detalhes estão na [especificação de mensagem de tunnel](/docs/specs/tunnel-message).

### Criptografia de Gateway

Após o pré-processamento das mensagens em um payload preenchido, o gateway constrói um valor IV aleatório de 16 bytes, criptografando-o iterativamente junto com a mensagem do tunnel conforme necessário, e encaminha a tupla {tunnelID, IV, mensagem do tunnel criptografada} para o próximo salto.

Como a criptografia no gateway é feita depende de se o tunnel é um tunnel de entrada ou de saída. Para tunnels de entrada, eles simplesmente selecionam um IV aleatório, pós-processando e atualizando-o para gerar o IV para o gateway e usando esse IV junto com sua própria chave de camada para criptografar os dados pré-processados. Para tunnels de saída, eles devem descriptografar iterativamente o IV (não criptografado) e os dados pré-processados com o IV e as chaves de camada para todos os saltos no tunnel. O resultado da criptografia do tunnel de saída é que quando cada peer o criptografa, o endpoint recuperará os dados pré-processados iniciais.

### Processamento de Participantes {#tunnel.participant}

Quando um peer recebe uma mensagem de tunnel, ele verifica se a mensagem veio do mesmo hop anterior de antes (inicializado quando a primeira mensagem passa pelo tunnel). Se o peer anterior for um router diferente, ou se a mensagem já foi vista, a mensagem é descartada. O participante então criptografa o IV recebido com AES256/ECB usando sua chave IV para determinar o IV atual, usa esse IV com a chave de camada do participante para criptografar os dados, criptografa o IV atual com AES256/ECB usando sua chave IV novamente, então encaminha a tupla {nextTunnelId, nextIV, encryptedData} para o próximo hop. Esta criptografia dupla do IV (tanto antes quanto depois do uso) ajuda a lidar com uma certa classe de ataques de confirmação.

A detecção de mensagens duplicadas é tratada por um filtro Bloom com decaimento nos IVs das mensagens. Cada router mantém um único filtro Bloom para conter o XOR do IV e do primeiro bloco da mensagem recebida para todos os tunnels nos quais está participando, modificado para descartar entradas vistas após 10-20 minutos (quando os tunnels terão expirado). O tamanho do filtro bloom e os parâmetros utilizados são suficientes para mais que saturar a conexão de rede do router com uma chance negligível de falso positivo. O valor único alimentado no filtro Bloom é o XOR do IV e do primeiro bloco para impedir que pares coludidos não sequenciais no tunnel marquem uma mensagem reenviando-a com o IV e o primeiro bloco trocados.

### Processamento de Endpoint {#tunnel.endpoint}

Após receber e validar uma mensagem de tunnel no último salto do tunnel, como o endpoint recupera os dados codificados pelo gateway depende de se o tunnel é um tunnel de entrada ou de saída. Para tunnels de saída, o endpoint criptografa a mensagem com sua chave de camada assim como qualquer outro participante, expondo os dados pré-processados. Para tunnels de entrada, o endpoint também é o criador do tunnel, então ele pode simplesmente descriptografar iterativamente o IV e a mensagem, usando as chaves de camada e IV de cada etapa em ordem reversa.

Neste ponto, o endpoint do tunnel tem os dados pré-processados enviados pelo gateway, que pode então analisar para extrair as mensagens I2NP incluídas e encaminhá-las conforme solicitado em suas instruções de entrega.

## Construção de Tunnel {#tunnel.building}

Ao construir um tunnel, o criador deve enviar uma solicitação com os dados de configuração necessários para cada um dos saltos e aguardar que todos concordem antes de habilitar o tunnel. As solicitações são criptografadas para que apenas os peers que precisam conhecer uma informação (como a camada do tunnel ou chave IV) tenham esses dados. Além disso, apenas o criador do tunnel terá acesso à resposta do peer. Há três dimensões importantes a ter em mente ao produzir os tunnels: quais peers são usados (e onde), como as solicitações são enviadas (e respostas recebidas), e como são mantidos.

### Seleção de Peers {#tunnel.peerselection}

Além dos dois tipos de tunnels - inbound e outbound - existem dois estilos de seleção de peers utilizados para diferentes tunnels - exploratório e cliente. Tunnels exploratórios são usados tanto para manutenção da base de dados de rede quanto para manutenção de tunnels, enquanto tunnels de cliente são usados para mensagens cliente de ponta a ponta.

#### Seleção de Peer para Tunnel Exploratório {#tunnel.selection.exploratory}

Os tunnels exploratórios são construídos a partir de uma seleção aleatória de peers de um subconjunto da rede. O subconjunto específico varia conforme o router local e suas necessidades de roteamento de tunnel. Em geral, os tunnels exploratórios são construídos a partir de peers selecionados aleatoriamente que estão na categoria de perfil "não falhando mas ativo" do peer. O propósito secundário dos tunnels, além do mero roteamento de tunnel, é encontrar peers de alta capacidade subutilizados para que possam ser promovidos para uso em tunnels de cliente.

A seleção exploratória de peers é discutida mais detalhadamente na [página de Profiling e Seleção de Peers](/docs/overview/peer-selection).

#### Seleção de Pares de Tunnel de Cliente {#tunnel.selection.client}

Os client tunnels são construídos com um conjunto mais rigoroso de requisitos - o router local selecionará peers de sua categoria de perfil "rápidos e de alta capacidade" para que o desempenho e a confiabilidade atendam às necessidades da aplicação cliente. No entanto, existem vários detalhes importantes além dessa seleção básica que devem ser seguidos, dependendo das necessidades de anonimato do cliente.

A seleção de peers do cliente é discutida mais detalhadamente na [página de Profiling e Seleção de Peers](/docs/overview/peer-selection).

#### Ordenação de Pares dentro dos Tunnels {#ordering}

Os peers são ordenados dentro dos tunnels para lidar com o [ataque predecessor](http://forensics.umass.edu/pubs/wright-tissec.pdf) ([atualização de 2008](http://forensics.umass.edu/pubs/wright.tissec.2008.pdf)).

Para frustrar o ataque predecessor, a seleção de tunnel mantém os peers selecionados em uma ordem rigorosa - se A, B e C estão em um tunnel para um determinado pool de tunnels, o salto após A é sempre B, e o salto após B é sempre C.

A ordenação é implementada gerando uma chave aleatória de 32 bytes para cada pool de tunnel na inicialização. Os peers não devem conseguir adivinhar a ordenação, ou um atacante poderia criar dois hashes de router distantes para maximizar a chance de estar em ambas as extremidades de um tunnel. Os peers são ordenados pela distância XOR do Hash SHA256 de (o hash do peer concatenado com a chave aleatória) da chave aleatória:

```
      p = peer hash
      k = random key
      d = XOR(H(p+k), k)
```
Como cada pool de tunnel usa uma chave aleatória diferente, a ordenação é consistente dentro de um único pool, mas não entre pools diferentes. Novas chaves são geradas a cada reinicialização do router.

### Entrega de Solicitação {#tunnel.request}

Um tunnel multi-hop é construído usando uma única mensagem de construção que é repetidamente descriptografada e encaminhada. Na terminologia de [Hashing it out in Public](http://www-users.cs.umn.edu/~hopper/hashing_it_out.pdf), isso é construção de tunnel telescópica "não-interativa".

Este método de preparação, entrega e resposta de solicitação de tunnel é [projetado](/docs/specs/tunnel-creation) para reduzir o número de predecessores expostos, corta o número de mensagens transmitidas, verifica a conectividade adequada e evita o ataque de contagem de mensagens da criação telescópica tradicional de tunnel. (Este método, que envia mensagens para estender um tunnel através da parte já estabelecida do tunnel, é denominado construção telescópica "interativa" de tunnel no artigo "Hashing it out".)

Os detalhes das mensagens de solicitação e resposta de tunnel, e sua criptografia, [são especificados aqui](/docs/specs/tunnel-creation).

Peers podem rejeitar solicitações de criação de tunnel por várias razões, embora uma série de quatro rejeições de gravidade crescente sejam conhecidas: rejeição probabilística (devido à aproximação da capacidade do router, ou em resposta a uma enxurrada de solicitações), sobrecarga transitória, sobrecarga de largura de banda e falha crítica. Quando recebidas, essas quatro são interpretadas pelo criador do tunnel para ajudar a ajustar seu perfil do router em questão.

Para mais informações sobre criação de perfis de peers, consulte a [página de Criação de Perfis e Seleção de Peers](/docs/overview/peer-selection).

### Pools de Tunnel {#tunnel.pooling}

Para permitir uma operação eficiente, o router mantém uma série de pools de tunnels, cada um gerenciando um grupo de tunnels usados para um propósito específico com sua própria configuração. Quando um tunnel é necessário para esse propósito, o router seleciona um do pool apropriado aleatoriamente. No geral, existem dois pools de tunnels exploratórios - um de entrada e um de saída - cada um usando a configuração padrão do router. Além disso, existe um par de pools para cada destino local - um pool de tunnels de entrada e um de saída. Esses pools usam a configuração especificada quando o destino local se conecta ao router via [I2CP](/docs/specs/i2cp), ou os padrões do router se não especificado.

Cada pool tem dentro de sua configuração algumas definições-chave, definindo quantos tunnels manter ativos, quantos tunnels de backup manter em caso de falha, qual deve ser o comprimento dos tunnels, se esses comprimentos devem ser aleatorizados, bem como qualquer uma das outras configurações permitidas ao configurar tunnels individuais. As opções de configuração são especificadas na [página I2CP](/docs/specs/i2cp).

### Comprimentos de Tunnel e Padrões {#length}

[Na página de visão geral do tunnel](/docs/overview/tunnel-routing#length).

### Estratégia de Construção Antecipada e Prioridade {#strategy}

A construção de tunnels é custosa, e os tunnels expiram em um tempo fixo após serem construídos. No entanto, quando um pool fica sem tunnels, o Destination fica essencialmente morto. Além disso, a taxa de sucesso na construção de tunnels pode variar drasticamente tanto com as condições de rede locais quanto globais. Portanto, é importante manter uma estratégia de construção antecipatória e adaptativa para garantir que novos tunnels sejam construídos com sucesso antes de serem necessários, sem construir tunnels em excesso, construí-los muito cedo, ou consumir muita CPU ou largura de banda criando e enviando as mensagens de construção criptografadas.

Para cada tupla {exploratório/cliente, entrada/saída, comprimento, variação de comprimento} o router mantém estatísticas sobre o tempo necessário para uma construção bem-sucedida de tunnel. Usando essas estatísticas, ele calcula quanto tempo antes da expiração de um tunnel deve começar a tentar construir um substituto. À medida que o tempo de expiração se aproxima sem um substituto bem-sucedido, ele inicia múltiplas tentativas de construção em paralelo, e então aumentará o número de tentativas paralelas se necessário.

Para limitar o uso de largura de banda e CPU, o router também limita o número máximo de tentativas de construção pendentes em todos os pools. Construções críticas (aquelas para túneis exploratórios e para pools que ficaram sem túneis) são priorizadas.

## Limitação de Mensagens do Tunnel {#tunnel.throttling}

Embora os tunnels dentro do I2P tenham uma semelhança com uma rede de comutação de circuitos, tudo dentro do I2P é estritamente baseado em mensagens - tunnels são meramente truques de contabilização para ajudar a organizar a entrega de mensagens. Nenhuma suposição é feita em relação à confiabilidade ou ordenação de mensagens, e retransmissões são deixadas para níveis superiores (por exemplo, a biblioteca de streaming da camada cliente do I2P). Isso permite que o I2P aproveite técnicas de throttling (limitação de largura de banda) disponíveis tanto para redes de comutação de pacotes quanto para redes de comutação de circuitos. Por exemplo, cada router pode acompanhar a média móvel de quantos dados cada tunnel está usando, combinar isso com todas as médias usadas por outros tunnels dos quais o router está participando, e ser capaz de aceitar ou rejeitar solicitações adicionais de participação em tunnel com base em sua capacidade e utilização. Por outro lado, cada router pode simplesmente descartar mensagens que estão além de sua capacidade, explorando a pesquisa utilizada na Internet normal.

Na implementação atual, os routers implementam uma estratégia de descarte antecipado aleatório ponderado (WRED). Para todos os routers participantes (participante interno, gateway de entrada e endpoint de saída), o router começará a descartar aleatoriamente uma porção das mensagens conforme os limites de largura de banda forem sendo aproximados. À medida que o tráfego se aproxima ou excede os limites, mais mensagens são descartadas. Para um participante interno, todas as mensagens são fragmentadas e preenchidas e, portanto, têm o mesmo tamanho. No gateway de entrada e endpoint de saída, no entanto, a decisão de descarte é feita na mensagem completa (coalescida), e o tamanho da mensagem é levado em consideração. Mensagens maiores têm maior probabilidade de serem descartadas. Além disso, as mensagens têm maior probabilidade de serem descartadas no endpoint de saída do que no gateway de entrada, pois essas mensagens não estão tão "avançadas" em sua jornada e, portanto, o custo de rede de descartar essas mensagens é menor.

## Trabalho Futuro {#future}

### Mistura/Loteamento {#tunnel.mixing}

Que estratégias poderiam ser usadas no gateway e em cada hop para atrasar, reordenar, reencaminhar ou preencher mensagens? Até que ponto isso deveria ser feito automaticamente, quanto deveria ser configurado como uma configuração por tunnel ou por hop, e como o criador do tunnel (e por sua vez, o usuário) deveria controlar essa operação? Tudo isso permanece desconhecido, para ser trabalhado em uma versão futura distante.

### Preenchimento

As estratégias de padding podem ser usadas em vários níveis, abordando a exposição de informações sobre o tamanho da mensagem para diferentes adversários. O tamanho fixo atual da mensagem do tunnel é de 1024 bytes. Dentro disso, no entanto, as mensagens fragmentadas em si não recebem padding do tunnel, embora para mensagens fim a fim, elas possam receber padding como parte do garlic wrapping.

### WRED

As estratégias WRED têm um impacto significativo no desempenho fim-a-fim e na prevenção do colapso de congestionamento da rede. A estratégia WRED atual deve ser cuidadosamente avaliada e aprimorada.
