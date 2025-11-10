---
title: "Notas de status do I2P de 2004-08-24"
date: 2004-08-24
author: "jr"
description: "Atualização semanal de status do I2P abordando o lançamento da versão 0.3.4.3, novos recursos do console do router, progresso da versão 0.4 e diversas melhorias"
categories: ["status"]
---

Olá a todos, muitas atualizações hoje

## Índice

1. 0.3.4.3 status
   1.1) timestamper
   1.2) new router console authentication
2. 0.4 status
   2.1) service & systray integration
   2.2) jbigi & jcpuid
   2.3) i2paddresshelper
3. AMOC vs. restricted routes
4. stasher
5. pages of note
6. ???

## 1) 0.3.4.3 estado

A versão 0.3.4.3 foi lançada na sexta-feira passada e, desde então, as coisas têm corrido muito bem. Houve alguns problemas com código recém-introduzido de testes de tunnel e de seleção de pares, mas, após alguns ajustes desde o lançamento, está bastante estável. Não sei se o servidor IRC já está na nova revisão, então geralmente precisamos depender de testes com eepsites(Sites I2P) e os http outproxies (squid.i2p e www1.squid.i2p). Transferências de arquivos grandes (>5MB) na versão 0.3.4.3 ainda não são suficientemente confiáveis, mas, nos meus testes, as modificações desde então melhoraram as coisas ainda mais.

A rede também vem crescendo - atingimos 45 usuários simultâneos mais cedo hoje e temos ficado consistentemente na faixa de 38-44 usuários há alguns dias (w00t)! Esse é um número saudável por enquanto, e venho monitorando a atividade geral da rede para observar possíveis riscos. Ao migrarmos para a versão 0.4, vamos querer aumentar gradualmente a base de usuários até por volta da marca de 100 routers e testar mais um pouco antes de crescer ainda mais. Pelo menos, esse é o meu objetivo do ponto de vista de desenvolvedor.

### 1.1) timestamper

Uma das coisas totalmente sensacionais que mudou com a versão 0.3.4.3 e que eu acabei esquecendo completamente de mencionar foi uma atualização no código do SNTP. Graças à generosidade de Adam Buckley, que concordou em publicar seu código SNTP sob a licença BSD, incorporamos o antigo aplicativo Timestamper ao núcleo do I2P SDK e o integramos completamente ao nosso relógio. Isso significa três coisas: 1. você pode excluir o timestamper.jar (o código está no i2p.jar agora) 2. você pode remover as linhas relacionadas a clientApp da sua configuração 3. você pode atualizar sua configuração para usar as novas opções de sincronização de tempo

As novas opções no router.config são simples, e os valores padrão devem ser bons o suficiente (isso é especialmente verdade, já que a maioria de vocês os usa involuntariamente :)

Para definir a lista de servidores SNTP a consultar:

```
time.sntpServerList=pool.ntp.org,pool.ntp.org,pool.ntp.org
```
Para desativar a sincronização de tempo (apenas se você for um guru de NTP e souber que o relógio do seu sistema operacional está *sempre* correto - executar "windows time" NÃO é suficiente):

```
time.disabled=true
```
Você não precisa mais ter uma 'timestamper password' (senha de carimbo de tempo), já que tudo está integrado diretamente no código (ah, as alegrias de BSD vs GPL :)

### 1.2) new router console authentication

Isto é relevante apenas para aqueles de vocês que estão executando o novo console do router, mas, se você o tiver escutando em uma interface pública, talvez queira aproveitar a autenticação HTTP básica integrada. Sim, a autenticação HTTP básica é absurdamente fraca — ela não protegerá contra quem captura o tráfego da sua rede ou entra por força bruta, mas manterá afastado o bisbilhoteiro ocasional. De qualquer forma, para usá-la, basta adicionar a linha

```
consolePassword=blah
```
ao seu router.config. Infelizmente, você terá que reiniciar o router, pois esse parâmetro é passado ao Jetty apenas uma vez (durante a inicialização).

## 2) 0.4 status

Estamos avançando bastante na versão 0.4, e esperamos disponibilizar algumas versões prévias na próxima semana. Ainda estamos acertando alguns detalhes, então não temos um processo de atualização sólido definido ainda. Essa versão será compatível com versões anteriores, portanto, a atualização não deve ser muito trabalhosa. De qualquer forma, fique atento e saberá quando tudo estiver pronto.

### 1.1) carimbador de tempo

Hypercubus está avançando bastante na integração do instalador, de um aplicativo da bandeja do sistema e de algum código de gerenciamento de serviços. Basicamente, na versão 0.4, todos os usuários do Windows terão automaticamente um pequeno ícone na bandeja do sistema (Iggy!), embora possam desativá-lo (e/ou reativá-lo) pelo console web. Além disso, vamos incluir o JavaService wrapper, o que nos permitirá fazer uma série de coisas interessantes, como executar o I2P na inicialização do sistema (ou não), reinicializar automaticamente em determinadas condições, realizar uma reinicialização forçada da JVM sob demanda, gerar rastreamentos de pilha e várias outras funcionalidades úteis.

### 1.2) nova autenticação do console do router

Uma das grandes atualizações na versão 0.4 será uma reformulação do código do jbigi, mesclando as modificações que Iakin fez para o Freenet, bem como a nova biblioteca nativa "jcpuid" de Iakin. A biblioteca jcpuid funciona apenas em arquiteturas x86 e, em conjunto com algum código novo do jbigi, determinará qual é o jbigi 'correto' a ser carregado. Assim, passaremos a distribuir um único jbigi.jar que todos terão e, a partir dele, selecionar o 'correto' para a máquina atual. As pessoas continuarão, é claro, podendo compilar seu próprio jbigi nativo, sobrepondo-se ao que o jcpuid determinar (basta compilá-lo e copiá-lo para o diretório de instalação do I2P, ou nomeá-lo "jbigi" e colocá-lo em um arquivo .jar no seu classpath (caminho de classes)). No entanto, por causa das atualizações, ele *não* é retrocompatível - ao atualizar, você deve ou recompilar seu próprio jbigi ou remover sua biblioteca nativa existente (para permitir que o novo código do jcpuid escolha o correto).

### 2.3) i2paddresshelper

oOo preparou um utilitário muito interessante para permitir que as pessoas naveguem por eepsites(I2P Sites) sem atualizar seu hosts.txt. Já foi integrado ao CVS e será implantado na próxima versão, mas talvez valha a pena considerar atualizar os links de acordo (cervantes atualizou o bbcode [i2p] do forum.i2p para oferecer suporte a isso com um link "Try it [i2p]").

Basicamente, basta criar um link para o eepsite(I2P Site) com o nome que quiser e, em seguida, acrescentar um parâmetro especial de URL especificando o destino:

```
http://wowthisiscool.i2p/?i2paddresshelper=FpCkYW5pw...
```
Nos bastidores, é bastante seguro - você não pode falsificar outro endereço, e o nome *não* fica gravado em hosts.txt, mas isso permitirá que você veja imagens / etc vinculadas em eepsites(I2P Sites) que você não conseguiria com o antigo truque `http://i2p/base64/`. Se você quiser sempre poder usar "wowthisiscool.i2p" para acessar esse site, ainda vai, claro, ter que adicionar a entrada ao seu hosts.txt (até que o catálogo de endereços do MyI2P seja disponibilizado, isto é ;)

## 3) AMOC vs. restricted routes

Mule vem reunindo algumas ideias e me instando a explicar algumas coisas e, nesse processo, vem obtendo algum progresso em me levar a reavaliar toda a ideia de AMOC. Especificamente, se abrirmos mão de uma das restrições que impus à nossa camada de transporte - permitindo-nos assumir bidirecionalidade - talvez possamos abandonar todo o transporte AMOC, implementando em seu lugar uma operação básica de rota restrita (deixando os fundamentos para técnicas de rota restrita mais avançadas, como pares confiáveis e multihop router tunnels, para depois).

Se seguirmos esta abordagem, isso significaria que as pessoas poderiam participar da rede por trás de firewalls, NATs, etc., sem qualquer configuração, além de oferecer algumas das propriedades de anonimato de rota restrita. Por sua vez, isso provavelmente implicaria uma grande reformulação do nosso roteiro, mas, se conseguirmos fazê-lo com segurança, nos pouparia uma enorme quantidade de tempo e valeria muito a pena a mudança.

No entanto, não queremos apressar as coisas e precisaremos avaliar cuidadosamente as implicações para o anonimato e a segurança antes de nos comprometermos com essa abordagem. Faremos isso depois que 0.4 for lançada e estiver funcionando sem problemas, então não há pressa.

## 2) 0.4 status

Dizem por aí que aum está fazendo um bom progresso - não sei se ele vai estar por aqui na reunião para trazer uma atualização, mas ele nos deixou um trecho no #i2p esta manhã:

```
<aum> hi all, can't talk long, just a quick stasher update - work is
      continuing on implementing freenet keytypes, and freenet FCP
      compatibility - work in progress, should have a test build
      ready to try out by the end of the week
```
Uhul.

## 5) pages of note

Quero apenas destacar dois novos recursos disponíveis que os usuários do I2P talvez queiram conferir — DrWoo montou uma página com um monte de informações para quem deseja navegar anonimamente, e Luckypunk publicou um howto descrevendo suas experiências com algumas JVMs (Máquinas Virtuais Java) no FreeBSD. Hypercubus também publicou a documentação sobre como testar o serviço e a integração com a systray (área de notificação), ainda não lançados.

## 6) ???

Ok, isso é tudo o que tenho a dizer no momento - apareça na reunião hoje às 21h GMT se quiser trazer mais alguma coisa.

=jr
