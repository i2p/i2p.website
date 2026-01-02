---
title: "Modelo de Ameaças do I2P"
description: "Catálogo de ataques considerados no design do I2P e as mitigações implementadas"
slug: "threat-model"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
reviewStatus: "needs-review"
---

## 1. O que "Anônimo" Significa

O I2P fornece *anonimato prático*—não invisibilidade. Anonimato é definido como a dificuldade para um adversário obter informações que você deseja manter privadas: quem você é, onde você está ou com quem você fala. Anonimato absoluto é impossível; em vez disso, o I2P visa **anonimato suficiente** contra adversários globais passivos e ativos.

Seu anonimato depende de como você configura o I2P, como escolhe peers e assinaturas, e quais aplicações você expõe.

---

## 2. Evolução Criptográfica e de Transporte (2003 → 2025)

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Era</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Primary Algorithms</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.3 – 0.9</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ElGamal + AES-256 + DSA-SHA1</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Legacy stack (2003–2015)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.15</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Ed25519 signatures</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Replaced DSA</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.36 (2018)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>NTCP2</strong> introduced</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Noise <em>XK_25519_ChaChaPoly_SHA256</em></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.56 (2022)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>SSU2</strong> enabled by default</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Noise-based UDP transport</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.4.0 (2023)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>NetDB Sub-DB isolation</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Prevents router↔client linkage</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.8.0+ (2025)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Congestion-aware routing / observability reductions</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">DoS hardening</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.10.0 (2025)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Post-quantum hybrid ML-KEM support (optional)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Experimental</td>
    </tr>
  </tbody>
</table>
**Conjunto criptográfico atual (Noise XK):** - **X25519** para troca de chaves   - **ChaCha20/Poly1305 AEAD** para criptografia   - **Ed25519 (EdDSA-SHA512)** para assinaturas   - **SHA-256** para hashing e HKDF   - **Híbridos ML-KEM** opcionais para testes pós-quânticos

Todos os usos de ElGamal e AES-CBC foram descontinuados. O transporte é inteiramente NTCP2 (TCP) e SSU2 (UDP); ambos suportam IPv4/IPv6, forward secrecy e ofuscação DPI.

---

## 3. Resumo da Arquitetura de Rede

- **Mixnet de rota livre:** Remetentes e destinatários definem seus próprios tunnels.  
- **Sem autoridade central:** Roteamento e nomenclatura são descentralizados; cada router mantém confiança local.  
- **Tunnels unidirecionais:** Entrada e saída são separados (tempo de vida de 10 min).  
- **Tunnels exploratórios:** 2 saltos por padrão; tunnels de cliente 2–3 saltos.  
- **Routers floodfill:** ~1 700 de ~55 000 nós (~6 %) mantêm o NetDB distribuído.  
- **Rotação do NetDB:** O espaço de chaves rotaciona diariamente à meia-noite UTC.  
- **Isolamento de sub-DB:** Desde a versão 2.4.0, cada cliente e router usam bancos de dados separados para evitar vinculação.

---

## 4. Categorias de Ataque e Defesas Atuais

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Category</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Current Status (2025)</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Primary Defenses</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Brute Force / Cryptanalysis</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Impractical with modern primitives (X25519, ChaCha20).</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Strong crypto, key rotation, Noise handshakes.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Timing Attacks</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Still unsolved for low-latency systems.</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Unidirectional tunnels, 1024&nbsp;B cells, profile recalc (45&nbsp;s). Research continues for non-trivial delays (3.0+).</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Intersection Attacks</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Inherent weakness of low latency mixnets.</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Tunnel rotation (10&nbsp;min), leaseset expirations, multihoming.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Predecessor Attacks</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Partially mitigated.</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Tiered peer selection, strict XOR ordering, variable length tunnels.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Sybil Attacks</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">No comprehensive defense.</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">IP /16 limits, profiling, diversity rules; HashCash infra exists but not required.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Floodfill / NetDB Attacks</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Improved but still a concern.</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">One /16 per lookup, limit 500 active, daily rotation, randomized verification delay, Sub-DB isolation.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>DoS / Flooding</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Frequent (esp. 2023 incidents).</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Congestion-aware routing (2.4+), aggressive leaseset removal (2.8+).</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Traffic ID / Fingerprinting</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Greatly reduced.</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Noise obfuscation, random padding, no plaintext headers.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Censorship / Partitioning</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Possible with state-level blocking.</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Hidden mode, IPv6, multiple reseeds, mirrors.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Development / Supply Chain</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Mitigated.</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Open source, signed SU3 releases (RSA-4096), multi-signer trust model.</td>
    </tr>
  </tbody>
</table>
---

## 5. Banco de Dados de Rede Moderno (NetDB)

**Fatos principais (ainda precisos):** - DHT Kademlia modificado armazena RouterInfo e LeaseSets.   - Hashing de chave SHA-256; consultas paralelas aos 2 floodfills mais próximos com timeout de 10 s.   - Tempo de vida do LeaseSet ≈ 10 min (LeaseSet2) ou 18 h (MetaLeaseSet).

**Novos tipos (desde 0.9.38):** - **LeaseSet2 (Tipo 3)** – múltiplos tipos de criptografia, com timestamp.   - **EncryptedLeaseSet2 (Tipo 5)** – destino ofuscado para serviços privados (autenticação DH ou PSK).   - **MetaLeaseSet (Tipo 7)** – multihoming e expirações estendidas.

**Grande atualização de segurança – Isolamento de Sub-DB (2.4.0):** - Impede a associação router↔cliente.   - Cada cliente e router utilizam segmentos netDb separados.   - Verificado e auditado (2.5.0).

---

## 6. Modo Oculto e Rotas Restritas

- **Modo Oculto:** Implementado (automático em países rigorosos segundo pontuações da Freedom House).  
    Os routers não publicam RouterInfo nem encaminham tráfego.  
- **Rotas Restritas:** Parcialmente implementado (tunnels básicos somente para confiáveis).  
    O roteamento abrangente por pares confiáveis permanece planejado (3.0+).

Compromisso: Melhor privacidade ↔ redução da contribuição para a capacidade da rede.

---

## 7. Ataques DoS e Floodfill

**Histórico:** Pesquisa da UCSB de 2013 mostrou que ataques Eclipse e tomadas de controle de Floodfill eram possíveis. **Defesas modernas incluem:** - Rotação diária do espaço de chaves. - Limite de Floodfill ≈ 500, um por /16. - Atrasos de verificação de armazenamento aleatorizados. - Preferência por routers mais recentes (2.6.0). - Correção de inscrição automática (2.9.0). - Roteamento com reconhecimento de congestionamento e limitação de leases (2.4.0+).

Ataques floodfill permanecem teoricamente possíveis, mas praticamente mais difíceis.

---

## 8. Análise de Tráfego e Censura

O tráfego I2P é difícil de identificar: sem porta fixa, sem handshake em texto simples e padding aleatório. Os pacotes NTCP2 e SSU2 imitam protocolos comuns e usam ofuscação de cabeçalho ChaCha20. As estratégias de padding são básicas (tamanhos aleatórios), tráfego fictício não está implementado (custoso). Conexões de nós de saída Tor são bloqueadas desde a versão 2.6.0 (para proteger recursos).

---

## 9. Limitações Persistentes (reconhecidas)

- Correlação de temporização para aplicativos de baixa latência permanece um risco fundamental.
- Ataques de interseção ainda são poderosos contra destinos públicos conhecidos.
- Ataques Sybil carecem de defesa completa (HashCash não aplicado).
- Tráfego de taxa constante e atrasos não triviais permanecem não implementados (planejado para 3.0).

A transparência sobre esses limites é intencional — ela impede que os usuários superestimem o anonimato.

---

## 10. Estatísticas da Rede (2025)

- ~55 000 routers ativos em todo o mundo (↑ de 7 000 em 2013)  
- ~1 700 routers floodfill (~6 %)  
- 95 % participam no roteamento de tunnel por padrão  
- Níveis de largura de banda: K (<12 KB/s) → X (>2 MB/s)  
- Taxa mínima para floodfill: 128 KB/s  
- Console do router Java 8+ (necessário), Java 17+ planejado para o próximo ciclo

---

## 11. Desenvolvimento e Recursos Centrais

- Site oficial: [geti2p.net](/)
- Documentação: [Documentation](/docs/)  
- Repositório Debian: <https://deb.i2pgit.org> ( substituiu deb.i2p2.de em outubro de 2023 )  
- Código fonte: <https://i2pgit.org/I2P_Developers/i2p.i2p> (Gitea) + espelho no GitHub  
- Todas as versões são containers SU3 assinados (RSA-4096, chaves zzz/str4d)  
- Sem listas de discussão ativas; comunidade via <https://i2pforum.net> e IRC2P.  
- Ciclo de atualização: versões estáveis a cada 6–8 semanas.

---

## 12. Resumo das Melhorias de Segurança Desde a Versão 0.8.x

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Year</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Feature</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Effect</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2015</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Ed25519 signatures</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Removed SHA1/DSA weakness</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2018</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">NTCP2</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Noise-based TCP transport</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2019</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">LeaseSet2 / EncryptedLeaseSet2</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Hidden services privacy</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2022</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">SSU2</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Noise-based UDP transport</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2023</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Sub-DB Isolation + Congestion-Aware Routing</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Stopped NetDB linkage / improved resilience</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2024</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Floodfill selection improvements</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reduced long-term node influence</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2025</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Observability reductions + PQ hybrid crypto</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Harder timing analysis / future-proofing</td>
    </tr>
  </tbody>
</table>
---

## 13. Trabalho Não Resolvido Conhecido ou Planejado

- Rotas restritas abrangentes (roteamento de pares confiáveis) → planejado para 3.0.  
- Atraso/agrupamento não-trivial para resistência temporal → planejado para 3.0.  
- Padding avançado e tráfego fictício → não implementado.  
- Verificação de identidade HashCash → infraestrutura existe mas inativa.  
- Substituição DHT R5N → apenas proposta.

---

## 14. Referências Principais

- *Practical Attacks Against the I2P Network* (Egger et al., RAID 2013)  
- *Privacy Implications of Performance-Based Peer Selection* (Herrmann & Grothoff, PETS 2011)  
- *Resilience of the Invisible Internet Project* (Muntaka et al., Wiley 2025)  
- [Documentação Oficial do I2P](/docs/)

---

## 15. Conclusão

O modelo central de anonimato do I2P mantém-se há duas décadas: sacrificar a unicidade global em favor da confiança e segurança locais. De ElGamal a X25519, de NTCP a NTCP2, e de reseeds manuais ao isolamento de Sub-DB, o projeto evoluiu mantendo sua filosofia de defesa em profundidade e transparência.

Muitos ataques permanecem teoricamente possíveis contra qualquer mixnet de baixa latência, mas o fortalecimento contínuo do I2P os torna cada vez mais impraticáveis. A rede é maior, mais rápida e mais segura do que nunca — mas ainda assim honesta sobre suas limitações.
