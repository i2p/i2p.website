---
title: "Guia de Operações de Tunnels"
description: "Especificação unificada para construir, criptografar e transportar tráfego com I2P tunnels."
slug: "implementation"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
type: docs
reviewStatus: "needs-review"
---

> **Escopo:** Este guia consolida a implementação de tunnel, o formato de mensagem e ambas as especificações de criação de tunnel (ECIES e ElGamal legado). Os links profundos existentes continuam funcionando por meio dos apelidos acima.

## Modelo de Tunnel {#tunnel-model}

I2P encaminha cargas úteis por meio de *tunnels unidirecionais*: conjuntos ordenados de routers que transportam o tráfego em uma única direção. Uma ida e volta completa entre dois destinos requer quatro tunnels (dois de saída, dois de entrada).

Comece com a [Visão geral de Tunnel](/docs/overview/tunnel-routing/) para a terminologia e, em seguida, use este guia para os detalhes operacionais.

### Ciclo de vida da mensagem {#message-lifecycle}

1. O tunnel **gateway** (porta de entrada) agrupa uma ou mais mensagens I2NP, as fragmenta e escreve instruções de entrega.
2. O gateway encapsula a carga útil em uma mensagem de tunnel de tamanho fixo (1024&nbsp;B), adicionando preenchimento se necessário.
3. Cada **participante** verifica o salto anterior, aplica sua camada de criptografia e encaminha {nextTunnelId, nextIV, encryptedPayload} para o próximo salto.
4. O tunnel **endpoint** (ponto final) remove a camada final, consome as instruções de entrega, remonta os fragmentos e despacha as mensagens I2NP reconstruídas.

A detecção de duplicatas usa um filtro de Bloom com decaimento, indexado pela XOR entre o vetor de inicialização (IV) e o primeiro bloco de cifra, para impedir ataques de marcação baseados em trocas de IV.

### Resumo dos Papéis {#roles}

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Role</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Pre-processing</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Crypto Operation</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Post-processing</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Outbound gateway (creator)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Fragment, batch, pad</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Iteratively <em>decrypt</em> using every hop’s keys (so downstream peers encrypt)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Forward to first hop</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Participant</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">—</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Encrypt IV and payload with hop keys</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Forward to next hop</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Outbound endpoint</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">—</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Encrypt once more to reveal plaintext payload</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deliver to target tunnel/destination</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Inbound gateway</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Fragment, batch, pad</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Encrypt with local keys</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Forward to next hop</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Inbound endpoint (creator)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">—</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Iteratively decrypt using stored hop keys</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reassemble and deliver locally</td>
    </tr>
  </tbody>
</table>
### Fluxo de criptografia {#encryption-workflow}

- **Inbound tunnels:** o gateway criptografa uma vez com sua chave de camada; os participantes a jusante continuam criptografando até o criador decifrar a carga útil final.
- **Outbound tunnels:** o gateway pré-aplica o inverso da criptografia de cada salto, de modo que cada participante criptografe. Quando o ponto final criptografa, o texto em claro original do gateway é revelado.

Ambas as direções encaminham `{tunnelId, IV, encryptedPayload}` para o próximo salto.

---

## Formato de Mensagem de Tunnel {#tunnel-message-format}

Os gateways de tunnel fragmentam as mensagens I2NP em envelopes de tamanho fixo para ocultar o comprimento da carga útil e simplificar o processamento em cada salto.

### Layout Criptografado {#encrypted-layout}

```
+----------------+----------------+-------------------+
| Tunnel ID (4B) | IV (16B)       | Encrypted payload |
+----------------+----------------+-------------------+
```
- **Tunnel ID** – identificador de 32 bits para o próximo salto (diferente de zero, é renovado a cada ciclo de construção).
- **IV** – IV de 16 bytes do AES escolhido por mensagem.
- **Encrypted payload** – 1008 bytes de texto cifrado em AES-256-CBC.

Tamanho total: 1028 bytes.

### Layout descriptografado {#decrypted-layout}

Depois que um salto remove sua camada de criptografia:

```
[Checksum (4B)][Padding ... 0x00 terminator]
[Delivery Instructions 1][I2NP fragment 1]
[Delivery Instructions 2][I2NP fragment 2]
...
```
- **Soma de verificação** valida o bloco descriptografado.
- **Preenchimento** são bytes aleatórios não nulos terminados por um byte zero.
- **Instruções de entrega** dizem ao ponto final como lidar com cada fragmento (entregar localmente, encaminhar para outro tunnel, etc.).
- **Fragmentos** transportam as mensagens I2NP subjacentes; o ponto final os remonta antes de passá-los para camadas superiores.

### Etapas de Processamento {#processing-steps}

1. Gateways fragmentam e enfileiram mensagens I2NP, retendo fragmentos parciais por um breve período para remontagem.
2. O gateway cifra a carga útil com as chaves de camada apropriadas e insere o tunnel ID e o IV.
3. Cada participante cifra o IV (AES-256/ECB) e depois a carga útil (AES-256/CBC), antes de recifrar o IV e encaminhar a mensagem.
4. O endpoint decifra na ordem inversa, verifica o checksum, consome as instruções de entrega e remonta os fragmentos.

---

## Criação de Tunnel (ECIES-X25519) {#tunnel-creation-ecies}

Routers modernos constroem tunnels com chaves ECIES-X25519, reduzindo o tamanho das mensagens de criação e permitindo sigilo direto.

- **Mensagem de construção:** uma única mensagem I2NP `TunnelBuild` (ou `VariableTunnelBuild`) carrega de 1–8 registros de construção criptografados, um por salto.
- **Chaves de camada:** os criadores derivam, para cada salto, as chaves de camada, IV e de resposta via HKDF, usando a identidade X25519 estática do salto e a chave efêmera do criador.
- **Processamento:** cada salto descriptografa seu registro, valida os flags da solicitação, escreve o bloco de resposta (sucesso ou código de falha detalhado), recriptografa os registros restantes e encaminha a mensagem.
- **Respostas:** o criador recebe uma mensagem de resposta garlic-wrapped (encapsulada usando garlic encryption). Registros marcados como falhos incluem um código de severidade para que o router possa traçar um perfil do par.
- **Compatibilidade:** routers ainda podem aceitar construções legadas em ElGamal para retrocompatibilidade, mas novos tunnels usam ECIES por padrão.

> Para constantes campo a campo e notas de derivação de chaves, consulte o histórico da proposta ECIES e o código-fonte do router; este guia aborda o fluxo operacional.

---

## Criação legada de Tunnel (ElGamal-2048) {#tunnel-creation-elgamal}

O formato original de construção de tunnel usava chaves públicas ElGamal. Os routers modernos mantêm suporte limitado para retrocompatibilidade.

> **Status:** Obsoleto. Mantido aqui para referência histórica e para quem mantém ferramentas compatíveis com versões legadas.

- **Telescoping não interativo:** uma única mensagem de construção percorre todo o caminho. Cada salto decifra seu registro de 528 bytes, atualiza a mensagem e a encaminha.
- **Comprimento variável:** a Variable Tunnel Build Message (VTBM, Mensagem de construção de tunnel variável) permitia 1–8 registros. A mensagem fixa anterior sempre continha oito registros para obscurecer o comprimento do tunnel.
- **Layout do registro de solicitação:**

```
Bytes 0–3    : Tunnel ID (receiving ID)
Bytes 4–35   : Current hop router hash
Bytes 36–39  : Next tunnel ID
Bytes 40–71  : Next hop router hash
Bytes 72–103 : AES-256 layer key
Bytes 104–135: AES-256 IV key
Bytes 136–167: AES-256 reply key
Bytes 168–183: AES-256 reply IV
Byte 184     : Flags (bit7=IBGW, bit6=OBEP)
Bytes 185–188: Request time (hours since epoch)
Bytes 189–192: Next message ID
Bytes 193–221: Padding
```
- **Sinalizadores:** o bit 7 indica um gateway de entrada (IBGW); o bit 6 marca uma extremidade de saída (OBEP). Eles são mutuamente exclusivos.
- **Criptografia:** cada registro é cifrado com ElGamal-2048 usando a chave pública do salto. O encadeamento simétrico em camadas com AES-256-CBC garante que apenas o salto destinado possa ler seu registro.
- **Fatos-chave:** os IDs de tunnel são valores de 32 bits não nulos; os criadores podem inserir registros fictícios para ocultar o comprimento real do tunnel; a confiabilidade depende de refazer construções de tunnel que falharam.

---

## Tunnel Pools e Ciclo de Vida {#tunnel-pools}

Routers mantêm pools de tunnel de entrada e de saída independentes para o tráfego exploratório e para cada sessão I2CP.

- **Seleção de pares:** tunnels exploratórios usam o balde de pares "ativos, sem falhas" para incentivar diversidade; tunnels de cliente preferem pares rápidos e de alta capacidade.
- **Ordenação determinística:** os pares são ordenados pela distância XOR entre `SHA256(peerHash || poolKey)` e a chave aleatória do pool. A chave é rotacionada na reinicialização, dando estabilidade dentro de uma execução enquanto dificulta ataques de predecessor entre execuções.
- **Ciclo de vida:** routers rastreiam tempos históricos de construção por tupla {modo, direção, comprimento, variância}. À medida que os tunnels se aproximam da expiração, as substituições começam cedo; o router aumenta as construções paralelas quando ocorrem falhas, enquanto limita as tentativas pendentes.
- **Ajustes de configuração:** contagens de tunnels ativos/de backup, comprimento de salto e variância, permissões de zero salto e limites de taxa de construção são todos ajustáveis por pool.

---

## Congestionamento e Confiabilidade {#congestion}

Embora tunnels se assemelhem a circuitos, routers os tratam como filas de mensagens. O Descarte Aleatório Ponderado Antecipado (WRED) é usado para manter a latência limitada:

- A probabilidade de descarte aumenta à medida que a utilização se aproxima dos limites configurados.
- Os participantes consideram fragmentos de tamanho fixo; gateways/endpoints descartam com base no tamanho combinado dos fragmentos, penalizando primeiro cargas úteis grandes.
- Os endpoints de saída descartam antes de outros papéis para desperdiçar o mínimo possível de esforço de rede.

A entrega garantida fica a cargo de camadas superiores, como a [biblioteca de streaming](/docs/specs/streaming/). As aplicações que requerem fiabilidade devem tratar elas próprias da retransmissão e das confirmações de receção.

---

## Leitura adicional {#further-reading}

- [Seleção de Pares](/docs/overview/tunnel-routing#peer-selection/)
- [Visão Geral de Tunnels](/docs/overview/tunnel-routing/)
- [Implementação Antiga de Tunnel](/docs/legacy/old-implementation/)
