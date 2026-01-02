---
title: "Roteamento Garlic"
description: "Compreendendo a terminologia, arquitetura e implementação moderna do garlic routing no I2P"
slug: "garlic-routing"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

---

## 1. Visão Geral

**Garlic routing** permanece como uma das inovações centrais do I2P, combinando criptografia em camadas, agrupamento de mensagens e túneis unidirecionais. Embora conceitualmente semelhante ao **onion routing**, ele estende o modelo para agrupar múltiplas mensagens criptografadas ("cloves") em um único envelope ("garlic"), melhorando eficiência e anonimato.

O termo *garlic routing* foi cunhado por [Michael J. Freedman](https://www.cs.princeton.edu/~mfreed/) na [Tese de Mestrado Free Haven de Roger Dingledine](https://www.freehaven.net/papers.html) (junho de 2000, §8.1.1). Os desenvolvedores do I2P adotaram o termo no início dos anos 2000 para refletir suas melhorias de empacotamento e modelo de transporte unidirecional, distinguindo-o do design de comutação de circuito do Tor.

> **Resumo:** Garlic routing = criptografia em camadas + agrupamento de mensagens + entrega anônima através de túneis unidirecionais.

---

## 2. A Terminologia "Garlic"

Historicamente, o termo *garlic* tem sido usado em três contextos diferentes dentro do I2P:

1. **Criptografia em camadas** – proteção estilo onion ao nível do tunnel  
2. **Agrupamento de múltiplas mensagens** – múltiplos "cloves" dentro de uma "garlic message"  
3. **Criptografia ponta a ponta** – anteriormente *ElGamal/AES+SessionTags*, agora *ECIES‑X25519‑AEAD‑Ratchet*

Embora a arquitetura permaneça intacta, o esquema de criptografia foi completamente modernizado.

---

## 3. Criptografia em Camadas

O garlic routing compartilha seu princípio fundamental com o roteamento cebola: cada router descriptografa apenas uma camada de criptografia, conhecendo apenas o próximo salto e não o caminho completo.

No entanto, o I2P implementa **túneis unidirecionais**, não circuitos bidirecionais:

- **Túnel de saída (Outbound tunnel)**: envia mensagens para longe do criador  
- **Túnel de entrada (Inbound tunnel)**: transporta mensagens de volta para o criador

Uma ida e volta completa (Alice ↔ Bob) usa quatro tunnels: outbound de Alice → inbound de Bob, depois outbound de Bob → inbound de Alice. Este design **reduz pela metade a exposição de dados de correlação** em comparação com circuitos bidirecionais.

Para detalhes da implementação de tunnel, consulte a [Especificação de Tunnel](/docs/specs/implementation) e a especificação de [Criação de Tunnel (ECIES)](/docs/specs/implementation).

---

## 4. Agrupamento de Múltiplas Mensagens (Os "Cloves")

O garlic routing original de Freedman previa agrupar múltiplos "bulbos" criptografados dentro de uma mensagem. O I2P implementa isso como **cloves** (dentes de alho) dentro de uma **garlic message** (mensagem garlic) — cada clove tem suas próprias instruções de entrega criptografadas e destino (router, destination ou tunnel).

O garlic bundling permite que o I2P:

- Combinar confirmações e metadados com mensagens de dados  
- Reduzir padrões de tráfego observáveis  
- Suportar estruturas de mensagem complexas sem conexões extras

![Garlic Message Cloves](/images/garliccloves.png)   *Figura 1: Uma Garlic Message contendo múltiplos cloves (dentes), cada um com suas próprias instruções de entrega.*

Os dentes típicos incluem:

1. **Mensagem de Status de Entrega** — confirmações que atestam sucesso ou falha na entrega.  
   Estas são encapsuladas em sua própria camada garlic para preservar confidencialidade.
2. **Mensagem de Armazenamento de Banco de Dados** — LeaseSets agrupados automaticamente para que os pares possam responder sem consultar novamente o netDb.

Os cravo-da-índias são agrupados quando:

- Um novo LeaseSet deve ser publicado  
- Novas tags de sessão são entregues  
- Nenhum agrupamento ocorreu recentemente (~1 minuto por padrão)

Mensagens garlic alcançam entrega eficiente ponta-a-ponta de múltiplos componentes criptografados em um único pacote.

---

## 5. Evolução da Criptografia

### 5.1 Historical Context

A documentação inicial (≤ v0.9.12) descreveu a encriptação *ElGamal/AES+SessionTags*:   - **ElGamal 2048‑bit** para encapsular chaves de sessão AES   - **AES‑256/CBC** para encriptação de payload   - session tags de 32 bytes utilizadas uma vez por mensagem

Esse sistema criptográfico está **descontinuado**.

### 5.2 ECIES‑X25519‑AEAD‑Ratchet (Current Standard)

Entre 2019 e 2023, o I2P migrou completamente para ECIES‑X25519‑AEAD‑Ratchet. A stack moderna padroniza os seguintes componentes:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Layer</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">ECIES Primitive or Concept</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Transport Layer (NTCP2, SSU2)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Noise_NX → X25519, ChaCha20/Poly1305, BLAKE2s</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">I2NP Delivery</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ECIES‑X25519‑AEAD (ChaCha20/Poly1305)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Session Management</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Ratchet with rekey records, per-clove key material</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Offline Authentication</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">EdDSA (Ed25519) with LeaseSet2/MetaLeaseSet chains</td>
    </tr>
  </tbody>
</table>
Benefícios da migração ECIES:

- **Sigilo futuro** via chaves de ratcheting por mensagem  
- **Tamanho de payload reduzido** comparado ao ElGamal  
- **Resiliência** contra avanços criptoanalíticos  
- **Compatibilidade** com futuros híbridos pós-quânticos (veja Proposta 169)

Detalhes adicionais: consulte a [Especificação ECIES](/docs/specs/ecies) e a [especificação EncryptedLeaseSet](/docs/specs/encryptedleaseset).

---

## 6. LeaseSets and Garlic Bundling

Os envelopes garlic frequentemente incluem LeaseSets para publicar ou atualizar a acessibilidade do destino.

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Version</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Key Capabilities</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Distribution Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">LeaseSet (legacy)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Single encryption/signature pair</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Accepted for backward compatibility</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">3</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">LeaseSet2</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Multiple crypto suites, offline signing keys</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Default for modern routers</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">5</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">EncryptedLeaseSet</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Access-controlled, destination hidden from floodfill</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Requires shared decryption key</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">7</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MetaLeaseSet</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Aggregates multiple destinations or multi-homed services</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Extends LeaseSet2 fields recursively</td>
    </tr>
  </tbody>
</table>
Todos os LeaseSets são distribuídos através da *floodfill DHT* mantida por roteadores especializados. As publicações são verificadas, registradas com timestamp e limitadas por taxa para reduzir correlação de metadados.

Veja a [documentação da Base de Dados de Rede](/docs/specs/common-structures) para mais detalhes.

---

## 7. Modern “Garlic” Applications within I2P

A criptografia baseada em garlic encryption e o agrupamento de mensagens são usados em toda a pilha de protocolos do I2P:

1. **Criação e uso de túneis** — criptografia em camadas por salto  
2. **Entrega de mensagens ponta a ponta** — mensagens garlic agrupadas com confirmação clonada e cloves de LeaseSet  
3. **Publicação no Network Database** — LeaseSets encapsulados em envelopes garlic para privacidade  
4. **Transportes SSU2 e NTCP2** — criptografia de subcamada usando framework Noise e primitivas X25519/ChaCha20

O garlic routing é, portanto, tanto um *método de camadas de criptografia* quanto um *modelo de mensagens de rede*.

---

## 6. LeaseSets e Garlic Bundling

O centro de documentação do I2P está [disponível aqui](/docs/), mantido continuamente. As especificações relevantes em desenvolvimento incluem:

- [Especificação ECIES](/docs/specs/ecies) — ECIES‑X25519‑AEAD‑Ratchet
- [Criação de Tunnel (ECIES)](/docs/specs/implementation) — protocolo moderno de construção de tunnel
- [Especificação I2NP](/docs/specs/i2np) — formatos de mensagem I2NP
- [Especificação SSU2](/docs/specs/ssu2) — transporte UDP SSU2
- [Estruturas Comuns](/docs/specs/common-structures) — comportamento de netDb e floodfill

Validação académica: Hoang et al. (IMC 2018, USENIX FOCI 2019) e Muntaka et al. (2025) confirmam a estabilidade arquitetural e a resiliência operacional do design do I2P.

---

## 7. Aplicações Modernas "Garlic" dentro do I2P

Propostas em andamento:

- **Proposta 169:** Híbrido pós-quântico (ML-KEM 512/768/1024 + X25519)  
- **Proposta 168:** Otimização de largura de banda de transporte  
- **Atualizações de datagrama e streaming:** Gerenciamento aprimorado de congestionamento

Adaptações futuras podem incluir estratégias adicionais de atraso de mensagens ou redundância multi-tunnel ao nível de garlic-message, baseando-se em opções de entrega não utilizadas originalmente descritas por Freedman.

---

## 8. Documentação Atual e Referências

- Freedman, M. J. & Dingledine, R. (2000). *Free Haven Master's Thesis,* § 8.1.1. [Free Haven Papers](https://www.freehaven.net/papers.html)  
- [Onion Router Publications](https://www.onion-router.net/Publications.html)  
- [Garlic Routing (Wikipedia)](https://en.wikipedia.org/wiki/Garlic_routing)  
- [Tor Project](https://www.torproject.org/)  
- [Free Haven Anonbib](https://freehaven.net/anonbib/topic.html)  
- Goldschlag, D. M., Reed, M. G., Syverson, P. F. (1996). *Hiding Routing Information.* NRL Publication.

---
