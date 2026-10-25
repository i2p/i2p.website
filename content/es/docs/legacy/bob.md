---
title: "BOB - Basic Open Bridge"
description: "API obsoleta para gestión de destinos"
slug: "bob"
aliases:
  - "/es/docs/api/bob"
  - "/es/docs/api/bob/"
  - "/es/bob"
  - "/es/bob/"
lastUpdated: "2025-05"
accurateFor: "0.9.8"
---

## Advertencia - Obsoleto

No debe ser usado por aplicaciones nuevas. BOB, como se especifica aquí, solo soporta el tipo de firma DSA-SHA1. BOB no será extendido para soportar nuevos tipos de firma u otras características avanzadas. Las aplicaciones nuevas deben usar [SAM V3](/docs/api/samv3).

El soporte para BOB fue eliminado de las nuevas instalaciones de Java I2P a partir de la versión 1.7.0 (2022-02). Seguirá funcionando en Java I2P instalado originalmente como versión 1.6.1 o anterior, incluso después de actualizaciones, pero no tiene soporte y puede fallar en cualquier momento. BOB sigue siendo compatible con i2pd hasta 2025-05, pero las aplicaciones aún deberían migrar a SAMv3 por las razones mencionadas anteriormente. Consulta [la documentación de i2pd](https://i2pd.readthedocs.io/en/latest/devs/i2pd-specifics/) para cualquier extensión a la API documentada aquí que sea compatible con i2pd.

En este punto, la mayoría de las buenas ideas de BOB han sido incorporadas en SAMv3, que tiene más características y más uso en el mundo real. BOB puede seguir funcionando en algunas instalaciones (ver arriba), pero no está obteniendo las características avanzadas disponibles para SAMv3 y está esencialmente sin soporte, excepto por i2pd.

## Librerías de Lenguajes para la API BOB

- Go - [ccondom](https://bitbucket.org/kallevedin/ccondom)
- Python - i2py-bob (git.repo.i2p)
- Twisted - [txi2p](https://pypi.python.org/pypi/txi2p)
- C++ - [bobcpp](https://gitlab.com/rszibele/bobcpp)

## Resumen

`KEYS` = par de claves pública+privada, estas son BASE64

`KEY` = clave pública, también BASE64

`ERROR` como se implica devuelve el mensaje `"ERROR "+DESCRIPTION+"\n"`, donde `DESCRIPTION` es lo que salió mal.

`OK` devuelve `"OK"`, y si hay datos que devolver, están en la misma línea. `OK` significa que el comando ha terminado.

Las líneas `DATA` contienen información que solicitaste. Puede haber múltiples líneas `DATA` por solicitud.

**NOTA:** El comando help es el ÚNICO comando que tiene una excepción a las reglas... ¡realmente puede no devolver nada! Esto es intencional, ya que help es un comando HUMANO y no de APLICACIÓN.

## Conexión y Versión

Toda la salida de estado de BOB es por líneas. Las líneas pueden terminar con \\n o \\r\\n, dependiendo del sistema. Al conectarse, BOB produce dos líneas:

```
BOB version
OK
```
La versión actual es: 00.00.10

Tenga en cuenta que las versiones anteriores utilizaban dígitos hexadecimales en mayúsculas y no cumplían con los estándares de versionado de I2P. Se recomienda que las versiones posteriores utilicen únicamente dígitos del 0 al 9.

### Historial de Versiones

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Version</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">I2P Router Version</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Changes</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">00.00.10</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.8</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">current version</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">00.00.00 - 00.00.0F</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">&nbsp;</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">development versions</td>
    </tr>
  </tbody>
</table>
## Comandos

**TENGA EN CUENTA:** Para obtener detalles ACTUALES sobre los comandos, POR FAVOR use el comando de ayuda incorporado. Simplemente conéctese por telnet a localhost 2827 y escriba help para obtener documentación completa sobre cada comando.

Los comandos nunca se vuelven obsoletos o se cambian, sin embargo, de vez en cuando se añaden nuevos comandos.

```
COMMAND     OPERAND                             RETURNS
help        (optional command to get help on)   NOTHING or OK and description of the command
clear                                           ERROR or OK
getdest                                         ERROR or OK and KEY
getkeys                                         ERROR or OK and KEYS
getnick     tunnelname                          ERROR or OK
inhost      hostname or IP address              ERROR or OK
inport      port number                         ERROR or OK
list                                            ERROR or DATA lines and final OK
lookup      hostname                            ERROR or OK and KEY
newkeys                                         ERROR or OK and KEY
option      key1=value1 key2=value2...          ERROR or OK
outhost     hostname or IP address              ERROR or OK
outport     port number                         ERROR or OK
quiet                                           ERROR or OK
quit                                            OK and terminates the command connection
setkeys     KEYS                                ERROR or OK and KEY
setnick     tunnel nickname                     ERROR or OK
show                                            ERROR or OK and information
showprops                                       ERROR or OK and information
start                                           ERROR or OK
status      tunnel nickname                     ERROR or OK and information
stop                                            ERROR or OK
verify      KEY                                 ERROR or OK
visit                                           OK, and dumps BOB's threads to the wrapper.log
zap                                             nothing, quits BOB
```
Una vez configurado, todos los sockets TCP pueden y van a bloquearse según sea necesario, y no hay necesidad de mensajes adicionales hacia/desde el canal de comandos. Esto permite al router controlar el ritmo del flujo sin explotar con errores de memoria insuficiente (OOM) como hace SAM cuando se ahoga intentando empujar muchos flujos de entrada o salida por un solo socket -- ¡eso no puede escalar cuando tienes muchas conexiones!

Lo que también es agradable de esta interfaz en particular es que escribir cualquier cosa para interactuar con ella es mucho, mucho más fácil que SAM. No hay otro procesamiento que hacer después de la configuración. Su configuración es tan simple, que herramientas muy simples, como nc (netcat) pueden usarse para apuntar a alguna aplicación. El valor ahí es que uno podría programar tiempos de activación y desactivación para una aplicación, y no tener que cambiar la aplicación para hacer eso, o incluso tener que detener esa aplicación. En su lugar, puedes literalmente "desconectar" el destino, y "conectarlo" de nuevo. Mientras se usen las mismas direcciones IP/puerto y claves de destino cuando se levante el puente, la aplicación TCP normal no se preocupará, y no lo notará. Simplemente será engañada -- los destinos no son alcanzables, y nada está llegando.

## Ejemplos

Para el siguiente ejemplo, configuraremos una conexión loopback local muy simple, con dos destinos. El destino "mouth" será el servicio CHARGEN del demonio superservidor INET. El destino "ear" será un puerto local al que puedes conectarte por telnet y observar cómo brota el bonito vómito de prueba ASCII.

### Ejemplo de Diálogo de Sesión

Un simple telnet 127.0.0.1 2827 funciona.

- A = Aplicación
- C = Respuesta de comando de BOB.

```
FROM    TO      DIALOGUE
C       A       BOB 00.00.10
C       A       OK
A       C       setnick mouth
C       A       OK Nickname set to mouth
A       C       newkeys
C       A       OK ZMPz1zinTdy3~zGD~f3g9aikZTipujEvvXOEyYfq4Su-mNKerqG710hFbkR6P-xkouVyNQsqWLI8c6ngnkSwGdUfM7hGccqBYDjIubTrlr~0g2-l0vM7Y8nSqtFrSdMw~pyufXZ0Ys3NqUSb8NuZXpiH2lCCkFG21QPRVfKBGwvvyDVU~hPVfBHuR8vkd5x0teMXGGmiTzdB96DuNRWayM0y8vkP-1KJiPFxKjOXULjuXhLmINIOYn39bQprq~dAtNALoBgd-waZedYgFLvwHDCc9Gui8Cpp41EihlYGNW0cu0vhNFUN79N4DEpO7AtJyrSu5ZjFTAGjLw~lOvhyO2NwQ4RiC4UCKSuM70Fz0BFKTJquIjUNkQ8pBPBYvJRRlRG9HjAcSqAMckC3pvKKlcTJJBAE8GqexV7rdCCIsnasJXle-6DoWrDkY1s1KNbEVH6i1iUEtmFr2IHTpPeFCyWfZ581CAFNRbbUs-MmnZu1tXAYF7I2-oXTH2hXoxCGAAAA
```
**¡ANOTA LA CLAVE DE DESTINO ANTERIOR, LA TUYA SERÁ DIFERENTE!**

```
FROM    TO      DIALOGUE
A       C       outhost 127.0.0.1
C       A       OK outhost set
A       C       outport 19
C       A       OK outbound port set
A       C       start
C       A       OK tunnel starting
```
En este punto, no hubo ningún error, se configuró un destino con el apodo "mouth". Cuando te conectas al destino proporcionado, en realidad te conectas al servicio `CHARGEN` en `19/TCP`.

Ahora la otra mitad, para que realmente podamos contactar con este destino.

```
FROM    TO      DIALOGUE
C       A       BOB 00.00.10
C       A       OK
A       C       setnick ear
C       A       OK Nickname set to ear
A       C       newkeys
C       A       OK 8SlWuZ6QNKHPZ8KLUlExLwtglhizZ7TG19T7VwN25AbLPsoxW0fgLY8drcH0r8Klg~3eXtL-7S-qU-wdP-6VF~ulWCWtDMn5UaPDCZytdGPni9pK9l1Oudqd2lGhLA4DeQ0QRKU9Z1ESqejAIFZ9rjKdij8UQ4amuLEyoI0GYs2J~flAvF4wrbF-LfVpMdg~tjtns6fA~EAAM1C4AFGId9RTGot6wwmbVmKKFUbbSmqdHgE6x8-xtqjeU80osyzeN7Jr7S7XO1bivxEDnhIjvMvR9sVNC81f1CsVGzW8AVNX5msEudLEggpbcjynoi-968tDLdvb-CtablzwkWBOhSwhHIXbbDEm0Zlw17qKZw4rzpsJzQg5zbGmGoPgrSD80FyMdTCG0-f~dzoRCapAGDDTTnvjXuLrZ-vN-orT~HIVYoHV7An6t6whgiSXNqeEFq9j52G95MhYIfXQ79pO9mcJtV3sfea6aGkMzqmCP3aikwf4G3y0RVbcPcNMQetDAAAA
A       C       inhost 127.0.0.1
C       A       OK inhost set
A       C       inport 37337
C       A       OK inbound port set
A       C       start
C       A       OK tunnel starting
A       C       quit
C       A       OK Bye!
```
Ahora todo lo que necesitamos hacer es conectarnos por telnet a 127.0.0.1, puerto 37337, enviar la clave de destino o dirección de host del libro de direcciones que queremos contactar. En este caso, queremos contactar "mouth", todo lo que hacemos es pegar la clave y funciona.

**NOTA:** El comando "quit" en el canal de comandos NO desconecta los túneles como SAM.

```
$ telnet 127.0.0.1 37337
Trying 127.0.0.1...
Connected to 127.0.0.1.
Escape character is '^]'.
ZMPz1zinTdy3~zGD~f3g9aikZTipujEvvXOEyYfq4Su-mNKerqG710hFbkR6P-xkouVyNQsqWLI8c6ngnkSwGdUfM7hGccqBYDjIubTrlr~0g2-l0vM7Y8nSqtFrSdMw~pyufXZ0Ys3NqUSb8NuZXpiH2lCCkFG21QPRVfKBGwvvyDVU~hPVfBHuR8vkd5x0teMXGGmiTzdB96DuNRWayM0y8vkP-1KJiPFxKjOXULjuXhLmINIOYn39bQprq~dAtNALoBgd-waZedYgFLvwHDCc9Gui8Cpp41EihlYGNW0cu0vhNFUN79N4DEpO7AtJyrSu5ZjFTAGjLw~lOvhyO2NwQ4RiC4UCKSuM70Fz0BFKTJquIjUNkQ8pBPBYvJRRlRG9HjAcSqAMckC3pvKKlcTJJBAE8GqexV7rdCCIsnasJXle-6DoWrDkY1s1KNbEVH6i1iUEtmFr2IHTpPeFCyWfZ581CAFNRbbUs-MmnZu1tXAYF7I2-oXTH2hXoxCGAAAA
 !"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefg
!"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefgh
"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghi
#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghij
$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijk
...
```
Después de unas pocas millas virtuales de esta avalancha de datos, presiona `Control-]`

```
...
cdefghijklmnopqrstuvwxyz{|}~ !"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJK
defghijklmnopqrstuvwxyz{|}~ !"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKL
efghijklmnopqrstuvwxyz{|}~ !"#$%&'()*+,-./0123456789:;<=
telnet> c
Connection closed.
```
Esto es lo que pasó...

```
telnet -> ear -> i2p -> mouth -> chargen -.
telnet <- ear <- i2p <- mouth <-----------'
```
¡También puedes conectarte a SITIOS I2P!

```
$ telnet 127.0.0.1 37337
Trying 127.0.0.1...
Connected to 127.0.0.1.
Escape character is '^]'.
i2host.i2p
GET / HTTP/1.1

HTTP/1.1 200 OK
Date: Fri, 05 Dec 2008 14:20:28 GMT
Connection: close
Content-Type: text/html
Content-Length: 3946
Last-Modified: Fri, 05 Dec 2008 10:33:36 GMT
Accept-Ranges: bytes

<html>
<head>
  <title>I2HOST</title>
  <link rel="shortcut icon" href="favicon.ico">
</head>
...
<a href="http://sponge.i2p/">--Sponge.</a></pre>
<img src="/counter.gif" alt="!@^7A76Z!#(*&%"> visitors. </body>
</html>
Connection closed by foreign host.
$
```
Bastante genial, ¿no? Prueba con algunos otros sitios I2P conocidos si quieres, algunos inexistentes, etc., para tener una idea del tipo de salida que puedes esperar en diferentes situaciones. En su mayoría, se sugiere que ignores cualquier mensaje de error. Serían insignificantes para la aplicación y solo se presentan para depuración humana.

### Limpieza

Vamos a cerrar nuestros destinos ahora que hemos terminado con todos ellos.

Primero, veamos qué apodos de destino tenemos.

```
FROM    TO      DIALOGUE
A       C       list
C       A       DATA NICKNAME: mouth STARTING: false RUNNING: true STOPPING: false KEYS: true QUIET: false INPORT: not_set INHOST: localhost OUTPORT: 19 OUTHOST: 127.0.0.1
C       A       DATA NICKNAME: ear STARTING: false RUNNING: true STOPPING: false KEYS: true QUIET: false INPORT: 37337 INHOST: 127.0.0.1 OUTPORT: not_set OUTHOST: localhost
C       A       OK Listing done
```
Muy bien, ahí están. Primero, eliminemos "mouth".

```
FROM    TO      DIALOGUE
A       C       getnick mouth
C       A       OK Nickname set to mouth
A       C       stop
C       A       OK tunnel stopping
A       C       clear
C       A       OK cleared
```
Ahora para eliminar "ear", ten en cuenta que esto es lo que pasa cuando escribes demasiado rápido, y te muestra cómo se ven los mensajes de ERROR típicos.

```
FROM    TO      DIALOGUE
A       C       getnick ear
C       A       OK Nickname set to ear
A       C       stop
C       A       OK tunnel stopping
A       C       clear
C       A       ERROR tunnel is active
A       C       clear
C       A       OK cleared
A       C       quit
C       A       OK Bye!
```
## Modo Silencioso

No me molestaré en mostrar un ejemplo del extremo receptor de un puente porque es muy simple. Hay dos configuraciones posibles para él, y se alterna con el comando "quiet".

El valor predeterminado NO es silencioso, y los primeros datos que llegan a tu socket de escucha son el destino que está haciendo el contacto. Es una sola línea que consiste en la dirección BASE64 seguida de un salto de línea. Todo lo que viene después es para que la aplicación lo consuma realmente.

En modo silencioso, piénsalo como una conexión regular a Internet. No entra ningún dato adicional en absoluto. Es como si estuvieras conectado directamente a Internet normal. Este modo permite una forma de transparencia muy similar a la disponible en las páginas de configuración de túneles de la consola del router, para que puedas usar BOB para dirigir un destino a un servidor web, por ejemplo, y no tendrías que modificar el servidor web en absoluto.

## Ventajas de BOB

La ventaja de usar BOB para esto es como se discutió anteriormente. Podrías programar tiempos de actividad aleatorios para la aplicación, redirigir a una máquina diferente, etc. Un uso de esto podría ser algo como querer intentar confundir las conjeturas de disponibilidad de router a destino. Podrías detener e iniciar el destino con un proceso totalmente diferente para crear tiempos aleatorios de actividad y desactividad en los servicios. De esa manera solo estarías deteniendo la capacidad de contactar tal servicio, y no tendrías que molestarte cerrándolo y reiniciándolo. Podrías redirigir y apuntar a una máquina diferente en tu LAN mientras haces actualizaciones, o apuntar a un conjunto de máquinas de respaldo dependiendo de lo que esté ejecutándose, etc, etc. Solo tu imaginación limita lo que podrías hacer con BOB.
