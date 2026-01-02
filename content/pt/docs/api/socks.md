---
title: "Proxy SOCKS"
description: "Usando o túnel SOCKS do I2P com segurança (atualizado para 2.10.0)"
slug: "socks"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

> **Atenção:** O túnel SOCKS encaminha payloads de aplicações sem sanitizá-los. Muitos protocolos expõem IPs, nomes de host ou outros identificadores. Use SOCKS apenas com software que você tenha auditado para anonimato.

---

## 1. Visão Geral

O I2P fornece suporte para proxy **SOCKS 4, 4a e 5** para conexões de saída através de um **cliente I2PTunnel**. Ele permite que aplicações padrão alcancem destinos I2P, mas **não pode acessar a clearnet**. Não há **outproxy SOCKS**, e todo o tráfego permanece dentro da rede I2P.

### Resumo da Implementação

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Parameter</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Java I2P</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">i2pd</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Default Port</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">User-defined</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>127.0.0.1:4447</code></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Supported SOCKS Versions</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">4, 4a, 5</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">4, 4a, 5</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">UDP Mode</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Stubbed (non-functional)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Stubbed (non-functional)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Persistent Keys</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">✅ Since 0.9.9</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">✅</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Shared Client Tunnels</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Supported</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Supported</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Outproxy Support</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">❌ None</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">❌ None</td>
    </tr>
  </tbody>
</table>
**Tipos de endereço suportados:** - Nomes de host `.i2p` (entradas do catálogo de endereços) - Hashes Base32 (`.b32.i2p`) - Sem suporte para Base64 ou clearnet

---

## 2. Riscos de Segurança e Limitações

### Vazamento na Camada de Aplicação

SOCKS opera abaixo da camada de aplicação e não consegue sanitizar protocolos. Muitos clientes (por exemplo, navegadores, IRC, email) incluem metadados que revelam seu endereço IP, nome do host ou detalhes do sistema.

Vazamentos comuns incluem: - IPs em cabeçalhos de e-mail ou respostas CTCP do IRC - Nomes reais/nomes de usuário em cargas úteis de protocolo - Strings de user-agent com impressões digitais do SO - Consultas DNS externas - WebRTC e telemetria do navegador

**I2P não pode prevenir estes vazamentos**—eles ocorrem acima da camada de tunnel. Use apenas SOCKS para **clientes auditados** projetados para anonimato.

### Identidade de Túnel Compartilhado

Se múltiplas aplicações compartilham um túnel SOCKS, elas compartilham a mesma identidade de destino I2P. Isso permite correlação ou fingerprinting entre diferentes serviços.

**Mitigação:** Use **tunnels não compartilhados** para cada aplicação e ative **chaves persistentes** para manter identidades criptográficas consistentes entre reinicializações.

### Modo UDP Desabilitado

O suporte UDP no SOCKS5 não está implementado. O protocolo anuncia capacidade UDP, mas as chamadas são ignoradas. Use clientes somente TCP.

### Sem Outproxy por Design

Ao contrário do Tor, o I2P **não** oferece outproxies para a clearnet baseados em SOCKS. Tentativas de alcançar IPs externos falharão ou exporão a identidade. Use proxies HTTP ou HTTPS se for necessário usar outproxy.

---

## 3. Contexto Histórico

Os desenvolvedores há muito tempo desaconselham o uso de SOCKS para uso anônimo. De discussões internas de desenvolvedores e da [Reunião 81](/pt/blog/2004/03/16/i2p-dev-meeting-march-16-2004/) e [Reunião 82](/pt/blog/2004/03/23/i2p-dev-meeting-march-23-2004/) de 2004:

> "Encaminhar tráfego arbitrário é inseguro, e cabe a nós, como desenvolvedores de software de anonimato, ter a segurança dos nossos utilizadores finais em primeiro lugar nas nossas mentes."

O suporte SOCKS foi incluído por compatibilidade, mas não é recomendado para ambientes de produção. Quase todas as aplicações de internet vazam metadados sensíveis inadequados para roteamento anônimo.

---

## 4. Configuração

### Java I2P

1. Abra o [I2PTunnel Manager](http://127.0.0.1:7657/i2ptunnel)  
2. Crie um novo tunnel cliente do tipo **"SOCKS 4/4a/5"**  
3. Configure as opções:  
   - Porta local (qualquer disponível)  
   - Cliente compartilhado: *desabilitar* para identidade separada por aplicativo  
   - Chave persistente: *habilitar* para reduzir correlação de chaves  
4. Inicie o tunnel

### i2pd

O i2pd inclui suporte SOCKS5 ativado por padrão em `127.0.0.1:4447`. A configuração em `i2pd.conf` na seção `[SOCKSProxy]` permite ajustar a porta, o host e os parâmetros do tunnel.

---

## 5. Cronograma de Desenvolvimento

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Version</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Change</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Date</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.7.1</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Initial SOCKS 4/4a/5 support</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2010</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.9</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Added persistent keying</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2013</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1.7.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">BOB API deprecated and removed</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2022</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.6.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">I2P-over-Tor blocked to improve network health</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2024</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.10.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Post-quantum hybrid encryption introduced</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2025</td>
    </tr>
  </tbody>
</table>
O próprio módulo SOCKS não recebeu atualizações importantes no protocolo desde 2013, mas a pilha de túneis circundante recebeu melhorias de desempenho e criptográficas.

---

## 6. Alternativas Recomendadas

Para qualquer aplicação de **produção**, **voltada ao público**, ou **crítica em termos de segurança**, use uma das APIs oficiais do I2P em vez de SOCKS:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">API</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Description</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Recommended For</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>SAM v3 (3.3)</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Simple Anonymous Messaging API</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Cross-language apps needing socket-like I/O</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Streaming Library</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">TCP-like sockets for Java</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Native Java integrations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>I2CP</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Low-level router communication</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Custom protocols, router-level integration</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>BOB</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deprecated (removed 2022)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Legacy only; migrate to SAM</td>
    </tr>
  </tbody>
</table>
Essas APIs fornecem isolamento adequado de destino, controle de identidade criptográfica e melhor desempenho de roteamento.

---

## 7. OnionCat / GarliCat

OnionCat suporta I2P através do seu modo GarliCat (intervalo IPv6 `fd60:db4d:ddb5::/48`). Ainda funcional, mas com desenvolvimento limitado desde 2019.

**Ressalvas de uso:** - Requer configuração manual de `.oc.b32.i2p` no SusiDNS   - Necessita atribuição estática de IPv6   - Não é oficialmente suportado pelo projeto I2P

Recomendado apenas para configurações avançadas de VPN-over-I2P.

---

## 8. Melhores Práticas

Se você precisa usar SOCKS: 1. Crie tunnels separados por aplicação.   2. Desative o modo de cliente compartilhado.   3. Ative chaves persistentes.   4. Force a resolução DNS do SOCKS5.   5. Audite o comportamento do protocolo para vazamentos.   6. Evite conexões clearnet.   7. Monitore o tráfego de rede para vazamentos.

---

## 9. Resumo Técnico

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Parameter</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Value</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Supported SOCKS Versions</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">4, 4a, 5</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Transport</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">TCP only</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>UDP Support</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Stubbed (non-functional)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Clearnet Access</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Not supported</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Default Ports</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Java I2P: user-set; i2pd: <code>127.0.0.1:4447</code></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Persistent Keying</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Supported since 0.9.9</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Shared Tunnels</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Supported (discouraged)</td>
    </tr>
  </tbody>
</table>
---

## 10. Conclusão

O proxy SOCKS no I2P oferece compatibilidade básica com aplicações TCP existentes, mas **não é projetado para garantias fortes de anonimato**. Deve ser usado apenas em ambientes de teste controlados e auditados.

> Para implantações sérias, migre para **SAM v3** ou a **API Streaming**. Essas APIs isolam as identidades das aplicações, usam criptografia moderna e recebem desenvolvimento contínuo.

---

### Recursos Adicionais

- [Documentação Oficial SOCKS](/docs/api/socks/)  
- [Especificação SAMv3](/docs/api/samv3/)  
- [Documentação da Biblioteca Streaming](/docs/specs/streaming/)  
- [Referência I2PTunnel](/docs/specs/implementation/)  
- [Documentação para Desenvolvedores I2P](https://i2pgit.org/I2P_Developers/i2p.i2p)  
- [Fórum da Comunidade](https://i2pforum.net)
