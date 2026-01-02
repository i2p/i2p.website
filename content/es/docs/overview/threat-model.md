---
title: "Modelo de Amenazas de I2P"
description: "Catálogo de ataques considerados en el diseño de I2P y las mitigaciones implementadas"
slug: "threat-model"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
reviewStatus: "needs-review"
---

## 1. Qué Significa "Anónimo"

I2P proporciona *anonimato práctico*—no invisibilidad. El anonimato se define como la dificultad para un adversario de obtener información que deseas mantener privada: quién eres, dónde estás o con quién hablas. El anonimato absoluto es imposible; en su lugar, I2P busca lograr **anonimato suficiente** frente a adversarios pasivos y activos globales.

Tu anonimato depende de cómo configures I2P, cómo elijas peers y suscripciones, y qué aplicaciones expongas.

---

## 2. Evolución Criptográfica y de Transporte (2003 → 2025)

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Era</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Primary Algorithms</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.3 – 0.9</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ElGamal + AES-256 + DSA-SHA1</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Legacy stack (2003–2015)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.15</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Ed25519 signatures</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Replaced DSA</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.36 (2018)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>NTCP2</strong> introduced</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Noise <em>XK_25519_ChaChaPoly_SHA256</em></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.56 (2022)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>SSU2</strong> enabled by default</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Noise-based UDP transport</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.4.0 (2023)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>NetDB Sub-DB isolation</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Prevents router↔client linkage</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.8.0+ (2025)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Congestion-aware routing / observability reductions</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">DoS hardening</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.10.0 (2025)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Post-quantum hybrid ML-KEM support (optional)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Experimental</td>
    </tr>
  </tbody>
</table>
**Suite criptográfica actual (Noise XK):** - **X25519** para intercambio de claves   - **ChaCha20/Poly1305 AEAD** para cifrado   - **Ed25519 (EdDSA-SHA512)** para firmas   - **SHA-256** para hashing y HKDF   - **Híbridos ML-KEM** opcionales para pruebas post-cuánticas

Todos los usos de ElGamal y AES-CBC han sido retirados. El transporte es enteramente NTCP2 (TCP) y SSU2 (UDP); ambos soportan IPv4/IPv6, forward secrecy (secreto hacia adelante) y ofuscación DPI.

---

## 3. Resumen de la Arquitectura de Red

- **Mixnet de ruta libre:** Los remitentes y receptores definen sus propios tunnels.  
- **Sin autoridad central:** El enrutamiento y el nombramiento están descentralizados; cada router mantiene confianza local.  
- **Tunnels unidireccionales:** Los entrantes y salientes son separados (ciclos de vida de 10 min).  
- **Tunnels exploratorios:** 2 saltos por defecto; tunnels de cliente de 2–3 saltos.  
- **Routers floodfill:** ~1 700 de ~55 000 nodos (~6 %) mantienen el NetDB distribuido.  
- **Rotación de NetDB:** El espacio de claves rota diariamente a medianoche UTC.  
- **Aislamiento de sub-BD:** Desde la versión 2.4.0, cada cliente y router utilizan bases de datos separadas para evitar la vinculación.

---

## 4. Categorías de Ataques y Defensas Actuales

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Category</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Current Status (2025)</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Primary Defenses</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Brute Force / Cryptanalysis</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Impractical with modern primitives (X25519, ChaCha20).</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Strong crypto, key rotation, Noise handshakes.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Timing Attacks</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Still unsolved for low-latency systems.</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Unidirectional tunnels, 1024&nbsp;B cells, profile recalc (45&nbsp;s). Research continues for non-trivial delays (3.0+).</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Intersection Attacks</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Inherent weakness of low latency mixnets.</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Tunnel rotation (10&nbsp;min), leaseset expirations, multihoming.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Predecessor Attacks</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Partially mitigated.</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Tiered peer selection, strict XOR ordering, variable length tunnels.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Sybil Attacks</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">No comprehensive defense.</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">IP /16 limits, profiling, diversity rules; HashCash infra exists but not required.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Floodfill / NetDB Attacks</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Improved but still a concern.</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">One /16 per lookup, limit 500 active, daily rotation, randomized verification delay, Sub-DB isolation.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>DoS / Flooding</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Frequent (esp. 2023 incidents).</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Congestion-aware routing (2.4+), aggressive leaseset removal (2.8+).</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Traffic ID / Fingerprinting</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Greatly reduced.</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Noise obfuscation, random padding, no plaintext headers.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Censorship / Partitioning</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Possible with state-level blocking.</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Hidden mode, IPv6, multiple reseeds, mirrors.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Development / Supply Chain</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Mitigated.</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Open source, signed SU3 releases (RSA-4096), multi-signer trust model.</td>
    </tr>
  </tbody>
</table>
---

## 5. Base de Datos de Red Moderna (NetDB)

**Datos fundamentales (aún vigentes):** - DHT Kademlia modificado almacena RouterInfo y LeaseSets.   - Hash de clave SHA-256; consultas paralelas a los 2 floodfills más cercanos con tiempo de espera de 10 s.   - Vida útil de LeaseSet ≈ 10 min (LeaseSet2) o 18 h (MetaLeaseSet).

**Nuevos tipos (desde 0.9.38):** - **LeaseSet2 (Tipo 3)** – múltiples tipos de cifrado, con marca de tiempo.   - **EncryptedLeaseSet2 (Tipo 5)** – destino ofuscado para servicios privados (autenticación DH o PSK).   - **MetaLeaseSet (Tipo 7)** – multialojamiento y expiraciones extendidas.

**Actualización de seguridad importante – Aislamiento de Sub-DB (2.4.0):** - Previene la asociación router↔cliente.   - Cada cliente y router utilizan segmentos netDb separados.   - Verificado y auditado (2.5.0).

---

## 6. Modo Oculto y Rutas Restringidas

- **Modo Oculto:** Implementado (automático en países estrictos según puntuaciones de Freedom House).  
    Los routers no publican RouterInfo ni enrutan tráfico.  
- **Rutas Restringidas:** Parcialmente implementado (túneles básicos solo de confianza).  
    El enrutamiento integral de peers de confianza permanece planificado (3.0+).

Compromiso: Mejor privacidad ↔ menor contribución a la capacidad de la red.

---

## 7. Ataques DoS y Floodfill

**Histórico:** Una investigación de UCSB en 2013 demostró que los ataques Eclipse y la toma de control de Floodfill eran posibles. **Las defensas modernas incluyen:** - Rotación diaria del espacio de claves. - Límite de Floodfill ≈ 500, uno por /16. - Retrasos aleatorios de verificación de almacenamiento. - Preferencia por routers más nuevos (2.6.0). - Corrección de inscripción automática (2.9.0). - Enrutamiento consciente de congestión y limitación de lease (2.4.0+).

Los ataques floodfill siguen siendo teóricamente posibles pero prácticamente más difíciles.

---

## 8. Análisis de Tráfico y Censura

El tráfico I2P es difícil de identificar: sin puerto fijo, sin handshake en texto plano y relleno aleatorio. Los paquetes NTCP2 y SSU2 imitan protocolos comunes y usan ofuscación de encabezado ChaCha20. Las estrategias de relleno son básicas (tamaños aleatorios), el tráfico ficticio no está implementado (costoso). Las conexiones desde nodos de salida Tor están bloqueadas desde la versión 2.6.0 (para proteger recursos).

---

## 9. Limitaciones Persistentes (reconocidas)

- La correlación de tiempo para aplicaciones de baja latencia sigue siendo un riesgo fundamental.
- Los ataques de intersección siguen siendo poderosos contra destinos públicos conocidos.
- Los ataques Sybil carecen de defensa completa (HashCash no se aplica).
- El tráfico de tasa constante y los retrasos no triviales permanecen sin implementar (planificados para 3.0).

La transparencia sobre estos límites es intencional — evita que los usuarios sobreestimen el anonimato.

---

## 10. Estadísticas de Red (2025)

- ~55 000 routers activos en todo el mundo (↑ desde 7 000 en 2013)  
- ~1 700 routers floodfill (~6 %)  
- 95 % participa en enrutamiento de túneles por defecto  
- Niveles de ancho de banda: K (<12 KB/s) → X (>2 MB/s)  
- Tasa mínima floodfill: 128 KB/s  
- Consola del router Java 8+ (requerido), Java 17+ planificado para el próximo ciclo

---

## 11. Desarrollo y Recursos Centrales

- Sitio oficial: [geti2p.net](/)
- Documentación: [Documentation](/docs/)  
- Repositorio Debian: <https://deb.i2pgit.org> ( reemplazó deb.i2p2.de en Oct 2023 )  
- Código fuente: <https://i2pgit.org/I2P_Developers/i2p.i2p> (Gitea) + espejo GitHub  
- Todas las versiones son contenedores SU3 firmados (RSA-4096, claves zzz/str4d)  
- Sin listas de correo activas; comunidad vía <https://i2pforum.net> e IRC2P.  
- Ciclo de actualizaciones: versiones estables cada 6–8 semanas.

---

## 12. Resumen de Mejoras de Seguridad Desde 0.8.x

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Year</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Feature</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Effect</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2015</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Ed25519 signatures</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Removed SHA1/DSA weakness</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2018</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">NTCP2</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Noise-based TCP transport</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2019</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">LeaseSet2 / EncryptedLeaseSet2</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Hidden services privacy</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2022</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">SSU2</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Noise-based UDP transport</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2023</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Sub-DB Isolation + Congestion-Aware Routing</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Stopped NetDB linkage / improved resilience</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2024</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Floodfill selection improvements</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reduced long-term node influence</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2025</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Observability reductions + PQ hybrid crypto</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Harder timing analysis / future-proofing</td>
    </tr>
  </tbody>
</table>
---

## 13. Trabajo Conocido No Resuelto o Planificado

- Rutas restringidas completas (enrutamiento de pares confiables) → planificado 3.0.  
- Retardo/agrupamiento no trivial para resistencia de temporización → planificado 3.0.  
- Relleno avanzado y tráfico ficticio → no implementado.  
- Verificación de identidad HashCash → la infraestructura existe pero está inactiva.  
- Reemplazo R5N DHT → solo propuesta.

---

## 14. Referencias Clave

- *Practical Attacks Against the I2P Network* (Egger et al., RAID 2013)  
- *Privacy Implications of Performance-Based Peer Selection* (Herrmann & Grothoff, PETS 2011)  
- *Resilience of the Invisible Internet Project* (Muntaka et al., Wiley 2025)  
- [Documentación Oficial de I2P](/docs/)

---

## 15. Conclusión

El modelo central de anonimato de I2P se ha mantenido durante dos décadas: sacrificar la unicidad global por la confianza y seguridad locales. Desde ElGamal a X25519, NTCP a NTCP2, y desde reseeds manuales hasta el aislamiento de Sub-DB, el proyecto ha evolucionado manteniendo su filosofía de defensa en profundidad y transparencia.

Muchos ataques siguen siendo teóricamente posibles contra cualquier mixnet de baja latencia, pero el fortalecimiento continuo de I2P los hace cada vez más impracticables. La red es más grande, más rápida y más segura que nunca, pero sigue siendo honesta acerca de sus límites.
