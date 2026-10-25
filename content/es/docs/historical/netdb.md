---
title: "Discusión sobre la Base de Datos de Red"
description: "Notas históricas sobre floodfill, experimentos con Kademlia, y ajustes futuros para la netDb"
slug: "netdb"
aliases:
  - "/es/docs/legacy/netdb"
  - "/es/docs/legacy/netdb/"
  - "/es/netdb_discussion"
  - "/es/netdb_discussion/"
lastUpdated: "2008-03"
accurateFor: "0.7"
---

NOTA: Lo siguiente es una discusión sobre la historia de la implementación de netdb y no es información actual. Consulte [la página principal de netdb](/docs/overview/network-database) para la documentación actual.

## Historial {#status}

La netDb se distribuye con una técnica simple llamada "floodfill". Hace mucho tiempo, la netDb también usaba el DHT Kademlia como algoritmo de respaldo. Sin embargo, no funcionó bien en nuestra aplicación, y fue completamente deshabilitado en la versión 0.6.1.20.

*(Adaptado de una publicación de jrandom en el antiguo Syndie, 26 de noviembre de 2005)*

El floodfill netDb es realmente solo una medida simple y quizás temporal, usando el algoritmo más simple posible - enviar los datos a un peer en el floodfill netDb, esperar 10 segundos, elegir un peer aleatorio en el netDb y pedirle la entrada que se envió, verificando su inserción/distribución apropiada. Si el peer de verificación no responde, o no tiene la entrada, el remitente repite el proceso. Cuando el peer en el floodfill netDb recibe un almacén netDb de un peer que no está en el floodfill netDb, lo envía a todos los peers en el floodfill netDb.

En un momento, la funcionalidad de búsqueda/almacenamiento de Kademlia aún estaba en funcionamiento. Los peers consideraban a los peers floodfill como siempre "más cercanos" a cada clave que cualquier peer que no participara en la netDb. Recurríamos a la netDb de Kademlia si los peers floodfill fallaban por alguna razón u otra. Sin embargo, Kademlia fue luego deshabilitado completamente (ver más abajo).

Más recientemente, Kademlia fue parcialmente reintroducido a finales de 2009, como una forma de limitar el tamaño de la netDb que cada router floodfill debe almacenar.

### La Introducción del Algoritmo Floodfill

Floodfill fue introducido en la versión 0.6.0.4, manteniendo Kademlia como algoritmo de respaldo.

*(Adaptado de publicaciones de jrandom en el antiguo Syndie, 26 de noviembre de 2005)*

Como he dicho a menudo, no estoy particularmente atado a ninguna tecnología específica - lo que me importa es lo que dará resultados. Mientras he estado trabajando con varias ideas de netDb durante los últimos años, los problemas que hemos enfrentado en las últimas semanas han llevado algunos de ellos a un punto crítico. En la red en vivo, con el factor de redundancia del netDb establecido en 4 peers (lo que significa que seguimos enviando una entrada a nuevos peers hasta que 4 de ellos confirmen que la han recibido) y el timeout por peer establecido en 4 veces el tiempo promedio de respuesta de ese peer, **todavía** estamos obteniendo un promedio de 40-60 peers enviados antes de que 4 confirmen el almacenamiento. Eso significa enviar 36-56 veces más mensajes de los que deberían salir, cada uno usando tunnels y por lo tanto cruzando 2-4 enlaces. Aún más, ese valor está muy sesgado, ya que el número promedio de peers enviados en un almacenamiento 'fallido' (lo que significa que menos de 4 personas confirmaron el mensaje después de 60 segundos de enviar mensajes) estaba en el rango de 130-160 peers.

Esto es una locura, especialmente para una red con solo unos 250 peers en ella.

La respuesta más simple sería decir "bueno, obvio jrandom, está roto. arréglalo", pero eso no llega realmente al núcleo del problema. En línea con otro esfuerzo actual, es probable que tengamos un número sustancial de problemas de red debido a rutas restringidas - peers que no pueden comunicarse con otros peers, a menudo debido a problemas de NAT o firewall. Si, digamos, los K peers más cercanos a una entrada particular de netDb están detrás de una 'ruta restringida' tal que el mensaje de almacenamiento de netDb podría alcanzarlos pero el mensaje de búsqueda de netDb de algún otro peer no podría, esa entrada sería esencialmente inalcanzable. Siguiendo un poco más esas líneas y tomando en consideración el hecho de que algunas rutas restringidas serán creadas con intención hostil, es claro que vamos a tener que examinar más de cerca una solución netDb a largo plazo.

Hay algunas alternativas, pero vale la pena mencionar dos en particular. La primera es simplemente ejecutar el netDb como un DHT Kademlia usando un subconjunto de la red completa, donde todos esos peers son accesibles externamente. Los peers que no participan en el netDb aún consultan a esos peers pero no reciben mensajes netDb store o lookup no solicitados. La participación en el netDb sería tanto de auto-selección como de eliminación por el usuario - los routers elegirían si publicar una bandera en su routerInfo indicando si quieren participar, mientras que cada router elige qué peers quiere tratar como parte del netDb (los peers que publican esa bandera pero que nunca proporcionan datos útiles serían ignorados, esencialmente eliminándolos del netDb).

Otra alternativa es un regreso al pasado, volviendo a la mentalidad DTSTTCPW (Do The Simplest Thing That Could Possibly Work, "Haz la cosa más simple que posiblemente pueda funcionar") - un floodfill netDb, pero como la alternativa anterior, usando solo un subconjunto de la red completa. Cuando un usuario quiere publicar una entrada en el floodfill netDb, simplemente la envía a uno de los routers participantes, espera un ACK, y luego 30 segundos después, consulta otro participante aleatorio en el floodfill netDb para verificar que se distribuyó correctamente. Si fue así, genial, y si no, simplemente repite el proceso. Cuando un floodfill router recibe un netDb store, responde con ACK inmediatamente y pone en cola el netDb store para todos sus peers netDb conocidos. Cuando un floodfill router recibe un netDb lookup, si tienen los datos, responden con ellos, pero si no los tienen, responden con los hashes de, digamos, otros 20 peers en el floodfill netDb.

Desde una perspectiva de economía de red, el floodfill netDb es bastante similar al netDb de difusión original, excepto que el costo de publicar una entrada es asumido principalmente por los pares en el netDb, en lugar de por el publicador. Desarrollando esto un poco más y tratando el netDb como una caja negra, podemos ver que el ancho de banda total requerido por el netDb es:

```
recvKBps = N * (L + 1) * (1 + F) * (1 + R) * S / T
```
donde:

```
N = number of routers in the entire network
L = average number of client destinations on each router
    (+1 for the routerInfo)
F = tunnel failure percentage
R = tunnel rebuild period, as a fraction of the tunnel lifetime
S = average netDb entry size
T = tunnel lifetime
```
Sustituyendo algunos valores:

```
recvKBps = 1000 * (5 + 1) * (1 + 0.05) * (1 + 0.2) * 2KB / 10m
         = 25.2KBps
```
Eso, a su vez, escala linealmente con N (con 100,000 pares, la netDb debe ser capaz de manejar mensajes de almacenamiento de netDb que suman 2.5MBps, o, con 300 pares, 7.6KBps).

Mientras que el floodfill netDb haría que cada participante del netDb reciba solo una pequeña fracción de las stores del netDb generadas por el cliente directamente, todos recibirían todas las entradas eventualmente, por lo que todos sus enlaces deberían ser capaces de manejar el recvKBps completo. A su vez, todos necesitarán enviar `(recvKBps/sizeof(netDb)) * (sizeof(netDb)-1)` para mantener sincronizados a los otros peers.

Un floodfill netDb no requeriría ni enrutamiento de túneles para la operación del netDb ni ninguna selección especial sobre qué entradas puede responder de forma 'segura', ya que la suposición básica es que todos están almacenando todo. Ah, y con respecto al uso de disco del netDb requerido, sigue siendo bastante trivial para cualquier máquina moderna, requiriendo alrededor de 11MB por cada 1000 peers `(N * (L + 1) * S)`.

La netDb Kademlia reduciría estos números, idealmente llevándolos a K sobre M veces su valor, con K = el factor de redundancia y M siendo el número de routers en la netDb (por ejemplo, 5/100, dando un recvKBps de 126KBps y 536MB con 100,000 routers). Sin embargo, la desventaja de la netDb Kademlia es la mayor complejidad de operación segura en un entorno hostil.

Lo que estoy pensando ahora es simplemente implementar y desplegar una floodfill netDb en nuestra red en vivo existente, permitiendo que los peers que quieran usarla seleccionen otros peers que estén marcados como miembros y los consulten en lugar de consultar los peers tradicionales de la Kademlia netDb. Los requisitos de ancho de banda y disco en esta etapa son lo suficientemente triviales (7.6KBps y 3MB de espacio en disco) y eliminará completamente la netDb del plan de depuración - los problemas que queden por abordar serán causados por algo no relacionado con la netDb.

¿Cómo se elegirían los peers para publicar esa bandera diciendo que son parte del floodfill netDb? Al principio, podría hacerse manualmente como una opción de configuración avanzada (ignorada si el router no puede verificar su alcanzabilidad externa). Si demasiados peers establecen esa bandera, ¿cómo eligen los participantes del netDb cuáles expulsar? De nuevo, al principio podría hacerse manualmente como una opción de configuración avanzada (después de descartar peers que son inalcanzables). ¿Cómo evitamos la partición del netDb? Haciendo que los routers verifiquen que el netDb está realizando el flood fill correctamente consultando K peers del netDb aleatorios. ¿Cómo descubren nuevos routers para hacer túneles los routers que no participan en el netDb? Quizás esto podría hacerse enviando una consulta particular del netDb para que el router del netDb respondiera no con peers en el netDb, sino con peers aleatorios fuera del netDb.

La netDb de I2P es muy diferente de las DHT tradicionales que soportan carga - solo transporta metadatos de red, no ninguna carga útil real, razón por la cual incluso una netDb que use un algoritmo floodfill será capaz de sostener una cantidad arbitraria de datos de sitios I2P/IRC/bt/correo/syndie/etc. Incluso podemos hacer algunas optimizaciones a medida que I2P crezca para distribuir esa carga un poco más (tal vez pasando filtros bloom entre los participantes de la netDb para ver qué necesitan compartir), pero parece que por ahora podemos arreglárnoslas con una solución mucho más simple.

Un dato que vale la pena explorar a fondo es que no todos los leaseSets necesitan ser publicados en la netDb. De hecho, la mayoría no necesita serlo - solo aquellos para destinos que van a recibir mensajes no solicitados (es decir, servidores). Esto se debe a que los mensajes envueltos con garlic encryption enviados de un destino a otro ya incluyen el leaseSet del remitente, por lo que cualquier envío/recepción posterior entre esos dos destinos (dentro de un período corto de tiempo) funciona sin ninguna actividad de la netDb.

Entonces, volviendo a esas ecuaciones, podemos cambiar L de 5 a algo como 0.1 (asumiendo que solo 1 de cada 50 destinos es un servidor). Las ecuaciones anteriores también pasaron por alto la carga de red requerida para responder consultas de los clientes, pero aunque esto es muy variable (basado en la actividad del usuario), también es muy probable que sea bastante insignificante comparado con la frecuencia de publicación.

En cualquier caso, todavía no hay magia, pero una buena reducción de casi 1/5 del ancho de banda/espacio en disco requerido (tal vez más adelante, dependiendo de si la distribución de routerInfo va directamente como parte del establecimiento de pares o solo a través del netDb).

### La Desactivación del Algoritmo Kademlia

Kademlia fue completamente deshabilitado en la versión 0.6.1.20.

*(Adaptado de una conversación de IRC con jrandom 11/07)*

Kademlia requiere un nivel mínimo de servicio que la línea base no podría ofrecer (ancho de banda, CPU), incluso después de añadir niveles (kad puro es absurdo en ese punto). Kademlia simplemente no funcionaría. Era una buena idea, pero no para un entorno hostil y fluido.

### Estado Actual

La netDb desempeña un papel muy específico en la red I2P, y los algoritmos han sido ajustados hacia nuestras necesidades. Esto también significa que no ha sido ajustada para abordar las necesidades que aún no hemos encontrado. I2P es actualmente bastante pequeña (unos pocos cientos de routers). Hubo algunos cálculos que indicaban que 3-5 routers floodfill deberían ser capaces de manejar 10,000 nodos en la red. La implementación de netDb satisface más que adecuadamente nuestras necesidades en este momento, pero es probable que haya más ajustes y corrección de errores a medida que la red crezca.

### Actualización de Cálculos 03-2008

Números actuales:

```
recvKBps = N * (L + 1) * (1 + F) * (1 + R) * S / T
```
donde:

```
N = number of routers in the entire network
L = average number of client destinations on each router
    (+1 for the routerInfo)
F = tunnel failure percentage
R = tunnel rebuild period, as a fraction of the tunnel lifetime
S = average netDb entry size
T = tunnel lifetime
```
Cambios en las suposiciones:

- L ahora es aproximadamente .5, comparado con .1 anterior, debido a la popularidad de i2psnark
  y otras aplicaciones.
- F es aproximadamente .33, pero los errores en las pruebas de tunnel están corregidos en 0.6.1.33, así que mejorará mucho.
- Dado que netDb es aproximadamente 2/3 routerInfos de 5K y 1/3 leaseSets de 2K, S = 4K.
  El tamaño de RouterInfo se está reduciendo en 0.6.1.32 y 0.6.1.33 mientras eliminamos estadísticas innecesarias.
- R = período de construcción de tunnel: 0.2 era muy bajo - tal vez era 0.7 -
  pero las mejoras del algoritmo de construcción en 0.6.1.32 deberían reducirlo a aproximadamente 0.2
  conforme la red se actualice. Digamos 0.5 ahora con la mitad de la red en .30 o anterior.

```
recvKBps = 700 * (0.5 + 1) * (1 + 0.33) * (1 + 0.5) * 4KB / 10m
         ~= 28KBps
```
Esto solo tiene en cuenta los almacenes - ¿qué pasa con las consultas?

### ¿El Regreso del Algoritmo Kademlia?

*(Adaptado de la reunión de I2P del 2 de enero de 2007)*

La netDb de Kademlia simplemente no funcionaba correctamente. ¿Está muerta para siempre o volverá? Si regresa, los pares en la netDb de Kademlia serían un subconjunto muy limitado de los routers en la red (básicamente un número ampliado de pares floodfill, si/cuando los pares floodfill no puedan manejar la carga). Pero hasta que los pares floodfill no puedan manejar la carga (y no se puedan agregar otros pares que sí puedan), es innecesario.

### El Futuro de Floodfill

*(Adaptado de una conversación de IRC con jrandom 11/07)*

Aquí hay una propuesta: La clase de capacidad O es automáticamente floodfill. Hmm. A menos que estemos seguros, podríamos terminar con una forma elegante de hacer DDoS a todos los routers de clase O. Este es precisamente el caso: queremos asegurarnos de que el número de floodfill sea lo más pequeño posible mientras proporcionamos suficiente alcanzabilidad. Si/cuando las solicitudes de netDb fallan, entonces necesitamos aumentar el número de peers floodfill, pero en este momento, no tengo conocimiento de un problema de obtención de netDb. Hay 33 peers de clase "O" según mis registros. 33 es /mucho/ para hacer floodfill.

Entonces floodfill funciona mejor cuando el número de pares en ese grupo está firmemente limitado? Y el tamaño del grupo floodfill no debería crecer mucho, incluso si la red en sí gradualmente lo haría? 3-5 pares floodfill pueden manejar 10K routers si mal no recuerdo (publiqué un montón de números sobre eso explicando los detalles en el viejo syndie). Suena como un requisito difícil de cumplir con opt-in automático, especialmente si los nodos que optan por participar no pueden confiar en datos de otros. ej. "veamos si estoy entre los 5 primeros", y solo pueden confiar en datos sobre sí mismos (ej. "definitivamente soy clase O, y moviendo 150 KB/s, y activo por 123 días"). Y los 5 primeros también es hostil. Básicamente, es lo mismo que los servidores de directorio de tor - elegidos por gente de confianza (también conocidos como desarrolladores). Sí, ahora mismo podría ser explotado por opt-in, pero eso sería trivial de detectar y tratar. Parece que al final, podríamos necesitar algo más útil que Kademlia, y tener solo pares razonablemente capaces unirse a ese esquema. Clase N y superior debería ser una cantidad lo suficientemente grande para suprimir el riesgo de que un adversario cause denegación de servicio, esperaría. Pero tendría que ser diferente de floodfill entonces, en el sentido de que no causaría tráfico descomunal. Cantidad grande? Para un netDb basado en DHT? No necesariamente basado en DHT.

### Lista de tareas pendientes de Floodfill {#todo}

NOTA: La siguiente información no está actualizada. Consulte [la página principal de netdb](/docs/overview/network-database) para el estado actual y una lista de trabajo futuro.

La red estuvo reducida a solo un floodfill durante un par de horas el 13 de marzo de 2008 (aproximadamente 18:00 - 20:00 UTC), y causó muchos problemas.

Dos cambios implementados en 0.6.1.33 deberían reducir la interrupción causada por la eliminación o rotación de peers floodfill:

1. Aleatorizar los peers floodfill utilizados para la búsqueda cada vez.
   Esto te permitirá eventualmente sobrepasar los que están fallando.
   Este cambio también solucionó un error desagradable que a veces volvía loco al código de búsqueda ff.
2. Preferir los peers floodfill que están activos.
   El código ahora evita peers que están en lista negra, fallando, o de los que no se ha tenido noticias en
   media hora, si es posible.

Un beneficio es el contacto inicial más rápido con un sitio I2P (es decir, cuando tienes que obtener primero el leaseset). El tiempo de espera de búsqueda es de 10 segundos, por lo que si no empiezas preguntando a un par que esté caído, puedes ahorrar 10 segundos.

*Puede* haber implicaciones de anonimato en estos cambios. Por ejemplo, en el código **store** del floodfill, hay comentarios que indican que los peers en la lista negra no se evitan, ya que un peer podría ser "malo" y luego ver qué sucede. Las búsquedas son mucho menos vulnerables que los almacenamientos - son mucho menos frecuentes y revelan menos información. ¿Entonces tal vez no creemos que necesitemos preocuparnos por ello? Pero si queremos ajustar los cambios, sería fácil enviar a un peer listado como "caído" o en la lista negra de todos modos, simplemente no contarlo como parte de los 2 a los que estamos enviando (ya que realmente no esperamos una respuesta).

Hay varios lugares donde se selecciona un peer floodfill - esta corrección aborda solo uno - desde quién busca un peer regular [2 a la vez]. Otros lugares donde debería implementarse una mejor selección de floodfill:

1. A quién almacena un peer regular [1 a la vez]
   (aleatorio - necesita agregar calificación, porque los timeouts son largos)
2. A quién busca un peer regular para verificar un almacenamiento [1 a la vez]
   (aleatorio - necesita agregar calificación, porque los timeouts son largos)
3. A quién envía un floodfill peer en respuesta a una búsqueda fallida (los 3 más cercanos a la búsqueda)
4. A quién hace flood un floodfill peer (todos los otros floodfill peers)
5. La lista de floodfill peers enviada en el "susurro" NTCP cada 6 horas
   (aunque esto puede que ya no sea necesario debido a otras mejoras de floodfill)

Hay mucho más que se podría y debería hacer:

- Usar las estadísticas "dbHistory" para evaluar mejor la integración de un peer floodfill
- Usar las estadísticas "dbHistory" para reaccionar inmediatamente a peers floodfill que no responden
- Ser más inteligente con los reintentos - los reintentos son manejados por una capa superior, no en
  FloodOnlySearchJob, por lo que hace otro ordenamiento aleatorio e intenta de nuevo,
  en lugar de omitir intencionalmente los peers ff que acabamos de intentar.
- Mejorar más las estadísticas de integración
- Realmente usar estadísticas de integración en lugar de solo la indicación floodfill en netDb
- ¿Usar también estadísticas de latencia?
- Más mejoras en el reconocimiento de peers floodfill que fallan

Completado recientemente:

- [En la versión 0.6.3]
  Implementar la adhesión automática
  a floodfill para cierto porcentaje de peers de clase O, basado en el análisis de la red.
- [En la versión 0.6.3]
  Continuar reduciendo el tamaño de las entradas de netDb para reducir el tráfico de floodfill -
  ahora estamos en el número mínimo de estadísticas requeridas para monitorear la red.
- [En la versión 0.6.3]
  Lista manual de peers floodfill para excluir
  ([listas de bloqueo](/docs/overview/threat-model#blocklist) por identidad de router)
- [En la versión 0.6.3]
  Mejor selección de peers floodfill para almacenamientos:
  Evitar peers cuyo netDb es antiguo, o tienen un almacenamiento fallido reciente,
  o están en la lista negra permanentemente.
- [En la versión 0.6.4]
  Preferir peers floodfill ya conectados para almacenamientos de RouterInfo, para
  reducir el número de conexiones directas a peers floodfill.
- [En la versión 0.6.5]
  Los peers que ya no son floodfill envían su routerInfo en respuesta
  a una consulta, para que el router que hace la consulta sepa que
  ya no es floodfill.
- [En la versión 0.6.5]
  Ajuste adicional de los requisitos para convertirse automáticamente en floodfill
- [En la versión 0.6.5]
  Corregir el perfilado de tiempo de respuesta en preparación para favorecer floodfills rápidos
- [En la versión 0.6.5]
  Mejorar las listas de bloqueo
- [En la versión 0.7]
  Corregir la exploración de netDb
- [En la versión 0.7]
  Activar las listas de bloqueo por defecto, bloquear a los problemáticos conocidos
- [Varias mejoras en versiones recientes, un esfuerzo continuo]
  Reducir las demandas de recursos en routers de alto ancho de banda y floodfill

Es una lista larga, pero se necesitará tanto trabajo para tener una red que sea resistente a ataques DOS de muchos peers activando y desactivando el interruptor floodfill. O fingiendo ser un router floodfill. Nada de esto era un problema cuando solo teníamos dos routers ff, y ambos estaban funcionando 24/7. De nuevo, la ausencia de jrandom nos ha señalado lugares que necesitan mejoras.

Para ayudar en este esfuerzo, ahora se muestran datos de perfil adicionales para los peers floodfill (a partir de la versión 0.6.1.33) en la página "Perfiles" en la consola del router. Usaremos esto para analizar qué datos son apropiados para calificar a los peers floodfill.

La red es actualmente bastante resiliente, sin embargo continuaremos mejorando nuestros algoritmos para medir y reaccionar al rendimiento y confiabilidad de los peers floodfill. Aunque no estamos, en este momento, completamente protegidos contra las amenazas potenciales de floodfills maliciosos o un DDOS de floodfill, la mayor parte de la infraestructura está en su lugar, y estamos bien posicionados para reaccionar rápidamente si surge la necesidad.
