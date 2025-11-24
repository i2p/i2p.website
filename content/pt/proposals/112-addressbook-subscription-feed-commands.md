---
title: "Comandos do Feed de Assinatura do Catálogo de Endereços"
number: "112"
author: "zzz"
created: "2014-09-15"
lastupdated: "2020-07-16"
status: "Closed"
thread: "http://zzz.i2p/topics/1704"
target: "0.9.26"
implementedin: "0.9.26"
---

## Nota
Implementação na rede concluída.
Consulte [SPEC](/docs/specs/subscription/) para a especificação oficial.

## Visão Geral

Esta proposta trata da extensão do feed de assinatura de endereços com comandos, para
permitir que servidores de nomes transmitam atualizações de entradas de detentores de nomes de host.
Implementado na versão 0.9.26.

## Motivação

Atualmente, os servidores de assinatura hosts.txt apenas enviam dados no formato hosts.txt,
que é o seguinte:

  ```text
  example.i2p=b64destination
  ```

Existem vários problemas com isso:

- Os detentores de nomes de host não podem atualizar a Destinação associada aos seus nomes de host
  (por exemplo, para atualizar a chave de assinatura para um tipo mais forte).
- Os detentores de nomes de host não podem abdicar de seus nomes arbitrariamente; eles devem entregar
  as chaves privadas de Destinação correspondentes diretamente ao novo detentor.
- Não há como autenticar que um subdomínio é controlado pelo
  nome base correspondente; atualmente, isso é apenas assegurado individualmente por
  alguns servidores de nomes.

## Design

Esta proposta adiciona uma série de linhas de comando ao formato hosts.txt. Com esses
comandos, os servidores de nomes podem estender seus serviços para fornecer uma série de
recursos adicionais. Clientes que implementarem esta proposta poderão ouvir
esses recursos através do processo regular de assinatura.

Todas as linhas de comando devem ser assinadas pela Destinação correspondente. Isso garante
que as mudanças sejam feitas apenas a pedido do titular do nome de host.

## Implicações de Segurança

Esta proposta não tem implicações sobre anonimato.

Há um aumento no risco associado à perda de controle de uma chave de Destinação,
pois alguém que a obtenha pode usar esses comandos para fazer alterações em qualquer
nome de host associado. Mas isso não é mais problemático do que o status atual,
onde alguém que obtém uma Destinação pode se passar por um nome de host e
(parcialmente) assumir seu tráfego. O risco aumentado também é equilibrado
ao dar aos detentores de nomes de host a capacidade de mudar a Destinação associada a um
nome de host, caso acreditem que a Destinação foi comprometida; isso é
impossível com o sistema atual.

## Especificação

### Novos tipos de linha

Esta proposta adiciona dois novos tipos de linhas:

1. Comandos de Adição e Alteração:

    ```
    example.i2p=b64destination#!key1=val1#key2=val2 ...
    ```

2. Comandos de Remoção:

    ```
    #!key1=val1#key2=val2 ...
    ```

#### Ordenação
Um feed não é necessariamente ordenado ou completo. Por exemplo, um comando de alteração
pode estar em uma linha antes de um comando de adição, ou sem um comando de adição.

As chaves podem estar em qualquer ordem. Chaves duplicadas não são permitidas. Todas as chaves e valores são sensíveis a maiúsculas e minúsculas.

### Chaves Comuns

Obrigatórias em todos os comandos:

sig
  Assinatura em B64, usando a chave de assinatura da destinação

Referências a um segundo nome de host e/ou destinação:

oldname
  Um segundo nome de host (novo ou alterado)
olddest
  Uma segunda destinação em b64 (nova ou alterada)
oldsig
  Uma segunda assinatura em b64, usando a chave de assinatura de nolddest

Outras chaves comuns:

action
  Um comando
name
  O nome do host, presente apenas se não precedido por example.i2p=b64dest
dest
  A destinação em b64, presente apenas se não precedida por example.i2p=b64dest
date
  Em segundos desde a época
expires
  Em segundos desde a época

### Comandos

Todos os comandos exceto o comando "Add" devem conter uma chave/valor "action=command".

Para compatibilidade com clientes mais antigos, a maioria dos comandos é precedida por example.i2p=b64dest,
conforme indicado abaixo. Para alterações, estes são sempre os novos valores. Quaisquer valores antigos
são incluídos na seção chave/valor.

As chaves listadas são obrigatórias. Todos os comandos podem conter itens adicionais de chave/valor
não definidos aqui.

#### Adicionar nome do host
Precedido por example.i2p=b64dest
  SIM, este é o novo nome de host e destinação.
action
  NÃO incluído, é implícito.
sig
  assinatura

Exemplo:

  ```text
  example.i2p=b64dest#!sig=b64sig
  ```

#### Alterar nome do host
Precedido por example.i2p=b64dest
  SIM, este é o novo nome de host e destinação antiga.
action
  changename
oldname
  o antigo nome do host, a ser substituído
sig
  assinatura

Exemplo:

  ```text
  example.i2p=b64dest#!action=changename#oldname=oldhostname#sig=b64sig
  ```

#### Alterar destinação
Precedido por example.i2p=b64dest
  SIM, este é o nome de host antigo e nova destinação.
action
  changedest
olddest
  a antiga destinação, a ser substituída
oldsig
  assinatura usando olddest
sig
  assinatura

Exemplo:

  ```text
  example.i2p=b64dest#!action=changedest#olddest=oldb64dest#oldsig=b64sig#sig=b64sig
  ```

#### Adicionar alias de nome do host
Precedido por example.i2p=b64dest
  SIM, este é o novo nome de host (alias) e a destinação antiga.
action
  addname
oldname
  o antigo nome do host
sig
  assinatura

Exemplo:

  ```text
  example.i2p=b64dest#!action=addname#oldname=oldhostname#sig=b64sig
  ```

#### Adicionar alias de destinação
(Usado para atualização de criptografia)

Precedido por example.i2p=b64dest
  SIM, este é o nome de host antigo e nova destinação (alternativa).
action
  adddest
olddest
  a antiga destinação
oldsig
  assinatura usando olddest
sig
  assinatura usando dest

Exemplo:

  ```text
  example.i2p=b64dest#!action=adddest#olddest=oldb64dest#oldsig=b64sig#sig=b64sig
  ```

#### Adicionar subdomínio
Precedido por subdomain.example.i2p=b64dest
  SIM, este é o novo nome de subdomínio de host e destinação.
action
  addsubdomain
oldname
  o nome de host de nível superior (example.i2p)
olddest
  a destinação de nível superior (para example.i2p)
oldsig
  assinatura usando olddest
sig
  assinatura usando dest

Exemplo:

  ```text
  subdomain.example.i2p=b64dest#!action=addsubdomain#oldname=example.i2p#olddest=oldb64dest#oldsig=b64sig#sig=b64sig
  ```

#### Atualizar metadados
Precedido por example.i2p=b64dest
  SIM, este é o nome de host e destinação antigos.
action
  update
sig
  assinatura

(adicione quaisquer chaves atualizadas aqui)

Exemplo:

  ```text
  example.i2p=b64dest#!action=update#k1=v1#k2=v2#sig=b64sig
  ```

#### Remover nome do host
Precedido por example.i2p=b64dest
  NÃO, estes são especificados nas opções
action
  remove
name
  o nome do host
dest
  a destinação
sig
  assinatura

Exemplo:

  ```text
  #!action=removeall#name=example.i2p#dest=b64destsig=b64sig
  ```

#### Remover todos com esta destinação
Precedido por example.i2p=b64dest
  NÃO, estes são especificados nas opções
action
  removeall
name
  o antigo nome do host, apenas aconselhável
dest
  a antiga destinação, todos com esta destinação são removidos
sig
  assinatura

Exemplo:

  ```text
  #!action=removeall#name=example.i2p#dest=b64destsig=b64sig
  ```

### Assinaturas

Todos os comandos devem conter uma chave/valor de assinatura "sig=b64signature" onde
a assinatura para os outros dados, usando a chave de assinatura de destinação.

Para comandos incluindo uma destinação antiga e nova, deve haver também uma
oldsig=b64signature, e ou oldname, olddest, ou ambos.

Em um comando de Adição ou Alteração, a chave pública para verificação está na
Destinação a ser adicionada ou alterada.

Em alguns comandos de adição ou edição, pode haver uma destinação adicional referenciada,
por exemplo ao adicionar um alias, ou ao mudar uma destinação ou nome de host. Neste
caso, deve haver uma segunda assinatura incluída e ambas devem ser
verificadas. A segunda assinatura é a assinatura "interna" e é assinada e
verificada primeiro (excluindo a assinatura "externa"). O cliente deve tomar qualquer
ação adicional necessária para verificar e aceitar mudanças.

oldsig é sempre a assinatura "interna". Assinar e verificar sem as chaves 'oldsig' ou
'sig' presentes. sig é sempre a assinatura "externa". Assinar e verificar com
a chave 'oldsig' presente, mas não a chave 'sig'.

#### Entrada para assinaturas
Para gerar um fluxo de bytes para criar ou verificar a assinatura, serializar da seguinte forma:

- Remova a chave "sig"
- Se verificando com oldsig, também remova a chave "oldsig"
- Apenas para comandos de Adição ou Alteração,
  saída example.i2p=b64dest
- Se restarem chaves, saída "#!"
- Classifique as opções por chave UTF-8, falhe se houver chaves duplicadas
- Para cada chave/valor, saída key=value, seguida (se não for a última chave/valor)
  de um '#'

Notas

- Não saia com uma nova linha
- A codificação da saída é UTF-8
- Toda a codificação de destinações e assinaturas é em Base 64 usando o alfabeto I2P
- Chaves e valores são sensíveis a maiúsculas e minúsculas
- Os nomes de host devem estar em letras minúsculas

## Compatibilidade

Todas as novas linhas no formato hosts.txt são implementadas usando caracteres de comentário
iniciais, então todas as versões antigas do I2P interpretarão os novos comandos como
comentários.

Quando os roteadores I2P forem atualizados para a nova especificação, eles não reinterpretarão
os comentários antigos, mas começarão a ouvir novos comandos em buscas subsequentes de
seus feeds de assinatura. Assim, é importante que os servidores de nomes persistam
entradas de comando de alguma forma, ou habilitem o suporte a etag para que os roteadores possam
buscar todos os comandos passados.
