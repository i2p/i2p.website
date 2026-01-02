---
title: "Camada de Transporte"
description: "Compreendendo a camada de transporte do I2P - métodos de comunicação ponto a ponto entre routers, incluindo NTCP2 e SSU2"
slug: "transport"
lastUpdated: "2025-03"
accurateFor: "2.10.0"
---

---

## 1. Visão geral

Um **transporte** no I2P é um método para comunicação direta, ponto a ponto, entre routers. Esses mecanismos garantem confidencialidade e integridade enquanto verificam a autenticação do router.

Cada transporte opera com paradigmas de conexão que incluem autenticação, controle de fluxo, confirmações de recebimento e recursos de retransmissão.

---

## 2. Transportes atuais

O I2P atualmente suporta dois transportes principais:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Transport</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Protocol</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>NTCP2</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">TCP</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Noise-based TCP transport with modern encryption (as of 0.9.36)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>SSU2</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">UDP</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Secure Semireliable UDP with modern encryption (as of 0.9.56)</td>
    </tr>
  </tbody>
</table>
### 2.1 Transportes legados (obsoletos)

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Transport</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Protocol</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Status</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>NTCP</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">TCP</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Replaced by NTCP2; removed in 0.9.62</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>SSU</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">UDP</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Replaced by SSU2; removed in 0.9.62</td>
    </tr>
  </tbody>
</table>
---

## 3. Serviços de Transporte

O subsistema de transporte fornece os seguintes serviços:

### 3.1 Entrega de Mensagens

- Entrega confiável de mensagens [I2NP](/docs/specs/i2np/) (os transportes tratam exclusivamente de mensagens I2NP)
- A entrega em ordem NÃO é garantida universalmente
- Enfileiramento de mensagens baseado em prioridade

### 3.2 Gerenciamento de Conexões

- Estabelecimento e encerramento de conexões
- Gerenciamento de limites de conexão com imposição de limiares
- Rastreamento do estado de cada par
- Aplicação automática e manual de lista de banimento de pares

### 3.3 Configuração de Rede

- Múltiplos endereços de router por transporte (suporte a IPv4 e IPv6 desde a v0.9.8)
- Abertura de portas no firewall via UPnP
- Suporte à travessia de NAT/Firewall
- Detecção de IP local via vários métodos

### 3.4 Segurança

- Criptografia para comunicações ponto a ponto
- Validação de endereços IP conforme regras locais
- Determinação de consenso de relógio (NTP como backup)

### 3.5 Gestão de Largura de Banda

- Limites de largura de banda de entrada e de saída
- Seleção ótima de transporte para mensagens de saída

---

## 4. Endereços de Transporte

O subsistema mantém uma lista de pontos de contato do router:

- Método de transporte (NTCP2, SSU2)
- Endereço IP
- Número da porta
- Parâmetros opcionais

É possível usar vários endereços para cada método de transporte.

### 4.1 Configurações Comuns de Endereço

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Configuration</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Hidden</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Routers with no published addresses</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Firewalled</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Routers publishing SSU2 addresses with "introducer" peer lists for NAT traversal</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Unrestricted</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Routers advertising both NTCP2 and SSU2 addresses on IPv4 and/or IPv6</td>
    </tr>
  </tbody>
</table>
---

## 5. Seleção de transporte

O sistema seleciona transportes para [mensagens I2NP](/docs/specs/i2np/) independentemente dos protocolos de camadas superiores. A seleção emprega um **sistema de lances** em que cada transporte submete lances, e o menor valor vence.

### 5.1 Fatores para Determinação de Lances

- Configurações de preferência de transporte
- Conexões existentes com pares
- Contagem de conexões atual versus limiar
- Histórico recente de tentativas de conexão
- Restrições de tamanho de mensagem
- Capacidades de transporte do RouterInfo do par (metadados do router)
- Diretividade da conexão (direta versus dependente de introducer (mediador))
- Preferências de transporte anunciadas pelo par

Em geral, dois routers mantêm conexões de transporte único simultaneamente, embora conexões multi-transporte simultâneas sejam possíveis.

---

## 6. NTCP2

**NTCP2** (Novo Protocolo de Transporte 2) é o transporte moderno baseado em TCP para o I2P, introduzido na versão 0.9.36.

### 6.1 Principais funcionalidades

- Baseado no **Noise Protocol Framework** (padrão Noise_XK)
- Usa **X25519** para troca de chaves
- Usa **ChaCha20/Poly1305** para criptografia autenticada
- Usa **BLAKE2s** para funções de hash
- Ofuscação do protocolo para resistir à DPI (Inspeção Profunda de Pacotes)
- Preenchimento opcional para resistência à análise de tráfego

### 6.2 Estabelecimento de Conexão

1. **Solicitação de Sessão** (Alice → Bob): Chave X25519 efêmera + carga útil criptografada
2. **Sessão Criada** (Bob → Alice): Chave efêmera + confirmação criptografada
3. **Sessão Confirmada** (Alice → Bob): Handshake final com RouterInfo (informações do router)

Todos os dados posteriores são criptografados com chaves de sessão derivadas do handshake (negociação inicial).

Consulte a [Especificação do NTCP2](/docs/specs/ntcp2/) para obter todos os detalhes.

---

## 7. SSU2

**SSU2** (Secure Semireliable UDP 2) é o transporte moderno baseado em UDP do I2P, introduzido na versão 0.9.56.

### 7.1 Principais Recursos

- Baseado no **Noise Protocol Framework** (padrão Noise_XK)
- Usa **X25519** para troca de chaves
- Usa **ChaCha20/Poly1305** para criptografia autenticada
- Entrega parcialmente confiável com confirmações seletivas
- Travessia de NAT via hole punching (perfuração de NAT) e retransmissão/introdução
- Suporte a migração de conexão
- Descoberta do MTU do caminho

### 7.2 Vantagens em relação ao SSU (Legado)

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Feature</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">SSU (Legacy)</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">SSU2</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Encryption</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ElGamal + AES</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">X25519 + ChaCha20/Poly1305</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Header encryption</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Partial</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Full (ChaCha20)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Connection ID</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Fixed</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Encrypted, rotatable</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">NAT traversal</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Basic introduction</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Enhanced hole punching + relay</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Obfuscation</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Minimal</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Improved (variable padding)</td>
    </tr>
  </tbody>
</table>
Consulte a [Especificação do SSU2](/docs/specs/ssu2/) para obter todos os detalhes.

---

## 8. Atravessamento de NAT

Ambos os transportes suportam atravessamento de NAT para permitir que routers atrás de firewall participem da rede.

### 8.1 Introdução ao SSU2

Quando um router não consegue receber conexões de entrada diretamente:

1. Router publica endereços de **introducer** (nó introdutor) no seu RouterInfo
2. O par que se conecta envia uma solicitação de introdução ao introducer
3. O introducer encaminha as informações de conexão ao router atrás de um firewall
4. O router atrás de um firewall inicia uma conexão de saída (hole punch — perfuração de NAT)
5. Comunicação direta estabelecida

### 8.2 NTCP2 e firewalls

NTCP2 requer conectividade TCP de entrada. Routers atrás de NAT podem:

- Use o UPnP para abrir portas automaticamente
- Configure manualmente o redirecionamento de portas
- Confie no SSU2 para conexões de entrada enquanto usa o NTCP2 para conexões de saída

---

## 9. Ofuscação de Protocolo

Ambos os transportes modernos incorporam recursos de ofuscação:

- **Preenchimento aleatório** em mensagens de negociação inicial
- **Cabeçalhos criptografados** que não revelam assinaturas de protocolo
- **Mensagens de comprimento variável** para resistir à análise de tráfego
- **Sem padrões fixos** no estabelecimento de conexão

> **Observação**: A ofuscação na camada de transporte complementa, mas não substitui o anonimato fornecido pela arquitetura de tunnel do I2P.

---

## 10. Desenvolvimento futuro

As pesquisas e melhorias planejadas incluem:

- **Transportes plugáveis** – plugins de ofuscação compatíveis com Tor
- **Transporte baseado em QUIC** – Investigação dos benefícios do protocolo QUIC
- **Otimização dos limites de conexão** – Pesquisa sobre limites ideais de conexões entre pares
- **Estratégias de preenchimento aprimoradas** – Maior resistência à análise de tráfego

---

## 11. Referências

- [Especificação do NTCP2](/docs/specs/ntcp2/) – Transporte TCP baseado em Noise (framework de protocolos criptográficos)
- [Especificação do SSU2](/docs/specs/ssu2/) – UDP 2 seguro com confiabilidade parcial
- [Especificação do I2NP](/docs/specs/i2np/) – Mensagens do Protocolo de Rede do I2P
- [Estruturas Comuns](/docs/specs/common-structures/) – RouterInfo e estruturas de endereço
- [Discussão Histórica sobre NTCP](/docs/ntcp/) – Histórico do desenvolvimento do transporte legado
- [Documentação Legada do SSU](/docs/legacy/ssu/) – Especificação original do SSU (obsoleta)
