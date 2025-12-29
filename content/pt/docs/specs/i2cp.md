---
title: "Protocolo do Cliente do I2P (I2CP)"
description: "Como as aplicações negociam sessões, tunnels e LeaseSets com o I2P router."
slug: "i2cp"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

## Visão geral

I2CP é o protocolo de controle de baixo nível entre um router I2P e qualquer processo cliente. Ele define uma separação rigorosa de responsabilidades:

- **Router**: Gerencia o roteamento, a criptografia, os ciclos de vida dos tunnels e as operações do banco de dados da rede
- **Cliente**: Seleciona propriedades de anonimato, configura tunnels e envia/recebe mensagens

Toda a comunicação flui por um único socket TCP (opcionalmente encapsulado em TLS), permitindo operações assíncronas e full-duplex (transmissão bidirecional simultânea).

**Versão do Protocolo**: I2CP usa um byte de versão de protocolo `0x2A` (42 decimal) enviado durante o estabelecimento inicial da conexão. Esse byte de versão permaneceu estável desde a criação do protocolo.

**Estado atual**: Esta especificação aplica-se à versão do router 0.9.67 (versão da API 0.9.67), lançada em 2025-09.

## Contexto de Implementação

### Implementação em Java

A implementação de referência está no Java I2P: - SDK do cliente: pacote `i2p.jar` - Implementação do Router: pacote `router.jar` - [Javadocs](http://docs.i2p-projekt.de/javadoc/)

Quando o cliente e o router executam na mesma JVM, as mensagens I2CP são passadas como objetos Java sem serialização. Clientes externos usam o protocolo serializado sobre TCP.

### Implementação em C++

i2pd (o router I2P em C++) também implementa o I2CP externamente para conexões de clientes.

### Clientes não Java

**Não há implementações não-Java conhecidas** de uma biblioteca de cliente I2CP completa. Aplicações não-Java devem usar, em vez disso, protocolos de nível mais alto:

- **SAM (Simple Anonymous Messaging) v3**: Interface baseada em socket com bibliotecas em várias linguagens de programação
- **BOB (Basic Open Bridge)**: Alternativa mais simples ao SAM

Esses protocolos de nível superior lidam com a complexidade do I2CP internamente e também fornecem a biblioteca de streaming (para conexões semelhantes ao TCP) e a biblioteca de datagramas (para conexões semelhantes ao UDP).

## Estabelecimento de Conexão

### 1. Conexão TCP

Conecte-se à porta I2CP do router: - Padrão: `127.0.0.1:7654` - Configurável nas configurações do router - Encapsulador TLS opcional (altamente recomendado para conexões remotas)

### 2. Negociação de Protocolo

**Etapa 1**: Envie o byte de versão do protocolo `0x2A`

**Etapa 2**: Sincronização do relógio

```
Client → Router: GetDateMessage
Router → Client: SetDateMessage
```
O router retorna o carimbo de data e hora atual e a string de versão da API I2CP (desde 0.8.7).

**Etapa 3**: Autenticação (se ativada)

A partir da versão 0.9.11, a autenticação pode ser incluída em GetDateMessage por meio de um Mapping (mapeamento) contendo: - `i2cp.username` - `i2cp.password`

A partir da versão 0.9.16, quando a autenticação estiver ativada, ela **deve** ser concluída por meio de GetDateMessage antes que quaisquer outras mensagens sejam enviadas.

**Etapa 4**: Criação da sessão

```
Client → Router: CreateSessionMessage (contains SessionConfig)
Router → Client: SessionStatusMessage (status=Created)
```
**Etapa 5**: Sinal de Prontidão do Tunnel

```
Router → Client: RequestVariableLeaseSetMessage
```
Esta mensagem sinaliza que os tunnels de entrada foram construídos. O router NÃO enviará isto até que exista pelo menos um tunnel de entrada E um tunnel de saída.

**Etapa 6**: Publicação do LeaseSet

```
Client → Router: CreateLeaseSet2Message
```
Neste ponto, a sessão está totalmente operacional para enviar e receber mensagens.

## Padrões de Fluxo de Mensagens

### Mensagem de saída (o cliente envia para o destino remoto)

**Com i2cp.messageReliability=none**:

```
Client → Router: SendMessageMessage (nonce=0)
[No acknowledgments]
```
**Com i2cp.messageReliability=BestEffort**:

```
Client → Router: SendMessageMessage (nonce>0)
Router → Client: MessageStatusMessage (status=Accepted)
Router → Client: MessageStatusMessage (status=Success or Failure)
```
### Mensagem recebida (Router entrega ao cliente)

**Com i2cp.fastReceive=true** (padrão desde 0.9.4):

```
Router → Client: MessagePayloadMessage
[No acknowledgment required]
```
**Com i2cp.fastReceive=false** (OBSOLETO):

```
Router → Client: MessageStatusMessage (status=Available)
Client → Router: ReceiveMessageBeginMessage
Router → Client: MessagePayloadMessage
Client → Router: ReceiveMessageEndMessage
```
Clientes modernos devem sempre usar o modo de recebimento rápido.

## Estruturas de Dados Comuns

### Cabeçalho da Mensagem I2CP

Todas as mensagens I2CP utilizam este cabeçalho comum:

```
+----+----+----+----+----+----+----+----+
| Body Length (4 bytes)                 |
+----+----+----+----+----+----+----+----+
|Type|  Message Body (variable)        |
+----+----+----+----+----+----+----+----+
```
- **Comprimento do Corpo**: inteiro de 4 bytes, comprimento apenas do corpo da mensagem (exclui o cabeçalho)
- **Tipo**: inteiro de 1 byte, identificador do tipo de mensagem
- **Corpo da Mensagem**: 0+ bytes, o formato varia conforme o tipo de mensagem

**Limite de tamanho da mensagem**: Aproximadamente 64 KB no máximo.

### ID da sessão

Inteiro de 2 bytes que identifica exclusivamente uma sessão em um router.

**Valor especial**: `0xFFFF` indica "sem sessão" (usado para consultas de nome de host sem uma sessão estabelecida).

### ID da mensagem

Inteiro de 4 bytes gerado pelo router para identificar univocamente uma mensagem dentro de uma sessão.

**Importante**: Os IDs de mensagem **não** são globalmente únicos, apenas únicos dentro de uma sessão. Eles também são distintos do nonce (número arbitrário usado apenas uma vez) gerado pelo cliente.

### Formato da carga útil

As cargas úteis das mensagens são comprimidas com gzip, com um cabeçalho gzip padrão de 10 bytes: - Começa com: `0x1F 0x8B 0x08` (RFC 1952) - Desde a versão 0.7.1: As partes não utilizadas do cabeçalho gzip contêm informações de protocolo, porta de origem e porta de destino - Isso permite streaming e datagramas no mesmo destino

**Controle de compressão**: Defina `i2cp.gzip=false` para desativar a compressão (define o esforço do gzip para 0). O cabeçalho gzip ainda é incluído, mas com sobrecarga mínima de compressão.

### Estrutura de SessionConfig

Define a configuração para uma sessão de cliente:

```
+----------------------------------+
| Destination                      |
+----------------------------------+
| Mapping (configuration options)  |
+----------------------------------+
| Creation Date                    |
+----------------------------------+
| Signature                        |
+----------------------------------+
```
**Requisitos críticos**: 1. **O mapeamento deve estar ordenado por chave** para validação da assinatura 2. **Data de criação** deve estar dentro de ±30 segundos da hora atual do router 3. **Assinatura** é criada pela SigningPrivateKey do Destination (destino no I2P)

**Assinaturas offline** (a partir da versão 0.9.38):

Se estiver usando assinatura offline, o mapeamento deve conter: - `i2cp.leaseSetOfflineExpiration` - `i2cp.leaseSetTransientPublicKey` - `i2cp.leaseSetOfflineSignature`

A Signature é então gerada pela SigningPrivateKey temporária.

## Opções de Configuração do Núcleo

### Configuração do Tunnel

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Option</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Default</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>inbound.length</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Number of hops for inbound tunnels</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>outbound.length</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Number of hops for outbound tunnels</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>inbound.lengthVariance</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Random variance in hop count (since 0.7.6)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>outbound.lengthVariance</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Random variance in hop count (since 0.7.6)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>inbound.quantity</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Number of concurrent inbound tunnels</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>outbound.quantity</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Number of concurrent outbound tunnels</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>inbound.backupQuantity</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Standby inbound tunnels (hot spares)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>outbound.backupQuantity</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Standby outbound tunnels (hot spares)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>inbound.allowZeroHop</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">true</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Allow 0-hop tunnels (disable for full anonymity)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>outbound.allowZeroHop</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">true</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Allow 0-hop tunnels (disable for full anonymity)</td>
    </tr>
  </tbody>
</table>
**Notas**: - Valores para `quantity` > 6 requerem pares executando 0.9.0+ e aumentam significativamente o consumo de recursos - Defina `backupQuantity` como 1-2 para serviços de alta disponibilidade - Zero-hop tunnels sacrificam o anonimato em favor da latência mas são úteis para testes

### Tratamento de Mensagens

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Option</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Default</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>clientMessageTimeout</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">60000&nbsp;ms</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Legacy timeout for message delivery</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>i2cp.messageReliability</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">BestEffort</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>None</code>, <code>BestEffort</code>, or <code>Guaranteed</code></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>i2cp.fastReceive</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">true</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Skip ReceiveMessageBegin/End handshake (default since 0.9.4)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>i2cp.gzip</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">true</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Enable gzip compression of message payloads</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>outbound.priority</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Priority for outbound scheduling (-25 to +25)</td>
    </tr>
  </tbody>
</table>
**Confiabilidade de Mensagens**: - `None`: Sem confirmações do router (padrão da biblioteca de streaming desde 0.8.1) - `BestEffort`: O router envia aceitação + notificações de sucesso/falha - `Guaranteed`: Não implementado (atualmente comporta-se como BestEffort)

**Substituição por mensagem** (desde 0.9.14): - Em uma sessão com `messageReliability=none`, definir um nonce (número usado uma vez) diferente de zero solicita notificação de entrega para essa mensagem específica - Definir nonce=0 em uma sessão `BestEffort` desativa as notificações para essa mensagem

### Configuração do LeaseSet

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Option</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Default</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>i2cp.dontPublishLeaseSet</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">false</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Disable automatic LeaseSet publication (for client-only destinations)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>i2cp.leaseSetType</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">LeaseSet variant: 1 = standard, 3 = LS2, 5 = encrypted, 7 = meta</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>i2cp.leaseSetEncType</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Comma-separated encryption type codes (see below)</td>
    </tr>
  </tbody>
</table>
### Tags de Sessão ElGamal/AES legadas

Essas opções são relevantes apenas para a criptografia ElGamal legada:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Option</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Default</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>crypto.lowTagThreshold</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">30</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Minimum session tags before replenishing</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>crypto.tagsToSend</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">40</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Number of tags to send in a batch</td>
    </tr>
  </tbody>
</table>
**Observação**: Os clientes ECIES-X25519 utilizam um mecanismo de ratchet (mecanismo de avanço criptográfico) diferente e ignoram estas opções.

## Tipos de criptografia

I2CP oferece suporte a múltiplos esquemas de criptografia de ponta a ponta por meio da opção `i2cp.leaseSetEncType`. Podem ser especificados vários tipos (separados por vírgula) para oferecer suporte tanto a pares modernos quanto a pares legados.

### Tipos de Criptografia Suportados

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Algorithm</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Key Size</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Since</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Status</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ElGamal/AES+SessionTags</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">2048-bit ElGamal</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Original</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Legacy</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1-3</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">-</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Unused</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ECIES-X25519-AEAD-Ratchet</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">32-byte X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.46</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current Standard</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">5</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ECIES-X25519-AEAD-Ratchet + ML-KEM-768 hybrid</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">32&nbsp;+&nbsp;PQ</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Beta</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">6</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ECIES-X25519-AEAD-Ratchet + ML-KEM-1024 hybrid</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">32&nbsp;+&nbsp;PQ</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Beta</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">7</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved (likely ML-KEM-512 hybrid)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">32&nbsp;+&nbsp;PQ</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Future</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Planned</td>
    </tr>
  </tbody>
</table>
**Configuração recomendada**:

```
i2cp.leaseSetEncType=4,0
```
Isso oferece X25519 (preferido), com ElGamal como opção de reserva para compatibilidade.

### Detalhes do Tipo de Criptografia

**Tipo 0 - ElGamal/AES+SessionTags**: - chaves públicas ElGamal de 2048 bits (256 bytes) - criptografia simétrica AES-256 - tags de sessão de 32 bytes enviadas em lotes - alta sobrecarga de CPU, largura de banda e memória - está sendo gradualmente descontinuado em toda a rede

**Tipo 4 - ECIES-X25519-AEAD-Ratchet**: - Troca de chaves X25519 (chaves de 32 bytes) - ChaCha20/Poly1305 AEAD - Double Ratchet ao estilo Signal (mecanismo de catraca dupla) - Tags de sessão de 8 bytes (vs 32 bytes para ElGamal) - Tags geradas via PRNG sincronizado (não enviadas com antecedência) - ~92% de redução de sobrecarga vs ElGamal - Padrão para o I2P moderno (a maioria dos routers utiliza isto)

**Tipos 5-6 - Híbrido pós-quântico**: - Combina X25519 com ML-KEM (NIST FIPS 203, mecanismo de encapsulamento de chaves) - Oferece segurança resistente a ataques quânticos - ML-KEM-768 para equilíbrio entre segurança e desempenho - ML-KEM-1024 para máxima segurança - Tamanhos de mensagem maiores devido ao material de chaves pós-quânticas (PQ) - Suporte na rede ainda em implantação

### Estratégia de Migração

A rede I2P está migrando ativamente de ElGamal (tipo 0) para X25519 (tipo 4): - NTCP → NTCP2 (concluído) - SSU → SSU2 (concluído) - ElGamal tunnels → X25519 tunnels (concluído) - ElGamal fim a fim → ECIES-X25519 (em grande parte concluído)

## LeaseSet2 e Recursos Avançados

### Opções do LeaseSet2 (desde 0.9.38)

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Option</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Since</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Purpose</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>i2cp.leaseSetType</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.38</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Specifies LeaseSet variant (1, 3, 5, 7)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>i2cp.leaseSetEncType</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.38</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Encryption types supported (comma-separated)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>i2cp.leaseSetAuthType</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.41</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Per-client authentication: 0 = none, 1 = DH, 2 = PSK</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>i2cp.leaseSetPrivKey</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.41</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">X25519 private key for decrypting LS2 with auth</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>i2cp.leaseSetSecret</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.39</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Base64 secret for blinded addresses</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>i2cp.leaseSetTransientPublicKey</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.38</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Transient signing key for offline signatures</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>i2cp.leaseSetPrivateKey</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.18</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Persistent LeaseSet encryption keys (type:key pairs)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>i2cp.leaseSetOption.nnn</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.66</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Service records (proposal 167)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>i2cp.leaseSetClient.dh.nnn</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.41</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">DH client auth material (indexed from 0)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>i2cp.leaseSetClient.psk.nnn</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.41</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">PSK client auth material (indexed from 0)</td>
    </tr>
  </tbody>
</table>
### Blinded Addresses (endereços cegos)

A partir da versão 0.9.39, os destinos podem usar endereços "blinded" (endereços cegados) (formato b33) que mudam periodicamente:
- Requer `i2cp.leaseSetSecret` para proteção por senha
- Autenticação opcional por cliente
- Consulte as propostas 123 e 149 para obter detalhes

### Registros de Serviço (desde 0.9.66)

LeaseSet2 suporta opções de registro de serviço (proposta 167):

```
i2cp.leaseSetOption.0=_smtp._tcp=1 86400 0 0 25 mail.example.b32.i2p
```
O formato segue o estilo do registro SRV do DNS, mas adaptado para o I2P.

## Múltiplas sessões (desde a versão 0.9.21)

Uma única conexão I2CP pode manter várias sessões:

**Sessão Primária**: A primeira sessão criada em uma conexão **Subsessões**: Sessões adicionais que compartilham o tunnel pool da sessão primária

### Características da subsessão

1. **Tunnels compartilhados**: Use os mesmos pools de inbound/outbound tunnel que a sessão primária
2. **Chaves de criptografia compartilhadas**: Deve usar chaves de criptografia do LeaseSet idênticas
3. **Chaves de assinatura diferentes**: Deve usar chaves de assinatura distintas da Destination (destino no I2P)
4. **Sem garantia de anonimato**: Claramente vinculado à sessão primária (mesmo router, mesmos tunnels)

### Caso de uso de Subsession (subsessão)

Permitir comunicação com destinos usando diferentes tipos de assinatura: - Principal: assinatura EdDSA (moderna) - Subsession (subsessão): assinatura DSA (para compatibilidade com legado)

### Ciclo de vida da subsessão

**Criação**:

```
Client → Router: CreateSessionMessage
Router → Client: SessionStatusMessage (unique Session ID)
Router → Client: RequestVariableLeaseSetMessage (separate for each destination)
Client → Router: CreateLeaseSet2Message (separate for each destination)
```
**Destruição**: - Destruir uma subsessão: Mantém a sessão principal intacta - Destruir a sessão principal: Destrói todas as subsessões e fecha a conexão - DisconnectMessage (mensagem de desconexão): Destrói todas as sessões

### Tratamento do ID de sessão

A maioria das mensagens I2CP contém um campo de ID de sessão. Exceções: - DestLookup / DestReply (obsoleto, use HostLookup / HostReply) - GetBandwidthLimits / BandwidthLimits (resposta não específica da sessão)

**Importante**: Os clientes não devem ter várias mensagens CreateSession (comando de criação de sessão) pendentes simultaneamente, pois as respostas não podem ser correlacionadas inequivocamente às solicitações.

## Catálogo de Mensagens

### Resumo dos Tipos de Mensagem

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Name</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Direction</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Since</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Status</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">CreateSession</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">C → R</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Original</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ReconfigureSession</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">C → R</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.7.1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">DestroySession</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">C → R</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Original</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">CreateLeaseSet</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">C → R</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Original</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">5</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">SendMessage</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">C → R</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Original</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">6</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ReceiveMessageBegin</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">C → R</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Original</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">7</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ReceiveMessageEnd</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">C → R</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Original</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">8</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">GetBandwidthLimits</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">C → R</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.7.2</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">20</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">SessionStatus</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">R → C</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Original</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">21</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">RequestLeaseSet</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">R → C</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Original</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">22</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">MessageStatus</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">R → C</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Original</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">23</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">BandwidthLimits</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">R → C</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.7.2</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">29</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ReportAbuse</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Bidirectional</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Original</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Unused</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">30</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Disconnect</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Bidirectional</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Original</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">31</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">MessagePayload</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">R → C</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Original</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">GetDate</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">C → R</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Original</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">33</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">SetDate</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">R → C</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Original</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">34</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">DestLookup</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">C → R</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.7</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">35</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">DestReply</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">R → C</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.7</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">36</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">SendMessageExpires</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">C → R</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.7.1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">37</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">RequestVariableLeaseSet</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">R → C</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.7</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">38</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">HostLookup</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">C → R</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.11</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">39</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">HostReply</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">R → C</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.11</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">41</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">CreateLeaseSet2</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">C → R</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.39</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">42</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">BlindingInfo</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">C → R</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.43</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
  </tbody>
</table>
**Legenda**: C = Cliente, R = Router

### Detalhes da Mensagem-chave

#### CreateSessionMessage (mensagem de criação de sessão, Tipo 1)

**Objetivo**: Iniciar uma nova sessão I2CP

**Conteúdo**: estrutura de SessionConfig

**Resposta**: SessionStatusMessage (status=Created ou Invalid)

**Requisitos**: - A data em SessionConfig deve estar dentro de ±30 segundos do relógio do router - O mapeamento deve estar ordenado por chave para validação da assinatura - Destination (destino no I2P) não deve já ter uma sessão ativa

#### RequestVariableLeaseSetMessage (Tipo 37)

**Objetivo**: Router solicita autorização do cliente para tunnels de entrada

**Conteúdo**: - ID da sessão - Número de leases (entradas de túnel) - Array de estruturas Lease (cada uma com expiração individual)

**Resposta**: CreateLeaseSet2Message

**Significado**: Este é o sinal de que a sessão está operacional. O router envia isto apenas depois de: 1. Pelo menos um tunnel de entrada ter sido construído 2. Pelo menos um tunnel de saída ter sido construído

**Recomendação de tempo limite**: Os clientes devem encerrar a sessão se esta mensagem não for recebida em até 5+ minutos após a criação da sessão.

#### CreateLeaseSet2Message (Tipo 41)

**Finalidade**: O cliente publica o LeaseSet no netDb (base de dados da rede)

**Conteúdo**: - ID de sessão - byte do tipo de LeaseSet (1, 3, 5 ou 7) - LeaseSet ou LeaseSet2 ou EncryptedLeaseSet ou MetaLeaseSet - Número de chaves privadas - Lista de chaves privadas (uma por chave pública no LeaseSet, na mesma ordem)

**Chaves Privadas**: Necessárias para descriptografar garlic messages (mensagens "garlic" do I2P, formato de mensagem agregada) recebidas. Formato:

```
Encryption type (2 bytes)
Key length (2 bytes)
Private key data (variable)
```
**Nota**: Substitui o CreateLeaseSetMessage obsoleto (tipo 4), que não oferece suporte a: - variantes de LeaseSet2 - criptografia não-ElGamal - múltiplos tipos de criptografia - LeaseSets criptografados - chaves de assinatura offline

#### SendMessageExpiresMessage (Tipo 36)

**Finalidade**: Enviar mensagem para o destino com expiração e opções avançadas

**Conteúdo**: - ID da sessão - Destino - Carga útil (compactado com gzip) - Nonce (valor único de uso único) (4 bytes) - Flags (2 bytes) - veja abaixo - Data de expiração (6 bytes, truncada de 8)

**Campo de Flags** (2 bytes, ordem dos bits 15...0):

**Bits 15-11**: Não utilizados, devem ser 0

**Bits 10-9**: Substituição da confiabilidade da mensagem (não utilizado, use nonce (número usado uma vez) em vez disso)

**Bit 8**: Não incluir o LeaseSet - 0: Router pode incluir o LeaseSet em garlic (técnica de encapsulamento do I2P) - 1: Não incluir o LeaseSet

**Bits 7-4**: Limiar baixo de tags (apenas para ElGamal, ignorado para ECIES)

```
0000 = Use session settings
0001 = 2 tags
0010 = 3 tags
...
1111 = 192 tags
```
**Bits 3-0**: Tags a enviar se necessário (apenas para ElGamal, ignorado para ECIES)

```
0000 = Use session settings
0001 = 2 tags
0010 = 4 tags
...
1111 = 160 tags
```
#### MessageStatusMessage (Tipo 22)

**Finalidade**: Notificar o cliente sobre o status de entrega da mensagem

**Conteúdo**: - ID de sessão - ID da mensagem (gerado pelo router) - Código de status (1 byte) - Tamanho (4 bytes, relevante apenas para status=0) - Nonce (4 bytes, corresponde ao nonce de SendMessage do cliente)

**Códigos de status** (Mensagens de saída):

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Code</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Name</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Meaning</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Result</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Accepted</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Router accepted message</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Success</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Best Effort Success</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Probable delivery</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Success</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Guaranteed Success</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Probable delivery</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Success</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">6</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Local Success</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Delivered to local client</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Success</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Best Effort Failure</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Probable failure</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">5</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Guaranteed Failure</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Generic failure</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">7</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Local Failure</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Local delivery failed</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">8</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Router Failure</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Router shutdown/error</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">9</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Network Failure</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">No network connectivity</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">10</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Bad Session</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Invalid/closed session</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">11</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Bad Message</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Invalid payload</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">12</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Bad Options</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Invalid options/expiration</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">13</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Overflow Failure</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Queue/buffer full</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">14</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Message Expired</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Expired before send</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">15</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Bad Local LeaseSet</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Local LeaseSet problem</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">16</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">No Local Tunnels</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">No tunnels available</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">17</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Unsupported Encryption</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Incompatible encryption</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">18</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Bad Destination</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Invalid remote destination</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">19</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Bad Leaseset</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Invalid remote LeaseSet</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">20</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Expired Leaseset</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Remote LeaseSet expired</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">21</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">No Leaseset</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Remote LeaseSet not found</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">22</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Meta Leaseset</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Cannot send to meta LS</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">23</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Loopback Denied</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Same source and destination</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
    </tr>
  </tbody>
</table>
**Códigos de sucesso**: 1, 2, 4, 6 **Códigos de falha**: Todos os demais

**Código de status 0** (OBSOLETO): Mensagem disponível (entrada, recebimento rápido desativado)

#### HostLookupMessage (Tipo 38)

**Finalidade**: Consultar o destino por nome de host ou hash (substitui DestLookup)

**Conteúdo**: - ID de sessão (ou 0xFFFF para nenhuma sessão) - ID da solicitação (4 bytes) - Tempo limite em milissegundos (4 bytes, mínimo recomendado: 10000) - Tipo de solicitação (1 byte) - Chave de consulta (Hash, String de nome de host, ou Destino)

**Tipos de solicitação**:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Lookup Key</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Returns</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Since</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Hash</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Destination</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Original</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Hostname String</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Destination</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Original</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Hash</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Destination + Options</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.66</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Hostname String</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Destination + Options</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.66</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Destination</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Destination + Options</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.66</td>
    </tr>
  </tbody>
</table>
Tipos 2–4 retornam opções de LeaseSet (proposta 167) se disponíveis.

**Resposta**: HostReplyMessage

#### HostReplyMessage (mensagem de resposta do host) (Tipo 39)

**Finalidade**: Resposta ao HostLookupMessage (mensagem de consulta de host)

**Conteúdo**: - ID da sessão - ID da solicitação - Código de resultado (1 byte) - Destino (presente em caso de sucesso, às vezes em falhas específicas) - Mapeamento (apenas para os tipos de consulta 2-4, pode estar vazio)

**Códigos de Resultado**:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Code</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Name</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Meaning</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Success</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Lookup succeeded</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Generic failure</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Lookup Password Required</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Blinded address requires password</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Private Key Required</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Blinded address requires private key</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Password and Key Required</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Blinded address requires both</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">5</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">LeaseSet Decryption Failure</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Cannot decrypt LeaseSet</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">6</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">LeaseSet Lookup Failure</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">LeaseSet not found in netdb</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">7</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Lookup Type Unsupported</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Router doesn't support this type</td>
    </tr>
  </tbody>
</table>
#### BlindingInfoMessage (Tipo 42)

**Finalidade**: Informar o router sobre os requisitos de autenticação de blinded destination (destino cego) (desde 0.9.43)

**Conteúdo**: - ID da sessão - Flags (1 byte) - Tipo de endpoint (1 byte): 0=Hash, 1=hostname, 2=Destino, 3=TipoAssinatura+Chave - Tipo de assinatura cega (2 bytes) - Expiração (4 bytes, segundos desde a época Unix) - Dados do endpoint (varia conforme o tipo) - Chave privada (32 bytes, somente se o bit 0 do flag estiver definido) - Senha de consulta (String, somente se o bit 4 do flag estiver definido)

**Sinalizadores** (ordem dos bits 76543210):

- **Bit 0**: 0=todos, 1=por cliente
- **Bits 3-1**: Esquema de autenticação (se o bit 0=1): 000=DH, 001=PSK
- **Bit 4**: 1=segredo obrigatório
- **Bits 7-5**: Não utilizados, definir como 0

**Sem resposta**: Router processa silenciosamente

**Caso de uso**: Antes de enviar para um blinded destination (destino ofuscado) (b33 address), o cliente deve: 1. Consultar o b33 via HostLookup, OU 2. Enviar a mensagem BlindingInfo

Se o destino exigir autenticação, BlindingInfo (informação de cegamento) é obrigatório.

#### ReconfigureSessionMessage (Tipo 2)

**Objetivo**: Atualizar a configuração da sessão após a criação

**Conteúdo**: - ID da sessão - SessionConfig (apenas as opções alteradas são necessárias)

**Resposta**: SessionStatusMessage (mensagem de status da sessão) (status=Updated or Invalid)

**Notas**: - O Router mescla a nova configuração com a configuração existente - As opções de Tunnel (`inbound.*`, `outbound.*`) são sempre aplicadas - Algumas opções podem ser imutáveis após a criação da sessão - A data deve estar dentro de ±30 segundos do horário do router - O mapeamento deve ser ordenado por chave

#### DestroySessionMessage (mensagem de destruição de sessão) (Tipo 3)

**Propósito**: Encerrar uma sessão

**Conteúdo**: ID da sessão

**Resposta esperada**: SessionStatusMessage (status=Destroyed)

**Comportamento atual** (Java I2P até a 0.9.66): - Router nunca envia SessionStatus(Destroyed) - Se não restarem sessões: Envia DisconnectMessage - Se restarem subsessões: Sem resposta

**Importante**: O comportamento do Java I2P difere da especificação. As implementações devem ser cautelosas ao destruir subsessões individuais.

#### DisconnectMessage (Tipo 30)

**Finalidade**: Notificar que a conexão está prestes a ser encerrada

**Conteúdo**: String do motivo

**Efeito**: Todas as sessões na conexão são destruídas, o socket é fechado

**Implementação**: Principalmente router → cliente no Java I2P

## Histórico de versões do protocolo

### Detecção de Versão

A versão do protocolo I2CP é trocada em mensagens Get/SetDate (desde a versão 0.8.7). Para routers mais antigos, as informações de versão não estão disponíveis.

**String de versão**: Indica a versão da API "core", não necessariamente a versão do router.

### Cronologia de funcionalidades

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Version</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Key Features</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.67</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">PQ Hybrid ML-KEM (enc types 5-7) in LeaseSet</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.66</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Host lookup/reply extensions (proposal 167), service records</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.62</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">MessageStatus loopback error code</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.46</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">X25519 (enc type 4) in LeaseSet, ECIES end-to-end</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.43</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">BlindingInfo message, extended HostReply failure codes</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.41</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">EncryptedLeaseSet options, Meta LS error code</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.39</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">CreateLeaseSet2 message, RedDSA Ed25519 support</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.38</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Preliminary LS2 support (format changed in 0.9.39)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.21</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Multiple sessions on single connection</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.20</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Additional SetDate messages for clock shifts</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.16</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Authentication required before other messages (when enabled)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.15</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">EdDSA Ed25519 signature type</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.14</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Per-message reliability override with nonzero nonce</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.12</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA P-256/384/521 signature types, RSA support</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.11</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">HostLookup/HostReply messages, auth in GetDate</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.7</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">RequestVariableLeaseSet message</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.5</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Additional MessageStatus codes</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.4</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Fast receive mode default, nonce=0 allowed</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.2</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">SendMessageExpires flag tag bits</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">16 leases per LeaseSet (up from 6)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.8.7</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Version strings in Get/SetDate</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.8.4</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">SendMessageExpires flag bits</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.8.3</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">DestLookup in standard session, concurrent lookups</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.8.1</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>messageReliability=none</code></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.7.2</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">GetBandwidthLimits, BandwidthLimits</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.7.1</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">SendMessageExpires, ReconfigureSession, ports in gzip header</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.7</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">DestLookup, DestReply</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.6.5-</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Original protocol features</td>
    </tr>
  </tbody>
</table>
## Considerações de Segurança

### Autenticação

**Padrão**: Nenhuma autenticação necessária **Opcional**: Autenticação por nome de usuário/senha (desde 0.9.11) **Obrigatório**: Quando ativada, a autenticação deve ser concluída antes de outras mensagens (desde 0.9.16)

**Conexões Remotas**: Sempre use TLS (`i2cp.SSL=true`) para proteger credenciais e chaves privadas.

### Defasagem do relógio

SessionConfig Date deve estar com diferença de no máximo ±30 segundos em relação à hora do router, ou a sessão será rejeitada. Use Get/SetDate para sincronizar.

### Manipulação de Chaves Privadas

CreateLeaseSet2Message contém chaves privadas para descriptografar mensagens recebidas. Estas chaves devem ser: - Transmitidas com segurança (TLS para conexões remotas) - Armazenadas com segurança pelo router - Rotacionadas quando comprometidas

### Expiração de mensagens

Use sempre SendMessageExpires (não SendMessage) para definir uma expiração explícita. Isto: - Impede que mensagens sejam enfileiradas indefinidamente - Reduz o consumo de recursos - Melhora a confiabilidade

### Gerenciamento de Tags de Sessão

**ElGamal** (obsoleto): - As tags devem ser transmitidas em lotes - Tags perdidas causam falhas de descriptografia - Elevada sobrecarga de memória

**ECIES-X25519** (atual): - Tags geradas via PRNG (gerador de números pseudoaleatórios) sincronizado - Não é necessária transmissão antecipada - Resiliente à perda de mensagens - Sobrecarga significativamente menor

## Boas práticas

### Para desenvolvedores de clientes

1. **Use o modo de recebimento rápido**: Sempre defina `i2cp.fastReceive=true` (ou mantenha o padrão)

2. **Prefira ECIES-X25519 (ECIES com X25519, esquema de criptografia)**: Configure `i2cp.leaseSetEncType=4,0` para obter o melhor desempenho mantendo a compatibilidade

3. **Defina uma expiração explícita**: Use SendMessageExpires, não SendMessage

4. **Lide com Subsessions (subsessões) com cuidado**: Esteja ciente de que as Subsessions não oferecem anonimato entre destinos

5. **Tempo limite para criação de sessão**: Destrua a sessão se RequestVariableLeaseSet (solicitação de LeaseSet variável) não for recebido dentro de 5 minutos

6. **Ordenar mapeamentos de configuração**: Sempre ordene as chaves do Mapping (estrutura de chave/valor) antes de assinar o SessionConfig (mensagem de configuração de sessão)

7. **Use números apropriados de Tunnel**: Não defina `quantity` > 6 a menos que seja necessário

8. **Considere SAM/BOB (interfaces para aplicações se comunicarem com o router I2P) para não-Java**: Implemente SAM em vez de I2CP diretamente

### Para desenvolvedores de Router

1. **Validar Datas**: Impor uma janela de ±30 segundos nas datas do SessionConfig

2. **Limitar o tamanho da mensagem**: Impor um tamanho máximo de ~64 KB por mensagem

3. **Suporte a Múltiplas Sessões**: Implementar suporte a subsessões conforme a especificação 0.9.21

4. **Envie RequestVariableLeaseSet imediatamente**: Somente depois que ambos os tunnels de entrada e de saída existirem

5. **Tratar Mensagens Obsoletas**: Aceitar, mas desencorajar ReceiveMessageBegin/End

6. **Suporte a ECIES-X25519**: Priorize a criptografia do tipo 4 para novas implantações

## Depuração e Resolução de Problemas

### Problemas comuns

**Sessão rejeitada (inválida)**: - Verifique o desvio do relógio (deve estar dentro de ±30 segundos) - Verifique se o Mapping está ordenado por chave - Certifique-se de que a Destination (destino do I2P) não está em uso

**Sem RequestVariableLeaseSet (pedido de leaseSet variável)**: - Router pode estar construindo tunnels (aguarde até 5 minutos) - Verifique se há problemas de conectividade de rede - Verifique se há conexões com pares suficientes

**Falhas na Entrega de Mensagens**: - Verifique os códigos MessageStatus para identificar o motivo específico da falha - Verifique se o LeaseSet remoto está publicado e atual - Certifique-se de que os tipos de criptografia são compatíveis

**Problemas de Subsessão**: - Verifique se a sessão principal foi criada primeiro - Confirme que as chaves de criptografia são as mesmas - Verifique se as chaves de assinatura são distintas

### Mensagens de diagnóstico

**GetBandwidthLimits**: Consultar a capacidade do router **HostLookup**: Testar a resolução de nomes e a disponibilidade do LeaseSet **MessageStatus**: Acompanhar a entrega de mensagens de ponta a ponta

## Especificações relacionadas

- **Estruturas Comuns**: /docs/specs/common-structures/
- **I2NP (Protocolo de Rede)**: /docs/specs/i2np/
- **ECIES-X25519**: /docs/specs/ecies/
- **Criação de Tunnel**: /docs/specs/implementation/
- **Biblioteca de Streaming**: /docs/specs/streaming/
- **Biblioteca de Datagramas**: /docs/api/datagrams/
- **SAM v3**: /docs/api/samv3/

## Propostas Referenciadas

- [Proposta 123](/proposals/123-new-netdb-entries/): LeaseSets criptografados e autenticação
- [Proposta 144](/proposals/144-ecies-x25519-aead-ratchet/): ECIES-X25519-AEAD-Ratchet
- [Proposta 149](/proposals/149-b32-encrypted-ls2/): Formato de endereço cego (b33)
- [Proposta 152](/proposals/152-ecies-tunnels/): Criação de tunnel com X25519
- [Proposta 154](/proposals/154-ecies-lookups/): Consultas ao banco de dados a partir de destinos ECIES
- [Proposta 156](/proposals/156-ecies-routers/): Migração do router para ECIES-X25519
- [Proposta 161](/pt/proposals/161-ri-dest-padding/): Compressão do preenchimento de destino
- [Proposta 167](/proposals/167-service-records/): Registros de serviço de LeaseSet
- [Proposta 169](/proposals/169-pq-crypto/): Criptografia híbrida pós-quântica (ML-KEM)

## Referência do Javadoc

- [Pacote I2CP](http://docs.i2p-projekt.de/javadoc/net/i2p/data/i2cp/package-summary.html)
- [MessageStatusMessage](http://docs.i2p-projekt.de/javadoc/net/i2p/data/i2cp/MessageStatusMessage.html)
- [API do Cliente](http://docs.i2p-projekt.de/javadoc/net/i2p/client/package-summary.html)

## Resumo de Obsolescência

### Mensagens obsoletas (não usar)

- **CreateLeaseSetMessage** (tipo 4): Use CreateLeaseSet2Message
- **RequestLeaseSetMessage** (tipo 21): Use RequestVariableLeaseSetMessage
- **ReceiveMessageBeginMessage** (tipo 6): Use o modo de recebimento rápido
- **ReceiveMessageEndMessage** (tipo 7): Use o modo de recebimento rápido
- **DestLookupMessage** (tipo 34): Use HostLookupMessage
- **DestReplyMessage** (tipo 35): Use HostReplyMessage
- **ReportAbuseMessage** (tipo 29): Nunca implementado

### Opções obsoletas

- Criptografia ElGamal (tipo 0): Migrar para ECIES-X25519 (tipo 4)
- Assinaturas DSA: Migrar para EdDSA ou ECDSA
- `i2cp.fastReceive=false`: Sempre usar o modo de recebimento rápido
