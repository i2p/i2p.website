---
title: "Ejecutar GitLab sobre I2P"
description: "Desplegando GitLab dentro de I2P usando Docker y un router I2P"
slug: "gitlab"
lastUpdated: "2025-02"
accurateFor: "2.5.0"
---

Alojar GitLab dentro de I2P es sencillo: ejecuta el contenedor omnibus de GitLab, expónlo en loopback y reenvía el tráfico a través de un tunnel I2P. Los pasos a continuación reflejan la configuración utilizada para `git.idk.i2p` pero funcionan para cualquier instancia auto-alojada.

## 1. Prerrequisitos

- Debian u otra distribución de Linux con Docker Engine instalado (`sudo apt install docker.io` o `docker-ce` desde el repositorio de Docker).
- Un router I2P (Java I2P o i2pd) con suficiente ancho de banda para servir a tus usuarios.
- Opcional: una VM dedicada para que GitLab y el router permanezcan aislados de tu entorno de escritorio.

## 2. Descargar la Imagen de GitLab

```bash
docker pull gitlab/gitlab-ce:latest
```
La imagen oficial se construye a partir de capas base de Ubuntu y se actualiza regularmente. Audite el [Dockerfile](https://gitlab.com/gitlab-org/omnibus-gitlab/-/blob/master/docker/Dockerfile) si necesita garantías adicionales.

## 3. Decidir entre Bridging vs. Solo I2P

- Las instancias **exclusivas de I2P** nunca contactan con hosts de clearnet. Los usuarios pueden replicar repositorios de otros servicios I2P, pero no desde GitHub/GitLab.com. Esto maximiza el anonimato.
- Las instancias **puente** se conectan a hosts Git de clearnet mediante un proxy HTTP. Esto es útil para replicar proyectos públicos en I2P, pero desanonimiza las solicitudes salientes del servidor.

Si eliges el modo bridged, configura GitLab para usar un proxy HTTP de I2P vinculado en el host de Docker (por ejemplo `http://172.17.0.1:4446`). El proxy del router predeterminado escucha solo en `127.0.0.1`; agrega un nuevo tunnel de proxy vinculado a la dirección del gateway de Docker.

## 4. Iniciar el Contenedor

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
- Vincula los puertos publicados a loopback; los túneles I2P los expondrán según sea necesario.
- Reemplaza `/srv/gitlab/...` con las rutas de almacenamiento que se ajusten a tu host.

Una vez que el contenedor esté en ejecución, visita `https://127.0.0.1:8443/`, establece una contraseña de administrador y configura los límites de cuenta.

## 5. Exponer GitLab a través de I2P

Crea tres túneles **servidor** de I2PTunnel:

| Purpose | Local target | Suggested inbound port |
| --- | --- | --- |
| HTTPS web UI | `127.0.0.1:8443` | auto-generated |
| HTTP web UI (optional) | `127.0.0.1:8080` | auto-generated |
| SSH push/pull | `127.0.0.1:8022` | auto-generated |
Configure cada túnel con longitudes de túnel y ancho de banda apropiados. Para instancias públicas, 3 saltos con 4–6 túneles por dirección es un buen punto de partida. Publique los destinos Base32/Base64 resultantes en su página de inicio para que los usuarios puedan configurar los túneles de cliente.

### Destination Enforcement

Si usas túneles HTTP(S), habilita la aplicación de destino para que solo el nombre de host previsto pueda acceder al servicio. Esto evita que el túnel sea usado indebidamente como un proxy genérico.

## 6. Maintenance Tips

- Ejecuta `docker exec gitlab gitlab-ctl reconfigure` cada vez que cambies la configuración de GitLab.
- Monitorea el uso de disco (`/srv/gitlab/data`)—los repositorios Git crecen rápidamente.
- Respalda los directorios de configuración y datos regularmente. Las [tareas rake de respaldo](https://docs.gitlab.com/ee/raketasks/backup_restore.html) de GitLab funcionan dentro del contenedor.
- Considera colocar un tunnel de monitoreo externo en modo cliente para asegurar que el servicio sea accesible desde la red más amplia.

## 6. Consejos de Mantenimiento

- [Integrar I2P en tu aplicación](/docs/applications/embedding/)
- [Git sobre I2P (guía del cliente)](/docs/applications/git/)
- [Paquetes Git para redes sin conexión/lentas](/docs/applications/git-bundle/)

Una instancia de GitLab bien configurada proporciona un centro de desarrollo colaborativo completamente dentro de I2P. Mantén el router saludable, mantente actualizado con las actualizaciones de seguridad de GitLab y coordina con la comunidad a medida que crece tu base de usuarios.
