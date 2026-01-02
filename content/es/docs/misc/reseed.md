---
title: "Servidores de Reseed (proceso de arranque inicial para obtener pares)"
description: "Operación de los servicios de reseed (abastecimiento inicial de nodos) y métodos alternativos de arranque inicial"
slug: "reseed"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

## Acerca de los servidores Reseed (servidores de arranque de I2P)

Los routers nuevos necesitan un puñado de pares para unirse a la red I2P. Los reseed hosts (servidores que suministran el conjunto de arranque inicial) proporcionan ese conjunto a través de descargas HTTPS cifradas. Cada reseed bundle (paquete de reseed) está firmado por el host, lo que impide manipulaciones por parte de terceros no autenticados. Los routers ya establecidos pueden realizar reseed ocasionalmente si su conjunto de pares se vuelve obsoleto.

### Proceso de Bootstrap (arranque inicial) de la red

Cuando un router I2P se inicia por primera vez o ha estado desconectado durante un período prolongado, necesita datos de RouterInfo (información del router) para conectarse a la red. Dado que el router no tiene pares existentes, no puede obtener esta información desde dentro de la propia red I2P. El mecanismo de reseed (proceso de arranque inicial) resuelve este problema de arranque proporcionando archivos RouterInfo desde servidores HTTPS externos de confianza.

El proceso de reseed (proceso de arranque desde servidores de semillas) entrega 75-100 archivos RouterInfo en un único paquete firmado criptográficamente. Esto garantiza que los routers nuevos puedan establecer conexiones rápidamente sin exponerlos a ataques de intermediario que podrían aislarlos en particiones de red separadas y no confiables.

### Estado actual de la red

A octubre de 2025, la red I2P opera con la versión de router 2.10.0 (versión de la API 0.9.67). El protocolo de reseed (proceso de obtención inicial de pares) introducido en la versión 0.9.14 se mantiene estable y sin cambios en su funcionalidad básica. La red mantiene varios servidores de reseed independientes distribuidos a nivel mundial para garantizar la disponibilidad y la resistencia a la censura.

El servicio [checki2p](https://checki2p.com/reseed) supervisa todos los servidores de reseed de I2P (servicios de arranque inicial de la red que proporcionan datos iniciales del netDb) cada 4 horas, proporcionando comprobaciones de estado en tiempo real y métricas de disponibilidad para la infraestructura de reseed.

## Especificación del formato de archivo SU3

El formato de archivo SU3 es la base del protocolo de reseed (proceso de arranque inicial de pares) de I2P, y permite la entrega de contenido firmado criptográficamente. Comprender este formato es esencial para implementar servidores y clientes de reseed.

### Estructura de archivos

El formato SU3 consta de tres componentes principales: encabezado (40+ bytes), contenido (longitud variable) y firma (longitud especificada en el encabezado).

#### Formato del encabezado (Bytes 0-39 como mínimo)

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Byte Range</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Field</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">0-5</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Magic Number</td><td style="border:1px solid var(--color-border); padding:0.5rem;">ASCII string "I2Psu3" (0x493250737533)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">6</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Unused, must be 0x00</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">7</td><td style="border:1px solid var(--color-border); padding:0.5rem;">File Format Version</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Current version: 0x00</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">8-9</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Signature Type</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big-endian 16-bit integer. Type 6 = RSA-4096-SHA512 (reseed standard)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">10-11</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Signature Length</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big-endian 16-bit integer. 512 bytes (0x0200) for RSA-4096</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Unused, must be 0x00</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">13</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Version Length</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Minimum 16 bytes (0x10) for compatibility</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">14</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Unused, must be 0x00</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">15</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Signer ID Length</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Length of UTF-8 signer identifier string</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">16-23</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Content Length</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big-endian 64-bit integer, length of content in bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">24</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Unused, must be 0x00</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">25</td><td style="border:1px solid var(--color-border); padding:0.5rem;">File Type</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0x00 = ZIP, 0x01 = XML, 0x02 = HTML, 0x03 = XML.GZ, 0x04 = TXT.GZ, 0x05 = DMG, 0x06 = EXE</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">26</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Unused, must be 0x00</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">27</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Content Type</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0x00 = unknown, 0x01 = router update, 0x02 = plugin, 0x03 = reseed, 0x04 = news, 0x05 = blocklist</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">28-39</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Padding</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Unused, must be all zeros</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">40-55</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Version String</td><td style="border:1px solid var(--color-border); padding:0.5rem;">ASCII version string, padded with zeros (minimum 16 bytes)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">56-...</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Signer ID</td><td style="border:1px solid var(--color-border); padding:0.5rem;">UTF-8 encoded signer identifier (e.g., "user@mail.i2p")</td></tr>
  </tbody>
</table>
### Parámetros SU3 específicos de Reseed (proceso de arranque de la red)

Para los paquetes de reseed (proceso de obtención de nodos iniciales de la red), el archivo SU3 debe tener las siguientes características:

- **Nombre de archivo**: Debe ser exactamente `i2pseeds.su3`
- **Tipo de contenido** (byte 27): 0x03 (RESEED)
- **Tipo de archivo** (byte 25): 0x00 (ZIP)
- **Tipo de firma** (bytes 8-9): 0x0006 (RSA-4096-SHA512)
- **Cadena de versión**: marca de tiempo Unix en ASCII (segundos desde la época Unix, formato date +%s)
- **ID del firmante**: identificador con formato de correo electrónico que coincide con el CN del certificado X.509

#### Parámetro de consulta del ID de red

Desde la versión 0.9.42, los routers añaden `?netid=2` a las solicitudes de reseed (arranque inicial). Esto evita las conexiones entre redes, ya que las redes de prueba usan distintos ID de red. La red de producción actual de I2P usa el ID de red 2.

Ejemplo de solicitud: `https://reseed.example.com/i2pseeds.su3?netid=2`

### Estructura del contenido del ZIP

La sección de contenido (después del encabezado, antes de la firma) contiene un archivo ZIP estándar con los siguientes requisitos:

- **Compresión**: Compresión ZIP estándar (DEFLATE)
- **Número de archivos**: Por lo general 75-100 archivos RouterInfo (información del router)
- **Estructura de directorios**: Todos los archivos deben estar en el nivel superior (sin subdirectorios)
- **Nombrado de archivos**: `routerInfo-{44-character-base64-hash}.dat`
- **Alfabeto Base64**: Debe usar el alfabeto Base64 modificado de I2P

El alfabeto base64 de I2P difiere del base64 estándar al usar `-` y `~` en lugar de `+` y `/` para garantizar la compatibilidad con el sistema de archivos y las URL.

### Firma criptográfica

La firma cubre todo el archivo desde el byte 0 hasta el final de la sección de contenido. La firma en sí se añade después del contenido.

#### Algoritmo de firma (RSA-4096-SHA512)

1. Calcular el hash SHA-512 de los bytes desde 0 hasta el final del contenido
2. Firmar el hash con RSA "raw" (NONEwithRSA en terminología de Java)
3. Rellenar la firma con ceros a la izquierda si es necesario para alcanzar 512 bytes
4. Añadir la firma de 512 bytes al archivo

#### Proceso de verificación de firmas

Los clientes deben:

1. Leer los bytes 0-11 para determinar el tipo y la longitud de la firma
2. Leer el encabezado completo para localizar los límites del contenido
3. Procesar el contenido como flujo mientras se calcula el hash SHA-512
4. Extraer la firma del final del archivo
5. Verificar la firma usando la clave pública RSA-4096 del firmante
6. Rechazar el archivo si falla la verificación de la firma

### Modelo de confianza de certificados

Las claves de firma de reseed (proceso de arranque/semillado inicial) se distribuyen como certificados X.509 autofirmados con claves RSA de 4096 bits. Estos certificados se incluyen en los paquetes del router de I2P en el directorio `certificates/reseed/`.

Formato del certificado: - **Tipo de clave**: RSA-4096 - **Firma**: Autofirmado - **CN del sujeto**: Debe coincidir con el ID del firmante en el encabezado SU3 - **Fechas de validez**: Los clientes deberían hacer cumplir los periodos de validez del certificado

## Ejecutar un host de Reseed (servidor que suministra a los routers listas iniciales de pares)

Operar un servicio de reseed (servicio que proporciona semillas iniciales de la red) requiere prestar mucha atención a los requisitos de seguridad, fiabilidad y diversidad de la red. Un mayor número de servidores de reseed independientes aumenta la resiliencia y dificulta que atacantes o censores bloqueen la incorporación de nuevos routers.

### Requisitos técnicos

#### Especificaciones del servidor

- **Sistema operativo**: Unix/Linux (Ubuntu, Debian, FreeBSD probados y recomendados)
- **Conectividad**: Se requiere dirección IPv4 estática, IPv6 recomendado pero opcional
- **CPU**: Mínimo 2 núcleos
- **RAM**: Mínimo 2 GB
- **Ancho de banda**: Aproximadamente 15 GB por mes
- **Tiempo de actividad**: Se requiere operación 24/7
- **I2P Router**: I2P router bien integrado ejecutándose continuamente

#### Requisitos de software

- **Java**: JDK 8 o posterior (se requerirá Java 17+ a partir de I2P 2.11.0)
- **Servidor web**: nginx o Apache con soporte de proxy inverso (Lighttpd ya no es compatible debido a limitaciones del encabezado X-Forwarded-For)
- **TLS/SSL**: Certificado TLS válido (Let's Encrypt, autofirmado o CA comercial)
- **Protección DDoS**: fail2ban o equivalente (obligatorio, no opcional)
- **Herramientas de reseed (proceso inicial de obtención de pares)**: reseed-tools oficiales de https://i2pgit.org/idk/reseed-tools

### Requisitos de seguridad

#### Configuración de HTTPS/TLS

- **Protocolo**: Solo HTTPS, sin alternativa HTTP
- **Versión de TLS**: Mínimo TLS 1.2
- **Conjuntos de cifrado**: Debe admitir conjuntos de cifrado fuertes compatibles con Java 8+
- **CN/SAN del certificado**: Debe coincidir con el nombre de host de la URL servida
- **Tipo de certificado**: Puede ser autofirmado si se comunica con el equipo de desarrollo, o emitido por una autoridad certificadora reconocida (CA)

#### Gestión de certificados

Los certificados de firma SU3 y los certificados TLS cumplen funciones diferentes:

- **Certificado TLS** (`certificates/ssl/`): Asegura el transporte HTTPS
- **Certificado de firma SU3** (`certificates/reseed/`): Firma paquetes de reseed (arranque inicial de la red)

Ambos certificados deben proporcionarse al coordinador de reseed (proceso de arranque inicial de la red) (zzz@mail.i2p) para su inclusión en los paquetes del router.

#### Protección contra DDoS y scraping (extracción automatizada de datos)

Los Reseed servers (servidores de arranque inicial de la red) se enfrentan a ataques periódicos de implementaciones defectuosas, botnets y actores maliciosos que intentan raspar la base de datos de la red. Las medidas de protección incluyen:

- **fail2ban**: Requerido para limitación de tasa y mitigación de ataques
- **Bundle Diversity**: Entregar diferentes conjuntos de RouterInfo (información del router) a distintos solicitantes
- **Bundle Consistency**: Entregar el mismo bundle (paquete) a solicitudes repetidas desde la misma IP dentro de una ventana de tiempo configurable
- **IP Logging Restrictions**: No hacer públicos los registros ni las direcciones IP (requisito de la política de privacidad)

### Métodos de implementación

#### Método 1: reseed-tools (conjunto de herramientas para reseed de I2P) oficiales (Recomendado)

La implementación canónica mantenida por el proyecto I2P. Repositorio: https://i2pgit.org/idk/reseed-tools

**Instalación**:

```bash
# Install dependencies
sudo apt-get install golang git

# Clone repository
git clone https://i2pgit.org/idk/reseed-tools.git
cd reseed-tools

# Build
make

# Generate keys and start server (first run)
./reseed-tools reseed \
  --signer=your-email@mail.i2p \
  --netdb=/path/to/i2p/netDb \
  --tlsHost=your-domain.tld \
  --port=8443
```
En la primera ejecución, la herramienta generará: - `your-email@mail.i2p.crt` (certificado de firma SU3) - `your-email@mail.i2p.pem` (clave privada de firma SU3) - `your-email@mail.i2p.crl` (lista de revocación de certificados) - archivos de certificado y clave TLS

**Características**: - Generación automática de SU3 bundle (paquete firmado de I2P) (350 variaciones, 77 RouterInfos (metadatos de router) cada una) - Servidor HTTPS integrado - Reconstruir la caché cada 9 horas mediante cron - Compatibilidad con el encabezado X-Forwarded-For con la opción `--trustProxy` - Compatible con configuraciones de proxy inverso

**Despliegue en producción**:

```bash
# Create systemd service
cat > /etc/systemd/system/i2p-reseed.service << EOF
[Unit]
Description=I2P Reseed Server
After=network.target

[Service]
Type=simple
User=i2p-reseed
WorkingDirectory=/opt/i2p-reseed
ExecStart=/opt/i2p-reseed/reseed-tools reseed \
  --signer=your-email@mail.i2p \
  --netdb=/var/lib/i2p/netDb \
  --port=8443 \
  --ip=127.0.0.1 \
  --trustProxy
Restart=always

[Install]
WantedBy=multi-user.target
EOF

systemctl enable i2p-reseed
systemctl start i2p-reseed
```
#### Método 2: Implementación en Python (pyseeder)

Implementación alternativa del proyecto PurpleI2P: https://github.com/PurpleI2P/pyseeder

```bash
pip install pyseeder

# Generate SU3 file
echo "your_password" | pyseeder reseed \
  --netdb /path/to/netDb \
  --private-key priv_key.pem \
  --outfile i2pseeds.su3 \
  --signer-id user@mail.i2p

# Serve via built-in server
pyseeder serve \
  --port 8443 \
  --host 0.0.0.0 \
  --private-key priv_key.pem \
  --cert user_at_mail.i2p.crt \
  --file i2pseeds.su3
```
#### Método 3: Despliegue con Docker

Para entornos contenedorizados, existen varias implementaciones preparadas para Docker:

- **DivaExchange i2p-reseed**: https://github.com/diva-exchange/i2p-reseed
- **RTradeLtd/i2p-tools-1**: Añade soporte para servicio onion de Tor y para IPFS

### Configuración de proxy inverso

#### Configuración de nginx

```nginx
upstream i2p_reseed {
    server 127.0.0.1:8443;
}

server {
    listen 443 ssl http2;
    server_name reseed.example.com;

    ssl_certificate /path/to/tls-cert.crt;
    ssl_certificate_key /path/to/tls-key.key;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;

    location / {
        proxy_pass http://i2p_reseed;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $remote_addr;
        proxy_set_header Host $host;
    }
}
```
#### Configuración de Apache

```apache
<VirtualHost *:443>
    ServerName reseed.example.com
    
    SSLEngine on
    SSLCertificateFile /path/to/tls-cert.crt
    SSLCertificateKeyFile /path/to/tls-key.key
    SSLProtocol all -SSLv2 -SSLv3 -TLSv1 -TLSv1.1
    
    ProxyRequests Off
    <Proxy *>
        Order deny,allow
        Allow from all
    </Proxy>
    
    ProxyPass / http://127.0.0.1:8443/
    ProxyPassReverse / http://127.0.0.1:8443/
</VirtualHost>
```
### Registro y coordinación

Para incluir tu reseed server (servidor de resembrado) en el paquete oficial de I2P:

1. Completa la configuración y las pruebas
2. Envía ambos certificados (firma SU3 y TLS) al coordinador de reseed (proceso para obtener pares iniciales de la red)
3. Contacto: zzz@mail.i2p o zzz@i2pmail.org
4. Únete a #i2p-dev en IRC2P para coordinarte con otros operadores

### Mejores prácticas operativas

#### Supervisión y registro

- Habilitar el formato de registro combinado de Apache/nginx para estadísticas
- Implementar la rotación de registros (los registros crecen rápidamente)
- Supervisar el éxito de la generación del paquete y los tiempos de reconstrucción
- Hacer seguimiento del uso de ancho de banda y de los patrones de solicitudes
- Nunca divulgar direcciones IP ni registros de acceso detallados

#### Calendario de mantenimiento

- **Cada 9 horas**: Reconstruir la caché del paquete SU3 (automatizado mediante cron)
- **Semanalmente**: Revisar los registros en busca de patrones de ataque
- **Mensualmente**: Actualizar el I2P router y reseed-tools
- **Según sea necesario**: Renovar los certificados TLS (automatizar con Let's Encrypt)

#### Selección de puertos

- Predeterminado: 8443 (recomendado)
- Alternativa: Cualquier puerto entre 1024 y 49151
- Puerto 443: Requiere privilegios de root o redirección de puertos (se recomienda la redirección con iptables)

Ejemplo de reenvío de puertos:

```bash
iptables -A PREROUTING -t nat -p tcp --dport 443 -j REDIRECT --to-port 8443
```
## Métodos alternativos de reseed (obtención inicial de pares)

Otras opciones de arranque ayudan a los usuarios detrás de redes restrictivas:

### Reseed (proceso de arranque inicial de la red) basado en archivos

Introducido en la versión 0.9.16, el resembrado basado en archivos permite a los usuarios cargar manualmente paquetes de RouterInfo. Este método es particularmente útil para usuarios en regiones con censura donde los servidores de resembrado HTTPS están bloqueados.

**Proceso**: 1. Un contacto de confianza genera un paquete SU3 usando su router 2. El paquete se transfiere por correo electrónico, unidad USB u otro canal fuera de banda 3. El usuario coloca `i2pseeds.su3` en el directorio de configuración de I2P 4. El router detecta y procesa automáticamente el paquete al reiniciar

**Documentación**: /blog/2020/06/07/help-your-friends-join-i2p-by-sharing-reseed-bundles/

**Casos de uso**: - Usuarios detrás de cortafuegos nacionales que bloquean reseed servers (servidores de arranque) - Redes aisladas que requieren arranque manual - Entornos de prueba y desarrollo

### Resembrado a través del proxy de Cloudflare

Enrutar el tráfico de reseed (obtención inicial de pares) a través de la CDN de Cloudflare ofrece varias ventajas para los operadores en regiones con alta censura.

**Beneficios**: - Dirección IP del servidor de origen oculta a los clientes - Protección contra DDoS mediante la infraestructura de Cloudflare - Distribución geográfica de la carga mediante caché perimetral - Mejor rendimiento para clientes en todo el mundo

**Requisitos de implementación**: - opción `--trustProxy` habilitada en reseed-tools - Proxy de Cloudflare habilitado para el registro DNS - Manejo correcto del encabezado X-Forwarded-For

**Consideraciones importantes**: - Se aplican las restricciones de puertos de Cloudflare (debe usar puertos admitidos) - La consistencia de la agrupación por cliente requiere soporte para X-Forwarded-For - La configuración de SSL/TLS está gestionada por Cloudflare

**Documentación**: https://homepage.np-tokumei.net/post/notes-i2p-reseed-over-cloudflare/

### Estrategias resistentes a la censura

La investigación de Nguyen Phong Hoang (USENIX FOCI 2019) identifica métodos de arranque adicionales para redes censuradas:

#### Proveedores de almacenamiento en la nube

- **Box, Dropbox, Google Drive, OneDrive**: Alojar archivos SU3 en enlaces públicos
- **Ventaja**: Difícil de bloquear sin interrumpir servicios legítimos
- **Limitación**: Requiere distribuir manualmente la URL a los usuarios

#### Distribución mediante IPFS

- Alojar paquetes de reseed (paquetes para resembrar la red) en InterPlanetary File System
- El almacenamiento direccionado por contenido impide la manipulación
- Resiliente frente a intentos de retirada

#### Servicios Onion de Tor

- Reseed servers (servidores de inicialización) accesibles mediante direcciones .onion
- Resistente al bloqueo basado en IP
- Requiere un cliente de Tor en el sistema del usuario

**Documentación de investigación**: https://homepage.np-tokumei.net/post/notes-censorship-resistant-i2p-reseeding/

#### Países donde se sabe que se bloquea I2P

A partir de 2025, se ha confirmado que los siguientes países bloquean los servidores de reseed de I2P (servidores de arranque de la red): - China - Irán - Omán - Catar - Kuwait

Los usuarios en estas regiones deberían utilizar métodos alternativos de bootstrap (proceso de arranque inicial) o estrategias de reseeding (obtención inicial de información de nodos de la red) resistentes a la censura.

## Detalles del protocolo para implementadores

### Especificación de la solicitud de reseed

#### Comportamiento del cliente

1. **Selección de servidor**: Router mantiene una lista codificada de forma fija de URLs de reseed (proceso de bootstrapping inicial)
2. **Selección aleatoria**: El cliente selecciona aleatoriamente un servidor de la lista disponible
3. **Formato de solicitud**: `GET /i2pseeds.su3?netid=2 HTTP/1.1`
4. **User-Agent**: Debe imitar navegadores comunes (p. ej., "Wget/1.11.4")
5. **Lógica de reintento**: Si la solicitud SU3 falla, recurrir al análisis de la página de índice
6. **Validación de certificado**: Verificar el certificado TLS contra el almacén de confianza del sistema
7. **Validación de la firma SU3**: Verificar la firma contra certificados de reseed conocidos

#### Comportamiento del servidor

1. **Selección de paquetes**: Seleccione un subconjunto seudoaleatorio de RouterInfos (información de router) de netDb
2. **Seguimiento de clientes**: Identifique las solicitudes por la IP de origen (respetando X-Forwarded-For)
3. **Consistencia del paquete**: Devuelva el mismo paquete a las solicitudes repetidas dentro de una ventana de tiempo (normalmente 8-12 horas)
4. **Diversidad de paquetes**: Devuelva paquetes diferentes a distintos clientes para la diversidad de la red
5. **Content-Type**: `application/octet-stream` o `application/x-i2p-reseed`

### Formato del archivo RouterInfo

Cada archivo `.dat` en el paquete de reseed contiene una estructura RouterInfo:

**Convención de nombres de archivos**: `routerInfo-{base64-hash}.dat` - El hash tiene 44 caracteres usando el alfabeto base64 de I2P - Ejemplo: `routerInfo-ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmn.dat`

**Contenido del archivo**: - RouterIdentity (identidad del router; hash del router, clave de cifrado, clave de firma) - Marca de tiempo de publicación - Direcciones del router (IP, puerto, tipo de transporte) - Capacidades y opciones del router - Firma que cubre todos los datos anteriores

### Requisitos de diversidad de la red

Para evitar la centralización de la red y permitir la detección de ataques Sybil:

- **No volcados completos de NetDb**: Nunca servir todos los RouterInfos (información del router) a un único cliente
- **Muestreo aleatorio**: Cada paquete contiene un subconjunto diferente de los pares disponibles
- **Tamaño mínimo del paquete**: 75 RouterInfos (aumentado desde los 50 originales)
- **Tamaño máximo del paquete**: 100 RouterInfos
- **Vigencia**: Los RouterInfos deben ser recientes (dentro de las 24 horas desde su generación)

### Consideraciones sobre IPv6

**Estado actual** (2025): - Varios servidores de reseed (servidores de resembrado) muestran falta de respuesta en IPv6 - Los clientes deberían preferir o forzar IPv4 para mayor fiabilidad - Se recomienda el soporte de IPv6 para nuevas implementaciones, pero no es crítico

**Nota de implementación**: Al configurar servidores de doble pila, asegúrese de que las direcciones de escucha tanto de IPv4 como de IPv6 funcionen correctamente, o deshabilite IPv6 si no se puede soportar adecuadamente.

## Consideraciones de seguridad

### Modelo de amenazas

El protocolo de reseed (proceso inicial para obtener información de routers de I2P) protege contra:

1. **Ataques de intermediario (man-in-the-middle)**: las firmas RSA-4096 evitan la manipulación del paquete
2. **Partición de la red**: múltiples servidores de reseed (servidores de aprovisionamiento inicial) independientes evitan un único punto de control
3. **Ataques Sybil**: la diversidad de paquetes limita la capacidad del atacante para aislar a los usuarios
4. **Censura**: múltiples servidores y métodos alternativos proporcionan redundancia

El protocolo reseed (resembrado) NO protege contra:

1. **Servidores de reseed comprometidos**: Si el atacante controla las claves privadas de los certificados de reseed (mecanismo de arranque inicial)
2. **Bloqueo completo de la red**: Si todos los métodos de reseed están bloqueados en una región
3. **Monitoreo a largo plazo**: Las solicitudes de reseed revelan la IP que intenta unirse a I2P

### Gestión de certificados

**Seguridad de claves privadas**: - Almacene las claves de firma SU3 fuera de línea cuando no se estén usando - Utilice contraseñas robustas para el cifrado de claves - Mantenga copias de seguridad seguras de las claves y certificados - Considere módulos de seguridad de hardware (HSMs) para implementaciones de alto valor

**Revocación de certificados**: - Listas de revocación de certificados (CRLs) distribuidas vía feed de noticias - Los certificados comprometidos pueden ser revocados por el coordinador - Routers actualizan automáticamente las CRLs con las actualizaciones de software

### Mitigación de ataques

**Protección contra DDoS**: - reglas de fail2ban para solicitudes excesivas - Limitación de tasa a nivel del servidor web - Límites de conexiones por dirección IP - Cloudflare o CDN similar para una capa adicional

**Prevención de scraping (extracción automatizada)**: - Paquetes diferentes por IP solicitante - Almacenamiento en caché de paquetes basado en el tiempo por IP - Registro de patrones que indiquen intentos de scraping - Coordinación con otros operadores sobre los ataques detectados

## Pruebas y validación

### Prueba de su servidor Reseed (servidor de arranque de I2P)

#### Método 1: Instalación limpia del router

1. Instale I2P en un sistema limpio
2. Añada su URL de reseed (proceso de arranque de pares) a la configuración
3. Elimine o desactive otras URL de reseed
4. Inicie el router y supervise los registros para confirmar un reseed exitoso
5. Verifique la conexión a la red en un plazo de 5–10 minutos

Salida de registro esperada:

```
Reseed got 77 router infos from https://your-reseed.example.com/i2pseeds.su3?netid=2 with 0 errors
Reseed complete, 77 received
```
#### Método 2: Validación manual de SU3 (formato de archivo de actualización firmado de I2P)

```bash
# Download bundle
curl -k -A "Wget/1.11.4" https://your-reseed.example.com/i2pseeds.su3 > test.su3

# Verify it's a valid SU3 file
hexdump -C test.su3 | head -n 3
# Should show: 49 32 50 73 75 33 (I2Psu3)

# Extract content (requires su3 tools)
java -cp /path/to/i2p.jar net.i2p.crypto.SU3File verify test.su3 your-cert.crt

# Unzip content
# (Extract content section, skip header+signature, then unzip)
```
#### Método 3: Monitoreo de checki2p

El servicio en https://checki2p.com/reseed realiza comprobaciones automatizadas cada 4 horas en todos los servidores de reseed (servidores de arranque que suministran pares iniciales) de I2P registrados. Esto proporciona:

- Supervisión de disponibilidad
- Métricas de tiempo de respuesta
- Validación de certificados TLS
- Verificación de firma SU3
- Datos históricos de tiempo de actividad

Una vez que su reseed (servidor de arranque) esté registrado en el proyecto I2P, aparecerá automáticamente en checki2p dentro de 24 horas.

### Solución de problemas comunes

**Problema**: "Unable to read signing key" en la primera ejecución - **Solución**: Esto es lo esperado. Responde 'y' para generar nuevas claves.

**Problema**: Router no logra verificar la firma - **Causa**: El certificado no está en el almacén de confianza del router - **Solución**: Coloca el certificado en el directorio `~/.i2p/certificates/reseed/`

**Problema**: Mismo paquete servido a diferentes clientes - **Causa**: el encabezado X-Forwarded-For no se reenvía correctamente - **Solución**: habilita `--trustProxy` y configura las cabeceras del proxy inverso

**Problema**: errores "Conexión rechazada" - **Causa**: Puerto no accesible desde Internet - **Solución**: Comprueba las reglas del firewall, verifica el reenvío de puertos

**Problema**: Alto uso de CPU durante la reconstrucción del paquete - **Causa**: Comportamiento normal al generar 350+ variantes SU3 - **Solución**: Asegúrese de contar con recursos de CPU adecuados, considere reducir la frecuencia de reconstrucción

## Información de referencia

### Documentación oficial

- **Guía para colaboradores de Reseed (proceso de sembrado inicial de pares de I2P)**: /guides/creating-and-running-an-i2p-reseed-server/
- **Requisitos de la política de Reseed**: /guides/reseed-policy/
- **Especificación de SU3**: /docs/specs/updates/
- **Repositorio de herramientas de Reseed**: https://i2pgit.org/idk/reseed-tools
- **Documentación de las herramientas de Reseed**: https://eyedeekay.github.io/reseed-tools/

### Implementaciones alternativas

- **PurpleI2P pyseeder**: https://github.com/PurpleI2P/pyseeder
- **DivaExchange i2p-reseed**: https://github.com/diva-exchange/i2p-reseed
- **RTradeLtd i2p-tools-1**: https://github.com/RTradeLtd/i2p-tools-1
- **Reseeder de Python WSGI**: https://github.com/torbjo/i2p-reseeder

### Recursos de la comunidad

- **Foro de I2P**: https://i2pforum.net/
- **Repositorio de Gitea**: https://i2pgit.org/I2P_Developers/i2p.i2p
- **IRC**: #i2p-dev en IRC2P
- **Supervisión del estado**: https://checki2p.com/reseed

### Historial de versiones

- **0.9.14** (2014): Se introduce el formato SU3 de reseed (proceso de incorporación inicial a la red mediante servidores semilla)
- **0.9.16** (2014): Añadido reseeding basado en archivos
- **0.9.42** (2019): Requisito del parámetro de consulta Network ID
- **2.0.0** (2022): Se introduce el protocolo de transporte SSU2
- **2.4.0** (2024): Aislamiento de NetDB y mejoras de seguridad
- **2.6.0** (2024): Conexiones I2P-over-Tor bloqueadas
- **2.10.0** (2025): Versión estable actual (a septiembre de 2025)

### Referencia de tipos de firma

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Code</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Algorithm</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Key Size</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Signature Size</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Hash</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">DSA-SHA1</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem;">DSA</td><td style="border:1px solid var(--color-border); padding:0.5rem;">1024-bit</td><td style="border:1px solid var(--color-border); padding:0.5rem;">40 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">SHA-1</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA-SHA256-P256</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA</td><td style="border:1px solid var(--color-border); padding:0.5rem;">P-256</td><td style="border:1px solid var(--color-border); padding:0.5rem;">64 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">SHA-256</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA-SHA384-P384</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA</td><td style="border:1px solid var(--color-border); padding:0.5rem;">P-384</td><td style="border:1px solid var(--color-border); padding:0.5rem;">96 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">SHA-384</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA-SHA512-P521</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA</td><td style="border:1px solid var(--color-border); padding:0.5rem;">P-521</td><td style="border:1px solid var(--color-border); padding:0.5rem;">132 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">SHA-512</td></tr>
    <tr><td style="border:1px solidvar(--color-border); padding:0.5rem;">RSA-SHA256-2048</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4</td><td style="border:1px solid var(--color-border); padding:0.5rem;">RSA</td><td style="border:1px solid var(--color-border); padding:0.5rem;">2048-bit</td><td style="border:1px solid var(--color-border); padding:0.5rem;">256 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">SHA-256</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RSA-SHA384-3072</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">5</td><td style="border:1px solid var(--color-border); padding:0.5rem;">RSA</td><td style="border:1px solid var(--color-border); padding:0.5rem;">3072-bit</td><td style="border:1px solid var(--color-border); padding:0.5rem;">384 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">SHA-384</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RSA-SHA512-4096</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">6</td><td style="border:1px solid var(--color-border); padding:0.5rem;">RSA</td><td style="border:1px solid var(--color-border); padding:0.5rem;">4096-bit</td><td style="border:1px solid var(--color-border); padding:0.5rem;">512 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">SHA-512</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">EdDSA-SHA512-Ed25519</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">7</td><td style="border:1px solid var(--color-border); padding:0.5rem;">EdDSA</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Ed25519</td><td style="border:1px solid var(--color-border); padding:0.5rem;">64 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">SHA-512</td></tr>
  </tbody>
</table>
**Estándar de reseed (incorporación inicial a la red)**: Se requiere el Tipo 6 (RSA-SHA512-4096) para los paquetes de reseed.

## Agradecimientos

Gracias a cada operador de reseed (servidor que proporciona pares iniciales) por mantener la red accesible y resiliente. Reconocimiento especial a los siguientes colaboradores y proyectos:

- **zzz**: Veterano desarrollador de I2P y coordinador de reseed (proceso de arranque/bootstrapping de I2P)
- **idk**: Mantenedor actual de reseed-tools y responsable de lanzamientos
- **Nguyen Phong Hoang**: Investigación sobre estrategias de reseeding resistentes a la censura
- **PurpleI2P Team**: Implementaciones alternativas de I2P y herramientas
- **checki2p**: Servicio de monitoreo automatizado para la infraestructura de reseed

La infraestructura de reseed (proceso de arranque inicial para obtener pares) descentralizada de la red I2P representa un esfuerzo colaborativo de docenas de operadores en todo el mundo, garantizando que los nuevos usuarios siempre puedan encontrar una ruta para unirse a la red, independientemente de la censura local o de las barreras técnicas.
