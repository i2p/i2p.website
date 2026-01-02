---
title: "Instalación de Plugins Personalizados"
description: "Instalación, actualización y desarrollo de plugins del router"
slug: "plugins"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

El framework de plugins de I2P te permite extender el router sin tocar la instalación principal. Los plugins disponibles incluyen correo, blogs, IRC, almacenamiento, wikis, herramientas de monitoreo y más.

> **Nota de seguridad:** Los plugins se ejecutan con los mismos permisos que el router. Trate las descargas de terceros de la misma manera que trataría cualquier actualización de software firmado: verifique la fuente antes de instalar.

## 1. Instalar un Plugin

1. Copia la URL de descarga del plugin desde la página del proyecto.  
   ![Copy plugin URL](/images/plugins/plugin-step-0.png)
2. Abre la [página de Configuración de Plugins](http://127.0.0.1:7657/configplugins) de la consola del router.  
   ![Open plugin configuration](/images/plugins/plugin-step-1.png)
3. Pega la URL en el campo de instalación y haz clic en **Install Plugin**.  
   ![Install plugin](/images/plugins/plugin-step-2.png)

El router descarga el archivo firmado, verifica la firma y activa el plugin inmediatamente. La mayoría de los plugins añaden enlaces en la consola o servicios en segundo plano sin requerir un reinicio del router.

## 2. Por qué Importan los Plugins

- Distribución con un solo clic para usuarios finales—sin ediciones manuales a `wrapper.config` o `clients.config`
- Mantiene el paquete principal `i2pupdate.su3` pequeño mientras entrega funcionalidades grandes o especializadas bajo demanda
- JVM opcionales por plugin proporcionan aislamiento de procesos cuando se requiere
- Verificaciones automáticas de compatibilidad con la versión del router, el runtime de Java y Jetty
- El mecanismo de actualización refleja al router: paquetes firmados y descargas incrementales
- Se soportan integraciones en la consola, paquetes de idiomas, temas de UI y aplicaciones no-Java (mediante scripts)
- Permite directorios de "tiendas de aplicaciones" curadas como `plugins.i2p`

## 3. Gestionar Plugins Instalados

Usa los controles en [I2P Router Plugin's](http://127.0.0.1:7657/configclients.jsp#plugin) para:

- Verificar actualizaciones de un solo plugin
- Verificar todos los plugins a la vez (se activa automáticamente después de actualizaciones del router)
- Instalar cualquier actualización disponible con un solo clic  
  ![Update plugins](/images/plugins/plugin-update-0.png)
- Activar/desactivar el inicio automático para plugins que registran servicios
- Desinstalar plugins de forma limpia

## 4. Construye Tu Propio Plugin

1. Revisa la [especificación de plugins](/docs/specs/plugin/) para conocer los requisitos de empaquetado, firma y metadatos.
2. Usa [`makeplugin.sh`](https://github.com/i2p/i2p.scripts/tree/master/plugin/makeplugin.sh) para envolver un binario o webapp existente en un archivo instalable.
3. Publica tanto las URLs de instalación como de actualización para que el router pueda distinguir entre instalaciones nuevas y actualizaciones incrementales.
4. Proporciona checksums y claves de firma de manera prominente en la página de tu proyecto para ayudar a los usuarios a verificar la autenticidad.

¿Buscas ejemplos? Examina el código fuente de los plugins de la comunidad en `plugins.i2p` (por ejemplo, la muestra `snowman`).

## 5. Limitaciones Conocidas

- Actualizar un plugin que incluye archivos JAR simples puede requerir un reinicio del router porque el cargador de clases de Java almacena las clases en caché.
- La consola puede mostrar un botón **Detener** incluso si el plugin no tiene ningún proceso activo.
- Los plugins lanzados en una JVM separada crean un directorio `logs/` en el directorio de trabajo actual.
- La primera vez que aparece una clave de firmante se confía automáticamente; no existe una autoridad de firma central.
- Windows a veces deja directorios vacíos después de desinstalar un plugin.
- Instalar un plugin exclusivo de Java 6 en una JVM de Java 5 reporta "plugin is corrupt" debido a la compresión Pack200.
- Los plugins de temas y traducciones permanecen en gran medida sin probar.
- Los indicadores de inicio automático no siempre persisten para plugins no administrados.

## 6. Requisitos y Mejores Prácticas

- El soporte para plugins está disponible en I2P **0.7.12 y versiones más recientes**.
- Mantén tu router y plugins actualizados para recibir correcciones de seguridad.
- Incluye notas de versión concisas para que los usuarios comprendan los cambios entre versiones.
- Cuando sea posible, aloja los archivos de plugins mediante HTTPS dentro de I2P para minimizar la exposición de metadatos en la red abierta.

## 7. Lectura adicional

- [Especificación de plugins](/docs/specs/plugin/)
- [Framework de aplicaciones cliente](/docs/applications/managed-clients/)
- [Repositorio de scripts de I2P](https://github.com/i2p/i2p.scripts/) para utilidades de empaquetado
