---
title: "Sobre o I2P"
description: "Saiba mais sobre o The Invisible Internet Project - uma rede de sobreposição ponto a ponto totalmente criptografada, projetada para comunicação anônima."
tagline: "The Invisible Internet Project"
type: "sobre"
layout: "sobre"
established: "2002"
---

O The Invisible Internet Project começou em 2002. A visão do projeto era que a Rede I2P "oferecesse anonimato total, privacidade e segurança no mais alto nível possível. Internet descentralizada e ponto a ponto significa não se preocupar mais com o seu provedor de serviços de internet controlando seu tráfego. Isso permitirá que as pessoas realizem atividades sem interrupções e mudem a forma como vemos a segurança e até mesmo a Internet, utilizando criptografia de chave pública, esteganografia de IP e autenticação de mensagens. A Internet que deveria ter sido, será em breve."

Desde então, o I2P evoluiu para especificar e implementar um conjunto completo de protocolos de rede capazes de fornecer um alto nível de privacidade, segurança e autenticação para uma variedade de aplicações.

## A Rede I2P

A rede I2P é uma rede de sobreposição ponto a ponto totalmente criptografada. Um observador não pode ver o conteúdo de uma mensagem, sua origem ou destino. Ninguém pode ver de onde vem o tráfego, para onde está indo ou qual é o conteúdo. Além disso, os transportes do I2P oferecem resistência ao reconhecimento e bloqueio por censores. Como a rede depende de pares para rotear o tráfego, o bloqueio com base na localização é um desafio que cresce com a rede. Todo roteador na rede participa para tornar a rede anônima. Exceto em casos onde seria inseguro, todos participam do envio e recebimento de tráfego na rede.

## Como Conectar-se à Rede I2P

O software principal (Java) inclui um roteador que introduz e mantém uma conexão com a rede. Ele também oferece aplicações e opções de configuração para personalizar sua experiência e fluxo de trabalho. Saiba mais em nossa [documentação](/docs/).

## O Que Posso Fazer na Rede I2P?

A rede fornece uma camada de aplicação para serviços, aplicações e gerenciamento de rede. A rede também possui seu próprio DNS único que permite a auto-hospedagem e espelhamento de conteúdo da Internet (Clearnet). A rede I2P funciona da mesma forma que a Internet. O software Java inclui um cliente BitTorrent, e-mail, bem como um modelo de site estático. Outras aplicações podem ser facilmente adicionadas ao seu console do roteador.

## Uma Visão Geral da Rede

O I2P usa criptografia para alcançar uma variedade de propriedades para os túneis que constrói e as comunicações que transporta. Os túneis I2P usam transportes, [NTCP2](/docs/specs/ntcp2/) e [SSU2](/docs/specs/ssu2/), para ocultar o tráfego sendo transportado sobre eles. As conexões são criptografadas de roteador para roteador e de cliente para cliente (de ponta a ponta). A confidencialidade direta é fornecida para todas as conexões. Como o I2P é criptograficamente endereçado, os endereços de rede do I2P são auto-autenticadores e pertencem apenas ao usuário que os gerou.

A rede é composta por pares ("roteadores") e túneis virtuais unidirecionais de entrada e saída. Os roteadores se comunicam entre si usando protocolos construídos sobre mecanismos de transporte existentes (TCP, UDP), passando mensagens. As aplicações cliente possuem seu próprio identificador criptográfico ("Destinação") que lhes permite enviar e receber mensagens. Esses clientes podem conectar-se a qualquer roteador e autorizar a alocação temporária ("leasing") de alguns túneis que serão usados para enviar e receber mensagens através da rede. O I2P possui seu próprio banco de dados de rede interno (usando uma modificação do Kademlia DHT) para distribuir informações de roteamento e contato de forma segura.

## Sobre Descentralização e a Rede I2P

A rede I2P é quase completamente descentralizada, com exceção do que são chamados de Servidores de Reseed. Isso é para lidar com o problema de bootstrap do DHT (Tabela de Hash Distribuída). Basicamente, não existe um modo bom e confiável de operar, exceto operando pelo menos um nó bootstrap permanente que participantes fora da rede possam encontrar para começar. Uma vez conectado à rede, um roteador descobre apenas pares construindo túneis "exploratórios", mas para fazer a conexão inicial, é necessário um host de reseed para criar conexões e integrar um novo roteador à rede. Servidores de reseed podem observar quando um novo roteador baixou um reseed deles, mas nada mais sobre o tráfego na rede I2P.

## Comparações

Existem muitas outras aplicações e projetos trabalhando em comunicação anônima e o I2P foi inspirado por muitos de seus esforços. Esta não é uma lista abrangente de recursos de anonimidade - tanto a [Bibliografia sobre Anonimidade de freehaven](http://freehaven.net/anonbib/topic.html) quanto os [projetos relacionados ao GNUnet](https://www.gnunet.org/links/) cumprem bem esse propósito. Dito isso, alguns sistemas se destacam para uma comparação mais detalhada. Saiba mais sobre como o I2P se compara a outras redes de anonimato em nossa [documentação de comparação detalhada](/docs/overview/comparison/).
