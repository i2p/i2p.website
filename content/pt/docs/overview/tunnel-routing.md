---
title: "Roteamento de Tunnel"
description: "Visão geral da terminologia, construção e operação de tunnels I2P"
slug: "tunnel-routing"
lastUpdated: "2026-03"
accurateFor: "0.9.68"
---

## Visão Geral

Esta página contém uma visão geral da terminologia e operação de tunnel I2P, com links para páginas mais técnicas, detalhes e especificações.

Como brevemente explicado na [introdução](/docs/overview/intro/), o I2P constrói "túneis" virtuais - caminhos temporários e unidirecionais através de uma sequência de routers. Estes túneis são classificados como túneis de entrada (onde tudo que é dado a eles vai em direção ao criador do túnel) ou túneis de saída (onde o criador do túnel empurra mensagens para longe de si). Quando Alice quer enviar uma mensagem para Bob, ela irá (tipicamente) enviá-la através de um dos seus túneis de saída existentes com instruções para que o endpoint desse túnel a encaminhe para o router gateway de um dos túneis de entrada atuais do Bob, que por sua vez a passa para Bob.

![Alice conectando através de seu tunnel de saída para Bob via tunnel de entrada dele](/images/tunnelSending.svg)

```
A: Outbound Gateway (Alice)
B: Outbound Participant
C: Outbound Endpoint
D: Inbound Gateway
E: Inbound Participant
F: Inbound Endpoint (Bob)
```
---

## Vocabulário de Tunnel

- **Tunnel gateway** - o primeiro router em um tunnel. Para tunnels de entrada, este é o mencionado no LeaseSet publicado na [base de dados da rede](/docs/overview/network-database/). Para tunnels de saída, o gateway é o router de origem. (ex: tanto A quanto D acima)

- **Tunnel endpoint** - o último router em um tunnel. (ex.: tanto C quanto F acima)

- **Participante do tunnel** - todos os routers em um tunnel exceto o gateway ou endpoint (ex: tanto B quanto E acima)

- **tunnel n-Hop** - um tunnel com um número específico de saltos entre roteadores, por exemplo:
  - **tunnel 0-hop** - um tunnel onde o gateway é também o endpoint
  - **tunnel 1-hop** - um tunnel onde o gateway fala diretamente com o endpoint
  - **tunnel 2-(ou mais)-hop** - um tunnel onde há pelo menos um participante intermediário do tunnel. (o diagrama acima inclui dois tunnels 2-hop - um outbound da Alice, um inbound para Bob)

- **Tunnel ID** - Um [inteiro de 4 bytes](/docs/specs/common-structures/#type_TunnelId) diferente para cada hop em um tunnel, e único entre todos os tunnels em um router. Escolhido aleatoriamente pelo criador do tunnel.

---

## Informações de Construção de Tunnel

Routers desempenhando os três papéis (gateway, participante, endpoint) recebem diferentes dados na [Mensagem de Construção de Tunnel](/docs/specs/tunnel-creation/) inicial para realizar suas tarefas:

**O gateway do tunnel recebe:**

- **chave de criptografia do tunnel** - uma [chave privada AES](/docs/specs/common-structures/#type_SessionKey) para criptografar mensagens e instruções para o próximo salto
- **chave IV do tunnel** - uma [chave privada AES](/docs/specs/common-structures/#type_SessionKey) para criptografia dupla do IV para o próximo salto
- **chave de resposta** - uma [chave pública AES](/docs/specs/common-structures/#type_SessionKey) para criptografar a resposta à solicitação de construção do tunnel
- **IV de resposta** - o IV para criptografar a resposta à solicitação de construção do tunnel
- **ID do tunnel** - inteiro de 4 bytes (apenas gateways de entrada)
- **próximo salto** - qual router é o próximo no caminho (a menos que seja um tunnel de 0 saltos, e o gateway também seja o endpoint)
- **ID do próximo tunnel** - O ID do tunnel no próximo salto

**Todos os participantes intermediários do tunnel recebem:**

- **tunnel encryption key** - uma [chave privada AES](/docs/specs/common-structures/#type_SessionKey) para criptografar mensagens e instruções para o próximo salto
- **tunnel IV key** - uma [chave privada AES](/docs/specs/common-structures/#type_SessionKey) para criptografar duplamente o IV para o próximo salto
- **reply key** - uma [chave pública AES](/docs/specs/common-structures/#type_SessionKey) para criptografar a resposta à solicitação de construção do tunnel
- **reply IV** - o IV para criptografar a resposta à solicitação de construção do tunnel
- **tunnel id** - inteiro de 4 bytes
- **next hop** - qual router é o próximo no caminho
- **next tunnel id** - O ID do tunnel no próximo salto

**O endpoint do tunnel recebe:**

- **chave de criptografia do tunnel** - uma [chave privada AES](/docs/specs/common-structures/#type_SessionKey) para criptografar mensagens e instruções para o endpoint (ele próprio)
- **chave IV do tunnel** - uma [chave privada AES](/docs/specs/common-structures/#type_SessionKey) para criptografar duplamente o IV para o endpoint (ele próprio)
- **chave de resposta** - uma [chave pública AES](/docs/specs/common-structures/#type_SessionKey) para criptografar a resposta à solicitação de construção do tunnel (apenas endpoints de saída)
- **IV de resposta** - o IV para criptografar a resposta à solicitação de construção do tunnel (apenas endpoints de saída)
- **ID do tunnel** - inteiro de 4 bytes (apenas endpoints de saída)
- **router de resposta** - o gateway de entrada do tunnel através do qual enviar a resposta (apenas endpoints de saída)
- **ID do tunnel de resposta** - O ID do tunnel do router de resposta (apenas endpoints de saída)

Os detalhes estão na [especificação de criação de tunnel](/docs/specs/tunnel-creation/).

---

## Agrupamento de Tunnels

Vários tunnels para um propósito específico podem ser agrupados em um "pool de tunnels", conforme descrito na [especificação de tunnel](/docs/specs/tunnel-implementation/#tunnel.pooling). Isso proporciona redundância e largura de banda adicional. Os pools usados pelo próprio router são chamados de "tunnels exploratórios". Os pools usados pelas aplicações são chamados de "tunnels de cliente".

---

## Comprimento do Tunnel

Como mencionado acima, cada cliente solicita que seu router forneça tunnels para incluir pelo menos um certo número de saltos. A decisão sobre quantos routers ter nos tunnels de saída e entrada tem um efeito importante na latência, throughput, confiabilidade e anonimato fornecido pelo I2P - quanto mais peers pelas quais as mensagens precisam passar, mais tempo leva para chegar ao destino e maior a probabilidade de que um desses routers falhe prematuramente. Quanto menos routers em um tunnel, mais fácil é para um adversário realizar ataques de análise de tráfego e quebrar o anonimato de alguém. Os comprimentos dos tunnels são especificados pelos clientes através das [opções I2CP](/docs/specs/i2cp/#options). O número máximo de saltos em um tunnel é 7.

### tunnels de 0 saltos

Sem routers remotos em um tunnel, o usuário tem uma negação plausível muito básica (já que ninguém sabe com certeza se o peer que lhe enviou a mensagem não estava simplesmente encaminhando-a como parte do tunnel). No entanto, seria bastante fácil montar um ataque de análise estatística e notar que mensagens direcionadas a um destino específico são sempre enviadas através de um único gateway. Análises estatísticas contra tunnels de saída de 0-hop são mais complexas, mas poderiam mostrar informações similares (embora seriam ligeiramente mais difíceis de executar).

### tunnels de 1 salto

Com apenas um router remoto em um tunnel, o usuário tem tanto negação plausível quanto anonimato básico, desde que não esteja enfrentando um adversário interno (como descrito no [modelo de ameaças](/docs/overview/threat-model/)). No entanto, se o adversário executasse um número suficiente de routers de tal forma que o único router remoto no tunnel fosse frequentemente um daqueles comprometidos, eles seriam capazes de realizar o ataque de análise de tráfego estatística mencionado acima.

### tunnels de 2 saltos

Com dois ou mais routers remotos num tunnel, os custos de montar o ataque de análise de tráfego aumentam, já que muitos routers remotos teriam de ser comprometidos para montá-lo.

### túneis de 3 saltos (ou mais)

Para reduzir a suscetibilidade a [alguns ataques](https://blog.torproject.org/one-cell-enough-break-tors-anonymity/), recomenda-se 3 ou mais saltos para o mais alto nível de proteção. [Estudos recentes](https://blog.torproject.org/one-cell-enough-break-tors-anonymity/) também concluem que mais de 3 saltos não oferece proteção adicional.

### Comprimentos padrão de tunnel

O router usa túneis de 2 saltos por padrão para seus túneis exploratórios. Os padrões dos túneis cliente são definidos pela aplicação, usando [opções I2CP](/docs/specs/i2cp/#options). A maioria das aplicações usa 2 ou 3 saltos como padrão.

---

## Teste de Tunnel

Todos os tunnels são periodicamente testados pelo seu criador enviando uma DeliveryStatusMessage através de um tunnel de saída e destinada a outro tunnel de entrada (testando ambos os tunnels de uma só vez). Se algum deles falhar em um número consecutivo de testes, é marcado como não funcional. Se foi usado para o tunnel de entrada de um cliente, um novo leaseSet é criado. Falhas nos testes de tunnel também são refletidas na [classificação de capacidade no perfil do peer](/docs/overview/peer-selection/#capacity).

---

A criação de túneis é gerenciada pelo [garlic routing](/docs/overview/garlic-routing/) uma Mensagem de Construção de Túnel para um router, solicitando que ele participe no túnel (fornecendo-lhe todas as informações apropriadas, como acima, junto com um certificado, que atualmente é um certificado 'nulo', mas suportará hashcash ou outros certificados não gratuitos quando necessário). Esse router encaminha a mensagem para o próximo salto no túnel. Os detalhes estão na [especificação de criação de túneis](/docs/specs/tunnel-creation/).

## Criação de Tunnel

---

A criptografia multicamada é tratada pela [garlic encryption](/docs/overview/garlic-routing/) das mensagens de tunnel. Os detalhes estão na [especificação de tunnel](/docs/specs/tunnel-implementation/). O IV de cada salto é criptografado com uma chave separada, conforme explicado lá.

## Criptografia de Tunnel

---

---

## Trabalho Futuro

- Outras técnicas de teste de tunnel poderiam ser usadas, como garlic wrapping de vários testes em cloves, testando participantes individuais de tunnel separadamente, etc.

- Mover para padrões de tunnels exploratórios de 3 saltos.

- Em uma versão futura distante, opções especificando as configurações de pooling, mixing e geração de chaff podem ser implementadas.

- Em uma versão futura distante, limites na quantidade e tamanho de mensagens permitidas durante o tempo de vida do tunnel podem ser implementados (por exemplo, não mais que 300 mensagens ou 1MB por minuto).

---

## Veja Também

- [Especificação de tunnel](/docs/specs/tunnel-implementation/)
- [Especificação de criação de tunnel](/docs/specs/tunnel-creation/)
- [Tunnels unidirecionais](/docs/legacy/unidirectional/)
- [Especificação de mensagem de tunnel](/docs/specs/tunnel-message/)
- [Roteamento garlic](/docs/overview/garlic-routing/)
- [ElGamal/AES+SessionTag](/docs/specs/elgamal-aes/)
- [Opções I2CP](/docs/specs/i2cp/#options)
