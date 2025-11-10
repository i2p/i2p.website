---
title: "Guia de Tradução"
description: "Ajude a tornar o I2P acessível a usuários em todo o mundo traduzindo o console do roteador e o site"
date: 2025-01-15
layout: "single"
type: "docs"
---

## Visão Geral

Ajude a tornar o I2P acessível a usuários ao redor do mundo traduzindo o console do roteador e o site do I2P para o seu idioma. A tradução é um processo contínuo, e contribuições de qualquer tamanho são valiosas.

## Plataforma de Tradução

Usamos **Transifex** para todas as traduções do I2P. Este é o método mais fácil e recomendado tanto para tradutores novos quanto experientes.

### Como Começar com o Transifex

1. **Crie uma conta** em [Transifex](https://www.transifex.com/)
2. **Participe do projeto I2P**: [I2P no Transifex](https://explore.transifex.com/otf/I2P/)
3. **Solicite para entrar** na equipe de tradução do seu idioma (ou solicite um novo idioma, se não estiver listado)
4. **Comece a traduzir** assim que for aprovado

### Por que Transifex?

- **Interface amigável** - Nenhum conhecimento técnico é necessário
- **Memória de tradução** - Sugere traduções com base em trabalhos anteriores
- **Colaboração** - Trabalhe com outros tradutores no seu idioma
- **Controle de qualidade** - Processo de revisão garante precisão
- **Atualizações automáticas** - Alterações sincronizam com a equipe de desenvolvimento

## O que Traduzir

### Console do Roteador (Prioridade)

O console do roteador I2P é a interface primária com a qual os usuários interagem ao usar o I2P. Traduzir isso tem o impacto mais imediato na experiência do usuário.

**Áreas principais para traduzir:**

- **Interface principal** - Navegação, menus, botões, mensagens de status
- **Páginas de configuração** - Descrições de configurações e opções
- **Documentação de ajuda** - Arquivos de ajuda embutidos e dicas
- **Notícias e atualizações** - Feed de notícias inicial mostrado aos usuários
- **Mensagens de erro** - Mensagens de erro e aviso voltadas para o usuário
- **Configurações de proxy** - Páginas de configuração de HTTP, SOCKS e túnel

Todas as traduções do console do roteador são gerenciadas através do Transifex no formato `.po` (gettext).

## Diretrizes de Tradução

### Estilo e Tom

- **Clareza e concisão** - O I2P lida com conceitos técnicos; mantenha as traduções simples
- **Terminologia consistente** - Use os mesmos termos ao longo do texto (verifique a memória de tradução)
- **Formal vs. informal** - Siga as convenções para o seu idioma
- **Preserve a formatação** - Mantenha os espaços reservados como `{0}`, `%s`, `<b>tags</b>` intactos

### Considerações Técnicas

- **Codificação** - Sempre use codificação UTF-8
- **Espaços reservados** - Não traduza espaços reservados de variáveis (`{0}`, `{1}`, `%s`, etc.)
- **HTML/Markdown** - Preserve as tags HTML e a formatação Markdown
- **Links** - Mantenha os URLs inalterados, a menos que haja uma versão localizada
- **Abreviações** - Considere se deve traduzir ou manter o original (por exemplo, "KB/s", "HTTP")

### Testando suas Traduções

Se você tiver acesso a um roteador I2P:

1. Baixe os arquivos de tradução mais recentes do Transifex
2. Coloque-os na sua instalação do I2P
3. Reinicie o console do roteador
4. Revise as traduções no contexto
5. Informe quaisquer problemas ou melhorias necessárias

## Obtendo Ajuda

### Suporte da Comunidade

- **Canal IRC**: `#i2p-dev` no IRC do I2P ou OFTC
- **Fórum**: Fóruns de desenvolvimento do I2P
- **Comentários no Transifex**: Faça perguntas diretamente nas cadeias de tradução

### Perguntas Comuns

**Q: Com que frequência devo traduzir?**
Traduza no seu próprio ritmo. Mesmo traduzir algumas cadeias ajuda. O projeto é contínuo.

**Q: O que fazer se meu idioma não estiver listado?**
Solicite um novo idioma no Transifex. Se houver demanda, a equipe o adicionará.

**Q: Posso traduzir sozinho ou preciso de uma equipe?**
Você pode começar sozinho. À medida que mais tradutores ingressarem no seu idioma, você poderá colaborar.

**Q: Como sei o que precisa de tradução?**
O Transifex mostra porcentagens de conclusão e destaca cadeias não traduzidas.

**Q: O que fazer se eu discordar de uma tradução existente?**
Sugira melhorias no Transifex. Os revisores avaliarão as alterações.

## Avançado: Tradução Manual (Opcional)

Para tradutores experientes que desejam acesso direto aos arquivos de origem:

### Requisitos

- **Git** - Sistema de controle de versão
- **POEdit** ou editor de texto - Para editar arquivos `.po`
- **Conhecimento básico de linha de comando**

### Processo

1. **Clone o repositório**:
   ```bash
   git clone https://i2pgit.org/i2p-hackers/i2p.i2p.git
   ```

2. **Encontre os arquivos de tradução**:
   - Console do roteador: `apps/routerconsole/locale/`
   - Procure `messages_xx.po` (onde `xx` é o código do seu idioma)

3. **Edição de traduções**:
   - Use POEdit ou um editor de texto
   - Salve com codificação UTF-8

4. **Teste localmente** (se tiver o I2P instalado)

5. **Envie as alterações**:
   - Crie uma solicitação de mesclagem no [I2P Git](https://i2pgit.org/)
   - Ou compartilhe seu arquivo `.po` com a equipe de desenvolvimento

**Nota**: A maioria dos tradutores deve usar o Transifex. A tradução manual é apenas para aqueles que se sentem confortáveis com Git e fluxos de trabalho de desenvolvimento.

## Obrigado

Cada tradução ajuda a tornar o I2P mais acessível a usuários em todo o mundo. Se você traduzir algumas cadeias ou seções inteiras, sua contribuição faz uma diferença real ao ajudar as pessoas a protegerem sua privacidade online.

**Pronto para começar?** [Participe do I2P no Transifex →](https://explore.transifex.com/otf/I2P/)
