---
title: "Incorporar I2P en tu aplicación"
description: "Guía práctica actualizada para integrar un router I2P con tu aplicación de manera responsable"
slug: "embedding"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

Empaquetar I2P con tu aplicación es una forma poderosa de incorporar usuarios, pero solo si el router está configurado de manera responsable.

## 1. Coordinar con los equipos de Router

- Contacta a los mantenedores de **Java I2P** e **i2pd** antes de empaquetarlos. Pueden revisar tus configuraciones predeterminadas y destacar problemas de compatibilidad.
- Elige la implementación de router que se ajuste a tu stack:
  - **Java/Scala** → Java I2P
  - **C/C++** → i2pd
  - **Otros lenguajes** → empaqueta un router e integra usando [SAM v3](/docs/api/samv3/) o [I2CP](/docs/specs/i2cp/)
- Verifica los términos de redistribución para los binarios del router y dependencias (Java runtime, ICU, etc.).

## 2. Valores Predeterminados de Configuración Recomendados

Aspira a "contribuir más de lo que consumes". Los valores predeterminados modernos priorizan la salud y estabilidad de la red.

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Setting</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Recommended Default (2025)</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Bandwidth share</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">80% for participating tunnels </td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Tunnel quantities</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">i2pd: 3 inbound / 3 outbound; Java I2P: 2 inbound / 2 outbound. </td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Signature &amp; encryption</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Use Ed25519 (<code>SIGNATURE_TYPE=7</code>) and advertise ECIES-X25519 + ElGamal (<code>i2cp.leaseSetEncType=4,0</code>).</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Client protocols</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Use SAM v3 or I2CP.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">API listeners</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Bind SAM/I2CP to <code>127.0.0.1</code> only. Disable if not needed.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">UI toggles</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Expose bandwidth controls, logs, and an opt-in checkbox for participating tunnels.</td>
    </tr>
  </tbody>
</table>
### Los túneles de participación siguen siendo esenciales

**No** deshabilite los túneles de participación.

1. Los routers que no retransmiten tienen peor rendimiento.  
2. La red depende del intercambio voluntario de capacidad.  
3. El tráfico de cobertura (tráfico retransmitido) mejora el anonimato.

**Mínimos oficiales:** - Ancho de banda compartido: ≥ 12 KB/s   - Auto-inclusión floodfill: ≥ 128 KB/s   - Recomendado: 2 túneles de entrada / 2 túneles de salida (predeterminado en Java I2P)

## 3. Persistencia y Reseeding

Los directorios de estado persistente (`netDb/`, perfiles, certificados) deben conservarse entre ejecuciones.

Sin persistencia, tus usuarios activarán reseeds en cada inicio, degradando el rendimiento y aumentando la carga en los servidores de reseed.

Si la persistencia es imposible (por ejemplo, contenedores o instalaciones efímeras):

1. Incluir **1,000–2,000 router infos** en el instalador.  
2. Operar uno o más servidores de reseed personalizados para descargar los públicos.

Variables de configuración: - Directorio base: `i2p.dir.base` - Directorio de configuración: `i2p.dir.config` - Incluye `certificates/` para el reseeding.

## 4. Seguridad y Exposición

- Mantén la consola del router (`127.0.0.1:7657`) solo para acceso local.  
- Usa HTTPS si expones la interfaz externamente.  
- Deshabilita SAM/I2CP externos a menos que sea necesario.  
- Revisa los plugins incluidos—distribuye solo lo que tu aplicación soporte.  
- Incluye siempre autenticación para el acceso remoto a la consola.

**Características de seguridad introducidas desde la versión 2.5.0:** - Aislamiento de NetDB entre aplicaciones (2.4.0+)   - Mitigación de DoS y listas de bloqueo de Tor (2.5.1)   - Resistencia al sondeo NTCP2 (2.9.0)   - Mejoras en la selección de routers floodfill (2.6.0+)

## 5. APIs compatibles (2025)

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">API</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Status</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>SAM v3 (3.3)</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">✅ Active</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Recommended bridge for non-Java apps.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>I2CP</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">✅ Active</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Stable protocol core, used internally by Java I2P.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>I2PControl</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">✅ Active</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">JSON-RPC API; plugin maintained.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>BOB</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">⚠️ Deprecated</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Removed from Java I2P since 1.7.0; use SAM v3 instead.</td>
    </tr>
  </tbody>
</table>
Toda la documentación oficial se encuentra en `/docs/api/` — la antigua ruta `/spec/samv3/` **no** existe.

## 6. Redes y Puertos

Puertos predeterminados típicos: - 4444 – Proxy HTTP   - 4445 – Proxy HTTPS   - 7654 – I2CP   - 7656 – SAM Bridge   - 7657 – Consola del Router   - 7658 – Sitio I2P local   - 6668 – Proxy IRC   - 9000–31000 – Puerto de router aleatorio (UDP/TCP entrante)

Los routers seleccionan un puerto de entrada aleatorio en la primera ejecución. El reenvío mejora el rendimiento, pero UPnP puede gestionar esto automáticamente.

## 7. Cambios Modernos (2024–2025)

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Change</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Status</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Details</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>SSU1 Transport</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Removed</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">SSU2 is now the exclusive UDP transport.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>I2P-over-Tor</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Blocked</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Since 2.6.0 (July 2024).</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Datagram2/3</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Added</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Authenticated, repliable datagram formats (2.9.0).</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>LeaseSet service records</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Added</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Enables service discovery (Proposal 167).</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Tunnel build parameters</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Improved</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Adaptive congestion handling (2.9.0+).</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Post-quantum crypto</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Introduced (beta)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ML-KEM hybrid ratchet, opt-in from 2.10.0.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Java 17 requirement</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Announced</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Becomes mandatory in 2.11.0 (early 2026).</td>
    </tr>
  </tbody>
</table>
## 8. Experiencia de Usuario y Pruebas

- Comunicar qué hace I2P y por qué se comparte el ancho de banda.
- Proporcionar diagnósticos del router (ancho de banda, tunnels, estado de reseed).
- Probar los paquetes en Windows, macOS y Linux (incluidos equipos con poca RAM).
- Verificar la interoperabilidad con peers de **Java I2P** e **i2pd**.
- Probar la recuperación tras caídas de red y cierres inesperados.

## 9. Recursos de la Comunidad

- Foro: [i2pforum.net](https://i2pforum.net) o `http://i2pforum.i2p` dentro de I2P.  
- Código: [i2pgit.org/I2P_Developers/i2p.i2p](https://i2pgit.org/I2P_Developers/i2p.i2p).  
- IRC (red Irc2P): `#i2p-dev`, `#i2pd`.  
  - `#i2papps` no verificado; puede no existir.  
  - Aclara qué red (Irc2P vs ilita.i2p) aloja tu canal.

Integrar de manera responsable significa equilibrar la experiencia del usuario, el rendimiento y la contribución a la red. Utiliza estos valores predeterminados, mantente sincronizado con los mantenedores del router y prueba bajo carga real antes del lanzamiento.
