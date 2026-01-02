---
title: "I2PTunnel"
description: "Herramienta para interactuar con I2P y proporcionar servicios en la red"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

## Resumen

I2PTunnel es un componente central de I2P para interactuar con la red I2P y proporcionar servicios en ella. Permite que aplicaciones basadas en TCP y de transmisión de medios operen de forma anónima mediante abstracción de túneles. El destino de un túnel puede definirse por un [nombre de host](/docs/overview/naming), [Base32](/docs/overview/naming#base32), o una clave de destino completa.

Cada tunnel establecido escucha localmente (por ejemplo, `localhost:port`) y se conecta internamente a destinos I2P. Para alojar un servicio, crea un tunnel que apunte a la IP y puerto deseados. Se genera una clave de destino I2P correspondiente, lo que permite que el servicio sea accesible globalmente dentro de la red I2P. La interfaz web de I2PTunnel está disponible en [I2P Router Tunnel Manager](http://localhost:7657/i2ptunnel/).

---

## Servicios Predeterminados

### Túnel de servidor

- **I2P Webserver** – Un tunnel a un servidor web Jetty en [localhost:7658](http://localhost:7658) para alojar fácilmente en I2P.  
  - **Unix:** `$HOME/.i2p/eepsite/docroot`  
  - **Windows:** `%LOCALAPPDATA%\I2P\I2P Site\docroot` → `C:\Users\<username>\AppData\Local\I2P\I2P Site\docroot`

### Túneles de cliente

- **I2P HTTP Proxy** – `localhost:4444` – Utilizado para navegar por I2P e Internet a través de outproxies.  
- **I2P HTTPS Proxy** – `localhost:4445` – Variante segura del HTTP proxy.  
- **Irc2P** – `localhost:6668` – Túnel predeterminado de red IRC anónima.  
- **Git SSH (gitssh.idk.i2p)** – `localhost:7670` – Túnel cliente para acceso SSH a repositorios.  
- **Postman SMTP** – `localhost:7659` – Túnel cliente para correo saliente.  
- **Postman POP3** – `localhost:7660` – Túnel cliente para correo entrante.

> Nota: Solo el servidor web I2P es un **túnel de servidor** predeterminado; todos los demás son túneles de cliente que se conectan a servicios I2P externos.

---

## Configuración

La especificación de configuración de I2PTunnel está documentada en [/spec/configuration](/docs/specs/configuration/).

---

## Modos de Cliente

### Estándar

Abre un puerto TCP local que se conecta a un servicio en un destino I2P. Admite múltiples entradas de destino separadas por comas para redundancia.

### HTTP

Un túnel proxy para solicitudes HTTP/HTTPS. Soporta outproxies locales y remotos, eliminación de encabezados, almacenamiento en caché, autenticación y compresión transparente.

**Protecciones de privacidad:**   - Elimina encabezados: `Accept-*`, `Referer`, `Via`, `From`   - Reemplaza encabezados de host con destinos Base32   - Aplica eliminación hop-by-hop conforme a RFC   - Añade soporte para descompresión transparente   - Proporciona páginas de error internas y respuestas localizadas

**Comportamiento de compresión:**   - Las solicitudes pueden usar el encabezado personalizado `X-Accept-Encoding: x-i2p-gzip`   - Las respuestas con `Content-Encoding: x-i2p-gzip` se descomprimen de forma transparente   - La compresión se evalúa según el tipo MIME y la longitud de la respuesta para mayor eficiencia

**Persistencia (nuevo desde 2.5.0):**   HTTP Keepalive y las conexiones persistentes ahora son compatibles con servicios alojados en I2P a través del Administrador de Servicios Ocultos. Esto reduce la latencia y la sobrecarga de conexión, pero aún no habilita sockets persistentes totalmente compatibles con RFC 2616 en todos los saltos.

**Pipelining:**   Sigue sin estar soportado y es innecesario; los navegadores modernos lo han dejado obsoleto.

**Comportamiento del User-Agent:**   - **Outproxy:** Utiliza un User-Agent actual de Firefox ESR.   - **Interno:** `MYOB/6.66 (AN/ON)` para consistencia de anonimato.

### Cliente IRC

Se conecta a servidores IRC basados en I2P. Permite un subconjunto seguro de comandos mientras filtra identificadores para proteger la privacidad.

### SOCKS 4/4a/5

Proporciona capacidad de proxy SOCKS para conexiones TCP. UDP permanece sin implementar en Java I2P (solo en i2pd).

### CONNECT

Implementa túneles HTTP `CONNECT` para conexiones SSL/TLS.

### Streamr

Habilita la transmisión de estilo UDP a través de encapsulación basada en TCP. Soporta transmisión de medios cuando se combina con un túnel de servidor Streamr correspondiente.

![Diagrama de I2PTunnel Streamr](/images/I2PTunnel-streamr.png)

---

## Modos de Servidor

### Servidor Estándar

Crea un destino TCP mapeado a una IP:puerto local.

### Servidor HTTP

Crea un destino que interactúa con un servidor web local. Soporta compresión (`x-i2p-gzip`), eliminación de encabezados y protecciones contra DDoS. Ahora se beneficia del **soporte de conexiones persistentes** (v2.5.0+) y **optimización de pool de hilos** (v2.7.0–2.9.0).

### HTTP Bidireccional

**Obsoleto** – Sigue siendo funcional pero desaconsejado. Actúa como servidor y cliente HTTP sin outproxying (proxy de salida). Se utiliza principalmente para pruebas de diagnóstico de loopback.

### Servidor IRC

Crea un destino filtrado para servicios IRC, pasando las claves de destino del cliente como nombres de host.

### Servidor Streamr

Se acopla con un túnel cliente Streamr para manejar flujos de datos estilo UDP sobre I2P.

---

## Nuevas Funcionalidades (2.4.0–2.10.0)

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Feature</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Introduced</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Summary</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Keepalive/Persistent Connections</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.5.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">HTTP tunnels now support persistent sockets for I2P-hosted services, improving performance.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Thread Pooling Optimization</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.7.0-2.9.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reduced CPU overhead and latency by improving thread management.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Post-Quantum Encryption (ML-KEM)</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.10.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Optional hybrid X25519+ML-KEM encryption to resist future quantum attacks.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>NetDB Segmentation</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.4.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Isolates I2PTunnel contexts for improved security and privacy.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>SSU1 Removal / SSU2 Adoption</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.4.0-2.6.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Upgraded transport layer; transparent to users.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>I2P-over-Tor Blocking</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.6.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Prevents inefficient and unstable I2P-over-Tor routing.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Browser Proxy (Proposal 166)</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.7.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Introduced identity-aware proxy mode; details pending confirmation.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Java 17 Requirement (upcoming)</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.11.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Future release will require Java 17+.</td>
    </tr>
  </tbody>
</table>
---

## Características de Seguridad

- **Eliminación de encabezados** para anonimato (Accept, Referer, From, Via)
- **Aleatorización de User-Agent** según in/outproxy
- **Limitación de tasa de POST** y **protección contra Slowloris**
- **Limitación de conexiones** en subsistemas de streaming
- **Manejo de congestión de red** en la capa de tunnel
- **Aislamiento de NetDB** previniendo filtraciones entre aplicaciones

---

## Detalles Técnicos

- Tamaño de clave de destino predeterminado: 516 bytes (puede exceder para certificados LS2 extendidos)  
- Direcciones Base32: `{52–56+ chars}.b32.i2p`  
- Los túneles de servidor permanecen compatibles tanto con Java I2P como con i2pd  
- Característica obsoleta: solo `httpbidirserver`; sin eliminaciones desde 0.9.59  
- Verificados los puertos predeterminados correctos y directorios raíz de documentos para todas las plataformas

---

## Resumen

I2PTunnel sigue siendo la columna vertebral de la integración de aplicaciones con I2P. Entre las versiones 0.9.59 y 2.10.0, obtuvo soporte para conexiones persistentes, cifrado post-cuántico y mejoras importantes en el manejo de hilos. La mayoría de las configuraciones permanecen compatibles, pero los desarrolladores deben verificar sus configuraciones para garantizar el cumplimiento con los valores predeterminados modernos de transporte y seguridad.
