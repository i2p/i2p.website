---
title: "Desaprobación de nombres de host en direcciones del router"
number: "141"
author: "zzz"
created: "2017-08-03"
lastupdated: "2018-03-17"
status: "Cerrado"
thread: "http://zzz.i2p/topics/2363"
target: "0.9.32"
implementedin: "0.9.32"
toc: true
---

## Descripción general

A partir de la versión 0.9.32, actualiza la especificación de netdb
para desaprobar nombres de host en router infos,
o más precisamente, en las direcciones individuales del router.
En todas las implementaciones de I2P,
los routers de publicación configurados con nombres de host deben reemplazarlos con IPs antes de publicar,
y otros routers deben ignorar direcciones con nombres de host.
Los routers no deben realizar búsquedas DNS de nombres de host publicados.


## Motivación

Los nombres de host han sido permitidos en las direcciones del router desde el inicio de I2P.
Sin embargo, muy pocos routers publican nombres de host, porque se requiere
tanto un nombre de host público (que pocos usuarios tienen), como una configuración manual
(que pocos usuarios se molestan en hacer).
En una muestra reciente, el 0.7% de los routers estaban publicando un nombre de host.

El propósito original de los nombres de host era ayudar a los usuarios con IPs
que cambian frecuentemente y un servicio de DNS dinámico (como http://dyn.com/dns/)
para no perder conectividad cuando su IP cambiaba. Sin embargo, en ese entonces
la red era pequeña y la expiración de la información del router era más larga.
Además, el código Java no tenía lógica funcional para reiniciar el router o
republicar la información del router cuando la IP local cambiaba.

También, al principio, I2P no soportaba IPv6, por lo que la complicación
de resolver un nombre de host a una dirección IPv4 o IPv6 no existía.

En Java I2P, siempre ha sido un desafío propagar un nombre de host configurado
a ambos transportes publicados, y la situación se volvió más compleja
con IPv6.
No está claro si un host de doble pila debería publicar tanto un nombre de host como una dirección
IPv6 literal o no. El nombre de host se publica para la dirección SSU pero no para la dirección NTCP.

Recientemente, los problemas de DNS fueron mencionados (tanto indirecta como directamente) por
investigaciones en Georgia Tech. Los investigadores ejecutaron un gran número de floodfills
con nombres de host publicados. El problema inmediato fue que para un pequeño número de
usuarios con posiblemente DNS local roto, colgó I2P completamente.

El problema más grande fue DNS en general y cómo
DNS (ya sea activo o pasivo) podría usarse para enumerar rápidamente la red,
especialmente si los routers publicados eran floodfill.
Nombres de host inválidos o respondedores DNS no receptivos, lentos o maliciosos podrían
ser usados para ataques adicionales.
EDNS0 podría proporcionar escenarios adicionales de enumeración o ataque.
DNS también podría proporcionar vías de ataque basadas en el momento de la consulta,
revelando tiempos de conexión entre routers, ayudar a construir gráficos de conexión,
estimar tráfico y otras inferencias.

Además, el grupo de Georgia Tech, liderado por David Dagon, ha enumerado varias preocupaciones
con DNS en aplicaciones enfocadas en la privacidad. Las consultas DNS generalmente se realizan por
una biblioteca de bajo nivel, no controlada por la aplicación.
Estas bibliotecas no fueron diseñadas específicamente para el anonimato;
pueden no proporcionar control fino a la aplicación;
y su salida puede ser única.
Las bibliotecas de Java en particular pueden ser problemáticas, pero esto no es solo un problema de Java.
Algunas bibliotecas usan consultas DNS ANY que pueden ser rechazadas.
Todo esto es aún más preocupante por la presencia generalizada
de monitoreo pasivo DNS y consultas disponibles para múltiples organizaciones.
Todo el monitoreo y los ataques DNS están fuera de banda desde la perspectiva de
los routers I2P y requieren pocos o ningún recurso dentro de la red I2P,
y ninguna modificación de las implementaciones existentes.

Aunque no hemos pensado completamente en los posibles problemas,
la superficie de ataque parece ser grande. Hay otras formas de
enumerar la red y reunir datos relacionados, pero los ataques DNS
podrían ser mucho más fáciles, más rápidos y menos detectables.

Las implementaciones de routers podrían, en teoría, cambiar a usar una biblioteca DNS
de terceros sofisticada, pero eso sería bastante complejo, sería una carga de mantenimiento,
y está claramente fuera del núcleo de experiencia de los desarrolladores de I2P.

Las soluciones inmediatas implementadas para Java 0.9.31 incluyeron corregir el problema del cuelgue,
aumentar los tiempos de caché DNS, e implementar una caché negativa de DNS. Por supuesto,
aumentar los tiempos de caché reduce el beneficio de tener nombres de host en routerinfos para empezar.

Sin embargo, estos cambios son solo mitigaciones a corto plazo y no resuelven los problemas subyacentes indicados anteriormente. Por lo tanto, la solución más simple y completa es prohibir los
nombres de host en la información del router, eliminando así las búsquedas DNS para ellos.


## Diseño

Para el código de publicación de información del router, los implementadores tienen dos opciones: o bien
deshabilitar/eliminar la opción de configuración para nombres de host, o
convertir nombres de host configurados a IPs en el momento de la publicación.
En cualquier caso, los routers deben republicar inmediatamente cuando su IP cambie.

Para el código de validación de información del router y de conexión de transporte,
los implementadores deben ignorar direcciones del router que contengan nombres de host,
y usar las otras direcciones publicadas que contengan IPs, si las hay.
Si ninguna dirección en la información del router contiene IPs, el router
no debe conectarse al router publicado.
En ningún caso un router debe realizar una consulta DNS de un nombre de host publicado,
ya sea directamente o a través de una biblioteca subyacente.


## Especificación

Cambia las especificaciones de transporte de NTCP y SSU para indicar que el parámetro "host" debe ser
una IP, no un nombre de host, y que los routers deben ignorar direcciones individuales
del router que contengan nombres de host.

Esto también se aplica a los parámetros "ihost0", "ihost1" e "ihost2" en una dirección SSU.
Los routers deben ignorar direcciones de introductor que contengan nombres de host.


## Notas

Esta propuesta no aborda nombres de host para hosts de resiembra.
Aunque las búsquedas DNS para hosts de resiembra son mucho menos frecuentes,
podrían seguir siendo un problema. Si es necesario, esto puede solucionarse simplemente
reemplazando los nombres de host con IPs en la lista de URLs codificadas;
no se requerirían cambios en la especificación o el código.


## Migración

Esta propuesta puede implementarse inmediatamente, sin una migración gradual,
porque muy pocos routers publican nombres de host, y aquellos que lo hacen generalmente
no publican el nombre de host en todas las direcciones.

Los routers no necesitan verificar la versión del router publicado
antes de decidir ignorar nombres de host, y no hay necesidad
de un lanzamiento coordinado o estrategia común entre
las diversas implementaciones de routers.

Para aquellos routers que aún están publicando nombres de host, obtendrán menos
conexiones entrantes, y eventualmente podrían tener dificultades para construir
túneles entrantes.

Para minimizar el impacto aún más, los implementadores podrían comenzar por ignorar
direcciones del router con nombres de host solo para routers de floodfill,
o para routers con una versión publicada menor a 0.9.32,
e ignorar nombres de host para todos los routers en un lanzamiento posterior.
