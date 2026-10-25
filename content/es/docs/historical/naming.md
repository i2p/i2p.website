---
title: "Discusión sobre Nomenclatura"
description: "Debate histórico sobre el modelo de nomenclatura de I2P y por qué se rechazaron los esquemas globales estilo DNS"
slug: "naming"
aliases:
  - "/es/docs/legacy/naming"
  - "/es/docs/legacy/naming/"
  - "/es/naming_discussion"
  - "/es/naming_discussion/"
lastUpdated: "2025-02"
accurateFor: "historical"
---

NOTA: Lo siguiente es una discusión de las razones detrás del sistema de nomenclatura de I2P, argumentos comunes y posibles alternativas. Consulte [la página de nomenclatura](/docs/naming) para la documentación actual.

## Alternativas Descartadas

El nombrado dentro de I2P ha sido un tema muy debatido desde el principio, con defensores en todo el espectro de posibilidades. Sin embargo, dada la demanda inherente de I2P de comunicación segura y operación descentralizada, el sistema de nombrado tradicional al estilo DNS está claramente descartado, al igual que los sistemas de votación de "mayoría gana".

I2P no promueve el uso de servicios similares a DNS, ya que el daño causado por el secuestro de un sitio puede ser tremendo - y los destinos inseguros no tienen valor. DNSsec en sí mismo aún depende de registradores y autoridades de certificación, mientras que con I2P, las solicitudes enviadas a un destino no pueden ser interceptadas o la respuesta falsificada, ya que están cifradas con las claves públicas del destino, y un destino en sí mismo es solo un par de claves públicas y un certificado. Los sistemas tipo DNS, por otro lado, permiten que cualquiera de los servidores de nombres en la ruta de búsqueda monte ataques simples de denegación de servicio y suplantación. Agregar un certificado que autentique las respuestas como firmadas por alguna autoridad de certificación centralizada abordaría muchos de los problemas de servidores de nombres hostiles, pero dejaría abiertos los ataques de reproducción así como los ataques de autoridades de certificación hostiles.

El estilo de nomenclatura por votación también es peligroso, especialmente dada la efectividad de los ataques Sybil en sistemas anónimos - el atacante puede simplemente crear un número arbitrariamente alto de pares y "votar" con cada uno para apoderarse de un nombre dado. Los métodos de proof-of-work pueden usarse para hacer que la identidad no sea gratuita, pero a medida que la red crece, la carga requerida para contactar a todos para realizar votaciones en línea es implausible, o si no se consulta toda la red, pueden alcanzarse diferentes conjuntos de respuestas.

Sin embargo, al igual que con Internet, I2P mantiene el diseño y funcionamiento de un sistema de nombres fuera de la capa de comunicación (similar a IP). La biblioteca de nombres incluida incorpora una interfaz simple de proveedor de servicios en la que [sistemas de nombres alternativos](#alternatives) pueden conectarse, permitiendo a los usuarios finales decidir qué tipo de compensaciones de nombres prefieren.

## Discusión

Ver también [Names: Decentralized, Secure, Human-Meaningful: Choose Two](https://zooko.com/distnames.html).

### Comentarios de jrandom

(adaptado de una publicación en el antiguo Syndie, 26 de noviembre de 2005)

P: ¿Qué hacer si algunos hosts no se ponen de acuerdo en una dirección y si algunas direcciones funcionan pero otras no? ¿Quién es la fuente correcta de un nombre?

R: No lo haces. Esta es en realidad una diferencia crítica entre los nombres en I2P y cómo funciona DNS - los nombres en I2P son legibles para humanos, seguros, pero **no son globalmente únicos**. Esto es por diseño, y una parte inherente de nuestra necesidad de seguridad.

Si de alguna manera pudiera convencerte de cambiar el destino asociado con algún nombre, habría logrado "tomar el control" del sitio, y bajo ninguna circunstancia eso es aceptable. En su lugar, lo que hacemos es hacer que los nombres sean **únicos localmente**: son lo que *tú* usas para llamar a un sitio, tal como puedes llamar a las cosas como quieras cuando las agregas a los marcadores de tu navegador, o a la lista de contactos de tu cliente de mensajería instantánea. A quien tú llamas "Jefe" puede ser a quien alguien más llama "Sally".

Los nombres nunca serán, jamás, legibles por humanos de forma segura y globalmente únicos.

### Comentarios de zzz

Lo siguiente de zzz es una revisión de varias quejas comunes sobre el sistema de nombres de I2P.

- **Ineficiencia:** Se descarga todo el archivo hosts.txt (si ha cambiado, ya que eepget usa las cabeceras etag y last-modified). Actualmente son aproximadamente 400K para casi 800 hosts.

Cierto, pero esto no es mucho tráfico en el contexto de I2P, que en sí mismo es tremendamente ineficiente (bases de datos floodfill, enormes gastos generales de cifrado y relleno, garlic routing, etc.). Si descargaras un archivo hosts.txt de alguien cada 12 horas, el promedio sería de aproximadamente 10 bytes/segundo.

Como suele ser el caso en I2P, aquí existe un compromiso fundamental entre anonimato y eficiencia. Algunos dirían que usar las cabeceras etag y last-modified es peligroso porque expone cuándo solicitaste los datos por última vez. Otros han sugerido solicitar solo claves específicas (similar a lo que hacen los servicios jump, pero de manera más automatizada), posiblemente a un costo adicional en el anonimato.

Las posibles mejoras serían un reemplazo o complemento para el address book (ver i2host.i2p), o algo simple como suscribirse a http://example.i2p/cgi-bin/recenthosts.cgi en lugar de http://example.i2p/hosts.txt. Si un hipotético recenthosts.cgi distribuyera todos los hosts de las últimas 24 horas, por ejemplo, eso podría ser tanto más eficiente como más anónimo que el actual hosts.txt con last-modified y etag.

Una implementación de ejemplo está en stats.i2p en http://stats.i2p/cgi-bin/newhosts.txt. Este script devuelve un Etag con una marca de tiempo. Cuando llega una solicitud con el etag If-None-Match, el script SOLO devuelve hosts nuevos desde esa marca de tiempo, o 304 Not Modified si no los hay. De esta manera, el script devuelve eficientemente solo los hosts que el suscriptor no conoce, de una manera compatible con la libreta de direcciones.

Por lo tanto, la ineficiencia no es un problema grave y hay varias formas de mejorar las cosas sin cambios radicales.

- **No Escalable:** El archivo hosts.txt de 400K (con búsqueda lineal) no es tan grande en este momento y probablemente podamos crecer 10x o 100x antes de que sea un problema.

En cuanto al tráfico de red, ver arriba. Pero a menos que vayas a hacer una consulta lenta en tiempo real a través de la red para una clave, necesitas tener todo el conjunto de claves almacenado localmente, a un costo de aproximadamente 500 bytes por clave.

- **Requiere configuración y "confianza":** La libreta de direcciones predeterminada solo está suscrita a http://www.i2p2.i2p/hosts.txt, que rara vez se actualiza, lo que lleva a una experiencia deficiente para nuevos usuarios.

Esto es muy intencional. jrandom quiere que un usuario "confíe" en un proveedor de hosts.txt, y como le gusta decir, "la confianza no es un booleano". El paso de configuración intenta obligar a los usuarios a pensar sobre las cuestiones de confianza en una red anónima.

Como otro ejemplo, la página de error "I2P Site Unknown" en el HTTP Proxy enumera algunos servicios de salto, pero no "recomienda" ninguno en particular, y depende del usuario elegir uno (o no hacerlo). jrandom diría que confiamos en los proveedores listados lo suficiente como para incluirlos en la lista, pero no lo suficiente como para obtener automáticamente la clave de ellos.

Qué tan exitoso es esto, no estoy seguro. Pero debe haber algún tipo de jerarquía de confianza para el sistema de nombres. Tratar a todos por igual puede aumentar el riesgo de secuestro.

- **No es DNS**

Desafortunadamente, las búsquedas en tiempo real a través de I2P ralentizarían significativamente la navegación web.

Además, DNS se basa en consultas con caché limitado y tiempo de vida, mientras que las claves I2P son permanentes.

Claro, podríamos hacer que funcione, pero ¿por qué? No es una buena opción.

- **No es confiable:** Depende de servidores específicos para las suscripciones de libreta de direcciones.

Sí, depende de algunos servidores que hayas configurado. Dentro de I2P, los servidores y servicios aparecen y desaparecen. Cualquier otro sistema centralizado (por ejemplo, los servidores DNS raíz) tendría el mismo problema. Un sistema completamente descentralizado (donde todos son autoritativos) es posible implementando una solución donde "todos son un servidor DNS raíz", o mediante algo aún más simple, como un script que añada a todos en tu hosts.txt a tu libreta de direcciones.

Las personas que abogan por soluciones completamente autoritativas generalmente no han reflexionado sobre los problemas de conflictos y secuestro, sin embargo.

- **Incómodo, no en tiempo real:** Es un mosaico de proveedores de hosts.txt, proveedores de formularios web para agregar claves, proveedores de servicios de salto, reportadores de estado de sitios I2P. Los servidores de salto y las suscripciones son problemáticos, debería funcionar como DNS.

Consulte las secciones de confiabilidad y confianza.

Entonces, en resumen, el sistema actual no está terriblemente roto, no es ineficiente ni poco escalable, y las propuestas de "simplemente usar DNS" no están bien pensadas.

## Alternativas

El código fuente de I2P contiene varios sistemas de nombres conectables y admite opciones de configuración para permitir la experimentación con sistemas de nombres.

- **Meta** - llama a dos o más sistemas de nombres en orden. Por defecto, llama a PetName y luego a HostsTxt.
- **PetName** - Busca en un archivo petnames.txt. El formato de este archivo NO es el mismo que hosts.txt.
- **HostsTxt** - Busca en los siguientes archivos, en orden:
  1. privatehosts.txt
  2. userhosts.txt
  3. hosts.txt
- **AddressDB** - Cada host se lista en un archivo separado en un directorio addressDb/.
- **Eepget** - realiza una solicitud de búsqueda HTTP desde un servidor externo - debe apilarse después de la búsqueda HostsTxt con Meta. Esto podría aumentar o reemplazar el sistema de salto. Incluye caché en memoria.
- **Exec** - llama a un programa externo para la búsqueda, permite experimentación adicional en esquemas de búsqueda, independiente de java. Puede usarse después de HostsTxt o como el único sistema de nombres. Incluye caché en memoria.
- **Dummy** - usado como respaldo para nombres Base64, de lo contrario falla.

El sistema de nomenclatura actual se puede cambiar con la opción de configuración avanzada `i2p.naming.impl` (requiere reinicio). Consulta `core/java/src/net/i2p/client/naming` para más detalles.

Cualquier sistema nuevo debe estar apilado con HostsTxt, o debe implementar almacenamiento local y/o las funciones de suscripción de la libreta de direcciones, ya que la libreta de direcciones solo conoce los archivos y formato hosts.txt.

## Certificados

Los destinos I2P contienen un certificado, sin embargo en este momento ese certificado siempre es nulo. Con un certificado nulo, los destinos en base64 siempre tienen 516 bytes terminando en "AAAA", y esto se verifica en el mecanismo de fusión del libro de direcciones, y posiblemente en otros lugares. Además, no hay ningún método disponible para generar un certificado o añadirlo a un destino. Por lo tanto, estos tendrán que ser actualizados para implementar certificados.

Un posible uso de los certificados es para [prueba de trabajo](/get-involved/todo#hashcash).

Otra es para que los "subdominios" (entre comillas porque realmente no existe tal cosa, I2P usa un sistema de nombres plano) sean firmados por las claves del dominio de segundo nivel.

Con cualquier implementación de certificados debe venir el método para verificar los certificados. Presumiblemente esto sucedería en el código de fusión de la libreta de direcciones. ¿Existe un método para múltiples tipos de certificados, o múltiples certificados?

Agregar un certificado que autentique las respuestas como firmadas por alguna autoridad de certificación centralizada abordaría muchos de los problemas de servidores de nombres hostiles, pero dejaría abiertos los ataques de repetición así como los ataques de autoridades de certificación hostiles.
