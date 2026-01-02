---
title: "I2P: Un framework escalable para comunicación anónima"
description: "Introducción técnica a la arquitectura y operación de I2P"
slug: "tech-intro"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

## Introducción

I2P es una capa de red anónima escalable, auto-organizada y resiliente de conmutación de paquetes, sobre la cual puede operar cualquier número de aplicaciones diferentes conscientes del anonimato o la seguridad. Cada una de estas aplicaciones puede realizar sus propias compensaciones entre anonimato, latencia y rendimiento sin preocuparse por la implementación adecuada de un mixnet de ruta libre, permitiéndoles mezclar su actividad con el conjunto de anonimato más amplio de usuarios que ya se ejecutan sobre I2P.

Las aplicaciones ya disponibles proporcionan la gama completa de actividades típicas de Internet — navegación web **anónima**, alojamiento web, chat, compartición de archivos, correo electrónico, blogs y sindicación de contenidos, así como varias otras aplicaciones en desarrollo.

- **Navegación web:** usando cualquier navegador existente que soporte un proxy  
- **Chat:** IRC y otros protocolos  
- **Compartir archivos:** [I2PSnark](#i2psnark) y otras aplicaciones  
- **Correo electrónico:** [Susimail](#i2pmail) y otras aplicaciones  
- **Blog:** usando cualquier servidor web local, o plugins disponibles

A diferencia de los sitios web alojados en redes de distribución de contenido como [Freenet](/docs/overview/comparison#freenet) o [GNUnet](https://www.gnunet.org/), los servicios alojados en I2P son completamente interactivos: hay motores de búsqueda tradicionales estilo web, tableros de anuncios, blogs en los que puedes comentar, sitios basados en bases de datos y puentes para consultar sistemas estáticos como Freenet sin necesidad de instalarlos localmente.

Con todas estas aplicaciones habilitadas para el anonimato, I2P actúa como **middleware orientado a mensajes** — las aplicaciones especifican los datos a enviar a un identificador criptográfico (un "destination"), e I2P asegura que lleguen de forma segura y anónima. I2P también incluye una simple [biblioteca de streaming](#streaming) para permitir que los mensajes anónimos de mejor esfuerzo de I2P se transfieran como flujos confiables y ordenados, ofreciendo control de congestión basado en TCP ajustado para el alto producto ancho de banda-retardo de la red.

Aunque se han desarrollado proxies SOCKS simples para conectar aplicaciones existentes, su valor es limitado ya que la mayoría de las aplicaciones filtran información sensible en un contexto anónimo. El enfoque más seguro es **auditar y adaptar** la aplicación para usar las APIs de I2P directamente.

I2P no es un proyecto de investigación —académico, comercial o gubernamental— sino un esfuerzo de ingeniería orientado a proporcionar anonimato utilizable. Ha estado en desarrollo continuo desde principios de 2003 por un grupo distribuido de colaboradores en todo el mundo. Todo el trabajo de I2P es **código abierto** en el [sitio web oficial](https://geti2p.net/), principalmente liberado al dominio público, con algunos componentes bajo licencias permisivas de estilo BSD. Varias aplicaciones cliente con licencia GPL están disponibles, como [I2PTunnel](#i2ptunnel), [Susimail](#i2pmail) e [I2PSnark](#i2psnark). La financiación proviene únicamente de donaciones de usuarios.

---

## Operación

### Overview

I2P distingue claramente entre routers (nodos que participan en la red) y destinos (endpoints anónimos para aplicaciones). Ejecutar I2P en sí no es secreto; lo que está oculto es **qué** está haciendo el usuario y qué router utilizan sus destinos. Los usuarios finales típicamente ejecutan varios destinos (por ejemplo, uno para navegación web, otro para alojamiento, otro para IRC).

Un concepto clave en I2P es el **tunnel** — una ruta encriptada unidireccional a través de una serie de routers. Cada router solo desencripta una capa y solo conoce el siguiente salto. Los tunnels expiran cada 10 minutos y deben reconstruirse.

![Esquema de túnel entrante y saliente](/images/tunnels.png)   *Figura 1: Existen dos tipos de túneles — entrantes y salientes.*

- **Túneles de salida** envían mensajes desde el creador.  
- **Túneles de entrada** traen mensajes de vuelta al creador.

Combinar estos permite la comunicación bidireccional. Por ejemplo, "Alice" utiliza un tunnel saliente para enviar al tunnel entrante de "Bob". Alice cifra su mensaje con instrucciones de enrutamiento hacia el gateway entrante de Bob.

Otro concepto clave es la **base de datos de red** o **netDb**, que distribuye metadatos sobre routers y destinos:

- **RouterInfo:** Contiene información de contacto del router y material de claves.
- **LeaseSet:** Contiene información necesaria para contactar un destino (gateways de túneles, tiempos de expiración, claves de cifrado).

Los routers publican su RouterInfo directamente en la netDb; los LeaseSets se envían a través de túneles de salida para mantener el anonimato.

Para construir túneles, Alice consulta la netDb en busca de entradas RouterInfo para elegir pares, y envía mensajes de construcción de túnel cifrados salto por salto hasta que el túnel esté completo.

![La información del router se utiliza para construir túneles](/images/netdb_get_routerinfo_2.png)   *Figura 2: La información del router se utiliza para construir túneles.*

Para enviar a Bob, Alice busca el LeaseSet de Bob y utiliza uno de sus túneles de salida para enrutar los datos a través de la puerta de enlace del túnel de entrada de Bob.

![Los LeaseSets conectan túneles de entrada y salida](/images/netdb_get_leaseset.png)   *Figura 3: Los LeaseSets conectan túneles de salida y entrada.*

Debido a que I2P está basado en mensajes, añade **cifrado de ajo de extremo a extremo (end-to-end garlic encryption)** para proteger los mensajes incluso del punto de salida o puerta de entrada. Un mensaje garlic envuelve múltiples "cloves" (mensajes) cifrados para ocultar metadatos y mejorar el anonimato.

Las aplicaciones pueden usar la interfaz de mensajes directamente o depender de la [biblioteca de streaming](#streaming) para conexiones confiables.

---

### Tunnels

Tanto los túneles entrantes como salientes utilizan cifrado por capas, pero difieren en su construcción:

- En **túneles de entrada**, el creador (el endpoint) descifra todas las capas.
- En **túneles de salida**, el creador (el gateway) pre-descifra las capas para asegurar claridad en el endpoint.

I2P perfila a los peers mediante métricas indirectas como latencia y confiabilidad sin sondeo directo. Basándose en estos perfiles, los peers se agrupan dinámicamente en cuatro niveles:

1. Rápido y alta capacidad  
2. Alta capacidad  
3. Sin fallos  
4. Fallando

La selección de pares de túnel típicamente prefiere pares de alta capacidad, elegidos aleatoriamente para equilibrar anonimato y rendimiento, con estrategias adicionales de ordenamiento basadas en XOR para mitigar ataques de predecesor y recolección de netDb.

Para más detalles, consulta la [Especificación de Túneles](/docs/specs/implementation).

---

### Descripción general

Los routers que participan en la tabla hash distribuida (DHT) **floodfill** almacenan y responden a las consultas de LeaseSet. La DHT utiliza una variante de [Kademlia](https://en.wikipedia.org/wiki/Kademlia). Los routers floodfill se seleccionan automáticamente si tienen suficiente capacidad y estabilidad, o pueden configurarse manualmente.

- **RouterInfo:** Describe las capacidades y transportes de un router.  
- **LeaseSet:** Describe los túneles y claves de cifrado de un destino.

Todos los datos en la netDb están firmados por el publicador y tienen una marca de tiempo para prevenir ataques de repetición o de entradas obsoletas. La sincronización temporal se mantiene mediante SNTP y detección de desfase en la capa de transporte.

#### Additional concepts

- **LeaseSets no publicados y cifrados:**  
  Un destino puede permanecer privado al no publicar su LeaseSet, compartiéndolo solo con pares de confianza. El acceso requiere la clave de descifrado apropiada.

- **Bootstrapping (reseeding):**  
  Para unirse a la red, un nuevo router obtiene archivos RouterInfo firmados desde servidores HTTPS de reseed de confianza.

- **Escalabilidad de búsqueda:**  
  I2P utiliza búsquedas **iterativas**, no recursivas, para mejorar la escalabilidad y seguridad del DHT.

---

### Túneles

La comunicación moderna de I2P utiliza dos transportes completamente cifrados:

- **[NTCP2](/docs/specs/ntcp2):** Protocolo cifrado basado en TCP  
- **[SSU2](/docs/specs/ssu2):** Protocolo cifrado basado en UDP

Ambos están construidos sobre el moderno [Noise Protocol Framework](https://noiseprotocol.org/), proporcionando autenticación fuerte y resistencia a la huella digital de tráfico. Reemplazaron los protocolos heredados NTCP y SSU (completamente retirados desde 2023).

**NTCP2** ofrece transmisión cifrada y eficiente sobre TCP.

**SSU2** proporciona confiabilidad basada en UDP, atravesamiento de NAT y perforación de agujeros opcional. SSU2 es conceptualmente similar a WireGuard o QUIC, equilibrando confiabilidad y anonimato.

Los routers pueden soportar tanto IPv4 como IPv6, publicando sus direcciones de transporte y costos en la netDb. El transporte de una conexión se selecciona dinámicamente mediante un **sistema de ofertas** que optimiza según las condiciones y los enlaces existentes.

---

### Base de Datos de Red (netDb)

I2P utiliza criptografía en capas para todos los componentes: transportes, tunnels, mensajes garlic y la base de datos de red (netDb).

Las primitivas actuales incluyen:

- X25519 para intercambio de claves  
- EdDSA (Ed25519) para firmas  
- ChaCha20-Poly1305 para cifrado autenticado  
- SHA-256 para hashing  
- AES256 para cifrado de capa de tunnel

Los algoritmos heredados (ElGamal, DSA-SHA1, ECDSA) se mantienen por compatibilidad con versiones anteriores.

I2P está introduciendo actualmente esquemas criptográficos híbridos post-cuánticos (PQ) que combinan **X25519** con **ML-KEM** para resistir ataques de "recolectar ahora, descifrar después".

#### Garlic Messages

Los mensajes garlic extienden el enrutamiento onion agrupando múltiples "cloves" (dientes) encriptados con instrucciones de entrega independientes. Estos permiten flexibilidad de enrutamiento a nivel de mensaje y relleno de tráfico uniforme.

#### Session Tags

Se admiten dos sistemas criptográficos para el cifrado de extremo a extremo:

- **ElGamal/AES+SessionTags (legacy):**  
  Utiliza etiquetas de sesión pre-entregadas como nonces de 32 bytes. Ahora obsoleto debido a su ineficiencia.

- **ECIES-X25519-AEAD-Ratchet (actual):**  
  Utiliza ChaCha20-Poly1305 y PRNGs basados en HKDF sincronizados para generar claves de sesión efímeras y etiquetas de 8 bytes de forma dinámica, reduciendo la sobrecarga de CPU, memoria y ancho de banda mientras mantiene el secreto hacia adelante (forward secrecy).

---

## Future of the Protocol

Las áreas de investigación clave se centran en mantener la seguridad contra adversarios a nivel estatal e introducir protecciones post-cuánticas. Dos conceptos de diseño tempranos — **rutas restringidas** y **latencia variable** — han sido superados por desarrollos modernos.

### Restricted Route Operation

Los conceptos originales de enrutamiento restringido tenían como objetivo ocultar las direcciones IP. Esta necesidad ha sido en gran medida mitigada por:

- UPnP para reenvío automático de puertos  
- Traversal robusto de NAT en SSU2  
- Soporte para IPv6  
- Introducers cooperativos y perforación de NAT (NAT hole-punching)  
- Conectividad opcional de overlay (p. ej., Yggdrasil)

Por lo tanto, el I2P moderno logra los mismos objetivos de manera más práctica sin el enrutamiento restringido complejo.

---

## Similar Systems

I2P integra conceptos de middleware orientado a mensajes, DHTs (tablas hash distribuidas) y mixnets (redes de mezcla). Su innovación radica en combinar estos elementos en una plataforma de anonimato auto-organizada y utilizable.

### Protocolos de Transporte

*[Sitio web](https://www.torproject.org/)*

**Tor** e **I2P** comparten objetivos pero difieren arquitectónicamente:

- **Tor:** Conmutación de circuitos; depende de autoridades de directorio confiables. (~10k relays)  
- **I2P:** Conmutación de paquetes; red completamente distribuida impulsada por DHT. (~50k routers)

Los túneles unidireccionales de I2P exponen menos metadatos y permiten rutas de enrutamiento flexibles, mientras que Tor se enfoca en el acceso anónimo a **Internet (outproxying)**.   I2P en cambio soporta **alojamiento anónimo dentro de la red**.

### Criptografía

*[Sitio web](https://freenetproject.org/)*

**Freenet** se enfoca en la publicación y recuperación anónima y persistente de archivos. **I2P**, en contraste, proporciona una **capa de comunicaciones en tiempo real** para uso interactivo (web, chat, torrents). Juntos, los dos sistemas se complementan entre sí: Freenet proporciona almacenamiento resistente a la censura; I2P proporciona anonimato en el transporte.

### Other Networks

- **Lokinet:** Superposición basada en IP que utiliza nodos de servicio incentivados.  
- **Nym:** Mixnet de próxima generación que enfatiza la protección de metadatos con tráfico de cobertura a mayor latencia.

---

## Appendix A: Application Layer

I2P en sí solo maneja el transporte de mensajes. La funcionalidad de la capa de aplicación se implementa externamente a través de APIs y bibliotecas.

### Streaming Library {#streaming}

La **biblioteca de streaming** funciona como el análogo TCP de I2P, con un protocolo de ventana deslizante y control de congestión ajustado para transporte anónimo de alta latencia.

Los patrones típicos de solicitud/respuesta HTTP a menudo pueden completarse en un solo viaje de ida y vuelta debido a las optimizaciones de agrupación de mensajes.

### Naming Library and Address Book

*Desarrollado por: mihi, Ragnarok*   Consulta la página [Nomenclatura y Libreta de Direcciones](/docs/overview/naming).

El sistema de nombres de I2P es **local y descentralizado**, evitando nombres globales al estilo DNS. Cada router mantiene un mapeo local de nombres legibles por humanos a destinos. Opcionalmente, se pueden compartir o importar libretas de direcciones basadas en web-of-trust desde pares de confianza.

Este enfoque evita las autoridades centralizadas y elude las vulnerabilidades Sybil inherentes a los sistemas de nomenclatura globales o basados en votación.

### Operación de Ruta Restringida

*Desarrollado por: mihi*

**I2PTunnel** es la interfaz principal de la capa de cliente que permite el proxy TCP anónimo. Admite:

- **Túneles de cliente** (salida hacia destinos I2P)  
- **Cliente HTTP (eepproxy)** para dominios ".i2p"  
- **Túneles de servidor** (entrada desde I2P hacia un servicio local)  
- **Túneles de servidor HTTP** (proxy seguro de servicios web)

El outproxying (hacia Internet regular) es opcional, implementado por túneles "servidor" administrados por voluntarios.

### I2PSnark {#i2psnark}

*Desarrollado por: jrandom, et al — portado desde [Snark](http://www.klomp.org/snark/)*

Incluido con I2P, **I2PSnark** es un cliente BitTorrent anónimo multi-torrent con soporte DHT y UDP, accesible a través de una interfaz web.

### Tor

*Desarrollado por: postman, susi23, mastiejaner*

**I2Pmail** proporciona correo electrónico anónimo a través de conexiones I2PTunnel. **Susimail** es un cliente basado en web diseñado específicamente para prevenir filtraciones de información comunes en los clientes de correo electrónico tradicionales. El servicio [mail.i2p](https://mail.i2p/) cuenta con filtrado de virus, cuotas de [hashcash](https://en.wikipedia.org/wiki/Hashcash) y separación de outproxy para protección adicional.

---
