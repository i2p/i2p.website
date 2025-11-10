---
title: "Actualización sobre la notarización de Mac Easy Install"
date: 2023-01-31
author: "idk, sadie"
description: "El Easy Install Bundle para Mac está atascado"
categories: ["release"]
API_Translate: verdadero
---

El I2P Easy-Install Bundle para Mac ha tenido las actualizaciones paralizadas durante las últimas 2 versiones debido a la salida de su mantenedor. Se recomienda a los usuarios del Easy-Install bundle para Mac que cambien al instalador clásico de estilo Java, que fue restaurado recientemente en la página de descargas. La versión 1.9.0 presenta problemas de seguridad conocidos y no es adecuada para alojar servicios ni para ningún uso a largo plazo. Se aconseja a los usuarios migrar lo antes posible. Los usuarios avanzados del Easy-Install bundle pueden sortear esto compilando el bundle desde el código fuente y autofirmando el software.

## El proceso de notarización para MacOS

Hay muchos pasos en el proceso de distribuir una aplicación a los usuarios de Apple. Para distribuir de forma segura una aplicación como un .dmg, la aplicación debe superar un proceso de notarización. Para presentar una aplicación para su notarización, el desarrollador debe firmarla utilizando un conjunto de certificados que incluye uno para la firma de código y otro para firmar la propia aplicación. Esta firma debe realizarse en puntos específicos durante el proceso de compilación, antes de que se pueda crear el paquete .dmg final que se distribuye a los usuarios finales.

I2P Java es una aplicación compleja y, por ello, ajustar los tipos de código utilizados en la aplicación a los certificados de Apple, así como determinar dónde debe realizarse la firma para producir una marca de tiempo válida, es un proceso de prueba y error. A causa de esta complejidad, la documentación existente para desarrolladores se queda corta a la hora de ayudar al equipo a comprender la combinación correcta de factores que dará como resultado una notarización exitosa.

Estas dificultades hacen que el cronograma para completar este proceso sea difícil de predecir. No sabremos que hemos terminado hasta que podamos limpiar el entorno de compilación y seguir el proceso de extremo a extremo. La buena noticia es que solo nos quedan 4 errores durante el proceso de notarización, frente a más de 50 en el primer intento, y podemos prever razonablemente que se completará antes o a tiempo para la próxima versión en abril.

## Opciones para instalaciones nuevas y actualizaciones de I2P en macOS

Los nuevos participantes de I2P aún pueden descargar el Easy Installer del software 1.9.0 para macOS. Espero tener una versión lista hacia finales de abril. Las actualizaciones a la versión más reciente estarán disponibles en cuanto la notarización sea exitosa.

Las opciones clásicas de instalación también están disponibles. Esto requerirá descargar Java y el software de I2P mediante el instalador basado en .jar.

[Las instrucciones de instalación del JAR están disponibles aquí](https://geti2p.net/en/download/macos)

Los usuarios de Easy-Install pueden actualizar a esa última versión utilizando una compilación de desarrollo producida localmente.

[Las instrucciones de compilación de Easy-Install están disponibles aquí](https://i2pgit.org/i2p-hackers/i2p-jpackage-mac/-/blob/master/BUILD.md)

También existe la opción de desinstalar el software, eliminar el directorio de configuración de I2P y reinstalar I2P usando el instalador .jar.
