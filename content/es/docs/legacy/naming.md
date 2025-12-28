---
title: "Discusión sobre el sistema de nombres"
description: "Debate histórico sobre el modelo de nombres de I2P y por qué se rechazaron los esquemas globales al estilo DNS"
slug: "naming"
layout: "single"
lastUpdated: "2025-02"
accurateFor: "historical"
reviewStatus: "needs-review"
---

> **Contexto:** Esta página archiva debates prolongados de los primeros tiempos del diseño de I2P. Explica por qué el proyecto optó por libretas de direcciones de confianza local en lugar de consultas al estilo DNS o registros por voto mayoritario. Para obtener orientación sobre el uso actual, consulta la [documentación de nombres](/docs/overview/naming/).

## Alternativas descartadas

Los objetivos de seguridad de I2P descartan los esquemas de nombres convencionales:

- **Resolución al estilo DNS.** Cualquier resolvedor en la ruta de consulta podría falsificar o censurar respuestas. Incluso con DNSSEC, los registradores o las autoridades certificadoras comprometidos siguen siendo un punto único de falla. En I2P, los destinos *son* claves públicas—secuestrar una consulta comprometería por completo una identidad.
- **Nomenclatura basada en votación.** Un adversario puede crear identidades ilimitadas (un ataque Sybil) y “ganar” votos para nombres populares. Las mitigaciones de prueba de trabajo elevan el costo pero introducen una fuerte sobrecarga de coordinación.

En cambio, I2P mantiene deliberadamente la resolución de nombres por encima de la capa de transporte. La biblioteca de resolución de nombres incluida ofrece una interfaz de proveedor de servicios para que los esquemas alternativos puedan coexistir—los usuarios deciden en qué libretas de direcciones o jump services (servicios de salto) confían.

## Nombres locales vs globales (jrandom, 2005)

- Los nombres en I2P son únicos localmente pero legibles para humanos. Tu `boss.i2p` puede no coincidir con el `boss.i2p` de otra persona, y eso es por diseño.
- Si un actor malicioso te engañara para cambiar el destino detrás de un nombre, en la práctica secuestraría un servicio. Rechazar la unicidad global evita esa clase de ataque.
- Trata los nombres como marcadores o apodos de mensajería instantánea—tú eliges en qué destinos confiar suscribiéndote a libretas de direcciones específicas o agregando claves manualmente.

## Objeciones comunes & respuestas (zzz)

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Concern</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Response</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>“Downloading hosts.txt is inefficient.”</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">At ~400&nbsp;KB for ~800 hosts the bandwidth impact is minor (~10&nbsp;B/s if refreshed twice daily). ETags already avoid unnecessary transfers. Alternate formats (for example <code>recenthosts.cgi</code>) can deliver only new entries.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>“It won’t scale.”</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">A hosts.txt entry is ~500&nbsp;bytes; storing thousands locally is practical. Real-time lookups would dramatically slow browsing.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>“Requires trust and manual setup.”</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">True—and intentional. Users must choose address book providers they trust. Trust is not binary; forcing configuration encourages users to think about it.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>“Why not just use DNS?”</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">DNS depends on short TTLs and can be hijacked mid-path. I2P destinations are immutable public keys, so DNS semantics map poorly.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>“Subscriptions rely on specific servers.”</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Subscriptions are decentralised—you can add multiple providers or run your own. Completely decentralised systems struggle with conflict resolution and hijacking.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>“Jump services and hosts.txt feel awkward.”</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">They are pragmatic trade-offs. Jump services provide just-in-time lookups; subscriptions keep a local cache for performance.</td>
    </tr>
  </tbody>
</table>
## Ideas de eficiencia discutidas

- Proporcionar actualizaciones incrementales (solo los destinos añadidos desde la última obtención).
- Ofrecer fuentes suplementarias (`recenthosts.cgi`) junto con archivos de hosts completos.
- Explorar herramientas automatizables con scripts (por ejemplo, `i2host.i2p`) para combinar fuentes o filtrar por niveles de confianza.

## Puntos clave

- La seguridad prima sobre el consenso global: las libretas de direcciones gestionadas localmente minimizan el riesgo de secuestro.
- Múltiples enfoques de nomenclatura pueden coexistir mediante la API de nombres—los usuarios deciden en qué confiar.
- La nomenclatura global completamente descentralizada sigue siendo un problema de investigación abierto; los compromisos entre la seguridad, la memorabilidad humana y la unicidad global aún reflejan el [triángulo de Zooko](https://zooko.com/distnames.html).

## Referencias

- [Documentación de nombres](/docs/overview/naming/)
- [“Nombres: descentralizados, seguros y significativos para humanos: elige dos” de Zooko](https://zooko.com/distnames.html)
- Fuente incremental de ejemplo: [stats.i2p/cgi-bin/newhosts.txt](http://stats.i2p/cgi-bin/newhosts.txt)
