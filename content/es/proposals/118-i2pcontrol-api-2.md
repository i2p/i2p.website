---
title: "API I2PControl 2"
number: "118"
author: "hottuna"
created: "2016-01-23"
lastupdated: "2018-03-22"
status: "Rechazado"
thread: "http://zzz.i2p/topics/2030"
toc: true
---

## Resumen

Esta propuesta describe la API2 para I2PControl.

Esta propuesta fue rechazada y no se implementará, porque rompe la compatibilidad hacia atrás.
Ver el enlace del hilo de discusión para más detalles.

### Advertencia para desarrolladores

Todos los parámetros RPC ahora estarán en minúsculas. Esto *romperá* la compatibilidad hacia atrás con las implementaciones de API1. Las razones para esto son proporcionar a los usuarios de >=API2 la API más simple y coherente posible.


## Especificación de API 2

```json
{
    "id": "id",
    "method": "nombre_del_metodo",
    "params": {
      "token": "token_de_autenticación",
      "method_param": "valor_del_parametro_del_metodo",
    },
    "jsonrpc": "2.0"
  }

  {
    "id": "id",
    "result": "valor_del_resultado",
    "jsonrpc": "2.0"
  }
```

### Parámetros

**`"id"`**

El número de identificación de la solicitud. Se utiliza para identificar qué respuesta se generó por cuál solicitud.

**`"nombre_del_metodo"`**

El nombre del RPC que se está invocando.

**`"token_de_autenticación"`**

El token de autenticación de la sesión. Necesita ser proporcionado con cada RPC, excepto para la llamada 'authenticate'.

**`"valor_del_parametro_del_metodo"`**

El parámetro del método. Se usa para ofrecer diferentes variantes de un método. Como 'obtener', 'establecer' y variantes similares.

**`"valor_del_resultado"`**

El valor que retorna el RPC. Su tipo y contenido depende del método y de cuál método.


### Prefijos

El esquema de nombres RPC es similar a cómo se hace en CSS, con prefijos de vendedor para las diferentes implementaciones de API (i2p, kovri, i2pd):

```text
XXX.YYY.ZZZ
    i2p.XXX.YYY.ZZZ
    i2pd.XXX.YYY.ZZZ
    kovri.XXX.YYY.ZZZ
```

La idea general con los prefijos específicos del vendedor es permitir cierta flexibilidad y dejar que las implementaciones innoven sin tener que esperar a que todas las demás implementaciones se pongan al día. Si un RPC es implementado por todas las implementaciones, se pueden eliminar sus múltiples prefijos y puede incluirse como un RPC central en la próxima versión de API.


### Guía de lectura de métodos

 * **rpc.metodo**

   * *parámetro* [tipo de parámetro]:  [nulo], [número], [cadena], [booleano],
     [arreglo] o [objeto]. [objeto] siendo un mapa {clave:valor}.

Devuelve:
```text

  "valor_devuelto" [cadena] // Este es el valor devuelto por la llamada RPC
```


### Métodos

* **authenticate** - Dado que se proporcione una contraseña correcta, este método te proporciona un token para un acceso posterior y una lista de niveles de API compatibles.

  * *contraseña* [cadena]: La contraseña para esta implementación de i2pcontrol

  Devuelve:
```text

    [objeto]
    {
      "token" : [cadena], // El token que se usará con todos los demás métodos RPC
      "api" : [[int],[int], ...] // Una lista de niveles de API compatibles.
    }
```


* **control.** - Controlar i2p

  * **control.reseed** - Iniciar reabastecimiento

    * [nulo]: No se necesita ningún parámetro

    Devuelve:
```text

      [nulo]

```
  * **control.restart** - Reiniciar instancia de i2p

    * [nulo]: No se necesita ningún parámetro

    Devuelve:
```text

      [nulo]

```
  * **control.restart.graceful** - Reiniciar instancia de i2p de forma ordenada

    * [nulo]: No se necesita ningún parámetro

    Devuelve:
```text

      [nulo]

```
  * **control.shutdown** - Apagar instancia de i2p

    * [nulo]: No se necesita ningún parámetro

    Devuelve:
```text

      [nulo]

```
  * **control.shutdown.graceful** - Apagar instancia de i2p de forma ordenada

    * [nulo]: No se necesita ningún parámetro

    Devuelve:
```text

      [nulo]

```
  * **control.update.find** - **BLOQUEO** Buscar actualizaciones firmadas

    * [nulo]: No se necesita ningún parámetro

    Devuelve:
```text

      true [booleano] // Verdadero si hay una actualización firmada disponible

```
  * **control.update.start** - Iniciar proceso de actualización

    * [nulo]: No se necesita ningún parámetro

    Devuelve:
```text

      [nulo]
```


* **i2pcontrol.** - Configurar i2pcontrol

  * **i2pcontrol.address** - Obtener/Establecer la dirección IP a la que escucha i2pcontrol.

    * *obtener* [nulo]: Este parámetro no necesita ser establecido.

    Devuelve:
```text

      "0.0.0.0" [cadena]

    * *establecer* [cadena]: Esta será una dirección IP como "0.0.0.0" o "192.168.0.1"

    Devuelve:
```text

      [nulo]

```
  * **i2pcontrol.password** - Cambiar la contraseña de i2pcontrol.

    * *establecer* [cadena]: Establecer la nueva contraseña a esta cadena

    Devuelve:
```text

      [nulo]

```
  * **i2pcontrol.port** - Obtener/Establecer el puerto al que escucha i2pcontrol.

    * *obtener* [nulo]: Este parámetro no necesita ser establecido.

    Devuelve:
```text

      7650 [número]

    * *establecer* [número]: Cambiar el puerto al que escucha i2pcontrol a este puerto

    Devuelve:
```text

      [nulo]
```


* **settings.** - Obtener/Establecer configuraciones de instancia de i2p

  * **settings.advanced** - Configuraciones avanzadas

    * *obtener*  [cadena]: Obtener el valor de esta configuración

    Devuelve:
```text

      "valor-configuración" [cadena]

    * *obtenerTodo* [nulo]:

    Devuelve:
```text

      [objeto]
      {
        "nombre-configuración" : "valor-configuración", [cadena]
        ".." : ".." 
      }

    * *establecer* [cadena]: Establecer el valor de esta configuración
    * *establecerTodo* [objeto] {"nombre-configuración" : "valor-configuración", ".." : ".." }

    Devuelve:
```text

      [nulo]

```
  * **settings.bandwidth.in** - Configuraciones de ancho de banda entrante
  * **settings.bandwidth.out** - Configuraciones de ancho de banda saliente

    * *obtener* [nulo]: Este parámetro no necesita ser establecido.

    Devuelve:
```text

      0 [número]

    * *establecer* [número]: Establecer el límite de ancho de banda

    Devuelve:
```text

     [nulo]

```
  * **settings.ntcp.autoip** - Obtener configuración de detección automática de IP para NTCP

    * *obtener* [nulo]: Este parámetro no necesita ser establecido.

    Devuelve:
```text

      true [booleano]

```
  * **settings.ntcp.hostname** - Obtener nombre de host NTCP

    * *obtener* [nulo]: Este parámetro no necesita ser establecido.

    Devuelve:
```text

      "0.0.0.0" [cadena]

    * *establecer* [cadena]: Establecer nuevo nombre de host

    Devuelve:
```text

      [nulo]

```
  * **settings.ntcp.port** - Puerto NTCP

    * *obtener* [nulo]: Este parámetro no necesita ser establecido.

    Devuelve:
```text

      0 [número]

    * *establecer* [número]: Establecer nuevo puerto NTCP.

    Devuelve:
```text

      [nulo]

    * *establecer* [booleano]: Establecer detección automática de IP NTCP

    Devuelve:
```text

      [nulo]

```
  * **settings.ssu.autoip** - Configurar detección automática de IP para SSU

    * *obtener* [nulo]: Este parámetro no necesita ser establecido.

    Devuelve:
```text

      true [booleano]

```
  * **settings.ssu.hostname** - Configurar nombre de host SSU

    * *obtener* [nulo]: Este parámetro no necesita ser establecido.

    Devuelve:
```text

      "0.0.0.0" [cadena]

    * *establecer* [cadena]: Establecer nuevo nombre de host SSU

    Devuelve:
```text

      [nulo]

```
  * **settings.ssu.port** - Puerto SSU

    * *obtener* [nulo]: Este parámetro no necesita ser establecido.

    Devuelve:
```text

      0 [número]

    * *establecer* [número]: Establecer nuevo puerto SSU.

    Devuelve:
```text

      [nulo]

    * *establecer* [booleano]: Establecer detección automática de IP SSU

    Devuelve:
```text

      [nulo]

```
  * **settings.share** - Obtener porcentaje de compartición de ancho de banda

    * *obtener* [nulo]: Este parámetro no necesita ser establecido.

    Devuelve:
```text

      0 [número] // Porcentaje de compartición de ancho de banda (0-100)

    * *establecer* [número]: Establecer porcentaje de compartición de ancho de banda (0-100)

```
  * **settings.upnp** - Activar o desactivar UPNP

    * *obtener* [nulo]: Este parámetro no necesita ser establecido.

    Devuelve:
```text

      true [booleano]

    * *establecer* [booleano]: Establecer detección automática de IP SSU

    Devuelve:
```text

      [nulo]
```



* **stats.** - Obtener estadísticas de la instancia de i2p

  * **stats.advanced** - Este método proporciona acceso a todas las estadísticas guardadas dentro de la instancia.

    * *obtener* [cadena]:  Nombre de la estadística avanzada que se proporcionará
    * *Opcional:* *periodo* [número]:  El periodo para la estadística solicitada

  * **stats.knownpeers** - Devuelve el número de pares conocidos
  * **stats.uptime** - Devuelve el tiempo en ms desde que se inició el enrutador
  * **stats.bandwidth.in** - Devuelve el ancho de banda entrante (idealmente del último segundo)
  * **stats.bandwidth.in.total** - Devuelve el número de bytes recibidos desde el último reinicio
  * **stats.bandwidth.out** - Devuelve el ancho de banda saliente (idealmente del último segundo)'
  * **stats.bandwidth.out.total** - Devuelve el número de bytes enviados desde el último reinicio'
  * **stats.tunnels.participating** - Devuelve el número de túneles con los que se participa actualmente
  * **stats.netdb.peers.active** - Devuelve el número de pares con los que hemos comunicado recientemente
  * **stats.netdb.peers.fast** - Devuelve el número de pares 'rápidos'
  * **stats.netdb.peers.highcapacity** - Devuelve el número de pares de 'alta capacidad'
  * **stats.netdb.peers.known** - Devuelve el número de pares conocidos

    * *obtener* [nulo]: Este parámetro no necesita ser establecido.

    Devuelve:
```text

      0.0 [número]
```


* **status.** - Obtener estado de la instancia de i2p

  * **status.router** - Obtener estado del enrutador

    * *obtener* [nulo]: Este parámetro no necesita ser establecido.

    Devuelve:
```text

      "estado" [cadena]

```
  * **status.net** - Obtener estado de la red del enrutador

    * *obtener* [nulo]: Este parámetro no necesita ser establecido.

    Devuelve:
```text

      0 [número]
      /**
       *    0 – OK
       *    1 – PROBANDO
       *    2 – BLOQUEADO POR CORTAFUEGOS
       *    3 – OCULTO
       *    4 – ADVERTENCIA_BLOQUEADO_POR_CORTAFUEGOS_Y_RÁPIDO
       *    5 – ADVERTENCIA_BLOQUEADO_POR_CORTAFUEGOS_Y_FLOODFILL
       *    6 – ADVERTENCIA_BLOQUEADO_POR_CORTAFUEGOS_CON_TCP_ENTRANTE
       *    7 – ADVERTENCIA_BLOQUEADO_POR_CORTAFUEGOS_CON_UDP_DESACTIVADO
       *    8 – ERROR_I2CP
       *    9 – ERROR_DESFASE_DE_RELOJ
       *   10 – ERROR_DIRECCIÓN_TCP_PRIVADA
       *   11 – ERROR_NAT_SIMÉTRICO
       *   12 – ERROR_PUERTO_UDP_EN_USO
       *   13 – ERROR_NO_HAY_PARES_ACTIVOS_VERIFICAR_CONEXIÓN_Y_CORTAFUEGOS
       *   14 – ERROR_UDP_DESACTIVADO_Y_TCP_NO_ESTABLECIDO
       */

```
  * **status.isfloodfill** - ¿Es actualmente la instancia i2p un floodfill?

    * *obtener* [nulo]: Este parámetro no necesita ser establecido.

    Devuelve:
```text

      true [booleano]

```
  * **status.isreseeding** - ¿Está actualmente la instancia i2p reabasteciendo?

    * *obtener* [nulo]: Este parámetro no necesita ser establecido.

    Devuelve:
```text

      true [booleano]

```
  * **status.ip** - IP pública detectada de esta instancia de i2p

    * *obtener* [nulo]: Este parámetro no necesita ser establecido.

    Devuelve:
```text

      "0.0.0.0" [cadena]
```
