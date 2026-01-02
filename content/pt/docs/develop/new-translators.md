---
title: "Guia para Novos Tradutores"
description: "Como contribuir com traduções para o site I2P e console do router usando Transifex ou métodos manuais"
slug: "new-translators"
lastUpdated: "2025-10"
type: docs
---

Quer ajudar a tornar o I2P acessível a mais pessoas ao redor do mundo? A tradução é uma das contribuições mais valiosas que você pode fazer ao projeto. Este guia irá orientá-lo na tradução do console do router.

## Métodos de Tradução

Existem duas maneiras de contribuir com traduções:

### Método 1: Transifex (Recomendado)

**Esta é a forma mais fácil de traduzir o I2P.** O Transifex fornece uma interface baseada na web que torna a tradução simples e acessível.

1. Inscreva-se em [Transifex](https://www.transifex.com/otf/I2P/)
2. Solicite participação na equipe de tradução do I2P
3. Comece a traduzir diretamente no seu navegador

Nenhum conhecimento técnico necessário - basta se inscrever e começar a traduzir!

### Método 2: Tradução Manual

Para tradutores que preferem trabalhar com git e arquivos locais, ou para idiomas ainda não configurados no Transifex.

**Requisitos:** - Familiaridade com controle de versão git - Editor de texto ou ferramenta de tradução (POEdit recomendado) - Ferramentas de linha de comando: git, gettext

**Configuração:** 1. Entre no [#i2p-dev no IRC](/contact/#irc) e apresente-se 2. Atualize o status da tradução na wiki (peça acesso no IRC) 3. Clone o repositório apropriado (veja as seções abaixo)

---

## Tradução do Console do Router

O console do router é a interface web que você vê ao executar o I2P. Traduzi-lo ajuda usuários que não se sentem confortáveis com inglês.

### Usando o Transifex (Recomendado)

1. Acesse [I2P no Transifex](https://www.transifex.com/otf/I2P/)
2. Selecione o projeto do router console
3. Escolha seu idioma
4. Comece a traduzir

### Tradução Manual do Console do Roteador

**Pré-requisitos:** - Iguais aos da tradução de website (git, gettext) - Chave GPG (para acesso de commit) - Acordo de desenvolvedor assinado

**Clone o repositório principal do I2P:**

```bash
git clone https://i2pgit.org/I2P_Developers/i2p.i2p.git
cd i2p.i2p
```
**Arquivos para traduzir:**

O console do roteador tem aproximadamente 15 arquivos que precisam de tradução:

1. **Arquivos de interface principais:**
   - `apps/routerconsole/locale/messages_*.po` - Mensagens principais do console
   - `apps/routerconsole/locale-news/messages_*.po` - Mensagens de notícias

2. **Arquivos de proxy:**
   - `apps/i2ptunnel/locale/messages_*.po` - Interface de configuração de tunnel

3. **Locales de aplicação:**
   - `apps/susidns/locale/messages_*.po` - Interface do catálogo de endereços
   - `apps/susimail/locale/messages_*.po` - Interface de e-mail
   - Outros diretórios de locales específicos de aplicações

4. **Arquivos de documentação:**
   - `installer/resources/readme/readme_*.html` - Leia-me da instalação
   - Arquivos de ajuda em vários aplicativos

**Fluxo de trabalho de tradução:**

```bash
# Update .po files from source
ant extractMessages

# Edit .po files with POEdit or text editor
poedit apps/routerconsole/locale/messages_es.po

# Build and test
ant updaters
# Install the update and check translations in the console
```
**Envie seu trabalho:** - Crie uma solicitação de mesclagem no [GitLab](https://i2pgit.org/I2P_Developers/i2p.i2p) - Ou compartilhe arquivos com a equipe de desenvolvimento no IRC

---

## Ferramentas de Tradução

### POEdit (Altamente Recomendado)

[POEdit](https://poedit.net/) é um editor especializado para arquivos de tradução .po.

**Recursos:** - Interface visual para trabalho de tradução - Mostra o contexto da tradução - Validação automática - Disponível para Windows, macOS e Linux

### Editores de Texto

Você também pode usar qualquer editor de texto: - VS Code (com extensões i18n) - Sublime Text - vim/emacs (para usuários de terminal)

### Verificações de Qualidade

Antes de submeter: 1. **Verifique a formatação:** Certifique-se de que os marcadores como `%s` e `{0}` permanecem inalterados 2. **Teste suas traduções:** Instale e execute o I2P para ver como ficam 3. **Consistência:** Mantenha a terminologia consistente entre os arquivos 4. **Comprimento:** Algumas strings têm restrições de espaço na interface

---

## Dicas para Tradutores

### Diretrizes Gerais

- **Mantenha a consistência:** Use as mesmas traduções para termos comuns em todo o documento
- **Preserve a formatação:** Mantenha tags HTML, marcadores de posição (`%s`, `{0}`) e quebras de linha
- **O contexto importa:** Leia o texto original em inglês cuidadosamente para entender o contexto
- **Faça perguntas:** Use IRC ou fóruns se algo não estiver claro

### Termos Comuns do I2P

Alguns termos devem permanecer em inglês ou ser transliterados cuidadosamente:

- **I2P** - Keep as is
- **eepsite** - Site I2P (website na rede I2P)
- **tunnel** - Caminho de conexão (evite terminologia do Tor como "circuito")
- **netDb** - Base de dados da rede
- **floodfill** - Tipo de router
- **destination** - Ponto final de endereço I2P

### Testando Suas Traduções

1. Compile o I2P com suas traduções
2. Altere o idioma nas configurações do console do router
3. Navegue por todas as páginas para verificar:
   - O texto se ajusta aos elementos da interface
   - Não há caracteres ilegíveis (problemas de codificação)
   - As traduções fazem sentido no contexto

---

## Perguntas Frequentes

### Por que o processo de tradução é tão complexo?

O processo usa controle de versão (git) e ferramentas de tradução padrão (arquivos .po) porque:

1. **Responsabilidade:** Rastrear quem alterou o quê e quando
2. **Qualidade:** Revisar alterações antes de entrarem em produção
3. **Consistência:** Manter formatação e estrutura adequadas dos arquivos
4. **Escalabilidade:** Gerenciar traduções em vários idiomas de forma eficiente
5. **Colaboração:** Vários tradutores podem trabalhar no mesmo idioma

### Preciso de habilidades de programação?

**Não!** Se você usar o Transifex, você só precisa de: - Fluência em inglês e no seu idioma de destino - Um navegador web - Habilidades básicas de informática

Para tradução manual, você precisará de conhecimento básico de linha de comando, mas nenhuma programação é necessária.

### Quanto tempo leva?

- **Console do roteador:** Aproximadamente 15-20 horas para todos os arquivos
- **Manutenção:** Algumas horas por mês para atualizar novas strings

### Várias pessoas podem trabalhar em um idioma?

Sim! A coordenação é fundamental: - Use o Transifex para coordenação automática - Para trabalho manual, comunique-se no canal IRC #i2p-dev - Divida o trabalho por seções ou arquivos

### E se meu idioma não estiver listado?

Solicite no Transifex ou entre em contato com a equipe no IRC. A equipe de desenvolvimento pode configurar um novo idioma rapidamente.

### Como posso testar minhas traduções antes de enviar?

- Compilar I2P a partir do código-fonte com suas traduções
- Instalar e executar localmente
- Alterar idioma nas configurações do console

---

## Obtendo Ajuda

### Suporte IRC

Junte-se ao [#i2p-dev no IRC](/contact/#irc) para: - Ajuda técnica com ferramentas de tradução - Perguntas sobre terminologia do I2P - Coordenação com outros tradutores - Suporte direto dos desenvolvedores

### Fóruns

- Discussões sobre tradução nos [Fóruns I2P](http://i2pforum.net/)
- Inside I2P: fórum de Tradução em zzz.i2p (requer router I2P)

### Documentação

- [Documentação do Transifex](https://docs.transifex.com/)
- [Documentação do POEdit](https://poedit.net/support)
- [Manual do gettext](https://www.gnu.org/software/gettext/manual/)

---

## Reconhecimento

Todos os tradutores são creditados em: - O console do router I2P (página Sobre) - Página de créditos do site - Histórico de commits do Git - Anúncios de lançamento

O seu trabalho ajuda diretamente pessoas ao redor do mundo a usar o I2P de forma segura e privada. Obrigado por contribuir!

---

## Próximos Passos

Pronto para começar a traduzir?

1. **Escolha seu método:**
   - Início rápido: [Inscreva-se no Transifex](https://www.transifex.com/otf/I2P/)
   - Abordagem manual: Participe do [#i2p-dev no IRC](/contact/#irc)

2. **Comece aos poucos:** Traduza algumas strings para se familiarizar com o processo

3. **Peça ajuda:** Não hesite em entrar em contato no IRC ou nos fóruns

**Obrigado por ajudar a tornar o I2P acessível a todos!**
