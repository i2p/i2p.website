---
title: "¡Bitcoin Core añade soporte para I2P!"
date: 2021-09-18
author: "idk"
description: "A new use case and a signal of growing acceptance"
categories: ["general"]
API_Translate: verdadero
---

Un evento que llevaba meses gestándose: ¡Bitcoin Core ha incorporado soporte oficial para I2P! Los nodos de Bitcoin sobre I2P pueden interactuar plenamente con el resto de los nodos de Bitcoin, con la ayuda de nodos que operan tanto dentro de I2P como en la clearnet (Internet abierta), lo que los convierte en participantes de primera clase en la red de Bitcoin. Es emocionante ver que comunidades grandes como Bitcoin reconozcan las ventajas que I2P puede aportarles, proporcionando privacidad y reachability (posibilidad de recibir conexiones) a personas de todo el mundo.

## Cómo funciona

El soporte de I2P es automático, mediante la SAM API. Esto también es una noticia emocionante, porque destaca algunas de las cosas en las que I2P es especialmente bueno, como permitir a los desarrolladores de aplicaciones crear conexiones I2P de forma programática y práctica. Los usuarios de Bitcoin sobre I2P pueden usar I2P sin configuración manual habilitando la SAM API y ejecutando Bitcoin con I2P habilitado.

## Configuración de su Router I2P

Para configurar un I2P Router para proporcionar conectividad anónima a bitcoin, es necesario habilitar la SAM API. En Java I2P, debes ir a http://127.0.0.1:7657/configclients e iniciar el SAM Application Bridge con el botón "Start". También puedes habilitar el SAM Application Bridge de forma predeterminada marcando la casilla "Run at Startup" y haciendo clic en "Save Client Configuration".

En i2pd, la API SAM normalmente está habilitada por defecto, pero si no lo está, debes configurar:

```
sam.enabled=true
```
en su archivo i2pd.conf.

## Configuración de su nodo de Bitcoin para anonimato y conectividad

Iniciar Bitcoin en modo anónimo aún requiere editar algunos archivos de configuración en el Directorio de datos de Bitcoin, que es %APPDATA%\Bitcoin en Windows, ~/.bitcoin en Linux y ~/Library/Application Support/Bitcoin/ en Mac OSX. También se requiere al menos la versión 22.0.0 para que el soporte de I2P esté disponible.

Después de seguir estas instrucciones, deberías tener un nodo de Bitcoin privado que use I2P para las conexiones I2P y Tor para las conexiones .onion y clearnet (internet abierta), de modo que todas tus conexiones sean anónimas. Por comodidad, los usuarios de Windows deberían abrir su directorio de datos de Bitcoin abriendo el menú Inicio y buscando "Run." En el cuadro de diálogo Run, escribe "%APPDATA%\Bitcoin" y presiona Enter.

En ese directorio, crea un archivo llamado "i2p.conf." En Windows, debes asegurarte de poner comillas alrededor del nombre del archivo al guardarlo, para evitar que Windows agregue una extensión de archivo predeterminada. El archivo debe contener las siguientes opciones de configuración de Bitcoin relacionadas con I2P:

```
i2psam=127.0.0.1:7656
i2pacceptincoming=true
onlynet=i2p
```
A continuación, debes crear otro archivo llamado "tor.conf." El archivo debe contener las siguientes opciones de configuración relacionadas con Tor:

```
proxy=127.0.0.1:9050
onion=127.0.0.1:9050
onlynet=tor
```
Finalmente, tendrás que "incluir" estas opciones de configuración en tu archivo de configuración de Bitcoin, llamado "bitcoin.conf" en el Directorio de datos. Añade estas dos líneas a tu archivo bitcoin.conf:

```
includeconf=i2p.conf
includeconf=tor.conf
```
Ahora su nodo de Bitcoin está configurado para usar únicamente conexiones anónimas. Para habilitar conexiones directas con nodos remotos, elimine las líneas que comiencen por:

```
onlynet=
```
Puedes hacer esto si no requieres que tu nodo de Bitcoin sea anónimo, y ayuda a que los usuarios anónimos se conecten al resto de la red de Bitcoin.
