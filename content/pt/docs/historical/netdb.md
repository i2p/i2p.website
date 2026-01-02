---
title: "Discussão sobre o Banco de Dados da Rede"
description: "Notas históricas sobre floodfill, experimentos com Kademlia (protocolo de tabela de hash distribuída), e ajustes futuros para o netDb"
slug: "netdb"
reviewStatus: "needs-review"
---

> **Observação:** Esta discussão arquivada descreve abordagens históricas para o banco de dados da rede (netDb). Consulte a [documentação principal do netDb](/docs/specs/common-structures/) para conhecer o comportamento atual e as orientações.

## Histórico

A netDb do I2P é distribuída usando um algoritmo floodfill simples. Versões iniciais também mantinham uma implementação de Kademlia DHT (tabela de hash distribuída Kademlia) como alternativa, mas ela se mostrou pouco confiável e foi completamente desativada na versão 0.6.1.20. O design floodfill encaminha uma entrada publicada para um router participante, aguarda confirmação e tenta novamente com outros pares floodfill, se necessário. Pares floodfill difundem mensagens de armazenamento de routers não-floodfill para todos os demais participantes floodfill.

No final de 2009, as consultas Kademlia foram parcialmente reintroduzidas para reduzir a carga de armazenamento em floodfill routers individuais.

### Introdução ao Floodfill (nó especial da netDb que armazena e difunde entradas)

Floodfill surgiu pela primeira vez na versão 0.6.0.4, enquanto Kademlia permaneceu disponível como opção de backup. Na época, a alta perda de pacotes e as rotas restritas dificultavam a obtenção de confirmações de recebimento dos quatro pares mais próximos, frequentemente exigindo dezenas de tentativas redundantes de armazenamento. Migrar para um subconjunto floodfill de routers acessíveis externamente forneceu uma solução pragmática de curto prazo.

### Repensando Kademlia

Algumas alternativas consideradas incluíam:

- Executar o netDb como uma Kademlia DHT (tabela hash distribuída Kademlia) limitada a routers alcançáveis que optem por participar
- Manter o modelo floodfill, mas limitar a participação a routers capazes e verificar a distribuição com verificações aleatórias

A abordagem floodfill prevaleceu porque era mais fácil de implantar e a netDb transporta apenas metadados, não dados de usuário. A maioria dos destinos nunca publica um LeaseSet porque o remetente normalmente agrega o seu LeaseSet em garlic messages (mensagens compostas no I2P).

## Estado Atual (Perspectiva Histórica)

Os algoritmos do netDb estão ajustados às necessidades da rede e historicamente deram conta confortavelmente de algumas centenas de routers. Estimativas iniciais sugeriam que 3–5 floodfill routers poderiam suportar cerca de 10.000 nós.

### Cálculos Atualizados (Março de 2008)

```
recvKBps = N * (L + 1) * (1 + F) * (1 + R) * S / T
```
Onde:

- `N`: Routers na rede
- `L`: Número médio de destinos de cliente por router (mais um para o `RouterInfo`)
- `F`: Percentual de falhas de Tunnel
- `R`: Período de reconstrução do Tunnel como fração da vida útil do tunnel
- `S`: Tamanho médio de entrada no netDb
- `T`: Vida útil do Tunnel

Usando valores de 2008 (`N = 700`, `L = 0.5`, `F = 0.33`, `R = 0.5`, `S = 4 KB`, `T = 10 minutes`) produz:

```
recvKBps ≈ 700 * (0.5 + 1) * (1 + 0.33) * (1 + 0.5) * 4 KB / 10m ≈ 28 KBps
```
### Kademlia voltará?

Os desenvolvedores discutiram reintroduzir Kademlia (um protocolo DHT) por volta do início de 2007. O consenso foi que a capacidade de floodfill poderia ser ampliada incrementalmente conforme necessário, enquanto Kademlia acrescentava complexidade significativa e requisitos de recursos para a população básica de routers. O fallback (mecanismo de reserva) permanece inativo, a menos que a capacidade de floodfill se torne insuficiente.

### Planejamento de Capacidade do Floodfill

A inclusão automática de routers de classe de largura de banda `O` no floodfill, embora tentadora, implica riscos de cenários de negação de serviço se nós hostis aderirem. Análises históricas sugeriram que limitar o pool de floodfill (por exemplo, 3–5 pares lidando com ~10K routers) era mais seguro. Operadores confiáveis ou heurísticas automáticas têm sido utilizados para manter um conjunto de floodfill adequado, porém controlado.

## Floodfill TODO (Histórico)

> Esta seção é mantida para a posteridade. A página principal do netDb acompanha o roteiro atual e as considerações de design.

Incidentes operacionais, como um período em 13 de março de 2008 com apenas um floodfill router disponível, levaram a várias melhorias entregues entre as versões 0.6.1.33 e 0.7.x, incluindo:

- Aleatorizando a seleção de floodfill para buscas e priorizando pares responsivos
- Exibindo métricas adicionais de floodfill na página "Profiles" do console do router
- Reduções progressivas no tamanho das entradas do netDb para reduzir o uso de largura de banda do floodfill
- Opt-in automático para um subconjunto de routers de classe `O`, com base no desempenho coletado por meio de dados de perfil
- Aprimoramentos em listas de bloqueio, na seleção de pares de floodfill e nas heurísticas de exploração

As ideias remanescentes do período incluíam:

- Usando estatísticas de `dbHistory` para avaliar e selecionar melhor pares floodfill (routers que mantêm e distribuem a netDb)
- Melhorando o comportamento de novas tentativas para evitar contatar repetidamente pares com falhas
- Tirando partido de métricas de latência e pontuações de integração na seleção
- Detectando e reagindo mais rapidamente a routers floodfill com falhas
- Continuando a reduzir as exigências de recursos em nós de alta largura de banda e floodfill

Mesmo na data destas notas, a rede era considerada resiliente, com infraestrutura pronta para responder rapidamente a floodfills (routers especiais que mantêm e propagam a netDb) hostis ou a ataques de negação de serviço direcionados contra floodfill.

## Notas adicionais

- A console do router há muito tempo exibe dados de perfil aprimorados para ajudar na análise da confiabilidade do floodfill.
- Embora comentários históricos tenham especulado sobre Kademlia ou esquemas de DHT (tabela hash distribuída) alternativos, o floodfill tem permanecido o algoritmo principal para redes de produção.
- A pesquisa prospectiva concentrou-se em tornar a admissão ao floodfill adaptativa, ao mesmo tempo em que limita as oportunidades de abuso.
