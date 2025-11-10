---
title: "Cómo configurar un servidor ssh detrás de I2P para acceso personal"
date: 2019-06-15
author: "idk"
description: "SSH sobre I2P"
---

# Cómo configurar un servidor SSH detrás de I2P para acceso personal

Este es un tutorial sobre cómo configurar y ajustar un I2P tunnel para acceder a un servidor SSH de forma remota, usando I2P o i2pd. Por ahora, se asume que instalarás tu servidor SSH desde un gestor de paquetes y que se ejecuta como un servicio.

Consideraciones: En esta guía, asumo algunas cosas. Será necesario ajustarlas según las complicaciones que surjan en tu configuración particular, especialmente si usas VMs (máquinas virtuales) o contenedores para aislamiento. Se asume que el router de I2P y el servidor SSH se están ejecutando en el mismo localhost. Deberías usar claves de host SSH recién generadas, ya sea utilizando un sshd recién instalado o eliminando las claves antiguas y forzando su regeneración. Por ejemplo:

```
sudo service openssh stop
sudo rm -f /etc/ssh/ssh_host_*
sudo ssh-keygen -N "" -t rsa -f /etc/ssh/ssh_host_rsa_key
sudo ssh-keygen -N "" -t dsa -f /etc/ssh/ssh_host_dsa_key
sudo ssh-keygen -N "" -t ecdsa -f /etc/ssh/ssh_host_ecdsa_key
sudo ssh-keygen -N "" -t ed25519 -f /etc/ssh/ssh_host_ed25519_key
```
## Step One: Set up I2P tunnel for SSH Server

### Using Java I2P

Usando la interfaz web de I2P en Java, navega al [Administrador de Servicios Ocultos](http://127.0.0.1:7657/i2ptunnelmgr) e inicia el asistente de tunnel.

#### Tunnel Wizard

Dado que estás configurando este tunnel para el servidor SSH, debes seleccionar el tipo de tunnel "Server".

**Marcador de posición de la captura de pantalla:** Utiliza el asistente para crear un "Server" tunnel

Deberías afinarlo más adelante, pero el tipo de tunnel estándar es el más fácil para empezar.

**Marcador de posición de captura de pantalla:** De la variedad "Estándar"

Escriba una buena descripción:

**Marcador de posición de la captura de pantalla:** Describe para qué sirve

Y especifique dónde estará disponible el servidor SSH.

**Marcador de posición de captura de pantalla:** Apúntalo a la futura ubicación de tu servidor SSH

Revisa los resultados y guarda tu configuración.

**Marcador de posición de la captura de pantalla:** Guarde la configuración.

#### Advanced Settings

Ahora vuelve al Hidden Services Manager (Administrador de Servicios Ocultos) y revisa los ajustes avanzados disponibles. Una cosa que sin duda querrás cambiar es configurarlo para conexiones interactivas en lugar de conexiones masivas.

**Marcador de posición de captura de pantalla:** Configure su tunnel para conexiones interactivas

Además de eso, estas otras opciones pueden afectar el rendimiento al acceder a tu servidor SSH. Si no te preocupa demasiado tu anonimato, entonces podrías reducir la cantidad de saltos que realizas. Si tienes problemas de velocidad, una mayor cantidad de tunnel podría ayudar. Unos cuantos tunnel de respaldo probablemente sean una buena idea. Quizás tengas que ajustar la configuración un poco.

**Marcador de posición de la captura de pantalla:** Si no le preocupa el anonimato, entonces reduzca la longitud del tunnel.

Finally, restart the tunnel so that all of your settings take effect.

Otra configuración interesante, especialmente si decides ejecutar un gran número de tunnels, es "Reduce on Idle", que reducirá el número de tunnels que se ejecutan cuando el servidor ha experimentado inactividad prolongada.

**Marcador de posición de la captura de pantalla:** Reducir en inactividad, si eligió un número alto de tunnels

### Using i2pd

Con i2pd, toda la configuración se realiza mediante archivos en lugar de a través de una interfaz web. Para configurar un tunnel de servicio SSH para i2pd, ajuste los siguientes parámetros de ejemplo según sus necesidades de anonimato y rendimiento y cópielos en tunnels.conf

```
[SSH-SERVER]
type = server
host = 127.0.0.1
port = 22
inbound.length = 1
outbound.length = 1
inbound.quantity = 5
outbound.quantity = 5
i2cp.reduceOnIdle = true
keys = ssh-in.dat
```
#### Restart your I2P router

## Paso Uno: Configurar I2P tunnel para el servidor SSH

Según cómo quieras acceder a tu servidor SSH, quizá quieras hacer algunos cambios en la configuración. Además de las medidas obvias de endurecimiento de SSH que deberías aplicar en todos los servidores SSH (autenticación con clave pública, sin inicio de sesión como root, etc.), si no quieres que tu servidor SSH escuche en ninguna dirección excepto en el tunnel de tu servidor, deberías cambiar AddressFamily a inet y ListenAddress a 127.0.0.1.

```
AddressFamily inet
ListenAddress 127.0.0.1
```
Si decide usar un puerto distinto de 22 para su servidor SSH, deberá cambiar el puerto en la configuración de su I2P tunnel.

## Step Three: Set up I2P tunnel for SSH Client

Necesitarás poder ver la consola del router I2P del servidor SSH para configurar la conexión de tu cliente. Una ventaja de esta configuración es que la conexión inicial al I2P tunnel está autenticada, lo que reduce en cierta medida el riesgo de que tu conexión inicial al servidor SSH sea objeto de un ataque Man-in-the-Middle (MITM), como sucede en los escenarios de Trust-On-First-Use (confianza al primer uso).

### Uso de Java I2P

#### Asistente de Tunnel

Primero, inicie el asistente de configuración de tunnel desde el administrador de servicios ocultos y seleccione un tunnel de cliente.

**Marcador de posición de captura de pantalla:** Use el asistente para crear un client tunnel

A continuación, seleccione el tipo de tunnel estándar. Podrá afinar esta configuración más adelante.

**Marcador de posición de la captura de pantalla:** Del tipo estándar

Escribe una buena descripción.

**Marcador de posición de la captura de pantalla:** Proporcione una buena descripción

Esta es la única parte ligeramente complicada. Ve al administrador de servicios ocultos de la consola del router de I2P y encuentra el "local destination" (destino local) en base64 del tunnel del servidor SSH. Necesitarás encontrar una forma de copiar esta información en el siguiente paso. Normalmente me lo envío por [Tox](https://tox.chat); cualquier método off-the-record debería ser suficiente para la mayoría de las personas.

**Marcador de posición de la captura de pantalla:** Busca el destino al que deseas conectarte

Una vez que hayas encontrado, en tu dispositivo cliente, el destino en base64 al que deseas conectarte, pégalo en el campo de destino del cliente.

**Marcador de posición de la captura de pantalla:** Fije el destino

Por último, configure un puerto local al que se conectará su cliente SSH. Ese puerto local se conectará al destino en base64 y, por lo tanto, al servidor SSH.

**Marcador de posición de la captura de pantalla:** Elija un puerto local

Decida si desea que se inicie automáticamente.

**Espacio reservado para captura de pantalla:** Decide si quieres que se inicie automáticamente

#### Configuración avanzada

Como antes, querrás cambiar la configuración para optimizarla para conexiones interactivas. Además, si quieres configurar una lista blanca de clientes en el servidor, deberías marcar el botón de opción "Generate key to enable persistent client tunnel identity".

**Marcador de posición de la captura de pantalla:** Configúrelo para que sea interactivo

### Using i2pd

Puedes configurarlo añadiendo las siguientes líneas a tu tunnels.conf y ajustarlo según tus necesidades de rendimiento/anonimato.

```
[SSH-CLIENT]
type = client
host = 127.0.0.1
port = 7622
inbound.length = 1
outbound.length = 1
inbound.quantity = 5
outbound.quantity = 5
i2cp.dontPublishLeaseSet = true
destination = thisshouldbethebase32ofthesshservertunnelabovebefore.b32.i2p
keys = ssh-in.dat
```
#### Restart the I2P router on the client

## Step Four: Set up SSH client

Hay muchas maneras de configurar un cliente SSH para conectarse a tu servidor en I2P, pero hay algunas cosas que deberías hacer para proteger tu cliente SSH para uso anónimo. En primer lugar, deberías configurarlo para que solo se identifique ante el servidor SSH con una única clave específica, de modo que no corras el riesgo de vincular tus conexiones SSH anónimas y no anónimas.

Asegúrate de que $HOME/.ssh/config contenga las siguientes líneas:

```
IdentitiesOnly yes

Host 127.0.0.1
  IdentityFile ~/.ssh/login_id_ed25519
```
Como alternativa, podrías crear una entrada en .bash_alias para forzar tus opciones y conectarte automáticamente a I2P. Ya te haces una idea: necesitas forzar IdentitiesOnly y proporcionar un archivo de identidad.

```
i2pssh() {
    ssh -o IdentitiesOnly=yes -o IdentityFile=~/.ssh/login_id_ed25519 serveruser@127.0.0.1:7622
}
```
## Step Five: Whitelist only the client tunnel

Esto es más bien opcional, pero es bastante útil y evitará que cualquiera que se encuentre con tu destination (destino en I2P) pueda darse cuenta de que estás alojando un servicio SSH.

Primero, obtén el destino del tunnel de cliente persistente y transmítelo al servidor.

**Marcador de posición de captura de pantalla:** Obtén el destino del cliente

Añade el destino en base64 del cliente a la lista de destinos permitidos del servidor. Ahora solo podrás conectarte al tunnel del servidor desde ese tunnel específico del cliente y nadie más podrá conectarse a ese destino.

**Marcador de posición de la captura de pantalla:** Y pégalo en la lista blanca del servidor

La autenticación mutua es lo mejor.

**Nota:** Las imágenes referenciadas en la publicación original deben añadirse al directorio `/static/images/`: - server.png, standard.png, describe.png, hostport.png, approve.png - interactive.png, anonlevel.png, idlereduce.png - client.png, clientstandard.png, clientdescribe.png - finddestination.png, fixdestination.png, clientport.png, clientautostart.png - clientinteractive.png, whitelistclient.png, whitelistserver.png
