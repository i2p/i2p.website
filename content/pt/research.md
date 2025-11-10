---
title: "Pesquisa Acadêmica"
description: "Informações e diretrizes para pesquisa acadêmica na rede I2P"
layout: "research"
aliases:
  - /en/research
  - /en/research/index
  - /en/research/questions
---

<div id="intro"></div>

## Pesquisa Acadêmica I2P

Há uma grande comunidade de pesquisa investigando uma ampla gama de aspectos da anonimato. Para que as redes de anonimato continuem a se aprimorar, acreditamos ser essencial compreender os problemas que estão sendo enfrentados. A pesquisa na rede I2P ainda está nos estágios iniciais, com grande parte do trabalho de pesquisa até agora focado em outras redes de anonimato. Isso apresenta uma oportunidade única para contribuições de pesquisa originais.

<div id="notes"></div>

## Notas para Pesquisadores

### Prioridades de Pesquisa Defensiva

Nós acolhemos pesquisas que nos ajudem a fortificar a rede e melhorar sua segurança. Testes que fortalecem a infraestrutura do I2P são encorajados e apreciados.

### Diretrizes de Comunicação de Pesquisa

Nós encorajamos fortemente que os pesquisadores comuniquem suas ideias de pesquisa cedo para a equipe de desenvolvimento. Isso ajuda:

- Evitar potencial sobreposição com projetos existentes
- Minimizar possíveis danos à rede
- Coordenar esforços de teste e coleta de dados
- Garantir que a pesquisa esteja alinhada com os objetivos da rede

<div id="ethics"></div>

## Ética de Pesquisa & Diretrizes de Teste

### Princípios Gerais

Ao conduzir pesquisas no I2P, por favor considere o seguinte:

1. **Avaliar benefícios vs. riscos da pesquisa** - Considere se os benefícios potenciais de sua pesquisa superam quaisquer riscos para a rede ou seus usuários
2. **Preferir rede de teste em vez de rede ao vivo** - Use a configuração de rede de teste do I2P sempre que possível
3. **Coletar apenas o mínimo necessário de dados** - Coletar apenas a quantidade mínima de dados necessária para sua pesquisa
4. **Garantir que os dados publicados respeitem a privacidade do usuário** - Quaisquer dados publicados devem ser anonimados e respeitar a privacidade do usuário

### Métodos de Teste de Rede

Para pesquisadores que precisam testar no I2P:

- **Usar configuração de rede de teste** - O I2P pode ser configurado para rodar em uma rede de teste isolada
- **Utilizar modo MultiRouter** - Executar múltiplas instâncias de roteadores em uma única máquina para testes
- **Configurar família de roteadores** - Tornar seus roteadores de pesquisa identificáveis configurando-os como uma família de roteadores

### Práticas Recomendadas

- **Contatar a equipe do I2P antes de testes na rede ao vivo** - Entre em contato conosco em research@i2p.net antes de conduzir quaisquer testes na rede ao vivo
- **Usar configuração de família de roteadores** - Isso torna seus roteadores de pesquisa transparentes para a rede
- **Prevenir interferência potencial na rede** - Projete seus testes para minimizar qualquer impacto negativo nos usuários regulares

<div id="questions"></div>

## Questões Abertas de Pesquisa

A comunidade I2P identificou várias áreas onde a pesquisa seria particularmente valiosa:

### Banco de Dados de Rede

**Floodfills:**
- Existem outras maneiras de mitigar ataques de força bruta na rede através de controle significativo de floodfill?
- Existe alguma maneira de detectar, sinalizar e potencialmente remover 'floodfills ruins' sem realmente precisar confiar em uma forma de autoridade central?

### Transportes

- Como as estratégias de retransmissão de pacotes e tempos de espera poderiam ser melhoradas?
- Há uma maneira do I2P obfuscar pacotes e reduzir a análise de tráfego de forma mais eficiente?

### Túneis e Destinos

**Seleção de Pares:**
- Existe uma maneira de o I2P realizar a seleção de pares de forma mais eficiente ou segura?
- Usar geoip para priorizar pares próximos impactaria negativamente na anonimidade?

**Túneis Unidirecionais:**
- Quais são os benefícios dos túneis unidirecionais sobre os túneis bidirecionais?
- Quais são as compensações entre túneis unidirecionais e bidirecionais?

**Multihoming:**
- Quão efetivo é o multihoming no balanceamento de carga?
- Como ele escala?
- O que acontece à medida que mais roteadores hospedam o mesmo Destino?
- Quais são as compensações de anonimidade?

### Roteamento de Mensagens

- Quanto a efetividade dos ataques de temporização é reduzida pela fragmentação e mistura de mensagens?
- Que estratégias de mistura o I2P poderia se beneficiar?
- Como técnicas de alta latência podem ser empregadas efetivamente dentro ou junto à nossa rede de baixa latência?

### Anonimidade

- Quão significativamente a impressão digital do navegador impacta a anonimidade dos usuários do I2P?
- Desenvolver um pacote de navegador beneficiaria usuários comuns?

### Relacionados à Rede

- Qual é o impacto geral na rede criado por 'usuários gananciosos'?
- Seriam valiosos passos adicionais para encorajar a participação em largura de banda?

<div id="contact"></div>

## Contato

Para consultas de pesquisa, oportunidades de colaboração ou para discutir seus planos de pesquisa, por favor entre em contato conosco em:

**Email:** research@i2p.net

Esperamos trabalhar com a comunidade de pesquisa para melhorar a rede I2P!