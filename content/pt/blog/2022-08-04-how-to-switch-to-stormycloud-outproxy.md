---
title: "Como alternar para o serviço de outproxy (proxy de saída) da StormyCloud"
date: 2022-08-04
author: "idk"
description: "Como alternar para o serviço de outproxy (proxy de saída) da StormyCloud"
categories: ["general"]
---

## Como mudar para o serviço de Outproxy da StormyCloud

**Um novo outproxy profissional**

Durante anos, o I2P tem sido atendido por um único outproxy (proxy de saída) padrão, `false.i2p`, cuja confiabilidade vem se deteriorando. Embora tenham surgido vários concorrentes para suprir parte da demanda, em geral eles não conseguem se voluntariar para atender, por padrão, aos clientes de uma implementação inteira do I2P. No entanto, a StormyCloud, uma organização profissional sem fins lucrativos que opera nós de saída do Tor, iniciou um novo serviço profissional de outproxy, que foi testado por membros da comunidade do I2P e que se tornará o novo outproxy padrão na próxima versão.

**Quem é a StormyCloud**

Nas próprias palavras deles, a StormyCloud é:

> Missão da StormyCloud Inc: Defender o acesso à Internet como um direito humano universal. Ao fazer isso, o grupo protege a privacidade eletrônica dos usuários e constrói comunidade ao fomentar o acesso irrestrito à informação e, assim, a livre troca de ideias além das fronteiras. Isso é essencial porque a Internet é a ferramenta mais poderosa disponível para causar um impacto positivo no mundo.

> Hardware: Somos proprietários de todo o nosso hardware e, atualmente, fazemos colocation em um data center Tier 4. No momento, temos um uplink de 10GBps, com a opção de atualização para 40GBps, sem necessidade de muitas alterações. Temos nosso próprio ASN e espaço de endereços IP (IPv4 e IPv6).

Para saber mais sobre a StormyCloud, visite o [site deles](https://www.stormycloud.org/).

Ou, visite-os no [I2P](http://stormycloud.i2p/).

**Mudando para o Outproxy StormyCloud (proxy de saída) no I2P**

Para alternar para o outproxy (proxy de saída) StormyCloud *hoje*, você pode visitar [the Hidden Services Manager](http://127.0.0.1:7657/i2ptunnel/edit?tunnel=0) (Gerenciador de Serviços Ocultos). Quando estiver lá, você deve alterar o valor de **Outproxies** e **SSL Outproxies** para `exit.stormycloud.i2p`. Depois de fazer isso, role até a parte inferior da página e clique no botão "Save".

**Agradecimentos a StormyCloud**

Gostaríamos de agradecer a StormyCloud por se voluntariar para fornecer serviços de outproxy (proxy de saída) de alta qualidade à rede I2P.
