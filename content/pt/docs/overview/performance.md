---
title: "Performance"
description: "Desempenho da rede I2P: velocidade, conexões e gerenciamento de recursos"
slug: "performance"
aliases:
  - "/pt/about/performance/future"
  - "/pt/about/performance/future/"
  - "/pt/about/performance/history"
  - "/pt/about/performance/history/"
  - "/pt/performance"
  - "/pt/performance/"
  - "/pt/performance-history"
  - "/pt/performance-history/"
  - "/pt/benchmarks"
  - "/pt/benchmarks/"
lastUpdated: "2025-01"
accurateFor: "0.9.65"
---

## Desempenho da Rede I2P: Velocidade, Conexões e Gerenciamento de Recursos

A rede I2P é totalmente dinâmica. Cada cliente é conhecido por outros nós e testa nós conhecidos localmente quanto à acessibilidade e capacidade. Apenas nós acessíveis e capazes são salvos em um NetDB local. Durante o processo de construção de tunnel, os melhores recursos são selecionados desta pool para construir tunnels. Como os testes acontecem continuamente, a pool de nós muda. Cada nó I2P conhece uma parte diferente do NetDB, significando que cada router tem um conjunto diferente de nós I2P para serem usados em tunnels. Mesmo se dois routers tiverem o mesmo subconjunto de nós conhecidos, os testes de acessibilidade and capacidade provavelmente mostrarão resultados diferentes, já que os outros routers poderiam estar sob carga justamente quando um router testa, mas estar livres quando o segundo router testa.

Isso descreve por que cada nó I2P tem nós diferentes para construir tunnels. Como cada nó I2P tem latência e largura de banda diferentes, os tunnels (que são construídos através desses nós) têm valores de latência e largura de banda diferentes. E como cada nó I2P tem tunnels diferentes construídos, nenhum dos dois nós I2P têm os mesmos conjuntos de tunnels.

Um servidor/cliente é conhecido como um "destination" e cada destination tem pelo menos um tunnel de entrada e um de saída. O padrão é 3 saltos por tunnel. Isso totaliza 12 saltos (ou seja, 12 nós I2P diferentes) para uma viagem completa de ida e volta cliente-servidor-cliente.

Cada pacote de dados é enviado através de 6 outros nós I2P até chegar ao servidor:

```
client - hop1 - hop2 - hop3 - hopa1 - hopa2 - hopa3 - server
```
e no caminho de volta 6 nós I2P diferentes:

```
server - hopb1 - hopb2 - hopb3 - hopc1 - hopc2 - hopc3 - client
```
O tráfego na rede precisa de um ACK antes que novos dados sejam enviados, precisa aguardar até que um ACK retorne de um servidor: enviar dados, aguardar ACK, enviar mais dados, aguardar ACK. Como o RTT (RoundTripTime - Tempo de Ida e Volta) se acumula a partir da latência de cada nó I2P individual e cada conexão nesta ida e volta, geralmente leva de 1-3 segundos até que um ACK volte para o cliente. Devido ao design do transporte TCP e I2P, um pacote de dados tem um tamanho limitado. Juntas, essas condições estabelecem um limite máximo de largura de banda por tunnel de 20-50 kbyte/seg. No entanto, se APENAS UM salto no tunnel tem apenas 5 kb/seg de largura de banda para gastar, todo o tunnel fica limitado a 5 kb/seg, independentemente da latência e outras limitações.

A criptografia, latência e como um tunnel é construído torna bastante caro em tempo de CPU construir um tunnel. É por isso que um destino só pode ter um máximo de 6 tunnels IN e 6 tunnels OUT para transportar dados. Com um máximo de 50 kb/s por tunnel, um destino pode usar aproximadamente 300 kb/s de tráfego combinado (na realidade pode ser mais se tunnels mais curtos forem usados com baixo ou nenhum anonimato disponível). Os tunnels usados são descartados a cada 10 minutos e novos são construídos. Esta mudança de tunnels, e às vezes clientes que desligam ou perdem sua conexão com a rede, às vezes quebram tunnels e conexões. Um exemplo disso pode ser visto na IRC2P Network na perda de conexão (ping timeout) ou ao usar eepget.

Com um conjunto limitado de destinos e um conjunto limitado de tunnels por destino, um nó I2P usa apenas um conjunto limitado de tunnels através de outros nós I2P. Por exemplo, se um nó I2P é "hop1" no pequeno exemplo acima, vemos apenas 1 tunnel participante originando do cliente. Se somarmos toda a rede I2P, apenas um número bastante limitado de tunnels participantes poderia ser construído com uma quantidade limitada de largura de banda no total. Se distribuirmos esses números limitados pelo número de nós I2P, há apenas uma fração da largura de banda/capacidade disponível para uso.

Para manter o anonimato, um router não deve ser usado por toda a rede para construir tunnels. Se um router atuar como router de tunnel para TODOS os nós I2P, torna-se um ponto central de falha muito real, bem como um ponto central para coletar IPs e dados dos clientes. É por isso que a rede distribui o tráfego entre os nós no processo de construção de tunnels.

Outra consideração para o desempenho é a forma como o I2P lida com redes mesh. Cada salto de conexão utiliza uma conexão TCP ou UDP nos nós I2P. Com 1000 conexões, observa-se 1000 conexões TCP. Isso é bastante, e alguns roteadores domésticos e de pequenos escritórios permitem apenas um pequeno número de conexões. O I2P tenta limitar essas conexões a menos de 1500 por tipo UDP e por tipo TCP. Isso também limita a quantidade de tráfego roteado através de um nó I2P.

Se um nó é acessível, tem uma configuração de largura de banda >128 kbyte/seg compartilhados e é acessível 24/7, ele deve ser usado após algum tempo para tráfego participante. Se ele ficar fora do ar no meio tempo, o teste de um nó I2P feito por outros nós irá informá-los que ele não é acessível. Isso bloqueia um nó por pelo menos 24 horas em outros nós. Então, os outros nós que testaram aquele nó como fora do ar não usarão aquele nó por 24 horas para construir tunnels. É por isso que seu tráfego é menor após um reinício/desligamento do seu router I2P por um mínimo de 24 horas.

Além disso, outros nós I2P precisam conhecer um I2P router para testá-lo quanto à acessibilidade e capacidade. Este processo pode ser acelerado quando você interage com a rede, por exemplo, usando aplicações ou visitando sites I2P, o que resultará em mais construção de tunnels e, portanto, mais atividade e acessibilidade para testes pelos nós da rede.

---

## Melhorias de Performance

Para possíveis melhorias futuras de desempenho, consulte [Melhorias Futuras de Desempenho](/docs/overview/performance#future).

Para melhorias de desempenho anteriores, consulte o [Histórico de Desempenho](/docs/overview/performance#history).
