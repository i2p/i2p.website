---
title: "Configuración del Navegador Web"
description: "Configurar navegadores populares para usar los proxies HTTP/HTTPS de I2P en escritorio y Android"
slug: "browser-config"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
type: docs
---

Esta guía muestra cómo configurar los navegadores más comunes para enviar tráfico a través del proxy HTTP integrado de I2P. Cubre Safari, Firefox y navegadores Chrome/Chromium con instrucciones detalladas paso a paso.

**Notas Importantes**:

- El proxy HTTP predeterminado de I2P escucha en `127.0.0.1:4444`.
- I2P protege el tráfico dentro de la red I2P (sitios .i2p).
- Asegúrate de que tu router I2P esté ejecutándose antes de configurar tu navegador.

## Safari (macOS)

Safari utiliza la configuración de proxy del sistema en macOS.

### Step 1: Open Network Settings

1. Abre **Safari** y ve a **Safari → Ajustes** (o **Preferencias**)
2. Haz clic en la pestaña **Avanzado**
3. En la sección **Proxies**, haz clic en **Cambiar ajustes...**

Esto abrirá la Configuración de Red del Sistema de tu Mac.

![Configuración Avanzada de Safari](/images/guides/browser-config/accessi2p_1.png)

### Paso 1: Abrir la Configuración de Red

1. En la configuración de Red, marca la casilla de **Proxy Web (HTTP)**
2. Introduce lo siguiente:
   - **Servidor Proxy Web**: `127.0.0.1`
   - **Puerto**: `4444`
3. Haz clic en **Aceptar** para guardar tu configuración

![Configuración de Proxy en Safari](/images/guides/browser-config/accessi2p_2.png)

¡Ahora puedes navegar por sitios `.i2p` en Safari!

**Nota**: Esta configuración de proxy afectará a todas las aplicaciones que utilicen los proxies del sistema de macOS. Considera crear una cuenta de usuario separada o usar un navegador diferente exclusivamente para I2P si deseas aislar la navegación de I2P.

## Firefox (Desktop)

Firefox tiene su propia configuración de proxy independiente del sistema, lo que lo hace ideal para navegar dedicadamente en I2P.

### Paso 2: Configurar el Proxy HTTP

1. Haz clic en el **botón de menú** (☰) en la esquina superior derecha
2. Selecciona **Configuración**

![Configuración de Firefox](/images/guides/browser-config/accessi2p_3.png)

### Step 2: Find Proxy Settings

1. En el cuadro de búsqueda de Configuración, escribe **"proxy"**
2. Desplázate hasta **Configuración de red**
3. Haz clic en el botón **Configuración...**

![Firefox Proxy Search](/images/guides/browser-config/accessi2p_4.png)

### Paso 1: Abrir Configuración

1. Selecciona **Configuración manual del proxy**
2. Ingresa lo siguiente:
   - **Proxy HTTP**: `127.0.0.1` **Puerto**: `4444`
3. Deja **Host SOCKS** vacío (a menos que necesites específicamente un proxy SOCKS)
4. Marca **Proxy DNS cuando se use SOCKS** solo si usas proxy SOCKS
5. Haz clic en **Aceptar** para guardar

![Configuración Manual de Proxy en Firefox](/images/guides/browser-config/accessi2p_5.png)

¡Ahora puedes navegar por sitios `.i2p` en Firefox!

**Consejo**: Considera crear un perfil de Firefox independiente dedicado a la navegación por I2P. Esto mantiene tu navegación I2P aislada de la navegación regular. Para crear un perfil, escribe `about:profiles` en la barra de direcciones de Firefox.

## Chrome / Chromium (Desktop)

Chrome y los navegadores basados en Chromium (Brave, Edge, etc.) normalmente utilizan la configuración de proxy del sistema en Windows y macOS. Esta guía muestra la configuración en Windows.

### Paso 2: Encontrar la Configuración del Proxy

1. Haz clic en el **menú de tres puntos** (⋮) en la esquina superior derecha
2. Selecciona **Configuración**

![Configuración de Chrome](/images/guides/browser-config/accessi2p_6.png)

### Paso 3: Configurar el Proxy Manual

1. En el cuadro de búsqueda de Configuración, escribe **"proxy"**
2. Haz clic en **Abrir la configuración de proxy de tu equipo**

![Chrome Proxy Search](/images/guides/browser-config/accessi2p_7.png)

### Step 3: Open Manual Proxy Setup

Esto abrirá la configuración de Red e Internet de Windows.

1. Desplázate hacia abajo hasta **Configuración manual de proxy**
2. Haz clic en **Configurar**

![Configuración de Proxy en Windows](/images/guides/browser-config/accessi2p_8.png)

### Paso 1: Abrir la Configuración de Chrome

1. Cambia **Usar un servidor proxy** a **Activado**
2. Introduce lo siguiente:
   - **Dirección IP del proxy**: `127.0.0.1`
   - **Puerto**: `4444`
3. Opcionalmente, añade excepciones en **"No usar el servidor proxy para direcciones que empiecen con"** (por ejemplo, `localhost;127.*`)
4. Haz clic en **Guardar**

![Configuración de Proxy en Chrome](/images/guides/browser-config/accessi2p_9.png)

¡Ahora puedes navegar sitios `.i2p` en Chrome!

**Nota**: Estas configuraciones afectan a todos los navegadores basados en Chromium y algunas otras aplicaciones en Windows. Para evitar esto, considera usar Firefox con un perfil I2P dedicado en su lugar.

### Paso 2: Abrir la Configuración del Proxy

En Linux, puedes iniciar Chrome/Chromium con flags de proxy para evitar cambiar la configuración del sistema:

```bash
chromium \
  --proxy-server="http=127.0.0.1:4444 \
  --proxy-bypass-list="<-loopback>"
```
O crear un script de lanzador de escritorio:

```bash
#!/bin/bash
chromium --proxy-server="http=127.0.0.1:4444" --user-data-dir="$HOME/.config/chromium-i2p"
```
La bandera `--user-data-dir` crea un perfil de Chrome separado para la navegación en I2P.

## Firefox (Escritorio)

Las compilaciones modernas de Firefox "Fenix" limitan about:config y las extensiones por defecto. IceRaven es un fork de Firefox que habilita un conjunto seleccionado de extensiones, facilitando la configuración del proxy.

Configuración basada en extensiones (IceRaven):

1) Si ya usas IceRaven, considera borrar el historial de navegación primero (Menú → Historial → Eliminar historial). 2) Abre Menú → Complementos → Administrador de complementos. 3) Instala la extensión "I2P Proxy for Android and Other Systems". 4) El navegador ahora se conectará a través de I2P.

Esta extensión también funciona en navegadores basados en Firefox pre-Fenix si se instala desde [AMO](https://addons.mozilla.org/en-US/android/addon/i2p-proxy/).

Habilitar el soporte amplio de extensiones en Firefox Nightly requiere un proceso separado [documentado por Mozilla](https://blog.mozilla.org/addons/2020/09/29/expanded-extension-support-in-firefox-for-android-nightly/).

## Internet Explorer / Windows System Proxy

En Windows, el diálogo de proxy del sistema aplica a IE y puede ser utilizado por navegadores basados en Chromium cuando heredan la configuración del sistema.

1) Abre "Configuración de red e Internet" → "Proxy". 2) Activa "Usar un servidor proxy para tu LAN". 3) Establece la dirección `127.0.0.1`, puerto `4444` para HTTP. 4) Opcionalmente marca "Omitir servidor proxy para direcciones locales".
