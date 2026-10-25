---
title: "Tunnels Unidireccionales"
description: "Resumen histórico del diseño de túneles unidireccionales de I2P"
slug: "unidirectional"
aliases:
  - "/es/unidirectional-tunnels"
  - "/es/unidirectional-tunnels/"
lastUpdated: "2016-11"
accurateFor: "0.9.27"
---

## Descripción general

Esta página describe los orígenes y el diseño de los tunnels unidireccionales de I2P. Para más información consulte:

- [Página de resumen de tunnels](/docs/overview/tunnel-routing)
- [Especificación de tunnels](/docs/specs/tunnel-implementation)
- [Especificación de creación de tunnels](/docs/specs/tunnel-creation)
- [Discusión sobre el diseño de tunnels](/docs/discussions/tunnel)
- [Selección de peers](/docs/overview/peer-selection)

## Revisión

Aunque no tenemos conocimiento de ninguna investigación publicada sobre las ventajas de los tunnels unidireccionales, parecen hacer más difícil detectar un patrón de solicitud/respuesta, que es bastante posible detectar a través de un tunnel bidireccional. Varias aplicaciones y protocolos, especialmente HTTP, transfieren datos de esta manera. Hacer que el tráfico siga la misma ruta hacia su destino y de vuelta podría facilitar a un atacante que solo tenga datos de tiempo y volumen de tráfico inferir la ruta que está tomando un tunnel. Hacer que la respuesta regrese por una ruta diferente posiblemente lo hace más difícil.

Al enfrentarse a un adversario interno o a la mayoría de adversarios externos, los túneles unidireccionales de I2P exponen la mitad de datos de tráfico que se expondrían con circuitos bidireccionales simplemente observando los flujos en sí mismos: una solicitud y respuesta HTTP seguirían el mismo camino en Tor, mientras que en I2P los paquetes que componen la solicitud saldrían a través de uno o más túneles de salida y los paquetes que componen la respuesta regresarían a través de uno o más túneles de entrada diferentes.

La estrategia de usar dos tunnels separados para la comunicación entrante y saliente no es la única técnica disponible, y sí tiene implicaciones de anonimato. En el lado positivo, al usar tunnels separados se reduce los datos de tráfico expuestos para análisis a los participantes en un tunnel - por ejemplo, los peers en un tunnel saliente desde un navegador web solo verían el tráfico de un HTTP GET, mientras que los peers en un tunnel entrante verían la carga útil entregada a lo largo del tunnel. Con tunnels bidireccionales, todos los participantes tendrían acceso al hecho de que, por ejemplo, se envió 1KB en una dirección, luego 100KB en la otra. En el lado negativo, usar tunnels unidireccionales significa que hay dos conjuntos de peers que necesitan ser perfilados y contabilizados, y se debe tener cuidado adicional para abordar la velocidad aumentada de los ataques de predecesor. El proceso de agrupación y construcción de tunnels (estrategias de selección y ordenamiento de peers) debería minimizar las preocupaciones del ataque de predecesor.

## Anonimato

Un [artículo de Hermann y Grothoff](http://grothoff.org/christian/i2p.pdf) declaró que los tunnels unidireccionales de I2P "parece ser una mala decisión de diseño".

El punto principal del artículo es que las desanonimizaciones en túneles unidireccionales toman más tiempo, lo cual es una ventaja, pero que un atacante puede estar más seguro en el caso unidireccional. Por lo tanto, el artículo afirma que no es una ventaja en absoluto, sino una desventaja, al menos con sitios I2P de larga duración.

Esta conclusión no está completamente respaldada por el artículo. Los tunnels unidireccionales claramente mitigan otros ataques y no está claro cómo equilibrar el riesgo del ataque en el artículo con ataques en una arquitectura de tunnel bidireccional.

Esta conclusión se basa en una ponderación arbitraria (compromiso) entre certeza y tiempo que puede no ser aplicable en todos los casos. Por ejemplo, alguien podría hacer una lista de IPs posibles y luego emitir citaciones judiciales para cada una. O el atacante podría realizar ataques DDoS contra cada una por turnos y mediante un simple ataque de intersección ver si el I2P Site se cae o se ralentiza. Así que estar cerca puede ser suficiente, o el tiempo puede ser más importante.

La conclusión se basa en una ponderación específica de la importancia de la certeza frente al tiempo, y esa ponderación puede ser incorrecta, y definitivamente es debatible, especialmente en un mundo real con citaciones judiciales, órdenes de registro y otros métodos disponibles para la confirmación final.

Un análisis completo de las compensaciones entre tunnels unidireccionales vs. bidireccionales está claramente fuera del alcance del documento, y no se ha realizado en otro lugar. Por ejemplo, ¿cómo se compara este ataque con los numerosos ataques de temporización posibles publicados sobre redes de enrutamiento cebolla? Claramente los autores no han realizado ese análisis, si es que es posible hacerlo de manera efectiva.

Tor usa túneles bidireccionales y ha tenido mucha revisión académica. I2P usa túneles unidireccionales y ha tenido muy poca revisión. ¿La falta de un documento de investigación que defienda los túneles unidireccionales significa que es una mala elección de diseño, o simplemente que necesita más estudio? Los ataques de temporización y ataques distribuidos son difíciles de defender tanto en I2P como en Tor. La intención del diseño (ver referencias arriba) era que los túneles unidireccionales son más resistentes a ataques de temporización. Sin embargo, el documento presenta un tipo algo diferente de ataque de temporización. ¿Es este ataque, tan innovador como es, suficiente para etiquetar la arquitectura de túneles de I2P (y por lo tanto I2P en su conjunto) como un "mal diseño", y por implicación claramente inferior a Tor, o es simplemente una alternativa de diseño que claramente necesita más investigación y análisis? Hay varias otras razones para considerar I2P actualmente inferior a Tor y otros proyectos (tamaño pequeño de red, falta de financiación, falta de revisión) pero ¿son realmente los túneles unidireccionales una razón?

En resumen, "mala decisión de diseño" es aparentemente (ya que el documento no etiqueta los tunnels bidireccionales como "malos") una forma abreviada de decir "los tunnels unidireccionales son inequívocamente inferiores a los tunnels bidireccionales", sin embargo, esta conclusión no está respaldada por el documento.
