---
title: "SAM v3"
description: "Protocolo puente estable para aplicaciones I2P no basadas en Java"
slug: "samv3"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

SAM v3 ("Simple Anonymous Messaging") es la **API estable e independiente del router** actual que permite a las aplicaciones externas comunicarse con la red I2P sin necesidad de integrar el router. Proporciona acceso unificado a **streams**, **datagrams** y **mensajes sin procesar**, y sigue siendo la capa puente canónica para software no basado en Java.

## 1. Descripción General y Propósito

SAM v3 permite a los desarrolladores crear software compatible con I2P en cualquier lenguaje utilizando un protocolo TCP/UDP ligero. Abstrae los componentes internos del router, exponiendo un conjunto mínimo de comandos sobre TCP (7656) y UDP (7655). Tanto **Java I2P** como **i2pd** implementan subconjuntos de la especificación SAM v3, aunque i2pd todavía carece de la mayoría de las extensiones 3.2 y 3.3 a partir de 2025.

## 2. Historial de versiones

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Version</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Introduced</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Key Features</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>3.0</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.7.3 (May 2009)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Streams + Datagrams; binary destinations; `SESSION CREATE STYLE=` parameter.</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>3.1</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.14 (Jul 2014)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Signature type negotiation via `SIGNATURE_TYPE`; improved `DEST GENERATE`.</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>3.2</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.24 (Jan 2016)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Per session encryption + tunnel options; `STREAM CONNECT ID` support.</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>3.3</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.25 (Mar 2016)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">PRIMARY / SUBSESSION architecture; multiplexing; improved datagrams.</td></tr>
  </tbody>
</table>
### Nota sobre Nomenclatura

- **Java I2P** utiliza `PRIMARY/SUBSESSION`.
- **i2pd** e **I2P+** continúan usando la terminología heredada `MASTER/SUBSESSION` para compatibilidad con versiones anteriores.

## 3. Flujo de trabajo principal

### Negociación de Versión

```
HELLO VERSION MIN=3.1 MAX=3.3
HELLO REPLY RESULT=OK VERSION=3.3
```
### Creación de Destino

```
DEST GENERATE SIGNATURE_TYPE=7
```
- `SIGNATURE_TYPE=7` → **Ed25519 (EdDSA SHA512)**. Fuertemente recomendado desde I2P 0.9.15.

### Creación de Sesión

```
SESSION CREATE STYLE=STREAM DESTINATION=NAME     OPTION=i2cp.leaseSetEncType=4,0     OPTION=inbound.quantity=3     OPTION=outbound.quantity=3
```
- `i2cp.leaseSetEncType=4,0` → `4` es X25519 (ECIES X25519 AEAD Ratchet) y `0` es ElGamal de respaldo para compatibilidad.
- Cantidades de túneles explícitas para consistencia: Java I2P predeterminado **2**, i2pd predeterminado **5**.

### Operaciones del Protocolo

```
STREAM CONNECT ID=1 DESTINATION=b32address.i2p
STREAM SEND ID=1 SIZE=128
STREAM CLOSE ID=1
```
Los tipos de mensajes principales incluyen: `STREAM CONNECT`, `STREAM ACCEPT`, `STREAM FORWARD`, `DATAGRAM SEND`, `RAW SEND`, `NAMING LOOKUP`, `DEST LOOKUP`, `PING`, `QUIT`.

### Apagado Ordenado

```
QUIT
```
## 4. Diferencias de Implementación (Java I2P vs i2pd)

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Feature</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Java I2P 2.10.0</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">i2pd 2.58.0 (Sept&nbsp;2025)</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">SAM enabled by default</td><td style="border:1px solid var(--color-border); padding:0.5rem;">❌ Requires manual enable in router console</td><td style="border:1px solid var(--color-border); padding:0.5rem;">✅ Enabled via `enabled=true` in `i2pd.conf`</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Default ports</td><td style="border:1px solid var(--color-border); padding:0.5rem;">TCP 7656 / UDP 7655</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Same</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">AUTH / USER / PASSWORD</td><td style="border:1px solid var(--color-border); padding:0.5rem;">✓ Supported</td><td style="border:1px solid var(--color-border); padding:0.5rem;">✗ Not implemented</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">PING / PONG keepalive</td><td style="border:1px solid var(--color-border); padding:0.5rem;">✓ Supported</td><td style="border:1px solid var(--color-border); padding:0.5rem;">✗ Not implemented</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">QUIT / STOP / EXIT commands</td><td style="border:1px solid var(--color-border); padding:0.5rem;">✓ Supported</td><td style="border:1px solid var(--color-border); padding:0.5rem;">✗ Not implemented</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">FROM_PORT / TO_PORT / PROTOCOL</td><td style="border:1px solid var(--color-border); padding:0.5rem;">✓ Supported</td><td style="border:1px solid var(--color-border); padding:0.5rem;">✗ Not implemented</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">PRIMARY/SUBSESSION support</td><td style="border:1px solid var(--color-border); padding:0.5rem;">✓ (since 0.9.47)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">✗ Absent</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">SESSION ADD / REMOVE</td><td style="border:1px solid var(--color-border); padding:0.5rem;">✓ Supported</td><td style="border:1px solid var(--color-border); padding:0.5rem;">✗ Not implemented</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Datagram2 / Datagram3 support</td><td style="border:1px solid var(--color-border); padding:0.5rem;">✓ (since 2.9.0)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">✗ Not implemented</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">SSL/TLS</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Optional</td><td style="border:1px solid var(--color-border); padding:0.5rem;">✗ None</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Default tunnel quantities</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Inbound/outbound=2</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Inbound/outbound=5</td></tr>
  </tbody>
</table>
**Recomendación:** Especifique siempre las cantidades de túneles explícitamente para garantizar la coherencia entre routers.

## 5. Bibliotecas compatibles (estado en 2025)

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Library</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Language</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">SAM Support</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Maintenance Status (2025)</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/i2p/libsam3">libsam3</a></td><td style="border:1px solid var(--color-border); padding:0.5rem;">C</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.1</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Maintained by I2P Project (eyedeekay)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/i2p/i2psam">i2psam</a></td><td style="border:1px solid var(--color-border); padding:0.5rem;">C++</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.1</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Minimal updates since 2019</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/go-i2p/sam3">sam3</a></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Go</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.3</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active; migrated from `eyedeekay/sam3`</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/go-i2p/onramp">onramp</a></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Go</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.3</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Actively maintained (2025)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/majestrate/i2plib">i2plib</a></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Python</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.1</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Modern async replacement for `i2p.socket`</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/majestrate/i2p.socket">i2p.socket</a></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Python</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.2</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Abandoned (last release 2017)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://i2pgit.org/robin/Py2p">Py2p</a></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Python</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.3</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Unverified/inactive</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/i2p/i2p-rs">i2p-rs</a></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Rust</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.1</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Experimental; unstable API</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/diva-exchange/i2p-sam">@diva.exchange/i2p-sam</a></td><td style="border:1px solid var(--color-border); padding:0.5rem;">TypeScript / JS</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.3</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Most actively maintained (2024–2025)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/eyedeekay/I2PSharp">I2PSharp</a></td><td style="border:1px solid var(--color-border); padding:0.5rem;">C#</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.3</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Functional; light maintenance</td></tr>
  </tbody>
</table>
## 6. Funciones Nuevas y Próximas (2024–2025)

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Feature</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Status</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Introduced</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">NAMING LOOKUP `OPTIONS=true`</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">✓ Supported</td><td style="border:1px solid var(--color-border); padding:0.5rem;">2.8.0</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Datagram2 / Datagram3 formats</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">✓ (Java only)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">2.9.0</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Post-quantum hybrid crypto (ML KEM)</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Optional</td><td style="border:1px solid var(--color-border); padding:0.5rem;">2.10.0</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Java 17+ runtime requirement</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Planned</td><td style="border:1px solid var(--color-border); padding:0.5rem;">2.11.0</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">I2P over Tor blocking</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Active</td><td style="border:1px solid var(--color-border); padding:0.5rem;">2.6.0</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Improved floodfill selection</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Active</td><td style="border:1px solid var(--color-border); padding:0.5rem;">2.8.0+</td></tr>
  </tbody>
</table>
## 7. Notas de Seguridad y Configuración

- Vincular SAM solo a `127.0.0.1`.
- Para servicios persistentes, usar sesiones **PRIMARY** con claves estáticas.
- Usar `HELLO VERSION` para probar el soporte de funcionalidades.
- Usar `PING` o `NAMING LOOKUP` para verificar que el router esté activo.
- Evitar conexiones SAM remotas no autenticadas (sin TLS en i2pd).

## 8. Referencias y Especificaciones

- [Especificación SAMv3](/docs/api/samv3/)
- [SAM v2 (Heredado)](/docs/legacy/samv2/)
- [Especificación de Streaming](/docs/specs/streaming/)
- [Datagramas](/docs/api/datagrams/)
- [Centro de Documentación](/docs/)
- [Documentación de i2pd](https://i2pd.website/docs)

## 9. Resumen

SAM v3 sigue siendo el **protocolo puente recomendado** para todas las aplicaciones I2P que no sean Java. Ofrece estabilidad, enlaces entre lenguajes y rendimiento consistente en todos los tipos de router.

Al desarrollar con SAM: - Usa firmas **Ed25519** y cifrado **X25519**. - Verifica el soporte de características dinámicamente mediante `HELLO VERSION`. - Diseña para compatibilidad, especialmente cuando soportas tanto routers Java I2P como i2pd.
