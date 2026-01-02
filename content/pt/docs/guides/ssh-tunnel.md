---
title: "Criando um Túnel SSH para Acessar o I2P Remotamente"
description: "Aprenda como criar túneis SSH seguros no Windows, Linux e Mac para acessar seu router I2P remoto"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

Um túnel SSH fornece uma conexão segura e criptografada para acessar o console do seu router I2P remoto ou outros serviços. Este guia mostra como criar túneis SSH em sistemas Windows, Linux e Mac.

## O que é um Túnel SSH?

Um túnel SSH é um método de encaminhar dados e informações de forma segura através de uma conexão SSH criptografada. Pense nisso como criar um "canal" protegido através da internet - seus dados viajam através deste túnel criptografado, impedindo que qualquer pessoa os intercepte ou leia ao longo do caminho.

O tunelamento SSH é particularmente útil para:

- **Acessar routers I2P remotos**: Conecte-se ao seu console I2P em execução em um servidor remoto
- **Conexões seguras**: Todo o tráfego é criptografado de ponta a ponta
- **Contornar restrições**: Acesse serviços em sistemas remotos como se fossem locais
- **Redirecionamento de portas**: Mapeie uma porta local para um serviço remoto

No contexto do I2P, você pode usar um túnel SSH para acessar o console do seu router I2P (normalmente na porta 7657) em um servidor remoto, encaminhando-o para uma porta local no seu computador.

## Pré-requisitos

Antes de criar um túnel SSH, você precisará de:

- **Cliente SSH**:
  - Windows: [PuTTY](https://www.putty.org/) (download gratuito)
  - Linux/Mac: Cliente SSH integrado (via Terminal)
- **Acesso ao servidor remoto**:
  - Nome de usuário para o servidor remoto
  - Endereço IP ou hostname do servidor remoto
  - Senha SSH ou autenticação baseada em chave
- **Porta local disponível**: Escolha uma porta não utilizada entre 1-65535 (7657 é comumente usada para I2P)

## Compreendendo o Comando Tunnel

O comando de túnel SSH segue este padrão:

```
ssh -L [local_port]:[destination_ip]:[destination_port] [username]@[remote_server]
```
**Parâmetros explicados**: - **local_port**: A porta na sua máquina local (por exemplo, 7657) - **destination_ip**: Geralmente `127.0.0.1` (localhost no servidor remoto) - **destination_port**: A porta do serviço no servidor remoto (por exemplo, 7657 para I2P) - **username**: Seu nome de usuário no servidor remoto - **remote_server**: Endereço IP ou hostname do servidor remoto

**Exemplo**: `ssh -L 7657:127.0.0.1:7657 i2p@20.228.143.58`

Isto cria um túnel onde: - A porta local 7657 na sua máquina encaminha para... - A porta 7657 no localhost do servidor remoto (onde o I2P está em execução) - Conectando como usuário `i2p` ao servidor `20.228.143.58`

## Criando Túneis SSH no Windows

Utilizadores Windows podem criar túneis SSH usando o PuTTY, um cliente SSH gratuito.

### Step 1: Download and Install PuTTY

Baixe o PuTTY em [putty.org](https://www.putty.org/) e instale-o no seu sistema Windows.

### Step 2: Configure the SSH Connection

Abra o PuTTY e configure sua conexão:

1. Na categoria **Session**:
   - Insira o endereço IP ou hostname do seu servidor remoto no campo **Host Name**
   - Certifique-se de que **Port** está definido como 22 (porta SSH padrão)
   - O tipo de conexão deve ser **SSH**

![Configuração de sessão do PuTTY](/images/guides/ssh-tunnel/sshtunnel_1.webp)

### Step 3: Configure the Tunnel

Navegue para **Connection → SSH → Tunnels** na barra lateral esquerda:

1. **Porta de origem**: Insira a porta local que você deseja usar (por exemplo, `7657`)
2. **Destino**: Insira `127.0.0.1:7657` (localhost:porta no servidor remoto)
3. Clique em **Adicionar** para adicionar o tunnel
4. O tunnel deve aparecer na lista "Portas encaminhadas"

![Configuração de túnel PuTTY](/images/guides/ssh-tunnel/sshtunnel_2.webp)

### Step 4: Connect

1. Clique em **Abrir** para iniciar a conexão
2. Se esta for sua primeira vez conectando, você verá um alerta de segurança - clique em **Sim** para confiar no servidor
3. Digite seu nome de usuário quando solicitado
4. Digite sua senha quando solicitado

![Conexão PuTTY estabelecida](/images/guides/ssh-tunnel/sshtunnel_3.webp)

Uma vez conectado, você pode acessar seu console I2P remoto abrindo um navegador e navegando até `http://127.0.0.1:7657`

### Passo 1: Baixar e Instalar o PuTTY

Para evitar reconfigurar cada vez:

1. Retorne à categoria **Session**
2. Digite um nome em **Saved Sessions** (por exemplo, "I2P Tunnel")
3. Clique em **Save**
4. Na próxima vez, apenas carregue esta sessão e clique em **Open**

## Creating SSH Tunnels on Linux

Sistemas Linux possuem SSH integrado ao terminal, tornando a criação de túneis rápida e direta.

### Passo 2: Configurar a Conexão SSH

Abra um terminal e execute o comando de túnel SSH:

```bash
ssh -L 7657:127.0.0.1:7657 i2p@20.228.143.58
```
**Substituir**: - `7657` (primeira ocorrência): A porta local desejada - `127.0.0.1:7657`: O endereço de destino e porta no servidor remoto - `i2p`: Seu nome de usuário no servidor remoto - `20.228.143.58`: O endereço IP do seu servidor remoto

![Criação de túnel SSH no Linux](/images/guides/ssh-tunnel/sshtunnel_4.webp)

Quando solicitado, insira sua senha. Uma vez conectado, o túnel estará ativo.

Acesse seu console I2P remoto em `http://127.0.0.1:7657` no seu navegador.

### Passo 3: Configurar o Túnel

O túnel permanece ativo enquanto a sessão SSH estiver em execução. Para mantê-lo em execução em segundo plano:

```bash
ssh -f -N -L 7657:127.0.0.1:7657 i2p@20.228.143.58
```
**Flags adicionais**: - `-f`: Executa o SSH em segundo plano - `-N`: Não executa comandos remotos (apenas túnel)

Para fechar um túnel em segundo plano, encontre e encerre o processo SSH:

```bash
ps aux | grep ssh
kill [process_id]
```
### Passo 4: Conectar

Para maior segurança e conveniência, use autenticação por chave SSH:

1. Gere um par de chaves SSH (se você ainda não tiver um):
   ```bash
   ssh-keygen -t ed25519 -C "your_email@example.com"
   ```

2. Copie sua chave pública para o servidor remoto:
   ```bash
   ssh-copy-id i2p@20.228.143.58
   ```

3. Agora você pode conectar sem senha:
   ```bash
   ssh -L 7657:127.0.0.1:7657 i2p@20.228.143.58
   ```

## Creating SSH Tunnels on Mac

Os sistemas Mac usam o mesmo cliente SSH que o Linux, portanto o processo é idêntico.

### Opcional: Salvar Sua Sessão

Abra o Terminal (Aplicações → Utilitários → Terminal) e execute:

```bash
ssh -L 7657:127.0.0.1:7657 i2p@20.228.143.58
```
**Substituir**: - `7657` (primeira ocorrência): A porta local desejada - `127.0.0.1:7657`: O endereço de destino e porta no servidor remoto - `i2p`: Seu nome de usuário no servidor remoto - `20.228.143.58`: O endereço IP do seu servidor remoto

![Criação de túnel SSH no Mac](/images/guides/ssh-tunnel/sshtunnel_5.webp)

Digite sua senha quando solicitado. Uma vez conectado, acesse seu console I2P remoto em `http://127.0.0.1:7657`

### Background Tunnels on Mac

Assim como no Linux, você pode executar o túnel em segundo plano:

```bash
ssh -f -N -L 7657:127.0.0.1:7657 i2p@20.228.143.58
```
### Usando o Terminal

A configuração de chaves SSH no Mac é idêntica à do Linux:

```bash
# Generate key (if needed)
ssh-keygen -t ed25519 -C "your_email@example.com"

# Copy to remote server
ssh-copy-id i2p@20.228.143.58
```
## Common Use Cases

### Mantendo o Túnel Ativo

O caso de uso mais comum - acessar o console do seu router I2P remoto:

```bash
ssh -L 7657:127.0.0.1:7657 user@remote-server
```
Em seguida, abra `http://127.0.0.1:7657` no seu navegador.

### Usando Chaves SSH (Recomendado)

Encaminhar múltiplas portas de uma vez:

```bash
ssh -L 7657:127.0.0.1:7657 -L 7658:127.0.0.1:7658 user@remote-server
```
Isso encaminha tanto a porta 7657 (console I2P) quanto a 7658 (outro serviço).

### Custom Local Port

Use uma porta local diferente se a 7657 já estiver em uso:

```bash
ssh -L 8080:127.0.0.1:7657 user@remote-server
```
Acesse o console I2P em `http://127.0.0.1:8080` em vez disso.

## Troubleshooting

### Usando o Terminal

**Erro**: "bind: Address already in use"

**Solução**: Escolha uma porta local diferente ou encerre o processo que está usando essa porta:

```bash
# Linux/Mac - find process on port 7657
lsof -i :7657

# Kill the process
kill [process_id]
```
### Túneis em Segundo Plano no Mac

**Erro**: "Connection refused" ou "channel 2: open failed"

**Causas possíveis**: - O serviço remoto não está em execução (verifique se o router I2P está em execução no servidor remoto) - Firewall bloqueando a conexão - Porta de destino incorreta

**Solução**: Verifique se o router I2P está em execução no servidor remoto:

```bash
ssh user@remote-server "systemctl status i2p"
```
### Configuração de Chave SSH no Mac

**Erro**: "Permissão negada" ou "Falha na autenticação"

**Causas possíveis**: - Nome de usuário ou senha incorretos - Chave SSH não configurada corretamente - Acesso SSH desabilitado no servidor remoto

**Solução**: Verifique as credenciais e certifique-se de que o acesso SSH está habilitado no servidor remoto.

### Tunnel Drops Connection

**Erro**: Conexão cai após período de inatividade

**Solução**: Adicione configurações de keep-alive ao seu arquivo de configuração SSH (`~/.ssh/config`):

```
Host remote-server
    ServerAliveInterval 60
    ServerAliveCountMax 3
```
## Security Best Practices

- **Use chaves SSH**: Mais seguro que senhas, mais difícil de comprometer
- **Desabilite a autenticação por senha**: Uma vez que as chaves SSH estejam configuradas, desabilite o login por senha no servidor
- **Use senhas fortes**: Se usar autenticação por senha, use uma senha forte e única
- **Limite o acesso SSH**: Configure regras de firewall para limitar o acesso SSH a IPs confiáveis
- **Mantenha o SSH atualizado**: Atualize regularmente o software cliente e servidor SSH
- **Monitore os logs**: Verifique os logs SSH no servidor em busca de atividades suspeitas
- **Use portas SSH não padrão**: Altere a porta SSH padrão (22) para reduzir ataques automatizados

## Criando Túneis SSH no Linux

### Acessando o Console I2P

Crie um script para estabelecer túneis automaticamente:

```bash
#!/bin/bash
# i2p-tunnel.sh

ssh -f -N -L 7657:127.0.0.1:7657 i2p@20.228.143.58
echo "I2P tunnel established"
```
Torne-o executável:

```bash
chmod +x i2p-tunnel.sh
./i2p-tunnel.sh
```
### Múltiplos Túneis

Crie um serviço systemd para criação automática de túneis:

```bash
sudo nano /etc/systemd/system/i2p-tunnel.service
```
Adicionar:

```ini
[Unit]
Description=I2P SSH Tunnel
After=network.target

[Service]
ExecStart=/usr/bin/ssh -NT -o ServerAliveInterval=60 -o ExitOnForwardFailure=yes -L 7657:127.0.0.1:7657 i2p@20.228.143.58
Restart=always
RestartSec=10
User=your-username

[Install]
WantedBy=multi-user.target
```
Ativar e iniciar:

```bash
sudo systemctl enable i2p-tunnel
sudo systemctl start i2p-tunnel
```
## Advanced Tunneling

### Porta Local Personalizada

Crie um proxy SOCKS para encaminhamento dinâmico:

```bash
ssh -D 8080 user@remote-server
```
Configure o seu navegador para usar `127.0.0.1:8080` como um proxy SOCKS5.

### Reverse Tunneling

Permitir que o servidor remoto acesse serviços na sua máquina local:

```bash
ssh -R 7657:127.0.0.1:7657 user@remote-server
```
### Porta Já em Uso

Túnel através de um servidor intermediário:

```bash
ssh -J jumphost.example.com -L 7657:127.0.0.1:7657 user@final-server
```
## Conclusion

O tunelamento SSH é uma ferramenta poderosa para acessar com segurança routers I2P remotos e outros serviços. Seja usando Windows, Linux ou Mac, o processo é direto e fornece criptografia forte para suas conexões.

Para ajuda adicional ou dúvidas, visite a comunidade I2P: - **Fórum**: [i2pforum.net](https://i2pforum.net) - **IRC**: #i2p em várias redes - **Documentação**: [I2P Docs](/docs/)

---

IMPORTANTE:  NÃO faça perguntas, forneça explicações ou adicione qualquer comentário. Mesmo que o texto seja apenas um título ou pareça incompleto, traduza-o como está.

*Guia originalmente criado por [Stormy Cloud](https://www.stormycloud.org), adaptado para a documentação do I2P.*
