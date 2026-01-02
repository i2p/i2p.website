---
title: "Discussão sobre NTCP"
description: "Notas históricas comparando os transportes NTCP e SSU e propostas de ajuste fino"
slug: "ntcp"
layout: "single"
reviewStatus: "needs-review"
---

## NTCP vs. SSU Debate (março de 2007)

### Perguntas sobre NTCP

_Adaptado de uma conversa no IRC entre zzz e cervantes._

- **Por que o NTCP tem prioridade sobre o SSU quando o NTCP parece adicionar sobrecarga e latência?**  
  O NTCP geralmente oferece melhor confiabilidade do que a implementação original do SSU.
- **O streaming sobre NTCP incorre no colapso clássico de TCP sobre TCP?**  
  Possivelmente, mas o SSU foi concebido para ser a opção leve baseada em UDP e mostrou-se pouco confiável na prática.

### “NTCP considerado prejudicial” (zzz, 25 de março de 2007)

Resumo: a maior latência e a sobrecarga do NTCP podem causar congestionamento, ainda assim, o roteamento prefere NTCP porque suas pontuações de lance são hard-coded (codificado fixo) como menores do que as do SSU. A análise levantou vários pontos:

- Atualmente, o NTCP faz um lance (bid) menor do que o SSU, portanto os routers preferem o NTCP, a menos que uma sessão SSU já esteja estabelecida.
- O SSU implementa confirmações (ACKs) com tempos limite (timeouts) estritamente limitados e coleta de estatísticas; o NTCP depende do Java NIO TCP com tempos limite ao estilo RFC que podem ser muito mais longos.
- A maior parte do tráfego (HTTP, IRC, BitTorrent) usa a biblioteca de streaming do I2P, efetivamente empilhando TCP sobre NTCP. Quando ambas as camadas retransmitem, é possível ocorrer colapso. Referências clássicas incluem [TCP sobre TCP é uma má ideia](http://sites.inka.de/~W1011/devel/tcp-tcp.html).
- Os tempos limite da biblioteca de streaming aumentaram de 10 s para 45 s na versão 0.8; o tempo limite máximo do SSU é 3 s, enquanto os tempos limite do NTCP presumivelmente se aproximam de 60 s (recomendação da RFC). Os parâmetros do NTCP são difíceis de inspecionar externamente.
- Observações de campo em 2007 mostraram a taxa de upload do i2psnark oscilando, sugerindo colapso de congestionamento periódico.
- Testes de eficiência (forçando preferência por SSU) reduziram as razões de overhead do tunnel de aproximadamente 3.5:1 para 3:1 e melhoraram métricas de streaming (tamanho de janela, RTT, relação envio/ack).

#### Propostas do tópico de 2007

1. **Inverter as prioridades de transporte** para que routers prefiram SSU (restaurando `i2np.udp.alwaysPreferred`).
2. **Marcar o tráfego de streaming** para que o SSU atribua prioridade menor apenas às mensagens marcadas, sem comprometer o anonimato.
3. **Restringir os limites de retransmissão do SSU** para reduzir o risco de colapso.
4. **Estudar underlays (camadas subjacentes da rede) semi-confiáveis** para determinar se retransmissões abaixo da biblioteca de streaming trazem benefício líquido.
5. **Revisar filas de prioridade e tempos limite**—por exemplo, aumentar os tempos limite de streaming além de 45 s para alinhar com o NTCP.

### Resposta de jrandom (27 de março de 2007)

Principais contrapontos:

- NTCP existe porque as primeiras implantações de SSU sofreram colapso por congestionamento. Mesmo taxas modestas de retransmissão por salto podem explodir ao longo de tunnels multi-salto.
- Sem confirmações em nível de tunnel, apenas uma fração das mensagens recebe status de entrega fim a fim; falhas podem ser silenciosas.
- O controle de congestionamento do TCP tem décadas de otimizações; o NTCP aproveita isso por meio de pilhas TCP maduras.
- Os ganhos de eficiência observados ao preferir SSU podem refletir o comportamento de enfileiramento do router, em vez de vantagens intrínsecas do protocolo.
- Timeouts de streaming maiores já estavam melhorando a estabilidade; recomendou-se mais observação e dados antes de mudanças significativas.

O debate ajudou a aprimorar os ajustes de transporte posteriores, mas não reflete a arquitetura moderna NTCP2/SSU2 (protocolos de transporte do I2P).
