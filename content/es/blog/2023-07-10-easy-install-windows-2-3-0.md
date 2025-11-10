---
title: "Publicado Easy-Install para Windows 2.3.0"
date: 2023-07-10
author: "idk"
description: "Publicado Easy-Install para Windows 2.3.0"
categories: ["release"]
API_Translate: verdadero
---

Ya se ha publicado la versión 2.3.0 del I2P Easy-Install bundle para Windows. Como de costumbre, esta versión incluye una actualización del router de I2P. Esto también abarca cuestiones de seguridad que afectan a quienes alojan servicios en la red.

Esta será la última versión del paquete Easy-Install que será incompatible con la I2P Desktop GUI. Se ha actualizado para incluir nuevas versiones de todas las extensiones web incluidas. Se ha corregido un error de larga data en I2P in Private Browsing que lo hacía incompatible con temas personalizados. Aun así, se recomienda a los usuarios *no* instalar temas personalizados. Las pestañas de Snark no se fijan automáticamente en la parte superior del orden de las pestañas en Firefox. Excepto por usar cookieStores alternativos, las pestañas de Snark ahora se comportan como pestañas normales del navegador.

**Lamentablemente, esta versión sigue siendo un instalador `.exe` sin firmar.** Por favor, verifique la suma de verificación del instalador antes de usarlo. **Las actualizaciones, en cambio** están firmadas con mis claves de firma de I2P y, por lo tanto, son seguras.

Esta versión se compiló con OpenJDK 20. Utiliza i2p.plugins.firefox versión 1.1.0 como biblioteca para iniciar el navegador. Utiliza i2p.i2p versión 2.3.0 como un I2P router y para proporcionar aplicaciones. Como siempre, se recomienda actualizar a la versión más reciente del I2P router en cuanto le sea conveniente.

- [Easy-Install Bundle Source](http://git.idk.i2p/i2p-hackers/i2p.firefox/-/tree/i2p-firefox-2.3.0)
- [Router Source](http://git.idk.i2p/i2p-hackers/i2p.i2p/-/tree/i2p-2.3.0)
- [Profile Manager Source](http://git.idk.i2p/i2p-hackers/i2p.plugins.firefox/-/tree/1.1.0)
