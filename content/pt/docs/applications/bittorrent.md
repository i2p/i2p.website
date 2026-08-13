---
title: "Bittorrent sobre I2P"
description: "Especificações de protocolo para clientes BitTorrent e trackers no I2P"
slug: "bittorrent"
lastUpdated: "2026-08"
accurateFor: "0.9.70"
---

Existem vários clientes e trackers de bittorrent no I2P. Como o endereçamento I2P usa um Destination em vez de um IP e porta, pequenas alterações são necessárias no software de tracker e cliente para operação no I2P. Essas alterações são especificadas abaixo. Observe cuidadosamente as diretrizes para compatibilidade com clientes e trackers I2P mais antigos.

Esta página especifica detalhes de protocolo comuns a todos os clientes e trackers. Clientes e trackers específicos podem implementar outros recursos ou protocolos únicos.

Damos as boas-vindas a portes adicionais de software de cliente e tracker para I2P.

---

## Orientações Gerais para Desenvolvedores

A maioria dos clientes bittorrent não-Java se conectarão ao I2P via [SAMv3](/docs/api/samv3/). As sessões SAM (ou dentro do I2P, pools de tunnel ou conjuntos de tunnels) são projetadas para ter longa duração. A maioria dos clientes bittorrent precisará apenas de uma sessão, criada na inicialização e fechada na saída. O I2P é diferente do Tor, onde circuitos podem ser rapidamente criados e descartados. Pense cuidadosamente e consulte os desenvolvedores do I2P antes de projetar sua aplicação para usar mais de uma ou duas sessões simultâneas, ou para criá-las e descartá-las rapidamente. Os clientes bittorrent não devem criar uma sessão única para cada conexão. Projete seu cliente para usar a mesma sessão para anúncios e conexões de cliente.

Além disso, certifique-se de que as configurações do seu cliente (e orientações aos usuários sobre configurações do router, ou padrões do router se você incluir um router) resultem em seus usuários contribuindo com mais recursos para a rede do que consomem. I2P é uma rede peer-to-peer, e a rede não pode sobreviver se uma aplicação popular levar a rede a um congestionamento permanente.

Não forneça suporte para bittorrent através de um outproxy I2P para a clearnet, pois provavelmente será bloqueado. Consulte os operadores de outproxy para orientação.

As implementações de router Java I2P e i2pd são independentes e têm pequenas diferenças no comportamento, suporte a recursos e configurações padrão. Por favor, teste sua aplicação com a versão mais recente de ambos os routers.

O SAM do i2pd está habilitado por padrão; o SAM do Java I2P não está. Forneça instruções aos seus usuários sobre como habilitar o SAM no Java I2P (via /configclients no console do router), e/ou forneça uma boa mensagem de erro ao usuário se a conexão inicial falhar, por exemplo "certifique-se de que o I2P está rodando e a interface SAM está habilitada".

Os routers Java I2P e i2pd têm padrões diferentes para quantidades de tunnel. O padrão do Java é 2 e o padrão do i2pd é 5. Para a maioria dos cenários de largura de banda baixa a média e contagens de conexão baixas a médias, 3 é suficiente. Por favor, especifique a quantidade de tunnel na mensagem SESSION CREATE para obter desempenho consistente com os routers Java I2P e i2pd.

O I2P suporta múltiplos tipos de assinatura e criptografia. Para compatibilidade, o I2P usa por padrão tipos antigos e ineficientes, então todos os clientes devem especificar tipos mais novos.

Se estiver usando SAM, o tipo de assinatura é especificado nos comandos DEST GENERATE e SESSION CREATE (para transiente). Todos os clientes devem definir SIGNATURE_TYPE=7 (Ed25519).

O tipo de encriptação é especificado no comando SAM SESSION CREATE ou nas opções i2cp. Vários tipos de encriptação são permitidos. Alguns trackers suportam ECIES-X25519, alguns suportam ElGamal, e alguns suportam ambos. Os clientes devem definir i2cp.leaseSetEncType=4,0 (para ECIES-X25519 e ElGamal) para que possam conectar-se a ambos.

O suporte DHT requer SAMv3.3 PRIMARY e SUBSESSIONS para TCP e UDP na mesma sessão. Isso exigirá um esforço substancial de desenvolvimento no lado do cliente, a menos que o cliente seja escrito em Java. O i2pd atualmente não suporta SAMv3.3. O libtorrent atualmente não suporta SAMv3.3.

Sem suporte a DHT, você pode desejar anunciar automaticamente para uma lista configurável de rastreadores abertos conhecidos para que os links magnéticos funcionem. Consulte os usuários do I2P para obter informações sobre rastreadores abertos atualmente ativos e mantenha seus padrões atualizados. O suporte à extensão i2p_pex também ajudará a aliviar a falta de suporte a DHT.

Para mais orientação aos desenvolvedores sobre como garantir que sua aplicação use apenas os recursos necessários, consulte a [especificação SAMv3](/docs/api/samv3/) e [nosso guia para incluir I2P em sua aplicação](/docs/applications/embedding/). Entre em contato com os desenvolvedores do I2P ou i2pd para assistência adicional.

---

## Anúncios

Os clientes geralmente incluem um parâmetro falso port=6881 no anúncio, para compatibilidade com trackers mais antigos. Os trackers podem ignorar o parâmetro de porta e não devem exigi-lo.

O parâmetro ip é a base 64 do [Destination](/docs/specs/common-structures/#struct_Destination) do cliente, usando o alfabeto Base 64 do I2P [A-Z][a-z][0-9]-~. [Destinations](/docs/specs/common-structures/#struct_Destination) têm 387+ bytes, então a Base 64 tem 516+ bytes. Clientes geralmente anexam ".i2p" ao Destination Base 64 para compatibilidade com trackers mais antigos. Trackers não devem exigir um ".i2p" anexado.

Os outros parâmetros são os mesmos do bittorrent padrão.

Os Destinations atuais para clientes têm 387 ou mais bytes (516 ou mais na codificação Base 64). Um máximo razoável para assumir, por enquanto, é 475 bytes. Como o tracker deve decodificar o Base64 para fornecer respostas compactas (veja abaixo), o tracker provavelmente deveria decodificar e rejeitar Base64 inválido quando anunciado.

O tipo de resposta padrão é não-compacto. Os clientes podem solicitar uma resposta compacta com o parâmetro compact=1. Um tracker pode, mas não é obrigatório, retornar uma resposta compacta quando solicitado. Nota: Todos os trackers populares agora suportam respostas compactas e pelo menos um exige compact=1 no anúncio. Todos os clientes devem solicitar e suportar respostas compactas.

Desenvolvedores de novos clientes I2P são fortemente encorajados a implementar anúncios através do seu próprio tunnel em vez do proxy cliente HTTP na porta 4444. Fazer isso é tanto mais eficiente quanto permite a aplicação de destino pelo tracker (veja abaixo).

A especificação para anúncios UDP foi finalizada em 2025-06. O suporte em vários clientes I2P e trackers será implementado ao longo de 2025. Veja abaixo para informações adicionais.

---

## Respostas de Tracker Não-Compactas

Nota: Descontinuado. Todos os trackers populares agora suportam respostas compactas e pelo menos um requer compact=1 no anúncio. Todos os clientes devem solicitar e suportar respostas compactas.

A resposta não-compacta é igual ao BitTorrent padrão, com um "ip" I2P. Esta é uma longa "string DNS" codificada em base64, provavelmente com um sufixo ".i2p".

Trackers geralmente incluem uma chave de porta falsa, ou usam a porta do anúncio, para compatibilidade com clientes mais antigos. Clientes devem ignorar o parâmetro de porta, e não devem exigi-lo.

O valor da chave ip é o base 64 do [Destination](/docs/specs/common-structures/#struct_Destination) do cliente, como descrito acima. Os trackers geralmente anexam ".i2p" ao Destination Base 64 se não estava no ip do announce, para compatibilidade com clientes mais antigos. Os clientes não devem exigir um ".i2p" anexado nas respostas.

Outras chaves e valores de resposta são os mesmos do BitTorrent padrão.

---

## Respostas Compactas do Tracker

Na resposta compacta, o valor da chave do dicionário "peers" é uma única string de bytes, cujo comprimento é um múltiplo de 32 bytes. Esta string contém os [Hashes SHA-256 de 32 bytes](/docs/specs/common-structures/#type_Hash) concatenados das [Destinations](/docs/specs/common-structures/#struct_Destination) binárias dos peers. Este hash deve ser computado pelo tracker, a menos que a imposição de destination (veja abaixo) seja usada, caso em que o hash entregue nos cabeçalhos HTTP X-I2P-DestHash ou X-I2P-DestB32 pode ser convertido para binário e armazenado. A chave peers pode estar ausente, ou o valor peers pode ter comprimento zero.

Embora o suporte a respostas compactas seja opcional tanto para clientes quanto para trackers, é altamente recomendado, pois reduz o tamanho nominal da resposta em mais de 90%.

---

## Aplicação de Destino

Alguns, mas não todos, os clientes bittorrent I2P fazem anúncios através dos seus próprios tunnels. Os trackers podem optar por prevenir spoofing exigindo isso e verificando o [Destination](/docs/specs/common-structures/#struct_Destination) do cliente usando cabeçalhos HTTP adicionados pelo tunnel I2PTunnel HTTP Server. Os cabeçalhos são X-I2P-DestHash, X-I2P-DestB64 e X-I2P-DestB32, que são formatos diferentes para a mesma informação. Estes cabeçalhos não podem ser falsificados pelo cliente. Um tracker que exige destinations não precisa requerer o parâmetro de anúncio ip de forma alguma.

Como vários clientes usam o proxy HTTP em vez de seu próprio tunnel para anúncios, a aplicação de destino impedirá o uso por esses clientes, a menos que ou até que esses clientes sejam convertidos para anunciar através de seu próprio tunnel.

Infelizmente, à medida que a rede cresce, a quantidade de malícia também aumentará, então esperamos que todos os trackers eventualmente imponham destinos. Tanto os desenvolvedores de trackers quanto os de clientes devem antecipar isso.

---

## Anunciar Nomes de Host

Os nomes de host das URLs de anúncio em arquivos torrent geralmente seguem os [padrões de nomenclatura do I2P](/docs/overview/naming/). Além dos nomes de host dos livros de endereços e nomes de host Base 32 ".b32.i2p", o Destination Base 64 completo (com ou sem ".i2p" anexado) deve ser suportado. Trackers não-abertos devem reconhecer seu próprio nome de host em qualquer um desses formatos.

Para preservar o anonimato, os clientes geralmente devem ignorar URLs de anúncio não-I2P em arquivos torrent.

---

## Conexões de Cliente

As conexões cliente-para-cliente usam o protocolo padrão sobre TCP. Não há clientes I2P conhecidos que atualmente suportem comunicação uTP.

O I2P utiliza [Destinations](/docs/specs/common-structures/#struct_Destination) de 387+ bytes para endereços, como explicado acima.

Se o cliente tiver apenas o hash do destino (como de uma resposta compacta ou PEX), ele deve realizar uma busca codificando-o com Base 32, anexando ".b32.i2p", e consultando o Serviço de Nomeação, que retornará o Destination completo se disponível.

Se o cliente tiver o Destination completo de um peer que recebeu em uma resposta não-compacta, deve usá-lo diretamente na configuração da conexão. Não converta um Destination de volta para um hash Base 32 para consulta, isso é bastante ineficiente.

---

## Prevenção Entre Redes

Para preservar o anonimato, os clientes bittorrent I2P geralmente não suportam anúncios ou conexões de peers não-I2P. Os outproxies HTTP I2P frequentemente bloqueiam anúncios. Não há outproxies SOCKS conhecidos que suportem tráfego bittorrent.

Para prevenir o uso por clientes não-I2P através de um inproxy HTTP, os trackers I2P frequentemente bloqueiam acessos ou anúncios que contenham um cabeçalho HTTP X-Forwarded-For. Os trackers devem rejeitar anúncios de rede padrão com IPs IPv4 ou IPv6, e não entregá-los nas respostas.

---

## PEX

O I2P PEX é baseado no ut_pex. Como não parece haver uma especificação formal do ut_pex disponível, pode ser necessário revisar o código-fonte do libtorrent para assistência. É uma mensagem de extensão, identificada como "i2p_pex" no [handshake de extensão](http://www.bittorrent.org/beps/bep_0010.html). Contém um dicionário bencoded com até 3 chaves: "added", "added.f" e "dropped". Os valores added e dropped são cada um uma string de byte única, cujo comprimento é um múltiplo de 32 bytes. Essas strings de bytes são os hashes SHA-256 concatenados dos [Destinations](/docs/specs/common-structures/#struct_Destination) binários dos peers. Este é o mesmo formato que o valor do dicionário peers no formato de resposta compacta i2p especificado acima. O valor added.f, se presente, é o mesmo que no ut_pex.

---

## DHT

O suporte DHT está incluído no cliente i2psnark a partir da versão 0.9.2. As diferenças preliminares do [BEP 5](http://www.bittorrent.org/beps/bep_0005.html) são descritas abaixo e estão sujeitas a alterações. Entre em contato com os desenvolvedores do I2P se desejar desenvolver um cliente que suporte DHT.

Ao contrário do DHT padrão, o I2P DHT não usa um bit no handshake de opções, ou a mensagem PORT. É anunciado com uma mensagem de extensão, identificada como "i2p_dht" no [handshake de extensão](http://www.bittorrent.org/beps/bep_0010.html). Contém um dicionário bencoded com duas chaves, "port" e "rport", ambas números inteiros.

A porta UDP (datagrama) listada nas informações compactas do nó é usada para receber datagramas respondíveis (assinados). Isso é usado para consultas, exceto para anúncios. Chamamos isso de "porta de consulta". Este é o valor "port" da mensagem de extensão. As consultas usam o número de protocolo 17 do [I2CP](/docs/specs/i2cp/).

Além dessa porta UDP, usamos uma segunda porta de datagrama igual à porta de consulta + 1. Isso é usado para receber datagramas não assinados (brutos) para respostas, erros e anúncios. Esta porta oferece maior eficiência, pois as respostas contêm tokens enviados na consulta e não precisam ser assinadas. Chamamos isso de "porta de resposta". Este é o valor "rport" da mensagem de extensão. Deve ser 1 + a porta de consulta. Respostas e anúncios usam o número de protocolo [I2CP](/docs/specs/i2cp/) 18.

A informação compacta de peer é de 32 bytes (Hash SHA256 de 32 bytes) em vez de IP de 4 bytes + porta de 2 bytes. Não há porta de peer. Em uma resposta, a chave "values" é uma lista de strings, cada uma contendo uma única informação compacta de peer.

A informação compacta do nó tem 54 bytes (20 bytes do Node ID + 32 bytes do SHA256 Hash + 2 bytes da porta) em vez de 20 bytes do Node ID + 4 bytes do IP + 2 bytes da porta. Em uma resposta, a chave "nodes" é uma única string de bytes com informações compactas do nó concatenadas.

Requisito de ID de nó seguro: Para tornar vários ataques DHT mais difíceis, os primeiros 4 bytes do ID do Nó devem corresponder aos primeiros 4 bytes do Hash de destino, e os próximos dois bytes do ID do Nó devem corresponder aos próximos dois bytes do hash de destino com OR exclusivo com a porta.

Em um arquivo torrent, a chave "nodes" do dicionário de torrent sem tracker está por definir (TBD). Poderia ser uma lista de strings binárias de 32 bytes (Hashes SHA256) em vez de uma lista de listas contendo uma string de host e um inteiro de porta. Alternativas: Uma única string de bytes com hashes concatenados, ou uma lista apenas de strings.

---

## Trackers de Datagrama (UDP)

A especificação para anúncios UDP no I2P foi finalizada em 2025-06. O suporte em vários clientes I2P e trackers será implementado gradualmente ao longo de 2025. As diferenças em relação ao [BEP 15](http://www.bittorrent.org/beps/bep_0015.html) estão documentadas na [especificação de anúncios UDP](/docs/specs/udp-announces/). A especificação também requer suporte para [os novos formatos Datagram 2/3](/docs/specs/datagrams/).

---

## Informações Adicionais

Uma especificação preliminar para o cálculo do conjunto rápido permitido está em [Proposta 172](/proposals/172-bep6-allowed-fast)

---

## Informações Adicionais

- Os padrões de bittorrent I2P são geralmente discutidos em [zzz.i2p](http://zzz.i2p/).
- Um gráfico das capacidades atuais do software de tracker está [também disponível lá](http://zzz.i2p/files/trackers.html).
- O [FAQ de bittorrent I2P](http://forum.i2p/viewtopic.php?t=2068)
- [Discussão sobre DHT no I2P](http://zzz.i2p/topics/812)
