---
title: "BitTorrent sobre I2P"
description: "Especificación detallada y descripción general del ecosistema de BitTorrent dentro de la red I2P"
slug: "bittorrent"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

## Resumen

BitTorrent sobre I2P permite el intercambio anónimo de archivos a través de túneles cifrados utilizando la capa de streaming de I2P. Todos los pares se identifican mediante destinos criptográficos de I2P en lugar de direcciones IP. El sistema soporta rastreadores HTTP y UDP, enlaces magnet híbridos y cifrado híbrido post-cuántico.

---

## 1. Pila de Protocolos

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Layer</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Function</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Example</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Application</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">BitTorrent</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">i2psnark, BiglyBT</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Transport</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Streaming / SAM v3</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">I2CP, NTCP2</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Network</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Garlic routing</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">I2NP</td>
    </tr>
  </tbody>
</table>
Todas las conexiones se ejecutan a través de la capa de transporte cifrada de I2P (NTCP2 o SSU2). Incluso los paquetes del tracker UDP están encapsulados dentro del streaming de I2P.

---

## 2. Rastreadores

### Rastreadores HTTP

Los trackers `.i2p` estándar responden a peticiones HTTP GET tales como:

```
http://tracker2.postman.i2p/announce?info_hash=<20-byte>&peer_id=<20-byte>&port=6881&uploaded=0&downloaded=0&left=1234&compact=1
```
Las respuestas están **bencodeadas** y utilizan hashes de destino I2P para los peers.

### Rastreadores UDP

Los rastreadores UDP fueron estandarizados en 2025 (Propuesta 160).

**Rastreadores UDP principales** - `udp://tracker2.postman.i2p/announce` - `udp://opentracker.simp.i2p/a` - `http://opentracker.skank.i2p/a` - `http://opentracker.dg2.i2p/a` ---

## 3. Enlaces Magnet

```
magnet:?xt=urn:btih:<infohash>&dn=<name>&tr=http://tracker2.postman.i2p/announce&tr=udp://denpa.i2p/announce&xs=i2p:<destination.b32.i2p>
```
<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Parameter</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Meaning</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>xs=i2p:&lt;dest&gt;</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Explicit I2P destination</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>tr=</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Tracker URLs (HTTP or UDP)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>dn=</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Display name</td>
    </tr>
  </tbody>
</table>
Los enlaces magnet admiten enjambres híbridos entre I2P y clearnet cuando están configurados.

---

## 4. Implementaciones de DHT

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Implementation</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Status</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Java I2P</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Experimental overlay</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Stable</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">i2pd</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">UDP-based internal overlay</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Active</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">BiglyBT</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">SAM v3.3-based</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Fully supported</td>
    </tr>
  </tbody>
</table>
---

## 5. Implementaciones de Cliente

### I2PSnark

- Incluido con todos los routers
- Soporte solo para rastreadores HTTP
- Rastreador integrado en `http://127.0.0.1:7658/`
- Sin soporte para rastreadores UDP

### BiglyBT

- Con todas las funciones mediante complemento I2P
- Compatible con rastreadores HTTP + UDP
- Compatibilidad con torrents híbridos
- Utiliza la interfaz SAM v3.3

### Tixati / XD

- Clientes ligeros
- Túneles basados en SAM
- Cifrado híbrido ML-KEM experimental

---

## 6. Configuración

### I2PSnark

```
i2psnark.dir=/home/user/torrents
i2psnark.autostart=true
i2psnark.maxUpBW=128
i2psnark.maxDownBW=256
i2psnark.enableDHT=false
```
### BiglyBT

```
SAMHost=127.0.0.1
SAMPort=7656
SAMNickname=BiglyBT-I2P
SAMAutoStart=true
DHTEnabled=true
```
---

## 7. Modelo de Seguridad

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Component</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Encryption</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">NTCP2 / SSU2 with X25519+ML-KEM hybrid</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Identity</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">I2P destinations replace IP addresses</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Anonymity</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Peer info hidden; traffic multiplexed</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Leak Prevention</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Remove headers (X-Forwarded-For, Client-IP, Via)</td>
    </tr>
  </tbody>
</table>
Los torrents híbridos (clearnet + I2P) deben usarse solo si el anonimato no es crítico.

---

## 8. Rendimiento

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Factor</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Impact</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Recommendation</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Tunnel length</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Adds latency</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1-hop client, 2-hop server</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Peers</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Boosts speed</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">20+ active peers</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Compression</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Minimal gain</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Usually off</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Bandwidth</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Router-limited</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Default settings optimal</td>
    </tr>
  </tbody>
</table>
Las velocidades típicas oscilan entre **30–80 KB/s**, dependiendo de los peers y las condiciones de la red.

---

## 9. Problemas Conocidos

- Interoperabilidad parcial de DHT entre Java I2P e i2pd  
- Retraso en la obtención de metadatos magnet bajo carga elevada  
- NTCP1 obsoleto pero aún utilizado por peers antiguos  
- UDP simulado sobre streaming aumenta la latencia

---

## 10. Hoja de Ruta Futura

- Multiplexación tipo QUIC  
- Integración completa de ML-KEM  
- Lógica unificada de enjambre híbrido  
- Mirrors de reseed mejorados  
- Reintentos adaptativos de DHT

---

## Referencias

- [BEP 15 – UDP Tracker Protocol](https://www.bittorrent.org/beps/bep_0015.html)
- [Propuesta 160 – UDP Tracker sobre I2P](/proposals/160-udp-trackers/)
- [Documentación de I2PSnark](/docs/applications/bittorrent/)
- [Especificación de la Biblioteca Streaming](/docs/specs/streaming/)

---
