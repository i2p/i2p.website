---
title: "Access Filter Format"
description: "Syntax for tunnel access-control filter files"
slug: "filter-format"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
type: docs
---

Access filters let I2PTunnel server operators allow, deny, or throttle inbound connections based on the source Destination and recent connection rate. The filter is a plain text file of rules. The file is read top to bottom and the **first matching rule wins**.

> Changes to the filter definition take effect **on tunnel restart**. Some builds may re-read file-based lists at runtime, but plan for a restart to guarantee changes are applied.

## File format

- One rule per line.  
- Blank lines are ignored.  
- `#` starts a comment that runs to end of line.  
- Rules are evaluated in order; the first match is used.

## Thresholds

A **threshold** defines how many connection attempts from a single Destination are permitted in a rolling time window.

- **Numeric:** `N/S` means allow `N` connections per `S` seconds. Example: `15/5` permits up to 15 connections every 5 seconds. The `N+1` attempt within the window is rejected.  
- **Keywords:** `allow` means no limit. `deny` means always reject.

## Rule syntax

Rules take the form:

```
<threshold> <scope> <target>
```

Where:

- `<threshold>` is `N/S`, `allow`, or `deny`  
- `<scope>` is one of `default`, `explicit`, `file`, or `record` (see below)  
- `<target>` depends on scope

### Default rule

Applies when no other rule matches. Only **one** default rule is allowed. If omitted, unknown Destinations are permitted without restriction.

```
15/5 default
allow default
deny default
```

### Explicit rule

Targets a specific Destination by Base32 address (for example `example1.b32.i2p`) or full key.

```
15/5 explicit example1.b32.i2p
deny explicit example2.b32.i2p
allow explicit example3.b32.i2p
```

### File-based rule

Targets **all** Destinations listed in an external file. Each line contains one Destination; `#` comments and blank lines are allowed.

```
15/5 file /var/i2p/throttled.txt
deny file /var/i2p/blocked.txt
allow file /var/i2p/trusted.txt
```

> Operational note: Some implementations re-read file lists periodically. If you edit a list while the tunnel is running, expect a short delay before changes are noticed. Restart to apply immediately.

### Recorder (progressive control)

A **recorder** monitors connection attempts and writes Destinations that breach a threshold to a file. You can then reference that file in a `file` rule to apply throttles or blocks on future attempts.

```
# Start permissive
allow default

# Record Destinations exceeding 30 connections in 5 seconds
30/5 record /var/i2p/aggressive.txt

# Apply throttling to recorded Destinations
15/5 file /var/i2p/aggressive.txt
```

> Verify recorder support in your build before relying on it. Use `file` lists for guaranteed behavior.

## Evaluation order

Put specific rules first, then general ones. A common pattern:

1. Explicit allows for trusted peers  
2. Explicit denies for known abusers  
3. File-based allow/deny lists  
4. Recorders for progressive throttling  
5. Default rule as a catch-all

## Full example

```
# Moderate limits by default
30/10 default

# Always allow trusted peers
allow explicit friend1.b32.i2p
allow explicit friend2.b32.i2p

# Block known bad actors
deny file /var/i2p/blocklist.txt

# Throttle aggressive sources
15/5 file /var/i2p/throttle.txt

# Automatically populate the throttle list
60/5 record /var/i2p/throttle.txt
```

## Implementation notes

- The access filter operates at the tunnel layer, before application handling, so abusive traffic can be rejected early.  
- Place the filter file in your I2PTunnel configuration directory and restart the tunnel to apply changes.  
- Share file-based lists across multiple tunnels if you want consistent policy across services.
