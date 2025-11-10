---
title: "Notas de status do I2P de 2005-07-12"
date: 2005-07-12
author: "jr"
description: "Atualização semanal cobrindo a restauração de serviços, o progresso dos testes de SSU e a análise da camada criptográfica do I2CP para potencial simplificação"
categories: ["status"]
---

Hi y'all, its that time of the week again

* Index

1) squid/www/cvs/dev.i2p restaurado 2) Testes de SSU 3) Criptografia do I2CP 4) ???

* 1) squid/www/cvs/dev.i2p restored

Depois de quebrar a cabeça com vários servidores em colocation, alguns dos serviços antigos foram restaurados - squid.i2p (um dos dois outproxies (proxies de saída) padrão), www.i2p (um apontador seguro para www.i2p.net), dev.i2p (um apontador seguro para dev.i2p.net, onde se encontram os arquivos das listas de discussão, o cvsweb e as sementes padrão do netDb), e cvs.i2p (um apontador seguro para o nosso servidor CVS - cvs.i2p.net:2401). Meu blog ainda está fora do ar, mas o conteúdo se perdeu de qualquer forma, então vai ser preciso recomeçar do zero mais cedo ou mais tarde. Agora que esses serviços voltaram a ficar online de forma confiável, é hora de seguir adiante para o...

* 2) SSU testing

Como mencionado naquela pequena caixa amarela no console do router de todos, iniciamos a próxima rodada de testes na rede real para o SSU. Os testes não são para todos, mas, se você for aventureiro e estiver confortável em fazer alguma configuração manual, confira os detalhes indicados no seu console do router (http://localhost:7657/index.jsp). Pode haver várias rodadas de testes, mas não prevejo mudanças significativas no SSU antes da versão 0.6 (a 0.6.1 adicionará suporte para aqueles que não podem redirecionar as suas portas ou receber conexões UDP de entrada por outros meios).

* 3) I2CP crypto

Ao revisar novamente a nova documentação introdutória, estou tendo alguma dificuldade para justificar a camada adicional de criptografia realizada dentro do I2CP SDK. A intenção original da camada criptográfica do I2CP era fornecer uma proteção básica de ponta a ponta das mensagens transmitidas, bem como permitir que clientes I2CP (também chamados de I2PTunnel, the SAM bridge, I2Phex, azneti2p, etc) se comunicassem por meio de routers não confiáveis. À medida que a implementação progrediu, contudo, a proteção de ponta a ponta da camada I2CP tornou-se redundante, pois todas as mensagens do cliente são criptografadas de ponta a ponta dentro de garlic messages (mensagens no formato garlic) pelo router, agregando o leaseSet do remetente e, às vezes, uma mensagem de status de entrega. Essa camada garlic já fornece criptografia de ponta a ponta do router do remetente ao router do destinatário - a única diferença é que isso não protege contra o próprio router ser hostil.

Olhando para os casos de uso previsíveis, porém, não consigo pensar em um cenário válido em que o router local não seria confiável. No mínimo, a criptografia do I2CP apenas oculta o conteúdo da mensagem transmitida a partir do router - o router ainda precisa saber para qual destino ela deve ser enviada. Se necessário, podemos adicionar um listener (serviço de escuta) I2CP via SSH/SSL para permitir que o cliente I2CP e o router operem em máquinas separadas, ou pessoas que precisarem disso podem usar ferramentas de tunelamento existentes.

Apenas para reiterar as camadas de criptografia utilizadas neste momento, temos:  * A camada ElGamal/AES+SessionTag de ponta a ponta do I2CP, criptografando do
    destino do remetente ao destino do destinatário.  * A camada de garlic encryption de ponta a ponta do router
    (ElGamal/AES+SessionTag), criptografando do router do remetente ao
    router do destinatário.  * A camada de criptografia de tunnel para ambos os tunnels de entrada e de saída
    nos saltos ao longo de cada um (mas não entre o ponto final de saída
    e o gateway de entrada).  * A camada de criptografia de transporte entre cada router.

Quero ser bastante cauteloso ao remover uma dessas camadas, mas não quero desperdiçar nossos recursos fazendo trabalho desnecessário. O que estou propondo é remover aquela primeira camada de criptografia do I2CP (mas, é claro, mantendo a autenticação usada durante o estabelecimento da sessão do I2CP, a autorização do leaseSet e a autenticação do remetente). Alguém consegue pensar em um motivo para mantê-la?

* 4) ???

É isso por enquanto, mas, como sempre, há muita coisa acontecendo. Ainda sem reunião esta semana, mas, se alguém tiver algo a tratar, por favor não hesite em publicar na lista ou no fórum. Além disso, embora eu leia o scrollback (histórico do chat) no #i2p, perguntas ou preocupações gerais devem ser enviadas à lista, para que mais pessoas possam participar da discussão.

=jr
