---
title: "Hoja de ruta de alto nivel para 2018"
date: 2018-02-11
slug: "high-level-roadmap-for-2018"
author: "str4d"
description: "2018 será el año de nuevos protocolos, nuevas colaboraciones y un enfoque más depurado"
categories: ["roadmap"]
---

Una de las muchas cosas que discutimos en el 34C3 fue en qué deberíamos centrarnos durante el próximo año. En particular, queríamos una hoja de ruta que dejara claro qué queremos asegurarnos de completar, frente a lo que estaría muy bien tener, y que pudiera ayudar a incorporar a los recién llegados a cualquiera de esas dos categorías. Esto fue lo que acordamos:

## Prioridad: Nueva cripto(grafía!)

Muchas de las primitivas y los protocolos actuales aún conservan sus diseños originales de alrededor de 2005 y necesitan mejoras. Hemos tenido varias propuestas abiertas durante varios años con ideas, pero el progreso ha sido lento. Todos coincidimos en que esto debe ser nuestra máxima prioridad para 2018. Los componentes fundamentales son:

- New transport protocols (to replace NTCP and SSU). See [Prop111](https://geti2p.net/spec/proposals/111).
- New onion-encryption protocol for building and using tunnels.
- New NetDB datatypes to enable enhanced Destinations. See [Prop123](https://geti2p.net/spec/proposals/123).
- Upgraded end-to-end protocol (replacing ElGamal).

El trabajo en esta prioridad se divide en varias áreas:

- Writing proposals.
- Writing working implementations of them that we can test.
- Reviewing proposals.

No podemos publicar nuevas especificaciones de protocolo en toda la red sin trabajar en todas estas áreas.

## Deseable: Reutilización de código

Una de las ventajas de iniciar el trabajo anterior ahora es que, en los últimos años, ha habido esfuerzos independientes para crear protocolos simples y marcos de protocolos que cumplen muchos de los objetivos que tenemos para nuestros propios protocolos y que han ganado aceptación en la comunidad más amplia. Al aprovechar este trabajo, obtenemos un "efecto multiplicador":

- We benefit from protocol designs, security proofs, and code written by others, reducing the amount of work we need to do for the same level of feature-completeness and security assurances.

- Work we do can be leveraged by other communities, increasing their interest in collaborating with us, and thinking about I2P as a whole.

Mis propuestas, en particular, aprovecharán el [Noise Protocol Framework](https://noiseprotocol.org/) y el [formato de paquetes SPHINX](https://katzenpost.mixnetworks.org/docs/specs/sphinx.html). ¡Tengo colaboraciones previstas con varias personas fuera de I2P para estas!

## Prioridad: Colaboración con el Clearnet (Internet abierta)

A ese respecto, hemos ido generando interés poco a poco durante los últimos seis meses aproximadamente. A lo largo de PETS2017, 34C3 y RWC2018, he mantenido muy buenas conversaciones sobre formas de mejorar la colaboración con la comunidad más amplia. Esto es realmente importante para garantizar que podamos recabar la mayor cantidad de revisión posible para los nuevos protocolos. El mayor obstáculo que he visto es el hecho de que la mayor parte de la colaboración en el desarrollo de I2P actualmente tiene lugar dentro de la propia I2P, lo que incrementa significativamente el esfuerzo necesario para contribuir.

Las dos prioridades en esta área son:

- Set up a project-run development forum that is accessible both inside and outside I2P.

- Set up mailing lists for review and discussion of proposals (possibly connected to the above forum).

Otros objetivos clasificados como deseables:

- Set up a usable git-to-mtn pathway, to enable us to effectively solicit clearnet contributions on GitHub while keeping the canonical dev environment on Monotone.

- Write a "position paper" that accurately explains I2P to academic audiences, and puts it in context with existing literature.

Espero que las colaboraciones con personas ajenas a I2P se lleven a cabo íntegramente en GitHub, para minimizar la fricción.

## Prioridad: Preparación para versiones de larga duración

I2P ahora está en Debian Sid (su repositorio inestable), que se estabilizará dentro de aproximadamente un año y medio, y también se ha incorporado al repositorio de Ubuntu para su inclusión en la próxima versión LTS en abril. Vamos a empezar a tener versiones de I2P que permanecerán durante años, y necesitamos asegurarnos de que podemos gestionar su presencia en la red.

El objetivo principal aquí es desplegar tantos de los nuevos protocolos como nos sea posible durante el próximo año, para coincidir con el próximo lanzamiento estable de Debian. Para aquellos que requieran despliegues de varios años, deberíamos incorporar los cambios de compatibilidad con versiones futuras tan pronto como podamos.

## Prioridad: conversión de las aplicaciones actuales en complementos

El modelo de Debian fomenta tener paquetes separados para componentes separados. Coincidimos en que desacoplar las aplicaciones Java actualmente empaquetadas del router Java principal sería beneficioso por varias razones:

- It codifies the boundary between the applications and the router.

- It should make it easier to get these apps running with non-Java routers.

- It would enable third parties to create "I2P bundles" containing just the applications they want.

En combinación con las prioridades anteriores, esto orienta el proyecto principal de I2P hacia un modelo más parecido al del kernel de Linux. Dedicaremos más tiempo a centrarnos en la red en sí, dejando que los desarrolladores de terceros se enfoquen en aplicaciones que usan la red (algo que es significativamente más fácil de hacer tras nuestro trabajo de los últimos años en APIs y bibliotecas).

## Opcional: mejoras de la aplicación

Hay varias mejoras a nivel de aplicación en las que queremos trabajar, pero actualmente no contamos con tiempo de desarrollo para hacerlo, dadas nuestras otras prioridades. ¡Esta es un área en la que nos encantaría ver nuevos colaboradores! Una vez que el desacoplamiento anterior esté completo, será significativamente más fácil que alguien trabaje en una aplicación específica de forma independiente del router Java principal.

Una aplicación para la que nos encantaría contar con ayuda es I2P Android. La mantendremos actualizada con las versiones principales de I2P y corregiremos errores en la medida de lo posible, pero hay mucho que se podría hacer para mejorar tanto el código subyacente como la usabilidad.

## Prioridad: estabilización de Susimail e I2P-Bote

Dicho esto, sí queremos trabajar específicamente en correcciones para Susimail e I2P-Bote a corto plazo (algunas de las cuales ya se han incluido en la 0.9.33). Han recibido menos trabajo en los últimos años que otras aplicaciones de I2P, así que queremos dedicar algo de tiempo a poner sus bases de código al día y facilitar que nuevos colaboradores se incorporen.

## Deseable: Priorización de tickets

Tenemos una gran acumulación de tickets pendientes en varios subsistemas y aplicaciones de I2P. Como parte del esfuerzo de estabilización mencionado anteriormente, nos encantaría resolver algunas de nuestras incidencias antiguas que llevan mucho tiempo abiertas. Más importante aún, queremos asegurarnos de que nuestros tickets estén correctamente organizados, para que los nuevos colaboradores puedan encontrar buenos tickets en los que trabajar.

## Prioridad: Soporte al usuario

Uno de los aspectos de lo anterior en el que nos centraremos es mantener el contacto con los usuarios que se toman el tiempo de informar de problemas. ¡Gracias! Cuanto más podamos acortar el ciclo de retroalimentación, más rápido podremos resolver los problemas a los que se enfrentan los nuevos usuarios y más probable será que sigan participando en la comunidad.

## ¡Nos encantaría contar con tu ayuda!

Todo eso parece muy ambicioso, ¡y lo es! Pero muchos de los elementos anteriores se superponen y, con una planificación cuidadosa, podemos lograr un avance importante en ellos.

Si te interesa ayudar con cualquiera de los objetivos anteriores, ¡ven a charlar con nosotros! Puedes encontrarnos en OFTC y Freenode (#i2p-dev) y en Twitter (@GetI2P).
