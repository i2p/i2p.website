---
title: "Notas de Status do I2P de 2004-09-14"
date: 2004-09-14
author: "jr"
description: "Atualização semanal de status do I2P abrangendo o lançamento da versão 0.4.0.1, atualizações do modelo de ameaças, melhorias no site, alterações no roadmap (plano de desenvolvimento) e necessidades de desenvolvimento de aplicações cliente"
categories: ["status"]
---

Olá, pessoal, chegou aquela hora da semana novamente

## Índice:

1. 0.4.0.1
2. Threat model updates
3. Website updates
4. Roadmap
5. Client apps
6. ???

## 1) 0.4.0.1

Desde o lançamento 0.4.0.1 da última quarta-feira, as coisas têm ido bastante bem na rede — mais de dois terços da rede já foi atualizada, e temos mantido entre 60 e 80 routers na rede. Os tempos de conexão ao IRC variam, mas, ultimamente, conexões de 4 a 12 horas têm sido normais. Houve alguns relatos de comportamentos estranhos ao iniciar no OS/X, porém acredito que também está sendo feito algum progresso nesse aspecto.

## 2) Atualizações do modelo de ameaças

Como mencionado em resposta ao post do Toni, houve uma reescrita bastante substancial do modelo de ameaças. A principal diferença é que, em vez da antiga forma de abordar as ameaças de maneira ad hoc, procurei seguir algumas das taxonomias propostas na literatura. O maior problema, para mim, foi encontrar maneiras de encaixar as técnicas reais que as pessoas podem usar nos padrões propostos - muitas vezes um único ataque se enquadrava em várias categorias diferentes. Sendo assim, não estou muito satisfeito com a forma como as informações naquela página são apresentadas, mas está melhor do que estava antes.

## 3) Atualizações do site

Graças à ajuda do Curiosity, começamos a implementar algumas atualizações no site — a mais visível pode ser vista na própria página inicial. Isso deve ajudar as pessoas que esbarram no I2P e querem saber de cara o que diabos é esse tal de I2P, em vez de terem que vasculhar as várias páginas. De qualquer forma, progresso, sempre em frente :)

## 4) Roteiro

Falando em progresso, finalmente montei um roteiro reformulado com base no que considero que precisamos implementar e no que deve ser realizado para atender às necessidades do usuário. As principais mudanças no roteiro antigo são:

- Drop AMOC altogether, replaced with UDP (however, we'll support TCP for those who can't use UDP *cough*mihi*cough*)
- Kept all of the restricted route operation to the 2.0 release, rather than bring in partial restricted routes earlier. I believe we'll be able to meet the needs of many users without restricted routes, though of course with them many more users will be able to join us. Walk before run, as they say.
- Pulled the streaming lib in to the 0.4.3 release, as we don't want to go 1.0 with the ~4KBps per stream limit. The bounty on this is still of course valid, but if no one claims it before 0.4.2 is done, I'll start working on it.
- TCP revamp moved to 0.4.1 to address some of our uglier issues (high CPU usage when connecting to people, the whole mess with "target changed identities", adding autodetection of IP address)

Os demais itens previstos para diversas versões 0.4.* já foram implementados. No entanto, há mais uma coisa que foi retirada do roteiro...

## 5) Aplicações cliente

Precisamos de aplicações cliente. Aplicações cativantes, seguras, escaláveis e anónimas. O I2P, por si só, não faz grande coisa; limita-se a permitir que dois pontos de extremidade comuniquem entre si de forma anónima. Embora o I2PTunnel de facto ofereça um verdadeiro canivete suíço, ferramentas desse tipo só são realmente apelativas para os entusiastas de tecnologia entre nós. Precisamos de mais do que isso - precisamos de algo que permita às pessoas fazer o que realmente querem fazer e que as ajude a fazê-lo melhor. Precisamos de um motivo para as pessoas utilizarem o I2P para além do simples facto de ser mais seguro.

Até agora tenho promovido o MyI2P para atender a essa necessidade — um sistema de blogs distribuído que oferece uma interface ao estilo do LiveJournal. Recentemente, discuti algumas das funcionalidades do MyI2P na lista. No entanto, retirei-o do roadmap, pois é trabalho demais para eu dar conta e ainda dedicar à rede I2P base a atenção de que ela precisa (já estamos no limite).

Há alguns outros aplicativos que prometem bastante. O Stasher forneceria uma infraestrutura significativa para armazenamento de dados distribuído, mas não tenho certeza de como isso está progredindo. Mesmo com o Stasher, no entanto, seria necessário haver uma interface do usuário atraente (embora alguns aplicativos FCP possam funcionar com ele).

IRC também é um sistema poderoso, embora tenha suas limitações devido à arquitetura baseada em servidor. oOo fez algum trabalho para avaliar a implementação de DCC transparente, então talvez o lado do IRC possa ser usado para bate-papo público e o DCC para transferências de arquivos privadas ou bate-papo sem servidor.

A funcionalidade geral de eepsite(I2P Site) também é importante, e o que temos agora é completamente insatisfatório. Como o DrWoo aponta, há riscos significativos ao anonimato com a configuração atual e, embora o oOo tenha feito algumas correções filtrando alguns cabeçalhos, há muito mais trabalho a ser feito antes que eepsites(I2P Sites) possam ser considerados seguros. Há algumas abordagens diferentes para tratar disso, todas as quais podem funcionar, mas todas exigem trabalho. Eu sei que o duck mencionou que tinha alguém trabalhando em algo, embora eu não saiba como isso está avançando ou se isso poderia ser incluído no I2P para todos usarem ou não. Duck?

Outro par de aplicativos cliente que poderia ajudar seria ou um aplicativo de transferência de arquivos do tipo swarming (no estilo do BitTorrent) ou um aplicativo de compartilhamento de arquivos mais tradicional (no estilo de DC/Napster/Gnutella/etc). É o que suspeito que muitas pessoas querem, mas há questões com cada um desses sistemas. No entanto, eles são bem conhecidos e portar pode não dar muito trabalho (talvez).

Ok, então o que foi dito acima não é nada de novo - por que eu mencionei tudo isso? Bem, precisamos encontrar uma forma de implementar uma aplicação cliente atraente, segura, escalável e anônima, e isso não vai acontecer por si só, do nada. Cheguei a aceitar que não vou conseguir fazer isso sozinho, então precisamos ser proativos e encontrar uma forma de realizá-lo.

Para isso, acho que nosso sistema de recompensas pode ajudar, mas creio que uma das razões pelas quais não vimos muita atividade nessa frente (pessoas trabalhando na implementação de uma recompensa) é que as pessoas estão sobrecarregadas, espalhadas por tarefas demais. Para obter os resultados de que precisamos, sinto que precisamos priorizar o que queremos e concentrar nossos esforços naquele item principal, aumentando o valor da recompensa para, com sorte, incentivar alguém a assumir e trabalhar na recompensa.

Minha opinião pessoal continua sendo que um sistema de blogs seguro e distribuído como o MyI2P seria o melhor. Em vez de simplesmente trafegar dados anonimamente de um lado para o outro, ele oferece uma forma de construir comunidades, que são essenciais para qualquer esforço de desenvolvimento. Além disso, oferece uma relação sinal-ruído relativamente alta, baixa probabilidade de abuso do bem comum e, em geral, uma carga leve na rede. Não oferece, no entanto, toda a riqueza dos sites normais, mas os 1,8 milhão de usuários ativos do LiveJournal não parecem se importar.

Depois disso, proteger a arquitetura de eepsite(I2P Site) seria minha próxima preferência, proporcionando aos navegadores a segurança de que necessitam e permitindo que as pessoas hospedem eepsites(I2P Sites) 'prontos para uso'.

A transferência de arquivos e o armazenamento distribuído de dados também são incrivelmente poderosos, mas não parecem ser tão voltados para a comunidade quanto provavelmente queremos para o primeiro aplicativo normal para o usuário final.

Quero que todos os aplicativos listados sejam implementados para ontem, assim como outros mil aplicativos que eu nem consigo começar a imaginar. Também quero paz mundial, o fim da fome, a destruição do capitalismo, estarmos livres do estatismo, do racismo, do sexismo, da homofobia, o fim da destruição pura e simples do meio ambiente e todas aquelas outras coisas nefastas. No entanto, somos poucas pessoas e só conseguimos fazer até certo ponto. Assim, precisamos priorizar e concentrar nossos esforços em alcançar o que pudermos, em vez de ficar parados, sobrecarregados com tudo o que queremos fazer.

Talvez possamos discutir algumas ideias sobre o que deveríamos fazer na reunião de hoje à noite.

## 6) ???

Bem, é tudo o que tenho por enquanto, e olha, consegui redigir as notas de status *antes* da reunião! Então, sem desculpas: apareça às 21h GMT e nos bombardeie a todos com suas ideias.

=jr
