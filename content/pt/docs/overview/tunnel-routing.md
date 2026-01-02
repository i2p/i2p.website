---
title: "Roteamento de Tunnel"
description: "Visão geral da terminologia, construção e ciclo de vida dos túneis I2P"
slug: "tunnel-routing"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

## Visão Geral

I2P constrói túneis temporários e unidirecionais — sequências ordenadas de routers que encaminham tráfego criptografado. Os túneis são classificados como **inbound** (mensagens fluem em direção ao criador) ou **outbound** (mensagens fluem para longe do criador).

Uma troca típica roteia a mensagem de Alice através de um dos seus túneis de saída (outbound tunnels), instrui o ponto final de saída a encaminhá-la para o gateway de um dos túneis de entrada (inbound tunnels) de Bob, e então Bob a recebe no seu ponto final de entrada.

![Alice conectando através de seu túnel de saída para Bob via seu túnel de entrada](/images/tunnelSending.png)

- **A**: Outbound Gateway (Alice)
- **B**: Outbound Participant
- **C**: Outbound Endpoint
- **D**: Inbound Gateway
- **E**: Inbound Participant
- **F**: Inbound Endpoint (Bob)

Os túneis têm um tempo de vida fixo de 10 minutos e transportam mensagens de tamanho fixo de 1024 bytes (1028 bytes incluindo o cabeçalho do túnel) para evitar análise de tráfego baseada em tamanho de mensagem ou padrões de temporização.

## Vocabulário de Tunnel

- **Tunnel gateway:** Primeiro router em um tunnel. Para tunnels de entrada (inbound), a identidade deste router aparece no [LeaseSet](/docs/specs/common-structures/) publicado. Para tunnels de saída (outbound), o gateway é o router de origem (A e D acima).
- **Tunnel endpoint:** Último router em um tunnel (C e F acima).
- **Tunnel participant:** Router intermediário em um tunnel (B e E acima). Os participantes não conseguem determinar sua posição ou a direção do tunnel.
- **n-hop tunnel:** Número de saltos entre routers.
  - **0-hop:** Gateway e endpoint são o mesmo router – anonimato mínimo.
  - **1-hop:** Gateway conecta diretamente ao endpoint – baixa latência, baixo anonimato.
  - **2-hop:** Padrão para tunnels exploratórios; segurança/desempenho equilibrados.
  - **3-hop:** Recomendado para aplicações que requerem anonimato forte.
- **Tunnel ID:** Inteiro de 4 bytes único por router e por salto, escolhido aleatoriamente pelo criador. Cada salto recebe e encaminha usando IDs diferentes.

## Informações de Construção de Túnel

Routers desempenhando funções de gateway, participante e endpoint recebem diferentes registros dentro da Mensagem de Construção de Túnel. O I2P moderno suporta dois métodos:

- **ElGamal** (legado, registros de 528 bytes)
- **ECIES-X25519** (atual, registros de 218 bytes via Short Tunnel Build Message – STBM)

### Information Distributed to Participants

**Gateway recebe:** - Chave da camada do túnel (chave AES-256 ou ChaCha20 dependendo do tipo de túnel) - Chave IV do túnel (para criptografar vetores de inicialização) - Chave de resposta e IV de resposta (para criptografia de resposta de construção) - ID do túnel (apenas gateways de entrada) - Hash de identidade do próximo salto e ID do túnel (se não-terminal)

**Participantes intermediários recebem:** - Chave da camada de túnel e chave IV para o seu salto - ID do túnel e informações do próximo salto - Chave de resposta e IV para criptografia da resposta de construção

**Os endpoints recebem:** - Chaves da camada de tunnel e IV - Router de resposta e ID do tunnel (apenas endpoints de saída) - Chave de resposta e IV (apenas endpoints de saída)

Para detalhes completos, consulte a [Especificação de Criação de Túnel](/docs/specs/implementation/) e a [Especificação de Criação de Túnel ECIES](/docs/specs/implementation/).

## Tunnel Pooling

Os routers agrupam túneis em **pools de túneis** para redundância e distribuição de carga. Cada pool mantém múltiplos túneis paralelos, permitindo failover quando um falha. Pools usados internamente são **exploratory tunnels**, enquanto pools específicos de aplicação são **client tunnels**.

Cada destino mantém pools de entrada e saída separados configurados pelas opções I2CP (contagem de túneis, contagem de backup, comprimento e parâmetros de QoS). Os roteadores monitoram a saúde dos túneis, executam testes periódicos e reconstroem túneis com falha automaticamente para manter o tamanho do pool.

## Agrupamento de Túneis

**Túneis de 0 saltos**: Oferecem apenas negação plausível. O tráfego sempre se origina e termina no mesmo router — desencorajado para qualquer uso anônimo.

**Túneis de 1 salto**: Fornecem anonimato básico contra observadores passivos, mas são vulneráveis se um adversário controlar esse único salto.

**Túneis de 2 saltos** : Incluem dois routers remotos e aumentam substancialmente o custo de ataque. Padrão para pools exploratórios.

**Túneis de 3 saltos**: Recomendado para aplicações que exigem proteção robusta de anonimato. Saltos extras adicionam latência sem ganho significativo de segurança.

**Padrões** : Os routers usam túneis exploratórios de **2 saltos** e túneis cliente específicos de aplicação de **2 ou 3 saltos**, equilibrando desempenho e anonimato.

## Comprimento do Túnel

Os routers testam periodicamente os tunnels enviando uma `DeliveryStatusMessage` através de um tunnel de saída para um tunnel de entrada. Se o teste falhar, ambos os tunnels recebem peso negativo no perfil. Falhas consecutivas marcam um tunnel como inutilizável; o router então reconstrói um substituto e publica um novo LeaseSet. Os resultados alimentam as métricas de capacidade de peers usadas pelo [sistema de seleção de peers](/docs/overview/tunnel-routing/).

## Teste de Túnel

Os routers constroem túneis usando um método **telescópico** não interativo: uma única Mensagem de Construção de Túnel se propaga salto a salto. Cada salto descriptografa seu registro, adiciona sua resposta e encaminha a mensagem adiante. O salto final retorna a resposta agregada de construção por um caminho diferente, prevenindo correlação. Implementações modernas usam **Short Tunnel Build Messages (STBM)** para ECIES e **Variable Tunnel Build Messages (VTBM)** para caminhos legados. Cada registro é criptografado por salto usando ElGamal ou ECIES-X25519.

## Criação de Túnel

O tráfego dos túneis usa criptografia multicamadas. Cada salto adiciona ou remove uma camada de criptografia conforme as mensagens atravessam o túnel.

- **Túneis ElGamal:** AES-256/CBC para payloads com preenchimento PKCS#5.
- **Túneis ECIES:** ChaCha20 ou ChaCha20-Poly1305 para criptografia autenticada.

Cada salto tem duas chaves: uma **chave de camada** e uma **chave IV**. Os routers descriptografam o IV, usam-no para processar a carga útil e depois criptografam novamente o IV antes de encaminhar. Este esquema duplo de IV previne a marcação de mensagens.

Os gateways de saída pré-descriptografam todas as camadas para que os endpoints recebam texto simples depois que todos os participantes adicionaram criptografia. Os túneis de entrada criptografam na direção oposta. Os participantes não conseguem determinar a direção ou o comprimento do túnel.

## Criptografia de Túnel

- Tempos de vida dinâmicos de túneis e dimensionamento adaptativo de pool para balanceamento de carga da rede
- Estratégias alternativas de teste de túneis e diagnósticos individuais de saltos
- Validação opcional de proof-of-work ou certificado de largura de banda (implementado na API 0.9.65+)
- Pesquisa sobre modelagem de tráfego e inserção de chaff para mistura de endpoints
- Aposentadoria contínua do ElGamal e migração para ECIES-X25519

## Desenvolvimento Contínuo

- [Especificação de Implementação de Tunnel](/docs/specs/implementation/)
- [Especificação de Criação de Tunnel (ElGamal)](/docs/specs/implementation/)
- [Especificação de Criação de Tunnel (ECIES-X25519)](/docs/specs/implementation/)
- [Especificação de Mensagem de Tunnel](/docs/specs/implementation/)
- [Garlic Routing](/docs/overview/garlic-routing/)
- [I2P Network Database](/docs/specs/common-structures/)
- [Criação de Perfis e Seleção de Pares](/docs/overview/tunnel-routing/)
- [Modelo de Ameaças do I2P](/docs/overview/threat-model/)
- [Criptografia ElGamal/AES + SessionTag](/docs/legacy/elgamal-aes/)
- [Opções I2CP](/docs/specs/i2cp/)
