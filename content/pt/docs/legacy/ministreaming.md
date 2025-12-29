---
title: "Biblioteca de Ministreaming"
description: "Notas históricas sobre a primeira camada de transporte semelhante ao TCP do I2P"
slug: "ministreaming"
lastUpdated: "2025-02"
accurateFor: "historical"
---

> **Obsoleto:** A biblioteca ministreaming é anterior à [biblioteca de streaming](/docs/specs/streaming/) atual. Aplicações modernas devem usar a API de streaming completa ou SAM v3. As informações abaixo são mantidas para desenvolvedores que revisam código-fonte legado distribuído em `ministreaming.jar`.

## Visão geral

Ministreaming (uma camada de streaming minimalista) opera sobre o [I2CP](/docs/specs/i2cp/) para fornecer entrega confiável e em ordem na camada de mensagens do I2P—de forma semelhante ao TCP sobre IP. Ele foi originalmente extraído do aplicativo **I2PTunnel** inicial (sob licença BSD) para que transportes alternativos pudessem evoluir de forma independente.

Principais restrições de projeto:

- Estabelecimento de conexão clássico em duas fases (SYN/ACK/FIN) emprestado do TCP
- Tamanho de janela fixo de **1** pacote
- Sem identificadores por pacote nem confirmações seletivas

Essas escolhas mantiveram a implementação pequena, mas limitam a vazão—cada pacote geralmente espera quase dois RTT (tempo de ida e volta) antes que o próximo seja enviado. Para fluxos de longa duração, a penalidade é aceitável, mas trocas curtas no estilo HTTP sofrem de forma perceptível.

## Relação com a Biblioteca de Streaming

A biblioteca de streaming atual permanece no mesmo pacote Java (`net.i2p.client.streaming`). Classes e métodos obsoletos permanecem na documentação Javadoc, claramente anotados para que os desenvolvedores possam identificar APIs da era do ministreaming (implementação anterior minimalista de streaming). Quando a biblioteca de streaming substituiu o ministreaming, ela adicionou:

- Configuração de conexão mais inteligente, com menos viagens de ida e volta
- Janelas de congestionamento adaptativas e lógica de retransmissão
- Melhor desempenho em tunnels com perdas

## Quando o Ministreaming (biblioteca de streaming mínima do I2P) foi útil?

Apesar de suas limitações, ministreaming (mecanismo de streaming minimalista) fornecia um transporte confiável nas primeiras implantações. A API foi intencionalmente pequena e preparada para o futuro, de modo que mecanismos alternativos de streaming pudessem ser trocados sem quebrar o código chamador. Aplicações Java o integravam diretamente; clientes não-Java acessavam a mesma funcionalidade por meio do suporte do [SAM](/docs/legacy/sam/) a sessões de streaming.

Hoje, considere `ministreaming.jar` apenas como uma camada de compatibilidade. Novos desenvolvimentos devem:

1. Tenha como alvo a biblioteca completa de streaming (Java) ou o SAM v3 (estilo `STREAM`)  
2. Remova quaisquer pressupostos remanescentes de janela fixa ao modernizar o código  
3. Prefira tamanhos de janela maiores e handshakes de conexão otimizados para melhorar cargas de trabalho sensíveis à latência

## Referência

- [Documentação da Biblioteca de Streaming](/docs/specs/streaming/)
- [Javadoc de Streaming](http://idk.i2p/javadoc-i2p/net/i2p/client/streaming/package-summary.html) – inclui classes de ministreaming (implementação mínima de streaming) obsoletas
- [Especificação do SAM v3](/docs/api/samv3/) – suporte de streaming para aplicações não Java

Se você encontrar código que ainda depende de ministreaming (biblioteca de streaming antiga do I2P), planeje portá-lo para a API de streaming moderna — a rede e suas ferramentas esperam o comportamento mais recente.
