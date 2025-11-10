---
title: "Notas de status do I2P de 2006-01-10"
date: 2006-01-10
author: "jr"
description: "Atualização semanal abrangendo algoritmos de perfilamento de vazão, melhorias na visualização de blog no Syndie, progresso nas conexões persistentes HTTP e desenvolvimento do gwebcache do I2Phex"
categories: ["status"]
---

Oi pessoal, parece que terça-feira chegou de novo

* Index

1) Estado da rede 2) Perfilamento de throughput (taxa efetiva de transferência) 3) Blogs do Syndie 4) Conexões HTTP persistentes 5) gwebcache do I2Phex 6) ???

* 1) Net status

Na última semana houve muitas correções de bugs e melhorias acontecendo no CVS, com o build atual em 0.6.1.8-11. A rede tem estado razoavelmente estável, embora algumas quedas em diferentes provedores de serviços i2p tenham causado interrupções ocasionais. Finalmente nos livramos da rotatividade de identidade do router desnecessariamente alta no CVS, e há uma nova correção de bug no núcleo que o zzz apresentou ontem e que parece bastante promissora, mas teremos que esperar para ver como isso afeta as coisas. Outras duas grandes novidades da semana foram o novo perfilamento de velocidade baseado em throughput (taxa efetiva de transferência) e um trabalho importante na visualização de blog do Syndie. Quanto a quando veremos 0.6.1.9, deve sair ainda esta semana, no máximo no fim de semana. Fiquem atentos aos locais de sempre.

* 2) Throughput profiling

Testamos alguns novos algoritmos de perfilamento de pares para monitorar a taxa de transferência, mas na última semana, mais ou menos, parece que nos definimos por um que parece bastante bom. Essencialmente, ele monitora a taxa de transferência confirmada de tunnels individuais em períodos de 1 minuto, ajustando as estimativas de taxa de transferência para os pares em conformidade. Ele não tenta calcular uma taxa média para um par, pois isso é muito complicado, devido ao fato de que os tunnels incluem vários pares, bem como ao fato de que medições de taxa de transferência confirmada frequentemente exigem múltiplos tunnels. Em vez disso, ele calcula a média das taxas de pico - especificamente, mede as três taxas mais rápidas com que os tunnels do par foram capazes de transferir e faz a média delas.

O essencial é que essas taxas, por serem medidas ao longo de um minuto completo, são velocidades sustentadas que o par é capaz de suportar, e, como todo par é pelo menos tão rápido quanto a taxa medida de ponta a ponta, é seguro marcar cada um deles como sendo tão rápido. Nós tentamos outra variação disso - medir a taxa de transferência geral de um par através de tunnels em diferentes períodos, e isso ofereceu informações ainda mais claras sobre a taxa de pico, mas penalizava fortemente aqueles pares que ainda não estavam marcados como "fast", já que os "fast" são usados com muito mais frequência (client tunnels only use fast peers). O resultado dessa medição de taxa de transferência geral foi que ela coletou ótimos dados para aqueles suficientemente exigidos, mas apenas os pares "fast" estavam suficientemente exigidos e houve pouca exploração efetiva.

Usar períodos de 1 minuto e a taxa de transferência de um tunnel individual, no entanto, parece produzir valores mais razoáveis. Veremos este algoritmo implantado na próxima versão.

* 3) Syndie blogs

Com base em alguns comentários, foram feitas melhorias adicionais na visualização de blog do Syndie, conferindo-lhe um caráter nitidamente distinto da visualização encadeada, semelhante a grupos de notícias/fórum. Além disso, há um recurso totalmente novo para definir informações gerais do blog por meio da arquitetura do Syndie já existente. Como exemplo, confira a postagem padrão do blog "about Syndie":  http://syndiemedia.i2p.net/blog.jsp?blog=ovpBy2mpO1CQ7deYhQ1cDGAwI6pQzLbWOm1Sdd0W06c=&entry=ovpBy2mpO1CQ7deYhQ1cDGAwI6pQzLbWOm1Sdd0W06c=/1132012800001

Isso apenas arranha a superfície do que podemos fazer. A próxima versão permitirá definir o logotipo do seu próprio blog, seus próprios links (para blogs, posts, anexos e URLs externas arbitrárias) e, com sorte, ainda mais personalização. Uma dessas personalizações é ícones por tag - eu gostaria de distribuir um conjunto de ícones padrão para uso com tags padrão, mas as pessoas poderão definir ícones para suas próprias tags para uso em seus blogs, e até substituir os ícones padrão para as tags padrão (novamente, apenas quando as pessoas estiverem visualizando o blog delas, é claro). Talvez até alguma configuração de estilo para exibir posts com tags diferentes de forma diferente (claro, apenas personalizações de estilo muito específicas seriam permitidas - nada de exploits de CSS arbitrários com o Syndie, muito obrigado :)

Ainda há muito que eu gostaria de fazer com a visualização do blog que não estará na próxima versão, mas deve ser um bom pontapé inicial para levar as pessoas a explorarem algumas de suas capacidades, o que, com sorte, permitirá que *vocês* me mostrem do que precisam, em vez do que eu acho que vocês querem. Posso ser um bom programador, mas sou um péssimo vidente.

* 4) HTTP persistent connections

zzz é um maluco, estou te dizendo. Houve algum progresso em um recurso solicitado há muito tempo - suporte a conexões HTTP persistentes, permitindo enviar várias solicitações HTTP por um único stream, recebendo várias respostas em troca. Acho que alguém pediu isso pela primeira vez há uns dois anos, e isso pode ajudar com alguns tipos de eepsite(Site I2P) ou com bastante uso de outproxy (proxy de saída). Sei que o trabalho ainda não está concluído, mas está avançando. Tomara que zzz possa nos dar uma atualização de status durante a reunião.

* 5) I2Phex gwebcache

Tenho ouvido relatos de progresso em restaurar o suporte a gwebcache no I2Phex, mas não sei qual é a situação no momento. Talvez Complication possa nos dar uma atualização sobre isso esta noite?

* 6) ???

Há muita coisa acontecendo, como vocês podem ver, mas se houver outras coisas que vocês queiram comentar e discutir, passem na reunião daqui a alguns minutos e deem um alô. A propósito, um site bem legal que tenho acompanhado ultimamente é http://freedomarchive.i2p/ (para o pessoal preguiçoso que não tem o I2P instalado, vocês podem usar o inproxy do Tino via http://freedomarchive.i2p.tin0.de/). De qualquer forma, nos vemos daqui a poucos minutos.

=jr
