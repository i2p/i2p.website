---
title: "I2P no se ve afectado por la vulnerabilidad de log4j"
date: 2021-12-11
author: "idk, zzz"
description: "I2P no utiliza log4j y, por lo tanto, no está afectado por CVE-2021-44228"
categories: ["security"]
API_Translate: verdadero
---

I2P no se ve afectado por la vulnerabilidad de día cero de log4j publicada ayer, CVE-2021-44228. I2P no utiliza log4j para el registro; sin embargo, también fue necesario revisar nuestras dependencias por si usaban log4j, especialmente jetty. Esta revisión no ha revelado ninguna vulnerabilidad.

También fue importante revisar todos nuestros complementos. Los complementos pueden incorporar sus propios sistemas de registro, incluyendo log4j. Comprobamos que la mayoría de los complementos tampoco usan log4j, y que aquellos que sí lo usan no utilizaban una versión vulnerable de log4j.

No hemos encontrado ninguna dependencia, plugin ni aplicación vulnerable.

Incluimos un archivo log4j.properties con jetty para los plugins que incorporan log4j. Este archivo solo tiene efecto en los plugins que usan el registro de log4j internamente. Hemos aplicado la mitigación recomendada en el archivo log4j.properties. Los plugins que habilitan log4j se ejecutarán con la funcionalidad vulnerable desactivada. Como no podemos encontrar ningún uso de log4j 2.x en ninguna parte, no tenemos planes de hacer un lanzamiento de emergencia en este momento.
