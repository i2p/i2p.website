---
title: "Protocolo Cliente I2P (I2CP)"
description: "Como as aplicações negociam sessões, tunnels e LeaseSets com o router I2P."
slug: "i2cp"
aliases:
  - "/pt/docs/api/i2cp"
  - "/pt/docs/api/i2cp/"
  - "/pt/docs/specs/i2cp-spec"
  - "/pt/docs/specs/i2cp-spec/"
  - "/pt/i2cp_spec"
  - "/pt/i2cp_spec/"
category: "Protocolos"
lastUpdated: "2025-07"
accurateFor: "0.9.67"
---

## Visão Geral

Esta é a especificação do I2P Control Protocol (I2CP), a interface de baixo nível entre clientes e o router. Clientes Java usarão a API cliente I2CP, que implementa este protocolo.

Não há implementações conhecidas não-Java de uma biblioteca client-side que implemente I2CP. Além disso, aplicações orientadas a socket (streaming) precisariam de uma implementação do protocolo de streaming, mas também não existem bibliotecas não-Java para isso. Portanto, clientes não-Java devem usar o protocolo de camada superior SAM [SAMv3](/docs/api/samv3/), para o qual existem bibliotecas em várias linguagens.

Este é um protocolo de baixo nível suportado tanto internamente quanto externamente pelo router I2P Java. O protocolo só é serializado se o cliente e o router não estiverem na mesma JVM; caso contrário, os objetos Java de mensagem I2CP são passados através de uma interface JVM interna. O I2CP também é suportado externamente pelo router C++ i2pd.

Mais informações estão na página de Visão Geral do I2CP [I2CP](/docs/specs/i2cp/).

## Sessões

O protocolo foi projetado para lidar com múltiplas "sessões", cada uma com um ID de sessão de 2 bytes, através de uma única conexão TCP, no entanto, múltiplas sessões não foram implementadas até a versão 0.9.21. Veja a [seção multissão abaixo](#multisession). Não tente usar múltiplas sessões em uma única conexão I2CP com routers mais antigos que a versão 0.9.21.

Também parece que há algumas disposições para um único cliente se comunicar com múltiplos routers através de conexões separadas. Isso também não foi testado, e provavelmente não é útil.

Não há como manter uma sessão após uma desconexão, ou recuperá-la em uma conexão I2CP diferente. Quando o socket é fechado, a sessão é destruída.

## Sequências de Mensagens de Exemplo

Nota: Os exemplos abaixo não mostram o Byte de Protocolo (0x2a) que deve ser enviado do cliente para o router ao conectar pela primeira vez. Mais informações sobre a inicialização da conexão estão na página de Visão Geral do I2CP [I2CP](/docs/specs/i2cp/).

### Estabelecimento de Sessão Padrão

```
  Client                                           Router

                           --------------------->  Get Date Message
        Set Date Message  <---------------------
                           --------------------->  Create Session Message
  Session Status Message  <---------------------
Request LeaseSet Message  <---------------------
                           --------------------->  Create LeaseSet Message

```
### Obter Limites de Largura de Banda (Sessão Simples)

```
  Client                                           Router

                           --------------------->  Get Bandwidth Limits Message
Bandwidth Limits Message  <---------------------

```
### Pesquisa de Destino (Sessão Simples)

```
  Client                                           Router

                           --------------------->  Dest Lookup Message
      Dest Reply Message  <---------------------

```
### Mensagem de Saída

Sessão existente, com i2cp.messageReliability=none

```
  Client                                           Router

                           --------------------->  Send Message Message

```
Sessão existente, com i2cp.messageReliability=none e nonce diferente de zero

```
  Client                                           Router

                           --------------------->  Send Message Message
  Message Status Message  <---------------------
  (succeeded)

```
Sessão existente, com i2cp.messageReliability=BestEffort

```
  Client                                           Router

                           --------------------->  Send Message Message
  Message Status Message  <---------------------
  (accepted)
  Message Status Message  <---------------------
  (succeeded)

```
### Mensagem Recebida

Sessão existente, com i2cp.fastReceive=true (a partir da versão 0.9.4)

```
  Client                                           Router

 Message Payload Message  <---------------------

```
Sessão existente, com i2cp.fastReceive=false (DESCONTINUADO)

```
  Client                                           Router

  Message Status Message  <---------------------
  (available)
                           --------------------->  Receive Message Begin Message
 Message Payload Message  <---------------------
                           --------------------->  Receive Message End Message

```
### Notas de Multisessão {#multisession}

Múltiplas sessões em uma única conexão I2CP são suportadas a partir da versão 0.9.21 do router. A primeira sessão criada é a "sessão primária". Sessões adicionais são "subsessões". Subsessões são usadas para suportar múltiplos destinos compartilhando um conjunto comum de tunnels. A aplicação inicial é para a sessão primária usar chaves de assinatura ECDSA, enquanto a subsessão usa chaves de assinatura DSA para comunicação com eepsites antigos.

As subsessões compartilham os mesmos pools de túneis de entrada e saída da sessão principal. As subsessões devem usar as mesmas chaves de criptografia da sessão principal. Isso se aplica tanto às chaves de criptografia do leaseSet quanto às chaves de criptografia do destino (não utilizadas). As subsessões devem usar chaves de assinatura diferentes no destino, portanto o hash do destino é diferente da sessão principal. Como as subsessões usam as mesmas chaves de criptografia e túneis da sessão principal, fica evidente para todos que os destinos estão executando no mesmo router, então as garantias usuais de anonimato anti-correlação não se aplicam.

Subsessões são criadas enviando uma mensagem CreateSession e recebendo uma mensagem SessionStatus em resposta, como de costume. Subsessões devem ser criadas após a sessão primária ser criada. A resposta SessionStatus irá, em caso de sucesso, conter um ID de Sessão único, distinto do ID da sessão primária. Embora as mensagens CreateSession devam ser processadas em ordem, não há uma maneira segura de correlacionar uma mensagem CreateSession com a resposta, então um cliente não deve ter múltiplas mensagens CreateSession pendentes simultaneamente. As opções SessionConfig para a subsessão podem não ser respeitadas quando são diferentes da sessão primária. Em particular, como subsessões usam o mesmo pool de tunnel que a sessão primária, as opções de tunnel podem ser ignoradas.

O router enviará mensagens RequestVariableLeaseSet separadas para cada Destination ao cliente, e o cliente deve responder com uma mensagem CreateLeaseSet para cada uma. Os leases para os dois Destinations não serão necessariamente idênticos, mesmo que sejam selecionados do mesmo pool de túneis.

Uma subsessão pode ser destruída com a mensagem DestroySession como de costume. Isso não destruirá a sessão primária nem interromperá a conexão I2CP. Destruir a sessão primária irá, no entanto, destruir todas as subsessões e interromper a conexão I2CP. Uma mensagem Disconnect destrói todas as sessões.

Note que a maioria das mensagens I2CP, mas não todas, contêm um Session ID. Para aquelas que não contêm, os clientes podem precisar de lógica adicional para lidar adequadamente com as respostas do router. DestLookup e DestReply não contêm Session IDs; use os mais novos HostLookup e HostReply em vez disso. GetBandwidthLimts e BandwidthLimits não contêm session IDs, porém a resposta não é específica da sessão.

### Notas da Versão {#notes}

O byte de versão de protocolo inicial (0x2a) enviado pelo cliente não deve mudar. Antes da versão 0.8.7, a informação de versão do router não estava disponível para o cliente, impedindo assim que novos clientes funcionassem com routers antigos. A partir da versão 0.8.7, as strings de versão de protocolo das duas partes são trocadas nas Mensagens Get/Set Date. Daqui em diante, os clientes podem usar esta informação para comunicar corretamente com routers antigos. Clientes e routers não devem enviar mensagens que não são suportadas pelo outro lado, pois geralmente desconectam a sessão ao receber uma mensagem não suportada.

As informações de versão trocadas são a versão da API "core" ou a versão do protocolo I2CP, e não necessariamente a versão do router.

Um resumo básico das versões do protocolo I2CP é o seguinte. Para detalhes, veja abaixo.

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Version</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Required I2CP Features</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.67</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">PQ Hybrid ML-KEM (enc types 5-7) supported in LS</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.66</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Host lookup/reply extensions (see proposal 167)</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.62</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">MessageStatus message Loopback error code</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.46</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">X25519 (enc type 4) supported in LS</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.43</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">BlindingInfo message supported; Additional HostReply message failure codes</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.41</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">EncryptedLeaseSet options; MessageStatus message Meta LS error code</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.39</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">CreateLeaseSet2 message and options supported; Dest/LS key certs w/ RedDSA Ed25519 sig type supported</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.38</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Preliminary CreateLeaseSet2 message supported (abandoned)</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.21</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Multiple sessions on a single I2CP connection supported</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.20</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Additional SetDate messages may be sent to the client at any time</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.16</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Authentication, if enabled, is required via GetDate before all other messages</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.15</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Dest/LS key certs w/ EdDSA Ed25519 sig type supported</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.14</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Per-message override of messageReliability=none with nonzero nonce</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.12</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Dest/LS key certs w/ ECDSA P-256, P-384, and P-521 sig types supported; RSA sig types also supported but currently unused</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.11</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Host Lookup and Host Reply messages supported; Authentication mapping in Get Date message supported</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.7</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Request Variable Lease Set message supported</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Additional Message Status codes defined</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.4</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Send Message nonce=0 allowed; Fast receive mode is the default</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.2</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Send Message Expires flag tag bits supported</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Supports up to 16 leases in a lease set (6 previously)</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.8.7</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Get Date and Set Date version strings included. If not present, the client or router is version 0.8.6 or older.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.8.4</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Send Message Expires flag bits supported</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.8.3</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Dest Lookup and Get Bandwidth messages supported in standard session; Concurrent Dest Lookup messages supported</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.8.1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">i2cp.messageReliability=none supported</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.7.2</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Get Bandwidth Limits and Bandwidth Limits messages supported</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.7.1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Send Message Expires message supported; Reconfigure Session message supported; Ports and protocol numbers in gzip header</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.7</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Dest Lookup and Dest Reply messages supported</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.6.5 or lower</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">All messages and features not listed above</td>
</tr>
</table>
## Estruturas comuns {#structures}

### Cabeçalho de mensagem I2CP {#struct-I2CPMessageHeader}

#### Descrição

Cabeçalho comum a todas as mensagens I2CP, contendo o comprimento da mensagem e o tipo de mensagem.

#### Conteúdo

1.  4 bytes [Integer](/docs/specs/common-structures/#integer) especificando o comprimento do
    corpo da mensagem
2.  1 byte [Integer](/docs/specs/common-structures/#integer) especificando o tipo da
    mensagem.
3.  O corpo da mensagem I2CP, 0 ou mais bytes

#### Notas

O limite real de comprimento da mensagem é de cerca de 64 KB.

### ID da Mensagem {#struct-MessageId}

#### Descrição

Identifica unicamente uma mensagem aguardando em um router específico em um determinado momento. Isso é sempre gerado pelo router e NÃO é o mesmo que o nonce gerado pelo cliente.

#### Conteúdo

1.  4 byte [Integer](/docs/specs/common-structures/#integer)

#### Notas

Os IDs de mensagem são únicos apenas dentro de uma sessão; eles não são globalmente únicos.

### Payload {#struct-Payload}

#### Descrição

Esta estrutura é o conteúdo de uma mensagem sendo entregue de um Destination para outro.

#### Conteúdo

1.  4 bytes de comprimento [Integer](/docs/specs/common-structures/#integer)
2.  Essa quantidade de bytes

#### Notas

O payload está em formato gzip conforme especificado na página de Visão Geral do I2CP [I2CP-FORMAT](/docs/specs/i2cp/#format).

O limite real de comprimento da mensagem é de cerca de 64 KB.

### Configuração de Sessão {#struct-SessionConfig}

#### Descrição

Define as opções de configuração para uma sessão de cliente específica.

#### Conteúdo

1.  [Destination](/docs/specs/common-structures/#destination)
2.  [Mapping](/docs/specs/common-structures/#mapping) de opções
3.  [Date](/docs/specs/common-structures/#date) de criação
4.  [Signature](/docs/specs/common-structures/#signature) dos 3 campos anteriores,
    assinada pela [SigningPrivateKey](/docs/specs/common-structures/#signingprivatekey)

#### Notas

- As opções são especificadas na página de Visão Geral I2CP
  [I2CP-OPTIONS](/docs/specs/i2cp/#options).
- O [Mapping](/docs/specs/common-structures/#mapping) deve ser ordenado por chave para que
  a assinatura seja validada corretamente no router.
- A data de criação deve estar dentro de +/- 30 segundos do tempo atual
  quando processada pelo router, ou a configuração será rejeitada.

#### Assinaturas Offline

- Se o [Destination](/docs/specs/common-structures/#destination) for assinado offline,
  o [Mapping](/docs/specs/common-structures/#mapping) deve conter as três opções
  i2cp.leaseSetOfflineExpiration, i2cp.leaseSetTransientPublicKey, e
  i2cp.leaseSetOfflineSignature. A
  [Signature](/docs/specs/common-structures/#signature) é então gerada pela
  [SigningPrivateKey](/docs/specs/common-structures/#signingprivatekey) transitória e
  é verificada com a
  [SigningPublicKey](/docs/specs/common-structures/#signingpublickey) especificada em
  i2cp.leaseSetTransientPublicKey. Veja
  [I2CP-OPTIONS](/docs/specs/i2cp/#options) para detalhes.

### ID da Sessão {#struct-SessionId}

#### Descrição

Identifica exclusivamente uma sessão em um router específico em um determinado momento.

#### Conteúdo

1.  2 bytes [Integer](/docs/specs/common-structures/#integer)

#### Notas

O ID de sessão 0xffff é usado para indicar "sem sessão", por exemplo para consultas de nome de host.

## Mensagens

Veja também os [Javadocs do I2CP](http://javadoc.i2p.net/net/i2p/data/i2cp/package-summary.html).

### Tipos de Mensagem {#types}

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Message</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Direction</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Type</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Since</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#BandwidthLimitsMessage">BandwidthLimitsMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">R -> C</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">23</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.7.2</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#BlindingInfoMessage">BlindingInfoMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">C -> R</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">42</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.43</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#CreateLeaseSetMessage">CreateLeaseSetMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">C -> R</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">4</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">deprecated</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#CreateLeaseSet2Message">CreateLeaseSet2Message</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">C -> R</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">41</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.39</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#CreateSessionMessage">CreateSessionMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">C -> R</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#DestLookupMessage">DestLookupMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">C -> R</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">34</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.7</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#DestReplyMessage">DestReplyMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">R -> C</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">35</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.7</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#DestroySessionMessage">DestroySessionMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">C -> R</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">3</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#DisconnectMessage">DisconnectMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">bidir.</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">30</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#GetBandwidthLimitsMessage">GetBandwidthLimitsMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">C -> R</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">8</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.7.2</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#GetDateMessage">GetDateMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">C -> R</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">32</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#HostLookupMessage">HostLookupMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">C -> R</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">38</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.11</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#HostReplyMessage">HostReplyMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">R -> C</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">39</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.11</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#MessagePayloadMessage">MessagePayloadMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">R -> C</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">31</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#MessageStatusMessage">MessageStatusMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">R -> C</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">22</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#ReceiveMessageBeginMessage">ReceiveMessageBeginMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">C -> R</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">6</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">deprecated</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#ReceiveMessageEndMessage">ReceiveMessageEndMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">C -> R</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">7</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">deprecated</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#ReconfigureSessionMessage">ReconfigureSessionMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">C -> R</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">2</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.7.1</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#ReportAbuseMessage">ReportAbuseMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">bidir.</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">29</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">deprecated</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#RequestLeaseSetMessage">RequestLeaseSetMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">R -> C</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">21</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">deprecated</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#RequestVariableLeaseSetMessage">RequestVariableLeaseSetMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">R -> C</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">37</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.7</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#SendMessageMessage">SendMessageMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">C -> R</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#SendMessageExpiresMessage">SendMessageExpiresMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">C -> R</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">36</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.7.1</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#SessionStatusMessage">SessionStatusMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">R -> C</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">20</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#SetDateMessage">SetDateMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">R -> C</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">33</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
</table>
### BandwidthLimitsMessage {#BandwidthLimitsMessage}

#### Descrição

Informa ao cliente quais são os limites de largura de banda.

Enviado do Router para o Cliente em resposta a uma [GetBandwidthLimitsMessage](#GetBandwidthLimitsMessage).

#### Conteúdo

1.  4 byte [Integer](/docs/specs/common-structures/#integer) Limite de entrada do cliente
    (KBps)
2.  4 byte [Integer](/docs/specs/common-structures/#integer) Limite de saída do cliente
    (KBps)
3.  4 byte [Integer](/docs/specs/common-structures/#integer) Limite de entrada do router
    (KBps)
4.  4 byte [Integer](/docs/specs/common-structures/#integer) Limite de rajada de entrada do router
    (KBps)
5.  4 byte [Integer](/docs/specs/common-structures/#integer) Limite de saída do router
    (KBps)
6.  4 byte [Integer](/docs/specs/common-structures/#integer) Limite de rajada de saída do router
    (KBps)
7.  4 byte [Integer](/docs/specs/common-structures/#integer) Tempo de rajada do router
    (segundos)
8.  Nove [Integer](/docs/specs/common-structures/#integer) de 4 bytes (indefinido)

#### Notas

Os limites do cliente podem ser os únicos valores definidos, e podem ser os limites reais do router, ou uma porcentagem dos limites do router, ou específicos para o cliente particular, dependendo da implementação. Todos os valores rotulados como limites do router podem ser 0, dependendo da implementação. A partir da versão 0.7.2.

### BlindingInfoMessage {#BlindingInfoMessage}

#### Descrição

Informa o router que um Destination está oculto, com senha de consulta opcional e chave privada opcional para descriptografia. Veja as propostas 123 e 149 para detalhes.

O router precisa saber se um destino está ofuscado. Se estiver ofuscado e usar uma autenticação secreta ou por cliente, também precisa ter essa informação.

Uma Host Lookup de um endereço b32 de novo formato ("b33") informa ao router que o endereço é blinded, mas não há mecanismo para passar a chave secreta ou privada para o router na mensagem Host Lookup. Embora pudéssemos estender a mensagem Host Lookup para adicionar essa informação, é mais limpo definir uma nova mensagem.

Esta mensagem fornece uma forma programática para o cliente informar ao router. Caso contrário, o usuário teria que configurar manualmente cada destino.

#### Uso

Antes que um cliente envie uma mensagem para um destino ofuscado, ele deve ou procurar o "b33" numa mensagem Host Lookup, ou enviar uma mensagem Blinding Info. Se o destino ofuscado requer uma chave secreta ou autenticação por cliente, o cliente deve enviar uma mensagem Blinding Info.

O router não envia uma resposta para esta mensagem. Enviada do Cliente para o Router.

#### Conteúdo

1.  [Session ID](#struct-sessionid)
2.  1 byte [Integer](/docs/specs/common-structures/#integer) Flags

> - Ordem dos bits: 76543210 > - Bit 0: 0 para todos, 1 para por-cliente > - Bits 3-1: Esquema de autenticação, se o bit 0 estiver definido como 1 para >   por-cliente, caso contrário 000 >   - 000: Autenticação de cliente DH (ou nenhuma autenticação por-cliente) >   - 001: Autenticação de cliente PSK > - Bit 4: 1 se segredo necessário, 0 se nenhum segredo necessário > - Bits 7-5: Não utilizados, definir como 0 para compatibilidade futura

3.  1 byte [Integer](/docs/specs/common-structures/#integer) Tipo de endpoint

> - Tipo 0 é um [Hash](/docs/specs/common-structures/#hash) > - Tipo 1 é um hostname [String](/docs/specs/common-structures/#string) > - Tipo 2 é um [Destination](/docs/specs/common-structures/#destination) > - Tipo 3 é um Sig Type e >   [SigningPublicKey](/docs/specs/common-structures/#signingpublickey)

4.  2 byte [Integer](/docs/specs/common-structures/#integer) Tipo de Assinatura Cega
5.  4 byte [Integer](/docs/specs/common-structures/#integer) Segundos de Expiração desde
    a época
6.  Endpoint: Dados conforme especificado, um de

> - Tipo 0: 32 bytes [Hash](/docs/specs/common-structures/#hash) > > - Tipo 1: nome do host [String](/docs/specs/common-structures/#string) > > - Tipo 2: [Destination](/docs/specs/common-structures/#destination) binário > >  > >  - Tipo 3: 2 bytes [Integer](/docs/specs/common-structures/#integer) tipo de assinatura, seguido por > >  -   [SigningPublicKey](/docs/specs/common-structures/#signingpublickey) (comprimento conforme >       implícito pelo tipo de assinatura)

7.  [PrivateKey](/docs/specs/common-structures/#privatekey) Chave de descriptografia Presente apenas
    se o bit 0 da flag estiver definido como 1. Uma chave privada ECIES_X25519 de 32 bytes,
    little-endian
8.  [String](/docs/specs/common-structures/#string) Senha de Consulta Presente apenas se
    o bit 4 da flag estiver definido como 1.

#### Notas

- A partir da versão 0.9.43.
- O tipo de endpoint Hash provavelmente não é útil a menos que o router possa fazer
  uma consulta reversa no livro de endereços para obter o Destination.
- O tipo de endpoint hostname provavelmente não é útil a menos que o router
  possa fazer uma consulta no livro de endereços para obter o Destination.

### CreateLeaseSetMessage {#CreateLeaseSetMessage}

DEPRECIADO. Não pode ser usado para LeaseSet2, chaves offline, tipos de criptografia não-ElGamal, múltiplos tipos de criptografia, ou LeaseSets criptografados. Use CreateLeaseSet2Message com todos os routers 0.9.39 ou superior.

#### Descrição

Esta mensagem é enviada em resposta a uma [RequestLeaseSetMessage](#RequestLeaseSetMessage) ou [RequestVariableLeaseSetMessage](#RequestVariableLeaseSetMessage) e contém todas as estruturas [Lease](/docs/specs/common-structures/#lease) que devem ser publicadas na Network Database I2NP.

Enviado do Cliente para o Router.

#### Conteúdo

1.  [Session ID](#struct-sessionid)
2.  DSA [SigningPrivateKey](/docs/specs/common-structures/#signingprivatekey) ou 20
    bytes ignorados
3.  [PrivateKey](/docs/specs/common-structures/#privatekey)
4.  [LeaseSet](/docs/specs/common-structures/#leaseset)

#### Notas

A SigningPrivateKey corresponde à [SigningPublicKey](/docs/specs/common-structures/#signingpublickey) dentro do leaseSet, apenas se o tipo de chave de assinatura for DSA. Isso é para revogação de leaseSet, que não está implementada e é improvável que seja implementada. Se o tipo de chave de assinatura não for DSA, este campo contém 20 bytes de dados aleatórios. O comprimento deste campo é sempre de 20 bytes, nunca é igual ao comprimento de uma chave privada de assinatura não-DSA.

A PrivateKey corresponde à [PublicKey](/docs/specs/common-structures/#publickey) do LeaseSet. A PrivateKey é necessária para descriptografar mensagens roteadas por garlic encryption.

A revogação não está implementada. A conexão com múltiplos routers não está implementada em nenhuma biblioteca de cliente.

### CreateLeaseSet2Message {#CreateLeaseSet2Message}

#### Descrição

Esta mensagem é enviada em resposta a uma [RequestLeaseSetMessage](#RequestLeaseSetMessage) ou [RequestVariableLeaseSetMessage](#RequestVariableLeaseSetMessage) e contém todas as estruturas de [Lease](/docs/specs/common-structures/#lease) que devem ser publicadas no Network Database I2NP.

Enviado do Cliente para o Router. Desde a versão 0.9.39. Autenticação por cliente para EncryptedLeaseSet suportada a partir da 0.9.41. MetaLeaseSet ainda não é suportado via I2CP. Veja a proposta 123 para mais informações.

#### Conteúdo

1.  [ID da Sessão](#struct-sessionid)
2.  Um byte do tipo de leaseSet a seguir.

> - Tipo 1 é um [LeaseSet](/docs/specs/common-structures/#leaseset) (obsoleto) > - Tipo 3 é um [LeaseSet2](/docs/specs/common-structures/#leaseset2) > - Tipo 5 é um [EncryptedLeaseSet](/docs/specs/common-structures/#leaseset2) > - Tipo 7 é um [MetaLeaseSet](/docs/specs/common-structures/#leaseset2)

3.  [LeaseSet](/docs/specs/common-structures/#leaseset) ou
    [LeaseSet2](/docs/specs/common-structures/#leaseset2) ou
    [EncryptedLeaseSet](/docs/specs/common-structures/#leaseset2) ou
    [MetaLeaseSet](/docs/specs/common-structures/#leaseset2)
4.  Um byte com o número de chaves privadas a seguir.
5.  Lista de [PrivateKey](/docs/specs/common-structures/#privatekey). Uma para cada chave
    pública no lease set, na mesma ordem. (Não presente para Meta LS2)

> - Tipo de criptografia (2 bytes [Integer](/docs/specs/common-structures/#integer)) > - Comprimento da chave de criptografia (2 bytes [Integer](/docs/specs/common-structures/#integer)) > - [PrivateKey](/docs/specs/common-structures/#privatekey) de criptografia (número de bytes >   especificado)

#### Notas

As PrivateKeys correspondem a cada uma das [PublicKey](/docs/specs/common-structures/#publickey) do LeaseSet. As PrivateKeys são necessárias para descriptografar mensagens roteadas com garlic encryption.

Consulte a proposta 123 para mais informações sobre Encrypted LeaseSets.

O conteúdo e formato para MetaLeaseSet são preliminares e sujeitos a mudanças. Não há protocolo especificado para administração de múltiplos routers. Consulte a proposta 123 para mais informações.

A chave privada de assinatura, anteriormente definida para revogação e não utilizada, não está presente no LS2.

A versão preliminar com tipo de mensagem 40 estava na 0.9.38, mas o formato foi alterado. O tipo 40 foi abandonado e não é suportado. O tipo 41 não é válido até a 0.9.39.

### CreateSessionMessage {#CreateSessionMessage}

#### Descrição

Esta mensagem é enviada de um cliente para iniciar uma sessão, onde uma sessão é definida como a conexão de um único Destination à rede, para a qual todas as mensagens para esse Destination serão entregues e através da qual todas as mensagens que esse Destination envia para qualquer outro Destination serão enviadas.

Enviado do Cliente para o Router. O router responde com uma [SessionStatusMessage](#SessionStatusMessage).

#### Conteúdo

1.  [Configuração de Sessão](#struct-sessionconfig)

#### Notas

- Esta é a segunda mensagem enviada pelo cliente. Anteriormente o cliente
  enviou uma [GetDateMessage](#GetDateMessage) e recebeu uma
  resposta [SetDateMessage](#SetDateMessage).
- Se a Data na Configuração da Sessão estiver muito distante (mais de +/- 30
  segundos) do horário atual do router, a sessão será
  rejeitada.
- Se já existir uma sessão no router para este Destination, a
  sessão será rejeitada.
- O [Mapping](/docs/specs/common-structures/#mapping) na Configuração da Sessão deve estar
  ordenado por chave para que a assinatura seja validada corretamente no
  router.

### DestLookupMessage {#DestLookupMessage}

#### Descrição

Enviado do Cliente para o Router. O router responde com uma [DestReplyMessage](#DestReplyMessage).

#### Conteúdo

1.  SHA-256 [Hash](/docs/specs/common-structures/#hash)

#### Notas

A partir da versão 0.7.

A partir da versão 0.8.3, são suportadas múltiplas consultas pendentes, e as consultas são suportadas tanto no I2PSimpleSession quanto em sessões padrão.

[HostLookupMessage](#HostLookupMessage) é preferido a partir da versão 0.9.11.

### DestReplyMessage {#DestReplyMessage}

#### Descrição

Enviado do Router para o Cliente em resposta a uma [DestLookupMessage](#DestLookupMessage).

#### Conteúdo

1.  [Destination](/docs/specs/common-structures/#destination) em caso de sucesso, ou
    [Hash](/docs/specs/common-structures/#hash) em caso de falha

#### Notas

A partir da versão 0.7.

A partir da versão 0.8.3, o Hash solicitado é retornado se a consulta falhar, para que o cliente possa ter múltiplas consultas pendentes e correlacionar as respostas com as consultas. Para correlacionar uma resposta de Destination com uma solicitação, pegue o Hash do Destination. Antes da versão 0.8.3, a resposta era vazia em caso de falha.

### DestroySessionMessage {#DestroySessionMessage}

#### Descrição

Esta mensagem é enviada de um cliente para destruir uma sessão.

Enviado do Cliente para o Router. O router deve responder com uma [SessionStatusMessage](#SessionStatusMessage) (Destroyed). No entanto, veja as notas importantes abaixo.

#### Conteúdo

1.  [ID da Sessão](#struct-sessionid)

#### Notas

O router neste ponto deve liberar todos os recursos relacionados à sessão.

Através da API 0.9.66, o router Java I2P e as bibliotecas cliente desviam substancialmente desta especificação. O router nunca envia uma resposta SessionStatus(Destroyed). Se não restarem sessões, ele envia uma [DisconnectMessage](#DisconnectMessage). Se houver subsessões ou a sessão primária permanecer, ele não responde.

A biblioteca cliente Java responde a uma mensagem SessionStatus destruindo todas as sessões e reconectando.

Destruir subsessões individuais em uma conexão com múltiplas sessões pode não estar totalmente testado ou funcionando em várias implementações de router e cliente. Use com cautela.

As implementações devem tratar um destroy para uma sessão primária como um destroy para todas as subsessões, mas permitir um destroy para uma única subsessão e manter a conexão aberta, mas o Java I2P não faz isso atualmente. Se o comportamento do Java I2P for alterado em versões subsequentes, será documentado aqui.

### DisconnectMessage {#DisconnectMessage}

#### Descrição

Informa à outra parte que há problemas e que a conexão atual está prestes a ser destruída. Isso encerra todas as sessões nessa conexão. O socket será fechado em breve. Enviado tanto do router para o cliente quanto do cliente para o router.

#### Conteúdos

1.  Motivo [String](/docs/specs/common-structures/#string)

#### Notas

Implementado apenas na direção router-para-cliente, pelo menos no Java I2P.

### GetBandwidthLimitsMessage {#GetBandwidthLimitsMessage}

#### Descrição

Solicitar que o router informe quais são seus limites atuais de largura de banda.

Enviado do Cliente para o Router. O router responde com uma [BandwidthLimitsMessage](#BandwidthLimitsMessage).

#### Conteúdo

*Nenhum*

#### Notas

A partir da versão 0.7.2.

A partir da versão 0.8.3, suportado tanto no I2PSimpleSession quanto em sessões padrão.

### GetDateMessage {#GetDateMessage}

#### Descrição

Enviado do Cliente para o Router. O router responde com uma [SetDateMessage](#SetDateMessage).

#### Conteúdo

1.  Versão da API I2CP [String](/docs/specs/common-structures/#string)
2.  Autenticação [Mapping](/docs/specs/common-structures/#mapping) (opcional, a partir da
    versão 0.9.11)

#### Notas

- Geralmente a primeira mensagem enviada pelo cliente após enviar o
  byte da versão do protocolo.
- A string da versão é incluída a partir da versão 0.8.7. Isso só é
  útil se o cliente e o router não estiverem na mesma JVM. Se não
  estiver presente, o cliente é da versão 0.8.6 ou anterior.
- A partir da versão 0.9.11, o
  [Mapping](/docs/specs/common-structures/#mapping) de autenticação pode ser incluído, com as chaves
  i2cp.username e i2cp.password. O Mapping não precisa estar ordenado pois
  esta mensagem não é assinada. Antes e incluindo a versão 0.9.10,
  a autenticação é incluída no
  Mapping [Session Config](#struct-sessionconfig),
  e nenhuma autenticação é aplicada para
  [GetDateMessage](#GetDateMessage),
  [GetBandwidthLimitsMessage](#GetBandwidthLimitsMessage), ou
  [DestLookupMessage](#DestLookupMessage). Quando habilitada, autenticação
  via [GetDateMessage](#GetDateMessage) é obrigatória antes de qualquer outra
  mensagem a partir da versão 0.9.16. Isso só é útil fora do contexto do router.
  Esta é uma mudança incompatível, mas só afetará sessões
  fora do contexto do router com autenticação, o que deve ser raro.

### HostLookupMessage {#HostLookupMessage}

#### Descrição

Enviado do Cliente para o Router. O router responde com uma [HostReplyMessage](#HostReplyMessage).

Isso substitui o [DestLookupMessage](#DestLookupMessage) e adiciona um ID de solicitação, um timeout e suporte para pesquisa de nome de host. Como também suporta pesquisas Hash, pode ser usado para todas as pesquisas se o router suportar. Para pesquisas de nome de host, o router consultará o serviço de nomeação do seu contexto. Isso só é útil se o cliente estiver fora do contexto do router. Dentro do contexto do router, o cliente deve consultar o próprio serviço de nomeação, o que é muito mais eficiente.

#### Conteúdo

1.  [Session ID](#struct-sessionid)
2.  4 byte [Integer](/docs/specs/common-structures/#integer) ID da requisição
3.  4 byte [Integer](/docs/specs/common-structures/#integer) timeout (ms)
4.  1 byte [Integer](/docs/specs/common-structures/#integer) tipo de requisição
5.  SHA-256 [Hash](/docs/specs/common-structures/#hash) ou nome do host
    [String](/docs/specs/common-structures/#string) ou
    [Destination](/docs/specs/common-structures/#destination)

Tipos de solicitação:

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Type</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Lookup key (item 5)</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">As of</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Hash</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">host name String</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">2</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Hash</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.66</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">3</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">host name String</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.66</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">4</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Destination</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.66</td>
</tr>
</table>
Tipos 2-4 solicitam que o mapeamento de opções do LeaseSet seja retornado na mensagem HostReply. Veja a proposta 167.

#### Notas

- A partir da versão 0.9.11. Use [DestLookupMessage](#DestLookupMessage) para
  routers mais antigos.
- O ID da sessão e o ID da solicitação serão retornados na
  [HostReplyMessage](#HostReplyMessage). Use 0xFFFF para o ID da sessão
  se não houver sessão.
- Timeout é útil para consultas de Hash. Mínimo recomendado de 10.000 (10
  seg.). No futuro também pode ser útil para consultas de serviços de
  nomenclatura remotos. O valor pode não ser respeitado para consultas de
  nomes de host locais, que devem ser rápidas.
- A consulta de nome de host Base 32 é suportada, mas é preferível convertê-lo
  para um Hash primeiro.

### HostReplyMessage {#HostReplyMessage}

#### Descrição

Enviado do Router para o Cliente em resposta a uma [HostLookupMessage](#HostLookupMessage).

#### Conteúdo

1.  [Session ID](#struct-sessionid)
2.  4 bytes [Integer](/docs/specs/common-structures/#integer) ID da requisição
3.  1 byte [Integer](/docs/specs/common-structures/#integer) código de resultado

> - 0: Sucesso > - 1: Falha > - 2: Senha de consulta necessária (a partir da versão 0.9.43) > - 3: Chave privada necessária (a partir da versão 0.9.43) > - 4: Senha de consulta e chave privada necessárias (a partir da versão 0.9.43) > - 5: Falha na descriptografia do leaseSet (a partir da versão 0.9.43) > - 6: Falha na consulta do leaseSet (a partir da versão 0.9.66) > - 7: Tipo de consulta não suportado (a partir da versão 0.9.66)

4.  [Destination](/docs/specs/common-structures/#destination), presente apenas se o código de resultado
    for zero, exceto que também pode ser retornado para tipos de lookup 2-4. Veja
    abaixo.
5.  [Mapping](/docs/specs/common-structures/#mapping), presente apenas se o código de resultado for
    zero, retornado apenas para tipos de lookup 2-4. A partir da versão 0.9.66. Veja abaixo.

#### Respostas para tipos de consulta 2-4

A Proposta 167 define tipos de pesquisa adicionais que retornam todas as opções do leaseSet, se presente. Para tipos de pesquisa 2-4, o router deve buscar o leaseSet, mesmo que a chave de pesquisa esteja no livro de endereços.

Se bem-sucedido, o HostReply conterá as opções Mapping do leaseset, e as inclui como item 5 após o destino. Se não houver opções no Mapping, ou o leaseset foi versão 1, ainda será incluído como um Mapping vazio (dois bytes: 0 0). Todas as opções do leaseset serão incluídas, não apenas opções de registro de serviço. Por exemplo, opções para parâmetros definidos no futuro podem estar presentes. O Mapping retornado pode ou não estar ordenado, dependendo da implementação.

Em caso de falha na busca do leaseSet, a resposta conterá um novo código de erro 6 (Falha na busca do leaseSet) e não incluirá um mapeamento. Quando o código de erro 6 for retornado, o campo Destination pode ou não estar presente. Estará presente se uma busca de hostname no livro de endereços foi bem-sucedida, ou se uma busca anterior foi bem-sucedida e o resultado foi armazenado em cache, ou se o Destination estava presente na mensagem de busca (tipo de busca 4).

Se um tipo de consulta não for suportado, a resposta conterá um novo código de erro 7 (tipo de consulta não suportado).

#### Notas

- A partir da versão 0.9.11. Veja as notas da [HostLookupMessage](#HostLookupMessage).
- O ID da sessão e o ID da solicitação são aqueles da [HostLookupMessage](#HostLookupMessage).
- O código de resultado é 0 para sucesso, 1-255 para falha. 1 indica uma falha genérica. A partir da versão 0.9.43, os códigos de falha adicionais 2-5 foram definidos para suportar erros estendidos para lookups "b33". Veja as propostas 123 e 149 para informações adicionais. A partir da versão 0.9.66, os códigos de falha adicionais 6-7 foram definidos para suportar erros estendidos para lookups tipo 2-4. Veja a proposta 167 para informações adicionais.

### MessagePayloadMessage {#MessagePayloadMessage}

#### Descrição

Entregar a carga útil de uma mensagem ao cliente.

Enviado do Router para o Cliente. Se i2cp.fastReceive=true, que não é o padrão, o cliente responde com um [ReceiveMessageEndMessage](#ReceiveMessageEndMessage).

#### Conteúdo

1.  [ID da Sessão](#struct-sessionid)
2.  [ID da Mensagem](#struct-messageid)
3.  [Payload](#struct-payload)

#### Notas

### MessageStatusMessage {#MessageStatusMessage}

#### Descrição

Notificar o cliente sobre o status de entrega de uma mensagem recebida ou enviada. Enviada do Router para o Cliente. Se esta mensagem indicar que uma mensagem recebida está disponível, o cliente responde com uma [ReceiveMessageBeginMessage](#ReceiveMessageBeginMessage). Para uma mensagem enviada, esta é uma resposta a uma [SendMessageMessage](#SendMessageMessage) ou [SendMessageExpiresMessage](#SendMessageExpiresMessage).

#### Conteúdo

1.  [Session ID](#struct-sessionid)
2.  [Message ID](#struct-messageid) gerado pelo router
3.  1 byte [Integer](/docs/specs/common-structures/#integer) status
4.  4 byte [Integer](/docs/specs/common-structures/#integer) tamanho
5.  4 byte [Integer](/docs/specs/common-structures/#integer) nonce previamente gerado
    pelo cliente

#### Notas

Até a versão 0.9.4, os valores de status conhecidos são 0 para mensagem está disponível, 1 para aceita, 2 para melhor esforço bem-sucedido, 3 para melhor esforço falhou, 4 para garantido bem-sucedido, 5 para garantido falhou. O Integer de tamanho especifica o tamanho da mensagem disponível e é relevante apenas para status = 0. Embora o garantido não esteja implementado (melhor esforço é o único serviço), a implementação atual do router usa os códigos de status garantido, não os códigos de melhor esforço.

A partir da versão 0.9.5 do router, códigos de status adicionais são definidos, porém não são necessariamente implementados. Consulte [MessageStatusMessage Javadocs](http://javadoc.i2p.net/net/i2p/data/i2cp/MessageStatusMessage.html) para detalhes. Para mensagens de saída, os códigos 1, 2, 4 e 6 indicam sucesso; todos os outros são falhas. Os códigos de falha retornados podem variar e são específicos da implementação.

Todos os códigos de status:

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Status Code</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">As Of Release</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Name</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Description</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Available</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">DEPRECATED. For incoming messages only. All other status codes below are for outgoing messages. The included size is the size in bytes of the available message. This is unused in "fast receive" mode, which is the default as of release 0.9.4.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Accepted</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Outgoing message accepted by the local router for delivery. The included nonce matches the nonce in the <a href="#SendMessageMessage">SendMessageMessage</a>, and the included Message ID will be used for subsequent success or failure notification.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">2</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Best Effort Success</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Probable success (unused)</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">3</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Best Effort Failure</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Probable failure</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">4</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Guaranteed Success</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Probable success</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Guaranteed Failure</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Generic failure, specific cause unknown. May not really be a guaranteed failure.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">6</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Local Success</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Local delivery successful. The destination was another client on the same router.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">7</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Local Failure</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Local delivery failure. The destination was another client on the same router.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">8</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Router Failure</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">The local router is not ready, has shut down, or has major problems. This is a guaranteed failure.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">9</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Network Failure</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">The local computer apparently has no network connectivity at all. This is a guaranteed failure.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">10</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Bad Session</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">The I2CP session is invalid or closed. This is a guaranteed failure.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">11</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Bad Message</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">The message payload is invalid or zero-length or too big. This is a guaranteed failure.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">12</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Bad Options</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Something is invalid in the message options, or the expiration is in the past or too far in the future. This is a guaranteed failure.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">13</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Overflow Failure</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Some queue or buffer in the router is full and the message was dropped. This is a guaranteed failure.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">14</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Message Expired</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">The message expired before it could be sent. This is a guaranteed failure.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">15</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Bad Local Leaseset</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">The client has not yet signed a <a href="/docs/specs/common-structures/#leaseset">LeaseSet</a>, or the local keys are invalid, or it has expired, or it does not have any tunnels in it. This is a guaranteed failure.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">16</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">No Local Tunnels</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Local problems. No outbound tunnel to send through, or no inbound tunnel if a reply is required. This is a guaranteed failure.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">17</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Unsupported Encryption</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">The certs or options in the <a href="/docs/specs/common-structures/#destination">Destination</a> or its <a href="/docs/specs/common-structures/#leaseset">LeaseSet</a> indicate that it uses an encryption format that we don't support, so we can't talk to it. This is a guaranteed failure.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">18</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Bad Destination</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Something is wrong with the far-end <a href="/docs/specs/common-structures/#destination">Destination</a>. Bad format, unsupported options, certificates, etc. This is a guaranteed failure.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">19</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Bad Leaseset</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">We got the far-end <a href="/docs/specs/common-structures/#leaseset">LeaseSet</a> but something strange is wrong with it. Unsupported options or certificates, no tunnels, etc. This is a guaranteed failure.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">20</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Expired Leaseset</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">We got the far-end <a href="/docs/specs/common-structures/#leaseset">LeaseSet</a> but it's expired and we can't get a new one. This is a guaranteed failure.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">21</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">No Leaseset</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Could not find the far-end <a href="/docs/specs/common-structures/#leaseset">LeaseSet</a>. This is a common failure, equivalent to a DNS lookup failure. This is a guaranteed failure.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">22</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.41</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Meta Leaseset</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">The far-end destination's lease set was a meta lease set, and cannot be sent to. The client should request the meta lease set's contents with a HostLookupMessage, and select one of the hashes contained within to look up and send to. This is a guaranteed failure.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">23</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.62</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Loopback Denied</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">The message was attempted to be sent from and to the same destination or session. This is a guaranteed failure.</td>
</tr>
</table>
Quando status = 1 (aceito), o nonce corresponde ao nonce na [SendMessageMessage](#SendMessageMessage), e o Message ID incluído será usado para notificação subsequente de sucesso ou falha. Caso contrário, o nonce pode ser ignorado.

### ReceiveMessageBeginMessage {#ReceiveMessageBeginMessage}

DESCONTINUADO. Não suportado pelo i2pd.

#### Descrição

Solicita ao router que entregue uma mensagem da qual foi previamente notificado. Enviado do Cliente para o Router. O router responde com uma [MessagePayloadMessage](#MessagePayloadMessage).

#### Conteúdo

1.  [ID da Sessão](#struct-sessionid)
2.  [ID da Mensagem](#struct-messageid)

#### Notas

O [ReceiveMessageBeginMessage](#ReceiveMessageBeginMessage) é enviado como resposta a um [MessageStatusMessage](#MessageStatusMessage) declarando que uma nova mensagem está disponível para coleta. Se o id da mensagem especificado no [ReceiveMessageBeginMessage](#ReceiveMessageBeginMessage) for inválido ou incorreto, o router pode simplesmente não responder, ou pode enviar de volta um [DisconnectMessage](#DisconnectMessage).

Isto não é utilizado no modo "recepção rápida", que é o padrão desde a versão 0.9.4.

### ReceiveMessageEndMessage {#ReceiveMessageEndMessage}

DESCONTINUADO. Não suportado pelo i2pd.

#### Descrição

Informe o router que a entrega de uma mensagem foi concluída com sucesso e que o router pode descartar a mensagem.

Enviado do Cliente para o Router.

#### Conteúdos

1.  [ID da Sessão](#struct-sessionid)
2.  [ID da Mensagem](#struct-messageid)

#### Notas

O [ReceiveMessageEndMessage](#ReceiveMessageEndMessage) é enviado após um [MessagePayloadMessage](#MessagePayloadMessage) entregar completamente a carga útil de uma mensagem.

Isso não é usado no modo "recepção rápida", que é o padrão desde a versão 0.9.4.

### ReconfigureSessionMessage {#ReconfigureSessionMessage}

#### Descrição

Enviado do Cliente para o Router para atualizar a configuração da sessão. O router responde com uma [SessionStatusMessage](#SessionStatusMessage).

#### Conteúdo

1.  [ID da Sessão](#struct-sessionid)
2.  [Configuração da Sessão](#struct-sessionconfig)

#### Notas

- A partir da versão 0.7.1.
- Se a Data na Configuração da Sessão estiver muito distante (mais de +/- 30
  segundos) do horário atual do router, a sessão será
  rejeitada.
- O [Mapping](/docs/specs/common-structures/#mapping) na Configuração da Sessão deve estar
  ordenado por chave para que a assinatura seja validada corretamente no
  router.
- Algumas opções de configuração podem ser definidas apenas na
  [CreateSessionMessage](#CreateSessionMessage), e mudanças aqui não serão
  reconhecidas pelo router. Mudanças nas opções de tunnel inbound.\*
  e outbound.\* são sempre reconhecidas.
- Em geral, o router deve mesclar a configuração atualizada com a
  configuração atual, então a configuração atualizada precisa conter apenas as
  opções novas ou alteradas. No entanto, devido à mesclagem, as opções não podem ser
  removidas desta forma; elas devem ser definidas explicitamente para o valor
  padrão desejado.

### ReportAbuseMessage {#ReportAbuseMessage}

DESCONTINUADO, NÃO UTILIZADO, NÃO SUPORTADO

#### Descrição

Informar à outra parte (cliente ou router) que estão sob ataque, potencialmente com referência a um MessageId específico. Se o router estiver sob ataque, o cliente pode decidir migrar para outro router, e se um cliente estiver sob ataque, o router pode reconstruir seus routers ou colocar alguns dos peers que enviaram mensagens entregando o ataque na lista de bloqueio.

Enviado do router para o cliente ou do cliente para o router.

#### Conteúdo

1.  [Session ID](#struct-sessionid)
2.  1 byte [Integer](/docs/specs/common-structures/#integer) severidade do abuso (0 é
    minimamente abusivo, 255 sendo extremamente abusivo)
3.  Razão [String](/docs/specs/common-structures/#string)
4.  [Message ID](#struct-messageid)

#### Notas

Não utilizado. Não totalmente implementado. Tanto o router quanto o cliente podem gerar uma [ReportAbuseMessage](#ReportAbuseMessage), mas nenhum dos dois possui um manipulador para a mensagem quando recebida.

### RequestLeaseSetMessage {#RequestLeaseSetMessage}

OBSOLETO. Não suportado pelo i2pd. Não enviado pelo Java I2P para clientes versão 0.9.7 ou superior (2013-07). Use RequestVariableLeaseSetMessage.

#### Descrição

Solicita que um cliente autorize a inclusão de um conjunto específico de túneis de entrada. Enviado do Router para o Cliente. O cliente responde com uma [CreateLeaseSetMessage](#CreateLeaseSetMessage).

A primeira dessas mensagens enviadas numa sessão é um sinal ao cliente de que os tunnels estão construídos e prontos para tráfego. O router não deve enviar a primeira dessas mensagens até que pelo menos um tunnel de entrada E um tunnel de saída tenham sido construídos. Os clientes devem expirar o tempo limite e destruir a sessão se a primeira dessas mensagens não for recebida após algum tempo (recomendado: 5 minutos ou mais).

#### Conteúdo

1.  [Session ID](#struct-sessionid)
2.  1 byte [Integer](/docs/specs/common-structures/#integer) número de tunnels
3.  Essa quantidade de pares de:
    1.  [Hash](/docs/specs/common-structures/#hash)
    2.  [TunnelId](/docs/specs/common-structures/#tunnelid)
4.  [Date](/docs/specs/common-structures/#date) de fim

#### Notas

Isso solicita um [LeaseSet](/docs/specs/common-structures/#leaseset) com todas as entradas [Lease](/docs/specs/common-structures/#lease) configuradas para expirar ao mesmo tempo. Para versões de cliente 0.9.7 ou superior, [RequestVariableLeaseSetMessage](#RequestVariableLeaseSetMessage) é usado.

### RequestVariableLeaseSetMessage {#RequestVariableLeaseSetMessage}

#### Descrição

Solicitar que um cliente autorize a inclusão de um conjunto específico de tunnels de entrada.

Enviado do Router para o Cliente. O cliente responde com uma [CreateLeaseSetMessage](#CreateLeaseSetMessage) ou [CreateLeaseSet2Message](#CreateLeaseSet2Message).

A primeira dessas mensagens enviada numa sessão é um sinal ao cliente de que os tunnels foram construídos e estão prontos para o tráfego. O router não deve enviar a primeira dessas mensagens até que pelo menos um tunnel de entrada E um tunnel de saída tenham sido construídos. Os clientes devem expirar o tempo limite e destruir a sessão se a primeira dessas mensagens não for recebida após algum tempo (recomendado: 5 minutos ou mais).

#### Conteúdo

1.  [Session ID](#struct-sessionid)
2.  1 byte [Integer](/docs/specs/common-structures/#integer) número de tunnels
3.  Esse número de entradas [Lease](/docs/specs/common-structures/#lease)

#### Notas

Isto solicita um [LeaseSet](/docs/specs/common-structures/#leaseset) com um tempo de expiração individual para cada [Lease](/docs/specs/common-structures/#lease).

A partir da versão 0.9.7. Para clientes anteriores a essa versão, use [RequestLeaseSetMessage](#RequestLeaseSetMessage).

### SendMessageMessage {#SendMessageMessage}

#### Descrição

Assim é como um cliente envia uma mensagem (o payload) para o [Destination](/docs/specs/common-structures/#destination). O router usará uma expiração padrão.

Enviado do Cliente para o Router. O router responde com uma [MessageStatusMessage](#MessageStatusMessage).

#### Conteúdo

1.  [Session ID](#struct-sessionid)
2.  [Destination](/docs/specs/common-structures/#destination)
3.  [Payload](#struct-payload)
4.  4 bytes [Integer](/docs/specs/common-structures/#integer) nonce

#### Notas

Assim que a [SendMessageMessage](#SendMessageMessage) chegar completamente intacta, o router deve retornar uma [MessageStatusMessage](#MessageStatusMessage) declarando que foi aceita para entrega. Essa mensagem conterá o mesmo nonce enviado aqui. Posteriormente, com base nas garantias de entrega da configuração da sessão, o router pode adicionalmente enviar de volta outra [MessageStatusMessage](#MessageStatusMessage) atualizando o status.

A partir da versão 0.8.1, o router não envia nenhum [MessageStatusMessage](#MessageStatusMessage) se i2cp.messageReliability=none.

Antes da versão 0.9.4, um valor de nonce 0 não era permitido. A partir da versão 0.9.4, um valor de nonce 0 é permitido, e informa ao router que ele não deve enviar [MessageStatusMessage](#MessageStatusMessage), ou seja, age como se i2cp.messageReliability=none apenas para esta mensagem.

Antes da versão 0.9.14, uma sessão com i2cp.messageReliability=none não podia ser substituída numa base por mensagem. A partir da versão 0.9.14, numa sessão com i2cp.messageReliability=none, o cliente pode solicitar a entrega de uma [MessageStatusMessage](#MessageStatusMessage) com o sucesso ou falha da entrega definindo o nonce para um valor diferente de zero. O router não enviará a [MessageStatusMessage](#MessageStatusMessage) "aceite" mas posteriormente enviará ao cliente uma [MessageStatusMessage](#MessageStatusMessage) com o mesmo nonce, e um valor de sucesso ou falha.

### SendMessageExpiresMessage {#SendMessageExpiresMessage}

#### Descrição

Enviado do Cliente para o Router. Mesmo que [SendMessageMessage](#SendMessageMessage), exceto que inclui uma expiração e opções.

#### Conteúdo

1.  [Session ID](#struct-sessionid)
2.  [Destination](/docs/specs/common-structures/#destination)
3.  [Payload](#struct-payload)
4.  4 bytes [Integer](/docs/specs/common-structures/#integer) nonce
5.  2 bytes de flags (opções)
6.  [Date](/docs/specs/common-structures/#date) de expiração truncada de 8 bytes para 6
    bytes

#### Notas

A partir da versão 0.7.1.

No modo "best effort", assim que a SendMessageExpiresMessage chegar completamente íntegra, o router deve retornar uma MessageStatusMessage indicando que foi aceita para entrega. Essa mensagem conterá o mesmo nonce enviado aqui. Posteriormente, baseado nas garantias de entrega da configuração da sessão, o router pode adicionalmente enviar de volta outra MessageStatusMessage atualizando o status.

A partir da versão 0.8.1, o router não envia nenhuma Message Status Message se i2cp.messageReliability=none.

Antes da versão 0.9.4, um valor de nonce 0 não era permitido. A partir da versão 0.9.4, um valor de nonce 0 é permitido, e informa ao router que ele não deve enviar nenhuma Message Status Message, ou seja, age como se i2cp.messageReliability=none apenas para esta mensagem.

Antes da versão 0.9.14, uma sessão com i2cp.messageReliability=none não podia ser substituída por mensagem individual. A partir da versão 0.9.14, numa sessão com i2cp.messageReliability=none, o cliente pode solicitar a entrega de uma Message Status Message com o sucesso ou falha da entrega definindo o nonce para um valor diferente de zero. O router não enviará a Message Status Message "accepted" mas posteriormente enviará ao cliente uma Message Status Message com o mesmo nonce, e um valor de sucesso ou falha.

#### Campo de Flags

A partir da versão 0.8.4, os dois bytes superiores da Data são redefinidos para conter flags. As flags devem ter como padrão todos os zeros para compatibilidade com versões anteriores. A Data não invadirá o campo de flags até o ano 10889. As flags podem ser usadas pela aplicação para fornecer dicas ao router sobre se um LeaseSet e/ou ElGamal/AES Session Tags devem ser entregues com a mensagem. As configurações afetarão significativamente a quantidade de overhead do protocolo e a confiabilidade da entrega de mensagens. Os bits individuais das flags são definidos da seguinte forma, a partir da versão 0.9.2. As definições estão sujeitas a alterações. Use a classe SendMessageOptions para construir as flags.

Ordem dos bits: 15...0

Bits 15-11

:   Não utilizado, deve ser zero

Bits 10-9

:   Substituição de Confiabilidade de Mensagem (Não implementado, a ser removido).

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Field value</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Description</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">00</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Use session setting i2cp.messageReliability (default)</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">01</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Use "best effort" message reliability for this message, overriding the session setting. The router will send one or more MessageStatusMessages in response. Unused. Use a nonzero nonce value to override a session setting of "none".</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">10</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Use "guaranteed" message reliability for this message, overriding the session setting. The router will send one or more MessageStatusMessages in response. Unused. Use a nonzero nonce value to override a session setting of "none".</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">11</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Unused. Use a nonce value of 0 to force "none" and override a session setting of "best effort" or "guaranteed".</td>
</tr>
</table>
Bit 8

:   Se 1, não incluir um lease set no garlic com esta mensagem. Se

    0, the router may bundle a lease set at its discretion.

Bits 7-4

:   Limite mínimo de tags. Se houver menos tags disponíveis que este número,

    send more. This is advisory and does not force tags to be delivered.
    For ElGamal only. Ignored for ECIES-Ratchet.

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Field value</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Tag threshold</th>
</tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">0000</td><td style="border: 1px solid var(--color-border); padding: 8px;">Use session key manager settings</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">0001</td><td style="border: 1px solid var(--color-border); padding: 8px;">2</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">0010</td><td style="border: 1px solid var(--color-border); padding: 8px;">3</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">0011</td><td style="border: 1px solid var(--color-border); padding: 8px;">6</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">0100</td><td style="border: 1px solid var(--color-border); padding: 8px;">9</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">0101</td><td style="border: 1px solid var(--color-border); padding: 8px;">14</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">0110</td><td style="border: 1px solid var(--color-border); padding: 8px;">20</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">0111</td><td style="border: 1px solid var(--color-border); padding: 8px;">27</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">1000</td><td style="border: 1px solid var(--color-border); padding: 8px;">35</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">1001</td><td style="border: 1px solid var(--color-border); padding: 8px;">45</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">1010</td><td style="border: 1px solid var(--color-border); padding: 8px;">57</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">1011</td><td style="border: 1px solid var(--color-border); padding: 8px;">72</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">1100</td><td style="border: 1px solid var(--color-border); padding: 8px;">92</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">1101</td><td style="border: 1px solid var(--color-border); padding: 8px;">117</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">1110</td><td style="border: 1px solid var(--color-border); padding: 8px;">147</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">1111</td><td style="border: 1px solid var(--color-border); padding: 8px;">192</td></tr>
</table>
Bits 3-0

:   Número de tags para enviar se necessário. Isto é consultivo e não

    force tags to be delivered. For ElGamal only. Ignored for
    ECIES-Ratchet.

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Field value</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Tags to send</th>
</tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">0000</td><td style="border: 1px solid var(--color-border); padding: 8px;">Use session key manager settings</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">0001</td><td style="border: 1px solid var(--color-border); padding: 8px;">2</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">0010</td><td style="border: 1px solid var(--color-border); padding: 8px;">4</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">0011</td><td style="border: 1px solid var(--color-border); padding: 8px;">6</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">0100</td><td style="border: 1px solid var(--color-border); padding: 8px;">8</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">0101</td><td style="border: 1px solid var(--color-border); padding: 8px;">12</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">0110</td><td style="border: 1px solid var(--color-border); padding: 8px;">16</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">0111</td><td style="border: 1px solid var(--color-border); padding: 8px;">24</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">1000</td><td style="border: 1px solid var(--color-border); padding: 8px;">32</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">1001</td><td style="border: 1px solid var(--color-border); padding: 8px;">40</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">1010</td><td style="border: 1px solid var(--color-border); padding: 8px;">51</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">1011</td><td style="border: 1px solid var(--color-border); padding: 8px;">64</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">1100</td><td style="border: 1px solid var(--color-border); padding: 8px;">80</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">1101</td><td style="border: 1px solid var(--color-border); padding: 8px;">100</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">1110</td><td style="border: 1px solid var(--color-border); padding: 8px;">125</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">1111</td><td style="border: 1px solid var(--color-border); padding: 8px;">160</td></tr>
</table>
### SessionStatusMessage {#SessionStatusMessage}

#### Descrição

Instruir o cliente sobre o status da sua sessão.

Enviado do Router para o Cliente, em resposta a uma [CreateSessionMessage](#CreateSessionMessage), [ReconfigureSessionMessage](#ReconfigureSessionMessage), ou [DestroySessionMessage](#DestroySessionMessage). Em todos os casos, incluindo em resposta à [CreateSessionMessage](#CreateSessionMessage), o router deve responder imediatamente (não aguardar a construção dos tunnels).

#### Conteúdo

1.  [Session ID](#struct-sessionid)
2.  1 byte [Integer](/docs/specs/common-structures/#integer) status

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Status</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Since</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Name</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Definition</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Destroyed</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">The session with the given ID is terminated. May be a response to a <a href="#DestroySessionMessage">DestroySessionMessage</a>.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Created</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">In response to a <a href="#CreateSessionMessage">CreateSessionMessage</a>, a new session with the given ID is now active.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">2</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Updated</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">In response to a <a href="#ReconfigureSessionMessage">ReconfigureSessionMessage</a>, an existing session with the given ID has been reconfigured.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">3</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Invalid</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">In response to a <a href="#CreateSessionMessage">CreateSessionMessage</a>, the configuration is invalid. The included session ID should be ignored. In response to a <a href="#ReconfigureSessionMessage">ReconfigureSessionMessage</a>, the new configuration is invalid for the session with the given ID.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">4</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.12</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Refused</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">In response to a <a href="#CreateSessionMessage">CreateSessionMessage</a>, the router was unable to create the session, perhaps due to limits being exceeded. The included session ID should be ignored.</td>
</tr>
</table>
#### Notas

Os valores de status são definidos acima. Se o status for Created, o Session ID é o identificador a ser usado para o resto da sessão.

### SetDateMessage {#SetDateMessage}

#### Descrição

A data e hora atuais. Enviada do Router para o Cliente como parte do handshake inicial. A partir da versão 0.9.20, também pode ser enviada a qualquer momento após o handshake para notificar o cliente sobre uma mudança no relógio.

#### Conteúdo

1.  [Data](/docs/specs/common-structures/#date)
2.  Versão da API I2CP [String](/docs/specs/common-structures/#string)

#### Notas

Esta é geralmente a primeira mensagem enviada pelo router. A string de versão está incluída a partir da versão 0.8.7. Isso só é útil se o cliente e o router não estiverem na mesma JVM. Se não estiver presente, o router é da versão 0.8.6 ou anterior.

Mensagens SetDate adicionais não serão enviadas para clientes na mesma JVM.

## Referências

- [Date](/docs/specs/common-structures/#date)
- [Destination](/docs/specs/common-structures/#destination)
- [EncryptedLeaseSet](/docs/specs/common-structures/#leaseset2)
- [Hash](/docs/specs/common-structures/#hash)
- [Visão Geral do I2CP](/docs/specs/i2cp/)
- [Javadocs do I2CP](http://javadoc.i2p.net/net/i2p/data/i2cp/package-summary.html)
- [Integer](/docs/specs/common-structures/#integer)
- [Lease](/docs/specs/common-structures/#lease)
- [LeaseSet](/docs/specs/common-structures/#leaseset)
- [LeaseSet2](/docs/specs/common-structures/#leaseset2)
- [Mapping](/docs/specs/common-structures/#mapping)
- [MetaLeaseSet](/docs/specs/common-structures/#leaseset2)
- [Javadocs do MessageStatusMessage](http://javadoc.i2p.net/net/i2p/data/i2cp/MessageStatusMessage.html)
- [PrivateKey](/docs/specs/common-structures/#privatekey)
- [PublicKey](/docs/specs/common-structures/#publickey)
- [RouterIdentity](/docs/specs/common-structures/#routeridentity)
- [SAMv3](/docs/api/samv3/)
- [Signature](/docs/specs/common-structures/#signature)
- [SigningPrivateKey](/docs/specs/common-structures/#signingprivatekey)
- [SigningPublicKey](/docs/specs/common-structures/#signingpublickey)
- [String](/docs/specs/common-structures/#string)
- [TunnelId](/docs/specs/common-structures/#tunnelid)
