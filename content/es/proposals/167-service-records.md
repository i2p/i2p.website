---
title: "Registros de Servicio en LS2"
number: "167"
author: "zzz, orignal, eyedeekay"
created: "2024-06-22"
lastupdated: "2025-04-03"
status: "Cerrado"
thread: "http://zzz.i2p/topics/3641"
target: "0.9.66"
toc: true
---

## Estado
Aprobado en la segunda revisión 2025-04-01; las especificaciones están actualizadas; aún no implementado.


## Resumen

I2P carece de un sistema DNS centralizado.
Sin embargo, la libreta de direcciones, junto con el sistema de nombres de host b32, permite
que el router busque destinos completos y obtenga conjuntos de arrendamiento, los cuales contienen
una lista de puertas de enlace y llaves para que los clientes puedan conectarse a ese destino.

Entonces, los conjuntos de arrendamiento son algo así como un registro DNS. Pero actualmente no hay ninguna facilidad para
determinar si ese host admite algún servicio, ya sea en ese destino o en otro diferente,
de una manera similar a los registros DNS SRV [SRV](https://en.wikipedia.org/wiki/SRV_record) [RFC2782](https://datatracker.ietf.org/doc/html/rfc2782).

La primera aplicación para esto podría ser el correo electrónico peer-to-peer.
Otras aplicaciones posibles: DNS, GNS, servidores de claves, autoridades de certificación, servidores de tiempo,
bittorrent, criptomonedas, otras aplicaciones peer-to-peer.


## Propuestas Relacionadas y Alternativas

### Listas de Servicios

La propuesta LS2 123 [Prop123](/en/proposals/123-new-netdb-entries/) definió 'registros de servicio' que indicaban que un destino
participaba en un servicio global. Los floodfills agruparían estos registros
en 'listas de servicios' globales.
Esto nunca se implementó debido a su complejidad, falta de autenticación,
seguridad y preocupaciones por spam.

Esta propuesta es diferente en cuanto a que proporciona búsqueda de un servicio para un destino específico,
no un grupo global de destinos para algún servicio global.

### GNS

GNS [GNS](http://zzz.i2p/topcs/1545) propone que todos ejecuten su propio servidor DNS.
Esta propuesta es complementaria, en cuanto a que podríamos usar registros de servicio para especificar
que GNS (o DNS) es compatible, con un nombre de servicio estándar de "domain" en el puerto 53.

### Dot well-known

En [DOTWELLKNOWN](http://i2pforum.i2p/viewtopic.php?p=3102) se propone que los servicios se busquen mediante una solicitud HTTP a
/.well-known/i2pmail.key. Esto requiere que cada servicio tenga un sitio web relacionado para
alojar la llave. La mayoría de los usuarios no ejecutan sitios web.

Una solución es presuponer que un servicio para una dirección b32 se está ejecutando en esa misma dirección b32. Así que buscar el servicio para example.i2p requiere
la solicitud HTTP de http://example.i2p/.well-known/i2pmail.key, pero
un servicio para aaa...aaa.b32.i2p no requiere esa búsqueda, puede conectarse directamente.

Pero hay una ambigüedad allí, porque example.i2p también puede ser direccionado por su b32.

### Registros MX

Los registros SRV son simplemente una versión genérica de los registros MX para cualquier servicio.
"_smtp._tcp" es el registro "MX".
No hay necesidad de registros MX si tenemos registros SRV, y los registros MX
por sí solos no proporcionan un registro genérico para cualquier servicio.


## Diseño

Los registros de servicio se ubican en la sección de opciones en LS2 [LS2](/en/docs/spec/common-structures/).
La sección de opciones de LS2 está actualmente sin uso.
No es compatible con LS1.
Esto es similar a la propuesta de ancho de banda de túnel [Prop168](/en/proposals/168-tunnel-bandwidth/),
que define opciones para registros de construcción de túneles.

Para buscar una dirección de servicio para un nombre de host o b32 específico, el router obtiene el
conjunto de arrendamiento y busca el registro de servicio en las propiedades.

El servicio puede estar alojado en el mismo destino que el propio LS, o puede referirse
a un nombre de host/b32 diferente.

Si el destino objetivo para el servicio es diferente, el LS objetivo también debe
incluir un registro de servicio, apuntando a sí mismo, indicando que soporta el servicio.

El diseño no requiere soporte especial o almacenamiento en caché ni ningún cambio en los floodfills.
Solo el publicador del conjunto de arrendamiento, y el cliente buscando un registro de servicio,
deben soportar estos cambios.

Se proponen extensiones menores a I2CP y SAM para facilitar la recuperación de
registros de servicio por los clientes.



## Especificación

### Especificación de Opciones LS2

Las opciones de LS2 DEBEN ser ordenadas por clave, por lo que la firma es invariable.

Definido de la siguiente manera:

- serviceoption := optionkey optionvalue
- optionkey := _service._proto
- service := El nombre simbólico del servicio deseado. Debe estar en minúsculas. Ejemplo: "smtp".
  Se permiten caracteres [a-z0-9-] y no debe empezar o terminar con un '-'.
  Los identificadores estándar de [REGISTRY](http://www.dns-sd.org/ServiceTypes.html) o Linux /etc/services deben ser utilizados si están definidos allí.
- proto := El protocolo de transporte del servicio deseado. Debe estar en minúsculas, ya sea "tcp" o "udp".
  "tcp" significa streaming y "udp" significa datagramas replegables.
  Los indicadores de protocolo para datagramas sin procesar y datagram2 pueden definirse más tarde.
  Se permiten caracteres [a-z0-9-] y no debe empezar o terminar con un '-'.
- optionvalue := self | srvrecord[,srvrecord]*
- self := "0" ttl port [appoptions]
- srvrecord := "1" ttl priority weight port target [appoptions]
- ttl := tiempo de vida, segundos enteros. Entero positivo. Ejemplo: "86400".
  Se recomienda un mínimo de 86400 (un día), consulte la sección Recomendaciones a continuación para obtener detalles.
- priority := La prioridad del host objetivo, un valor más bajo significa más preferido. Entero no negativo. Ejemplo: "0"
  Solo es útil si hay más de un registro, pero es obligatorio incluso si solo hay un registro.
- weight := Un peso relativo para registros con la misma prioridad. Un valor más alto significa más probabilidad de ser elegido. Entero no negativo. Ejemplo: "0"
  Solo es útil si hay más de un registro, pero es obligatorio incluso si solo hay un registro.
- port := El puerto I2CP en el que se encontrará el servicio. Entero no negativo. Ejemplo: "25"
  El puerto 0 es compatible pero no recomendado.
- target := El nombre de host o b32 del destino que proporciona el servicio. Un nombre de host válido como en [NAMING](/en/docs/naming/). Debe estar en minúsculas.
  Ejemplo: "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa.b32.i2p" o "example.i2p".
  b32 se recomienda a menos que el nombre de host sea "bien conocido", es decir, en los libros de direcciones oficiales o predeterminados.
- appoptions := texto arbitrario específico para la aplicación, no debe contener " " o ",". La codificación es UTF-8.

### Ejemplos


En LS2 para aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa.b32.i2p, apuntando a un servidor SMTP:

    "_smtp._tcp" "1 86400 0 0 25 bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb.b32.i2p"

En LS2 para aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa.b32.i2p, apuntando a dos servidores SMTP:

    "_smtp._tcp" "1 86400 0 0 25 bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb.b32.i2p,86400 1 0 25 cccccccccccccccccccccccccccccccccccccccccccc.b32.i2p"

En LS2 para bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb.b32.i2p, apuntando a sí mismo como un servidor SMTP:

    "_smtp._tcp" "0 999999 25"

Formato posible para redireccionamiento de correo electrónico (ver abajo):

    "_smtp._tcp" "1 86400 0 0 25 smtp.postman.i2p example@mail.i2p"


### Límites


El formato de estructura de datos Mapping utilizado para las opciones LS2 limita las claves y los valores a un máximo de 255 bytes (no caracteres).
Con un objetivo b32, el optionvalue tiene alrededor de 67 bytes, por lo que solo cabrían 3 registros.
Tal vez solo uno o dos con un campo appoptions largo, o hasta cuatro o cinco con un nombre de host corto.
Esto debería ser suficiente; múltiples registros deberían ser raros.


### Diferencias de [RFC2782](https://datatracker.ietf.org/doc/html/rfc2782)


- Sin puntos finales
- Sin nombre después del proto
- Minúsculas requeridas
- En formato de texto con registros separados por comas, no en formato binario DNS
- Indicadores de tipo de registro diferentes
- Campo adicional appoptions


### Notas


No se permite el uso de comodines como (asterisco), (asterisco)._tcp, o _tcp.
Cada servicio compatible debe tener su propio registro.



### Registro de Nombre de Servicio

Los identificadores no estándar que no están listados en [REGISTRY](http://www.dns-sd.org/ServiceTypes.html) o Linux /etc/services
pueden ser solicitados y añadidos a la especificación de estructuras comunes [LS2](/en/docs/spec/common-structures/).

Los formatos de appoptions específicas de servicio también pueden ser añadidos allí.


### Especificación I2CP

El protocolo [I2CP](/en/docs/spec/i2cp/) debe ser extendido para soportar búsquedas de servicio.
Se requieren códigos de error adicionales de MessageStatusMessage y/o HostReplyMessage relacionados con la búsqueda de servicio.
Para hacer que la facilidad de búsqueda sea general, no solo específica para registros de servicio,
el diseño es para soportar la recuperación de todas las opciones de LS2.

Implementación: Extender HostLookupMessage para añadir solicitudes de
opciones LS2 para hash, nombre de host y destino (tipos de solicitud 2-4).
Extender HostReplyMessage para añadir el mapeo de opciones si se solicita.
Extender HostReplyMessage con códigos de error adicionales.

Los mapeos de opciones pueden ser almacenados o negativamente almacenados en caché por un corto tiempo en el lado del cliente o del router,
dependiendo de la implementación. Se recomienda un tiempo máximo de una hora, a menos que el TTL de registro del servicio sea más corto.
Los registros de servicio pueden ser almacenados en caché hasta el TTL especificado por la aplicación, cliente, o router.

Extender la especificación de la siguiente manera:

### Opciones de configuración

Añadir lo siguiente a [I2CP-OPTIONS]

i2cp.leaseSetOption.nnn

Opciones a ser colocadas en el conjunto de arrendamiento. Solo disponible para LS2.
nnn comienza con 0. El valor de la opción contiene "key=value".
(no incluir comillas)

Ejemplo:

    i2cp.leaseSetOption.0=_smtp._tcp=1 86400 0 0 25 bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb.b32.i2p


### Mensaje de Búsqueda de Host


- Tipo de búsqueda 2: Búsqueda de hash, solicitud de mapeo de opciones
- Tipo de búsqueda 3: Búsqueda de nombre de host, solicitud de mapeo de opciones
- Tipo de búsqueda 4: Búsqueda de destino, solicitud de mapeo de opciones

Para el tipo de búsqueda 4, el ítem 5 es un Destino.



### Mensaje de Respuesta de Host


Para búsquedas de tipos 2-4, el router debe obtener el conjunto de arrendamiento,
incluso si la clave de búsqueda está en la libreta de direcciones.

Si tiene éxito, la respuesta de Host contendrá el Mapeo de opciones
del conjunto de arrendamiento, y lo incluye como ítem 5 después del destino.
Si no hay opciones en el Mapeo, o el conjunto de arrendamiento era versión 1,
aún se incluirá como un Mapeo vacío (dos bytes: 0 0).
Se incluirán todas las opciones del conjunto de arrendamiento, no solo las opciones de registro de servicio.
Por ejemplo, opciones para parámetros definidos en el futuro pueden estar presentes.

En caso de error al buscar el conjunto de arrendamiento, la respuesta contendrá un nuevo código de error 6 (Error al buscar el conjunto de arrendamiento)
y no incluirá un mapeo.
Cuando se devuelve el código de error 6, es posible que el campo de Destino esté presente o no.
Estará presente si una búsqueda de nombre de host en la libreta de direcciones tuvo éxito,
o si una búsqueda anterior tuvo éxito y el resultado fue almacenado en caché,
o si el Destino estaba presente en el mensaje de búsqueda (tipo de búsqueda 4).

Si un tipo de búsqueda no es compatible,
la respuesta contendrá un nuevo código de error 7 (tipo de búsqueda no compatible).



### Especificación SAM

El protocolo [SAMv3](/en/docs/api/samv3/) debe ser extendido para soportar búsquedas de servicio.

Extender NAMING LOOKUP de la siguiente manera:

NAMING LOOKUP NAME=example.i2p OPTIONS=true solicita el mapeo de opciones en la respuesta.

NAME puede ser un destino base64 completo cuando OPTIONS=true.

Si la búsqueda de destino fue exitosa y las opciones estaban presentes en el conjunto de arrendamiento,
entonces en la respuesta, después del destino,
habrá una o más opciones en forma de OPTION:key=value.
Cada opción tendrá un prefijo OPTION: separado.
Se incluirán todas las opciones del conjunto de arrendamiento, no solo las opciones de registro de servicios.
Por ejemplo, opciones para parámetros definidos en el futuro pueden estar presentes.
Ejemplo:

    NAMING REPLY RESULT=OK NAME=example.i2p VALUE=base64dest OPTION:_smtp._tcp="1 86400 0 0 25 bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb.b32.i2p"

Las claves que contienen '=', y las claves o valores que contienen un salto de línea,
se consideran inválidas y el par clave/valor será removido de la respuesta.

Si no se encuentran opciones en el conjunto de arrendamiento, o si el conjunto de arrendamiento era versión 1,
entonces la respuesta no incluirá ninguna opción.

Si OPTIONS=true estaba en la búsqueda, y el conjunto de arrendamiento no se encuentra, se devolverá un nuevo valor de resultado LEASESET_NOT_FOUND.


## Alternativa de Búsqueda de Nombres

Se consideró un diseño alternativo, para soportar búsquedas de servicios
como un nombre de host completo, por ejemplo _smtp._tcp.example.i2p,
al actualizar [NAMING](/en/docs/naming/) para especificar el manejo de nombres de host que comienzan con '_'.
Esto fue rechazado por dos razones:

- Todavía serían necesarios los cambios en I2CP y SAM para pasar información TTL y de puerto al cliente.
- No sería una facilidad general que podría ser utilizada para recuperar otras opciones de LS2
  que podrían ser definidas en el futuro.


## Recomendaciones

Los servidores deben especificar un TTL de al menos 86400, y el puerto estándar para la aplicación.



## Características Avanzadas

### Búsquedas Recursivas

Podría ser deseable soportar búsquedas recursivas, donde cada conjunto de arrendamiento sucesivo
es revisado para encontrar un registro de servicio que apunte a otro conjunto de arrendamiento, al estilo DNS.
Esto probablemente no sea necesario, al menos en una implementación inicial.

TODO



### Campos específicos de la aplicación

Podría ser deseable tener datos específicos de la aplicación en el registro de servicio.
Por ejemplo, el operador de example.i2p podría desear indicar que el correo electrónico debe
ser reenviado a example@mail.i2p. La parte "example@" necesitaría estar en un campo separado
del registro de servicio, o ser eliminada del objetivo.

Incluso si el operador ejecuta su propio servicio de correo, puede desear indicar que
el correo electrónico debe ser enviado a example@example.i2p. La mayoría de los servicios I2P son ejecutados por una sola persona.
Así que un campo separado puede ser útil aquí también.

TODO cómo hacer esto de una manera genérica


### Cambios requeridos para el Correo Electrónico

Fuera del alcance de esta propuesta. Ver [DOTWELLKNOWN](http://i2pforum.i2p/viewtopic.php?p=3102) para una discusión.


## Notas de Implementación

El almacenamiento en caché de los registros de servicio hasta el TTL puede ser realizado por el router o la aplicación,
dependiendo de la implementación. Si se debe almacenar en caché de manera persistente también depende de la implementación.

Las búsquedas también deben obtener el conjunto de arrendamiento objetivo y verificar que contenga un registro "self"
antes de devolver el destino objetivo al cliente.


## Análisis de Seguridad

Dado que el conjunto de arrendamiento está firmado, cualquier registro de servicio dentro de él es autenticado por la llave de firma del destino.

Los registros de servicio son públicos y visibles para los floodfills, a menos que el conjunto de arrendamiento esté cifrado.
Cualquier router que solicite el conjunto de arrendamiento podrá ver los registros de servicio.

Un registro SRV que no sea "self" (es decir, uno que apunte a un objetivo de nombre de host/b32 diferente)
no requiere el consentimiento del nombre de host/b32 objetivo.
No está claro si una redirección de un servicio a un destino arbitrario podría facilitar algún
tipo de ataque, o cuál sería el propósito de tal ataque.
Sin embargo, esta propuesta mitiga tal ataque requiriendo que el objetivo
también publique un registro SRV "self". Los implementadores deben verificar un registro "self"
en el conjunto de arrendamiento del objetivo.


## Compatibilidad

LS2: No hay problemas. Todas las implementaciones conocidas actualmente ignoran el campo de opciones en LS2,
y omiten correctamente un campo de opciones no vacío.
Esto fue verificado durante la prueba tanto por Java I2P como por i2pd durante el desarrollo de LS2.
LS2 se implementó en 0.9.38 en 2016 y es bien soportado por todas las implementaciones de routers.
El diseño no requiere soporte especial o almacenamiento en caché ni ningún cambio en los floodfills.

Naming: '_' no es un carácter válido en los nombres de host de i2p.

I2CP: Los tipos de búsqueda 2-4 no deben ser enviados a routers por debajo de la versión mínima de API
en la que es compatible (TBD).

SAM: El servidor Java SAM ignora claves/valores adicionales como OPTIONS=true.
i2pd debería hacerlo también, a ser verificado.
Los clientes de SAM no obtendrán los valores adicionales en la respuesta a menos que se solicite con OPTIONS=true.
No debería ser necesario un aumento de versión.


