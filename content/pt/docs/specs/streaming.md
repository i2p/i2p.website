---
title: "Protocolo de Streaming"
description: "Transporte confiável, semelhante ao TCP, usado pela maioria das aplicações do I2P"
slug: "streaming"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
type: docs
---

## Visão geral

A Biblioteca de Streaming do I2P fornece entrega de dados confiável, em ordem e autenticada sobre a camada de mensagens não confiável do I2P — análoga ao TCP sobre IP. Ela é usada por quase todas as aplicações interativas do I2P, como navegação na web, IRC, e-mail e compartilhamento de arquivos.

Isso garante transmissão confiável, controle de congestionamento, retransmissão e controle de fluxo através dos tunnels anônimos de alta latência do I2P. Cada fluxo é totalmente criptografado de ponta a ponta entre os destinos.

---

## Princípios Fundamentais de Design

A biblioteca de streaming implementa um **estabelecimento de conexão em uma única fase**, em que as flags SYN, ACK e FIN podem transportar cargas úteis de dados na mesma mensagem. Isso minimiza as idas e voltas em ambientes de alta latência — uma pequena transação HTTP pode ser concluída em uma única ida e volta.

O controle de congestionamento e a retransmissão são modelados a partir do TCP, mas adaptados ao ambiente do I2P. Os tamanhos de janela são baseados em mensagens, não em bytes, e ajustados para a latência do tunnel e a sobrecarga. O protocolo oferece suporte a início lento, evitação de congestionamento e retrocesso exponencial, semelhantes ao algoritmo AIMD do TCP (Aumento Aditivo e Diminuição Multiplicativa).

---

## Arquitetura

A biblioteca de streaming opera entre as aplicações e a interface I2CP.

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Layer</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Responsibility</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Application</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Standard I2PSocket and I2PServerSocket usage</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Streaming Library</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Connection setup, sequencing, retransmission, and flow control</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>I2CP</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Tunnel creation, routing, and message handling</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>I2NP / Router Layer</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Transport through tunnels</td>
    </tr>
  </tbody>
</table>
A maioria dos usuários o acessa via I2PSocketManager, I2PTunnel ou SAMv3. A biblioteca lida de forma transparente com o gerenciamento de destinos, o uso de tunnel e as retransmissões.

---

## Formato do Pacote

```
+-----------------------------------------------+
| Send Stream ID (4B) | Receive Stream ID (4B) |
+-----------------------------------------------+
| Sequence Number (4B) | Ack Through (4B)      |
+-----------------------------------------------+
| NACK Count (1B) | optional NACK list (4B each)
+-----------------------------------------------+
| Flags (1B) | Option Size (1B) | Options ...   |
+-----------------------------------------------+
| Payload ...                                  |
```
### Detalhes do cabeçalho

- **IDs de fluxo**: Valores de 32 bits que identificam exclusivamente fluxos locais e remotos.
- **Número de sequência**: Começa em 0 para SYN (sinal de sincronização do TCP), incrementa a cada mensagem.
- **Ack Through**: Confirma todas as mensagens até N, excluindo as da lista de NACK (negação de recebimento).
- **Flags**: Máscara de bits que controla o estado e o comportamento.
- **Opções**: Lista de comprimento variável para RTT (tempo de ida e volta), MTU (unidade máxima de transmissão) e negociação de protocolo.

### Sinalizadores de chave

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Flag</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Purpose</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">SYN</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Connection initiation</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ACK</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Acknowledge received packets</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">FIN</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Graceful close</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">RST</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reset connection</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">FROM_INCLUDED</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Sender’s destination included</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">SIGNATURE_INCLUDED</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Message signed by sender</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ECHO / ECHO_REPLY</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Ping/Pong keepalive</td>
    </tr>
  </tbody>
</table>
---

## Controle de Fluxo e Confiabilidade

O Streaming usa **controle de janela baseado em mensagens**, ao contrário da abordagem baseada em bytes do TCP. O número de pacotes não confirmados permitidos em trânsito é igual ao tamanho atual da janela (padrão 128).

### Mecanismos

- **Controle de congestionamento:** Início lento e evitação baseada em AIMD (Aumento Aditivo, Diminuição Multiplicativa).  
- **Choke/Unchoke (estrangular/liberar):** Sinalização de controle de fluxo baseada na ocupação do buffer.  
- **Retransmissão:** Cálculo de RTO (tempo limite de retransmissão) baseado na RFC 6298 com backoff exponencial.  
- **Filtragem de duplicatas:** Garante confiabilidade sobre mensagens potencialmente reordenadas.

Valores típicos de configuração:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Parameter</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Default</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>maxWindowSize</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">128</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Max unacknowledged messages</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>maxMessageSize</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1730</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Maximum payload bytes per message</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>initialRTO</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">9000 ms</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Initial retransmission timeout</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>inactivityTimeout</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">90000 ms</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Idle connection timeout</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>connectTimeout</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">300000 ms</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Connection establishment timeout</td>
    </tr>
  </tbody>
</table>
---

## Estabelecimento de conexão

1. **Iniciador** envia um SYN (opcionalmente com carga útil e FROM_INCLUDED).  
2. **Respondente** responde com SYN+ACK (pode incluir carga útil).  
3. **Iniciador** envia o ACK final confirmando o estabelecimento.

Cargas úteis iniciais opcionais permitem a transmissão de dados antes da conclusão completa do handshake (negociação inicial).

---

## Detalhes de Implementação

### Retransmissão e tempo limite

O algoritmo de retransmissão segue a **RFC 6298**.   - **RTO inicial:** 9s   - **RTO mínimo:** 100ms   - **RTO máximo:** 45s   - **Alfa:** 0.125   - **Beta:** 0.25

### Compartilhamento de Bloco de Controle

Conexões recentes com o mesmo par reutilizam o RTT e os dados de janela anteriores para um ramp-up (aceleração inicial) mais rápido, evitando a latência de “cold start” (arranque a frio). Blocos de controle expiram após alguns minutos.

### MTU e Fragmentação

- MTU padrão: **1730 bytes** (acomoda duas mensagens I2NP).  
- Destinos ECIES (Esquema Integrado de Criptografia com Curvas Elípticas): **1812 bytes** (sobrecarga reduzida).  
- MTU mínimo suportado: 512 bytes.

O tamanho da carga útil exclui o cabeçalho mínimo de streaming de 22 bytes.

---

## Histórico de versões

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Router Version</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Feature</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.7.1</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Protocol numbers defined in I2CP</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.11</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Variable-length signatures</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.12</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ECDSA signature support</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.15</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Ed25519 signature support</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.18</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Ping/Pong payloads</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.20</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">FROM_INCLUDED not required in RESET</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.36</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Protocol enforcement enabled by default</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.39</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">OFFLINE_SIGNATURE support</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.58</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Bob’s hash added to NACK field in SYN</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.10.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Post-Quantum hybrid encryption (experimental)</td>
    </tr>
  </tbody>
</table>
---

## Uso em nível de aplicação

### Exemplo em Java

```java
Properties props = new Properties();
props.setProperty("i2p.streaming.maxWindowSize", "512");
I2PSocketManager mgr = I2PSocketManagerFactory.createManager(props);

I2PSocket socket = mgr.connect(destination);
InputStream in = socket.getInputStream();
OutputStream out = socket.getOutputStream();
```
### Suporte a SAMv3 e i2pd

- **SAMv3**: Fornece modos STREAM (fluxo) e DATAGRAM (datagrama) para clientes que não usam Java.  
- **i2pd**: Expõe parâmetros de streaming idênticos por meio de opções no arquivo de configuração (por exemplo, `i2p.streaming.maxWindowSize`, `profile`, etc.).

---

## Escolhendo entre Streaming e Datagramas

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Use Case</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Recommended Transport</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Reason</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">HTTP, IRC, Email</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Streaming</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Requires reliability</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">DNS</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Repliable Datagram</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Single request/response</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Telemetry, Logging</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Raw Datagram</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Best-effort acceptable</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">P2P DHT</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Datagram</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">High connection churn</td>
    </tr>
  </tbody>
</table>
---

## Segurança e Futuro Pós-Quântico

As sessões de streaming são criptografadas de ponta a ponta na camada I2CP.   A criptografia híbrida pós-quântica (ML-KEM + X25519) é suportada experimentalmente na versão 2.10.0, mas está desativada por padrão.

---

## Referências

- [Visão geral da API de Streaming](/docs/specs/streaming/)  
- [Especificação do Protocolo de Streaming](/docs/specs/streaming/)  
- [Especificação do I2CP](/docs/specs/i2cp/)  
- [Proposta 144: Cálculos de MTU para Streaming](/proposals/144-ecies-x25519-aead-ratchet/)  
- [Notas de versão do I2P 2.10.0](/pt/blog/2025/09/08/i2p-2.10.0-release/)
