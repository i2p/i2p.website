---
title: "Especificación de actualización de software"
description: "Mecanismo seguro de actualización firmada y estructura del feed para routers I2P"
slug: "updates"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

## Descripción general

Los routers comprueban automáticamente si hay actualizaciones consultando periódicamente una fuente de noticias firmada, distribuida a través de la red I2P. Cuando se anuncia una versión más reciente, el router descarga un archivo de actualización firmado criptográficamente (`.su3`) y lo deja listo para su instalación.   Este sistema garantiza una distribución de las versiones oficiales **autenticada y resistente a manipulaciones**, y **multicanal**.

A partir de I2P 2.10.0, el sistema de actualización utiliza: - **RSA-4096 / SHA-512** firmas - **Formato de contenedor SU3** (reemplazando SUD/SU2 heredados) - **Espejos redundantes:** HTTP dentro de la red, HTTPS en clearnet (Internet pública) y BitTorrent

---

## 1. Fuente de noticias

Routers consultan periódicamente la fuente Atom firmada cada pocas horas para descubrir nuevas versiones y avisos de seguridad.   La fuente está firmada y se distribuye como un archivo `.su3`, que puede incluir:

- `<i2p:version>` — nuevo número de versión  
- `<i2p:minVersion>` — versión mínima del router compatible  
- `<i2p:minJavaVersion>` — entorno de ejecución de Java mínimo requerido  
- `<i2p:update>` — enumera múltiples espejos de descarga (I2P, HTTPS, torrent)  
- `<i2p:revocations>` — datos de revocación de certificados  
- `<i2p:blocklist>` — listas de bloqueo a nivel de red para pares comprometidos

### Distribución del feed

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Channel</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Description</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Usage</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>I2P HTTP (eepsite)</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Primary update source</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Private, resilient</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Clearnet HTTPS</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Fallback mirror</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Public fallback</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>BitTorrent magnet</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Distributed channel</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reduces mirror load</td>
    </tr>
  </tbody>
</table>
Routers prefieren el feed de I2P, pero pueden recurrir a clearnet (internet abierta) o a la distribución por torrent si es necesario.

---

## 2. Formatos de archivo

### SU3 (Estándar actual)

Introducido en la versión 0.9.9, SU3 reemplazó los formatos heredados SUD y SU2. Cada archivo contiene un encabezado, una carga útil y una firma final.

**Estructura del encabezado** <table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">   <thead>

    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Field</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Description</th>
    </tr>
</thead>   <tbody>

    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Magic</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>"I2Psu3"</code></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Format Version</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>0</code></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Signature Type</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">e.g., <code>0x000B</code> (RSA-SHA512-4096)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Signature Length</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>512 bytes</code></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Version String</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Router version</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Signer ID</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Certificate name</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Content Type</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1 = router update, 3 = reseed, 4 = news feed</td>
    </tr>
</tbody> </table>

**Pasos para la verificación de la firma** 1. Analiza el encabezado e identifica el algoritmo de firma.   2. Verifica el hash y la firma usando el certificado del firmante almacenado.   3. Confirma que el firmante no esté revocado.   4. Compara la cadena de versión incrustada con los metadatos de la carga útil.

Routers se distribuyen con certificados de firmantes de confianza (actualmente **zzz** y **str4d**) y rechazan cualquier fuente no firmada o revocada.

### SU2 (Obsoleto)

- Se utilizó la extensión `.su2` con archivos JAR comprimidos con Pack200.  
- Se eliminó después de que Java 14 marcara Pack200 como obsoleto (JEP 367).  
- Deshabilitado en I2P 0.9.48+; ahora completamente reemplazado por la compresión ZIP.

### SUD (heredado)

- Formato ZIP firmado con DSA-SHA1 (previo a la 0.9.9).  
- Sin ID de firmante ni encabezado, integridad limitada.  
- Reemplazado debido a criptografía débil y ausencia de obligatoriedad de versión.

---

## 3. Flujo de trabajo de actualización

### 3.1 Verificación del encabezado

Routers obtienen únicamente el **encabezado SU3** para verificar la cadena de versión antes de descargar los archivos completos.   Esto evita malgastar ancho de banda en espejos obsoletos o versiones desactualizadas.

### 3.2 Descarga completa

Después de verificar el encabezado, el router descarga el archivo `.su3` completo desde: - Espejos de eepsite dentro de la red (preferido)   - Espejos HTTPS en clearnet (Internet pública) (alternativa)   - BitTorrent (distribución asistida por pares opcional)

Las descargas utilizan clientes HTTP estándar de I2PTunnel, con reintentos, manejo de tiempos de espera y conmutación a un espejo de respaldo.

### 3.3 Verificación de firma

Cada archivo descargado se somete a: - **Comprobación de firma:** verificación RSA-4096/SHA512   - **Coincidencia de versiones:** comprobación de la versión del encabezado frente a la de la carga útil   - **Prevención de retroceso de versión:** garantiza que la actualización sea más reciente que la versión instalada

Los archivos no válidos o que no coinciden se descartan de inmediato.

### 3.4 Preparación de la instalación

Una vez verificado: 1. Extraer el contenido del ZIP a un directorio temporal   2. Eliminar los archivos listados en `deletelist.txt`   3. Sustituir las bibliotecas nativas si se incluye `lib/jbigi.jar`   4. Copiar los certificados del firmante a `~/.i2p/certificates/`   5. Mover la actualización a `i2pupdate.zip` para aplicarla en el próximo reinicio

La actualización se instala automáticamente en el próximo inicio o cuando se activa manualmente la opción “Instalar actualización ahora”.

---

## 4. Gestión de archivos

### deletelist.txt

Una lista en texto plano de archivos obsoletos para eliminar antes de desempaquetar el contenido nuevo.

**Reglas:** - Una ruta por línea (solo rutas relativas) - Líneas que comienzan con `#` ignoradas - `..` y rutas absolutas rechazadas

### Bibliotecas nativas

Para evitar binarios nativos obsoletos o incompatibles: - Si existe `lib/jbigi.jar`, se eliminan los archivos `.so` o `.dll` antiguos   - Garantiza que las bibliotecas específicas de la plataforma se extraigan nuevamente

---

## 5. Gestión de certificados

Routers pueden recibir **nuevos certificados de firmante** mediante actualizaciones o revocaciones en el feed de noticias.

- Los nuevos archivos `.crt` se copian en el directorio de certificados.  
- Los certificados revocados se eliminan antes de futuras verificaciones.  
- Admite la rotación de claves sin requerir intervención manual del usuario.

Todas las actualizaciones se firman sin conexión utilizando **sistemas de firma aislados físicamente**.   Las claves privadas nunca se almacenan en los servidores de compilación.

---

## 6. Directrices para desarrolladores

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Topic</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Details</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Signing</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Use RSA-4096 (SHA-512) via <code>apps/jetty/news</code> SU3 tooling.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Mirror Policy</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">I2P eepsite preferred, clearnet HTTPS fallback, torrent optional.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Testing</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Validate updates from prior releases, across all OS platforms.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Version Enforcement</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>minVersion</code> prevents incompatible upgrades.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Certificate Rotation</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Distribute new certs in updates and revocation lists.</td>
    </tr>
  </tbody>
</table>
Las próximas versiones explorarán la integración de firmas poscuánticas (véase la Propuesta 169) y compilaciones reproducibles.

---

## 7. Descripción general de seguridad

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Threat</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Mitigation</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Tampering</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Cryptographic signature (RSA-4096/SHA512)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Key Compromise</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Feed-based certificate revocation</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Downgrade Attack</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Version comparison enforcement</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Mirror Hijack</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Signature verification, multiple mirrors</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>DoS</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Fallback to alternate mirrors/torrents</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>MITM</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">HTTPS transport + signature-level integrity</td>
    </tr>
  </tbody>
</table>
---

## 8. Versionado

- Router: **2.10.0 (API 0.9.67)**  
- Versionado semántico con `Major.Minor.Patch`.  
- La exigencia de una versión mínima evita actualizaciones inseguras.  
- Java compatible: **Java 8–17**. En el futuro, 2.11.0+ requerirá Java 17+.

---
