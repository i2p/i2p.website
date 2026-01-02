---
title: "Protocolo de Streaming"
description: "Transporte similar ao TCP usado pela maioria das aplicações I2P"
slug: "streaming"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

## Visão Geral

A **I2P Streaming Library** fornece transporte confiável, ordenado e autenticado sobre a camada de mensagens do I2P, semelhante ao **TCP sobre IP**. Ela fica acima do [protocolo I2CP](/docs/specs/i2cp/) e é usada por quase todas as aplicações interativas do I2P, incluindo proxies HTTP, IRC, BitTorrent e email.

### Características Principais

- Configuração de conexão em uma fase usando flags **SYN**, **ACK** e **FIN** que podem ser agrupadas com dados de payload para reduzir ida e volta.
- **Controle de congestionamento por janela deslizante**, com início lento e prevenção de congestionamento ajustados para o ambiente de alta latência do I2P.
- Compressão de pacotes (segmentos comprimidos de 4KB por padrão) equilibrando custo de retransmissão e latência de fragmentação.
- Abstração de canal totalmente **autenticado, criptografado** e **confiável** entre destinos I2P.

Este design permite que pequenas requisições e respostas HTTP sejam concluídas em uma única ida e volta. Um pacote SYN pode transportar a carga útil da requisição, enquanto o SYN/ACK/FIN do respondedor pode conter o corpo completo da resposta.

---

## Conceitos Básicos da API

A API de streaming Java espelha a programação padrão de sockets Java:

```java
I2PSocketManager mgr = I2PSocketManagerFactory.createManager(host, port, options);
I2PSocket socket       = mgr.connect(destination);
I2PServerSocket server = mgr.getServerSocket();
```
- `I2PSocketManagerFactory` negocia ou reutiliza uma sessão de router via I2CP.  
- Se nenhuma chave for fornecida, um novo destino é gerado automaticamente.  
- Desenvolvedores podem passar opções I2CP (por exemplo, comprimentos de tunnel, tipos de criptografia ou configurações de conexão) através do mapa `options`.  
- `I2PSocket` e `I2PServerSocket` espelham as interfaces padrão `Socket` do Java, tornando a migração direta.

Os Javadocs completos estão disponíveis no console do roteador I2P ou [aqui](/docs/specs/streaming/).

---

## Configuração e Ajuste

Você pode passar propriedades de configuração ao criar um gerenciador de socket através de:

```java
I2PSocketManagerFactory.createManager(host, port, properties);
```
### Opções de Chave

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Option</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Description</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Default</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>i2p.streaming.maxWindowSize</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Maximum send window (bytes)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">128 KB</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>i2p.streaming.initialRTO</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Initial retransmission timeout</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">9s</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>i2p.streaming.inactivityTimeout</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Timeout before connection close</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">90s</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>i2p.streaming.enforceProtocol</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Enforce protocol ID (prevents confusion)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">true</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>i2p.streaming.congestionAlgorithm</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Congestion control method</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Default (AIMD TCP-like)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>i2p.streaming.disableRejectLogging</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Disable logging rejected packets</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">false</td>
    </tr>
  </tbody>
</table>
### Comportamento por Carga de Trabalho

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Workload</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Recommended Settings</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>HTTP-like</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Default parameters are ideal.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Bulk Transfer</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Increase window size to 256 KB or 512 KB; lengthen timeouts.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Real-time Streaming</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Lower tunnel length to 1-2 hops; adjust RTO downwards.</td>
    </tr>
  </tbody>
</table>
Recursos mais recentes desde a versão 0.9.4 incluem supressão de log de rejeição, suporte à lista DSA (0.9.21) e aplicação obrigatória de protocolo (0.9.36). Routers desde a versão 2.10.0 incluem criptografia híbrida pós-quântica (ML-KEM + X25519) na camada de transporte.

---

## Detalhes do Protocolo

Cada stream é identificado por um **Stream ID**. Os pacotes transportam sinalizadores de controle semelhantes ao TCP: `SYNCHRONIZE`, `ACK`, `FIN` e `RESET`. Os pacotes podem conter simultaneamente dados e sinalizadores de controle, melhorando a eficiência para conexões de curta duração.

### Ciclo de Vida da Conexão

1. **SYN enviado** — o iniciador inclui dados opcionais.  
2. **Resposta SYN/ACK** — o respondedor inclui dados opcionais.  
3. **Finalização ACK** — estabelece confiabilidade e estado de sessão.  
4. **FIN/RESET** — usado para fechamento ordenado ou terminação abrupta.

### Fragmentação e Reordenação

Como os túneis I2P introduzem latência e reordenação de mensagens, a biblioteca armazena em buffer os pacotes de streams desconhecidos ou que chegam antecipadamente. As mensagens armazenadas em buffer são mantidas até que a sincronização seja concluída, garantindo entrega completa e em ordem.

### Aplicação de Protocolo

A opção `i2p.streaming.enforceProtocol=true` (padrão desde a versão 0.9.36) garante que as conexões usem o número de protocolo I2CP correto, prevenindo conflitos entre múltiplos subsistemas que compartilham um mesmo destino.

---

## Interoperabilidade e Boas Práticas

O protocolo de streaming coexiste com a **API de Datagramas**, dando aos desenvolvedores a escolha entre transportes orientados a conexão e sem conexão.

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Use Case</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Recommended Transport</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reliable, ordered data (HTTP, IRC, FTP)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Streaming</strong></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Connectionless or lossy data (DNS, telemetry)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Datagram</strong></td>
    </tr>
  </tbody>
</table>
### Clientes Compartilhados

As aplicações podem reutilizar túneis existentes executando como **clientes compartilhados**, permitindo que múltiplos serviços compartilhem o mesmo destino. Embora isso reduza a sobrecarga, aumenta o risco de correlação entre serviços—use com cuidado.

### Controle de Congestionamento

- A camada de streaming se adapta continuamente à latência e vazão da rede através de feedback baseado em RTT.
- As aplicações têm melhor desempenho quando os routers são peers contribuintes (túneis participantes habilitados).
- Mecanismos de controle de congestionamento semelhantes ao TCP previnem a sobrecarga de peers lentos e ajudam a equilibrar o uso de largura de banda através dos túneis.

### Considerações sobre Latência

Como o I2P adiciona várias centenas de milissegundos de latência base, as aplicações devem minimizar as viagens de ida e volta. Agrupe dados com a configuração de conexão sempre que possível (por exemplo, requisições HTTP no SYN). Evite designs que dependam de muitas trocas sequenciais pequenas.

---

## Testes e Compatibilidade

- Sempre teste contra **Java I2P** e **i2pd** para garantir compatibilidade total.
- Embora o protocolo seja padronizado, pequenas diferenças de implementação podem existir.
- Lide com routers mais antigos de forma adequada—muitos peers ainda executam versões anteriores à 2.0.
- Monitore estatísticas de conexão usando `I2PSocket.getOptions()` e `getSession()` para ler métricas de RTT e retransmissão.

O desempenho depende fortemente da configuração do tunnel:   - **Tunnels curtos (1–2 hops)** → menor latência, anonimato reduzido.   - **Tunnels longos (3+ hops)** → maior anonimato, RTT aumentado.

---

## Melhorias Principais (2.0.0–2.10.0)

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Feature</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Introduced</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Persistent ACK Bundling</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.0.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Optimized round-trip reduction for HTTP workloads.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Adaptive Window Scaling</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.3.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Improved large file transfer stability.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Thread Pooling and Socket Reuse</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.5.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reduced per-connection overhead.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Protocol Enforcement Default</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.36</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Ensures correct stream usage.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Hybrid ML-KEM Ratchet</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.10.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Adds post-quantum hybrid encryption layer.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>i2pd Streaming API Compatibility Fixes</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.9.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Full parity with Java I2P library behavior.</td>
    </tr>
  </tbody>
</table>
---

## Resumo

A **Biblioteca de Streaming I2P** é a espinha dorsal de toda comunicação confiável dentro do I2P. Ela garante entrega de mensagens ordenada, autenticada e criptografada, e fornece uma substituição quase direta para TCP em ambientes anônimos.

Para obter desempenho ideal: - Minimize idas e voltas com agrupamento SYN+payload.   - Ajuste os parâmetros de janela e timeout para sua carga de trabalho.   - Prefira tunnels mais curtos para aplicações sensíveis à latência.   - Use designs amigáveis ao congestionamento para evitar sobrecarregar peers.
