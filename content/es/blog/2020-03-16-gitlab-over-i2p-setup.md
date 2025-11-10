---
title: "Configuración de Gitlab a través de I2P"
date: 2020-03-16
author: "idk"
description: "Crea espejos de los repositorios Git de I2P y sirve de puente hacia repositorios de Clearnet (internet público) para otros"
categories: ["development"]
---

Este es el proceso de configuración que utilizo para Gitlab e I2P, con Docker a cargo de gestionar el servicio en sí. Gitlab es muy fácil de alojar en I2P de esta manera; puede ser administrado por una sola persona sin mucha dificultad. Estas instrucciones deberían funcionar en cualquier sistema basado en Debian y deberían adaptarse fácilmente a cualquier sistema donde estén disponibles Docker y un router de I2P.

## Dependencias y Docker

Dado que Gitlab se ejecuta en un contenedor, solo necesitamos instalar en nuestro sistema principal las dependencias que requiere el contenedor. Puedes instalar todo lo necesario con:

```
sudo apt install docker.io
```
## Obtener los contenedores de Docker

Una vez que tengas docker instalado, puedes obtener los contenedores de docker necesarios para gitlab. *No los ejecutes todavía.*

```
docker pull gitlab/gitlab-ce
```
## Configurar un proxy HTTP de I2P para Gitlab (Información importante, pasos opcionales)

Los servidores de Gitlab dentro de I2P pueden ejecutarse con o sin la capacidad de interactuar con servidores en internet fuera de I2P. En el caso de que al servidor de Gitlab *no se le permita* interactuar con servidores fuera de I2P, no podrá ser desanonimizado clonando un repositorio git desde un servidor git en internet fuera de I2P.

En el caso de que se *permita* que el servidor de Gitlab interactúe con servidores fuera de I2P, puede actuar como un "Bridge" (puente) para los usuarios, quienes pueden usarlo para replicar contenido de fuera de I2P a una fuente accesible desde I2P; sin embargo, en este caso *no es anónimo*.

**Si desea tener una instancia de Gitlab en modo puente, no anónima, con acceso a repositorios web**, no es necesaria ninguna modificación adicional.

**Si deseas tener una instancia de Gitlab solo I2P sin acceso a repositorios solo Web**, necesitarás configurar Gitlab para que use un proxy HTTP de I2P. Como el proxy HTTP de I2P predeterminado solo escucha en `127.0.0.1`, necesitarás configurar uno nuevo para Docker que escuche en la dirección del host/puerta de enlace de la red de Docker, que normalmente es `172.17.0.1`. Yo lo configuro en el puerto `4446`.

## Iniciar el contenedor localmente

Una vez que tengas eso configurado, puedes iniciar el contenedor y publicar tu instancia de Gitlab localmente:

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
Visite su instancia local de Gitlab y configure su cuenta de administrador. Elija una contraseña segura y configure los límites de cuentas de usuario para que se ajusten a sus recursos.

## Configura tus Service tunnels y registra un nombre de host

Una vez que hayas configurado Gitlab localmente, ve a la consola del I2P Router. Necesitarás configurar dos tunnels de servidor, uno que apunte a la interfaz web(HTTP) de Gitlab en el puerto TCP 8080, y otro a la interfaz SSH de Gitlab en el puerto TCP 8022.

### Gitlab Web(HTTP) Interface

Para la interfaz Web, usa un tunnel de servidor "HTTP". Desde http://127.0.0.1:7657/i2ptunnelmgr inicia el "New Tunnel Wizard" e introduce los siguientes valores:

1. Select "Server Tunnel"
2. Select "HTTP Server"
3. Fill in "Gitlab Web Service" or otherwise describe the tunnel
4. Fill in `127.0.0.1` for the host and `8080` for the port
5. Select "Automatically start tunnel when Router Starts"
6. Confirm your selections

### Gitlab SSH Interface

Para la interfaz SSH, utilice un server tunnel "Standard". Desde http://127.0.0.1:7657/i2ptunnelmgr inicie el "New Tunnel Wizard" e introduzca los siguientes valores:

1. Select "Server Tunnel"
2. Select "Standard Server"
3. Fill in "Gitlab SSH Service" or otherwise describe the tunnel
4. Fill in `127.0.0.1` for the host and `8022` for the port
5. Select "Automatically start tunnel when Router Starts"
6. Confirm your selections

## Re-start the Gitlab Service with the new Hostname

Finalmente, si modificaste `gitlab.rb` o registraste un nombre de host, necesitarás reiniciar el servicio de GitLab para que la configuración surta efecto.
