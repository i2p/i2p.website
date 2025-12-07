---
title: "Investigación Académica"
description: "Información y pautas para la investigación académica en la red I2P"
layout: "research"
---

<div id="intro"></div>

## Investigación Académica en I2P

Existe una gran comunidad de investigación que investiga una amplia gama de aspectos de anonimato. Creemos que es esencial comprender los problemas que se enfrentan para que las redes de anonimato continúen mejorando. La investigación en la red I2P aún está en sus inicios, y gran parte del trabajo de investigación hasta ahora se ha centrado en otras redes de anonimato. Esto presenta una oportunidad única para contribuciones de investigación original.

<div id="notes"></div>

## Notas para Investigadores

### Prioridades de Investigación Defensiva

Damos la bienvenida a investigaciones que nos ayuden a fortalecer la red y mejorar su seguridad. Se fomenta y agradece la realización de pruebas que refuercen la infraestructura de I2P.

### Pautas de Comunicación para Investigadores

Animamos encarecidamente a los investigadores a comunicar sus ideas de investigación pronto al equipo de desarrollo. Esto ayuda a:

- Evitar posibles superposiciones con proyectos existentes
- Minimizar posibles daños a la red
- Coordinar esfuerzos de pruebas y recolección de datos
- Asegurar que la investigación se alinee con los objetivos de la red

<div id="ethics"></div>

## Ética de Investigación y Pautas de Pruebas

### Principios Generales

Al realizar investigaciones en I2P, considere lo siguiente:

1. **Evaluar beneficios vs. riesgos de la investigación** - Considere si los beneficios potenciales de su investigación superan los riesgos para la red o sus usuarios
2. **Preferir la red de pruebas sobre la red en vivo** - Utilice la configuración de red de pruebas de I2P siempre que sea posible
3. **Recoger únicamente los datos necesarios mínimos** - Solo recoja la cantidad mínima de datos requerida para su investigación
4. **Asegurar que los datos publicados respeten la privacidad del usuario** - Cualquier dato publicado debe ser anonimizado y respetar la privacidad del usuario

### Métodos de Prueba de la Red

Para investigadores que necesiten realizar pruebas en I2P:

- **Utilizar la configuración de la red de pruebas** - I2P se puede configurar para ejecutarse en una red de pruebas aislada
- **Utilizar el modo MultiRouter** - Ejecutar múltiples instancias de enrutadores en una sola máquina para pruebas
- **Configurar una familia de enrutadores** - Hacer que sus enrutadores de investigación sean identificables configurándolos como una familia de enrutadores

### Prácticas Recomendadas

- **Contactar al equipo de I2P antes de realizar pruebas en la red en vivo** - Póngase en contacto con nosotros en research@i2p.net antes de realizar cualquier prueba en la red en vivo
- **Usar configuración de familia de enrutadores** - Esto hace que sus enrutadores de investigación sean transparentes para la red
- **Prevenir interferencias potenciales en la red** - Diseñe sus pruebas para minimizar cualquier impacto negativo en los usuarios regulares

<div id="questions"></div>

## Preguntas Abiertas de Investigación

La comunidad de I2P ha identificado varias áreas donde la investigación sería particularmente valiosa:

### Base de Datos de la Red

**Floodfills:**
- ¿Existen otras formas de mitigar el ataque de fuerza bruta en la red mediante un control significativo de floodfill?
- ¿Existe alguna forma de detectar, marcar y potencialmente eliminar 'malos floodfills' sin necesidad de depender de una forma de autoridad central?

### Transportes

- ¿Cómo se podrían mejorar las estrategias de retransmisión de paquetes y los tiempos de espera?
- ¿Hay una forma para que I2P confunda los paquetes y reduzca el análisis de tráfico de manera más eficiente?

### Túneles y Destinos

**Selección de Pares:**
- ¿Hay una forma en que I2P podría realizar la selección de pares de manera más eficiente o segura?
- ¿Priorizar pares cercanos usando geoip afectaría negativamente al anonimato?

**Túneles Unidireccionales:**
- ¿Cuáles son los beneficios de los túneles unidireccionales frente a los bidireccionales?
- ¿Cuáles son las compensaciones entre túneles unidireccionales y bidireccionales?

**Multihoming:**
- ¿Qué tan efectivo es el multihoming en el balanceo de carga?
- ¿Cómo se escala?
- ¿Qué sucede cuando más enrutadores alojan el mismo Destino?
- ¿Cuáles son las compensaciones de anonimato?

### Enrutamiento de Mensajes

- ¿Cuánto se reduce la efectividad de los ataques de temporización mediante la fragmentación y mezcla de mensajes?
- ¿De qué técnicas de mezcla podría beneficiarse I2P?
- ¿Cómo se pueden emplear efectivamente técnicas de alta latencia dentro o junto a nuestra red de baja latencia?

### Anonimato

- ¿Qué impacto tiene el fingerprinting del navegador en el anonimato de los usuarios de I2P?
- ¿Desarrollar un paquete de navegador beneficiaría a los usuarios promedio?

### Relacionado con la Red

- ¿Cuál es el impacto general en la red creado por 'usuarios codiciosos'?
- ¿Serían valiosos pasos adicionales para fomentar la participación en el ancho de banda?

<div id="contact"></div>

## Contacto

Para consultas de investigación, oportunidades de colaboración, o para discutir sus planes de investigación, por favor contáctenos en:

**Correo Electrónico:** research@i2p.net

¡Esperamos trabajar con la comunidad de investigación para mejorar la red I2P!