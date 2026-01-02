---
title: "IRC sobre I2P"
description: "Guía completa de redes IRC de I2P, clientes, túneles y configuración de servidores (actualizada 2025)"
slug: "irc"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

## Descripción general

**Puntos clave**

- I2P proporciona **cifrado de extremo a extremo** para el tráfico IRC a través de sus túneles. **Desactiva SSL/TLS** en los clientes IRC a menos que estés usando un outproxy hacia clearnet.
- El túnel de cliente **Irc2P** preconfigurado escucha en **127.0.0.1:6668** por defecto. Conecta tu cliente IRC a esa dirección y puerto.
- No uses el término "TLS proporcionado por el router". Usa "cifrado nativo de I2P" o "cifrado de extremo a extremo".

## Inicio rápido (Java I2P)

1. Abre el **Administrador de Servicios Ocultos** en `http://127.0.0.1:7657/i2ptunnel/` y asegúrate de que el túnel **Irc2P** esté **ejecutándose**.
2. En tu cliente IRC, configura **servidor** = `127.0.0.1`, **puerto** = `6668`, **SSL/TLS** = **desactivado**.
3. Conéctate y únete a canales como `#i2p`, `#i2p-dev`, `#i2p-help`.

Para usuarios de **i2pd** (router en C++), crea un túnel cliente en `tunnels.conf` (ver ejemplos a continuación).

## Redes y servidores

### IRC2P (main community network)

- Servidores federados: `irc.postman.i2p:6667`, `irc.echelon.i2p:6667`, `irc.dg.i2p:6667`.
- El túnel **Irc2P** en `127.0.0.1:6668` se conecta a uno de estos automáticamente.
- Canales típicos: `#i2p`, `#i2p-chat`, `#i2p-dev`, `#i2p-help`.

### Ilita network

- Servidores: `irc.ilita.i2p:6667`, `irc.r4sas.i2p:6667`, `irc.acetone.i2p:6667`, `rusirc.ilita.i2p:6667`.
- Idiomas principales: ruso e inglés. Algunos hosts disponen de interfaces web.

## Client setup

### Recommended, actively maintained

- **WeeChat (terminal)** — soporte SOCKS robusto; fácil de programar mediante scripts.
- **Pidgin (escritorio)** — todavía mantenido; funciona bien en Windows/Linux.
- **Thunderbird Chat (escritorio)** — compatible con ESR 128+.
- **The Lounge (web autoalojado)** — cliente web moderno.

### IRC2P (red comunitaria principal)

- **LimeChat** (gratis, código abierto).
- **Textual** (de pago en App Store; código fuente disponible para compilar).

### Red Ilita

#### WeeChat via SOCKS5

```
/proxy add i2p socks5 127.0.0.1 4447
/set irc.server.i2p.addresses "127.0.0.1/6668"
/set irc.server.i2p.proxy "i2p"
/connect i2p
```
#### Pidgin

- Protocolo: **IRC**
- Servidor: **127.0.0.1**
- Puerto: **6668**
- Cifrado: **desactivado**
- Nombre de usuario/nick: cualquiera

#### Thunderbird Chat

- Tipo de cuenta: **IRC**
- Servidor: **127.0.0.1**
- Puerto: **6668**
- SSL/TLS: **desactivado**
- Opcional: unirse automáticamente a canales al conectar

#### Dispatch (SAM v3)

Ejemplo de valores predeterminados de `config.toml`:

```
[defaults]
name = "Irc2P"
host = "irc.postman.i2p"
port = 6667
channels = ["#i2p","#i2p-dev"]
ssl = false
```
## Tunnel configuration

### Java I2P defaults

- Túnel de cliente Irc2P: **127.0.0.1:6668** → servidor upstream en el **puerto 6667**.
- Administrador de Servicios Ocultos: `http://127.0.0.1:7657/i2ptunnel/`.

### Recomendado, mantenido activamente

`~/.i2pd/tunnels.conf`:

```
[IRC-IRC2P]
type = client
address = 127.0.0.1
port = 6668
destination = irc.postman.i2p
destinationport = 6667
keys = irc-keys.dat
```
Túnel separado para Ilita (ejemplo):

```
[IRC-ILITA]
type = client
address = 127.0.0.1
port = 6669
destination = irc.ilita.i2p
destinationport = 6667
keys = irc-ilita-keys.dat
```
### Opciones de macOS

- **Habilitar SAM** en Java I2P (desactivado por defecto) en `/configclients` o `clients.config`.
- Valores predeterminados: **127.0.0.1:7656/TCP** y **127.0.0.1:7655/UDP**.
- Criptografía recomendada: `SIGNATURE_TYPE=7` (Ed25519) y `i2cp.leaseSetEncType=4,0` (ECIES‑X25519 con respaldo ElGamal) o simplemente `4` para solo modernos.

### Configuraciones de ejemplo

- Java I2P predeterminado: **2 entrantes / 2 salientes**.
- i2pd predeterminado: **5 entrantes / 5 salientes**.
- Para IRC: **2–3 cada uno** es suficiente; configúrelo explícitamente para un comportamiento consistente entre routers.

## Configuración del cliente

- **No habilite SSL/TLS** para conexiones IRC internas de I2P. I2P ya proporciona cifrado de extremo a extremo. TLS adicional añade sobrecarga sin ganancias en anonimato.
- Use **claves persistentes** para identidad estable; evite regenerar claves en cada reinicio a menos que esté probando.
- Si múltiples aplicaciones usan IRC, prefiera **túneles separados** (no compartidos) para reducir la correlación entre servicios.
- Si debe permitir control remoto (SAM/I2CP), vincule a localhost y asegure el acceso con túneles SSH o proxies inversos autenticados.

## Alternative connection method: SOCKS5

Algunos clientes pueden conectarse a través del proxy SOCKS5 de I2P: **127.0.0.1:4447**. Para obtener mejores resultados, es preferible usar un túnel de cliente IRC dedicado en el puerto 6668; SOCKS no puede sanear identificadores de capa de aplicación y puede filtrar información si el cliente no está diseñado para anonimato.

## Troubleshooting

- **No se puede conectar** — asegúrate de que el túnel Irc2P esté ejecutándose y el router esté completamente bootstrapped.
- **Se cuelga en resolve/join** — verifica que SSL esté **deshabilitado** y el cliente apunte a **127.0.0.1:6668**.
- **Latencia alta** — I2P tiene latencia más alta por diseño. Mantén las cantidades de túneles moderadas (2–3) y evita bucles de reconexión rápida.
- **Uso de aplicaciones SAM** — confirma que SAM esté habilitado (Java) o no bloqueado por firewall (i2pd). Se recomiendan sesiones de larga duración.

## Appendix: Ports and naming

- Puertos de túnel IRC comunes: **6668** (predeterminado de Irc2P), **6667** y **6669** como alternativas.
- Nombres de host `.b32.i2p`: formato estándar de 52 caracteres; existen formatos extendidos de 56+ caracteres para LS2/certificados avanzados. Utiliza nombres de host `.i2p` a menos que necesites explícitamente direcciones b32.
