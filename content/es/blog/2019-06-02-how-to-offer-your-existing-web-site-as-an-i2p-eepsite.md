---
title: "Cómo ofrecer su sitio web existente como un I2P eepSite"
date: 2019-06-02
author: "idk"
description: "Ofrecer un espejo de I2P"
categories: ["tutorial"]
---

Esta entrada del blog está pensada como una guía general para mantener un espejo de un servicio de clear-net (Internet convencional) como un eepSite. Amplía la entrada anterior del blog sobre túneles básicos de I2PTunnel.

Por desgracia, probablemente sea imposible cubrir *completamente* todos los casos posibles de cómo hacer que un sitio web existente esté disponible como un eepSite; existe simplemente una variedad demasiado amplia de software del lado del servidor, sin mencionar las peculiaridades prácticas de cualquier implementación concreta de ese software. En su lugar, intentaré transmitir, con la mayor precisión posible, el proceso general para preparar un servicio para su implementación en eepWeb u otros servicios ocultos.

Gran parte de esta guía tratará al lector como un participante en una conversación; en particular, si realmente lo digo en serio, me dirigiré al lector directamente (es decir, usando "tú" en lugar de "uno") y con frecuencia encabezaré secciones con preguntas que creo que el lector podría estar haciéndose. Al fin y al cabo, esto es un "proceso" en el que un administrador debe considerarse "involucrado", igual que al alojar cualquier otro servicio.

**DESCARGOS DE RESPONSABILIDAD:**

Aunque sería estupendo, probablemente me resulte imposible proporcionar instrucciones específicas para cada tipo de software que se pueda usar para alojar sitios web. Por lo tanto, este tutorial requiere algunas suposiciones por parte del autor y, por parte del lector, pensamiento crítico y sentido común. Para dejarlo claro, **he supuesto que la persona que sigue este tutorial ya opera un servicio en la web clara vinculable a una identidad u organización real** y, por lo tanto, simplemente ofrece acceso anónimo y no se anonimiza.

Por lo tanto, **no intenta en absoluto anonimizar** una conexión de un servidor a otro. Si desea operar un servicio oculto nuevo, no vinculable, que aloje contenido no asociado a usted, entonces no debería hacerlo desde su propio servidor clearnet ni desde su propia casa.
