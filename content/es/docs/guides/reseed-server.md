---
title: "Creación y Ejecución de un Servidor de Reseed de I2P"
description: "Guía completa para configurar y operar un servidor de reseed de I2P para ayudar a los nuevos routers a unirse a la red"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

Los hosts de reseed son infraestructura crucial para la red I2P, proporcionando a los routers nuevos un grupo inicial de nodos durante el proceso de arranque. Esta guía te guiará a través de la configuración y ejecución de tu propio servidor reseed.

## ¿Qué es un servidor de Reseed de I2P?

Un servidor de reseed de I2P ayuda a integrar nuevos routers en la red I2P mediante:

- **Proporcionar descubrimiento inicial de pares**: Los nuevos routers reciben un conjunto inicial de nodos de red a los que conectarse
- **Recuperación de arranque**: Ayudar a los routers que tienen dificultades para mantener conexiones
- **Distribución segura**: El proceso de reseeding está cifrado y firmado digitalmente para garantizar la seguridad de la red

Cuando un router I2P nuevo se inicia por primera vez (o ha perdido todas sus conexiones con peers), contacta servidores reseed para descargar un conjunto inicial de información de routers. Esto permite que el nuevo router comience a construir su propia base de datos de red y establecer túneles.

## Prerrequisitos

Antes de comenzar, necesitarás:

- Un servidor Linux (se recomienda Debian/Ubuntu) con acceso root
- Un nombre de dominio apuntando a tu servidor
- Al menos 1GB de RAM y 10GB de espacio en disco
- Un router I2P en ejecución en el servidor para poblar la netDb
- Familiaridad básica con la administración de sistemas Linux

## Preparando el Servidor

### Step 1: Update System and Install Dependencies

Primero, actualiza tu sistema e instala los paquetes requeridos:

```bash
sudo apt update && sudo apt upgrade -y && sudo apt-get install golang-go git make docker.io docker-compose -y
```
Esto instala: - **golang-go**: Runtime del lenguaje de programación Go - **git**: Sistema de control de versiones - **make**: Herramienta de automatización de compilación - **docker.io & docker-compose**: Plataforma de contenedores para ejecutar Nginx Proxy Manager

![Instalación de paquetes requeridos](/images/guides/reseed/reseed_01.png)

### Step 2: Clone and Build Reseed Tools

Clona el repositorio de reseed-tools y compila la aplicación:

```bash
cd /home/i2p
git clone https://i2pgit.org/idk/reseed-tools
cd reseed-tools
make build
sudo make install
```
El paquete `reseed-tools` proporciona la funcionalidad principal para ejecutar un servidor reseed. Se encarga de: - Recopilar información del router de tu base de datos de red local - Empaquetar la información del router en archivos SU3 firmados - Servir estos archivos a través de HTTPS

![Clonando el repositorio reseed-tools](/images/guides/reseed/reseed_02.png)

### Step 3: Generate SSL Certificate

Genera el certificado SSL y la clave privada de tu servidor reseed:

```bash
su - i2p -c 'reseed-tools reseed --signer=admin@stormycloud.org --netdb=/home/i2p/.i2p/netDb --port=8443 --ip=127.0.0.1 --trustProxy'
```
**Parámetros importantes**: - `--signer`: Tu dirección de correo electrónico (reemplaza `admin@stormycloud.org` con la tuya) - `--netdb`: Ruta a la base de datos de red (netDb) de tu router I2P - `--port`: Puerto interno (se recomienda 8443) - `--ip`: Enlazar a localhost (usaremos un proxy inverso para el acceso público) - `--trustProxy`: Confiar en las cabeceras X-Forwarded-For del proxy inverso

El comando generará: - Una clave privada para firmar archivos SU3 - Un certificado SSL para conexiones HTTPS seguras

![Generación de certificado SSL](/images/guides/reseed/reseed_03.png)

### Paso 1: Actualizar el Sistema e Instalar Dependencias

**Crítico**: Haz una copia de seguridad de forma segura de las claves generadas ubicadas en `/home/i2p/.reseed/`:

```bash
sudo tar -czf reseed-keys-backup.tar.gz /home/i2p/.reseed/
```
Almacene esta copia de seguridad en una ubicación segura y encriptada con acceso limitado. Estas claves son esenciales para el funcionamiento de su servidor reseed y deben protegerse cuidadosamente.

## Configuring the Service

### Paso 2: Clonar y Compilar las Herramientas de Reseed

Crea un servicio systemd para ejecutar el servidor reseed automáticamente:

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
**Recuerda reemplazar** `admin@stormycloud.org` con tu propia dirección de correo electrónico.

Ahora habilita e inicia el servicio:

```bash
sudo systemctl daemon-reload
sudo systemctl enable reseed
sudo systemctl start reseed
```
Verifica que el servicio esté en ejecución:

```bash
sudo systemctl status reseed
```
![Verificando el estado del servicio de reseed](/images/guides/reseed/reseed_04.png)

### Paso 3: Generar el Certificado SSL

Para un rendimiento óptimo, es posible que desees reiniciar el servicio de reseed periódicamente para actualizar la información del router:

```bash
sudo crontab -e
```
Añade esta línea para reiniciar el servicio cada 3 horas:

```
0 */3 * * * systemctl restart reseed
```
## Setting Up Reverse Proxy

El servidor de reseed se ejecuta en localhost:8443 y necesita un proxy inverso para manejar el tráfico HTTPS público. Recomendamos Nginx Proxy Manager por su facilidad de uso.

### Paso 4: Haz una copia de seguridad de tus claves

Desplegar Nginx Proxy Manager usando Docker:

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
Esto expone: - **Puerto 80**: Tráfico HTTP - **Puerto 81**: Interfaz de administración - **Puerto 443**: Tráfico HTTPS

### Configure Proxy Manager

1. Accede a la interfaz de administración en `http://your-server-ip:81`

2. Iniciar sesión con las credenciales predeterminadas:
   - **Correo electrónico**: admin@example.com
   - **Contraseña**: changeme

**Importante**: ¡Cambia estas credenciales inmediatamente después del primer inicio de sesión!

![Inicio de sesión de Nginx Proxy Manager](/images/guides/reseed/reseed_05.png)

3. Navega a **Proxy Hosts** y haz clic en **Add Proxy Host**

![Agregando un host proxy](/images/guides/reseed/reseed_06.png)

4. Configura el host del proxy:
   - **Nombre de Dominio**: Tu dominio de reseed (por ejemplo, `reseed.example.com`)
   - **Esquema**: `https`
   - **Hostname / IP de Reenvío**: `127.0.0.1`
   - **Puerto de Reenvío**: `8443`
   - Habilita **Cache Assets**
   - Habilita **Block Common Exploits**
   - Habilita **Websockets Support**

![Configurando los detalles del host proxy](/images/guides/reseed/reseed_07.png)

5. En la pestaña **SSL**:
   - Selecciona **Request a new SSL Certificate** (Let's Encrypt)
   - Habilita **Force SSL**
   - Habilita **HTTP/2 Support**
   - Acepta los Términos de Servicio de Let's Encrypt

![Configuración de certificado SSL](/images/guides/reseed/reseed_08.png)

6. Haz clic en **Guardar**

Tu servidor reseed ahora debería estar accesible en `https://reseed.example.com`

![Configuración exitosa del servidor de reseed](/images/guides/reseed/reseed_09.png)

## Registering Your Reseed Server

Una vez que tu servidor de reseed esté operativo, contacta a los desarrolladores de I2P para que sea añadido a la lista oficial de servidores de reseed.

### Paso 5: Crear el Servicio Systemd

Envía un correo electrónico a **zzz** (desarrollador principal de I2P) con la siguiente información:

- **Correo electrónico I2P**: zzz@mail.i2p
- **Correo electrónico Clearnet**: zzz@i2pmail.org

### Paso 6: Opcional - Configurar Reinicios Periódicos

Incluye en tu correo electrónico:

1. **URL del servidor reseed**: La URL HTTPS completa (p. ej., `https://reseed.example.com`)
2. **Certificado público reseed**: Ubicado en `/home/i2p/.reseed/` (adjuntar el archivo `.crt`)
3. **Correo electrónico de contacto**: Tu método de contacto preferido para notificaciones de mantenimiento del servidor
4. **Ubicación del servidor**: Opcional pero útil (país/región)
5. **Tiempo de actividad esperado**: Tu compromiso para mantener el servidor

### Verification

Los desarrolladores de I2P verificarán que tu servidor de reseed: - Esté configurado correctamente y sirviendo información de router - Use certificados SSL válidos - Proporcione archivos SU3 correctamente firmados - Sea accesible y responda adecuadamente

Una vez aprobado, tu servidor de reseed será agregado a la lista distribuida con los routers I2P, ¡ayudando a los nuevos usuarios a unirse a la red!

## Monitoring and Maintenance

### Instalar Nginx Proxy Manager

Monitorea tu servicio de reseed:

```bash
sudo systemctl status reseed
sudo journalctl -u reseed -f
```
### Configurar el Administrador de Proxy

Mantén un control de los recursos del sistema:

```bash
htop
df -h
```
### Update Reseed Tools

Actualiza periódicamente las reseed-tools para obtener las últimas mejoras:

```bash
cd /home/i2p/reseed-tools
git pull
make build
sudo make install
sudo systemctl restart reseed
```
### Información de Contacto

Si usas Let's Encrypt a través de Nginx Proxy Manager, los certificados se renovarán automáticamente. Verifica que la renovación esté funcionando:

```bash
docker logs nginx-proxy-manager | grep -i certificate
```
## Configurando el Servicio

### Información Requerida

Verifica los logs en busca de errores:

```bash
sudo journalctl -u reseed -n 50
```
Problemas comunes: - El router I2P no está ejecutándose o la netDb está vacía - El puerto 8443 ya está en uso - Problemas de permisos con el directorio `/home/i2p/.reseed/`

### Verificación

Asegúrate de que tu router I2P esté en ejecución y haya poblado su base de datos de red:

```bash
ls -lh /home/i2p/.i2p/netDb/
```
Deberías ver muchos archivos `.dat`. Si está vacío, espera a que tu router I2P descubra peers.

### SSL Certificate Errors

Verifica que tus certificados sean válidos:

```bash
openssl s_client -connect reseed.example.com:443 -servername reseed.example.com
```
### Verificar el Estado del Servicio

Verificar: - Los registros DNS están apuntando correctamente a tu servidor - El firewall permite los puertos 80 y 443 - Nginx Proxy Manager está en ejecución: `docker ps`

## Security Considerations

- **Mantén tus claves privadas seguras**: Nunca compartas ni expongas el contenido de `/home/i2p/.reseed/`
- **Actualizaciones regulares**: Mantén actualizados los paquetes del sistema, Docker y reseed-tools
- **Monitorea los logs**: Busca patrones de acceso sospechosos
- **Limitación de velocidad**: Considera implementar limitación de velocidad para prevenir abusos
- **Reglas de firewall**: Solo expone los puertos necesarios (80, 443, 81 para administración)
- **Interfaz de administración**: Restringe la interfaz de administración de Nginx Proxy Manager (puerto 81) a IPs de confianza

## Contributing to the Network

Al ejecutar un servidor reseed, estás proporcionando infraestructura crítica para la red I2P. ¡Gracias por contribuir a una internet más privada y descentralizada!

Para preguntas o asistencia, contacta con la comunidad I2P: - **Foro**: [i2pforum.net](https://i2pforum.net) - **IRC/Reddit**: #i2p en varias redes - **Desarrollo**: [i2pgit.org](https://i2pgit.org)

I'm ready to translate. However, I notice that no text was provided after the "---" marker in your message. Could you please share the English text you'd like me to translate to Spanish?

*Guía creada originalmente por [Stormy Cloud](https://www.stormycloud.org), adaptada para la documentación de I2P.*
