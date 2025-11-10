---
title: "Notas de status do I2P de 2005-08-02"
date: 2005-08-02
author: "jr"
description: "Atualização tardia abordando o status do lançamento da versão 0.6, o sistema PeerTest, introduções do SSU, correções na interface web do I2PTunnel e mnet sobre I2P"
categories: ["status"]
---

Oi, pessoal, anotações atrasadas hoje,

* Index:

1) status 0.6 2) PeerTest 3) introduções do SSU 4) interface web do I2PTunnel 5) mnet sobre i2p 6) ???

* 1) 0.6 status

Como todos viram, lançamos a versão 0.6 há alguns dias e, no geral, as coisas têm corrido bastante bem. Algumas das melhorias na camada de transporte desde a 0.5.* expuseram problemas na implementação do netDb, mas correções para grande parte disso estão em testes agora (como a build 0.6-1) e serão disponibilizadas como 0.6.0.1 muito em breve. Também nos deparamos com alguns problemas com diferentes configurações de NAT e firewall, bem como questões de MTU com alguns usuários — problemas que não estavam presentes na rede de testes menor devido ao menor número de testadores. Foram adicionadas soluções de contorno para os casos mais problemáticos, mas temos uma solução de longo prazo chegando em breve - testes de pares.

* 2) PeerTest

Com a 0.6.1, vamos implantar um novo sistema para testar e configurar, de forma colaborativa, os IPs públicos e as portas. Isso está integrado no núcleo do protocolo SSU e será compatível com versões anteriores. Essencialmente, ele permite que Alice pergunte a Bob qual é o IP público e o número da porta dela e, por sua vez, que Bob peça a Charlie para confirmar se a configuração dela está correta, ou para descobrir qual é a limitação que está impedindo a properation. A técnica não é nenhuma novidade na Internet, mas é uma nova adição à base de código do i2p e deve eliminar a maioria dos erros de configuração comuns.

* 3) SSU introductions

Conforme descrito na especificação do protocolo SSU, haverá funcionalidade para permitir que pessoas atrás de firewalls e NATs participem plenamente da rede, mesmo que, de outra forma, não pudessem receber mensagens UDP não solicitadas. Isso não funcionará para todas as situações possíveis, mas abrangerá a maioria. Há semelhanças entre as mensagens descritas na especificação do SSU e as mensagens necessárias para o PeerTest, então talvez, quando a especificação for atualizada com essas mensagens, possamos veicular as introduções junto com as mensagens do PeerTest. De qualquer forma, implementaremos essas introduções na 0.6.2, e isso também será compatível com versões anteriores.

* 4) I2PTunnel web interface

Algumas pessoas notaram e relataram várias peculiaridades na interface web do I2PTunnel, e smeghead começou a preparar as correções necessárias - talvez ele possa explicar essas atualizações com mais detalhes, bem como fornecer uma estimativa de prazo para elas?

* 5) mnet over i2p

Embora eu não tenha estado no canal quando as discussões estavam acontecendo, ao ler os logs parece que o icepick tem feito alguns hacks para colocar o mnet para funcionar sobre o i2p - permitindo que o armazenamento de dados distribuído do mnet ofereça publicação de conteúdo resiliente com operação anônima. Não sei muito sobre o progresso nessa frente, mas parece que o icepick está fazendo bons progressos na integração com o I2P por meio do SAM e do twisted, mas talvez o icepick possa nos esclarecer melhor?

* 6) ???

Ok, há muito mais acontecendo do que o mencionado acima, mas já estou atrasado, então acho melhor parar de digitar e enviar esta mensagem. Vou conseguir ficar online por um tempo esta noite, então, se alguém estiver por perto, podemos fazer uma reunião por volta das 21h30 (quando receberem isto ;) no #i2p nos servidores IRC de sempre {irc.duck.i2p, irc.postman.i2p, irc.freenode.net, irc.metropipe.net}.

Agradecemos a sua paciência e a ajuda para levar as coisas adiante!

=jr
