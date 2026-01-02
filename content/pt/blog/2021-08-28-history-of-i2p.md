---
title: "20 anos de privacidade: uma breve história do I2P"
date: 2021-08-28
slug: "20-years-of-privacy-a-brief-history-of-i2p"
author: "sadie"
description: "Uma história do I2P como o conhecemos"
categories: ["general"]
---

## Invisibility is the best defense: building an internet within an internet

> "Acredito que a maioria das pessoas queira esta tecnologia para que elas possam se expressar livremente. É reconfortante saber que você pode fazer isso. Ao mesmo tempo, podemos superar alguns dos problemas observados na Internet, mudando a forma como a segurança e a privacidade são vistas, bem como o grau em que são valorizadas."

Em outubro de 2001, 0x90 (Lance James) teve um sonho. Começou como um "desejo de comunicação instantânea com outros usuários do Freenet para falar sobre questões do Freenet e trocar chaves do Freenet, mantendo ainda assim o anonimato, a privacidade e a segurança." Chamava-se IIP — the Invisible IRC Project.

O The Invisible IRC Project foi baseado em um ideal e no framework (estrutura) por trás do The InvisibleNet. Em uma entrevista de 2002, 0x90 descreveu o projeto como focado na "inovação em tecnologia de rede inteligente", com o objetivo de "oferecer os mais altos padrões de segurança e privacidade na Internet amplamente utilizada, porém notoriamente insegura."

Até 2003, vários outros projetos semelhantes já haviam começado, sendo os maiores o Freenet, o GNUNet e o Tor. Todos esses projetos tinham objetivos amplos de criptografar e anonimizar diversos tipos de tráfego. Para o IIP, ficou claro que apenas o IRC não era um alvo suficientemente grande. O que era necessário era uma camada de anonimização para todos os protocolos.

No início de 2003, um novo desenvolvedor anônimo, "jrandom" juntou-se ao projeto. Seu objetivo explícito era ampliar o âmbito do IIP. jrandom desejava reescrever a base de código do IIP em Java e redesenhar os protocolos com base em artigos recentes e nas decisões de design iniciais que o Tor e o Freenet estavam tomando. Alguns conceitos, como "onion routing", foram modificados para se tornarem "garlic routing" (roteamento garlic).

No final do verão de 2003, jrandom havia assumido o controle do projeto e o renomeado para Invisible Internet Project, ou "I2P". Ele publicou um documento delineando a filosofia do projeto e situou suas metas técnicas e seu design no contexto de mixnets (redes de mix) e camadas de anonimização. Ele também publicou a especificação de dois protocolos (I2CP e I2NP) que formaram a base da rede que o I2P usa hoje.

No outono de 2003, I2P, Freenet e Tor estavam se desenvolvendo rapidamente. jrandom lançou a versão 0.2 do I2P em 1 de novembro de 2003 e continuou com lançamentos rápidos nos três anos seguintes.

Em fevereiro de 2005, zzz instalou o I2P pela primeira vez. Até o verão de 2005, zzz já havia configurado zzz.i2p e stats.i2p, que se tornaram recursos centrais para o desenvolvimento do I2P. Em julho de 2005, jrandom lançou a versão 0.6, incluindo o inovador protocolo de transporte SSU (Secure Semi-reliable UDP) para descoberta de IP e travessia de firewall.

Do final de 2006 e ao longo de 2007, o desenvolvimento do núcleo do I2P desacelerou drasticamente, à medida que jrandom mudou o foco para o Syndie. Em novembro de 2007, ocorreu um desastre quando jrandom enviou uma mensagem críptica dizendo que teria que se afastar por um ano ou mais. Infelizmente, nunca mais tiveram notícias de jrandom.

A segunda etapa do desastre ocorreu em 13 de janeiro de 2008, quando a empresa de hospedagem de quase todos os servidores i2p.net sofreu uma queda de energia e não retomou totalmente o serviço. Complication, welterde e zzz tomaram rapidamente decisões para colocar o projeto de volta em funcionamento, migrando para i2p2.de e trocando de CVS para monotone para o controle de código-fonte.

O projeto percebeu que havia dependido excessivamente de recursos centralizados. O trabalho ao longo de 2008 descentralizou o projeto e distribuiu funções entre várias pessoas. A partir da versão 0.7.6, em 31 de julho de 2009, zzz assinaria as 49 versões seguintes.

Em meados de 2009, zzz passou a compreender muito melhor a base de código e identificou muitos problemas de escalabilidade. A rede experimentou crescimento devido tanto às capacidades de anonimização quanto às de contorno. As atualizações automáticas dentro da rede tornaram-se disponíveis.

No outono de 2010, zzz declarou uma moratória no desenvolvimento do I2P até que a documentação do site estivesse completa e precisa. Levou 3 meses.

A partir de 2010, zzz, ech, hottuna e outros colaboradores participaram do CCC (Chaos Communications Congress) anualmente até as restrições da COVID. O projeto fortaleceu a comunidade e celebrou lançamentos em conjunto.

Em 2013, Anoncoin foi criada como a primeira criptomoeda com suporte integrado ao I2P, com desenvolvedores como meeh fornecendo infraestrutura para a rede I2P.

Em 2014, str4d começou a contribuir para o I2PBote e, na Real World Crypto, iniciaram-se discussões sobre a atualização da criptografia do I2P. No final de 2014, a maior parte dos novos algoritmos de assinatura estava concluída, incluindo ECDSA e EdDSA.

Em 2015, a I2PCon ocorreu em Toronto, com palestras, apoio da comunidade e participantes da América e da Europa. Em 2016, no Real World Crypto Stanford, str4d apresentou uma palestra sobre o progresso da migração criptográfica.

NTCP2 foi implementado em 2018 (release 0.9.36), oferecendo resistência à censura por DPI (inspeção profunda de pacotes) e reduzindo a carga da CPU por meio de criptografia moderna e mais rápida.

Em 2019, a equipe participou de mais conferências, incluindo a DefCon e a Monero Village, estabelecendo contato com desenvolvedores e pesquisadores. A pesquisa de Hoàng Nguyên Phong sobre censura no I2P foi aceita no FOCI na USENIX, levando à criação do I2P Metrics.

Durante o CCC 2019, foi tomada a decisão de migrar do Monotone para o GitLab. Em 10 de dezembro de 2020, o projeto mudou oficialmente do Monotone para o Git, juntando-se ao mundo dos desenvolvedores que usam Git.

0.9.49 (2021) iniciou a migração para a nova e mais rápida criptografia ECIES-X25519 para routers, concluindo anos de trabalho de especificação. A migração levaria vários lançamentos.

## 1.5.0 — O lançamento antecipado de aniversário

Após 9 anos de lançamentos 0.9.x, o projeto foi diretamente da 0.9.50 para a 1.5.0 como reconhecimento de quase 20 anos de trabalho para fornecer anonimato e segurança. Esta versão concluiu a implementação de mensagens menores de construção de tunnel para reduzir a largura de banda e deu continuidade à transição para a criptografia X25519.

**Parabéns, equipe. Vamos fazer mais 20.**
