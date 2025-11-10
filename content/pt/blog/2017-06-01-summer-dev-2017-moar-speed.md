---
title: "Dev de Verão do I2P 2017: Muito mais velocidade!"
date: 2017-06-01
author: "str4d"
description: "O Summer Dev deste ano terá como foco a coleta de métricas e melhorias de desempenho para a rede."
categories: ["summer-dev"]
---

Chegou novamente aquela época do ano! Estamos iniciando o nosso programa de desenvolvimento de verão, no qual nos concentramos em um aspecto específico do I2P para impulsioná-lo. Nos próximos três meses, incentivaremos tanto novos contribuidores quanto membros atuais da comunidade a escolherem uma tarefa e a divertirem-se com ela!

No ano passado, concentramos nossos esforços em ajudar usuários e desenvolvedores a aproveitar o I2P, melhorando as ferramentas de API e dando uma atenção especial às aplicações que rodam sobre o I2P. Neste ano, queremos melhorar a experiência do usuário trabalhando em um aspecto que afeta a todos: desempenho.

Apesar de as redes de onion-routing (roteamento em cebola) frequentemente serem chamadas de redes "baixa latência", há uma sobrecarga significativa criada ao rotear o tráfego através de computadores adicionais. O design de tunnel unidirecional do I2P significa que, por padrão, um percurso de ida e volta entre duas Destinations (destinos no I2P) envolverá doze participantes! Melhorar o desempenho desses participantes ajudará tanto a reduzir a latência das conexões ponta a ponta quanto a aumentar a qualidade dos tunnels em toda a rede.

## MAIS velocidade!

Nosso programa de desenvolvimento deste ano terá quatro componentes:

### Measure

Não temos como saber se melhoramos o desempenho sem uma linha de base!
Vamos criar um sistema de métricas para coletar dados de uso e desempenho sobre o I2P de forma que preserve a privacidade, bem como portar várias ferramentas de benchmarking para executar sobre o I2P (por exemplo, iperf3).

### Medir

Há bastante margem para melhorar o desempenho do nosso código existente, por exemplo, reduzindo a sobrecarga de participar em tunnels. Vamos avaliar melhorias potenciais em primitivas criptográficas, transportes de rede (tanto na camada de enlace quanto de ponta a ponta), perfilamento de pares e seleção de caminho de tunnel.

### Otimizar

Temos várias propostas em aberto para melhorar a escalabilidade da rede I2P (por exemplo, Prop115, Prop123, Prop124, Prop125, Prop138, Prop140). Trabalharemos nessas propostas e começaremos a implementar as que forem finalizadas nos diversos routers da rede.

### Avançar

I2P é uma rede comutada por pacotes, como a internet sobre a qual ela roda. Isso nos dá uma grande flexibilidade em como roteamos pacotes, tanto para desempenho quanto para privacidade. A maior parte dessa flexibilidade ainda não foi explorada! Queremos incentivar pesquisas sobre como várias técnicas de clearnet (internet aberta) para melhorar a largura de banda podem ser aplicadas ao I2P e como elas podem afetar a privacidade dos participantes da rede.

## Take part in Summer Dev!

Temos muitas outras ideias para coisas que gostaríamos de realizar nessas áreas. Se você tem interesse em hackear software de privacidade e anonimato, projetar protocolos (criptográficos ou não) ou pesquisar ideias para o futuro, venha conversar conosco no IRC ou no Twitter! Estamos sempre felizes em receber novos participantes em nossa comunidade. Também enviaremos adesivos do I2P a todos os novos colaboradores que participarem!

Vamos publicar aqui à medida que avançamos, mas você também pode acompanhar nosso progresso e compartilhar suas próprias ideias e trabalhos com a hashtag #I2PSummer no Twitter. Que venha o verão!
