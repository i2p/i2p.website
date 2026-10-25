---
title: "Discussão sobre NTCP"
description: "Discussão histórica sobre protocolos de transporte NTCP vs SSU de março de 2007"
slug: "ntcp-discussion"
aliases:
  - "/pt/docs/discussions/ntcp"
  - "/pt/docs/discussions/ntcp/"
  - "/pt/ntcp_discussion"
  - "/pt/ntcp_discussion/"
lastUpdated: "2007-03"
accurateFor: "historical"
---

A seguir está uma discussão sobre NTCP que ocorreu em março de 2007. Ela não foi atualizada para refletir a implementação atual. Para a especificação NTCP atual, consulte [a página NTCP2](/docs/specs/ntcp2).

## Discussão NTCP vs. SSU, Março 2007 {#ntcp-ssu}

### Perguntas sobre NTCP

(adaptado de uma discussão no IRC entre zzz e cervantes)

Por que o NTCP é preferido ao SSU, o NTCP não tem maior overhead e latência? Ele tem melhor confiabilidade.

A biblioteca de streaming sobre NTCP não sofre dos problemas clássicos de TCP-sobre-TCP? E se tivéssemos um transporte UDP realmente simples para tráfego originado da streaming-lib? Acho que o SSU deveria ser esse transporte UDP realmente simples - mas simplesmente se mostrou muito pouco confiável.

### Análise "NTCP Considered Harmful" por zzz {#harmful}

Publicado no novo Syndie, 2007-03-25. Isso foi publicado para estimular discussão, não leve muito a sério.

**Resumo:** NTCP tem maior latência e overhead que SSU, e é mais provável que falhe quando usado com a biblioteca de streaming. No entanto, o tráfego é roteado com preferência para NTCP sobre SSU e isso está atualmente codificado diretamente no código.

#### Discussão

Atualmente temos dois transportes, NTCP e SSU. Como implementado atualmente, NTCP tem "lances" menores que SSU, então é preferido, exceto no caso onde há uma conexão SSU estabelecida mas nenhuma conexão NTCP estabelecida para um peer.

SSU é similar ao NTCP no sentido de que implementa confirmações, timeouts e retransmissões. No entanto, SSU é código I2P com restrições rigorosas nos timeouts e estatísticas disponíveis sobre tempos de ida e volta, retransmissões, etc. NTCP é baseado em Java NIO TCP, que é uma caixa preta e presumivelmente implementa padrões RFC, incluindo timeouts máximos muito longos.

A maioria do tráfego dentro do I2P é originada do streaming-lib (HTTP, IRC, Bittorrent), que é nossa implementação do TCP. Como o transporte de nível inferior é geralmente NTCP devido às ofertas mais baixas, o sistema está sujeito ao problema bem conhecido e temido do TCP-over-TCP http://sites.inka.de/~W1011/devel/tcp-tcp.html , onde tanto as camadas superiores quanto inferiores do TCP estão fazendo retransmissões simultaneamente, levando ao colapso.

Diferentemente do cenário PPP over SSH descrito no link acima, temos vários saltos para a camada inferior, cada um coberto por um link NTCP. Assim, cada latência NTCP é geralmente muito menor que a latência da biblioteca de streaming da camada superior. Isso reduz a chance de colapso.

Além disso, as probabilidades de colapso são reduzidas quando o TCP da camada inferior é rigidamente restringido com timeouts baixos e número de retransmissões comparado à camada superior.

O lançamento .28 aumentou o timeout máximo da biblioteca de streaming de 10 seg para 45 seg, o que melhorou muito as coisas. O timeout máximo SSU é de 3 seg. O timeout máximo NTCP é presumivelmente de pelo menos 60 seg, que é a recomendação RFC. Não há como alterar parâmetros NTCP ou monitorar desempenho. O colapso da camada NTCP é [editor: texto perdido]. Talvez uma ferramenta externa como tcpdump possa ajudar.

No entanto, executando a versão .28, o upstream reportado pelo i2psnark geralmente não se mantém em um nível alto. Frequentemente cai para 3-4 KBps antes de subir novamente. Este é um sinal de que ainda há colapsos.

SSU também é mais eficiente. NTCP tem maior overhead e provavelmente tempos de ida e volta mais altos. ao usar NTCP a proporção de (saída do tunnel) / (saída de dados do i2psnark) é de pelo menos 3,5 : 1. Executando um experimento onde o código foi modificado para preferir SSU (a opção de configuração i2np.udp.alwaysPreferred não tem efeito no código atual), a proporção reduziu para cerca de 3 : 1, indicando melhor eficiência.

Conforme relatado pelas estatísticas da biblioteca de streaming, as coisas melhoraram muito - o tamanho da janela de vida útil aumentou de 6,3 para 7,5, RTT diminuiu de 11,5s para 10s, envios por ack diminuíram de 1,11 para 1,07.

Que isso fosse tão eficaz foi surpreendente, considerando que estávamos apenas alterando o transporte para o primeiro de 3 a 5 hops totais que as mensagens de saída fariam.

O efeito nas velocidades de saída do i2psnark não ficou claro devido a variações normais. Também para o experimento, o NTCP de entrada foi desabilitado. O efeito nas velocidades de entrada no i2psnark não ficou claro.

#### Propostas

1. **1A)** Isto é fácil -
   Devemos inverter as prioridades de lance para que SSU seja preferido para todo o tráfego, se
   pudermos fazer isso sem causar todo tipo de outros problemas. Isso corrigirá a
   opção de configuração i2np.udp.alwaysPreferred para que funcione (seja como true
   ou false).

2. **1B)** Alternativa à 1A), não tão fácil -
   Se conseguirmos marcar o tráfego sem afetar adversamente nossos objetivos de anonimato, devemos
   identificar o tráfego gerado pela streaming-lib e fazer com que o SSU gere uma oferta baixa
   para esse tráfego. Esta marcação terá que acompanhar a mensagem através de cada hop
   para que os routers de encaminhamento também honrem a preferência do SSU.

3. **2)** Limitar ainda mais o SSU (reduzindo as retransmissões máximas das atuais
   10) provavelmente é sensato para reduzir a chance de colapso.

4. **3)** Precisamos de mais estudos sobre os benefícios vs. malefícios de um protocolo semi-confiável
   por baixo da biblioteca de streaming. As retransmissões sobre um único hop são benéficas
   e uma grande vitória ou são piores que inúteis?
   Poderíamos fazer um novo SUU (secure unreliable UDP) mas provavelmente não vale a pena. 
   Poderíamos talvez adicionar um tipo de mensagem no-ack-required no SSU se não quisermos
   retransmissões de tráfego da streaming-lib. São desejáveis retransmissões com limites
   rigorosos?

5. **4)** O código de envio por prioridade na .28 é apenas para NTCP. Até agora meus testes não mostraram muito uso para prioridade SSU já que as mensagens não ficam na fila tempo suficiente para que as prioridades façam algum bem. Mas são necessários mais testes.

6. **5)** O novo timeout máximo da biblioteca de streaming de 45s provavelmente ainda é muito baixo.
   O RFC do TCP diz 60s. Provavelmente não deveria ser menor que o timeout máximo do NTCP subjacente (presumivelmente 60s).

### Resposta por jrandom {#jrandom-response}

Postado no novo Syndie, 2007-03-27

No geral, estou aberto a experimentar com isso, embora lembre-se do porquê o NTCP estar lá em primeiro lugar - o SSU falhou em um colapso de congestionamento. O NTCP "simplesmente funciona", e embora taxas de retransmissão de 2-10% possam ser tratadas em redes normais de um único salto, isso nos dá uma taxa de retransmissão de 40% com tunnels de 2 saltos. Se você incluir algumas das taxas de retransmissão do SSU medidas que vimos antes do NTCP ser implementado (10-30+%), isso nos dá uma taxa de retransmissão de 83%. Talvez essas taxas tenham sido causadas pelo baixo timeout de 10 segundos, mas aumentar tanto nos prejudicaria (lembre-se, multiplique por 5 e você tem metade da jornada).

Ao contrário do TCP, não temos feedback do tunnel para saber se a mensagem chegou ao destino - não há confirmações (ACKs) no nível do tunnel. Temos ACKs de ponta a ponta, mas apenas em um pequeno número de mensagens (sempre que distribuímos novas tags de sessão) - das 1.553.591 mensagens de cliente que meu router enviou, tentamos confirmar apenas 145.207 delas. As outras podem ter falhado silenciosamente ou ter sido bem-sucedidas.

Não estou convencido pelo argumento TCP-sobre-TCP para nós, especialmente dividido entre os vários caminhos pelos quais transferimos dados. Medições no I2P podem me convencer do contrário, é claro.

> *O timeout máximo do NTCP é presumivelmente de pelo menos 60 seg, que é a > recomendação da RFC. Não há como alterar os parâmetros do NTCP ou monitorar > o desempenho.*

Verdade, mas as conexões de rede só chegam a esse nível quando algo realmente ruim está acontecendo - o timeout de retransmissão no TCP é frequentemente da ordem de dezenas ou centenas de milissegundos. Como foofighter aponta, eles têm mais de 20 anos de experiência e correção de bugs em suas pilhas TCP, além de uma indústria de bilhões de dólares otimizando hardware e software para ter bom desempenho de acordo com o que quer que eles façam.

> *O NTCP tem maior overhead e provavelmente tempos de ida e volta mais altos. ao usar NTCP > a proporção de (saída do tunnel) / (saída de dados do i2psnark) é de pelo menos 3,5 : 1. > Executando um experimento onde o código foi modificado para preferir SSU (a opção de > configuração i2np.udp.alwaysPreferred não tem efeito no código atual), a proporção > reduziu para cerca de 3 : 1, indicando melhor eficiência.*

Estes são dados muito interessantes, embora mais como uma questão de congestionamento do router do que eficiência de largura de banda - você teria que comparar 3.5*$n*$NTCPRetransmissionPct ./. 3.0*$n*$SSURetransmissionPct. Este ponto de dados sugere que há algo no router que leva ao enfileiramento local excessivo de mensagens já sendo transferidas.

> *janela de tempo de vida aumentada de 6.3 para 7.5, RTT reduzido de 11.5s para 10s, envios por > ACK reduzidos de 1.11 para 1.07.*

Lembre-se de que o sends-per-ACK é apenas uma amostra, não uma contagem completa (já que não tentamos fazer ACK de cada envio). Também não é uma amostra aleatória, mas sim amostra mais intensamente períodos de inatividade ou o início de uma rajada de atividade - carga sustentada não requer muitos ACKs.

Tamanhos de janela nessa faixa ainda são lamentavelmente baixos para obter o benefício real do AIMD, e ainda muito baixos para transmitir um único chunk BT de 32KB (aumentar o piso para 10 ou 12 cobriria isso).

Ainda assim, a estatística wsize parece promissora - por quanto tempo ela foi mantida?

Na verdade, para fins de teste, você pode querer olhar para StreamSinkClient/StreamSinkServer ou até mesmo TestSwarm em apps/ministreaming/java/src/net/i2p/client/streaming/ - StreamSinkClient é um aplicativo CLI que envia um arquivo selecionado para um destino selecionado e StreamSinkServer cria um destino e escreve todos os dados enviados para ele (exibindo tamanho e tempo de transferência). TestSwarm combina os dois - inundando dados aleatórios para quem quer que se conecte. Isso deve fornecer as ferramentas para medir a capacidade de throughput sustentado sobre a biblioteca de streaming, em oposição ao choke/send do BT.

> *1A) Isso é fácil - > Devemos inverter as prioridades de lance para que o SSU seja preferido para todo o tráfego, se > pudermos fazer isso sem causar todos os tipos de outros problemas. Isso corrigirá a > opção de configuração i2np.udp.alwaysPreferred para que funcione (seja como true > ou false).*

Respeitar i2np.udp.alwaysPreferred é uma boa ideia em qualquer caso - fique à vontade para fazer commit dessa alteração. Vamos coletar um pouco mais de dados antes de mudar as preferências, já que o NTCP foi adicionado para lidar com um colapso de congestionamento criado pelo SSU.

> *1B) Alternativa ao 1A), não tão fácil - > Se conseguirmos marcar o tráfego sem afetar adversamente nossos objetivos de anonimato, > devemos identificar o tráfego gerado pela streaming-lib > e fazer com que o SSU gere uma oferta baixa para esse tráfego. Esta tag terá que acompanhar > a mensagem através de cada hop > para que os routers de encaminhamento também honrem a preferência SSU.*

Na prática, existem três tipos de tráfego - construção/teste de tunnel, consulta/resposta de netDb e tráfego da biblioteca de streaming. A rede foi projetada para tornar muito difícil diferenciar esses três tipos.

> *2) Limitar o SSU ainda mais (reduzindo as retransmissões máximas dos atuais > 10) provavelmente é sensato para reduzir a chance de colapso.*

Com 10 retransmissões, já estamos numa situação muito complicada, concordo. Uma, talvez duas retransmissões é razoável, do ponto de vista da camada de transporte, mas se o outro lado está muito congestionado para fazer ACK a tempo (mesmo com a capacidade SACK/NACK implementada), não há muito que possamos fazer.

Na minha opinião, para realmente abordar a questão central precisamos abordar por que o router fica tão congestionado para fazer ACK a tempo (que, pelo que descobri, é devido à contenção de CPU). Talvez possamos reorganizar algumas coisas no processamento do router para tornar a transmissão de um tunnel já existente uma prioridade de CPU mais alta do que descriptografar uma nova solicitação de tunnel? Embora tenhamos que ter cuidado para evitar starvation (privação de recursos).

> *3) Precisamos de mais estudos sobre os benefícios vs. prejuízos de um protocolo semi-confiável > subjacente à biblioteca de streaming. As retransmissões em um único salto são benéficas > e representam uma grande vitória ou são piores que inúteis? > Poderíamos criar um novo SUU (UDP não confiável seguro) mas provavelmente não vale a pena. Nós > poderíamos talvez adicionar um tipo de mensagem que não requer ACK no SSU se não quisermos > retransmissões de tráfego da biblioteca de streaming. Retransmissões > com limites rígidos são desejáveis?*

Vale a pena investigar - e se simplesmente desabilitássemos as retransmissões do SSU? Provavelmente levaria a taxas muito mais altas de reenvio da biblioteca de streaming, mas talvez não.

> *4) O código de envio prioritário no .28 é apenas para NTCP. Até agora meus testes não > mostraram muito uso para prioridade SSU, já que as mensagens não ficam em fila tempo > suficiente para que as prioridades façam algum bem. Mas são necessários mais testes.*

Há UDPTransport.PRIORITY_LIMITS e UDPTransport.PRIORITY_WEIGHT (respeitados por TimedWeightedPriorityMessageQueue), mas atualmente os pesos são quase todos iguais, então não há efeito. Isso poderia ser ajustado, é claro (mas como você menciona, se não há fila, não importa).

> *5) O novo timeout máximo da biblioteca de streaming de 45s provavelmente ainda é muito baixo. O RFC do TCP > diz 60s. Provavelmente não deveria ser menor que o timeout máximo do NTCP subjacente > (presumivelmente 60s).*

Esses 45s são o timeout máximo de retransmissão da biblioteca de streaming, não o timeout do stream. O TCP na prática tem timeouts de retransmissão ordens de magnitude menores, embora sim, possa chegar a 60s em links que passam por fios expostos ou transmissões de satélite ;) Se aumentarmos o timeout de retransmissão da biblioteca de streaming para, por exemplo, 75 segundos, poderíamos tomar uma cerveja antes de uma página web carregar (especialmente assumindo um transporte com menos de 98% de confiabilidade). Essa é uma das razões pelas quais preferimos NTCP.

### Resposta por zzz {#zzz-response}

Postado no novo Syndie, 2007-03-31

> *Com 10 retransmissões, já estamos numa situação muito complicada, concordo. Uma, talvez duas > retransmissões é razoável, de uma camada de transporte, mas se o outro lado está > muito congestionado para ACK a tempo (mesmo com a capacidade SACK/NACK implementada), > não há muito que possamos fazer.* > > *Na minha opinião, para realmente resolver a questão central precisamos abordar por que o > router fica tão congestionado para ACK a tempo (que, pelo que descobri, é devido a > contenção de CPU). Talvez possamos ajustar algumas coisas no processamento do router para > tornar a transmissão de um tunnel já existente com maior prioridade de CPU do que > descriptografar uma nova solicitação de tunnel? Embora tenhamos que ter cuidado para evitar > starvation.*

Uma das minhas principais técnicas de coleta de estatísticas é ativar net.i2p.client.streaming.ConnectionPacketHandler=DEBUG e observar os tempos de RTT e os tamanhos de janela conforme passam. Para generalizar excessivamente por um momento, é comum ver 3 tipos de conexões: ~4s RTT, ~10s RTT, e ~30s RTT. Tentar reduzir as conexões de 30s RTT é o objetivo. Se a contenção de CPU for a causa, então talvez algum malabarismo resolva.

Reduzir o SSU max retrans de 10 é realmente apenas um tiro no escuro, pois não temos bons dados sobre se estamos colapsando, tendo problemas de TCP-over-TCP, ou o que seja, então mais dados são necessários.

> *Vale a pena investigar - e se simplesmente desabilitássemos as retransmissões do SSU? Provavelmente levaria a taxas muito maiores de reenvio da biblioteca de streaming, mas talvez não.*

O que eu não entendo, se você pudesse elaborar, são os benefícios das retransmissões SSU para tráfego que não seja da streaming-lib. Precisamos que mensagens de tunnel (por exemplo) usem um transporte semi-confiável ou elas podem usar um transporte não-confiável ou meio-confiável (1 ou 2 retransmissões no máximo, por exemplo)? Em outras palavras, por que semi-confiabilidade?

> *(mas como você menciona, se não há filas de espera, não importa).*

Implementei o envio por prioridade para UDP, mas ele foi acionado cerca de 100.000 vezes menos frequentemente que o código no lado NTCP. Talvez isso seja uma pista para investigação adicional ou uma dica - não entendo por que haveria acúmulo com tanta frequência no NTCP, mas talvez isso seja uma dica sobre por que o NTCP tem desempenho pior.

### Pergunta respondida por jrandom {#jrandom-followup}

Publicado no novo Syndie, 2007-03-31

> *taxas de retransmissão SSU medidas que vimos antes do NTCP ser implementado > (10-30+%)* > > O próprio router pode medir isso? Se sim, poderia um transporte ser selecionado com base > no desempenho medido? (ou seja, se uma conexão SSU para um peer está perdendo um > número excessivo de mensagens, preferir NTCP ao enviar para esse peer)

Sim, atualmente usa essa estatística como uma detecção de MTU simplificada (se a taxa de retransmissão é alta, usa o tamanho de pacote pequeno, mas se é baixa, usa o tamanho de pacote grande). Tentamos algumas coisas quando introduzimos pela primeira vez o NTCP (e quando nos afastamos pela primeira vez do transporte TCP original) que preferiria SSU mas falharia facilmente esse transporte para um peer, fazendo com que recorresse ao NTCP. No entanto, certamente há mais que poderia ser feito nesse aspecto, embora fique complicado rapidamente (como/quando ajustar/resetar as ofertas, se deve compartilhar essas preferências entre múltiplos peers ou não, se deve compartilhá-las entre múltiplas sessões com o mesmo peer (e por quanto tempo), etc).

### Resposta por foofighter {#foofighter}

Publicado no novo Syndie, 2007-03-26

Se entendi corretamente, a razão principal a favor do TCP (em geral, tanto a variedade antiga quanto a nova) era que você não precisa se preocupar em codificar uma boa pilha TCP. O que não é impossível de acertar... é só que as pilhas TCP existentes têm uma vantagem de 20 anos.

Pelo que sei, não houve muita teoria aprofundada por trás da preferência entre TCP versus UDP, exceto pelas seguintes considerações:

- Uma rede somente TCP é muito dependente de peers alcançáveis (aqueles que podem encaminhar conexões entrantes através do seu NAT)
- Ainda assim, mesmo que peers alcançáveis sejam raros, tê-los com alta capacidade de alguma forma alivia os problemas de escassez topológica
- UDP permite "NAT hole punching" que deixa as pessoas serem "meio que pseudo-alcançáveis" (com a ajuda de introducers) que de outra forma só poderiam conectar para fora
- A implementação de transporte TCP "antiga" exigia muitas threads, o que prejudicava a performance, enquanto o transporte TCP "novo" funciona bem com poucas threads
- Routers do conjunto A falham quando saturados com UDP. Routers do conjunto B falham quando saturados com TCP.
- "Parece" (ou seja, há algumas indicações mas nenhum dado científico ou estatísticas de qualidade) que A está mais amplamente implantado que B
- Algumas redes carregam datagramas UDP não-DNS com qualidade francamente ruim, enquanto ainda se preocupam um pouco em carregar streams TCP.

Nesse contexto, uma pequena diversidade de transportes (tantos quanto necessários, mas não mais) parece sensata em ambos os casos. Qual deveria ser o transporte principal depende do seu desempenho. Já vi coisas desagradáveis na minha linha quando tentei usar sua capacidade total com UDP. Perdas de pacotes na ordem de 35%.

Poderíamos definitivamente tentar ajustar as prioridades de UDP versus TCP, mas eu recomendaria cautela nisso. Eu sugeriria que elas não sejam alteradas de forma muito radical de uma só vez, ou isso pode quebrar coisas.

### Resposta de zzz (para foofighter) {#zzz-foofighter}

Postado no novo Syndie, 2007-03-27

> *Pelo que eu saiba, não houve muita teoria aprofundada por trás da preferência entre TCP versus UDP, exceto pelas seguintes considerações:*

Essas são todas questões válidas. No entanto, você está considerando os dois protocolos isoladamente, ao invés de pensar sobre qual protocolo de transporte é melhor para um protocolo de nível superior específico (ou seja, biblioteca de streaming ou não).

O que estou dizendo é que você precisa levar a biblioteca de streaming em consideração.

Então, ou altere as preferências para todos ou trate o tráfego da biblioteca de streaming de forma diferente.

É disso que minha proposta 1B) está falando - ter uma preferência diferente para o tráfego de streaming-lib do que para o tráfego que não é de streaming-lib (por exemplo, mensagens de construção de tunnel).

> *Nesse contexto, uma pequena diversidade de transportes (tantos quantos necessários, mas não mais) parece sensata em ambos os casos. Qual deveria ser o transporte principal depende do desempenho deles. Vi coisas desagradáveis na minha linha quando tentei usar sua capacidade total com UDP. Perdas de pacotes na ordem de 35%.*

Concordo. A nova versão .28 pode ter melhorado as coisas para perda de pacotes sobre UDP, ou talvez não.

Um ponto importante - o código de transporte lembra as falhas de um transporte. Então, se UDP é o transporte preferido, ele tentará primeiro, mas se falhar para um destino específico, na próxima tentativa para esse destino ele tentará NTCP ao invés de tentar UDP novamente.

> *Poderíamos definitivamente tentar brincar com as prioridades UDP versus TCP, mas eu recomendaria > cautela nisso. Eu recomendaria que elas não sejam alteradas de forma muito radical de > uma só vez, ou isso pode quebrar as coisas.*

Temos quatro botões de ajuste - os quatro valores de lance (SSU e NTCP, para já conectado e não já conectado). Podemos fazer com que SSU seja preferido sobre NTCP apenas se ambos estiverem conectados, por exemplo, mas tentar NTCP primeiro se nenhum transporte estiver conectado.

A outra forma de fazer isso gradualmente é mudando apenas o tráfego da biblioteca de streaming (a proposta 1B), porém isso pode ser difícil e pode ter implicações de anonimato, eu não sei. Ou talvez mudar o tráfego apenas para o primeiro salto de saída (ou seja, não propagar a flag para o próximo router), o que te dá apenas benefício parcial, mas pode ser mais anônimo e mais fácil.

## Resultados da Discussão {#results}

... e outras mudanças relacionadas no mesmo período (2007):

- Ajuste significativo dos parâmetros da biblioteca de streaming,
  aumentando muito o desempenho de saída, foi implementado na versão 0.6.1.28
- Envio prioritário para NTCP foi implementado na versão 0.6.1.28
- Envio prioritário para SSU foi implementado por zzz mas nunca foi incluído
- O controle avançado de licitação de transporte
  i2np.udp.preferred foi implementado na versão 0.6.1.29.
- Pushback para NTCP foi implementado na versão 0.6.1.30, desabilitado na versão 0.6.1.31 devido a preocupações de anonimato,
  e reabilitado com melhorias para tratar essas preocupações na versão 0.6.1.32.
- Nenhuma das propostas 1-5 do zzz foi implementada.
