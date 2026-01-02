---
title: "Programação da Conferência Agosto de 2019"
date: 2019-07-29
author: "sadie"
description: "Os desenvolvedores do I2P estão participando de várias conferências este mês"
---

# Programação da Conferência de Agosto de 2019

Olá a todos,


O próximo mês será agitado! Encontre-se com os desenvolvedores do I2P em dois workshops na Defcon 27 e conecte-se com pesquisadores que vêm observando a censura ao I2P no FOCI '19.

## I2P for Cryptocurrency Developers

**zzz**

- Monero Village
- August 9, 3:15pm
- Monero Village will be on the 26th floor of Bally's [map](https://defcon.org/html/defcon-27/dc-27-venue.html)

Este workshop auxiliará desenvolvedores a projetar aplicações para se comunicarem via I2P, visando anonimato e segurança. Discutiremos requisitos comuns para aplicações de criptomoedas e analisaremos a arquitetura e as necessidades específicas de cada aplicação. Em seguida, abordaremos as comunicações de tunnel, a seleção de router e de bibliotecas, e as opções de empacotamento, e responderemos a todas as perguntas relacionadas à integração do I2P.

O objetivo é criar arquiteturas seguras, escaláveis, extensíveis e eficientes que atendam às necessidades de cada projeto em particular.

## I2P para Desenvolvedores de Criptomoedas

**não sei**

- Crypto & Privacy Village
- Saturday August 10, 2pm - 3:30pm
- Planet Hollywood [map](https://defcon.org/images/defcon-27/maps/ph-final-public.pdf)
- This workshop is not recorded. So don't miss it!

O workshop oferece uma introdução às maneiras pelas quais uma aplicação pode ser adaptada para funcionar com a rede anônima Peer-to-Peer do I2P. Os desenvolvedores devem aprender que o uso de P2P anônimo em suas aplicações não precisa ser muito diferente do que já fazem em aplicações Peer-to-Peer não anônimas. Ele começa com uma introdução ao sistema de plugins do I2P, mostrando como os plugins existentes se configuram para realizar comunicação sobre o I2P e o que há de bom e de ruim em cada abordagem. Depois, seguiremos para o controle programático do I2P por meio de suas APIs SAM e I2PControl. Por fim, mergulharemos na API SAMv3, iniciando o desenvolvimento de uma nova biblioteca que a utilize em Lua e escrevendo uma aplicação simples.

## I2P para Desenvolvedores de Aplicações

**sadie**

- FOCI '19
- Tuesday August 13th 10:30am
- Hyatt Regency Santa Clara
- Co-located with USENIX Security '19
- [Workshop Program](https://www.usenix.org/conference/foci19/workshop-program)

A prevalência da censura na Internet estimulou a criação de várias plataformas de medição para monitorar atividades de filtragem. Um desafio importante enfrentado por essas plataformas gira em torno do compromisso entre a profundidade das medições e a amplitude da cobertura. Neste artigo, apresentamos uma infraestrutura oportunística de medição de censura construída sobre uma rede de servidores de VPN distribuídos operados por voluntários, que utilizamos para medir em que medida a rede de anonimato I2P é bloqueada ao redor do mundo. Essa infraestrutura nos fornece não apenas numerosos e geograficamente diversos pontos de observação, mas também a capacidade de realizar medições aprofundadas em todos os níveis da pilha de rede. Usando essa infraestrutura, medimos em escala global a disponibilidade de quatro serviços diferentes do I2P: a página inicial oficial, seu site espelho, reseed servers (servidores que fornecem dados iniciais para a descoberta de pares), e relays ativos na rede. Ao longo de um mês, realizamos um total de 54.000 medições a partir de 1.700 localizações de rede em 164 países. Com diferentes técnicas para detectar bloqueio de nomes de domínio, injeção de pacotes de rede e páginas de bloqueio, descobrimos censura ao I2P em cinco países: China, Irã, Omã, Catar e Kuwait. Por fim, concluímos discutindo abordagens potenciais para contornar a censura no I2P.

**Nota:** As imagens referenciadas na publicação original (monerovillageblog.png, cryptovillageblog.png, censorship.jpg) podem precisar ser adicionadas ao diretório `/static/images/blog/`.
