---
title: "Especificación SAM V1"
description: "Protocolo heredado de Mensajería Anónima Simple versión 1 (obsoleto)"
slug: "sam"
aliases:
  - "/es/docs/api/sam"
  - "/es/docs/api/sam/"
  - "/es/sam"
  - "/es/sam/"
lastUpdated: "2025-03"
accurateFor: "0.9.20"
---

## Advertencia - Obsoleto - No compatible - Usar [SAMv3](/docs/api/samv3)

Se especifica a continuación la versión 1 de un protocolo de cliente simple para interactuar con I2P. Alternativas más nuevas: [SAM V2](/docs/api/samv2), [SAM V3](/docs/api/samv3), [BOB](/docs/api/bob).

## Bibliotecas de lenguaje para la API SAMv1

- C
- C#
- Perl
- Python

Las librerías están en el repositorio de código fuente de I2P.

### Cambios de I2P 0.9.14

La versión reportada permanece "1.0".

- DEST GENERATE ahora soporta un parámetro SIGNATURE_TYPE.
- El parámetro MIN en HELLO VERSION ahora es opcional.
- Los parámetros MIN y MAX en HELLO VERSION ahora soportan versiones de un solo dígito como "3".

## Protocolo Versión 1

La aplicación cliente se comunica con el puente SAM, que maneja toda la funcionalidad de I2P (usando la biblioteca de streaming para flujos virtuales, o I2CP directamente para mensajes asíncronos).

Toda la comunicación cliente\<--\>puente SAM no está cifrada ni autenticada a través de un solo socket TCP. El acceso al puente SAM debe protegerse mediante cortafuegos u otros medios (quizás el puente pueda tener ACLs sobre qué IPs acepta conexiones).

Todos estos mensajes SAM se envían en una sola línea en ASCII plano, terminados por el carácter de nueva línea (\\n). El formato mostrado a continuación es meramente para legibilidad, y aunque las primeras dos palabras en cada mensaje deben mantener su orden específico, el ordenamiento de los pares clave=valor puede cambiar (p. ej. "ONE TWO A=B C=D" o "ONE TWO C=D A=B" son construcciones perfectamente válidas). Además, el protocolo distingue entre mayúsculas y minúsculas.

Los mensajes SAM se interpretan en UTF-8. Los pares clave=valor deben estar separados por un solo espacio. Los valores pueden estar encerrados entre comillas dobles si contienen espacios, por ejemplo clave="texto de valor largo". No hay mecanismo de escape.

La comunicación puede adoptar tres formas distintas:

- [Flujos virtuales](/docs/api/streaming)
- [Datagramas con respuesta](/docs/specs/datagrams#repliable) (mensajes con un campo FROM)
- [Datagramas anónimos](/docs/specs/datagrams#raw) (mensajes anónimos sin procesar)

## Protocolo de Conexión SAM

No puede ocurrir comunicación SAM hasta que el cliente y el bridge hayan acordado una versión del protocolo, lo cual se hace cuando el cliente envía un HELLO y el bridge envía un HELLO REPLY:

```
HELLO VERSION MIN=$min MAX=$max
```
y

```
HELLO REPLY RESULT=$result VERSION=1.0
```
A partir de I2P 0.9.14, el parámetro MIN es opcional. El parámetro MAX debe proporcionarse y ser mayor o igual a "1" y menor que "2" para usar la versión 1.

El valor RESULT puede ser uno de:

- `OK`
- `NOVERSION`

## Sesiones SAM

Una sesión SAM es creada por un cliente que abre un socket al puente SAM, opera un handshake, y envía un mensaje SESSION CREATE, y la sesión termina cuando el socket es desconectado.

Cada destino I2P solo puede usarse para una sesión SAM a la vez, y solo puede usar una de esas formas (los mensajes recibidos a través de otras formas se descartan).

El mensaje SESSION CREATE enviado por el cliente al bridge es el siguiente:

```
SESSION CREATE
        STYLE={STREAM,DATAGRAM,RAW}
        DESTINATION={$name,TRANSIENT}
        [DIRECTION={BOTH,RECEIVE,CREATE}]
        [option=value]*
```
DESTINATION especifica qué destino debe utilizarse para enviar y recibir mensajes/flujos. Si se proporciona un $name, el puente SAM busca en su propio almacenamiento local (el archivo sam.keys) un destino asociado (y clave privada). Si no existe una asociación que coincida con ese nombre, crea una nueva. Si el destino se especifica como TRANSIENT, siempre crea uno nuevo.

Ten en cuenta que DESTINATION es un identificador, *no* datos codificados en Base 64. Para especificar el Destination, debes usar [SAM V3](/docs/api/samv3).

La DIRECTION puede especificarse solo para sesiones STREAM, indicando al bridge que el cliente estará creando o recibiendo streams, o ambos. Si no se especifica, se asumirá BOTH. Intentar crear un stream saliente cuando DIRECTION=RECEIVE debería resultar en un error, y los streams entrantes cuando DIRECTION=CREATE serán ignorados.

Las opciones adicionales proporcionadas deben ser alimentadas en la configuración de sesión de I2P si no son interpretadas por el puente SAM (por ejemplo, "tunnels.depthInbound=0"). Estas opciones están documentadas a continuación.

El bridge SAM en sí ya debería estar configurado con qué router debe comunicarse a través de I2P (aunque si es necesario puede haber una forma de proporcionar una anulación, por ejemplo i2cp.tcp.host=localhost e i2cp.tcp.port=7654).

Después de recibir el mensaje de creación de sesión, el puente SAM responderá con un mensaje de estado de sesión, como sigue:

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

Si no está bien, el MESSAGE debe contener información legible para humanos sobre por qué no se pudo crear la sesión.

Ten en cuenta que no se da ninguna advertencia si no se encuentra el $name y se crea un destino transitorio en su lugar. Ten en cuenta que el destino base 64 transitorio real no se muestra en la respuesta; es el $name o TRANSIENT tal como se suministró en SESSION CREATE. Si necesitas estas características, debes usar [SAM V3](/docs/api/samv3).

## Flujos Virtuales SAM

Se garantiza que los flujos virtuales se envían de manera confiable y en orden, con notificación de fallo y éxito tan pronto como esté disponible.

Después de establecer la sesión con STYLE=STREAM, tanto el cliente como el puente SAM pueden enviar de forma asíncrona varios mensajes de ida y vuelta para gestionar los streams, como se enumera a continuación:

```
STREAM CONNECT
       ID=$id
       DESTINATION=$destination
```
Esto establece una nueva conexión virtual desde el destino local al peer especificado, marcándola con el ID único del alcance de sesión. El ID único es un entero ASCII base 10 del 1 al (2^31-1).

El $destination es la base 64 del [Destination](/docs/specs/common-structures#type_Destination), que son 516 o más caracteres en base 64 (387 o más bytes en binario), dependiendo del tipo de firma.

El bridge SAM debe responder a esto con un mensaje de estado de flujo:

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
Esto añade los datos especificados al búfer que se está enviando al peer a través de la conexión virtual. El tamaño de envío $numBytes indica cuántos bytes de 8 bits están incluidos después del salto de línea, que puede ser de 1 a 32768 (32KB).

El puente SAM entonces hará todo lo posible por entregar el mensaje tan rápida y eficientemente como sea posible, quizás almacenando en búfer múltiples mensajes SEND juntos. Si hay un error al entregar los datos, o si el lado remoto cierra la conexión, el puente SAM le dirá al cliente:

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

Si la conexión ha sido cerrada limpiamente por el otro peer, $result se establece en OK. Si $result no es OK, MESSAGE puede transmitir un mensaje descriptivo, como "peer unreachable", etc. Siempre que un cliente desee cerrar la conexión, envía al puente SAM el mensaje de cierre:

```
STREAM CLOSE
       ID=$id
```
El bridge luego limpia lo que necesita y descarta esa ID - no se pueden enviar ni recibir más mensajes en ella.

Para el otro lado de la comunicación, cuando el peer ha enviado algunos datos y están disponibles para el cliente, el puente SAM los entregará inmediatamente:

```
STREAM RECEIVED
       ID=$id
       SIZE=$numBytes\n[$numBytes of data]
```
Todos los streams se cierran implícitamente cuando se interrumpe la conexión entre el puente SAM y el cliente.

## Datagramas Replicables SAM

Aunque I2P no contiene inherentemente una dirección FROM, para facilitar su uso se proporciona una capa adicional como datagramas respondibles - mensajes no ordenados y no confiables de hasta 31744 bytes que incluyen una dirección FROM (dejando hasta 1KB para material de cabecera). Esta dirección FROM es autenticada internamente por SAM (haciendo uso de la clave de firma del destino para verificar la fuente) e incluye prevención de repetición.

El tamaño mínimo es 1. Para obtener la mejor confiabilidad de entrega, el tamaño máximo recomendado es aproximadamente 11 KB.

Después de establecer una sesión SAM con STYLE=DATAGRAM, el cliente puede enviar al puente SAM:

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

El puente SAM nunca expone al cliente las cabeceras de autenticación u otros campos, solamente los datos que proporcionó el remitente. Esto continúa hasta que se cierra la sesión (cuando el cliente abandona la conexión).

## Datagramas Anónimos SAM

Aprovechando al máximo el ancho de banda de I2P, SAM permite a los clientes enviar y recibir datagramas anónimos, dejando la información de autenticación y respuesta a cargo de los propios clientes. Estos datagramas no son confiables y están desordenados, y pueden tener hasta 32768 bytes.

El tamaño mínimo es 1. Para una mejor confiabilidad de entrega, el tamaño máximo recomendado es aproximadamente 11 KB.

Después de establecer una sesión SAM con STYLE=RAW, el cliente puede enviar al puente SAM:

```
RAW SEND
    DESTINATION=$destination
    SIZE=$numBytes\n[$numBytes of data]
```
El $destination es la base 64 del [Destination](/docs/specs/common-structures#type_Destination), que tiene 516 o más caracteres en base 64 (387 o más bytes en binario), dependiendo del tipo de firma.

Cuando llega un datagrama sin procesar, el puente lo entrega al cliente a través de:

```
RAW RECEIVED
    SIZE=$numBytes\n[$numBytes of data]
```
## Funcionalidad de Utilidad SAM

El siguiente mensaje puede ser usado por el cliente para consultar al puente SAM para la resolución de nombres:

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

El $destination es la base 64 del [Destination](/docs/specs/common-structures#type_Destination), que tiene 516 o más caracteres en base 64 (387 o más bytes en binario), dependiendo del tipo de firma.

Las claves base64 públicas y privadas pueden generarse usando el siguiente mensaje:

```
DEST GENERATE
```
que es respondido por

```
DEST REPLY
     PUB=$destination
     PRIV=$privkey
```
A partir de I2P 0.9.14, se admite un parámetro opcional SIGNATURE_TYPE. El valor de SIGNATURE_TYPE puede ser cualquier nombre (por ejemplo, ECDSA_SHA256_P256, sin distinguir mayúsculas y minúsculas) o número (por ejemplo, 1) que sea compatible con [Key Certificates](/docs/specs/common-structures#type_Certificate). El valor predeterminado es DSA_SHA1.

El $destination es la base 64 del [Destination](/docs/specs/common-structures#type_Destination), que tiene 516 o más caracteres en base 64 (387 o más bytes en binario), dependiendo del tipo de firma.

El $privkey es la base 64 de la concatenación del [Destination](/docs/specs/common-structures#type_Destination) seguido de la [Private Key](/docs/specs/common-structures#type_PrivateKey) seguida de la [Signing Private Key](/docs/specs/common-structures#type_SigningPrivateKey), que son 884 o más caracteres en base 64 (663 o más bytes en binario), dependiendo del tipo de firma.

## Valores RESULT

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

Todas las sesiones pueden incluir [opciones I2CP como longitudes de túnel](/docs/protocol/i2cp#options). Las sesiones STREAM pueden incluir [opciones de la librería Streaming](/docs/api/streaming#options). Consulta esas referencias para nombres de opciones y valores predeterminados.

## Notas sobre Base 64

La codificación Base 64 debe usar el alfabeto Base 64 estándar de I2P "A-Z, a-z, 0-9, -, ~".

## Implementaciones de Bibliotecas de Cliente

Las librerías cliente están disponibles para C, C++, C#, Perl y Python. Estas se encuentran en el directorio apps/sam/ en el Paquete de Código Fuente de I2P.

## Configuración Predeterminada de SAM

El puerto SAM predeterminado es 7656. SAM no está habilitado por defecto en el router I2P; debe iniciarse manualmente, o configurarse para iniciar automáticamente, en la página de configurar clientes en la consola del router, o en el archivo clients.config.
