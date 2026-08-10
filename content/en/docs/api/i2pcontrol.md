---
title: "I2PControl JSON-RPC"
description: "Remote router management API via the I2PControl webapp"
slug: "i2pcontrol"
lastUpdated: "2026-07-10"
accurateFor: "2.12.0"
reviewStatus: "needs-review"
---
# I2PControl API Documentation

I2PControl is a **JSON-RPC 2.0** API bundled with the I2P router (since version 0.9.39). It enables authenticated monitoring and control of the router via structured JSON requests.

> **Default password:** `itoopie` — this is the factory default and **should be changed** immediately for security.

---

## 1. Overview & Access

| Implementation             | Default Endpoint                 | Protocol | Enabled by Default                             | Notes                  |
|----------------------------|----------------------------------|----------|------------------------------------------------|------------------------|
| Java I2P (2.10.0+)         | `http://127.0.0.1:7657/jsonrpc/` | HTTP     | ❌ Must be enabled via WebApps (Router Console) | Bundled webapp         |
| i2pd (C++ implementation)  | `https://127.0.0.1:7650/`        | HTTPS    | ✅ Enabled by default                           | Legacy plugin behavior |

In the Java I2P case, you must go to **Router Console → WebApps → I2PControl** and enable it (set to start automatically).
Once active, all methods require that you first authenticate and receive a session token.

---

## 2. JSON-RPC Format

All requests follow the JSON-RPC 2.0 structure:

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

A successful response includes a `result` field; on failure, an `error` object is returned:

```json
{
  "jsonrpc": "2.0",
  "id": "1",
  "result": { /* data */ }
}
```

or

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

---

## 3. Authentication Flow

### Request (Authenticate)

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

### Successful Response

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

| Field      | Direction | Type   | Description                                              |
|------------|-----------|--------|----------------------------------------------------------|
| `API`      | Request   | long   | I2PControl API version requested by the client. Use `1`. |
| `Password` | Request   | String | Password used to authenticate with I2PControl.           |
| `API`      | Response  | long   | Primary API version implemented by the server.           |
| `Token`    | Response  | String | Authentication token used for subsequent requests.       |

You must include that `Token` in all subsequent requests in the `params`.

---

## 4. Methods & Endpoints

### 4.1 RouterInfo

Fetches key telemetry about the router.

**Request Example**

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

Include each desired key in `params` with any value. Only requested keys are returned.

#### Router and Bandwidth Fields

| Key                                    | Type   | Description                                                             |
|----------------------------------------|--------|-------------------------------------------------------------------------|
| `i2p.router.status`                    | String | Free-format, translated router status intended for display.             |
| `i2p.router.uptime`                    | long   | Router uptime in milliseconds. Older i2pd versions may return a string. |
| `i2p.router.version`                   | String | Full router version.                                                    |
| `i2p.router.net.status`                | long   | Network status code; see the table below.                               |
| `i2p.router.net.bw.inbound.1s`         | double | Current inbound bandwidth in bytes per second.                          |
| `i2p.router.net.bw.inbound.15s`        | double | 15-second average inbound bandwidth in bytes per second.                |
| `i2p.router.net.bw.outbound.1s`        | double | Current outbound bandwidth in bytes per second.                         |
| `i2p.router.net.bw.outbound.15s`       | double | 15-second average outbound bandwidth in bytes per second.               |
| `i2p.router.net.tunnels.participating` | long   | Number of tunnels in which this router is participating.                |

#### Status Code Enum (`i2p.router.net.status`)

| Code | Meaning                                             |
|------|-----------------------------------------------------|
| 0    | OK                                                  |
| 1    | TESTING                                             |
| 2    | FIREWALLED                                          |
| 3    | HIDDEN                                              |
| 4    | WARN_FIREWALLED_AND_FAST                            |
| 5    | WARN_FIREWALLED_AND_FLOODFILL                       |
| 6    | WARN_FIREWALLED_WITH_INBOUND_TCP                    |
| 7    | WARN_FIREWALLED_WITH_UDP_DISABLED                   |
| 8    | ERROR_I2CP                                          |
| 9    | ERROR_CLOCK_SKEW                                    |
| 10   | ERROR_PRIVATE_TCP_ADDRESS                           |
| 11   | ERROR_SYMMETRIC_NAT                                 |
| 12   | ERROR_UDP_PORT_IN_USE                               |
| 13   | ERROR_NO_ACTIVE_PEERS_CHECK_CONNECTION_AND_FIREWALL |
| 14   | ERROR_UDP_DISABLED_AND_TCP_UNSET                    |

#### NetDB and Peer Fields

| Key                                  | Type    | Description                                        |
|--------------------------------------|---------|----------------------------------------------------|
| `i2p.router.netdb.knownpeers`        | long    | Number of known peers, excluding the local router. |
| `i2p.router.netdb.activepeers`       | long    | Number of active peers.                            |
| `i2p.router.netdb.fastpeers`         | long    | Number of peers classified as fast.                |
| `i2p.router.netdb.highcapacitypeers` | long    | Number of peers classified as high capacity.       |
| `i2p.router.netdb.isreseeding`       | boolean | Whether a reseed is in progress.                   |

---

### 4.2 GetRate

Used to fetch rate metrics (e.g. bandwidth, tunnel success) over a given time window.

| Parameter | Type   | Description                  |
|-----------|--------|------------------------------|
| `Stat`    | String | Router RateStat name.        |
| `Period`  | long   | Rate period in milliseconds. |

**Request Example**

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

**Sample Response**

```json
{
  "jsonrpc": "2.0",
  "id": "3",
  "result": {
    "Result": 12345.67
  }
}
```

---

### 4.3 RouterManager

Perform administrative actions.

| Parameter          | Result            | Description                                                           |
|--------------------|-------------------|-----------------------------------------------------------------------|
| `Restart`          | null              | Initiates an immediate router restart.                                |
| `RestartGraceful`  | null              | Restarts after participating tunnels expire.                          |
| `Shutdown`         | null              | Initiates an immediate router shutdown.                               |
| `ShutdownGraceful` | null              | Shuts down after participating tunnels expire.                        |
| `Reseed`           | null              | Starts a router reseed.                                               |
| `FindUpdates`      | boolean or String | Blocking. Searches for a signed router update.                        |
| `Update`           | String            | Blocking. Starts a signed router update and returns its final status. |

**Request Example**

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

**Successful Response**

```json
{
  "jsonrpc": "2.0",
  "id": "4",
  "result": {
    "Restart": null
  }
}
```

---

### 4.4 NetworkSetting

Get or set network configuration parameters (ports, upnp, bandwidth share, etc.)

Submit a key with `null` to read its current value, or submit a String to change it.

| Key                             | Accepted Value                                      | Description                                                  |
|---------------------------------|-----------------------------------------------------|--------------------------------------------------------------|
| `i2p.router.net.ntcp.port`      | String, 1–65535                                     | NTCP port; a change requires restart.                        |
| `i2p.router.net.ntcp.hostname`  | String                                              | NTCP hostname; a change requires restart.                    |
| `i2p.router.net.ntcp.autoip`    | `always`, `true`, or `false`                        | NTCP automatic address selection.                            |
| `i2p.router.net.ssu.port`       | String, 1–65535                                     | SSU port; a change requires restart.                         |
| `i2p.router.net.ssu.hostname`   | String                                              | SSU external hostname; a change requires restart.            |
| `i2p.router.net.ssu.autoip`     | `ssu`, `local,ssu`, `upnp,ssu`, or `local,upnp,ssu` | SSU address-discovery sources.                               |
| `i2p.router.net.ssu.detectedip` | null                                                | Read-only detected SSU address.                              |
| `i2p.router.net.upnp`           | String                                              | UPnP setting.                                                |
| `i2p.router.net.bw.share`       | String, 0–100                                       | Percentage of bandwidth available for participating tunnels. |
| `i2p.router.net.bw.in`          | Non-negative integer String                         | Inbound bandwidth limit in KiB/s.                            |
| `i2p.router.net.bw.out`         | Non-negative integer String                         | Outbound bandwidth limit in KiB/s.                           |
| `i2p.router.net.laptopmode`     | String                                              | Laptop mode setting.                                         |

**Request Example (get current values)**

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

**Sample Response**

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

> Note: i2pd versions prior to 2.41 may return numeric types instead of strings — clients should handle both.

---

### 4.5 AdvancedSettings

Allows manipulating internal router parameters.

| Parameter | Type                | Description                                                           |
|-----------|---------------------|-----------------------------------------------------------------------|
| `get`     | String              | Returns one setting inside a `get` result object.                     |
| `getAll`  | n/a                 | Returns the complete configuration map inside `getAll`.               |
| `set`     | Map<String, String> | Updates the supplied settings without removing other keys.            |
| `setAll`  | Map<String, String> | **Destructive:** replaces all settings and removes keys not supplied. |

Parameter names are case-sensitive and use the lower camel-case spelling shown above.

**Request Example**

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

**Response Example**

```json
{
  "jsonrpc": "2.0",
  "id": "6",
  "result": {}
}
```

---

### 4.6 Echo

Echoes a String for debugging and connectivity checks.

| Parameter | Type   | Description                 |
|-----------|--------|-----------------------------|
| `Echo`    | String | Value returned as `Result`. |

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

### 4.7 I2PControl

Manages I2PControl itself. The current Java handler supports password changes.

| Parameter             | Type   | Description                                                                |
|-----------------------|--------|----------------------------------------------------------------------------|
| `i2pcontrol.password` | String | Sets a new I2PControl password and revokes existing authentication tokens. |

The result contains `SettingsSaved`. If the password was changed, the result also contains `"i2pcontrol.password": null`. Listen-address and listen-port settings from the legacy standalone plugin are not active in the current Java handler.

---

## 5. Error Codes

### Standard JSON-RPC2 Error Codes

| Code   | Meaning            |
|--------|--------------------|
| -32700 | JSON parse error   |
| -32600 | Invalid request    |
| -32601 | Method not found   |
| -32602 | Invalid parameters |
| -32603 | Internal error     |

### I2PControl Specific Error Codes

| Code   | Meaning                                                                                  |
|--------|------------------------------------------------------------------------------------------|
| -32001 | Invalid password provided                                                                |
| -32002 | No authentication token presented                                                        |
| -32003 | Authentication token doesn't exist                                                       |
| -32004 | The provided authentication token was expired and will be removed                        |
| -32005 | The version of the I2PControl API used wasn't specified, but is required to be specified |
| -32006 | The version of the I2PControl API specified is not supported by I2PControl               |

---

## 6. Usage & Best Practices

- Always include the `Token` parameter (except when authenticating).
- Change the default password (`itoopie`) upon first use.
- For Java I2P, ensure the I2PControl webapp is enabled via WebApps.
- Be prepared for slight variations: some fields may be numbers or strings, depending on I2P version.
- Wrap long status strings for display-friendly output.

---
