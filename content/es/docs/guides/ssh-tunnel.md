---
title: "Creación de un túnel SSH para acceder a I2P de forma remota"
description: "Aprende cómo crear túneles SSH seguros en Windows, Linux y Mac para acceder a tu router I2P remoto"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

Un túnel SSH proporciona una conexión segura y cifrada para acceder a la consola de tu router I2P remoto u otros servicios. Esta guía te muestra cómo crear túneles SSH en sistemas Windows, Linux y Mac.

## ¿Qué es un túnel SSH?

Un túnel SSH es un método para enrutar datos e información de manera segura a través de una conexión SSH cifrada. Piénsalo como crear una "tubería" protegida a través de internet: tus datos viajan a través de este túnel cifrado, evitando que cualquiera los intercepte o los lea en el camino.

El tunneling SSH es particularmente útil para:

- **Acceso a routers I2P remotos**: Conéctate a tu consola I2P ejecutándose en un servidor remoto
- **Conexiones seguras**: Todo el tráfico está cifrado de extremo a extremo
- **Evitar restricciones**: Accede a servicios en sistemas remotos como si fueran locales
- **Reenvío de puertos**: Mapea un puerto local a un servicio remoto

En el contexto de I2P, puedes usar un túnel SSH para acceder a tu consola de router I2P (típicamente en el puerto 7657) en un servidor remoto reenviándola a un puerto local en tu computadora.

## Requisitos previos

Antes de crear un túnel SSH, necesitarás:

- **Cliente SSH**:
  - Windows: [PuTTY](https://www.putty.org/) (descarga gratuita)
  - Linux/Mac: Cliente SSH integrado (vía Terminal)
- **Acceso al servidor remoto**:
  - Nombre de usuario para el servidor remoto
  - Dirección IP o nombre de host del servidor remoto
  - Contraseña SSH o autenticación basada en clave
- **Puerto local disponible**: Elija un puerto sin usar entre 1-65535 (7657 es comúnmente usado para I2P)

## Entendiendo el Comando Tunnel

El comando del túnel SSH sigue este patrón:

```
ssh -L [local_port]:[destination_ip]:[destination_port] [username]@[remote_server]
```
**Parámetros explicados**: - **local_port**: El puerto en tu máquina local (por ejemplo, 7657) - **destination_ip**: Usualmente `127.0.0.1` (localhost en el servidor remoto) - **destination_port**: El puerto del servicio en el servidor remoto (por ejemplo, 7657 para I2P) - **username**: Tu nombre de usuario en el servidor remoto - **remote_server**: Dirección IP o nombre de host del servidor remoto

**Ejemplo**: `ssh -L 7657:127.0.0.1:7657 i2p@20.228.143.58`

Esto crea un túnel donde: - El puerto local 7657 en tu máquina reenvía a... - El puerto 7657 en el localhost del servidor remoto (donde I2P está ejecutándose) - Conectando como usuario `i2p` al servidor `20.228.143.58`

## Creación de túneles SSH en Windows

Los usuarios de Windows pueden crear túneles SSH usando PuTTY, un cliente SSH gratuito.

### Step 1: Download and Install PuTTY

Descarga PuTTY desde [putty.org](https://www.putty.org/) e instálalo en tu sistema Windows.

### Step 2: Configure the SSH Connection

Abre PuTTY y configura tu conexión:

1. En la categoría **Session**:
   - Ingresa la dirección IP o nombre de host de tu servidor remoto en el campo **Host Name**
   - Asegúrate de que **Port** esté configurado en 22 (puerto SSH predeterminado)
   - El tipo de conexión debe ser **SSH**

![Configuración de sesión de PuTTY](/images/guides/ssh-tunnel/sshtunnel_1.webp)

### Step 3: Configure the Tunnel

Navega a **Connection → SSH → Tunnels** en la barra lateral izquierda:

1. **Puerto de origen**: Ingresa el puerto local que deseas usar (ej., `7657`)
2. **Destino**: Ingresa `127.0.0.1:7657` (localhost:puerto en el servidor remoto)
3. Haz clic en **Agregar** para añadir el túnel
4. El túnel debería aparecer en la lista "Puertos reenviados"

![Configuración de túnel PuTTY](/images/guides/ssh-tunnel/sshtunnel_2.webp)

### Step 4: Connect

1. Haz clic en **Abrir** para iniciar la conexión
2. Si es la primera vez que te conectas, verás una alerta de seguridad - haz clic en **Sí** para confiar en el servidor
3. Ingresa tu nombre de usuario cuando se te solicite
4. Ingresa tu contraseña cuando se te solicite

![Conexión PuTTY establecida](/images/guides/ssh-tunnel/sshtunnel_3.webp)

Una vez conectado, puedes acceder a tu consola I2P remota abriendo un navegador y navegando a `http://127.0.0.1:7657`

### Paso 1: Descargar e Instalar PuTTY

Para evitar reconfigurar cada vez:

1. Regresa a la categoría **Session**
2. Introduce un nombre en **Saved Sessions** (por ejemplo, "I2P Tunnel")
3. Haz clic en **Save**
4. La próxima vez, simplemente carga esta sesión y haz clic en **Open**

## Creating SSH Tunnels on Linux

Los sistemas Linux tienen SSH integrado en el terminal, lo que hace que la creación de túneles sea rápida y sencilla.

### Paso 2: Configurar la Conexión SSH

Abre una terminal y ejecuta el comando del túnel SSH:

```bash
ssh -L 7657:127.0.0.1:7657 i2p@20.228.143.58
```
**Reemplazar**: - `7657` (primera ocurrencia): Tu puerto local deseado - `127.0.0.1:7657`: La dirección de destino y puerto en el servidor remoto - `i2p`: Tu nombre de usuario en el servidor remoto - `20.228.143.58`: La dirección IP de tu servidor remoto

![Creación de túnel SSH en Linux](/images/guides/ssh-tunnel/sshtunnel_4.webp)

Cuando se te solicite, ingresa tu contraseña. Una vez conectado, el túnel estará activo.

Accede a tu consola I2P remota en `http://127.0.0.1:7657` en tu navegador.

### Paso 3: Configurar el Túnel

El túnel permanece activo mientras la sesión SSH esté en ejecución. Para mantenerlo ejecutándose en segundo plano:

```bash
ssh -f -N -L 7657:127.0.0.1:7657 i2p@20.228.143.58
```
**Banderas adicionales**: - `-f`: Ejecuta SSH en segundo plano - `-N`: No ejecutar comandos remotos (solo túnel)

Para cerrar un túnel en segundo plano, encuentra y termina el proceso SSH:

```bash
ps aux | grep ssh
kill [process_id]
```
### Paso 4: Conectar

Para mayor seguridad y comodidad, utilice autenticación por clave SSH:

1. Genera un par de claves SSH (si no tienes uno):
   ```bash
   ssh-keygen -t ed25519 -C "your_email@example.com"
   ```

2. Copia tu clave pública al servidor remoto:
   ```bash
   ssh-copy-id i2p@20.228.143.58
   ```

3. Ahora puedes conectarte sin contraseña:
   ```bash
   ssh -L 7657:127.0.0.1:7657 i2p@20.228.143.58
   ```

## Creating SSH Tunnels on Mac

Los sistemas Mac utilizan el mismo cliente SSH que Linux, por lo que el proceso es idéntico.

### Opcional: Guardar tu sesión

Abre Terminal (Aplicaciones → Utilidades → Terminal) y ejecuta:

```bash
ssh -L 7657:127.0.0.1:7657 i2p@20.228.143.58
```
**Reemplazar**: - `7657` (primera aparición): El puerto local que desees - `127.0.0.1:7657`: La dirección de destino y puerto en el servidor remoto - `i2p`: Tu nombre de usuario en el servidor remoto - `20.228.143.58`: La dirección IP de tu servidor remoto

![Creación de túnel SSH en Mac](/images/guides/ssh-tunnel/sshtunnel_5.webp)

Ingresa tu contraseña cuando se te solicite. Una vez conectado, accede a tu consola remota de I2P en `http://127.0.0.1:7657`

### Background Tunnels on Mac

Al igual que en Linux, puedes ejecutar el túnel en segundo plano:

```bash
ssh -f -N -L 7657:127.0.0.1:7657 i2p@20.228.143.58
```
### Usar la Terminal

La configuración de claves SSH en Mac es idéntica a la de Linux:

```bash
# Generate key (if needed)
ssh-keygen -t ed25519 -C "your_email@example.com"

# Copy to remote server
ssh-copy-id i2p@20.228.143.58
```
## Common Use Cases

### Manteniendo el Túnel Activo

El caso de uso más común - acceder a la consola de tu router I2P remoto:

```bash
ssh -L 7657:127.0.0.1:7657 user@remote-server
```
Luego abre `http://127.0.0.1:7657` en tu navegador.

### Usar Claves SSH (Recomendado)

Reenviar múltiples puertos a la vez:

```bash
ssh -L 7657:127.0.0.1:7657 -L 7658:127.0.0.1:7658 user@remote-server
```
Esto reenvía tanto el puerto 7657 (consola I2P) como el 7658 (otro servicio).

### Custom Local Port

Usa un puerto local diferente si el 7657 ya está en uso:

```bash
ssh -L 8080:127.0.0.1:7657 user@remote-server
```
Accede a la consola de I2P en `http://127.0.0.1:8080` en su lugar.

## Troubleshooting

### Usando la Terminal

**Error**: "bind: Address already in use"

**Solución**: Elija un puerto local diferente o finalice el proceso que está usando ese puerto:

```bash
# Linux/Mac - find process on port 7657
lsof -i :7657

# Kill the process
kill [process_id]
```
### Túneles en Segundo Plano en Mac

**Error**: "Connection refused" o "channel 2: open failed"

**Posibles causas**: - El servicio remoto no está en ejecución (verifica que el router I2P esté ejecutándose en el servidor remoto) - Firewall bloqueando la conexión - Puerto de destino incorrecto

**Solución**: Verifica que el router I2P esté funcionando en el servidor remoto:

```bash
ssh user@remote-server "systemctl status i2p"
```
### Configuración de Clave SSH en Mac

**Error**: "Permiso denegado" o "Autenticación fallida"

**Posibles causas**: - Nombre de usuario o contraseña incorrectos - Clave SSH no configurada correctamente - Acceso SSH deshabilitado en el servidor remoto

**Solución**: Verifique las credenciales y asegúrese de que el acceso SSH esté habilitado en el servidor remoto.

### Tunnel Drops Connection

**Error**: La conexión se interrumpe después de un período de inactividad

**Solución**: Agrega configuraciones de keep-alive a tu configuración de SSH (`~/.ssh/config`):

```
Host remote-server
    ServerAliveInterval 60
    ServerAliveCountMax 3
```
## Security Best Practices

- **Use claves SSH**: Más seguras que las contraseñas, más difíciles de comprometer
- **Deshabilite la autenticación por contraseña**: Una vez configuradas las claves SSH, deshabilite el inicio de sesión por contraseña en el servidor
- **Use contraseñas fuertes**: Si utiliza autenticación por contraseña, use una contraseña fuerte y única
- **Limite el acceso SSH**: Configure reglas de firewall para limitar el acceso SSH a IPs de confianza
- **Mantenga SSH actualizado**: Actualice regularmente el software de su cliente y servidor SSH
- **Monitoree los registros**: Revise los registros SSH en el servidor en busca de actividad sospechosa
- **Use puertos SSH no estándar**: Cambie el puerto SSH predeterminado (22) para reducir ataques automatizados

## Creación de túneles SSH en Linux

### Accediendo a la Consola I2P

Crea un script para establecer túneles automáticamente:

```bash
#!/bin/bash
# i2p-tunnel.sh

ssh -f -N -L 7657:127.0.0.1:7657 i2p@20.228.143.58
echo "I2P tunnel established"
```
Hazlo ejecutable:

```bash
chmod +x i2p-tunnel.sh
./i2p-tunnel.sh
```
### Múltiples Túneles

Crea un servicio systemd para la creación automática de túneles:

```bash
sudo nano /etc/systemd/system/i2p-tunnel.service
```
Añadir:

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
Habilitar e iniciar:

```bash
sudo systemctl enable i2p-tunnel
sudo systemctl start i2p-tunnel
```
## Advanced Tunneling

### Puerto Local Personalizado

Crear un proxy SOCKS para reenvío dinámico:

```bash
ssh -D 8080 user@remote-server
```
Configura tu navegador para usar `127.0.0.1:8080` como proxy SOCKS5.

### Reverse Tunneling

Permite que el servidor remoto acceda a servicios en tu máquina local:

```bash
ssh -R 7657:127.0.0.1:7657 user@remote-server
```
### Puerto Ya en Uso

Túnel a través de un servidor intermedio:

```bash
ssh -J jumphost.example.com -L 7657:127.0.0.1:7657 user@final-server
```
## Conclusion

El túnel SSH es una herramienta poderosa para acceder de forma segura a routers I2P remotos y otros servicios. Ya sea que uses Windows, Linux o Mac, el proceso es sencillo y proporciona un cifrado robusto para tus conexiones.

Para obtener ayuda adicional o realizar preguntas, visita la comunidad de I2P: - **Foro**: [i2pforum.net](https://i2pforum.net) - **IRC**: #i2p en varias redes - **Documentación**: [Documentación de I2P](/docs/)

---

*Guía creada originalmente por [Stormy Cloud](https://www.stormycloud.org), adaptada para la documentación de I2P.*
