---
title: "Notas de status do I2P de 2005-01-25"
date: 2005-01-25
author: "jr"
description: "Notas semanais de status do desenvolvimento do I2P cobrindo o progresso no roteamento de tunnel 0.5, porte do SAM para .NET, compilação com o GCJ e discussões sobre o transporte UDP"
categories: ["status"]
---

Hi y'all, quick weekly status update

* Index

1) 0.5 status 2) sam.net 3) progresso do gcj 4) udp 5) ???

* 1) 0.5 status

Ao longo da última semana, houve muito progresso no ramo 0.5. Os problemas de que estávamos falando antes foram resolvidos, simplificando drasticamente a criptografia e eliminando o problema de loop de tunnel. A nova técnica [1] foi implementada e os testes de unidade estão prontos. Em seguida, vou reunir mais código para integrar esses tunnels ao router principal, depois construir a infraestrutura de gerenciamento e de pooling (agrupamento) de tunnels. Depois que isso estiver no lugar, vamos passá-lo pelo simulador e, por fim, para uma rede paralela para fazer o burn-in (teste de estresse inicial) antes de dar os retoques finais e chamá-lo de 0.5.

[1] http://dev.i2p.net/cgi-bin/cvsweb.cgi/i2p/router/doc/tunnel-alt.html?rev=HEAD

* 2) sam.net

smeghead preparou um novo port do protocolo SAM para .net - compatível com c#, mono/gnu.NET (viva smeghead!).  Isso está no cvs em i2p/apps/sam/csharp/ com nant e outros auxiliares - agora todos vocês, devs de .net, podem começar a hackear com i2p :)

* 3) gcj progress

smeghead está definitivamente a todo vapor - na última contagem, com algumas modificações o router está compilando com a build mais recente do gcj [2] (w00t!). Ainda não funciona, mas as modificações para contornar a confusão do gcj com alguns construtos de classes internas são definitivamente um progresso. Talvez smeghead possa nos dar uma atualização?

[2] http://gcc.gnu.org/java/

* 4) udp

Não há muito a dizer aqui, embora Nightblade tenha levantado um conjunto interessante de preocupações [3] no fórum, perguntando por que estamos adotando o UDP. Se você tiver preocupações semelhantes ou outras sugestões sobre como podemos abordar as questões que abordei na minha resposta, por favor, participe!

[3] http://forum.i2p.net/viewtopic.php?t=280

* 5) ???

É, ok, estou atrasado com as anotações de novo, pode descontar do meu salário ;)  De qualquer forma, muita coisa acontecendo, então apareça no canal para a reunião, confira os logs publicados depois, ou poste na lista se tiver algo a dizer.  Ah, de passagem, acabei cedendo e comecei um blog dentro do i2p [4].

=jr [4] http://jrandom.dev.i2p/ (chave em http://dev.i2p.net/i2p/hosts.txt)
