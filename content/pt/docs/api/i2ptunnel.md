---
title: "I2PTunnel"
description: "Ferramenta para interagir e fornecer serviços na I2P"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

## Visão Geral

I2PTunnel é um componente central do I2P para interface e fornecimento de serviços na rede I2P. Ele permite que aplicações baseadas em TCP e streaming de mídia operem anonimamente através de abstração de túnel. O destino de um túnel pode ser definido por um [hostname](/docs/overview/naming), [Base32](/docs/overview/naming#base32), ou uma chave de destino completa.

Cada tunnel estabelecido escuta localmente (por exemplo, `localhost:port`) e conecta-se internamente aos destinos I2P. Para hospedar um serviço, crie um tunnel apontando para o IP e porta desejados. Uma chave de destino I2P correspondente é gerada, permitindo que o serviço se torne globalmente acessível dentro da rede I2P. A interface web do I2PTunnel está disponível em [I2P Router Tunnel Manager](http://localhost:7657/i2ptunnel/).

---

## Serviços Padrão

### Túnel de servidor

- **I2P Webserver** – Um tunnel para um servidor web Jetty em [localhost:7658](http://localhost:7658) para hospedagem fácil no I2P.  
  - **Unix:** `$HOME/.i2p/eepsite/docroot`  
  - **Windows:** `%LOCALAPPDATA%\I2P\I2P Site\docroot` → `C:\Users\<username>\AppData\Local\I2P\I2P Site\docroot`

### Túneis de cliente

- **I2P HTTP Proxy** – `localhost:4444` – Usado para navegar na I2P e na Internet através de outproxies.  
- **I2P HTTPS Proxy** – `localhost:4445` – Variante segura do proxy HTTP.  
- **Irc2P** – `localhost:6668` – Tunnel padrão da rede IRC anônima.  
- **Git SSH (gitssh.idk.i2p)** – `localhost:7670` – Client tunnel para acesso SSH a repositórios.  
- **Postman SMTP** – `localhost:7659` – Client tunnel para envio de e-mail.  
- **Postman POP3** – `localhost:7660` – Client tunnel para recebimento de e-mail.

> Nota: Apenas o Webserver I2P é um **túnel de servidor** padrão; todos os outros são túneis de cliente que se conectam a serviços I2P externos.

---

## Configuração

A especificação de configuração do I2PTunnel está documentada em [/spec/configuration](/docs/specs/configuration/).

---

## Modos de Cliente

### Padrão

Abre uma porta TCP local que se conecta a um serviço em um destino I2P. Suporta múltiplas entradas de destino separadas por vírgulas para redundância.

### HTTP

Um túnel proxy para requisições HTTP/HTTPS. Suporta outproxies locais e remotos, remoção de cabeçalhos, cache, autenticação e compressão transparente.

**Proteções de privacidade:**   - Remove cabeçalhos: `Accept-*`, `Referer`, `Via`, `From`   - Substitui cabeçalhos de host por destinos Base32   - Aplica remoção hop-by-hop conforme RFC   - Adiciona suporte para descompressão transparente   - Fornece páginas de erro internas e respostas localizadas

**Comportamento de compressão:**   - Requisições podem usar cabeçalho personalizado `X-Accept-Encoding: x-i2p-gzip`   - Respostas com `Content-Encoding: x-i2p-gzip` são descomprimidas transparentemente   - Compressão avaliada por tipo MIME e comprimento da resposta para eficiência

**Persistência (novo desde 2.5.0):**   HTTP Keepalive e conexões persistentes agora são suportados para serviços hospedados no I2P através do Hidden Services Manager. Isso reduz a latência e a sobrecarga de conexão, mas ainda não habilita sockets persistentes totalmente compatíveis com RFC 2616 em todos os saltos.

**Pipelining:**   Permanece sem suporte e desnecessário; navegadores modernos o descontinuaram.

**Comportamento do User-Agent:**   - **Outproxy:** Usa um User-Agent atual do Firefox ESR.   - **Interno:** `MYOB/6.66 (AN/ON)` para consistência de anonimato.

### Cliente IRC

Conecta-se a servidores IRC baseados em I2P. Permite um subconjunto seguro de comandos enquanto filtra identificadores para privacidade.

### SOCKS 4/4a/5

Fornece capacidade de proxy SOCKS para conexões TCP. UDP permanece não implementado no Java I2P (apenas no i2pd).

### CONECTAR

Implementa tunelamento HTTP `CONNECT` para conexões SSL/TLS.

### Streamr

Habilita streaming estilo UDP via encapsulamento baseado em TCP. Suporta streaming de mídia quando emparelhado com um túnel servidor Streamr correspondente.

![Diagrama do I2PTunnel Streamr](/images/I2PTunnel-streamr.png)

---

## Modos de Servidor

### Servidor Padrão

Cria um destino TCP mapeado para um IP:porta local.

### Servidor HTTP

Cria um destino que se conecta com um servidor web local. Suporta compressão (`x-i2p-gzip`), remoção de cabeçalhos e proteções contra DDoS. Agora beneficia-se de **suporte a conexões persistentes** (v2.5.0+) e **otimização de pool de threads** (v2.7.0–2.9.0).

### HTTP Bidirecional

**Descontinuado** – Ainda funcional mas desencorajado. Atua como servidor e cliente HTTP sem outproxying. Utilizado principalmente para testes de diagnóstico em loopback.

### Servidor IRC

Cria um destino filtrado para serviços IRC, passando as chaves de destino do cliente como nomes de host.

### Servidor Streamr

Combina-se com um túnel cliente Streamr para manipular fluxos de dados no estilo UDP sobre I2P.

---

## Novos Recursos (2.4.0–2.10.0)

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Feature</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Introduced</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Summary</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Keepalive/Persistent Connections</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.5.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">HTTP tunnels now support persistent sockets for I2P-hosted services, improving performance.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Thread Pooling Optimization</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.7.0-2.9.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reduced CPU overhead and latency by improving thread management.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Post-Quantum Encryption (ML-KEM)</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.10.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Optional hybrid X25519+ML-KEM encryption to resist future quantum attacks.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>NetDB Segmentation</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.4.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Isolates I2PTunnel contexts for improved security and privacy.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>SSU1 Removal / SSU2 Adoption</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.4.0-2.6.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Upgraded transport layer; transparent to users.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>I2P-over-Tor Blocking</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.6.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Prevents inefficient and unstable I2P-over-Tor routing.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Browser Proxy (Proposal 166)</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.7.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Introduced identity-aware proxy mode; details pending confirmation.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Java 17 Requirement (upcoming)</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.11.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Future release will require Java 17+.</td>
    </tr>
  </tbody>
</table>
---

## Recursos de Segurança

- **Remoção de cabeçalhos** para anonimato (Accept, Referer, From, Via)
- **Randomização do User-Agent** dependendo do in/outproxy
- **Limitação de taxa de POST** e **proteção contra Slowloris**
- **Controle de conexões** nos subsistemas de streaming
- **Tratamento de congestionamento de rede** na camada de tunnel
- **Isolamento do NetDB** prevenindo vazamentos entre aplicações

---

## Detalhes Técnicos

- Tamanho padrão da chave de destino: 516 bytes (pode exceder para certificados LS2 estendidos)
- Endereços Base32: `{52–56+ chars}.b32.i2p`
- Túneis de servidor permanecem compatíveis com Java I2P e i2pd
- Recurso descontinuado: apenas `httpbidirserver`; nenhuma remoção desde 0.9.59
- Verificadas portas padrão corretas e raízes de documentos para todas as plataformas

---

## Resumo

I2PTunnel permanece a espinha dorsal da integração de aplicações com I2P. Entre 0.9.59 e 2.10.0, ganhou suporte a conexões persistentes, criptografia pós-quântica e grandes melhorias no gerenciamento de threads. A maioria das configurações permanece compatível, mas os desenvolvedores devem verificar suas configurações para garantir conformidade com os padrões modernos de transporte e segurança.
