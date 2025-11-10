---
title: "Rutas Restringidas"
number: "100"
author: "zzz"
created: "2008-09-14"
lastupdated: "2008-10-13"
status: "Reserva"
thread: "http://zzz.i2p/topics/114"
---

## Introducción


## Pensamientos

- Añadir un nuevo transporte "IND" (indirecto) que publique un hash leaseSet en la
  estructura RouterAddress: "IND: [key=aababababababababb]". Este transporte hace
  la oferta de la prioridad más baja cuando el router de destino lo publica. Para enviar a un par a través de
  este transporte, obtiene el leaseset de un par ff como de costumbre, y lo envía
  directamente al alquiler.

- Un par que publicite IND debe construir y mantener un conjunto de túneles a otro
  par. Estos no son túneles exploratorios ni túneles de cliente, sino un segundo
  conjunto de túneles del router.

  - ¿Es suficiente 1 salto?
  - ¿Cómo seleccionar pares para estos túneles?
  - Necesitan ser "no restringidos", pero ¿cómo sabes eso? ¿Mapeo de accesibilidad?
    La teoría de grafos, algoritmos, estructuras de datos pueden ayudar aquí. Necesito
    leer sobre esto. Ver túneles TODO.

- Si tienes túneles IND, entonces tu transporte IND debe hacer una oferta
  (baja prioridad) para enviar mensajes por estos túneles.

- Cómo decidir habilitar la construcción de túneles indirectos

- Cómo implementar y probar sin comprometer la cobertura
