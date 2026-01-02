---
title: "Como se voluntariar ajudando no bootstrap do I2P-Bote"
date: 2019-05-20
author: "idk"
description: "Ajude a inicializar o I2P-Bote!"
categories: ["development"]
---

Uma maneira fácil de ajudar as pessoas a trocarem mensagens privadas entre si é executar um par (peer) do I2P-Bote que possa ser usado por novos usuários do bote para inicializar seus próprios pares do I2P-Bote. Infelizmente, até agora, o processo de configurar um par de inicialização do I2P-Bote tem sido muito mais obscuro do que deveria ser. Na verdade, é extremamente simples!

**O que é o I2P-bote?**

O I2P-bote é um sistema de mensagens privadas construído sobre o i2p, que possui recursos adicionais para tornar ainda mais difícil inferir informações sobre as mensagens que são transmitidas. Por isso, pode ser usado para transmitir mensagens privadas com segurança, tolerando alta latência e sem depender de um retransmissor centralizado para enviar mensagens quando o remetente fica offline. Isso contrasta com quase todos os outros sistemas populares de mensagens privadas, que ou exigem que ambas as partes estejam online, ou dependem de um serviço semi-confiável que transmite mensagens em nome de remetentes que ficam offline.

ou, ELI5: É usado de forma semelhante ao e-mail, mas não sofre de nenhuma das falhas de privacidade do e-mail.

**Passo Um: Instale o I2P-Bote**

I2P-Bote é um plugin do i2p, e instalá-lo é muito fácil. As instruções originais estão disponíveis em [bote eepSite, bote.i2p](http://bote.i2p/install/), mas, se você quiser lê-las na clearnet (internet comum), estas instruções são cortesia de bote.i2p:

1. Go to the plugin install form in your routerconsole: http://127.0.0.1:7657/configclients#plugin
2. Paste in the URL http://bote.i2p/i2pbote.su3
3. Click Install Plugin.
4. Once installed, click SecureMail in the routerconsole sidebar or homepage, or go to http://127.0.0.1:7657/i2pbote/

**Passo Dois: Obtenha o endereço base64 do seu nó I2P-Bote**

Esta é a parte em que alguém pode emperrar, mas não se preocupe. Embora seja um pouco difícil encontrar instruções, na verdade, é fácil e há várias ferramentas e opções à sua disposição, dependendo das suas circunstâncias. Para pessoas que queiram ajudar a operar nós de bootstrap (nós de inicialização) como voluntários, a melhor forma é obter as informações necessárias a partir do arquivo de chave privada usado pelo tunnel do bote.

**Onde estão as chaves?**

I2P-Bote armazena suas chaves de destino em um arquivo de texto que, no Debian, fica em `/var/lib/i2p/i2p-config/i2pbote/local_dest.key`. Em sistemas não-Debian onde o i2p é instalado pelo usuário, o arquivo estará em `$HOME/.i2p/i2pbote/local_dest.key`, e no Windows, o arquivo estará em `C:\ProgramData\i2p\i2pbote\local_dest.key`.

**Método A: Converter a chave em texto claro para o destino em base64**

Para converter uma chave em texto simples em um destino em base64, é necessário pegar a chave e separar dela apenas a parte do destino. Para fazer isso corretamente, é preciso seguir as etapas a seguir:

1. First, take the full destination and decode it from i2p's base64 character set into binary.
2. Second, take bytes 386 and 387 and convert them to a single Big-Endian integer.
3. Add the number you computed from the two bytes in step two to 387. This is the length of the base64 destination.
4. Take that nummber of bytes from the front of the full destination to get the destination as a range of bytes.
5. Convert back to a base64 representation using i2p's base64 character set.

Há diversos aplicativos e scripts que executam essas etapas para você. Aqui estão alguns deles, mas esta lista está longe de ser exaustiva:

- [the i2p.scripts collection of scripts(Mostly java and bash)](https://github.com/i2p/i2p.scripts)
- [my application for converting keys(Go)](https://github.com/eyedeekay/keyto)

Essas funcionalidades também estão disponíveis em diversas bibliotecas de desenvolvimento de aplicações I2P.

**Atalho:**


Como o destino local do seu nó do Bote é um destino DSA, é mais rápido simplesmente truncar o arquivo local_dest.key para os primeiros 516 bytes. Para fazer isso facilmente, execute este comando quando estiver executando o I2P-Bote com o I2P no Debian:

```bash
sudo -u i2psvc head -c 516 /var/lib/i2p/i2p-config/i2pbote/local_dest.key
```
Ou, se o I2P estiver instalado na sua conta de usuário:

```bash
head -c 516 ~/.i2p/i2pbote/local_dest.key
```
**Método B: Faça uma consulta**

Se isso lhe parecer trabalho demais, é possível obter o destino base64 da sua conexão Bote consultando o seu endereço base32 usando qualquer um dos meios disponíveis para pesquisar um endereço base32. O endereço base32 do seu nó Bote está disponível na página "Connection" do aplicativo do plugin Bote, em [127.0.0.1:7657/i2pbote/network](http://127.0.0.1:7657/i2pbote/network)

**Passo Três: Fale conosco!**

**Atualize o arquivo built-in-peers.txt com seu novo nó**

Agora que você tem o destino correto do seu nó I2P-Bote, a etapa final é adicionar-se à lista padrão de pares do [I2P-Bote aqui](https://github.com/i2p/i2p.i2p-bote/tree/master/core/src/main/resources/i2p/bote/network) aqui. Você pode fazer isso fazendo um fork do repositório, adicionando-se à lista com seu nome comentado e seu destino de 516 caracteres logo abaixo, assim:

```
# idk
QuabT3H5ljZyd-PXCQjvDzdfCec-2yv8E9i6N71I5WHAtSEZgazQMReYNhPWakqOEj8BbpRvnarpHqbQjoT6yJ5UObKv2hA2M4XrroJmydPV9CLJUCqgCqFfpG-bkSo0gEhB-GRCUaugcAgHxddmxmAsJVRj3UeABLPHLYiakVz3CG2iBMHLJpnC6H3g8TJivtqabPYOxmZGCI-P~R-s4vwN2st1lJyKDl~u7OG6M6Y~gNbIzIYeQyNggvnANL3t6cUqS4v0Vb~t~CCtXgfhuK5SK65Rtkt2Aid3s7mrR2hDxK3SIxmAsHpnQ6MA~z0Nus-VVcNYcbHUBNpOcTeKlncXsuFj8vZL3ssnepmr2DCB25091t9B6r5~681xGEeqeIwuMHDeyoXIP0mhEcy3aEB1jcchLBRLMs6NtFKPlioxz0~Vs13VaNNP~78bTjFje5ya20ahWlO0Md~x5P5lWLIKDgaqwNdIrijtZAcILn1h18tmABYauYZQtYGyLTOXAAAA
```
e enviar um pull request. É só isso — ajude a manter o i2p vivo, descentralizado e confiável.
