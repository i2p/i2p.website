---
title: "Incorporando I2P na Sua Aplicação"
description: "Orientação prática atualizada para incluir um roteador I2P com sua aplicação de forma responsável"
slug: "embedding"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

Incluir o I2P com sua aplicação é uma forma poderosa de integrar usuários—mas apenas se o router estiver configurado de forma responsável.

## 1. Coordenar com as Equipes de Router

- Contacte os mantenedores do **Java I2P** e **i2pd** antes de empacotar. Eles podem revisar suas configurações padrão e destacar questões de compatibilidade.
- Escolha a implementação de router que se adequa à sua stack:
  - **Java/Scala** → Java I2P
  - **C/C++** → i2pd
  - **Outras linguagens** → empacote um router e integre usando [SAM v3](/docs/api/samv3/) ou [I2CP](/docs/specs/i2cp/)
- Verifique os termos de redistribuição para binários do router e dependências (runtime Java, ICU, etc.).

## 2. Padrões de Configuração Recomendados

Busque "contribuir mais do que consumir." Os padrões modernos priorizam a saúde e estabilidade da rede.

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Setting</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Recommended Default (2025)</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Bandwidth share</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">80% for participating tunnels </td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Tunnel quantities</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">i2pd: 3 inbound / 3 outbound; Java I2P: 2 inbound / 2 outbound. </td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Signature &amp; encryption</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Use Ed25519 (<code>SIGNATURE_TYPE=7</code>) and advertise ECIES-X25519 + ElGamal (<code>i2cp.leaseSetEncType=4,0</code>).</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Client protocols</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Use SAM v3 or I2CP.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">API listeners</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Bind SAM/I2CP to <code>127.0.0.1</code> only. Disable if not needed.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">UI toggles</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Expose bandwidth controls, logs, and an opt-in checkbox for participating tunnels.</td>
    </tr>
  </tbody>
</table>
### Túneis Participantes Permanecem Essenciais

**Não** desative os túneis de participação.

1. Roteadores que não retransmitem têm pior desempenho.
2. A rede depende do compartilhamento voluntário de capacidade.
3. Tráfego de cobertura (tráfego retransmitido) melhora o anonimato.

**Mínimos oficiais:** - Largura de banda compartilhada: ≥ 12 KB/s   - Ativação automática de floodfill: ≥ 128 KB/s   - Recomendado: 2 túneis de entrada / 2 túneis de saída (padrão do Java I2P)

## 3. Persistência e Reseeding

Diretórios de estado persistente (`netDb/`, perfis, certificados) devem ser preservados entre execuções.

Sem persistência, seus usuários vão acionar reseeds a cada inicialização—degradando o desempenho e aumentando a carga nos servidores de reseed.

Se a persistência for impossível (por exemplo, contêineres ou instalações efêmeras):

1. Inclua **1.000–2.000 router infos** no instalador.
2. Opere um ou mais servidores de reseed personalizados para desafogar os públicos.

Variáveis de configuração: - Diretório base: `i2p.dir.base` - Diretório de configuração: `i2p.dir.config` - Inclui `certificates/` para reseed (ressemeadura).

## 4. Segurança e Exposição

- Mantenha o console do router (`127.0.0.1:7657`) apenas local.  
- Use HTTPS se expor a UI externamente.  
- Desative SAM/I2CP externo a menos que necessário.  
- Revise os plugins incluídos—distribua apenas o que sua aplicação suporta.  
- Sempre inclua autenticação para acesso remoto ao console.

**Recursos de segurança introduzidos desde a versão 2.5.0:** - Isolamento de NetDB entre aplicações (2.4.0+)   - Mitigação de DoS e listas de bloqueio Tor (2.5.1)   - Resistência a sondagem NTCP2 (2.9.0)   - Melhorias na seleção de roteadores floodfill (2.6.0+)

## 5. APIs Suportadas (2025)

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">API</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Status</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>SAM v3 (3.3)</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">✅ Active</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Recommended bridge for non-Java apps.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>I2CP</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">✅ Active</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Stable protocol core, used internally by Java I2P.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>I2PControl</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">✅ Active</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">JSON-RPC API; plugin maintained.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>BOB</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">⚠️ Deprecated</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Removed from Java I2P since 1.7.0; use SAM v3 instead.</td>
    </tr>
  </tbody>
</table>
Toda a documentação oficial está localizada em `/docs/api/` — o caminho antigo `/spec/samv3/` **não** existe.

## 6. Redes e Portas

Portas padrão típicas: - 4444 – Proxy HTTP   - 4445 – Proxy HTTPS   - 7654 – I2CP   - 7656 – SAM Bridge   - 7657 – Console do Router   - 7658 – Site I2P local   - 6668 – Proxy IRC   - 9000–31000 – Porta aleatória do router (UDP/TCP entrada)

Os roteadores selecionam uma porta de entrada aleatória na primeira execução. O encaminhamento melhora o desempenho, mas o UPnP pode lidar com isso automaticamente.

## 7. Mudanças Modernas (2024–2025)

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Change</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Status</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Details</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>SSU1 Transport</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Removed</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">SSU2 is now the exclusive UDP transport.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>I2P-over-Tor</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Blocked</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Since 2.6.0 (July 2024).</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Datagram2/3</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Added</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Authenticated, repliable datagram formats (2.9.0).</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>LeaseSet service records</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Added</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Enables service discovery (Proposal 167).</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Tunnel build parameters</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Improved</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Adaptive congestion handling (2.9.0+).</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Post-quantum crypto</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Introduced (beta)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ML-KEM hybrid ratchet, opt-in from 2.10.0.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Java 17 requirement</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Announced</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Becomes mandatory in 2.11.0 (early 2026).</td>
    </tr>
  </tbody>
</table>
## 8. Experiência do Usuário e Testes

- Comunicar o que o I2P faz e por que a largura de banda é compartilhada.
- Fornecer diagnósticos do router (largura de banda, tunnels, status de reseed).
- Testar pacotes no Windows, macOS e Linux (incluindo baixa RAM).
- Verificar interoperabilidade com peers do **Java I2P** e **i2pd**.
- Testar recuperação de quedas de rede e saídas abruptas.

## 9. Recursos da Comunidade

- Fórum: [i2pforum.net](https://i2pforum.net) ou `http://i2pforum.i2p` dentro do I2P.  
- Código: [i2pgit.org/I2P_Developers/i2p.i2p](https://i2pgit.org/I2P_Developers/i2p.i2p).  
- IRC (rede Irc2P): `#i2p-dev`, `#i2pd`.  
  - `#i2papps` não verificado; pode não existir.  
  - Esclareça qual rede (Irc2P vs ilita.i2p) hospeda seu canal.

Incorporar de forma responsável significa equilibrar a experiência do usuário, o desempenho e a contribuição para a rede. Use esses padrões, mantenha-se sincronizado com os mantenedores do router e teste sob carga real antes do lançamento.
