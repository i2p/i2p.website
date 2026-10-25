---
title: "Visão geral do I2CP"
description: "Visão geral do Protocolo de Cliente I2P (I2CP) - gerenciamento de sessão, opções, formato de carga útil e multiplexação."
slug: "i2cp-overview"
aliases:
  - "/pt/docs/protocol/i2cp"
  - "/pt/docs/protocol/i2cp/"
  - "/pt/i2cp"
  - "/pt/i2cp/"
category: "Protocolos"
lastUpdated: "2025-04"
accurateFor: "0.9.66"
---

## Visão geral

O Protocolo de Cliente I2P (I2CP) expõe uma forte separação de responsabilidades entre o roteador e qualquer cliente que deseje se comunicar pela rede. Ele permite mensagens seguras e assíncronas enviando e recebendo mensagens por meio de um único socket TCP. Com o I2CP, uma aplicação cliente informa ao roteador quem ela é (sua "destinação"), quais compensações de anonimato, confiabilidade e latência devem ser feitas, e para onde as mensagens devem ser enviadas. Por sua vez, o roteador utiliza o I2CP para informar ao cliente quando mensagens chegaram, e para solicitar autorização para que alguns túneis sejam utilizados.

O próprio protocolo é implementado em Java, para fornecer o SDK do cliente. Este SDK é exposto no pacote i2p.jar, que implementa o lado cliente do I2CP. Os clientes nunca deveriam precisar acessar o pacote router.jar, que contém o roteador em si e o lado do roteador do I2CP. Um cliente não Java também teria que implementar a [biblioteca de streaming](/docs/api/streaming/) para conexões no estilo TCP.

Aplicativos podem aproveitar o I2CP básico mais as bibliotecas de [streaming](/docs/api/streaming/) e [datagrama](/docs/specs/datagrams/) utilizando o protocolo [Simple Anonymous Messaging (SAM)](/docs/api/samv3/), que não exige que os clientes lidem com qualquer tipo de criptografia. Além disso, os clientes podem acessar a rede por meio de diversos proxies – HTTP, CONNECT e SOCKS 4/4a/5. Alternativamente, clientes em Java podem acessar essas bibliotecas nos arquivos ministreaming.jar e streaming.jar. Assim, existem várias opções tanto para aplicações em Java quanto para aplicações não baseadas em Java.

A criptografia ponta a ponta no lado do cliente (criptografar os dados sobre a conexão I2CP) foi desativada na versão 0.6 do I2P, mantendo-se a criptografia ponta a ponta ElGamal/AES que é implementada no roteador. A única criptografia que as bibliotecas cliente ainda precisam implementar é a assinatura de chaves pública/privada DSA para [LeaseSets](/docs/specs/i2cp/#msg_CreateLeaseSet) e [Configurações de Sessão](/docs/specs/i2cp/#struct_SessionConfig), além da gestão dessas chaves.

Em uma instalação padrão do I2P, a porta 7654 é usada por clientes Java externos para se comunicar com o roteador local através do I2CP. Por padrão, o roteador vincula-se ao endereço 127.0.0.1. Para vincular-se ao 0.0.0.0, defina a opção avançada de configuração do roteador `i2cp.tcp.bindAllInterfaces=true` e reinicie. Clientes na mesma JVM que o roteador passam mensagens diretamente para o roteador através de uma interface interna da JVM.

Algumas implementações de roteador e cliente também podem suportar conexões externas por SSL, conforme configurado pela opção `i2cp.SSL=true`. Embora o SSL não seja o padrão, é fortemente recomendado para qualquer tráfego que possa ser exposto à Internet aberta. O usuário e senha de autorização (se houver), a [Chave Privada](/docs/specs/common-structures/#type_PrivateKey) e a [Chave Privada de Assinatura](/docs/specs/common-structures/#type_SigningPrivateKey) para a [Destinação](/docs/specs/common-structures/#struct_Destination) são todos transmitidos em texto claro, a menos que o SSL esteja habilitado. Algumas implementações de roteador e cliente também podem suportar conexões externas por meio de sockets de domínio.

## Especificação do Protocolo I2CP

Veja a [página de Especificação I2CP](/docs/specs/i2cp/) para a especificação completa do protocolo.

## Inicialização I2CP {#initialization}

Quando um cliente se conecta ao roteador, ele primeiro envia um único byte de versão do protocolo (0x2A). Em seguida, envia uma [Mensagem GetDate](/docs/specs/i2cp/#msg_GetDate) e aguarda a resposta da [Mensagem SetDate](/docs/specs/i2cp/#msg_SetDate). Depois, envia uma [Mensagem CreateSession](/docs/specs/i2cp/#msg_CreateSession) contendo a configuração da sessão. Em seguida, aguarda uma [Mensagem RequestLeaseSet](/docs/specs/i2cp/#msg_RequestLeaseSet) do roteador, indicando que os túneis de entrada foram criados, e responde com uma CreateLeaseSetMessage contendo o LeaseSet assinado. O cliente agora pode iniciar ou receber conexões de outras destinações I2P.

## Opções I2CP {#options}

### Opções do lado do roteador

As seguintes opções são tradicionalmente passadas para o roteador por meio de um [SessionConfig](/docs/specs/i2cp/#struct_SessionConfig) contido em uma [Mensagem CreateSession](/docs/specs/i2cp/#msg_CreateSession) ou em uma [Mensagem ReconfigureSession](/docs/specs/i2cp/#msg_ReconfigureSession).

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;" colspan="6">Router-side Options</th>
</tr>
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Option</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">As Of Release</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Recommended Arguments</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Allowable Range</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Default</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Description</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">clientMessageTimeout</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">8*1000 - 120*1000</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">60*1000</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">The timeout (ms) for all sent messages. Unused. See the protocol specification for per-message settings.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">crypto.lowTagThreshold</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.2</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1-128</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">30</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Minimum number of ElGamal/AES Session Tags before we send more. Recommended: approximately tagsToSend * 2/3</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">crypto.ratchet.inboundTags</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.47</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1-?</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">160</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Inbound tag window for ECIES-X25519-AEAD-Ratchet. Local inbound tagset size. See proposal 144.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">crypto.ratchet.outboundTags</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.47</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1-?</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">160</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Outbound tag window for ECIES-X25519-AEAD-Ratchet. Advisory to send to the far-end in the options block. See proposal 144.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">crypto.tagsToSend</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.2</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1-128</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">40</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Number of ElGamal/AES Session Tags to send at a time. For clients with relatively low bandwidth per-client-pair (IRC, some UDP apps), this may be set lower.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">explicitPeers</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">null</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Comma-separated list of Base 64 Hashes of peers to build tunnels through; for debugging only</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">i2cp.dontPublishLeaseSet</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">true, false</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">false</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Should generally be set to true for clients and false for servers</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">i2cp.fastReceive</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.4</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">true, false</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">false</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">If true, the router just sends the MessagePayload instead of sending a MessageStatus and awaiting a ReceiveMessageBegin.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">i2cp.leaseSetAuthType</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.41</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0-2</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">The type of authentication for encrypted LS2. 0 for no per-client authentication (the default); 1 for DH per-client authentication; 2 for PSK per-client authentication. See proposal 123.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">i2cp.leaseSetEncType</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.38</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">4,0</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0-65535,...</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">The encryption type to be used, as of 0.9.38. Interpreted client-side, but also passed to the router in the SessionConfig, to declare intent and check support. As of 0.9.39, may be comma-separated values for multiple types. See PublicKey in common structures spec for values. See proposals 123, 144, and 145.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">i2cp.leaseSetOfflineExpiration</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.38</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">The expiration of the offline signature, 4 bytes, seconds since the epoch. See proposal 123.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">i2cp.leaseSetOfflineSignature</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.38</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">The base 64 of the offline signature. See proposal 123.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">i2cp.leaseSetPrivKey</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.41</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">A base 64 X25519 private key for the router to use to decrypt the encrypted LS2 locally, only if per-client authentication is enabled. Optionally preceded by the key type and ':'. Only "ECIES_X25519:" is supported, which is the default. See proposal 123. Do not confuse with i2cp.leaseSetPrivateKey which is for the leaseset encryption keys.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">i2cp.leaseSetSecret</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.39</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">""</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Base 64 encoded UTF-8 secret used to blind the leaseset address. See proposal 123.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">i2cp.leaseSetTransientPublicKey</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.38</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">[type:]b64 The base 64 of the transient private key, prefixed by an optional sig type number or name, default DSA_SHA1. See proposal 123.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">i2cp.leaseSetType</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.38</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1,3,5,7</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1-255</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">The type of leaseset to be sent in the CreateLeaseSet2 Message. Interpreted client-side, but also passed to the router in the SessionConfig, to declare intent and check support. See proposal 123.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">i2cp.messageReliability</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">BestEffort, None</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">BestEffort</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Guaranteed is disabled; None implemented in 0.8.1; the streaming lib default is None as of 0.8.1, the client side default is None as of 0.9.4</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">i2cp.password</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.8.2</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">string</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;" rowspan="2">For authorization, if required by the router. If the client is running in the same JVM as a router, this option is not required. Warning - username and password are sent in the clear to the router, unless using SSL (i2cp.SSL=true). Authorization is only recommended when using SSL.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">i2cp.username</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.8.2</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">string</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">inbound.allowZeroHop</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">true, false</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">true</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">If incoming zero hop tunnel is allowed</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">outbound.allowZeroHop</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">true, false</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">true</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">If outgoing zero hop tunnel is allowed</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">inbound.backupQuantity</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">number from 0 to 3</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">No limit</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Number of redundant fail-over for tunnels in</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">outbound.backupQuantity</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">number from 0 to 3</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">No limit</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Number of redundant fail-over for tunnels out</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">inbound.IPRestriction</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">number from 0 to 4</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0 to 4</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">2</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Number of IP bytes to match to determine if two routers should not be in the same tunnel. 0 to disable.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">outbound.IPRestriction</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">number from 0 to 4</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0 to 4</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">2</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Number of IP bytes to match to determine if two routers should not be in the same tunnel. 0 to disable.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">inbound.length</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">number from 0 to 3</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0 to 7</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">3</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Length of tunnels in</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">outbound.length</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">number from 0 to 3</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0 to 7</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">3</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Length of tunnels out</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">inbound.lengthVariance</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">number from -1 to 2</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">-7 to 7</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Random amount to add or subtract to the length of tunnels in. A positive number x means add a random amount from 0 to x inclusive. A negative number -x means add a random amount from -x to x inclusive. The router will limit the total length of the tunnel to 0 to 7 inclusive. The default variance was 1 prior to release 0.7.6.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">outbound.lengthVariance</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">number from -1 to 2</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">-7 to 7</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Random amount to add or subtract to the length of tunnels out. A positive number x means add a random amount from 0 to x inclusive. A negative number -x means add a random amount from -x to x inclusive. The router will limit the total length of the tunnel to 0 to 7 inclusive. The default variance was 1 prior to release 0.7.6.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">inbound.nickname</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">string</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Name of tunnel - generally used in routerconsole, which will use the first few characters of the Base64 hash of the destination by default.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">outbound.nickname</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">string</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Name of tunnel - generally ignored unless inbound.nickname is unset.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">outbound.priority</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.4</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">number from -25 to 25</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">-25 to 25</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Priority adjustment for outbound messages. Higher is higher priority.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">inbound.quantity</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">number from 1 to 3</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1 to 16</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">2</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Number of tunnels in. Limit was increased from 6 to 16 in release 0.9; however, numbers higher than 6 are incompatible with older releases.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">outbound.quantity</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">number from 1 to 3</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">No limit</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">2</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Number of tunnels out</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">inbound.randomKey</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.17</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Base 64 encoding of 32 random bytes</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;" rowspan="2">Used for consistent peer ordering across restarts.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">outbound.randomKey</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.17</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Base 64 encoding of 32 random bytes</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">inbound.*</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Any other options prefixed with "inbound." are stored in the "unknown options" properties of the inbound tunnel pool's settings.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">outbound.*</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Any other options prefixed with "outbound." are stored in the "unknown options" properties of the outbound tunnel pool's settings.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">shouldBundleReplyInfo</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.2</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">true, false</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">true</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Set to false to disable ever bundling a reply LeaseSet. For clients that do not publish their LeaseSet, this option must be true for any reply to be possible. "true" is also recommended for multihomed servers with long connection times.

Setting to "false" may save significant outbound bandwidth, especially if the client is configured with a large number of inbound tunnels (Leases). If replies are still required, this may shift the bandwidth burden to the far-end client and the floodfill. There are several cases where "false" may be appropriate:

- Unidirectional communication, no reply required
- LeaseSet is published and higher reply latency is acceptable
- LeaseSet is published, client is a "server", all connections are inbound so the connecting far-end destination obviously has the leaseset already. Connections are either short, or it is acceptable for latency on a long-lived connection to temporarily increase while the other end re-fetches the LeaseSet after expiration. HTTP servers may fit these requirements.</td>
</tr>
</table>
Observação: Configurações com quantidade, comprimento ou variação elevados podem causar problemas significativos de desempenho ou confiabilidade.

Observação: A partir da versão 0.7.7, os nomes e valores das opções devem usar codificação UTF-8. Isso é principalmente útil para apelidos. Antes dessa versão, opções com caracteres multibyte eram corrompidas. Como as opções são codificadas em um [Mapping](/docs/specs/common-structures/#type_Mapping), todos os nomes e valores de opções são limitados a no máximo 255 bytes (não caracteres).

### Opções do lado do cliente

As seguintes opções são interpretadas no lado do cliente e serão interpretadas se passadas para a I2PSession através da chamada I2PClient.createSession(). A biblioteca de streaming também deve repassar essas opções ao I2CP. Outras implementações podem ter padrões diferentes.

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;" colspan="6">Client-side Options</th>
</tr>
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Option</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">As Of Release</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Recommended Arguments</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Allowable Range</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Default</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Description</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">i2cp.closeIdleTime</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.7.1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1800000</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">300000 minimum</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">(ms) Idle time required (default 30 minutes)</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">i2cp.closeOnIdle</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.7.1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">true, false</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">false</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Close I2P session when idle</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">i2cp.encryptLeaseSet</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.7.1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">true, false</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">false</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Encrypt the lease</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">i2cp.fastReceive</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.4</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">true, false</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">true</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">If true, the router just sends the MessagePayload instead of sending a MessageStatus and awaiting a ReceiveMessageBegin.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">i2cp.gzip</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.6.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">true, false</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">true</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Gzip outbound data</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">i2cp.leaseSetAuthType</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.41</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0-2</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">The type of authentication for encrypted LS2. 0 for no per-client authentication (the default); 1 for DH per-client authentication; 2 for PSK per-client authentication. See proposal 123.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">i2cp.leaseSetBlindedType</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.39</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0-65535</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">See prop. 123</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">The sig type of the blinded key for encrypted LS2. Default depends on the destination sig type. See proposal 123.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">i2cp.leaseSetClient.dh.nnn</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.41</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">b64name:b64pubkey</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">The base 64 of the client name (ignored, UI use only), followed by a ':', followed by the base 64 of the public key to use for DH per-client auth. nnn starts with 0. See proposal 123.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">i2cp.leaseSetClient.psk.nnn</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.41</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">b64name:b64privkey</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">The base 64 of the client name (ignored, UI use only), followed by a ':', followed by the base 64 of the private key to use for PSK per-client auth. nnn starts with 0. See proposal 123.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">i2cp.leaseSetEncType</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.38</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0-65535,...</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">The encryption type to be used, as of 0.9.38. Interpreted client-side, but also passed to the router in the SessionConfig, to declare intent and check support. As of 0.9.39, may be comma-separated values for multiple types. See also i2cp.leaseSetPrivateKey. See PublicKey in common structures spec for values. See proposals 123, 144, and 145.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">i2cp.leaseSetKey</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.7.1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">For encrypted leasesets. Base 64 SessionKey (44 characters)</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">i2cp.leaseSetOption.nnn</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.66</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">srvKey=srvValue</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">A service record to be placed in the LeaseSet2 options. Example: "_smtp._tcp=1 86400 0 0 25 ...b32.i2p". nnn starts with 0. See proposal 167.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">i2cp.leaseSetPrivateKey</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.18</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Base 64 private keys for encryption. Optionally preceded by the encryption type name or number and ':'. For LS1, only one key is supported, and only "0:" or "ELGAMAL_2048:" is supported, which is the default. As of 0.9.39, for LS2, multiple keys may be comma-separated, and each key must be a different encryption type. I2CP will generate the public key from the private key. Use for persistent leaseset keys across restarts. See proposals 123, 144, and 145. See also i2cp.leaseSetEncType. Do not confuse with i2cp.leaseSetPrivKey which is for encrypted LS2.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">i2cp.leaseSetSecret</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.39</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">""</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Base 64 encoded UTF-8 secret used to blind the leaseset address. See proposal 123.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">i2cp.leaseSetSigningPrivateKey</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.18</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Base 64 private key for signatures. Optionally preceded by the key type and ':'. DSA_SHA1 is the default. Key type must match the signature type in the destination. I2CP will generate the public key from the private key. Use for persistent leaseset keys across restarts.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">i2cp.leaseSetType</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.38</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1,3,5,7</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1-255</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">The type of leaseset to be sent in the CreateLeaseSet2 Message. Interpreted client-side, but also passed to the router in the SessionConfig, to declare intent and check support. See proposal 123.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">i2cp.messageReliability</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">BestEffort, None</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">None</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Guaranteed is disabled; None implemented in 0.8.1; None is the default as of 0.9.4</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">i2cp.reduceIdleTime</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.7.1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1200000</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">300000 minimum</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">(ms) Idle time required (default 20 minutes, minimum 5 minutes)</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">i2cp.reduceOnIdle</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.7.1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">true, false</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">false</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Reduce tunnel quantity when idle</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">i2cp.reduceQuantity</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.7.1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1 to 5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Tunnel quantity when reduced (applies to both inbound and outbound)</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">i2cp.SSL</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.8.3</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">true, false</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">false</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Connect to the router using SSL. If the client is running in the same JVM as a router, this option is ignored, and the client connects to that router internally.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">i2cp.tcp.host</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">127.0.0.1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Router hostname. If the client is running in the same JVM as a router, this option is ignored, and the client connects to that router internally.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">i2cp.tcp.port</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1-65535</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">7654</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Router I2CP port. If the client is running in the same JVM as a router, this option is ignored, and the client connects to that router internally.</td>
</tr>
</table>
Observação: Todos os argumentos, incluindo números, são strings. Valores verdadeiro/falso são strings não sensíveis a maiúsculas/minúsculas. Qualquer valor diferente de "true" (verdadeiro), independentemente de maiúsculas e minúsculas, é interpretado como falso. Todos os nomes de opções são sensíveis a maiúsculas e minúsculas.

## Formato dos Dados de Carga I2CP e Multiplexação {#format}

As mensagens de ponta a ponta manipuladas pelo I2CP (ou seja, os dados enviados pelo cliente em uma [SendMessageMessage](/docs/specs/i2cp/#msg_SendMessage) e recebidos pelo cliente em uma [MessagePayloadMessage](/docs/specs/i2cp/#msg_MessagePayload)) são compactados com um cabeçalho gzip padrão de 10 bytes que começa com 0x1F 0x8B 0x08 conforme especificado pela [RFC 1952](http://www.ietf.org/rfc/rfc1952.txt). A partir da versão 0.7.1, o I2P utiliza partes ignoradas do cabeçalho gzip para incluir informações de protocolo, porta de origem e porta de destino, permitindo assim o uso de streaming e datagramas no mesmo destino, e possibilitando que consultas/respostas usando datagramas funcionem de forma confiável na presença de múltiplos canais.

A função gzip não pode ser completamente desativada, no entanto, definir `i2cp.gzip=false` ajusta o nível de esforço do gzip para 0, o que pode economizar um pouco de CPU. As implementações podem escolher diferentes níveis de esforço do gzip por socket ou por mensagem, dependendo da avaliação da compressibilidade do conteúdo. Devido à compressibilidade do preenchimento do destino implementado na API 0.9.57 (proposta 161), recomenda-se a compressão dos pacotes SYN de streaming em ambas as direções e dos datagramas com resposta, mesmo que a carga útil não seja compressível. As implementações podem desejar escrever uma função trivial de gzip/descompactação para um esforço de gzip igual a 0, o que proporcionará grandes ganhos de eficiência em comparação com uma biblioteca gzip neste caso.

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Bytes</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Content</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0-2</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Gzip header 0x1F 0x8B 0x08</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">3</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Gzip flags</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">4-5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">I2P Source port (Gzip mtime)</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">6-7</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">I2P Destination port (Gzip mtime)</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">8</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Gzip xflags (set to 2 to be indistinguishable from the Java implementation)</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">9</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">I2P Protocol (6 = Streaming, 17 = Datagram, 18 = Raw Datagrams) (Gzip OS)</td>
</tr>
</table>
Observação: Os números de protocolo I2P de 224 a 254 são reservados para protocolos experimentais. O número de protocolo I2P 255 é reservado para expansão futura.

A integridade dos dados é verificada com o CRC-32 padrão gzip conforme especificado em [RFC 1952](http://www.ietf.org/rfc/rfc1952.txt).

## Diferenças Importantes em Relação ao IP Padrão {#ip-differences}

As portas I2CP são para sockets e datagramas I2P. Elas não têm relação com seus sockets ou portas locais. Como o I2P não suportava portas e números de protocolo antes da versão 0.7.1, as portas e números de protocolo são um pouco diferentes das usadas em IP padrão, por compatibilidade com versões anteriores:

- A porta 0 é válida e possui significado especial.
- As portas 1-1023 não são especiais nem privilegiadas.
- Servidores escutam na porta 0 por padrão, o que significa "todas as portas".
- Clientes enviam para a porta 0 por padrão, o que significa "qualquer porta".
- Clientes enviam da porta 0 por padrão, o que significa "não especificado".
- Servidores podem ter um serviço escutando na porta 0 e outros serviços escutando em portas superiores. Nesse caso, o serviço na porta 0 é o padrão e será usado se a porta do socket ou datagrama de entrada não corresponder a outro serviço.
- A maioria dos destinos I2P executa apenas um serviço, portanto você pode usar os valores padrão e ignorar a configuração de porta I2CP.
- O protocolo 0 é válido e significa "qualquer protocolo". No entanto, isso não é recomendado e provavelmente não funcionará. O streaming exige que o número do protocolo seja definido como 6.
- Os sockets de streaming são rastreados por um ID interno de conexão. Portanto, não é necessário que a 5-tupla de dest:porta:dest:porta:protocolo seja única. Por exemplo, pode haver vários sockets com as mesmas portas entre dois destinos. Os clientes não precisam escolher uma "porta livre" para uma conexão de saída.

## Trabalhos Futuros {#future}

- O mecanismo atual de autorização poderia ser modificado para usar senhas com hash.
- A Chave Privada de Assinatura está incluída na mensagem Criar Conjunto de Arrendamento (Create Lease Set), mas não é necessária. A revogação não está implementada. Ela deveria ser substituída por dados aleatórios ou removida.
- Algumas melhorias podem ser capazes de usar mensagens previamente definidas, mas não implementadas.
