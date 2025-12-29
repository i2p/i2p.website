---
title: "Protocolo de Rede I2P (I2NP)"
description: "Formatos de mensagens de router para router, prioridades e limites de tamanho dentro do I2P."
slug: "i2np"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

## Visão geral

O I2P Network Protocol (I2NP, protocolo de rede do I2P) define como routers trocam mensagens, selecionam transportes e misturam o tráfego preservando o anonimato. Ele opera entre **I2CP** (API do cliente) e os protocolos de transporte (**NTCP2** e **SSU2**).

I2NP é a camada acima dos protocolos de transporte do I2P. É um protocolo de router-para-router usado para: - Consultas e respostas ao banco de dados da rede - Criação de tunnels - Mensagens de dados de router e cliente criptografadas

Mensagens I2NP podem ser enviadas ponto a ponto para outro router, ou enviadas anonimamente através de tunnels para esse router.

Os Routers enfileiram o trabalho de saída usando prioridades locais. Números de prioridade mais altos são processados primeiro. Qualquer coisa acima da prioridade padrão de dados de tunnel (400) é tratada como urgente.

### Transportes Atuais

I2P agora usa **NTCP2** (TCP) e **SSU2** (UDP) tanto para IPv4 quanto para IPv6. Ambos os transportes utilizam: - **X25519** troca de chaves (Noise protocol framework — framework de protocolos Noise) - **ChaCha20/Poly1305** criptografia autenticada (AEAD) - **SHA-256** para cálculo de hash

**Transportes legados removidos:** - NTCP (TCP original) foi removido do Java router na versão 0.9.50 (maio de 2021) - SSU v1 (UDP original) foi removido do Java router na versão 2.4.0 (dezembro de 2023) - SSU v1 foi removido do i2pd na versão 2.44.0 (novembro de 2022)

A partir de 2025, a rede concluiu a transição para transportes baseados em Noise (framework de protocolos criptográficos), sem qualquer suporte a transportes legados.

---

## Sistema de numeração de versões

**IMPORTANTE:** I2P usa um sistema de versionamento duplo que deve ser claramente compreendido:

### Versões de Lançamento (voltadas para o usuário)

Estas são as versões que os usuários veem e baixam: - 0.9.50 (maio de 2021) - Última versão 0.9.x - **1.5.0** (agosto de 2021) - Primeira versão 1.x - 1.6.0, 1.7.0, 1.8.0, 1.9.0 (ao longo de 2021-2022) - **2.0.0** (novembro de 2022) - Primeira versão 2.x - 2.1.0 até 2.9.0 (ao longo de 2023-2025) - **2.10.0** (8 de setembro de 2025) - Versão atual

### Versões da API (Compatibilidade de Protocolo)

Estes são números de versão internos publicados no campo "router.version" nas propriedades do RouterInfo: - 0.9.50 (maio de 2021) - **0.9.51** (agosto de 2021) - Versão da API para o lançamento 1.5.0 - 0.9.52 até 0.9.66 (continuando ao longo dos lançamentos 2.x) - **0.9.67** (setembro de 2025) - Versão da API para o lançamento 2.10.0

**Ponto-chave:** NÃO houve versões numeradas de 0.9.51 a 0.9.67. Esses números existem apenas como identificadores de versão da API. I2P passou da versão 0.9.50 diretamente para a 1.5.0.

### Tabela de Mapeamento de Versões

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Release Version</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">API Version</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Date</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Key Features</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.50</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.50</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">May 2021</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Last 0.9.x release, removed NTCP1</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">1.5.0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.51</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">August 2021</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Short tunnel build messages (218 bytes)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">1.6.0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.52</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">November 2021</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Various improvements</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">1.7.0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.53</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">January 2022</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Performance enhancements</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">1.8.0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.54</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">May 2022</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">SSU2 introduced</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">1.9.0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.55</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">August 2022</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">SSU2 improvements</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">2.0.0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.56</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">November 2022</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">SSU2 enabled by default</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">2.1.0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.57</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">January 2023</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Stability improvements</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">2.2.0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.58</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">March 2023</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>ElGamal routers deprecated</strong></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">2.3.0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.59</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">May 2023</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Various improvements</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">2.4.0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.61</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">December 2023</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Removed SSU1 support</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">2.5.0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.62</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">February 2024</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Performance improvements</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">2.6.0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.63</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">May 2024</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Network optimizations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">2.7.0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.64</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">October 2024</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Post-quantum preparation work</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">2.8.0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.65</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">February 2025</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Tunnel bandwidth parameters</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">2.9.0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.66</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">June 2025</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">LeaseSet service records</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">2.10.0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">September 2025</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Post-quantum hybrid cryptography (beta)</td>
    </tr>
  </tbody>
</table>
**Em breve:** Versão 2.11.0 (prevista para dezembro de 2025) exigirá Java 17+ e habilitará a criptografia pós-quântica por padrão.

---

## Versões de Protocolo

Todos os routers devem publicar sua versão do protocolo I2NP no campo "router.version" nas propriedades do RouterInfo. Esse campo de versão é a versão da API, indicando o nível de suporte para vários recursos do protocolo I2NP, e não é necessariamente a versão real do router.

Se routers alternativos (não Java) desejarem publicar qualquer informação de versão sobre a implementação real do router, devem fazê-lo em outra propriedade. São permitidas versões diferentes das listadas abaixo. O suporte será determinado por meio de uma comparação numérica; por exemplo, 0.9.13 implica suporte para os recursos da 0.9.12.

**Observação:** A propriedade "coreVersion" não é mais publicada nas informações do router e nunca foi utilizada para determinar a versão do protocolo I2NP.

### Resumo de funcionalidades por versão da API

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">API Version</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Required I2NP Features</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Post-quantum hybrid cryptography (MLKEM ratchet) support (beta), UDP tracker support</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.66</td><td style="border:1px solid var(--color-border); padding:0.5rem;">LeaseSet2 service record options (see proposal 167)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.65</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Tunnel build bandwidth parameters (see proposal 168)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.59</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Minimum peers will build tunnels through (as of 0.9.63), minimum floodfill peers will send DSM to (as of 0.9.63)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.58</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Minimum peers will build tunnels through (as of 0.9.62), <strong>ElGamal routers deprecated</strong></td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.55</td><td style="border:1px solid var(--color-border); padding:0.5rem;">SSU2 transport support (if published in router info)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.51</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Short tunnel build messages for ECIES-X25519 routers, minimum peers will build tunnels through (as of 0.9.58), minimum floodfill peers will send DSM to (as of 0.9.58)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.49</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Garlic messages to ECIES-X25519 routers</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.48</td><td style="border:1px solid var(--color-border); padding:0.5rem;">ECIES-X25519 routers, ECIES-X25519 build request/response records</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.46</td><td style="border:1px solid var(--color-border); padding:0.5rem;">DatabaseLookup flag bit 4 for AEAD reply</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.44</td><td style="border:1px solid var(--color-border); padding:0.5rem;">ECIES-X25519 keys in LeaseSet2</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.40</td><td style="border:1px solid var(--color-border); padding:0.5rem;">MetaLeaseSet may be sent in a DSM</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.39</td><td style="border:1px solid var(--color-border); padding:0.5rem;">EncryptedLeaseSet may be sent in a DSM, RedDSA_SHA512_Ed25519 signature type supported</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.38</td><td style="border:1px solid var(--color-border); padding:0.5rem;">DSM type bits 3-0 now contain the type; LeaseSet2 may be sent in a DSM</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.36</td><td style="border:1px solid var(--color-border); padding:0.5rem;">NTCP2 transport support (if published in router info), minimum peers will build tunnels through (as of 0.9.46)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.28</td><td style="border:1px solid var(--color-border); padding:0.5rem;">RSA signature types disallowed, minimum floodfill peers will send DSM to (as of 0.9.34)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.18</td><td style="border:1px solid var(--color-border); padding:0.5rem;">DSM type bits 7-1 ignored</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.16</td><td style="border:1px solid var(--color-border); padding:0.5rem;">RI key certs / ECDSA and EdDSA signature types, DLM lookup types (flag bits 3-2), minimum version compatible with the current network</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.15</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Destination/LeaseSet key certificates with EdDSA Ed25519 signature type (if floodfill)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Destination/LeaseSet key certificates with ECDSA P-256, P-384, and P-521 signature types (if floodfill); non-zero expiration allowed in RouterAddress</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.7</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Encrypted DSM/DSRM replies supported (DLM flag bit 1) for floodfill routers</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.6</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Non-zero DLM flag bits 7-1 allowed</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.3</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Requires zero expiration in RouterAddress</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Supports up to 16 leases in a DSM LeaseSet store (previously 6)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.7.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">VTBM and VTBRM message support</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.7.10</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Floodfill supports encrypted DSM stores</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.6.1.10</td><td style="border:1px solid var(--color-border); padding:0.5rem;">TBM and TBRM messages introduced; minimum version compatible with the current network</td></tr>
  </tbody>
</table>
**Observação:** Há também recursos relacionados ao transporte e problemas de compatibilidade. Consulte a documentação de transporte do NTCP2 e do SSU2 para obter detalhes.

---

## Cabeçalho da Mensagem

O I2NP usa uma estrutura de cabeçalho lógica de 16 bytes, enquanto os transportes modernos (NTCP2 e SSU2) usam um cabeçalho reduzido de 9 bytes, omitindo campos redundantes de tamanho e soma de verificação. Os campos continuam conceitualmente idênticos.

### Comparação do Formato do Cabeçalho

**Formato Padrão (16 bytes):**

Usado no transporte NTCP legado e quando mensagens I2NP são incorporadas em outras mensagens (TunnelData, TunnelGateway, GarlicClove).

```
Bytes 0-15:
+----+----+----+----+----+----+----+----+
|type|      msg_id       |  expiration
+----+----+----+----+----+----+----+----+
                         |  size   |chks|
+----+----+----+----+----+----+----+----+

type :: Integer (1 byte)
        Identifies the message type (see message type table)

msg_id :: Integer (4 bytes)
          Uniquely identifies this message (for some time at least)
          Usually a locally-generated random number, but for outgoing
          tunnel build messages may be derived from the incoming message

expiration :: Date (8 bytes)
              Unix timestamp in milliseconds when this message expires

size :: Integer (2 bytes)
        Length of the payload (0 to ~61.2 KB for tunnel messages)

chks :: Integer (1 byte)
        SHA256 hash of payload truncated to first byte
        Deprecated - NTCP2/SSU2 use ChaCha20/Poly1305 AEAD for integrity
```
**Formato curto para SSU (obsoleto, 5 bytes):**

```
+----+----+----+----+----+
|type| short_expiration  |
+----+----+----+----+----+

type :: Integer (1 byte)
short_expiration :: Integer (4 bytes, seconds since epoch)
```
**Formato curto para NTCP2, SSU2 e ECIES-Ratchet Garlic Cloves (unidades de mensagem 'garlic') (9 bytes):**

Utilizado em transportes modernos e em mensagens garlic (mensagens agregadas no I2P) criptografadas com ECIES.

```
+----+----+----+----+----+----+----+----+
|type|      msg_id       | short_expira-
+----+----+----+----+----+----+----+----+
 tion|
+----+

type :: Integer (1 byte)
msg_id :: Integer (4 bytes)
short_expiration :: Integer (4 bytes, seconds since epoch, unsigned)
```
### Detalhes do campo de cabeçalho

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Field</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Bytes</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Type</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Identifies the message class (0&ndash;255, see message types below)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Unique ID</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Locally unique identifier for matching replies</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Expiration</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">8 (standard) / 4 (short)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Timestamp when the message expires. Routers discard expired messages. Short format uses seconds since epoch (unsigned, wraps February 7, 2106)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Payload Length</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Size in bytes (0 to ~61.2 KB for tunnel messages). NTCP2 and SSU2 encode this in their frame headers</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Checksum</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated. First byte of SHA-256 hash of the payload. NTCP2/SSU2 use ChaCha20/Poly1305 AEAD for integrity</td>
    </tr>
  </tbody>
</table>
### Notas de Implementação

- Ao ser transmitido via SSU (obsoleto), apenas o tipo e a expiração de 4 bytes foram incluídos
- Ao ser transmitido via NTCP2 ou SSU2, usa-se o formato curto de 9 bytes
- O cabeçalho padrão de 16 bytes é obrigatório para mensagens I2NP contidas em outras mensagens (Data, TunnelData, TunnelGateway, GarlicClove)
- A partir da versão 0.8.12, a verificação de checksum está desativada em alguns pontos da pilha do protocolo por eficiência, mas a geração de checksum ainda é necessária para compatibilidade
- A expiração curta é sem sinal e sofrerá wrap-around (reinício/estouro de contagem) em 7 de fevereiro de 2106. Após essa data, deve-se adicionar um deslocamento para obter a hora correta
- Por compatibilidade com versões antigas, sempre gere checksums, mesmo que possam não ser verificados

---

## Restrições de tamanho

Mensagens de tunnel fragmentam as cargas úteis do I2NP em partes de tamanho fixo: - **Primeiro fragmento:** aproximadamente 956 bytes - **Fragmentos subsequentes:** aproximadamente 996 bytes cada - **Máximo de fragmentos:** 64 (numerados de 0 a 63) - **Carga útil máxima:** aproximadamente 61.200 bytes (61,2 KB)

**Cálculo:** 956 + (63 × 996) = 63.704 bytes como máximo teórico, com limite prático em torno de 61.200 bytes devido à sobrecarga.

### Contexto histórico

Os transportes antigos tinham limites mais rígidos de tamanho de quadro: - NTCP: quadros de 16 KB - SSU: quadros de aproximadamente 32 KB

O NTCP2 suporta quadros de aproximadamente 65 KB, mas o limite de fragmentação do tunnel ainda se aplica.

### Considerações sobre Dados da Aplicação

Mensagens garlic (mensagens compostas) podem agrupar LeaseSets, tags de sessão ou variantes de LeaseSet2 criptografadas, reduzindo o espaço disponível para os dados da carga útil.

**Recomendação:** Datagramas devem ficar ≤ 10 KB para garantir entrega confiável. Mensagens que se aproximam do limite de 61 KB podem apresentar: - Maior latência devido à remontagem de fragmentos - Maior probabilidade de falha na entrega - Maior exposição à análise de tráfego

### Detalhes técnicos da fragmentação

Cada mensagem de tunnel tem exatamente 1.024 bytes (1 KB) e contém: - ID de tunnel de 4 bytes - vetor de inicialização (IV) de 16 bytes - 1.004 bytes de dados criptografados

Dentro dos dados criptografados, as mensagens de tunnel transportam mensagens I2NP fragmentadas com cabeçalhos de fragmento indicando: - Número do fragmento (0-63) - Se este é o primeiro fragmento ou um fragmento subsequente - ID total da mensagem para remontagem

O primeiro fragmento inclui o cabeçalho completo da mensagem I2NP (16 bytes), deixando aproximadamente 956 bytes para a carga útil. Os fragmentos subsequentes não incluem o cabeçalho da mensagem, permitindo aproximadamente 996 bytes de carga útil por fragmento.

---

## Tipos Comuns de Mensagens

Routers usam o tipo de mensagem e a prioridade para agendar o trabalho de saída. Valores de prioridade mais altos são processados primeiro. Os valores abaixo correspondem aos padrões atuais do Java I2P (a partir da versão da API 0.9.67).

**Nota:** As prioridades dependem da implementação. Para valores de prioridade definitivos, consulte a documentação da classe `OutNetMessage` no código-fonte do I2P em Java.

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Message</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Priority</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Typical Size</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Purpose</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>DatabaseStore</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">460</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Varies (LeaseSet ≈ 898&nbsp;B, RouterInfo ≈ 2&ndash;4&nbsp;KB compressed)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Publishes RouterInfo or LeaseSet objects. Supports LeaseSet2, EncryptedLeaseSet, and MetaLeaseSet</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>DatabaseLookup</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">500</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Varies</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Queries the network database for RouterInfo or LeaseSet entries</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>DatabaseSearchReply</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">300</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">≈161&nbsp;B (5 hashes)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Returns candidate floodfill router hashes (typically 3&ndash;16 hashes, recommended maximum 16)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>DeliveryStatus</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">10</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Varies</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">12&nbsp;B</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Receipts for tunnel tests or acknowledgements inside GarlicMessages</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>GarlicMessage</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">11</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">100 (local)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Varies</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Bundles multiple message cloves (e.g., DataMessage, LeaseSets). Supports ElGamal/AES (deprecated) and ECIES-X25519-AEAD-Ratchet encryption</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>TunnelData</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">18</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">400</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">1,028&nbsp;B (fixed)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Encrypted tunnel message exchanged between hops. Contains a 4-byte tunnel ID, 16-byte IV, and 1,004 bytes of encrypted data</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>TunnelGateway</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">19</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">300&ndash;400</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Varies</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Encapsulates messages at the tunnel gateway before fragmentation</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>DataMessage</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">20</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">425</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">4&ndash;62&nbsp;KB</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Carries end-to-end garlic payloads (application traffic)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>TunnelBuild</strong> <em>(deprecated)</em></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">21</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">500</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">4,224&nbsp;B</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Requests tunnel participation from routers (8 × 528-byte records). Replaced by VariableTunnelBuild for ECIES</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>TunnelBuildReply</strong> <em>(deprecated)</em></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">22</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">300</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">4,224&nbsp;B</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Replies to TunnelBuild with accept/reject status per hop</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>VariableTunnelBuild</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">23</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">500</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">1,057&ndash;4,225&nbsp;B</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Variable-length tunnel build for ElGamal or ECIES-X25519 routers (1&ndash;8 records, API 0.9.12+)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>VariableTunnelBuildReply</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">24</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">300</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">1,057&ndash;4,225&nbsp;B</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Replies to VariableTunnelBuild</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>ShortTunnelBuild</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">25</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">500</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">873&ndash;1,745&nbsp;B</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Short tunnel build messages for ECIES-X25519 routers only (1&ndash;8 × 218-byte records, API 0.9.51+)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>OutboundTunnelBuildReply</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">26</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">300</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">873&ndash;1,745&nbsp;B</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Sent from outbound endpoint to originator for ECIES-X25519 routers (API 0.9.51+)</td>
    </tr>
  </tbody>
</table>
**Tipos de mensagem reservados:** - Tipo 0: Reservado - Tipos 4-9: Reservados para uso futuro - Tipos 12-17: Reservados para uso futuro - Tipos 224-254: Reservados para mensagens experimentais - Tipo 255: Reservado para expansão futura

### Notas sobre Tipos de Mensagem

- Mensagens do plano de controle (DatabaseLookup, TunnelBuild, etc.) normalmente trafegam através de **tunnels exploratórios**, não de tunnels de cliente, permitindo priorização independente
- Os valores de prioridade são aproximados e podem variar conforme a implementação
- TunnelBuild (21) e TunnelBuildReply (22) estão obsoletos, mas ainda são implementados por compatibilidade com tunnels muito longos (>8 saltos)
- A prioridade padrão de dados de tunnel é 400; qualquer valor acima disso é tratado como urgente
- O comprimento típico de um tunnel na rede atual é de 3-4 saltos, portanto a maioria das construções de tunnel usa ShortTunnelBuild (registros de 218 bytes) ou VariableTunnelBuild (registros de 528 bytes)

---

## Criptografia e Encapsulamento de Mensagens

Routers frequentemente encapsulam mensagens I2NP antes da transmissão, criando múltiplas camadas de criptografia. Uma mensagem DeliveryStatus (confirmação de entrega) pode estar: 1. Encapsulada em um GarlicMessage (criptografada) 2. Dentro de um DataMessage 3. Dentro de uma mensagem TunnelData (criptografada novamente)

Cada salto apenas decifra sua camada; o destino final revela a carga útil mais interna.

### Algoritmos de Criptografia

**Legado (em fase de descontinuação):** - ElGamal/AES + SessionTags (marcadores de sessão) - ElGamal-2048 para criptografia assimétrica - AES-256 para criptografia simétrica - session tags de 32 bytes

**Atual (Padrão desde a API 0.9.48):** - ECIES-X25519 + ChaCha20/Poly1305 AEAD com sigilo direto por meio de ratcheting (mecanismo de rotação de chaves) - framework do protocolo Noise (Noise_IK_25519_ChaChaPoly_SHA256 para destinos) - tags de sessão de 8 bytes (reduzidas de 32 bytes) - algoritmo Signal Double Ratchet para sigilo direto - Introduzido na versão 0.9.46 da API (2020) - Obrigatório para todos os routers a partir da versão 0.9.58 da API (2023)

**Futuro (Beta a partir da 2.10.0):** - Criptografia híbrida pós-quântica usando MLKEM (ML-KEM-768) combinada com X25519 - Hybrid ratchet (mecanismo de atualização de chaves) combinando acordo de chaves clássico e pós-quântico - Retrocompatível com ECIES-X25519 - Se tornará o padrão na versão 2.11.0 (dezembro de 2025)

### Descontinuação do Router ElGamal

**CRÍTICO:** Os routers ElGamal foram descontinuados a partir da versão 0.9.58 da API (versão 2.2.0, março de 2023). Como a versão mínima recomendada de floodfill para consulta agora é 0.9.58, as implementações não precisam implementar criptografia para routers de floodfill ElGamal.

**No entanto:** destinos ElGamal ainda são suportados para compatibilidade com versões anteriores. Clientes que usam criptografia ElGamal ainda podem se comunicar por meio de ECIES routers.

### Detalhes do ECIES-X25519-AEAD-Ratchet

Este é o tipo de criptografia 4 na especificação de criptografia do I2P. Ele fornece:

**Principais recursos:** - Sigilo futuro por meio de ratcheting (mecanismo de catraca criptográfica; novas chaves para cada mensagem) - Armazenamento reduzido de tags de sessão (8 bytes vs. 32 bytes) - Vários tipos de sessão (Nova sessão, Sessão existente, Uso único) - Baseado no protocolo Noise Noise_IK_25519_ChaChaPoly_SHA256 - Integrado ao algoritmo Double Ratchet do Signal

**Primitivas criptográficas:** - X25519 para acordo de chaves Diffie-Hellman - ChaCha20 para criptografia de fluxo - Poly1305 para autenticação de mensagens (AEAD) - SHA-256 para cálculo de hash - HKDF para derivação de chaves

**Gerenciamento de Sessão:** - Nova Sessão: Conexão inicial usando chave de destino estática - Sessão Existente: Mensagens subsequentes usando tags de sessão - Sessão de Uso Único: Sessões de mensagem única para menor sobrecarga

Consulte a [Especificação ECIES](/docs/specs/ecies/) e a [Proposta 144](/proposals/144-ecies-x25519-aead-ratchet/) para obter detalhes técnicos completos.

---

## Estruturas Comuns

As estruturas a seguir são elementos de múltiplas mensagens I2NP. Elas não são mensagens completas.

### Registro de Solicitação de Construção (ElGamal)

**OBSOLETO.** Utilizado apenas na rede atual quando um tunnel contém um ElGamal router. Veja [Criação de ECIES Tunnel](/docs/specs/implementation/) para o formato moderno.

**Finalidade:** Um registro dentro de um conjunto de vários registros para solicitar a criação de um salto no tunnel.

**Formato:**

Criptografado com ElGamal e AES (528 bytes no total):

```
+----+----+----+----+----+----+----+----+
| encrypted data (528 bytes)            |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
```
Estrutura criptografada ElGamal (528 bytes):

```
+----+----+----+----+----+----+----+----+
| toPeer (16 bytes)                     |
+----+----+----+----+----+----+----+----+
| ElGamal encrypted data (512 bytes)    |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+

toPeer :: First 16 bytes of SHA-256 hash of peer's RouterIdentity

encrypted_data :: ElGamal-2048 encrypted (bytes 1-256 and 258-513
                  of the 514-byte ElGamal block, with padding bytes
                  at positions 0 and 257 removed)
```
Estrutura de texto em claro (222 bytes antes da criptografia):

```
+----+----+----+----+----+----+----+----+
| receive_tunnel (4) | our_ident (32)   |
+----+----+----+----+                   +
|                                       |
+                   +----+----+----+----+
|                   | next_tunnel (4)   |
+----+----+----+----+----+----+----+----+
| next_ident (32 bytes)                 |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
| layer_key (32 bytes)                  |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
| iv_key (32 bytes)                     |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
| reply_key (32 bytes)                  |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
| reply_iv (16 bytes)                   |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|flag| request_time (4) | send_msg_id  |
+----+----+----+----+----+----+----+----+
     (4)                | padding (29)  |
+----+----+----+----+----+              +
|                                       |
+                             +----+----+
|                             |
+----+----+----+----+----+----+

receive_tunnel :: TunnelId (4 bytes, nonzero)
our_ident :: Hash (32 bytes)
next_tunnel :: TunnelId (4 bytes, nonzero)
next_ident :: Hash (32 bytes)
layer_key :: SessionKey (32 bytes)
iv_key :: SessionKey (32 bytes)
reply_key :: SessionKey (32 bytes)
reply_iv :: 16 bytes
flag :: Integer (1 byte)
request_time :: Integer (4 bytes, hours since epoch = time / 3600)
send_message_id :: Integer (4 bytes)
padding :: 29 bytes random data
```
**Notas:** - A criptografia ElGamal-2048 produz um bloco de 514 bytes, mas os dois bytes de preenchimento (nas posições 0 e 257) são removidos, resultando em 512 bytes - Consulte a [Especificação de Criação de Tunnel](/docs/specs/implementation/) para detalhes dos campos - Código-fonte: `net.i2p.data.i2np.BuildRequestRecord` - Constante: `EncryptedBuildRecord.RECORD_SIZE = 528`

### BuildRequestRecord (ECIES-X25519 Longo)

Para routers ECIES-X25519, introduzidos na versão 0.9.48 da API. Usam 528 bytes para compatibilidade com versões anteriores em tunnels mistos.

**Formato:**

```
+----+----+----+----+----+----+----+----+
| toPeer (16 bytes)                     |
+----+----+----+----+----+----+----+----+
| ephemeral_key (32 bytes)              |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
| ChaCha20 encrypted data (464 bytes)   |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| Poly1305 MAC (16 bytes)               |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+

toPeer :: First 16 bytes of SHA-256 hash of peer's RouterIdentity
ephemeral_key :: X25519 ephemeral public key (32 bytes)
encrypted_data :: ChaCha20 encrypted (464 bytes)
mac :: Poly1305 message authentication code (16 bytes)
```
**Tamanho total:** 528 bytes (igual ao ElGamal para compatibilidade)

Consulte [ECIES Tunnel Creation](/docs/specs/implementation/) para obter detalhes sobre a estrutura do texto em claro e sobre a criptografia.

### BuildRequestRecord (ECIES-X25519 Short)

Somente para routers ECIES-X25519, a partir da versão 0.9.51 da API (lançamento 1.5.0). Este é o formato padrão atual.

**Formato:**

```
+----+----+----+----+----+----+----+----+
| toPeer (16 bytes)                     |
+----+----+----+----+----+----+----+----+
| ephemeral_key (32 bytes)              |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
| ChaCha20 encrypted data (154 bytes)   |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| Poly1305 MAC (16 bytes)               |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+

toPeer :: First 16 bytes of SHA-256 hash of peer's RouterIdentity
ephemeral_key :: X25519 ephemeral public key (32 bytes)
encrypted_data :: ChaCha20 encrypted (154 bytes)
mac :: Poly1305 message authentication code (16 bytes)
```
**Tamanho total:** 218 bytes (redução de 59% em relação a 528 bytes)

**Diferença principal:** Registros curtos derivam TODAS as chaves via HKDF (função de derivação de chaves) em vez de incluí-las explicitamente no registro. Isso inclui: - Chaves de camada (para criptografia do tunnel) - Chaves IV (para criptografia do tunnel) - Chaves de resposta (para build reply (resposta de construção)) - IVs de resposta (para build reply)

Todas as chaves são derivadas usando o mecanismo HKDF do Noise protocol (protocolo Noise), com base no segredo compartilhado proveniente da troca de chaves X25519.

**Benefícios:** - 4 registros curtos cabem em uma mensagem de tunnel (873 bytes) - construções de tunnel em 3 mensagens em vez de mensagens separadas para cada registro - Redução de largura de banda e latência - Mesmas propriedades de segurança que o formato longo

Consulte [Proposta 157](/proposals/157-new-tbm/) para a justificativa e [ECIES Tunnel Creation](/docs/specs/implementation/) para a especificação completa.

**Código-fonte:** - `net.i2p.data.i2np.ShortEncryptedBuildRecord` - Constante: `ShortEncryptedBuildRecord.RECORD_SIZE = 218`

### BuildResponseRecord (registro de resposta de construção) (ElGamal)

**OBSOLETO.** Usado apenas quando o tunnel contém um router ElGamal.

**Finalidade:** Um registro em um conjunto de múltiplos registros com respostas a uma solicitação de construção.

**Formato:**

Criptografado (528 bytes, mesmo tamanho que BuildRequestRecord (registro de requisição de construção)):

```
bytes 0-527 :: AES-encrypted record
```
Estrutura não criptografada:

```
+----+----+----+----+----+----+----+----+
| SHA-256 hash (32 bytes)               |
+                                       +
|        (hash of bytes 32-527)         |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
| random data (495 bytes)               |
~                                       ~
|                                  |ret |
+----+----+----+----+----+----+----+----+

bytes 0-31 :: SHA-256 hash of bytes 32-527
bytes 32-526 :: Random data (could be used for congestion info)
byte 527 :: Reply code (0 = accept, 30 = reject)
```
**Códigos de resposta:** - `0` - Aceito - `30` - Rejeitado (largura de banda excedida)

Consulte [Especificação de Criação do Tunnel](/docs/specs/implementation/) para obter detalhes sobre o campo de resposta.

### BuildResponseRecord (registro de resposta de construção) (ECIES-X25519)

Para routers ECIES-X25519, versão da API 0.9.48+. Tamanho igual ao da solicitação correspondente (528 para o tipo longo, 218 para o tipo curto).

**Formato:**

Formato longo (528 bytes):

```
+----+----+----+----+----+----+----+----+
| ChaCha20 encrypted data (512 bytes)   |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| Poly1305 MAC (16 bytes)               |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
```
Formato curto (218 bytes):

```
+----+----+----+----+----+----+----+----+
| ChaCha20 encrypted data (202 bytes)   |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| Poly1305 MAC (16 bytes)               |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
```
**Estrutura do texto em claro (ambos os formatos):**

Contém uma estrutura de mapeamento (formato de pares chave-valor do I2P) com: - Código de status de resposta (obrigatório) - Parâmetro de largura de banda disponível ("b") (opcional, adicionado na API 0.9.65) - Outros parâmetros opcionais para futuras extensões

**Códigos de Status de Resposta:** - `0` - Sucesso - `30` - Rejeitado: largura de banda excedida

Consulte [Criação do ECIES Tunnel](/docs/specs/implementation/) para a especificação completa.

### GarlicClove (ElGamal/AES) — submensagem usada no esquema garlic encryption

**AVISO:** Este é o formato usado para garlic cloves (submensagens encapsuladas) dentro de garlic messages (mensagens compostas) criptografadas com ElGamal. O formato para garlic messages e garlic cloves ECIES-AEAD-X25519-Ratchet é significativamente diferente. Consulte a [Especificação ECIES](/docs/specs/ecies/) para o formato moderno.

**Obsoleto para routers (API 0.9.58+), ainda suportado para destinos.**

**Formato:**

Não criptografado:

```
+----+----+----+----+----+----+----+----+
| Delivery Instructions (variable)      |
~                                       ~
+----+----+----+----+----+----+----+----+
| I2NP Message (variable)               |
~                                       ~
+----+----+----+----+----+----+----+----+
| Clove ID (4)  | Expiration (8)   |Cert|
+----+----+----+----+----+----+----+----+
                                    (3) |
+----+----+----+----+----+----+----+----+

Delivery Instructions :: Variable length (typically 1, 33, or 37 bytes)
I2NP Message :: Any I2NP message
Clove ID :: 4-byte Integer (random, checked for duplicates)
Expiration :: Date (8 bytes)
Certificate :: Always NULL (3 bytes total, all zeroes)
```
**Notas:** - Cloves (submensagens) nunca são fragmentados - Quando o primeiro bit do byte de flag das Instruções de Entrega é 0, o clove não é criptografado - Quando o primeiro bit é 1, o clove é criptografado (recurso não implementado) - O comprimento máximo é uma função dos comprimentos totais dos cloves e do comprimento máximo de GarlicMessage - O certificado poderia possivelmente ser usado com HashCash para "pagar" pelo roteamento (possibilidade futura) - Mensagens usadas na prática: DataMessage, DeliveryStatusMessage, DatabaseStoreMessage - GarlicMessage pode conter GarlicMessage (garlic aninhado), mas isso não é usado na prática

Veja [Garlic Routing](/docs/overview/garlic-routing/) (roteamento Garlic) para uma visão geral conceitual.

### GarlicClove (ECIES-X25519-AEAD-Ratchet)

Para routers e destinos ECIES-X25519, versão da API 0.9.46+. Este é o formato padrão atual.

**DIFERENÇA CRÍTICA:** ECIES garlic usa uma estrutura totalmente diferente baseada em blocos do Noise protocol (protocolo Noise), em vez de estruturas de clove (submensagens do garlic) explícitas.

**Formato:**

As mensagens garlic ECIES contêm uma série de blocos:

```
Block structure:
+----+----+----+----+----+----+----+----+
|type| length    | data ...
+----+----+----+----+----+-//-

type :: 1 byte block type
length :: 2 bytes block length
data :: variable length data
```
**Tipos de Blocos:** - `0` - Garlic Clove Block (submensagem garlic; contém uma mensagem I2NP) - `1` - Bloco de Data e Hora (carimbo de data/hora) - `2` - Bloco de Opções (opções de entrega) - `3` - Bloco de Preenchimento - `254` - Bloco de Terminação (não implementado)

**Garlic Clove Block (tipo 0 — bloco 'clove' de garlic):**

```
+----+----+----+----+----+----+----+----+
|  0 | length    | Delivery Instructions |
+----+----+----+----+                    +
~                                       ~
+----+----+----+----+----+----+----+----+
| I2NP Message                          |
~                                       ~
+----+----+----+----+----+----+----+----+
| Clove ID (4)  | Expiration (4)        |
+----+----+----+----+----+----+----+----+
```
**Principais diferenças em relação ao formato ElGamal:** - Usa expiração de 4 bytes (segundos desde a época Unix) em vez de data de 8 bytes - Sem campo de certificado - Envolvido em uma estrutura de bloco com tipo e comprimento - Mensagem inteira criptografada com ChaCha20/Poly1305 AEAD - Gerenciamento de sessão via ratcheting (mecanismo de atualização progressiva de chaves)

Consulte a [Especificação do ECIES](/docs/specs/ecies/) para obter detalhes completos sobre o framework do protocolo Noise e as estruturas de bloco.

### Instruções de Entrega do Garlic Clove (submensagem individual em uma mensagem garlic)

Este formato é usado tanto para garlic cloves (submensagens no esquema garlic encryption) de ElGamal quanto de ECIES. Ele especifica como entregar a mensagem contida.

**AVISO CRÍTICO:** Esta especificação é APENAS para instruções de entrega dentro de Garlic Cloves (submensagens encapsuladas no esquema garlic encryption). As "instruções de entrega" também são usadas dentro de Tunnel Messages (mensagens transmitidas via tunnel), onde o formato é significativamente diferente. Consulte a [Tunnel Message Specification](/docs/specs/implementation/) para instruções de entrega de tunnel. NÃO confunda esses dois formatos.

**Formato:**

A chave de sessão e o atraso não são usados e nunca estão presentes, portanto, os três comprimentos possíveis são: - 1 byte (LOCAL) - 33 bytes (ROUTER e DESTINO) - 37 bytes (TUNNEL)

```
+----+----+----+----+----+----+----+----+
|flag|                                  |
+----+                                  +
|       Session Key (optional, 32)     |
+                                       +
|                                       |
+    +----+----+----+----+--------------+
|    |                                  |
+----+                                  +
|       To Hash (optional, 32)         |
+                                       +
|                                       |
+    +----+----+----+----+--------------+
|    | Tunnel ID (4, opt)| Delay (4, opt)|
+----+----+----+----+----+----+----+----+

flag :: 1 byte
        Bit order: 76543210
        bit 7: encrypted? (Unimplemented, always 0)
               If 1, a 32-byte encryption session key follows
        bits 6-5: delivery type
               0x0 = LOCAL (0)
               0x1 = DESTINATION (1)
               0x2 = ROUTER (2)
               0x3 = TUNNEL (3)
        bit 4: delay included? (Not fully implemented, always 0)
               If 1, four delay bytes are included
        bits 3-0: reserved, set to 0 for compatibility

Session Key :: 32 bytes (Optional, unimplemented)
               Present if encrypt flag bit is set

To Hash :: 32 bytes (Optional)
           Present if delivery type is DESTINATION, ROUTER, or TUNNEL
           - DESTINATION: SHA256 hash of the destination
           - ROUTER: SHA256 hash of the router identity
           - TUNNEL: SHA256 hash of the gateway router identity

Tunnel ID :: 4 bytes (Optional)
             Present if delivery type is TUNNEL
             The destination tunnel ID (nonzero)

Delay :: 4 bytes (Optional, unimplemented)
         Present if delay included flag is set
         Specifies delay in seconds
```
**Tamanhos típicos:** - entrega LOCAL: 1 byte (apenas flag) - entrega ROUTER / DESTINO: 33 bytes (flag + hash) - entrega TUNNEL: 37 bytes (flag + hash + ID do tunnel)

**Descrições dos Tipos de Entrega:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Value</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">LOCAL</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Deliver to the local router (this router)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">DESTINATION</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Deliver to a destination (client) identified by hash</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ROUTER</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Deliver to another router identified by hash</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">TUNNEL</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Deliver to a tunnel gateway router</td>
    </tr>
  </tbody>
</table>
**Notas de Implementação:** - A criptografia com chave de sessão não está implementada e o bit de flag é sempre 0 - O atraso não está totalmente implementado e o bit de flag é sempre 0 - Para entrega TUNNEL, o hash identifica o gateway router e o tunnel ID especifica qual tunnel de entrada - Para entrega DESTINATION, o hash é o SHA-256 da chave pública do destino - Para entrega ROUTER, o hash é o SHA-256 da identidade do router

---

## Mensagens do I2NP

Especificações completas de mensagens para todos os tipos de mensagens do I2NP.

### Resumo dos Tipos de Mensagem

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Message</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Since</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Status</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">DatabaseStore</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.6.1.10</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">DatabaseLookup</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.6.1.10</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">DatabaseSearchReply</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.6.1.10</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">DeliveryStatus</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">10</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.6.1.10</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Garlic</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">11</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.6.1.10</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">TunnelData</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">18</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.6.1.10</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">TunnelGateway</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">19</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.6.1.10</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Data</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">20</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.6.1.10</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">TunnelBuild</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">21</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.6.1.10</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">TunnelBuildReply</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">22</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.6.1.10</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">VariableTunnelBuild</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">23</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.7.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">VariableTunnelBuildReply</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">24</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.7.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ShortTunnelBuild</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">25</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.51</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">OutboundTunnelBuildReply</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">26</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.51</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
  </tbody>
</table>
**Reservado:** - Tipo 0: Reservado - Tipos 4-9: Reservado para uso futuro - Tipos 12-17: Reservado para uso futuro - Tipos 224-254: Reservado para mensagens experimentais - Tipo 255: Reservado para expansão futura

---

### DatabaseStore (Tipo 1)

**Finalidade:** Um armazenamento no banco de dados não solicitado, ou a resposta a uma mensagem DatabaseLookup bem-sucedida.

**Conteúdo:** Um LeaseSet, LeaseSet2, MetaLeaseSet ou EncryptedLeaseSet não compactado, ou um RouterInfo compactado.

**Formato com token de resposta:**

```
+----+----+----+----+----+----+----+----+
| SHA256 Hash as key (32 bytes)        |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|type| reply token (4)   | reply_tunnelId
+----+----+----+----+----+----+----+----+
     (4)               | reply gateway  |
+----+----+----+----+----+              +
|       SHA256 hash (32 bytes)          |
+                                       +
|                                       |
+                                  +----+
|                                  |
+----+----+----+----+----+----+----+
| data ...
+----+-//

key :: 32 bytes
       SHA256 hash (the "real" hash, not routing key)

type :: 1 byte
        Type identifier
        bit 0:
            0 = RouterInfo
            1 = LeaseSet or variants
        bits 3-1: (as of 0.9.38)
            0: RouterInfo or LeaseSet (types 0 or 1)
            1: LeaseSet2 (type 3)
            2: EncryptedLeaseSet (type 5)
            3: MetaLeaseSet (type 7)
            4-7: Unsupported, invalid
        bits 7-4:
            Reserved, set to 0

reply token :: 4 bytes
               If greater than zero, a DeliveryStatusMessage is
               requested with the Message ID set to the reply token
               A floodfill router is also expected to flood the data
               to the closest floodfill peers

reply_tunnelId :: 4 bytes (only if reply token > 0)
                  TunnelId of the inbound gateway of the tunnel
                  for the response
                  If 0, reply is sent directly to reply gateway

reply gateway :: 32 bytes (only if reply token > 0)
                 SHA256 hash of the RouterInfo
                 If reply_tunnelId is nonzero: inbound gateway router
                 If reply_tunnelId is zero: router to send reply to

data :: Variable length
        If type == 0: 2-byte Integer length + gzip-compressed RouterInfo
        If type == 1: Uncompressed LeaseSet
        If type == 3: Uncompressed LeaseSet2
        If type == 5: Uncompressed EncryptedLeaseSet
        If type == 7: Uncompressed MetaLeaseSet
```
**Formato com token de resposta == 0:**

```
+----+----+----+----+----+----+----+----+
| SHA256 Hash as key (32 bytes)        |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|type|         0         | data ...
+----+----+----+----+----+-//
```

**Código-fonte:** - `net.i2p.data.i2np.DatabaseStoreMessage` - `net.i2p.data.RouterInfo` (para a estrutura RouterInfo) - `net.i2p.data.LeaseSet` (para a estrutura LeaseSet)

---

### DatabaseLookup (Tipo 2)

**Objetivo:** Uma solicitação para consultar um item no banco de dados da rede. A resposta pode ser um DatabaseStore ou um DatabaseSearchReply.

**Formato:**

```
+----+----+----+----+----+----+----+----+
| SHA256 hash as the key (32 bytes)    |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
| SHA256 hash of the from router (32)  |
+    or reply tunnel gateway            +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|flag| reply_tunnelId (4)| size (2)|   |
+----+----+----+----+----+----+----+    +
| SHA256 of key1 to exclude (32 bytes) |
+                                       +
|                                       |
+                                  +----+
|                                  |    |
+----+----+----+----+----+----+----+    +
| SHA256 of key2 to exclude (32)       |
+                                       +
~                                       ~
|                                       |
+                                  +----+
|                                  |    |
+----+----+----+----+----+----+----+    +
|   Session key if reply encryption     |
+       requested (32 bytes)             +
|                                       |
+                                  +----+
|                                  |tags|
+----+----+----+----+----+----+----+----+
|   Session tags if reply encryption    |
+       requested (variable)             +
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+

key :: 32 bytes
       SHA256 hash of the object to lookup

from :: 32 bytes
        If deliveryFlag == 0: SHA256 hash of RouterInfo (sender)
        If deliveryFlag == 1: SHA256 hash of reply tunnel gateway

flags :: 1 byte
         Bit order: 76543210
         bit 0: deliveryFlag
             0 = send reply directly
             1 = send reply to some tunnel
         bit 1: encryptionFlag
             Through 0.9.5: must be 0
             As of 0.9.6: ignored
             As of 0.9.7:
                 0 = send unencrypted reply
                 1 = send AES encrypted reply using key and tag
         bits 3-2: lookup type flags
             Through 0.9.5: must be 00
             As of 0.9.6: ignored
             As of 0.9.16:
                 00 = ANY (deprecated, use LS or RI as of 0.9.16)
                 01 = LS lookup (LeaseSet or variants)
                 10 = RI lookup (RouterInfo)
                 11 = exploration lookup (RouterInfo, non-floodfill)
         bit 4: ECIESFlag
             Before 0.9.46: ignored
             As of 0.9.46:
                 0 = send unencrypted or ElGamal reply
                 1 = send ChaCha/Poly encrypted reply using key
         bits 7-5:
             Reserved, set to 0

reply_tunnelId :: 4 bytes (only if deliveryFlag == 1)
                  TunnelId of the tunnel to send reply to (nonzero)

size :: 2 bytes
        Integer (valid range: 0-512)
        Number of peers to exclude from DatabaseSearchReply

excludedPeers :: $size SHA256 hashes of 32 bytes each
                 If lookup fails, exclude these peers from the reply
                 If includes a hash of all zeroes, the request is
                 exploratory (return non-floodfill routers only)

reply_key :: 32 bytes (conditional, see encryption modes below)
reply_tags :: 1 byte count + variable length tags (conditional)
```
**Modos de Criptografia de Resposta:**

**NOTA:** Os routers ElGamal estão obsoletos a partir da API 0.9.58. Como a versão mínima recomendada de floodfill para consultar agora é 0.9.58, as implementações não precisam implementar criptografia para routers de floodfill ElGamal. Os destinos ElGamal ainda são suportados.

O bit 4 de flag (ECIESFlag) é usado em combinação com o bit 1 (encryptionFlag) para determinar o modo de criptografia da resposta:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Flag bits 4,1</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">From</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">To Router</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Reply</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">DH?</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0 0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Any</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Any</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">No encryption</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">n/a</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">No encryption</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0 1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ElG</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ElG</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">AES</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">No</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">As of 0.9.7, deprecated 0.9.58</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1 0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ECIES</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ElG</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">AEAD</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">No</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">As of 0.9.46, deprecated 0.9.58</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1 0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ECIES</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ECIES</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">AEAD</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">No</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">As of 0.9.49, current standard</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1 1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ElG</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ECIES</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">AES</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">TBD, future</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1 1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ECIES</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ECIES</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">AEAD</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">TBD, future</td>
    </tr>
  </tbody>
</table>
**Sem criptografia (flags 0,0):**

reply_key, tags e reply_tags não estão presentes.

**ElG para ElG (flags 0,1) - OBSOLETO:**

Suportado a partir da versão 0.9.7, obsoleto a partir da versão 0.9.58.

```
reply_key :: 32 byte SessionKey (big-endian)
             CSRNG(32) random data

tags :: 1 byte Integer (1-32, typically 1)
        Number of reply tags that follow

reply_tags :: One or more 32-byte SessionTags
              Each is CSRNG(32) random data
```
**ECIES para ElG (flags 1,0) - OBSOLETO:**

Suportado a partir da versão 0.9.46, obsoleto a partir da versão 0.9.58.

```
reply_key :: 32 byte ECIES SessionKey (big-endian)
             CSRNG(32) random data

tags :: 1 byte Integer (required value: 1)
        Number of reply tags that follow

reply_tags :: One 8-byte ECIES SessionTag
              CSRNG(8) random data
```
A resposta é uma mensagem ECIES Existing Session (sessão existente), conforme definida em [ECIES Specification](/docs/specs/ecies/):

```
+----+----+----+----+----+----+----+----+
| Session Tag (8 bytes)                 |
+----+----+----+----+----+----+----+----+
| ChaCha20 encrypted payload            |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| Poly1305 MAC (16 bytes)               |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+

tag :: 8 byte reply_tag
k :: 32 byte session key (the reply_key)
n :: 0 (nonce)
ad :: The 8 byte reply_tag
payload :: Plaintext data (DSM or DSRM)
ciphertext = ENCRYPT(k, n, payload, ad)
```
**ECIES para ECIES (flags 1,0) - PADRÃO ATUAL:**

Um destino ECIES (esquema de criptografia integrado por curvas elípticas) ou um router envia uma consulta a um router ECIES. Suportado a partir da versão 0.9.49.

Mesmo formato que "ECIES to ElG" acima. A criptografia da mensagem de consulta é especificada em [ECIES Routers](/docs/specs/ecies/#routers). O solicitante é anônimo.

**ECIES para ECIES com DH (flags 1,1) - FUTURO:**

Ainda não está totalmente definido. Consulte [Proposta 156](/proposals/156-ecies-routers/).

**Notas:** - Antes da 0.9.16, a chave podia ser para um RouterInfo ou um LeaseSet (mesmo espaço de chaves, sem flag para distinguir) - Respostas criptografadas só são úteis quando a resposta é através de um tunnel - O número de tags incluídas pode ser maior que um se forem implementadas estratégias alternativas de busca na DHT (tabela hash distribuída) - A chave de busca e as chaves de exclusão são os hashes "reais", NÃO chaves de roteamento - Tipos 3, 5 e 7 (variantes de LeaseSet2) podem ser retornados a partir da 0.9.38. Consulte [Proposta 123](/proposals/123-new-netdb-entries/) - **Notas sobre consulta exploratória:** Uma consulta exploratória é definida para retornar uma lista de hashes não-floodfill próximos da chave. No entanto, as implantações variam: Java de fato procura a chave de busca para um RI (RouterInfo) e retorna um DatabaseStore se presente; i2pd não. Portanto, não é recomendado usar uma consulta exploratória para hashes recebidos anteriormente

**Código-fonte:** - `net.i2p.data.i2np.DatabaseLookupMessage` - Criptografia: `net.i2p.crypto.SessionKeyManager`

---

### DatabaseSearchReply (Tipo 3)

**Finalidade:** A resposta a uma mensagem DatabaseLookup (consulta ao banco de dados) com falha.

**Conteúdo:** Uma lista de hashes de routers mais próximos da chave solicitada.

**Formato:**

```
+----+----+----+----+----+----+----+----+
| SHA256 hash as query key (32 bytes)  |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
| num| peer_hashes (variable)           |
+----+                                  +
|                                       |
~                                       ~
|                                       |
+    +----+----+----+----+----+----+----+
|    | from (32 bytes)                  |
+----+                                  +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+    +----+----+----+----+----+----+----+
|    |
+----+

key :: 32 bytes
       SHA256 of the object being searched

num :: 1 byte Integer
       Number of peer hashes that follow (0-255)

peer_hashes :: $num SHA256 hashes of 32 bytes each (total $num*32 bytes)
               SHA256 of the RouterIdentity that the sender thinks is
               close to the key

from :: 32 bytes
        SHA256 of the RouterInfo of the router this reply was sent from
```
**Notas:** - O hash 'from' não é autenticado e não pode ser considerado confiável - Os hashes de pares retornados não são necessariamente mais próximos da chave do que o router consultado. Para respostas a consultas normais, isso facilita a descoberta de novos floodfills e a pesquisa "ao contrário" (mais distante da chave) para maior robustez - Para consultas de exploração, a chave geralmente é gerada aleatoriamente. Os peer_hashes não-floodfill da resposta podem ser selecionados usando um algoritmo otimizado (por exemplo, pares próximos, mas não necessariamente os mais próximos) para evitar a ordenação ineficiente de todo o banco de dados local. Estratégias de cache também podem ser usadas. Isso é dependente da implementação - **Número típico de hashes retornados:** 3 - **Número máximo recomendado de hashes a retornar:** 16 - A chave da consulta, os hashes de pares e o hash from são hashes "reais", NÃO chaves de roteamento - Se num for 0, isso indica que não foram encontrados pares mais próximos (beco sem saída)

**Código-fonte:** - `net.i2p.data.i2np.DatabaseSearchReplyMessage`

---

### DeliveryStatus (Tipo 10)

**Finalidade:** Uma confirmação simples de recebimento de mensagem. Geralmente criada pelo remetente da mensagem e encapsulada em uma Garlic Message (mensagem do tipo "garlic" no I2P) junto com a própria mensagem, para ser retornada pelo destino.

**Conteúdo:** O ID da mensagem entregue e o horário de criação ou de chegada.

**Formato:**

```
+----+----+----+----+----+----+----+----+----+----+----+----+
| msg_id (4)            | time_stamp (8)                    |
+----+----+----+----+----+----+----+----+----+----+----+----+

msg_id :: Integer (4 bytes)
          Unique ID of the message we deliver the DeliveryStatus for
          (see I2NP Message Header for details)

time_stamp :: Date (8 bytes)
              Time the message was successfully created or delivered
```
**Notas:** - O carimbo de data/hora é sempre definido pelo criador para o momento atual. No entanto, há vários usos disso no código, e mais podem ser adicionados no futuro - Esta mensagem também é usada como confirmação de sessão estabelecida no SSU. Nesse caso, o ID da mensagem é definido como um número aleatório, e o "arrival time" é definido como o ID atual de toda a rede, que é 2 (isto é, `0x0000000000000002`) - DeliveryStatus geralmente é encapsulado em um GarlicMessage (tipo de mensagem 'garlic' no I2P) e enviado através de um tunnel para fornecer confirmação de recebimento sem revelar o remetente - Usado para testes de tunnel a fim de medir latência e confiabilidade

**Código-fonte:** - `net.i2p.data.i2np.DeliveryStatusMessage` - Usado em: `net.i2p.router.tunnel.InboundEndpointProcessor` para testes de tunnel

---

### GarlicMessage (mensagem de garlic encryption do I2P; Tipo 11)

**AVISO:** Este é o formato usado para garlic messages criptografadas com ElGamal (mensagens "garlic", um formato de encapsulamento em camadas do I2P). O formato das garlic messages do ECIES-AEAD-X25519-Ratchet é significativamente diferente. Consulte [Especificação do ECIES](/docs/specs/ecies/) para o formato moderno.

**Finalidade:** Usado para encapsular várias mensagens I2NP criptografadas.

**Conteúdo:** Quando decifrado, consiste em uma série de Garlic Cloves (submensagens 'clove') e dados adicionais, também conhecidos como um Clove Set (conjunto de 'cloves').

**Formato criptografado:**

```
+----+----+----+----+----+----+----+----+
| length (4)            | data          |
+----+----+----+----+----+              +
|                                       |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+

length :: 4 byte Integer
          Number of bytes that follow (0 to 64 KB)

data :: $length bytes
        ElGamal encrypted data
```
**Dados descriptografados (Clove Set — conjunto de submensagens):**

```
+----+----+----+----+----+----+----+----+
| num| clove 1 (variable)               |
+----+                                  +
|                                       |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| clove 2 (variable)                    |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| Certificate (3) | Message_ID (4)  |
+----+----+----+----+----+----+----+----+
    Expiration (8)                  |
+----+----+----+----+----+----+----+----+

num :: 1 byte Integer
       Number of GarlicCloves to follow

clove :: GarlicClove (see GarlicClove structure above)

Certificate :: Always NULL (3 bytes total, all zeroes)

Message_ID :: 4 byte Integer

Expiration :: Date (8 bytes)
```

**Para o formato ECIES-X25519-AEAD-Ratchet (padrão atual para routers):**

Consulte [Especificação ECIES](/docs/specs/ecies/) e [Proposta 144](/proposals/144-ecies-x25519-aead-ratchet/).

**Código-fonte:** - `net.i2p.data.i2np.GarlicMessage` - Criptografia: `net.i2p.crypto.elgamal.ElGamalAESEngine` (obsoleto) - Criptografia moderna: `net.i2p.crypto.ECIES` pacotes

---

### TunnelData (Tipo 18)

**Finalidade:** Uma mensagem enviada a partir do gateway do tunnel ou de um participante para o próximo participante ou endpoint. Os dados têm comprimento fixo, contendo mensagens I2NP que são fragmentadas, agrupadas em lotes, preenchidas e criptografadas.

**Formato:**

```
+----+----+----+----+----+----+----+----+
| tunnelID (4)          | data (1024)   |
+----+----+----+----+----+              +
|                                       |
~                                       ~
|                                       |
+                   +----+----+----+----+
|                   |
+----+----+----+----+

tunnelId :: 4 bytes
            TunnelId identifying the tunnel this message is directed at
            Nonzero

data :: 1024 bytes
        Payload data, fixed to 1024 bytes
```
**Estrutura da carga útil (1024 bytes):**

```
Bytes 0-15: Initialization Vector (IV) for AES encryption
Bytes 16-1023: Encrypted tunnel message data (1008 bytes)
```
**Notas:** - O ID de mensagem I2NP para TunnelData é definido como um novo número aleatório a cada salto - O formato da mensagem de tunnel (dentro dos dados criptografados) é especificado em [Especificação de Mensagens de Tunnel](/docs/specs/implementation/) - Cada salto descriptografa uma camada usando AES-256 em modo CBC - O IV é atualizado a cada salto usando os dados descriptografados - O tamanho total é exatamente 1,028 bytes (4 tunnelId + 1024 dados) - Esta é a unidade fundamental do tráfego de tunnel - Mensagens TunnelData transportam mensagens I2NP fragmentadas (GarlicMessage, DatabaseStore, etc.)

**Código-fonte:** - `net.i2p.data.i2np.TunnelDataMessage` - Constante: `TunnelDataMessage.DATA_LENGTH = 1024` - Processamento: `net.i2p.router.tunnel.InboundGatewayProcessor`

---

### TunnelGateway (Tipo 19)

**Objetivo:** Encapsula outra mensagem I2NP para ser enviada para dentro de um tunnel no gateway de entrada do tunnel.

**Formato:**

```
+----+----+----+----+----+----+----+-//
| tunnelId (4)          | length (2)| data...
+----+----+----+----+----+----+----+-//

tunnelId :: 4 bytes
            TunnelId identifying the tunnel this message is directed at
            Nonzero

length :: 2 byte Integer
          Length of the payload

data :: $length bytes
        Actual payload of this message
```
**Notas:** - A carga útil é uma mensagem I2NP com um cabeçalho padrão de 16 bytes - Usado para injetar mensagens em tunnels a partir do router local - O gateway (ponto de entrada) fragmenta a mensagem contida, se necessário - Após a fragmentação, os fragmentos são encapsulados em mensagens TunnelData (tipo de mensagem de dados de tunnel) - TunnelGateway (tipo de mensagem do gateway de tunnel) nunca é enviado pela rede; é um tipo de mensagem interno usado antes do processamento do tunnel

**Código-fonte:** - `net.i2p.data.i2np.TunnelGatewayMessage` - Processamento: `net.i2p.router.tunnel.OutboundGatewayProcessor`

---

### DataMessage (Tipo 20)

**Finalidade:** Usado por Garlic Messages (mensagens "garlic", no I2P) e Garlic Cloves (submensagens "cloves") para encapsular dados arbitrários (normalmente dados de aplicação criptografados de ponta a ponta).

**Formato:**

```
+----+----+----+----+----+----+-//-+
| length (4)            | data...    |
+----+----+----+----+----+----+-//-+

length :: 4 bytes
          Length of the payload

data :: $length bytes
        Actual payload of this message
```
**Notas:** - Esta mensagem não contém informações de roteamento e nunca será enviada "sem encapsulamento" - Usada apenas dentro de mensagens Garlic - Normalmente contém dados de aplicação criptografados de ponta a ponta (HTTP, IRC, e-mail, etc.) - Os dados geralmente consistem em uma carga útil criptografada com ElGamal/AES ou ECIES - O comprimento máximo prático é de cerca de 61.2 KB devido aos limites de fragmentação de mensagens de tunnel

**Código-fonte:** - `net.i2p.data.i2np.DataMessage`

---

### TunnelBuild (Tipo 21)

**OBSOLETO.** Use VariableTunnelBuild (tipo 23) ou ShortTunnelBuild (tipo 25).

**Finalidade:** Solicitação de construção de tunnel com comprimento fixo para 8 saltos.

**Formato:**

```
+----+----+----+----+----+----+----+----+
| Record 0 (528 bytes)                  |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| Record 1 (528 bytes)                  |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| Record 7 (528 bytes)                  |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+

Just 8 BuildRequestRecords attached together
Record size: 528 bytes
Total size: 8 × 528 = 4,224 bytes
```
**Notas:** - A partir da versão 0.9.48, pode conter ECIES-X25519 BuildRequestRecords (registros de solicitação de construção). Veja [ECIES Tunnel Creation](/docs/specs/implementation/) - Consulte [Tunnel Creation Specification](/docs/specs/implementation/) para detalhes - O ID de mensagem I2NP para esta mensagem deve ser definido de acordo com a especificação de criação de tunnel - Embora raramente visto na rede atual (substituído por VariableTunnelBuild (construção de tunnel variável)), ainda pode ser usado para tunnels muito longos e não foi formalmente descontinuado - Routers ainda devem implementar isto para compatibilidade - O formato fixo de 8 registros é inflexível e desperdiça largura de banda para tunnels mais curtos

**Código-fonte:** - `net.i2p.data.i2np.TunnelBuildMessage` - Constante: `TunnelBuildMessageBase.MAX_RECORD_COUNT = 8`

---

### TunnelBuildReply (Tipo 22)

**OBSOLETO.** Use VariableTunnelBuildReply (tipo 24) ou OutboundTunnelBuildReply (tipo 26).

**Finalidade:** Resposta de construção de tunnel de comprimento fixo para 8 saltos.

**Formato:**

Mesmo formato que TunnelBuildMessage, com BuildResponseRecords em vez de BuildRequestRecords.

```
Total size: 8 × 528 = 4,224 bytes
```
**Notas:** - A partir da versão 0.9.48, pode conter ECIES-X25519 BuildResponseRecords. Veja [Criação de tunnel ECIES](/docs/specs/implementation/) - Veja [Especificação de Criação de tunnel](/docs/specs/implementation/) para detalhes - O ID de mensagem I2NP para esta mensagem deve ser definido de acordo com a especificação de criação de tunnel - Embora raramente visto na rede atual (substituído por VariableTunnelBuildReply (resposta de construção de tunnel variável)), ainda pode ser usado para tunnels muito longos e não foi formalmente descontinuado - Routers ainda devem implementar isso para compatibilidade

**Código-fonte:** - `net.i2p.data.i2np.TunnelBuildReplyMessage`

---

### VariableTunnelBuild (Tipo 23)

**Objetivo:** Criação de tunnel com comprimento variável de 1 a 8 saltos. Suporta ambos os routers ElGamal e ECIES-X25519.

**Formato:**

```
+----+----+----+----+----+----+----+----+
| num| BuildRequestRecords (variable)   |
+----+----+----+----+----+----+----+----+

num :: 1 byte Integer
       Valid values: 1-8

BuildRequestRecords :: $num records of 528 bytes each

Record size: 528 bytes
Total size: 1 + ($num × 528) bytes
```
**Notas:** - A partir da 0.9.48, pode conter ECIES-X25519 BuildRequestRecords (registros de solicitação de construção). Veja [Criação de tunnel com ECIES (esquema integrado de criptografia de curva elíptica)](/docs/specs/implementation/) - Introduzido na versão 0.7.12 do router (2009) - Pode não ser enviado a participantes do tunnel com versões anteriores à 0.7.12 - Veja [Especificação de Criação de Tunnel](/docs/specs/implementation/) para detalhes - O ID de mensagem I2NP deve ser definido de acordo com a especificação de criação de tunnel - **Número típico de registros:** 4 (para um tunnel de 4 saltos) - **Tamanho total típico:** 1 + (4 × 528) = 2,113 bytes - Esta é a mensagem padrão de construção de tunnel para routers ElGamal (algoritmo de criptografia assimétrica ElGamal) - Routers ECIES geralmente usam ShortTunnelBuild (mensagem de construção de tunnel curta) (type 25) em vez disso

**Código-fonte:** - `net.i2p.data.i2np.VariableTunnelBuildMessage`

---

### VariableTunnelBuildReply (Tipo 24)

**Finalidade:** Resposta de construção de tunnel de comprimento variável para 1-8 saltos. Suporta ambos os routers ElGamal e ECIES-X25519.

**Formato:**

Mesmo formato que VariableTunnelBuildMessage, com BuildResponseRecords em vez de BuildRequestRecords.

```
+----+----+----+----+----+----+----+----+
| num| BuildResponseRecords (variable)  |
+----+----+----+----+----+----+----+----+

num :: 1 byte Integer
       Valid values: 1-8

BuildResponseRecords :: $num records of 528 bytes each

Record size: 528 bytes
Total size: 1 + ($num × 528) bytes
```
**Notas:** - A partir da versão 0.9.48, pode conter ECIES-X25519 BuildResponseRecords (registros de resposta de construção). Consulte [Criação de Tunnel ECIES](/docs/specs/implementation/) - Introduzido na versão 0.7.12 do router (2009) - Não deve ser enviado a participantes do tunnel com versões anteriores à 0.7.12 - Consulte [Especificação de Criação de Tunnel](/docs/specs/implementation/) para detalhes - O ID de mensagem I2NP deve ser definido de acordo com a especificação de criação de tunnel - **Número típico de registros:** 4 - **Tamanho total típico:** 2,113 bytes

**Código-fonte:** - `net.i2p.data.i2np.VariableTunnelBuildReplyMessage`

---

### ShortTunnelBuild (Tipo 25)

**Finalidade:** Mensagens curtas de construção de tunnel apenas para routers ECIES-X25519. Introduzidas na versão 0.9.51 da API (lançamento 1.5.0, agosto de 2021). Este é o padrão atual para construções de tunnel ECIES.

**Formato:**

```
+----+----+----+----+----+----+----+----+
| num| ShortBuildRequestRecords (var)   |
+----+----+----+----+----+----+----+----+

num :: 1 byte Integer
       Valid values: 1-8

ShortBuildRequestRecords :: $num records of 218 bytes each

Record size: 218 bytes
Total size: 1 + ($num × 218) bytes
```
**Notas:** - Introduzido na versão 0.9.51 do router (release 1.5.0, agosto de 2021) - Não deve ser enviado a participantes do tunnel com versão da API anterior à 0.9.51 - Consulte [ECIES Tunnel Creation](/docs/specs/implementation/) para a especificação completa - Consulte [Proposal 157](/proposals/157-new-tbm/) para a justificativa - **Número típico de registros:** 4 - **Tamanho total típico:** 1 + (4 × 218) = 873 bytes - **Economia de largura de banda:** 59% menor que VariableTunnelBuild (873 vs. 2.113 bytes) - **Benefício de desempenho:** 4 registros curtos cabem em uma mensagem de tunnel; VariableTunnelBuild requer 3 mensagens de tunnel - Este é agora o formato padrão de construção de tunnel para tunnels ECIES-X25519 puros - Os registros derivam chaves via HKDF em vez de incluí-las explicitamente

**Código-fonte:** - `net.i2p.data.i2np.ShortTunnelBuildMessage` - Constante: `ShortEncryptedBuildRecord.RECORD_SIZE = 218`

---

### OutboundTunnelBuildReply (resposta de construção de tunnel de saída) (Tipo 26)

**Finalidade:** Enviado da extremidade de saída de um novo tunnel para o originador. Apenas para routers ECIES-X25519. Introduzido na versão da API 0.9.51 (release 1.5.0, agosto de 2021).

**Formato:**

Mesmo formato que ShortTunnelBuildMessage, com ShortBuildResponseRecords em vez de ShortBuildRequestRecords.

```
+----+----+----+----+----+----+----+----+
| num| ShortBuildResponseRecords (var)  |
+----+----+----+----+----+----+----+----+

num :: 1 byte Integer
       Valid values: 1-8

ShortBuildResponseRecords :: $num records of 218 bytes each

Record size: 218 bytes
Total size: 1 + ($num × 218) bytes
```
**Notas:** - Introduzido na versão do router 0.9.51 (release 1.5.0, agosto de 2021) - Consulte [ECIES Tunnel Creation](/docs/specs/implementation/) para a especificação completa - **Número típico de registros:** 4 - **Tamanho total típico:** 873 bytes - Esta resposta é enviada do endpoint de saída (OBEP) de volta ao criador do tunnel através do tunnel de saída recém-criado - Fornece confirmação de que todos os saltos aceitaram a construção do tunnel

**Código-fonte:** - `net.i2p.data.i2np.OutboundTunnelBuildReplyMessage`

---

## Referências

### Especificações Oficiais

- **[Especificação do I2NP](/docs/specs/i2np/)** - Especificação completa do formato de mensagens do I2NP
- **[Estruturas Comuns](/docs/specs/common-structures/)** - Tipos de dados e estruturas utilizados em todo o I2P
- **[Criação de tunnel](/docs/specs/implementation/)** - Criação de tunnel ElGamal (obsoleta)
- **[Criação de tunnel ECIES](/docs/specs/implementation/)** - Criação de tunnel ECIES-X25519 (atual)
- **[Mensagem de tunnel](/docs/specs/implementation/)** - Formato de mensagem de tunnel e instruções de entrega
- **[Especificação do NTCP2](/docs/specs/ntcp2/)** - Protocolo de transporte TCP
- **[Especificação do SSU2](/docs/specs/ssu2/)** - Protocolo de transporte UDP
- **[Especificação do ECIES](/docs/specs/ecies/)** - Criptografia ECIES-X25519-AEAD-Ratchet
- **[Especificação de Criptografia](/docs/specs/cryptography/)** - Primitivas criptográficas de baixo nível
- **[Especificação do I2CP](/docs/specs/i2cp/)** - Especificação do protocolo do cliente
- **[Especificação de Datagramas](/docs/api/datagrams/)** - Formatos Datagram2 e Datagram3

### Propostas

- **[Proposal 123](/proposals/123-new-netdb-entries/)** - Novas entradas no netDB (LeaseSet2, EncryptedLeaseSet, MetaLeaseSet)
- **[Proposal 144](/proposals/144-ecies-x25519-aead-ratchet/)** - Criptografia ECIES-X25519-AEAD-Ratchet
- **[Proposal 154](/proposals/154-ecies-lookups/)** - Consulta criptografada ao banco de dados
- **[Proposal 156](/proposals/156-ecies-routers/)** - ECIES routers
- **[Proposal 157](/proposals/157-new-tbm/)** - Mensagens de criação de tunnel (formato curto)
- **[Proposal 159](/proposals/159-ssu2/)** - Transporte SSU2
- **[Proposal 161](/pt/proposals/161-ri-dest-padding/)** - Preenchimento compressível
- **[Proposal 163](/proposals/163-datagram2/)** - Datagram2 e Datagram3
- **[Proposal 167](/proposals/167-service-records/)** - Parâmetros do registro de serviço do LeaseSet
- **[Proposal 168](/proposals/168-tunnel-bandwidth/)** - Parâmetros de largura de banda para a criação de tunnel
- **[Proposal 169](/proposals/169-pq-crypto/)** - Criptografia híbrida pós-quântica

### Documentação

- **[Garlic Routing](/docs/overview/garlic-routing/)** (roteamento garlic) - Agrupamento de mensagens em camadas
- **[ElGamal/AES](/docs/legacy/elgamal-aes/)** - Esquema de criptografia obsoleto
- **[Implementação de Tunnel](/docs/specs/implementation/)** - Fragmentação e processamento
- **[Banco de dados da rede](/docs/specs/common-structures/)** - Tabela hash distribuída
- **[Transporte NTCP2](/docs/specs/ntcp2/)** - Especificação de transporte TCP
- **[Transporte SSU2](/docs/specs/ssu2/)** - Especificação de transporte UDP
- **[Introdução técnica](/docs/overview/tech-intro/)** - Visão geral da arquitetura do I2P

### Código-fonte

- **[Java I2P Repository](https://i2pgit.org/I2P_Developers/i2p.i2p)** - Implementação oficial em Java
- **[GitHub Mirror](https://github.com/i2p/i2p.i2p)** - Espelho no GitHub do Java I2P
- **[i2pd Repository](https://github.com/PurpleI2P/i2pd)** - Implementação em C++

### Principais locais do código-fonte

**Java I2P (i2pgit.org/I2P_Developers/i2p.i2p):** - `core/java/src/net/i2p/data/i2np/` - Implementações de mensagens I2NP (protocolo de rede da I2P) - `core/java/src/net/i2p/crypto/` - Implementações criptográficas - `router/java/src/net/i2p/router/tunnel/` - Processamento de tunnel (túnel da I2P) - `router/java/src/net/i2p/router/transport/` - Implementações de transporte

**Constantes e valores:** - `I2NPMessage.MAX_SIZE = 65536` - Tamanho máximo da mensagem I2NP - `I2NPMessageImpl.HEADER_LENGTH = 16` - Tamanho padrão do cabeçalho - `TunnelDataMessage.DATA_LENGTH = 1024` - Carga útil da mensagem de tunnel - `EncryptedBuildRecord.RECORD_SIZE = 528` - Build record (registro de construção) longo - `ShortEncryptedBuildRecord.RECORD_SIZE = 218` - Build record curto - `TunnelBuildMessageBase.MAX_RECORD_COUNT = 8` - Máximo de registros por build

---

## Apêndice A: Estatísticas da Rede e Estado Atual

### Composição da Rede (em outubro de 2025)

- **Total de routers:** Aproximadamente 60.000-70.000 (varia)
- **Floodfill routers:** Aproximadamente 500-700 ativos
- **Tipos de criptografia:**
  - ECIES-X25519: >95% dos routers
  - ElGamal: <5% dos routers (obsoleto, apenas legado)
- **Adoção de transportes:**
  - SSU2: >60% como transporte principal
  - NTCP2: ~40% como transporte principal
  - Transportes legados (SSU1, NTCP): 0% (removidos)
- **Tipos de assinatura:**
  - EdDSA (Ed25519): Imensa maioria
  - ECDSA: Pequena porcentagem
  - RSA: Não permitido (removido)

### Requisitos mínimos do Router

- **Versão da API:** 0.9.16+ (para compatibilidade do EdDSA com a rede)
- **Mínimo recomendado:** API 0.9.51+ (compilações ECIES para short tunnel)
- **Mínimo atual para floodfills:** API 0.9.58+ (obsolescência do router ElGamal)
- **Requisito futuro:** Java 17+ (a partir da versão 2.11.0, dezembro de 2025)

### Requisitos de Largura de Banda

- **Mínimo:** 128 KBytes/sec (flag N ou superior) para floodfill
- **Recomendado:** 256 KBytes/sec (flag O) ou superior
- **Requisitos de floodfill:**
  - Largura de banda mínima de 128 KB/sec
  - Tempo de atividade estável (>95% recomendado)
  - Baixa latência (<500ms para os pares)
  - Aprovar nos testes de integridade (tempo de fila, atraso de tarefas)

### Estatísticas de Tunnel

- **Comprimento típico do tunnel:** 3-4 saltos
- **Comprimento máximo do tunnel:** 8 saltos (teórico, raramente utilizado)
- **Tempo de vida típico do tunnel:** 10 minutos
- **Taxa de sucesso de construção de tunnel:** >85% para routers bem conectados
- **Formato da mensagem de construção de tunnel:**
  - routers ECIES: ShortTunnelBuild (registros de 218 bytes)
  - tunnels mistos: VariableTunnelBuild (registros de 528 bytes)

### Métricas de Desempenho

- **Tempo de construção do Tunnel:** 1-3 segundos (típico)
- **Latência fim a fim:** 0.5-2 segundos (típica, 6-8 saltos no total)
- **Taxa de transferência:** Limitada pela largura de banda do tunnel (tipicamente 10-50 KB/sec por tunnel)
- **Tamanho máximo do datagrama:** 10 KB recomendado (61.2 KB de máximo teórico)

---

## Apêndice B: Funcionalidades Obsoletas e Removidas

### Completamente removido (não é mais suportado)

- **Transporte NTCP** - Removido na versão 0.9.50 (maio de 2021)
- **Transporte SSU v1** - Removido do Java I2P na versão 2.4.0 (dezembro de 2023)
- **Transporte SSU v1** - Removido do i2pd na versão 2.44.0 (novembro de 2022)
- **Tipos de assinatura RSA** - Não permitidos a partir da API 0.9.28

### Obsoleto (Suportado mas Não Recomendado)

- **ElGamal routers** - Obsoletos desde a API 0.9.58 (março de 2023)
  - Destinos ElGamal ainda suportados para compatibilidade com versões anteriores
  - Novos routers devem usar ECIES-X25519 exclusivamente
- **TunnelBuild (tipo 21)** - Obsoleto em favor de VariableTunnelBuild e ShortTunnelBuild
  - Ainda implementado para tunnels muito longos (>8 saltos)
- **TunnelBuildReply (tipo 22)** - Obsoleto em favor de VariableTunnelBuildReply e OutboundTunnelBuildReply
- **Criptografia ElGamal/AES** - Obsoleta em favor de ECIES-X25519-AEAD-Ratchet
  - Ainda usada para destinos legados
- **ECIES BuildRequestRecords (registros de solicitação de construção) longos (528 bytes)** - Obsoletos em favor do formato curto (218 bytes)
  - Ainda usados para tunnels mistos com saltos ElGamal

### Cronograma de suporte legado

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Feature</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Introduced</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Deprecated</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Removed</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">NTCP</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2003</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2018 (0.9.36)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2021 (0.9.50)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Replaced by NTCP2</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">SSU v1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2004</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2022 (0.9.54)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2023 (Java) / 2022 (i2pd)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Replaced by SSU2</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ElGamal routers</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2003</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2023 (0.9.58)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">TBD</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Destinations still supported</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">RSA signatures</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2015</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2017</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2017 (0.9.28)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Never widely used</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">TunnelBuild</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2004</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2009 (0.7.12)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Not removed</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Still supported for long tunnels</td>
    </tr>
  </tbody>
</table>
---

## Apêndice C: Desenvolvimentos futuros

### Criptografia pós-quântica

**Status:** Beta desde a versão 2.10.0 (setembro de 2025), passará a ser o padrão na 2.11.0 (dezembro de 2025)

**Implementação:** - Abordagem híbrida que combina X25519 clássico e MLKEM pós-quântico (ML-KEM-768) - Retrocompatível com a infraestrutura ECIES-X25519 existente - Usa o Signal Double Ratchet (algoritmo Double Ratchet do Signal) com material de chave tanto clássico quanto pós-quântico - Veja [Proposta 169](/proposals/169-pq-crypto/) para detalhes

**Caminho de migração:** 1. Versão 2.10.0 (setembro de 2025): Disponível como opção beta 2. Versão 2.11.0 (dezembro de 2025): Habilitado por padrão 3. Versões futuras: Passará a ser obrigatório

### Funcionalidades planejadas

- **Melhorias no IPv6** - Melhor suporte a IPv6 e mecanismos de transição
- **Limitação de taxa por tunnel** - Controle granular de largura de banda por tunnel
- **Métricas aprimoradas** - Melhor monitoramento de desempenho e diagnóstico
- **Otimizações de protocolo** - Menor sobrecarga e eficiência aprimorada
- **Seleção de floodfill aprimorada** - Melhor distribuição do banco de dados da rede

### Áreas de Pesquisa

- **Otimização do comprimento do tunnel** - Comprimento de tunnel dinâmico baseado no modelo de ameaça
- **Preenchimento avançado** - Melhorias na resistência à análise de tráfego
- **Novos esquemas de criptografia** - Preparação para ameaças da computação quântica
- **Controle de congestionamento** - Melhor gerenciamento da carga de rede
- **Suporte móvel** - Otimizações para dispositivos e redes móveis

---

## Apêndice D: Diretrizes de Implementação

### Para novas implementações

**Requisitos mínimos:** 1. Suporte aos recursos da API versão 0.9.51+ 2. Implementar criptografia ECIES-X25519-AEAD-Ratchet (ratchet: mecanismo de avanço progressivo do estado criptográfico) 3. Suporte aos transportes NTCP2 e SSU2 4. Implementar mensagens ShortTunnelBuild (construção abreviada de tunnel) (registros de 218 bytes) 5. Suporte às variantes LeaseSet2 (tipos 3, 5, 7) 6. Usar assinaturas EdDSA (Ed25519)

**Recomendado:** 1. Suportar criptografia híbrida pós-quântica (a partir da versão 2.11.0) 2. Implementar parâmetros de largura de banda por tunnel 3. Suportar os formatos Datagram2 e Datagram3 4. Implementar opções de registro de serviço em LeaseSets 5. Seguir as especificações oficiais em /docs/specs/

**Não obrigatório:** 1. Suporte ao router ElGamal (obsoleto) 2. Suporte a transportes legados (SSU1, NTCP) 3. BuildRequestRecords ECIES longos (registros de solicitação de construção) (528 bytes para tunnels ECIES puros) 4. Mensagens TunnelBuild/TunnelBuildReply (use as variantes Variable ou Short)

### Testes e Validação

**Conformidade com o Protocolo:** 1. Testar interoperabilidade com o router I2P oficial em Java 2. Testar interoperabilidade com o router i2pd em C++ 3. Validar os formatos de mensagem conforme as especificações 4. Testar ciclos de construção/desmontagem de tunnel 5. Verificar criptografia/descriptografia com vetores de teste

**Testes de Desempenho:** 1. Medir as taxas de sucesso da construção de tunnel (devem ser >85%) 2. Testar com vários comprimentos de tunnel (2-8 saltos) 3. Validar fragmentação e remontagem 4. Testar sob carga (múltiplos tunnels simultâneos) 5. Medir a latência de ponta a ponta

**Testes de segurança:** 1. Verifique a implementação da criptografia (use vetores de teste) 2. Teste a prevenção de ataques de repetição 3. Valide o tratamento da expiração de mensagens 4. Teste contra mensagens malformadas 5. Verifique a geração adequada de números aleatórios

### Armadilhas comuns na implementação

1. **Formatos de instruções de entrega confusos** - garlic clove (submensagem encapsulada) vs mensagem de tunnel
2. **Derivação de chave incorreta** - Uso de HKDF para registros de construção curtos
3. **Tratamento do ID da mensagem** - Não definido corretamente para construções de tunnel
4. **Problemas de fragmentação** - Não respeitar o limite prático de 61,2 KB
5. **Erros de endianness (ordem dos bytes)** - Java usa big-endian para todos os inteiros
6. **Tratamento de expiração** - O formato curto transborda em 7 de fevereiro de 2106
7. **Geração de checksum** - Ainda é obrigatória mesmo que não seja verificada
