---
title: "Hoja de ruta de alto nivel para 2018"
date: 2018-02-11
slug: "high-level-roadmap-for-2018"
author: "str4d"
description: "2018 será el año de nuevos protocolos, nuevas colaboraciones y un enfoque más refinado."
categories: ["roadmap"]
---

Una de las muchas cosas que debatimos en el 34C3 fue en qué deberíamos centrarnos durante el próximo año. En particular, queríamos una hoja de ruta que dejara claro qué queremos asegurarnos de lograr, frente a lo que sería muy bueno tener, y que además nos permitiera ayudar a incorporar a los recién llegados en cualquiera de las dos categorías. Esto es lo que acordamos:

## Prioridad: Nueva cripto(grafía!)

Muchas de las primitivas y los protocolos actuales aún conservan sus diseños originales de alrededor de 2005 y necesitan mejoras. Hemos tenido varias propuestas abiertas con ideas desde hace años, pero el avance ha sido lento. Todos coincidimos en que esto debe ser nuestra máxima prioridad para 2018. Los componentes fundamentales son:

- New transport protocols (to replace NTCP and SSU). See Prop111.
- New onion-encryption protocol for building and using tunnels.
- New NetDB datatypes to enable enhanced Destinations. See Prop123.
- Upgraded end-to-end protocol (replacing ElGamal).

El trabajo en esta prioridad se divide en varias áreas:

- Writing proposals.
- Writing working implementations of them that we can test.
- Reviewing proposals.

No podemos publicar nuevas especificaciones de protocolo en toda la red sin trabajar en todas estas áreas.

## Deseable: Reutilización de código

Uno de los beneficios de iniciar el trabajo anterior ahora es que, en los últimos años, ha habido esfuerzos independientes para crear protocolos y marcos de protocolos simples que cumplen muchos de los objetivos que tenemos para nuestros propios protocolos y que han ganado tracción en la comunidad en general. Al aprovechar este trabajo, obtenemos un efecto de "multiplicador de fuerza":

- We benefit from protocol designs, security proofs, and code written by others, reducing the amount of work we need to do for the same level of feature-completeness and security assurances.

- Work we do can be leveraged by other communities, increasing their interest in collaborating with us, and thinking about I2P as a whole.

Mis propuestas, en particular, aprovecharán el [Noise Protocol Framework](https://noiseprotocol.org/) y el [formato de paquetes SPHINX](https://katzenpost.mixnetworks.org/docs/specs/sphinx.html). ¡Ya tengo colaboraciones concertadas con varias personas fuera de I2P para estas!

## Prioridad: Colaboración con la Clearnet (Internet público convencional)

Al respecto, hemos ido generando interés de forma gradual durante los últimos seis meses aproximadamente. Durante PETS2017, 34C3 y RWC2018 he tenido muy buenas conversaciones sobre maneras en que podemos mejorar la colaboración con la comunidad en general. Esto es muy importante para garantizar que podamos recabar la mayor revisión posible para los nuevos protocolos. El mayor obstáculo que he visto es que la mayor parte de la colaboración en el desarrollo de I2P actualmente ocurre dentro del propio I2P, lo que aumenta significativamente el esfuerzo necesario para contribuir.

Las dos prioridades en esta área son:

- Set up a project-run development forum that is accessible both inside and outside I2P.

- Set up mailing lists for review and discussion of proposals (possibly connected to the above forum).

Otros objetivos clasificados como deseables:

- Set up a usable git-to-mtn pathway, to enable us to effectively solicit clearnet contributions on GitHub while keeping the canonical dev environment on Monotone.

- Write a "position paper" that accurately explains I2P to academic audiences, and puts it in context with existing literature.

Espero que las colaboraciones con personas fuera de I2P se realicen íntegramente en GitHub, para minimizar la fricción.

## Prioridad: Preparación para lanzamientos de larga duración

I2P ahora está en Debian Sid (su repositorio inestable), que se estabilizará en alrededor de un año y medio, y también se ha incorporado al repositorio de Ubuntu para su inclusión en la próxima versión LTS en abril. Vamos a empezar a tener versiones de I2P que permanecerán durante años, y debemos asegurarnos de poder gestionar su presencia en la red.

El objetivo principal aquí es desplegar tantos de los nuevos protocolos como nos sea factible durante el próximo año, para llegar a tiempo a la próxima versión estable de Debian. Para aquellos que requieran despliegues de varios años, deberíamos incorporar los cambios de compatibilidad hacia adelante lo antes posible.

## Prioridad: Conversión en complementos de las aplicaciones actuales

El modelo de Debian fomenta tener paquetes separados para componentes separados. Acordamos que desacoplar las aplicaciones Java actualmente incluidas del router Java principal sería beneficioso por varias razones:

- It codifies the boundary between the applications and the router.

- It should make it easier to get these apps running with non-Java routers.

- It would enable third parties to create "I2P bundles" containing just the applications they want.

En combinación con las prioridades anteriores, esto orienta el proyecto principal de I2P más en la dirección de, por ejemplo, el kernel de Linux. Dedicaremos más tiempo a centrarnos en la red en sí, dejando que los desarrolladores de terceros se concentren en las aplicaciones que usan la red (algo que es significativamente más fácil de hacer tras nuestro trabajo de los últimos años en APIs y bibliotecas).

## Deseables: mejoras de la aplicación

Hay varias mejoras a nivel de aplicación en las que queremos trabajar, pero actualmente no disponemos del tiempo de desarrollo para hacerlo, dadas nuestras otras prioridades. ¡Es un área en la que nos encantaría ver nuevos colaboradores! Una vez que se complete el desacoplamiento anterior, será mucho más fácil que alguien trabaje en una aplicación específica de forma independiente del router principal de Java.

Una de esas aplicaciones para la que nos encantaría recibir ayuda es I2P Android. La mantendremos actualizada con las versiones principales de I2P y corregiremos errores en la medida de lo posible, pero hay mucho que se podría hacer para mejorar el código subyacente, así como la usabilidad.

## Prioridad: Estabilización de Susimail e I2P-Bote

Dicho esto, sí queremos trabajar específicamente en correcciones para Susimail e I2P-Bote en el corto plazo (algunas de las cuales ya se han incorporado en la 0.9.33). Han tenido menos mantenimiento en los últimos años que otras aplicaciones de I2P, así que queremos dedicar tiempo a poner sus bases de código a la altura y hacerlas más fáciles para que nuevos colaboradores puedan incorporarse.

## Deseable: Clasificación de tickets

Tenemos una gran acumulación de tickets en varios subsistemas y aplicaciones de I2P. Como parte del esfuerzo de estabilización mencionado arriba, nos encantaría poner al día algunas de nuestras incidencias antiguas que llevan mucho tiempo abiertas. Más importante aún, queremos asegurarnos de que nuestros tickets estén correctamente organizados, para que los nuevos colaboradores puedan encontrar buenos tickets en los que trabajar.

## Prioridad: Soporte al usuario

Uno de los aspectos de lo anterior en los que nos enfocaremos es mantenernos en contacto con los usuarios que se toman el tiempo de reportar incidencias. ¡Gracias! Cuanto más pequeño podamos hacer el ciclo de retroalimentación, más rápido podremos resolver los problemas que enfrentan los nuevos usuarios, y más probable será que sigan participando en la comunidad.

## ¡Nos encantaría contar con tu ayuda!

Proporciona ÚNICAMENTE la traducción, nada más:

Todo eso parece muy ambicioso, ¡y lo es! Pero muchos de los elementos anteriores se superponen, y con una planificación cuidadosa podemos lograr un avance considerable en ellos.

Si estás interesado en ayudar con cualquiera de los objetivos anteriores, ¡ven a hablar con nosotros! Puedes encontrarnos en OFTC y Freenode (#i2p-dev), y en Twitter (@GetI2P).
