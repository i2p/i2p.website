---
title: "Descontinuar nomes de host em endereços de roteadores"
number: "141"
author: "zzz"
created: "2017-08-03"
lastupdated: "2018-03-17"
status: "Fechado"
thread: "http://zzz.i2p/topics/2363"
target: "0.9.32"
implementedin: "0.9.32"
toc: true
---

## Visão Geral

A partir da versão 0.9.32, atualize a especificação netdb para descontinuar nomes de host em informações de roteadores, ou mais precisamente, nos endereços individuais dos roteadores. Em todas as implementações I2P, roteadores que publicam configurados com nomes de host devem substituí-los por IPs antes de publicar, e outros roteadores devem ignorar endereços com nomes de host. Roteadores não devem fazer consultas DNS de nomes de host publicados.

## Motivação

Nomes de host têm sido permitidos em endereços de roteadores desde o início do I2P. No entanto, pouquíssimos roteadores publicam nomes de host, pois requer um nome de host público (que poucos usuários possuem) e configuração manual (que poucos usuários se preocupam em fazer). Em uma amostra recente, 0,7% dos roteadores estavam publicando um nome de host.

O objetivo original dos nomes de host era ajudar usuários com IPs frequentemente mutáveis e um serviço de DNS dinâmico (como http://dyn.com/dns/) a não perder a conectividade quando seu IP mudasse. No entanto, naquela época, a rede era pequena e a expiração das informações do roteador era mais longa. Além disso, o código Java não tinha uma lógica funcional para reiniciar o roteador ou republicar as informações do roteador quando o IP local mudava.

Além disso, no início, o I2P não suportava IPv6, então a complicação de resolver um nome de host para um endereço IPv4 ou IPv6 não existia.

No Java I2P, sempre foi um desafio propagar um nome de host configurado para ambos os transportes publicados, e a situação ficou mais complexa com IPv6. Não está claro se um host dual-stack deve publicar tanto um nome de host quanto um endereço IPv6 literal ou não. O nome de host é publicado para o endereço SSU, mas não para o endereço NTCP.

Recentemente, questões de DNS foram levantadas (tanto indiretamente quanto diretamente) por pesquisas no Georgia Tech. Os pesquisadores operaram um grande número de floodfills com nomes de host publicados. O problema imediato era que, para um pequeno número de usuários com possível DNS local quebrado, isso travava completamente o I2P.

A questão maior era o DNS em geral, e como o DNS (seja ativo ou passivo) poderia ser usado para enumerar rapidamente a rede, especialmente se os roteadores publicadores fossem floodfill. Nomes de host inválidos ou respondentes DNS sem resposta, lentos ou maliciosos poderiam ser usados para ataques adicionais. O EDNS0 pode fornecer mais cenários de enumeração ou ataque. O DNS também pode proporcionar vias de ataque baseadas no tempo da consulta, revelando horários de conexão entre roteadores, ajudando a construir gráficos de conexão, estimar tráfego e outras inferências.

Além disso, o grupo do Georgia Tech, liderado por David Dagon, listou várias preocupações com o DNS em aplicações focadas em privacidade. As consultas DNS geralmente são feitas por uma biblioteca de baixo nível, não controlada pela aplicação. Essas bibliotecas não foram especificamente projetadas para anonimato; podem não fornecer controle fino pela aplicação; e sua saída pode ser impressa digitalmente. Bibliotecas Java em particular podem ser problemáticas, mas isso não é apenas uma questão do Java. Algumas bibliotecas usam consultas DNS ANY que podem ser rejeitadas. Tudo isso fica ainda mais preocupante com a presença generalizada de monitoramento passivo de DNS e consultas disponíveis para várias organizações. Todo o monitoramento e ataques de DNS são fora de banda do ponto de vista dos roteadores I2P e requerem poucos ou nenhum recurso de I2P na rede, sem modificação das implementações existentes.

Enquanto não pensamos completamente nas possíveis questões, a superfície de ataque parece ser grande. Existem outras maneiras de enumerar a rede e reunir dados relacionados, mas ataques via DNS podem ser muito mais fáceis, rápidos e menos detectáveis.

As implementações de roteadores poderiam, em teoria, mudar para usar uma sofisticada biblioteca DNS de terceiros, mas isso seria bastante complexo, um fardo de manutenção, e está bem fora da expertise principal dos desenvolvedores do I2P.

As soluções imediatas implementadas para o Java 0.9.31 incluíram corrigir o problema de travamento, aumentar os tempos de cache DNS e implementar um cache negativo de DNS. Claro, aumentar os tempos de cache reduz o benefício de ter nomes de host em informações de roteadores para começar.

No entanto, essas mudanças são apenas mitigações a curto prazo e não corrigem os problemas subjacentes acima. Portanto, a solução mais simples e completa é proibir nomes de host em informações de roteadores, eliminando assim consultas DNS para eles.

## Design

Para o código de publicação das informações do roteador, os implementadores têm duas escolhas, ou desativar/remover a opção de configuração para nomes de host, ou converter os nomes de host configurados para IPs no momento da publicação. Em ambos os casos, os roteadores devem republicar imediatamente quando seu IP mudar.

Para o código de validação das informações do roteador e conexão de transporte, os implementadores devem ignorar endereços de roteadores contendo nomes de host, e usar os outros endereços publicados contendo IPs, se houver. Se nenhum endereço nas informações do roteador contiver IPs, o roteador não deve conectar ao roteador publicado. Em nenhum caso um roteador deve fazer uma consulta DNS de um nome de host publicado, seja diretamente ou via uma biblioteca subjacente.

## Especificação

Altere as especificações de transporte NTCP e SSU para indicar que o parâmetro "host" deve ser um IP, não um nome de host, e que os roteadores devem ignorar endereços individuais de roteadores que contenham nomes de host.

Isso também se aplica aos parâmetros "ihost0", "ihost1" e "ihost2" em um endereço SSU. Os roteadores devem ignorar endereços de introdutores que contenham nomes de host.


## Notas

Esta proposta não aborda nomes de host para hosts de reseed. Embora as consultas DNS para hosts de reseed sejam muito menos frequentes, ainda podem ser um problema. Se necessário, isso pode ser corrigido simplesmente substituindo os nomes de host por IPs na lista de URLs embutida; não seriam necessárias mudanças de especificação ou de código.

## Migração

Esta proposta pode ser implementada imediatamente, sem uma migração gradual, porque pouquíssimos roteadores publicam nomes de host, e aqueles que o fazem geralmente não publicam o nome de host em todos os endereços.

Os roteadores não precisam verificar a versão do roteador publicado antes de decidir ignorar nomes de host, e não há necessidade de um lançamento coordenado ou estratégia comum entre as várias implementações de roteadores.

Para aqueles roteadores que ainda publicam nomes de host, eles receberão menos conexões de entrada e podem eventualmente ter dificuldade para construir túneis de entrada.

Para minimizar ainda mais o impacto, os implementadores podem começar ignorando endereços de roteadores com nomes de host apenas para roteadores floodfill, ou para roteadores com uma versão publicada inferior a 0.9.32, e ignorar nomes de host para todos os roteadores em um lançamento posterior.
