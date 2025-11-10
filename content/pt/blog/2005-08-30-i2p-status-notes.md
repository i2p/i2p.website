---
title: "Notas de status do I2P de 2005-08-30"
date: 2005-08-30
author: "jr"
description: "Atualização semanal sobre o estado da rede 0.6.0.3 com problemas de NAT, implantação do floodfill netDb e progresso da internacionalização do Syndie"
categories: ["status"]
---

Oi, pessoal, chegou aquela hora da semana de novo

* Index

1) Estado da rede
2) floodfill netDb
3) Syndie
4) ???

* 1) Net status

Com a 0.6.0.3 disponível há uma semana, os relatos são bastante bons, embora o registro de logs e a exibição tenham sido bastante confusos para alguns. Até alguns minutos atrás, o I2P estava informando que um número considerável de pessoas configurou incorretamente seus NATs ou firewalls - de 241 pares, 41 viram o status mudar para ERR-Reject, enquanto 200 ficaram simplesmente OK (quando conseguem obter um status explícito). Isso não é bom, mas ajudou a focar um pouco mais no que precisa ser feito.

Desde o lançamento, houve algumas correções de erros de longa data, elevando o CVS HEAD atual para 0.6.0.3-4, que provavelmente será lançado como 0.6.0.4 ainda esta semana.

* 2) floodfill netDb

Como discutido [1] no meu blog [2], estamos experimentando um novo netDb retrocompatível que vai abordar tanto a situação de rotas restritas que estamos observando (20% dos routers) quanto simplificar um pouco as coisas. O floodfill netDb é implantado como parte da 0.6.0.3-4, sem qualquer configuração adicional, e basicamente funciona consultando primeiro o banco de dados floodfill antes de recorrer ao banco de dados Kademlia existente. Se algumas pessoas quiserem ajudar a testar, atualizem para a 0.6.0.3-4 e deem uma experimentada!

[1] http://syndiemedia.i2p.net/index.jsp?selector=entry://ovpBy2mpO1CQ7deYhQ1cDGAwI6pQzLbWOm1Sdd0W06c=/1125100800001 [2] http://syndiemedia.i2p.net/index.jsp?blog=ovpBy2mpO1CQ7deYhQ1cDGAwI6pQzLbWOm1Sdd0W06c=

* 3) Syndie

O desenvolvimento do Syndie está progredindo muito bem, com a sindicação remota completa em operação e otimizada para as necessidades do I2P (minimizando o número de requisições HTTP, em vez disso, agrupando os resultados e os envios em requisições HTTP POST multipart). A nova sindicação remota significa que você pode executar sua própria instância local do Syndie, lendo e publicando offline, e, depois, sincronizar seu Syndie com o de outra pessoa - baixando quaisquer novas publicações e enviando quaisquer publicações criadas localmente (seja em lote, por blog ou por publicação).

Um site público do Syndie é syndiemedia.i2p (também acessível na web em http://syndiemedia.i2p.net/), com seus arquivos públicos acessíveis em http://syndiemedia.i2p/archive/archive.txt (aponte o seu nó do Syndie para esse endereço para sincronizá-lo). A 'página inicial' desse syndiemedia foi filtrada para incluir apenas o meu blog, por padrão, mas você ainda pode acessar os outros blogs pelo menu suspenso e ajustar sua configuração padrão de acordo. (com o tempo, a configuração padrão do syndiemedia.i2p passará a ser um conjunto de publicações e blogs introdutórios, fornecendo um bom ponto de entrada para o syndie).

Um esforço ainda em andamento é a internacionalização da base de código do Syndie. Eu modifiquei minha cópia local para funcionar corretamente com qualquer conteúdo (qualquer conjunto de caracteres / locale (configuração regional) / etc.) em qualquer máquina (potencialmente com conjuntos de caracteres / locale / etc. diferentes), servindo os dados de forma limpa para que o navegador do usuário possa interpretá-los corretamente. No entanto, encontrei problemas com um componente do Jetty que o Syndie usa, pois a classe deles para lidar com requisições multipart internacionalizadas não é sensível ao conjunto de caracteres. Ainda ;)

De qualquer forma, isso significa que, assim que a parte de internacionalização estiver resolvida, o conteúdo e os blogs serão renderizáveis e editáveis em todos os idiomas (mas ainda não traduzidos, é claro). Até lá, porém, o conteúdo criado pode se corromper quando a internacionalização for concluída (já que há strings em UTF-8 dentro das áreas de conteúdo assinadas). Mas, ainda assim, sinta-se à vontade para experimentar, e espero terminar tudo hoje à noite ou amanhã.

Além disso, algumas ideias ainda no horizonte para o SML [3] incluem uma tag [torrent attachment="1"]my file[/torrent] que ofereceria uma maneira, com um único clique, de permitir que as pessoas iniciem o torrent anexado no seu cliente BT favorito (susibt, i2p-bt, azneti2p ou até mesmo um cliente BT não-I2P). Há demanda por outros tipos de ganchos (por exemplo, uma tag [ed2k]?), ou as pessoas têm ideias completamente diferentes e malucas para distribuir conteúdo no Syndie?

[3] http://syndiemedia.i2p.net/index.jsp?blog=ovpBy2mpO1CQ7deYhQ1cDGAwI6pQzLbWOm1Sdd0W06c=&entry=1124496000000

* 4) ???

De qualquer forma, há muita, muita coisa acontecendo, então apareça na reunião em 10 minutos em irc://irc.{postman,arcturus,freshcoffee}.i2p/#i2p ou freenode.net!

=jr
