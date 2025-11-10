---
title: "Notas de status do I2P de 2004-11-23"
date: 2004-11-23
author: "jr"
description: "Atualização semanal da situação do I2P abrangendo a recuperação da rede, o progresso dos testes da biblioteca de streaming, os planos para o lançamento da versão 0.4.2 e melhorias no livro de endereços"
categories: ["status"]
---

Olá, pessoal, é hora de uma atualização de status

## Índice:

1. Net status
2. Streaming lib
3. 0.4.2
4. Addressbook.py 0.3.1
5. ???

## 1) Status da rede

Após o período de 2-3 dias na semana passada em que as coisas estavam bem congestionadas, a rede voltou ao normal (provavelmente porque paramos de fazer testes de estresse na porta do bittorrent ;). A rede tem sido bastante confiável desde então - temos alguns routers que estão em funcionamento há 30-40+ dias, mas as conexões de IRC ainda têm tido alguns percalços ocasionais. Por outro lado...

## 2) Biblioteca de streaming

Na última semana, mais ou menos, temos feito muito mais testes ao vivo da biblioteca de streaming na rede, e os resultados têm sido bastante bons. O Duck configurou um tunnel com essa biblioteca, que as pessoas podiam usar para acessar o servidor IRC dele e, ao longo de alguns dias, tive apenas duas desconexões desnecessárias (o que nos ajudou a identificar alguns bugs). Também mantivemos uma instância do i2ptunnel apontando para um squid outproxy (proxy de saída) que as pessoas têm experimentado, e a taxa de transferência, a latência e a confiabilidade estão muito melhores quando comparadas à biblioteca antiga, que testamos lado a lado.

No geral, a biblioteca de streaming parece estar suficientemente madura para um primeiro lançamento. Ainda há algumas coisas que não foram concluídas, mas é uma melhoria significativa em relação à biblioteca antiga, e precisamos dar a você um motivo para atualizar mais tarde, certo? ;)

Na verdade, apenas para instigá-lo (ou talvez inspirá-lo a propor algumas soluções), as principais coisas que vejo no horizonte para a streaming lib (biblioteca de streaming) são: - alguns algoritmos para compartilhar informações de congestionamento e RTT (tempo de ida e volta) entre fluxos (por destino-alvo? por destino de origem? para todos os destinos locais?) - mais otimizações para fluxos interativos (na implementação atual, a maior parte do foco está em fluxos de alto volume) - uso mais explícito dos recursos da nova streaming lib em I2PTunnel, reduzindo a sobrecarga por tunnel. - limitação de largura de banda no nível do cliente (em uma ou ambas as direções de um fluxo, ou possivelmente compartilhada entre vários fluxos). Isso seria, é claro, além da limitação geral de largura de banda do router. - vários controles para que os destinos limitem quantos fluxos aceitam ou criam (temos algum código básico, mas em grande parte desativado) - listas de controle de acesso (permitindo apenas fluxos para ou de certos outros destinos conhecidos) - controles via web e monitoramento da integridade dos vários fluxos, bem como a capacidade de encerrá-los explicitamente ou limitá-los

Y'all can probably come up with some other things too, but thats just a brief list of things I'd love to see in the streaming lib, but won't hold up the 0.4.2 release for. If anyone is interested in any of those, please, lemmie know!

## 3) 0.4.2

Então, se a biblioteca de streaming está em boa forma, quando vamos ter o lançamento? O plano atual é lançá-la até o fim da semana, talvez até amanhã mesmo. Há mais algumas coisas em andamento que quero resolver primeiro e, claro, elas precisam ser testadas, blá blá blá.

A grande mudança na versão 0.4.2 será, claro, a nova biblioteca de streaming. Do ponto de vista da API, ela é idêntica à biblioteca antiga - I2PTunnel e fluxos SAM a utilizam automaticamente, mas do ponto de vista dos pacotes, ela *não* é compatível com versões anteriores. Isso nos deixa com um dilema interessante - não há nada no I2P que exija que tornemos a 0.4.2 uma atualização obrigatória, porém as pessoas que não atualizarem não poderão usar o I2PTunnel - sem eepsites(sites I2P), sem IRC, sem outproxy, sem e-mail. Não quero alienar nossos usuários de longa data forçando-os a atualizar, mas também não quero aliená-los fazendo com que tudo o que é útil deixe de funcionar ;)

Estou aberto a ser convencido de um jeito ou de outro — seria fácil o suficiente alterar uma única linha de código para que a versão 0.4.2 não se comunique com as versões mais antigas, ou poderíamos simplesmente deixar como está e deixar que as pessoas atualizem sempre que forem ao site ou ao fórum reclamar que está tudo quebrado. O que vocês acham?

## 4) AddressBook.py 0.3.1

Ragnarok lançou uma nova atualização (patch) para seu aplicativo de livro de endereços - veja `http://ragnarok.i2p/` para mais informações (ou talvez ele possa nos dar uma atualização na reunião?)

## 5) ???

Sei que há muito mais atividade acontecendo — com a porta do BitTorrent, o susimail, o novo serviço de hospedagem do slacker, entre outras coisas. Alguém tem mais algo para trazer à pauta? Se tiver, apareça na reunião em ~30m no #i2p, nos servidores IRC de sempre!

=jr
