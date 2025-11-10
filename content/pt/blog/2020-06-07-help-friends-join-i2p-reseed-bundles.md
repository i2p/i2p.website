---
title: "Ajude seus amigos a juntar-se ao I2P compartilhando Reseed Bundles (pacotes de reseed)"
date: 2020-06-07
author: "idk"
description: "Criar, trocar e usar pacotes de reseed"
categories: ["reseed"]
---

A maioria dos novos I2P routers ingressa na rede fazendo bootstrap com a ajuda de um reseed service (serviço de Reseed). No entanto, os reseed services são centralizados e comparativamente fáceis de bloquear, considerando a ênfase em conexões descentralizadas e impossíveis de bloquear no restante da rede I2P. Se um novo I2P router não conseguir fazer bootstrap, pode ser possível usar um I2P router existente para gerar um "Reseed bundle" funcional e fazer bootstrap sem a necessidade de um reseed service.

É possível que um usuário com uma conexão I2P funcional ajude um router bloqueado a ingressar na rede gerando um arquivo de reseed (processo de inicialização da rede) e repassando-o por meio de um canal secreto ou não bloqueado. Na verdade, em muitas circunstâncias, um router I2P que já está conectado não será afetado pelo bloqueio de reseed de forma alguma, então **ter routers I2P funcionais por perto significa que routers I2P existentes podem ajudar novos routers I2P fornecendo-lhes uma forma oculta de inicialização**.

## Gerando um Pacote de Reseed

- To create a reseed bundle for others to use, go to the [Reseed configuration page](http://127.0.0.1:7657/configreseed). You will see a section that looks like this. Click the button indicated by the red circle to create a reseed zip.
- Now that you've clicked the button, a zip will be generated containing enough information to bootstrap a new I2P router. Download it and transfer it to the computer with the new, un-bootstrapped I2P router.

## Executando um Reseed (obtenção de pares iniciais) a partir de um arquivo

- Obtain an i2preseed.zip file from a friend with an I2P router that is already running, or from a trusted source somewhere on the internet, and visit the [Reseed Configuration page](http://127.0.0.1:7657/configreseed). Click the button that says "Select zip or su3 file" and navigate to that file.
- When you've selected your reseed file, click the "Reseed from File" button. You're done! Your router will now bootstrap using the zip file, and you will be ready to join the I2P network.
