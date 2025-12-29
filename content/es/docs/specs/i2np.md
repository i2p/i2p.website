---
title: "Protocolo de red de I2P (I2NP)"
description: "Formatos de mensajes de router a router, prioridades y límites de tamaño dentro de I2P."
slug: "i2np"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

## Descripción general

El Protocolo de Red de I2P (I2NP) define cómo los routers intercambian mensajes, seleccionan transportes y mezclan el tráfico manteniendo el anonimato. Opera entre **I2CP** (API de cliente) y los protocolos de transporte (**NTCP2** y **SSU2**).

I2NP es la capa por encima de los protocolos de transporte de I2P. Es un protocolo de router a router utilizado para: - Búsquedas y respuestas en la base de datos de la red - Creación de tunnels - Mensajes cifrados de datos de router y de cliente

Los mensajes I2NP pueden enviarse punto a punto a otro router, o de forma anónima a través de tunnels a ese router.

Los routers ponen en cola el trabajo saliente usando prioridades locales. Los números de prioridad más altos se procesan primero. Cualquier valor por encima de la prioridad estándar de datos de tunnel (400) se considera urgente.

### Transportes actuales

I2P ahora utiliza **NTCP2** (TCP) y **SSU2** (UDP) tanto para IPv4 como para IPv6. Ambos transportes emplean: - **X25519** para el intercambio de claves (marco del protocolo Noise) - **ChaCha20/Poly1305** cifrado autenticado (AEAD) - **SHA-256** (función de hash)

**Se retiraron los transportes heredados:** - NTCP (TCP original) se eliminó del router de Java en la versión 0.9.50 (mayo de 2021) - SSU v1 (UDP original) se eliminó del router de Java en la versión 2.4.0 (diciembre de 2023) - SSU v1 se eliminó de i2pd en la versión 2.44.0 (noviembre de 2022)

A partir de 2025, la red ha migrado por completo a transportes basados en Noise, sin soporte alguno para transportes heredados.

---

## Sistema de numeración de versiones

**IMPORTANTE:** I2P utiliza un sistema de versionado dual que debe entenderse claramente:

### Versiones de lanzamiento (de cara al usuario)

Estas son las versiones que los usuarios ven y descargan: - 0.9.50 (mayo de 2021) - Última versión 0.9.x - **1.5.0** (agosto de 2021) - Primera versión 1.x - 1.6.0, 1.7.0, 1.8.0, 1.9.0 (entre 2021 y 2022) - **2.0.0** (noviembre de 2022) - Primera versión 2.x - 2.1.0 a 2.9.0 (entre 2023 y 2025) - **2.10.0** (8 de septiembre de 2025) - Versión actual

### Versiones de la API (Compatibilidad del protocolo)

Estos son números de versión internos publicados en el campo "router.version" en las propiedades de RouterInfo: - 0.9.50 (mayo de 2021) - **0.9.51** (agosto de 2021) - Versión de la API para el lanzamiento 1.5.0 - 0.9.52 a 0.9.66 (continuando en los lanzamientos 2.x) - **0.9.67** (septiembre de 2025) - Versión de la API para el lanzamiento 2.10.0

**Punto clave:** NO hubo versiones numeradas de la 0.9.51 a la 0.9.67. Estos números existen solo como identificadores de versión de la API. I2P saltó de la versión 0.9.50 directamente a la 1.5.0.

### Tabla de correspondencia de versiones

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Release Version</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">API Version</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Date</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Key Features</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.50</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.50</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">May 2021</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Last 0.9.x release, removed NTCP1</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">1.5.0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.51</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">August 2021</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Short tunnel build messages (218 bytes)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">1.6.0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.52</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">November 2021</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Various improvements</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">1.7.0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.53</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">January 2022</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Performance enhancements</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">1.8.0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.54</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">May 2022</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">SSU2 introduced</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">1.9.0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.55</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">August 2022</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">SSU2 improvements</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">2.0.0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.56</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">November 2022</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">SSU2 enabled by default</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">2.1.0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.57</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">January 2023</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Stability improvements</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">2.2.0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.58</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">March 2023</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>ElGamal routers deprecated</strong></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">2.3.0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.59</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">May 2023</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Various improvements</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">2.4.0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.61</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">December 2023</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Removed SSU1 support</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">2.5.0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.62</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">February 2024</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Performance improvements</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">2.6.0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.63</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">May 2024</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Network optimizations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">2.7.0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.64</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">October 2024</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Post-quantum preparation work</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">2.8.0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.65</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">February 2025</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Tunnel bandwidth parameters</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">2.9.0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.66</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">June 2025</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">LeaseSet service records</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">2.10.0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">September 2025</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Post-quantum hybrid cryptography (beta)</td>
    </tr>
  </tbody>
</table>
**Próximamente:** La versión 2.11.0 (prevista para diciembre de 2025) requerirá Java 17+ y habilitará por defecto la criptografía poscuántica.

---

## Versiones de protocolo

Todos los routers deben publicar su versión del protocolo I2NP en el campo "router.version" en las propiedades de RouterInfo. Este campo de versión es la versión de la API, que indica el nivel de compatibilidad con varias funciones del protocolo I2NP, y no es necesariamente la versión real del router.

Si los routers alternativos (no Java) desean publicar cualquier información de versión sobre la implementación real del router, deben hacerlo en otra propiedad. Se permiten versiones distintas de las que se enumeran a continuación. La compatibilidad se determinará mediante una comparación numérica; por ejemplo, 0.9.13 implica compatibilidad con las funcionalidades de la versión 0.9.12.

**Nota:** La propiedad "coreVersion" ya no se publica en la información del router y nunca se utilizó para determinar la versión del protocolo I2NP.

### Resumen de características por versión de la API

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">API Version</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Required I2NP Features</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Post-quantum hybrid cryptography (MLKEM ratchet) support (beta), UDP tracker support</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.66</td><td style="border:1px solid var(--color-border); padding:0.5rem;">LeaseSet2 service record options (see proposal 167)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.65</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Tunnel build bandwidth parameters (see proposal 168)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.59</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Minimum peers will build tunnels through (as of 0.9.63), minimum floodfill peers will send DSM to (as of 0.9.63)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.58</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Minimum peers will build tunnels through (as of 0.9.62), <strong>ElGamal routers deprecated</strong></td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.55</td><td style="border:1px solid var(--color-border); padding:0.5rem;">SSU2 transport support (if published in router info)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.51</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Short tunnel build messages for ECIES-X25519 routers, minimum peers will build tunnels through (as of 0.9.58), minimum floodfill peers will send DSM to (as of 0.9.58)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.49</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Garlic messages to ECIES-X25519 routers</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.48</td><td style="border:1px solid var(--color-border); padding:0.5rem;">ECIES-X25519 routers, ECIES-X25519 build request/response records</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.46</td><td style="border:1px solid var(--color-border); padding:0.5rem;">DatabaseLookup flag bit 4 for AEAD reply</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.44</td><td style="border:1px solid var(--color-border); padding:0.5rem;">ECIES-X25519 keys in LeaseSet2</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.40</td><td style="border:1px solid var(--color-border); padding:0.5rem;">MetaLeaseSet may be sent in a DSM</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.39</td><td style="border:1px solid var(--color-border); padding:0.5rem;">EncryptedLeaseSet may be sent in a DSM, RedDSA_SHA512_Ed25519 signature type supported</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.38</td><td style="border:1px solid var(--color-border); padding:0.5rem;">DSM type bits 3-0 now contain the type; LeaseSet2 may be sent in a DSM</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.36</td><td style="border:1px solid var(--color-border); padding:0.5rem;">NTCP2 transport support (if published in router info), minimum peers will build tunnels through (as of 0.9.46)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.28</td><td style="border:1px solid var(--color-border); padding:0.5rem;">RSA signature types disallowed, minimum floodfill peers will send DSM to (as of 0.9.34)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.18</td><td style="border:1px solid var(--color-border); padding:0.5rem;">DSM type bits 7-1 ignored</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.16</td><td style="border:1px solid var(--color-border); padding:0.5rem;">RI key certs / ECDSA and EdDSA signature types, DLM lookup types (flag bits 3-2), minimum version compatible with the current network</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.15</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Destination/LeaseSet key certificates with EdDSA Ed25519 signature type (if floodfill)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Destination/LeaseSet key certificates with ECDSA P-256, P-384, and P-521 signature types (if floodfill); non-zero expiration allowed in RouterAddress</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.7</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Encrypted DSM/DSRM replies supported (DLM flag bit 1) for floodfill routers</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.6</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Non-zero DLM flag bits 7-1 allowed</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.3</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Requires zero expiration in RouterAddress</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Supports up to 16 leases in a DSM LeaseSet store (previously 6)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.7.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">VTBM and VTBRM message support</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.7.10</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Floodfill supports encrypted DSM stores</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.6.1.10</td><td style="border:1px solid var(--color-border); padding:0.5rem;">TBM and TBRM messages introduced; minimum version compatible with the current network</td></tr>
  </tbody>
</table>
**Nota:** También hay características relacionadas con el transporte y problemas de compatibilidad. Consulte la documentación de transporte de NTCP2 (protocolo de transporte de I2P) y SSU2 (protocolo de transporte de I2P) para obtener detalles.

---

## Encabezado del mensaje

I2NP utiliza una estructura lógica de encabezado de 16 bytes, mientras que los transportes modernos (NTCP2 y SSU2) usan un encabezado abreviado de 9 bytes que omite los campos redundantes de tamaño y suma de verificación. Los campos siguen siendo conceptualmente idénticos.

### Comparación de formatos de encabezado

**Formato estándar (16 bytes):**

Se usa en el transporte NTCP legado y cuando los mensajes I2NP están encapsulados dentro de otros mensajes (TunnelData, TunnelGateway, GarlicClove).

```
Bytes 0-15:
+----+----+----+----+----+----+----+----+
|type|      msg_id       |  expiration
+----+----+----+----+----+----+----+----+
                         |  size   |chks|
+----+----+----+----+----+----+----+----+

type :: Integer (1 byte)
        Identifies the message type (see message type table)

msg_id :: Integer (4 bytes)
          Uniquely identifies this message (for some time at least)
          Usually a locally-generated random number, but for outgoing
          tunnel build messages may be derived from the incoming message

expiration :: Date (8 bytes)
              Unix timestamp in milliseconds when this message expires

size :: Integer (2 bytes)
        Length of the payload (0 to ~61.2 KB for tunnel messages)

chks :: Integer (1 byte)
        SHA256 hash of payload truncated to first byte
        Deprecated - NTCP2/SSU2 use ChaCha20/Poly1305 AEAD for integrity
```
**Formato corto para SSU (obsoleto, 5 bytes):**

```
+----+----+----+----+----+
|type| short_expiration  |
+----+----+----+----+----+

type :: Integer (1 byte)
short_expiration :: Integer (4 bytes, seconds since epoch)
```
**Formato abreviado para NTCP2, SSU2 y ECIES-Ratchet Garlic Cloves (9 bytes):**

Se utiliza en transportes modernos y en garlic messages (mensajes "garlic", técnica de empaquetado de mensajes en I2P) cifrados con ECIES.

```
+----+----+----+----+----+----+----+----+
|type|      msg_id       | short_expira-
+----+----+----+----+----+----+----+----+
 tion|
+----+

type :: Integer (1 byte)
msg_id :: Integer (4 bytes)
short_expiration :: Integer (4 bytes, seconds since epoch, unsigned)
```
### Detalles de los campos de cabecera

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Field</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Bytes</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Type</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Identifies the message class (0&ndash;255, see message types below)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Unique ID</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Locally unique identifier for matching replies</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Expiration</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">8 (standard) / 4 (short)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Timestamp when the message expires. Routers discard expired messages. Short format uses seconds since epoch (unsigned, wraps February 7, 2106)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Payload Length</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Size in bytes (0 to ~61.2 KB for tunnel messages). NTCP2 and SSU2 encode this in their frame headers</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Checksum</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated. First byte of SHA-256 hash of the payload. NTCP2/SSU2 use ChaCha20/Poly1305 AEAD for integrity</td>
    </tr>
  </tbody>
</table>
### Notas de implementación

- Cuando se transmite por SSU (obsoleto), solo se incluían el tipo y la expiración de 4 bytes
- Cuando se transmite por NTCP2 o SSU2, se utiliza el formato corto de 9 bytes
- El encabezado estándar de 16 bytes es obligatorio para los mensajes I2NP contenidos en otros mensajes (Data, TunnelData, TunnelGateway, GarlicClove)
- Desde la versión 0.8.12, la verificación de la suma de comprobación está deshabilitada en algunos puntos de la pila del protocolo por eficiencia, pero la generación de la suma de comprobación sigue siendo necesaria por compatibilidad
- La expiración corta es sin signo y se desbordará el 7 de febrero de 2106. Después de esa fecha, debe añadirse un desplazamiento para obtener la hora correcta
- Por compatibilidad con versiones anteriores, genere siempre sumas de comprobación aunque puede que no se verifiquen

---

## Restricciones de tamaño

Los mensajes de Tunnel fragmentan las cargas útiles de I2NP en piezas de tamaño fijo:
- **Primer fragmento:** aproximadamente 956 bytes
- **Fragmentos posteriores:** aproximadamente 996 bytes cada uno
- **Máximo de fragmentos:** 64 (numerados 0-63)
- **Carga útil máxima:** aproximadamente 61,200 bytes (61.2 KB)

**Cálculo:** 956 + (63 × 996) = 63,704 bytes máximo teórico, con un límite práctico de alrededor de 61,200 bytes debido a la sobrecarga.

### Contexto histórico

Los transportes antiguos tenían límites más estrictos de tamaño de trama: - NTCP: tramas de 16 KB - SSU: tramas de aproximadamente 32 KB

NTCP2 admite tramas de aproximadamente 65 KB, pero el límite de fragmentación del tunnel sigue aplicándose.

### Consideraciones sobre los datos de la aplicación

Garlic messages (técnica de agrupación de mensajes en I2P) pueden agrupar LeaseSets, Session Tags (etiquetas de sesión), o variantes cifradas de LeaseSet2, reduciendo el espacio para los datos de la carga útil.

**Recomendación:** Los datagramas deben mantenerse ≤ 10 KB para garantizar una entrega fiable. Los mensajes que se acerquen al límite de 61 KB pueden experimentar: - Mayor latencia debido al reensamblado de fragmentos - Mayor probabilidad de fallo en la entrega - Mayor exposición al análisis de tráfico

### Detalles técnicos de la fragmentación

Cada mensaje de tunnel tiene exactamente 1,024 bytes (1 KB) y contiene: - ID de tunnel de 4 bytes - vector de inicialización (IV) de 16 bytes - 1,004 bytes de datos cifrados

Dentro de los datos cifrados, los mensajes de tunnel transportan mensajes I2NP fragmentados con cabeceras de fragmento que indican: - Número de fragmento (0-63) - Si es el primer fragmento o uno posterior - ID total del mensaje para el reensamblado

El primer fragmento incluye el encabezado completo del mensaje I2NP (16 bytes), dejando aproximadamente 956 bytes para la carga útil. Los fragmentos posteriores no incluyen el encabezado del mensaje, lo que permite aproximadamente 996 bytes de carga útil por fragmento.

---

## Tipos comunes de mensajes

Los Routers utilizan el tipo de mensaje y la prioridad para programar el trabajo saliente. Los valores de mayor prioridad se procesan primero. Los siguientes valores coinciden con los predeterminados actuales de Java I2P (a partir de la versión de la API 0.9.67).

**Nota:** Las prioridades dependen de la implementación. Para obtener los valores de prioridad oficiales, consulte la documentación de la clase `OutNetMessage` en el código fuente de I2P en Java.

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Message</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Priority</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Typical Size</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Purpose</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>DatabaseStore</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">460</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Varies (LeaseSet ≈ 898&nbsp;B, RouterInfo ≈ 2&ndash;4&nbsp;KB compressed)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Publishes RouterInfo or LeaseSet objects. Supports LeaseSet2, EncryptedLeaseSet, and MetaLeaseSet</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>DatabaseLookup</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">500</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Varies</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Queries the network database for RouterInfo or LeaseSet entries</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>DatabaseSearchReply</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">300</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">≈161&nbsp;B (5 hashes)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Returns candidate floodfill router hashes (typically 3&ndash;16 hashes, recommended maximum 16)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>DeliveryStatus</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">10</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Varies</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">12&nbsp;B</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Receipts for tunnel tests or acknowledgements inside GarlicMessages</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>GarlicMessage</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">11</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">100 (local)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Varies</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Bundles multiple message cloves (e.g., DataMessage, LeaseSets). Supports ElGamal/AES (deprecated) and ECIES-X25519-AEAD-Ratchet encryption</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>TunnelData</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">18</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">400</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">1,028&nbsp;B (fixed)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Encrypted tunnel message exchanged between hops. Contains a 4-byte tunnel ID, 16-byte IV, and 1,004 bytes of encrypted data</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>TunnelGateway</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">19</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">300&ndash;400</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Varies</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Encapsulates messages at the tunnel gateway before fragmentation</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>DataMessage</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">20</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">425</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">4&ndash;62&nbsp;KB</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Carries end-to-end garlic payloads (application traffic)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>TunnelBuild</strong> <em>(deprecated)</em></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">21</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">500</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">4,224&nbsp;B</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Requests tunnel participation from routers (8 × 528-byte records). Replaced by VariableTunnelBuild for ECIES</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>TunnelBuildReply</strong> <em>(deprecated)</em></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">22</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">300</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">4,224&nbsp;B</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Replies to TunnelBuild with accept/reject status per hop</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>VariableTunnelBuild</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">23</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">500</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">1,057&ndash;4,225&nbsp;B</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Variable-length tunnel build for ElGamal or ECIES-X25519 routers (1&ndash;8 records, API 0.9.12+)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>VariableTunnelBuildReply</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">24</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">300</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">1,057&ndash;4,225&nbsp;B</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Replies to VariableTunnelBuild</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>ShortTunnelBuild</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">25</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">500</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">873&ndash;1,745&nbsp;B</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Short tunnel build messages for ECIES-X25519 routers only (1&ndash;8 × 218-byte records, API 0.9.51+)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>OutboundTunnelBuildReply</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">26</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">300</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">873&ndash;1,745&nbsp;B</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Sent from outbound endpoint to originator for ECIES-X25519 routers (API 0.9.51+)</td>
    </tr>
  </tbody>
</table>
**Tipos de mensajes reservados:** - Tipo 0: Reservado - Tipos 4-9: Reservados para uso futuro - Tipos 12-17: Reservados para uso futuro - Tipos 224-254: Reservados para mensajes experimentales - Tipo 255: Reservado para expansión futura

### Notas sobre tipos de mensaje

- Mensajes del plano de control (DatabaseLookup, TunnelBuild, etc.) generalmente viajan a través de **tunnels exploratorios**, no de tunnels de cliente, lo que permite una priorización independiente
- Los valores de prioridad son aproximados y pueden variar según la implementación
- TunnelBuild (21) y TunnelBuildReply (22) están obsoletos, pero siguen implementados para compatibilidad con tunnels muy largos (>8 saltos)
- La prioridad estándar de los datos de tunnel es 400; cualquier valor por encima de esto se trata como urgente
- La longitud típica de un tunnel en la red actual es de 3-4 saltos, por lo que la mayoría de las construcciones de tunnels usan ShortTunnelBuild (registros de 218 bytes) o VariableTunnelBuild (registros de 528 bytes)

---

## Cifrado y encapsulación de mensajes

Los Routers encapsulan con frecuencia mensajes I2NP antes de la transmisión, creando múltiples capas de cifrado. Un DeliveryStatus message (mensaje de estado de entrega) puede estar: 1. Envuelto en un GarlicMessage (mensaje de tipo GarlicMessage; cifrado) 2. Dentro de un DataMessage (mensaje de datos) 3. Dentro de un TunnelData message (mensaje de datos de tunnel; cifrado de nuevo)

Cada salto solo descifra su capa; el destino final revela la carga útil más interna.

### Algoritmos de cifrado

**Legado (en proceso de retirada):** - ElGamal/AES + SessionTags (etiquetas de sesión) - ElGamal-2048 para cifrado asimétrico - AES-256 para cifrado simétrico - SessionTags de 32 bytes

**Actual (Estándar a partir de la API 0.9.48):** - ECIES-X25519 + ChaCha20/Poly1305 AEAD con ratcheting forward secrecy (secreto hacia adelante mediante un mecanismo de rotación progresiva de claves) - marco del protocolo Noise (Noise_IK_25519_ChaChaPoly_SHA256 para destinos) - etiquetas de sesión de 8 bytes (reducidas de 32 bytes) - algoritmo Signal Double Ratchet para secreto hacia adelante - Introducido en la versión 0.9.46 de la API (2020) - Obligatorio para todos los routers desde la versión 0.9.58 de la API (2023)

**Futuro (Beta a partir de la 2.10.0):** - Criptografía híbrida poscuántica usando MLKEM (ML-KEM-768) combinada con X25519 - Hybrid ratchet (ratchet híbrido: mecanismo de avance de claves) que combina acuerdo de claves clásico y poscuántico - Retrocompatible con ECIES-X25519 - Se convertirá en el valor predeterminado en la versión 2.11.0 (diciembre de 2025)

### Desuso del Router ElGamal

**CRÍTICO:** Los routers ElGamal quedaron obsoletos a partir de la versión 0.9.58 de la API (lanzamiento 2.2.0, marzo de 2023). Dado que la versión mínima recomendada de floodfill para consultar ahora es la 0.9.58, las implementaciones no necesitan implementar cifrado para routers floodfill ElGamal.

**Sin embargo:** Los destinos ElGamal se siguen admitiendo por compatibilidad con versiones anteriores. Los clientes que usan cifrado ElGamal todavía pueden comunicarse a través de routers ECIES.

### Detalles de ECIES-X25519-AEAD-Ratchet (mecanismo de cifrado autenticado con intercambio de claves ECIES basado en X25519 y un ratchet AEAD)

Este es el tipo criptográfico 4 en la especificación de criptografía de I2P. Proporciona:

**Características clave:** - Secreto hacia adelante mediante ratcheting (mecanismo de actualización escalonada de claves; nuevas claves para cada mensaje) - Almacenamiento reducido de etiquetas de sesión (8 bytes frente a 32 bytes) - Varios tipos de sesión (New Session, Existing Session, One-Time) - Basado en el protocolo Noise Noise_IK_25519_ChaChaPoly_SHA256 - Integrado con el algoritmo Double Ratchet de Signal

**Primitivas criptográficas:** - X25519 para acuerdo de claves Diffie-Hellman - ChaCha20 para cifrado de flujo - Poly1305 para autenticación de mensajes (AEAD, cifrado y autenticación con datos asociados) - SHA-256 para cálculo de hash - HKDF para derivación de claves

**Gestión de sesiones:** - Sesión nueva: Conexión inicial usando una clave de destino estática - Sesión existente: Mensajes posteriores usando etiquetas de sesión - Sesión de una sola vez: Sesiones de un único mensaje para menor sobrecarga

Consulte la [Especificación ECIES](/docs/specs/ecies/) y la [Propuesta 144](/proposals/144-ecies-x25519-aead-ratchet/) para obtener detalles técnicos completos.

---

## Estructuras comunes

Las siguientes estructuras son elementos de múltiples mensajes I2NP. No son mensajes completos.

### BuildRequestRecord (registro de solicitud de construcción) (ElGamal)

**OBSOLETO.** Solo se usa en la red actual cuando un tunnel contiene un router ElGamal. Consulta [Creación de tunnel ECIES](/docs/specs/implementation/) para el formato moderno.

**Propósito:** Un registro dentro de un conjunto de múltiples registros para solicitar la creación de un salto en el tunnel.

**Formato:**

Cifrado con ElGamal y AES (528 bytes en total):

```
+----+----+----+----+----+----+----+----+
| encrypted data (528 bytes)            |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
```
Estructura cifrada con ElGamal (528 bytes):

```
+----+----+----+----+----+----+----+----+
| toPeer (16 bytes)                     |
+----+----+----+----+----+----+----+----+
| ElGamal encrypted data (512 bytes)    |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+

toPeer :: First 16 bytes of SHA-256 hash of peer's RouterIdentity

encrypted_data :: ElGamal-2048 encrypted (bytes 1-256 and 258-513
                  of the 514-byte ElGamal block, with padding bytes
                  at positions 0 and 257 removed)
```
Estructura en texto claro (222 bytes antes del cifrado):

```
+----+----+----+----+----+----+----+----+
| receive_tunnel (4) | our_ident (32)   |
+----+----+----+----+                   +
|                                       |
+                   +----+----+----+----+
|                   | next_tunnel (4)   |
+----+----+----+----+----+----+----+----+
| next_ident (32 bytes)                 |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
| layer_key (32 bytes)                  |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
| iv_key (32 bytes)                     |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
| reply_key (32 bytes)                  |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
| reply_iv (16 bytes)                   |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|flag| request_time (4) | send_msg_id  |
+----+----+----+----+----+----+----+----+
     (4)                | padding (29)  |
+----+----+----+----+----+              +
|                                       |
+                             +----+----+
|                             |
+----+----+----+----+----+----+

receive_tunnel :: TunnelId (4 bytes, nonzero)
our_ident :: Hash (32 bytes)
next_tunnel :: TunnelId (4 bytes, nonzero)
next_ident :: Hash (32 bytes)
layer_key :: SessionKey (32 bytes)
iv_key :: SessionKey (32 bytes)
reply_key :: SessionKey (32 bytes)
reply_iv :: 16 bytes
flag :: Integer (1 byte)
request_time :: Integer (4 bytes, hours since epoch = time / 3600)
send_message_id :: Integer (4 bytes)
padding :: 29 bytes random data
```
**Notas:** - El cifrado ElGamal-2048 produce un bloque de 514 bytes, pero se eliminan los dos bytes de relleno (en las posiciones 0 y 257), quedando en 512 bytes - Véase [Especificación de creación de Tunnel](/docs/specs/implementation/) para los detalles de los campos - Código fuente: `net.i2p.data.i2np.BuildRequestRecord` - Constante: `EncryptedBuildRecord.RECORD_SIZE = 528`

### BuildRequestRecord (registro de solicitud de construcción) (ECIES-X25519 Long)

Para los router ECIES-X25519, introducidos en la versión 0.9.48 de la API. Usa 528 bytes para compatibilidad con versiones anteriores con tunnel mixtos.

**Formato:**

```
+----+----+----+----+----+----+----+----+
| toPeer (16 bytes)                     |
+----+----+----+----+----+----+----+----+
| ephemeral_key (32 bytes)              |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
| ChaCha20 encrypted data (464 bytes)   |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| Poly1305 MAC (16 bytes)               |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+

toPeer :: First 16 bytes of SHA-256 hash of peer's RouterIdentity
ephemeral_key :: X25519 ephemeral public key (32 bytes)
encrypted_data :: ChaCha20 encrypted (464 bytes)
mac :: Poly1305 message authentication code (16 bytes)
```
**Tamaño total:** 528 bytes (igual que ElGamal por compatibilidad)

Consulta [ECIES Tunnel Creation](/docs/specs/implementation/) para conocer la estructura del texto en claro y los detalles del cifrado.

### BuildRequestRecord (registro de solicitud de construcción) (ECIES-X25519 corto)

Solo para routers ECIES-X25519 (ECIES con X25519), a partir de la versión 0.9.51 de la API (lanzamiento 1.5.0). Este es el formato estándar actual.

**Formato:**

```
+----+----+----+----+----+----+----+----+
| toPeer (16 bytes)                     |
+----+----+----+----+----+----+----+----+
| ephemeral_key (32 bytes)              |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
| ChaCha20 encrypted data (154 bytes)   |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| Poly1305 MAC (16 bytes)               |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+

toPeer :: First 16 bytes of SHA-256 hash of peer's RouterIdentity
ephemeral_key :: X25519 ephemeral public key (32 bytes)
encrypted_data :: ChaCha20 encrypted (154 bytes)
mac :: Poly1305 message authentication code (16 bytes)
```
**Tamaño total:** 218 bytes (reducción del 59% respecto a 528 bytes)

**Diferencia clave:** Los registros cortos derivan TODAS las claves mediante HKDF (función de derivación de claves) en lugar de incluirlas explícitamente en el registro. Esto incluye: - Claves de capa (para el cifrado de tunnel) - Claves de IV (para el cifrado de tunnel) - Claves de respuesta (para build reply, respuesta de construcción) - IVs de respuesta (para build reply)

Todas las claves se derivan utilizando el mecanismo HKDF del protocolo Noise, a partir del secreto compartido del intercambio de claves X25519.

**Beneficios:** - 4 registros cortos caben en un mensaje de tunnel (873 bytes) - 3 mensajes de construcción de tunnel en lugar de mensajes separados para cada registro - Ancho de banda y latencia reducidos - Las mismas propiedades de seguridad que el formato largo

Consulte [Proposal 157](/proposals/157-new-tbm/) para la justificación y [Creación de tunnel ECIES](/docs/specs/implementation/) para la especificación completa.

**Código fuente:** - `net.i2p.data.i2np.ShortEncryptedBuildRecord` - Constante: `ShortEncryptedBuildRecord.RECORD_SIZE = 218`

### BuildResponseRecord (registro de respuesta de construcción) (ElGamal)

**OBSOLETO.** Solo se usa cuando el tunnel contiene un router ElGamal.

**Propósito:** Un registro dentro de un conjunto de múltiples registros con respuestas a una solicitud de construcción.

**Formato:**

Cifrado (528 bytes, mismo tamaño que BuildRequestRecord):

```
bytes 0-527 :: AES-encrypted record
```
Estructura sin cifrar:

```
+----+----+----+----+----+----+----+----+
| SHA-256 hash (32 bytes)               |
+                                       +
|        (hash of bytes 32-527)         |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
| random data (495 bytes)               |
~                                       ~
|                                  |ret |
+----+----+----+----+----+----+----+----+

bytes 0-31 :: SHA-256 hash of bytes 32-527
bytes 32-526 :: Random data (could be used for congestion info)
byte 527 :: Reply code (0 = accept, 30 = reject)
```
**Códigos de respuesta:** - `0` - Aceptar - `30` - Rechazar (ancho de banda excedido)

Consulte [Especificación de creación de Tunnel](/docs/specs/implementation/) para obtener detalles sobre el campo de respuesta.

### BuildResponseRecord (ECIES-X25519, esquema de cifrado ECIES con curva X25519)

Para routers ECIES-X25519, versión de API 0.9.48+. Mismo tamaño que la solicitud correspondiente (528 para la larga, 218 para la corta).

**Formato:**

Formato largo (528 bytes):

```
+----+----+----+----+----+----+----+----+
| ChaCha20 encrypted data (512 bytes)   |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| Poly1305 MAC (16 bytes)               |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
```
Formato corto (218 bytes):

```
+----+----+----+----+----+----+----+----+
| ChaCha20 encrypted data (202 bytes)   |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| Poly1305 MAC (16 bytes)               |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
```
**Estructura de texto en claro (ambos formatos):**

Contiene una estructura Mapping (formato clave-valor de I2P) con: - Código de estado de respuesta (obligatorio) - Parámetro de ancho de banda disponible ("b") (opcional, añadido en la API 0.9.65) - Otros parámetros opcionales para futuras extensiones

**Códigos de estado de respuesta:** - `0` - Éxito - `30` - Rechazo: ancho de banda excedido

Consulte [Creación de Tunnel ECIES](/docs/specs/implementation/) para la especificación completa.

### GarlicClove (submensaje "clove" de garlic encryption) (ElGamal/AES)

**ADVERTENCIA:** Este es el formato utilizado para las garlic cloves (submensajes del esquema garlic) dentro de los garlic messages (mensajes del esquema garlic) cifrados con ElGamal. El formato para los garlic messages y las garlic cloves de ECIES-AEAD-X25519-Ratchet es significativamente diferente. Consulta [Especificación de ECIES](/docs/specs/ecies/) para el formato moderno.

**Obsoleto para routers (API 0.9.58+), aún compatible para destinos.**

**Formato:**

Sin cifrar:

```
+----+----+----+----+----+----+----+----+
| Delivery Instructions (variable)      |
~                                       ~
+----+----+----+----+----+----+----+----+
| I2NP Message (variable)               |
~                                       ~
+----+----+----+----+----+----+----+----+
| Clove ID (4)  | Expiration (8)   |Cert|
+----+----+----+----+----+----+----+----+
                                    (3) |
+----+----+----+----+----+----+----+----+

Delivery Instructions :: Variable length (typically 1, 33, or 37 bytes)
I2NP Message :: Any I2NP message
Clove ID :: 4-byte Integer (random, checked for duplicates)
Expiration :: Date (8 bytes)
Certificate :: Always NULL (3 bytes total, all zeroes)
```
**Notas:** - Los clove (submensaje dentro de un GarlicMessage) nunca se fragmentan - Cuando el primer bit del byte de indicadores de Delivery Instructions es 0, el clove no está cifrado - Cuando el primer bit es 1, el clove está cifrado (función no implementada) - La longitud máxima es una función de la suma de longitudes de los clove y de la longitud máxima de GarlicMessage (mensaje de I2NP que encapsula múltiples cloves) - El certificado podría usarse con HashCash para "pagar" el enrutamiento (posible función futura) - Mensajes usados en la práctica: DataMessage, DeliveryStatusMessage, DatabaseStoreMessage - GarlicMessage puede contener GarlicMessage (anidamiento de GarlicMessage), pero esto no se usa en la práctica

Consulte [Garlic Routing](/docs/overview/garlic-routing/) (enrutamiento Garlic) para una visión general conceptual.

### GarlicClove (submensaje en garlic encryption de I2P) (ECIES-X25519-AEAD-Ratchet)

Para routers y destinos ECIES-X25519 (esquema criptográfico ECIES basado en X25519), versión de la API 0.9.46+. Este es el formato estándar actual.

**DIFERENCIA CRÍTICA:** ECIES garlic utiliza una estructura completamente distinta basada en bloques del protocolo Noise, en lugar de estructuras de clove (submensaje en garlic encryption) explícitas.

**Formato:**

Los mensajes garlic (técnica de encapsulación de múltiples mensajes en I2P) de ECIES contienen una serie de bloques:

```
Block structure:
+----+----+----+----+----+----+----+----+
|type| length    | data ...
+----+----+----+----+----+-//-

type :: 1 byte block type
length :: 2 bytes block length
data :: variable length data
```
**Tipos de bloques:** - `0` - Garlic Clove Block (contiene un mensaje I2NP) - `1` - Bloque de fecha y hora (marca de tiempo) - `2` - Bloque de opciones (opciones de entrega) - `3` - Bloque de relleno - `254` - Bloque de terminación (no implementado)

**Garlic Clove Block (bloque de diente de ajo) (tipo 0):**

```
+----+----+----+----+----+----+----+----+
|  0 | length    | Delivery Instructions |
+----+----+----+----+                    +
~                                       ~
+----+----+----+----+----+----+----+----+
| I2NP Message                          |
~                                       ~
+----+----+----+----+----+----+----+----+
| Clove ID (4)  | Expiration (4)        |
+----+----+----+----+----+----+----+----+
```
**Diferencias clave respecto al formato ElGamal:** - Usa una expiración de 4 bytes (segundos desde la época) en lugar de un Date de 8 bytes - Sin campo de certificado - Envuelto en una estructura de bloques con tipo y longitud - Todo el mensaje cifrado con ChaCha20/Poly1305 AEAD - Gestión de sesión mediante ratcheting (encadenamiento de claves)

Consulte la [Especificación ECIES](/docs/specs/ecies/) para obtener detalles completos sobre el marco del protocolo Noise y las estructuras de bloques.

### Instrucciones de entrega de Garlic Clove (submensaje individual dentro de un mensaje Garlic en I2P)

Este formato se utiliza tanto para los dientes de ajo de ElGamal como de ECIES. Especifica cómo entregar el mensaje contenido.

**ADVERTENCIA CRÍTICA:** Esta especificación es ÚNICAMENTE para Instrucciones de entrega dentro de Garlic Cloves (submensajes de garlic encryption). Las "Instrucciones de entrega" también se usan dentro de Mensajes de tunnel, donde el formato es significativamente diferente. Vea la [Especificación de mensajes de tunnel](/docs/specs/implementation/) para las instrucciones de entrega de tunnel. NO confunda estos dos formatos.

**Formato:**

La clave de sesión y el retardo no se utilizan y nunca están presentes, por lo que las tres longitudes posibles son: - 1 byte (LOCAL) - 33 bytes (ROUTER y DESTINO) - 37 bytes (TUNNEL)

```
+----+----+----+----+----+----+----+----+
|flag|                                  |
+----+                                  +
|       Session Key (optional, 32)     |
+                                       +
|                                       |
+    +----+----+----+----+--------------+
|    |                                  |
+----+                                  +
|       To Hash (optional, 32)         |
+                                       +
|                                       |
+    +----+----+----+----+--------------+
|    | Tunnel ID (4, opt)| Delay (4, opt)|
+----+----+----+----+----+----+----+----+

flag :: 1 byte
        Bit order: 76543210
        bit 7: encrypted? (Unimplemented, always 0)
               If 1, a 32-byte encryption session key follows
        bits 6-5: delivery type
               0x0 = LOCAL (0)
               0x1 = DESTINATION (1)
               0x2 = ROUTER (2)
               0x3 = TUNNEL (3)
        bit 4: delay included? (Not fully implemented, always 0)
               If 1, four delay bytes are included
        bits 3-0: reserved, set to 0 for compatibility

Session Key :: 32 bytes (Optional, unimplemented)
               Present if encrypt flag bit is set

To Hash :: 32 bytes (Optional)
           Present if delivery type is DESTINATION, ROUTER, or TUNNEL
           - DESTINATION: SHA256 hash of the destination
           - ROUTER: SHA256 hash of the router identity
           - TUNNEL: SHA256 hash of the gateway router identity

Tunnel ID :: 4 bytes (Optional)
             Present if delivery type is TUNNEL
             The destination tunnel ID (nonzero)

Delay :: 4 bytes (Optional, unimplemented)
         Present if delay included flag is set
         Specifies delay in seconds
```
**Longitudes típicas:** - entrega LOCAL: 1 byte (solo bandera) - entrega ROUTER / DESTINO: 33 bytes (bandera + hash) - entrega TUNNEL: 37 bytes (bandera + hash + ID de tunnel)

**Descripciones de los tipos de entrega:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Value</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">LOCAL</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Deliver to the local router (this router)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">DESTINATION</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Deliver to a destination (client) identified by hash</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ROUTER</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Deliver to another router identified by hash</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">TUNNEL</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Deliver to a tunnel gateway router</td>
    </tr>
  </tbody>
</table>
**Notas de implementación:** - El cifrado de clave de sesión no está implementado y el bit de indicador siempre es 0 - El retraso no está completamente implementado y el bit de indicador siempre es 0 - Para la entrega TUNNEL, el hash identifica el router de puerta de enlace y el tunnel ID especifica qué tunnel de entrada - Para la entrega DESTINATION, el hash es el SHA-256 de la clave pública del destino - Para la entrega ROUTER, el hash es el SHA-256 de la identidad del router

---

## Mensajes de I2NP

Especificaciones completas de mensajes para todos los tipos de mensajes de I2NP.

### Resumen de tipos de mensaje

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Message</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Since</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Status</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">DatabaseStore</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.6.1.10</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">DatabaseLookup</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.6.1.10</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">DatabaseSearchReply</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.6.1.10</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">DeliveryStatus</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">10</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.6.1.10</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Garlic</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">11</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.6.1.10</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">TunnelData</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">18</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.6.1.10</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">TunnelGateway</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">19</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.6.1.10</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Data</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">20</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.6.1.10</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">TunnelBuild</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">21</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.6.1.10</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">TunnelBuildReply</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">22</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.6.1.10</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">VariableTunnelBuild</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">23</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.7.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">VariableTunnelBuildReply</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">24</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.7.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ShortTunnelBuild</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">25</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.51</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">OutboundTunnelBuildReply</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">26</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.51</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
  </tbody>
</table>
**Reservado:** - Tipo 0: Reservado - Tipos 4-9: Reservados para uso futuro - Tipos 12-17: Reservados para uso futuro - Tipos 224-254: Reservados para mensajes experimentales - Tipo 255: Reservado para expansión futura

---

### DatabaseStore (Tipo 1)

**Propósito:** Un almacenamiento en la base de datos no solicitado, o la respuesta a un mensaje DatabaseLookup (búsqueda en la base de datos) exitoso.

**Contenido:** Un LeaseSet, LeaseSet2, MetaLeaseSet o EncryptedLeaseSet sin comprimir, o un RouterInfo (información del router) comprimido.

**Formato con el token de respuesta:**

```
+----+----+----+----+----+----+----+----+
| SHA256 Hash as key (32 bytes)        |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|type| reply token (4)   | reply_tunnelId
+----+----+----+----+----+----+----+----+
     (4)               | reply gateway  |
+----+----+----+----+----+              +
|       SHA256 hash (32 bytes)          |
+                                       +
|                                       |
+                                  +----+
|                                  |
+----+----+----+----+----+----+----+
| data ...
+----+-//

key :: 32 bytes
       SHA256 hash (the "real" hash, not routing key)

type :: 1 byte
        Type identifier
        bit 0:
            0 = RouterInfo
            1 = LeaseSet or variants
        bits 3-1: (as of 0.9.38)
            0: RouterInfo or LeaseSet (types 0 or 1)
            1: LeaseSet2 (type 3)
            2: EncryptedLeaseSet (type 5)
            3: MetaLeaseSet (type 7)
            4-7: Unsupported, invalid
        bits 7-4:
            Reserved, set to 0

reply token :: 4 bytes
               If greater than zero, a DeliveryStatusMessage is
               requested with the Message ID set to the reply token
               A floodfill router is also expected to flood the data
               to the closest floodfill peers

reply_tunnelId :: 4 bytes (only if reply token > 0)
                  TunnelId of the inbound gateway of the tunnel
                  for the response
                  If 0, reply is sent directly to reply gateway

reply gateway :: 32 bytes (only if reply token > 0)
                 SHA256 hash of the RouterInfo
                 If reply_tunnelId is nonzero: inbound gateway router
                 If reply_tunnelId is zero: router to send reply to

data :: Variable length
        If type == 0: 2-byte Integer length + gzip-compressed RouterInfo
        If type == 1: Uncompressed LeaseSet
        If type == 3: Uncompressed LeaseSet2
        If type == 5: Uncompressed EncryptedLeaseSet
        If type == 7: Uncompressed MetaLeaseSet
```
**Formato con token de respuesta == 0:**

```
+----+----+----+----+----+----+----+----+
| SHA256 Hash as key (32 bytes)        |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|type|         0         | data ...
+----+----+----+----+----+-//
```
**Notas:** - Por seguridad, los campos de respuesta se ignoran si el mensaje se recibe a través de un tunnel - La clave es el hash «real» de la RouterIdentity (identidad del router) o Destination (destino), NO la routing key (clave de enrutamiento) - Los tipos 3, 5 y 7 (variantes de LeaseSet2) se añadieron en la versión 0.9.38 (API 0.9.38). Consulte [Propuesta 123](/proposals/123-new-netdb-entries/) para más detalles - Estos tipos solo deben enviarse a routers con versión de API 0.9.38 o superior - Como optimización para reducir conexiones, si el tipo es un LeaseSet, se incluye el token de respuesta, el ID de tunnel de respuesta es distinto de cero, y el par puerta de enlace/tunnelID de respuesta se encuentra en el LeaseSet como un lease (arrendamiento), el destinatario puede redirigir la respuesta a cualquier otro lease en el LeaseSet - **Formato gzip de RouterInfo:** Para ocultar el SO del router y la implementación, imite la implementación del router en Java estableciendo la hora de modificación en 0 y el byte del SO en 0xFF, y establezca XFL en 0x02 (compresión máxima, algoritmo más lento) según la RFC 1952. Primeros 10 bytes: `1F 8B 08 00 00 00 00 00 02 FF`

**Código fuente:** - `net.i2p.data.i2np.DatabaseStoreMessage` - `net.i2p.data.RouterInfo` (para la estructura RouterInfo) - `net.i2p.data.LeaseSet` (para la estructura LeaseSet)

---

### DatabaseLookup (Tipo 2)

**Propósito:** Una solicitud para consultar un elemento en la base de datos de la red (netDb). La respuesta es un DatabaseStore o un DatabaseSearchReply.

**Formato:**

```
+----+----+----+----+----+----+----+----+
| SHA256 hash as the key (32 bytes)    |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
| SHA256 hash of the from router (32)  |
+    or reply tunnel gateway            +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|flag| reply_tunnelId (4)| size (2)|   |
+----+----+----+----+----+----+----+    +
| SHA256 of key1 to exclude (32 bytes) |
+                                       +
|                                       |
+                                  +----+
|                                  |    |
+----+----+----+----+----+----+----+    +
| SHA256 of key2 to exclude (32)       |
+                                       +
~                                       ~
|                                       |
+                                  +----+
|                                  |    |
+----+----+----+----+----+----+----+    +
|   Session key if reply encryption     |
+       requested (32 bytes)             +
|                                       |
+                                  +----+
|                                  |tags|
+----+----+----+----+----+----+----+----+
|   Session tags if reply encryption    |
+       requested (variable)             +
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+

key :: 32 bytes
       SHA256 hash of the object to lookup

from :: 32 bytes
        If deliveryFlag == 0: SHA256 hash of RouterInfo (sender)
        If deliveryFlag == 1: SHA256 hash of reply tunnel gateway

flags :: 1 byte
         Bit order: 76543210
         bit 0: deliveryFlag
             0 = send reply directly
             1 = send reply to some tunnel
         bit 1: encryptionFlag
             Through 0.9.5: must be 0
             As of 0.9.6: ignored
             As of 0.9.7:
                 0 = send unencrypted reply
                 1 = send AES encrypted reply using key and tag
         bits 3-2: lookup type flags
             Through 0.9.5: must be 00
             As of 0.9.6: ignored
             As of 0.9.16:
                 00 = ANY (deprecated, use LS or RI as of 0.9.16)
                 01 = LS lookup (LeaseSet or variants)
                 10 = RI lookup (RouterInfo)
                 11 = exploration lookup (RouterInfo, non-floodfill)
         bit 4: ECIESFlag
             Before 0.9.46: ignored
             As of 0.9.46:
                 0 = send unencrypted or ElGamal reply
                 1 = send ChaCha/Poly encrypted reply using key
         bits 7-5:
             Reserved, set to 0

reply_tunnelId :: 4 bytes (only if deliveryFlag == 1)
                  TunnelId of the tunnel to send reply to (nonzero)

size :: 2 bytes
        Integer (valid range: 0-512)
        Number of peers to exclude from DatabaseSearchReply

excludedPeers :: $size SHA256 hashes of 32 bytes each
                 If lookup fails, exclude these peers from the reply
                 If includes a hash of all zeroes, the request is
                 exploratory (return non-floodfill routers only)

reply_key :: 32 bytes (conditional, see encryption modes below)
reply_tags :: 1 byte count + variable length tags (conditional)
```
**Modos de cifrado de las respuestas:**

**NOTA:** Los routers ElGamal están obsoletos a partir de la API 0.9.58. Como la versión mínima recomendada de floodfill para consultar es ahora la 0.9.58, las implementaciones no necesitan implementar cifrado para los routers floodfill de ElGamal. Los destinos ElGamal siguen siendo compatibles.

El bit 4 de la bandera (ECIESFlag) se utiliza en combinación con el bit 1 (encryptionFlag) para determinar el modo de cifrado de la respuesta:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Flag bits 4,1</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">From</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">To Router</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Reply</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">DH?</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0 0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Any</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Any</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">No encryption</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">n/a</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">No encryption</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0 1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ElG</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ElG</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">AES</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">No</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">As of 0.9.7, deprecated 0.9.58</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1 0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ECIES</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ElG</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">AEAD</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">No</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">As of 0.9.46, deprecated 0.9.58</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1 0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ECIES</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ECIES</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">AEAD</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">No</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">As of 0.9.49, current standard</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1 1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ElG</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ECIES</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">AES</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">TBD, future</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1 1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ECIES</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ECIES</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">AEAD</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">TBD, future</td>
    </tr>
  </tbody>
</table>
**Sin cifrado (flags 0,0):**

reply_key, tags y reply_tags no están presentes.

**ElG a ElG (indicadores 0,1) - OBSOLETO:**

Compatible desde la 0.9.7, obsoleto desde la 0.9.58.

```
reply_key :: 32 byte SessionKey (big-endian)
             CSRNG(32) random data

tags :: 1 byte Integer (1-32, typically 1)
        Number of reply tags that follow

reply_tags :: One or more 32-byte SessionTags
              Each is CSRNG(32) random data
```
**ECIES (Esquema de Cifrado Integrado de Curva Elíptica) a ElG (ElGamal) (indicadores 1,0) - OBSOLETO:**

Compatible a partir de la versión 0.9.46, en desuso a partir de la versión 0.9.58.

```
reply_key :: 32 byte ECIES SessionKey (big-endian)
             CSRNG(32) random data

tags :: 1 byte Integer (required value: 1)
        Number of reply tags that follow

reply_tags :: One 8-byte ECIES SessionTag
              CSRNG(8) random data
```
La respuesta es un mensaje de sesión existente de ECIES tal como se define en [Especificación de ECIES](/docs/specs/ecies/):

```
+----+----+----+----+----+----+----+----+
| Session Tag (8 bytes)                 |
+----+----+----+----+----+----+----+----+
| ChaCha20 encrypted payload            |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| Poly1305 MAC (16 bytes)               |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+

tag :: 8 byte reply_tag
k :: 32 byte session key (the reply_key)
n :: 0 (nonce)
ad :: The 8 byte reply_tag
payload :: Plaintext data (DSM or DSRM)
ciphertext = ENCRYPT(k, n, payload, ad)
```
**ECIES (Esquema de cifrado integrado basado en curvas elípticas) a ECIES (flags 1,0) - ESTÁNDAR ACTUAL:**

Un destino ECIES o un router envía una consulta a un router ECIES. Compatible desde la versión 0.9.49.

El mismo formato que "ECIES to ElG" de arriba. El cifrado del mensaje de búsqueda se especifica en [ECIES Routers](/docs/specs/ecies/#routers). El solicitante es anónimo.

**ECIES (esquema de cifrado integrado con curvas elípticas) a ECIES con DH (Diffie-Hellman, intercambio de claves) (indicadores 1,1) - FUTURO:**

Todavía no está completamente definido. Consulte [Propuesta 156](/proposals/156-ecies-routers/).

**Notas:** - Antes de la 0.9.16, la clave podía corresponder a un RouterInfo (información del router) o a un LeaseSet (conjunto de arrendamientos) (mismo espacio de claves, sin indicador para distinguirlos) - Las respuestas cifradas solo son útiles cuando la respuesta es a través de un tunnel - El número de etiquetas incluidas (tags) podría ser mayor que uno si se implementan estrategias alternativas de búsqueda en DHT (tabla hash distribuida) - La clave de búsqueda y las claves de exclusión son los hashes "reales", NO claves de enrutamiento - Los tipos 3, 5 y 7 (variantes de LeaseSet2) pueden devolverse a partir de la 0.9.38. Véase [Propuesta 123](/proposals/123-new-netdb-entries/) - **Notas sobre la búsqueda exploratoria:** Una búsqueda exploratoria se define como aquella que devuelve una lista de hashes que no son floodfill cercanos a la clave. Sin embargo, las implementaciones varían: Java sí busca la clave de búsqueda para un RI y devuelve un DatabaseStore (almacenamiento de base de datos) si está presente; i2pd no lo hace. Por lo tanto, no se recomienda usar una búsqueda exploratoria para hashes recibidos previamente

**Código fuente:** - `net.i2p.data.i2np.DatabaseLookupMessage` - Cifrado: `net.i2p.crypto.SessionKeyManager`

---

### DatabaseSearchReply (Tipo 3)

**Propósito:** La respuesta a un mensaje DatabaseLookup fallido.

**Contenido:** Una lista de hashes de router más cercanos a la clave solicitada.

**Formato:**

```
+----+----+----+----+----+----+----+----+
| SHA256 hash as query key (32 bytes)  |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
| num| peer_hashes (variable)           |
+----+                                  +
|                                       |
~                                       ~
|                                       |
+    +----+----+----+----+----+----+----+
|    | from (32 bytes)                  |
+----+                                  +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+    +----+----+----+----+----+----+----+
|    |
+----+

key :: 32 bytes
       SHA256 of the object being searched

num :: 1 byte Integer
       Number of peer hashes that follow (0-255)

peer_hashes :: $num SHA256 hashes of 32 bytes each (total $num*32 bytes)
               SHA256 of the RouterIdentity that the sender thinks is
               close to the key

from :: 32 bytes
        SHA256 of the RouterInfo of the router this reply was sent from
```
**Notas:** - El hash 'from' no está autenticado y no puede considerarse confiable - Los hashes de pares devueltos no están necesariamente más cerca de la clave que el router consultado. Para respuestas a búsquedas normales, esto facilita el descubrimiento de nuevos floodfills y la búsqueda "hacia atrás" (más lejos de la clave) para mayor robustez - Para las búsquedas de exploración, la clave suele generarse aleatoriamente. Los peer_hashes que no son floodfill pueden seleccionarse usando un algoritmo optimizado (p. ej., pares cercanos pero no necesariamente los más cercanos) para evitar el ordenamiento ineficiente de toda la base de datos local. También pueden emplearse estrategias de almacenamiento en caché. Esto depende de la implementación - **Número típico de hashes devueltos:** 3 - **Número máximo recomendado de hashes a devolver:** 16 - La clave de búsqueda, los hashes de pares y el hash 'from' son hashes "reales", NO claves de enrutamiento - Si num es 0, esto indica que no se encontraron pares más cercanos (callejón sin salida)

**Código fuente:** - `net.i2p.data.i2np.DatabaseSearchReplyMessage`

---

### DeliveryStatus (estado de entrega, Tipo 10)

**Propósito:** Un acuse de recibo simple de un mensaje. Generalmente creado por el emisor del mensaje y encapsulado en un Garlic Message (mensaje Garlic de I2P que encapsula otros mensajes) junto con el propio mensaje, para que el destino lo devuelva.

**Contenido:** El ID del mensaje entregado y la hora de creación o de llegada.

**Formato:**

```
+----+----+----+----+----+----+----+----+----+----+----+----+
| msg_id (4)            | time_stamp (8)                    |
+----+----+----+----+----+----+----+----+----+----+----+----+

msg_id :: Integer (4 bytes)
          Unique ID of the message we deliver the DeliveryStatus for
          (see I2NP Message Header for details)

time_stamp :: Date (8 bytes)
              Time the message was successfully created or delivered
```
**Notas:** - La marca de tiempo siempre la establece el creador a la hora actual. Sin embargo, en el código hay varios usos de esto y podrían añadirse más en el futuro - Este mensaje también se usa como confirmación de sesión establecida en SSU. En este caso, el ID del mensaje se establece en un número aleatorio, y el "arrival time" (hora de llegada) se establece en el ID actual a nivel de red, que es 2 (es decir, `0x0000000000000002`) - DeliveryStatus (mensaje de estado de entrega) suele ir envuelto en un GarlicMessage (mensaje "garlic") y se envía a través de un tunnel para proporcionar acuse de recibo sin revelar al remitente - Se utiliza para pruebas de tunnel con el fin de medir la latencia y la fiabilidad

**Código fuente:** - `net.i2p.data.i2np.DeliveryStatusMessage` - Usado en: `net.i2p.router.tunnel.InboundEndpointProcessor` para pruebas de tunnel

---

### GarlicMessage (Tipo 11)

**ADVERTENCIA:** Este es el formato utilizado para garlic messages cifrados con ElGamal (mensajes "garlic" de I2P, que agrupan múltiples mensajes en uno). El formato para los garlic messages de ECIES-AEAD-X25519-Ratchet es significativamente diferente. Consulta [ECIES Specification](/docs/specs/ecies/) para el formato actual.

**Propósito:** Se utiliza para encapsular varios mensajes I2NP cifrados.

**Contenido:** Al descifrarse, consiste en una serie de Garlic Cloves (submensajes individuales) y datos adicionales, también llamado Clove Set (conjunto de submensajes).

**Formato cifrado:**

```
+----+----+----+----+----+----+----+----+
| length (4)            | data          |
+----+----+----+----+----+              +
|                                       |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+

length :: 4 byte Integer
          Number of bytes that follow (0 to 64 KB)

data :: $length bytes
        ElGamal encrypted data
```
**Datos descifrados (Clove Set — conjunto de submensajes 'cloves' en garlic encryption):**

```
+----+----+----+----+----+----+----+----+
| num| clove 1 (variable)               |
+----+                                  +
|                                       |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| clove 2 (variable)                    |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| Certificate (3) | Message_ID (4)  |
+----+----+----+----+----+----+----+----+
    Expiration (8)                  |
+----+----+----+----+----+----+----+----+

num :: 1 byte Integer
       Number of GarlicCloves to follow

clove :: GarlicClove (see GarlicClove structure above)

Certificate :: Always NULL (3 bytes total, all zeroes)

Message_ID :: 4 byte Integer

Expiration :: Date (8 bytes)
```
**Notas:** - Cuando no está cifrado, los datos contienen uno o más Garlic Cloves - El bloque cifrado con AES se rellena hasta un mínimo de 128 bytes; con la Etiqueta de sesión de 32 bytes, el tamaño mínimo del mensaje cifrado es 160 bytes; con el campo de longitud de 4 bytes, el tamaño mínimo del Garlic Message (mensaje "Garlic", formato de mensaje de I2P) es 164 bytes - La longitud máxima real es inferior a 64 KB (límite práctico de alrededor de 61.2 KB para mensajes de tunnel) - Consulte [Especificación ElGamal/AES](/docs/legacy/elgamal-aes/) para obtener detalles de cifrado - Consulte [Garlic Routing](/docs/overview/garlic-routing/) para una visión conceptual general - El tamaño mínimo de 128 bytes del bloque cifrado con AES no es configurable actualmente - El ID de mensaje generalmente se establece en un número aleatorio al transmitir y parece ignorarse al recibir - El certificado posiblemente podría usarse con HashCash para "pagar" el enrutamiento (posible función futura) - **Estructura de cifrado ElGamal:** etiqueta de sesión de 32 bytes + clave de sesión cifrada con ElGamal + carga útil cifrada con AES

**Para el formato ECIES-X25519-AEAD-Ratchet (estándar actual para routers):**

Véase [Especificación de ECIES](/docs/specs/ecies/) y [Propuesta 144](/proposals/144-ecies-x25519-aead-ratchet/).

**Código fuente:** - `net.i2p.data.i2np.GarlicMessage` - Cifrado: `net.i2p.crypto.elgamal.ElGamalAESEngine` (obsoleto) - Cifrado moderno: `net.i2p.crypto.ECIES` paquetes

---

### TunnelData (Tipo 18)

**Propósito:** Un mensaje enviado desde la puerta de enlace del tunnel o desde un participante al siguiente participante o al extremo. Los datos tienen longitud fija y contienen mensajes I2NP que están fragmentados, agrupados en lotes, rellenados y cifrados.

**Formato:**

```
+----+----+----+----+----+----+----+----+
| tunnelID (4)          | data (1024)   |
+----+----+----+----+----+              +
|                                       |
~                                       ~
|                                       |
+                   +----+----+----+----+
|                   |
+----+----+----+----+

tunnelId :: 4 bytes
            TunnelId identifying the tunnel this message is directed at
            Nonzero

data :: 1024 bytes
        Payload data, fixed to 1024 bytes
```
**Estructura de la carga útil (1024 bytes):**

```
Bytes 0-15: Initialization Vector (IV) for AES encryption
Bytes 16-1023: Encrypted tunnel message data (1008 bytes)
```
**Notas:** - El ID de mensaje de I2NP para TunnelData (datos del tunnel) se establece en un nuevo número aleatorio en cada salto - El formato del mensaje de tunnel (dentro de los datos cifrados) está especificado en [Especificación del mensaje de tunnel](/docs/specs/implementation/) - Cada salto descifra una capa usando AES-256 en modo CBC - El IV (vector de inicialización) se actualiza en cada salto usando los datos descifrados - El tamaño total es exactamente 1,028 bytes (4 tunnelId + 1024 datos) - Esta es la unidad fundamental del tráfico de tunnel - Los mensajes TunnelData transportan mensajes I2NP fragmentados (GarlicMessage, DatabaseStore, etc.)

**Código fuente:** - `net.i2p.data.i2np.TunnelDataMessage` - Constante: `TunnelDataMessage.DATA_LENGTH = 1024` - Procesamiento: `net.i2p.router.tunnel.InboundGatewayProcessor`

---

### TunnelGateway (puerta de enlace de tunnel) (Tipo 19)

**Propósito:** Encapsula otro mensaje I2NP para ser enviado dentro de un tunnel en la puerta de enlace de entrada de dicho tunnel.

**Formato:**

```
+----+----+----+----+----+----+----+-//
| tunnelId (4)          | length (2)| data...
+----+----+----+----+----+----+----+-//

tunnelId :: 4 bytes
            TunnelId identifying the tunnel this message is directed at
            Nonzero

length :: 2 byte Integer
          Length of the payload

data :: $length bytes
        Actual payload of this message
```
**Notas:** - La carga útil es un mensaje I2NP con un encabezado estándar de 16 bytes - Se usa para inyectar mensajes en tunnels desde el router local - La puerta de enlace fragmenta el mensaje incluido si es necesario - Tras la fragmentación, los fragmentos se encapsulan en mensajes TunnelData - TunnelGateway nunca se envía por la red; es un tipo de mensaje interno usado antes del procesamiento del tunnel

**Código fuente:** - `net.i2p.data.i2np.TunnelGatewayMessage` - Procesamiento: `net.i2p.router.tunnel.OutboundGatewayProcessor`

---

### DataMessage (mensaje de datos) (Tipo 20)

**Propósito:** Utilizado por Garlic Messages (mensajes "garlic") y Garlic Cloves (clavos "garlic") para encapsular datos arbitrarios (normalmente datos de aplicación cifrados de extremo a extremo).

**Formato:**

```
+----+----+----+----+----+----+-//-+
| length (4)            | data...    |
+----+----+----+----+----+----+-//-+

length :: 4 bytes
          Length of the payload

data :: $length bytes
        Actual payload of this message
```
**Notas:** - Este mensaje no contiene información de enrutamiento y nunca se enviará "sin encapsular" - Solo se usa dentro de Garlic messages (mensajes Garlic de I2P) - Suele contener datos de aplicación cifrados de extremo a extremo (HTTP, IRC, correo electrónico, etc.) - Los datos suelen ser una carga útil cifrada con ElGamal/AES o ECIES - La longitud máxima práctica es de alrededor de 61,2 KB debido a los límites de fragmentación de mensajes de tunnel

**Código fuente:** - `net.i2p.data.i2np.DataMessage`

---

### TunnelBuild (Tipo 21)

**OBSOLETO.** Utilice VariableTunnelBuild (tipo 23) o ShortTunnelBuild (tipo 25).

**Propósito:** Solicitud de construcción de tunnel de longitud fija para 8 saltos.

**Formato:**

```
+----+----+----+----+----+----+----+----+
| Record 0 (528 bytes)                  |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| Record 1 (528 bytes)                  |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| Record 7 (528 bytes)                  |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+

Just 8 BuildRequestRecords attached together
Record size: 528 bytes
Total size: 8 × 528 = 4,224 bytes
```
**Notas:** - A partir de la versión 0.9.48, puede contener ECIES-X25519 BuildRequestRecords (registros de solicitud de construcción). Véase [Creación de tunnel ECIES](/docs/specs/implementation/) - Véase [Especificación de creación de tunnel](/docs/specs/implementation/) para obtener detalles - El ID de mensaje I2NP para este mensaje debe establecerse según la especificación de creación de tunnel - Aunque rara vez se ve en la red actual (reemplazado por VariableTunnelBuild (construcción de túnel variable)), aún puede usarse para tunnels muy largos y no ha sido marcado formalmente como obsoleto - Routers aún deben implementar esto por compatibilidad - El formato fijo de 8 registros es inflexible y desperdicia ancho de banda para tunnels más cortos

**Código fuente:** - `net.i2p.data.i2np.TunnelBuildMessage` - Constante: `TunnelBuildMessageBase.MAX_RECORD_COUNT = 8`

---

### TunnelBuildReply (Tipo 22)

**OBSOLETO.** Usa VariableTunnelBuildReply (tipo 24) o OutboundTunnelBuildReply (tipo 26).

**Propósito:** Respuesta de construcción de tunnel de longitud fija de 8 saltos.

**Formato:**

Mismo formato que TunnelBuildMessage, con BuildResponseRecords en lugar de BuildRequestRecords.

```
Total size: 8 × 528 = 4,224 bytes
```
**Notas:** - A partir de la versión 0.9.48, puede contener ECIES-X25519 BuildResponseRecords (registros de respuesta de construcción). Véase [ECIES Tunnel Creation](/docs/specs/implementation/) - Véase [Tunnel Creation Specification](/docs/specs/implementation/) para más detalles - El ID de mensaje I2NP de este mensaje debe establecerse de acuerdo con la Tunnel Creation Specification - Aunque rara vez se ve en la red actual (reemplazado por VariableTunnelBuildReply (respuesta de construcción de tunnel variable)), aún puede usarse para tunnels muy largos y no se ha declarado obsoleto formalmente - Los routers aún deben implementar esto por compatibilidad

**Código fuente:** - `net.i2p.data.i2np.TunnelBuildReplyMessage`

---

### VariableTunnelBuild (Tipo 23)

**Propósito:** Construcción de tunnel de longitud variable de 1 a 8 saltos. Admite tanto routers ElGamal como ECIES-X25519.

**Formato:**

```
+----+----+----+----+----+----+----+----+
| num| BuildRequestRecords (variable)   |
+----+----+----+----+----+----+----+----+

num :: 1 byte Integer
       Valid values: 1-8

BuildRequestRecords :: $num records of 528 bytes each

Record size: 528 bytes
Total size: 1 + ($num × 528) bytes
```
**Notas:** - A partir de la 0.9.48, puede contener ECIES-X25519 BuildRequestRecords (registros de solicitud de construcción). Consulta [Creación de Tunnel ECIES](/docs/specs/implementation/) - Introducida en la versión 0.7.12 (2009) del router - Puede que no se envíe a participantes del tunnel anteriores a la versión 0.7.12 - Consulta [Especificación de Creación de Tunnel](/docs/specs/implementation/) para más detalles - El ID de mensaje de I2NP debe establecerse de acuerdo con la especificación de creación de tunnel - **Número típico de registros:** 4 (para un tunnel de 4 saltos) - **Tamaño total típico:** 1 + (4 × 528) = 2,113 bytes - Este es el mensaje estándar de construcción de tunnel para routers ElGamal - Los routers ECIES suelen usar ShortTunnelBuild (tipo 25) en su lugar

**Código fuente:** - `net.i2p.data.i2np.VariableTunnelBuildMessage`

---

### VariableTunnelBuildReply (Tipo 24)

**Propósito:** Respuesta de construcción de tunnel de longitud variable para 1-8 saltos. Es compatible con ambos routers, ElGamal y ECIES-X25519.

**Formato:**

El mismo formato que VariableTunnelBuildMessage, con BuildResponseRecords en lugar de BuildRequestRecords.

```
+----+----+----+----+----+----+----+----+
| num| BuildResponseRecords (variable)  |
+----+----+----+----+----+----+----+----+

num :: 1 byte Integer
       Valid values: 1-8

BuildResponseRecords :: $num records of 528 bytes each

Record size: 528 bytes
Total size: 1 + ($num × 528) bytes
```
**Notas:** - A partir de la versión 0.9.48, puede contener ECIES-X25519 BuildResponseRecords (registros BuildResponse de ECIES-X25519). Consulte [ECIES Tunnel Creation](/docs/specs/implementation/) - Introducido en la versión 0.7.12 del router (2009) - No puede enviarse a participantes del tunnel con versiones anteriores a la 0.7.12 - Consulte [Tunnel Creation Specification](/docs/specs/implementation/) para más detalles - El ID de mensaje de I2NP debe establecerse según la especificación de creación de tunnel - **Número típico de registros:** 4 - **Tamaño total típico:** 2,113 bytes

**Código fuente:** - `net.i2p.data.i2np.VariableTunnelBuildReplyMessage`

---

### ShortTunnelBuild (Tipo 25)

**Propósito:** Mensajes cortos de construcción de tunnel solo para routers ECIES-X25519. Presentado en la versión de la API 0.9.51 (lanzamiento 1.5.0, agosto de 2021). Este es el estándar vigente para la construcción de tunnel con ECIES (Esquema de Cifrado Integrado sobre Curvas Elípticas).

**Formato:**

```
+----+----+----+----+----+----+----+----+
| num| ShortBuildRequestRecords (var)   |
+----+----+----+----+----+----+----+----+

num :: 1 byte Integer
       Valid values: 1-8

ShortBuildRequestRecords :: $num records of 218 bytes each

Record size: 218 bytes
Total size: 1 + ($num × 218) bytes
```
**Notas:** - Introducido en la versión del router 0.9.51 (lanzamiento 1.5.0, agosto de 2021) - No se debe enviar a participantes del tunnel con una API anterior a la versión 0.9.51 - Consulte [ECIES Tunnel Creation](/docs/specs/implementation/) para la especificación completa - Consulte [Propuesta 157](/proposals/157-new-tbm/) para la justificación - **Número típico de registros:** 4 - **Tamaño total típico:** 1 + (4 × 218) = 873 bytes - **Ahorro de ancho de banda:** 59% más pequeño que VariableTunnelBuild (873 vs 2,113 bytes) - **Beneficio de rendimiento:** 4 registros cortos caben en un mensaje de tunnel; VariableTunnelBuild requiere 3 mensajes de tunnel - Este es ahora el formato estándar de construcción de tunnel para tunnels ECIES-X25519 puros - Los registros derivan claves mediante HKDF en lugar de incluirlas explícitamente

**Código fuente:** - `net.i2p.data.i2np.ShortTunnelBuildMessage` - Constante: `ShortEncryptedBuildRecord.RECORD_SIZE = 218`

---

### OutboundTunnelBuildReply (Tipo 26)

**Propósito:** Enviado desde el extremo de salida de un nuevo tunnel al originador. Solo para routers ECIES-X25519. Introducido en la versión 0.9.51 de la API (lanzamiento 1.5.0, agosto de 2021).

**Formato:**

El mismo formato que ShortTunnelBuildMessage, con ShortBuildResponseRecords en lugar de ShortBuildRequestRecords.

```
+----+----+----+----+----+----+----+----+
| num| ShortBuildResponseRecords (var)  |
+----+----+----+----+----+----+----+----+

num :: 1 byte Integer
       Valid values: 1-8

ShortBuildResponseRecords :: $num records of 218 bytes each

Record size: 218 bytes
Total size: 1 + ($num × 218) bytes
```
**Notas:** - Introducido en router versión 0.9.51 (lanzamiento 1.5.0, agosto de 2021) - Consulta [ECIES Tunnel Creation](/docs/specs/implementation/) para la especificación completa - **Número típico de registros:** 4 - **Tamaño total típico:** 873 bytes - Esta respuesta se envía desde el extremo de salida (OBEP) de vuelta al creador del tunnel a través del recién creado tunnel de salida - Proporciona confirmación de que todos los saltos aceptaron la construcción del tunnel

**Código fuente:** - `net.i2p.data.i2np.OutboundTunnelBuildReplyMessage`

---

## Referencias

### Especificaciones oficiales

- **[Especificación de I2NP](/docs/specs/i2np/)** - Especificación completa del formato de mensajes de I2NP
- **[Estructuras comunes](/docs/specs/common-structures/)** - Tipos de datos y estructuras utilizados en todo I2P
- **[Creación de tunnel](/docs/specs/implementation/)** - Creación de tunnel ElGamal (obsoleto)
- **[Creación de tunnel con ECIES](/docs/specs/implementation/)** - Creación de tunnel con ECIES-X25519 (actual)
- **[Mensaje de tunnel](/docs/specs/implementation/)** - Formato de los mensajes de tunnel e instrucciones de entrega
- **[Especificación de NTCP2](/docs/specs/ntcp2/)** - Protocolo de transporte TCP
- **[Especificación de SSU2](/docs/specs/ssu2/)** - Protocolo de transporte UDP
- **[Especificación de ECIES](/docs/specs/ecies/)** - Cifrado ECIES-X25519-AEAD-Ratchet
- **[Especificación de criptografía](/docs/specs/cryptography/)** - Primitivas criptográficas de bajo nivel
- **[Especificación de I2CP](/docs/specs/i2cp/)** - Especificación del protocolo de cliente
- **[Especificación de datagramas](/docs/api/datagrams/)** - Formatos Datagram2 y Datagram3

### Propuestas

- **[Propuesta 123](/proposals/123-new-netdb-entries/)** - Nuevas entradas de netDB (LeaseSet2, EncryptedLeaseSet, MetaLeaseSet)
- **[Propuesta 144](/proposals/144-ecies-x25519-aead-ratchet/)** - Cifrado ECIES-X25519-AEAD-Ratchet (mecanismo de avance criptográfico)
- **[Propuesta 154](/proposals/154-ecies-lookups/)** - Búsqueda cifrada en la base de datos
- **[Propuesta 156](/proposals/156-ecies-routers/)** - routers ECIES
- **[Propuesta 157](/proposals/157-new-tbm/)** - Mensajes más pequeños para la construcción de tunnel (formato corto)
- **[Propuesta 159](/proposals/159-ssu2/)** - Transporte SSU2
- **[Propuesta 161](/es/proposals/161-ri-dest-padding/)** - Relleno compresible
- **[Propuesta 163](/proposals/163-datagram2/)** - Datagram2 y Datagram3
- **[Propuesta 167](/proposals/167-service-records/)** - Parámetros del registro de servicio de LeaseSet
- **[Propuesta 168](/proposals/168-tunnel-bandwidth/)** - Parámetros de ancho de banda para la construcción de tunnel
- **[Propuesta 169](/proposals/169-pq-crypto/)** - Criptografía híbrida poscuántica

### Documentación

- **[Garlic Routing](/docs/overview/garlic-routing/)** - Agrupación en capas de mensajes
- **[ElGamal/AES](/docs/legacy/elgamal-aes/)** - Esquema de cifrado obsoleto
- **[Implementación de tunnel](/docs/specs/implementation/)** - Fragmentación y procesamiento
- **[Base de datos de red](/docs/specs/common-structures/)** - Tabla hash distribuida
- **[Transporte NTCP2](/docs/specs/ntcp2/)** - Especificación del transporte TCP
- **[Transporte SSU2](/docs/specs/ssu2/)** - Especificación del transporte UDP
- **[Introducción técnica](/docs/overview/tech-intro/)** - Descripción general de la arquitectura de I2P

### Código fuente

- **[Repositorio de Java I2P](https://i2pgit.org/I2P_Developers/i2p.i2p)** - Implementación oficial en Java
- **[Espejo en GitHub](https://github.com/i2p/i2p.i2p)** - Espejo en GitHub de Java I2P
- **[Repositorio de i2pd](https://github.com/PurpleI2P/i2pd)** - Implementación en C++

### Ubicaciones clave del código fuente

**Java I2P (i2pgit.org/I2P_Developers/i2p.i2p):** - `core/java/src/net/i2p/data/i2np/` - Implementaciones de mensajes I2NP - `core/java/src/net/i2p/crypto/` - Implementaciones criptográficas - `router/java/src/net/i2p/router/tunnel/` - Procesamiento de tunnel - `router/java/src/net/i2p/router/transport/` - Implementaciones de transporte

**Constantes y valores:** - `I2NPMessage.MAX_SIZE = 65536` - Tamaño máximo de un mensaje I2NP - `I2NPMessageImpl.HEADER_LENGTH = 16` - Tamaño de cabecera estándar - `TunnelDataMessage.DATA_LENGTH = 1024` - Carga útil de un mensaje de tunnel - `EncryptedBuildRecord.RECORD_SIZE = 528` - Registro de construcción largo - `ShortEncryptedBuildRecord.RECORD_SIZE = 218` - Registro de construcción corto - `TunnelBuildMessageBase.MAX_RECORD_COUNT = 8` - Máximo de registros por construcción

---

## Apéndice A: Estadísticas de la red y estado actual

### Composición de la red (a fecha de octubre de 2025)

- **Total de routers:** Aproximadamente 60,000-70,000 (varía)
- **Routers Floodfill:** Aproximadamente 500-700 activos
- **Tipos de cifrado:**
  - ECIES-X25519: >95% de los routers
  - ElGamal: <5% de los routers (en desuso, solo legado)
- **Adopción de transportes:**
  - SSU2: >60% como transporte principal
  - NTCP2: ~40% como transporte principal
  - Transportes heredados (SSU1, NTCP): 0% (eliminados)
- **Tipos de firma:**
  - EdDSA (Ed25519): Gran mayoría
  - ECDSA: Pequeño porcentaje
  - RSA: No permitido (eliminado)

### Requisitos mínimos del router

- **Versión de la API:** 0.9.16+ (para compatibilidad con la red de EdDSA)
- **Mínimo recomendado:** API 0.9.51+ (compilaciones de short tunnel ECIES)
- **Mínimo actual para floodfills:** API 0.9.58+ (obsolescencia del router ElGamal)
- **Próximo requisito:** Java 17+ (a partir de la versión 2.11.0, diciembre de 2025)

### Requisitos de ancho de banda

- **Mínimo:** 128 KBytes/sec (indicador N o superior) para floodfill
- **Recomendado:** 256 KBytes/sec (indicador O) o superior
- **Requisitos de floodfill:**
  - Ancho de banda mínimo de 128 KB/sec
  - Tiempo de actividad estable (>95% recomendado)
  - Baja latencia (<500ms hacia los pares)
  - Aprobar las pruebas de estado (tiempo de cola, retraso de tareas)

### Estadísticas de tunnel

- **Longitud típica del tunnel:** 3-4 saltos
- **Longitud máxima del tunnel:** 8 saltos (teórica, raramente utilizada)
- **Duración típica del tunnel:** 10 minutos
- **Tasa de éxito de construcción de tunnel:** >85% para routers bien conectados
- **Formato de mensaje de construcción de tunnel:**
  - Routers ECIES: ShortTunnelBuild (registros de 218 bytes)
  - Tunnels mixtos: VariableTunnelBuild (registros de 528 bytes)

### Métricas de rendimiento

- **Tiempo de construcción del tunnel:** 1-3 segundos (típico)
- **Latencia de extremo a extremo:** 0.5-2 segundos (típico, 6-8 saltos en total)
- **Rendimiento:** Limitado por el ancho de banda del tunnel (típicamente 10-50 KB/sec por tunnel)
- **Tamaño máximo del datagrama:** 10 KB recomendado (61.2 KB máximo teórico)

---

## Apéndice B: Características obsoletas y eliminadas

### Completamente eliminado (ya no tiene soporte)

- **Transporte NTCP** - Eliminado en la versión 0.9.50 (mayo de 2021)
- **Transporte SSU v1** - Eliminado de Java I2P en la versión 2.4.0 (diciembre de 2023)
- **Transporte SSU v1** - Eliminado de i2pd en la versión 2.44.0 (noviembre de 2022)
- **Tipos de firma RSA** - No permitidos a partir de la API 0.9.28

### Obsoleto (con soporte pero no recomendado)

- **ElGamal routers** - Obsoleto desde la API 0.9.58 (marzo de 2023)
  - Los destinos ElGamal se siguen admitiendo por compatibilidad con versiones anteriores
  - Los nuevos routers deberían usar exclusivamente ECIES-X25519
- **TunnelBuild (tipo 21)** - Obsoleto en favor de VariableTunnelBuild y ShortTunnelBuild
  - Sigue implementado para tunnels muy largos (>8 saltos)
- **TunnelBuildReply (tipo 22)** - Obsoleto en favor de VariableTunnelBuildReply y OutboundTunnelBuildReply
- **Cifrado ElGamal/AES** - Obsoleto en favor de ECIES-X25519-AEAD-Ratchet
  - Todavía se usa para destinos heredados
- **BuildRequestRecords ECIES largos (528 bytes)** - Obsoleto en favor del formato corto (218 bytes)
  - Todavía se usa para tunnels mixtos con saltos de ElGamal

### Cronograma de soporte heredado

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Feature</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Introduced</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Deprecated</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Removed</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">NTCP</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2003</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2018 (0.9.36)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2021 (0.9.50)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Replaced by NTCP2</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">SSU v1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2004</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2022 (0.9.54)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2023 (Java) / 2022 (i2pd)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Replaced by SSU2</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ElGamal routers</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2003</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2023 (0.9.58)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">TBD</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Destinations still supported</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">RSA signatures</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2015</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2017</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2017 (0.9.28)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Never widely used</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">TunnelBuild</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2004</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2009 (0.7.12)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Not removed</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Still supported for long tunnels</td>
    </tr>
  </tbody>
</table>
---

## Apéndice C: Desarrollos futuros

### Criptografía poscuántica

**Estado:** Beta desde la versión 2.10.0 (septiembre de 2025), será la predeterminada en la 2.11.0 (diciembre de 2025)

**Implementación:** - Enfoque híbrido que combina X25519 clásico y MLKEM poscuántico (ML-KEM-768) - Retrocompatible con la infraestructura ECIES-X25519 existente - Utiliza Signal Double Ratchet (protocolo de doble trinquete de Signal) con material de claves tanto clásico como PQ (poscuántico) - Consulte [Propuesta 169](/proposals/169-pq-crypto/) para más detalles

**Ruta de migración:** 1. Versión 2.10.0 (septiembre de 2025): Disponible como opción beta 2. Versión 2.11.0 (diciembre de 2025): Habilitado por defecto 3. Versiones futuras: Con el tiempo será obligatorio

### Características previstas

- **Mejoras en IPv6** - Mejor soporte de IPv6 y mecanismos de transición
- **Limitación por tunnel** - Control de ancho de banda granular por tunnel
- **Métricas mejoradas** - Mejor monitorización del rendimiento y diagnósticos
- **Optimizaciones de protocolo** - Menor sobrecarga y mayor eficiencia
- **Mejor selección de floodfill (nodos especializados que mantienen y distribuyen la netDb)** - Mejor distribución de la base de datos de red

### Áreas de investigación

- **Optimización de la longitud de tunnel** - Longitud de tunnel dinámica basada en el modelo de amenazas
- **Relleno avanzado** - Mejoras en la resistencia al análisis de tráfico
- **Nuevos esquemas de cifrado** - Preparación frente a amenazas de la computación cuántica
- **Control de congestión** - Mejor gestión de la carga de la red
- **Soporte móvil** - Optimizaciones para dispositivos y redes móviles

---

## Apéndice D: Directrices de implementación

### Para nuevas implementaciones

**Requisitos mínimos:** 1. Admitir las funciones de la API versión 0.9.51+ 2. Implementar cifrado ECIES-X25519-AEAD-Ratchet 3. Admitir los transportes NTCP2 y SSU2 4. Implementar mensajes ShortTunnelBuild (registros de 218 bytes) 5. Admitir variantes LeaseSet2 (tipos 3, 5, 7) 6. Usar firmas EdDSA (Ed25519)

**Recomendado:** 1. Admitir criptografía híbrida poscuántica (a partir de la versión 2.11.0) 2. Implementar parámetros de ancho de banda por tunnel 3. Admitir los formatos Datagram2 y Datagram3 4. Implementar opciones de registro de servicio en LeaseSets 5. Seguir las especificaciones oficiales en /docs/specs/

**No requerido:** 1. Soporte de router ElGamal (obsoleto) 2. Soporte de transportes heredados (SSU1, NTCP) 3. BuildRequestRecords de ECIES largos (528 bytes para tunnels ECIES puros) 4. Mensajes TunnelBuild/TunnelBuildReply (utilice las variantes Variable o Short)

### Pruebas y validación

**Cumplimiento del protocolo:** 1. Probar la interoperabilidad con el router oficial de I2P en Java 2. Probar la interoperabilidad con el router i2pd en C++ 3. Validar los formatos de mensaje conforme a las especificaciones 4. Probar los ciclos de construcción/desmontaje de tunnel 5. Verificar el cifrado/descifrado con vectores de prueba

**Pruebas de rendimiento:** 1. Medir las tasas de éxito al construir tunnel (deberían ser >85%) 2. Probar con diversas longitudes de tunnel (2-8 saltos) 3. Validar la fragmentación y el reensamblado 4. Probar bajo carga (múltiples tunnels simultáneos) 5. Medir la latencia de extremo a extremo

**Pruebas de seguridad:** 1. Verificar la implementación de cifrado (usar vectores de prueba) 2. Probar la prevención de ataques de repetición 3. Validar el manejo de la expiración de mensajes 4. Probar contra mensajes malformados 5. Verificar la generación adecuada de números aleatorios

### Escollos comunes de implementación

1. **Formatos de instrucciones de entrega confusos** - Garlic clove (submensaje de garlic) vs mensaje de tunnel
2. **Derivación de claves incorrecta** - Uso de HKDF para registros de construcción cortos
3. **Gestión del ID de mensaje** - No se establece correctamente para construcciones de tunnel
4. **Problemas de fragmentación** - No se respeta el límite práctico de 61.2 KB
5. **Errores de Endianness (orden de bytes)** - Java usa big-endian para todos los enteros
6. **Gestión de expiración** - El formato corto se desborda el 7 de febrero de 2106
7. **Generación de suma de verificación** - Sigue siendo obligatoria incluso si no se verifica
