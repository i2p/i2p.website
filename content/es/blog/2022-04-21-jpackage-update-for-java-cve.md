---
title: "Actualización de Jpackage para la CVE-2022-21449 de Java"
date: 2022-04-21
author: "idk"
description: "Se publicaron paquetes de Jpackage con correcciones para la CVE-2022-21449 de Java"
categories: ["release"]
API_Translate: verdadero
---

## Detalles de la actualización

Se han generado nuevos paquetes de instalación fácil de I2P utilizando la última versión de la Máquina Virtual de Java, que contiene una corrección para CVE-2022-21449 "Psychic Signatures". Se recomienda que los usuarios de los paquetes de instalación fácil actualicen lo antes posible. Los usuarios actuales de OSX recibirán actualizaciones automáticamente, los usuarios de Windows deben descargar el instalador desde nuestra página de descargas y ejecutar el instalador normalmente.

El router de I2P en Linux utiliza la Máquina Virtual de Java (JVM) configurada por el sistema host. Los usuarios en esas plataformas deberían volver a una versión estable de Java anterior a Java 14 para mitigar la vulnerabilidad hasta que los mantenedores de paquetes publiquen actualizaciones. Otros usuarios que utilicen una JVM externa deberían actualizar la JVM a una versión corregida lo antes posible.
