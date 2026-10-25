---
title: "Especificación SAM V2"
description: "Protocolo Legacy Simple Anonymous Messaging versión 2 (obsoleto)"
slug: "samv2"
aliases:
  - "/es/docs/api/samv2"
  - "/es/docs/api/samv2/"
  - "/es/samv2"
  - "/es/samv2/"
lastUpdated: "2025-03"
accurateFor: "0.9.20"
---

## Advertencia - Obsoleto - Sin soporte - Usar [SAMv3](/docs/api/samv3)

Se especifica a continuación la versión 2 de un protocolo de cliente simple para interactuar con I2P.

SAM V2 fue introducido en la versión 0.6.1.31 de I2P. Las diferencias significativas con respecto a SAM V1 están marcadas con "\*\*\*". Alternativas: [SAM V1](/docs/api/sam), [SAM V3](/docs/api/samv3), [BOB](/docs/api/bob).

## Cambios de la Versión 2

SAM V2 fue introducido en la versión 0.6.1.31 de I2P. En comparación con la versión 1, SAM v2 proporciona una forma de gestionar varios sockets en el mismo destino I2P *en paralelo*, es decir, el cliente no tiene que esperar a que los datos se envíen exitosamente en un socket antes de enviar datos en otro socket. Todos los datos transitan a través del mismo socket cliente\<--\>SAM. Para múltiples sockets, consulta [SAM V3](/docs/api/samv3).

### Cambios de I2P 0.9.14

La versión reportada permanece "2.0".

- DEST GENERATE ahora soporta un parámetro SIGNATURE_TYPE.
- El parámetro MIN en HELLO VERSION ahora es opcional.
- Los parámetros MIN y MAX en HELLO VERSION ahora soportan versiones de un solo dígito como "3".

## Protocolo Versión 2

La aplicación cliente se comunica con el puente SAM, que maneja toda la funcionalidad de I2P (usando la biblioteca de streaming para flujos virtuales, o I2CP directamente para mensajes asíncronos).

Toda la comunicación cliente\<--\>puente SAM está sin cifrar y sin autenticar a través de un solo socket TCP. El acceso al puente SAM debe protegerse mediante firewalls u otros medios (quizás el puente pueda tener ACLs sobre qué IPs acepta conexiones).

Todos estos mensajes SAM se envían en una sola línea en ASCII plano, terminados por el carácter de nueva línea (\\n). El formato mostrado a continuación es meramente para legibilidad, y aunque las primeras dos palabras en cada mensaje deben mantenerse en su orden específico, el orden de los pares clave=valor puede cambiar (por ejemplo, "ONE TWO A=B C=D" o "ONE TWO C=D A=B" son ambas construcciones perfectamente válidas). Además, el protocolo es sensible a mayúsculas y minúsculas.

Los mensajes SAM se interpretan en UTF-8. Los pares clave=valor deben estar separados por un solo espacio. Los valores pueden estar encerrados entre comillas dobles si contienen espacios, por ejemplo clave="texto de valor largo". No hay mecanismo de escape.

La comunicación puede tomar tres formas distintas:

- [Flujos virtuales](/docs/api/streaming)
- [Datagramas con respuesta](/docs/specs/datagrams#repliable) (mensajes con un campo FROM)
- [Datagramas anónimos](/docs/specs/datagrams#raw) (mensajes anónimos sin procesar)

## Establecimiento de conexión SAM

No puede ocurrir comunicación SAM hasta que el cliente y el bridge hayan acordado una versión de protocolo, lo cual se hace cuando el cliente envía un HELLO y el bridge envía un HELLO REPLY:

```
HELLO VERSION MIN=$min MAX=$max
```
y

```
*** HELLO REPLY RESULT=$result VERSION=2.0
```
A partir de I2P 0.9.14, el parámetro MIN es opcional. El parámetro MAX debe proporcionarse y ser mayor o igual a "2" y menor que "3" para usar la versión 2.

El valor RESULT puede ser uno de:

- `OK`
- `NOVERSION`

## Sesiones SAM

Una sesión SAM se crea cuando un cliente abre un socket al puente SAM, realiza un handshake y envía un mensaje SESSION CREATE, y la sesión termina cuando el socket se desconecta.

Cada I2P Destination solo puede ser utilizado para una sesión SAM a la vez, y solo puede usar una de esas formas (los mensajes recibidos a través de otras formas son descartados).

El mensaje SESSION CREATE enviado por el cliente al bridge es el siguiente:

```
SESSION CREATE
        STYLE={STREAM,DATAGRAM,RAW}
        DESTINATION={$name,TRANSIENT}
        [DIRECTION={BOTH,RECEIVE,CREATE}]
        [option=value]*
```
DESTINATION especifica qué destino debe usarse para enviar y recibir mensajes/streams. Si se proporciona un $name, el puente SAM busca en su almacenamiento local propio (el archivo sam.keys) un destino asociado (y clave privada). Si no existe una asociación que coincida con ese nombre, crea una nueva. Si el destino se especifica como TRANSIENT, siempre crea uno nuevo.

Ten en cuenta que DESTINATION es un identificador, *no* datos codificados en Base 64. Para especificar el Destination, debes usar [SAM V3](/docs/api/samv3).

La DIRECTION puede especificarse solo para sesiones STREAM, instruyendo al puente que el cliente estará creando o recibiendo streams, o ambos. Si esto no se especifica, se asumirá BOTH. Intentar crear un stream saliente cuando DIRECTION=RECEIVE debería resultar en un error, y los streams entrantes cuando DIRECTION=CREATE serán ignorados.

Las opciones adicionales proporcionadas deben ser enviadas a la configuración de la sesión I2P si no son interpretadas por el puente SAM (ej. "tunnels.depthInbound=0"). Estas opciones están documentadas a continuación.

El bridge SAM debería estar ya configurado con qué router debe comunicarse a través de I2P (aunque si es necesario puede haber una forma de proporcionar una anulación, p.ej. i2cp.tcp.host=localhost e i2cp.tcp.port=7654).

Después de recibir el mensaje de creación de sesión, el puente SAM responderá con un mensaje de estado de sesión, de la siguiente manera:

```
SESSION STATUS
        RESULT=$result
        DESTINATION={$name,TRANSIENT}
        [MESSAGE=...]
```
El valor RESULT puede ser uno de:

- `OK`
- `DUPLICATED_DEST`
- `I2P_ERROR`
- `INVALID_KEY`

Si no está bien, el MESSAGE debería contener información legible para humanos sobre por qué no se pudo crear la sesión.

Ten en cuenta que no se emite ninguna advertencia si no se encuentra el $name y en su lugar se crea un destino transitorio. Ten en cuenta que el destino base 64 transitorio real no se muestra en la respuesta; es el $name o TRANSIENT como se proporcionó en SESSION CREATE. Si necesitas estas características, debes usar [SAM V3](/docs/api/samv3).

## Streams Virtuales SAM

Los streams virtuales están garantizados para ser enviados de forma confiable y en orden, con notificación de fallo y éxito tan pronto como esté disponible.

Después de establecer la sesión con STYLE=STREAM, tanto el cliente como el puente SAM pueden enviar de forma asíncrona varios mensajes de ida y vuelta para gestionar los streams, como se enumera a continuación:

```
STREAM CONNECT
       ID=$id
       DESTINATION=$destination
```
Esto establece una nueva conexión virtual desde el destino local al peer especificado, marcándola con el ID único del ámbito de sesión. El ID único es un entero ASCII en base 10 del 1 al (2^31-1).

El $destination es la base 64 del [Destination](/docs/specs/common-structures#type_Destination), que son 516 o más caracteres en base 64 (387 o más bytes en binario), dependiendo del tipo de firma.

El bridge SAM responde a esto con un mensaje de estado del stream:

```
STREAM STATUS
       RESULT=$result
       ID=$id
       [MESSAGE=...]
```
El valor RESULT puede ser uno de:

- `OK`
- `CANT_REACH_PEER`
- `I2P_ERROR`
- `INVALID_KEY`
- `TIMEOUT`

Si el RESULT es OK, el destino especificado está activo y autorizó la conexión; si la conexión no fue posible (timeout, etc), RESULT contendrá el valor de error apropiado (acompañado de un MESSAGE opcional legible por humanos).

En el extremo receptor, el puente SAM simplemente notifica al cliente de la siguiente manera:

```
STREAM CONNECTED
       DESTINATION=$destination
       ID=$id
```
Esto le dice al cliente que el destino dado ha creado una conexión virtual con él. El siguiente flujo de datos será marcado con el ID único dado, que es un entero ASCII en base 10 desde -1 hasta -(2^31-1).

El $destination es la base 64 del [Destination](/docs/specs/common-structures#type_Destination), que tiene 516 o más caracteres en base 64 (387 o más bytes en binario), dependiendo del tipo de firma.

Cuando el cliente quiere enviar datos en la conexión virtual, lo hace de la siguiente manera:

```
STREAM SEND
       ID=$id
       SIZE=$numBytes\n[$numBytes of data]
```
Esto solicita al puente SAM que añada los datos especificados al búfer que se está enviando al par a través de la conexión virtual. El tamaño de envío $numBytes es cuántos bytes de 8 bits se incluyen después de la nueva línea, que puede ser de 1 a 32768 (32KB).

**\*\*\* El puente SAM responde inmediatamente con:**

```
*** STREAM SEND
***        ID=$id
***        RESULT=$result
***        STATE=$bufferState
```
**\*\*\*** donde $bufferState puede ser:

- `BUFFER_FULL` - El búfer de SAM tiene 32 o más KB de datos para enviar, y las solicitudes SEND posteriores fallarán
- `READY` - El búfer de SAM no está lleno, y la próxima solicitud SEND está garantizada de ser exitosa

**\*\*\*** y $result es uno de:

- `OK` - los datos han sido almacenados en el búfer exitosamente
- `FAILED` - el búfer estaba lleno, no se han almacenado datos

**\*\*\*** Si el puente SAM respondió con BUFFER_FULL, enviará otro mensaje tan pronto como su buffer esté disponible nuevamente:

```
*** STREAM READY_TO_SEND ID=$id
```
**\*\*\*** Cuando el resultado es OK, el bridge SAM hará todo lo posible para entregar el mensaje de la manera más rápida y eficiente posible, quizás almacenando en buffer múltiples mensajes SEND juntos. Si hay un error al entregar los datos, o si el lado remoto cierra la conexión, el bridge SAM le dirá al cliente:

```
STREAM CLOSED
       RESULT=$result
       ID=$id
       [MESSAGE=...]
```
El valor RESULT puede ser uno de:

- `OK`
- `CANT_REACH_PEER`
- `I2P_ERROR`
- `PEER_NOT_FOUND`
- `TIMEOUT`

Si la conexión ha sido cerrada limpiamente por el otro peer, $result se establece en OK. Si $result no es OK, MESSAGE puede transmitir un mensaje descriptivo, como "peer unreachable", etc. Cuando un cliente desee cerrar la conexión, envía al puente SAM el mensaje de cierre:

```
STREAM CLOSE
       ID=$id
```
El bridge entonces limpia lo que necesita y descarta ese ID - no se pueden enviar ni recibir más mensajes en él.

Para el otro lado de la comunicación, cuando el peer ha enviado algunos datos y están disponibles para el cliente, el puente SAM los entregará inmediatamente:

```
STREAM RECEIVED
       ID=$id
       SIZE=$numBytes\n[$numBytes of data]
```
**\*\*\*** Sin embargo, con SAM versión 2.0, el cliente primero debe decirle al puente SAM cuántos datos entrantes están permitidos para toda la sesión, enviando un mensaje:

```
*** STREAM RECEIVE
***        ID=$id
***        LIMIT=$limit\n
```
**\*\*\*** donde $limit puede ser:

- `NONE` - el puente SAM seguirá escuchando y entregará los datos entrantes (mismo comportamiento que en la versión 1.0)
- un entero (menor que 2^64) - el número de bytes recibidos después del cual el puente SAM dejará de escuchar en el flujo entrante. Siempre que el cliente esté listo para aceptar más bytes del flujo, tiene que enviar dicho mensaje nuevamente, con un $limit mayor.

**\*\*\*** El cliente debe enviar tales mensajes STREAM RECEIVE después de que se haya establecido la conexión con el peer, es decir, después de que el cliente haya recibido un "STREAM CONNECTED" o un "STREAM STATUS RESULT=OK" del puente SAM.

Todos los streams se cierran implícitamente cuando se pierde la conexión entre el puente SAM y el cliente.

## Datagramas Replicables SAM

Aunque I2P no contiene inherentemente una dirección FROM, para facilitar su uso se proporciona una capa adicional como datagramas replicables - mensajes no ordenados y no confiables de hasta 31744 bytes que incluyen una dirección FROM (dejando hasta 1KB para material de encabezado). Esta dirección FROM es autenticada internamente por SAM (haciendo uso de la clave de firma del destino para verificar la fuente) e incluye prevención de repetición.

El tamaño mínimo es 1. Para la mejor confiabilidad de entrega, el tamaño máximo recomendado es aproximadamente 11 KB.

Después de establecer una sesión SAM con STYLE=DATAGRAM, el cliente puede enviar al bridge SAM:

```
DATAGRAM SEND
         DESTINATION=$destination
         SIZE=$numBytes\n[$numBytes of data]
```
Cuando llega un datagrama, el puente lo entrega al cliente a través de:

```
DATAGRAM RECEIVED
         DESTINATION=$destination
         SIZE=$numBytes\n[$numBytes of data]
```
El $destination es la base 64 del [Destination](/docs/specs/common-structures#type_Destination), que son 516 o más caracteres en base 64 (387 o más bytes en binario), dependiendo del tipo de firma.

El puente SAM nunca expone al cliente las cabeceras de autenticación u otros campos, únicamente los datos que proporcionó el remitente. Esto continúa hasta que se cierra la sesión (cuando el cliente interrumpe la conexión).

## Datagramas Anónimos SAM

Aprovechando al máximo el ancho de banda de I2P, SAM permite a los clientes enviar y recibir datagramas anónimos, dejando la información de autenticación y respuesta a cargo de los propios clientes. Estos datagramas no son confiables y están desordenados, y pueden tener hasta 32768 bytes.

El tamaño mínimo es 1. Para la mejor confiabilidad de entrega, el tamaño máximo recomendado es aproximadamente 11 KB.

Después de establecer una sesión SAM con STYLE=RAW, el cliente puede enviar al puente SAM:

```
RAW SEND
    DESTINATION=$destination
    SIZE=$numBytes\n[$numBytes of data]
```
El $destination es la base 64 de la [Destination](/docs/specs/common-structures#type_Destination), que son 516 o más caracteres en base 64 (387 o más bytes en binario), dependiendo del tipo de firma.

Cuando llega un datagrama sin procesar, el puente lo entrega al cliente a través de:

```
RAW RECEIVED
    SIZE=$numBytes\n[$numBytes of data]
```
## Funcionalidad de la Utilidad SAM

El siguiente mensaje puede ser usado por el cliente para consultar al puente SAM para resolución de nombres:

```
NAMING LOOKUP
       NAME=$name
```
que es respondido por

```
NAMING REPLY
       RESULT=$result
       NAME=$name
       [VALUE=$destination]
       [MESSAGE=$message]
```
El valor RESULT puede ser uno de:

- `OK`
- `INVALID_KEY`
- `KEY_NOT_FOUND`

Si NAME=ME, entonces la respuesta contendrá el destino utilizado por la sesión actual (útil si estás usando uno TRANSIENT). Si $result no es OK, MESSAGE puede transmitir un mensaje descriptivo, como "bad format", etc.

El $destination es la base 64 del [Destination](/docs/specs/common-structures#type_Destination), que son 516 o más caracteres en base 64 (387 o más bytes en binario), dependiendo del tipo de firma.

Las claves públicas y privadas en base64 pueden generarse usando el siguiente mensaje:

```
DEST GENERATE
```
que es respondida por

```
DEST REPLY
     PUB=$destination
     PRIV=$privkey
```
A partir de I2P 0.9.14, se soporta un parámetro opcional SIGNATURE_TYPE. El valor de SIGNATURE_TYPE puede ser cualquier nombre (ej. ECDSA_SHA256_P256, sin distinción entre mayúsculas y minúsculas) o número (ej. 1) que sea soportado por [Key Certificates](/docs/specs/common-structures#type_Certificate). El valor predeterminado es DSA_SHA1.

El $destination es la base 64 del [Destination](/docs/specs/common-structures#type_Destination), que son 516 o más caracteres en base 64 (387 o más bytes en binario), dependiendo del tipo de firma.

La $privkey es la base 64 de la concatenación del [Destination](/docs/specs/common-structures#type_Destination) seguido de la [Private Key](/docs/specs/common-structures#type_PrivateKey) seguida de la [Signing Private Key](/docs/specs/common-structures#type_SigningPrivateKey), que son 884 o más caracteres en base 64 (663 o más bytes en binario), dependiendo del tipo de firma.

## Valores de RESULT

Estos son los valores que puede contener el campo RESULT, con su significado:

| Valor | Significado |
|-------|-------------|
| `OK` | Operación completada exitosamente |
| `CANT_REACH_PEER` | El peer existe, pero no se puede alcanzar |
| `DUPLICATED_DEST` | El Destination especificado ya está en uso |
| `I2P_ERROR` | Un error genérico de I2P (ej. desconexión I2CP, etc.) |
| `INVALID_KEY` | La clave especificada no es válida (formato incorrecto, etc.) |
| `KEY_NOT_FOUND` | El sistema de nombres no puede resolver el nombre dado |
| `PEER_NOT_FOUND` | El peer no se puede encontrar en la red |
| `TIMEOUT` | Tiempo de espera agotado mientras se esperaba un evento (ej. respuesta del peer) |
## Opciones de Tunnel, I2CP y Streaming

Estas opciones pueden pasarse como pares nombre=valor al final de una línea SAM SESSION CREATE.

Todas las sesiones pueden incluir [opciones de I2CP como longitudes de túnel](/docs/protocol/i2cp#options). Las sesiones STREAM pueden incluir [opciones de la librería Streaming](/docs/api/streaming#options). Consulta esas referencias para los nombres de opciones y valores predeterminados.

## Notas sobre Base 64

La codificación Base 64 debe usar el alfabeto Base 64 estándar de I2P "A-Z, a-z, 0-9, -, ~".

## Implementaciones de Bibliotecas de Cliente

Las bibliotecas cliente están disponibles para C, C++, C#, Perl y Python. Estas se encuentran en el directorio apps/sam/ del Paquete de Código Fuente de I2P. Algunas pueden ser más antiguas y no haber sido actualizadas para soporte de SAMv2.

## Configuración SAM por Defecto

El puerto SAM predeterminado es 7656. SAM no está habilitado por defecto en el Router I2P; debe iniciarse manualmente, o configurarse para iniciarse automáticamente, en la página de configurar clientes en la consola del router, o en el archivo clients.config.
