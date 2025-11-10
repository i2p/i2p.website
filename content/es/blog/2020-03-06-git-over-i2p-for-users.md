---
title: "Git sobre I2P para usuarios"
date: 2020-03-06
author: "idk"
description: "Git a través de I2P"
categories: ["development"]
---

Tutorial para configurar el acceso a git a través de un I2P Tunnel. Este tunnel actuará como tu punto de acceso a un único servicio de git en I2P. Forma parte del esfuerzo general para migrar I2P de monotone a Git.

## Antes que nada: Conozca las capacidades que el servicio ofrece al público

Según cómo esté configurado el servicio de Git, puede que ofrezca todos los servicios en la misma dirección o no. En el caso de git.idk.i2p, hay una URL HTTP pública y una URL SSH para configurar en su cliente SSH de Git. Ambas pueden usarse para hacer push o pull, pero se recomienda SSH.

## Primero: Crea una cuenta en un servicio de Git

Para crear tus repositorios en un servicio de Git remoto, regístrate para obtener una cuenta de usuario en ese servicio. Por supuesto, también es posible crear repositorios localmente y hacer push a un servicio de Git remoto, pero la mayoría requerirá una cuenta y que crees un espacio para el repositorio en el servidor.

## Segundo: Crear un proyecto para probar

Para asegurarte de que el proceso de configuración funciona, conviene crear un repositorio para realizar pruebas desde el servidor. Accede al repositorio i2p-hackers/i2p.i2p y haz un fork (bifurcación) en tu cuenta.

## Tercero: Configura el tunnel de tu cliente de git

Para tener acceso de lectura y escritura a un servidor, necesitarás configurar un tunnel para tu cliente SSH. Si lo único que necesitas es la clonación HTTP/S de solo lectura, entonces puedes omitir todo esto y simplemente usar la variable de entorno http_proxy para configurar git para que use el I2P HTTP Proxy preconfigurado. Por ejemplo:

```
http_proxy=http://localhost:4444 git clone --depth=1 http://git.idk.i2p/youruser/i2p.i2p
git fetch --unshallow
```
Para el acceso por SSH, inicia el "New Tunnel Wizard" desde http://127.0.0.1:7657/i2ptunnelmgr y configura un tunnel de cliente que apunte a la dirección base32 SSH del servicio Git.

## Cuarto: Intenta clonar

Ahora que tu tunnel ya está completamente configurado, puedes intentar clonar por SSH:

```
GIT_SSH_COMMAND="ssh -p 7670" \
    git clone git@127.0.0.1:youruser/i2p.i2p
```
Es posible que obtengas un error en el que la parte remota cierra la conexión de forma inesperada. Lamentablemente, git todavía no admite la clonación reanudable. Hasta que lo haga, hay un par de maneras bastante sencillas de manejar esto. La primera y más simple es intentar hacer una clonación superficial (con profundidad limitada):

```
GIT_SSH_COMMAND="ssh -p 7670" \
    git clone --depth 1 git@127.0.0.1:youruser/i2p.i2p
```
Una vez que hayas realizado una clonación superficial, puedes obtener el resto de manera reanudable cambiando al directorio del repositorio y ejecutando:

```
git fetch --unshallow
```
En este punto, todavía no tienes todas tus ramas. Puedes obtenerlas ejecutando:

```
git config remote.origin.fetch "+refs/heads/*:refs/remotes/origin/*"
git fetch origin
```
## Flujo de trabajo sugerido para desarrolladores

¡El control de versiones funciona mejor si se usa correctamente! Recomendamos encarecidamente un flujo de trabajo fork-first (crear un fork primero) y feature-branch (ramas de funcionalidades):

1. **Never make changes to the Master Branch**. Use the master branch to periodically obtain updates to the official source code. All changes should be made in feature branches.

2. Set up a second remote in your local repository using the upstream source code:

```
git remote add upstream git@127.0.0.1:i2p-hackers/i2p.i2p
```
3. Pull in any upstream changes on your current master:

```
git pull upstream master
```
4. Before making any changes to the source code, check out a new feature branch to develop on:

```
git checkout -b feature-branch-name
```
5. When you're done with your changes, commit them and push them to your branch:

```
git commit -am "I added an awesome feature!"
git push origin feature-branch-name
```
6. Submit a merge request. When the merge request is approved, check out the master locally and pull in the changes:

```
git checkout master
git pull upstream master
```