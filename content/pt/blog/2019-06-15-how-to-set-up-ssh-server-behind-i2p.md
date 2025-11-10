---
title: "Como configurar um servidor ssh por trás do I2P para acesso pessoal"
date: 2019-06-15
author: "idk"
description: "SSH sobre I2P"
---

# Como configurar um servidor ssh por trás do I2P para acesso pessoal

This is a tutorial on how to set up and tweak an I2P tunnel in order to use it to access an SSH server remotely, using either I2P or i2pd. For now, it assumes you will install your SSH server from a package manager and that it's running as a service.

Considerações: Neste guia, parto de alguns pressupostos. Eles precisarão ser ajustados dependendo das complicações que surgirem na sua configuração específica, especialmente se você usar VMs ou contêineres para isolamento. Isto pressupõe que o I2P router e o servidor SSH estão em execução no mesmo localhost. Você deve usar chaves de host SSH recém-geradas, seja utilizando um sshd recém-instalado, seja excluindo as chaves antigas e forçando sua regeneração. Por exemplo:

```
sudo service openssh stop
sudo rm -f /etc/ssh/ssh_host_*
sudo ssh-keygen -N "" -t rsa -f /etc/ssh/ssh_host_rsa_key
sudo ssh-keygen -N "" -t dsa -f /etc/ssh/ssh_host_dsa_key
sudo ssh-keygen -N "" -t ecdsa -f /etc/ssh/ssh_host_ecdsa_key
sudo ssh-keygen -N "" -t ed25519 -f /etc/ssh/ssh_host_ed25519_key
```
## Step One: Set up I2P tunnel for SSH Server

### Using Java I2P

Usando a interface web do java I2P, navegue até o [Gerenciador de Serviços Ocultos](http://127.0.0.1:7657/i2ptunnelmgr) e inicie o assistente de tunnel (túnel).

#### Tunnel Wizard

Como você está configurando este tunnel para o servidor SSH, você precisa selecionar o tipo de tunnel "Server".

**Espaço reservado para captura de tela:** Use o assistente para criar um "Server" tunnel

Você deve refiná-lo depois, mas o tipo de tunnel Padrão é o mais fácil para começar.

**Espaço reservado para captura de tela:** Do tipo "Standard"

Forneça uma boa descrição:

**Espaço reservado para captura de tela:** Descreva para que serve

E indique onde o servidor SSH estará disponível.

**Espaço reservado para captura de tela:** Aponte-o para o futuro local do seu servidor SSH

Revise os resultados e salve suas configurações.

**Espaço reservado para captura de tela:** Salve as configurações.

#### Advanced Settings

Agora volte ao Gerenciador de Serviços Ocultos e examine as configurações avançadas disponíveis. Uma coisa que você certamente vai querer alterar é configurá-lo para conexões interativas em vez de conexões em lote.

**Espaço reservado para captura de tela:** Configure o seu tunnel para conexões interativas

Além disso, essas outras opções podem afetar o desempenho ao acessar seu servidor SSH. Se você não estiver tão preocupado com o seu anonimato, então pode reduzir o número de saltos que faz. Se tiver problemas de velocidade, um número maior de tunnels pode ajudar. Alguns tunnels de backup provavelmente são uma boa ideia. Talvez seja preciso ajustar um pouco.

**Espaço reservado para captura de tela:** Se não estiver preocupado com o anonimato, então reduza o comprimento do tunnel.

Por fim, reinicie o tunnel para que todas as suas configurações tenham efeito.

Outra configuração interessante, especialmente se você optar por executar um número elevado de tunnels, é "Reduce on Idle", que reduzirá o número de tunnels em execução quando o servidor tiver passado por um período prolongado de inatividade.

**Espaço reservado para captura de tela:** Reduzir quando ocioso, se você escolheu um número elevado de tunnels

### Using i2pd

Com o i2pd, toda a configuração é feita por meio de arquivos, em vez de uma interface web. Para configurar um Serviço SSH tunnel para o i2pd, ajuste as configurações de exemplo a seguir às suas necessidades de anonimato e desempenho e copie-as para tunnels.conf

```
[SSH-SERVER]
type = server
host = 127.0.0.1
port = 22
inbound.length = 1
outbound.length = 1
inbound.quantity = 5
outbound.quantity = 5
i2cp.reduceOnIdle = true
keys = ssh-in.dat
```
#### Restart your I2P router

## Passo Um: Configurar o I2P tunnel para o servidor SSH

Dependendo de como você deseja acessar seu Servidor SSH, talvez você queira fazer algumas alterações nas configurações. Além das medidas óbvias de hardening de SSH que você deve aplicar em todos os servidores SSH (autenticação por chave pública, sem login como root, etc.), se você não quiser que seu Servidor SSH escute em quaisquer endereços, exceto no seu tunnel do servidor, você deve alterar AddressFamily para inet e ListenAddress para 127.0.0.1.

```
AddressFamily inet
ListenAddress 127.0.0.1
```
Se você optar por usar uma porta diferente de 22 para seu servidor SSH, será necessário alterar a porta na configuração do tunnel do I2P.

## Step Three: Set up I2P tunnel for SSH Client

Você precisará conseguir acessar o console do router I2P do servidor SSH para configurar a conexão do seu cliente. Uma vantagem interessante dessa configuração é que a conexão inicial ao I2P tunnel é autenticada, reduzindo um pouco o risco de que sua conexão inicial ao servidor SSH seja alvo de um ataque Man-in-the-Middle (MITM), como ocorre em cenários de Trust-On-First-Use (confiança na primeira utilização).

### Usando o Java I2P

#### Assistente de Tunnel

Primeiro, inicie o assistente de configuração de tunnel a partir do gerenciador de serviços ocultos e selecione um client tunnel.

**Espaço reservado para a captura de tela:** Use o assistente para criar um tunnel de cliente

Em seguida, selecione o tipo de tunnel padrão. Você irá refinar esta configuração mais tarde.

**Espaço reservado para captura de tela:** Do tipo Standard

Forneça uma boa descrição.

**Espaço reservado para captura de tela:** Dê uma boa descrição

Esta é a única parte ligeiramente complicada. Vá ao gerenciador de serviços ocultos do console do router I2P e encontre o "local destination" em base64 do tunnel do servidor SSH. Você precisará encontrar uma maneira de copiar essa informação para a próxima etapa. Geralmente envio para mim mesmo via [Tox](https://tox.chat), qualquer meio off-the-record deve ser suficiente para a maioria das pessoas.

**Espaço reservado para captura de tela:** Encontre o destino ao qual você deseja se conectar

Depois de encontrar o destino em base64 ao qual você deseja se conectar, transmitido para o seu dispositivo cliente, cole-o no campo de destino do cliente.

**Marcador de posição para captura de tela:** Fixe o destino

Por fim, defina uma porta local à qual seu cliente SSH se conectará. Essa porta local será conectada ao destino em Base64 e, portanto, ao servidor SSH.

**Espaço reservado para captura de tela:** Escolha uma porta local

Decida se deseja que ele inicie automaticamente.

**Espaço reservado para captura de tela:** Decida se você deseja que ele inicie automaticamente

#### Configurações avançadas

Como antes, você vai querer alterar as configurações para que fiquem otimizadas para conexões interativas. Além disso, se quiser configurar a lista de permissões de clientes no servidor, marque o botão de opção "Gerar chave para ativar a identidade persistente do tunnel do cliente".

**Espaço reservado para captura de tela:** Configure-o para ser interativo

### Using i2pd

Você pode configurar isso adicionando as seguintes linhas ao seu tunnels.conf e ajustando a configuração às suas necessidades de desempenho/anonimato.

```
[SSH-CLIENT]
type = client
host = 127.0.0.1
port = 7622
inbound.length = 1
outbound.length = 1
inbound.quantity = 5
outbound.quantity = 5
i2cp.dontPublishLeaseSet = true
destination = thisshouldbethebase32ofthesshservertunnelabovebefore.b32.i2p
keys = ssh-in.dat
```
#### Restart the I2P router on the client

## Step Four: Set up SSH client

Existem várias maneiras de configurar um cliente SSH para se conectar ao seu servidor na I2P, mas há algumas coisas que você deve fazer para proteger seu cliente SSH para uso anônimo. Primeiro, você deve configurá-lo para se identificar ao servidor SSH apenas com uma única chave específica, para não correr o risco de misturar suas conexões SSH anônimas e não anônimas.

Certifique-se de que o seu $HOME/.ssh/config contenha as seguintes linhas:

```
IdentitiesOnly yes

Host 127.0.0.1
  IdentityFile ~/.ssh/login_id_ed25519
```
Alternativamente, você pode criar uma entrada .bash_alias para impor suas opções e conectar-se automaticamente ao I2P. A ideia é que você precisa impor IdentitiesOnly e fornecer um arquivo de identidade.

```
i2pssh() {
    ssh -o IdentitiesOnly=yes -o IdentityFile=~/.ssh/login_id_ed25519 serveruser@127.0.0.1:7622
}
```
## Step Five: Whitelist only the client tunnel

Isto é quase opcional, mas é bem interessante e impedirá que qualquer pessoa que, por acaso, se depare com o seu destino perceba que você está hospedando um serviço SSH.

Primeiro, obtenha o destino do tunnel persistente do cliente e transmita-o ao servidor.

**Espaço reservado para captura de tela:** Obter o destino do cliente

Adicione o destino base64 do cliente à lista de permissões de destinos do servidor. Agora você só poderá se conectar ao tunnel do servidor a partir daquele tunnel de cliente específico e mais ninguém poderá se conectar a esse destino.

**Espaço reservado para captura de tela:** E cole-o na lista de permissões do servidor

Autenticação mútua é a melhor escolha.

**Nota:** As imagens referenciadas na postagem original precisam ser adicionadas ao diretório `/static/images/`: - server.png, standard.png, describe.png, hostport.png, approve.png - interactive.png, anonlevel.png, idlereduce.png - client.png, clientstandard.png, clientdescribe.png - finddestination.png, fixdestination.png, clientport.png, clientautostart.png - clientinteractive.png, whitelistclient.png, whitelistserver.png
