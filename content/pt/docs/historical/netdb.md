---
title: "Discussão da Base de Dados de Rede"
description: "Notas históricas sobre floodfill, experimentos Kademlia e ajustes futuros para o netDb"
slug: "netdb"
aliases:
  - "/pt/docs/legacy/netdb"
  - "/pt/docs/legacy/netdb/"
  - "/pt/netdb_discussion"
  - "/pt/netdb_discussion/"
lastUpdated: "2008-03"
accurateFor: "0.7"
---

NOTA: O que segue é uma discussão sobre o histórico da implementação do netdb e não são informações atuais. Consulte [a página principal do netdb](/docs/overview/network-database) para documentação atual.

## Histórico {#status}

O netDb é distribuído com uma técnica simples chamada "floodfill". Há muito tempo, o netDb também usava o Kademlia DHT como algoritmo de reserva. No entanto, não funcionou bem em nossa aplicação e foi completamente desabilitado na versão 0.6.1.20.

*(Adaptado de um post de jrandom no antigo Syndie, 26 de novembro de 2005)*

O floodfill netDb é realmente apenas uma medida simples e talvez temporária, usando o algoritmo mais simples possível - enviar os dados para um peer no floodfill netDb, aguardar 10 segundos, escolher um peer aleatório no netDb e pedir-lhes a entrada a ser enviada, verificando sua inserção/distribuição adequada. Se o peer de verificação não responder, ou não tiver a entrada, o remetente repete o processo. Quando o peer no floodfill netDb recebe um armazenamento netDb de um peer que não está no floodfill netDb, eles enviam para todos os peers no floodfill netDb.

Em certo ponto, a funcionalidade de busca/armazenamento Kademlia ainda estava em vigor. Os peers consideravam os floodfill peers como estando sempre 'mais próximos' de cada chave do que qualquer peer que não participasse do netDb. Recorríamos ao netDb Kademlia se os floodfill peers falhassem por alguma razão. No entanto, o Kademlia foi então completamente desabilitado (veja abaixo).

Mais recentemente, o Kademlia foi parcialmente reintroduzido no final de 2009, como uma forma de limitar o tamanho do netDb que cada router floodfill deve armazenar.

### A Introdução do Algoritmo Floodfill

O floodfill foi introduzido na versão 0.6.0.4, mantendo o Kademlia como algoritmo de backup.

*(Adaptado de posts do jrandom no antigo Syndie, 26 de novembro de 2005)*

Como eu sempre disse, não estou particularmente vinculado a nenhuma tecnologia específica - o que importa para mim é o que trará resultados. Enquanto tenho trabalhado em várias ideias de netDb nos últimos anos, os problemas que enfrentamos nas últimas semanas trouxeram algumas delas à tona. Na rede ativa, com o fator de redundância do netDb definido para 4 peers (significando que continuamos enviando uma entrada para novos peers até que 4 deles confirmem que a receberam) e o timeout por peer definido para 4 vezes o tempo médio de resposta daquele peer, **ainda** estamos obtendo uma média de 40-60 peers enviados antes que 4 confirmem o armazenamento. Isso significa enviar 36-56 vezes mais mensagens do que deveria sair, cada uma usando tunnels e assim atravessando 2-4 links. Além disso, esse valor está fortemente distorcido, já que o número médio de peers enviados em um armazenamento 'falho' (significando que menos de 4 pessoas confirmaram a mensagem após 60 segundos de envio de mensagens) estava na faixa de 130-160 peers.

Isto é insano, especialmente para uma rede com apenas talvez 250 peers.

A resposta mais simples seria dizer "bem, obviamente jrandom, está quebrado. conserte isso", mas isso não chega ao cerne da questão. Alinhado com outro esforço atual, é provável que tenhamos um número substancial de problemas de rede devido a rotas restritas - peers que não conseguem se comunicar com alguns outros peers, frequentemente devido a problemas de NAT ou firewall. Se, digamos, os K peers mais próximos de uma entrada netDb específica estiverem atrás de uma 'rota restrita' de tal forma que a mensagem de armazenamento netDb possa alcançá-los, mas a mensagem de consulta netDb de algum outro peer não possa, essa entrada seria essencialmente inacessível. Seguindo essas linhas um pouco mais adiante e levando em consideração o fato de que algumas rotas restritas serão criadas com intenção hostil, fica claro que vamos ter que examinar mais de perto uma solução netDb de longo prazo.

Existem algumas alternativas, mas duas merecem menção particular. A primeira é simplesmente executar o netDb como um Kademlia DHT usando um subconjunto da rede completa, onde todos esses peers são alcançáveis externamente. Peers que não estão participando do netDb ainda consultam esses peers, mas não recebem mensagens não solicitadas de armazenamento ou busca do netDb. A participação no netDb seria tanto de auto-seleção quanto de eliminação pelo usuário - routers escolheriam se devem publicar uma flag em seu routerInfo indicando se querem participar, enquanto cada router escolhe quais peers deseja tratar como parte do netDb (peers que publicam essa flag mas nunca fornecem dados úteis seriam ignorados, essencialmente eliminando-os do netDb).

Outra alternativa é uma explosão do passado, voltando à mentalidade DTSTTCPW (Do The Simplest Thing That Could Possibly Work - Faça a Coisa Mais Simples Que Possivelmente Funcione) - um floodfill netDb, mas como a alternativa acima, usando apenas um subconjunto da rede completa. Quando um usuário quer publicar uma entrada no floodfill netDb, ele simplesmente a envia para um dos routers participantes, espera por um ACK, e então 30 segundos depois, consulta outro participante aleatório no floodfill netDb para verificar se foi distribuída adequadamente. Se foi, ótimo, e se não foi, apenas repete o processo. Quando um floodfill router recebe um netDb store, ele envia ACK imediatamente e coloca em fila o netDb store para todos os seus pares netDb conhecidos. Quando um floodfill router recebe um netDb lookup, se eles têm os dados, respondem com eles, mas se não têm, respondem com os hashes para, digamos, 20 outros pares no floodfill netDb.

Olhando sob uma perspectiva de economia de rede, o floodfill netDb é bastante similar ao netDb de transmissão original, exceto que o custo para publicar uma entrada é suportado principalmente pelos peers no netDb, em vez do publicador. Desenvolvendo isso um pouco mais e tratando o netDb como uma caixa preta, podemos ver que a largura de banda total exigida pelo netDb é:

```
recvKBps = N * (L + 1) * (1 + F) * (1 + R) * S / T
```
onde:

```
N = number of routers in the entire network
L = average number of client destinations on each router
    (+1 for the routerInfo)
F = tunnel failure percentage
R = tunnel rebuild period, as a fraction of the tunnel lifetime
S = average netDb entry size
T = tunnel lifetime
```
Substituindo alguns valores:

```
recvKBps = 1000 * (5 + 1) * (1 + 0.05) * (1 + 0.2) * 2KB / 10m
         = 25.2KBps
```
Isso, por sua vez, escala linearmente com N (com 100.000 peers, o netDb deve ser capaz de lidar com mensagens de armazenamento do netDb totalizando 2,5MBps, ou, com 300 peers, 7,6KBps).

Embora o floodfill netDb faria com que cada participante do netDb recebesse apenas uma pequena fração dos armazenamentos de netDb gerados pelo cliente diretamente, todos receberiam todas as entradas eventualmente, então todos os seus links deveriam ser capazes de lidar com o recvKBps completo. Por sua vez, todos precisariam enviar `(recvKBps/sizeof(netDb)) * (sizeof(netDb)-1)` para manter os outros peers sincronizados.

Um floodfill netDb não exigiria nem roteamento de tunnel para operação do netDb nem qualquer seleção especial sobre quais entradas pode responder "com segurança", já que a suposição básica é que todos estão armazenando tudo. Ah, e com relação ao uso de disco do netDb necessário, ainda é bastante trivial para qualquer máquina moderna, exigindo cerca de 11MB para cada 1000 peers `(N * (L + 1) * S)`.

O netDb Kademlia reduziria esses números, idealmente trazendo-os para K sobre M vezes seu valor, com K = o fator de redundância e M sendo o número de roteadores no netDb (por exemplo, 5/100, dando um recvKBps de 126KBps e 536MB com 100.000 roteadores). A desvantagem do netDb Kademlia, no entanto, é a maior complexidade de operação segura em um ambiente hostil.

O que estou pensando agora é simplesmente implementar e implantar um floodfill netDb em nossa rede ativa existente, permitindo que peers que queiram usá-lo escolham outros peers que estão marcados como membros e os consultem em vez de consultar os peers tradicionais do Kademlia netDb. Os requisitos de largura de banda e disco nesta fase são triviais o suficiente (7,6KBps e 3MB de espaço em disco) e isso removerá completamente o netDb do plano de depuração - problemas que permanecerem a serem resolvidos serão causados por algo não relacionado ao netDb.

Como seriam escolhidos os peers para publicar essa flag dizendo que fazem parte do floodfill netDb? No início, isso poderia ser feito manualmente como uma opção de configuração avançada (ignorada se o router não conseguir verificar sua acessibilidade externa). Se muitos peers definirem essa flag, como os participantes do netDb escolhem quais ejetar? Novamente, no início isso poderia ser feito manualmente como uma opção de configuração avançada (após descartar peers que são inalcançáveis). Como evitamos o particionamento do netDb? Fazendo com que os routers verifiquem se o netDb está fazendo o flood fill adequadamente, consultando K peers aleatórios do netDb. Como os routers que não participam do netDb descobrem novos routers pelos quais fazer túneis? Talvez isso possa ser feito enviando uma consulta específica ao netDb para que o router do netDb responda não com peers no netDb, mas com peers aleatórios fora do netDb.

O netDb do I2P é muito diferente dos DHTs tradicionais que suportam carga - ele apenas transporta metadados da rede, não qualquer payload real, razão pela qual mesmo um netDb usando um algoritmo floodfill será capaz de sustentar uma quantidade arbitrária de dados de I2P Site/IRC/bt/mail/syndie/etc. Podemos até fazer algumas otimizações conforme o I2P cresce para distribuir essa carga um pouco mais (talvez passando filtros bloom entre os participantes do netDb para ver o que eles precisam compartilhar), mas parece que podemos nos virar com uma solução muito mais simples por enquanto.

Um fato que pode valer a pena investigar - nem todos os leaseSets precisam ser publicados na netDb! Na verdade, a maioria não precisa ser - apenas aqueles para destinos que receberão mensagens não solicitadas (ou seja, servidores). Isso acontece porque as mensagens encapsuladas com garlic encryption enviadas de um destino para outro já incluem o leaseSet do remetente, de modo que qualquer envio/recebimento subsequente entre esses dois destinos (dentro de um curto período de tempo) funciona sem nenhuma atividade da netDb.

Então, voltando àquelas equações, podemos mudar L de 5 para algo como 0,1 (assumindo que apenas 1 em cada 50 destinos é um servidor). As equações anteriores também ignoraram a carga de rede necessária para responder consultas de clientes, mas embora isso seja altamente variável (baseado na atividade do usuário), também é muito provável que seja bastante insignificante comparado à frequência de publicação.

De qualquer forma, ainda não é mágico, mas uma boa redução de quase 1/5 da largura de banda/espaço em disco necessário (talvez mais tarde, dependendo de a distribuição do routerInfo ir diretamente como parte do estabelecimento de peers ou apenas através do netDb).

### A Desabilitação do Algoritmo Kademlia

Kademlia foi completamente desabilitado na versão 0.6.1.20.

*(Adaptado de uma conversa no IRC com jrandom 11/07)*

Kademlia requer um nível mínimo de serviço que a linha de base não poderia oferecer (largura de banda, CPU), mesmo após adicionar camadas (kad puro é absurdo nesse ponto). Kademlia simplesmente não funcionaria. Foi uma boa ideia, mas não para um ambiente hostil e fluido.

### Status Atual

O netDb desempenha um papel muito específico na rede I2P, e os algoritmos foram ajustados para atender às nossas necessidades. Isso também significa que não foi ajustado para lidar com necessidades que ainda não enfrentamos. O I2P é atualmente bastante pequeno (algumas centenas de routers). Houve alguns cálculos de que 3-5 routers floodfill deveriam ser capazes de lidar com 10.000 nós na rede. A implementação do netDb atende mais do que adequadamente às nossas necessidades no momento, mas provavelmente haverá mais ajustes e correções de bugs conforme a rede crescer.

### Atualização dos Cálculos 03-2008

Números atuais:

```
recvKBps = N * (L + 1) * (1 + F) * (1 + R) * S / T
```
onde:

```
N = number of routers in the entire network
L = average number of client destinations on each router
    (+1 for the routerInfo)
F = tunnel failure percentage
R = tunnel rebuild period, as a fraction of the tunnel lifetime
S = average netDb entry size
T = tunnel lifetime
```
Mudanças nas suposições:

- L agora é cerca de .5, comparado a .1 acima, devido à popularidade do i2psnark
  e outras aplicações.
- F é cerca de .33, mas bugs no teste de tunnel estão corrigidos em 0.6.1.33, então vai melhorar muito.
- Como netDb é cerca de 2/3 routerInfos de 5K e 1/3 leaseSets de 2K, S = 4K.
  O tamanho do RouterInfo está diminuindo em 0.6.1.32 e 0.6.1.33 conforme removemos estatísticas desnecessárias.
- R = período de construção de tunnel: 0.2 estava muito baixo - talvez fosse 0.7 -
  mas melhorias no algoritmo de construção em 0.6.1.32 devem reduzir para cerca de 0.2
  conforme a rede atualiza. Vamos considerar 0.5 agora com metade da rede em .30 ou anterior.

```
recvKBps = 700 * (0.5 + 1) * (1 + 0.33) * (1 + 0.5) * 4KB / 10m
         ~= 28KBps
```
Isso só considera os armazenamentos - e quanto às consultas?

### O Retorno do Algoritmo Kademlia?

*(Adaptado da reunião I2P de 2 de janeiro de 2007)*

O netDb Kademlia simplesmente não estava funcionando adequadamente. Está morto para sempre ou voltará? Se voltar, os pares no netDb Kademlia seriam um subconjunto muito limitado dos routers na rede (basicamente um número expandido de pares floodfill, se/quando os pares floodfill não conseguirem lidar com a carga). Mas até que os pares floodfill não consigam lidar com a carga (e outros pares não possam ser adicionados que consigam), é desnecessário.

### O Futuro do Floodfill

*(Adaptado de uma conversa IRC com jrandom 11/07)*

Aqui está uma proposta: A classe de capacidade O é automaticamente floodfill. Hmm. A menos que tenhamos certeza, podemos acabar com uma maneira elegante de fazer DDoS em todos os routers da classe O. Este é bem o caso: queremos ter certeza de que o número de floodfill seja o menor possível enquanto fornece alcance suficiente. Se/quando as solicitações netDb falharem, então precisamos aumentar o número de peers floodfill, mas no momento, não estou ciente de um problema de busca netDb. Há 33 peers da classe "O" de acordo com meus registros. 33 é /muito/ para floodfill.

Então o floodfill funciona melhor quando o número de peers nesse pool é firmemente limitado? E o tamanho do pool de floodfill não deveria crescer muito, mesmo que a própria rede gradualmente crescesse? 3-5 peers de floodfill podem lidar com 10K routers se bem me lembro (postei um monte de números sobre isso explicando os detalhes no antigo syndie). Parece um requisito difícil de preencher com opt-in automático, especialmente se os nós que optam por participar não podem confiar em dados de outros. por exemplo "vamos ver se estou entre os top 5", e só podem confiar em dados sobre si mesmos (por exemplo "definitivamente sou classe O, e movendo 150 KB/s, e ativo há 123 dias"). E top 5 também é hostil. Basicamente, é o mesmo que os servidores de diretório do tor - escolhidos por pessoas confiáveis (aka devs). Sim, agora mesmo poderia ser explorado por opt-in, mas isso seria trivial de detectar e lidar. Parece que no final, podemos precisar de algo mais útil que Kademlia, e ter apenas peers razoavelmente capazes se juntando a esse esquema. Classe N e acima deveria ser uma quantidade grande o suficiente para suprimir o risco de um adversário causar negação de serviço, eu espero. Mas teria que ser diferente do floodfill então, no sentido de que não causaria tráfego enorme. Grande quantidade? Para um netDb baseado em DHT? Não necessariamente baseado em DHT.

### Lista de Tarefas Floodfill {#todo}

NOTA: As informações a seguir não são atuais. Consulte [a página principal do netDb](/docs/overview/network-database) para o status atual e uma lista de trabalhos futuros.

A rede ficou com apenas um floodfill por algumas horas em 13 de março de 2008 (aproximadamente 18:00 - 20:00 UTC), e isso causou muitos problemas.

Duas mudanças implementadas na versão 0.6.1.33 devem reduzir a interrupção causada pela remoção ou rotatividade de peers floodfill:

1. Aleatorizar os peers floodfill usados para busca a cada vez.
   Isso irá eventualmente contornar aqueles que estão falhando.
   Esta mudança também corrigiu um bug sério que às vezes deixava o código de busca ff maluco.
2. Preferir os peers floodfill que estão ativos.
   O código agora evita peers que estão na shitlist, falhando, ou dos quais não se tem notícias há
   meia hora, se possível.

Uma vantagem é o contato inicial mais rápido com um I2P Site (ou seja, quando você precisa buscar o leaseset primeiro). O timeout de consulta é de 10s, então se você não começar perguntando a um peer que está offline, você pode economizar 10s.

*Podem* haver implicações de anonimato nestas mudanças. Por exemplo, no código **store** do floodfill, há comentários de que peers na shitlist não são evitados, pois um peer pode estar "ruim" e então ver o que acontece. Buscas são muito menos vulneráveis que stores - são muito menos frequentes e revelam menos informação. Então talvez não precisemos nos preocupar com isso? Mas se quisermos ajustar as mudanças, seria fácil enviar para um peer listado como "down" ou na shitlist mesmo assim, apenas não contá-lo como parte dos 2 para os quais estamos enviando (já que realmente não esperamos uma resposta).

Existem vários lugares onde um peer floodfill é selecionado - esta correção aborda apenas um - de quem um peer regular pesquisa [2 por vez]. Outros lugares onde uma melhor seleção de floodfill deveria ser implementada:

1. Para quem um peer regular armazena [1 de cada vez]
   (aleatório - precisa adicionar qualificação, porque os timeouts são longos)
2. Para quem um peer regular busca para verificar um armazenamento [1 de cada vez]
   (aleatório - precisa adicionar qualificação, porque os timeouts são longos)
3. Para quem um peer floodfill envia em resposta a uma busca falhada (3 mais próximos da busca)
4. Para quem um peer floodfill faz flood (todos os outros peers floodfill)
5. A lista de peers floodfill enviada no "whisper" NTCP a cada 6 horas
   (embora isso possa não ser mais necessário devido a outras melhorias do floodfill)

Muito mais que poderia e deveria ser feito:

- Use as estatísticas "dbHistory" para melhor avaliar a integração de um peer floodfill
- Use as estatísticas "dbHistory" para reagir imediatamente aos peers floodfill que não respondem
- Seja mais inteligente nas tentativas - as tentativas são tratadas por uma camada superior, não no
  FloodOnlySearchJob, então ele faz outra ordenação aleatória e tenta novamente,
  em vez de propositalmente pular os peers ff que acabamos de tentar.
- Melhorar mais as estatísticas de integração
- Realmente usar estatísticas de integração em vez de apenas indicação floodfill no netDb
- Usar estatísticas de latência também?
- Mais melhorias no reconhecimento de peers floodfill com falhas

Concluído recentemente:

- [No Release 0.6.3]
  Implementar opt-in automático
  para floodfill para alguma percentagem de peers classe O, baseado na análise da rede.
- [No Release 0.6.3]
  Continuar a reduzir o tamanho das entradas netDb para reduzir o tráfego floodfill -
  estamos agora no número mínimo de estatísticas necessárias para monitorizar a rede.
- [No Release 0.6.3]
  Lista manual de peers floodfill a excluir
  ([blocklists](/docs/overview/threat-model#blocklist) por ident do router)
- [No Release 0.6.3]
  Melhor seleção de peers floodfill para armazenamentos:
  Evitar peers cujo netDb é antigo, ou que tiveram um armazenamento falhado recente,
  ou estão permanentemente na lista negra.
- [No Release 0.6.4]
  Preferir peers floodfill já conectados para armazenamentos RouterInfo, para
  reduzir o número de conexões diretas para peers floodfill.
- [No Release 0.6.5]
  Peers que já não são floodfill enviam o seu routerInfo em resposta
  a uma consulta, para que o router que faz a consulta saiba que ele
  já não é floodfill.
- [No Release 0.6.5]
  Ajuste adicional dos requisitos para tornar-se automaticamente floodfill
- [No Release 0.6.5]
  Corrigir o profiling do tempo de resposta em preparação para favorecer floodfills rápidos
- [No Release 0.6.5]
  Melhorar blocklisting
- [No Release 0.7]
  Corrigir exploração netDb
- [No Release 0.7]
  Ativar blocklisting por defeito, bloquear os problemáticos conhecidos
- [Várias melhorias em releases recentes, um esforço contínuo]
  Reduzir as exigências de recursos em routers de alta largura de banda e floodfill

Essa é uma lista longa, mas será necessário todo esse trabalho para ter uma rede que seja resistente a DOS de muitos peers ligando e desligando o switch de floodfill. Ou fingindo ser um router floodfill. Nada disso foi um problema quando tínhamos apenas dois routers ff, e ambos ficavam ativos 24/7. Novamente, a ausência do jrandom nos apontou para lugares que precisam de melhorias.

Para auxiliar neste esforço, dados de perfil adicionais para peers floodfill agora são (a partir da versão 0.6.1.33) exibidos na página "Profiles" no console do router. Usaremos isso para analisar quais dados são apropriados para avaliar peers floodfill.

A rede é atualmente bastante resiliente, no entanto continuaremos a aprimorar nossos algoritmos para medir e reagir ao desempenho e confiabilidade dos peers floodfill. Embora não estejamos, no momento, totalmente protegidos contra as ameaças potenciais de floodfills maliciosos ou um DDOS de floodfill, a maior parte da infraestrutura está instalada, e estamos bem posicionados para reagir rapidamente caso a necessidade surja.
