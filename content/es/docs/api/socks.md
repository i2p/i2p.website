---
title: "Proxy SOCKS"
description: "Uso seguro del túnel SOCKS de I2P (actualizado para 2.10.0)"
slug: "socks"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

> **Precaución:** El túnel SOCKS reenvía las cargas útiles de las aplicaciones sin desinfectarlas. Muchos protocolos filtran IPs, nombres de host u otros identificadores. Usa SOCKS únicamente con software que hayas auditado para anonimato.

---

## 1. Descripción general

I2P proporciona soporte de proxy **SOCKS 4, 4a y 5** para conexiones salientes a través de un **cliente I2PTunnel**. Permite que aplicaciones estándar alcancen destinos I2P pero **no puede acceder a clearnet**. **No hay outproxy SOCKS**, y todo el tráfico permanece dentro de la red I2P.

### Resumen de Implementación

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Parameter</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Java I2P</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">i2pd</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Default Port</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">User-defined</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>127.0.0.1:4447</code></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Supported SOCKS Versions</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">4, 4a, 5</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">4, 4a, 5</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">UDP Mode</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Stubbed (non-functional)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Stubbed (non-functional)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Persistent Keys</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">✅ Since 0.9.9</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">✅</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Shared Client Tunnels</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Supported</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Supported</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Outproxy Support</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">❌ None</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">❌ None</td>
    </tr>
  </tbody>
</table>
**Tipos de dirección soportados:** - Nombres de host `.i2p` (entradas de libreta de direcciones) - Hashes Base32 (`.b32.i2p`) - No hay soporte para Base64 o clearnet

---

## 2. Riesgos de Seguridad y Limitaciones

### Fuga en la Capa de Aplicación

SOCKS opera por debajo de la capa de aplicación y no puede sanitizar protocolos. Muchos clientes (por ejemplo, navegadores, IRC, correo electrónico) incluyen metadatos que revelan tu dirección IP, nombre de host o detalles del sistema.

Las fugas comunes incluyen: - IPs en encabezados de correo o respuestas CTCP de IRC   - Nombres reales/nombres de usuario en cargas útiles de protocolo   - Cadenas de user-agent con huellas de SO   - Consultas DNS externas   - WebRTC y telemetría del navegador

**I2P no puede prevenir estas filtraciones**—ocurren por encima de la capa de túnel. Solo utiliza SOCKS para **clientes auditados** diseñados para anonimato.

### Identidad de Túnel Compartida

Si múltiples aplicaciones comparten un túnel SOCKS, comparten la misma identidad de destino I2P. Esto permite la correlación o fingerprinting entre diferentes servicios.

**Mitigación:** Usa **túneles no compartidos** para cada aplicación y habilita **claves persistentes** para mantener identidades criptográficas consistentes entre reinicios.

### Modo UDP deshabilitado

El soporte UDP en SOCKS5 no está implementado. El protocolo anuncia capacidad UDP, pero las llamadas son ignoradas. Use clientes solo TCP.

### Sin Outproxy por Diseño

A diferencia de Tor, I2P **no** ofrece outproxies (proxies de salida) a la clearnet basados en SOCKS. Los intentos de alcanzar IPs externas fallarán o expondrán la identidad. Use proxies HTTP o HTTPS si se requiere outproxying.

---

## 3. Contexto Histórico

Los desarrolladores han desaconsejado durante mucho tiempo el uso de SOCKS para anonimato. De las discusiones internas de desarrolladores y de la [Reunión 81](/es/blog/2004/03/16/i2p-dev-meeting-march-16-2004/) y [Reunión 82](/es/blog/2004/03/23/i2p-dev-meeting-march-23-2004/) de 2004:

> "Reenviar tráfico arbitrario no es seguro, y nos corresponde como desarrolladores de software de anonimato tener la seguridad de nuestros usuarios finales en primer lugar en nuestras mentes."

El soporte SOCKS se incluyó por compatibilidad pero no se recomienda para entornos de producción. Casi todas las aplicaciones de internet filtran metadatos sensibles inadecuados para el enrutamiento anónimo.

---

## 4. Configuración

### Java I2P

1. Abra el [I2PTunnel Manager](http://127.0.0.1:7657/i2ptunnel)  
2. Cree un nuevo tunnel cliente de tipo **"SOCKS 4/4a/5"**  
3. Configure las opciones:  
   - Puerto local (cualquiera disponible)  
   - Cliente compartido: *deshabilitar* para identidad separada por aplicación  
   - Clave persistente: *habilitar* para reducir correlación de claves  
4. Inicie el tunnel

### i2pd

i2pd incluye soporte SOCKS5habilitado por defecto en `127.0.0.1:4447`. La configuración en `i2pd.conf` bajo `[SOCKSProxy]` te permite ajustar el puerto, host y parámetros del tunnel.

---

## 5. Cronograma de Desarrollo

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Version</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Change</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Date</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.7.1</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Initial SOCKS 4/4a/5 support</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2010</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.9</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Added persistent keying</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2013</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1.7.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">BOB API deprecated and removed</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2022</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.6.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">I2P-over-Tor blocked to improve network health</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2024</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.10.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Post-quantum hybrid encryption introduced</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2025</td>
    </tr>
  </tbody>
</table>
El módulo SOCKS en sí no ha tenido actualizaciones importantes del protocolo desde 2013, pero la pila de túneles circundante ha recibido mejoras de rendimiento y criptográficas.

---

## 6. Alternativas Recomendadas

Para cualquier aplicación de **producción**, **pública** o **crítica para la seguridad**, utilice una de las APIs oficiales de I2P en lugar de SOCKS:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">API</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Description</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Recommended For</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>SAM v3 (3.3)</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Simple Anonymous Messaging API</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Cross-language apps needing socket-like I/O</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Streaming Library</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">TCP-like sockets for Java</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Native Java integrations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>I2CP</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Low-level router communication</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Custom protocols, router-level integration</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>BOB</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deprecated (removed 2022)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Legacy only; migrate to SAM</td>
    </tr>
  </tbody>
</table>
Estas APIs proporcionan un aislamiento adecuado de destinos, control de identidad criptográfica y mejor rendimiento de enrutamiento.

---

## 7. OnionCat / GarliCat

OnionCat soporta I2P a través de su modo GarliCat (rango IPv6 `fd60:db4d:ddb5::/48`). Aún funcional pero con desarrollo limitado desde 2019.

**Advertencias de uso:** - Requiere configuración manual de `.oc.b32.i2p` en SusiDNS   - Necesita asignación estática de IPv6   - No cuenta con soporte oficial del proyecto I2P

Recomendado solo para configuraciones avanzadas de VPN sobre I2P.

---

## 8. Mejores Prácticas

Si debes usar SOCKS: 1. Crea túneles separados por aplicación.   2. Desactiva el modo de cliente compartido.   3. Habilita claves persistentes.   4. Fuerza la resolución DNS de SOCKS5.   5. Audita el comportamiento del protocolo en busca de fugas.   6. Evita conexiones a la red clearnet (internet convencional).   7. Monitorea el tráfico de red en busca de fugas.

---

## 9. Resumen Técnico

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Parameter</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Value</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Supported SOCKS Versions</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">4, 4a, 5</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Transport</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">TCP only</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>UDP Support</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Stubbed (non-functional)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Clearnet Access</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Not supported</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Default Ports</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Java I2P: user-set; i2pd: <code>127.0.0.1:4447</code></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Persistent Keying</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Supported since 0.9.9</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Shared Tunnels</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Supported (discouraged)</td>
    </tr>
  </tbody>
</table>
---

## 10. Conclusión

El proxy SOCKS en I2P proporciona compatibilidad básica con aplicaciones TCP existentes, pero **no está diseñado para garantías sólidas de anonimato**. Solo debe utilizarse en entornos de prueba controlados y auditados.

> Para implementaciones serias, migre a **SAM v3** o la **API de Streaming**. Estas APIs aíslan las identidades de aplicaciones, usan criptografía moderna y reciben desarrollo continuo.

---

### Recursos Adicionales

- [Documentación Oficial de SOCKS](/docs/api/socks/)  
- [Especificación SAMv3](/docs/api/samv3/)  
- [Documentación de la Biblioteca Streaming](/docs/specs/streaming/)  
- [Referencia de I2PTunnel](/docs/specs/implementation/)  
- [Documentación para Desarrolladores de I2P](https://i2pgit.org/I2P_Developers/i2p.i2p)  
- [Foro de la Comunidad](https://i2pforum.net)
