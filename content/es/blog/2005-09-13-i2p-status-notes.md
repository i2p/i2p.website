---
title: "Notas de estado de I2P del 2005-09-13"
date: 2005-09-13
author: "jr"
description: "Actualización semanal sobre las introducciones de SSU para la perforación de NAT, los avances del programa de recompensas por pruebas unitarias, la discusión sobre la hoja de ruta de la aplicación cliente y la eliminación del modo de entrega garantizada obsoleto"
categories: ["status"]
---

Hola a todos, es hora de las notas de estado semanales

* Index

1) Estado de la red 2) SSU introductions / perforación de NAT 3) Recompensas 4) Instrucciones para aplicaciones cliente 5) ???

* 1) Net status

Seguimos avanzando con la versión 0.6.0.5 en la red, y casi todos ya han actualizado, con muchos ejecutando alguna de las compilaciones desde entonces (CVS HEAD es 0.6.0.5-9 en este momento). En general, todo sigue funcionando bien, aunque, por lo que he observado, ha habido un aumento sustancial del tráfico de red, probablemente debido a un mayor uso de i2p-bt o i2phex. Uno de los servidores de irc tuvo un pequeño contratiempo anoche, pero el otro aguantó bien y parece que todo se ha recuperado correctamente. Sin embargo, ha habido mejoras sustanciales en el manejo de errores y otras funciones en las compilaciones de CVS, así que espero que tengamos una nueva versión a finales de esta semana.

* 2) SSU introductions / NAT hole punching

Las últimas compilaciones en CVS incluyen soporte para las tan discutidas SSU introductions [1] (introducciones de SSU), lo que nos permite realizar NAT hole punching (apertura de agujeros en NAT) descentralizado para usuarios detrás de un NAT o cortafuegos que no controlan. Aunque no maneja NAT simétrico, sí cubre la mayoría de los casos existentes. Los informes de campo son buenos, aunque solo los usuarios con las últimas compilaciones pueden contactar a los usuarios detrás de NAT; las compilaciones más antiguas deben esperar a que el usuario los contacte primero. Por ello, publicaremos el código en una versión antes de lo habitual para reducir el tiempo durante el cual tenemos estas rutas restringidas en funcionamiento.

[1] http://dev.i2p.net/cgi-bin/cvsweb.cgi/i2p/router/doc/udp.html?rev=HEAD#introduction

* 3) Bounties

Estuve revisando la lista de correo i2p-cvs más temprano y noté varios commits de Comwiz relacionados con lo que parece ser la fase 3 de la recompensa por pruebas unitarias [2]. Quizás Comwiz pueda darnos una actualización del estado sobre ese tema durante la reunión de esta noche.

[2] http://www.i2p.net/bounty_unittests

Como nota al margen, gracias a la sugerencia de una persona anónima, he actualizado un poco el salón de la fama [3], incluyendo las fechas de las contribuciones, agrupando múltiples donaciones de una misma persona y convirtiendo los importes a una sola moneda. Gracias de nuevo a todos los que han contribuido y, si hay información incorrecta publicada o falta algo, por favor pónganse en contacto y se actualizará.

[3] http://www.i2p.net/halloffame

* 4) Client app directions

Uno de los ajustes más recientes en las compilaciones actuales de CVS es la eliminación de la antigua forma de entrega mode=guaranteed. No me había dado cuenta de que alguien todavía lo usara (y es completamente innecesario, ya que contamos con la biblioteca de streaming completa desde hace un año), pero cuando estuve revisando i2phex noté que esa bandera (flag) estaba activada. Con la compilación actual (y todas las versiones posteriores), i2phex simplemente usará mode=best_effort, lo que con suerte mejorará su rendimiento.

Mi objetivo al sacar este tema (más allá de mencionarlo para los usuarios de i2phex) es preguntar qué necesitan en el lado del cliente de I2P y si debería dedicar parte de mi tiempo a ayudar a satisfacer algunas de esas necesidades. A bote pronto, veo mucho trabajo disponible en distintos aspectos:
 = Syndie: publicación simplificada, sincronización automatizada, datos
    importación, integración con aplicaciones (con i2p-bt, susimail, i2phex, etc.),
    compatibilidad con hilos para permitir un comportamiento tipo foro, y más.
 = eepproxy: rendimiento mejorado, soporte de pipelining (canalización)
 = i2phex: mantenimiento general (no lo he usado lo suficiente como para conocer sus
    puntos problemáticos)
 = irc: resiliencia mejorada, detectar caídas recurrentes de servidores irc y
    evitar servidores caídos, filtrar acciones CTCP localmente en lugar de en el
    servidor, proxy DCC
 = Mejor compatibilidad x64 con jbigi, jcpuid y el wrapper de servicio
 = Integración con la bandeja del sistema y eliminación de esa ventana de DOS
 = Controles de ancho de banda mejorados para ráfagas
 = Mejor control de congestión para sobrecarga de red y CPU, así como
    recuperación.
 = Exponer más funcionalidad y documentar las características disponibles de
    la consola del router para aplicaciones de terceros
 = Documentación para desarrolladores de clientes
 = Documentación de introducción a I2P

Además, más allá de todo eso, está el resto de las cosas en la hoja de ruta [4] y la lista de tareas pendientes [5]. Sé lo que necesitamos técnicamente, pero no sé qué es lo que *ustedes* necesitan como usuarios. Háblenme, ¿qué quieren?

[4] http://www.i2p.net/roadmap [5] http://www.i2p.net/todo

* 5) ???

Hay otras cosas en marcha en el núcleo del router y en el lado del desarrollo de aplicaciones, más allá de lo mencionado anteriormente, pero no todo está listo para su uso por el momento. Si alguien tiene algo que le gustaría plantear, pásense por la reunión esta noche a las 20:00 UTC en #i2p.

=jr
