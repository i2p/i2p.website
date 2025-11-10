---
title: "Notas de status do I2P de 2005-03-01"
date: 2005-03-01
author: "jr"
description: "Notas semanais sobre o estado do desenvolvimento do I2P abrangendo bugs da 0.5.0.1 e a próxima 0.5.0.2, atualizações do roteiro, editor do livro de endereços e atualizações do i2p-bt"
categories: ["status"]
---

Olá, pessoal, é hora da nossa atualização de status

* Index

1) 0.5.0.1 2) roteiro 3) editor e configuração do livro de endereços 4) i2p-bt 5) ???

* 1) 0.5.0.1

Como discutido na semana passada, algumas horas após a reunião publicamos a nova versão 0.5.0.1 corrigindo os bugs da 0.5 que haviam causado um número enorme de tunnels sendo construídos (entre outras coisas). De modo geral, esta revisão melhorou as coisas, mas, em testes mais amplos, encontramos alguns bugs adicionais que têm afetado algumas pessoas. Em particular, a revisão 0.5.0.1 pode devorar toneladas de CPU se você tiver uma máquina lenta ou se os tunnels do seu router falharem em massa, e alguns servidores I2PTunnel de longa duração podem devorar RAM até ocorrer OOM (falta de memória). Também há um bug de longa data na biblioteca de streaming, no qual podemos falhar ao estabelecer uma conexão se acontecer a combinação exata de falhas.

A maioria destes (entre outros) já foi corrigida no cvs, mas alguns ainda permanecem pendentes.  Assim que todos estiverem corrigidos, vamos empacotar e lançar como a versão 0.5.0.2.  Não tenho exatamente certeza de quando será; com sorte, esta semana, mas veremos.

* 2) roadmap

Após grandes lançamentos, o roadmap [1] parece acabar sendo... ajustado.  O lançamento 0.5 não foi diferente.  Essa página reflete o que considero razoável e apropriado para o caminho a seguir, mas, é claro, se mais pessoas se juntarem para ajudar com as tarefas, ela certamente pode ser ajustada.  Você notará o intervalo significativo entre 0.6 e 0.6.1 e, embora isso reflita muito trabalho, também reflete o fato de que vou me mudar (é aquela época do ano novamente).

[1] http://www.i2p.net/roadmap

* 3) addressbook editor and config

Detonate começou a trabalhar em uma interface web para gerenciar as entradas do livro de endereços (hosts.txt), e parece bastante promissora. Talvez possamos receber uma atualização do detonate durante a reunião?

Além disso, o smeghead tem trabalhado em uma interface baseada na web para gerenciar a configuração do livro de endereços (os subscriptions.txt, config.txt).  Talvez possamos obter uma atualização do smeghead durante a reunião?

* 4) i2p-bt

Houve algum progresso no i2p-bt, com uma nova versão 0.1.8 abordando os problemas de compatibilidade do azneti2p, conforme discutido na reunião da semana passada. Talvez possamos obter uma atualização do duck ou do smeghead durante a reunião?

Legion também criou um fork a partir do i2p-bt rev, mesclou algum outro código, corrigiu algumas coisas e tem um binário para Windows disponível em seu eepsite(I2P Site). O anúncio [2] parece sugerir que o código-fonte pode ser disponibilizado, embora ele não esteja no eepsite(I2P Site) no momento. Os desenvolvedores do I2P não auditaram (nem sequer viram) o código desse cliente, portanto, quem precisar de anonimato talvez queira obter e revisar uma cópia do código antes.

[2] http://forum.i2p.net/viewtopic.php?t=382

Também há trabalho em uma versão 2 do cliente BT do Legion, embora eu não saiba qual é o status disso. Talvez possamos obter uma atualização do Legion durante a reunião?

* 5) ???

É praticamente tudo o que tenho a dizer por enquanto, muita, muita coisa acontecendo.  Mais alguém trabalhando em algo sobre o qual talvez possamos obter uma atualização durante a reunião?

=jr
