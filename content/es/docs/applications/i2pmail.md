---
title: "I2P Mail (Correo Electrónico Anónimo sobre I2P)"
description: "Una descripción general de los sistemas de correo electrónico dentro de la red I2P — historia, opciones y estado actual"
slug: "i2p-mail"
lastUpdated: "2025-10"
---

## Introducción

I2P proporciona mensajería privada estilo correo electrónico a través del **servicio Postman's Mail.i2p** combinado con **SusiMail**, un cliente de correo web integrado. Este sistema permite a los usuarios enviar y recibir correos electrónicos tanto dentro de la red I2P como hacia/desde el internet regular (clearnet) a través de un puente gateway.

# Glosario de I2P

Este glosario define términos técnicos comúnmente utilizados en la documentación de I2P.

## A

### AddressBook
Un archivo local que mapea nombres legibles para humanos (como example.i2p) a destinos I2P. Similar al archivo hosts en sistemas operativos convencionales.

### Anonymity
El estado de ser anónimo - no identificable dentro de un conjunto de sujetos (el conjunto de anonimato).

## B

### Base32
Una codificación utilizada para representar destinos I2P en un formato más corto y seguro para URL. Los dominios Base32 terminan en `.b32.i2p`.

### Base64
Un esquema de codificación utilizado para representar datos binarios (como claves públicas o destinos) en caracteres ASCII imprimibles.

## C

### Client Application
Cualquier aplicación que utiliza I2P para comunicarse de forma anónima. Ejemplos incluyen navegadores web, clientes de correo electrónico y aplicaciones de compartición de archivos.

### Cryptography
La práctica y estudio de técnicas para comunicación segura en presencia de terceros adversarios.

## D

### Destination
Una identidad criptográfica dentro de I2P. Similar a una dirección IP en Internet, pero incluye claves criptográficas y es permanente.

### DHT (Distributed Hash Table)
Una tabla hash distribuida - una estructura de datos descentralizada utilizada para almacenar pares clave-valor a través de múltiples nodos.

## E

### Eepsite
Un sitio web alojado dentro de la red I2P, accesible solo a través de I2P. El término proviene de los dominios `.eep` utilizados anteriormente.

### Encryption
El proceso de codificar información de manera que solo las partes autorizadas puedan acceder a ella.

## F

### Floodfill
Un router I2P que almacena información de netDb y responde a consultas de búsqueda de otros routers. Los routers floodfill forman la columna vertebral del sistema de búsqueda distribuida de I2P.

## G

### Garlic Encryption
El método de encriptación en capas de I2P, similar a la encriptación onion de Tor pero más flexible. Múltiples mensajes pueden agruparse ("envueltos en ajo") juntos para mayor eficiencia y seguridad.

### Garlic Message
Un mensaje que contiene múltiples "cloves" (mensajes I2NP encriptados) agrupados juntos para eficiencia.

## H

### Hidden Service
Un servicio accesible únicamente dentro de una red de anonimato. En I2P, típicamente se refiere a eepsites u otros servicios I2P.

### Hop
Un salto individual en una ruta de red - el viaje de un paquete de un nodo al siguiente.

## I

### I2CP (I2P Client Protocol)
El protocolo que permite que las aplicaciones cliente se comuniquen con el router I2P.

### I2NP (I2P Network Protocol)
El protocolo de capa de red utilizado para el enrutamiento de mensajes dentro de I2P.

### I2PTunnel
Una herramienta que crea túneles para redirigir tráfico TCP/IP convencional a través de I2P o viceversa.

### Inbound Tunnel
Un túnel utilizado para recibir mensajes de otros routers I2P.

### Inproxy
Un servidor proxy que permite el acceso a contenido I2P desde Internet regular, aunque con garantías de anonimato reducidas.

## J

### Jump Service
Un servicio que resuelve nombres legibles para humanos a destinos I2P, permitiendo a los usuarios compartir enlaces a eepsites más fácilmente.

## K

### Key
Material criptográfico utilizado para cifrado, descifrado, firma o verificación.

## L

### Latency
El tiempo que tarda un mensaje en viajar de origen a destino. I2P típicamente tiene mayor latencia que Internet regular debido al enrutamiento por múltiples saltos.

### Lease
Una asociación temporal entre un gateway de túnel de entrada y un destination. Los leases expiran y deben renovarse periódicamente.

### LeaseSet
Una estructura que contiene los leases de un destination, publicada en netDb para que otros puedan encontrar cómo contactar ese destination.

## M

### Message
Una unidad de comunicación en I2P, típicamente un mensaje I2NP encapsulado dentro de garlic encryption.

### Multihoming
La capacidad de un router I2P de utilizar múltiples túneles simultáneamente para redundancia y equilibrio de carga.

## N

### NetDb (Network Database)
La base de datos distribuida que almacena información del router e información de leaseSet, permitiendo a los routers encontrarse entre sí.

### NTCP2 (NTCPv2)
Un transporte I2P que opera sobre TCP, proporcionando conexiones encriptadas y autenticadas entre routers.

### NTP (Network Time Protocol)
Un protocolo utilizado para sincronizar relojes entre sistemas informáticos. El tiempo preciso es importante para I2P.

## O

### Outbound Tunnel
Un túnel utilizado para enviar mensajes a otros routers I2P.

### Outproxy
Un nodo que permite a los usuarios de I2P acceder a servicios de Internet regular de forma anónima.

## P

### Participant
Un router I2P que forma parte de un túnel pero no es el punto final.

### Peer
Otro router I2P con el que tu router se comunica directamente.

### Prefix
Una porción inicial de un hash de destino o router utilizada para enrutamiento eficiente en netDb.

## Q

### QoS (Quality of Service)
Mecanismos para priorizar cierto tráfico de red y garantizar niveles de rendimiento.

## R

### Reseeding
El proceso de obtener inicialmente información de router de servidores confiables cuando se ejecuta I2P por primera vez o después de estar desconectado por largo tiempo.

### Router
El software principal de I2P que maneja el enrutamiento de mensajes, construcción de túneles y participación en netDb.

### RouterInfo
Una estructura publicada en netDb que contiene la identidad de un router, direcciones de contacto y otra información necesaria para que otros routers se conecten a él.

## S

### SAM (Simple Anonymous Messaging)
Una API basada en sockets que permite que aplicaciones cliente utilicen I2P sin implementar I2CP completo.

### Streaming Library
Una biblioteca que proporciona comunicación similar a TCP confiable sobre I2P.

### SSU (Secure Semireliable UDP)
Un transporte I2P que opera sobre UDP, diseñado para resistir el escaneo de puertos y proporcionar comunicación eficiente.

## T

### Throttling
Limitar intencionalmente la tasa de envío o recepción de datos para gestionar el ancho de banda.

### Tunnel
Una ruta unidireccional a través de múltiples routers I2P utilizada para transmisión anónima de mensajes.

### Tunnel Endpoint
El router final en un túnel - el gateway de entrada para túneles inbound o el origen para túneles outbound.

### Tunnel Gateway
El primer router en un túnel - el punto de entrada para túneles outbound o el destino para túneles inbound.

## U

### UDP (User Datagram Protocol)
Un protocolo de comunicación sin conexión utilizado como base para el transporte SSU.

## V

### Verifier
Código criptográfico utilizado para verificar firmas digitales.

## W

### Whitelist
Una lista de entidades permitidas (como destinos o routers) que tienen permiso para acceder a un recurso o servicio.

## X

### XOR
Una operación lógica (OR exclusivo) utilizada extensivamente en criptografía y operaciones de hash.

## Z

### Zero-day
Una vulnerabilidad de seguridad previamente desconocida que puede ser explotada por atacantes antes de que exista un parche.

---

*Este glosario se actualiza continuamente. Si encuentras términos que faltan o necesitan aclaración, por favor contribuye al proyecto de documentación de I2P.*

## Postman / Mail.i2p + SusiMail

### What it is

- **Mail.i2p** es un proveedor de correo electrónico alojado dentro de I2P, administrado por "Postman"
- **SusiMail** es el cliente de correo web integrado en la consola del router I2P. Está diseñado para evitar la filtración de metadatos (por ejemplo, hostname) a servidores SMTP externos.
- A través de esta configuración, los usuarios de I2P pueden enviar/recibir mensajes tanto dentro de I2P como hacia/desde la clearnet (por ejemplo, Gmail) mediante el puente de Postman.

### How Addressing Works

El correo electrónico de I2P utiliza un sistema de direcciones duales:

- **Dentro de la red I2P**: `username@mail.i2p` (ej., `idk@mail.i2p`)
- **Desde clearnet**: `username@i2pmail.org` (ej., `idk@i2pmail.org`)

El gateway `i2pmail.org` permite a usuarios regulares de internet enviar correos electrónicos a direcciones I2P, y a usuarios de I2P enviar a direcciones de clearnet. Los correos electrónicos de internet se enrutan a través del gateway antes de ser reenviados a través de I2P a tu bandeja de entrada de SusiMail.

**Cuota de envío a Clearnet**: 20 correos electrónicos por día al enviar a direcciones de internet regulares.

### Qué es

**Para registrarse para una cuenta de mail.i2p:**

1. Asegúrate de que tu router I2P esté en funcionamiento
2. Visita **[http://hq.postman.i2p](http://hq.postman.i2p)** dentro de I2P
3. Sigue el proceso de registro
4. Accede a tu correo electrónico a través de **SusiMail** en la consola del router

> **Nota**: `hq.postman.i2p` es una dirección de red I2P (eepsite) y solo se puede acceder mientras esté conectado a I2P. Para más información sobre la configuración, seguridad y uso del correo electrónico, visite Postman HQ.

### Cómo Funciona el Direccionamiento

- Eliminación automática de encabezados identificativos (`User-Agent:`, `X-Mailer:`) para mayor privacidad
- Sanitización de metadatos para prevenir filtraciones hacia servidores SMTP externos
- Cifrado de extremo a extremo para correos internos I2P-a-I2P

### Primeros Pasos

- Interoperabilidad con correo electrónico "normal" (SMTP/POP) a través del puente Postman
- Experiencia de usuario sencilla (webmail integrado en la consola del router)
- Integrado con la distribución principal de I2P (SusiMail se incluye con Java I2P)
- Eliminación de encabezados para protección de la privacidad

### Características de Privacidad

- El puente hacia correo electrónico externo requiere confianza en la infraestructura de Postman
- El puente hacia clearnet reduce la privacidad en comparación con la comunicación puramente interna de I2P
- Depende de la disponibilidad y seguridad del servidor de correo Postman

---


## Technical Details

**Servicio SMTP**: `localhost:7659` (proporcionado por Postman) **Servicio POP3**: `localhost:7660` **Acceso al Webmail**: Integrado en la consola del router en `http://127.0.0.1:7657/susimail/`

> **Importante**: SusiMail es solo para leer y enviar correo electrónico. La creación y gestión de cuentas debe realizarse en **hq.postman.i2p**.

---


## Best Practices

- **Cambia tu contraseña** después de registrar tu cuenta mail.i2p
- **Usa correo electrónico I2P-a-I2P** siempre que sea posible para máxima privacidad (sin puente a clearnet)
- **Ten en cuenta el límite de 20/día** al enviar a direcciones clearnet
- **Comprende las compensaciones**: El puente a clearnet proporciona conveniencia pero reduce el anonimato comparado con comunicaciones puramente internas de I2P
- **Mantén I2P actualizado** para beneficiarte de las mejoras de seguridad en SusiMail

# Guía de configuración de límites de ancho de banda de I2P

## Introducción

I2P permite controlar cuánto ancho de banda utiliza tu router. Configurar estos límites correctamente es crucial para el rendimiento de la red y tu experiencia de usuario.

## Configuración básica

### Límites de ancho de banda compartido

Por defecto, I2P comparte un porcentaje de tu ancho de banda disponible con otros usuarios de la red. Puedes ajustar estos valores en:

`Configuración > Ancho de banda`

**Opciones principales:**

- **Ancho de banda entrante**: Controla cuántos datos puede recibir tu router
- **Ancho de banda saliente**: Controla cuántos datos puede enviar tu router

### Recomendaciones

Para un rendimiento óptimo:

1. Configura al menos 128 KBps para tráfico compartido
2. Reserva ancho de banda adicional para tu uso personal
3. No limites excesivamente - esto afecta la salud de la red

## Configuración avanzada

### Límites de participación

Puedes configurar cuánto de tu ancho de banda se dedica a túneles de tránsito (participación en la red):

```
router.sharePercentage=80
```

Este valor representa el porcentaje de tu ancho de banda total disponible para la red.

### Burst bandwidth

I2P soporta ráfagas temporales de ancho de banda por encima de los límites configurados. Esto mejora el rendimiento durante picos de actividad.

## Consideraciones importantes

- **Conexiones de alta velocidad**: Si tienes > 10 Mbps, considera aumentar tus límites
- **Conexiones lentas**: Con < 1 Mbps, reduce la participación pero mantén el router activo
- **Rendimiento**: Límites más altos = mejor rendimiento personal + red más saludable
- **Privacidad**: Incluso con límites bajos, tu privacidad está protegida

## Monitoreo

Revisa la página de estado del router para verificar:

- Uso actual de ancho de banda
- Número de túneles de tránsito
- Mensajes de participación de la red

## Conclusión

La configuración apropiada de límites de ancho de banda equilibra tu experiencia personal con la contribución a la salud general de la red I2P.
