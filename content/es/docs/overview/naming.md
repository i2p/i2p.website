---
title: "Nomenclatura y Libreta de Direcciones"
description: "Cómo I2P mapea nombres de host legibles por humanos a destinos"
slug: "naming"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

Las direcciones I2P son claves criptográficas largas. El sistema de nombres proporciona una capa más amigable sobre esas claves **sin introducir una autoridad central**. Todos los nombres son **locales**: cada router decide de forma independiente a qué destino se refiere un nombre de host.

> **¿Necesitas contexto?** La [discusión sobre nombres](/docs/legacy/naming/) documenta los debates de diseño originales, propuestas alternativas y fundamentos filosóficos detrás del sistema de nombres descentralizado de I2P.

---

## 1. Componentes

La capa de nombres de I2P está compuesta por varios subsistemas independientes pero cooperantes:

1. **Servicio de nombres** – resuelve nombres de host a destinos y maneja [nombres de host Base32](#base32-hostnames).
2. **Proxy HTTP** – pasa las búsquedas `.i2p` al router y sugiere servicios jump cuando un nombre es desconocido.
3. **Servicios host-add** – formularios estilo CGI que añaden nuevas entradas en la libreta de direcciones local.
4. **Servicios jump** – ayudantes remotos que devuelven el destino para un nombre de host proporcionado.
5. **Libreta de direcciones** – obtiene y fusiona periódicamente listas de hosts remotas usando una "red de confianza" localmente confiable.
6. **SusiDNS** – una interfaz web para gestionar libretas de direcciones, suscripciones y anulaciones locales.

Este diseño modular permite a los usuarios definir sus propios límites de confianza y automatizar tanto o tan poco del proceso de nomenclatura como prefieran.

---

## 2. Servicios de Nombres

La API de nombres del router (`net.i2p.client.naming`) soporta múltiples backends a través de la propiedad configurable `i2p.naming.impl=<class>`. Cada implementación puede ofrecer diferentes estrategias de búsqueda, pero todas comparten el mismo modelo de confianza y resolución.

### 2.1 Hosts.txt (legacy format)

El modelo heredado utilizaba tres archivos de texto plano verificados en orden:

1. `privatehosts.txt`
2. `userhosts.txt`
3. `hosts.txt`

Cada línea almacena un mapeo `hostname=base64-destination`. Este formato de texto simple sigue siendo totalmente compatible para importar/exportar, pero ya no es el predeterminado debido al bajo rendimiento una vez que la lista de hosts supera unos pocos miles de entradas.

---

### 2.2 Blockfile Naming Service (default backend)

Introducido en la **versión 0.8.8**, el Blockfile Naming Service es ahora el backend predeterminado. Reemplaza los archivos planos con un almacén de clave/valor en disco de alto rendimiento basado en skiplist (`hostsdb.blockfile`) que ofrece búsquedas aproximadamente **10× más rápidas**.

**Características clave:** - Almacena múltiples libretas de direcciones lógicas (privada, usuario y hosts) en una base de datos binaria. - Mantiene compatibilidad con importación/exportación del formato heredado hosts.txt. - Admite búsquedas inversas, metadatos (fecha de agregado, origen, comentarios) y caché eficiente. - Utiliza el mismo orden de búsqueda de tres niveles: privada → usuario → hosts.

Este enfoque preserva la compatibilidad con versiones anteriores mientras mejora drásticamente la velocidad de resolución y la escalabilidad.

---

### 2.1 Hosts.txt (formato heredado)

Los desarrolladores pueden implementar backends personalizados tales como: - **Meta** – agrega múltiples sistemas de nombres. - **PetName** – soporta petnames almacenados en un `petnames.txt`. - **AddressDB**, **Exec**, **Eepget**, y **Dummy** – para resolución externa o de respaldo.

La implementación de blockfile sigue siendo el backend **recomendado** para uso general debido a su rendimiento y confiabilidad.

---

## 3. Base32 Hostnames

Los nombres de host Base32 (`*.b32.i2p`) funcionan de manera similar a las direcciones `.onion` de Tor. Cuando accedes a una dirección `.b32.i2p`:

1. El router decodifica la carga útil Base32.
2. Reconstruye el destino directamente desde la clave—**no se requiere búsqueda en la libreta de direcciones**.

Esto garantiza la accesibilidad incluso si no existe un nombre de host legible por humanos. Los nombres Base32 extendidos introducidos en la **versión 0.9.40** admiten **LeaseSet2** y destinos cifrados.

---

## 4. Address Book & Subscriptions

La aplicación de libreta de direcciones recupera listas de hosts remotos a través de HTTP y las fusiona localmente según las reglas de confianza configuradas por el usuario.

### 2.2 Servicio de Nombres Blockfile (backend predeterminado)

- Las suscripciones son URLs `.i2p` estándar que apuntan a `hosts.txt` o feeds de actualización incremental.
- Las actualizaciones se obtienen periódicamente (cada hora por defecto) y se validan antes de fusionarse.
- Los conflictos se resuelven **por orden de llegada**, siguiendo el orden de prioridad:  
  `privatehosts.txt` → `userhosts.txt` → `hosts.txt`.

#### Default Providers

Desde **I2P 2.3.0 (junio de 2023)**, se incluyen dos proveedores de suscripción predeterminados: - `http://i2p-projekt.i2p/hosts.txt` - `http://notbob.i2p/hosts.txt`

Esta redundancia mejora la fiabilidad mientras preserva el modelo de confianza local. Los usuarios pueden agregar o eliminar suscripciones a través de SusiDNS.

#### Incremental Updates

Las actualizaciones incrementales se obtienen mediante `newhosts.txt` (reemplazando el concepto anterior de `recenthosts.cgi`). Este endpoint proporciona actualizaciones delta eficientes **basadas en ETag**, devolviendo solo las entradas nuevas desde la última solicitud o `304 Not Modified` cuando no hay cambios.

---

### 2.3 Backends Alternativos y Complementos

- **Servicios Host-add** (`add*.cgi`) permiten el envío manual de mapeos de nombre a destino. Verifica siempre el destino antes de aceptar.  
- **Servicios Jump** responden con la clave apropiada y pueden redirigir a través del proxy HTTP con un parámetro `?i2paddresshelper=`.  
  Ejemplos comunes: `stats.i2p`, `identiguy.i2p`, y `notbob.i2p`.  
  Estos servicios **no son autoridades de confianza**—los usuarios deben decidir cuáles usar.

---

## 5. Managing Entries Locally (SusiDNS)

SusiDNS está disponible en: `http://127.0.0.1:7657/susidns/`

Puedes: - Ver y editar libretas de direcciones locales. - Gestionar y priorizar suscripciones. - Importar/exportar listas de hosts. - Configurar horarios de actualización.

**Nuevo en I2P 2.8.1 (Marzo 2025):** - Se agregó una función de "ordenar por más reciente". - Se mejoró el manejo de suscripciones (corrección para inconsistencias de ETag).

Todos los cambios permanecen **locales**: la libreta de direcciones de cada router es única.

---

## 3. Nombres de Host Base32

Siguiendo la RFC 9476, I2P registró **`.i2p.alt`** con la GNUnet Assigned Numbers Authority (GANA) a partir de **marzo de 2025 (I2P 2.8.1)**.

**Propósito:** Prevenir filtraciones accidentales de DNS por software mal configurado.

- Los resolvers DNS conformes con RFC 9476 **no reenviarán** dominios `.alt` al DNS público.
- El software I2P trata `.i2p.alt` como equivalente a `.i2p`, eliminando el sufijo `.alt` durante la resolución.
- `.i2p.alt` **no** está destinado a reemplazar `.i2p`; es una medida de seguridad técnica, no un cambio de marca.

---

## 4. Libreta de Direcciones y Suscripciones

- **Claves de destino:** 516–616 bytes (Base64)  
- **Nombres de host:** Máximo 67 caracteres (incluyendo `.i2p`)  
- **Caracteres permitidos:** a–z, 0–9, `-`, `.` (sin puntos dobles, sin mayúsculas)  
- **Reservado:** `*.b32.i2p`  
- **ETag y Last-Modified:** utilizados activamente para minimizar el ancho de banda  
- **Tamaño promedio de hosts.txt:** ~400 KB para ~800 hosts (cifra de ejemplo)  
- **Uso de ancho de banda:** ~10 bytes/seg si se obtiene cada 12 horas

---

## 8. Security Model and Philosophy

I2P intencionalmente sacrifica la unicidad global a cambio de descentralización y seguridad—una aplicación directa del **Triángulo de Zooko**.

**Principios clave:** - **Sin autoridad central:** todas las búsquedas son locales.   - **Resistencia al secuestro de DNS:** las consultas están cifradas hacia las claves públicas de destino.   - **Prevención de ataques Sybil:** sin votación ni nomenclatura basada en consenso.   - **Mapeos inmutables:** una vez que existe una asociación local, no puede ser anulada remotamente.

Los sistemas de nombres basados en blockchain (por ejemplo, Namecoin, ENS) han explorado resolver los tres lados del triángulo de Zooko, pero I2P intencionalmente los evita debido a la latencia, complejidad e incompatibilidad filosófica con su modelo de confianza local.

---

## 9. Compatibility and Stability

- No se han descontinuado funciones de nombres entre 2023–2025.
- El formato hosts.txt, servicios de salto, suscripciones y todas las implementaciones de la API de nombres permanecen funcionales.
- El Proyecto I2P mantiene una estricta **compatibilidad hacia atrás** mientras introduce mejoras de rendimiento y seguridad (aislamiento de NetDB, separación de Sub-DB, etc.).

---

## 10. Best Practices

- Mantén solo suscripciones de confianza; evita listas de hosts grandes y desconocidas.
- Haz una copia de seguridad de `hostsdb.blockfile` y `privatehosts.txt` antes de actualizar o reinstalar.
- Revisa regularmente los servicios de salto y desactiva aquellos en los que ya no confíes.
- Recuerda: tu libreta de direcciones define tu versión del mundo I2P—**cada nombre de host es local**.

---

### Further Reading

- [Discusión sobre Naming](/docs/legacy/naming/)  
- [Especificación de Blockfile](/docs/specs/blockfile/)  
- [Formato del Archivo de Configuración](/docs/specs/configuration/)  
- [Javadoc del Servicio de Naming](http://idk.i2p/javadoc-i2p/net/i2p/client/naming/package-summary.html)

---
