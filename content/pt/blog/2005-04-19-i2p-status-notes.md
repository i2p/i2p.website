---
title: "Notas de status do I2P para 2005-04-19"
date: 2005-04-19
author: "jr"
description: "Atualização semanal abrangendo as correções previstas para a versão 0.5.0.7, o progresso do transporte SSU UDP, alterações no roadmap (plano de desenvolvimento) que movem a versão 0.6 para junho e o desenvolvimento do Q"
categories: ["status"]
---

Olá, pessoal, chegou aquela hora da semana de novo,

* Index

1) Estado da rede 2) Estado do SSU 3) Atualização do roadmap (plano de desenvolvimento) 4) Estado de Q 5) ???

* 1) Net status

Ao longo das quase duas semanas desde que a 0.5.0.6 foi lançada, as coisas têm sido em geral positivas, embora provedores de serviço (eepsites(I2P Sites), ircd, etc) venham enfrentando alguns bugs recentemente. Embora os clientes estejam em bom estado, com o tempo um servidor pode deparar-se com uma situação em que tunnels com falha podem acionar algum código de limitação (throttling) excessivo, impedindo a devida reconstrução e publicação do leaseSet.

Houve algumas correções no CVS, entre outras coisas, e espero que tenhamos uma nova versão 0.5.0.7 disponível dentro de um dia ou dois.

* 2) SSU status

Para quem não acompanha meu (ah, tão empolgante) blog, houve muito progresso com o transporte UDP, e neste momento é relativamente seguro dizer que o transporte UDP não será nosso gargalo de taxa de transferência :) Enquanto depurava aquele código, aproveitei para trabalhar também no enfileiramento nos níveis superiores, identificando pontos onde podemos remover gargalos desnecessários. Como eu disse na semana passada, porém, ainda há muito trabalho a fazer. Mais informações estarão disponíveis quando houver mais informações disponíveis.

* 3) Roadmap update

Agora é abril, então o roadmap [1] foi atualizado de acordo - removendo 0.5.1 e ajustando algumas datas. A grande mudança ali é mover 0.6 de abril para junho, embora isso realmente não seja uma mudança tão grande quanto parece. Como mencionei na semana passada, minha própria agenda mudou um pouco e, em vez de me mudar para $somewhere em junho, vou me mudar para $somewhere em maio. Embora pudéssemos ter o necessário para 0.6 pronto este mês, de jeito nenhum vou lançar às pressas uma atualização importante como essa e depois desaparecer por um mês, já que a realidade do software é que haverá bugs não detectados nos testes.

[1] http://www.i2p.net/roadmap

* 4) Q status

Aum tem trabalhado intensamente no Q, adicionando mais novidades para nós, com as capturas de tela mais recentes no site dele [2]. Ele também fez commit do código no CVS (oba), então, com sorte, poderemos começar os testes alfa em breve. Tenho certeza de que ouviremos mais do aum com detalhes sobre como ajudar, ou você pode mergulhar nas novidades no CVS em i2p/apps/q/

[2] http://aum.i2p/q/

* 5) ???

Muita coisa tem acontecido também, com algumas discussões animadas na lista de discussão, no fórum e no irc. Não vou tentar resumi-las aqui, pois faltam apenas alguns minutos para a reunião, mas apareça por lá se houver algo que não foi discutido e que você queira trazer à tona!

=jr
