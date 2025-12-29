---
title: "Mejorar la adopción y la incorporación a I2P mediante Jpackage, I2P-Zero"
date: 2021-09-15
slug: "improving-i2p-adoption-and-onboarding-using-jpackage-i2p-zero"
author: "idk"
description: "Formas versátiles y emergentes de instalar e integrar I2P en su aplicación"
categories: ["general"]
---

For the majority of I2P's existence, it's been an application that runs with the help of a Java Virtual Machine that is already installed on the platform. This has always been the normal way to distribute Java applications, but it leads to a complicated installation procedure for many people. To make things even more complicated, the "right answer" to making I2P easy to install on any given platform might not be the same as any other platform. For example, I2P is quite simple to install with standard tools on Debian and Ubuntu based operating systems, because we can simply list the required Java components as "Required" by our package, however on Windows or OSX, there is no such system allowing us to make sure that a compatible Java is installed.

La solución obvia sería gestionar nosotros mismos la instalación de Java, pero esto solía ser un problema en sí mismo, fuera del alcance de I2P. Sin embargo, en versiones recientes de Java ha surgido un nuevo conjunto de opciones que tiene el potencial de resolver este problema para muchas aplicaciones Java. Esta emocionante herramienta se llama **"Jpackage."**

## I2P-Zero e instalación de I2P sin dependencias

El primer esfuerzo muy exitoso para construir un paquete de I2P sin dependencias fue I2P-Zero, que fue creado por el proyecto Monero originalmente para usarse con la criptomoneda Monero. Este proyecto nos entusiasmó mucho debido a su éxito al crear un router I2P de propósito general que podía empaquetarse fácilmente con una aplicación I2P. Especialmente en Reddit, muchas personas expresan su preferencia por la simplicidad de configurar un router I2P-Zero.

Esto realmente nos demostró que, usando herramientas modernas de Java, era posible un paquete de I2P sin dependencias y fácil de instalar, pero el caso de uso de I2P-Zero era un poco diferente del nuestro. Es ideal para aplicaciones integradas que necesitan un router de I2P que puedan controlar fácilmente mediante su práctico puerto de control en el puerto "8051". Nuestro siguiente paso sería adaptar la tecnología a la aplicación de I2P de propósito general.

## Los cambios de seguridad de aplicaciones de OSX afectan al instalador I2P IzPack

El problema se volvió más apremiante en versiones recientes de Mac OSX, donde ya no es sencillo usar el instalador "Classic" que viene en formato .jar. Esto se debe a que la aplicación no está "notarizada" por las autoridades de Apple y se considera un riesgo de seguridad. **Sin embargo**, Jpackage puede producir un archivo .dmg, que puede ser notarizado por las autoridades de Apple, resolviendo convenientemente nuestro problema.

El nuevo instalador .dmg de I2P, creado por Zlatinb, hace que I2P sea más fácil de instalar en OSX que nunca; ya no requiere que los usuarios instalen Java por sí mismos y utiliza las herramientas de instalación estándar de OSX de la manera prescrita. El nuevo instalador .dmg hace que configurar I2P en Mac OSX sea más fácil que nunca.

Descarga el [dmg](https://geti2p.net/en/download/mac)

## El I2P del futuro es fácil de instalar

Una de las cosas que más oigo de los usuarios es que, si I2P quiere adopción, tiene que ser fácil de usar para la gente. Muchos quieren una experiencia de usuario "similar a Tor Browser", citando o parafraseando a muchos usuarios de Reddit conocidos. La instalación no debería requerir pasos complicados y propensos a errores de "posinstalación". Muchos usuarios nuevos no están preparados para configurar su navegador de forma exhaustiva y completa. Para abordar este problema, creamos el I2P Profile Bundle, que configuraba Firefox para que "Simplemente Funcione" automáticamente con I2P. A medida que se ha desarrollado, ha añadido funciones de seguridad y ha mejorado la integración con el propio I2P. En su última versión, **también** incluye un I2P Router completo, impulsado por Jpackage. El I2P Firefox Profile es ahora una distribución de I2P para Windows plenamente funcional, siendo la única dependencia restante el propio Firefox. Esto debería proporcionar un nivel de comodidad sin precedentes para los usuarios de I2P en Windows.

Obtén el [instalador](https://geti2p.net/en/download#windows)
