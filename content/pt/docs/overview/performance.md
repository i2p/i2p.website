---
title: "Desempenho"
description: "Desempenho da rede I2P: como se comporta hoje, melhorias históricas e ideias para ajustes futuros"
slug: "performance"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
reviewStatus: "needs-review"
---

## Desempenho da Rede I2P: Velocidade, Conexões e Gestão de Recursos

A rede I2P é totalmente dinâmica. Cada cliente é conhecido por outros nós e testa localmente os nós conhecidos quanto à acessibilidade e capacidade. Apenas os nós acessíveis e capazes são salvos em um NetDB local. Durante o processo de construção de túneis, os melhores recursos são selecionados deste conjunto para construir túneis. Como os testes acontecem continuamente, o conjunto de nós muda. Cada nó I2P conhece uma parte diferente do NetDB, o que significa que cada router possui um conjunto diferente de nós I2P a serem usados para túneis. Mesmo que dois routers tenham o mesmo subconjunto de nós conhecidos, os testes de acessibilidade e capacidade provavelmente mostrarão resultados diferentes, pois os outros routers podem estar sob carga justamente quando um router testa, mas estar livres quando o segundo router testa.

Isto descreve por que cada nó I2P possui nós diferentes para construir túneis. Como cada nó I2P tem uma latência e largura de banda diferentes, os tunnels (que são construídos através desses nós) possuem valores diferentes de latência e largura de banda. E como cada nó I2P possui tunnels construídos de forma diferente, dois nós I2P nunca têm os mesmos conjuntos de túneis.

Um servidor/cliente é conhecido como "destination" e cada destination tem pelo menos um tunnel de entrada e um de saída. O padrão é 3 hops por tunnel. Isso soma 12 hops (12 nós I2P diferentes) para uma ida e volta completa cliente → servidor → cliente.

Cada pacote de dados é enviado através de 6 outros nós I2P até alcançar o servidor:

cliente - hop1 - hop2 - hop3 - hopa1 - hopa2 - hopa3 - servidor

e no caminho de volta 6 nós I2P diferentes:

servidor - hopb1 - hopb2 - hopb3 - hopc1 - hopc2 - hopc3 - cliente

O tráfego na rede precisa de um ACK antes que novos dados sejam enviados; é necessário aguardar até que um ACK retorne do servidor: enviar dados, aguardar ACK, enviar mais dados, aguardar ACK. Como o RTT (Round Trip Time) se acumula a partir da latência de cada nó I2P individual e de cada conexão nesta ida e volta, geralmente leva de 1 a 3 segundos até que um ACK retorne ao cliente. Devido ao design do TCP e do transporte I2P, um pacote de dados tem um tamanho limitado. Juntas, essas condições estabelecem um limite de largura de banda máxima por tunnel de aproximadamente 20–50 kB/s. No entanto, se apenas um salto no tunnel tiver apenas 5 kB/s de largura de banda disponível, todo o tunnel fica limitado a 5 kB/s, independentemente da latência e de outras limitações.

A criptografia, latência e como um túnel é construído torna bastante custoso em tempo de CPU construir um túnel. É por isso que um destino só tem permissão para ter no máximo 6 túneis de entrada e 6 túneis de saída para transportar dados. Com um máximo de 50 kB/s por túnel, um destino poderia usar aproximadamente 300 kB/s de tráfego combinado (na realidade poderia ser mais se túneis mais curtos forem usados com baixo ou nenhum anonimato disponível). Os túneis usados são descartados a cada 10 minutos e novos são construídos. Esta mudança de túneis, e às vezes clientes que desligam ou perdem sua conexão com a rede, às vezes irá quebrar túneis e conexões. Um exemplo disso pode ser visto na IRC2P Network na perda de conexão (ping timeout) ou ao usar eepget.

Com um conjunto limitado de destinos e um conjunto limitado de túneis por destino, um nó I2P usa apenas um conjunto limitado de túneis através de outros nós I2P. Por exemplo, se um nó I2P é "hop1" no pequeno exemplo acima, ele vê apenas um participating tunnel originando-se do cliente. Se somarmos toda a rede I2P, apenas um número bastante limitado de participating tunnels poderia ser construído com uma quantidade limitada de largura de banda no total. Se distribuirmos esses números limitados pelo número de nós I2P, há apenas uma fração da largura de banda/capacidade disponível para uso.

Para permanecer anónimo, um router não deve ser usado por toda a rede para construir túneis. Se um router atuar como router de túnel para todos os nós I2P, ele torna-se um ponto central de falha muito real, bem como um ponto central para coletar IPs e dados de clientes. É por isso que a rede distribui o tráfego através dos nós no processo de construção de túneis.

Outra consideração para o desempenho é a forma como o I2P lida com mesh networking. Cada salto de conexão (hop-to-hop) utiliza uma conexão TCP ou UDP nos nós I2P. Com 1000 conexões, observa-se 1000 conexões TCP. Isso é bastante, e alguns roteadores domésticos e de pequenos escritórios permitem apenas um número pequeno de conexões. O I2P tenta limitar essas conexões para menos de 1500 por tipo UDP e por tipo TCP. Isso limita também a quantidade de tráfego roteado através de um nó I2P.

Se um nó está acessível e possui uma configuração de largura de banda de >128 kB/s compartilhados e está acessível 24/7, ele deve ser usado após algum tempo para tráfego participante. Se ele ficar inativo no meio tempo, o teste de um nó I2P feito por outros nós irá informá-los de que não está acessível. Isso bloqueia um nó por pelo menos 24 horas em outros nós. Portanto, os outros nós que testaram aquele nó como inativo não irão usar esse nó por 24 horas para construir túneis. É por isso que seu tráfego é menor após uma reinicialização/desligamento do seu router I2P por um mínimo de 24 horas.

Além disso, outros nós I2P precisam conhecer um router I2P para testá-lo quanto à acessibilidade e capacidade. Este processo pode ser acelerado quando você interage com a rede, por exemplo, usando aplicações ou visitando sites I2P, o que resultará em mais construção de tunnels e, portanto, mais atividade e acessibilidade para testes por nós na rede.

## Histórico de Desempenho (selecionado)

Ao longo dos anos, o I2P tem apresentado várias melhorias de desempenho notáveis:

### Native math

Implementado via bindings JNI para a biblioteca GNU MP (GMP) para acelerar o `modPow` do BigInteger, que anteriormente dominava o tempo de CPU. Resultados iniciais mostraram aumentos dramáticos de velocidade na criptografia de chave pública. Veja: /misc/jbigi/

### Garlic wrapping a "reply" LeaseSet (tuned)

Anteriormente, as respostas frequentemente exigiam uma consulta ao banco de dados de rede para o LeaseSet do remetente. Agrupar o LeaseSet do remetente no garlic inicial melhora a latência de resposta. Isso agora é feito seletivamente (início de uma conexão ou quando o LeaseSet muda) para reduzir a sobrecarga.

### Matemática nativa

Movidos alguns passos de validação para antes no handshake de transporte para rejeitar peers ruins mais cedo (relógios incorretos, NAT/firewall inadequado, versões incompatíveis), economizando CPU e largura de banda.

### Envolvendo com garlic um LeaseSet de "resposta" (ajustado)

Use testes de túnel conscientes do contexto: evite testar túneis que já se sabe estarem passando dados; priorize testes quando ociosos. Isso reduz a sobrecarga e acelera a detecção de túneis com falhas.

### Rejeição TCP mais eficiente

Manter as seleções para uma determinada conexão reduz a entrega fora de ordem e permite que a biblioteca de streaming aumente o tamanho das janelas, melhorando o throughput.

### Ajustes de teste de túnel

GZip ou similar para estruturas verbosas (por exemplo, opções de RouterInfo) reduz a largura de banda onde apropriado.

### Seleção persistente de túnel/lease

Substituto para o protocolo simplista "ministreaming". O streaming moderno inclui ACKs seletivos e controle de congestionamento adaptado ao substrato anônimo e orientado a mensagens do I2P. Veja: /docs/api/streaming/

## Future Performance Improvements (historical ideas)

Abaixo estão ideias documentadas historicamente como potenciais melhorias. Muitas estão obsoletas, implementadas ou substituídas por mudanças arquiteturais.

### Comprimir estruturas de dados selecionadas

Melhorar como os routers escolhem peers para construção de túneis para evitar aqueles lentos ou sobrecarregados, mantendo-se resistente a ataques Sybil por adversários poderosos.

### Protocolo de streaming completo

Reduza a exploração desnecessária quando o espaço de chaves estiver estável; ajuste quantos peers são retornados nas consultas e quantas pesquisas simultâneas são realizadas.

### Session Tag tuning and improvements (legacy)

Para o esquema legado ElGamal/AES+SessionTag, estratégias mais inteligentes de expiração e reabastecimento reduzem os fallbacks de ElGamal e tags desperdiçadas.

### Melhor perfil e seleção de pares

Gerar tags a partir de um PRNG sincronizado inicializado durante o estabelecimento de uma nova sessão, reduzindo a sobrecarga por mensagem das tags pré-entregues.

### Ajuste da base de dados de rede

Tempos de vida de túnel mais longos aliados à recuperação podem reduzir as sobrecargas de reconstrução; equilibre com anonimato e confiabilidade.

### Ajuste e melhorias de Session Tag (legado)

Rejeitar peers inválidos mais cedo e tornar os testes de tunnel mais sensíveis ao contexto para reduzir contenção e latência.

### Migrar SessionTag para PRNG sincronizado (legado)

O agrupamento seletivo de LeaseSet, as opções comprimidas de RouterInfo e a adoção do protocolo de streaming completo contribuem para um melhor desempenho percebido.

---

Veja também:

- [Roteamento de Túneis](/docs/overview/tunnel-routing/)
- [Seleção de Pares](/docs/overview/tunnel-routing/)
- [Transportes](/docs/overview/transport/)
- [Especificação SSU2](/docs/specs/ssu2/) e [Especificação NTCP2](/docs/specs/ntcp2/)
