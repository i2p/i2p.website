---
title: "Visão Geral do Transporte"
description: "Visão geral da camada de transporte do I2P para comunicação ponto-a-ponto entre routers"
slug: "transport"
aliases:
  - "/pt/transport"
  - "/pt/transport/"
lastUpdated: "2026-03"
accurateFor: "0.9.69"
---

## Transportes no I2P

Um "transport" no I2P é um método para comunicação direta, ponto-a-ponto entre dois routers. Os transports devem fornecer confidencialidade e integridade contra adversários externos enquanto autenticam que o router contatado é aquele que deveria receber uma determinada mensagem.

I2P suporta múltiplos transportes simultaneamente. Existem três transportes atualmente implementados:

1. [NTCP](/docs/legacy/ntcp/), um transporte TCP Java New I/O (NIO)
2. [SSU](/docs/legacy/ssu/), ou Secure Semireliable UDP
3. [NTCP2](/docs/specs/ntcp2/), uma nova versão do NTCP

Cada um fornece um paradigma de "conexão", com autenticação, controle de fluxo, confirmações e retransmissão.

- Entrega confiável de mensagens [I2NP](/docs/specs/i2np/). Os transportes suportam entrega de mensagens I2NP APENAS. Eles não são canais de dados de uso geral.
- A entrega ordenada de mensagens NÃO é garantida por todos os transportes.
- Manter um conjunto de endereços do router, um ou mais para cada transporte, que o router publica como suas informações de contato globais (o RouterInfo). Cada transporte pode se conectar usando um desses endereços, que podem ser IPv4 ou (a partir da versão 0.9.8) IPv6.
- Seleção do melhor transporte para cada mensagem de saída
- Enfileiramento de mensagens de saída por prioridade
- Limitação de largura de banda, tanto de saída quanto de entrada, de acordo com a configuração do router
- Configuração e desconexão de conexões de transporte
- Criptografia de comunicações ponto a ponto
- Manutenção de limites de conexão para cada transporte, implementação de vários limiares para esses limites, e comunicação do status do limiar ao router para que ele possa fazer mudanças operacionais baseadas no status
- Abertura de porta do firewall usando UPnP (Universal Plug and Play)
- Travessia cooperativa de NAT/Firewall
- Detecção de IP local por vários métodos, incluindo UPnP, inspeção de conexões de entrada, e enumeração de dispositivos de rede
- Coordenação do status do firewall e IP local, e mudanças em qualquer um deles, entre os transportes
- Comunicação do status do firewall e IP local, e mudanças em qualquer um deles, ao router e à interface do usuário
- Determinação de um relógio de consenso, que é usado para atualizar periodicamente o relógio do router, como backup para o NTP
- Manutenção do status para cada peer, incluindo se está conectado, se foi conectado recentemente, e se estava alcançável na última tentativa
- Qualificação de endereços IP válidos de acordo com um conjunto de regras locais
- Honrar as listas automatizadas e manuais de peers banidos mantidas pelo router, e recusar conexões de saída e entrada para esses peers

---

O subsistema de transporte no I2P fornece os seguintes serviços:

## Serviços de Transporte

---

- Um router não possui endereços publicados, então é considerado "oculto" e não pode receber conexões de entrada
- Um router está atrás de firewall e, portanto, publica um endereço SSU que contém uma lista de pares cooperantes ou "introducers" que irão auxiliar na travessia de NAT (veja [a especificação SSU](/docs/legacy/ssu/) para detalhes)
- Um router não está atrás de firewall ou suas portas NAT estão abertas; ele publica endereços NTCP e SSU contendo IP e portas diretamente acessíveis.

O subsistema de transporte mantém um conjunto de endereços de router, cada um dos quais lista um método de transporte, IP e porta. Estes endereços constituem os pontos de contato anunciados e são publicados pelo router na base de dados da rede. Os endereços também podem conter um conjunto arbitrário de opções adicionais.

## Endereços de Transporte

Cada método de transporte pode publicar múltiplos endereços de router.

Cenários típicos são:

---

- Configuração das preferências de transporte
- Se o transporte já está conectado ao peer
- O número de conexões atuais comparado aos vários limites de conexão
- Se tentativas recentes de conexão ao peer falharam
- O tamanho da mensagem, já que diferentes transportes têm diferentes limites de tamanho
- Se o peer pode aceitar conexões de entrada para esse transporte, conforme anunciado em seu RouterInfo
- Se a conexão seria indireta (requerendo introducers) ou direta
- A preferência de transporte do peer, conforme anunciada em seu RouterInfo

O sistema de transporte entrega apenas [mensagens I2NP](/docs/specs/i2np/). O transporte selecionado para qualquer mensagem é independente dos protocolos e conteúdos das camadas superiores (mensagens do router ou cliente, se uma aplicação externa estava usando TCP ou UDP para conectar ao I2P, se a camada superior estava usando [a biblioteca de streaming](/docs/api/streaming/) ou [datagramas](/docs/api/datagrams/), etc.).

## Seleção de Transporte

Para cada mensagem de saída, o sistema de transporte solicita "ofertas" de cada transporte. O transporte que oferecer o valor mais baixo (melhor) ganha a oferta e recebe a mensagem para entrega. Um transporte pode recusar-se a fazer uma oferta.

Se um transporte faz uma oferta, e com que valor, depende de vários fatores:

Em geral, os valores de lance são selecionados para que dois routers sejam conectados por apenas um transporte por vez. No entanto, isso não é um requisito.

- Um transporte similar ao TLS/SSH
- Um transporte "indireto" para routers que não são acessíveis por todos os outros routers (uma forma de "rotas restritas")
- Transportes plugáveis compatíveis com Tor

---

Transportes adicionais podem ser desenvolvidos, incluindo:

## Novos Transportes e Trabalho Futuro

O trabalho continua no ajuste dos limites padrão de conexão para cada transporte. O I2P é projetado como uma "rede mesh", onde se assume que qualquer router pode se conectar a qualquer outro router. Esta suposição pode ser quebrada por routers que excederam seus limites de conexão, e por routers que estão atrás de firewalls de estado restritivos (rotas restritas).

- Um transporte semelhante a TLS/SSH
- Um transporte "indireto" para roteadores que não são alcançáveis por todos os outros roteadores (uma forma de "rotas restritas")
- Transportes plugáveis compatíveis com Tor

Os limites de conexão atuais são mais altos para SSU do que para NTCP, baseados na suposição de que os requisitos de memória para uma conexão NTCP são maiores do que para SSU. No entanto, como os buffers NTCP estão parcialmente no kernel e os buffers SSU estão no heap Java, essa suposição é difícil de verificar.

Analise [Breaking and Improving Protocol Obfuscation](http://www.iis.se/docs/hjelmvik_breaking.pdf) e veja como o preenchimento da camada de transporte pode melhorar as coisas.

Analise [Breaking and Improving Protocol Obfuscation](http://www.iis.se/docs/hjelmvik_breaking.pdf) e veja como o preenchimento na camada de transporte pode melhorar as coisas.
