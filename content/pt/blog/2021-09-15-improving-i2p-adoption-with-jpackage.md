---
title: "Melhorando a adoção e a integração inicial do I2P usando Jpackage e I2P-Zero"
date: 2021-09-15
slug: "improving-i2p-adoption-and-onboarding-using-jpackage-i2p-zero"
author: "idk"
description: "Formas versáteis e emergentes de instalar e incorporar o I2P na sua aplicação"
categories: ["general"]
---

Durante a maior parte da existência do I2P, tem sido uma aplicação que é executada com a ajuda de uma Máquina Virtual Java já instalada na plataforma. Isso sempre foi a forma normal de distribuir aplicações Java, mas resulta em um procedimento de instalação complicado para muitas pessoas. Para complicar ainda mais, a "resposta certa" para tornar o I2P fácil de instalar em uma determinada plataforma pode não ser a mesma em outras plataformas. Por exemplo, o I2P é bastante simples de instalar com as ferramentas padrão em sistemas operacionais baseados em Debian e Ubuntu, porque podemos simplesmente listar os componentes Java necessários como "Required" no nosso pacote; contudo, no Windows ou no OSX, não há tal sistema que nos permita garantir que um Java compatível esteja instalado.

A solução óbvia seria gerenciarmos nós mesmos a instalação do Java, mas isso costumava ser um problema por si só, fora do escopo do I2P. No entanto, nas versões recentes do Java, surgiu um novo conjunto de opções que tem o potencial de resolver esse problema para muitos softwares Java. Esta ferramenta empolgante chama-se **"Jpackage."**

## I2P-Zero e Instalação do I2P sem Dependências

O primeiro esforço muito bem-sucedido para construir um pacote I2P sem dependências foi o I2P-Zero, criado pelo projeto Monero originalmente para uso com a criptomoeda Monero. Esse projeto nos deixou muito entusiasmados por causa do seu sucesso em criar um router I2P de uso geral que poderia ser facilmente empacotado com um aplicativo I2P. Especialmente no Reddit, muitas pessoas manifestam preferência pela simplicidade de configurar um router I2P-Zero.

Isto realmente nos provou que um pacote I2P sem dependências e fácil de instalar era possível usando ferramentas modernas de Java, mas o caso de uso do I2P-Zero era um pouco diferente do nosso. Ele é mais adequado para aplicativos embarcados que precisam de um router (roteador) I2P que possam controlar facilmente através de sua conveniente porta de controle na porta "8051". Nosso próximo passo seria adaptar a tecnologia ao Aplicativo I2P de uso geral.

## Mudanças na segurança de aplicativos do OSX afetam o Instalador IzPack do I2P

O problema tornou-se mais urgente nas versões recentes do Mac OSX, nas quais já não é simples usar o instalador "Classic" que vem no formato .jar. Isso ocorre porque o aplicativo não é "notarizado" pelas autoridades da Apple e é considerado um risco de segurança. **No entanto**, o Jpackage pode produzir um arquivo .dmg, que pode ser notarizado pelas autoridades da Apple, resolvendo convenientemente o nosso problema.

O novo instalador .dmg do I2P, criado por Zlatinb, torna a instalação do I2P no OSX mais fácil do que nunca, não exigindo mais que os usuários instalem o Java por conta própria e usando as ferramentas padrão de instalação do OSX da maneira prescrita. O novo instalador .dmg torna a configuração do I2P no Mac OSX mais fácil do que jamais foi.

Obtenha o [dmg](https://geti2p.net/en/download/mac)

## O I2P do futuro é fácil de instalar

Uma das coisas que mais ouço dos usuários é que, se o I2P quer ser adotado, precisa ser fácil de usar. Muitos deles querem uma experiência de uso “estilo Tor Browser”, para citar ou parafrasear muitos usuários do Reddit. A instalação não deve exigir etapas de “pós-instalação” complicadas e propensas a erros. Muitos usuários novos não estão preparados para lidar com a configuração do navegador de forma minuciosa e completa. Para resolver esse problema, criamos o I2P Profile Bundle, que configurava o Firefox para “simplesmente funcionar” automaticamente com o I2P. À medida que foi sendo desenvolvido, ele foi adicionando recursos de segurança e melhorando a integração com o próprio I2P. Na versão mais recente, ele **também** inclui um I2P Router completo, com tecnologia Jpackage. O I2P Firefox Profile agora é uma distribuição completa do I2P para Windows, com a única dependência restante sendo o próprio Firefox. Isso deve proporcionar um nível de conveniência sem precedentes para os usuários do I2P no Windows.

Obtenha o [instalador](https://geti2p.net/en/download#windows)
