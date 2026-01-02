---
title: "Clientes I2P Alternativos"
description: "Implementações de clientes I2P mantidas pela comunidade (atualizado para 2025)"
slug: "alternative-clients"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

A implementação principal do cliente I2P usa **Java**. Se você não pode ou prefere não usar Java em um sistema específico, existem implementações alternativas de cliente I2P desenvolvidas e mantidas por membros da comunidade. Esses programas fornecem a mesma funcionalidade principal usando diferentes linguagens de programação ou abordagens.

---

## Tabela de Comparação

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Client</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Language</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Maturity</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Actively Maintained</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Suitable For</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Java I2P</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Java</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Stable</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">✅ Yes (official)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">General users</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Standard full router; includes console, plugins, and tools</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>i2pd</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">C++</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Stable</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">✅ Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Low-resource systems, servers</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Lightweight, fully compatible with Java I2P, includes web console</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Go-I2P</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Go</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Experimental</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">⚙️ In development</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Developers, testing</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Early-stage Go implementation; not yet production ready</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>I2P+</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Java</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Stable (fork)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">✅ Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Advanced users</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Enhanced Java I2P fork with UI and performance improvements</td>
    </tr>
  </tbody>
</table>
---

## i2pd (C++)

**Website:** [https://i2pd.website](https://i2pd.website)

**Descrição:** i2pd (o *I2P Daemon*) é um cliente I2P completo implementado em C++. Ele está estável para uso em produção há muitos anos (desde aproximadamente 2016) e é mantido ativamente pela comunidade. O i2pd implementa completamente os protocolos de rede e APIs do I2P, tornando-o totalmente compatível com a rede I2P Java. Este router em C++ é frequentemente usado como uma alternativa leve em sistemas onde o ambiente de execução Java não está disponível ou não é desejado. O i2pd inclui um console baseado na web integrado para configuração e monitoramento. É multiplataforma e está disponível em muitos formatos de pacote — existe até uma versão Android do i2pd disponível (por exemplo, via F-Droid).

---

## Go-I2P (Go)

**Repositório:** [https://github.com/go-i2p/go-i2p](https://github.com/go-i2p/go-i2p)

**Descrição:** Go-I2P é um cliente I2P escrito na linguagem de programação Go. É uma implementação independente do router I2P, com o objetivo de aproveitar a eficiência e portabilidade do Go. O projeto está em desenvolvimento ativo, mas ainda está em estágio inicial e não possui todos os recursos completos. Em 2025, o Go-I2P é considerado experimental — está sendo desenvolvido ativamente por programadores da comunidade, mas não é recomendado para uso em produção até que amadureça mais. O objetivo do Go-I2P é fornecer um router I2P moderno e leve com compatibilidade total com a rede I2P assim que o desenvolvimento estiver completo.

---

## I2P+ (fork Java)

**Website:** [https://i2pplus.github.io](https://i2pplus.github.io)

**Descrição:** I2P+ é um fork mantido pela comunidade do cliente Java I2P padrão. Não é uma reimplementação em uma nova linguagem, mas sim uma versão aprimorada do router Java com recursos adicionais e otimizações. O I2P+ concentra-se em oferecer uma experiência de usuário melhorada e melhor desempenho, mantendo total compatibilidade com a rede I2P oficial. Ele introduz uma interface de console web renovada, opções de configuração mais amigáveis e várias otimizações (por exemplo, desempenho aprimorado de torrent e melhor gerenciamento de peers da rede, especialmente para routers atrás de firewalls). O I2P+ requer um ambiente Java assim como o software I2P oficial, portanto não é uma solução para ambientes não-Java. No entanto, para usuários que possuem Java e desejam uma versão alternativa com capacidades extras, o I2P+ oferece uma opção atraente. Este fork é mantido atualizado com os lançamentos upstream do I2P (com sua numeração de versão incluindo um "+") e pode ser obtido no site do projeto.
