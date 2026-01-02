---
title: "Configuração do Navegador Web"
description: "Configure navegadores populares para usar os proxies HTTP/HTTPS do I2P no desktop e Android"
slug: "browser-config"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
type: docs
---

Este guia mostra como configurar navegadores comuns para enviar tráfego através do proxy HTTP integrado do I2P. Ele cobre os navegadores Safari, Firefox e Chrome/Chromium com instruções detalhadas passo a passo.

**Notas Importantes**:

- O proxy HTTP padrão do I2P escuta em `127.0.0.1:4444`.
- O I2P protege o tráfego dentro da rede I2P (sites .i2p).
- Certifique-se de que seu router I2P está em execução antes de configurar seu navegador.

## Safari (macOS)

O Safari utiliza as configurações de proxy do sistema no macOS.

### Step 1: Open Network Settings

1. Abra o **Safari** e vá em **Safari → Ajustes** (ou **Preferências**)
2. Clique na aba **Avançado**
3. Na seção **Proxies**, clique em **Alterar Configurações...**

Isso abrirá as Configurações de Rede do Sistema do seu Mac.

![Configurações Avançadas do Safari](/images/guides/browser-config/accessi2p_1.png)

### Passo 1: Abrir as Configurações de Rede

1. Nas configurações de Rede, marque a caixa para **Proxy da Web (HTTP)**
2. Insira o seguinte:
   - **Servidor Proxy da Web**: `127.0.0.1`
   - **Porta**: `4444`
3. Clique em **OK** para salvar suas configurações

![Configuração de Proxy do Safari](/images/guides/browser-config/accessi2p_2.png)

Agora você pode navegar em sites `.i2p` no Safari!

**Nota**: Estas configurações de proxy afetarão todas as aplicações que usam os proxies do sistema macOS. Considere criar uma conta de usuário separada ou usar um navegador diferente exclusivamente para I2P se quiser isolar a navegação I2P.

## Firefox (Desktop)

O Firefox possui suas próprias configurações de proxy independentes do sistema, tornando-o ideal para navegação dedicada no I2P.

### Passo 2: Configurar o Proxy HTTP

1. Clique no **botão de menu** (☰) no canto superior direito
2. Selecione **Configurações**

![Configurações do Firefox](/images/guides/browser-config/accessi2p_3.png)

### Step 2: Find Proxy Settings

1. Na caixa de pesquisa de Configurações, digite **"proxy"**
2. Role até **Configurações de Rede**
3. Clique no botão **Configurações...**

![Pesquisa de Proxy do Firefox](/images/guides/browser-config/accessi2p_4.png)

### Passo 1: Abrir Configurações

1. Selecione **Configuração manual de proxy**
2. Insira o seguinte:
   - **Proxy HTTP**: `127.0.0.1` **Porta**: `4444`
3. Deixe o campo **Host SOCKS** vazio (a menos que você especificamente precise de proxy SOCKS)
4. Marque **Usar proxy DNS ao usar SOCKS** apenas se estiver usando proxy SOCKS
5. Clique em **OK** para salvar

![Configuração Manual de Proxy do Firefox](/images/guides/browser-config/accessi2p_5.png)

Agora você pode navegar em sites `.i2p` no Firefox!

**Dica**: Considere criar um perfil separado do Firefox dedicado à navegação no I2P. Isso mantém sua navegação no I2P isolada da navegação regular. Para criar um perfil, digite `about:profiles` na barra de endereços do Firefox.

## Chrome / Chromium (Desktop)

Chrome e navegadores baseados em Chromium (Brave, Edge, etc.) normalmente utilizam as configurações de proxy do sistema no Windows e macOS. Este guia mostra a configuração no Windows.

### Passo 2: Encontrar as Configurações de Proxy

1. Clique no **menu de três pontos** (⋮) no canto superior direito
2. Selecione **Configurações**

![Configurações do Chrome](/images/guides/browser-config/accessi2p_6.png)

### Passo 3: Configurar Proxy Manual

1. Na caixa de pesquisa de Configurações, digite **"proxy"**
2. Clique em **Abrir as configurações de proxy do seu computador**

![Chrome Proxy Search](/images/guides/browser-config/accessi2p_7.png)

### Step 3: Open Manual Proxy Setup

Isso abrirá as configurações de Rede e Internet do Windows.

1. Role para baixo até **Configuração manual de proxy**
2. Clique em **Configurar**

![Configuração de Proxy no Windows](/images/guides/browser-config/accessi2p_8.png)

### Passo 1: Abrir as Configurações do Chrome

1. Alterne **Usar um servidor proxy** para **Ativado**
2. Insira o seguinte:
   - **Endereço IP do proxy**: `127.0.0.1`
   - **Porta**: `4444`
3. Opcionalmente, adicione exceções em **"Não usar o servidor proxy para endereços começando com"** (por exemplo, `localhost;127.*`)
4. Clique em **Salvar**

![Configuração de Proxy do Chrome](/images/guides/browser-config/accessi2p_9.png)

Agora você pode navegar em sites `.i2p` no Chrome!

**Nota**: Estas configurações afetam todos os navegadores baseados em Chromium e algumas outras aplicações no Windows. Para evitar isso, considere usar o Firefox com um perfil I2P dedicado.

### Passo 2: Abrir as Configurações de Proxy

No Linux, você pode iniciar o Chrome/Chromium com flags de proxy para evitar alterar as configurações do sistema:

```bash
chromium \
  --proxy-server="http=127.0.0.1:4444 \
  --proxy-bypass-list="<-loopback>"
```
Ou crie um script de atalho para a área de trabalho:

```bash
#!/bin/bash
chromium --proxy-server="http=127.0.0.1:4444" --user-data-dir="$HOME/.config/chromium-i2p"
```
A flag `--user-data-dir` cria um perfil separado do Chrome para navegação I2P.

## Firefox (Desktop)

As versões modernas "Fenix" do Firefox limitam about:config e extensões por padrão. IceRaven é um fork do Firefox que habilita um conjunto curado de extensões, tornando a configuração de proxy simples.

Configuração baseada em extensão (IceRaven):

1) Se você já usa o IceRaven, considere limpar o histórico de navegação primeiro (Menu → Histórico → Excluir Histórico). 2) Abra Menu → Complementos → Gerenciador de Complementos. 3) Instale a extensão "I2P Proxy for Android and Other Systems". 4) O navegador agora fará proxy através do I2P.

Esta extensão também funciona em navegadores baseados no Firefox pré-Fenix se instalada do [AMO](https://addons.mozilla.org/en-US/android/addon/i2p-proxy/).

Habilitar o suporte extenso a extensões no Firefox Nightly requer um processo separado [documentado pela Mozilla](https://blog.mozilla.org/addons/2020/09/29/expanded-extension-support-in-firefox-for-android-nightly/).

## Internet Explorer / Windows System Proxy

No Windows, a caixa de diálogo de proxy do sistema aplica-se ao IE e pode ser usada por navegadores baseados em Chromium quando herdam as configurações do sistema.

1) Abra "Configurações de Rede e Internet" → "Proxy". 2) Ative "Usar um servidor proxy para sua LAN". 3) Defina o endereço `127.0.0.1`, porta `4444` para HTTP. 4) Opcionalmente marque "Ignorar servidor proxy para endereços locais".
