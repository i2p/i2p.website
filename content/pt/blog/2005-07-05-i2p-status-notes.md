---
title: "Notas de status do I2P para 2005-07-05"
date: 2005-07-05
author: "jr"
description: "Atualização semanal sobre o progresso do transporte SSU, a mitigação de ataque ao IV do tunnel e a otimização do MAC do SSU com HMAC-MD5"
categories: ["status"]
---

Olá, pessoal, chegou aquela hora da semana,

* Index

1) Status do desenvolvimento 2) Tunnel IVs (vetores de inicialização) 3) SSU MACs (códigos de autenticação de mensagens) 4) ???

* 1) Dev status

Mais uma semana, mais uma mensagem dizendo "Tem havido muito progresso no transporte SSU" ;) Minhas modificações locais estão estáveis e foram enviadas ao CVS (HEAD está em 0.5.0.7-9), mas ainda não há lançamento. Mais novidades nessa frente em breve. Detalhes sobre as alterações não relacionadas ao SSU estão no histórico [1], embora eu esteja mantendo as alterações relacionadas ao SSU fora dessa lista por enquanto, já que SSU ainda não é usado por nenhum não-desenvolvedor ainda (e os desenvolvedores leem i2p-cvs@ :)

[1] http://dev.i2p.net/cgi-bin/cvsweb.cgi/i2p/history.txt?rev=HEAD

* 2) Tunnel IVs

Nos últimos dias, dvorak tem postado reflexões ocasionais sobre diferentes maneiras de atacar a criptografia do tunnel e, embora a maioria já tenha sido abordada, conseguimos conceber um cenário que permitiria aos participantes marcar um par de mensagens para determinar que elas estão no mesmo tunnel. O funcionamento seria o seguinte: o par anterior deixaria uma mensagem passar por ele e, mais tarde, pegaria o IV (vetor de inicialização) e o primeiro bloco de dados daquela primeira mensagem do tunnel e os colocaria em uma nova. Essa nova estaria, claro, corrompida, mas não pareceria um ataque de repetição, já que os IVs eram diferentes. Mais adiante, o segundo par poderia então simplesmente descartar essa mensagem, de modo que a extremidade do tunnel não pudesse detectar o ataque.

Um dos problemas centrais por trás disso é que não há como verificar uma mensagem de tunnel conforme ela percorre o tunnel sem abrir espaço para uma série de ataques (consulte uma proposta anterior de criptografia de tunnel [2] para um método que chega perto, mas tem probabilidades bastante questionáveis e impõe alguns limites artificiais aos tunnels).

[2] http://dev.i2p.net/cgi-bin/cvsweb.cgi/i2p/router/doc/tunnel.html?rev=HEAD

Há, no entanto, uma maneira trivial de contornar o ataque específico descrito - basta tratar xor(IV, first data block) como o identificador único passado pelo filtro de Bloom em vez do IV (vetor de inicialização) sozinho. Assim, os pares intermediários verão o duplicado e o descartarão antes que ele alcance o segundo par em conluio. O CVS foi atualizado para incluir essa defesa, embora eu duvide muito, mas muito, que seja uma ameaça prática dado o tamanho atual da rede, então não estou lançando isso como uma versão por si só.

Isto não afeta, no entanto, a viabilidade de outros ataques de temporização ou de modelagem de tráfego, mas é melhor resolver os ataques mais fáceis de tratar assim que os vemos.

* 3) SSU MACs

Conforme descrito na especificação [3], o transporte SSU usa um MAC para cada datagrama transmitido. Isso é, além do hash de verificação enviado com cada mensagem I2NP (assim como os hashes de verificação de ponta a ponta nas mensagens de cliente). No momento, a especificação e o código usam um HMAC-SHA256 truncado - transmitindo e verificando apenas os primeiros 16 bytes do MAC. Isso é *cof* um pouco ineficiente, já que o HMAC usa o hash SHA256 duas vezes em sua operação, cada vez executando com um hash de 32 bytes, e o perfilamento recente do transporte SSU sugere que isso está perto do caminho crítico do uso de CPU. Sendo assim, fiz alguns experimentos substituindo o HMAC-SHA256-128 por um HMAC-MD5(-128) simples - embora o MD5 seja claramente menos robusto que o SHA256, estamos truncando o SHA256 para o mesmo tamanho do MD5 de qualquer forma, então a quantidade de força bruta necessária para causar colisão é a mesma (2^64 tentativas). Estou experimentando com isso no momento e o ganho é substancial (obtendo mais de 3x a vazão de HMAC em pacotes de 2KB do que com SHA256), então talvez possamos colocar isso em produção. Ou, se alguém puder apresentar um ótimo motivo para não fazê-lo (ou uma alternativa melhor), é simples o suficiente substituir (apenas uma linha de código).

[3] http://dev.i2p.net/cgi-bin/cvsweb.cgi/i2p/router/doc/udp.html?rev=HEAD

* 4) ???

É isso por enquanto e, como sempre, fiquem à vontade para publicar seus pensamentos e preocupações a qualquer momento. O CVS HEAD agora é compilável novamente para quem não tem o junit instalado (por enquanto eu retirei os testes de i2p.jar, mas ainda podem ser executados com o test ant target), e espero que haja mais novidades sobre os testes da 0.6 em breve (ainda estou lutando com as esquisitices da colo box (servidor em colocation) no momento - fazer telnet para minhas próprias interfaces falha localmente (sem nenhum errno útil), funciona remotamente, tudo isso sem qualquer iptables ou outros filtros. alegria). Ainda não tenho acesso à rede em casa, então não estarei disponível para uma reunião hoje à noite, mas talvez na próxima semana.

=jr
