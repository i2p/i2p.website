---
title: "Configuração do Gitlab sobre I2P"
date: 2020-03-16
author: "idk"
description: "Espelhar repositórios Git do I2P e servir de ponte para repositórios da Clearnet para terceiros"
categories: ["development"]
---

Este é o processo de configuração que utilizo para configurar o Gitlab e o I2P, com o Docker responsável por gerenciar o próprio serviço. O Gitlab é muito fácil de hospedar no I2P dessa forma; pode ser administrado por uma única pessoa sem muita dificuldade. Estas instruções devem funcionar em qualquer sistema baseado em Debian e podem ser facilmente adaptadas a qualquer sistema em que o Docker e um I2P router estejam disponíveis.

## Dependências e Docker

Como o Gitlab é executado em um container, apenas precisamos instalar as dependências necessárias para o container no nosso sistema principal. Convenientemente, você pode instalar tudo de que precisa com:

```
sudo apt install docker.io
```
## Obtenha os contêineres Docker

Depois que você tiver o docker instalado, você pode obter os containers docker necessários para o gitlab. *Não os execute ainda.*

```
docker pull gitlab/gitlab-ce
```
## Configurar um proxy HTTP do I2P para o Gitlab (Informações importantes, etapas opcionais)

Servidores Gitlab dentro do I2P podem ser executados com ou sem a capacidade de interagir com servidores na internet fora do I2P. No caso em que os servidores Gitlab *não têm permissão* para interagir com servidores fora do I2P, eles não podem ser desanonimizados ao clonar um repositório git a partir de um servidor git na internet fora do I2P.

No caso em que o servidor Gitlab está *autorizado* a interagir com servidores fora do I2P, ele pode atuar como uma "ponte" para os usuários, que podem usá-lo para espelhar conteúdo de fora do I2P para uma fonte acessível via I2P; no entanto, *não é anônimo* nesse caso.

**Se você quiser ter uma instância de Gitlab bridged (em ponte), não anônima, com acesso a repositórios na web**, nenhuma modificação adicional é necessária.

**Se você quiser ter uma instância do Gitlab apenas I2P, sem acesso a repositórios apenas Web**, você precisará configurar o Gitlab para usar um proxy HTTP do I2P. Como o proxy HTTP padrão do I2P escuta apenas em `127.0.0.1`, você precisará configurar um novo para o Docker que escute no endereço Host/Gateway da rede do Docker, que geralmente é `172.17.0.1`. Eu configuro o meu na porta `4446`.

## Iniciar o contêiner localmente

Depois que você tiver isso configurado, poderá iniciar o contêiner e publicar sua instância do Gitlab localmente:

```
docker run --detach \
  --env HTTP_PROXY=http://172.17.0.1:4446 \
  --publish 127.0.0.1:8443:443 --publish 127.0.0.1:8080:80 --publish 127.0.0.1:8022:22 \
  --name gitlab \
  --restart always \
  --volume /srv/gitlab/config:/etc/gitlab:Z \
  --volume /srv/gitlab/logs:/var/log/gitlab:Z \
  --volume /srv/gitlab/data:/var/opt/gitlab:Z \
  gitlab/gitlab-ce:latest
```
Visite sua instância local do Gitlab e configure sua conta de administrador. Escolha uma senha forte, e configure os limites de contas de usuário para corresponder aos seus recursos.

## Configure seus Service tunnels e registre um nome de host

Depois de ter o Gitlab configurado localmente, vá ao console do I2P Router. Você precisará configurar dois tunnels de servidor, um apontando para a interface web(HTTP) do Gitlab na porta TCP 8080 e outro para a interface SSH do Gitlab na porta TCP 8022.

### Gitlab Web(HTTP) Interface

Para a interface Web, use um tunnel de servidor "HTTP". Em http://127.0.0.1:7657/i2ptunnelmgr, inicie o "New Tunnel Wizard" e insira os seguintes valores:

1. Select "Server Tunnel"
2. Select "HTTP Server"
3. Fill in "Gitlab Web Service" or otherwise describe the tunnel
4. Fill in `127.0.0.1` for the host and `8080` for the port
5. Select "Automatically start tunnel when Router Starts"
6. Confirm your selections

### Gitlab SSH Interface

Para a interface SSH, use um túnel de servidor "Standard". Em http://127.0.0.1:7657/i2ptunnelmgr, inicie o "New Tunnel Wizard" e insira os seguintes valores:

1. Select "Server Tunnel"
2. Select "Standard Server"
3. Fill in "Gitlab SSH Service" or otherwise describe the tunnel
4. Fill in `127.0.0.1` for the host and `8022` for the port
5. Select "Automatically start tunnel when Router Starts"
6. Confirm your selections

## Re-start the Gitlab Service with the new Hostname

Por fim, se você tiver modificado o `gitlab.rb` ou registrado um nome de host, será necessário reiniciar o serviço do GitLab para que as configurações tenham efeito.
