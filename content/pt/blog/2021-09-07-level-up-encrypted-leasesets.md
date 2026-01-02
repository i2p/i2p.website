---
title: "Aprimore suas habilidades em I2P com LeaseSets criptografados"
date: 2021-09-07
slug: "level-up-your-i2p-skills-with-encrypted-leasesets"
author: "idk"
description: "Diz-se que o I2P enfatiza Serviços Ocultos, examinamos uma interpretação disso"
categories: ["general"]
---

## Aprimore suas habilidades em I2P com LeaseSets criptografados

Já se afirmou no passado que o I2P enfatiza o suporte a serviços ocultos, o que é verdadeiro de muitas maneiras. No entanto, o que isso significa para usuários, desenvolvedores e administradores de serviços ocultos nem sempre é o mesmo. LeaseSets criptografados e seus casos de uso oferecem uma janela única e prática sobre como o I2P torna os serviços ocultos mais versáteis, mais fáceis de administrar, e como o I2P amplia o conceito de serviço oculto para proporcionar benefícios de segurança para casos de uso potencialmente interessantes.

## O que é um LeaseSet?

Quando você cria um serviço oculto, você publica algo chamado "LeaseSet" na I2P NetDB. O "LeaseSet" é, em termos mais simples, o que outros usuários do I2P precisam para descobrir "onde" o seu serviço oculto está na Rede I2P. Ele contém "Leases" que identificam tunnels que podem ser usados para alcançar o seu serviço oculto, e a chave pública do seu destino, para a qual os clientes irão criptografar mensagens. Esse tipo de serviço oculto é acessível por qualquer pessoa que tenha o endereço, o que provavelmente é o caso de uso mais comum no momento.

Às vezes, porém, você pode não querer permitir que seus serviços ocultos sejam acessíveis por qualquer pessoa. Algumas pessoas usam serviços ocultos como uma forma de acessar um servidor SSH em um PC doméstico, ou para interconectar uma rede de dispositivos de IoT. Nesses casos, não é necessário, e pode ser contraproducente, tornar seu serviço oculto acessível a todos na rede I2P. É aqui que "Encrypted LeaseSets" entram em cena (LeaseSets criptografados).

## LeaseSets criptografados: Serviços MUITO ocultos

LeaseSets criptografados são LeaseSets publicados na NetDB em forma criptografada, onde nenhum dos Leases ou das chaves públicas é visível, a menos que o cliente tenha as chaves necessárias para descriptografar o LeaseSet dentro dele. Apenas os clientes com quem você compartilha chaves(Para PSK Encrypted LeaseSets), ou que compartilham suas chaves com você(Para DH Encrypted LeaseSets), poderão ver o destination (destino) e mais ninguém.

O I2P oferece suporte a várias estratégias para LeaseSets criptografados. É importante entender as características principais de cada estratégia ao decidir qual usar. Se um LeaseSet criptografado usar a estratégia de "Pre-Shared Key (PSK)", então o servidor gerará uma chave (ou chaves) que o operador do servidor compartilhará com cada cliente. Claro, essa troca deve acontecer fora de banda, possivelmente por meio de uma troca no IRC, por exemplo. Essa versão de LeaseSets criptografados é meio como se conectar ao Wi‑Fi com uma senha. Exceto que, na verdade, você está se conectando a um Serviço Oculto.

Se um Encrypted LeaseSet usa uma "estratégia Diffie-Hellman(DH)", então as chaves são geradas no cliente. Quando um cliente Diffie-Hellman se conecta a uma destination (destino no I2P) com um Encrypted LeaseSet, ele deve primeiro compartilhar suas chaves com o operador do servidor. O operador do servidor então decide se autoriza o cliente DH. Esta versão de Encrypted LeaseSets é algo parecido com SSH com um arquivo `authorized_keys`. Exceto que, o que você acessa ao fazer login é um Serviço Oculto.

Ao criptografar seu LeaseSet, você não apenas torna impossível que usuários não autorizados se conectem ao seu destino, como também impede que visitantes não autorizados sequer descubram o verdadeiro destino do serviço oculto do I2P. Alguns leitores provavelmente já consideraram um caso de uso para seu próprio LeaseSet criptografado.

## Usando LeaseSets Criptografados para Acessar com Segurança o Console do Router

Como regra geral, quanto mais complexas forem as informações sobre o seu dispositivo às quais um serviço tem acesso, mais perigoso é expor esse serviço à Internet ou mesmo a uma rede de serviço oculto como a I2P. Se você quiser expor esse tipo de serviço, precisa protegê-lo com algo como uma senha ou, no caso do I2P, uma opção muito mais abrangente e segura poderia ser um Encrypted LeaseSet.

**Antes de continuar, leia e compreenda que, se você realizar o procedimento a seguir sem um Encrypted LeaseSet, estará comprometendo a segurança do seu router I2P. Não configure o acesso ao console do seu router via I2P sem um Encrypted LeaseSet. Além disso, não compartilhe as suas PSKs (chaves pré-compartilhadas) do Encrypted LeaseSet com quaisquer dispositivos que você não controla.**

Um desses serviços, útil para compartilhar via I2P, mas SOMENTE com um Encrypted LeaseSet (ou seja, um LeaseSet com criptografia habilitada), é o próprio console do I2P router. Expor o console do I2P router de uma máquina na I2P com um Encrypted LeaseSet permite que outra máquina com um navegador administre a instância I2P remota. Considero isso útil para monitorar remotamente meus serviços I2P regulares. Também pode ser usado para monitorar um servidor utilizado para semear um torrent a longo prazo, como uma forma de acessar o I2PSnark.

Por mais tempo que leve para explicá-los, configurar um LeaseSet Criptografado é simples por meio da Hidden Services Manager UI.

## Em "Server"

Comece abrindo o Hidden Services Manager em http://127.0.0.1:7657/i2ptunnelmgr e role até o final da seção que diz "I2P Hidden Services." Crie um novo serviço oculto com o host "127.0.0.1" e a porta "7657" com estas "Tunnel Cryptography Options" e salve o serviço oculto.

Em seguida, selecione seu novo tunnel na página principal do Gerenciador de Serviços Ocultos. As Opções de Criptografia do tunnel agora devem incluir sua primeira chave pré-compartilhada. Anote isso para a próxima etapa, junto com o endereço Base32 criptografado do seu tunnel.

## No "Cliente"

Agora, mude para o computador cliente que se conectará ao serviço oculto e acesse a Keyring Configuration em http://127.0.0.1:7657/configkeyring para adicionar as chaves obtidas anteriormente. Comece colando a Base32 do Servidor no campo denominado: "Full destination, name, Base32, or hash." Em seguida, cole a chave pré-compartilhada (Pre-Shared Key) do Servidor no campo "Encryption Key". Clique em save, e você já pode acessar com segurança o Serviço Oculto usando um LeaseSet criptografado.

## Agora você está pronto para administrar o I2P remotamente.

Como você pode ver, o I2P oferece capacidades únicas aos Administradores de Serviços Ocultos que lhes permite gerenciar com segurança suas conexões I2P de qualquer lugar do mundo. Outros Encrypted LeaseSets que mantenho no mesmo dispositivo, pelo mesmo motivo, apontam para o servidor SSH, para a instância do Portainer que uso para gerenciar meus contêineres de serviço, e para minha instância pessoal do NextCloud. Com o I2P, a autohospedagem verdadeiramente privada e sempre acessível é um objetivo alcançável; na verdade, acho que é uma das coisas para as quais somos singularmente adequados, por causa dos Encrypted LeaseSets. Com eles, o I2P poderia se tornar a chave para proteger a automação residencial autohospedada ou simplesmente se tornar a espinha dorsal de uma nova web ponto-a-ponto mais privada.
