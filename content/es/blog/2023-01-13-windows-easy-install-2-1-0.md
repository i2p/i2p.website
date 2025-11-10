---
title: "Lanzamiento de Windows Easy-Install 2.1.0"
date: 2023-01-13
author: "idk"
description: "Se lanzó Windows Easy-Install Bundle 2.1.0 para mejorar la estabilidad y el rendimiento"
categories: ["release"]
API_Translate: verdadero
---

## Detalles de la actualización

Se ha publicado el I2P Easy-Install bundle para Windows, versión 2.1.0. Como de costumbre, esta versión incluye una actualización del I2P Router. Esta versión de I2P proporciona estrategias mejoradas para gestionar la congestión de la red. Estas deberían mejorar el rendimiento, la conectividad y garantizar la salud a largo plazo de la red de I2P.

Esta versión presenta principalmente mejoras internas en el iniciador del perfil del navegador. La compatibilidad con Tor Browser Bundle se ha mejorado al habilitar la configuración de TBB mediante variables de entorno. Se ha actualizado el perfil de Firefox y las versiones base de las extensiones. Se han realizado mejoras en todo el código base y en el proceso de despliegue.

Lamentablemente, esta versión sigue siendo un instalador .exe no firmado. Por favor, verifique la suma de verificación del instalador antes de usarlo. Las actualizaciones, en cambio, están firmadas con mis claves de firma de I2P y, por lo tanto, son seguras.

Esta versión se compiló con OpenJDK 19. Utiliza i2p.plugins.firefox versión 1.0.7 como biblioteca para iniciar el navegador. Utiliza i2p.i2p versión 2.1.0 como router de I2P y para proporcionar aplicaciones. Como siempre, se recomienda que actualice a la versión más reciente del router de I2P tan pronto como le resulte conveniente.
