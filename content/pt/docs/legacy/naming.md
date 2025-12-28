---
title: "Discussão sobre Nomenclatura"
description: "Debate histórico sobre o modelo de nomenclatura do I2P e por que esquemas globais ao estilo do DNS foram rejeitados"
slug: "naming"
layout: "single"
lastUpdated: "2025-02"
accurateFor: "historical"
reviewStatus: "needs-review"
---

> **Contexto:** Esta página arquiva debates de longa duração do período inicial do design do I2P. Ela explica por que o projeto privilegiou livros de endereços localmente confiáveis em vez de consultas no estilo DNS ou registros por votação majoritária. Para orientações de uso atuais, consulte a [documentação de nomenclatura](/docs/overview/naming/).

## Alternativas Descartadas

Os objetivos de segurança do I2P tornam inviáveis os esquemas de nomenclatura familiares:

- **Resolução no estilo DNS.** Qualquer resolvedor no caminho de resolução poderia forjar ou censurar respostas. Mesmo com DNSSEC, registradores comprometidos ou autoridades certificadoras permanecem um ponto único de falha. No I2P, os destinos *são* chaves públicas—sequestrar uma consulta comprometeria completamente uma identidade.
- **Nomeação baseada em votação.** Um adversário pode criar identidades ilimitadas (um ataque Sybil) e “vencer” votos para nomes populares. Mitigações por prova de trabalho aumentam o custo, mas introduzem uma sobrecarga pesada de coordenação.

Em vez disso, o I2P mantém deliberadamente o sistema de nomes acima da camada de transporte. A biblioteca de nomes incluída oferece uma interface de provedor de serviços para que esquemas alternativos possam coexistir — os usuários decidem em quais livros de endereços ou jump services (serviços de salto) confiam.

## Nomes Locais vs Globais (jrandom, 2005)

- Os nomes no I2P são **localmente exclusivos, porém legíveis por humanos**. O seu `boss.i2p` pode não corresponder ao `boss.i2p` de outra pessoa, e isso é intencional.
- Se um ator malicioso o enganasse para mudar o destino por trás de um nome, ele efetivamente sequestraria um serviço. Rejeitar a unicidade global previne esse tipo de ataque.
- Trate os nomes como favoritos/marcadores ou apelidos de IM (mensagens instantâneas)—você escolhe em quais destinos confiar assinando catálogos de endereços específicos ou adicionando chaves manualmente.

## Objeções Comuns e Respostas (zzz)

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
## Ideias de eficiência discutidas

- Forneça atualizações incrementais (apenas os destinos adicionados desde a última obtenção).
- Ofereça feeds suplementares (`recenthosts.cgi`) juntamente com arquivos completos de hosts.
- Explore ferramentas scriptáveis (por exemplo, `i2host.i2p`) para mesclar feeds ou filtrar por níveis de confiança.

## Principais pontos

- A segurança prevalece sobre o consenso global: livros de endereços mantidos localmente minimizam o risco de sequestro.
- Múltiplas abordagens de nomenclatura podem coexistir por meio da API de nomenclatura—os usuários decidem em que confiar.
- A nomenclatura global completamente descentralizada permanece um problema de pesquisa em aberto; os compromissos entre segurança, memorização humana e unicidade global ainda refletem o [triângulo de Zooko](https://zooko.com/distnames.html).

## Referências

- [Documentação de nomenclatura](/docs/overview/naming/)
- [“Nomes: Descentralizados, Seguros e Significativos para humanos: Escolha dois”, de Zooko](https://zooko.com/distnames.html)
- Exemplo de feed incremental: [stats.i2p/cgi-bin/newhosts.txt](http://stats.i2p/cgi-bin/newhosts.txt)
