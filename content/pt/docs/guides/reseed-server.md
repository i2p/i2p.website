---
title: "Criando e Executando um Servidor de Reseed I2P"
description: "Guia completo para configurar e operar um servidor de reseed I2P para ajudar novos routers a ingressarem na rede"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

Os hosts de reseed são infraestrutura crucial para a rede I2P, fornecendo aos novos routers um grupo inicial de nós durante o processo de bootstrap. Este guia irá orientá-lo na configuração e execução do seu próprio servidor de reseed.

## O que é um Servidor de Reseed I2P?

Um servidor de reseed I2P ajuda a integrar novos routers na rede I2P ao:

- **Fornecendo descoberta inicial de peers**: Novos roteadores recebem um conjunto inicial de nós de rede para se conectar
- **Recuperação de bootstrap**: Ajudando roteadores que estão com dificuldades para manter conexões
- **Distribuição segura**: O processo de reseeding é criptografado e assinado digitalmente para garantir a segurança da rede

Quando um novo router I2P é iniciado pela primeira vez (ou perdeu todas as suas conexões com peers), ele contacta servidores de reseed para baixar um conjunto inicial de informações de routers. Isso permite que o novo router comece a construir a sua própria netDb e estabelecer tunnels.

## Pré-requisitos

Antes de começar, você precisará de:

- Um servidor Linux (Debian/Ubuntu recomendado) com acesso root
- Um nome de domínio apontando para o seu servidor
- Pelo menos 1GB de RAM e 10GB de espaço em disco
- Um router I2P em execução no servidor para popular o netDb
- Familiaridade básica com administração de sistemas Linux

## Preparando o Servidor

### Step 1: Update System and Install Dependencies

Primeiro, atualize o seu sistema e instale os pacotes necessários:

```bash
sudo apt update && sudo apt upgrade -y && sudo apt-get install golang-go git make docker.io docker-compose -y
```
Isto instala: - **golang-go**: Runtime da linguagem de programação Go - **git**: Sistema de controle de versão - **make**: Ferramenta de automação de build - **docker.io & docker-compose**: Plataforma de contêineres para executar o Nginx Proxy Manager

![Instalação dos pacotes necessários](/images/guides/reseed/reseed_01.png)

### Step 2: Clone and Build Reseed Tools

Clone o repositório reseed-tools e compile a aplicação:

```bash
cd /home/i2p
git clone https://i2pgit.org/idk/reseed-tools
cd reseed-tools
make build
sudo make install
```
O pacote `reseed-tools` fornece a funcionalidade principal para executar um servidor de reseed. Ele cuida de: - Coletar informações de router do seu banco de dados de rede local - Empacotar informações de router em arquivos SU3 assinados - Servir esses arquivos via HTTPS

![Clonando o repositório reseed-tools](/images/guides/reseed/reseed_02.png)

### Step 3: Generate SSL Certificate

Gere o certificado SSL e a chave privada do seu servidor de reseed:

```bash
su - i2p -c 'reseed-tools reseed --signer=admin@stormycloud.org --netdb=/home/i2p/.i2p/netDb --port=8443 --ip=127.0.0.1 --trustProxy'
```
**Parâmetros importantes**: - `--signer`: Seu endereço de email (substitua `admin@stormycloud.org` pelo seu próprio) - `--netdb`: Caminho para o banco de dados de rede do seu router I2P - `--port`: Porta interna (8443 é recomendada) - `--ip`: Vincular ao localhost (usaremos um proxy reverso para acesso público) - `--trustProxy`: Confiar nos cabeçalhos X-Forwarded-For do proxy reverso

O comando irá gerar: - Uma chave privada para assinar arquivos SU3 - Um certificado SSL para conexões HTTPS seguras

![Geração de certificado SSL](/images/guides/reseed/reseed_03.png)

### Passo 1: Atualizar o Sistema e Instalar Dependências

**Crítico**: Faça backup seguro das chaves geradas localizadas em `/home/i2p/.reseed/`:

```bash
sudo tar -czf reseed-keys-backup.tar.gz /home/i2p/.reseed/
```
Armazene este backup em um local seguro e criptografado com acesso limitado. Essas chaves são essenciais para a operação do seu servidor de reseed e devem ser protegidas cuidadosamente.

## Configuring the Service

### Passo 2: Clonar e Compilar as Ferramentas de Reseed

Crie um serviço systemd para executar o servidor de reseed automaticamente:

```bash
sudo tee /etc/systemd/system/reseed.service <<EOF
[Unit]
Description=Reseed Service
After=network.target

[Service]
User=i2p
WorkingDirectory=/home/i2p
ExecStart=/bin/bash -c 'reseed-tools reseed --signer=admin@stormycloud.org --netdb=/home/i2p/.i2p/netDb --port=8443 --ip=127.0.0.1 --trustProxy'
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF
```
**Lembre-se de substituir** `admin@stormycloud.org` pelo seu próprio endereço de email.

Agora ative e inicie o serviço:

```bash
sudo systemctl daemon-reload
sudo systemctl enable reseed
sudo systemctl start reseed
```
Verifique se o serviço está em execução:

```bash
sudo systemctl status reseed
```
![Verificando o status do serviço de reseed](/images/guides/reseed/reseed_04.png)

### Passo 3: Gerar Certificado SSL

Para desempenho ideal, você pode querer reiniciar o serviço de reseed periodicamente para atualizar as informações do router:

```bash
sudo crontab -e
```
Adicione esta linha para reiniciar o serviço a cada 3 horas:

```
0 */3 * * * systemctl restart reseed
```
## Setting Up Reverse Proxy

O servidor de reseed é executado em localhost:8443 e precisa de um proxy reverso para lidar com o tráfego HTTPS público. Recomendamos o Nginx Proxy Manager pela sua facilidade de uso.

### Passo 4: Faça Backup das Suas Chaves

Implantar o Nginx Proxy Manager usando Docker:

```bash
docker run -d \
--name nginx-proxy-manager \
-p 80:80 \
-p 81:81 \
-p 443:443 \
-v $(pwd)/data:/data \
-v $(pwd)/letsencrypt:/etc/letsencrypt \
--restart unless-stopped \
jc21/nginx-proxy-manager:latest
```
Isto expõe: - **Porta 80**: Tráfego HTTP - **Porta 81**: Interface de administração - **Porta 443**: Tráfego HTTPS

### Configure Proxy Manager

1. Acesse a interface de administração em `http://your-server-ip:81`

2. Faça login com as credenciais padrão:
   - **Email**: admin@example.com
   - **Senha**: changeme

**Importante**: Altere estas credenciais imediatamente após o primeiro login!

![Login do Nginx Proxy Manager](/images/guides/reseed/reseed_05.png)

3. Navegue até **Proxy Hosts** e clique em **Add Proxy Host**

![Adicionando um host proxy](/images/guides/reseed/reseed_06.png)

4. Configure o host proxy:
   - **Domain Name**: Seu domínio de reseed (ex: `reseed.example.com`)
   - **Scheme**: `https`
   - **Forward Hostname / IP**: `127.0.0.1`
   - **Forward Port**: `8443`
   - Ative **Cache Assets**
   - Ative **Block Common Exploits**
   - Ative **Websockets Support**

![Configurando detalhes do host proxy](/images/guides/reseed/reseed_07.png)

5. Na aba **SSL**:
   - Selecione **Request a new SSL Certificate** (Let's Encrypt)
   - Ative **Force SSL**
   - Ative **HTTP/2 Support**
   - Aceite os Termos de Serviço do Let's Encrypt

![Configuração de certificado SSL](/images/guides/reseed/reseed_08.png)

6. Clique em **Save**

O seu servidor de reseed deverá agora estar acessível em `https://reseed.example.com`

![Configuração bem-sucedida do servidor de reseed](/images/guides/reseed/reseed_09.png)

## Registering Your Reseed Server

Assim que o seu servidor de reseed estiver operacional, entre em contato com os desenvolvedores do I2P para adicioná-lo à lista oficial de servidores de reseed.

### Passo 5: Criar Serviço Systemd

Envie um email para **zzz** (desenvolvedor líder do I2P) com as seguintes informações:

- **Email I2P**: zzz@mail.i2p
- **Email Clearnet**: zzz@i2pmail.org

### Passo 6: Opcional - Configurar Reinicializações Periódicas

Inclua no seu email:

1. **URL do servidor de reseed**: A URL HTTPS completa (ex.: `https://reseed.example.com`)
2. **Certificado público de reseed**: Localizado em `/home/i2p/.reseed/` (anexe o arquivo `.crt`)
3. **Email de contato**: Seu método de contato preferido para notificações de manutenção do servidor
4. **Localização do servidor**: Opcional, mas útil (país/região)
5. **Tempo de atividade esperado**: Seu compromisso em manter o servidor

### Verification

Os desenvolvedores do I2P irão verificar se o seu servidor de reseed está: - Devidamente configurado e servindo informações de router - Usando certificados SSL válidos - Fornecendo arquivos SU3 corretamente assinados - Acessível e responsivo

Uma vez aprovado, seu servidor de reseed será adicionado à lista distribuída com os roteadores I2P, ajudando novos usuários a entrarem na rede!

## Monitoring and Maintenance

### Instalar o Nginx Proxy Manager

Monitore seu serviço de reseed:

```bash
sudo systemctl status reseed
sudo journalctl -u reseed -f
```
### Configurar o Gestor de Proxy

Fique de olho nos recursos do sistema:

```bash
htop
df -h
```
### Update Reseed Tools

Atualize periodicamente as reseed-tools para obter as últimas melhorias:

```bash
cd /home/i2p/reseed-tools
git pull
make build
sudo make install
sudo systemctl restart reseed
```
### Informações de Contato

Se estiver usando Let's Encrypt através do Nginx Proxy Manager, os certificados renovarão automaticamente. Verifique se a renovação está funcionando:

```bash
docker logs nginx-proxy-manager | grep -i certificate
```
## Configurando o Serviço

### Informação Obrigatória

Verifique os logs em busca de erros:

```bash
sudo journalctl -u reseed -n 50
```
Problemas comuns: - Router I2P não está em execução ou a base de dados de rede está vazia - Porta 8443 já está em uso - Problemas de permissão com o diretório `/home/i2p/.reseed/`

### Verificação

Certifique-se de que o seu router I2P está em execução e preencheu a sua base de dados de rede:

```bash
ls -lh /home/i2p/.i2p/netDb/
```
Você deverá ver muitos arquivos `.dat`. Se estiver vazio, aguarde até que o seu roteador I2P descubra peers.

### SSL Certificate Errors

Verifique se seus certificados são válidos:

```bash
openssl s_client -connect reseed.example.com:443 -servername reseed.example.com
```
### Verificar Status do Serviço

Verifique: - Os registros DNS estão apontando corretamente para o seu servidor - O firewall permite as portas 80 e 443 - O Nginx Proxy Manager está em execução: `docker ps`

## Security Considerations

- **Mantenha suas chaves privadas seguras**: Nunca compartilhe ou exponha o conteúdo de `/home/i2p/.reseed/`
- **Atualizações regulares**: Mantenha os pacotes do sistema, Docker e reseed-tools atualizados
- **Monitore os logs**: Fique atento a padrões de acesso suspeitos
- **Limitação de taxa**: Considere implementar limitação de taxa para prevenir abuso
- **Regras de firewall**: Exponha apenas as portas necessárias (80, 443, 81 para admin)
- **Interface administrativa**: Restrinja a interface administrativa do Nginx Proxy Manager (porta 81) a IPs confiáveis

## Contributing to the Network

Ao executar um servidor de reseed, você está fornecendo infraestrutura crítica para a rede I2P. Obrigado por contribuir para uma internet mais privada e descentralizada!

Para dúvidas ou assistência, entre em contato com a comunidade I2P: - **Fórum**: [i2pforum.net](https://i2pforum.net) - **IRC/Reddit**: #i2p em várias redes - **Desenvolvimento**: [i2pgit.org](https://i2pgit.org)

---

IMPORTANTE:  NÃO faça perguntas, forneça explicações ou adicione qualquer comentário. Mesmo que o texto seja apenas um título ou pareça incompleto, traduza-o como está.

*Guia originalmente criado por [Stormy Cloud](https://www.stormycloud.org), adaptado para a documentação I2P.*
