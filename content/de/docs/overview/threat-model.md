---
title: "I2P Bedrohungsmodell"
description: "Katalog der bei der Entwicklung von I2P berücksichtigten Angriffe und die implementierten Gegenmaßnahmen"
slug: "threat-model"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
reviewStatus: "needs-review"
---

## 1. Was "Anonym" bedeutet

I2P bietet *praktische Anonymität* – keine Unsichtbarkeit. Anonymität ist definiert als die Schwierigkeit für einen Angreifer, Informationen zu erfahren, die Sie privat halten möchten: wer Sie sind, wo Sie sind oder mit wem Sie kommunizieren. Absolute Anonymität ist unmöglich; stattdessen strebt I2P **ausreichende Anonymität** unter globalen passiven und aktiven Angreifern an.

Ihre Anonymität hängt davon ab, wie Sie I2P konfigurieren, wie Sie Peers und Abonnements auswählen und welche Anwendungen Sie freigeben.

---

## 2. Kryptografische und Transport-Evolution (2003 → 2025)

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
**Aktuelle kryptografische Suite (Noise XK):** - **X25519** für Schlüsselaustausch   - **ChaCha20/Poly1305 AEAD** für Verschlüsselung   - **Ed25519 (EdDSA-SHA512)** für Signaturen   - **SHA-256** für Hashing und HKDF   - Optional **ML-KEM-Hybride** für Post-Quantum-Tests

Alle ElGamal- und AES-CBC-Verwendungen wurden eingestellt. Der Transport erfolgt vollständig über NTCP2 (TCP) und SSU2 (UDP); beide unterstützen IPv4/IPv6, Forward Secrecy und DPI-Verschleierung.

---

## 3. Übersicht der Netzwerkarchitektur

- **Free-route mixnet:** Sender und Empfänger definieren jeweils ihre eigenen tunnel.  
- **Keine zentrale Autorität:** Routing und Namensauflösung sind dezentralisiert; jeder router pflegt lokales Vertrauen.  
- **Unidirektionale tunnel:** Eingehende und ausgehende sind getrennt (10 Min. Lebensdauer).  
- **Exploratory tunnels:** Standardmäßig 2 hops; Client-tunnel 2–3 hops.  
- **Floodfill router:** ~1 700 von ~55 000 Knoten (~6 %) verwalten die verteilte netDb.  
- **NetDB-Rotation:** Schlüsselraum rotiert täglich um UTC-Mitternacht.  
- **Sub-DB-Isolierung:** Seit 2.4.0 verwenden jeder Client und router separate Datenbanken, um Verknüpfungen zu verhindern.

---

## 4. Angriffskategorien und aktuelle Schutzmaßnahmen

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

## 5. Moderne Netzwerkdatenbank (NetDB)

**Grundlegende Fakten (noch aktuell):** - Modifizierter Kademlia DHT speichert RouterInfo und LeaseSets.   - SHA-256 Key-Hashing; parallele Abfragen an 2 nächste Floodfills mit 10 s Timeout.   - LeaseSet-Lebensdauer ≈ 10 Min. (LeaseSet2) oder 18 Std. (MetaLeaseSet).

**Neue Typen (seit 0.9.38):** - **LeaseSet2 (Typ 3)** – mehrere Verschlüsselungstypen, mit Zeitstempel.   - **EncryptedLeaseSet2 (Typ 5)** – geblendete Destination für private Dienste (DH- oder PSK-Authentifizierung).   - **MetaLeaseSet (Typ 7)** – Multihoming und erweiterte Ablaufzeiten.

**Wichtiges Sicherheits-Upgrade – Sub-DB-Isolation (2.4.0):** - Verhindert die Zuordnung von router↔Client.   - Jeder Client und router verwenden separate netDb-Segmente.   - Verifiziert und geprüft (2.5.0).

---

## 6. Versteckter Modus und eingeschränkte Routen

- **Hidden Mode:** Implementiert (automatisch in restriktiven Ländern gemäß Freedom House-Bewertungen).  
    Router veröffentlichen keine RouterInfo und leiten keinen Traffic weiter.  
- **Restricted Routes:** Teilweise implementiert (nur grundlegende trust-basierte tunnel).  
    Umfassendes Routing über vertrauenswürdige Peers bleibt geplant (3.0+).

Kompromiss: Bessere Privatsphäre ↔ reduzierter Beitrag zur Netzwerkkapazität.

---

## 7. DoS- und Floodfill-Angriffe

**Historisch:** Eine Studie der UCSB aus 2013 zeigte, dass Eclipse- und Floodfill-Übernahmen möglich waren. **Moderne Abwehrmaßnahmen umfassen:** - Tägliche Keyspace-Rotation. - Floodfill-Obergrenze ≈ 500, eine pro /16. - Randomisierte Verzögerungen bei der Speicherüberprüfung. - Bevorzugung neuerer Router (2.6.0). - Behebung der automatischen Registrierung (2.9.0). - Überlastungsbewusste Routenführung und Lease-Drosselung (2.4.0+).

Floodfill-Angriffe bleiben theoretisch möglich, sind aber praktisch schwieriger.

---

## 8. Verkehrsanalyse und Zensur

I2P-Verkehr ist schwer zu identifizieren: kein fester Port, kein Klartext-Handshake und zufälliges Padding. NTCP2- und SSU2-Pakete ahmen gängige Protokolle nach und verwenden ChaCha20-Header-Verschleierung. Padding-Strategien sind grundlegend (zufällige Größen), Dummy-Traffic ist nicht implementiert (kostspielig). Verbindungen von Tor-Exit-Knoten werden seit Version 2.6.0 blockiert (zum Schutz der Ressourcen).

---

## 9. Dauerhafte Einschränkungen (anerkannt)

- Timing-Korrelation für Anwendungen mit niedriger Latenz bleibt ein grundlegendes Risiko.
- Intersection-Angriffe bleiben wirksam gegen bekannte öffentliche Ziele.
- Sybil-Angriffe haben keine vollständige Abwehr (HashCash wird nicht durchgesetzt).
- Konstanter Datenverkehr und nichttriviale Verzögerungen bleiben nicht implementiert (geplant für 3.0).

Transparenz über diese Grenzen ist beabsichtigt – sie verhindert, dass Benutzer die Anonymität überschätzen.

---

## 10. Netzwerkstatistiken (2025)

- ~55 000 aktive Router weltweit (↑ von 7 000 im Jahr 2013)  
- ~1 700 floodfill-Router (~6 %)  
- 95 % nehmen standardmäßig am Tunnel-Routing teil  
- Bandbreitenstufen: K (<12 KB/s) → X (>2 MB/s)  
- Minimale floodfill-Rate: 128 KB/s  
- Router-Konsole Java 8+ (erforderlich), Java 17+ für den nächsten Zyklus geplant

---

## 11. Entwicklung und zentrale Ressourcen

- Offizielle Website: [geti2p.net](/)
- Dokumentation: [Documentation](/docs/)  
- Debian-Repository: <https://deb.i2pgit.org> ( hat deb.i2p2.de im Oktober 2023 ersetzt )  
- Quellcode: <https://i2pgit.org/I2P_Developers/i2p.i2p> (Gitea) + GitHub-Mirror  
- Alle Releases sind signierte SU3-Container (RSA-4096, zzz/str4d-Schlüssel)  
- Keine aktiven Mailinglisten; Community über <https://i2pforum.net> und IRC2P.  
- Update-Zyklus: 6–8 Wochen für stabile Releases.

---

## 12. Zusammenfassung der Sicherheitsverbesserungen seit 0.8.x

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

## 13. Bekannte offene oder geplante Arbeiten

- Umfassende eingeschränkte Routen (trusted-peer routing) → geplant für 3.0.  
- Nicht-triviale Verzögerung/Bündelung für Timing-Resistenz → geplant für 3.0.  
- Erweiterte Padding- und Dummy-Traffic-Mechanismen → nicht implementiert.  
- HashCash-Identitätsverifizierung → Infrastruktur vorhanden, aber inaktiv.  
- R5N DHT-Ersatz → nur als Vorschlag.

---

## 14. Wichtige Referenzen

- *Practical Attacks Against the I2P Network* (Egger et al., RAID 2013)  
- *Privacy Implications of Performance-Based Peer Selection* (Herrmann & Grothoff, PETS 2011)  
- *Resilience of the Invisible Internet Project* (Muntaka et al., Wiley 2025)  
- [Offizielle I2P-Dokumentation](/docs/)

---

## 15. Fazit

Das zentrale Anonymitätsmodell von I2P besteht seit zwei Jahrzehnten: Verzicht auf globale Eindeutigkeit zugunsten lokalen Vertrauens und lokaler Sicherheit. Von ElGamal zu X25519, NTCP zu NTCP2 und von manuellen Reseeds bis zur Sub-DB-Isolation hat sich das Projekt weiterentwickelt und dabei seine Philosophie der mehrstufigen Verteidigung und Transparenz beibehalten.

Viele Angriffe bleiben theoretisch gegen jedes Mixnet mit geringer Latenz möglich, aber die kontinuierliche Härtung von I2P macht sie zunehmend unpraktisch. Das Netzwerk ist größer, schneller und sicherer als je zuvor – bleibt aber dennoch ehrlich hinsichtlich seiner Grenzen.
