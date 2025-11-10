---
title: "El Proceso de Propuestas de I2P"
number: "001"
author: "str4d"
created: "2016-04-10"
lastupdated: "2017-04-07"
status: "Meta"
thread: "http://zzz.i2p/topics/1980"
---

## Resumen

Este documento describe cómo cambiar las especificaciones de I2P, cómo funcionan las propuestas de I2P y la relación entre las propuestas de I2P y las especificaciones.

Este documento se adapta del proceso de propuestas de Tor, y gran parte del contenido a continuación fue originalmente escrito por Nick Mathewson.

Este es un documento informativo.

## Motivación

Anteriormente, nuestro proceso para actualizar las especificaciones de I2P era relativamente informal: haríamos una propuesta en el foro de desarrollo y discutiríamos los cambios, luego llegaríamos a un consenso y parchearíamos la especificación con cambios en borrador (no necesariamente en ese orden), y finalmente implementaríamos los cambios.

Esto tenía algunos problemas.

Primero, incluso en su forma más eficiente, el viejo proceso a menudo dejaría la especificación desincronizada con el código. Los peores casos eran aquellos donde la implementación se posponía: la especificación y el código podían permanecer desincronizados por versiones a la vez.

Segundo, era difícil participar en la discusión, ya que no siempre estaba claro qué partes del hilo de discusión formaban parte de la propuesta, o qué cambios a la especificación se habían implementado. Los foros de desarrollo también son accesibles solo dentro de I2P, lo que significa que las propuestas solo podían ser vistas por personas que usan I2P.

Tercero, era muy fácil olvidar algunas propuestas porque se enterraban varias páginas atrás en la lista de hilos del foro.

## Cómo cambiar las especificaciones ahora

Primero, alguien escribe un documento de propuesta. Debe describir el cambio que se debe realizar en detalle y dar una idea de cómo implementarlo. Una vez que esté suficientemente desarrollado, se convierte en una propuesta.

Al igual que un RFC, cada propuesta obtiene un número. A diferencia de los RFCs, las propuestas pueden cambiar con el tiempo y mantener el mismo número, hasta que finalmente sean aceptadas o rechazadas. La historia de cada propuesta se almacenará en el repositorio del sitio web de I2P.

Una vez que una propuesta está en el repositorio, deberíamos discutirla en el hilo correspondiente y mejorarla hasta que hayamos llegado a un consenso de que es una buena idea y que está lo suficientemente detallada para implementarse. Cuando esto sucede, implementamos la propuesta y la incorporamos a las especificaciones. Así, las especificaciones siguen siendo la documentación canónica para el protocolo I2P: ninguna propuesta es jamás la documentación canónica para una característica implementada.

(Este proceso es bastante similar al Proceso de Mejora de Python, con la excepción principal de que las propuestas de I2P se reintegran a las especificaciones después de la implementación, mientras que los PEPs *se convierten* en la nueva especificación.)

### Cambios pequeños

Todavía está permitido hacer cambios pequeños directamente en la especificación si el código puede ser escrito más o menos de inmediato, o cambios cosméticos si no se requiere un cambio de código. Este documento refleja la *intención* de los desarrolladores actuales, no una promesa permanente de siempre usar este proceso en el futuro: nos reservamos el derecho de emocionarnos mucho y salir corriendo a implementar algo en una sesión de programación nocturna alimentada por cafeína o M&M.

## Cómo se añaden nuevas propuestas

Para presentar una propuesta, publíquela en el foro de desarrollo o ingrese un ticket con la propuesta adjunta.

Una vez que se ha propuesto una idea, existe un borrador debidamente formateado (ver más abajo), y existe consenso general dentro de la comunidad de desarrollo activa de que esta idea merece consideración, los editores de propuestas añadirán oficialmente la propuesta.

Los editores de propuestas actuales son zzz y str4d.

## Qué debería incluir una propuesta

Cada propuesta debe tener un encabezado con estos campos:

```
:author:
:created:
:thread:
:lastupdated:
:status:
```

- El campo `author` debe contener los nombres de los autores de esta propuesta.
- El campo `thread` debe ser un enlace al hilo del foro de desarrollo donde se publicó originalmente esta propuesta, o a un nuevo hilo creado para discutir esta propuesta.
- El campo `lastupdated` debe ser inicialmente igual al campo `created`, y debe actualizarse siempre que se cambie la propuesta.

Estos campos deben establecerse cuando sea necesario:

```
:supercedes:
:supercededby:
:editor:
```

- El campo `supercedes` es una lista separada por comas de todas las propuestas que esta propuesta reemplaza. Esas propuestas deben ser Rechazadas y tener su campo `supercededby` establecido en el número de esta propuesta.
- El campo `editor` debe establecerse si se realizan cambios significativos a esta propuesta que no alteran sustancialmente su contenido. Si el contenido se está alterando sustancialmente, se debe agregar un `author` adicional, o crear una nueva propuesta que sustituya a esta.

Estos campos son opcionales pero recomendados:

```
:target:
:implementedin:
```

- El campo `target` debe describir en qué versión se espera implementar la propuesta (si está Abierta o Aceptada).
- El campo `implementedin` debe describir en qué versión se implementó la propuesta (si está Terminada o Cerrada).

El cuerpo de la propuesta debe comenzar con una sección de Resumen que explique de qué trata la propuesta, qué hace y en qué estado se encuentra.

Después del Resumen, la propuesta se vuelve más libre. Dependiendo de su longitud y complejidad, la propuesta puede dividirse en secciones según corresponda, o seguir un formato discursivo breve. Cada propuesta debe contener al menos la siguiente información antes de ser Aceptada, aunque la información no necesita estar en secciones con estos nombres.

**Motivación**
: ¿Qué problema intenta resolver la propuesta? ¿Por qué importa este problema? Si varias enfoques son posibles, ¿por qué elegir este?

**Diseño**
: Una visión de alto nivel de cuáles son las características nuevas o modificadas, cómo funcionan las características nuevas o modificadas, cómo interactúan entre sí y cómo interactúan con el resto de I2P. Este es el cuerpo principal de la propuesta. Algunas propuestas comenzarán solo con una Motivación y un Diseño, y esperarán por una especificación hasta que el Diseño parezca aproximadamente correcto.

**Implicaciones de seguridad**
: Qué efectos podrían tener los cambios propuestos en el anonimato, cuán bien entendidos están estos efectos, etc.

**Especificación**
: Una descripción detallada de lo que necesita añadirse a las especificaciones de I2P para implementar la propuesta. Esto debe ser en tantos detalles como las especificaciones contendrán eventualmente: debería ser posible para los programadores independientes escribir implementaciones mutuamente compatibles de la propuesta basándose en sus especificaciones.

**Compatibilidad**
: ¿Las versiones de I2P que siguen la propuesta serán compatibles con versiones que no lo hagan? Si es así, ¿cómo se logrará la compatibilidad? En general, intentamos no abandonar la compatibilidad si es posible; no hemos hecho un cambio de "día de la bandera" desde marzo de 2008, y no queremos hacer otro.

**Implementación**
: Si la propuesta será complicada de implementar en la arquitectura actual de I2P, el documento puede contener una discusión sobre cómo hacer que funcione. Los parches reales deben ir en ramas monotone públicas, o subirlos a Trac.

**Notas de rendimiento y escalabilidad**
: Si la característica tendrá un efecto en el rendimiento (en RAM, CPU, ancho de banda) o escalabilidad, debería haber algún análisis sobre cuán significativo será este efecto, para que podamos evitar regresiones de rendimiento realmente costosas, y para que podamos evitar perder tiempo en ganancias insignificantes.

**Referencias**
: Si la propuesta se refiere a documentos externos, estos deben ser enumerados.

## Estado de la propuesta

**Abierta**
: Una propuesta en discusión.

**Aceptada**
: La propuesta está completa, y tenemos la intención de implementarla. Después de este punto, se deben evitar cambios sustanciales a la propuesta, y considerarse como una señal de que el proceso ha fallado en algún lugar.

**Terminada**
: La propuesta ha sido aceptada e implementada. Después de este punto, la propuesta no debe ser cambiada.

**Cerrada**
: La propuesta ha sido aceptada, implementada y se ha integrado en los documentos de especificación principales. La propuesta no debe ser cambiada después de este punto.

**Rechazada**
: No vamos a implementar la característica tal como se describe aquí, aunque podríamos hacer alguna otra versión. Vea los comentarios en el documento para más detalles. La propuesta no debe ser cambiada después de este punto; para plantear otra versión de la idea, escriba una nueva propuesta.

**Borrador**
: Esta no es una propuesta completa todavía; hay piezas definitivamente faltantes. Por favor, no añada nuevas propuestas con este estado; póngalas en el subdirectorio "ideas" en su lugar.

**Necesita-Revisión**
: La idea de la propuesta es buena, pero la propuesta tal como está tiene problemas serios que impiden que sea aceptada. Vea los comentarios en el documento para más detalles.

**Muerta**
: La propuesta no ha sido tocada en mucho tiempo, y no parece que alguien vaya a completarla pronto. Puede volverse "Abierta" nuevamente si obtiene un nuevo proponente.

**Necesita-Investigación**
: Hay problemas de investigación que necesitan ser resueltos antes de que esté claro si la propuesta es una buena idea.

**Meta**
: Esto no es una propuesta, sino un documento sobre propuestas.

**Reserva**
: Esta propuesta no es algo que actualmente planeamos implementar, pero podríamos querer resucitarla algún día si decidimos hacer algo como lo que propone.

**Informativa**
: Esta propuesta es la última palabra sobre lo que está haciendo. No se va a convertir en una especificación a menos que alguien la copie y pegue en una nueva especificación para un nuevo subsistema.

Los editores mantienen el estado correcto de las propuestas, basado en el consenso general y su propia discreción.

## Numeración de Propuestas

Los números del 000-099 están reservados para propuestas especiales y meta-propuestas. 100 en adelante se usan para propuestas reales. Los números no se reciclan.

## Referencias

- [Proceso de Propuestas de Tor](https://gitweb.torproject.org/torspec.git/tree/proposals/001-process.txt)
