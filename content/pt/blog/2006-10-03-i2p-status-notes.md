---
title: "Notas de status do I2P de 2006-10-03"
date: 2006-10-03
author: "jr"
description: "Network performance analysis, CPU bottleneck investigation, Syndie 1.0 release planning, and distributed version control evaluation"
categories: ["status"]
---

Oi, pessoal, notas de status atrasadas esta semana

* Index

1) Status da rede 2) Status de desenvolvimento do Router 3) Justificativa do Syndie (continuação) 4) Status de desenvolvimento do Syndie 5) Controle de versão distribuído 6) ???

* 1) Net status

Na última semana ou duas, o irc e outros serviços têm estado bastante estáveis, embora dev.i2p/squid.i2p/www.i2p/cvs.i2p tenham tido alguns percalços (devido a problemas temporários relacionados ao sistema operacional). As coisas parecem estar em um estado estável no momento.

* 2) Router dev status

O outro lado da discussão sobre o Syndie é "então, o que isso significa para o router?", e, para responder a isso, deixe-me explicar um pouco em que ponto se encontra o desenvolvimento do router neste momento.

Em geral, o que impede o router de chegar à versão 1.0, na minha opinião, é o seu desempenho, não as suas propriedades de anonimato. Certamente, há questões de anonimato a melhorar, mas, embora consigamos um desempenho bastante bom para uma rede anônima, nosso desempenho não é suficiente para um uso mais amplo. Além disso, melhorias no anonimato da rede não irão melhorar seu desempenho (na maioria dos casos que consigo imaginar, melhorias no anonimato reduzem a vazão e aumentam a latência). Precisamos resolver primeiro os problemas de desempenho, pois, se o desempenho for insuficiente, todo o sistema será insuficiente, independentemente de quão fortes sejam suas técnicas de anonimato.

Então, o que está prejudicando nosso desempenho? Por incrível que pareça, parece ser o uso da CPU. Antes de chegarmos ao motivo exato, primeiro um pouco mais de contexto.

 - to prevent partitioning attacks, we all need to plausibly build
   our tunnels from the same pool of routers.
 - to allow the tunnels to be of manageable length (and source
   routed), the routers in that pool must be directly reachable by
   anyone.
 - the bandwidth costs of receiving and rejecting tunnel join
   requests exceeds the capacity of dialup users on burst.

Portanto, precisamos de níveis de routers - alguns acessíveis globalmente com limites altos de largura de banda (tier A), outros não (tier B). Isso já foi, na prática, implementado por meio das informações de capacidade no netDb e, há um ou dois dias, a proporção de tier B para tier A estava em torno de 3 para 1 (93 routers de cap L, M, N ou O, e 278 de cap K).

Agora, basicamente há dois recursos escassos a serem gerenciados no nível A - largura de banda e CPU. A largura de banda pode ser gerenciada pelos meios usuais (dividir a carga entre um pool amplo, fazer com que alguns pares lidem com quantidades absurdas [por exemplo, aqueles com T3s], e rejeitar ou limitar tunnels e conexões individuais).

Gerenciar o uso de CPU é mais difícil. O principal gargalo de CPU observado em routers de nível A é a descriptografia de solicitações de construção de tunnel. Routers grandes podem ser (e são) completamente consumidos por essa atividade - por exemplo, a média histórica do tempo de descriptografia de tunnel em um dos meus routers é de 225ms, e a *média* histórica da frequência de descriptografia de solicitações de tunnel é de 254 eventos por 60 segundos, ou 4,2 por segundo. Basta multiplicar os dois e isso mostra que 95% da CPU é consumida apenas pela descriptografia de solicitações de tunnel (e isso não leva em consideração os picos na contagem de eventos). Esse router ainda assim de alguma forma consegue participar de 4-6000 tunnels ao mesmo tempo, aceitando aproximadamente 80% das solicitações descriptografadas.

Infelizmente, como a CPU nesse router está tão sobrecarregada, ela precisa descartar um número significativo de solicitações de construção de tunnel antes mesmo que possam ser descriptografadas (caso contrário, as solicitações ficariam na fila por tanto tempo que, mesmo que fossem aceitas, o solicitante original as teria considerado perdidas ou sobrecarregadas demais para fazer qualquer coisa de qualquer forma). À luz disso, a taxa de aceitação de 80% do router parece muito pior - ao longo de sua vida útil, ele descriptografou cerca de 250k solicitações (ou seja, cerca de 200k foram aceitas), mas teve de descartar cerca de 430k solicitações na fila de descriptografia devido à sobrecarga da CPU (transformando aquela taxa de aceitação de 80% em 30%).

As soluções parecem estar no sentido de reduzir o custo de CPU relevante para a descriptografia de solicitações de tunnel. Se reduzirmos o tempo de CPU em uma ordem de grandeza, isso aumentaria substancialmente a capacidade do router de nível A, reduzindo, assim, as rejeições (tanto explícitas quanto implícitas, devido a solicitações descartadas). Isso, por sua vez, aumentaria a taxa de sucesso da construção de tunnel, reduzindo, assim, a frequência de expirações de lease (autorização temporária de uso do tunnel), o que então reduziria a carga de largura de banda na rede devido à reconstrução de tunnel.

Um método para fazer isso seria alterar as solicitações de construção de tunnel de 2048bit Elgamal para, digamos, 1024bit ou 768bit. O problema, porém, é que, se você quebrar a criptografia de uma mensagem de solicitação de construção de tunnel, você conhece todo o caminho do tunnel. Mesmo que seguíssemos por esse caminho, quanto isso nos ajudaria? Uma melhoria de uma ordem de grandeza no tempo de descriptografia poderia ser anulada por um aumento de uma ordem de grandeza na proporção de tier B para tier A (também conhecido como o problema dos free riders), e então ficaríamos sem saída, já que não há como migrarmos para 512 ou 256bit Elgamal (e conseguirmos nos olhar no espelho ;)

Uma alternativa seria usar criptografia mais fraca, mas abrir mão da proteção contra ataques de contagem de pacotes que adicionamos com o novo processo de construção de tunnel. Isso nos permitiria usar chaves negociadas inteiramente efêmeras em um tunnel telescópico semelhante ao Tor (embora, novamente, exporia o criador do tunnel a ataques passivos triviais de contagem de pacotes que identificam um serviço).

Outra ideia é publicar e usar informações de carga ainda mais explícitas no netDb, permitindo que os clientes detectem com mais precisão situações como a mencionada acima, em que um router de alta largura de banda descarta 60% de suas mensagens de solicitação de tunnel sem sequer olhá-las. Há alguns experimentos que valem a pena nessa direção, e eles podem ser realizados com retrocompatibilidade total, portanto devemos vê-los em breve.

Então, esse é o gargalo no router/rede como vejo hoje. Todas e quaisquer sugestões sobre como podemos lidar com isso serão muito bem-vindas.

* 3) Syndie rationale continued

Há uma postagem substancial no fórum sobre o Syndie e qual é o seu lugar no ecossistema - confira em <http://forum.i2p.net/viewtopic.php?t=1910>

Além disso, gostaria apenas de destacar dois trechos da documentação do Syndie em elaboração. Primeiro, do irc (e da FAQ que ainda não está disponível):

<bar> uma pergunta em que tenho pensado é: quem, no futuro, vai ter coragem suficiente para hospedar os servidores/repositórios de produção do Syndie?
<bar> eles não vão ser tão fáceis de rastrear quanto os eepsites(I2P Sites) são hoje?
<jrandom> repositórios públicos do Syndie não têm a capacidade de *ler* o conteúdo publicado nos fóruns, a menos que os fóruns publiquem as chaves para isso
<jrandom> e veja o segundo parágrafo de usecases.html
<jrandom> claro, aqueles que hospedarem repositórios e receberem ordens legais para remover um fórum provavelmente o farão
<jrandom> (mas então as pessoas podem migrar para outro repositório, sem interromper o funcionamento do fórum)
<void> sim, você deveria mencionar que a migração para um meio diferente será transparente
<bar> se o meu repositório fechar, posso enviar meu fórum inteiro para um novo, certo?
<jrandom> isso mesmo, bar
<void> eles podem usar dois métodos ao mesmo tempo durante a migração
<void> e qualquer um pode sincronizar os meios
<jrandom> isso mesmo, void

A seção relevante do (ainda não publicado) Syndie usecases.html é:

Embora muitos grupos diferentes frequentemente queiram organizar discussões em um fórum online, a natureza centralizada dos fóruns tradicionais (sites, BBSes, etc) pode ser um problema. Por exemplo, o site que hospeda o fórum pode ser tirado do ar por meio de ataques de negação de serviço ou por ação administrativa. Além disso, um único servidor oferece um ponto simples para monitorar a atividade do grupo, de modo que, mesmo que um fórum use pseudônimos, esses pseudônimos podem ser vinculados ao IP que publicou ou leu mensagens individuais.

Além disso, não apenas os fóruns são descentralizados, eles são organizados de forma ad hoc e ainda assim totalmente compatíveis com outras técnicas de organização. Isso significa que um pequeno grupo de pessoas pode operar seu fórum usando uma técnica (distribuindo as mensagens ao colá-las em um site wiki), outro pode operar seu fórum usando outra técnica (postando suas mensagens em uma tabela hash distribuída como o OpenDHT, ainda assim, se uma pessoa conhecer ambas as técnicas, ela pode sincronizar os dois fóruns. Isso permite que as pessoas que só conheciam o site wiki conversem com pessoas que só conheciam o serviço OpenDHT sem saberem nada umas sobre as outras. Levado ainda mais longe, Syndie permite que células individuais controlem sua própria exposição enquanto se comunicam por toda a organização.

* 4) Syndie dev status

Tem havido muito progresso no Syndie ultimamente, com 7 versões alfa distribuídas a pessoas no canal de IRC. A maioria dos principais problemas na interface scriptável foi resolvida, e espero que possamos lançar o Syndie 1.0 ainda este mês.

Eu acabei de dizer "1.0"? Pode apostar! Embora o Syndie 1.0 seja um aplicativo baseado em texto e sua usabilidade nem chegue a ser comparável à de outros aplicativos semelhantes baseados em texto (como mutt ou tin), ele fornecerá a gama completa de funcionalidades, permitirá estratégias de sindicação via HTTP e baseadas em arquivos e, com sorte, demonstrará a potenciais desenvolvedores as capacidades do Syndie.

No momento, estou planejando provisoriamente um lançamento do Syndie 1.1 (permitindo que as pessoas organizem melhor seus acervos e hábitos de leitura) e talvez um lançamento 1.2 para integrar alguma funcionalidade de busca (tanto buscas simples quanto talvez as buscas de texto completo do Lucene). O Syndie 2.0 provavelmente será o primeiro lançamento com GUI (interface gráfica do usuário), com o plug-in do navegador chegando com a 3.0. O suporte a acervos adicionais e redes de distribuição de mensagens virá à medida que forem implementados, é claro (freenet, mixminion/mixmaster/smtp, opendht, gnutella, etc).

Percebo, porém, que o Syndie 1.0 não será o divisor de águas que alguns desejam, pois aplicativos baseados em texto são realmente para usuários mais técnicos, mas gostaria de tentar nos livrar do hábito de ver a "1.0" como um lançamento final e, em vez disso, considerá-la um começo.

* 5) Distributed version control

Até agora, tenho mexido com o Subversion como o sistema de controle de versão do Syndie, embora eu só seja realmente fluente em CVS e ClearCase. Isso porque fico offline a maior parte do tempo e, mesmo quando estou online, a conexão discada é lenta, então o diff/revert/etc local do Subversion tem sido bastante útil. No entanto, ontem o void me sugeriu que, em vez disso, considerássemos um dos sistemas distribuídos.

Dei uma olhada neles há alguns anos, ao avaliar um VCS (sistema de controle de versão) para o I2P, mas os descartei porque não precisava da funcionalidade offline deles (na época eu tinha bom acesso à rede), então não valia a pena aprendê-los. Isso não é mais o caso, então estou analisando-os um pouco mais agora.

- From what I can see, darcs, monotone, and codeville are the top

candidatos, e o sistema de controle de versão (vcs) baseado em patches do darcs parece particularmente atraente. Por exemplo, posso fazer todo o meu trabalho localmente e apenas fazer scp dos diffs gzip'ed & gpg'ed para um diretório do apache em dev.i2p.net, e as pessoas podem contribuir com suas próprias alterações publicando seus diffs gzip'ed e gpg'ed em locais de sua escolha. Quando chegar a hora de atribuir uma tag a uma versão, eu faria um darcs diff que especifica o conjunto de patches contidos na versão e enviaria esse diff .gz'ed/.gpg'ed como os outros (além de disponibilizar os arquivos tar.bz2, .exe e .zip reais, é claro ;)

E, como um ponto particularmente interessante, esses diffs compactados com gzip e/ou criptografados com gpg podem ser publicados como anexos em mensagens do Syndie, permitindo que o Syndie se auto-hospede.

Por acaso alguém tem experiência com essas coisas? Alguma dica?

* 6) ???

Apenas 24 telas cheias de texto desta vez (incluindo a publicação no fórum) ;) Infelizmente não consegui ir à reunião, mas, como sempre, gostaria muito de ouvir de vocês se tiverem alguma ideia ou sugestão - é só publicar na lista, no fórum ou aparecer no IRC.

=jr
