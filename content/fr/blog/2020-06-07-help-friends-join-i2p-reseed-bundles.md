---
title: "Aidez vos amis à rejoindre I2P en partageant des Reseed Bundles (paquets de réensemencement)"
date: 2020-06-07
author: "idk"
description: "Créer, échanger et utiliser des paquets de réensemencement"
categories: ["reseed"]
---

La plupart des nouveaux I2P routers rejoignent le réseau en procédant au bootstrap (amorçage) à l’aide d’un service de réensemencement. Cependant, les services de réensemencement sont centralisés et relativement faciles à bloquer, compte tenu de l’accent mis sur des connexions décentralisées et impossibles à bloquer dans le reste du réseau I2P. Si un nouvel I2P router se trouve dans l’impossibilité d’effectuer le bootstrap, il peut être possible d’utiliser un I2P router existant pour générer un "Reseed bundle" fonctionnel et effectuer le bootstrap sans avoir besoin d’un service de réensemencement.

Il est possible pour un utilisateur disposant d’une connexion I2P fonctionnelle d’aider un router bloqué à rejoindre le réseau en générant un fichier de reseed (amorçage initial) et en le lui transmettant via un canal secret ou non bloqué. En fait, dans de nombreuses circonstances, un router I2P déjà connecté ne sera pas du tout affecté par le blocage du reseed, de sorte que **le fait d’avoir des routers I2P opérationnels signifie que les routers I2P existants peuvent aider de nouveaux routers I2P en leur fournissant un moyen caché d’amorçage**.

## Génération d’une archive de réensemencement

- To create a reseed bundle for others to use, go to the [Reseed configuration page](http://127.0.0.1:7657/configreseed). You will see a section that looks like this. Click the button indicated by the red circle to create a reseed zip.
- Now that you've clicked the button, a zip will be generated containing enough information to bootstrap a new I2P router. Download it and transfer it to the computer with the new, un-bootstrapped I2P router.

## Effectuer un réensemencement à partir d'un fichier

- Obtain an i2preseed.zip file from a friend with an I2P router that is already running, or from a trusted source somewhere on the internet, and visit the [Reseed Configuration page](http://127.0.0.1:7657/configreseed). Click the button that says "Select zip or su3 file" and navigate to that file.
- When you've selected your reseed file, click the "Reseed from File" button. You're done! Your router will now bootstrap using the zip file, and you will be ready to join the I2P network.
