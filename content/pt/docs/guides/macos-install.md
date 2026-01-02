---
title: "Instalando o I2P no macOS (O Caminho Longo)"
description: "Guia passo a passo para instalar manualmente o I2P e suas dependências no macOS"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

## O Que Você Vai Precisar

- Um Mac executando macOS 10.14 (Mojave) ou posterior
- Acesso de administrador para instalar aplicativos
- Cerca de 15-20 minutos de tempo
- Conexão à internet para baixar os instaladores

## Visão Geral

Este processo de instalação tem quatro etapas principais:

1. **Instalar Java** - Baixe e instale o Oracle Java Runtime Environment
2. **Instalar I2P** - Baixe e execute o instalador do I2P
3. **Configurar Aplicativo I2P** - Configure o launcher e adicione ao seu dock
4. **Configurar Largura de Banda do I2P** - Execute o assistente de configuração para otimizar sua conexão

## Parte Um: Instalar Java

O I2P requer Java para funcionar. Se você já tem o Java 8 ou posterior instalado, pode [pular para a Parte Dois](#part-two-download-and-install-i2p).

### Step 1: Download Java

Visite a [página de download do Oracle Java](https://www.oracle.com/java/technologies/downloads/) e baixe o instalador para macOS do Java 8 ou posterior.

![Baixar Oracle Java para macOS](/images/guides/macos-install/0-jre.png)

### Step 2: Run the Installer

Localize o arquivo `.dmg` baixado na sua pasta Downloads e clique duas vezes para abri-lo.

![Abrir o instalador do Java](/images/guides/macos-install/1-jre.png)

### Step 3: Allow Installation

O macOS pode exibir um aviso de segurança porque o instalador é de um desenvolvedor identificado. Clique em **Abrir** para continuar.

![Conceda permissão ao instalador para prosseguir](/images/guides/macos-install/2-jre.png)

### Passo 1: Baixar o Java

Clique em **Install** para iniciar o processo de instalação do Java.

![Iniciar a instalação do Java](/images/guides/macos-install/3-jre.png)

### Passo 2: Execute o Instalador

O instalador copiará os arquivos e configurará o Java no seu sistema. Isso geralmente leva de 1 a 2 minutos.

![Aguarde a conclusão do instalador](/images/guides/macos-install/4-jre.png)

### Passo 3: Permitir a Instalação

Quando você ver a mensagem de sucesso, o Java está instalado! Clique em **Fechar** para finalizar.

![Instalação do Java concluída](/images/guides/macos-install/5-jre.png)

## Part Two: Download and Install I2P

Agora que o Java está instalado, você pode instalar o router I2P.

### Passo 4: Instalar o Java

Visite a [página de Downloads](/downloads/) e baixe o instalador **I2P para Unix/Linux/BSD/Solaris** (o arquivo `.jar`).

![Baixar instalador I2P](/images/guides/macos-install/0-i2p.png)

### Passo 5: Aguarde a Instalação

Clique duas vezes no arquivo `i2pinstall_X.X.X.jar` baixado. O instalador será iniciado e solicitará que você selecione seu idioma preferido.

![Selecione o seu idioma](/images/guides/macos-install/1-i2p.png)

### Passo 6: Instalação Concluída

Leia a mensagem de boas-vindas e clique em **Next** para continuar.

![Introdução do instalador](/images/guides/macos-install/2-i2p.png)

### Step 4: Important Notice

O instalador exibirá um aviso importante sobre atualizações. As atualizações do I2P são **assinadas ponta a ponta** e verificadas, embora o próprio instalador não seja assinado. Clique em **Próximo**.

![Aviso importante sobre atualizações](/images/guides/macos-install/3-i2p.png)

### Passo 1: Baixar o I2P

Leia o acordo de licença do I2P (licença estilo BSD). Clique em **Próximo** para aceitar.

![Contrato de licença](/images/guides/macos-install/4-i2p.png)

### Passo 2: Execute o Instalador

Escolha onde instalar o I2P. A localização padrão (`/Applications/i2p`) é recomendada. Clique em **Próximo**.

![Selecionar diretório de instalação](/images/guides/macos-install/5-i2p.png)

### Passo 3: Tela de Boas-Vindas

Deixe todos os componentes selecionados para uma instalação completa. Clique em **Next**.

![Selecionar componentes para instalar](/images/guides/macos-install/6-i2p.png)

### Passo 4: Aviso Importante

Revise suas escolhas e clique em **Next** para começar a instalar o I2P.

![Iniciar a instalação](/images/guides/macos-install/7-i2p.png)

### Passo 5: Acordo de Licença

O instalador copiará os arquivos do I2P para o seu sistema. Isso leva cerca de 1-2 minutos.

![Instalação em andamento](/images/guides/macos-install/8-i2p.png)

### Passo 6: Selecionar Diretório de Instalação

O instalador cria scripts de lançamento para iniciar o I2P.

![Gerando scripts de inicialização](/images/guides/macos-install/9-i2p.png)

### Passo 7: Selecionar Componentes

O instalador oferece a criação de atalhos na área de trabalho e entradas no menu. Faça suas seleções e clique em **Avançar**.

![Criar atalhos](/images/guides/macos-install/10-i2p.png)

### Passo 8: Iniciar a Instalação

Sucesso! O I2P está agora instalado. Clique em **Concluído** para finalizar.

![Instalação concluída](/images/guides/macos-install/11-i2p.png)

## Part Three: Configure I2P App

Agora vamos facilitar o lançamento do I2P adicionando-o à sua pasta Aplicações e ao Dock.

### Passo 9: Instalando Arquivos

Abra o Finder e navegue até a sua pasta **Aplicações**.

![Abrir a pasta Aplicações](/images/guides/macos-install/0-conf.png)

### Passo 10: Gerar Scripts de Inicialização

Procure a pasta **I2P** ou a aplicação **Start I2P Router** dentro de `/Applications/i2p/`.

![Encontre o lançador do I2P](/images/guides/macos-install/1-conf.png)

### Passo 11: Atalhos de Instalação

Arraste o aplicativo **Start I2P Router** para o seu Dock para facilitar o acesso. Você também pode criar um alias na sua área de trabalho.

![Adicionar I2P ao Dock](/images/guides/macos-install/2-conf.png)

**Dica**: Clique com o botão direito no ícone do I2P no Dock e selecione **Opções → Manter no Dock** para torná-lo permanente.

## Part Four: Configure I2P Bandwidth

Quando você iniciar o I2P pela primeira vez, passará por um assistente de configuração para definir suas configurações de largura de banda. Isso ajuda a otimizar o desempenho do I2P para sua conexão.

### Passo 12: Instalação Concluída

Clique no ícone I2P no seu Dock (ou clique duas vezes no lançador). Seu navegador web padrão abrirá o Console do Router I2P.

![Tela de boas-vindas do Console do Roteador I2P](/images/guides/macos-install/0-wiz.png)

### Step 2: Welcome Wizard

O assistente de configuração irá cumprimentá-lo. Clique em **Next** para começar a configurar o I2P.

![Introdução do assistente de configuração](/images/guides/macos-install/1-wiz.png)

### Passo 1: Abrir a Pasta de Aplicativos

Selecione seu **idioma de interface** preferido e escolha entre o tema **claro** ou **escuro**. Clique em **Próximo**.

![Selecionar idioma e tema](/images/guides/macos-install/2-wiz.png)

### Passo 2: Encontrar o Lançador I2P

O assistente explicará o teste de largura de banda. Este teste conecta ao serviço **M-Lab** para medir a velocidade da sua internet. Clique em **Avançar** para prosseguir.

![Explicação do teste de largura de banda](/images/guides/macos-install/3-wiz.png)

### Passo 3: Adicionar ao Dock

Clique em **Run Test** para medir suas velocidades de upload e download. O teste leva cerca de 30-60 segundos.

![Executando o teste de largura de banda](/images/guides/macos-install/4-wiz.png)

### Step 6: Test Results

Revise os resultados do seu teste. O I2P recomendará configurações de largura de banda com base na velocidade da sua conexão.

![Resultados do teste de largura de banda](/images/guides/macos-install/5-wiz.png)

### Passo 1: Iniciar o I2P

Escolha quanta largura de banda você deseja compartilhar com a rede I2P:

- **Automático** (Recomendado): O I2P gerencia a largura de banda com base no seu uso
- **Limitado**: Defina limites específicos de upload/download
- **Ilimitado**: Compartilhe o máximo possível (para conexões rápidas)

Clique em **Next** para salvar suas configurações.

![Configure bandwidth sharing](/images/guides/macos-install/6-wiz.png)

### Passo 2: Assistente de Boas-vindas

O seu router I2P está agora configurado e em execução! A consola do router mostrará o estado da sua conexão e permitirá navegar em sites I2P.

## Getting Started with I2P

Agora que o I2P está instalado e configurado, você pode:

1. **Navegue por sites I2P**: Visite a [página inicial do I2P](http://127.0.0.1:7657/home) para ver links para serviços populares do I2P
2. **Configure seu navegador**: Configure um [perfil de navegador](/docs/guides/browser-config) para acessar sites `.i2p`
3. **Explore serviços**: Confira email I2P, fóruns, compartilhamento de arquivos e muito mais
4. **Monitore seu router**: O [console](http://127.0.0.1:7657/console) mostra o status da sua rede e estatísticas

### Passo 3: Idioma e Tema

- **Router Console**: [http://127.0.0.1:7657/](http://127.0.0.1:7657/)
- **Configuração**: [http://127.0.0.1:7657/config](http://127.0.0.1:7657/config)
- **Catálogo de Endereços**: [http://127.0.0.1:7657/susidns/addressbook](http://127.0.0.1:7657/susidns/addressbook)
- **Configurações de Largura de Banda**: [http://127.0.0.1:7657/config](http://127.0.0.1:7657/config)

## Re-running the Setup Wizard

Se você quiser alterar suas configurações de largura de banda ou reconfigurar o I2P posteriormente, você pode executar novamente o assistente de boas-vindas a partir do Router Console:

1. Vá para o [Assistente de Configuração do I2P](http://127.0.0.1:7657/welcome)
2. Siga os passos do assistente novamente

## Troubleshooting

### Passo 4: Informações do Teste de Largura de Banda

- **Verificar Java**: Certifique-se de que o Java está instalado executando `java -version` no Terminal
- **Verificar permissões**: Garanta que a pasta do I2P tenha as permissões corretas
- **Verificar logs**: Consulte `~/.i2p/wrapper.log` para mensagens de erro

### Passo 5: Executar Teste de Largura de Banda

- Certifique-se de que o I2P está em execução (verifique o Router Console)
- Configure as definições de proxy do seu navegador para usar o proxy HTTP `127.0.0.1:4444`
- Aguarde 5-10 minutos após iniciar para o I2P se integrar à rede

### Passo 6: Resultados dos Testes

- Execute o teste de largura de banda novamente e ajuste suas configurações
- Certifique-se de que você está compartilhando alguma largura de banda com a rede
- Verifique o status da sua conexão no Router Console

## Parte Dois: Baixar e Instalar o I2P

Para remover o I2P do seu Mac:

1. Encerre o roteador I2P se estiver em execução
2. Exclua a pasta `/Applications/i2p`
3. Exclua a pasta `~/.i2p` (sua configuração e dados do I2P)
4. Remova o ícone do I2P do seu Dock

## Next Steps

- **Junte-se à comunidade**: Visite [i2pforum.net](http://i2pforum.net) ou confira o I2P no Reddit
- **Saiba mais**: Leia a [documentação do I2P](/en/docs) para entender como a rede funciona
- **Envolva-se**: Considere [contribuir para o desenvolvimento do I2P](/en/get-involved) ou executar infraestrutura

Parabéns! Agora você faz parte da rede I2P. Bem-vindo à internet invisível!

