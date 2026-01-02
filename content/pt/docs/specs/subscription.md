---
title: "Comandos do Feed de Assinatura de Endereços"
description: "Extensão para feeds de assinatura de endereços, permitindo que os titulares de nomes de host atualizem e gerenciem suas entradas"
slug: "subscription"
lastUpdated: "2025-10"
accurateFor: "I2P 2.10.0"
---

## Visão geral

Esta especificação estende o feed de assinatura de endereços com comandos, permitindo que servidores de nomes difundam atualizações de entradas provenientes dos detentores de nomes de host. Proposta originalmente na [Proposta 112](/proposals/112-addressbook-subscription-feed-commands/) (setembro de 2014), implementada na versão 0.9.26 (junho de 2016) e implantada em toda a rede com status ENCERRADO.

O sistema permaneceu estável e inalterado desde a sua implementação inicial, continuando a operar de forma idêntica no I2P 2.10.0 (Router API 0.9.65, setembro de 2025).

## Motivação

Anteriormente, os servidores de assinatura de hosts.txt enviavam dados apenas em um formato hosts.txt simples:

```
example.i2p=b64destination
```
Este formato básico criou vários problemas:

- Os detentores de nomes de host não podem atualizar o Destino associado aos seus nomes de host (por exemplo, para atualizar a chave de assinatura para um tipo criptográfico mais forte).
- Os detentores de nomes de host não podem renunciar aos seus nomes de host arbitrariamente. Devem entregar as chaves privadas do Destino correspondentes diretamente ao novo titular.
- Não há como autenticar que um subdomínio é controlado pelo nome de host base correspondente. Isso atualmente é imposto apenas individualmente por alguns servidores de nomes.

## Projeto

Esta especificação adiciona comandos ao formato do hosts.txt. Com esses comandos, os servidores de nomes podem ampliar seus serviços para oferecer recursos adicionais. Clientes que implementarem esta especificação podem receber esses recursos por meio do processo de assinatura normal.

Todas as linhas de comando devem ser assinadas pela Destination correspondente (destino no I2P). Isso garante que as alterações sejam feitas apenas a pedido do titular do nome de host.

## Implicações de segurança

Esta especificação não afeta o anonimato.

Há um aumento do risco associado à perda do controle de uma Destination key (chave privada da Destination), pois quem a obtiver pode usar esses comandos para fazer alterações em quaisquer nomes de host associados. No entanto, isso não é mais problemático do que o status quo, em que alguém que obtenha uma Destination (identificador público no I2P) pode se passar por um nome de host e assumir (parcialmente) o controle do tráfego desse nome de host. O risco adicional é compensado ao conceder aos titulares de nomes de host a capacidade de alterar a Destination associada a um nome de host caso acreditem que a Destination foi comprometida. Isso é impossível no sistema atual.

## Especificação

### Novos Tipos de Linha

Há dois novos tipos de linhas:

1. **Comandos Add e Change:**

```
example.i2p=b64destination#!key1=val1#key2=val2...
```
2. **Remover comandos:**

```
#!key1=val1#key2=val2...
```
#### Ordenação

Um feed não é necessariamente ordenado nem completo. Por exemplo, um change command pode aparecer em uma linha antes de um add command, ou sem um add command.

As chaves podem estar em qualquer ordem. Chaves duplicadas não são permitidas. Todas as chaves e valores são sensíveis a maiúsculas/minúsculas.

### Chaves Comuns

**Obrigatório em todos os comandos:**

**sig** : Assinatura Base64, usando a chave de assinatura do destino

**Referências a um segundo nome de host e/ou destino:**

**oldname** : Um segundo nome de host (novo ou alterado)

**olddest** : Um segundo destino Base64 (novo ou alterado)

**oldsig** : Uma segunda assinatura Base64, usando a chave de assinatura de olddest

**Outras chaves comuns:**

**action** : Um comando

**name** : O nome do host, presente apenas se não for precedido por `example.i2p=b64dest`

**dest** : O destino em Base64, presente apenas se não for precedido por `example.i2p=b64dest`

**date** : Em segundos desde a época Unix

**expires** : Em segundos desde a época Unix

### Comandos

Todos os comandos, exceto o comando "Add", devem conter o par chave/valor `action=command`.

Para compatibilidade com clientes mais antigos, a maioria dos comandos é precedida por `example.i2p=b64dest`, conforme indicado abaixo. Em caso de alterações, os valores apresentados são sempre os novos. Quaisquer valores antigos são incluídos na seção de chave/valor.

As chaves listadas são obrigatórias. Todos os comandos podem conter itens chave/valor adicionais não definidos aqui.

#### Adicionar nome de host

**Precedido por example.i2p=b64dest** : SIM, este é o novo nome de host e destino.

**ação** : NÃO incluída, está implícita.

**sig** : assinatura

Exemplo:

```
example.i2p=b64dest#!sig=b64sig
```
#### Alterar nome do host

**Precedido por example.i2p=b64dest** : SIM, este é o novo nome de host e o destino antigo.

**ação** : changename

**oldname** : o nome de host antigo, a ser substituído

**sig** : assinatura

Exemplo:

```
example.i2p=b64dest#!action=changename#oldname=oldhostname#sig=b64sig
```
#### Alterar Destino

**Precedido por example.i2p=b64dest** : SIM, este é o antigo nome de host e o novo destino.

**ação** : changedest

**olddest** : o destino antigo, a ser substituído

**oldsig** : assinatura utilizando o olddest

**sig** : assinatura

Exemplo:

```
example.i2p=b64dest#!action=changedest#olddest=oldb64dest#oldsig=b64sig#sig=b64sig
```
#### Adicionar apelido de nome do host

**Precedido por example.i2p=b64dest** : SIM, este é o novo nome de host (apelido) e o destino antigo.

**ação** : addname

**oldname** : o nome de host antigo

**sig** : assinatura

Exemplo:

```
example.i2p=b64dest#!action=addname#oldname=oldhostname#sig=b64sig
```
#### Adicionar apelido de destino

(Usado para atualização de criptografia)

**Precedido por example.i2p=b64dest** : SIM, isto é o antigo nome de host e o novo destino (alternativo).

**ação** : adddest

**olddest** : o destino antigo

**oldsig** : assinatura usando olddest

**sig** : assinatura usando dest

Exemplo:

```
example.i2p=b64dest#!action=adddest#olddest=oldb64dest#oldsig=b64sig#sig=b64sig
```
#### Adicionar subdomínio

**Precedido por subdomain.example.i2p=b64dest** : SIM, este é o novo nome de subdomínio e o destino.

**action** : addsubdomain

**oldname** : o nome de host de nível superior (example.i2p)

**olddest** : o destino de nível superior (por exemplo, example.i2p)

**oldsig** : assinatura usando olddest

**sig** : assinatura usando dest

Exemplo:

```
subdomain.example.i2p=b64dest#!action=addsubdomain#oldname=example.i2p#olddest=oldb64dest#oldsig=b64sig#sig=b64sig
```
#### Atualizar Metadados

**Precedido por example.i2p=b64dest** : SIM, isto é o antigo nome de host e destino.

**ação** : atualizar

**sig** : assinatura

(adicione quaisquer chaves atualizadas aqui)

Exemplo:

```
example.i2p=b64dest#!action=update#k1=v1#k2=v2#sig=b64sig
```
#### Remover nome de host

**Precedido por example.i2p=b64dest** : NÃO, estes são especificados nas opções

**ação** : remover

**name** : o nome do host

**dest** : o destino

**sig** : assinatura

Exemplo:

```
#!action=remove#name=example.i2p#dest=b64dest#sig=b64sig
```
#### Remover todos com este destino

**Precedidos por example.i2p=b64dest** : NÃO, são especificados nas opções

**ação** : removeall

**dest** : o destino

**sig** : assinatura

Exemplo:

```
#!action=removeall#dest=b64dest#sig=b64sig
```
### Assinaturas

Todos os comandos devem ser assinados pela Destination (destino no I2P) correspondente. Comandos com duas Destinations podem precisar de duas assinaturas.

`oldsig` é sempre a assinatura "interna". Assine e verifique sem as chaves `oldsig` ou `sig` presentes. `sig` é sempre a assinatura "externa". Assine e verifique com a chave `oldsig` presente, mas sem a chave `sig`.

#### Entrada para Assinaturas

Para gerar um fluxo de bytes para criar ou verificar a assinatura, serialize da seguinte forma:

1. Remova a chave `sig`
2. Se estiver verificando com `oldsig`, também remova a chave `oldsig`
3. Somente para comandos Add ou Change, emita `example.i2p=b64dest`
4. Se restarem chaves, emita `#!`
5. Ordene as opções por chave UTF-8, falhe se houver chaves duplicadas
6. Para cada par chave/valor, emita `key=value`, seguido (se não for o último par chave/valor) de um `#`

**Notas**

- Não produza uma quebra de linha
- A codificação de saída é UTF-8
- Toda a codificação de destination e de assinatura é em Base 64 usando o alfabeto I2P
- Chaves e valores são sensíveis a maiúsculas/minúsculas
- Os nomes de host devem estar em minúsculas

#### Tipos de assinatura atuais

A partir do I2P 2.10.0, os seguintes tipos de assinatura são suportados para destinos:

- **EdDSA_SHA512_Ed25519** (Type 7): Mais comum para destinos desde 0.9.15. Usa uma chave pública de 32 bytes e uma assinatura de 64 bytes. Este é o tipo de assinatura recomendado para novos destinos.
- **RedDSA_SHA512_Ed25519** (Type 13): Disponível apenas para destinos e leasesets (estruturas do I2P usadas para descoberta de destinos) criptografados (desde 0.9.39).
- Tipos legados (DSA_SHA1, variantes de ECDSA): Ainda suportados, porém desaconselhados para novas Identidades de Router a partir de 0.9.58.

Nota: As opções criptográficas pós-quânticas estão disponíveis desde o I2P 2.10.0, mas ainda não são os tipos de assinatura padrão.

## Compatibilidade

Todas as novas linhas no formato hosts.txt são implementadas usando caracteres de comentário iniciais (`#!`), assim, todas as versões mais antigas do I2P interpretarão os novos comandos como comentários e os ignorarão sem problemas.

Quando os I2P routers atualizarem para a nova especificação, eles não reinterpretarão comentários antigos, mas passarão a atender a novos comandos nas buscas subsequentes de seus feeds de assinatura. Assim, é importante que os servidores de nomes persistam as entradas de comando de alguma forma, ou habilitem o suporte a ETag para que os routers possam buscar todos os comandos anteriores.

## Estado da implementação

**Implantação inicial:** Versão 0.9.26 (7 de junho de 2016)

**Estado atual:** Estável e inalterado até a versão I2P 2.10.0 (Router API 0.9.65, setembro de 2025)

**Status da proposta:** ENCERRADA (implantado com sucesso em toda a rede)

**Local de implementação:** `apps/addressbook/java/src/net/i2p/addressbook/` no router Java do I2P

**Principais classes:** - `SubscriptionList.java`: Gerencia o processamento de assinaturas - `Subscription.java`: Lida com feeds de assinatura individuais - `AddressBook.java`: Funcionalidade essencial do livro de endereços - `Daemon.java`: Serviço em segundo plano do livro de endereços

**URL de assinatura padrão:** `http://i2p-projekt.i2p/hosts.txt`

## Detalhes do transporte

Subscrições usam HTTP com suporte a GET condicional:

- **Cabeçalho ETag:** Suporta detecção eficiente de alterações
- **Cabeçalho Last-Modified:** Acompanha os horários de atualização da assinatura
- **304 Not Modified:** Os servidores devem retornar isso quando o conteúdo não tiver sido alterado
- **Content-Length:** Altamente recomendado para todas as respostas

O I2P router usa o comportamento padrão de cliente HTTP com suporte adequado a cache.

## Contexto da Versão

**Nota sobre o versionamento do I2P:** Por volta da versão 1.5.0 (agosto de 2021), o I2P mudou do versionamento 0.9.x para o versionamento semântico (1.x, 2.x, etc.). No entanto, a versão interna da Router API continua a usar a numeração 0.9.x para compatibilidade com versões anteriores. Em outubro de 2025, a versão atual é I2P 2.10.0 com a versão da Router API 0.9.65.

Este documento de especificação foi originalmente redigido para a versão 0.9.49 (fevereiro de 2021) e continua totalmente correto para a versão atual 0.9.65 (I2P 2.10.0), porque o sistema de feeds de subscrição não sofreu alterações desde a sua implementação original na versão 0.9.26.

## Referências

- [Proposta 112 (Original)](/proposals/112-addressbook-subscription-feed-commands/)
- [Especificação Oficial](/docs/specs/subscription/)
- [Documentação de Nomenclatura do I2P](/docs/overview/naming/)
- [Especificação de Estruturas Comuns](/docs/specs/common-structures/)
- [Repositório de Código-Fonte do I2P](https://github.com/i2p/i2p.i2p)
- [Repositório Gitea do I2P](https://i2pgit.org/I2P_Developers/i2p.i2p)

## Desenvolvimentos relacionados

Embora o próprio sistema de feed de assinaturas não tenha sido alterado, os seguintes desenvolvimentos relacionados na infraestrutura de nomes do I2P podem ser de interesse:

- **Nomes Base32 Estendidos** (0.9.40+): Suporte a endereços base32 com 56+ caracteres para leasesets criptografados. Não afeta o formato do feed de assinatura.
- **Registro do TLD .i2p.alt** (RFC 9476, final de 2023): Registro oficial na GANA de .i2p.alt como um TLD alternativo. Atualizações futuras do router podem remover o sufixo .alt, mas não são necessárias alterações nos comandos de assinatura.
- **Criptografia Pós-Quântica** (2.10.0+): Disponível, mas não é o padrão. Consideração futura para algoritmos de assinatura nos feeds de assinatura.
