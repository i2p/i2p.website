---
title: "Conheça o seu mantenedor: StormyCloud"
date: 2022-09-07
author: "sadie"
description: "Uma entrevista com os mantenedores do StormyCloud Outproxy"
categories: ["general"]
---

## Uma conversa com a StormyCloud Inc.

Com o [lançamento do I2P Java](https://geti2p.net/en/blog/2022/08/22/1.9.0-Release) mais recente, o outproxy (proxy de saída) existente, false.i2p, foi substituído pelo novo outproxy StormyCloud para novas instalações do I2P. Para quem está atualizando seu router, a mudança para o serviço Stormycloud pode ser feita rapidamente.

No seu Gerenciador de Serviços Ocultos, altere tanto Outproxies quanto SSL Outproxies para exit.stormycloud.i2p e clique no botão de salvar na parte inferior da página.

## Quem é a StormyCloud Inc?

**Missão da StormyCloud Inc.**

Defender o acesso à Internet como um direito humano universal. Ao fazer isso, o grupo protege a privacidade eletrônica dos usuários e constrói comunidade ao fomentar o acesso irrestrito à informação e, assim, a livre troca de ideias além-fronteiras. Isso é essencial porque a Internet é a ferramenta mais poderosa disponível para fazer uma diferença positiva no mundo.

**Declaração de Visão**

Tornar-se pioneiro em fornecer uma Internet livre e aberta a todos no universo, porque o acesso à Internet é um direito humano básico ([https://stormycloud.org/about-us/](https://stormycloud.org/about-us/))

Encontrei-me com Dustin para dizer olá e conversar mais sobre privacidade, a necessidade de serviços como o StormyCloud e o que atraiu a empresa ao I2P.

**Qual foi a inspiração por trás da criação da StormyCloud?**

No final de 2021, eu estava no subreddit /r/tor. Havia uma pessoa que respondeu em um tópico sobre como usar o Tor e disse que dependia do Tor para manter contato com a família. A família dessa pessoa vivia nos Estados Unidos, mas, na época, ela morava em um país onde o acesso à internet era muito restrito. Essa pessoa precisava ser muito cautelosa quanto a com quem se comunicava e o que dizia. Por esses motivos, ela confiava no Tor. Pensei em como posso me comunicar com as pessoas sem medo ou restrições e que deveria ser assim para todos.

O objetivo da StormyCloud é ajudar o maior número de pessoas possível a fazer isso.

**Quais têm sido alguns dos desafios para colocar a StormyCloud em funcionamento?**

O custo — é absurdamente elevado. Escolhemos recorrer a um centro de dados, pois a escala do que estamos a fazer não é algo que possa ser feito numa rede doméstica. Há despesas com equipamento e custos recorrentes de alojamento.

No que diz respeito à criação da organização sem fins lucrativos, seguimos os passos da Emerald Onion e utilizamos alguns de seus documentos e lições aprendidas. A comunidade do Tor tem muitos recursos disponíveis que são muito úteis.

**Como tem sido a receptividade aos seus serviços?**

Em julho, atendemos 1,5 bilhão de requisições DNS em todos os nossos serviços. As pessoas valorizam o fato de não haver geração de logs. Os dados simplesmente não estão lá, e as pessoas gostam disso.

**O que é um outproxy?**

Um outproxy (proxy de saída) é semelhante aos nós de saída do Tor, pois permite que o tráfego da clearnet (tráfego normal da Internet) seja encaminhado pela rede I2P. Em outras palavras, permite que os usuários da I2P acessem a Internet por meio da segurança da rede I2P.

**O que há de especial no Outproxy I2P da StormyCloud?**

Para começar, somos multi-homed, o que significa que temos vários servidores atendendo tráfego de outproxy (proxy de saída do I2P). Isso garante que o serviço esteja sempre disponível para a comunidade. Todos os logs em nossos servidores são apagados a cada 15 minutos. Isso garante que nem as autoridades nem nós tenhamos acesso a quaisquer dados. Oferecemos suporte para visitar links onion do Tor através do outproxy, e nosso outproxy é bem rápido.

**Como você define privacidade? Quais são alguns dos problemas que você vê em relação à ingerência excessiva e ao tratamento de dados?**

Privacidade é estar livre de acesso não autorizado. Transparência é importante, como no caso do opt-in — exemplo disso são os requisitos do GDPR.

Há grandes empresas acumulando dados que são usados para [acesso a dados de localização sem mandado](https://www.eff.org/deeplinks/2022/08/fog-revealed-guided-tour-how-cops-can-browse-your-location-data). Há uma intromissão excessiva das empresas de tecnologia naquilo que as pessoas consideram — e que deveria ser — privado, como fotos ou mensagens.

É importante continuar fazendo divulgação sobre como manter suas comunicações seguras e quais ferramentas ou aplicativos ajudarão uma pessoa a fazer isso. A forma como interagimos com todas as informações disponíveis também é importante. Precisamos confiar, mas verificar.

**Como o I2P se encaixa na Declaração de Missão e Visão da StormyCloud?**

I2P é um projeto de código aberto, e o que oferece está alinhado à missão da StormyCloud Inc. I2P fornece uma camada de privacidade e proteção para o tráfego e a comunicação, e o projeto acredita que todos têm direito à privacidade.

Tomamos conhecimento do I2P no início de 2022 ao conversar com pessoas da comunidade Tor e gostamos do que o projeto estava fazendo. Parecia semelhante ao Tor.

Durante nossa introdução ao I2P e às suas capacidades, vimos a necessidade de um outproxy (proxy de saída) confiável. Tivemos um apoio realmente excelente de pessoas da comunidade I2P para criar e começar a fornecer o serviço de outproxy.

**Conclusão**

A necessidade de sensibilização sobre a vigilância do que deveria ser privado nas nossas vidas online é contínua. A recolha de quaisquer dados deve ser consensual, e a privacidade deve ser implícita.

Quando não podemos confiar que o nosso tráfego ou a nossa comunicação não sejam monitorados sem o nosso consentimento, felizmente temos acesso a redes que, por design, anonimizarão o tráfego e ocultarão a nossa localização.

Obrigado à StormyCloud e a todos que fornecem outproxies (proxies de saída) ou nós do Tor e do I2P, para que as pessoas possam acessar a internet com mais segurança quando precisarem. Espero ver mais pessoas interligando as capacidades dessas redes complementares para criar um ecossistema de privacidade mais robusto para todos.

Saiba mais sobre os serviços da StormyCloud Inc. em [https://stormycloud.org/](https://stormycloud.org/) e ajude a apoiar o trabalho da StormyCloud Inc. fazendo uma doação em [https://stormycloud.org/donate/](https://stormycloud.org/donate/).
