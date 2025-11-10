---
title: "Resumen de verano para desarrolladores: APIs"
date: 2016-07-02
author: "str4d"
description: "En el primer mes de Summer Dev, hemos mejorado la usabilidad de nuestras APIs para desarrolladores de Java, Android y Python."
categories: ["summer-dev"]
---

Summer Dev está en pleno apogeo: hemos estado aceitando la maquinaria, puliendo asperezas y poniendo todo en orden. Ahora es el momento de nuestro primer resumen, en el que te ponemos al día sobre los avances que estamos logrando!

## Mes de las APIs

Nuestro objetivo para este mes fue "encajar" - hacer que nuestras APIs y bibliotecas funcionen dentro de la infraestructura existente de diversas comunidades, de modo que los desarrolladores de aplicaciones puedan trabajar con I2P más eficientemente y los usuarios no tengan que preocuparse por los detalles.

### Java / Android

¡Las bibliotecas de cliente de I2P ya están disponibles en Maven Central! Esto debería simplificar mucho que los desarrolladores de Java utilicen I2P en sus aplicaciones. En lugar de tener que obtener las bibliotecas de una instalación existente, pueden simplemente añadir I2P a sus dependencias. Actualizar a nuevas versiones también será mucho más sencillo.

La biblioteca de cliente de I2P para Android también se ha actualizado para usar las nuevas bibliotecas de I2P. Esto significa que las aplicaciones multiplataforma pueden funcionar de forma nativa tanto con I2P Android como con I2P de escritorio.

### Java / Android

#### txi2p

El complemento de Twisted `txi2p` ahora admite puertos dentro de I2P y funciona sin problemas a través de APIs SAM locales, remotas y con reenvío de puertos. Consulta su documentación para obtener instrucciones de uso, y reporta cualquier problema en GitHub.

#### i2psocket

¡Se ha lanzado la primera versión (beta) de `i2psocket`! Es un reemplazo directo de la biblioteca estándar de Python `socket`, que añade compatibilidad con I2P a través de la SAM API. Consulta su página de GitHub para obtener instrucciones de uso y para informar de cualquier problema.

### Python

- zzz has been hard at work on Syndie, getting a headstart on Plugins month
- psi has been creating an I2P test network using i2pd, and in the process has found and fixed several i2pd bugs that will improve its compatibility with Java I2P

## Coming up: Apps month!

¡Estamos entusiasmados de trabajar con Tahoe-LAFS en julio! I2P ha sido durante mucho tiempo el hogar de una de las redes públicas más grandes, usando una versión parcheada de Tahoe-LAFS. Durante el Mes de Apps estaremos ayudándoles con su trabajo en curso para añadir compatibilidad nativa con I2P y Tor, de modo que los usuarios de I2P puedan beneficiarse de todas las mejoras del proyecto principal.

Hay varios otros proyectos con los que estaremos hablando sobre sus planes de integración con I2P y colaborando en el diseño. ¡Estén atentos!

## Take part in Summer Dev!

Tenemos muchas más ideas sobre lo que nos gustaría lograr en estas áreas. Si te interesa hackear en software de privacidad y anonimato, diseñar sitios web o interfaces fáciles de usar, o escribir guías para usuarios: ¡ven y charla con nosotros en IRC o Twitter! Siempre nos alegra dar la bienvenida a quienes se incorporan a nuestra comunidad.

Iremos publicando aquí sobre la marcha, pero también puedes seguir nuestro progreso y compartir tus propias ideas y trabajo con el hashtag #I2PSummer en Twitter. ¡Que empiece el verano!
