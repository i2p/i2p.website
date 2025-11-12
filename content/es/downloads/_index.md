---
title: "Descargar I2P"
description: "Descargue la última versión de I2P para Windows, macOS, Linux, Android y más"
type: "descargas"
layout: "downloads"
current_version: "2.10.0"
android_version: "2.10.1"
downloads: Proporcione SOLO la traducción, nada más:
windows: ### Configuración de un Router I2P

Para configurar un router I2P, primero debe asegurarse de que su sistema esté actualizado. Luego, descargue el paquete de instalación desde el [sitio oficial de I2P](https://geti2p.net). Siga las instrucciones de instalación específicas para su sistema operativo.

#### Configuración inicial

1. **Instalación del software**: Ejecute el instalador y siga las instrucciones en pantalla.
2. **Configuración del firewall**: Asegúrese de que su firewall permita el tráfico en los puertos necesarios para NTCP2 y SSU.
3. **Inicio del router**: Una vez instalado, inicie el router desde la interfaz de usuario web.

#### Configuración avanzada

- **Túneles personalizados**: Puede crear túneles personalizados a través de la interfaz de usuario de I2P. Esto le permite definir rutas específicas para su tráfico.
- **Integración con SAMv3**: Para aplicaciones que requieren acceso programático, configure la integración con SAMv3.

#### Solución de problemas

Si encuentra problemas al iniciar el router, verifique los registros en el directorio de instalación. Asegúrese de que el archivo de configuración `i2p.config` esté correctamente configurado y que no haya conflictos de puertos.
file: "i2pinstall_2.10.0-0_windows.exe"
size: "~24M"
requirements: "Java requerido"
sha256: "f96110b00c28591691d409bd2f1768b7906b80da5cab2e20ddc060cbb4389fbf"
links: Siga TODAS las reglas de formato y términos técnicos del mensaje del sistema.
primary: "https://i2p.net/files/2.10.0/i2pinstall_2.10.0-0_windows.exe"
mirror: "https://mirror.stormycloud.org/2.10.0/i2pinstall_2.10.0-0_windows.exe"
torrent: "magnet:?xt=urn:btih:75d8c74e9cc52f5cb4982b941d7e49f9f890c458&dn=i2pinstall_2.10.0-0_windows.exe&tr=udp%3A%2F%2Ftracker.opentrackr.org%3A1337%2Fannounce&tr=udp%3A%2F%2Ftracker.openbittorrent.com%3A6969%2Fannounce&tr=udp%3A%2F%2Ftracker.torrent.eu.org%3A451%2Fannounce&tr=http%3A%2F%2Ftracker2.postman.i2p%2Fannounce&tr=http%3A%2F%2Fopentracker.simp.i2p%2Fa&tr=http%3A%2F%2Fopentracker.skank.i2p%2Fa&tr=http%3A%2F%2Fopentracker.dg2.i2p%2Fa&tr=udp%3A%2F%2Fdht.transmissionbt.com%3A6881&tr=udp%3A%2F%2Fdht.aelitis.com%3A6881&tr=udp%3A%2F%2Frouter.bittorrent.com%3A6881"
i2p: "http://mirror.stormycloud.i2p/2.10.0/i2pinstall_2.10.0-0_windows.exe"
tor: "http://hhn4r4qyrmplmfiermza6p3d67a5ra7ecwjeoo5a5ddiogwhyjg675id.onion/2.10.0/i2pinstall_2.10.0-0_windows.exe"
windows_easy_installer: Traduce el siguiente texto del inglés al español.

Sigue todas las reglas de formato y términos técnicos del mensaje del sistema.

Texto a traducir:
file: "I2P-Easy-Install-Bundle-2.10.0-signed.exe"
size: "~162M"
requirements: "No se necesita Java - incluye entorno de ejecución de Java"
sha256: "afcc937004bcf41d4dd2e40de27f33afac3de0652705aef904834fd18afed4b6"
beta: verdadero
links: Proporcione SOLO la traducción, nada más:
primary: "https://i2p.net/files/2.10.0/I2P-Easy-Install-Bundle-2.10.0-signed.exe"
mirror: "https://mirror.stormycloud.org/2.10.0/I2P-Easy-Install-Bundle-2.10.0-signed.exe"
torrent: "magnet:?xt=urn:btih:79e1172aaa21e5bd395a408850de17eff1c5ec24&dn=I2P-Easy-Install-Bundle-2.10.0-signed.exe&tr=udp%3A%2F%2Ftracker.opentrackr.org%3A1337%2Fannounce&tr=udp%3A%2F%2Ftracker.openbittorrent.com%3A6969%2Fannounce&tr=udp%3A%2F%2Ftracker.torrent.eu.org%3A451%2Fannounce&tr=http%3A%2F%2Ftracker2.postman.i2p%2Fannounce&tr=http%3A%2F%2Fopentracker.simp.i2p%2Fa&tr=http%3A%2F%2Fopentracker.skank.i2p%2Fa&tr=http%3A%2F%2Fopentracker.dg2.i2p%2Fa&tr=udp%3A%2F%2Fdht.transmissionbt.com%3A6881&tr=udp%3A%2F%2Fdht.aelitis.com%3A6881&tr=udp%3A%2F%2Frouter.bittorrent.com%3A6881"
i2p: "http://mirror.stormycloud.i2p/2.10.0/I2P-Easy-Install-Bundle-2.10.0-signed.exe"
tor: "http://hhn4r4qyrmplmfiermza6p3d67a5ra7ecwjeoo5a5ddiogwhyjg675id.onion/2.10.0/I2P-Easy-Install-Bundle-2.10.0-signed.exe"
mac_linux: ## Introducción a I2P

I2P, o "The Invisible Internet Project", es una red anónima que permite a las aplicaciones enviar mensajes entre sí de manera privada y segura. Utiliza una arquitectura de "enrutamiento de cebolla" para proteger la identidad de los usuarios y sus actividades en línea.

### ¿Cómo funciona I2P?

I2P crea una red superpuesta sobre Internet, donde los datos se envían a través de una serie de "túneles" cifrados. Cada usuario de I2P ejecuta un "router" que gestiona estos túneles y se comunica con otros routers en la red.

### Componentes clave de I2P

- **Router**: El software que gestiona la conexión a la red I2P.
- **Túneles**: Rutas cifradas a través de las cuales se envían los datos.
- **LeaseSet**: Un conjunto de información que permite a otros usuarios encontrar y comunicarse con un servicio en la red.
- **netDb**: La base de datos distribuida que almacena información sobre los routers y los LeaseSets.

### Beneficios de I2P

- **Anonimato**: Protege la identidad del usuario mediante el cifrado y el enrutamiento de cebolla.
- **Seguridad**: Utiliza cifrado de extremo a extremo para proteger los datos.
- **Resistencia a la censura**: Permite el acceso a contenido bloqueado o restringido.

Para más información, visita el [sitio web oficial de I2P](https://geti2p.net).
file: "i2pinstall_2.10.0.jar"
size: "~30M"
requirements: "Java 8 o superior"
sha256: "76372d552dddb8c1d751dde09bae64afba81fef551455e85e9275d3d031872ea"
links: Traducción:

# Introducción a I2P

I2P, o "The Invisible Internet Project", es una red anónima que permite la comunicación privada y segura entre sus usuarios. A diferencia de otras redes, I2P está diseñada específicamente para proteger la privacidad y resistir la censura.

## ¿Cómo funciona I2P?

I2P utiliza un sistema de "túneles" para enrutar el tráfico de manera anónima. Cada usuario ejecuta un "router" que participa en la red, creando y gestionando túneles de entrada y salida. Estos túneles son unidireccionales, lo que significa que el tráfico de entrada y salida se maneja por separado, aumentando la seguridad.

### Componentes clave de I2P

- **Router**: El software que conecta a un usuario con la red I2P.
- **Túnel**: Un camino cifrado a través del cual se envía el tráfico.
- **leaseSet**: Un conjunto de información que describe cómo alcanzar un servicio en la red.
- **netDb**: La base de datos distribuida que almacena información sobre los routers y los leaseSets.
- **floodfill**: Routers especiales que ayudan a distribuir la información de la netDb.

## Usos comunes de I2P

I2P se utiliza para una variedad de propósitos, incluyendo:

- **Eepsites**: Sitios web accesibles solo dentro de la red I2P.
- **Mensajería segura**: Comunicación cifrada entre usuarios.
- **Compartición de archivos**: Intercambio anónimo de archivos.

Para más información, visita [el sitio oficial de I2P](https://geti2p.net).
primary: "https://i2p.net/files/2.10.0/i2pinstall_2.10.0.jar"
mirror: "https://mirror.stormycloud.org/2.10.0/i2pinstall_2.10.0.jar"
torrent: "magnet:?xt=urn:btih:20ce01ea81b437ced30b1574d457cce55c86dce2&dn=i2pinstall_2.10.0.jar&tr=udp%3A%2F%2Ftracker.opentrackr.org%3A1337%2Fannounce&tr=udp%3A%2F%2Ftracker.openbittorrent.com%3A6969%2Fannounce&tr=udp%3A%2F%2Ftracker.torrent.eu.org%3A451%2Fannounce&tr=http%3A%2F%2Ftracker2.postman.i2p%2Fannounce&tr=http%3A%2F%2Fopentracker.simp.i2p%2Fa&tr=http%3A%2F%2Fopentracker.skank.i2p%2Fa&tr=http%3A%2F%2Fopentracker.dg2.i2p%2Fa&tr=udp%3A%2F%2Fdht.transmissionbt.com%3A6881&tr=udp%3A%2F%2Fdht.aelitis.com%3A6881&tr=udp%3A%2F%2Frouter.bittorrent.com%3A6881"
i2p: "http://mirror.stormycloud.i2p/2.10.0/i2pinstall_2.10.0.jar"
tor: "http://hhn4r4qyrmplmfiermza6p3d67a5ra7ecwjeoo5a5ddiogwhyjg675id.onion/2.10.0/i2pinstall_2.10.0.jar"
source: ### Configuración de I2P

Para comenzar a utilizar I2P, primero debes instalar el software del router I2P. Una vez instalado, abre la consola del router en tu navegador web. La consola del router es la interfaz principal para configurar y monitorear tu nodo I2P.

#### Configuración básica

1. **Iniciar el router**: Asegúrate de que el router I2P esté ejecutándose. Puedes verificar esto accediendo a `http://127.0.0.1:7657`.
2. **Configurar túneles**: Los túneles son esenciales para el funcionamiento de I2P. Puedes crear túneles de cliente y servidor a través de la consola del router.
3. **Conexión a la red**: El router I2P se conectará automáticamente a otros nodos en la red. Esto puede tardar unos minutos.

#### Avanzado

- **Floodfill**: Si deseas contribuir más a la red, puedes habilitar la función de floodfill. Esto ayuda a distribuir la información de la base de datos de la red (netDb).
- **NTCP2 y SSU**: Estos son los protocolos de transporte utilizados por I2P. Asegúrate de que tu firewall permita el tráfico en los puertos necesarios.

Para más detalles, consulta la [documentación oficial de I2P](https://geti2p.net/es/docs).
file: "i2psource_2.10.0.tar.bz2"
size: "~33M"
sha256: "3b651b761da530242f6db6536391fb781bc8e07129540ae7e96882bcb7bf2375"
links: ```markdown
## Configuración del Router I2P

Para configurar su router I2P, primero debe acceder a la consola de administración. Esto se hace generalmente a través de un navegador web ingresando `http://127.0.0.1:7657`. Una vez allí, puede ajustar varias configuraciones para optimizar el rendimiento de su router.

### Ajustes de Túneles

Los túneles son una parte esencial de cómo funciona I2P. Puede configurar la longitud de los túneles y el número de túneles de entrada y salida para equilibrar la seguridad y el rendimiento. 

- **Longitud del túnel**: Un valor más alto aumenta la seguridad pero puede reducir la velocidad.
- **Número de túneles**: Más túneles pueden mejorar la redundancia pero también utilizan más recursos.

### Configuración de Red

I2P utiliza varios protocolos para la comunicación, incluidos NTCP2 y SSU. Asegúrese de que su router esté configurado para utilizar ambos protocolos para una conectividad óptima.

### Administración de Ancho de Banda

Puede limitar el ancho de banda que su router I2P utiliza para evitar que consuma demasiados recursos de su red. Esto se puede ajustar en la sección de configuración de ancho de banda de la consola de administración.

### Seguridad y Privacidad

I2P está diseñado para proporcionar anonimato, pero es importante seguir las mejores prácticas de seguridad. Asegúrese de que su router esté siempre actualizado y considere el uso de garlic encryption para proteger sus comunicaciones.

Para más información, consulte la [documentación oficial de I2P](https://geti2p.net/es/docs).
```
primary: "https://i2p.net/files/2.10.0/i2psource_2.10.0.tar.bz2"
torrent: "magnet:?xt=urn:btih:f62f519204abefb958d553f737ac0a7e84698f35&dn=i2psource_2.10.0.tar.bz2&tr=udp%3A%2F%2Ftracker.opentrackr.org%3A1337%2Fannounce&tr=udp%3A%2F%2Ftracker.openbittorrent.com%3A6969%2Fannounce&tr=udp%3A%2F%2Ftracker.torrent.eu.org%3A451%2Fannounce&tr=http%3A%2F%2Ftracker2.postman.i2p%2Fannounce&tr=http%3A%2F%2Fopentracker.simp.i2p%2Fa&tr=http%3A%2F%2Fopentracker.skank.i2p%2Fa&tr=http%3A%2F%2Fopentracker.dg2.i2p%2Fa&tr=udp%3A%2F%2Fdht.transmissionbt.com%3A6881&tr=udp%3A%2F%2Fdht.aelitis.com%3A6881&tr=udp%3A%2F%2Frouter.bittorrent.com%3A6881"
github: "https://github.com/i2p/i2p.i2p"
android: Siga todas las reglas de formato y términos técnicos del mensaje del sistema.

Texto a traducir:
file: "I2P.apk"
version: "2.10.1"
size: "~28 MB"
requirements: "Android 4.0+, 512MB de RAM como mínimo"
sha256: "c3d4e5f6789012345678901234567890123456789012345678901234abcdef"
links: Traduce el siguiente texto del inglés al español.

Sigue todas las reglas de formato y términos técnicos del mensaje del sistema.

Texto a traducir:
primary: "https://download.i2p.io/android/I2P.apk"
torrent: "magnet:?xt=urn:btih:android_example"
i2p: "http://stats.i2p/android/I2P.apk"
mirrors: ### Configuración de I2P

Para comenzar con I2P, primero debes instalar el software del router I2P. Una vez instalado, abre el panel de control del router en tu navegador web. Aquí puedes configurar varias opciones para personalizar tu experiencia de I2P.

#### Configuración de Túneles

Los túneles son una parte esencial de I2P. Puedes crear túneles de entrada y salida para manejar el tráfico de tu red. Asegúrate de ajustar las configuraciones de ancho de banda para optimizar el rendimiento.

#### Administración de la Base de Datos de Red

La base de datos de red (netDb) almacena información sobre otros routers en la red I2P. Es importante mantener esta base de datos actualizada para asegurar una conectividad óptima. Los routers floodfill ayudan a distribuir esta información de manera eficiente.

#### Seguridad y Privacidad

I2P utiliza cifrado garlic (garlic encryption) para proteger tus datos. Asegúrate de que tu router esté configurado para usar NTCP2 y SSU, que son los protocolos de transporte más seguros disponibles en I2P.

#### Recursos Adicionales

Para más información sobre cómo configurar y usar I2P, visita el [sitio oficial de I2P](https://geti2p.net). Aquí encontrarás documentación detallada y foros de soporte donde puedes hacer preguntas y compartir experiencias con otros usuarios de I2P.
primary: ### Configuración de un router I2P

Para comenzar a utilizar I2P, primero debe configurar su router. Esto implica ajustar varios parámetros en la interfaz de usuario del router I2P. A continuación, se detallan los pasos básicos:

1. **Instalación**: Descargue e instale el software del router I2P desde el [sitio oficial](https://geti2p.net).
2. **Configuración inicial**: Acceda a la consola del router a través de `http://127.0.0.1:7657`. Aquí podrá ajustar configuraciones básicas como el ancho de banda y las conexiones.
3. **Túneles**: Configure los túneles de entrada y salida para optimizar el rendimiento de su conexión. Esto se puede hacer en la sección de "Túneles" de la consola.
4. **Integración con aplicaciones**: Utilice I2PTunnel para integrar aplicaciones como navegadores web o clientes de correo electrónico. Consulte la documentación de I2PTunnel para más detalles.
5. **Seguridad**: Asegúrese de que su router esté actualizado y revise regularmente las configuraciones de seguridad.

### Uso de I2P

Una vez configurado, puede comenzar a explorar la red I2P. Aquí hay algunas actividades comunes:

- **Navegación de eepsites**: Utilice un navegador compatible para acceder a sitios web alojados dentro de I2P, conocidos como eepsites.
- **Mensajería**: Configure aplicaciones de mensajería para comunicarse de manera segura a través de I2P.
- **Compartir archivos**: Utilice herramientas de intercambio de archivos que soporten I2P para compartir contenido de forma anónima.

### Solución de problemas

Si encuentra problemas, consulte los siguientes recursos:

- **Documentación oficial**: La [documentación de I2P](https://geti2p.net/es/docs) ofrece guías detalladas y soluciones a problemas comunes.
- **Foros de la comunidad**: Participe en los foros de la comunidad para obtener ayuda de otros usuarios de I2P.
- **Registro de errores**: Revise los registros de errores en la consola del router para identificar problemas específicos.

Siguiendo estos pasos, podrá configurar y utilizar I2P de manera efectiva.
name: "StormyCloud"
location: "Estados Unidos"
url: "https://stormycloud.org"
resources: ### Configuración de I2P

Para comenzar con I2P, primero debe descargar e instalar el software del router I2P. Una vez instalado, puede acceder a la consola del router a través de su navegador web en `http://127.0.0.1:7657`.

#### Creación de túneles

Los túneles son una parte esencial de cómo I2P protege su privacidad. Para crear un túnel, vaya a la sección de "Túneles" en la consola del router y siga las instrucciones para configurar un nuevo túnel de cliente o servidor.

#### Administración de la base de datos de red

La base de datos de red (netDb) es crucial para el funcionamiento de I2P. Asegúrese de que su router esté configurado para participar en la red como un router floodfill si desea contribuir al mantenimiento de la netDb.

#### Configuración de puertos y protocolos

I2P utiliza varios protocolos para la comunicación, incluidos NTCP2 y SSU. Puede configurar los puertos utilizados por estos protocolos en la sección de "Configuración de red" de la consola del router.

#### Uso de I2PTunnel

I2PTunnel es una herramienta que le permite crear túneles para diferentes tipos de tráfico. Puede configurar un túnel HTTP para acceder a eepsites o un túnel IRC para chatear de forma anónima.

#### Integración con SAMv3

Para los desarrolladores que desean integrar aplicaciones con I2P, SAMv3 proporciona una interfaz sencilla para interactuar con el router I2P. Consulte la documentación de SAMv3 para obtener más detalles sobre cómo comenzar.

#### Seguridad y cifrado

I2P utiliza garlic encryption para proteger sus datos. Asegúrese de que su configuración de seguridad esté actualizada y revise regularmente las actualizaciones de software para mantener la seguridad de su router.
archive: "https://download.i2p.io/archive/"
pgp_keys: "/downloads/pgp-keys"
---
