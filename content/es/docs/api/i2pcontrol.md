---
title: "I2PControl JSON-RPC"
description: "API de gestión remota de router a través de la aplicación web I2PControl"
slug: "i2pcontrol"
lastUpdated: "2026-07-10"
accurateFor: "2.12.0"
reviewStatus: "needs-review"
---

# Documentación de la API I2PControl

-------------revisar agregar cosas--------------

I2PControl es una API **JSON-RPC 2.0** incluida con el router I2P (desde la versión 0.9.39). Permite el monitoreo y control autenticado del router a través de solicitudes JSON estructuradas.

> **Contraseña por defecto:** `itoopie` — esta es la configuración de fábrica y **debe cambiarse** inmediatamente por seguridad.

## 1. Descripción general y acceso

| Implementación             | Punto final predeterminado                 | Protocolo | Habilitado por defecto                             | Notas                  |
|----------------------------|--------------------------------------------|-----------|----------------------------------------------------|------------------------|
| Java I2P (2.10.0+)         | `http://127.0.0.1:7657/jsonrpc/`           | HTTP      | ❌ Debe habilitarse mediante WebApps (Consola del router) | Aplicación web incluida |
| i2pd (implementación en C++) | `https://127.0.0.1:7650/`                | HTTPS     | ✅ Habilitado por defecto                           | Comportamiento de plugin heredado |
---

En el caso de Java I2P, debes ir a **Router Console → WebApps → I2PControl** y habilitarlo (configurar para que se inicie automáticamente). Una vez activo, todos los métodos requieren que primero te autentiques y recibas un token de sesión.

## 2. Formato JSON-RPC

---

```json
{
  "jsonrpc": "2.0",
  "id": "1",
  "method": "MethodName",
  "params": {
    /* named parameters */
  }
}
```
Todas las solicitudes siguen la estructura JSON-RPC 2.0:

```json
{
  "jsonrpc": "2.0",
  "id": "1",
  "result": { /* data */ }
}
```
Una respuesta exitosa incluye un campo `result`; en caso de fallo, se devuelve un objeto `error`:

```json
{
  "jsonrpc": "2.0",
  "id": "1",
  "error": {
    "code": -32001,
    "message": "Invalid password"
  }
}
```
o

## 3. Flujo de Autenticación

### Solicitud (Autenticar)

```bash
curl -s -H "Content-Type: application/json" \
  -d '{
        "jsonrpc": "2.0",
        "id": "1",
        "method": "Authenticate",
        "params": {
          "API": 1,
          "Password": "itoopie"
        }
      }' \
  http://127.0.0.1:7657/jsonrpc/
```
### Respuesta Exitosa

```json
{
  "jsonrpc": "2.0",
  "id": "1",
  "result": {
    "Token": "a1b2c3d4e5",
    "API": 1
  }
}
```
| Campo      | Dirección | Tipo   | Descripción                                              |
|------------|-----------|--------|----------------------------------------------------------|
| `API`      | Solicitud | long   | Versión de la API I2PControl solicitada por el cliente. Usar `1`. |
| `Password` | Solicitud | String | Contraseña usada para autenticarse con I2PControl.           |
| `API`      | Respuesta  | long   | Versión principal de la API implementada por el servidor.           |
| `Token`    | Respuesta  | String | Token de autenticación usado en solicitudes posteriores.       |
---

Debes incluir ese `Token` en todas las solicitudes posteriores en los `params`.

## 4. Métodos y Endpoints

### 4.1 RouterInfo

---

Obtiene telemetría clave sobre el router.

```bash
curl -s -H "Content-Type: application/json" \
  -d '{
        "jsonrpc": "2.0",
        "id": "2",
        "method": "RouterInfo",
        "params": {
          "Token": "a1b2c3d4e5",
          "i2p.router.version": "",
          "i2p.router.status": "",
          "i2p.router.net.status": "",
          "i2p.router.net.tunnels.participating": "",
          "i2p.router.net.bw.inbound.1s": "",
          "i2p.router.net.bw.outbound.1s": ""
        }
      }' \
  http://127.0.0.1:7657/jsonrpc/
```
**Ejemplo de Solicitud**

#### Enumeración de Códigos de Estado (`i2p.router.net.status`)

| Clave                                    | Tipo   | Descripción                                                             |
|----------------------------------------|--------|-------------------------------------------------------------------------|
| `i2p.router.status`                    | String | Estado del router en formato libre y traducido, destinado a visualización.             |
| `i2p.router.uptime`                    | long   | Tiempo activo del router en milisegundos. Versiones antiguas de i2pd podrían devolver una cadena. |
| `i2p.router.version`                   | String | Versión completa del router.                                                    |
| `i2p.router.net.status`                | long   | Código de estado de red; ver la tabla a continuación.                               |
| `i2p.router.net.bw.inbound.1s`         | double | Ancho de banda entrante actual en bytes por segundo.                          |
| `i2p.router.net.bw.inbound.15s`        | double | Promedio de ancho de banda entrante en los últimos 15 segundos, en bytes por segundo.                |
| `i2p.router.net.bw.outbound.1s`        | double | Ancho de banda saliente actual en bytes por segundo.                         |
| `i2p.router.net.bw.outbound.15s`       | double | Promedio de ancho de banda saliente en los últimos 15 segundos, en bytes por segundo.               |
| `i2p.router.net.tunnels.participating` | long   | Número de túneles en los que este router está participando.                |
#### Enumeración de Códigos de Estado (`i2p.router.net.status`)

| Código | Significado                                          |
|--------|------------------------------------------------------|
| 0      | OK                                                   |
| 1      | PRUEBAS                                              |
| 2      | DETRÁS DE CORTAFUEGOS                               |
| 3      | OCULTO                                               |
| 4      | ADVERTENCIA_DET_CORTAFUEGOS_Y_RÁPIDO                |
| 5      | ADVERTENCIA_DET_CORTAFUEGOS_Y_RELLENO               |
| 6      | ADVERTENCIA_DET_CORTAFUEGOS_CON_TCP_ENTRANTE         |
| 7      | ADVERTENCIA_DET_CORTAFUEGOS_CON_UDP_DESACTIVADO      |
| 8      | ERROR_I2CP                                           |
| 9      | ERROR_DESVIO_RELOJ                                   |
| 10     | ERROR_DIRECCION_TCP_PRIVADA                          |
| 11     | ERROR_NAT_SIMETRICO                                  |
| 12     | ERROR_PUERTO_UDP_EN_USO                              |
| 13     | ERROR_SIN_PARES_ACTIVOS_VERIFIQUE_CONEXION_Y_CORTAFUEGOS |
| 14     | ERROR_UDP_DESACTIVADO_Y_TCP_NO_CONFIGURADO           |
#### NetDB y campos de pares

| Clave                                  | Tipo    | Descripción                                        |
|----------------------------------------|---------|----------------------------------------------------|
| `i2p.router.netdb.knownpeers`          | long    | Número de pares conocidos, excluyendo el router local. |
| `i2p.router.netdb.activepeers`         | long    | Número de pares activos.                           |
| `i2p.router.netdb.fastpeers`           | long    | Número de pares clasificados como rápidos.         |
| `i2p.router.netdb.highcapacitypeers`   | long    | Número de pares clasificados como alta capacidad.  |
| `i2p.router.netdb.isreseeding`         | boolean | Indica si se está realizando un reseed.            |
**Campos de Respuesta (result)** Según la documentación oficial (GetI2P): - `i2p.router.status` (String) — un estado legible por humanos - `i2p.router.uptime` (long) — milisegundos (o string para i2pd más antiguo) :contentReference[oaicite:0]{index=0} - `i2p.router.version` (String) — cadena de versión :contentReference[oaicite:1]{index=1} - `i2p.router.net.bw.inbound.1s`, `i2p.router.net.bw.inbound.15s` (double) — ancho de banda entrante en B/s :contentReference[oaicite:2]{index=2} - `i2p.router.net.bw.outbound.1s`, `i2p.router.net.bw.outbound.15s` (double) — ancho de banda saliente en B/s :contentReference[oaicite:3]{index=3} - `i2p.router.net.status` (long) — código de estado numérico (ver enumeración a continuación) :contentReference[oaicite:4]{index=4} - `i2p.router.net.tunnels.participating` (long) — número de tunnels participantes :contentReference[oaicite:5]{index=5} - `i2p.router.netdb.activepeers`, `fastpeers`, `highcapacitypeers` (long) — estadísticas de peers del netDB :contentReference[oaicite:6]{index=6} - `i2p.router.netdb.isreseeding` (boolean) — si el reseed está activo :contentReference[oaicite:7]{index=7} - `i2p.router.netdb.knownpeers` (long) — total de peers conocidos :contentReference[oaicite:8]{index=8}

### 4.2 GetRate

---

| Parámetro | Tipo   | Descripción                     |
|-----------|--------|---------------------------------|
| `Stat`    | String | Nombre del RateStat del router. |
| `Period`  | long   | Periodo de tasa en milisegundos.|
Se utiliza para obtener métricas de velocidad (por ejemplo, ancho de banda, éxito de tunnel) durante una ventana de tiempo determinada.

```bash
curl -s -H "Content-Type: application/json" \
  -d '{
        "jsonrpc": "2.0",
        "id": "3",
        "method": "GetRate",
        "params": {
          "Token": "a1b2c3d4e5",
          "Stat": "bw.combined",
          "Period": 60000
        }
      }' \
  http://127.0.0.1:7657/jsonrpc/
```
**Ejemplo de Solicitud**

```json
{
  "jsonrpc": "2.0",
  "id": "3",
  "result": {
    "Result": 12345.67
  }
}
```
**Respuesta de Ejemplo**

### 4.3 RouterManager

---

| Parámetro            | Resultado           | Descripción                                                             |
|----------------------|---------------------|-------------------------------------------------------------------------|
| `Restart`            | null                | Inicia un reinicio inmediato del router.                                |
| `RestartGraceful`    | null                | Reinicia después de que expiren los túneles en los que participa.        |
| `Shutdown`           | null                | Inicia un apagado inmediato del router.                                 |
| `ShutdownGraceful`   | null                | Se apaga después de que expiren los túneles en los que participa.        |
| `Reseed`             | null                | Comienza un reseed del router.                                          |
| `FindUpdates`        | boolean o String    | Bloqueante. Busca una actualización firmada del router.                 |
| `Update`             | String              | Bloqueante. Inicia una actualización firmada del router y devuelve su estado final. |
Realizar acciones administrativas.

```bash
curl -s -H "Content-Type: application/json" \
  -d '{
        "jsonrpc": "2.0",
        "id": "4",
        "method": "RouterManager",
        "params": {
          "Token": "a1b2c3d4e5",
          "Restart": true
        }
      }' \
  http://127.0.0.1:7657/jsonrpc/
```
**Parámetros / métodos permitidos**   - `Restart`, `RestartGraceful`   - `Shutdown`, `ShutdownGraceful`   - `Reseed`, `FindUpdates`, `Update` :contentReference[oaicite:10]{index=10}

```json
{
  "jsonrpc": "2.0",
  "id": "4",
  "result": {
    "Restart": null
  }
}
```
**Ejemplo de Solicitud**

### 4.4 NetworkSetting

**Respuesta Exitosa**

---

| Clave                             | Valor aceptado                                      | Descripción                                                  |
|---------------------------------|-----------------------------------------------------|--------------------------------------------------------------|
| `i2p.router.net.ntcp.port`      | Cadena, 1–65535                                     | Puerto NTCP; un cambio requiere reinicio.                    |
| `i2p.router.net.ntcp.hostname`  | Cadena                                              | Nombre de host NTCP; un cambio requiere reinicio.            |
| `i2p.router.net.ntcp.autoip`    | `always`, `true` o `false`                          | Selección automática de dirección NTCP.                      |
| `i2p.router.net.ssu.port`       | Cadena, 1–65535                                     | Puerto SSU; un cambio requiere reinicio.                     |
| `i2p.router.net.ssu.hostname`   | Cadena                                              | Nombre de host externo SSU; un cambio requiere reinicio.     |
| `i2p.router.net.ssu.autoip`     | `ssu`, `local,ssu`, `upnp,ssu` o `local,upnp,ssu` | Fuentes de detección de dirección SSU.                       |
| `i2p.router.net.ssu.detectedip` | null                                                | Dirección SSU detectada de solo lectura.                    |
| `i2p.router.net.upnp`           | Cadena                                              | Configuración UPnP.                                          |
| `i2p.router.net.bw.share`       | Cadena, 0–100                                       | Porcentaje de ancho de banda disponible para túneles participantes. |
| `i2p.router.net.bw.in`          | Cadena de entero no negativo                        | Límite de ancho de banda entrante en KiB/s.                  |
| `i2p.router.net.bw.out`         | Cadena de entero no negativo                        | Límite de ancho de banda saliente en KiB/s.                  |
| `i2p.router.net.laptopmode`     | Cadena                                              | Configuración de modo portátil.                              |
Obtener o establecer parámetros de configuración de red (puertos, upnp, ancho de banda compartido, etc.)

```bash
curl -s -H "Content-Type: application/json" \
  -d '{
        "jsonrpc": "2.0",
        "id": "5",
        "method": "NetworkSetting",
        "params": {
          "Token": "a1b2c3d4e5",
          "i2p.router.net.ntcp.port": null,
          "i2p.router.net.ssu.port": null,
          "i2p.router.net.bw.share": null,
          "i2p.router.net.upnp": null
        }
      }' \
  http://127.0.0.1:7657/jsonrpc/
```
**Ejemplo de Solicitud (obtener valores actuales)**

```json
{
  "jsonrpc": "2.0",
  "id": "5",
  "result": {
    "i2p.router.net.ntcp.port": "1234",
    "i2p.router.net.ssu.port": "5678",
    "i2p.router.net.bw.share": "50",
    "i2p.router.net.upnp": "true",
    "SettingsSaved": false,
    "RestartNeeded": false
  }
}
```
**Respuesta de Ejemplo**

> Nota: las versiones de i2pd anteriores a la 2.41 pueden devolver tipos numéricos en lugar de cadenas — los clientes deben manejar ambos. :contentReference[oaicite:11]{index=11}

### 4.5 Configuración Avanzada

---

| Parámetro | Tipo                | Descripción                                                           |
|-----------|---------------------|-----------------------------------------------------------------------|
| `get`     | Cadena              | Devuelve una configuración dentro de un objeto resultado `get`.     |
| `getAll`  | n/a                 | Devuelve el mapa completo de configuración dentro de `getAll`.       |
| `set`     | Mapa<Cadena, Cadena> | Actualiza las configuraciones proporcionadas sin eliminar otras claves. |
| `setAll`  | Mapa<Cadena, Cadena> | **Destructivo:** reemplaza todas las configuraciones y elimina las claves no proporcionadas. |
Permite manipular parámetros internos del router.

**Ejemplo de Solicitud**

```bash
curl -s -H "Content-Type: application/json" \
  -d '{
        "jsonrpc": "2.0",
        "id": "6",
        "method": "AdvancedSettings",
        "params": {
          "Token": "a1b2c3d4e5",
          "set": {
            "router.sharePercentage": "75",
            "i2np.flushInterval": "6000"
          }
        }
      }' \
  http://127.0.0.1:7657/jsonrpc/
```
**Ejemplo de Respuesta**

```json
{
  "jsonrpc": "2.0",
  "id": "6",
  "result": {}
}
```
---

### Códigos de Error Estándar JSON-RPC2

---

| Parámetro | Tipo   | Descripción                 |
|-----------|--------|-----------------------------|
| `Echo`    | String | Valor devuelto como `Result`. |
```json
{
  "jsonrpc": "2.0",
  "id": "7",
  "method": "Echo",
  "params": {
    "Token": "a1b2c3d4e5",
    "Echo": "hello"
  }
}
```
```json
{
  "jsonrpc": "2.0",
  "id": "7",
  "result": {
    "Result": "hello"
  }
}
```
---

### Códigos de Error Específicos de I2PControl

Gestiona I2PControl mismo. El controlador Java actual soporta cambios de contraseña.

| Parámetro               | Tipo   | Descripción                                                                |
|-------------------------|--------|----------------------------------------------------------------------------|
| `i2pcontrol.password`   | String | Establece una nueva contraseña de I2PControl y revoca los tokens de autenticación existentes. |
El resultado contiene `SettingsSaved`. Si la contraseña fue cambiada, el resultado también contiene `"i2pcontrol.password": null`. La configuración de dirección y puerto de escucha del plugin independiente heredado no está activa en el controlador Java actual.

> **Contraseña por defecto:** `itoopie` — esta es la configuración de fábrica y **debe cambiarse** inmediatamente por seguridad.

## 5. Códigos de Error

### Códigos de error estándar JSON-RPC2

| Código   | Significado           |
|----------|-----------------------|
| -32700   | Error de análisis JSON |
| -32600   | Solicitud inválida     |
| -32601   | Método no encontrado   |
| -32602   | Parámetros inválidos   |
| -32603   | Error interno          |
### Códigos de error específicos de I2PControl

| Código   | Significado                                                                                  |
|----------|----------------------------------------------------------------------------------------------|
| -32001   | Contraseña inválida proporcionada                                                            |
| -32002   | No se presentó ningún token de autenticación                                                  |
| -32003   | El token de autenticación no existe                                                           |
| -32004   | El token de autenticación proporcionado ha expirado y será eliminado                         |
| -32005   | La versión de la API I2PControl utilizada no fue especificada, pero es obligatoria especificarla |
| -32006   | La versión de la API I2PControl especificada no es compatible con I2PControl                  |
> **Contraseña por defecto:** `itoopie` — esta es la configuración de fábrica y **debe cambiarse** inmediatamente por seguridad.

## 6. Uso y mejores prácticas

- Incluye siempre el parámetro `Token` (excepto al autenticarse).  
- Cambia la contraseña predeterminada (`itoopie`) en el primer uso.  
- Para Java I2P, asegúrate de que la webapp I2PControl esté habilitada a través de WebApps.  
- Prepárate para ligeras variaciones: algunos campos pueden ser números o cadenas, dependiendo de la versión de I2P.  
- Envuelve las cadenas de estado largas para obtener una salida amigable para la visualización.

> **Contraseña por defecto:** `itoopie` — esta es la configuración de fábrica y **debe cambiarse** inmediatamente por seguridad.
