---
title: "I2P en Maven Central"
date: 2016-06-13
author: "str4d"
description: "The I2P client libraries are now available on Maven Central!"
categories: ["summer-dev"]
---

Estamos casi a mitad del mes de APIs de Summer Dev y estamos logrando grandes avances en varios frentes. Me complace anunciar que el primero de ellos se ha completado: ¡las bibliotecas de cliente de I2P ya están disponibles en Maven Central!

Esto debería facilitar mucho a los desarrolladores de Java el uso de I2P en sus aplicaciones. En lugar de tener que obtener las bibliotecas de una instalación existente, pueden simplemente agregar I2P a sus dependencias. Actualizar a nuevas versiones también será mucho más fácil.

## Cómo usarlos

Existen dos bibliotecas que debe conocer:

- `net.i2p:i2p` - The core I2P APIs; you can use these to send individual datagrams.
- `net.i2p.client:streaming` - A TCP-like set of sockets for communicating over I2P.

Añade uno o ambos a las dependencias de tu proyecto, ¡y listo!

### Gradle

```
compile 'net.i2p:i2p:0.9.26'
compile 'net.i2p.client:streaming:0.9.26'
```
### Gradle

```xml
<dependency>
    <groupId>net.i2p</groupId>
    <artifactId>i2p</artifactId>
    <version>0.9.26</version>
</dependency>
<dependency>
    <groupId>net.i2p.client</groupId>
    <artifactId>streaming</artifactId>
    <version>0.9.26</version>
</dependency>
```
Para otros sistemas de compilación, consulte las páginas en Maven Central de las bibliotecas core y de streaming.

Los desarrolladores de Android deberían usar la biblioteca cliente de I2P para Android, que contiene las mismas bibliotecas, además de utilidades específicas para Android. Pronto la actualizaré para que dependa de las nuevas bibliotecas de I2P, de modo que las aplicaciones multiplataforma puedan funcionar de forma nativa tanto con I2P para Android como con I2P de escritorio.

## Get hacking!

Consulta nuestra guía de desarrollo de aplicaciones para empezar a usar estas bibliotecas. También puedes hablar con nosotros sobre ellas en #i2p-dev en IRC. Y si empiezas a usarlas, cuéntanos en qué estás trabajando con el hashtag #I2PSummer en Twitter.
