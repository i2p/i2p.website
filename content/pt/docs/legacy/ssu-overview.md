---
title: "Secure Semireliable UDP (SSU)"
description: "Transporte UDP original usado antes do SSU2 (descontinuado)"
slug: "ssu-overview"
aliases:
  - "/pt/udp"
  - "/pt/udp/"
lastUpdated: "2025-01"
accurateFor: "0.9.64"
---

**DESCONTINUADO** - SSU foi substituído por SSU2. O suporte para SSU foi removido do i2pd na versão 2.44.0 (API 0.9.56) 2022-11. O suporte para SSU foi removido do Java I2P na versão 2.4.0 (API 0.9.61) 2023-12.

SSU (também chamado de "UDP" em grande parte da documentação e interfaces de usuário do I2P) foi um dos dois [transportes](/docs/transport) implementados no I2P. O outro é [NTCP2](/docs/specs/ntcp2). O suporte para [NTCP](/docs/legacy/ntcp) foi removido.

SSU foi introduzido na versão 0.6 do I2P. Numa instalação padrão do I2P, o router usa tanto NTCP quanto SSU para conexões de saída. SSU-over-IPv6 é suportado a partir da versão 0.9.8.

SSU é chamado de "semirreliável" porque retransmitirá repetidamente mensagens não confirmadas, mas apenas até um número máximo de vezes. Depois disso, a mensagem é descartada.

## Serviços SSU

Como o transporte NTCP, o SSU fornece transporte de dados confiável, criptografado, orientado a conexão e ponto-a-ponto. Exclusivo do SSU, ele também fornece serviços de detecção de IP e atravessamento de NAT, incluindo:

- Travessia cooperativa de NAT/Firewall usando [introducers](#introduction)
- Detecção de IP local por inspeção de pacotes recebidos e [peer testing](#peerTesting)
- Comunicação do status do firewall e IP local, e mudanças de qualquer um para NTCP
- Comunicação do status do firewall e IP local, e mudanças de qualquer um, para o router e a interface do usuário

## Especificação de Endereço do Router {#ra}

As seguintes propriedades são armazenadas na base de dados da rede.

- **Nome do transporte:** SSU
- **caps:** [B,C,4,6] [Veja abaixo](#capabilities).
- **host:** IP (IPv4 ou IPv6).
  Endereço IPv6 encurtado (com "::") é permitido.
  Pode ou não estar presente se atrás de firewall.
  Nomes de host eram permitidos anteriormente, mas estão obsoletos a partir da versão 0.9.32. Veja a proposta 141.
- **iexp[0-2]:** Expiração deste introducer.
  Dígitos ASCII, em segundos desde a época.
  Presente apenas se atrás de firewall e introducers são necessários.
  Opcional (mesmo se outras propriedades para este introducer estiverem presentes).
  A partir da versão 0.9.30, proposta 133.
- **ihost[0-2]:** IP do introducer (IPv4 ou IPv6).
  Nomes de host eram permitidos anteriormente, mas estão obsoletos a partir da versão 0.9.32. Veja a proposta 141.
  Endereço IPv6 encurtado (com "::") é permitido.
  Presente apenas se atrás de firewall e introducers são necessários.
  [Veja abaixo](#introduction).
- **ikey[0-2]:** Chave de introdução Base 64 do introducer. [Veja abaixo](#key).
  Presente apenas se atrás de firewall e introducers são necessários.
  [Veja abaixo](#introduction).
- **iport[0-2]:** Porta do introducer 1024 - 65535.
  Presente apenas se atrás de firewall e introducers são necessários.
  [Veja abaixo](#introduction).
- **itag[0-2]:** Tag do introducer 1 - (2^32 - 1)
  Dígitos ASCII.
  Presente apenas se atrás de firewall e introducers são necessários.
  [Veja abaixo](#introduction).
- **key:** Chave de introdução Base 64. [Veja abaixo](#key).
- **mtu:** Opcional. Padrão e máximo é 1484. Mínimo é 620.
  Deve estar presente para IPv6, onde o mínimo é 1280 e o máximo é 1488
  (máximo era 1472 antes da versão 0.9.28).
  MTU IPv6 deve ser múltiplo de 16.
  (MTU IPv4 + 4) deve ser múltiplo de 16.
  [Veja abaixo](#mtu).
- **port:** 1024 - 65535
  Pode ou não estar presente se atrás de firewall.

# Detalhes do Protocolo

## Controle de Congestionamento {#congestioncontrol}

A necessidade do SSU de apenas entrega semi-confiável, operação compatível com TCP e a capacidade de alto throughput permite uma grande margem de manobra no controle de congestionamento. O algoritmo de controle de congestionamento descrito abaixo pretende ser tanto eficiente em largura de banda quanto simples de implementar.

Os pacotes são agendados de acordo com a política do router, tomando cuidado para não exceder a capacidade de saída do router ou exceder a capacidade medida do peer remoto. A capacidade medida opera seguindo as linhas do slow start e congestion avoidance do TCP, com aumentos aditivos na capacidade de envio e diminuições multiplicativas em face de congestionamento. Diferentemente do TCP, os routers podem desistir de algumas mensagens após um determinado período ou número de retransmissões enquanto continuam a transmitir outras mensagens.

As técnicas de detecção de congestionamento também variam do TCP, já que cada mensagem tem seu próprio identificador único e não sequencial, e cada mensagem tem um tamanho limitado - no máximo, 32KB. Para transmitir eficientemente esse feedback ao remetente, o receptor inclui periodicamente uma lista de identificadores de mensagem totalmente confirmados (ACKed) e também pode incluir bitfields para mensagens parcialmente recebidas, onde cada bit representa a recepção de um fragmento. Se fragmentos duplicados chegarem, a mensagem deve ser confirmada (ACKed) novamente, ou se a mensagem ainda não foi totalmente recebida, o bitfield deve ser retransmitido com quaisquer novas atualizações.

A implementação atual não preenche os pacotes para um tamanho específico, mas em vez disso apenas coloca um único fragmento de mensagem em um pacote e o envia (cuidando para não exceder o MTU).

### MTU {#mtu}

A partir da versão 0.8.12 do router, dois valores de MTU são usados para IPv4: 620 e 1484. O valor do MTU é ajustado com base na porcentagem de pacotes que são retransmitidos.

Para ambos os valores de MTU, é desejável que (MTU % 16) == 12, para que a porção de payload após o cabeçalho IP/UDP de 28 bytes seja um múltiplo de 16 bytes, para fins de criptografia.

Para o valor pequeno de MTU, é desejável empacotar uma Mensagem de Construção de Tunnel Variável de 2646 bytes de forma eficiente em múltiplos pacotes; com um MTU de 620 bytes, ela se encaixa bem em 5 pacotes.

Baseado em medições, 1492 cabe em quase todas as mensagens I2NP razoavelmente pequenas (mensagens I2NP maiores podem ter até 1900 a 4500 bytes, que de qualquer forma não cabem no MTU de uma rede ativa).

Os valores de MTU eram 608 e 1492 para as versões 0.8.9 - 0.8.11. O MTU grande era 1350 antes da versão 0.8.9.

O tamanho máximo do pacote de recebimento é de 1571 bytes a partir da versão 0.8.12. Para as versões 0.8.9 - 0.8.11 era de 1535 bytes. Antes da versão 0.8.9 era de 2048 bytes.

A partir da versão 0.9.2, se o MTU da interface de rede de um router for menor que 1484, ele publicará isso no banco de dados da rede, e outros routers devem respeitar isso quando uma conexão for estabelecida.

Para IPv6, o MTU mínimo é 1280. O cabeçalho IPv6 IP/UDP tem 48 bytes, então usamos um MTU onde (MTU % 16 == 0), o que é verdadeiro para 1280. O MTU máximo para IPv6 é 1488. (o máximo era 1472 antes da versão 0.9.28).

### Limites de Tamanho da Mensagem {#max}

Embora o tamanho máximo da mensagem seja nominalmente 32KB, o limite prático é diferente. O protocolo limita o número de fragmentos a 7 bits, ou 128. A implementação atual, no entanto, limita cada mensagem a um máximo de 64 fragmentos, o que é suficiente para 64 * 534 = 33,3 KB ao usar o MTU de 608. Devido ao overhead para leaseSets agrupados e chaves de sessão, o limite prático no nível da aplicação é cerca de 6KB menor, ou cerca de 26KB. Mais trabalho é necessário para elevar o limite de transporte UDP acima de 32KB. Para conexões usando o MTU maior, mensagens maiores são possíveis.

## Tempo Limite de Inatividade

O timeout de inatividade e o fechamento da conexão ficam a critério de cada endpoint e podem variar. A implementação atual reduz o timeout conforme o número de conexões se aproxima do máximo configurado, e aumenta o timeout quando a contagem de conexões está baixa. O timeout mínimo recomendado é de dois minutos ou mais, e o timeout máximo recomendado é de dez minutos ou mais.

## Chaves {#keys}

Toda a encriptação utilizada é AES256/CBC com chaves de 32 bytes e IVs de 16 bytes. Quando Alice origina uma sessão com Bob, as chaves MAC e de sessão são negociadas como parte da troca DH, e são então usadas para HMAC e encriptação, respectivamente. Durante a troca DH, a introKey publicamente conhecível do Bob é usada para MAC e encriptação.

Tanto a mensagem inicial quanto a resposta subsequente usam a introKey do respondente (Bob) - o respondente não precisa conhecer a introKey do solicitante (Alice). A chave de assinatura DSA usada por Bob já deve ser conhecida por Alice quando ela o contata, embora a chave DSA de Alice possa não ser ainda conhecida por Bob.

Ao receber uma mensagem, o receptor verifica o endereço IP "from" e a porta com todas as sessões estabelecidas - se houver correspondências, as chaves MAC dessa sessão são testadas no HMAC. Se nenhuma delas verificar ou se não houver endereços IP correspondentes, o receptor tenta sua introKey no MAC. Se isso não verificar, o pacote é descartado. Se verificar, é interpretado de acordo com o tipo de mensagem, embora se o receptor estiver sobrecarregado, pode ser descartado mesmo assim.

Se Alice e Bob têm uma sessão estabelecida, mas Alice perde as chaves por algum motivo e ela quer entrar em contato com Bob, ela pode a qualquer momento simplesmente estabelecer uma nova sessão através do SessionRequest e mensagens relacionadas. Se Bob perdeu a chave mas Alice não sabe disso, ela primeiro tentará cutucá-lo para responder, enviando uma DataMessage com a flag wantReply definida, e se Bob continuar falhando em responder, ela assumirá que a chave foi perdida e reestabelecerá uma nova.

Para o acordo de chaves DH, é usado o grupo MODP de 2048 bits (#14) do [RFC3526](http://www.faqs.org/rfcs/rfc3526.html):

```
  p = 2^2048 - 2^1984 - 1 + 2^64 * { [2^1918 pi] + 124476 }
  g = 2
```
Estes são os mesmos p e g usados para a [criptografia ElGamal](/docs/specs/cryptography#elgamal) do I2P.

## Prevenção de Replay {#replay}

A prevenção de replay na camada SSU ocorre rejeitando pacotes com timestamps excessivamente antigos ou aqueles que reutilizam um IV. Para detectar IVs duplicados, uma sequência de filtros Bloom é empregada para "decair" periodicamente de modo que apenas IVs adicionados recentemente sejam detectados.

Os messageIds usados em DataMessages são definidos em camadas acima do transporte SSU e são passados de forma transparente. Esses IDs não estão em nenhuma ordem particular - na verdade, é provável que sejam totalmente aleatórios. A camada SSU não faz nenhuma tentativa de prevenção de replay de messageId - camadas superiores devem levar isso em consideração.

## Endereçamento {#addressing}

Para contactar um peer SSU, um de dois conjuntos de informações é necessário: um endereço direto, para quando o peer é publicamente acessível, ou um endereço indireto, para usar uma terceira parte para introduzir o peer. Não há restrição no número de endereços que um peer pode ter.

```
    Direct: host, port, introKey, options
  Indirect: tag, relayhost, port, relayIntroKey, targetIntroKey, options
```
Cada um dos endereços também pode expor uma série de opções - capacidades especiais desse peer específico. Para uma lista das capacidades disponíveis, veja [abaixo](#capabilities).

Os endereços, opções e capacidades são publicados na [base de dados da rede](/docs/overview/network-database).

## Estabelecimento Direto de Sessão {#direct}

O estabelecimento direto de sessão é usado quando nenhuma terceira parte é necessária para a travessia de NAT. A sequência de mensagens é a seguinte:

### Estabelecimento de Conexão (Direto) {#establishDirect}

Alice conecta-se diretamente ao Bob. IPv6 é suportado a partir da versão 0.9.8.

```
        Alice                         Bob
    SessionRequest --------------------->
          <--------------------- SessionCreated
    SessionConfirmed ------------------->
          <--------------------- DeliveryStatusMessage
          <--------------------- DatabaseStoreMessage
    DatabaseStoreMessage --------------->
    Data <--------------------------> Data
```
Após a mensagem SessionConfirmed ser recebida, Bob envia uma pequena [mensagem DeliveryStatus](/docs/specs/i2np#msg_DeliveryStatus) como confirmação. Nesta mensagem, o ID da mensagem de 4 bytes é definido como um número aleatório, e o "tempo de chegada" de 8 bytes é definido como o ID atual da rede, que é 2 (ou seja, 0x0000000000000002).

Após a mensagem de status ser enviada, os peers geralmente trocam [mensagens DatabaseStore](/docs/specs/i2np#msg_DatabaseStore) contendo suas [RouterInfos](/docs/specs/common-structures#struct_RouterInfo), no entanto, isso não é obrigatório.

Não parece que o tipo da mensagem de status ou seu conteúdo importem. Foi originalmente adicionado porque a mensagem DatabaseStore estava atrasada vários segundos; já que o store agora é enviado imediatamente, talvez a mensagem de status possa ser eliminada.

## Introdução {#introduction}

As chaves de introdução são entregues através de um canal externo (o network database), onde tradicionalmente foram idênticas ao Hash do router até a versão 0.9.47, mas podem ser aleatórias a partir da versão 0.9.48. Elas devem ser usadas ao estabelecer uma chave de sessão. Para o endereço indireto, o peer deve primeiro contactar o relayhost e pedir-lhe uma introdução ao peer conhecido nesse relayhost sob a tag fornecida. Se possível, o relayhost envia uma mensagem ao peer endereçado dizendo-lhe para contactar o peer solicitante, e também fornece ao peer solicitante o IP e porta onde o peer endereçado está localizado. Além disso, o peer que estabelece a conexão deve já conhecer as chaves públicas do peer ao qual se está conectando (mas não necessariamente de qualquer peer relay intermediário).

O estabelecimento indireto de sessão por meio de uma introdução de terceiros é necessário para uma travessia eficiente de NAT. Charlie, um router atrás de um NAT ou firewall que não permite pacotes UDP de entrada não solicitados, primeiro contacta alguns peers, escolhendo alguns para servir como introdutores. Cada um desses peers (Bob, Bill, Betty, etc) fornecem a Charlie uma tag de introdução - um número aleatório de 4 bytes - que ele então disponibiliza ao público como métodos de contactá-lo. Alice, um router que tem os métodos de contacto publicados do Charlie, primeiro envia um pacote RelayRequest para um ou mais dos introdutores, pedindo a cada um que a apresente ao Charlie (oferecendo a tag de introdução para identificar Charlie). Bob então encaminha um pacote RelayIntro para Charlie incluindo o IP público e número de porta da Alice, depois envia de volta à Alice um pacote RelayResponse contendo o IP público e número de porta do Charlie. Quando Charlie recebe o pacote RelayIntro, ele envia um pequeno pacote aleatório para o IP e porta da Alice (abrindo um buraco no seu NAT/firewall), e quando Alice recebe o pacote RelayResponse do Bob, ela inicia um novo estabelecimento de sessão de direção completa com o IP e porta especificados.

### Estabelecimento de Conexão (Indireto Usando um Introducer) {#establishIndirect}

Alice primeiro se conecta ao introdutor Bob, que retransmite a solicitação para Charlie.

```
        Alice                         Bob                  Charlie
    RelayRequest ---------------------->
         <-------------- RelayResponse    RelayIntro ----------->
         <-------------------------------------------- HolePunch (data ignored)
    SessionRequest -------------------------------------------->
         <-------------------------------------------- SessionCreated
    SessionConfirmed ------------------------------------------>
         <-------------------------------------------- DeliveryStatusMessage
         <-------------------------------------------- DatabaseStoreMessage
    DatabaseStoreMessage -------------------------------------->
    Data <--------------------------------------------------> Data
```
Após o hole punch, a sessão é estabelecida entre Alice e Charlie como em um estabelecimento direto.

### Notas IPv6

IPv6 é suportado a partir da versão 0.9.8. Endereços de relay publicados podem ser IPv4 ou IPv6, e a comunicação Alice-Bob pode ser via IPv4 ou IPv6. Até a versão 0.9.49, a comunicação Bob-Charlie e Alice-Charlie é apenas via IPv4. O relaying para IPv6 é suportado a partir da versão 0.9.50. Veja a especificação para detalhes.

Embora a especificação tenha sido alterada a partir da versão 0.9.8, a comunicação Alice-Bob via IPv6 não foi realmente suportada até a versão 0.9.50. Versões anteriores dos routers Java publicavam erroneamente a capacidade 'C' para endereços IPv6, mesmo que não atuassem realmente como introdutor via IPv6. Portanto, os routers devem confiar apenas na capacidade 'C' em um endereço IPv6 se a versão do router for 0.9.50 ou superior.

## Teste de Peers {#peerTesting}

A automação de testes de alcançabilidade colaborativa para peers é habilitada por uma sequência de mensagens PeerTest. Com sua execução adequada, um peer será capaz de determinar sua própria alcançabilidade e pode atualizar seu comportamento de acordo. O processo de teste é bem simples:

```
        Alice                  Bob                  Charlie
    PeerTest ------------------->
                             PeerTest-------------------->
                                <-------------------PeerTest
         <-------------------PeerTest
         <------------------------------------------PeerTest
    PeerTest------------------------------------------>
         <------------------------------------------PeerTest
```
Cada uma das mensagens PeerTest carrega um nonce que identifica a própria série de testes, conforme inicializada por Alice. Se Alice não receber uma mensagem específica que ela espera, ela retransmitirá adequadamente, e com base nos dados recebidos ou nas mensagens perdidas, ela saberá sua alcançabilidade. Os vários estados finais que podem ser atingidos são os seguintes:

- Se ela não receber uma resposta do Bob, ela retransmitirá
  até um certo número de vezes, mas se nenhuma resposta chegar,
  ela saberá que seu firewall ou NAT está de alguma forma mal configurado,
  rejeitando todos os pacotes UDP de entrada mesmo em resposta direta a um
  pacote de saída. Alternativamente, Bob pode estar inativo ou incapaz de fazer
  Charlie responder.

- Se Alice não receber uma mensagem PeerTest com o
  nonce esperado de uma terceira parte (Charlie), ela retransmitirá
  sua solicitação inicial para Bob até um determinado número de vezes, mesmo
  se já tiver recebido a resposta de Bob. Se a primeira mensagem
  de Charlie ainda não passar mas a de Bob passar, ela sabe que está
  atrás de um NAT ou firewall que está rejeitando tentativas de conexão
  não solicitadas e que o encaminhamento de porta não está funcionando adequadamente (o
  IP e porta que Bob ofereceu deveriam estar sendo encaminhados).

- Se Alice recebe a mensagem PeerTest do Bob e ambas as mensagens PeerTest do Charlie, mas os números de IP e porta incluídos nas segundas mensagens do Bob e do Charlie não coincidem, ela sabe que está atrás de um NAT simétrico, reescrevendo todos os seus pacotes de saída com portas 'de origem' diferentes para cada peer contactado. Ela precisará encaminhar explicitamente uma porta e sempre ter essa porta exposta para conectividade remota, ignorando descobertas de porta futuras.

- Se Alice receber a primeira mensagem de Charlie mas não a segunda,
  ela retransmitirá sua mensagem PeerTest para Charlie até um
  certo número de vezes, mas se nenhuma resposta for recebida ela sabe
  que Charlie está confuso ou não está mais online.

Alice deve escolher Bob arbitrariamente entre os peers conhecidos que parecem capazes de participar em testes de peers. Bob por sua vez deve escolher Charlie arbitrariamente entre os peers que ele conhece e que parecem capazes de participar em testes de peers e que estão em um IP diferente tanto de Bob quanto de Alice. Se a primeira condição de erro ocorrer (Alice não recebe mensagens PeerTest de Bob), Alice pode decidir designar um novo peer como Bob e tentar novamente com um nonce diferente.

A chave de introdução da Alice está incluída em todas as mensagens PeerTest para que Charlie possa contactá-la sem conhecer qualquer informação adicional. A partir da versão 0.9.15, Alice deve ter uma sessão estabelecida com Bob, para prevenir ataques de spoofing. Alice não deve ter uma sessão estabelecida com Charlie para que o teste de peer seja válido. Alice pode continuar e estabelecer uma sessão com Charlie, mas não é obrigatório.

### Notas sobre IPv6

Até a versão 0.9.26, apenas o teste de endereços IPv4 é suportado. Apenas o teste de endereços IPv4 é suportado. Portanto, toda comunicação Alice-Bob e Alice-Charlie deve ser via IPv4. A comunicação Bob-Charlie, no entanto, pode ser via IPv4 ou IPv6. O endereço de Alice, quando especificado na mensagem PeerTest, deve ter 4 bytes. A partir da versão 0.9.27, o teste de endereços IPv6 é suportado, e a comunicação Alice-Bob e Alice-Charlie pode ser via IPv6, se Bob e Charlie indicarem suporte com uma capacidade 'B' em seu endereço IPv6 publicado. Veja [Proposta 126](/spec/proposals/126-ipv6-peer-testing) para detalhes.

Antes da versão 0.9.50, Alice envia a solicitação para Bob usando uma sessão existente sobre o transporte (IPv4 ou IPv6) que ela deseja testar. Quando Bob recebe uma solicitação de Alice via IPv4, Bob deve selecionar um Charlie que anuncia um endereço IPv4. Quando Bob recebe uma solicitação de Alice via IPv6, Bob deve selecionar um Charlie que anuncia um endereço IPv6. A comunicação real Bob-Charlie pode ser via IPv4 ou IPv6 (ou seja, independente do tipo de endereço de Alice).

A partir da versão 0.9.50, se a mensagem for sobre IPv6 para um teste de peer IPv4, ou (a partir da versão 0.9.50) sobre IPv4 para um teste de peer IPv6, Alice deve incluir seu endereço e porta de introdução.

Veja a [Proposta 158](/spec/proposals/158) para detalhes.

## Janela de Transmissão, ACKs e Retransmissões {#acks}

A mensagem DATA pode conter ACKs de mensagens completas e ACKs parciais de fragmentos individuais de uma mensagem. Consulte a seção de mensagem de dados da [página de especificação do protocolo](/docs/legacy/ssu) para detalhes.

Os detalhes das estratégias de janelamento, ACK e retransmissão não são especificados aqui. Consulte o código Java para a implementação atual. Durante a fase de estabelecimento e para teste de peers, os routers devem implementar backoff exponencial para retransmissão. Para uma conexão estabelecida, os routers devem implementar uma janela de transmissão ajustável, estimativa de RTT e timeout, similar ao TCP ou [streaming](/docs/api/streaming). Consulte o código para os parâmetros iniciais, mínimos e máximos.

## Segurança {#security}

Endereços de origem UDP podem, é claro, ser falsificados. Além disso, os IPs e portas contidos dentro de mensagens SSU específicas (RelayRequest, RelayResponse, RelayIntro, PeerTest) podem não ser legítimos. Além disso, certas ações e respostas podem precisar ter sua taxa limitada.

Os detalhes da validação não são especificados aqui. Os implementadores devem adicionar defesas quando apropriado.

## Capacidades dos Pares {#capabilities}

Uma ou mais capacidades podem ser publicadas na opção "caps". As capacidades podem estar em qualquer ordem, mas "BC46" é a ordem recomendada, para consistência entre implementações.

**B** : Se o endereço do peer contém a capacidade 'B', isso significa que eles estão dispostos e capazes de participar em testes de peer como 'Bob' ou 'Charlie'. Até a versão 0.9.26, os testes de peer não eram suportados para endereços IPv6, e a capacidade 'B', se presente para um endereço IPv6, deve ser ignorada. A partir da versão 0.9.27, os testes de peer são suportados para endereços IPv6, e a presença ou ausência da capacidade 'B' em um endereço IPv6 indica suporte real (ou falta de suporte).

**C** : Se o endereço do peer contém a capacidade 'C', isso significa que eles estão dispostos e capazes de servir como um introducer através desse endereço - servindo como um introducer Bob para um Charlie que de outra forma seria inacessível. Antes da versão 0.9.50, os routers Java incorretamente publicavam a capacidade 'C' para endereços IPv6, mesmo que os introducers IPv6 não estivessem totalmente implementados. Portanto, os routers devem assumir que versões anteriores à 0.9.50 não podem atuar como um introducer sobre IPv6, mesmo se a capacidade 'C' for anunciada.

**4** : A partir da versão 0.9.50, indica capacidade IPv4 de saída. Se um IP for publicado no campo host, esta capacidade não é necessária. Se este for um endereço com introdutores para introduções IPv4, '4' deve ser incluído. Se o router estiver oculto, '4' e '6' podem ser combinados em um único endereço.

**6** : A partir da versão 0.9.50, indica capacidade IPv6 de saída. Se um IP for publicado no campo host, esta capacidade não é necessária. Se este for um endereço com introducers para introduções IPv6, '6' deve ser incluído (atualmente não suportado). Se o router estiver oculto, '4' e '6' podem ser combinados em um único endereço.

# Trabalho Futuro {#future}

Nota: Essas questões serão abordadas no desenvolvimento do SSU2.

- A análise do desempenho atual do SSU, incluindo avaliação do ajuste do tamanho da janela
  e outros parâmetros, e ajuste da implementação do protocolo para melhorar
  o desempenho, é um tópico para trabalho futuro.

- A implementação atual envia repetidamente confirmações para os mesmos pacotes,
  o que aumenta desnecessariamente a sobrecarga.

- O valor MTU pequeno padrão de 620 deve ser analisado e possivelmente aumentado.
  A estratégia atual de ajuste de MTU deve ser avaliada.
  Um pacote de 1730 bytes da biblioteca de streaming cabe em 3 pacotes SSU pequenos? Provavelmente não.

- O protocolo deve ser estendido para trocar MTUs durante a configuração.

- O rekeying atualmente não está implementado e nunca será.

- O uso potencial dos campos 'challenge' em RelayIntro e RelayResponse,
  e o uso do campo padding em SessionRequest e SessionCreated, não está documentado.

- Um conjunto de tamanhos de pacote fixos pode ser apropriado para ocultar ainda mais a fragmentação de dados de adversários externos, mas o preenchimento de tunnel, garlic e ponta a ponta deve ser suficiente para a maioria das necessidades até então.

- Os tempos de login no SessionCreated e SessionConfirmed parecem não estar sendo usados ou verificados.

# Especificação {#spec}

[Agora na página de especificação SSU](/docs/legacy/ssu).
