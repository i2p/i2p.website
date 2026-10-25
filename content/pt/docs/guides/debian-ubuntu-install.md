---
title: "Instalando o I2P no Debian e Ubuntu"
aliases:
  - "/pt/debian"
  - "/pt/debian/"
description: "Guia completo para instalar o I2P no Debian, Ubuntu e seus derivados usando repositórios oficiais"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

O projeto I2P mantém pacotes oficiais para Debian, Ubuntu e suas distribuições derivadas. Este guia fornece instruções abrangentes para instalar o I2P usando nossos repositórios oficiais.

---

<div class="coming-soon-section">

## 🚀 Beta: Automatic Installation (Experimental)

**For advanced users who want a quick automated installation:**

This one-liner will automatically detect your distribution and install I2P. **Use with caution** - review the [installation script](https://i2p.net/installlinux.sh) before running.

```bash
curl -fsSL https://i2p.net/installlinux.sh | sudo bash
```

**What this does:**
- Detects your Linux distribution (Ubuntu/Debian)
- Adds the appropriate I2P repository
- Installs GPG keys and required packages
- Installs I2P automatically

⚠️ **This is a beta feature.** If you prefer manual installation or want to understand each step, use the manual installation methods below.

</div>
IMPORTANTE:  NÃO faça perguntas, forneça explicações ou adicione qualquer comentário. Mesmo que o texto seja apenas um cabeçalho ou pareça incompleto, traduza-o como está.

## Plataformas Suportadas

---

- **Ubuntu** 18.04 (Bionic) e mais recente
- **Linux Mint** 19 (Tara) e mais recente
- **Debian** Buster (10) e mais recente
- **Knoppix**
- Outras distribuições baseadas em Debian (LMDE, ParrotOS, Kali Linux, etc.)

IMPORTANTE:  NÃO faça perguntas, forneça explicações ou adicione qualquer comentário. Mesmo que o texto seja apenas um cabeçalho ou pareça incompleto, traduza-o como está.

Os pacotes Debian são compatíveis com:

## Métodos de Instalação

**Arquiteturas suportadas**: amd64, i386, armhf, arm64, powerpc, ppc64el, s390x

- **Opção 1**: [Ubuntu e derivados](#ubuntu-installation) (Linux Mint, elementary OS, Pop!_OS, etc.)
- **Opção 2**: [Debian e distribuições baseadas em Debian](#debian-installation) (incluindo LMDE, Kali, ParrotOS)

Os pacotes I2P podem funcionar em outros sistemas baseados em Debian não explicitamente listados acima. Se você encontrar problemas, por favor [reporte-os em nosso GitLab](https://i2pgit.org/I2P_Developers/i2p.i2p/).

## Instalação no Ubuntu

Escolha o método de instalação que corresponde à sua distribuição:

### Method 1: Command Line Installation (Recommended)

---

IMPORTANTE:  NÃO faça perguntas, forneça explicações ou adicione qualquer comentário. Mesmo que o texto seja apenas um cabeçalho ou pareça incompleto, traduza-o como está.

Ubuntu e seus derivados oficiais (Linux Mint, elementary OS, Trisquel, etc.) podem usar o PPA (Personal Package Archive) do I2P para instalação fácil e atualizações automáticas.

```bash
sudo apt-add-repository ppa:i2p-maintainers/i2p
```
Este é o método mais rápido e confiável para instalar o I2P em sistemas baseados em Ubuntu.

**Passo 1: Adicionar o PPA do I2P**

Abra um terminal e execute:

```bash
sudo apt-get update
```
Este comando adiciona o PPA do I2P a `/etc/apt/sources.list.d/` e importa automaticamente a chave GPG que assina o repositório. A assinatura GPG garante que os pacotes não foram adulterados desde que foram compilados.

**Passo 2: Atualizar a lista de pacotes**

Atualize a base de dados de pacotes do seu sistema para incluir o novo PPA:

```bash
sudo apt-get install i2p
```
Isso recupera as informações mais recentes dos pacotes de todos os repositórios habilitados, incluindo o PPA do I2P que você acabou de adicionar.

### Method 2: Using the Software Center GUI

**Passo 3: Instalar o I2P**

Agora instale o I2P:

É isso! Pule para a seção [Configuração Pós-Instalação](#post-installation-configuration) para aprender como iniciar e configurar o I2P.

Se você preferir uma interface gráfica, pode adicionar o PPA usando a Central de Programas do Ubuntu.

**Passo 1: Abrir Software e Atualizações**

Inicie "Software e Atualizações" a partir do seu menu de aplicativos.

![Menu do Centro de Software](/images/guides/debian/software-center-menu.png)

**Passo 2: Navegue para Outros Programas**

Selecione a aba "Outro Software" e clique no botão "Adicionar" na parte inferior para configurar um novo PPA.

```
ppa:i2p-maintainers/i2p
```
![Aba Outro Software](/images/guides/debian/software-center-addother.png)

**Passo 3: Adicionar o PPA do I2P**

Na caixa de diálogo PPA, insira:

![Diálogo Adicionar PPA](/images/guides/debian/software-center-ppatool.png)

**Passo 4: Recarregar informações do repositório**

Clique no botão "Reload" para baixar as informações atualizadas do repositório.

![Botão Recarregar](/images/guides/debian/software-center-reload.png)

**Passo 5: Instalar o I2P**

Abra a aplicação "Software" do seu menu de aplicações, procure por "i2p" e clique em Instalar.

## Debian Installation

![Aplicação de Software](/images/guides/debian/software-center-software.png)

### Important Notice

Assim que a instalação for concluída, prossiga para [Configuração Pós-Instalação](#post-installation-configuration).

### Prerequisites

---

### Método 1: Instalação por Linha de Comando (Recomendado)

Debian e suas distribuições derivadas (LMDE, Kali Linux, ParrotOS, Knoppix, etc.) devem usar o repositório oficial I2P Debian em `deb.i2p.net`.

**Nossos repositórios antigos em `deb.i2p2.de` e `deb.i2p2.no` estão descontinuados.** Se você está usando esses repositórios legados, siga as instruções abaixo para migrar para o novo repositório em `deb.i2p.net`.

```bash
sudo apt-get update
sudo apt-get install apt-transport-https lsb-release curl
```
Todos os passos abaixo requerem acesso root. Alterne para o usuário root com `su`, ou adicione o prefixo `sudo` a cada comando.

**Passo 1: Instalar os pacotes necessários**

Certifique-se de ter as ferramentas necessárias instaladas:

```bash
cat /etc/debian_version
```
Estes pacotes permitem acesso seguro ao repositório via HTTPS, detecção de distribuição e downloads de arquivos.

**Passo 2: Adicionar o repositório I2P**

```bash
echo "deb [signed-by=/usr/share/keyrings/i2p-archive-keyring.gpg] https://deb.i2p.net/ $(lsb_release -sc) main" \
  | sudo tee /etc/apt/sources.list.d/i2p.list
```
O comando que você usa depende da sua versão do Debian. Primeiro, determine qual versão você está executando:

```bash
echo "deb [signed-by=/usr/share/keyrings/i2p-archive-keyring.gpg] https://deb.i2p.net/ $(dpkg --status tzdata | grep Provides | cut -f2 -d'-') main" \
  | sudo tee /etc/apt/sources.list.d/i2p.list
```
Faça referência cruzada com as [informações de lançamento do Debian](https://wiki.debian.org/LTS/) para identificar o codinome da sua distribuição (ex.: Bookworm, Bullseye, Buster).

```bash
echo "deb https://deb.i2p.net/ $(lsb_release -sc) main" \
  | sudo tee /etc/apt/sources.list.d/i2p.list
```
**Para Debian Bullseye (11) ou mais recente:**

```bash
echo "deb https://deb.i2p.net/ $(dpkg --status tzdata | grep Provides | cut -f2 -d'-') main" \
  | sudo tee /etc/apt/sources.list.d/i2p.list
```
**Para derivados do Debian (LMDE, Kali, ParrotOS, etc.) no Bullseye-equivalente ou mais recente:**

```bash
curl -o i2p-archive-keyring.gpg https://i2p.net/i2p-archive-keyring.gpg
```
**Para Debian Buster (10) ou mais antigo:**

**Para derivados do Debian equivalentes ao Buster ou mais antigos:**

```bash
gpg --keyid-format long --import --import-options show-only --with-fingerprint i2p-archive-keyring.gpg
```
**Passo 3: Baixar a chave de assinatura do repositório**

```
7840 E761 0F28 B904 7535  49D7 67EC E560 5BCF 1346
```
**Passo 4: Verificar a impressão digital da chave**

Antes de confiar na chave, verifique se sua impressão digital corresponde à chave de assinatura oficial do I2P:

**Verifique se a saída mostra esta impressão digital:**

```bash
sudo cp i2p-archive-keyring.gpg /usr/share/keyrings
```
⚠️ **Não prossiga se a impressão digital não corresponder.** Isso pode indicar um download comprometido.

```bash
sudo ln -sf /usr/share/keyrings/i2p-archive-keyring.gpg /etc/apt/trusted.gpg.d/i2p-archive-keyring.gpg
```
**Passo 5: Instalar a chave do repositório**

Copie o keyring verificado para o diretório de keyrings do sistema:

```bash
sudo apt-get update
```
**Apenas para Debian Buster ou versões anteriores**, você também precisa criar um link simbólico:

**Passo 6: Atualizar listas de pacotes**

```bash
sudo apt-get install i2p i2p-keyring
```
Atualize a base de dados de pacotes do seu sistema para incluir o repositório I2P:

**Passo 7: Instalar o I2P**

## Post-Installation Configuration

Instale tanto o router I2P quanto o pacote keyring (que garante que você receberá futuras atualizações de chaves):

### Método 2: Usando a Interface Gráfica da Central de Software

Ótimo! O I2P está agora instalado. Continue para a seção [Configuração Pós-Instalação](#post-installation-configuration).

#### Option 1: On-Demand (Basic)

---

```bash
i2prouter start
```
IMPORTANTE:  NÃO faça perguntas, forneça explicações ou adicione qualquer comentário. Mesmo que o texto seja apenas um cabeçalho ou pareça incompleto, traduza-o como está.

Após instalar o I2P, você precisará iniciar o router e realizar algumas configurações iniciais.

```bash
i2prouter stop
```
#### Option 2: On-Demand (Without Java Service Wrapper)

Os pacotes I2P fornecem três formas de executar o router I2P:

```bash
i2prouter-nowrapper
```
Inicie o I2P manualmente quando necessário usando o script `i2prouter`:

#### Option 3: System Service (Recommended)

**Importante**: **Não** use `sudo` ou execute isso como root! O I2P deve ser executado como seu usuário regular.

```bash
sudo dpkg-reconfigure i2p
```
Para parar o I2P:

Se você estiver em um sistema não-x86 ou o Java Service Wrapper não funcionar na sua plataforma, use:

### Initial Router Configuration

Novamente, **não** use `sudo` ou execute como root.

#### 1. Configure NAT/Firewall

Para a melhor experiência, configure o I2P para iniciar automaticamente quando o sistema inicializar, mesmo antes do login:

1. Abra o [Console do Router I2P](http://127.0.0.1:7657/)
2. Navegue até a [página de Configuração de Rede](http://127.0.0.1:7657/confignet)
3. Anote os números de porta listados (geralmente portas aleatórias entre 9000-31000)
4. Encaminhe essas portas UDP e TCP no seu roteador/firewall

Isso abre uma caixa de diálogo de configuração. Selecione "Sim" para ativar o I2P como um serviço do sistema.

#### 2. Adjust Bandwidth Settings

**Este é o método recomendado** porque: - O I2P inicia automaticamente na inicialização - Seu router mantém melhor integração com a rede - Você contribui para a estabilidade da rede - O I2P está disponível imediatamente quando você precisar

1. Visite a [página de Configuração](http://127.0.0.1:7657/config.jsp)
2. Encontre a seção de configurações de largura de banda
3. Os padrões são 96 KB/s de download / 40 KB/s de upload
4. Aumente esses valores se você tiver internet mais rápida (por exemplo, 250 KB/s de download / 100 KB/s de upload para uma conexão banda larga típica)

Após iniciar o I2P pela primeira vez, levará alguns minutos para integrar na rede. Enquanto isso, configure estas definições essenciais:

#### 3. Configure Your Browser

Para desempenho ideal e participação na rede, encaminhe as portas I2P através do seu NAT/firewall:

Se você precisar de ajuda com encaminhamento de portas, [portforward.com](https://portforward.com) fornece guias específicos para roteadores.

As configurações padrão de largura de banda são conservadoras. Ajuste-as com base na sua conexão de internet:

## Instalação no Debian

### Aviso Importante

- Certifique-se de que não está a executar o I2P como root: `ps aux | grep i2p`
- Verifique os logs: `tail -f ~/.i2p/wrapper.log`
- Verifique se o Java está instalado: `java -version`

### Pré-requisitos

**Nota**: Definir limites mais altos ajuda a rede e melhora o seu próprio desempenho.

1. Faça o download novamente e verifique a impressão digital da chave (Passos 3-4 acima)
2. Certifique-se de que o arquivo keyring possui as permissões corretas: `sudo chmod 644 /usr/share/keyrings/i2p-archive-keyring.gpg`

### Passos de Instalação

Para aceder a sites I2P (eepsites) e serviços, configure o seu navegador para utilizar o proxy HTTP do I2P:

1. Verifique se o repositório está configurado: `cat /etc/apt/sources.list.d/i2p.list`
2. Atualize as listas de pacotes: `sudo apt-get update`
3. Verifique se há atualizações do I2P: `sudo apt-get upgrade`

### Migrating from old repositories

Consulte nosso [Guia de Configuração de Navegador](/docs/guides/browser-config) para instruções detalhadas de configuração para Firefox, Chrome e outros navegadores.

1. Remova o repositório antigo: `sudo rm /etc/apt/sources.list.d/i2p.list`
2. Siga os passos de [Instalação no Debian](#debian-installation) acima
3. Atualize: `sudo apt-get update && sudo apt-get install i2p i2p-keyring`

---

## Next Steps

Se você receber erros de chave GPG durante a instalação:

- [Configure seu navegador](/docs/guides/browser-config) para acessar sites I2P
- Explore o [console do router I2P](http://127.0.0.1:7657/) para monitorar seu router
- Conheça as [aplicações I2P](/docs/applications/) que você pode usar
- Leia sobre [como o I2P funciona](/docs/overview/tech-intro) para entender a rede

Se o I2P não estiver recebendo atualizações:
