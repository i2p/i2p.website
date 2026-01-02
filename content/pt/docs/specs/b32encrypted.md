---
title: "B32 para Leasesets criptografados"
description: "Formato de endereço Base 32 para leasesets LS2 criptografados (LeaseSet versão 2 no I2P)"
slug: "b32-for-encrypted-leasesets"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
status: "Implementado"
---

## Visão geral

Endereços Base 32 padrão ("b32") contêm o hash do destino. Isso não funciona para LS2 (LeaseSet 2, 'leaseSet' de segunda geração) criptografado (Proposta 123).

Não podemos usar um endereço base 32 tradicional para um LS2 criptografado (proposta 123), pois ele contém apenas o hash do destino. Ele não fornece a chave pública não cegada. Os clientes devem conhecer a chave pública do destino, o tipo de assinatura, o tipo de assinatura cegada e uma chave secreta ou privada opcional para obter e decifrar o leaseset. Portanto, um endereço base 32 por si só é insuficiente. O cliente precisa do destino completo (que contém a chave pública) ou da própria chave pública. Se o cliente tiver o destino completo em um livro de endereços e o livro de endereços suportar busca reversa por hash, então a chave pública poderá ser recuperada.

Este formato coloca a chave pública, em vez do hash, em um endereço base32. Este formato também deve conter o tipo de assinatura da chave pública e o tipo de assinatura do esquema de cegamento.

Este documento especifica um formato b32 para esses endereços. Embora tenhamos nos referido a esse novo formato durante as discussões como um endereço "b33", o novo formato de fato mantém o sufixo habitual ".b32.i2p".

## Status da Implementação

A Proposta 123 (Novas entradas do netDB) foi totalmente implementada na versão 0.9.43 (outubro de 2019). O conjunto de recursos do LS2 (leaseSet de segunda geração) criptografado manteve-se estável até a versão 2.10.0 (setembro de 2025), sem alterações incompatíveis no formato de endereçamento ou nas especificações criptográficas.

Principais marcos de implementação: - 0.9.38: Suporte a Floodfill para LS2 (LeaseSet versão 2) padrão com chaves offline - 0.9.39: Tipo de assinatura RedDSA 11 e criptografia/descriptografia básicas - 0.9.40: Suporte completo a endereçamento B32 (Proposta 149) - 0.9.41: Autenticação por cliente baseada em X25519 - 0.9.42: Todos os recursos de blinding (cegamento) operacionais - 0.9.43: Implementação completa declarada (outubro de 2019)

## Concepção

- O novo formato contém a chave pública não cega, o tipo de assinatura não cego e o tipo de assinatura cego.
- Opcionalmente indica requisitos de segredo e/ou de chave privada para links privados.
- Usa o sufixo existente ".b32.i2p", mas com um comprimento maior.
- Inclui um checksum para detecção de erros.
- Os endereços para leasesets criptografados são identificados por 56 ou mais caracteres codificados (35 ou mais bytes decodificados), em comparação com 52 caracteres (32 bytes) para endereços tradicionais base 32.

## Especificação

### Criação e Codificação

Construa um nome de host de {56+ caracteres}.b32.i2p (35+ caracteres em binário) da seguinte forma:

```
flag (1 byte)
  bit 0: 0 for one-byte sigtypes, 1 for two-byte sigtypes
  bit 1: 0 for no secret, 1 if secret is required
  bit 2: 0 for no per-client auth,
         1 if client private key is required
  bits 7-3: Unused, set to 0

public key sigtype (1 or 2 bytes as indicated in flags)
  If 1 byte, the upper byte is assumed zero

blinded key sigtype (1 or 2 bytes as indicated in flags)
  If 1 byte, the upper byte is assumed zero

public key
  Number of bytes as implied by sigtype
```
Pós-processamento e soma de verificação:

```
Construct the binary data as above.
Treat checksum as little-endian.
Calculate checksum = CRC-32(data[3:end])
data[0] ^= (byte) checksum
data[1] ^= (byte) (checksum >> 8)
data[2] ^= (byte) (checksum >> 16)

hostname = Base32.encode(data) || ".b32.i2p"
```
Quaisquer bits não utilizados no final do b32 (endereço base32) devem ser 0. Não há bits não utilizados para um endereço padrão de 56 caracteres (35 bytes).

### Decodificação e Verificação

```
strip the ".b32.i2p" from the hostname
data = Base32.decode(hostname)
Calculate checksum = CRC-32(data[3:end])
Treat checksum as little-endian.
flags = data[0] ^ (byte) checksum
if 1 byte sigtypes:
  pubkey sigtype = data[1] ^ (byte) (checksum >> 8)
  blinded sigtype = data[2] ^ (byte) (checksum >> 16)
else (2 byte sigtypes):
  pubkey sigtype = data[1] ^ ((byte) (checksum >> 8)) || data[2] ^ ((byte) (checksum >> 16))
  blinded sigtype = data[3] || data[4]
parse the remainder based on the flags to get the public key
```
### Bits de Chaves Secretas e Privadas

Os bits de chave secreta e de chave privada são usados para indicar a clientes, proxies ou a outro código do lado do cliente que a chave secreta e/ou a chave privada serão necessárias para descriptografar o leaseset. Implementações específicas podem solicitar ao usuário que forneça os dados necessários ou rejeitar tentativas de conexão se os dados necessários estiverem ausentes.

Esses bits servem apenas como indicadores. A chave secreta ou privada nunca deve ser incluída no próprio endereço B32, pois isso comprometeria a segurança.

## Detalhes Criptográficos

### Esquema de Cegamento

O esquema de cegamento usa RedDSA (um esquema de assinatura digital) baseado em Ed25519 e no design do ZCash, produzindo assinaturas Red25519 na curva Ed25519 usando SHA-512. Essa abordagem garante que as chaves públicas cegadas permaneçam no subgrupo de ordem prima, evitando as preocupações de segurança presentes em alguns projetos alternativos.

Blinded keys (chaves cegadas) são rotacionadas diariamente com base na data UTC usando a fórmula:

```
blinded_key = BLIND(unblinded_key, date, optional_secret)
```
O local de armazenamento na DHT (tabela hash distribuída) é calculado como:

```
SHA256(type_byte || blinded_public_key)
```
### Criptografia

O leaseset criptografado utiliza a cifra de fluxo ChaCha20 para a criptografia, escolhida por oferecer desempenho superior em dispositivos sem aceleração de hardware para AES. A especificação emprega HKDF para derivação de chaves e X25519 para operações de Diffie-Hellman.

Os leasesets (conjuntos de lease) criptografados têm uma estrutura de três camadas: - Camada externa: metadados em texto simples - Camada intermediária: autenticação do cliente (métodos DH ou PSK) - Camada interna: dados LS2 propriamente ditos com informações de lease

### Métodos de Autenticação

A autenticação por cliente suporta dois métodos:

**Autenticação DH**: Utiliza o acordo de chaves X25519. Cada cliente autorizado fornece sua chave pública ao servidor, e o servidor criptografa a camada intermediária usando um segredo compartilhado derivado de ECDH.

**Autenticação PSK**: Usa chaves pré-compartilhadas diretamente para criptografia.

O bit 2 da flag (indicador) no endereço B32 indica se a autenticação por cliente é necessária.

## Cache

Embora esteja fora do escopo desta especificação, routers e clientes devem lembrar e armazenar em cache (recomenda-se que seja persistente) o mapeamento de chave pública para destino, e vice-versa.

O serviço de nomenclatura em blockfile, o sistema de livro de endereços padrão do I2P desde a versão 0.9.8, mantém vários livros de endereços com um mapa dedicado de busca reversa que fornece consultas rápidas por hash. Essa funcionalidade é crítica para a resolução de leaseset (metadados de roteamento de um destino no I2P) criptografado quando apenas um hash é conhecido inicialmente.

## Tipos de Assinatura

A partir da versão 2.10.0 do I2P, estão definidos os tipos de assinatura de 0 a 11. A codificação de um byte continua sendo o padrão, com a codificação de dois bytes disponível, mas não utilizada na prática.

**Tipos Comumente Usados:** - Tipo 0 (DSA_SHA1): Obsoleto para routers, suportado para destinos - Tipo 7 (EdDSA_SHA512_Ed25519): Padrão atual para identidades de router e destinos - Tipo 11 (RedDSA_SHA512_Ed25519): Exclusivamente para leaseSets LS2 criptografados com suporte a blinding (cegamento criptográfico)

**Nota importante**: Apenas Ed25519 (tipo 7) e Red25519 (tipo 11) suportam o blinding (cegamento) necessário para leasesets criptografados. Outros tipos de assinatura não podem ser usados com este recurso.

Tipos 9-10 (algoritmos GOST) permanecem reservados, mas não implementados. Os tipos 4-6 e 8 estão marcados como "apenas offline" para chaves de assinatura offline.

## Notas

- Distinga as variações antigas das novas pelo comprimento. Endereços b32 antigos são sempre {52 chars}.b32.i2p. Os novos são {56+ chars}.b32.i2p
- A codificação base32 segue os padrões da RFC 4648, com decodificação sem distinção entre maiúsculas e minúsculas e preferência por saída em minúsculas
- Os endereços podem exceder 200 caracteres ao usar tipos de assinatura com chaves públicas maiores (por exemplo, ECDSA P521 com chaves de 132 bytes)
- O novo formato pode ser usado em jump links (links de salto) e servido por jump servers (servidores de jump), se desejado, assim como o b32 padrão
- Chaves cegadas rotacionam diariamente com base na data UTC para aumentar a privacidade
- Este formato diverge da abordagem do Tor no rend-spec-v3.txt, apêndice A.2, a qual tem potenciais implicações de segurança com chaves públicas cegadas fora da curva

## Compatibilidade de Versões

Esta especificação é precisa para a versão do I2P 0.9.47 (agosto de 2020) até a versão 2.10.0 (setembro de 2025). Não ocorreram alterações incompatíveis ao formato de endereçamento B32 (endereços base32 do I2P), à estrutura LS2 criptografada (LS2: leaseSet versão 2) ou às implementações criptográficas durante esse período. Todos os endereços criados com a 0.9.47 permanecem totalmente compatíveis com as versões atuais.

## Referências

**CRC-32** - [CRC-32 (Wikipédia)](https://en.wikipedia.org/wiki/CRC-32) - [RFC 3309: Checksum do Stream Control Transmission Protocol](https://tools.ietf.org/html/rfc3309)

**Especificações do I2P** - [Especificação de LeaseSet criptografado](/docs/specs/encryptedleaseset/) - [Proposta 123: Novas entradas de netDB](/proposals/123-new-netdb-entries/) - [Proposta 149: B32 para LS2 criptografado (LS2 é o formato v2 de LeaseSet)](/proposals/149-b32-encrypted-ls2/) - [Especificação de Estruturas Comuns](/docs/specs/common-structures/) - [Nomenclatura e Livro de Endereços](/docs/overview/naming/)

**Comparação com o Tor** - [Tópico de discussão do Tor (contexto de projeto)](https://lists.torproject.org/pipermail/tor-dev/2017-January/011816.html)

**Recursos adicionais** - [Projeto I2P](/) - [Fórum I2P](https://i2pforum.net) - [Documentação da API Java](http://docs.i2p-projekt.de/javadoc/)
