---
title: "NTCP-Diskussion"
description: "Historische Anmerkungen zum Vergleich der NTCP- und SSU-Transportprotokolle sowie vorgeschlagene Optimierungsideen"
slug: "ntcp"
layout: "single"
reviewStatus: "needs-review"
---

## NTCP vs. SSU Diskussion (März 2007)

### Fragen zu NTCP

_Basierend auf einem IRC-Gespräch zwischen zzz und cervantes._

- **Warum hat NTCP Vorrang vor SSU, wenn NTCP offenbar zusätzlichen Overhead und Latenz verursacht?**  
  NTCP bietet im Allgemeinen eine bessere Zuverlässigkeit als die ursprüngliche SSU-Implementierung.
- **Führt Streaming über NTCP zum klassischen TCP-over-TCP-Zusammenbruch?**  
  Möglicherweise, aber SSU war als leichtgewichtige UDP-Option gedacht und erwies sich in der Praxis als zu unzuverlässig.

### “NTCP gilt als schädlich” (zzz, 25. März 2007)

Zusammenfassung: Die höhere Latenz und der Overhead von NTCP können zu Überlastung führen, dennoch bevorzugt das Routing NTCP, weil dessen Gebotspunkte (bid scores) hartcodiert niedriger sind als die von SSU. Die Analyse brachte mehrere Punkte zur Sprache:


#### Vorschläge aus dem Thread von 2007

1. **Transportprioritäten umstellen**, damit Router SSU bevorzugen (Wiederherstellung von `i2np.udp.alwaysPreferred`).
2. **Streaming-Verkehr markieren**, sodass SSU nur für markierte Nachrichten niedriger bietet, ohne die Anonymität zu beeinträchtigen.
3. **Grenzen für SSU-Wiederübertragungen verschärfen**, um das Risiko eines Zusammenbruchs zu verringern.
4. **Teilzuverlässige Underlay-Netze untersuchen**, um festzustellen, ob Wiederübertragungen unterhalb der Streaming-Bibliothek ein Netto-Vorteil sind.
5. **Prioritätswarteschlangen und Timeouts überprüfen**—zum Beispiel die Streaming-Timeouts auf über 45 s erhöhen, um sie an NTCP anzugleichen.

### Antwort von jrandom (27. März 2007)

Wesentliche Gegenargumente:

- NTCP existiert, weil frühe SSU-Bereitstellungen unter Staukollaps litten. Selbst moderate Wiederübertragungsraten pro Hop können sich über tunnels mit mehreren Hops explosionsartig vervielfachen.
- Ohne Bestätigungen auf tunnel-Ebene erhält nur ein Teil der Nachrichten einen Ende-zu-Ende-Zustellstatus; Ausfälle können unbemerkt bleiben.
- Die TCP-Staukontrolle wurde über Jahrzehnte optimiert; NTCP nutzt dies über ausgereifte TCP-Stacks.
- Beobachtete Effizienzgewinne bei Bevorzugung von SSU könnten eher das Warteschlangenverhalten im router widerspiegeln als intrinsische Protokollvorteile.
- Größere Streaming-Timeouts verbesserten die Stabilität bereits; mehr Beobachtung und Daten wurden empfohlen, bevor größere Änderungen vorgenommen werden.

Die Debatte trug dazu bei, die nachfolgende Transportabstimmung zu verfeinern, spiegelt jedoch nicht die moderne NTCP2/SSU2-Architektur wider.
