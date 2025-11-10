---
title: "Cómo colaborar ayudando al arranque (bootstrap) de I2P-Bote"
date: 2019-05-20
author: "idk"
description: "¡Ayuda con el bootstrap (inicialización) de I2P-Bote!

Proporciona SOLO la traducción, nada más:"
categories: ["development"]
---

Una manera sencilla de ayudar a que las personas se envíen mensajes de forma privada es ejecutar un nodo de I2P-Bote que los usuarios nuevos de I2P-Bote puedan usar para hacer bootstrap (inicialización) de sus propios nodos de I2P-Bote. Lamentablemente, hasta ahora, el proceso de configurar un nodo de bootstrap de I2P-Bote ha sido mucho más confuso de lo que debería. De hecho, es extremadamente sencillo.

**¿Qué es I2P-bote?**

I2P-bote es un sistema de mensajería privada basado en i2p, que incorpora funciones adicionales para que resulte aún más difícil discernir información sobre los mensajes que se transmiten. Por esta razón, puede utilizarse para transmitir mensajes privados de forma segura, tolerando latencias altas y sin depender de un servidor de retransmisión centralizado para enviar mensajes cuando el remitente se desconecta. Esto contrasta con casi todos los demás sistemas populares de mensajería privada, que o bien requieren que ambas partes estén en línea, o bien dependen de un servicio semi-confiable que transmite los mensajes en nombre de los remitentes que se desconectan.

o, explicado como si tuviera 5 años: Se usa de forma similar al correo electrónico, pero no sufre ninguno de los defectos de privacidad del correo electrónico.

**Paso uno: Instalar I2P-Bote**

I2P-Bote es un complemento de i2p, y instalarlo es muy fácil. Las instrucciones originales están disponibles en el [bote eepSite, bote.i2p](http://bote.i2p/install/), pero si desea leerlas en la clearnet (Internet abierta), estas instrucciones se ofrecen por cortesía de bote.i2p:

1. Go to the plugin install form in your routerconsole: http://127.0.0.1:7657/configclients#plugin
2. Paste in the URL http://bote.i2p/i2pbote.su3
3. Click Install Plugin.
4. Once installed, click SecureMail in the routerconsole sidebar or homepage, or go to http://127.0.0.1:7657/i2pbote/

**Paso dos: Obtén la dirección base64 de tu nodo de I2P-Bote**

Esta es la parte en la que alguien podría quedarse atascado, pero no te preocupes. Aunque puede ser un poco difícil encontrar instrucciones, en realidad esto es sencillo y tienes varias herramientas y opciones a tu disposición, según cuáles sean tus circunstancias. Para quienes quieran ayudar a operar nodos de arranque como voluntarios, la mejor manera es obtener la información necesaria del archivo de clave privada utilizado por el bote tunnel.

**¿Dónde están las claves?**

I2P-Bote almacena sus claves de destino en un archivo de texto que, en Debian, se encuentra en `/var/lib/i2p/i2p-config/i2pbote/local_dest.key`. En sistemas no Debian donde i2p es instalado por el usuario, la clave estará en `$HOME/.i2p/i2pbote/local_dest.key`, y en Windows, el archivo estará en `C:\ProgramData\i2p\i2pbote\local_dest.key`.

**Método A: Convertir la clave en texto plano al destino en base64**

Para convertir una clave en texto plano en un destino en base64, es necesario tomar la clave y separar de ella únicamente la parte del destino. Para hacerlo correctamente, se deben seguir los siguientes pasos:

1. First, take the full destination and decode it from i2p's base64 character set into binary.
2. Second, take bytes 386 and 387 and convert them to a single Big-Endian integer.
3. Add the number you computed from the two bytes in step two to 387. This is the length of the base64 destination.
4. Take that nummber of bytes from the front of the full destination to get the destination as a range of bytes.
5. Convert back to a base64 representation using i2p's base64 character set.

Existen varias aplicaciones y scripts que realizan estos pasos por ti. Aquí hay algunas de ellas, pero esta lista está lejos de ser exhaustiva:

- [the i2p.scripts collection of scripts(Mostly java and bash)](https://github.com/i2p/i2p.scripts)
- [my application for converting keys(Go)](https://github.com/eyedeekay/keyto)

Estas capacidades también están disponibles en varias bibliotecas de desarrollo de aplicaciones de I2P.

**Atajo:**

Dado que el destino local de tu nodo de Bote es un destino DSA, es más rápido simplemente truncar el archivo local_dest.key a los primeros 516 bytes. Para hacerlo fácilmente, ejecuta este comando al ejecutar I2P-Bote con I2P en Debian:

```bash
sudo -u i2psvc head -c 516 /var/lib/i2p/i2p-config/i2pbote/local_dest.key
```
O bien, si I2P está instalado para tu usuario:

```bash
head -c 516 ~/.i2p/i2pbote/local_dest.key
```
**Método B: Realiza una consulta**

Si eso te parece demasiado trabajo, puedes consultar el destino base64 de tu conexión de Bote consultando su dirección base32 mediante cualquiera de los métodos disponibles para buscar una dirección base32. La dirección base32 de tu nodo de Bote está disponible en la página "Conexión" dentro de la aplicación del complemento Bote, en [127.0.0.1:7657/i2pbote/network](http://127.0.0.1:7657/i2pbote/network)

**Paso tres: ¡Contáctanos!**

**Actualiza el archivo built-in-peers.txt con tu nuevo nodo**

Ahora que ya tienes el destino correcto para tu nodo de I2P-Bote, el paso final es agregarte a la lista predeterminada de pares para [I2P-Bote aquí](https://github.com/i2p/i2p.i2p-bote/tree/master/core/src/main/resources/i2p/bote/network) aquí. Puedes hacerlo haciendo un fork (bifurcación) del repositorio, añadiéndote a la lista con tu nombre comentado, y tu destino de 516 caracteres directamente debajo, así:

```
# idk
QuabT3H5ljZyd-PXCQjvDzdfCec-2yv8E9i6N71I5WHAtSEZgazQMReYNhPWakqOEj8BbpRvnarpHqbQjoT6yJ5UObKv2hA2M4XrroJmydPV9CLJUCqgCqFfpG-bkSo0gEhB-GRCUaugcAgHxddmxmAsJVRj3UeABLPHLYiakVz3CG2iBMHLJpnC6H3g8TJivtqabPYOxmZGCI-P~R-s4vwN2st1lJyKDl~u7OG6M6Y~gNbIzIYeQyNggvnANL3t6cUqS4v0Vb~t~CCtXgfhuK5SK65Rtkt2Aid3s7mrR2hDxK3SIxmAsHpnQ6MA~z0Nus-VVcNYcbHUBNpOcTeKlncXsuFj8vZL3ssnepmr2DCB25091t9B6r5~681xGEeqeIwuMHDeyoXIP0mhEcy3aEB1jcchLBRLMs6NtFKPlioxz0~Vs13VaNNP~78bTjFje5ya20ahWlO0Md~x5P5lWLIKDgaqwNdIrijtZAcILn1h18tmABYauYZQtYGyLTOXAAAA
```
y enviar un pull request (solicitud de extracción). Eso es todo, así que ayuda a mantener i2p vivo, descentralizado y confiable.
