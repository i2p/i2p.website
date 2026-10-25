---
title: "Comandos de Feed de Assinatura do Livro de Endereços"
description: "Especificação para estender o feed de assinatura de endereços com comandos para permitir que servidores de nomes transmitam atualizações de entradas de detentores de nomes de host."
slug: "subscription"
aliases:
  - "/pt/docs/specs/subscription-spec"
  - "/pt/docs/specs/subscription-spec/"
category: "Formatos"
lastUpdated: "2021-01"
accurateFor: "0.9.49"
---

## Visão Geral

Esta especificação estende o feed de assinatura de endereços com comandos, para permitir que servidores de nomes transmitam atualizações de entradas de detentores de nomes de host. Implementado na versão 0.9.26, originalmente proposto na proposta 112.

## Motivação

Anteriormente, os servidores de subscrição hosts.txt apenas enviavam dados no formato hosts.txt, que é o seguinte:

```
example.i2p=b64destination
```
Existem vários problemas com isso:

- Detentores de hostnames não podem atualizar o Destination associado aos seus hostnames (para, por exemplo, atualizar a chave de assinatura para um tipo mais forte).
- Detentores de hostnames não podem renunciar aos seus hostnames arbitrariamente; eles devem entregar as chaves privadas do Destination correspondente diretamente ao novo detentor.
- Não há forma de autenticar que um subdomínio é controlado pelo hostname base correspondente; isso atualmente é aplicado apenas individualmente por alguns servidores de nomes.

## Design

Esta especificação adiciona uma série de linhas de comando ao formato hosts.txt. Com esses comandos, os servidores de nomes podem estender seus serviços para fornecer uma série de recursos adicionais. Clientes que implementam esta especificação poderão escutar esses recursos através do processo de subscrição regular.

Todas as linhas de comando devem ser assinadas pelo Destination correspondente. Isso garante que as alterações sejam feitas apenas mediante solicitação do detentor do nome de host.

## Implicações de Segurança

Esta especificação não afeta o anonimato.

Existe um aumento no risco associado à perda de controle de uma chave Destination, já que alguém que a obtém pode usar esses comandos para fazer alterações em quaisquer hostnames associados. Mas isso não é mais problemático do que o status quo atual, onde alguém que obtém um Destination pode se passar por um hostname e (parcialmente) assumir o controle de seu tráfego. O risco aumentado também é equilibrado ao dar aos detentores de hostname a capacidade de alterar o Destination associado a um hostname, no caso de acreditarem que o Destination foi comprometido; isso é impossível com o sistema atual.

## Especificação

### Novos Tipos de Linha

Existem dois novos tipos de linhas:

1. Comandos Add e Change:

   ```
   example.i2p=b64destination#!key1=val1#key2=val2 ...
   ```
2. Comandos de remoção:

   ```
   #!key1=val1#key2=val2 ...
   ```
#### Ordenação

Um feed não é necessariamente ordenado ou completo. Por exemplo, um comando de alteração pode estar em uma linha antes de um comando de adição, ou sem um comando de adição.

As chaves podem estar em qualquer ordem. Chaves duplicadas não são permitidas. Todas as chaves e valores são sensíveis a maiúsculas e minúsculas.

### Chaves Comuns

Obrigatório em todos os comandos:

**sig** : Assinatura B64, usando a chave de assinatura do destino

Referências a um segundo hostname e/ou destino:

**oldname** : Um segundo nome de host (novo ou alterado)

**olddest** : Um segundo destino b64 (novo ou alterado)

**oldsig** : Uma segunda assinatura b64, usando chave de assinatura de olddest

Outras chaves comuns:

**action** : Um comando

**name** : O nome do host, presente apenas se não precedido por `example.i2p=b64dest`

**dest** : O destino b64, presente apenas se não precedido por `example.i2p=b64dest`

**date** : Em segundos desde a época (epoch)

**expires** : Em segundos desde epoch

### Comandos

Todos os comandos exceto o comando "Add" devem conter uma chave/valor `action=command`.

Para compatibilidade com clientes mais antigos, a maioria dos comandos é precedida por `example.i2p=b64dest`, conforme observado abaixo. Para alterações, estes são sempre os novos valores. Quaisquer valores antigos são incluídos na seção chave/valor.

As chaves listadas são obrigatórias. Todos os comandos podem conter itens chave/valor adicionais não definidos aqui.

#### Adicionar Nome do Host

**Precedido por example.i2p=b64dest** : SIM, este é o novo nome do host e destino.

**action** : NÃO incluído, está implícito.

**sig** : assinatura

Exemplo:

```
example.i2p=b64dest#!sig=b64sig
```
#### Alterar Nome do Host

**Precedido por exemplo.i2p=b64dest** : SIM, este é o novo nome de host e o destino antigo.

**action** : changename

**oldname** : o antigo nome do host, a ser substituído

**sig** : assinatura

Exemplo:

```
example.i2p=b64dest#!action=changename#oldname=oldhostname#sig=b64sig
```
#### Alterar Destino

**Precedido por example.i2p=b64dest** : SIM, este é o nome de host antigo e o novo destino.

**action** : changedest

**olddest** : o dest antigo, a ser substituído

**oldsig** : assinatura usando olddest

**sig** : assinatura

Exemplo:

```
example.i2p=b64dest#!action=changedest#olddest=oldb64dest#oldsig=b64sig#sig=b64sig
```
#### Adicionar Alias de Hostname

**Precedido por example.i2p=b64dest** : SIM, este é o novo nome de host (alias) e o destino antigo.

**action** : addname

**oldname** : o antigo hostname

**sig** : assinatura

Exemplo:

```
example.i2p=b64dest#!action=addname#oldname=oldhostname#sig=b64sig
```
#### Adicionar Alias de Destino

(Usado para atualização de criptografia)

**Precedido por example.i2p=b64dest** : SIM, este é o nome de host antigo e o novo destino (alternativo).

**action** : adddest

**olddest** : o dest antigo

**oldsig** : assinatura usando olddest

**sig** : assinatura usando dest

Exemplo:

```
example.i2p=b64dest#!action=adddest#olddest=oldb64dest#oldsig=b64sig#sig=b64sig
```
#### Adicionar Subdomínio

**Precedido por subdomain.example.i2p=b64dest** : SIM, este é o novo nome de subdomínio do host e destino.

**action** : addsubdomain

**oldname** : o hostname de nível superior (example.i2p)

**olddest** : o destino de nível superior (por exemplo, example.i2p)

**oldsig** : assinatura usando olddest

**sig** : assinatura usando dest

Exemplo:

```
subdomain.example.i2p=b64dest#!action=addsubdomain#oldname=example.i2p#olddest=oldb64dest#oldsig=b64sig#sig=b64sig
```
#### Atualizar Metadados

**Precedido por example.i2p=b64dest** : SIM, este é o nome de host antigo e o destino.

**action** : update

**sig** : assinatura

(adicione aqui quaisquer chaves atualizadas)

Exemplo:

```
example.i2p=b64dest#!action=update#k1=v1#k2=v2#sig=b64sig
```
#### Remover Nome do Host

**Precedido por example.i2p=b64dest** : NÃO, estes são especificados nas opções

**action** : remove

**name** : o nome do host

**dest** : o destino

**sig** : assinatura

Exemplo:

```
#!action=remove#name=example.i2p#dest=b64dest#sig=b64sig
```
#### Remover Todos com Este Destino

**Precedido por example.i2p=b64dest** : NÃO, estes são especificados nas opções

**action** : removeall

**name** : o antigo hostname, apenas consultivo

**dest** : o dest antigo, todos com este dest são removidos

**sig** : assinatura

Exemplo:

```
#!action=removeall#name=example.i2p#dest=b64dest#sig=b64sig
```
### Assinaturas

Todos os comandos devem conter uma chave/valor de assinatura `sig=b64signature` onde a assinatura é para os outros dados, usando a chave de assinatura do destino.

Para comandos que incluem um destino antigo e novo, também deve haver um `oldsig=b64signature`, e oldname, olddest, ou ambos.

Em um comando Add ou Change, a chave pública para verificação está no Destination a ser adicionado ou alterado.

Em alguns comandos de adição ou edição, pode haver um destino adicional referenciado, por exemplo, ao adicionar um alias ou alterar um destino ou nome de host. Nesse caso, deve haver uma segunda assinatura incluída e ambas devem ser verificadas. A segunda assinatura é a assinatura "interna" e é assinada e verificada primeiro (excluindo a assinatura "externa"). O cliente deve tomar qualquer ação adicional necessária para verificar e aceitar as alterações.

oldsig é sempre a assinatura "interna". Assine e verifique sem as chaves 'oldsig' ou 'sig' presentes. sig é sempre a assinatura "externa". Assine e verifique com a chave 'oldsig' presente, mas não a chave 'sig'.

#### Entrada para Assinaturas

Para gerar um fluxo de bytes para criar ou verificar a assinatura, serialize da seguinte forma:

- Remover a chave "sig"
- Se verificando com oldsig, também remover a chave "oldsig"
- Apenas para comandos Add ou Change, produzir `example.i2p=b64dest`
- Se alguma chave permanecer, produzir `#!`
- Ordenar as opções por chave UTF-8, falhar se houver chaves duplicadas
- Para cada chave/valor, produzir `key=value`, seguido por (se não for o último par chave/valor) um `#`

Notas:

- Não gerar uma nova linha
- A codificação de saída é UTF-8
- Toda codificação de destino e assinatura está em Base 64 usando o alfabeto I2P
- Chaves e valores são sensíveis a maiúsculas e minúsculas
- Nomes de host devem estar em minúsculas

## Compatibilidade

Todas as novas linhas no formato hosts.txt são implementadas usando caracteres de comentário iniciais, então todas as versões mais antigas do I2P irão interpretar os novos comandos como comentários.

Quando os routers I2P atualizarem para a nova especificação, eles não vão reinterpretar comentários antigos, mas começarão a escutar novos comandos em buscas subsequentes de seus feeds de subscrição. Portanto, é importante que os servidores de nomes persistam as entradas de comandos de alguma forma, ou habilitem o suporte a etag para que os routers possam buscar todos os comandos anteriores.
