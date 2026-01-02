---
title: "Enrutamiento Garlic"
description: "Comprendiendo la terminología, arquitectura e implementación moderna del garlic routing en I2P"
slug: "garlic-routing"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

---

## 1. Descripción general

**Garlic routing** sigue siendo una de las innovaciones fundamentales de I2P, combinando cifrado por capas, agrupación de mensajes y túneles unidireccionales. Aunque conceptualmente similar al **enrutamiento cebolla** (onion routing), extiende el modelo al agrupar múltiples mensajes cifrados ("cloves" o dientes) en un único sobre ("garlic" o ajo), mejorando la eficiencia y el anonimato.

El término *garlic routing* fue acuñado por [Michael J. Freedman](https://www.cs.princeton.edu/~mfreed/) en la [Tesis de Maestría de Free Haven de Roger Dingledine](https://www.freehaven.net/papers.html) (junio de 2000, §8.1.1). Los desarrolladores de I2P adoptaron el término a principios de los años 2000 para reflejar sus mejoras de agrupación y modelo de transporte unidireccional, distinguiéndolo del diseño de conmutación de circuitos de Tor.

> **Resumen:** Garlic routing = cifrado en capas + agrupación de mensajes + entrega anónima mediante túneles unidireccionales.

---

## 2. La Terminología "Garlic"

Históricamente, el término *garlic* se ha utilizado en tres contextos diferentes dentro de I2P:

1. **Cifrado por capas** – protección estilo cebolla a nivel de tunnel  
2. **Agrupación de múltiples mensajes** – múltiples "cloves" dentro de un "garlic message"  
3. **Cifrado de extremo a extremo** – anteriormente *ElGamal/AES+SessionTags*, ahora *ECIES‑X25519‑AEAD‑Ratchet*

Aunque la arquitectura permanece intacta, el esquema de cifrado ha sido completamente modernizado.

---

## 3. Cifrado por capas

El garlic routing comparte su principio fundamental con el onion routing: cada router descifra solo una capa de cifrado, conociendo únicamente el siguiente salto y no la ruta completa.

Sin embargo, I2P implementa **túneles unidireccionales**, no circuitos bidireccionales:

- **Tunnel de salida**: envía mensajes desde el creador  
- **Tunnel de entrada**: transporta mensajes de vuelta al creador

Un viaje completo de ida y vuelta (Alice ↔ Bob) utiliza cuatro tunnels: el outbound de Alice → el inbound de Bob, luego el outbound de Bob → el inbound de Alice. Este diseño **reduce a la mitad la exposición de datos de correlación** en comparación con los circuitos bidireccionales.

Para detalles de implementación de túneles, consulta la [Especificación de Túneles](/docs/specs/implementation) y la especificación de [Creación de Túneles (ECIES)](/docs/specs/implementation).

---

## 4. Empaquetado de Múltiples Mensajes (Los "Cloves")

El garlic routing original de Freedman imaginaba agrupar múltiples "bulbos" encriptados dentro de un mensaje. I2P implementa esto como **cloves** (dientes) dentro de un **garlic message** (mensaje garlic) — cada clove tiene sus propias instrucciones de entrega encriptadas y destino (router, destino o tunnel).

El empaquetado garlic (garlic bundling) permite a I2P:

- Combinar confirmaciones y metadatos con mensajes de datos
- Reducir patrones de tráfico observables
- Soportar estructuras de mensajes complejas sin conexiones adicionales

![Garlic Message Cloves](/images/garliccloves.png)   *Figura 1: Un Garlic Message que contiene múltiples cloves, cada uno con sus propias instrucciones de entrega.*

Los dientes típicos incluyen:

1. **Mensaje de Estado de Entrega** — acuses de recibo que confirman el éxito o fracaso de la entrega.  
   Estos se envuelven en su propia capa garlic para preservar la confidencialidad.
2. **Mensaje de Almacenamiento de Base de Datos** — LeaseSets empaquetados automáticamente para que los peers puedan responder sin consultar nuevamente la netDb.

Los cloves se agrupan cuando:

- Se debe publicar un nuevo LeaseSet
- Se entregan nuevas etiquetas de sesión
- No ha ocurrido ningún bundle recientemente (~1 minuto por defecto)

Los mensajes garlic logran una entrega eficiente de extremo a extremo de múltiples componentes cifrados en un solo paquete.

---

## 5. Evolución del Cifrado

### 5.1 Historical Context

La documentación temprana (≤ v0.9.12) describía el cifrado *ElGamal/AES+SessionTags*:   - **ElGamal de 2048 bits** envolvía las claves de sesión AES   - **AES‑256/CBC** para el cifrado de la carga útil   - Etiquetas de sesión de 32 bytes usadas una vez por mensaje

Ese criptosistema está **obsoleto**.

### 5.2 ECIES‑X25519‑AEAD‑Ratchet (Current Standard)

Entre 2019 y 2023, I2P migró completamente a ECIES‑X25519‑AEAD‑Ratchet. La pila moderna estandariza los siguientes componentes:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Layer</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">ECIES Primitive or Concept</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Transport Layer (NTCP2, SSU2)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Noise_NX → X25519, ChaCha20/Poly1305, BLAKE2s</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">I2NP Delivery</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ECIES‑X25519‑AEAD (ChaCha20/Poly1305)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Session Management</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Ratchet with rekey records, per-clove key material</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Offline Authentication</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">EdDSA (Ed25519) with LeaseSet2/MetaLeaseSet chains</td>
    </tr>
  </tbody>
</table>
Beneficios de la migración a ECIES:

- **Secreto hacia adelante** mediante claves de trinquete por mensaje  
- **Tamaño de carga útil reducido** en comparación con ElGamal  
- **Resiliencia** contra avances criptoanalíticos  
- **Compatibilidad** con híbridos post-cuánticos futuros (ver Propuesta 169)

Detalles adicionales: consulte la [Especificación ECIES](/docs/specs/ecies) y la [especificación EncryptedLeaseSet](/docs/specs/encryptedleaseset).

---

## 6. LeaseSets and Garlic Bundling

Los envelopes garlic frecuentemente incluyen LeaseSets para publicar o actualizar la accesibilidad del destino.

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Version</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Key Capabilities</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Distribution Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">LeaseSet (legacy)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Single encryption/signature pair</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Accepted for backward compatibility</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">3</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">LeaseSet2</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Multiple crypto suites, offline signing keys</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Default for modern routers</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">5</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">EncryptedLeaseSet</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Access-controlled, destination hidden from floodfill</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Requires shared decryption key</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">7</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MetaLeaseSet</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Aggregates multiple destinations or multi-homed services</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Extends LeaseSet2 fields recursively</td>
    </tr>
  </tbody>
</table>
Todos los LeaseSets se distribuyen a través de la *floodfill DHT* mantenida por routers especializados. Las publicaciones se verifican, se les añade marca de tiempo y se limita su frecuencia para reducir la correlación de metadatos.

Consulte la [documentación de la Network Database](/docs/specs/common-structures) para más detalles.

---

## 7. Modern “Garlic” Applications within I2P

El cifrado basado en garlic y la agrupación de mensajes se utilizan en toda la pila de protocolos de I2P:

1. **Creación y uso de túneles** — cifrado por capas en cada salto  
2. **Entrega de mensajes de extremo a extremo** — mensajes garlic agrupados con acuse de recibo clonado y cloves de LeaseSet  
3. **Publicación en la base de datos de red** — LeaseSets envueltos en sobres garlic para privacidad  
4. **Transportes SSU2 y NTCP2** — cifrado de capa subyacente usando el framework Noise y primitivas X25519/ChaCha20

El garlic routing es por lo tanto tanto un *método de capas de cifrado* como un *modelo de mensajería de red*.

---

## 6. LeaseSets y Garlic Bundling

El centro de documentación de I2P está [disponible aquí](/docs/), mantenido continuamente. Las especificaciones vigentes relevantes incluyen:

- [Especificación ECIES](/docs/specs/ecies) — ECIES‑X25519‑AEAD‑Ratchet
- [Creación de Tunnel (ECIES)](/docs/specs/implementation) — protocolo moderno de construcción de tunnel
- [Especificación I2NP](/docs/specs/i2np) — formatos de mensaje I2NP
- [Especificación SSU2](/docs/specs/ssu2) — transporte UDP SSU2
- [Estructuras Comunes](/docs/specs/common-structures) — comportamiento de netDb y floodfill

Validación académica: Hoang et al. (IMC 2018, USENIX FOCI 2019) y Muntaka et al. (2025) confirman la estabilidad arquitectónica y la resiliencia operacional del diseño de I2P.

---

## 7. Aplicaciones "Garlic" Modernas dentro de I2P

Propuestas en curso:

- **Propuesta 169:** Híbrida post-cuántica (ML-KEM 512/768/1024 + X25519)  
- **Propuesta 168:** Optimización del ancho de banda de transporte  
- **Actualizaciones de datagramas y streaming:** Gestión mejorada de congestión

Las adaptaciones futuras pueden incluir estrategias adicionales de retardo de mensajes o redundancia multi-túnel a nivel de mensaje garlic, basándose en opciones de entrega no utilizadas descritas originalmente por Freedman.

---

## 8. Documentación Actual y Referencias

- Freedman, M. J. & Dingledine, R. (2000). *Free Haven Master's Thesis,* § 8.1.1. [Free Haven Papers](https://www.freehaven.net/papers.html)  
- [Onion Router Publications](https://www.onion-router.net/Publications.html)  
- [Garlic Routing (Wikipedia)](https://en.wikipedia.org/wiki/Garlic_routing)  
- [Tor Project](https://www.torproject.org/)  
- [Free Haven Anonbib](https://freehaven.net/anonbib/topic.html)  
- Goldschlag, D. M., Reed, M. G., Syverson, P. F. (1996). *Hiding Routing Information.* NRL Publication.

---
