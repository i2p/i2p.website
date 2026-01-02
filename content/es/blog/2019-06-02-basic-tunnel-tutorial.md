---
title: "Tutorial básico de I2P Tunnels con imágenes"
date: 2019-06-02
author: "idk"
description: "Configuración básica de i2ptunnel"
categories: ["tutorial"]
---

Aunque el Java I2P router viene preconfigurado con un servidor web estático, jetty, para proporcionar el primer eepSite (sitio web dentro de I2P) del usuario, muchos requieren una funcionalidad más sofisticada de su servidor web y prefieren crear un eepSite con un servidor diferente. Esto, por supuesto, es posible y, de hecho, es muy fácil una vez que lo has hecho por primera vez.

Aunque es fácil de hacer, hay algunas cosas que deberías considerar antes de hacerlo. Querrás eliminar características identificables de tu servidor web, como encabezados potencialmente identificativos y páginas de error predeterminadas que revelan el tipo de servidor/distribución. Para obtener más información sobre las amenazas al anonimato planteadas por aplicaciones mal configuradas, consulta: [Riseup aquí](https://riseup.net/en/security/network-security/tor/onionservices-best-practices), [Whonix aquí](https://www.whonix.org/wiki/Onion_Services), [Este artículo de blog sobre algunos errores de OPSEC](https://blog.0day.rocks/securing-a-web-hidden-service-89d935ba1c1d), [y la página de aplicaciones de I2P aquí](https://geti2p.net/docs/applications/supported). Aunque gran parte de esta información está dirigida a los servicios onion de Tor, los mismos procedimientos y principios se aplican al alojar aplicaciones sobre I2P.

### Paso uno: Abra el Asistente de Tunnel

Ve a la interfaz web de I2P en 127.0.0.1:7657 y abre el [Hidden Services Manager](http://127.0.0.1:7657/i2ptunnelmgr) (enlace a localhost). Haz clic en el botón que dice "Tunnel Wizard" para comenzar.

### Paso dos: Seleccione un tunnel de servidor

El asistente de tunnel es muy sencillo. Como estamos configurando un *servidor* http, lo único que necesitamos hacer es seleccionar un tunnel de *servidor*.

### Paso tres: Seleccione un HTTP tunnel

Un HTTP tunnel es el tipo de tunnel optimizado para alojar servicios HTTP. Tiene funciones de filtrado y de limitación de tasa habilitadas, adaptadas específicamente a ese propósito. Un tunnel estándar puede funcionar también, pero si eliges un tunnel estándar tendrás que encargarte tú mismo de esas funciones de seguridad. Un análisis más profundo de la configuración de HTTP Tunnel está disponible en el siguiente tutorial.

### Paso cuatro: Asigne un nombre y una descripción

Para tu propio beneficio y para poder recordar y distinguir para qué estás usando el tunnel, asígnale un buen apodo y una descripción. Si necesitas volver más adelante para hacer más tareas de administración, así es como identificarás el tunnel en el administrador de servicios ocultos.

### Paso cinco: Configurar el host y el puerto

En este paso, configuras el servidor web para que apunte al puerto TCP en el que tu servidor web está escuchando. Como la mayoría de los servidores web escuchan en el puerto 80 o 8080, el ejemplo refleja eso. Si usas puertos alternativos o máquinas virtuales o contenedores para aislar tus servicios web, puede que necesites ajustar el host (anfitrión), el puerto o ambos.

### Paso seis: Decide si iniciarlo automáticamente

No se me ocurre una forma de detallar más este paso.

### Paso siete: Revise su configuración

Finalmente, revisa los ajustes que has seleccionado. Si te parecen correctos, guárdalos. Si no elegiste iniciar el tunnel automáticamente, ve al Administrador de servicios ocultos y inícialo manualmente cuando desees que tu servicio esté disponible.

### Apéndice: Opciones de personalización del servidor HTTP

I2P ofrece un panel detallado para configurar el tunnel del servidor http de formas personalizadas. Terminaré este tutorial repasándolas todas. Con el tiempo.
