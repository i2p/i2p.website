---
title: "Guia do Novo Desenvolvedor"
description: "Como começar a contribuir para o I2P: materiais de estudo, código-fonte, compilação, ideias, publicação, comunidade, traduções e ferramentas"
slug: "new-developers"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
type: docs
notes: atualizar parte da tradução
---

Então você quer começar a trabalhar no I2P? Ótimo! Aqui está um guia rápido para começar a contribuir com o site ou o software, fazer desenvolvimento ou criar traduções.

Ainda não está pronto para programar? Tente [envolver-se](/get-involved/) primeiro.

## Conheça Java

O router I2P e suas aplicações integradas usam Java como linguagem principal de desenvolvimento. Se você não tem experiência com Java, pode sempre consultar [Thinking in Java](https://chenweixiang.github.io/docs/Thinking_in_Java_4th_Edition.pdf)

Estude a introdução "como", outros documentos "como", a introdução técnica e documentos associados:

- Como introdução: [Introdução ao I2P](/docs/overview/intro/)
- Central de documentação: [Documentação](/docs/)
- Introdução técnica: [Introdução Técnica](/docs/overview/tech-intro/)

Estes recursos fornecerão uma boa visão geral de como o I2P é estruturado e das diferentes funcionalidades que ele oferece.

## Obtendo o Código do I2P

Para desenvolvimento no router I2P ou nas aplicações incorporadas, você precisa obter o código-fonte.

### Nossa forma atual: Git

I2P tem serviços Git oficiais e aceita contribuições via Git em nosso próprio GitLab:

- Dentro do I2P: <http://git.idk.i2p>
- Fora do I2P: <https://i2pgit.org>

Clone o repositório principal:

```
git clone https://i2pgit.org/I2P_Developers/i2p.i2p.git
```
Um espelho somente leitura também está disponível no GitHub:

- Espelho no GitHub: [github.com/i2p/i2p.i2p](https://github.com/i2p/i2p.i2p)

```
git clone https://github.com/i2p/i2p.i2p.git
```
## Compilando I2P

Para compilar o código, você precisa do Sun/Oracle Java Development Kit 6 ou superior, ou JDK equivalente (Sun/Oracle JDK 6 fortemente recomendado) e Apache Ant versão 1.7.0 ou superior. Se você estiver trabalhando no código principal do I2P, entre no diretório `i2p.i2p` e execute `ant` para ver as opções de compilação.

Para compilar ou trabalhar em traduções do console, você precisa das ferramentas `xgettext`, `msgfmt` e `msgmerge` do pacote GNU gettext.

Para o desenvolvimento de novas aplicações, consulte o [guia de desenvolvimento de aplicações](/docs/develop/applications/).

## Ideias de Desenvolvimento

Veja a lista TODO do projeto ou a lista de issues no GitLab para ideias:

- Problemas do GitLab: [i2pgit.org/I2P_Developers/i2p.i2p/issues](https://i2pgit.org/I2P_Developers/i2p.i2p/issues)

## Disponibilizando os Resultados

Veja o final da página de licenças para os requisitos de privilégio de commit. Você precisa destes para colocar código no `i2p.i2p` (não é necessário para o site!).

- [Página de licenças](/docs/develop/licenses#commit)

## Conheça-nos!

Os desenvolvedores estão disponíveis no IRC. Eles podem ser contactados em várias redes e nas redes internas do I2P. O local habitual é o `#i2p-dev`. Entre no canal e diga olá! Também temos [diretrizes adicionais para desenvolvedores regulares](/docs/develop/dev-guidelines/).

## Traduções

Tradutores do site e do console do roteador: Consulte o [Guia para Novos Tradutores](/docs/develop/new-translators/) para os próximos passos.

## Ferramentas

I2P é um software de código aberto que é desenvolvido principalmente usando ferramentas de código aberto. O projeto I2P adquiriu recentemente uma licença para o YourKit Java Profiler. Projetos de código aberto são elegíveis para receber uma licença gratuita desde que o YourKit seja referenciado no site do projeto. Entre em contato se você estiver interessado em fazer profiling da base de código do I2P.

A YourKit está gentilmente apoiando projetos de código aberto com seus profilers completos. YourKit, LLC é a criadora de ferramentas inovadoras e inteligentes para criação de perfis de aplicações Java e .NET. Dê uma olhada nos produtos de software líderes da YourKit:

- [YourKit Java Profiler](http://www.yourkit.com/java/profiler/index.jsp)
- [YourKit .NET Profiler](http://www.yourkit.com/.net/profiler/index.jsp)
