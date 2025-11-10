---
title: "Notas de status do I2P de 2004-10-05"
date: 2004-10-05
author: "jr"
description: "Atualização semanal de status do I2P abrangendo o lançamento da versão 0.4.1.1, análise das estatísticas da rede, planos para a biblioteca de streaming na versão 0.4.2 e eepserver incluído"
categories: ["status"]
---

Olá, pessoal, é hora da atualização semanal

## Índice:

1. 0.4.1.1 status
2. Pretty pictures
3. 0.4.1.2 and 0.4.2
4. Bundled eepserver
5. ???

## 1) 0.4.1.1 estado

Depois de um lançamento 0.4.1 bastante turbulento (e a subsequente atualização rápida 0.4.1.1), a rede parece ter voltado ao normal - cinquenta e poucos pares ativos no momento, e tanto o irc quanto as eepsites(I2P Sites) estão acessíveis. A maior parte dos problemas foi causada por testes insuficientes do novo transporte fora de condições de laboratório (por exemplo, sockets falhando em momentos estranhos, atrasos excessivos, etc). Da próxima vez que precisarmos fazer mudanças nessa camada, vamos garantir que seja testado mais amplamente antes do lançamento.

## 2) Imagens bonitas

Nos últimos dias, tem havido um grande número de atualizações no CVS, e uma das novidades adicionadas foi um novo componente de registro de estatísticas, que nos permite simplesmente extrair os dados estatísticos brutos à medida que são gerados, em vez de lidar com as médias grosseiras obtidas em /stats.jsp. Com ele, tenho monitorado algumas estatísticas-chave em alguns routers, e estamos cada vez mais perto de identificar os problemas de estabilidade restantes. As estatísticas brutas são bastante volumosas (uma execução de 20 horas na máquina do duck gerou quase 60 MB de dados), mas é por isso que temos gráficos bonitos - `http://dev.i2p.net/~jrandom/stats/`

O eixo Y na maioria deles está em milissegundos, enquanto o eixo X está em segundos. Há algumas coisas interessantes a notar. Primeiro, client.sendAckTime.png é uma aproximação bastante boa de um único atraso de ida e volta, pois a mensagem de confirmação (ACK) é enviada junto com o payload (carga útil) e depois retorna por todo o caminho do tunnel - assim, a grande maioria das quase 33.000 mensagens bem-sucedidas enviadas teve um tempo de ida e volta inferior a 10 segundos. Se então analisarmos o client.sendsPerFailure.png ao lado do client.sendAttemptAverage.png, veremos que os 563 envios com falha foram quase todos tentados o número máximo de novas tentativas que permitimos (5 com um soft timeout (tempo limite brando) de 10s por tentativa e hard timeout (tempo limite rígido) de 60s), enquanto a maioria das outras tentativas teve sucesso na primeira ou na segunda tentativa.

Outra imagem interessante é a client.timeout.png, que lança muitas dúvidas sobre uma hipótese que eu tinha — de que as falhas no envio de mensagens estavam correlacionadas com algum tipo de congestionamento local. Os dados representados no gráfico mostram que o uso da largura de banda de entrada variou amplamente quando as falhas ocorreram, não houve picos consistentes no tempo de processamento do envio local e, aparentemente, nenhum padrão com a latência do teste de tunnel.

Os arquivos dbResponseTime.png e dbResponseTime2.png são semelhantes ao client.sendAckTime.png, exceto que correspondem a mensagens do netDb em vez de mensagens de cliente de ponta a ponta.

A transport.sendMessageFailedLifetime.png mostra por quanto tempo retemos uma mensagem localmente antes de marcá‑la como falha por algum motivo (por exemplo, devido à expiração ou ao fato de o par ao qual se destina estar inacessível). Algumas falhas são inevitáveis, mas esta imagem mostra um número significativo falhando logo após o tempo limite de envio local (10s). Há algumas coisas que podemos fazer para tratar disso: - primeiro, podemos tornar a lista de bloqueio mais adaptativa- aumentando exponencialmente o período pelo qual um par fica na lista de bloqueio, em vez de um valor fixo de 4 minutos para cada um. (isso já foi submetido ao CVS) - segundo, podemos falhar mensagens preventivamente quando parecer que falhariam de qualquer forma. Para fazer isso, fazemos com que cada conexão acompanhe sua taxa de envio e, sempre que uma nova mensagem é adicionada à sua fila, se o número de bytes já enfileirados dividido pela taxa de envio exceder o tempo restante até a expiração, marcamos a mensagem como falha imediatamente. Também podemos conseguir usar essa métrica ao decidir se devemos aceitar mais solicitações de tunnel através de um par.

De qualquer forma, vamos para a próxima imagem - transport.sendProcessingTime.png. Nela, você vê que esta máquina específica raramente é responsável por muito atraso - tipicamente 10-100ms, embora alguns picos cheguem a 1s ou mais.

Cada ponto representado em tunnel.participatingMessagesProcessed.png indica quantas mensagens foram encaminhadas ao longo de um tunnel do qual o router participou. Ao combinar isso com o tamanho médio da mensagem, obtemos uma estimativa da carga de rede que o par assume para outras pessoas.

A última imagem é a tunnel.testSuccessTime.png, mostrando quanto tempo leva para enviar uma mensagem para fora por um tunnel e recebê-la de volta para casa através de outro tunnel de entrada, dando-nos uma estimativa de quão bons são os nossos tunnels.

Ok, já chega de imagens bonitas por enquanto. Você pode gerar os dados por conta própria com qualquer versão após 0.4.1.1-6, definindo a propriedade de configuração do router "stat.logFilters" para uma lista de nomes de estatísticas separada por vírgulas (obtenha os nomes na página /stats.jsp). Isso é gravado em stats.log, que você pode processar com

```
java -cp lib/i2p.jar net.i2p.stat.StatLogFilter stat.log
```
que o divide em arquivos separados para cada estatística, adequado para ser carregado na sua ferramenta favorita (por exemplo, gnuplot).

## 3) 0.4.1.2 e 0.4.2

Houve muitas atualizações desde o lançamento 0.4.1.1 (veja o histórico para a lista completa), mas ainda não há correções críticas. Vamos disponibilizá-las no próximo lançamento de patch 0.4.1.2, ainda esta semana, depois que alguns bugs pendentes relacionados à autodetecção de IP forem resolvidos.

A próxima tarefa importante naquele ponto será chegar à 0.4.2, que atualmente está prevista como uma grande reformulação do processamento de tunnel. Será muito trabalho, revisando a criptografia e o processamento de mensagens, bem como o agrupamento de tunnel, mas é bastante crítico, pois um atacante poderia relativamente facilmente realizar alguns ataques estatísticos aos tunnels agora (por exemplo, predecessor com ordenação aleatória de tunnel ou coleta de netDb).

No entanto, dm levantou a questão de se faria sentido fazer a biblioteca de streaming primeiro (atualmente planejada para o lançamento 0.4.3). O benefício disso seria que a rede se tornaria mais confiável e teria melhor vazão, incentivando outros desenvolvedores a começar a desenvolver aplicativos cliente. Depois que isso estiver implementado, eu poderia então voltar à reformulação do tunnel e tratar das questões de segurança (não visíveis ao usuário).

Tecnicamente, as duas tarefas planejadas para 0.4.2 e 0.4.3 são ortogonais, e ambas serão feitas de qualquer forma, então não parece haver muita desvantagem em inverter as duas. Estou inclinado a concordar com dm e, a menos que alguém apresente motivos para manter 0.4.2 como a atualização de tunnel e 0.4.3 como a biblioteca de streaming, vamos invertê-las.

## 4) eepserver empacotado

Como foi mencionado nas notas de lançamento da versão 0.4.1, incluímos o software e a configuração necessários para executar um eepsite (Site I2P) prontos para uso - basta colocar um arquivo no diretório ./eepsite/docroot/ e compartilhar o destino I2P encontrado no console do router.

Algumas pessoas me chamaram a atenção pelo meu entusiasmo por arquivos .war, no entanto - a maioria dos aplicativos, infelizmente, precisa de um pouco mais de trabalho do que simplesmente colocar um arquivo no ./eepsite/webapps/ dir. Reuni um breve tutorial sobre como executar o mecanismo de blog blojsom, e você pode ver como isso fica no site do detonate.

## 5) ???

Por enquanto é isso - passe na reunião daqui a 90 minutos se quiser discutir.

=jr
