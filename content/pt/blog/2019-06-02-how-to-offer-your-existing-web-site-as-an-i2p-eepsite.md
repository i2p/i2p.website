---
title: "Como disponibilizar seu site da Web existente como um eepSite do I2P"
date: 2019-06-02
author: "idk"
description: "Oferecendo um espelho do I2P"
categories: ["tutorial"]
---

Esta postagem de blog destina-se a servir como um guia geral para operar um espelho de um serviço da clear-net (internet aberta) como um eepSite. Ela aprofunda a postagem anterior do blog sobre I2PTunnel tunnels básicos.

Infelizmente, provavelmente é impossível cobrir *completamente* todos os casos possíveis de tornar um site existente disponível como um eepSite; há simplesmente uma gama diversa demais de software do lado do servidor, sem falar nas peculiaridades, na prática, de qualquer implantação específica de software. Em vez disso, vou tentar transmitir, da forma mais específica possível, o processo geral de preparação de um serviço para implantação no eepWeb ou em outros serviços ocultos.

Grande parte deste guia tratará o leitor como um interlocutor; em particular, se eu realmente quiser enfatizar, me dirigirei ao leitor diretamente(isto é, usando "you" em vez de "one") e frequentemente encabeçarei seções com perguntas que acho que o leitor pode estar se fazendo. Afinal, trata-se de um "processo" no qual um administrador deve considerar-se "envolvido", assim como ao hospedar qualquer outro serviço.

**ISENÇÕES DE RESPONSABILIDADE:**

Embora fosse ótimo, provavelmente é impossível para mim fornecer instruções específicas para todo e qualquer tipo de software que alguém possa usar para hospedar sites. Sendo assim, este tutorial exige algumas suposições por parte do autor e um pouco de pensamento crítico e bom senso por parte do leitor. Para deixar claro, **pressuponho que a pessoa que segue este tutorial já opera um serviço na web aberta (clearnet) associável a uma identidade real ou organização** e, portanto, está apenas oferecendo acesso anônimo e não buscando anonimizar-se.

Assim, **não faz absolutamente nenhuma tentativa de anonimizar** uma conexão de um servidor a outro. Se você quiser operar um novo serviço oculto não vinculável que hospede conteúdo não associado a você, então não deve fazê-lo a partir do seu próprio servidor de clearnet (internet aberta) ou da sua própria casa.
