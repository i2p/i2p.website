---
title: "Capa de transporte"
description: "Comprender la capa de transporte de I2P - métodos de comunicación punto a punto entre routers, incluyendo NTCP2 y SSU2"
slug: "transport"
lastUpdated: "2025-03"
accurateFor: "2.10.0"
---

---

## 1. Descripción general

Un **transporte** en I2P es un método de comunicación directa, punto a punto, entre routers. Estos mecanismos garantizan la confidencialidad y la integridad, a la vez que verifican la autenticación de los routers.

Cada transporte funciona con paradigmas de conexión que incluyen autenticación, control de flujo, acuses de recibo y capacidades de retransmisión.

---

## 2. Transportes actuales

Actualmente, I2P admite dos transportes principales:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Transport</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Protocol</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>NTCP2</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">TCP</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Noise-based TCP transport with modern encryption (as of 0.9.36)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>SSU2</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">UDP</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Secure Semireliable UDP with modern encryption (as of 0.9.56)</td>
    </tr>
  </tbody>
</table>
### 2.1 Transportes heredados (obsoletos)

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Transport</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Protocol</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Status</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>NTCP</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">TCP</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Replaced by NTCP2; removed in 0.9.62</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>SSU</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">UDP</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Replaced by SSU2; removed in 0.9.62</td>
    </tr>
  </tbody>
</table>
---

## 3. Servicios de transporte

El subsistema de transporte proporciona los siguientes servicios:

### 3.1 Entrega de mensajes

- Entrega fiable de mensajes [I2NP](/docs/specs/i2np/) (los transportes gestionan la mensajería I2NP exclusivamente)
- La entrega en orden **NO está garantizada** universalmente
- Encolado de mensajes basado en prioridad

### 3.2 Gestión de conexiones

- Establecimiento y cierre de conexiones
- Gestión de límites de conexión con cumplimiento de umbrales
- Seguimiento del estado por par
- Aplicación, automática y manual, de la lista de bloqueo de pares

### 3.3 Configuración de red

- Múltiples direcciones del router para cada transporte (compatibilidad con IPv4 e IPv6 desde v0.9.8)
- Apertura de puertos del cortafuegos mediante UPnP
- Soporte para el atravesamiento de NAT/cortafuegos
- Detección de la dirección IP local mediante múltiples métodos

### 3.4 Seguridad

- Cifrado para intercambios punto a punto
- Validación de direcciones IP según las reglas locales
- Determinación del consenso del reloj (respaldo NTP)

### 3.5 Gestión del ancho de banda

- Límites de ancho de banda de entrada y salida
- Selección óptima de transporte para mensajes salientes

---

## 4. Direcciones de transporte

El subsistema mantiene una lista de puntos de contacto del router:

- Método de transporte (NTCP2, SSU2)
- Dirección IP
- Número de puerto
- Parámetros opcionales

Se pueden usar múltiples direcciones por método de transporte.

### 4.1 Configuraciones comunes de direcciones

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Configuration</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Hidden</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Routers with no published addresses</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Firewalled</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Routers publishing SSU2 addresses with "introducer" peer lists for NAT traversal</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Unrestricted</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Routers advertising both NTCP2 and SSU2 addresses on IPv4 and/or IPv6</td>
    </tr>
  </tbody>
</table>
---

## 5. Selección de transporte

El sistema selecciona los transportes para [mensajes I2NP](/docs/specs/i2np/) independientemente de los protocolos de capa superior. La selección emplea un **sistema de pujas** en el que cada transporte presenta pujas; gana la de menor valor.

### 5.1 Factores para determinar la puja

- Configuración de preferencias de transporte
- Conexiones con pares existentes
- Número de conexiones actual frente al umbral
- Historial reciente de intentos de conexión
- Restricciones de tamaño de mensaje
- Capacidades de transporte del RouterInfo (metadatos del router) del par
- Directitud de la conexión (directa frente a dependiente de introducer (nodo introductor))
- Preferencias de transporte anunciadas por el par

Generalmente, dos routers mantienen conexiones de un solo transporte simultáneamente, aunque son posibles conexiones simultáneas de múltiples transportes.

---

## 6. NTCP2

**NTCP2** (New Transport Protocol 2) es el transporte moderno basado en TCP para I2P, introducido en la versión 0.9.36.

### 6.1 Características clave

- Basado en el **Noise Protocol Framework** (patrón Noise_XK)
- Usa **X25519** para el intercambio de claves
- Usa **ChaCha20/Poly1305** para cifrado autenticado
- Usa **BLAKE2s** para el cálculo de hash
- Ofuscación del protocolo para resistir DPI (inspección profunda de paquetes)
- Relleno opcional para resistir el análisis de tráfico

### 6.2 Establecimiento de la conexión

1. **Solicitud de sesión** (Alice → Bob): Clave X25519 efímera + carga útil cifrada
2. **Sesión creada** (Bob → Alice): Clave efímera + confirmación cifrada
3. **Sesión confirmada** (Alice → Bob): Negociación final con RouterInfo (información del router)

Todos los datos posteriores se cifran con claves de sesión derivadas de la negociación inicial.

Consulte la [Especificación de NTCP2](/docs/specs/ntcp2/) para obtener todos los detalles.

---

## 7. SSU2

**SSU2** (UDP seguro semiconfiable 2) es el transporte moderno basado en UDP para I2P, introducido en la versión 0.9.56.

### 7.1 Características clave

- Basado en el **Noise Protocol Framework** (marco de protocolos Noise) (Noise_XK pattern)
- Usa **X25519** para el intercambio de claves
- Usa **ChaCha20/Poly1305** para cifrado autenticado
- Entrega parcialmente fiable con acuses de recibo selectivos
- Atravesamiento de NAT mediante hole punching (técnica de perforación de puertos) y relé/introducción
- Soporte para migración de conexiones
- Descubrimiento de MTU de ruta

### 7.2 Ventajas frente a SSU (legado)

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Feature</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">SSU (Legacy)</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">SSU2</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Encryption</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ElGamal + AES</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">X25519 + ChaCha20/Poly1305</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Header encryption</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Partial</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Full (ChaCha20)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Connection ID</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Fixed</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Encrypted, rotatable</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">NAT traversal</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Basic introduction</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Enhanced hole punching + relay</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Obfuscation</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Minimal</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Improved (variable padding)</td>
    </tr>
  </tbody>
</table>
Consulta la [Especificación de SSU2](/docs/specs/ssu2/) para obtener todos los detalles.

---

## 8. Atravesamiento de NAT

Ambos transportes admiten el atravesamiento de NAT para permitir que los routers detrás de un cortafuegos participen en la red.

### 8.1 Introducción a SSU2

Cuando un router no puede recibir conexiones entrantes directamente:

1. El router publica direcciones de **introducer** en su RouterInfo
2. El par que se conecta envía una solicitud de introducción al introducer
3. El introducer reenvía la información de la conexión al router detrás de un cortafuegos
4. El router detrás de un cortafuegos inicia una conexión saliente (hole punch: perforación de NAT)
5. Se establece comunicación directa

### 8.2 NTCP2 y cortafuegos

NTCP2 requiere conectividad TCP entrante. Los routers detrás de NAT pueden:

- Usar UPnP para abrir puertos automáticamente
- Configurar manualmente el reenvío de puertos
- Confiar en SSU2 para las conexiones entrantes mientras se usa NTCP2 para las salientes

---

## 9. Ofuscación del protocolo

Ambos transportes modernos incorporan características de ofuscación:

- **Relleno aleatorio** en los mensajes de negociación
- **Encabezados cifrados** que no revelan firmas del protocolo
- **Mensajes de longitud variable** para resistir el análisis de tráfico
- **Sin patrones fijos** en el establecimiento de la conexión

> **Nota**: La ofuscación en la capa de transporte complementa, pero no reemplaza el anonimato proporcionado por la arquitectura de tunnel de I2P.

---

## 10. Desarrollo futuro

Las investigaciones y mejoras planificadas incluyen:

- **Transportes conectables** – Complementos de ofuscación compatibles con Tor
- **Transporte basado en QUIC** – Investigación de los beneficios del protocolo QUIC
- **Optimización del límite de conexiones** – Investigación sobre límites óptimos de conexiones con pares
- **Estrategias de relleno mejoradas** – Mayor resistencia al análisis de tráfico

---

## 11. Referencias

- [NTCP2 Specification](/docs/specs/ntcp2/) – Transporte TCP basado en Noise (framework criptográfico)
- [SSU2 Specification](/docs/specs/ssu2/) – UDP 2 seguro y semiconfiable
- [I2NP Specification](/docs/specs/i2np/) – Mensajes del Protocolo de Red de I2P
- [Common Structures](/docs/specs/common-structures/) – RouterInfo y estructuras de direcciones
- [Historical NTCP Discussion](/docs/ntcp/) – Historia del desarrollo del transporte heredado
- [Legacy SSU Documentation](/docs/legacy/ssu/) – Especificación original de SSU (obsoleta)
