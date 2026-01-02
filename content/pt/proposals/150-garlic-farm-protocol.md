---
title: "Protocolo da Fazenda de Alho"
number: "150"
author: "zzz"
created: "02-05-2019"
lastupdated: "20-05-2019"
status: "Aberto"
thread: "http://zzz.i2p/topics/2234"
toc: true
---

## Visão Geral

Esta é a especificação para o protocolo de rede da Fazenda de Alho,
baseado no JRaft, seu código "exts" para implementação sobre TCP,
e seu aplicativo de exemplo "dmprinter" [JRAFT](https://github.com/datatechnology/jraft).
JRaft é uma implementação do protocolo Raft [RAFT](https://ramcloud.stanford.edu/wiki/download/attachments/11370504/raft.pdf).

Não conseguimos encontrar nenhuma implementação com um protocolo de rede documentado.
No entanto, a implementação do JRaft é simples o suficiente para que pudéssemos
inspecionar o código e então documentar seu protocolo.
Esta proposta é o resultado desse esforço.

Este será o backend para coordenação de roteadores que publicam
entradas em um Meta LeaseSet. Veja a proposta 123.


## Objetivos

- Tamanho de código reduzido
- Baseado em implementação existente
- Sem objetos Java serializados ou qualquer recurso ou codificação específica de Java
- Qualquer inicialização está fora do escopo. Pelo menos outro servidor deve ser
  codificado, ou configurado fora deste protocolo.
- Suporte para casos de uso fora da banda e dentro do I2P.


## Design

O protocolo Raft não é um protocolo concreto; ele define apenas uma máquina de estados.
Portanto, documentamos o protocolo concreto do JRaft e baseamos nosso protocolo nele.
Não há mudanças no protocolo JRaft além da adição de
um aperto de mão de autenticação.

O Raft elege um Líder cuja tarefa é publicar um log.
O log contém dados de Configuração de Raft e dados de Aplicação.
Os dados de Aplicação contêm o status de cada Roteador do Servidor e o Destino
para o cluster Meta LS2.
Os servidores usam um algoritmo comum para determinar o publicador e o conteúdo
do Meta LS2.
O publicador do Meta LS2 NÃO é necessariamente o Líder Raft.


## Especificação

O protocolo de rede é sobre sockets SSL ou sockets I2P não-SSL.
Sockets I2P são proxy através do Proxy HTTP.
Não há suporte para sockets non-SSL na rede pública.

### Aperto de mão e autenticação

Não definido pelo JRaft.

Objetivos:

- Método de autenticação usuário/senha
- Identificador de versão
- Identificador de cluster
- Extensível
- Facilita o proxy quando usado para sockets I2P
- Não expor desnecessariamente o servidor como servidor da Fazenda de Alho
- Protocolo simples para não exigir uma implementação completa de servidor web
- Compatível com padrões comuns, então implementações podem usar
  bibliotecas padrão se desejado

Usaremos um aperto de mão estilo websocket [WEBSOCKET](https://en.wikipedia.org/wiki/WebSocket) e
autenticação HTTP Digest [RFC-2617](https://tools.ietf.org/html/rfc2617).
A autenticação básica do RFC 2617 NÃO é suportada.
Ao proxy pelo proxy HTTP, comunique-se com
o proxy como especificado em [RFC-2616](https://tools.ietf.org/html/rfc2616).

#### Credenciais

Se os nomes de usuário e senhas são por cluster ou
por servidor, depende da implementação.


#### Solicitação HTTP 1

O originador enviará o seguinte.

Todas as linhas são terminadas com CRLF conforme requerido pelo HTTP.

```text
GET /GarlicFarm/CLUSTER/VERSION/websocket HTTP/1.1
  Host: (ip):(port)
  Cache-Control: no-cache
  Connection: close
  (quaisquer outros cabeçalhos são ignorados)
  (linha em branco)

  CLUSTER é o nome do cluster (padrão "farm")
  VERSION é a versão da Fazenda de Alho (atualmente "1")
```


#### Resposta HTTP 1

Se o caminho não for correto, o destinatário enviará uma resposta padrão "HTTP/1.1 404 Not Found",
como em [RFC-2616](https://tools.ietf.org/html/rfc2616).

Se o caminho estiver correto, o destinatário enviará uma resposta padrão "HTTP/1.1 401 Unauthorized",
incluindo o cabeçalho de autenticação HTTP digest WWW-Authenticate,
como em [RFC-2617](https://tools.ietf.org/html/rfc2617).

Ambas as partes então fecharão o socket.


#### Solicitação HTTP 2

O originador enviará o seguinte,
como em [RFC-2617](https://tools.ietf.org/html/rfc2617) e [WEBSOCKET](https://en.wikipedia.org/wiki/WebSocket).

Todas as linhas são terminadas com CRLF conforme requerido pelo HTTP.

```text
GET /GarlicFarm/CLUSTER/VERSION/websocket HTTP/1.1
  Host: (ip):(port)
  Cache-Control: no-cache
  Connection: keep-alive, Upgrade
  Upgrade: websocket
  (cabeçalhos Sec-Websocket-* se proxy)
  Authorization: (cabeçalho de autorização HTTP digest como no RFC 2617)
  (quaisquer outros cabeçalhos são ignorados)
  (linha em branco)

  CLUSTER é o nome do cluster (padrão "farm")
  VERSION é a versão da Fazenda de Alho (atualmente "1")
```


#### Resposta HTTP 2

Se a autenticação não for correta, o destinatário enviará outra resposta padrão "HTTP/1.1 401 Unauthorized",
como em [RFC-2617](https://tools.ietf.org/html/rfc2617).

Se a autenticação for correta, o destinatário enviará a seguinte resposta,
como em [WEBSOCKET](https://en.wikipedia.org/wiki/WebSocket).

Todas as linhas são terminadas com CRLF conforme requerido pelo HTTP.

```text
HTTP/1.1 101 Switching Protocols
  Connection: Upgrade
  Upgrade: websocket
  (cabeçalhos Sec-Websocket-*)
  (quaisquer outros cabeçalhos são ignorados)
  (linha em branco)
```

Depois que isso for recebido, o socket permanece aberto.
O protocolo Raft, conforme definido abaixo, começa, no mesmo socket.


#### Cache

As credenciais devem ser armazenadas em cache por pelo menos uma hora, para que
conexões subsequentes possam ir diretamente para
"Solicitação HTTP 2" acima.


### Tipos de Mensagem

Existem dois tipos de mensagens, solicitações e respostas.
As solicitações podem conter Entradas de Log e são de tamanho variável;
as respostas não contêm Entradas de Log e são de tamanho fixo.

Os tipos de mensagem 1-4 são as mensagens RPC padrão definidas pelo Raft.
Este é o protocolo Raft central.

Os tipos de mensagem 5-15 são as mensagens RPC estendidas definidas pelo
JRaft, para suportar clientes, alterações dinâmicas de servidor e
sincronização eficiente de logs.

Os tipos de mensagem 16-17 são as mensagens RPC de Compação de Log definidas
na seção 7 do Raft.


| Mensagem | Número | Enviado Por | Enviado Para | Notas |
| :--- | :--- | :--- | :--- | :--- |
| RequestVoteRequest | 1 | Candidato | Seguidor | RPC padrão do Raft; não deve conter entradas de log |
| RequestVoteResponse | 2 | Seguidor | Candidato | RPC padrão do Raft |
| AppendEntriesRequest | 3 | Líder | Seguidor | RPC padrão do Raft |
| AppendEntriesResponse | 4 | Seguidor | Líder / Cliente | RPC padrão do Raft |
| ClientRequest | 5 | Cliente | Líder / Seguidor | Resposta é AppendEntriesResponse; deve conter apenas entradas de log de Aplicação |
| AddServerRequest | 6 | Cliente | Líder | Deve conter apenas uma entrada de log ClusterServer |
| AddServerResponse | 7 | Líder | Cliente | O líder também envia um JoinClusterRequest |
| RemoveServerRequest | 8 | Seguidor | Líder | Deve conter apenas uma entrada de log ClusterServer |
| RemoveServerResponse | 9 | Líder | Seguidor | |
| SyncLogRequest | 10 | Líder | Seguidor | Deve conter apenas uma entrada de log LogPack |
| SyncLogResponse | 11 | Seguidor | Líder | |
| JoinClusterRequest | 12 | Líder | Novo Servidor | Convite para entrar; deve conter apenas uma entrada de log de Configuração |
| JoinClusterResponse | 13 | Novo Servidor | Líder | |
| LeaveClusterRequest | 14 | Líder | Seguidor | Comando para sair |
| LeaveClusterResponse | 15 | Seguidor | Líder | |
| InstallSnapshotRequest | 16 | Líder | Seguidor | Seção 7 do Raft; Deve conter apenas uma entrada de log SnapshotSyncRequest |
| InstallSnapshotResponse | 17 | Seguidor | Líder | Seção 7 do Raft |


### Estabelecimento

Após o aperto de mão HTTP, a sequência de estabelecimento é como segue:

```text
Novo Servidor Alice              Seguidor Aleatório Bob

  ClientRequest   ------->
          <---------   AppendEntriesResponse

  Se Bob diz que ele é o líder, continue como abaixo.
  Caso contrário, Alice deve desconectar de Bob e conectar-se ao líder.


  Novo Servidor Alice              Líder Charlie

  ClientRequest   ------->
          <---------   AppendEntriesResponse
  AddServerRequest   ------->
          <---------   AddServerResponse
          <---------   JoinClusterRequest
  JoinClusterResponse  ------->
          <---------   SyncLogRequest
                       OU InstallSnapshotRequest
  SyncLogResponse  ------->
  OU InstallSnapshotResponse
```

Sequência de Desconexão:

```text
Seguidor Alice              Líder Charlie

  RemoveServerRequest   ------->
          <---------   RemoveServerResponse
          <---------   LeaveClusterRequest
  LeaveClusterResponse  ------->
```

Sequência de Eleição:

```text
Candidato Alice               Seguidor Bob

  RequestVoteRequest   ------->
          <---------   RequestVoteResponse

  se Alice vence eleição:

  Líder Alice                Seguidor Bob

  AppendEntriesRequest   ------->
  (sinalização de vida)
          <---------   AppendEntriesResponse
```


### Definições

- Origem: Identifica o originador da mensagem
- Destino: Identifica o destinatário da mensagem
- Termos: Veja Raft. Inicializado para 0, aumenta monotonicamente
- Índices: Veja Raft. Inicializado para 0, aumenta monotonicamente


### Solicitações

As solicitações contêm um cabeçalho e zero ou mais entradas de log.
As solicitações contêm um cabeçalho de tamanho fixo e Entradas de Log opcionais de tamanho variável.


#### Cabeçalho da Solicitação

O cabeçalho da solicitação tem 45 bytes, como segue.
Todos os valores são unsigned big-endian.

```dataspec
Tipo da mensagem:     1 byte
  Origem:             ID, inteiro de 4 bytes
  Destino:            ID, inteiro de 4 bytes
  Termo:              Termo atual (veja notas), inteiro de 8 bytes
  Último Termo do Log:  8 byte integer
  Último Índice do Log: 8 byte integer
  Índice Comprometido:   8 byte integer
  Tamanho das entradas de log:  Tamanho total em bytes, inteiro de 4 bytes
  Entradas de log:    veja abaixo, comprimento total como especificado
```


#### Notas

No RequestVoteRequest, Termo é o termo do candidato.
Caso contrário, é o termo atual do líder.

No AppendEntriesRequest, quando o tamanho das entradas de log é zero,
esta mensagem é um sinal de vida (mensagem de manutenção).


#### Entradas de Log

O log contém zero ou mais entradas de log.
Cada entrada de log é como segue.
Todos os valores são unsigned big-endian.

```dataspec
Termo:        inteiro de 8 bytes
  Tipo de valor:   1 byte
  Tamanho da entrada:  Em bytes, inteiro de 4 bytes
  Entrada:         comprimento conforme especificado
```


#### Conteúdos do Log

Todos os valores são unsigned big-endian.

| Tipo de Valor do Log | Número |
| :--- | :--- |
| Aplicação | 1 |
| Configuração | 2 |
| Servidor de Cluster | 3 |
| Pacote de Log | 4 |
| Pedido de Sincronização de Snapshot | 5 |


#### Aplicação

Os conteúdos da aplicação são codificados em UTF-8 [JSON](https://www.json.org/).
Veja a seção da Camada de Aplicação abaixo.


#### Configuração

Isto é usado para o líder serializar uma nova configuração de cluster e replicar para pares.
Contém zero ou mais configurações de Servidor de Cluster.

```dataspec
Índice do Log:  inteiro de 8 bytes
  Último Índice do Log:  inteiro de 8 bytes
  Dados do Servidor de Cluster para cada servidor:
    ID:                inteiro de 4 bytes
    Compr. dos dados de endpoint: Em bytes, inteiro de 4 bytes
    Dados de endpoint:  string ASCII da forma "tcp://localhost:9001", comprimento conforme especificado
```


#### Servidor de Cluster

As informações de configuração para um servidor em um cluster.
Isso é incluído apenas em uma mensagem AddServerRequest ou RemoveServerRequest.

Quando usado em uma Mensagem AddServerRequest:

```dataspec
ID:                inteiro de 4 bytes
  Compr. dos dados de endpoint: Em bytes, inteiro de 4 bytes
  Dados de endpoint:  string ASCII da forma "tcp://localhost:9001", comprimento conforme especificado
```

Quando usado em uma Mensagem RemoveServerRequest:

```dataspec
ID:                inteiro de 4 bytes
```


#### Pacote de Log

Este é incluído apenas em uma mensagem SyncLogRequest.

O seguinte é compactado com gzip antes da transmissão:

```dataspec
Compr. dos dados de índice: Em bytes, inteiro de 4 bytes
  Compr. dos dados do log: Em bytes, inteiro de 4 bytes
  Dados do índice: 8 bytes para cada índice, comprimento conforme especificado
  Dados do log:   comprimento conforme especificado
```


#### Pedido de Sincronização de Snapshot

Este é incluído apenas em uma mensagem InstallSnapshotRequest.

```dataspec
Último Índice do Log:  inteiro de 8 bytes
  Último Termo do Log:  inteiro de 8 bytes
  Compr. dos dados de configuração: Em bytes, inteiro de 4 bytes
  Dados de configuração: comprimento conforme especificado
  Offset:          O offset dos dados no banco de dados, em bytes, inteiro de 8 bytes
  Compr. dos dados: Em bytes, inteiro de 4 bytes
  Dados:            comprimento conforme especificado
  Está concluído:   1 se concluído, 0 se não concluído (1 byte)
```


### Respostas

Todas as respostas têm 26 bytes, como segue.
Todos os valores são unsigned big-endian.

```dataspec
Tipo da mensagem:   1 byte
  Origem:            ID, inteiro de 4 bytes
  Destino:           Normalmente o ID do destino real (veja notas), inteiro de 4 bytes
  Termo:             Termo atual, inteiro de 8 bytes
  Próximo Índice:    Inicializado para o último índice de log do líder + 1, inteiro de 8 bytes
  Aceito:            1 se aceito, 0 se não aceito (veja notas), 1 byte
```


#### Notas

O ID do Destino é normalmente o destino real para esta mensagem.
No entanto, para AppendEntriesResponse, AddServerResponse e RemoveServerResponse,
ele é o ID do líder atual.

No RequestVoteResponse, Aceito é 1 para um voto para o candidato (solicitante),
e 0 para nenhum voto.


## Camada de Aplicação

Cada Servidor periodicamente publica dados de Aplicação no log em um ClientRequest.
Os dados da Aplicação contêm o status de cada Roteador do Servidor e o Destino
para o cluster Meta LS2.
Os servidores usam um algoritmo comum para determinar o publicador e o conteúdo
do Meta LS2.
O servidor com o status "melhor" recente no log é o publicador do Meta LS2.
O publicador do Meta LS2 NÃO é necessariamente o Líder Raft.


### Conteúdo dos Dados de Aplicação

Os conteúdos da aplicação são codificados em UTF-8 [JSON](https://www.json.org/),
para simplicidade e extensibilidade.
A especificação completa está a ser definida.
O objetivo é fornecer dados suficientes para escrever um algoritmo para determinar o "melhor"
roteador para publicar o Meta LS2, e para o publicador ter informações suficientes
para ponderar os Destinos no Meta LS2.
Os dados conterão tanto as estatísticas do roteador quanto do Destino.

Os dados podem opcionalmente conter dados de sensoriamento remoto sobre a saúde dos
outros servidores e a capacidade de buscar o Meta LS.
Esses dados não seriam suportados na primeira versão.

Os dados podem opcionalmente conter informações de configuração postadas
por um cliente administrador.
Esses dados não seriam suportados na primeira versão.

Se "nome: valor" estiver listado, isso especifica a chave e o valor do mapa JSON.
Caso contrário, a especificação está a ser definida.


Dados do Cluster (nível superior):

- cluster: Nome do cluster
- date: Data destes dados (longo, ms desde a época)
- id: ID do Raft (inteiro)

Dados de Configuração (config):

- Quaisquer parâmetros de configuração

Status de publicação do MetaLS (meta):

- destination: o destino do metals, codificação base64
- lastPublishedLS: se presente, codificação base64 do último metals publicado
- lastPublishedTime: em ms, ou 0 se nunca
- publishConfig: Status de configuração do publicador em off/on/auto
- publishing: status do publicador de metals booleano true/false

Dados do Roteador (router):

- lastPublishedRI: se presente, codificação base64 das últimas informações do roteador publicadas
- uptime: Tempo de atividade em ms
- Atraso de trabalho
- Túneis de exploração
- Túneis participantes
- Largura de banda configurada
- Largura de banda atual

Destinos (destinations):
Lista

Dados do Destino:

- destination: o destino, codificação base64
- uptime: Tempo de atividade em ms
- Túneis configurados
- Túneis atuais
- Largura de banda configurada
- Largura de banda atual
- Conexões configuradas
- Conexões atuais
- Dados de lista negra

Dados de sensoriamento remoto do roteador:

- Última versão RI vista
- Tempo de busca do LS
- Dados do teste de conexão
- Dados do perfil de floodfills mais próximos
  para os períodos de tempo ontem, hoje e amanhã

Dados de sensoriamento remoto do destino:

- Última versão LS vista
- Tempo de busca do LS
- Dados do teste de conexão
- Dados do perfil de floodfills mais próximos
  para os períodos de tempo ontem, hoje e amanhã

Dados de sensoriamento do Meta LS:

- Última versão vista
- Tempo de busca
- Dados do perfil de floodfills mais próximos
  para os períodos de tempo ontem, hoje e amanhã


## Interface de Administração

A ser definido, possivelmente em uma proposta separada.
Não é necessário para a primeira versão.

Requisitos de uma interface administrativa:

- Suporte para múltiplos destinos mestre, i.e. múltiplos clusters virtuais (fazendas)
- Fornecer visão abrangente do estado compartilhado do cluster - todas as estatísticas publicadas pelos membros, quem é o líder atual, etc.
- Capacidade de forçar a remoção de um participante ou líder do cluster
- Capacidade de forçar a publicação de metáLS (se o nó atual for o publicador)
- Capacidade de excluir hashes do metáLS (se o nó atual for o publicador)
- Funcionalidade de importação/exportação de configuração para implantações em massa


## Interface do Roteador

A ser definido, possivelmente em uma proposta separada.
i2pcontrol não é necessário para a primeira versão e alterações detalhadas serão incluídas em uma proposta separada.

Requisitos para API de Fazenda de Alho para roteador (Java in-JVM ou i2pcontrol)

- getLocalRouterStatus()
- getLocalLeafHash(Hash masterHash)
- getLocalLeafStatus(Hash leaf)
- getRemoteMeasuredStatus(Hash masterOrLeaf) // provavelmente não no MVP
- publishMetaLS(Hash masterHash, List<MetaLease> contents) // ou MetaLeaseSet assinado? Quem assina?
- stopPublishingMetaLS(Hash masterHash)
- autenticação a ser definida?


## Justificativa

Atomix é muito grande e não permitirá personalização para que possamos rotear
o protocolo sobre o I2P. Além disso, seu formato de protocolo é não documentado e depende
da serialização Java.


## Notas


## Problemas

- Não há maneira de um cliente descobrir e se conectar a um líder desconhecido.
  Seria uma mudança menor para um Seguidor enviar a Configuração como uma Entrada de Log na Resposta AppendEntries.


## Migração

Sem problemas de compatibilidade retroativa.


## Referências

* [JRAFT](https://github.com/datatechnology/jraft)
* [JSON](https://json.org/)
* [RAFT](https://ramcloud.stanford.edu/wiki/download/attachments/11370504/raft.pdf)
* [RFC-2616](https://tools.ietf.org/html/rfc2616)
* [RFC-2617](https://tools.ietf.org/html/rfc2617)
* [WEBSOCKET](https://en.wikipedia.org/wiki/WebSocket)
