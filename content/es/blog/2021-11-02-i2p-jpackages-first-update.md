---
title: "I2P Jpackages reciben su primera actualización"
date: 2021-11-02
author: "idk"
description: "Nuevos paquetes más fáciles de instalar alcanzan un nuevo hito"
categories: ["general"]
API_Translate: verdadero
---

Hace unos meses publicamos nuevos paquetes que esperábamos ayudarían con la incorporación de nuevas personas a la red I2P al facilitar la instalación y la configuración de I2P para más gente. Eliminamos decenas de pasos del proceso de instalación al pasar de una JVM externa a un Jpackage, creamos paquetes estándar para los sistemas operativos de destino y los firmamos de una forma que el sistema operativo reconociera para mantener seguro al usuario. Desde entonces, los jpackage routers han alcanzado un nuevo hito: están a punto de recibir sus primeras actualizaciones incrementales. Estas actualizaciones reemplazarán el JDK 16 jpackage por un JDK 17 jpackage actualizado y proporcionarán correcciones para algunos pequeños errores que detectamos después del lanzamiento.

## Actualizaciones comunes a Mac OS y Windows

Todos los instaladores de I2P jpackaged reciben las siguientes actualizaciones:

* Update the jpackaged I2P router to 1.5.1 which is built with JDK 17

Por favor, actualice lo antes posible.

## Actualizaciones del Jpackage de I2P para Windows

Los paquetes solo para Windows reciben las siguientes actualizaciones:

* Updates I2P in Private Browsing, NoScript browser extensions
* Begins to phase out HTTPS everywhere on new Firefox releases
* Updates launcher script to fix post NSIS launch issue on some architectures

Para una lista completa de cambios, consulte el archivo changelog.txt en i2p.firefox

## Actualizaciones de Jpackage de I2P para Mac OS

Los paquetes solo para Mac OS reciben las siguientes actualizaciones:

* No Mac-Specific changes. Mac OS is updated to build with JDK 17.

Para un resumen del desarrollo, consulte los checkins (confirmaciones) en i2p-jpackage-mac
