---
title: "Notas de status do I2P de 2005-09-20"
date: 2005-09-20
author: "jr"
description: "Atualização semanal sobre o sucesso do lançamento da versão 0.6.0.6 com introduções do SSU, atualização de segurança do I2Phex 0.1.1.27 e conclusão da migração de colocation (hospedagem em data center)"
categories: ["status"]
---

Olá, pessoal, é terça-feira de novo

* Index:

1) 0.6.0.6 2) I2Phex 0.1.1.27 3) migração 4) ???

* 1) 0.6.0.6

Com a versão 0.6.0.6 lançada no último sábado, temos vários componentes novos em operação na rede ativa, e vocês fizeram um ótimo trabalho ao atualizar - até algumas horas atrás, quase 250 routers já tinham atualizado! A rede também parece estar indo bem, e as introduções têm funcionado até agora - você pode acompanhar sua própria atividade de introdução no http://localhost:7657/oldstats.jsp, observando os udp.receiveHolePunch e udp.receiveIntroRelayResponse (bem como udp.receiveRelayIntro, para quem está atrás de NATs).

A propósito, o "Status: ERR-Reject" na verdade já não é um erro, então talvez devêssemos alterá-lo para "Status: OK (NAT)"?

Houve alguns relatos de bugs no Syndie. Mais recentemente, há um bug em que ele falha em sincronizar com pares remotos se você pedir para baixar entradas demais de uma vez (já que, tolamente, usei HTTP GET em vez de POST). Vou adicionar suporte a POST ao EepGet, mas, por enquanto, tente buscar apenas 20 ou 30 posts por vez. A propósito, talvez alguém possa criar o JavaScript para a página remote.jsp que diga "buscar todos os posts desse usuário", marcando automaticamente todas as caixas de seleção do blog desse usuário?

Dizem por aí que o OSX agora funciona bem logo de cara e, com a 0.6.0.6-1, o x86_64 também está operacional tanto no Windows quanto no Linux. Não ouvi relatos de problemas com os novos instaladores .exe, então isso quer dizer que ou está indo bem ou falhando completamente :)

* 2) I2Phex 0.1.1.27

Motivado por alguns relatos de diferenças entre o código-fonte e o que foi incluído no pacote do legion da versão 0.1.1.26, bem como por preocupações quanto à segurança do iniciador nativo de código fechado, tomei a iniciativa de adicionar ao cvs um novo i2phex.exe compilado com o launch4j [1] e compilei a versão mais recente do cvs no i2p file archive [2]. Não se sabe se houve outras alterações feitas por legion no seu código-fonte antes do lançamento, ou se o código-fonte que ele disponibilizou é de fato o mesmo que o que ele compilou.

Por motivos de segurança, não posso recomendar o uso nem do lançador de código fechado do legion nem da versão 0.1.1.26. A versão no site do I2P [2] contém o código mais recente do cvs, sem modificações.

Você pode reproduzir a compilação primeiro obtendo e compilando o código do I2P, depois obtendo o código do I2Phex, e então executando "ant makeRelease":   mkdir ~/devi2p ; cd ~/devi2p/   cvs -d :pserver:anoncvs-PQcCzt6076/R7s880joybQ@xxxxxxxxxxxxxxxx/cvsroot login

# (senha: anoncvs)

cvs -d :pserver:anoncvs-PQcCzt6076/R7s880joybQ@xxxxxxxxxxxxxxxx/cvsroot co i2p   cd i2p ; ant build ; cd ..   cvs -d :pserver:anoncvs-PQcCzt6076/R7s880joybQ@xxxxxxxxxxxxxxxx/cvsroot co i2phex   cd i2phex/build ; ant makeRelease ; cd ../..   ls -l i2phex/release/i2phex-0.1.1.27.zip

O i2phex.exe dentro desse zip pode ser usado no Windows simplesmente executando-o, ou em *nix/osx via "java -jar i2phex.exe". Ele depende de que o I2Phex esteja instalado em um diretório ao lado do I2P - (por exemplo, C:\Program Files\i2phex\ e C:\Program Files\i2p\), pois faz referência a alguns dos arquivos jar do I2P.

Não vou assumir a manutenção do I2Phex, mas colocarei futuras versões do I2Phex no site quando houver atualizações no cvs. Se alguém quiser trabalhar numa página na web que possamos colocar no ar para descrevê-lo/apresentá-lo (sirup, você está por aí?), com links para sirup.i2p, posts úteis do fórum, a lista de pares ativos do legion, seria ótimo.

[1] http://launch4j.sourceforge.net/ [2] http://dev.i2p.net/i2p/i2phex-0.1.1.27.zip e     http://dev.i2p.net/i2p/i2phex-0.1.1.27.zip.sig (assinado pela minha chave)

* 3) migration

Substituímos as máquinas em colocation dos serviços i2p, mas agora tudo deve estar totalmente operacional na nova máquina - se você notar algo estranho, por favor, avise-me!

* 4) ???

Tem havido muita discussão interessante na lista do i2p recentemente, o novo e prático proxy/filtro SMTP do Adam, assim como algumas boas publicações no syndie (já viram o tema do gloin em http://gloinsblog.i2p?). Estou trabalhando em algumas mudanças no momento para alguns problemas de longa data, mas elas não são iminentes. Se alguém tiver mais alguma coisa que queira trazer à tona e discutir, apareça na reunião em #i2p às 20h GMT (daqui a uns 10 minutos).

=jr
