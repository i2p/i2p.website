---
title: "Clientes Gestionados"
description: "Cómo las aplicaciones administradas por el enrutador se integran con ClientAppManager y el mapeador de puertos"
slug: "managed-clients"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

## 1. Descripción general

Las entradas en [`clients.config`](/docs/specs/configuration/#clients-config) indican al router qué aplicaciones lanzar al iniciar. Cada entrada puede ejecutarse como un cliente **administrado** (preferido) o como un cliente **no administrado**. Los clientes administrados colaboran con `ClientAppManager`, que:

- Instancia la aplicación y rastrea el estado del ciclo de vida para la consola del router
- Expone controles de inicio/detención al usuario y garantiza apagados limpios al salir del router
- Aloja un **registro de clientes** ligero y un **mapeador de puertos** para que las aplicaciones puedan descubrir los servicios de las demás

Los clientes no administrados simplemente invocan un método `main()`; úselos solo para código heredado que no puede ser modernizado.

## 2. Implementar un Cliente Administrado

Los clientes gestionados deben implementar `net.i2p.app.ClientApp` (para aplicaciones de cara al usuario) o `net.i2p.router.app.RouterApp` (para extensiones del router). Proporcione uno de los constructores siguientes para que el gestor pueda suministrar el contexto y los argumentos de configuración:

```java
public MyClientApp(I2PAppContext context, ClientAppManager manager, String[] args)
```
```java
public MyRouterApp(RouterContext context, ClientAppManager manager, String[] args)
```
El array `args` contiene los valores configurados en `clients.config` o archivos individuales en `clients.config.d/`. Extiende las clases auxiliares `ClientApp` / `RouterApp` cuando sea posible para heredar el cableado de ciclo de vida predeterminado.

### 2.1 Lifecycle Methods

Se espera que los clientes gestionados implementen:

- `startup()` - realizar la inicialización y retornar prontamente. Debe llamar a `manager.notify()` al menos una vez para transicionar desde el estado INITIALIZED.
- `shutdown(String[] args)` - liberar recursos y detener hilos en segundo plano. Debe llamar a `manager.notify()` al menos una vez para cambiar el estado a STOPPING o STOPPED.
- `getState()` - informar a la consola si la aplicación está ejecutándose, iniciándose, deteniéndose o ha fallado

El administrador llama a estos métodos cuando los usuarios interactúan con la consola.

### 2.2 Advantages

- Informes de estado precisos en la consola del router
- Reinicios limpios sin filtración de hilos o referencias estáticas
- Menor huella de memoria una vez que la aplicación se detiene
- Registro centralizado y reporte de errores a través del contexto inyectado

## 3. Unmanaged Clients (Fallback Mode)

Si la clase configurada no implementa una interfaz gestionada, el router la inicia invocando `main(String[] args)` y no puede rastrear el proceso resultante. La consola muestra información limitada y los hooks de apagado pueden no ejecutarse. Reserve este modo para scripts o utilidades puntuales que no pueden adoptar las APIs gestionadas.

## 4. Client Registry

Los clientes administrados y no administrados pueden registrarse a sí mismos con el gestor para que otros componentes puedan recuperar una referencia por nombre:

```java
manager.register(this);
```
El registro utiliza el valor de retorno de `getName()` del cliente como clave de registro. Los registros conocidos incluyen `console`, `i2ptunnel`, `Jetty`, `outproxy` y `update`. Recupera un cliente con `ClientAppManager.getRegisteredApp(String name)` para coordinar funcionalidades (por ejemplo, la consola consultando a Jetty para obtener detalles de estado).

Tenga en cuenta que el registro de clientes y el mapeador de puertos son sistemas separados. El registro de clientes permite la comunicación entre aplicaciones mediante búsqueda por nombre, mientras que el mapeador de puertos asigna nombres de servicios a combinaciones host:puerto para el descubrimiento de servicios.

## 3. Clientes No Gestionados (Modo de Reserva)

El mapeador de puertos ofrece un directorio simple para servicios TCP internos. Registra puertos de loopback para que los colaboradores eviten direcciones codificadas de forma fija:

```java
context.portMapper().register(PortMapper.SVC_HTTPS_PROXY, 4445);
```
O con especificación explícita del host:

```java
context.portMapper().register(PortMapper.SVC_HTTP_PROXY, "127.0.0.1", 4444);
```
Busca servicios usando `PortMapper.getPort(String name)` (devuelve -1 si no se encuentra) o `getPort(String name, int defaultPort)` (devuelve el valor predeterminado si no se encuentra). Verifica el estado de registro con `isRegistered(String name)` y obtén el host registrado con `getActualHost(String name)`.

Constantes comunes del servicio mapeador de puertos de `net.i2p.util.PortMapper`:

- `SVC_CONSOLE` - Consola del router (puerto predeterminado 7657)
- `SVC_HTTP_PROXY` - Proxy HTTP (puerto predeterminado 4444)
- `SVC_HTTPS_PROXY` - Proxy HTTPS (puerto predeterminado 4445)
- `SVC_I2PTUNNEL` - Gestor de I2PTunnel
- `SVC_SAM` - Puente SAM (puerto predeterminado 7656)
- `SVC_SAM_SSL` - Puente SAM SSL
- `SVC_SAM_UDP` - SAM UDP
- `SVC_BOB` - Puente BOB (puerto predeterminado 2827)
- `SVC_EEPSITE` - Eepsite estándar (puerto predeterminado 7658)
- `SVC_HTTPS_EEPSITE` - Eepsite HTTPS
- `SVC_IRC` - Túnel IRC (puerto predeterminado 6668)
- `SVC_SUSIDNS` - SusiDNS

Nota: `httpclient`, `httpsclient` y `httpbidirclient` son tipos de tunnel de i2ptunnel (usados en la configuración `tunnel.N.type`), no constantes de servicio de mapeo de puertos.

## 4. Registro de Clientes

### 2.1 Métodos del Ciclo de Vida

A partir de la versión 0.9.42, el router admite dividir la configuración en archivos individuales dentro del directorio `clients.config.d/`. Cada archivo contiene propiedades para un solo cliente con todas las propiedades prefijadas con `clientApp.0.`:

```
clientApp.0.main=net.i2p.router.web.RouterConsoleRunner
clientApp.0.name=Router Console
clientApp.0.args=7657 ::1,127.0.0.1 ./webapps/
clientApp.0.delay=0
clientApp.0.onBoot=true
```
Este es el enfoque recomendado para nuevas instalaciones y plugins.

### 2.2 Ventajas

Para retrocompatibilidad, el formato tradicional utiliza numeración secuencial:

```
clientApp.0.main=net.i2p.router.web.RouterConsoleRunner
clientApp.0.name=Router Console
clientApp.0.args=7657 ::1,127.0.0.1 ./webapps/
clientApp.1.main=net.i2p.apps.systray.UrlLauncher
clientApp.1.name=URL Launcher
clientApp.1.delay=5
```
### 6.3 Configuration Properties

**Requerido:** - `main` - Nombre completo de la clase que implementa ClientApp o RouterApp, o que contiene el método estático `main(String[] args)`

**Opcional:** - `name` - Nombre a mostrar en la consola del router (por defecto el nombre de la clase) - `args` - Argumentos separados por espacios o tabulaciones (admite cadenas entre comillas) - `delay` - Segundos antes de iniciar (por defecto 120) - `onBoot` - Fuerza `delay=0` si es verdadero - `startOnLoad` - Habilita/deshabilita el cliente (por defecto verdadero)

**Específico del plugin:** - `stopargs` - Argumentos pasados durante el apagado - `uninstallargs` - Argumentos pasados durante la desinstalación del plugin - `classpath` - Entradas de classpath adicionales separadas por comas

**Sustitución de variables para plugins:** - `$I2P` - Directorio base de I2P - `$CONFIG` - Directorio de configuración del usuario (ej., ~/.i2p) - `$PLUGIN` - Directorio del plugin - `$OS` - Nombre del sistema operativo - `$ARCH` - Nombre de la arquitectura

## 5. Mapeador de Puertos

- Prefiera clientes gestionados; recurra a clientes no gestionados solo cuando sea absolutamente necesario.
- Mantenga la inicialización y el apagado ligeros para que las operaciones de la consola permanezcan receptivas.
- Use nombres de registro y puerto descriptivos para que las herramientas de diagnóstico (y los usuarios finales) comprendan qué hace un servicio.
- Evite singletons estáticos: confíe en el contexto inyectado y el gestor para compartir recursos.
- Llame a `manager.notify()` en todas las transiciones de estado para mantener un estado preciso de la consola.
- Si debe ejecutarse en una JVM separada, documente cómo los registros y diagnósticos se exponen a la consola principal.
- Para programas externos, considere usar ShellService (añadido en la versión 1.7.0) para obtener los beneficios de un cliente gestionado.

## 6. Formato de Configuración

Los clientes administrados se introdujeron en la **versión 0.9.4** (17 de diciembre de 2012) y siguen siendo la arquitectura recomendada hasta la **versión 2.10.0** (9 de septiembre de 2025). Las APIs principales se han mantenido estables sin cambios disruptivos durante este período:

- Firmas de constructor sin cambios
- Métodos de ciclo de vida (startup, shutdown, getState) sin cambios
- Métodos de registro de ClientAppManager sin cambios
- Métodos de registro y búsqueda de PortMapper sin cambios

Mejoras notables: - **0.9.42 (2019)** - estructura de directorio clients.config.d/ para archivos de configuración individuales - **1.7.0 (2021)** - ShellService añadido para seguimiento del estado de programas externos - **2.10.0 (2025)** - Versión actual sin cambios en la API de cliente gestionado

La próxima versión principal requerirá Java 17+ como mínimo (requisito de infraestructura, no un cambio en la API).

## References

- [Especificación de clients.config](/docs/specs/configuration/#clients-config)
- [Especificación de Archivos de Configuración](/docs/specs/configuration/)
- [Índice de Documentación Técnica de I2P](/docs/)
- [Javadoc de ClientAppManager](https://i2p.github.io/i2p.i2p/net/i2p/app/ClientAppManager.html) (API 0.9.66)
- [Javadoc de PortMapper](https://i2p.github.io/i2p.i2p/net/i2p/util/PortMapper.html) (API 0.9.66)
- [Interfaz ClientApp](https://i2p.github.io/i2p.i2p/net/i2p/app/ClientApp.html) (API 0.9.66)
- [Interfaz RouterApp](https://i2p.github.io/i2p.i2p/net/i2p/router/app/RouterApp.html) (API 0.9.66)
- [Javadoc Alternativo (estable)](https://docs.i2p-projekt.de/javadoc/)
- [Javadoc Alternativo (espejo clearnet)](https://eyedeekay.github.io/javadoc-i2p/)

> **Nota:** La red I2P aloja documentación completa en http://idk.i2p/javadoc-i2p/ que requiere un router I2P para acceder. Para acceso desde clearnet, utiliza el mirror de GitHub Pages mencionado arriba.
