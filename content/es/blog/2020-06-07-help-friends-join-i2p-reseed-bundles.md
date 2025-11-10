---
title: "Ayuda a tus amigos a unirse a I2P compartiendo paquetes de reseed"
date: 2020-06-07
author: "idk"
description: "Crear, intercambiar y usar reseed bundles (paquetes de resiembra)"
categories: ["reseed"]
---

La mayoría de los routers I2P nuevos se unen a la red mediante bootstrap (arranque inicial) con la ayuda de un reseed service (servicio de reseed). Sin embargo, los reseed services son centralizados y relativamente fáciles de bloquear, considerando el énfasis en conexiones descentralizadas e imposibles de bloquear en el resto de la red I2P. Si un router I2P nuevo no puede realizar el bootstrap, puede ser posible usar un router I2P existente para generar un "Reseed bundle" (paquete de Reseed) funcional y realizar el bootstrap sin necesidad de un reseed service.

Es posible que un usuario con una conexión I2P funcional ayude a que un router bloqueado se una a la red generando un archivo de reseed (resembrado) y pasándoselo a través de un canal secreto o no bloqueado. De hecho, en muchas circunstancias, un router I2P que ya esté conectado no se verá afectado en absoluto por el bloqueo de reseed, por lo que **tener routers I2P funcionales alrededor significa que los routers I2P existentes pueden ayudar a nuevos routers I2P proporcionándoles una forma oculta de inicialización**.

## Generación de un paquete de Reseed

- To create a reseed bundle for others to use, go to the [Reseed configuration page](http://127.0.0.1:7657/configreseed). You will see a section that looks like this. Click the button indicated by the red circle to create a reseed zip.
- Now that you've clicked the button, a zip will be generated containing enough information to bootstrap a new I2P router. Download it and transfer it to the computer with the new, un-bootstrapped I2P router.

## Realizar un Reseed desde un archivo

- Obtain an i2preseed.zip file from a friend with an I2P router that is already running, or from a trusted source somewhere on the internet, and visit the [Reseed Configuration page](http://127.0.0.1:7657/configreseed). Click the button that says "Select zip or su3 file" and navigate to that file.
- When you've selected your reseed file, click the "Reseed from File" button. You're done! Your router will now bootstrap using the zip file, and you will be ready to join the I2P network.
