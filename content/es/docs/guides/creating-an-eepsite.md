---
title: "Creación de un I2P Eepsite"
description: "Aprende cómo crear y alojar tu propio sitio web en la red I2P usando el servidor web Jetty integrado"
lastUpdated: "2025-11"
toc: true
---

## ¿Qué es un Eepsite?

Un **eepsite** (sitio web dentro de I2P) es un sitio web que existe exclusivamente en la red I2P. A diferencia de los sitios web tradicionales accesibles a través de la clearnet (internet abierta), a los eepsites solo se puede acceder mediante I2P, lo que ofrece anonimato y privacidad tanto para el operador del sitio como para los visitantes. Eepsites utilizan el seudodominio de nivel superior `.i2p` y se accede a ellos a través de direcciones `.b32.i2p` especiales o de nombres legibles por humanos registrados en la libreta de direcciones de I2P.

Todas las implementaciones de I2P en Java incluyen [Jetty](https://jetty.org/index.html), un servidor web ligero basado en Java, preinstalado y preconfigurado. Esto hace que sea sencillo empezar a alojar tu propio eepsite en cuestión de minutos - no se requiere instalación de software adicional.

Esta guía te llevará a través del proceso de crear y configurar tu primer eepsite utilizando las herramientas integradas de I2P.

---

## Paso 1: Accede al Administrador de Servicios Ocultos

El Administrador de Servicios Ocultos (también llamado I2P Tunnel Manager) es donde configuras todos los tunnels de servidor y de cliente de I2P, incluidos los servidores HTTP (eepsites).

1. Abre tu [Consola del Router de I2P](http://127.0.0.1:7657)
2. Ve al [Administrador de Servicios Ocultos](http://127.0.0.1:7657/i2ptunnelmgr)

Deberías ver la interfaz del Administrador de Servicios Ocultos mostrando: - **Mensajes de estado** - Estado actual de tunnel y del cliente - **Control global de tunnel** - Botones para administrar todos los tunnels a la vez - **Servicios ocultos de I2P** - Lista de tunnels de servidor configurados

![Administrador de servicios ocultos](/images/guides/eepsite/hidden-services-manager.png)

De forma predeterminada, verás una entrada existente de **servidor web de I2P** configurada pero no iniciada. Se trata del servidor web Jetty preconfigurado, listo para que lo uses.

---

## Paso 2: Configura los ajustes del servidor de tu Eepsite

Haz clic en la entrada **I2P webserver** en la lista de Servicios ocultos para abrir la página de configuración del servidor. Aquí podrás personalizar los ajustes de tu eepsite (sitio web alojado en I2P).

![Configuración del servidor de Eepsite](/images/guides/eepsite/webserver-settings.png)

### Explicación de las opciones de configuración

**Nombre** - Este es un identificador interno para tu tunnel - Útil si estás ejecutando múltiples eepsites para llevar un registro de cuál es cuál - Predeterminado: "I2P webserver"

**Descripción** - Una breve descripción de tu eepsite para tu propia referencia - Solo visible para ti en el Administrador de Servicios Ocultos - Ejemplo: "Mi eepsite" o "Blog personal"

**Auto Start Tunnel** - **Importante**: Marca esta casilla para iniciar automáticamente tu eepsite cuando se inicie tu router I2P - Garantiza que tu sitio permanezca disponible sin intervención manual tras los reinicios del router - Recomendado: **Activado**

**Destino (Host y Puerto)** - **Host**: La dirección local donde se está ejecutando tu servidor web (predeterminado: `127.0.0.1`) - **Puerto**: El puerto en el que escucha tu servidor web (predeterminado: `7658` para Jetty) - Si estás usando el servidor web Jetty preinstalado, **déjalos con los valores predeterminados** - Solo cambia esto si estás ejecutando un servidor web personalizado en un puerto diferente

**Nombre de host del sitio web** - Este es el nombre de dominio `.i2p` legible por humanos de tu eepsite - Predeterminado: `mysite.i2p` (marcador de posición) - Puedes registrar un dominio personalizado como `stormycloud.i2p` o `myblog.i2p` - Déjalo en blanco si solo quieres usar la dirección `.b32.i2p` generada automáticamente (para outproxies (proxies de salida)) - Consulta [Registrar tu dominio I2P](#registering-your-i2p-domain) más abajo para saber cómo reclamar un nombre de host personalizado

**Destino local** - Este es el identificador criptográfico único de tu eepsite (sitio web dentro de I2P) (dirección de destino) - Se genera automáticamente cuando el tunnel se crea por primera vez - Piensa en esto como la "dirección IP" permanente de tu sitio en I2P - La cadena alfanumérica larga es la dirección `.b32.i2p` de tu sitio en forma codificada

**Archivo de clave privada** - Ubicación donde se almacenan las claves privadas de tu eepsite - Predeterminado: `eepsite/eepPriv.dat` - **Mantén este archivo seguro** - cualquiera que tenga acceso a este archivo puede hacerse pasar por tu eepsite - Nunca compartas ni elimines este archivo

### Nota importante

El recuadro de advertencia amarillo te recuerda que, para habilitar las funciones de generación de códigos QR o de autenticación de registro, debes configurar un nombre de host del sitio web con un sufijo `.i2p` (p. ej., `mynewsite.i2p`).

---

## Paso 3: Opciones avanzadas de red (Opcional)

Si te desplazas hacia abajo en la página de configuración, encontrarás opciones avanzadas de red. **Estos ajustes son opcionales** - los valores predeterminados funcionan bien para la mayoría de los usuarios. Sin embargo, puedes ajustarlos según tus requisitos de seguridad y necesidades de rendimiento.

### Opciones de longitud del tunnel

![Opciones de longitud y cantidad de Tunnel](/images/guides/eepsite/tunnel-options.png)

**Longitud del tunnel** - **Predeterminado**: tunnel de 3 saltos (alto anonimato) - Controla cuántos saltos de router atraviesa una solicitud antes de llegar a tu eepsite - **Más saltos = Mayor anonimato, pero rendimiento más lento** - **Menos saltos = Mayor rendimiento, pero menor anonimato** - Las opciones van de 0-3 saltos con ajustes de variación - **Recomendación**: Mantén 3 saltos a menos que tengas requisitos de rendimiento específicos

**Variación de tunnel** - **Predeterminado**: variación de 0 saltos (sin aleatorización, rendimiento consistente) - Añade aleatorización a la longitud del tunnel para mayor seguridad - Ejemplo: "variación de 0-1 saltos" significa que los tunnels serán aleatoriamente de 3 o 4 saltos - Aumenta la imprevisibilidad, pero puede provocar tiempos de carga inconsistentes

### Opciones de cantidad de Tunnel

**Cantidad (tunnels entrantes/salientes)** - **Predeterminado**: 2 tunnels entrantes, 2 tunnels salientes (ancho de banda y fiabilidad estándar) - Controla cuántos tunnels paralelos se asignan a tu eepsite - **Más tunnels = Mejor disponibilidad y gestión de carga, pero mayor uso de recursos** - **Menos tunnels = Menor uso de recursos, pero redundancia reducida** - Recomendado para la mayoría de los usuarios: 2/2 (predeterminado) - Los sitios con alto tráfico pueden beneficiarse de 3/3 o más

**Cantidad de tunnels de respaldo** - **Predeterminado**: 0 tunnels de respaldo (sin redundancia, sin uso adicional de recursos) - Tunnels en espera que se activan si fallan los tunnels primarios - Aumenta la fiabilidad, pero consume más ancho de banda y CPU - La mayoría de las eepsites personales no necesitan tunnels de respaldo

### Límites de POST

![Configuración de límites de POST](/images/guides/eepsite/post-limits.png)

Si tu eepsite incluye formularios (formularios de contacto, secciones de comentarios, carga de archivos, etc.), puedes configurar límites de solicitudes POST para evitar abusos:

**Límites por cliente** - **Por período**: Número máximo de solicitudes de un solo cliente (predeterminado: 6 cada 5 minutos) - **Duración del bloqueo**: Cuánto tiempo bloquear a clientes abusivos (predeterminado: 20 minutos)

**Límites totales** - **Total**: Máximo de solicitudes POST de todos los clientes en conjunto (predeterminado: 20 cada 5 minutos) - **Duración del bloqueo**: Tiempo durante el cual se rechazarán todas las solicitudes POST si se supera el límite (predeterminado: 10 minutos)

**Periodo de límite de POST** - Ventana de tiempo para medir las tasas de solicitudes (por defecto: 5 minutos)

Estos límites ayudan a proteger contra el spam, los ataques de denegación de servicio y el abuso de envíos automatizados de formularios.

### Cuándo ajustar la configuración avanzada

- **Sitio comunitario de alto tráfico**: Aumentar la cantidad de tunnel (3-4 entrantes/salientes)
- **Aplicación crítica para el rendimiento**: Reducir la longitud del tunnel a 2 saltos (compromiso de privacidad)
- **Se requiere anonimato máximo**: Mantener 3 saltos, agregar una variación de 0-1
- **Formularios con uso legítimo elevado**: Aumentar los límites de POST en consecuencia
- **Blog/portafolio personal**: Usar todos los valores predeterminados

---

## Paso 4: Añadir contenido a tu Eepsite

Ahora que tu eepsite está configurado, debes añadir los archivos de tu sitio web (HTML, CSS, imágenes, etc.) al document root (directorio raíz de documentos) del servidor web. La ubicación varía según tu sistema operativo, el tipo de instalación y la implementación de I2P.

### Cómo encontrar su directorio raíz de documentos

La **raíz del documento** (a menudo llamada `docroot`) es la carpeta donde colocas todos los archivos de tu sitio web. Tu archivo `index.html` debe ir directamente en esta carpeta.

#### Java I2P (Distribución estándar)

**Linux** - **Instalación estándar**: `~/.i2p/eepsite/docroot/` - **Instalación mediante paquete (que se ejecuta como servicio)**: `/var/lib/i2p/i2p-config/eepsite/docroot/`

**Windows** - **Instalación estándar**: `%LOCALAPPDATA%\I2P\eepsite\docroot\`   - Ruta típica: `C:\Users\YourUsername\AppData\Local\I2P\eepsite\docroot\` - **Instalación como servicio de Windows**: `%PROGRAMDATA%\I2P\eepsite\docroot\`   - Ruta típica: `C:\ProgramData\I2P\eepsite\docroot\`

**macOS** - **Instalación estándar**: `/Users/YourUsername/Library/Application Support/i2p/eepsite/docroot/`

#### I2P+ (Distribución mejorada de I2P)

I2P+ utiliza la misma estructura de directorios que Java I2P. Siga las rutas indicadas arriba según su sistema operativo.

#### i2pd (Implementación en C++)

**Linux/Unix** - **Predeterminado**: `/var/lib/i2pd/eepsite/` o `~/.i2pd/eepsite/` - Consulta tu archivo de configuración `i2pd.conf` para el valor real de `root` en el tunnel de tu servidor HTTP

**Windows** - Comprueba el archivo `i2pd.conf` en el directorio de instalación de i2pd

**macOS** - Por lo general: `~/Library/Application Support/i2pd/eepsite/`

### Añadir los archivos de tu sitio web

1. **Navega hasta la raíz del documento** usando tu gestor de archivos o la terminal
2. **Crea o copia los archivos de tu sitio web** en la carpeta `docroot`
   - Como mínimo, crea un archivo `index.html` (esta es tu página de inicio)
   - Añade CSS, JavaScript, imágenes y otros recursos según sea necesario
3. **Organiza los subdirectorios** como lo harías para cualquier sitio web:
   ```
   docroot/
   ├── index.html
   ├── about.html
   ├── css/
   │   └── style.css
   ├── images/
   │   └── logo.png
   └── js/
       └── script.js
   ```

### Inicio rápido: ejemplo sencillo de HTML

Si acabas de empezar, crea un archivo `index.html` básico en tu carpeta `docroot`:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>My I2P Eepsite</title>
</head>
<body>
    <h1>Welcome to My Eepsite!</h1>
    <p>This is my first website on the I2P network.</p>
    <p>Privacy-focused and decentralized!</p>
</body>
</html>
```
### Permisos (Linux/Unix/macOS)

Si ejecutas I2P como un servicio o con un usuario diferente, asegúrate de que el proceso de I2P tenga acceso de lectura a tus archivos:

```bash
# Set appropriate ownership (if running as i2p user)
sudo chown -R i2p:i2p /var/lib/i2p/i2p-config/eepsite/docroot/

# Or set readable permissions for all users
chmod -R 755 ~/.i2p/eepsite/docroot/
```
### Consejos

- **Contenido predeterminado**: Cuando instalas I2P por primera vez, ya hay contenido de ejemplo en la carpeta `docroot` - siéntete libre de reemplazarlo
- **Los sitios estáticos funcionan mejor**: Aunque Jetty admite servlets y JSP, los sitios sencillos en HTML/CSS/JavaScript son más fáciles de mantener
- **Servidores web externos**: Los usuarios avanzados pueden ejecutar servidores web personalizados (Apache, Nginx, Node.js, etc.) en diferentes puertos y apuntar el tunnel de I2P a ellos

---

## Paso 5: Iniciar tu eepsite

Ahora que tu eepsite está configurado y tiene contenido, es hora de iniciarlo y hacerlo accesible en la red I2P.

### Iniciar el Tunnel

1. **Vuelve al [Administrador de Servicios Ocultos](http://127.0.0.1:7657/i2ptunnelmgr)**
2. Busca la entrada de tu **servidor web I2P** en la lista
3. Haz clic en el botón **Iniciar** en la columna Control

![Eepsite en ejecución](/images/guides/eepsite/eepsite-running.png)

### Espere al establecimiento del Tunnel

Después de hacer clic en Start, tu eepsite tunnel comenzará a construirse. Este proceso suele tardar **30-60 segundos**. Observa el indicador de estado:

- **Luz roja** = Tunnel iniciándose/construyéndose
- **Luz amarilla** = Tunnel parcialmente establecido
- **Luz verde** = Tunnel completamente operativo y listo

¡Cuando veas la **luz verde**, tu eepsite estará en línea en la red de I2P!

### Accede a tu Eepsite

Haz clic en el botón **Preview** junto a tu eepsite en ejecución. Esto abrirá una nueva pestaña del navegador con la dirección de tu eepsite.

Tu eepsite tiene dos tipos de direcciones:

1. **Dirección Base32 (.b32.i2p)**: Una dirección criptográfica larga que se ve así:
   ```
   http://fcyianvr325tdgiiueyg4rsq4r5iuibzovl26msox5ryoselykpq.b32.i2p
   ```
   - Esta es la dirección permanente de tu eepsite (sitio web dentro de I2P), derivada criptográficamente
   - No puede cambiarse y está vinculada a tu clave privada
   - Funciona siempre, incluso sin registro de dominio

2. **Dominio legible por humanos (.i2p)**: Si configuras un nombre de host del sitio web (p. ej., `testwebsite.i2p`)
   - Solo funciona después del registro del dominio (consulta la siguiente sección)
   - Más fácil de recordar y compartir
   - Se resuelve a tu dirección .b32.i2p

El botón **Copy Hostname** te permite copiar rápidamente tu dirección `.b32.i2p` completa para compartirla.

---

## ⚠️ Crítico: realiza una copia de seguridad de tu clave privada

Antes de continuar, **debes hacer una copia de seguridad** del archivo de clave privada de tu eepsite. Esto es sumamente importante por varias razones:

### ¿Por qué hacer una copia de seguridad de tu clave?

**Tu clave privada (`eepPriv.dat`) es la identidad de tu eepsite.** Determina tu dirección `.b32.i2p` y demuestra la propiedad de tu eepsite.

- **Clave = dirección .b32**: Tu clave privada genera matemáticamente tu dirección .b32.i2p única
- **No se puede recuperar**: Si pierdes tu clave, pierdes permanentemente la dirección de tu eepsite
- **No se puede cambiar**: Si registraste un dominio que apunta a una dirección .b32, **no hay forma de actualizarlo** - el registro es permanente
- **Necesaria para la migración**: Cambiar a una computadora nueva o reinstalar I2P requiere esta clave para conservar la misma dirección
- **Multihoming support (soporte para operar desde múltiples ubicaciones)**: Ejecutar tu eepsite desde múltiples ubicaciones requiere la misma clave en cada servidor

### ¿Dónde está la clave privada?

De forma predeterminada, tu clave privada se almacena en: - **Linux**: `~/.i2p/eepsite/eepPriv.dat` (o `/var/lib/i2p/i2p-config/eepsite/eepPriv.dat` para instalaciones como servicio) - **Windows**: `%LOCALAPPDATA%\I2P\eepsite\eepPriv.dat` o `%PROGRAMDATA%\I2P\eepsite\eepPriv.dat` - **macOS**: `/Users/YourUsername/Library/Application Support/i2p/eepsite/eepPriv.dat`

También puedes comprobar o cambiar esta ruta en la configuración de tu tunnel, en "Archivo de clave privada".

### Cómo hacer una copia de seguridad

1. **Detén tu tunnel** (opcional, pero más seguro)
2. **Copia `eepPriv.dat`** a un lugar seguro:
   - Unidad USB externa
   - Unidad de copia de seguridad cifrada
   - Archivo protegido con contraseña
   - Almacenamiento en la nube seguro (cifrado)
3. **Mantén varias copias de seguridad** en diferentes ubicaciones físicas
4. **Nunca compartas este archivo** - cualquiera que lo tenga puede suplantar tu eepsite

### Restaurar desde copia de seguridad

Para restaurar su eepsite en un sistema nuevo o después de reinstalar:

1. Instala I2P y crea/configura los ajustes de tu tunnel
2. **Detén el tunnel** antes de copiar la clave
3. Copia tu `eepPriv.dat` de respaldo a la ubicación correcta
4. Inicia el tunnel - usará tu dirección .b32 original

---

## Si no vas a registrar un dominio

**¡Enhorabuena!** Si no planeas registrar un nombre de dominio `.i2p` personalizado, tu eepsite (sitio web dentro de I2P) ya está completo y en funcionamiento.

Puedes: - Compartir tu dirección `.b32.i2p` con otras personas - Acceder a tu sitio a través de la red I2P usando cualquier navegador compatible con I2P - Actualizar los archivos de tu sitio web en la carpeta `docroot` en cualquier momento - Supervisar el estado de tu tunnel en el Hidden Services Manager (Administrador de Servicios Ocultos)

**Si quieres un dominio legible para humanos** (como `mysite.i2p` en lugar de una dirección .b32 larga), pasa a la siguiente sección.

---

## Registro de su dominio de I2P

Un dominio `.i2p` legible por humanos (como `testwebsite.i2p`) es mucho más fácil de recordar y compartir que una dirección `.b32.i2p` larga. El registro del dominio es gratuito y vincula el nombre que elijas con la dirección criptográfica de tu eepsite.

### Requisitos previos

- Tu eepsite (sitio web en I2P) debe estar funcionando con el indicador en verde
- Debes haber configurado un **Nombre de host del sitio web** en la configuración del tunnel (túnel de I2P) (Paso 2)
- Ejemplo: `testwebsite.i2p` o `myblog.i2p`

### Paso 1: Generar la cadena de autenticación

1. **Vuelve a la configuración de tu tunnel** en el Administrador de Servicios Ocultos
2. Haz clic en tu entrada de **servidor web de I2P** para abrir la configuración
3. Desplázate hacia abajo para encontrar el botón **Autenticación de registro**

![Autenticación de registro](/images/guides/eepsite/registration-authentication.png)

4. Haz clic en **Registration Authentication**
5. **Copia la cadena de autenticación completa** mostrada para "Authentication for adding host [yourdomainhere]"

La cadena de autenticación tendrá el siguiente aspecto:

```
testwebsite.i2p=I8WiuSx1TcYAutCrhLveZ6gghdqsIJ1v9noSGPb7ItYjxaK5LHVNxgC60KuEu95nqCCF2qwgnW~2ehIY9vsi1iPForksdU3GALrQq4S73meoIIXarCCdb~Z6Ehj2-yLWI8WiuSx1TcYAutCrhLveZ6gghdqsIJ1v9noSGPb7ItYjxaK5LHVNxgC60KuEu95nqCCF2qwgnW~2ehIY9vsi1iPForksdU3GALrQq4S73meoIIXarCCdb~Z6Ehj2-yLWI8WiuSx1TcYAutCrhLveZ6gghdqsIJ1v9noSGPb7ItYjxaK5LHVNxgC60KuEu95nqCCF2qwgnW~2ehIY9vsi1iPForksdU3GALrQq4S73meoIIXarCCdb~Z6Ehj2-yLWI8WiuSx1TcYAutCrhLveZ6gghdqsIJ1v9noSGPb7ItYjxaK5LHVNxgC60KuEu95nqCCF2qwgnW~2ehIY9vsi1uNxFZ0HN7tQbbVj1pmbahepQZNxEW0ufwnMYAoFo8opBQAEAAcAAA==#!date=1762104890#sig=9DjEfrcNRxsoSxiE0Mp0-7rH~ktYWtgwU8c4J0eSo0VHbGxDxdiO9D1Cvwcx8hkherMO07UWOC9BWf-1wRyUAw==
```
Esta cadena contiene: - Tu nombre de dominio (`testwebsite.i2p`) - Tu dirección de destino (el identificador criptográfico largo) - Una marca de tiempo - Una firma criptográfica que demuestra que posees la clave privada

**Conserva esta cadena de autenticación** - la necesitarás para ambos servicios de registro.

### Paso 2: Regístrate en stats.i2p

1. **Ve a** [stats.i2p Add Key](http://stats.i2p/i2p/addkey.html) (dentro de I2P)

![Registro de dominio de stats.i2p](/images/guides/eepsite/stats-i2p-add.png)

2. **Pega la cadena de autenticación** en el campo "Authentication String"
3. **Añade tu nombre** (opcional) - de forma predeterminada es "Anonymous"
4. **Añade una descripción** (recomendado) - describe brevemente de qué trata tu eepsite
   - Ejemplo: "Nuevo I2P Eepsite", "Blog personal", "Servicio de intercambio de archivos"
5. **Marca "HTTP Service?"** si se trata de un sitio web (déjalo marcado para la mayoría de los eepsites)
   - Desmárcalo para IRC, NNTP, proxies, XMPP, git, etc.
6. Haz clic en **Submit**

Si todo sale bien, verás una confirmación de que tu dominio se ha añadido a la libreta de direcciones de stats.i2p.

### Paso 3: Regístrate en reg.i2p

Para garantizar la máxima disponibilidad, también deberías registrarte en el servicio reg.i2p:

1. **Accede a** [reg.i2p Agregar dominio](http://reg.i2p/add) (dentro de I2P)

![Registro de dominio de reg.i2p](/images/guides/eepsite/reg-i2p-add.png)

2. **Pega la misma cadena de autenticación** en el campo "Auth string"
3. **Añade una descripción** (opcional pero recomendable)
   - Esto ayuda a que otros usuarios de I2P entiendan lo que ofrece tu sitio
4. Haz clic en **Submit**

Debería recibir una confirmación de que su dominio se ha registrado.

### Paso 4: Espera la propagación

Después de enviar a ambos servicios, el registro de su dominio se propagará a través del sistema de libreta de direcciones de la red I2P.

**Cronología de propagación**: - **Registro inicial**: Inmediato en los servicios de registro - **Propagación en toda la red**: De varias horas a 24+ horas - **Disponibilidad total**: Puede tardar hasta 48 horas para que todos los routers se actualicen

**¡Esto es normal!** El sistema de libreta de direcciones de I2P se actualiza periódicamente, no al instante. Tu eepsite está funcionando - otros usuarios solo necesitan recibir la libreta de direcciones actualizada.

### Verifica tu dominio

Después de unas horas, puedes probar tu dominio:

1. **Abre una pestaña nueva** en tu navegador I2P
2. Intenta acceder a tu dominio directamente: `http://yourdomainname.i2p`
3. ¡Si carga, tu dominio está registrado y propagándose!

Si todavía no funciona: - Espera un poco más (las libretas de direcciones se actualizan a su propio ritmo) - La libreta de direcciones de tu router puede necesitar tiempo para sincronizarse - Intenta reiniciar tu I2P router para forzar una actualización de la libreta de direcciones

### Notas importantes

- **El registro es permanente**: Una vez registrado y propagado, tu dominio apunta permanentemente a tu dirección `.b32.i2p`
- **No se puede cambiar el destino**: No puedes actualizar a qué dirección `.b32.i2p` apunta tu dominio - por eso es fundamental hacer una copia de seguridad de `eepPriv.dat`
- **Propiedad del dominio**: Solo el titular de la clave privada puede registrar o actualizar el dominio
- **Servicio gratuito**: El registro de dominios en I2P es gratuito, gestionado por la comunidad y descentralizado
- **Múltiples registradores**: Registrarse tanto en stats.i2p como en reg.i2p aumenta la fiabilidad y la velocidad de propagación

---

## ¡Felicidades!

¡Tu eepsite de I2P ya está completamente operativo con un dominio registrado!

**Próximos pasos**: - Agrega más contenido a tu carpeta `docroot` - Comparte tu dominio con la comunidad de I2P - Mantén a salvo tu copia de seguridad de `eepPriv.dat` - Supervisa regularmente el estado de tu tunnel - Considera unirte a los foros de I2P o a IRC para promocionar tu sitio

¡Bienvenido a la red I2P! 🎉
