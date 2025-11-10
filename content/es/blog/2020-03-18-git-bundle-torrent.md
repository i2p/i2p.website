---
title: "Uso de git bundle para obtener el código fuente de I2P"
date: 2020-03-18
author: "idk"
description: "Descargar el código fuente de I2P a través de BitTorrent"
categories: ["development"]
---

Clonar repositorios de software grandes a través de I2P puede ser difícil, y usar git a veces puede dificultarlo aún más. Afortunadamente, en ocasiones también puede facilitarlo. Git tiene un comando `git bundle` que se puede usar para convertir un repositorio de git en un archivo que git luego puede clonar, obtener (fetch) o importar desde una ubicación en su disco local. Al combinar esta capacidad con descargas por bittorrent, podemos resolver nuestros problemas restantes con `git clone`.

## Antes de comenzar

Si tienes previsto generar un git bundle (paquete de git), **debes** ya tener una copia completa del repositorio de **git**, no del repositorio de mtn. Puedes obtenerlo de github o de git.idk.i2p, pero un clon superficial (un clon hecho con --depth=1) *no funcionará*. Fallará silenciosamente, creando algo que parece un bundle, pero cuando intentes clonarlo fallará. Si solo estás recuperando un git bundle pre-generado, entonces esta sección no se aplica a ti.

## Obtención del código fuente de I2P a través de BitTorrent

Alguien tendrá que proporcionarle un archivo torrent o un enlace magnet correspondiente a un `git bundle` (paquete de Git) que ya haya generado para usted. Una vez que tenga un bundle desde bittorrent, necesitará usar git para crear un repositorio de trabajo a partir de él.

## Uso de `git clone`

Clonar desde un paquete de git es fácil, basta con:

```
git clone $HOME/.i2p/i2psnark/i2p.i2p.bundle
```
Si obtiene el siguiente error, intente usar git init y git fetch manualmente en su lugar:

```
fatal: multiple updates for ref 'refs/remotes/origin/master' not allowed
```
## Uso de `git init` y `git fetch`

Primero, crea un directorio i2p.i2p para convertirlo en un repositorio de git:

```
mkdir i2p.i2p && cd i2p.i2p
```
A continuación, inicializa un repositorio git vacío en el que obtener los cambios:

```
git init
```
Por último, obtén el repositorio del paquete:

```
git fetch $HOME/.i2p/i2psnark/i2p.i2p.bundle
```
## Sustituye el remoto del paquete por el remoto upstream

Ahora que tienes un bundle, puedes mantenerte al día con los cambios configurando el remoto para que apunte a la fuente del repositorio upstream (repositorio principal):

```
git remote set-url origin git@127.0.0.1:i2p-hackers/i2p.i2p
```
## Generación de un paquete

Primero, sigue la guía de Git para usuarios hasta que tengas un clon del repositorio i2p.i2p al que se le haya aplicado correctamente `--unshallow`. Si ya tienes un clon, asegúrate de ejecutar `git fetch --unshallow` antes de generar un paquete torrent.

Una vez que tenga eso, simplemente ejecute el objetivo de Ant correspondiente:

```
ant bundle
```
y copia el paquete resultante en tu directorio de descargas de I2PSnark. Por ejemplo:

```
cp i2p.i2p.bundle* $HOME/.i2p/i2psnark/
```
En un minuto o dos, I2PSnark detectará el torrent. Haz clic en el botón "Start" para comenzar a sembrar el torrent.
