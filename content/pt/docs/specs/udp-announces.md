---
title: "Anúncios UDP do BitTorrent"
description: "Especificação do protocolo para mensagens announce (requisições de anúncio ao tracker) do tracker BitTorrent baseadas em UDP no I2P"
slug: "udp-announces"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

## Visão geral

Esta especificação documenta o protocolo para mensagens announce UDP do BitTorrent no I2P (announce: solicitação do cliente ao tracker). Para a especificação geral do BitTorrent no I2P, consulte a [documentação do BitTorrent via I2P](/docs/applications/bittorrent/). Para contexto e informações adicionais sobre o desenvolvimento desta especificação, consulte a [Proposta 160](/proposals/160-udp-trackers/).

Este protocolo foi formalmente aprovado em 24 de junho de 2025 e implementado na versão 2.10.0 do I2P (API 0.9.67), lançada em 8 de setembro de 2025. O suporte ao rastreador UDP está atualmente operacional na rede I2P, com múltiplos rastreadores em produção e suporte completo no cliente i2psnark.

## Arquitetura

Esta especificação usa datagram2 com possibilidade de resposta, datagram3 com possibilidade de resposta e datagramas brutos, conforme definidos na [I2P Datagram Specification](/docs/api/datagrams/). Datagram2 e Datagram3 são variantes de datagramas com possibilidade de resposta, definidas na [Proposal 163](/proposals/163-datagram2/). O Datagram2 adiciona resistência a ataques de repetição e suporte a assinatura offline. O Datagram3 é menor que o formato antigo de datagrama, porém sem autenticação.

### BEP 15

Para referência, o fluxo de mensagens definido no [BEP 15](http://www.bittorrent.org/beps/bep_0015.html) é o seguinte:

```
Client                        Tracker
  Connect Req. ------------->
    <-------------- Connect Resp.
  Announce Req. ------------->
    <-------------- Announce Resp.
  Announce Req. ------------->
    <-------------- Announce Resp.
```
A fase de conexão é necessária para evitar a falsificação de endereços IP. O rastreador retorna um ID de conexão que o cliente usa em anúncios subsequentes. Esse ID de conexão expira, por padrão, em um minuto no cliente e em dois minutos no rastreador.

I2P usa o mesmo fluxo de mensagens que o BEP 15, para facilitar a adoção em bases de código de clientes com suporte a UDP, por questões de eficiência, e por razões de segurança discutidas abaixo:

```
Client                        Tracker
  Connect Req. ------------->       (Repliable Datagram2)
    <-------------- Connect Resp.   (Raw)
  Announce Req. ------------->      (Repliable Datagram3)
    <-------------- Announce Resp.  (Raw)
  Announce Req. ------------->      (Repliable Datagram3)
    <-------------- Announce Resp.  (Raw)
           ...
```
Isso pode proporcionar uma grande economia de largura de banda em relação a anúncios via streaming (TCP). Embora o Datagram2 tenha aproximadamente o mesmo tamanho que um SYN de streaming, a resposta bruta é muito menor do que o SYN ACK de streaming. As solicitações subsequentes usam o Datagram3, e as respostas subsequentes são brutas.

As solicitações de anúncio são Datagram3 (formato de datagrama v3), de modo que o rastreador não precise manter uma grande tabela de mapeamento de IDs de conexão para destino de anúncio ou hash. Em vez disso, o rastreador pode gerar IDs de conexão criptograficamente a partir do hash do remetente, do carimbo de data/hora atual (com base em algum intervalo) e de um valor secreto. Quando uma solicitação de anúncio é recebida, o rastreador valida o ID de conexão e então usa o hash do remetente do Datagram3 como o destino de envio.

### Duração da conexão

[BEP 15](http://www.bittorrent.org/beps/bep_0015.html) especifica que o ID de conexão expira em um minuto no cliente e em dois minutos no rastreador. Isso não é configurável. Isso limita os ganhos potenciais de eficiência, a menos que os clientes agrupem as operações "announce" (requisições do BitTorrent ao rastreador) para realizar todas dentro de uma janela de um minuto. O i2psnark atualmente não agrupa as operações "announce"; ele as distribui para evitar picos de tráfego. Há relatos de que usuários avançados executam milhares de torrents ao mesmo tempo, e concentrar tantas operações "announce" em um único minuto não é realista.

Aqui, propomos estender a resposta de conexão para adicionar um campo opcional de tempo de vida da conexão. O padrão, caso o campo não esteja presente, é de um minuto. Caso contrário, o tempo de vida especificado em segundos deverá ser usado pelo cliente, e o rastreador manterá o ID da conexão por mais um minuto.

### Compatibilidade com o BEP 15

Este design mantém a compatibilidade com [BEP 15](http://www.bittorrent.org/beps/bep_0015.html) tanto quanto possível para limitar as mudanças necessárias nos clientes e rastreadores existentes.

A única alteração necessária é o formato das informações do par na resposta de anúncio. A adição do campo de tempo de vida na resposta de conexão não é necessária, mas é fortemente recomendada por questões de eficiência, conforme explicado acima.

### Análise de Segurança

Um objetivo importante de um protocolo de anúncio UDP é impedir a falsificação de endereços. O cliente deve de fato existir e incluir um leaseSet real. Ele deve ter tunnels de entrada para receber a Resposta de Conexão. Esses tunnels poderiam ser zero-hop e construídos instantaneamente, mas isso exporia o criador. Este protocolo cumpre esse objetivo.

### Problemas

Este protocolo não oferece suporte a blinded destinations (destinos ofuscados), mas pode ser estendido para fazê-lo. Veja abaixo.

## Especificação

### Protocolos e Portas

O Datagram2 replicável usa o protocolo I2CP 19; o Datagram3 replicável usa o protocolo I2CP 20; datagramas brutos usam o protocolo I2CP 18. As solicitações podem ser Datagram2 ou Datagram3. As respostas são sempre datagramas brutos. O formato mais antigo de datagrama replicável ("Datagram1"), que usa o protocolo I2CP 17, NÃO deve ser usado para solicitações ou respostas; estes devem ser descartados se recebidos nas portas de solicitação/resposta. Observe que o Datagram1, protocolo 17, ainda é usado pelo protocolo DHT.

As requisições usam o I2CP "to port" da URL de anúncio; veja abaixo. O "from port" da requisição é escolhido pelo cliente, mas deve ser diferente de zero e distinto das portas usadas pela DHT (tabela hash distribuída), para que as respostas possam ser classificadas facilmente. Os rastreadores devem rejeitar requisições recebidas na porta errada.

As respostas usam o "to port" do I2CP da solicitação. O "from port" da resposta é o "to port" da solicitação.

### URL de anúncio

O formato da URL de announce não é especificado no [BEP 15](http://www.bittorrent.org/beps/bep_0015.html), mas, como na clearnet (internet pública), URLs de announce UDP têm a forma "udp://host:port/path". O caminho é ignorado e pode estar vazio, mas é tipicamente "/announce" na clearnet. A parte :port deve estar sempre presente; entretanto, se a parte ":port" for omitida, use 6969 como porta I2CP padrão, já que essa é a porta comum na clearnet. Também podem ser anexados parâmetros CGI &a=b&c=d; eles podem ser processados e fornecidos na requisição de announce, veja [BEP 41](http://www.bittorrent.org/beps/bep_0041.html). Se não houver parâmetros ou caminho, a barra final / também pode ser omitida, como implícito no [BEP 41](http://www.bittorrent.org/beps/bep_0041.html).

### Formatos de Datagramas

Todos os valores são enviados em ordem de bytes de rede (big-endian). Não espere que os pacotes tenham exatamente um determinado tamanho. Extensões futuras podem aumentar o tamanho dos pacotes.

#### Solicitação de conexão

Do cliente para o tracker. 16 bytes. Deve ser um Datagram2 repliable (permite resposta). Igual ao [BEP 15](http://www.bittorrent.org/beps/bep_0015.html). Sem alterações.

```
Offset  Size            Name            Value
0       64-bit integer  protocol_id     0x41727101980 // magic constant
8       32-bit integer  action          0 // connect
12      32-bit integer  transaction_id
```
#### Resposta de Conexão

Do rastreador para o cliente. 16 ou 18 bytes. Deve estar em formato bruto. Igual ao definido no [BEP 15](http://www.bittorrent.org/beps/bep_0015.html), exceto conforme indicado abaixo.

```
Offset  Size            Name            Value
0       32-bit integer  action          0 // connect
4       32-bit integer  transaction_id
8       64-bit integer  connection_id
16      16-bit integer  lifetime        optional  // Change from BEP 15
```
A resposta DEVE ser enviada para o "to port" do I2CP que foi recebido como o "from port" da solicitação.

O campo lifetime é opcional e indica o tempo de vida do connection_id do cliente em segundos. O padrão é 60, e o mínimo, se especificado, é 60. O máximo é 65535 ou cerca de 18 horas. O rastreador deve manter o connection_id por 60 segundos a mais do que o tempo de vida do cliente.

#### Solicitação de anúncio

Cliente para o tracker. 98 bytes no mínimo. Deve ser um Datagram3 com possibilidade de resposta. Igual ao descrito em [BEP 15](http://www.bittorrent.org/beps/bep_0015.html) exceto conforme observado abaixo.

O connection_id é o mesmo que o recebido na resposta de conexão.

```
Offset  Size            Name            Value
0       64-bit integer  connection_id
8       32-bit integer  action          1     // announce
12      32-bit integer  transaction_id
16      20-byte string  info_hash
36      20-byte string  peer_id
56      64-bit integer  downloaded
64      64-bit integer  left
72      64-bit integer  uploaded
80      32-bit integer  event           0     // 0: none; 1: completed; 2: started; 3: stopped
84      32-bit integer  IP address      0     // default, unused in I2P
88      32-bit integer  key
92      32-bit integer  num_want        -1    // default
96      16-bit integer  port                  // must be same as I2CP from port
98      varies          options     optional  // As specified in BEP 41
```
Alterações em relação ao [BEP 15](http://www.bittorrent.org/beps/bep_0015.html):

- key é ignorado
- O endereço IP não é utilizado
- a porta provavelmente é ignorada, mas deve ser a mesma que o I2CP from port
- A seção de opções, se presente, é definida conforme [BEP 41](http://www.bittorrent.org/beps/bep_0041.html)

A resposta DEVE ser enviada ao "to port" do I2CP que foi recebido como o "from port" da requisição. Não use a porta da requisição de anúncio.

#### Resposta de Anúncio

Do rastreador para o cliente. Mínimo de 20 bytes. Deve ser em bruto. Igual ao [BEP 15](http://www.bittorrent.org/beps/bep_0015.html), exceto conforme observado abaixo.

```
Offset  Size            Name            Value
0           32-bit integer  action          1 // announce
4           32-bit integer  transaction_id
8           32-bit integer  interval
12          32-bit integer  leechers
16          32-bit integer  seeders
20   32 * n 32-byte hash    binary hashes     // Change from BEP 15
...                                           // Change from BEP 15
```
Alterações em relação ao [BEP 15](http://www.bittorrent.org/beps/bep_0015.html):

- Em vez de IPv4+porta de 6 bytes ou IPv6+porta de 18 bytes, retornamos um número múltiplo de "respostas compactas" de 32 bytes com os hashes SHA-256 binários dos pares. Como nas respostas compactas TCP, não incluímos uma porta.

A resposta DEVE ser enviada ao I2CP "to port" que foi recebido como o "from port" da solicitação. Não use a porta da solicitação de anúncio.

Os datagramas do I2P têm um tamanho máximo muito grande, de cerca de 64 KB; no entanto, para entrega confiável, é recomendável evitar datagramas maiores que 4 KB. Por eficiência de banda, os rastreadores provavelmente devem limitar o número máximo de pares a cerca de 50, o que corresponde a um pacote de aproximadamente 1600 bytes antes da sobrecarga em várias camadas, e deve ficar dentro do limite de carga útil de uma mensagem que percorre dois tunnel após a fragmentação.

Como no BEP 15, não há uma contagem incluída do número de endereços de pares (IP/porta no BEP 15, hashes aqui) a seguir. Embora não contemplado no BEP 15, poderia ser definido um marcador de fim de pares composto apenas por zeros para indicar que as informações dos pares estão completas e que alguns dados de extensão seguem.

Para que essa extensão seja possível no futuro, os clientes devem ignorar um hash de 32 bytes composto apenas por zeros, e quaisquer dados que vierem depois. Os rastreadores devem rejeitar anúncios provenientes de um hash composto apenas por zeros, embora esse hash já seja banido pelos Java routers.

#### Raspagem

A requisição/resposta de scrape (consulta ao tracker por estatísticas) de [BEP 15](http://www.bittorrent.org/beps/bep_0015.html) não é exigida por esta especificação, mas pode ser implementada se desejado, sem necessidade de alterações. O cliente deve obter um ID de conexão primeiro. A requisição de scrape é sempre um Datagram3 repliable. A resposta de scrape é sempre raw.

#### Resposta de erro

Do rastreador para o cliente. Mínimo de 8 bytes (se a mensagem estiver vazia). Deve ser em formato bruto. O mesmo que em [BEP 15](http://www.bittorrent.org/beps/bep_0015.html). Sem alterações.

```
Offset  Size            Name            Value
0       32-bit integer  action          3 // error
4       32-bit integer  transaction_id
8       string          message
```
## Extensões

Bits de extensão ou um campo de versão não estão incluídos. Clientes e trackers não devem assumir que os pacotes têm um tamanho específico. Dessa forma, campos adicionais podem ser adicionados sem comprometer a compatibilidade. O formato de extensões definido em [BEP 41](http://www.bittorrent.org/beps/bep_0041.html) é recomendado, se necessário.

A resposta de conexão é modificada para incluir um tempo de vida opcional do ID de conexão.

Se for necessário suporte a blinded destination (destino cego), podemos ou adicionar o endereço cego de 35 bytes ao final da requisição announce, ou solicitar hashes cegos nas respostas, usando o formato [BEP 41](http://www.bittorrent.org/beps/bep_0041.html) (parâmetros a definir). O conjunto de endereços de pares cegos de 35 bytes poderia ser acrescentado ao final da resposta announce, após um hash de 32 bytes composto apenas por zeros.

## Diretrizes de Implementação

Consulte a seção de design acima para uma discussão sobre os desafios enfrentados por clientes e rastreadores não integrados e que não usam I2CP.

### Clientes

Para um determinado nome de host do rastreador, um cliente deve preferir URLs UDP a URLs HTTP e não deve anunciar a ambos.

Clientes com suporte existente ao BEP 15 (proposta de melhoria do BitTorrent 15) devem necessitar apenas de pequenas modificações.

Se um cliente oferecer suporte a DHT ou a outros protocolos de datagrama, provavelmente deve selecionar uma porta diferente como a "from port" da solicitação, para que as respostas cheguem de volta a essa porta e não se confundam com mensagens do DHT. O cliente só recebe datagramas brutos como respostas. Os rastreadores nunca enviarão um repliable datagram2 (datagrama ao qual é possível responder) ao cliente.

Clientes com uma lista predefinida de trackers abertos devem atualizar a lista para adicionar URLs UDP depois de se confirmar que os trackers abertos conhecidos suportam UDP.

Os clientes podem ou não implementar retransmissão de solicitações. As retransmissões, se implementadas, devem usar um tempo limite inicial de pelo menos 15 segundos e dobrar o tempo limite a cada retransmissão (backoff exponencial).

Os clientes devem fazer back off (aguardar e reduzir a taxa antes de tentar novamente) após receber uma resposta de erro.

### Rastreadores

Rastreadores com suporte existente a BEP 15 deveriam exigir apenas pequenas modificações. Esta especificação difere da proposta de 2014, pois o rastreador deve suportar a recepção de datagram2 (datagrama versão 2) e datagram3 (datagrama versão 3) com capacidade de resposta na mesma porta.

Para minimizar os requisitos de recursos do rastreador, este protocolo foi projetado para eliminar qualquer necessidade de que o rastreador armazene mapeamentos de hashes de cliente para IDs de conexão para validação posterior. Isso é possível porque o pacote de solicitação de announce é um pacote Datagram3 (formato de datagrama do I2P) com possibilidade de resposta, portanto contém o hash do remetente.

Uma implementação recomendada é:

- Defina a epoch (época de tempo) atual como o tempo atual com resolução igual ao tempo de vida da conexão, `epoch = now / lifetime`.
- Defina uma função hash criptográfica `H(secret, clienthash, epoch)` que gera uma saída de 8 bytes.
- Gere o segredo constante aleatório usado para todas as conexões.
- Para respostas de conexão, gere `connection_id = H(secret, clienthash, epoch)`
- Para solicitações de anúncio, valide o ID de conexão recebido na epoch atual verificando `connection_id == H(secret, clienthash, epoch) || connection_id == H(secret, clienthash, epoch - 1)`

## Estado da implantação

Este protocolo foi aprovado em 24 de junho de 2025 e está plenamente operacional na rede I2P desde setembro de 2025.

### Implementações atuais

**i2psnark**: O suporte completo a rastreadores UDP está incluído no I2P versão 2.10.0 (API 0.9.67), lançado em 8 de setembro de 2025. Todas as instalações do I2P a partir desta versão incluem suporte a rastreadores UDP por padrão.

**zzzot tracker**: A partir da versão 0.20.0-beta2, há suporte a announce (anúncio do cliente ao rastreador) via UDP. Em outubro de 2025, os seguintes rastreadores de produção estão operacionais: - opentracker.dg2.i2p - opentracker.simp.i2p - opentracker.skank.i2p

### Notas de compatibilidade do cliente

**Limitações do SAM v3.3**: Clientes externos de BitTorrent que usam SAM (Simple Anonymous Messaging) exigem suporte ao SAM v3.3 para Datagram2/3. Isso está disponível no Java I2P, mas não é atualmente suportado pelo i2pd (a implementação de I2P em C++), o que pode limitar a adoção em clientes baseados em libtorrent (biblioteca BitTorrent em C++) como o qBittorrent.

**Clientes I2CP**: Clientes que usam I2CP diretamente (como o BiglyBT) podem implementar suporte a trackers UDP sem as limitações do SAM.

## Referências

- **[BEP15]**: [Protocolo de Tracker UDP do BitTorrent](http://www.bittorrent.org/beps/bep_0015.html)
- **[BEP41]**: [Extensões do Protocolo de Tracker UDP](http://www.bittorrent.org/beps/bep_0041.html)
- **[DATAGRAMS]**: [Especificação de Datagramas do I2P](/docs/api/datagrams/)
- **[Prop160]**: [Proposta de Trackers UDP](/proposals/160-udp-trackers/)
- **[Prop163]**: [Proposta do Datagram2](/proposals/163-datagram2/)
- **[SPEC]**: [BitTorrent sobre I2P](/docs/applications/bittorrent/)
