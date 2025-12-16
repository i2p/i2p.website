---
title: "I2PControl API 2"
number: "118"
author: "hottuna"
created: "2016-01-23"
lastupdated: "2018-03-22"
status: "Rejected"
thread: "http://zzz.i2p/topics/2030"
toc: true
---

## Visão Geral

Esta proposta descreve a API2 para o I2PControl.

Esta proposta foi rejeitada e não será implementada, pois quebra a compatibilidade retroativa.
Veja o link da discussão no fórum para detalhes.

### Aviso para desenvolvedores!

Todos os parâmetros RPC agora serão em letras minúsculas. Isso *quebrará* a compatibilidade
retroativa com as implementações da API1. A razão para isso é fornecer aos usuários de >=API2
a API mais simples e coerente possível.


## Especificação da API 2

```json
{
    "id": "id",
    "method": "method_name",
    "params": {
      "token": "auth_token",
      "method_param": "method_parameter_value",
    },
    "jsonrpc": "2.0"
  }

  {
    "id": "id",
    "result": "result_value",
    "jsonrpc": "2.0"
  }
```

### Parâmetros

**`"id"`**

O número de identificação ou a solicitação. Usado para identificar qual resposta foi gerada por qual solicitação.

**`"method_name"`**

O nome do RPC que está sendo invocado.

**`"auth_token"`**

O token de autenticação da sessão. Precisa ser fornecido com todos os RPCs, exceto para a chamada 'authenticate'.

**`"method_parameter_value"`**

O parâmetro do método. Usado para oferecer diferentes variações de um método. Como 'get', 'set' e variações desse tipo.

**`"result_value"`**

O valor que o RPC retorna. Seu tipo e conteúdo dependem do método em questão.


### Prefixos

O esquema de nomenclatura RPC é semelhante ao como é feito em CSS, com prefixos de fornecedores
para as diferentes implementações de API (i2p, kovri, i2pd):

```text
XXX.YYY.ZZZ
    i2p.XXX.YYY.ZZZ
    i2pd.XXX.YYY.ZZZ
    kovri.XXX.YYY.ZZZ
```

A ideia geral com os prefixos específicos de fornecedores é permitir alguma margem de manobra
e deixar as implementações inovarem sem ter que esperar que todas as outras implementações
alcancem. Se um RPC for implementado por todas as implementações seus múltiplos prefixos podem
ser removidos e ele pode ser incluído como um RPC central na próxima versão da API.


### Guia de leitura dos métodos

 * **rpc.method**

   * *parameter* [tipo de parâmetro]:  [null], [number], [string], [boolean],
     [array] ou [object]. [object] sendo um mapa {key:value}.
  * Retorna:

```text

  "return_value" [string] // Este é o valor retornado pela chamada RPC
```


### Métodos

* **authenticate** - Dado que uma senha correta é fornecida, este método fornece um token para acesso posterior e uma lista de níveis de API suportados.

  * *password* [string]:  A senha para esta implementação do i2pcontrol

    Retorna:
```text
    [object]
    {
      "token" : [string], // O token a ser usado que deve ser fornecido com todos os outros métodos RPC
      "api" : [[int],[int], ...]  // Uma lista de níveis de API suportados.
    }
```


* **control.** - Controlar i2p

  * **control.reseed** - Iniciar o reseeding

    * [nil]: Nenhum parâmetro necessário

    Retorna:
```text
      [nil]
```

  * **control.restart** - Reiniciar a instância do i2p

    * [nil]: Nenhum parâmetro necessário

    Retorna:
```text
      [nil]
```

  * **control.restart.graceful** - Reiniciar a instância do i2p de maneira graciosa

    * [nil]: Nenhum parâmetro necessário

    Retorna:
```text
      [nil]
```

  * **control.shutdown** - Encerrar a instância do i2p

    * [nil]: Nenhum parâmetro necessário

    Retorna:
```text
      [nil]
```

  * **control.shutdown.graceful** - Encerrar a instância do i2p de maneira graciosa

    * [nil]: Nenhum parâmetro necessário

    Retorna:
```text
      [nil]
```

  * **control.update.find** - **BLOQUEANTE** Procurar por atualizações assinadas

    * [nil]: Nenhum parâmetro necessário

    Retorna:
```text
      true [boolean] // Verdadeiro se houver uma atualização assinada disponível
```

  * **control.update.start** - Iniciar o processo de atualização

    * [nil]: Nenhum parâmetro necessário

    Retorna:
```text
      [nil]
```


* **i2pcontrol.** - Configurar o i2pcontrol

  * **i2pcontrol.address** - Obter/Definir o endereço IP ao qual o i2pcontrol se conecta.

    * *get* [null]: Este parâmetro não precisa ser definido.

    Retorna:
```text
      "0.0.0.0" [string]
```

    * *set* [string]: Este será um endereço IP como "0.0.0.0" ou "192.168.0.1"

    Retorna:
```text
      [nil]
```

  * **i2pcontrol.password** - Alterar a senha do i2pcontrol.

    * *set* [string]: Definir a nova senha para esta string

    Retorna:
```text
      [nil]
```

  * **i2pcontrol.port** - Obter/Definir a porta à qual o i2pcontrol se conecta.

    * *get* [null]: Este parâmetro não precisa ser definido.

    Retorna:
```text
      7650 [number]
```

    * *set* [number]: Alterar a porta à qual o i2pcontrol se conecta para esta porta

    Retorna:
```text
      [nil]
```


* **settings.** - Obter/Definir configurações da instância i2p

  * **settings.advanced** - Configurações avançadas

    * *get*  [string]: Obter o valor desta configuração

    Retorna:
```text
      "setting-value" [string]
```

    * *getAll* [null]:

    Retorna:
```text
      [object]
      {
        "setting-name" : "setting-value", [string]
        ".." : ".."
      }
```

    * *set* [string]: Definir o valor desta configuração
    * *setAll* [object] {"setting-name" : "setting-value", ".." : ".." }

    Retorna:
```text
      [nil]
```

  * **settings.bandwidth.in** - Configurações de largura de banda de entrada
  * **settings.bandwidth.out** - Configurações de largura de banda de saída

    * *get* [nil]: Este parâmetro não precisa ser definido.

    Retorna:
```text
      0 [number]
```

    * *set* [number]: Definir o limite de largura de banda

    Retorna:
```text
     [nil]
```

  * **settings.ntcp.autoip** - Obter configuração de detecção automática de IP para NTCP

    * *get* [null]: Este parâmetro não precisa ser definido.

    Retorna:
```text
      true [boolean]
```

  * **settings.ntcp.hostname** - Obter nome do host NTCP

    * *get* [null]: Este parâmetro não precisa ser definido.

    Retorna:
```text
      "0.0.0.0" [string]
```

    * *set* [string]: Definir novo nome do host

    Retorna:
```text
      [nil]
```

  * **settings.ntcp.port** - Porta NTCP

    * *get* [null]: Este parâmetro não precisa ser definido.

    Retorna:
```text
      0 [number]
```

    * *set* [number]: Definir nova porta NTCP.

    Retorna:
```text
      [nil]
```

    * *set* [boolean]: Definir detecção automática de IP NTCP

    Retorna:
```text
      [nil]
```

  * **settings.ssu.autoip** - Configurar detecção automática de IP para SSU

    * *get* [nil]: Este parâmetro não precisa ser definido.

    Retorna:
```text
      true [boolean]
```

  * **settings.ssu.hostname** - Configurar nome do host SSU

    * *get* [null]: Este parâmetro não precisa ser definido.

    Retorna:
```text
      "0.0.0.0" [string]
```

    * *set* [string]: Definir novo nome do host SSU

    Retorna:
```text
      [nil]
```

  * **settings.ssu.port** - Porta SSU

    * *get* [null]: Este parâmetro não precisa ser definido.

    Retorna:
```text
      0 [number]
```

    * *set* [number]: Definir nova porta SSU.

    Retorna:
```text
      [nil]
```

    * *set* [boolean]: Definir detecção automática de IP SSU

    Retorna:
```text
      [nil]
```

  * **settings.share** - Obter porcentagem de compartilhamento de largura de banda

    * *get* [null]: Este parâmetro não precisa ser definido.

    Retorna:
```text
      0 [number] // Porcentagem de compartilhamento de largura de banda (0-100)
```

    * *set* [number]: Definir porcentagem de compartilhamento de largura de banda (0-100)

    Retorna:
```text
      [nil]
```

  * **settings.upnp** - Ativar ou desativar o UPNP

    * *get* [nil]: Este parâmetro não precisa ser definido.

    Retorna:
```text
      true [boolean]
```

    * *set* [boolean]: Definir detecção automática de IP SSU

    Retorna:
```text
      [nil]
```



* **stats.** - Obter estatísticas da instância i2p

  * **stats.advanced** - Este método fornece acesso a todas as estatísticas mantidas dentro da instância.

    * *get* [string]:  Nome da estatística avançada a ser fornecida
    * *Opicional:* *period* [number]:  O período para a estatística solicitada

  * **stats.knownpeers** - Retorna o número de peers conhecidos
  * **stats.uptime** - Retorna o tempo em ms desde que o roteador foi iniciado
  * **stats.bandwidth.in** - Retorna a largura de banda de entrada (idealmente para o último segundo)
  * **stats.bandwidth.in.total** - Retorna o número de bytes recebidos desde o último reinício
  * **stats.bandwidth.out** - Retorna a largura de banda de saída (idealmente para o último segundo)
  * **stats.bandwidth.out.total** - Retorna o número de bytes enviados desde o último reinício
  * **stats.tunnels.participating** - Retorna o número de túneis participando atualmente
  * **stats.netdb.peers.active** - Retorna o número de peers com os quais nos comunicamos recentemente
  * **stats.netdb.peers.fast** - Retorna o número de peers 'rápidos'
  * **stats.netdb.peers.highcapacity** - Retorna o número de peers 'alta capacidade'
  * **stats.netdb.peers.known** - Retorna o número de peers conhecidos

    * *get* [null]: Este parâmetro não precisa ser definido.

    Retorna:
```text
      0.0 [number]
```


* **status.** - Obter status da instância i2p

  * **status.router** - Obter status do roteador

    * *get* [null]: Este parâmetro não precisa ser definido.

    Retorna:
```text
      "status" [string]
```

  * **status.net** - Obter status da rede do roteador

    * *get* [null]: Este parâmetro não precisa ser definido.

    Retorna:
```text
      0 [number]
      /**
       *    0 – OK
       *    1 – TESTANDO
       *    2 – COM FIREWALL
       *    3 – OCULTO
       *    4 – AVISO_FIREWALLED_AND_FAST
       *    5 – AVISO_FIREWALLED_AND_FLOODFILL
       *    6 – AVISO_FIREWALLED_WITH_INBOUND_TCP
       *    7 – AVISO_FIREWALLED_WITH_UDP_DISABLED
       *    8 – ERRO_I2CP
       *    9 – ERRO_DESVIO_DE_RELOGIO
       *   10 – ERRO_ENDEREÇO_TCP_PRIVADO
       *   11 – ERRO_NAT_SIMÉTRICO
       *   12 – ERRO_PORTA_UDP_EM_USO
       *   13 – ERRO_SEM_PEERS_ATIVOS_VERIFIQUE_CONEXÃO_E_FIREWALL
       *   14 – ERRO_UDP_DESABILITADO_E_TCP_NÃO_DEFINIDO
       */
```

  * **status.isfloodfill** - A instância i2p é atualmente um floodfill

    * *get* [null]: Este parâmetro não precisa ser definido.

    Retorna:
```text
      true [boolean]
```

  * **status.isreseeding** - A instância i2p está atualmente em reseeding

    * *get* [null]: Este parâmetro não precisa ser definido.

    Retorna:
```text
      true [boolean]
```

  * **status.ip** - IP público detectado desta instância i2p

    * *get* [null]: Este parâmetro não precisa ser definido.

    Retorna:
```text
      "0.0.0.0" [string]
```
