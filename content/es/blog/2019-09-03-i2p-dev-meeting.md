---
title: "Reunión de desarrolladores de I2P - 03 de septiembre de 2019"
date: 2019-09-03
author: "zzz"
description: "Registro de la reunión de desarrollo de I2P del 3 de septiembre de 2019."
categories: ["meeting"]
---

## Resumen rápido

<p class="attendees-inline"><strong>Presentes:</strong> eyedeekay, sadie, zlatinb, zzz</p>

## Registro de la reunión

<div class="irc-log">                Nota: las líneas de sadie no se recibieron durante la reunión; se han pegado más abajo.

20:00:00 <zzz> 0) Hola
20:00:00 <zzz> 1) estado de la publicación 0.9.42 (zzz)
20:00:00 <zzz> 2) estado del proyecto I2P Browser "labs" (sadie, meeh)
20:00:00 <zzz> 3) casos de uso de outproxy / estado (sadie)
20:00:00 <zzz> 4) estado del desarrollo 0.9.43 (zzz)
20:00:00 <zzz> 5) estado de las propuestas (zzz)
20:00:00 <zzz> 6) Status scrum (zlatinb)
20:00:04 <zzz> 0) Hola
20:00:06 <zzz> hola
20:00:17 <zlatinb> hola
20:00:30 <zzz> 1) estado de la publicación 0.9.42 (zzz)
20:00:48 <zzz> la publicación salió bastante bien la semana pasada
20:00:56 <zzz> solo quedan unas pocas cosas pendientes
20:01:27 <zzz> volver a poner en funcionamiento el puente de GitHub (nextloop), el paquete de Debian sid (mhatta), y la biblioteca de cliente de Android que olvidamos para la 41 (meeh)
20:01:37 <zzz> nextloop, meeh, ¿tienen fechas estimadas para esos elementos?
20:03:06 <zzz> ¿algo más en 1) ?
20:04:02 <zzz> 2) estado del proyecto I2P Browser "labs" (sadie, meeh)
20:04:25 <zzz> sadie, meeh, ¿cuál es el estado y cuál es el próximo hito?          <sadie> La Beta 5 se suponía que saldría el viernes, pero hubo algunos problemas. Parece que algunas están listas https://i2bbparts.meeh.no/i2p-browser/ pero realmente necesitaba saber de meeh cuál es el próximo plazo para esto          <sadie> La Página del Laboratorio estará en línea antes de que termine esta semana. El próximo hito del Browser será discutir los requisitos de la consola para la versión beta 6
20:05:51 <zzz> ¿algo más en 2) ?
20:06:43 <zzz> 3) casos de uso de outproxy / estado (sadie)
20:06:57 <zzz> sadie, ¿cuál es el estado y cuál es el próximo hito?          <sadie> Cualquiera puede seguir nuestras notas de reunión en el ticket 2472. Hemos decidido los estados de los casos de uso y tenemos una lista de requisitos. El siguiente hito serán los requisitos de usuario para un caso de uso de Amigos y Familia, así como los requisitos de desarrollo para Amigos y Familia y para el caso de uso General, para ver dónde pueden superponerse
20:08:05 <zzz> ¿algo más en 3) ?
20:08:19 <eyedeekay> Perdón por llegar tarde
20:09:01 <zzz> 4) estado del desarrollo 0.9.43 (zzz)
20:09:21 <zzz> apenas estamos empezando el ciclo de la 43 que planeamos publicar en unas 7 semanas
20:09:40 <zzz> hemos actualizado la hoja de ruta en el sitio web, pero agregaremos algunos elementos más
20:10:06 <zzz> he estado corrigiendo algunos errores de IPv6 y acelerando el procesamiento AES del tunnel
20:10:30 <zzz> pronto dirigiré mi atención al nuevo mensaje de I2CP de blinding info
20:10:59 <zzz> eyedeekay, zlatinb, ¿tienen algo que añadir sobre la .43?
20:11:46 <eyedeekay> No, no lo creo
20:12:02 <zlatinb> probablemente más cosas de la red de pruebas
20:12:32 <zzz> sí, tenemos algunos tickets más de jogger que revisar, con respecto a SSU
20:12:48 <zzz> ¿algo más en 4) ?
20:14:00 <zzz> 5) estado de las propuestas (zzz)
20:14:20 <zzz> nuestro enfoque principal está en la propuesta 144, una nueva de cifrado muy compleja
20:14:48 <zzz> hemos avanzado bien en las últimas semanas y hemos hecho actualizaciones importantes a la propuesta en sí
20:15:35 <zzz> quedan algunas limpiezas y huecos por rellenar, pero confío en que está en buen estado como para empezar a codificar pronto algunas implementaciones de pruebas unitarias, quizá para fin de mes
20:16:17 <zzz> además, el mensaje de blinding info para la propuesta 123 (LS2 cifrado) recibirá otra revisión después de que empiece a codificarlo la próxima semana
20:16:52 <zzz> también esperamos pronto una actualización de chisana sobre la propuesta 152 (mensajes de construcción de tunnel)
20:17:27 <zzz> terminamos la propuesta 147 (prevención entre redes) el mes pasado y tanto i2p como i2pd ya lo tienen codificado e incluido en la versión .42
20:18:23 <zzz> así que las cosas avanzan; aunque la 144 parezca lenta y abrumadora, también está progresando bien
20:18:27 <zzz> ¿algo más en 5) ?
20:20:00 <zzz> 6) Status scrum (zlatinb)
20:20:05 <zzz> adelante, zlatinb
20:20:42 <zlatinb> Hola, por favor digan en pocas palabras: 1) qué han estado haciendo desde el último scrum 2) qué planean hacer el próximo mes 3) si tienen bloqueadores o necesitan ayuda. Digan EOT cuando terminen
20:21:23 <zlatinb> yo: 1) Varios experimentos en la red de pruebas para acelerar transferencias masivas 2) más trabajo en la red de pruebas en un servidor/red que espero sea más grande 3) sin bloqueadores EOT
20:22:15 <zzz> 1) correcciones de errores, el cambio de división de configuración, publicación .42, propuestas, talleres de DEFCON (vean mi informe de viaje en i2pforum y en nuestro sitio web)
20:23:56 <zzz> 2) correcciones de errores, propuesta 144, mensaje de blinding info, aceleraciones, ayudar con la investigación de outproxy, arreglar el asistente de SSL roto por la división de conf.
20:24:20 <zzz> más correcciones de IPv6
20:24:38 <zzz> 3) sin bloqueadores EOT
20:24:50 <eyedeekay> 1) Desde el último scrum he estado trabajando en correcciones de errores, el sitio web, trabajando en la propuesta de outproxy y cosas relacionadas con i2ptunnels. 2) Seguir reorganizando y mejorando la presentación del sitio web. Trabajar en avanzar la propuesta de outproxy 3) sin bloqueadores EOT          <sadie> 1) Asistí a FOCI, investigué opciones de financiación, me reuní con posibles financiadores, tuve una reunión con Tails (incluido Mhatta), trabajé en la marca de I2P Browser, actualizaciones del sitio web con IDK, hice pequeños cambios a la consola para la última publicación          <sadie> 2) el próximo mes trabajaré en subvenciones, mejoras de la consola y del sitio web, asistente de configuración, asistir a Our Networks en Toronto, e impulsar la investigación de I2P Browser y OutProxy          <sadie> 3) sin bloqueadores EOT
20:25:29 <zlatinb> scrum.setTimeout( 60 * 1000 );
20:27:04 <zzz> ok, se acaba el tiempo
20:27:10 <zlatinb> ScrumTimeoutException
20:27:41 <zzz> último aviso para sadie meeh nextloop para volver a 1)-3)
20:27:52 <zzz> ¿algún otro tema para la reunión?
20:28:47 * zzz agarra el baffer
20:30:00 * zzz ***bafs*** se cierra la reunión </div>
