---
title: "Executando o GitLab sobre I2P"
description: "Implantando GitLab dentro do I2P usando Docker e um roteador I2P"
slug: "gitlab"
lastUpdated: "2025-02"
accurateFor: "2.5.0"
---

Hospedar o GitLab dentro do I2P é simples: execute o container omnibus do GitLab, exponha-o no loopback e encaminhe o tráfego através de um túnel I2P. Os passos abaixo refletem a configuração usada para `git.idk.i2p`, mas funcionam para qualquer instância auto-hospedada.

## 1. Pré-requisitos

- Debian ou outra distribuição Linux com Docker Engine instalado (`sudo apt install docker.io` ou `docker-ce` do repositório do Docker).
- Um router I2P (Java I2P ou i2pd) com largura de banda suficiente para servir seus usuários.
- Opcional: uma VM dedicada para que o GitLab e o router permaneçam isolados do seu ambiente desktop.

## 2. Baixar a Imagem do GitLab

```bash
docker pull gitlab/gitlab-ce:latest
```
A imagem oficial é construída a partir de camadas base do Ubuntu e atualizada regularmente. Audite o [Dockerfile](https://gitlab.com/gitlab-org/omnibus-gitlab/-/blob/master/docker/Dockerfile) se você precisar de garantias adicionais.

## 3. Decidir entre Bridging e I2P-Only

- **Somente I2P** instâncias nunca contactam hosts da clearnet. Os utilizadores podem espelhar repositórios de outros serviços I2P, mas não do GitHub/GitLab.com. Isto maximiza o anonimato.
- **Com ponte** instâncias acedem a hosts Git da clearnet através de um proxy HTTP. Isto é útil para espelhar projetos públicos para a I2P, mas desanonimiza as requisições de saída do servidor.

Se você escolher o modo bridged, configure o GitLab para usar um proxy HTTP I2P vinculado ao host Docker (por exemplo `http://172.17.0.1:4446`). O proxy padrão do router escuta apenas em `127.0.0.1`; adicione um novo túnel proxy vinculado ao endereço do gateway Docker.

## 4. Iniciar o Container

```bash
docker run --detach \
  --env HTTP_PROXY=http://172.17.0.1:4446 \  # omit for I2P-only
  --publish 127.0.0.1:8443:443 \
  --publish 127.0.0.1:8080:80 \
  --publish 127.0.0.1:8022:22 \
  --name gitlab \
  --restart always \
  --volume /srv/gitlab/config:/etc/gitlab:Z \
  --volume /srv/gitlab/logs:/var/log/gitlab:Z \
  --volume /srv/gitlab/data:/var/opt/gitlab:Z \
  gitlab/gitlab-ce:latest
```
- Vincule as portas publicadas ao loopback; os túneis I2P irão expô-las conforme necessário.
- Substitua `/srv/gitlab/...` por caminhos de armazenamento adequados ao seu host.

Quando o container estiver em execução, visite `https://127.0.0.1:8443/`, defina uma senha de administrador e configure os limites da conta.

## 5. Expor o GitLab Através do I2P

Crie três túneis **servidor** I2PTunnel:

| Purpose | Local target | Suggested inbound port |
| --- | --- | --- |
| HTTPS web UI | `127.0.0.1:8443` | auto-generated |
| HTTP web UI (optional) | `127.0.0.1:8080` | auto-generated |
| SSH push/pull | `127.0.0.1:8022` | auto-generated |
Configure cada túnel com comprimentos de túnel e largura de banda apropriados. Para instâncias públicas, 3 saltos com 4–6 túneis por direção é um bom ponto de partida. Publique os destinos Base32/Base64 resultantes em sua página inicial para que os usuários possam configurar túneis cliente.

### Destination Enforcement

Se você usar túneis HTTP(S), ative a imposição de destino para que apenas o hostname pretendido possa alcançar o serviço. Isso impede que o túnel seja usado indevidamente como um proxy genérico.

## 6. Maintenance Tips

- Execute `docker exec gitlab gitlab-ctl reconfigure` sempre que alterar as configurações do GitLab.
- Monitore o uso de disco (`/srv/gitlab/data`)—repositórios Git crescem rapidamente.
- Faça backup dos diretórios de configuração e dados regularmente. As [tarefas rake de backup](https://docs.gitlab.com/ee/raketasks/backup_restore.html) do GitLab funcionam dentro do contêiner.
- Considere colocar um tunnel de monitoramento externo em modo cliente para garantir que o serviço seja acessível a partir da rede mais ampla.

## 6. Dicas de Manutenção

- [Incorporar I2P na sua aplicação](/docs/applications/embedding/)
- [Git sobre I2P (guia do cliente)](/docs/applications/git/)
- [Git bundles para redes offline/lentas](/docs/applications/git-bundle/)

Uma instância GitLab bem configurada oferece um hub de desenvolvimento colaborativo totalmente dentro do I2P. Mantenha o router saudável, mantenha-se atualizado com as atualizações de segurança do GitLab e coordene com a comunidade à medida que sua base de usuários cresce.
