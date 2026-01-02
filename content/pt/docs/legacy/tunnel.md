---
title: "Discussão sobre Tunnel"
description: "Exploração histórica do padding (preenchimento) de tunnel, da fragmentação de tunnel e das estratégias de construção de tunnel"
slug: "tunnel"
layout: "single"
lastUpdated: "2019-07"
accurateFor: "0.9.41"
reviewStatus: "needs-review"
---

> **Observação:** Este arquivo reúne trabalho de design especulativo anterior ao I2P 0.9.41. Para a implementação de produção, consulte a [documentação de tunnel](/docs/specs/implementation/).

## Alternativas de configuração

As ideias consideradas para futuros ajustes do tunnel incluíram:

- Limitadores de frequência para entrega de mensagens
- Políticas de preenchimento (incluindo injeção de chaff, ruído falso)
- Controles de vida útil de Tunnel
- Estratégias de lote e de fila para envio de carga útil

Nenhuma dessas opções foi incluída na implementação legada.

## Estratégias de preenchimento

Abordagens potenciais de preenchimento discutidas:

- Sem preenchimento
- Preenchimento de comprimento aleatório
- Preenchimento de comprimento fixo
- Preenchimento até o quilobyte mais próximo
- Preenchimento para potências de dois (`2^n` bytes)

Medições iniciais (versão 0.4) resultaram no tamanho fixo atual de 1024 bytes para mensagens de tunnel. Garlic messages (mensagens "garlic") de nível superior podem adicionar seu próprio preenchimento.

## Fragmentação

Para evitar ataques de marcação por meio do tamanho da mensagem, as mensagens de tunnel são fixadas em 1024 bytes. Cargas úteis I2NP maiores são fragmentadas pelo gateway (porta de entrada); o endpoint (ponto final) remonta os fragmentos dentro de um curto tempo limite. Routers podem reorganizar os fragmentos para maximizar a eficiência de empacotamento antes do envio.

## Alternativas adicionais

### Ajustar o processamento do Tunnel em trânsito

Três possibilidades foram examinadas:

1. Permitir que um salto intermediário encerre temporariamente um tunnel ao conceder acesso às cargas úteis descriptografadas.
2. Permitir que os routers participantes “remixem” mensagens, enviando-as por um dos seus próprios tunnels de saída antes de continuar para o próximo salto.
3. Permitir que o criador do tunnel redefina dinamicamente o próximo salto de um par.

### Tunnels Bidirecionais

Usar tunnels de entrada e de saída separados limita as informações que qualquer conjunto individual de pares pode observar (por exemplo, uma requisição GET vs. uma resposta grande). Tunnels bidirecionais simplificam o gerenciamento de pares, mas expõem padrões completos de tráfego em ambas as direções simultaneamente. Tunnels unidirecionais, portanto, permaneceram o design preferido.

### Canais de retorno e tamanhos variáveis

Permitir tamanhos variáveis de mensagens de tunnel possibilitaria canais encobertos entre pares em conluio (por exemplo, codificando dados por meio de tamanhos ou frequências selecionados). Mensagens de tamanho fixo mitigam esse risco ao custo de sobrecarga adicional de padding (preenchimento).

## Alternativas para a construção de Tunnel

Referência: [Hashing it out in Public](http://www-users.cs.umn.edu/~hopper/hashing_it_out.pdf)

### Método de Construção “Paralelo” Legado

Antes da versão 0.6.1.10, as solicitações de construção de tunnel eram enviadas em paralelo para cada participante. Esse método está documentado na [página antiga de tunnel](/docs/legacy/old-implementation/).

### Construção Telescópica em Um Único Passo (Método Atual)

A abordagem moderna envia mensagens de construção salto a salto através do tunnel parcialmente construído. Embora semelhante ao telescoping (técnica de construção incremental de circuitos) do Tor, rotear mensagens de construção através de tunnels exploratórios reduz o vazamento de informações.

### Telescopagem “interativa”

Construir um salto de cada vez com ciclos de ida e volta explícitos permite que os pares contem as mensagens e infiram sua posição no tunnel, portanto, essa abordagem foi rejeitada.

### Tunnels de gerenciamento não exploratórios

Uma proposta foi manter um pool separado de tunnels de gerenciamento para o tráfego de construção (build traffic). Embora pudesse ajudar routers particionados, considerou-se desnecessário com uma integração adequada à rede.

### Entrega Exploratória (Legado)

Antes da versão 0.6.1.10, solicitações individuais de tunnel eram garlic-encrypted e entregues via tunnels exploratórios, com as respostas retornando separadamente. Essa estratégia foi substituída pelo one-shot telescoping method (método telescópico de uma só vez) atual.

## Principais pontos

- Mensagens de tunnel de tamanho fixo protegem contra marcação baseada em tamanho e canais encobertos, apesar do custo adicional de preenchimento.
- Estratégias alternativas de preenchimento, fragmentação e construção foram exploradas, mas não adotadas quando ponderadas em relação aos compromissos de anonimato.
- O design de tunnel continua a equilibrar eficiência, observabilidade e resistência a ataques de predecessor e de congestionamento.
