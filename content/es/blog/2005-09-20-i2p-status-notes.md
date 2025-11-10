---
title: "Notas de estado de I2P del 2005-09-20"
date: 2005-09-20
author: "jr"
description: "Actualización semanal que cubre el éxito del lanzamiento 0.6.0.6 con introducciones de SSU, actualización de seguridad de I2Phex 0.1.1.27 y finalización de la migración de colo"
categories: ["status"]
---

Hola, gente, es martes otra vez

* Index:

1) 0.6.0.6 2) I2Phex 0.1.1.27 3) migración 4) ???

* 1) 0.6.0.6

Con la versión 0.6.0.6 del sábado pasado, tenemos varios componentes nuevos en funcionamiento en la red en producción, y ustedes han hecho un gran trabajo al actualizar: hasta hace unas horas, ¡casi 250 routers se habían actualizado! La red también parece ir bien, y las introducciones han estado funcionando hasta ahora: pueden seguir su propia actividad de introducción en http://localhost:7657/oldstats.jsp, fijándose en udp.receiveHolePunch y udp.receiveIntroRelayResponse (así como udp.receiveRelayIntro, para quienes están detrás de NATs).

¿Por cierto, el "Status: ERR-Reject" en realidad ya no es un error, así que quizá deberíamos cambiarlo a "Status: OK (NAT)"?

Ha habido algunos informes de errores con Syndie. Más recientemente, hay un error por el que fallará al sincronizarse con pares remotos si se le pide descargar demasiadas entradas a la vez (ya que, tontamente, usé HTTP GET en lugar de POST). Voy a añadir soporte para POST a EepGet, pero, mientras tanto, prueba a descargar solo 20 o 30 publicaciones a la vez. Como nota al margen, quizá alguien pueda crear el JavaScript para la página remote.jsp que diga "obtener todas las publicaciones de este usuario", marcando automáticamente todas las casillas de verificación de su blog?

Se comenta que ahora OSX funciona bien de inmediato, y con la 0.6.0.6-1, x86_64 también está operativo tanto en windows como en linux. No he recibido informes de problemas con los nuevos instaladores .exe, así que eso significa que o bien todo va bien o bien está fallando por completo :)

* 2) I2Phex 0.1.1.27

Prompted by some reports of differences between the source and what was bundled in legion's packaging of 0.1.1.26, as well as concern for the safety of the closed source native launcher, I've gone ahead and added a new launch4j [1] built i2phex.exe to cvs and built the latest from cvs on the i2p file archive [2]. It is unknown whether there are other changes made by legion to his source code prior to his release, or whether the source code he put out is in fact the same as what he built.

Por motivos de seguridad, no puedo recomendar el uso ni del lanzador de código cerrado de legion ni de la versión 0.1.1.26. La versión en el sitio web de I2P [2] contiene el código más reciente de cvs, sin modificaciones.

Puede reproducir la compilación primero obteniendo y compilando el código de I2P, luego obteniendo el código de I2Phex, y después ejecutando "ant makeRelease":   mkdir ~/devi2p ; cd ~/devi2p/   cvs -d :pserver:anoncvs-PQcCzt6076/R7s880joybQ@xxxxxxxxxxxxxxxx/cvsroot login

# (contraseña: anoncvs)

cvs -d :pserver:anoncvs-PQcCzt6076/R7s880joybQ@xxxxxxxxxxxxxxxx/cvsroot co i2p   cd i2p ; ant build ; cd ..   cvs -d :pserver:anoncvs-PQcCzt6076/R7s880joybQ@xxxxxxxxxxxxxxxx/cvsroot co i2phex   cd i2phex/build ; ant makeRelease ; cd ../..   ls -l i2phex/release/i2phex-0.1.1.27.zip

El i2phex.exe dentro de ese zip se puede usar en Windows simplemente ejecutándolo, o en *nix/osx mediante "java -jar i2phex.exe". Sí depende de que I2Phex esté instalado en un directorio junto a I2P - (p. ej., C:\Program Files\i2phex\ y C:\Program Files\i2p\), ya que hace referencia a algunos de los archivos JAR de I2P.

No voy a hacerme cargo del mantenimiento de I2Phex, pero subiré futuras versiones de I2Phex al sitio web cuando haya actualizaciones en cvs. Si alguien quiere trabajar en una página web que podamos publicar para describir/presentarlo (sirup, ¿estás por ahí?), con enlaces a sirup.i2p, publicaciones útiles del foro, la lista de pares activos de legion, sería estupendo.

[1] http://launch4j.sourceforge.net/ [2] http://dev.i2p.net/i2p/i2phex-0.1.1.27.zip y     http://dev.i2p.net/i2p/i2phex-0.1.1.27.zip.sig (firmado con mi clave)

* 3) migration

Hemos cambiado los servidores del centro de datos para los servicios de I2P, pero todo debería estar ya completamente operativo en el servidor nuevo - si ves algo raro, ¡por favor, avísame!

* 4) ???

Últimamente ha habido mucha discusión interesante en la lista de I2P: el nuevo y práctico proxy/filtro SMTP de Adam, así como algunas buenas publicaciones en Syndie (¿han visto el tema (skin) de gloin en http://gloinsblog.i2p?). Estoy trabajando en algunos cambios en este momento para problemas pendientes desde hace tiempo, pero no son inminentes. Si alguien tiene algo más que quiera plantear y discutir, pásense por la reunión en #i2p a las 8 p. m. GMT (en unos 10 minutos o así).

=jr
