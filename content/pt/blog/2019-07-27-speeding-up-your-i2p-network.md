---
title: "Acelerando sua rede I2P"
date: 2019-07-27
author: "mhatta"
description: "Acelerando sua rede I2P"
categories: ["tutorial"]
---

*Este post foi adaptado diretamente de material criado originalmente para o de mhatta* [medium blog](https://medium.com/@mhatta/speeding-up-your-i2p-network-c08ec9de225d) *.* *Ele merece o crédito pelo post original (OP). Foi atualizado em certos trechos onde* *se refere a versões antigas de I2P como se fossem atuais e passou por uma* *edição leve. -idk*

Logo após iniciar, o I2P costuma parecer um pouco lento. É verdade, e todos nós sabemos por quê: por sua natureza, [garlic routing](https://en.wikipedia.org/wiki/Garlic_routing) (roteamento 'garlic') adiciona sobrecarga à experiência familiar de usar a internet para que você tenha privacidade, mas isso significa que, para muitos ou para a maioria dos serviços do I2P, seus dados precisarão passar por 12 saltos por padrão.

![Análise de ferramentas para anonimato online](https://www.researchgate.net/publication/289531182_An_analysis_of_tools_for_online_anonymity)

Além disso, ao contrário do Tor, o I2P foi projetado principalmente como uma rede fechada. Você pode acessar facilmente [eepsites](https://medium.com/@mhatta/how-to-set-up-untraceable-websites-eepsites-on-i2p-1fe26069271d) ou outros recursos dentro do I2P, mas não se destina a acessar sites da [clearnet](https://en.wikipedia.org/wiki/Clearnet_(networking)) (internet aberta) por meio do I2P. Existem alguns "outproxies" do I2P (proxies de saída), semelhantes aos nós de saída do [Tor](https://en.wikipedia.org/wiki/Tor_(anonymity_network)), para acessar a clearnet, mas a maioria deles é muito lenta de usar, pois ir para a clearnet é, efetivamente, *mais um* salto na conexão que já tem 6 saltos de entrada e seis de saída.

Até algumas versões atrás, esse problema era ainda mais difícil de lidar, porque muitos usuários de I2P router estavam tendo dificuldades para configurar as configurações de largura de banda de seus routers. Se todos os que puderem dedicarem tempo para ajustar corretamente suas configurações de largura de banda, melhorarão não apenas a sua conexão, mas também a rede I2P como um todo.

## Ajustando os limites de largura de banda

Como o I2P é uma rede peer-to-peer, você precisa compartilhar parte da sua largura de banda de rede com outros pares. Você pode escolher quanto em "I2P Bandwidth Configuration" (botão "Configure Bandwidth" na seção "Applications and Configuration" do I2P Router Console, ou em http://localhost:7657/config).

![Configuração de Largura de Banda do I2P](https://geti2p.net/images/blog/bandwidthmenu.png)

Se você vir um limite de largura de banda compartilhada de 48 KBps, que é muito baixo, então é possível que você não tenha ajustado sua largura de banda compartilhada a partir do valor padrão. Como observou o autor original do material do qual este post de blog foi adaptado, o I2P tem um limite padrão de largura de banda compartilhada que é muito baixo até que o usuário o ajuste, para evitar causar problemas com a conexão do usuário.

No entanto, como muitos usuários podem não saber exatamente quais configurações de largura de banda ajustar, o [lançamento do I2P 0.9.38](https://geti2p.net/en/download) introduziu um Assistente de Nova Instalação. Ele contém um Teste de Largura de Banda, que detecta automaticamente (graças ao [NDT](https://www.measurementlab.net/tests/ndt/) do M-Lab) e ajusta as configurações de largura de banda do I2P de acordo.

Se você quiser executar novamente o assistente, por exemplo após uma mudança no seu provedor de serviços ou porque instalou o I2P antes da versão 0.9.38, você pode iniciá-lo novamente pelo link 'Setup' na página 'Help & FAQ', ou simplesmente acessar o assistente diretamente em http://localhost:7657/welcome

![Você consegue encontrar "Setup"?](https://geti2p.net/images/blog/sidemenu.png)

Usar o Assistente é simples, basta continuar clicando em "Next". Às vezes, os servidores de medição escolhidos pelo M-Lab estão fora do ar e o teste falha. Nesse caso, clique em "Previous" (não use o botão "back" do seu navegador), depois tente novamente.

![Resultados do Teste de Largura de Banda](https://geti2p.net/images/blog/bwresults.png)

## Executando o I2P continuamente

Mesmo após ajustar a largura de banda, sua conexão ainda pode ficar lenta. Como eu disse, o I2P é uma rede P2P. Levará algum tempo para o seu I2P router ser descoberto por outros pares e integrado à rede I2P. Se o seu router não ficar tempo suficiente em funcionamento para se integrar bem, ou se você o desligar de forma abrupta com muita frequência, a rede permanecerá relativamente lenta. Por outro lado, quanto mais tempo você mantiver seu I2P router em execução continuamente, mais rápida e estável sua conexão se tornará, e mais da sua cota de largura de banda será utilizada na rede.

No entanto, muitas pessoas podem não conseguir manter o I2P router em funcionamento. Nesse caso, ainda é possível executar o I2P router em um servidor remoto, como um VPS, e então usar encaminhamento de portas via SSH.
