---
title: "Guía de operaciones de Tunnel"
description: "Especificación unificada para la creación, el cifrado y el transporte de tráfico con I2P tunnels."
slug: "implementation"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
type: docs
reviewStatus: "needs-review"
---

> **Alcance:** Esta guía consolida la implementación de tunnel, el formato de mensaje y ambas especificaciones de creación de tunnel (ECIES y ElGamal heredado). Los enlaces profundos existentes siguen funcionando a través de los alias mencionados arriba.

## Modelo de tunnel {#tunnel-model}

I2P reenvía cargas útiles a través de *tunnels unidireccionales*: conjuntos ordenados de routers que transportan tráfico en una sola dirección. Un viaje de ida y vuelta completo entre dos destinos requiere cuatro tunnels (dos de salida, dos de entrada).

Comienza con la [Descripción general de Tunnel](/docs/overview/tunnel-routing/) (túneles de I2P) para la terminología, luego usa esta guía para los detalles operativos.

### Ciclo de vida del mensaje {#message-lifecycle}

1. La **puerta de enlace** del tunnel agrupa en lotes uno o más mensajes I2NP, los fragmenta y escribe instrucciones de entrega.
2. La puerta de enlace encapsula la carga útil en un mensaje de tunnel de tamaño fijo (1024&nbsp;B), añadiendo relleno si es necesario.
3. Cada **participante** verifica el salto anterior, aplica su capa de cifrado y reenvía {nextTunnelId, nextIV, encryptedPayload} al siguiente salto.
4. El **extremo** del tunnel elimina la capa final, consume las instrucciones de entrega, reensambla los fragmentos y envía los mensajes I2NP reconstruidos.

La detección de duplicados utiliza un filtro de Bloom con decaimiento, indexado por el XOR del IV (vector de inicialización) y el primer bloque de cifrado, para impedir ataques de etiquetado basados en intercambios de IV.

### Roles de un vistazo {#roles}

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Role</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Pre-processing</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Crypto Operation</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Post-processing</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Outbound gateway (creator)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Fragment, batch, pad</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Iteratively <em>decrypt</em> using every hop’s keys (so downstream peers encrypt)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Forward to first hop</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Participant</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">—</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Encrypt IV and payload with hop keys</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Forward to next hop</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Outbound endpoint</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">—</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Encrypt once more to reveal plaintext payload</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deliver to target tunnel/destination</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Inbound gateway</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Fragment, batch, pad</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Encrypt with local keys</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Forward to next hop</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Inbound endpoint (creator)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">—</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Iteratively decrypt using stored hop keys</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reassemble and deliver locally</td>
    </tr>
  </tbody>
</table>
### Flujo de trabajo de cifrado {#encryption-workflow}

- **Tunnels entrantes:** la puerta de enlace cifra una vez con su clave de capa; los participantes posteriores siguen cifrando hasta que el creador descifra la carga útil final.
- **Tunnels salientes:** la puerta de enlace aplica previamente la inversa del cifrado de cada salto para que cada participante cifre. Cuando el extremo cifra, se revela el texto en claro original de la puerta de enlace.

Ambas direcciones reenvían `{tunnelId, IV, encryptedPayload}` al siguiente salto.

---

## Formato del mensaje de Tunnel {#tunnel-message-format}

Las puertas de enlace del tunnel fragmentan los mensajes I2NP en envolturas de tamaño fijo para ocultar la longitud de la carga útil y simplificar el procesamiento salto a salto.

### Diseño cifrado {#encrypted-layout}

```
+----------------+----------------+-------------------+
| Tunnel ID (4B) | IV (16B)       | Encrypted payload |
+----------------+----------------+-------------------+
```
- **Tunnel ID** – identificador de 32 bits para el siguiente salto (no es cero; rota en cada ciclo de construcción).
- **IV** – IV de AES de 16 bytes seleccionado para cada mensaje.
- **Carga útil cifrada** – 1008 bytes de texto cifrado AES-256-CBC.

Tamaño total: 1028 bytes.

### Diseño descifrado {#decrypted-layout}

Después de que un salto retira su capa de cifrado:

```
[Checksum (4B)][Padding ... 0x00 terminator]
[Delivery Instructions 1][I2NP fragment 1]
[Delivery Instructions 2][I2NP fragment 2]
...
```
- **Suma de verificación** valida el bloque descifrado.
- **Relleno** es una secuencia de bytes aleatorios distintos de cero, terminada por un byte cero.
- **Instrucciones de entrega** indican al extremo cómo manejar cada fragmento (entregar localmente, reenviar a otro tunnel, etc.).
- **Fragmentos** transportan los mensajes I2NP subyacentes; el extremo los reensambla antes de pasarlos a capas superiores.

### Pasos de procesamiento {#processing-steps}

1. Las puertas de enlace fragmentan y ponen en cola mensajes I2NP, reteniendo brevemente fragmentos parciales para su reensamblaje.
2. La puerta de enlace cifra la carga útil con las claves de capa apropiadas e inserta el ID del tunnel más el IV (vector de inicialización).
3. Cada participante cifra el IV (AES-256/ECB) y luego la carga útil (AES-256/CBC) antes de volver a cifrar el IV y reenviar el mensaje.
4. El extremo descifra en orden inverso, verifica la suma de verificación, procesa las instrucciones de entrega y reensambla los fragmentos.

---

## Creación de Tunnel (ECIES-X25519) {#tunnel-creation-ecies}

Los routers modernos construyen tunnels con claves ECIES-X25519, reduciendo el tamaño de los mensajes de construcción (build messages) y permitiendo secreto hacia adelante.

- **Mensaje de construcción:** un único mensaje I2NP `TunnelBuild` (o `VariableTunnelBuild`) transporta de 1–8 registros de construcción cifrados, uno por salto.
- **Claves de capa:** los creadores derivan, por salto, las claves de capa, IV (vector de inicialización) y de respuesta mediante HKDF (función de derivación de claves basada en HMAC) usando la identidad estática X25519 del salto y la clave efímera del creador.
- **Procesamiento:** cada salto descifra su registro, valida las banderas de la solicitud, escribe el bloque de respuesta (éxito o código de fallo detallado), vuelve a cifrar los registros restantes y reenvía el mensaje.
- **Respuestas:** el creador recibe un mensaje de respuesta envuelto con garlic encryption (técnica de cifrado y encapsulado propia de I2P). Los registros marcados como fallidos incluyen un código de gravedad para que el router pueda perfilar al par.
- **Compatibilidad:** los routers todavía pueden aceptar construcciones heredadas con ElGamal por compatibilidad retroactiva, pero los nuevos tunnels usan ECIES por defecto.

> Para las constantes por campo y las notas sobre derivación de claves, consulte el historial de propuestas de ECIES y el código fuente del router; esta guía cubre el flujo operativo.

---

## Creación de Tunnel heredado (ElGamal-2048) {#tunnel-creation-elgamal}

El formato original de construcción de tunnel utilizaba claves públicas de ElGamal. Los routers modernos conservan un soporte limitado por compatibilidad con versiones anteriores.

> **Estado:** Obsoleto. Se conserva aquí como referencia histórica y para cualquier persona que mantenga herramientas compatibles con sistemas heredados.

- **Non-interactive telescoping (encadenamiento no interactivo):** un único mensaje de construcción recorre toda la ruta. Cada salto descifra su registro de 528 bytes, actualiza el mensaje y lo reenvía.
- **Longitud variable:** la Variable Tunnel Build Message (VTBM, mensaje de construcción de tunnel de longitud variable) permitía entre 1 y 8 registros. El mensaje fijo anterior siempre contenía ocho registros para ocultar la longitud del tunnel.
- **Formato del registro de solicitud:**

```
Bytes 0–3    : Tunnel ID (receiving ID)
Bytes 4–35   : Current hop router hash
Bytes 36–39  : Next tunnel ID
Bytes 40–71  : Next hop router hash
Bytes 72–103 : AES-256 layer key
Bytes 104–135: AES-256 IV key
Bytes 136–167: AES-256 reply key
Bytes 168–183: AES-256 reply IV
Byte 184     : Flags (bit7=IBGW, bit6=OBEP)
Bytes 185–188: Request time (hours since epoch)
Bytes 189–192: Next message ID
Bytes 193–221: Padding
```
- **Indicadores:** el bit 7 indica una puerta de enlace de entrada (IBGW); el bit 6 marca un extremo de salida (OBEP). Son mutuamente excluyentes.
- **Cifrado:** cada registro está cifrado con ElGamal-2048 usando la clave pública del salto. El uso en capas simétricas de AES-256-CBC garantiza que solo el salto previsto pueda leer su registro.
- **Datos clave:** los ID de tunnel son valores de 32 bits no nulos; los creadores pueden insertar registros ficticios para ocultar la longitud real del tunnel; la fiabilidad depende de reintentar construcciones fallidas.

---

## Pools de tunnel y ciclo de vida {#tunnel-pools}

Los Routers mantienen conjuntos independientes de tunnel entrantes y salientes para el tráfico exploratorio y para cada sesión de I2CP.

- **Selección de pares:** los tunnels exploratorios toman del conjunto de pares “activos, sin fallos” para fomentar la diversidad; los tunnels de cliente prefieren pares rápidos y de alta capacidad.
- **Ordenación determinista:** los pares se ordenan por la distancia XOR entre `SHA256(peerHash || poolKey)` y la clave aleatoria del grupo. La clave rota al reiniciar, lo que aporta estabilidad dentro de una ejecución y frustra los ataques de predecesor entre ejecuciones.
- **Ciclo de vida:** routers registran tiempos históricos de construcción por tupla {mode, direction, length, variance}. A medida que los tunnels se acercan a su vencimiento, los reemplazos comienzan con antelación; el router incrementa las construcciones en paralelo cuando ocurren fallos, al tiempo que limita los intentos pendientes.
- **Ajustes de configuración:** los recuentos de tunnels activos/de respaldo, la longitud de salto y la varianza, las permisiones de cero saltos y los límites de velocidad de construcción son ajustables por grupo.

---

## Congestión y fiabilidad {#congestion}

Aunque los tunnels se asemejan a circuitos, los routers los tratan como colas de mensajes. Se utiliza Weighted Random Early Discard (WRED, descarte aleatorio temprano ponderado) para mantener la latencia acotada:

- La probabilidad de descarte aumenta a medida que la utilización se acerca a los límites configurados.
- Los participantes consideran fragmentos de tamaño fijo; las puertas de enlace/extremos descartan en función del tamaño combinado de los fragmentos, penalizando primero las cargas útiles grandes.
- Los extremos salientes descartan antes que otros roles para desperdiciar el menor esfuerzo de red posible.

La entrega garantizada se delega a capas superiores como la [Streaming library](/docs/specs/streaming/) (biblioteca de transmisión). Las aplicaciones que requieren fiabilidad deben encargarse ellas mismas de la retransmisión y de los acuses de recibo.

---

## Lecturas adicionales {#further-reading}

- [Selección de pares](/docs/overview/tunnel-routing#peer-selection/)
- [Visión general de Tunnel](/docs/overview/tunnel-routing/)
- [Implementación antigua de Tunnel](/docs/legacy/old-implementation/)
