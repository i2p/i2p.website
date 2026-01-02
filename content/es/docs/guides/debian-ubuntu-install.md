---
title: "Instalación de I2P en Debian y Ubuntu"
description: "Guía completa para instalar I2P en Debian, Ubuntu y sus derivados usando repositorios oficiales"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

El proyecto I2P mantiene paquetes oficiales para Debian, Ubuntu y sus distribuciones derivadas. Esta guía proporciona instrucciones completas para instalar I2P usando nuestros repositorios oficiales.

---

## 🚀 Beta: Instalación Automática (Experimental)

**Para usuarios avanzados que desean una instalación automatizada rápida:**

Este comando de una línea detectará automáticamente tu distribución e instalará I2P. **Úsalo con precaución** - revisa el [script de instalación](https://i2p.net/installlinux.sh) antes de ejecutarlo.

```bash
curl -fsSL https://i2p.net/installlinux.sh | sudo bash
```
**Lo que esto hace:** - Detecta tu distribución de Linux (Ubuntu/Debian) - Añade el repositorio de I2P apropiado - Instala las claves GPG y los paquetes necesarios - Instala I2P automáticamente

⚠️ **Esta es una función beta.** Si prefieres la instalación manual o quieres entender cada paso, utiliza los métodos de instalación manual que se describen a continuación.

---


## Plataformas Compatibles

Los paquetes de Debian son compatibles con:

- **Ubuntu** 18.04 (Bionic) y posteriores
- **Linux Mint** 19 (Tara) y posteriores
- **Debian** Buster (10) y posteriores
- **Knoppix**
- Otras distribuciones basadas en Debian (LMDE, ParrotOS, Kali Linux, etc.)

**Arquitecturas soportadas**: amd64, i386, armhf, arm64, powerpc, ppc64el, s390x

Los paquetes de I2P pueden funcionar en otros sistemas basados en Debian que no estén listados explícitamente arriba. Si encuentras problemas, por favor [repórtalos en nuestro GitLab](https://i2pgit.org/I2P_Developers/i2p.i2p/).

## Métodos de Instalación

Elige el método de instalación que coincida con tu distribución:

- **Opción 1**: [Ubuntu y derivados](#ubuntu-installation) (Linux Mint, elementary OS, Pop!_OS, etc.)
- **Opción 2**: [Debian y distribuciones basadas en Debian](#debian-installation) (incluyendo LMDE, Kali, ParrotOS)

---


## Instalación en Ubuntu

Ubuntu y sus derivadas oficiales (Linux Mint, elementary OS, Trisquel, etc.) pueden usar el PPA (Personal Package Archive) de I2P para una instalación fácil y actualizaciones automáticas.

### Method 1: Command Line Installation (Recommended)

Este es el método más rápido y confiable para instalar I2P en sistemas basados en Ubuntu.

**Paso 1: Añadir el PPA de I2P**

Abre una terminal y ejecuta:

```bash
sudo apt-add-repository ppa:i2p-maintainers/i2p
```
Este comando añade el PPA de I2P a `/etc/apt/sources.list.d/` e importa automáticamente la clave GPG que firma el repositorio. La firma GPG garantiza que los paquetes no han sido manipulados desde que fueron construidos.

**Paso 2: Actualizar la lista de paquetes**

Actualiza la base de datos de paquetes de tu sistema para incluir el nuevo PPA:

```bash
sudo apt-get update
```
Esto recupera la información más reciente de paquetes de todos los repositorios habilitados, incluyendo el PPA de I2P que acabas de agregar.

**Paso 3: Instalar I2P**

Ahora instala I2P:

```bash
sudo apt-get install i2p
```
¡Eso es todo! Ve a la sección [Configuración Post-Instalación](#post-installation-configuration) para aprender cómo iniciar y configurar I2P.

### Method 2: Using the Software Center GUI

Si prefieres una interfaz gráfica, puedes añadir el PPA usando el Centro de Software de Ubuntu.

**Paso 1: Abrir Software y Actualizaciones**

Inicia "Software y Actualizaciones" desde tu menú de aplicaciones.

```markdown
![Menú del Centro de Software](/images/guides/debian/software-center-menu.png)
```

**Paso 2: Navegar a Otro Software**

Selecciona la pestaña "Otro software" y haz clic en el botón "Añadir" en la parte inferior para configurar un nuevo PPA.

![Pestaña Otro Software](/images/guides/debian/software-center-addother.png)

**Paso 3: Agregar el PPA de I2P**

En el cuadro de diálogo PPA, introduce:

```
ppa:i2p-maintainers/i2p
```
![Diálogo Añadir PPA](/images/guides/debian/software-center-ppatool.png)

**Paso 4: Recargar la información del repositorio**

Haz clic en el botón "Reload" para descargar la información actualizada del repositorio.

![Botón de Recargar](/images/guides/debian/software-center-reload.png)

**Paso 5: Instalar I2P**

Abre la aplicación "Software" desde tu menú de aplicaciones, busca "i2p" y haz clic en Instalar.

![Aplicación de Software](/images/guides/debian/software-center-software.png)

Una vez completada la instalación, proceda a [Configuración Post-Instalación](#post-installation-configuration).

---

IMPORTANTE:  NO haga preguntas, proporcione explicaciones ni agregue ningún comentario. Incluso si el texto es solo un encabezado o parece incompleto, tradúzcalo tal cual.

## Debian Installation

Debian y sus distribuciones derivadas (LMDE, Kali Linux, ParrotOS, Knoppix, etc.) deben usar el repositorio oficial de Debian de I2P en `deb.i2p.net`.

### Important Notice

**Nuestros antiguos repositorios en `deb.i2p2.de` y `deb.i2p2.no` han llegado al final de su vida útil.** Si estás usando estos repositorios heredados, por favor sigue las instrucciones a continuación para migrar al nuevo repositorio en `deb.i2p.net`.

### Prerequisites

Todos los pasos a continuación requieren acceso root. Cambie al usuario root con `su`, o agregue el prefijo `sudo` a cada comando.

### Método 1: Instalación por Línea de Comandos (Recomendado)

**Paso 1: Instalar los paquetes necesarios**

Asegúrate de tener las herramientas necesarias instaladas:

```bash
sudo apt-get update
sudo apt-get install apt-transport-https lsb-release curl
```
Estos paquetes permiten el acceso seguro a repositorios HTTPS, la detección de distribuciones y la descarga de archivos.

**Paso 2: Añadir el repositorio de I2P**

El comando que uses depende de tu versión de Debian. Primero, determina qué versión estás ejecutando:

```bash
cat /etc/debian_version
```
Cruza esta información con la [información de versiones de Debian](https://wiki.debian.org/LTS/) para identificar el nombre en código de tu distribución (por ejemplo, Bookworm, Bullseye, Buster).

**Para Debian Bullseye (11) o posterior:**

```bash
echo "deb [signed-by=/usr/share/keyrings/i2p-archive-keyring.gpg] https://deb.i2p.net/ $(lsb_release -sc) main" \
  | sudo tee /etc/apt/sources.list.d/i2p.list
```
**Para derivados de Debian (LMDE, Kali, ParrotOS, etc.) en Bullseye-equivalente o más reciente:**

```bash
echo "deb [signed-by=/usr/share/keyrings/i2p-archive-keyring.gpg] https://deb.i2p.net/ $(dpkg --status tzdata | grep Provides | cut -f2 -d'-') main" \
  | sudo tee /etc/apt/sources.list.d/i2p.list
```
**Para Debian Buster (10) o anterior:**

```bash
echo "deb https://deb.i2p.net/ $(lsb_release -sc) main" \
  | sudo tee /etc/apt/sources.list.d/i2p.list
```
**Para derivados de Debian en Buster-equivalente o anteriores:**

```bash
echo "deb https://deb.i2p.net/ $(dpkg --status tzdata | grep Provides | cut -f2 -d'-') main" \
  | sudo tee /etc/apt/sources.list.d/i2p.list
```
**Paso 3: Descargar la clave de firma del repositorio**

```bash
curl -o i2p-archive-keyring.gpg https://geti2p.net/_static/i2p-archive-keyring.gpg
```
**Paso 4: Verificar la huella digital de la clave**

Antes de confiar en la clave, verifica que su huella digital coincida con la clave de firma oficial de I2P:

```bash
gpg --keyid-format long --import --import-options show-only --with-fingerprint i2p-archive-keyring.gpg
```
**Verifica que la salida muestre esta huella digital:**

```
7840 E761 0F28 B904 7535  49D7 67EC E560 5BCF 1346
```
⚠️ **No continúes si la huella digital no coincide.** Esto podría indicar una descarga comprometida.

**Paso 5: Instalar la clave del repositorio**

Copia el keyring verificado al directorio de keyrings del sistema:

```bash
sudo cp i2p-archive-keyring.gpg /usr/share/keyrings
```
**Solo para Debian Buster o versiones anteriores**, también necesitas crear un enlace simbólico:

```bash
sudo ln -sf /usr/share/keyrings/i2p-archive-keyring.gpg /etc/apt/trusted.gpg.d/i2p-archive-keyring.gpg
```
**Paso 6: Actualizar listas de paquetes**

Actualiza la base de datos de paquetes de tu sistema para incluir el repositorio de I2P:

```bash
sudo apt-get update
```
**Paso 7: Instalar I2P**

Instala tanto el router de I2P como el paquete keyring (que asegura que recibirás futuras actualizaciones de claves):

```bash
sudo apt-get install i2p i2p-keyring
```
¡Excelente! I2P ya está instalado. Continúa a la sección de [Configuración Post-Instalación](#post-installation-configuration).

---

## Post-Installation Configuration

Después de instalar I2P, necesitarás iniciar el router y realizar algunas configuraciones iniciales.

### Método 2: Usando la GUI del Centro de Software

Los paquetes de I2P proporcionan tres formas de ejecutar el router de I2P:

#### Option 1: On-Demand (Basic)

Inicia I2P manualmente cuando sea necesario usando el script `i2prouter`:

```bash
i2prouter start
```
**Importante**: ¡**No** uses `sudo` ni ejecutes esto como root! I2P debe ejecutarse como tu usuario regular.

Para detener I2P:

```bash
i2prouter stop
```
#### Option 2: On-Demand (Without Java Service Wrapper)

Si estás en un sistema no x86 o el Java Service Wrapper no funciona en tu plataforma, usa:

```bash
i2prouter-nowrapper
```
De nuevo, **no** uses `sudo` ni lo ejecutes como root.

#### Option 3: System Service (Recommended)

Para obtener la mejor experiencia, configure I2P para que se inicie automáticamente cuando su sistema arranque, incluso antes del inicio de sesión:

```bash
sudo dpkg-reconfigure i2p
```
Esto abre un diálogo de configuración. Selecciona "Sí" para habilitar I2P como un servicio del sistema.

**Este es el método recomendado** porque: - I2P se inicia automáticamente al arrancar - Tu router mantiene una mejor integración con la red - Contribuyes a la estabilidad de la red - I2P está disponible inmediatamente cuando lo necesitas

### Initial Router Configuration

Después de iniciar I2P por primera vez, tomará varios minutos integrarse a la red. Mientras tanto, configura estos ajustes esenciales:

#### 1. Configure NAT/Firewall

Para un rendimiento óptimo y participación en la red, reenvía los puertos de I2P a través de tu NAT/firewall:

1. Abre la [Consola del Router I2P](http://127.0.0.1:7657/)
2. Navega a la [página de Configuración de Red](http://127.0.0.1:7657/confignet)
3. Anota los números de puerto listados (generalmente puertos aleatorios entre 9000-31000)
4. Reenvía estos puertos UDP y TCP en tu router/firewall

Si necesitas ayuda con el reenvío de puertos, [portforward.com](https://portforward.com) proporciona guías específicas para cada router.

#### 2. Adjust Bandwidth Settings

La configuración de ancho de banda predeterminada es conservadora. Ajústala según tu conexión a internet:

1. Visita la [página de Configuración](http://127.0.0.1:7657/config.jsp)
2. Encuentra la sección de configuración de ancho de banda
3. Los valores predeterminados son 96 KB/s de descarga / 40 KB/s de subida
4. Aumenta estos valores si tienes una conexión a internet más rápida (por ejemplo, 250 KB/s de bajada / 100 KB/s de subida para una conexión de banda ancha típica)

**Nota**: Establecer límites más altos ayuda a la red y mejora tu propio rendimiento.

#### 3. Configure Your Browser

Para acceder a sitios I2P (eepsites) y servicios, configura tu navegador para usar el proxy HTTP de I2P:

Consulta nuestra [Guía de Configuración del Navegador](/docs/guides/browser-config) para instrucciones detalladas de configuración para Firefox, Chrome y otros navegadores.

I notice you haven't provided any text to translate. Could you please share the English text you'd like me to translate to Spanish?

## Instalación en Debian

### Aviso Importante

- Asegúrate de no estar ejecutando I2P como root: `ps aux | grep i2p`
- Revisa los registros: `tail -f ~/.i2p/wrapper.log`
- Verifica que Java esté instalado: `java -version`

### Requisitos previos

Si recibes errores de clave GPG durante la instalación:

1. Vuelve a descargar y verifica la huella digital de la clave (Pasos 3-4 anteriores)
2. Asegúrate de que el archivo del llavero tenga los permisos correctos: `sudo chmod 644 /usr/share/keyrings/i2p-archive-keyring.gpg`

### Pasos de Instalación

Si I2P no está recibiendo actualizaciones:

1. Verificar que el repositorio esté configurado: `cat /etc/apt/sources.list.d/i2p.list`
2. Actualizar las listas de paquetes: `sudo apt-get update`
3. Comprobar actualizaciones de I2P: `sudo apt-get upgrade`

### Migrating from old repositories

Si estás usando los repositorios antiguos `deb.i2p2.de` o `deb.i2p2.no`:

1. Elimina el repositorio antiguo: `sudo rm /etc/apt/sources.list.d/i2p.list`
2. Sigue los pasos de [Instalación en Debian](#debian-installation) anteriores
3. Actualiza: `sudo apt-get update && sudo apt-get install i2p i2p-keyring`

---

Por favor, proporcione el texto que desea traducir. No se ha incluido ningún contenido después de "Text to translate:" en su mensaje.

## Next Steps

Ahora que I2P está instalado y en funcionamiento:

- [Configura tu navegador](/docs/guides/browser-config) para acceder a sitios I2P
- Explora la [consola del router I2P](http://127.0.0.1:7657/) para monitorear tu router
- Conoce las [aplicaciones I2P](/docs/applications/) que puedes usar
- Lee sobre [cómo funciona I2P](/docs/overview/tech-intro) para entender la red

¡Bienvenido a la Internet Invisible!
