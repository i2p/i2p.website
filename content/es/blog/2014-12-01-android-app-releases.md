---
title: "Versiones de la aplicación de Android"
date: 2014-12-01
author: "str4d"
description: "I2P Android 0.9.17 y Bote 0.3 se han publicado en el sitio web, Google Play y F-Droid."
categories: ["press"]
---

Ha pasado un tiempo desde la última vez que publiqué actualizaciones sobre nuestro desarrollo en Android, y se han publicado varias versiones de I2P sin lanzamientos de Android correspondientes. ¡Por fin, la espera ha terminado!

## Nuevas versiones de aplicaciones

¡Se han publicado nuevas versiones de I2P Android y Bote!

Se pueden descargar desde estas URL:

- [I2P Android 0.9.17](https://geti2p.net/en/download#android)
- [Bote 0.3](https://download.i2p.io/android/bote/releases/0.3/Bote.apk)

El cambio principal en estas versiones es la transición al nuevo sistema de diseño Material de Android. Material ha hecho mucho más fácil para los desarrolladores de aplicaciones con, digamos, habilidades de diseño "minimalistas" (como yo) crear aplicaciones más agradables de usar. I2P Android también actualiza su I2P router subyacente a la versión 0.9.17 recién lanzada. Bote incorpora varias funciones nuevas junto con muchas mejoras menores; por ejemplo, ahora es posible añadir nuevos destinos de correo electrónico mediante códigos QR.

Como mencioné en mi última actualización, la clave de firma utilizada para firmar las aplicaciones ha cambiado. El motivo de esto fue que necesitábamos cambiar el nombre del paquete de I2P Android. El antiguo nombre de paquete (`net.i2p.android.router`) ya estaba ocupado en Google Play (todavía no sabemos quién lo estaba usando), y queríamos usar el mismo nombre de paquete y la misma clave de firma para todas las distribuciones de I2P Android. Hacerlo significa que un usuario podría instalar inicialmente la aplicación desde el sitio web de I2P y, más tarde, si el sitio web estuviera bloqueado, podría actualizarla mediante Google Play. El sistema operativo Android considera que una aplicación es completamente diferente cuando cambia su nombre de paquete, así que aprovechamos la oportunidad para aumentar la seguridad de la clave de firma.

La huella digital (SHA-256) de la nueva clave de firma es:

```
AD 1E 11 C2 58 46 3E 68 15 A9 86 09 FF 24 A4 8B C0 25 86 C2 36 00 84 9C 16 66 53 97 2F 39 7A 90
```
## Google Play

Hace unos meses publicamos tanto I2P Android como Bote en Google Play en Noruega, para probar allí el proceso de publicación. Nos complace anunciar que ambas aplicaciones ahora se están publicando a nivel mundial por parte de [Privacy Solutions](https://privacysolutions.no/). Las aplicaciones se pueden encontrar en estas URL:

- [I2P on Google Play](https://play.google.com/store/apps/details?id=net.i2p.android)
- [Bote on Google Play](https://play.google.com/store/apps/details?id=i2p.bote.android)

El lanzamiento global se está realizando en varias etapas, comenzando por los países para los que tenemos traducciones. La excepción notable a esto es Francia; debido a las regulaciones de importación sobre código criptográfico, todavía no podemos distribuir estas aplicaciones en Google Play de Francia. Este es el mismo problema que ha afectado a otras aplicaciones como TextSecure y Orbot.

## F-Droid

¡No crean que nos hemos olvidado de ustedes, usuarios de F-Droid! Además de las dos ubicaciones anteriores, hemos establecido nuestro propio repositorio de F-Droid. Si están leyendo esta publicación en su teléfono, [hagan clic aquí](https://f-droid.i2p.io/repo?fingerprint=68E76561AAF3F53DD53BA7C03D795213D0CA1772C3FAC0159B50A5AA85C45DC6) para añadirlo a F-Droid (esto solo funciona en algunos navegadores de Android). O bien, pueden agregar manualmente la URL de abajo a su lista de repositorios de F-Droid:

https://f-droid.i2p.io/repo

Si desea verificar manualmente la huella digital (SHA-256) de la clave de firma del repositorio, o introducirla al agregar el repositorio, aquí está:

```
68 E7 65 61 AA F3 F5 3D D5 3B A7 C0 3D 79 52 13 D0 CA 17 72 C3 FA C0 15 9B 50 A5 AA 85 C4 5D C6
```
Lamentablemente, la aplicación I2P en el repositorio principal de F-Droid no se ha actualizado porque nuestro mantenedor de F-Droid ha desaparecido. Esperamos que, al mantener este repositorio binario, podamos brindar un mejor soporte a nuestros usuarios de F-Droid y mantenerlos al día. Si ya has instalado I2P desde el repositorio principal de F-Droid, tendrás que desinstalarlo si quieres actualizar, porque la clave de firma será diferente. Las aplicaciones en nuestro repositorio de F-Droid son los mismos archivos APK que se ofrecen en nuestro sitio web y en Google Play, así que en el futuro podrás actualizar usando cualquiera de estas fuentes.
