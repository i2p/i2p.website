---
title: "Datagramas"
description: "Formatos de mensagem autenticados, respondíveis e brutos acima do I2CP"
slug: "datagrams"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
toc: true
---

## Visão Geral

Datagramas fornecem comunicação orientada a mensagens acima do [I2CP](/docs/specs/i2cp/) e paralela à biblioteca de streaming. Eles permitem pacotes **com capacidade de resposta**, **autenticados** ou **brutos** sem exigir fluxos orientados a conexão. Os routers encapsulam datagramas em mensagens I2NP e mensagens de túnel, independentemente de o tráfego ser transportado por NTCP2 ou SSU2.

A motivação principal é permitir que aplicações (como trackers, resolvedores DNS ou jogos) enviem pacotes autocontidos que identifiquem seu remetente.

> **Novidade em 2025:** O Projeto I2P aprovou **Datagram2 (protocolo 19)** e **Datagram3 (protocolo 20)**, adicionando proteção contra replay e mensagens respondíveis com menor sobrecarga pela primeira vez em uma década.

---

## 1. Constantes do Protocolo

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Protocol</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Value</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Introduced</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>PROTO_DATAGRAM</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">17</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Signed (repliable) datagram – “Datagram1”</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Original</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>PROTO_DATAGRAM_RAW</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">18</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Unsigned (raw) datagram – no sender info</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Original</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>PROTO_DATAGRAM2</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">19</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Signed + replay-protected datagram</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">API 0.9.66 (2025)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>PROTO_DATAGRAM3</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">20</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Repliable (no signature, hash only)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">API 0.9.66 (2025)</td>
    </tr>
  </tbody>
</table>
Os protocolos 19 e 20 foram formalizados na **Proposta 163 (Abril de 2025)**. Eles coexistem com Datagram1 / RAW para compatibilidade retroativa.

---

## 2. Tipos de Datagramas

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Protocol</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Repliable</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Authenticated</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Replay Protection</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Min Overhead</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Raw</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">18</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">No</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">No</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">No</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Minimal size; spoofable.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Datagram1</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">17</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">No</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">≈ 427</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Full Destination + signature.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Datagram2</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">19</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">≈ 457</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Replay prevention + offline signatures; PQ-ready.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Datagram3</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">20</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">No</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">No</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">≈ 34</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Sender hash only; low overhead.</td>
    </tr>
  </tbody>
</table>
### Padrões de Design Típicos

- **Requisição → Resposta:** Envie um Datagram2 assinado (requisição + nonce), receba uma resposta raw ou Datagram3 (echo nonce).  
- **Alta frequência/baixo overhead:** Prefira Datagram3 ou RAW.  
- **Mensagens de controle autenticadas:** Datagram2.  
- **Compatibilidade legada:** Datagram1 ainda totalmente suportado.

---

## 3. Detalhes do Datagram2 e Datagram3 (2025)

### Datagram2 (Protocolo 19)

Substituto aprimorado para Datagram1. Recursos: - **Prevenção de replay:** token anti-replay de 4 bytes. - **Suporte a assinatura offline:** permite uso por Destinations assinados offline. - **Cobertura de assinatura expandida:** inclui hash de destination, flags, opções, bloco de assinatura offline, payload. - **Preparado para pós-quântico:** compatível com futuros híbridos ML-KEM. - **Overhead:** ≈ 457 bytes (chaves X25519).

### Datagram3 (Protocolo 20)

Preenche a lacuna entre tipos brutos e assinados. Características: - **Replicável sem assinatura:** contém hash de 32 bytes do remetente + flags de 2 bytes. - **Sobrecarga mínima:** ≈ 34 bytes. - **Sem defesa contra replay** — a aplicação deve implementar.

Ambos os protocolos são recursos da API 0.9.66 e implementados no router Java desde a versão 2.9.0; ainda não há implementações no i2pd ou Go (outubro de 2025).

---

## 4. Limites de Tamanho e Fragmentação

- **Tamanho da mensagem tunnel:** 1 028 bytes (4 B Tunnel ID + 16 B IV + 1 008 B payload).  
- **Fragmento inicial:** 956 B (entrega TUNNEL típica).  
- **Fragmento subsequente:** 996 B.  
- **Fragmentos máximos:** 63–64.  
- **Limite prático:** ≈ 62 708 B (~61 KB).  
- **Limite recomendado:** ≤ 10 KB para entrega confiável (perdas aumentam exponencialmente além deste limite).

**Resumo de overhead:** - Datagram1 ≈ 427 B (mínimo).   - Datagram2 ≈ 457 B.   - Datagram3 ≈ 34 B.   - Camadas adicionais (cabeçalho gzip I2CP, I2NP, Garlic, Tunnel): + ~5.5 KB no pior caso.

---

## 5. Integração I2CP / I2NP

Caminho da mensagem: 1. A aplicação cria um datagrama (via API I2P ou SAM).   2. I2CP envolve com cabeçalho gzip (`0x1F 0x8B 0x08`, RFC 1952) e checksum CRC-32.   3. Números de Protocolo + Porta armazenados nos campos do cabeçalho gzip.   4. Router encapsula como mensagem I2NP → Garlic clove → fragmentos de tunnel de 1 KB.   5. Fragmentos atravessam tunnel de saída → rede → tunnel de entrada.   6. Datagrama remontado entregue ao manipulador da aplicação com base no número do protocolo.

**Integridade:** CRC-32 (do I2CP) + assinatura criptográfica opcional (Datagram1/2). Não há um campo de checksum separado dentro do próprio datagrama.

---

## 6. Interfaces de Programação

### API Java

O pacote `net.i2p.client.datagram` inclui: - `I2PDatagramMaker` – constrói datagramas assinados.   - `I2PDatagramDissector` – verifica e extrai informações do remetente.   - `I2PInvalidDatagramException` – lançada em caso de falha na verificação.

`I2PSessionMuxedImpl` (`net.i2p.client.impl.I2PSessionMuxedImpl`) gerencia a multiplexação de protocolo e porta para aplicações que compartilham um Destination.

**Acesso ao Javadoc:** - [idk.i2p Javadoc](http://idk.i2p/javadoc-i2p/) (somente rede I2P) - [Espelho do Javadoc](https://eyedeekay.github.io/javadoc-i2p/) (espelho na clearnet) - [Javadocs Oficiais](http://docs.i2p-projekt.de/javadoc/) (documentação oficial)

### Suporte SAM v3

- SAM 3.2 (2016): adicionou parâmetros PORT e PROTOCOL.  
- SAM 3.3 (2016): introduziu modelo PRIMARY/subsession; permite streams + datagramas em um Destination.  
- Suporte para estilos de sessão Datagram2 / 3 adicionado à especificação em 2025 (implementação pendente).  
- Especificação oficial: [Especificação SAM v3](/docs/api/samv3/)

### Módulos i2ptunnel

- **udpTunnel:** Base totalmente funcional para aplicações I2P UDP (`net.i2p.i2ptunnel.udpTunnel`).  
- **streamr:** Operacional para streaming A/V (`net.i2p.i2ptunnel.streamr`).  
- **SOCKS UDP:** **Não funcional** a partir da versão 2.10.0 (apenas stub UDP).

> Para UDP de uso geral, use a API Datagram ou udpTunnel diretamente—não dependa de SOCKS UDP.

---

## 7. Ecossistema e Suporte a Linguagens (2025)

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Language</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Library / Package</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">SAM Version</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Status</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Java</td><td style="border:1px solid var(--color-border); padding:0.5rem;">core API (net.i2p.client.datagram)</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.3</td><td style="border:1px solid var(--color-border); padding:0.5rem;">✓ full support</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">C++</td><td style="border:1px solid var(--color-border); padding:0.5rem;">i2pd / libsam3</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.2 partial</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Limited</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Go</td><td style="border:1px solid var(--color-border); padding:0.5rem;">go-i2p / sam3</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.1–3.2</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Python</td><td style="border:1px solid var(--color-border); padding:0.5rem;">i2plib, i2p.socket, txi2p</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.2</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Rust</td><td style="border:1px solid var(--color-border); padding:0.5rem;">i2p-rs, i2p_client</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.3</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">C#</td><td style="border:1px solid var(--color-border); padding:0.5rem;">I2PSharp</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.3</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">JS/TS</td><td style="border:1px solid var(--color-border); padding:0.5rem;">node-i2p, i2p-sam</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.2</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Haskell</td><td style="border:1px solid var(--color-border); padding:0.5rem;">network-anonymous-i2p</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.2</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Experimental</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Lua</td><td style="border:1px solid var(--color-border); padding:0.5rem;">mooni2p</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.2</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Experimental</td></tr>
  </tbody>
</table>
Java I2P é o único router que suporta subsessões completas SAM 3.3 e API Datagram2 neste momento.

---

## 8. Exemplo de Uso – Rastreador UDP (I2PSnark 2.10.0)

Primeira aplicação real do Datagram2/3:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Operation</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Datagram Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Purpose</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Announce Request</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Datagram3</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Repliable but low-overhead update</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Response</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Raw Datagram</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Minimal payload return</td></tr>
  </tbody>
</table>
O padrão demonstra o uso misto de datagramas autenticados e leves para equilibrar segurança e desempenho.

---

## 9. Segurança e Melhores Práticas

- Use Datagram2 para qualquer troca autenticada ou quando ataques de replay importarem.
- Prefira Datagram3 para respostas rápidas e replicáveis com confiança moderada.
- Use RAW para transmissões públicas ou dados anônimos.
- Mantenha payloads ≤ 10 KB para entrega confiável.
- Esteja ciente de que SOCKS UDP permanece não-funcional.
- Sempre verifique CRC gzip e assinaturas digitais no recebimento.

---

## 10. Especificação Técnica

Esta seção aborda os formatos de datagrama de baixo nível, encapsulamento e detalhes do protocolo.

### 10.1 Identificação de Protocolo

Os formatos de datagrama **não** compartilham um cabeçalho comum. Os routers não podem inferir o tipo apenas a partir dos bytes do payload.

Ao misturar vários tipos de datagrama—ou ao combinar datagramas com streaming—defina explicitamente: - O **número do protocolo** (via I2CP ou SAM) - Opcionalmente o **número da porta**, se a sua aplicação multiplexa serviços

Deixar o protocolo sem definição (`0` ou `PROTO_ANY`) é desencorajado e pode levar a erros de roteamento ou entrega.

### 10.2 Datagramas Brutos

Datagramas não respondíveis não transportam dados do remetente ou de autenticação. São cargas úteis opacas, tratadas fora da API de datagrama de nível superior, mas suportadas via SAM e I2PTunnel.

**Protocolo:** `18` (`PROTO_DATAGRAM_RAW`)

**Formato:**

```
+----+----+----+----+----//
|     payload...
+----+----+----+----+----//
```
O comprimento do payload é limitado pelos limites de transporte (≈32 KB máximo prático, frequentemente muito menor).

### 10.3 Datagram1 (Datagramas Respondíveis)

Incorpora o **Destination** do remetente e uma **Signature** para autenticação e endereçamento de resposta.

**Protocolo:** `17` (`PROTO_DATAGRAM`)

**Sobrecarga:** ≥427 bytes **Carga útil:** até ~31,5 KB (limitado pelo transporte)

**Formato:**

```
+----+----+----+----+----+----+----+----+
|               from                    |
+                                       +
|                                       |
~             Destination bytes         ~
|                                       |
+----+----+----+----+----+----+----+----+
|             signature                 |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|     payload...
+----+----+----+----//
```
- `from`: um Destination (387+ bytes)
- `signature`: uma Signature correspondente ao tipo de chave
  - Para DSA_SHA1: Signature do hash SHA-256 do payload
  - Para outros tipos de chave: Signature diretamente sobre o payload

**Notas:** - As assinaturas para tipos não-DSA foram padronizadas no I2P 0.9.14. - As assinaturas offline LS2 (Proposta 123) não são atualmente suportadas no Datagram1.

### 10.4 Formato Datagram2

Um datagrama respondível aprimorado que adiciona **resistência a replay** conforme definido na [Proposta 163](/proposals/163-datagram2/).

**Protocolo:** `19` (`PROTO_DATAGRAM2`)

A implementação está em andamento. As aplicações devem incluir verificações de nonce ou timestamp para redundância.

### 10.5 Formato Datagram3

Fornece datagramas **respondíveis mas não autenticados**. Baseia-se na autenticação de sessão mantida pelo router em vez de destino e assinatura incorporados.

**Protocolo:** `20` (`PROTO_DATAGRAM3`) **Status:** Em desenvolvimento desde 0.9.66

Útil quando: - Os destinos são grandes (por exemplo, chaves pós-quânticas) - A autenticação ocorre em outra camada - A eficiência de largura de banda é crítica

### 10.6 Integridade de Dados

A integridade do datagrama é protegida pelo **checksum gzip CRC-32** na camada I2CP. Nenhum campo de checksum explícito existe dentro do próprio formato de payload do datagrama.

### 10.7 Encapsulamento de Pacotes

Cada datagrama é encapsulado como uma única mensagem I2NP ou como um cravo individual em uma **Garlic Message**. As camadas I2CP, I2NP e tunnel tratam o comprimento e o enquadramento — não há delimitador interno ou campo de comprimento no protocolo de datagrama.

### 10.8 Considerações Pós-Quânticas (PQ)

Se a **Proposta 169** (assinaturas ML-DSA) for implementada, os tamanhos de assinatura e destino aumentarão drasticamente — de ~455 bytes para **≥3739 bytes**. Esta mudança aumentará substancialmente a sobrecarga de datagramas e reduzirá a capacidade efetiva de payload.

**Datagram3**, que depende de autenticação no nível de sessão (não assinaturas incorporadas), provavelmente se tornará o design preferido em ambientes I2P pós-quânticos.

---

## 11. Referências

- [Proposta 163 – Datagram2 e Datagram3](/proposals/163-datagram2/)
- [Proposta 160 – Integração de Tracker UDP](/proposals/160-udp-trackers/)
- [Proposta 144 – Cálculos de MTU para Streaming](/proposals/144-ecies-x25519-aead-ratchet/)
- [Proposta 169 – Assinaturas Pós-Quânticas](/proposals/169-pq-crypto/)
- [Especificação I2CP](/docs/specs/i2cp/)
- [Especificação I2NP](/docs/specs/i2np/)
- [Especificação de Mensagem de Tunnel](/docs/specs/implementation/)
- [Especificação SAM v3](/docs/api/samv3/)
- [Documentação i2ptunnel](/docs/api/i2ptunnel/)

## 12. Destaques do Registro de Alterações (2019 – 2025)

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Year</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Release</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Change</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">2019</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.43</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Datagram API stabilization</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">2021</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.50</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Protocol port handling reworked</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">2022</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2.0.0</td><td style="border:1px solid var(--color-border); padding:0.5rem;">SSU2 adoption completed</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">2024</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2.6.0</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Legacy transport removal simplified UDP code</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">2025</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2.9.0</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Datagram2/3 support added (Java API)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">2025</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2.10.0</td><td style="border:1px solid var(--color-border); padding:0.5rem;">UDP Tracker implementation released</td></tr>
  </tbody>
</table>
---

## 13. Resumo

O subsistema de datagramas agora suporta quatro variantes de protocolo oferecendo um espectro desde totalmente autenticado até transmissão bruta leve. Os desenvolvedores devem migrar para **Datagram2** para casos de uso sensíveis à segurança e **Datagram3** para tráfego respondível eficiente. Todos os tipos mais antigos permanecem compatíveis para garantir interoperabilidade de longo prazo.
