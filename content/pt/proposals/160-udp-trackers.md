---
title: "Rastreadores UDP"
number: "160"
author: "zzz"
created: "2022-01-03"
lastupdated: "2025-06-25"
status: "Fechado"
thread: "http://zzz.i2p/topics/1634"
target: "0.9.67"
---

## Status

Aprovado na revisão em 2025-06-24.
Especificação está em [UDP specification](/en/docs/spec/udp-bittorrent-announces/).
Implementado em zzzot 0.20.0-beta2.
Implementado em i2psnark a partir da API 0.9.67.
Verifique a documentação de outras implementações para status.


## Visão Geral

Esta proposta é para a implementação de rastreadores UDP no I2P.


### Histórico de Alterações

Uma proposta preliminar para rastreadores UDP no I2P foi postada em nossa página de especificação de bittorrent [/en/docs/applications/bittorrent/](/en/docs/applications/bittorrent/)
em maio de 2014; isso precedeu nosso processo formal de propostas e nunca foi implementado.
Esta proposta foi criada no início de 2022 e simplifica a versão de 2014.

Como esta proposta depende de datagramas repliáveis, ela foi colocada em espera uma vez que começamos a trabalhar na proposta Datagram2 [/en/proposals/163-datagram2/](/en/proposals/163-datagram2/) no início de 2023.
Essa proposta foi aprovada em abril de 2025.

A versão de 2023 desta proposta especificou dois modos, "compatibilidade" e "rápido".
Análises adicionais revelaram que o modo rápido seria inseguro e também ineficiente para clientes com um grande número de torrents.
Além disso, BiglyBT indicou uma preferência pelo modo de compatibilidade.
Este modo facilitará a implementação para qualquer rastreador ou cliente que suporte o padrão [BEP 15](http://www.bittorrent.org/beps/bep_0015.html).

Embora o modo de compatibilidade seja mais complexo de implementar do zero no tamanho do cliente, temos código preliminar para isso iniciado em 2023.

Portanto, a versão atual aqui é ainda mais simplificada para remover o modo rápido e o termo "compatibilidade". A versão atual troca para o novo formato Datagram2 e adiciona referências ao protocolo de extensão de anúncio UDP [BEP 41](http://www.bittorrent.org/beps/bep_0041.html).

Além disso, um campo de duração de ID de conexão é adicionado à resposta de conexão, para estender os ganhos de eficiência deste protocolo.


## Motivação

À medida que a base de usuários em geral e o número de usuários de bittorrent especificamente continua a crescer, precisamos tornar os rastreadores e anúncios mais eficientes para que os rastreadores não sejam sobrecarregados.

O Bittorrent propôs rastreadores UDP no BEP 15 [BEP 15](http://www.bittorrent.org/beps/bep_0015.html) em 2008, e a vasta maioria dos rastreadores no clearnet agora são somente UDP.

É difícil calcular a economia de largura de banda de datagramas versus protocolo de streaming.
Uma solicitação de réplica tem aproximadamente o mesmo tamanho de um SYN de streaming, mas a carga útil é cerca de 500 bytes menor porque o HTTP GET tem uma enorme string de parâmetros de URL de 600 bytes.
A resposta bruta é muito menor que um SYN ACK de streaming, proporcionando redução significativa para o tráfego de saída de um rastreador.

Além disso, deve haver reduções específicas de memória na implementação, já que datagramas exigem muito menos estado na memória do que uma conexão de streaming.

A criptografia e assinaturas pós-quânticas, conforme previsto em [/en/proposals/169-pq-crypto/](/en/proposals/169-pq-crypto/), aumentarão substancialmente a sobrecarga de estruturas criptografadas e assinadas, incluindo destinos, leasesets, streaming SYN e SYN ACK. É importante minimizar essa sobrecarga sempre que possível antes que a criptografia PQ seja adotada no I2P.


## Design

Esta proposta usa datagrama2 repliável, datagrama3 repliável e datagramas brutos, conforme definido em [/en/docs/spec/datagrams/](/en/docs/spec/datagrams/).
Datagrama2 e Datagram3 são novas variantes de datagramas repliáveis, definidos na Proposta 163 [/en/proposals/163-datagram2/](/en/proposals/163-datagram2/).
Datagrama2 adiciona resistência a replay e suporte a assinatura offline.
Datagrama3 é menor do que o antigo formato de datagrama, mas sem autenticação.


### BEP 15

Para referência, o fluxo de mensagens definido em [BEP 15](http://www.bittorrent.org/beps/bep_0015.html) é o seguinte:

```
Cliente                      Rastreador
    Req. de Conexão -------------->
      <-------------- Resp. de Conexão
    Req. de Anúncio -------------->
      <-------------- Resp. de Anúncio
    Req. de Anúncio -------------->
      <-------------- Resp. de Anúncio
```

A fase de conexão é necessária para evitar falsificação de endereços IP.
O rastreador retorna um ID de conexão que o cliente usa em anúncios subsequentes.
Esse ID de conexão expira por padrão em um minuto no cliente e em dois minutos no rastreador.

O I2P usará o mesmo fluxo de mensagens que o BEP 15, para facilidade de adoção em bases de código de clientes existentes compatíveis com UDP: por eficiência e por motivos de segurança discutidos abaixo:

```
Cliente                      Rastreador
    Req. de Conexão -------------->       (Datagrama Repliável2)
      <-------------- Resp. de Conexão   (Bruto)
    Req. de Anúncio ------------->      (Datagrama Repliável3)
      <-------------- Resp. de Anúncio  (Bruto)
    Req. de Anúncio ------------->      (Datagrama Repliável3)
      <-------------- Resp. de Anúncio  (Bruto)
             ...
```

Isso potencialmente fornece uma grande economia de largura de banda sobre anúncios por streaming (TCP).
Embora o Datagram2 tenha aproximadamente o mesmo tamanho de um SYN de streaming, a resposta bruta é muito menor que o SYN ACK de streaming.
As solicitações subsequentes usam Datagram3, e as respostas subsequentes são brutas.

As solicitações de anúncio são Datagram3 para que o rastreador não precise manter uma grande tabela de mapeamento de IDs de conexão para destino de anúncio ou hash.
Em vez disso, o rastreador pode gerar IDs de conexão criptograficamente a partir do hash do remetente, o carimbo de tempo atual (com base em algum intervalo) e um valor secreto.
Quando uma solicitação de anúncio é recebida, o rastreador valida o ID de conexão e então usa o hash do remetente do Datagram3 como o alvo de envio.


### Suporte ao Rastreador/Cliente

Para uma aplicação integrada (roteador e cliente em um único processo, como i2psnark e o plugin ZzzOT Java), ou para uma aplicação baseada em I2CP (por exemplo, BiglyBT), deve ser simples implementar e rotear o tráfego de streaming e datagrama separadamente.
Espera-se que ZzzOT e i2psnark sejam o primeiro rastreador e cliente a implementar esta proposta.

Rastreadores e clientes não integrados são discutidos abaixo.


Rastreadores
``````````

Existem quatro implementações conhecidas de rastreadores I2P:

- zzzot, um plugin Java de roteador integrado, rodando em opentracker.dg2.i2p e vários outros
- tracker2.postman.i2p, rodando presumivelmente atrás de um roteador Java e túnel HTTP Server
- O antigo C opentracker, portado por zzz, com suporte UDP comentado
- O novo C opentracker, portado por r4sas, rodando em opentracker.r4sas.i2p e possivelmente outros, rodando presumivelmente atrás de um roteador i2pd e túnel HTTP Server

Para uma aplicação de rastreador externo que atualmente usa um túnel de servidor HTTP para receber solicitações de anúncio, a implementação pode ser bastante difícil.
Um túnel especializado poderia ser desenvolvido para traduzir datagramas para solicitações/respostas HTTP locais.
Ou, um túnel especializado que trata tanto as solicitações HTTP quanto os datagramas poderia ser projetado para encaminhar os datagramas para o processo externo.
Essas decisões de design dependerão fortemente das implementações específicas do roteador e do rastreador, e estão fora do escopo desta proposta.


Clientes
```````
Clientes torrent baseados em SAM externo, como qbittorrent e outros clientes baseados em libtorrent, exigiriam SAM v3.3 [/en/docs/api/samv3/](/en/docs/api/samv3/) que não é suportada pelo i2pd.
Isso também é necessário para suporte a DHT, e é complexo o suficiente para que nenhum cliente torrent SAM conhecido tenha implementado.
Nenhuma implementação baseada em SAM para esta proposta é esperada em breve.


### Duração da Conexão

[BEP 15](http://www.bittorrent.org/beps/bep_0015.html) especifica que o ID de conexão expira em um minuto no cliente e em dois minutos no rastreador.
Isso não é configurável.
Isso limita os possíveis ganhos de eficiência, a menos que os clientes agrupem anúncios para fazer todos dentro de uma janela de um minuto.
i2psnark atualmente não agrupa anúncios; ele os espalha para evitar picos de tráfego.
Usuários avançados relatam estar executando milhares de torrents de uma só vez, e agrupar esse número de anúncios em um minuto não é realista.

Aqui, propomos estender a resposta de conexão para adicionar um campo opcional de duração da conexão.
O padrão, se não presente, é um minuto. Caso contrário, a duração especificada em segundos, deve ser usada pelo cliente, e o rastreador manterá o ID de conexão por mais um minuto.


### Compatibilidade com BEP 15

Este design mantém a compatibilidade com [BEP 15](http://www.bittorrent.org/beps/bep_0015.html) tanto quanto possível para limitar as mudanças necessárias em clientes e rastreadores existentes.

A única mudança obrigatória é o formato da informação de peer na resposta de anúncio.
A adição do campo de duração na resposta de conexão não é obrigatória, mas é fortemente recomendada para eficiência, conforme explicado acima.



### Análise de Segurança

Um objetivo importante de um protocolo de anúncio UDP é prevenir falsificação de endereços.
O cliente deve realmente existir e incorporar um leaseset real.
Ele deve ter túneis de entrada para receber a Resposta de Conexão.
Esses túneis poderiam ser de zero salto e construídos instantaneamente, mas isso exporia o criador.
Este protocolo alcança esse objetivo.



### Problemas

- Esta proposta não oferece suporte a destinos cegos, mas pode ser estendida para fazê-lo. Veja abaixo.




## Especificação

### Protocolos e Portas

O Datagram2 Repliável usa o protocolo I2CP 19;
o Datagram3 Repliável usa o protocolo I2CP 20;
datagramas brutos usam o protocolo I2CP 18.
As solicitações podem ser Datagram2 ou Datagram3. As respostas são sempre brutas.
O formato mais antigo do datagrama repliável ("Datagrama1") usando o protocolo I2CP 17 NÃO deve ser usado para solicitações ou respostas; estes devem ser descartados se recebidos nas portas de solicitação/resposta. Note que o protocolo Datagram1 17 ainda é usado para o protocolo DHT.

As solicitações usam o "to port" do I2CP da URL de anúncio; veja abaixo.
O "from port" da solicitação é escolhido pelo cliente, mas deve ser diferente de zero, e uma porta diferente das usadas por DHT, para que as respostas possam ser facilmente classificadas.
Os rastreadores devem rejeitar solicitações recebidas na porta errada.

As respostas usam o "to port" do I2CP da solicitação.
O "from port" da solicitação é o "to port" da solicitação.


### URL de Anúncio

O formato da URL de anúncio não é especificado em [BEP 15](http://www.bittorrent.org/beps/bep_0015.html), mas como no clearnet, URLs de anúncio UDP são da forma "udp://host:port/path".
O caminho é ignorado e pode estar vazio, mas é tipicamente "/announce" no clearnet.
A parte :port deve sempre estar presente, no entanto, se a parte ":port" for omitida, use uma porta I2CP padrão de 6969, pois essa é a porta comum no clearnet.
Pode haver também parâmetros cgi &a=b&c=d anexados, estes podem ser processados e fornecidos na solicitação de anúncio, veja [BEP 41](http://www.bittorrent.org/beps/bep_0041.html).
Se não houver parâmetros ou caminho, a barra final também pode ser omitida, conforme implícito em [BEP 41](http://www.bittorrent.org/beps/bep_0041.html).


### Formatos de Datagramas

Todos os valores são enviados na ordem de bytes de rede (big endian).
Não espere pacotes para serem exatamente de um certo tamanho.
Extensões futuras podem aumentar o tamanho dos pacotes.



Solicitud de Conexão
`````````````````

Cliente para rastreador.
16 bytes. Deve ser Datagram2 Repliável. Igual ao especificado em [BEP 15](http://www.bittorrent.org/beps/bep_0015.html). Sem alterações.


```
Offset  Size            Name            Value
  0       64-bit integer  protocol_id     0x41727101980 // constante mágica
  8       32-bit integer  action          0 // conectar
  12      32-bit integer  transaction_id
```



Resposta de Conexão
````````````````

Rastreador para cliente.
16 ou 18 bytes. Deve ser bruto. Igual ao especificado em [BEP 15](http://www.bittorrent.org/beps/bep_0015.html) exceto conforme observado abaixo.


```
Offset  Size            Name            Value
  0       32-bit integer  action          0 // conectar
  4       32-bit integer  transaction_id
  8       64-bit integer  connection_id
  16      16-bit integer  lifetime        opcional  // Alteração de BEP 15
```

A resposta DEVE ser enviada para o "to port" do I2CP que foi recebido como o "from port" da solicitação.

O campo de duração é opcional e indica o tempo de vida do ID de conexão do cliente em segundos.
O padrão é 60, e o mínimo, se especificado, é 60.
O máximo é 65535 ou cerca de 18 horas.
O rastreador deve manter o ID de conexão por 60 segundos a mais do que a duração do cliente.



Solicitud de Anúncio
````````````````

Cliente para rastreador.
98 bytes mínimos. Deve ser Datagram3 Repliável. Igual ao especificado em [BEP 15](http://www.bittorrent.org/beps/bep_0015.html) exceto conforme observado abaixo.

O ID de conexão é como recebido na resposta de conexão.



```
Offset  Size            Name            Value
  0       64-bit integer  connection_id
  8       32-bit integer  action          1     // anunciar
  12      32-bit integer  transaction_id
  16      20-byte string  info_hash
  36      20-byte string  peer_id
  56      64-bit integer  downloaded
  64      64-bit integer  left
  72      64-bit integer  uploaded
  80      32-bit integer  event           0     // 0: nenhum; 1: completado; 2: iniciado; 3: parado
  84      32-bit integer  IP address      0     // padrão
  88      32-bit integer  key
  92      32-bit integer  num_want        -1    // padrão
  96      16-bit integer  port
  98      varies          options     opcional  // Conforme especificado no BEP 41
```

Alterações de [BEP 15](http://www.bittorrent.org/beps/bep_0015.html):

- a chave é ignorada
- a porta provavelmente é ignorada
- A seção de opções, se presente, é conforme definido em [BEP 41](http://www.bittorrent.org/beps/bep_0041.html)

A resposta DEVE ser enviada para o "to port" do I2CP que foi recebido como o "from port" da solicitação.
Não use a porta da solicitação de anúncio.



Resposta de Anúncio
`````````````````

Rastreador para cliente.
20 bytes, no mínimo. Deve ser bruto. Igual ao especificado em [BEP 15](http://www.bittorrent.org/beps/bep_0015.html) exceto conforme observado abaixo.



```
Offset  Size            Name            Value
  0           32-bit integer  action          1 // anunciar
  4           32-bit integer  transaction_id
  8           32-bit integer  interval
  12          32-bit integer  leechers
  16          32-bit integer  seeders
  20   32 * n 32-byte hash    binary hashes     // Alteração de BEP 15
  ...                                           // Alteração de BEP 15
```

Alterações de [BEP 15](http://www.bittorrent.org/beps/bep_0015.html):

- Em vez de 6 bytes IPv4+porta ou 18 bytes IPv6+porta, retornamos
  múltiplos de respostas "compactas" de 32 bytes com os hashes binários SHA-256 dos peers.
  Como com respostas compactas TCP, não incluímos uma porta.

A resposta DEVE ser enviada para o "to port" do I2CP que foi recebido como o "from port" da solicitação.
Não use a porta da solicitação de anúncio.

Os datagramas I2P têm um tamanho máximo muito grande de cerca de 64 KB; no entanto, para entrega confiável, datagramas maiores que 4 KB devem ser evitados.
Para eficiência de largura de banda, os rastreadores provavelmente devem limitar o número máximo de peers para cerca de 50, o que corresponde a cerca de um pacote de 1600 bytes antes da sobrecarga em várias camadas, e deve estar dentro de um limite de carga de mensagem de dois túneis após a fragmentação.

Como no BEP 15, não há uma contagem incluída do número de endereços de peers (IP/porta para BEP 15, hashes aqui) a seguir.
Embora não contemplado no BEP 15, um marcador de final de peers de todos zeros poderia ser definido para indicar que a informação de peers está completa e alguns dados de extensão seguem.

Para que extensões sejam possíveis no futuro, os clientes devem ignorar um hash de 32 bytes de todos zeros, e qualquer dado que siga.
Os rastreadores devem rejeitar anúncios de um hash de todos zeros, embora esse hash já esteja banido por roteadores Java.


Scrape
``````

A solicitação/resposta de scrape de [BEP 15](http://www.bittorrent.org/beps/bep_0015.html) não é exigida por esta proposta, mas pode ser implementada, se desejado, sem alterações necessárias.
O cliente deve adquirir um ID de conexão primeiro.
A solicitação de scrape é sempre um Datagram3 repliável.
A resposta de scrape é sempre bruta.



Resposta de Erro
``````````````

Rastreador para cliente.
8 bytes, no mínimo (se a mensagem estiver vazia).
Deve ser bruto. Igual ao especificado em [BEP 15](http://www.bittorrent.org/beps/bep_0015.html). Sem alterações.

```

Offset  Size            Name            Value
  0       32-bit integer  action          3 // erro
  4       32-bit integer  transaction_id
  8       string          message

```



## Extensões

Bits de extensão ou um campo de versão não estão incluídos.
Clientes e rastreadores não devem assumir pacotes de um tamanho específico.
Dessa forma, campos adicionais podem ser adicionados sem quebrar a compatibilidade.
O formato de extensões definido em [BEP 41](http://www.bittorrent.org/beps/bep_0041.html) é recomendado se necessário.

A resposta de conexão é modificada para adicionar uma duração de ID de conexão opcional.

Se o suporte a destinos cegos for necessário, podemos ou adicionar o endereço cego de 35 bytes ao final da solicitação de anúncio, ou solicitar hashes cegas nas respostas, usando o formato [BEP 41](http://www.bittorrent.org/beps/bep_0041.html) (parâmetros a serem determinados).
O conjunto de endereços de peers cegos de 35 bytes pode ser adicionado ao final da resposta de anúncio após um hash de 32 bytes de todos zeros.



## Diretrizes de Implementação

Ver a seção de design acima para uma discussão dos desafios para clientes e rastreadores não integrados, não I2CP.


### Clientes

Para um determinado hostname de rastreador, um cliente deve preferir URLs UDP sobre URLs HTTP, e não deve anunciar para ambos.

Clientes com suporte BEP 15 existente devem requerer apenas pequenas modificações.

Se um cliente suportar DHT ou outros protocolos de datagrama, ele deve provavelmente selecionar uma porta diferente como o "from port" da solicitação para que as respostas retornem para essa porta e não sejam confundidas com mensagens DHT.
O cliente só recebe datagramas brutos como respostas.
Os rastreadores nunca enviarão um datagrama repliável2 para o cliente.

Clientes com uma lista padrão de opentrackers devem atualizar a lista para adicionar URLs UDP após os opentrackers conhecidos serem conhecidos por suportar UDP.

Clientes podem ou não implementar retransmissão de solicitações.
Retransmissões, se implementadas, devem usar um tempo de espera inicial de pelo menos 15 segundos, e dobrar o tempo de espera para cada retransmissão (retardo exponencial).

Clientes devem dar um tempo após receber uma resposta de erro.


### Rastreadores

Rastreadores com suporte BEP 15 existente devem requerer apenas pequenas modificações.
Esta proposta difere da proposta de 2014, pois o rastreador deve suportar a recepção de datagrama2 repliável e datagrama3 na mesma porta.

Para minimizar os requisitos de recursos do rastreador, este protocolo é projetado para eliminar qualquer requisito de que o rastreador armazene mapeamentos de hashes de cliente para IDs de conexão para validação posterior.
Isso é possível porque o pacote de solicitação de anúncio é um pacote Datagram3 repliável, por isso contém o hash do remetente.

Uma implementação recomendada é:

- Defina a época atual como o tempo atual com uma resolução da duração da conexão, ``epoch = now / lifetime``.
- Defina uma função de hash criptográfica ``H(secret, clienthash, epoch)`` que gera uma saída de 8 bytes.
- Gere a constante secreta aleatória usada para todas as conexões.
- Para respostas de conexão, gere ``connection_id = H(secret,  clienthash, epoch)``
- Para solicitações de anúncio, valide o ID de conexão recebido na época atual verificando ``connection_id == H(secret, clienthash, epoch) || connection_id == H(secret, clienthash, epoch - 1)``


## Migração

Clientes existentes não suportam URLs de anúncio UDP e os ignoram.

Rastreadores existentes não suportam a recepção de datagramas repliáveis ou brutos, eles serão descartados.

Esta proposta é completamente opcional. Nem clientes nem rastreadores são obrigados a implementá-la em qualquer momento.



## Implementação

Espera-se que as primeiras implementações sejam no ZzzOT e i2psnark.
Elas serão usadas para teste e verificação desta proposta.

Outras implementações seguirão conforme desejado após a conclusão dos testes e verificação.




