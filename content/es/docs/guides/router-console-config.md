---
title: "Guía de Configuración de la Consola del Router"
description: "Una guía completa para comprender y configurar la Consola del Router I2P"
slug: "router-console-config"
lastUpdated: "2025-11"
accurateFor: "2.10.0"
type: docs
---

Esta guía proporciona una descripción general de la Consola del Router I2P y sus páginas de configuración. Cada sección explica qué hace la página y para qué está destinada, ayudándote a comprender cómo monitorear y configurar tu router I2P.

## Acceso a la Consola del Router

La Consola del Router I2P es el centro de control para gestionar y monitorear tu router I2P. Por defecto, se puede acceder en la [Consola del Router I2P](http://127.0.0.1:7657/home) una vez que tu router I2P esté en funcionamiento.

![Consola del Router - Inicio](/images/router-console-home.png)

La página de inicio muestra varias secciones clave:

- **Aplicaciones** - Acceso rápido a las aplicaciones integradas de I2P como Correo electrónico, Torrents, Gestor de servicios ocultos y Servidor web
- **Sitios comunitarios de I2P** - Enlaces a recursos importantes de la comunidad incluyendo foros, documentación y sitios web del proyecto
- **Configuración y ayuda** - Herramientas para configurar ajustes de ancho de banda, gestionar plugins y acceder a recursos de ayuda
- **Información de red y para desarrolladores** - Acceso a gráficos, registros, documentación técnica y estadísticas de red

## Libreta de Direcciones

**URL:** [Libreta de Direcciones](http://127.0.0.1:7657/dns)

![Router Console Address Book](/images/router-console-address-book.png)

El Address Book de I2P funciona de manera similar al DNS en la clearnet, permitiéndote gestionar nombres legibles para destinos I2P (eepsites). Aquí es donde puedes ver y agregar direcciones I2P a tu libreta de direcciones personal.

El sistema de libreta de direcciones funciona a través de múltiples capas:

- **Registros Locales** - Tus libretas de direcciones personales que se almacenan únicamente en tu router
  - **Libreta de Direcciones Local** - Hosts que añades manualmente o guardas para tu propio uso
  - **Libreta de Direcciones Privada** - Direcciones que no deseas compartir con otros; nunca se distribuyen públicamente

- **Suscripciones** - Fuentes remotas de libreta de direcciones (como `http://i2p-projekt.i2p/hosts.txt`) que actualizan automáticamente la libreta de direcciones de tu router con sitios I2P conocidos

- **Router Addressbook** - El resultado combinado de tus registros locales y suscripciones, consultable por todas las aplicaciones I2P en tu router

- **Published Addressbook** - Compartición pública opcional de tu libreta de direcciones para que otros la usen como fuente de suscripción (útil si estás ejecutando un sitio I2P)

La libreta de direcciones consulta regularmente tus suscripciones y fusiona el contenido en la libreta de direcciones de tu router, manteniendo tu archivo hosts.txt actualizado con la red I2P.

## Configuración

**URL:** [Configuración Avanzada](http://127.0.0.1:7657/configadvanced)

La sección de Configuración proporciona acceso a todos los ajustes del router a través de múltiples pestañas especializadas.

### Advanced

![Router Console Advanced Configuration](/images/router-console-config-advanced.png)

La página de configuración avanzada proporciona acceso a ajustes de bajo nivel del router que normalmente no son necesarios para la operación normal. **La mayoría de los usuarios no deberían modificar estos ajustes a menos que comprendan la opción de configuración específica y su impacto en el comportamiento del router.**

Características principales:

- **Configuración de Floodfill** - Controla si tu router participa como peer floodfill, lo cual ayuda a la red almacenando y distribuyendo información de la base de datos de red (netDb). Esto puede usar más recursos del sistema pero fortalece la red I2P.

- **Configuración Avanzada de I2P** - Acceso directo al archivo `router.config`, mostrando todos los parámetros de configuración avanzada incluyendo:
  - Límites de ancho de banda y configuración de ráfagas
  - Configuración de transporte (NTCP2, SSU2, puertos UDP y claves)
  - Identificación del router e información de versión
  - Preferencias de consola y configuración de actualizaciones

La mayoría de las opciones de configuración avanzadas no están expuestas en la interfaz de usuario porque rara vez son necesarias. Para habilitar la edición de estas configuraciones, debe agregar `routerconsole.advanced=true` a su archivo `router.config` manualmente.

**Advertencia:** Modificar incorrectamente la configuración avanzada puede afectar negativamente el rendimiento o la conectividad de tu router. Solo cambia estos ajustes si sabes lo que estás haciendo.

### Bandwidth

**URL:** [Configuración de Ancho de Banda](http://127.0.0.1:7657/config)

![Configuración de ancho de banda de la Consola del Router](/images/router-console-config-bandwidth.png)

La página de configuración de ancho de banda te permite controlar cuánto ancho de banda contribuye tu router a la red I2P. I2P funciona mejor cuando configuras tus tasas para que coincidan con la velocidad de tu conexión a internet.

**Configuraciones Clave:**

- **KBps In** - Ancho de banda entrante máximo que tu router aceptará (velocidad de descarga)
- **KBps Out** - Ancho de banda saliente máximo que tu router utilizará (velocidad de subida)
- **Share** - Porcentaje de tu ancho de banda saliente dedicado al tráfico participativo (ayudar a enrutar tráfico para otros)

**Notas Importantes:**

- Todos los valores están en **bytes por segundo** (KBps), no en bits por segundo
- Cuanta más banda ancha pongas a disposición, más ayudas a la red y mejoras tu propio anonimato
- Tu cantidad de subida compartida (KBps Out) determina tu contribución general a la red
- Si no estás seguro de la velocidad de tu red, utiliza la **Prueba de Banda Ancha** para medirla
- Una mayor banda ancha compartida mejora tanto tu anonimato como ayuda a fortalecer la red I2P

La página de configuración muestra la transferencia de datos mensual estimada según tu configuración, ayudándote a planificar la asignación de ancho de banda de acuerdo con los límites de tu plan de internet.

### Client Configuration

**URL:** [Configuración del Cliente](http://127.0.0.1:7657/configclients)

![Configuración de Clientes de la Consola del Router](/images/router-console-config-clients.png)

La página de Configuración del Cliente te permite controlar qué aplicaciones y servicios de I2P se ejecutan al inicio. Aquí puedes habilitar o deshabilitar los clientes integrados de I2P sin desinstalarlos.

**Advertencia Importante:** Ten cuidado al cambiar la configuración aquí. La consola del router y los túneles de aplicación son necesarios para la mayoría de los usos de I2P. Solo los usuarios avanzados deben modificar esta configuración.

**Clientes Disponibles:**

- **Túneles de aplicación** - El sistema I2PTunnel que gestiona túneles de cliente y servidor (proxy HTTP, IRC, etc.)
- **Consola del Router I2P** - La interfaz de administración basada en web que estás usando actualmente
- **Servidor web I2P (eepsite)** - Servidor web Jetty integrado para alojar tu propio sitio web I2P
- **Abrir Consola del Router en el navegador web al iniciar** - Lanza automáticamente tu navegador a la página de inicio de la consola
- **Puente de aplicaciones SAM** - Puente API para que aplicaciones de terceros se conecten a I2P

Cada cliente muestra:
- **¿Ejecutar al Inicio?** - Casilla de verificación para activar/desactivar el inicio automático
- **Control** - Botones de Iniciar/Detener para control inmediato
- **Clase y argumentos** - Detalles técnicos sobre cómo se lanza el cliente

Los cambios en la configuración "¿Ejecutar al inicio?" requieren reiniciar el router para que surtan efecto. Todas las modificaciones se guardan en `/var/lib/i2p/i2p-config/clients.config.d/`.

### Avanzado

**URL:** [Configuración de I2CP](http://127.0.0.1:7657/configi2cp)

![Consola del Router Configuración I2CP](/images/router-console-config-i2cp.png)

La página de configuración de I2CP (I2P Client Protocol) te permite configurar cómo las aplicaciones externas se conectan a tu router I2P. I2CP es el protocolo que las aplicaciones utilizan para comunicarse con el router para crear tunnels y enviar/recibir datos a través de I2P.

**Importante:** La configuración predeterminada funcionará para la mayoría de las personas. Cualquier cambio realizado aquí también debe configurarse en la aplicación cliente externa. Muchos clientes no admiten SSL o autorización. **Todos los cambios requieren reiniciar para que surtan efecto.**

**Opciones de Configuración:**

- **Configuración de interfaz I2CP externa**
  - **Habilitada sin SSL** - Acceso I2CP estándar (predeterminado y más compatible)
  - **Habilitada con SSL requerido** - Solo conexiones I2CP cifradas
  - **Deshabilitada** - Bloquea la conexión de clientes externos vía I2CP

- **Interfaz I2CP** - La interfaz de red en la que escuchar (por defecto: 127.0.0.1 solo para localhost)
- **Puerto I2CP** - El número de puerto para las conexiones I2CP (por defecto: 7654)

- **Autorización**
  - **Requerir nombre de usuario y contraseña** - Habilitar autenticación para conexiones I2CP
  - **Nombre de usuario** - Establecer el nombre de usuario requerido para acceso I2CP
  - **Contraseña** - Establecer la contraseña requerida para acceso I2CP

**Nota de Seguridad:** Si solo ejecutas aplicaciones en la misma máquina que tu router I2P, mantén la interfaz configurada en `127.0.0.1` para prevenir acceso remoto. Solo cambia estas configuraciones si necesitas permitir que aplicaciones I2P desde otros dispositivos se conecten a tu router.

### Ancho de banda

**URL:** [Configuración de Red](http://127.0.0.1:7657/confignet)

![Consola del Router Configuración de Red](/images/router-console-config-network.png)

La página de Configuración de Red te permite configurar cómo tu router I2P se conecta a internet, incluyendo la detección de dirección IP, preferencias de IPv4/IPv6 y configuración de puertos para los transportes UDP y TCP.

**Dirección IP Accesible Externamente:**

- **Usar todos los métodos de autodetección** - Detecta automáticamente tu IP pública usando múltiples métodos (recomendado)
- **Deshabilitar detección de dirección IP por UPnP** - Evita usar UPnP para descubrir tu IP
- **Ignorar dirección IP de interfaz local** - No usar tu IP de red local
- **Usar solo detección de dirección IP por SSU** - Solo usar el transporte SSU2 para detección de IP
- **Modo oculto - no publicar IP** - Evita participar en el tráfico de red (reduce el anonimato)
- **Especificar hostname o IP** - Configurar manualmente tu IP pública o hostname

**Configuración de IPv4:**

- **Deshabilitar entrante (Con cortafuegos)** - Marca esta opción si estás detrás de un cortafuegos, red doméstica, ISP, DS-Lite, o NAT de nivel de operadora que bloquea las conexiones entrantes

**Configuración de IPv6:**

- **Preferir IPv4 sobre IPv6** - Prioriza las conexiones IPv4
- **Preferir IPv6 sobre IPv4** - Prioriza las conexiones IPv6 (predeterminado para redes de doble pila)
- **Habilitar IPv6** - Permite conexiones IPv6
- **Deshabilitar IPv6** - Deshabilita toda la conectividad IPv6
- **Usar solo IPv6 (deshabilitar IPv4)** - Modo experimental solo IPv6
- **Deshabilitar conexiones entrantes (Cortafuegos)** - Marque si su IPv6 está protegido por cortafuegos

**Acción Cuando Cambia la IP:**

- **Modo portátil** - Función experimental que cambia la identidad del router y el puerto UDP cuando tu IP cambia para mayor anonimato

**Configuración UDP:**

- **Especificar Puerto** - Establece un puerto UDP específico para el transporte SSU2 (debe estar abierto en tu firewall)
- **Deshabilitar completamente** - Selecciona solo si estás detrás de un firewall que bloquea todo el tráfico UDP saliente

**Configuración TCP:**

- **Especificar Puerto** - Establece un puerto TCP específico para el transporte NTCP2 (debe estar abierto en tu firewall)
- **Usar el mismo puerto configurado para UDP** - Simplifica la configuración usando un solo puerto para ambos transportes
- **Usar dirección IP autodetectada** - Detecta automáticamente tu IP pública (muestra "actualmente desconocida" si aún no se ha detectado o está tras firewall)
- **Usar siempre dirección IP autodetectada (Sin firewall)** - Mejor opción para routers con acceso directo a internet
- **Deshabilitar conexiones entrantes (Con firewall)** - Marca esta opción si las conexiones TCP están bloqueadas por tu firewall
- **Deshabilitar completamente** - Selecciona solo si estás detrás de un firewall que limita o bloquea TCP saliente
- **Especificar hostname o IP** - Configura manualmente tu dirección accesible desde el exterior

**Importante:** Los cambios en la configuración de red pueden requerir un reinicio del router para que surtan efecto completo. Una configuración adecuada del reenvío de puertos mejora significativamente el rendimiento de tu router y ayuda a la red I2P.

### Configuración del Cliente

**URL:** [Configuración de pares](http://127.0.0.1:7657/configpeer)

![Consola del Router Configuración de Pares](/images/router-console-config-peer.png)

La página de Configuración de Pares proporciona controles manuales para gestionar pares individuales en la red I2P. Esta es una función avanzada que normalmente se utiliza solo para solucionar problemas con pares problemáticos.

**Controles Manuales de Pares:**

- **Hash del Router** - Ingrese el hash del router en base64 de 44 caracteres del peer que desea administrar

**Banear / Desbanear Manualmente un Peer:**

Bloquear un peer evita que participe en cualquier túnel que crees. Esta acción: - Evita que el peer sea utilizado en tus túneles de cliente o exploratorios - Toma efecto inmediatamente sin requerir un reinicio - Persiste hasta que desbloquees manualmente el peer o reinicies tu router - **Bloquear peer hasta el reinicio** - Bloquea temporalmente el peer - **Desbloquear peer** - Elimina el bloqueo de un peer previamente bloqueado

**Ajustar Bonificaciones de Perfil:**

Los bonos de perfil afectan cómo se seleccionan los pares para la participación en túneles. Los bonos pueden ser positivos o negativos: - **Pares rápidos** - Utilizados para túneles de cliente que requieren alta velocidad - **Pares de alta capacidad** - Utilizados para algunos túneles exploratorios que requieren enrutamiento confiable - Los bonos actuales se muestran en la página de perfiles

**Configuración:** - **Velocidad** - Ajustar el bono de velocidad para este peer (0 = neutral) - **Capacidad** - Ajustar el bono de capacidad para este peer (0 = neutral) - **Ajustar bonos de peer** - Aplicar la configuración de bonos

**Casos de Uso:** - Banear un peer que causa problemas de conexión de forma consistente - Excluir temporalmente un peer que sospechas que es malicioso - Ajustar bonificaciones para despriorizar peers con bajo rendimiento - Depurar problemas de construcción de túneles excluyendo peers específicos

**Nota:** La mayoría de los usuarios nunca necesitarán utilizar esta función. El router de I2P gestiona automáticamente la selección de peers y el perfilado basándose en métricas de rendimiento.

### Configuración de I2CP

**URL:** [Configuración de Reseed](http://127.0.0.1:7657/configreseed)

![Consola del Router Configuración de Reseed](/images/router-console-config-reseed.png)

La página de Configuración de Reseed te permite resembrar manualmente tu router si el reseed automático falla. El reseed es el proceso de arranque utilizado para encontrar otros routers cuando instalas I2P por primera vez, o cuando tu router tiene muy pocas referencias de routers restantes.

**Cuándo Usar Reseed Manual:**

1. Si el reseed ha fallado, primero debes verificar tu conexión de red
2. Si un firewall está bloqueando tus conexiones a los hosts de reseed, es posible que tengas acceso a un proxy:
   - El proxy puede ser un proxy público remoto, o puede estar ejecutándose en tu computadora (localhost)
   - Para usar un proxy, configura el tipo, host y puerto en la sección de Configuración de Reseeding
   - Si estás ejecutando Tor Browser, haz reseed a través de él configurando SOCKS 5, localhost, puerto 9150
   - Si estás ejecutando Tor por línea de comandos, haz reseed a través de él configurando SOCKS 5, localhost, puerto 9050
   - Si tienes algunos peers pero necesitas más, puedes probar la opción I2P Outproxy. Deja el host y el puerto en blanco. Esto no funcionará para un reseed inicial cuando no tienes peers en absoluto
   - Luego, haz clic en "Guardar cambios y hacer reseed ahora"
   - La configuración predeterminada funcionará para la mayoría de las personas. Cambia estas opciones solo si HTTPS está bloqueado por un firewall restrictivo y el reseed ha fallado

3. Si conoces y confías en alguien que ejecuta I2P, pídele que te envíe un archivo reseed generado usando esta página en su consola del router. Luego, usa esta página para hacer reseed con el archivo que recibiste. Primero, selecciona el archivo a continuación. Después, haz clic en "Reseed from file"

4. Si conoces y confías en alguien que publica archivos reseed, pídele la URL. Luego, usa esta página para hacer reseed con la URL que recibiste. Primero, ingresa la URL a continuación. Después, haz clic en "Reseed from URL"

5. Consulta [las preguntas frecuentes](/docs/overview/faq/) para obtener instrucciones sobre cómo resembrar manualmente

**Opciones de Reseed Manual:**

- **Reseed desde URL** - Ingresa una URL de archivo zip o su3 de una fuente confiable y haz clic en "Reseed from URL"
  - Se prefiere el formato su3, ya que se verificará como firmado por una fuente confiable
  - El formato zip no está firmado; usa un archivo zip solo de una fuente en la que confíes

- **Reseed desde Archivo** - Navega y selecciona un archivo zip o su3 local, luego haz clic en "Reseed from file"
  - Puedes encontrar archivos reseed en [checki2p.com/reseed](https://checki2p.com/reseed)

- **Crear Archivo de Reseed** - Generar un nuevo archivo zip de reseed que puedes compartir para que otros hagan reseed manualmente
  - Este archivo nunca contendrá la identidad de tu propio router ni tu IP

**Configuración de Reseeding:**

La configuración predeterminada funcionará para la mayoría de las personas. Cambie estos valores solo si HTTPS está bloqueado por un firewall restrictivo y el reseed ha fallado.

- **URLs de Reseed** - Lista de URLs HTTPS a servidores de reseed (la lista predeterminada está integrada y se actualiza regularmente)
- **Configuración de Proxy** - Configura proxy HTTP/HTTPS/SOCKS si necesitas acceder a los servidores de reseed a través de un proxy
- **Restablecer lista de URLs** - Restaura la lista predeterminada de servidores de reseed

**Importante:** El reseed manual solo debería ser necesario en casos excepcionales donde el reseed automático falle repetidamente. La mayoría de los usuarios nunca necesitarán usar esta página.

### Configuración de la Red

**URL:** [Configuración de Familia de Router](http://127.0.0.1:7657/configfamily)

![Consola del Router Configuración de Familia de Routers](/images/router-console-config-family.png)

La página de Configuración de Familia de Routers te permite gestionar familias de routers. Los routers en la misma familia comparten una clave de familia, que los identifica como operados por la misma persona u organización. Esto evita que múltiples routers que controlas sean seleccionados para el mismo tunnel, lo que reduciría el anonimato.

**¿Qué es una Familia de Routers?**

Cuando operas múltiples routers I2P, debes configurarlos para que sean parte de la misma familia. Esto garantiza: - Tus routers no se usarán juntos en la misma ruta de túnel - Otros usuarios mantienen el anonimato adecuado cuando sus túneles usan tus routers - La red puede distribuir correctamente la participación en los túneles

**Familia Actual:**

La página muestra el nombre actual de la familia de tu router. Si no formas parte de una familia, esto estará vacío.

**Exportar Clave de Familia:**

- **Exporta la clave secreta de familia para importarla en otros routers que controles**
- Haz clic en "Export Family Key" para descargar tu archivo de clave de familia
- Importa esta clave en tus otros routers para añadirlos a la misma familia

**Abandonar Familia de Router:**

- **Dejar de ser miembro de la familia**
- Haz clic en "Abandonar familia" para eliminar este router de su familia actual
- Esta acción no se puede deshacer sin volver a importar la clave de familia

**Consideraciones Importantes:**

- **Registro Público Requerido:** Para que tu familia sea reconocida en toda la red, tu clave de familia debe ser añadida al código base de I2P por el equipo de desarrollo. Esto asegura que todos los routers en la red conozcan tu familia.
- **Contacta al equipo de I2P** para registrar tu clave de familia si operas múltiples routers públicos
- La mayoría de los usuarios que ejecutan solo un router nunca necesitarán usar esta función
- La configuración de familia es utilizada principalmente por operadores de múltiples routers públicos o proveedores de infraestructura

**Casos de Uso:**

- Operar múltiples routers I2P para redundancia
- Ejecutar infraestructura como servidores reseed o outproxies en múltiples máquinas
- Gestionar una red de routers I2P para una organización

### Configuración de Pares

**URL:** [Configuración de Túneles](http://127.0.0.1:7657/configtunnels)

![Configuración de Túneles de la Consola del Router](/images/router-console-config-tunnels.png)

La página de Configuración de Túneles te permite ajustar la configuración predeterminada de túneles tanto para túneles exploratorios (usados para la comunicación del router) como para túneles de cliente (usados por aplicaciones). **La configuración predeterminada funciona para la mayoría de las personas y solo debería cambiarse si comprendes las compensaciones.**

**Advertencias Importantes:**

⚠️ **Compensación entre Anonimato y Rendimiento:** Existe una compensación fundamental entre el anonimato y el rendimiento. Los túneles de más de 3 saltos (por ejemplo, 2 saltos + 0-2 saltos, 3 saltos + 0-1 saltos, 3 saltos + 0-2 saltos), o una cantidad alta + cantidad de respaldo, pueden reducir gravemente el rendimiento o la fiabilidad. Esto puede resultar en un uso elevado de CPU y/o ancho de banda saliente. Modifique estos ajustes con precaución y ajústelos si tiene problemas.

⚠️ **Persistencia:** Los cambios en la configuración de túneles exploratorios se almacenan en el archivo router.config. Los cambios en túneles de cliente son temporales y no se guardan. Para realizar cambios permanentes en túneles de cliente, consulta la [página de I2PTunnel](/docs/api/i2ptunnel).

**Túneles Exploratorios:**

Los túneles exploratorios son utilizados por tu router para comunicarse con la base de datos de red y participar en la red I2P.

Opciones de configuración tanto para Inbound como para Outbound: - **Length** - Número de saltos en el tunnel (por defecto: 2-3 saltos) - **Randomization** - Variación aleatoria en la longitud del tunnel (por defecto: 0-1 saltos) - **Quantity** - Número de tunnels activos (por defecto: 2 tunnels) - **Backup quantity** - Número de tunnels de respaldo listos para activarse (por defecto: 0 tunnels)

**Túneles de Cliente para Servidor Web I2P:**

Estas configuraciones controlan los túneles para el servidor web I2P integrado (eepsite).

⚠️ **ADVERTENCIA DE ANONIMATO** - La configuración incluye túneles de 1 salto. ⚠️ **ADVERTENCIA DE RENDIMIENTO** - La configuración incluye cantidades elevadas de túneles.

Opciones de configuración tanto para Entrante como para Saliente: - **Longitud** - Longitud del túnel (por defecto: 1 salto para servidor web) - **Aleatorización** - Variación aleatoria en la longitud del túnel - **Cantidad** - Número de túneles activos - **Cantidad de respaldo** - Número de túneles de respaldo

**Túneles de Cliente para Clientes Compartidos:**

Estas configuraciones se aplican a las aplicaciones cliente compartidas (proxy HTTP, IRC, etc.).

Opciones de configuración tanto para Entrada como para Salida: - **Length** - Longitud del túnel (por defecto: 3 saltos) - **Randomization** - Varianza aleatoria en la longitud del túnel - **Quantity** - Número de túneles activos - **Backup quantity** - Número de túneles de respaldo

**Comprender los Parámetros de Túnel:**

- **Longitud:** Los túneles más largos proporcionan mayor anonimato pero reducen el rendimiento y la fiabilidad
- **Aleatorización:** Añade imprevisibilidad a las rutas de los túneles, mejorando la seguridad
- **Cantidad:** Más túneles mejoran la fiabilidad y distribución de carga pero aumentan el uso de recursos
- **Cantidad de respaldo:** Túneles preconstruidos listos para reemplazar túneles fallidos, mejorando la resiliencia

**Mejores Prácticas:**

- Mantén la configuración predeterminada a menos que tengas necesidades específicas
- Solo aumenta la longitud del túnel si el anonimato es crítico y puedes aceptar un rendimiento más lento
- Aumenta la cantidad/respaldo solo si experimentas fallos frecuentes de túneles
- Monitorea el rendimiento del router después de realizar cambios
- Haz clic en "Save changes" para aplicar las modificaciones

### Configuración de Reseed

**URL:** [Configuración de la UI](http://127.0.0.1:7657/configui)

![Interfaz de configuración de la Consola del Router](/images/router-console-config-ui.png)

La página de Configuración de UI te permite personalizar la apariencia y accesibilidad de tu consola del router, incluyendo selección de tema, preferencias de idioma y protección con contraseña.

**Tema de la Consola del Router:**

Elige entre temas oscuros y claros para la interfaz de la consola del router:
- **Oscuro** - Tema en modo oscuro (más cómodo para la vista en ambientes con poca luz)
- **Claro** - Tema en modo claro (apariencia tradicional)

Opciones adicionales de tema: - **Establecer tema universalmente en todas las aplicaciones** - Aplicar el tema seleccionado a todas las aplicaciones I2P, no solo a la consola del router - **Forzar el uso de la consola móvil** - Utilizar la interfaz optimizada para móviles incluso en navegadores de escritorio - **Incrustar aplicaciones de Email y Torrent en la consola** - Integrar Susimail e I2PSnark directamente en la interfaz de la consola en lugar de abrirlas en pestañas separadas

**Idioma de la Consola del Router:**

Selecciona tu idioma preferido para la interfaz de la consola del router desde el menú desplegable. I2P admite muchos idiomas incluyendo inglés, alemán, francés, español, ruso, chino, japonés y más.

**Bienvenidas las contribuciones a las traducciones:** Si notas traducciones incompletas o incorrectas, puedes ayudar a mejorar I2P contribuyendo al proyecto de traducción. Contacta a los desarrolladores en #i2p-dev en IRC o revisa el informe de estado de traducción (enlazado en la página).

**Contraseña de la Consola del Router:**

Añade autenticación de nombre de usuario y contraseña para proteger el acceso a tu consola del router:

- **Nombre de usuario** - Ingrese el nombre de usuario para acceder a la consola
- **Contraseña** - Ingrese la contraseña para acceder a la consola
- **Añadir usuario** - Crear un nuevo usuario con las credenciales especificadas
- **Eliminar seleccionados** - Eliminar cuentas de usuario existentes

**¿Por qué añadir una contraseña?**

- Previene el acceso local no autorizado a tu consola del router
- Esencial si varias personas usan tu computadora
- Recomendado si tu consola del router es accesible en tu red local
- Protege tu configuración de I2P y ajustes de privacidad contra manipulación

**Nota de Seguridad:** La protección con contraseña solo afecta el acceso a la interfaz web de la consola del router en la [Consola del Router I2P](http://127.0.0.1:7657). No cifra el tráfico de I2P ni impide que las aplicaciones usen I2P. Si eres el único usuario de tu computadora y la consola del router solo escucha en localhost (predeterminado), puede que no sea necesaria una contraseña.

### Configuración de Familia de Router

**URL:** [Configuración de WebApp](http://127.0.0.1:7657/configwebapps)

![Configuración de WebApp de la Consola del Router](/images/router-console-config-webapps.png)

La página de Configuración de WebApp te permite gestionar las aplicaciones web Java que se ejecutan dentro de tu router I2P. Estas aplicaciones son iniciadas por el cliente webConsole y se ejecutan en la misma JVM que el router, proporcionando funcionalidad integrada accesible a través de la consola del router.

**¿Qué son las WebApps?**

Las WebApps son aplicaciones basadas en Java que pueden ser:
- **Aplicaciones completas** (ej. I2PSnark para torrents)
- **Interfaces front-end para otros clientes** que deben habilitarse por separado (ej. Susidns, I2PTunnel)
- **Aplicaciones web sin interfaz web** (ej. libreta de direcciones)

**Notas Importantes:**

- Una webapp puede estar deshabilitada completamente, o puede estar deshabilitada solo para no ejecutarse al inicio
- Eliminar un archivo war del directorio webapps deshabilita la webapp completamente
- Sin embargo, el archivo .war y el directorio de la webapp reaparecerán cuando actualices tu router a una versión más reciente
- **Para deshabilitar permanentemente una webapp:** Deshabílala aquí, que es el método preferido

**WebApps Disponibles:**

| WebApp | Description |
|--------|-------------|
| **i2psnark** | Torrents - Built-in BitTorrent client for I2P |
| **i2ptunnel** | Hidden Services Manager - Configure client and server tunnels |
| **imagegen** | Identification Image Generator - Creates unique identicons |
| **jsonrpc** | jsonrpc.war - JSON-RPC API interface (disabled by default) |
| **routerconsole** | I2P Router Console - The main administrative interface |
| **susidns** | Address Book - Manage I2P addresses and subscriptions |
| **susimail** | Email - Web-based email client for I2P |
**Controles:**

Para cada webapp: - **¿Ejecutar al inicio?** - Casilla de verificación para habilitar/deshabilitar el inicio automático - **Control** - Botones Iniciar/Detener para control inmediato   - **Detener** - Detiene la webapp actualmente en ejecución   - **Iniciar** - Inicia una webapp detenida

**Botones de Configuración:**

- **Cancelar** - Descartar los cambios y volver a la página anterior
- **Guardar Configuración de WebApp** - Guardar los cambios y aplicarlos

**Casos de Uso:**

- Detén I2PSnark si no usas torrents para ahorrar recursos
- Desactiva jsonrpc si no necesitas acceso a la API
- Detén Susimail si usas un cliente de correo externo
- Detén temporalmente las webapps para liberar memoria o solucionar problemas

**Consejo de Rendimiento:** Deshabilitar las aplicaciones web no utilizadas puede reducir el uso de memoria y mejorar el rendimiento del router, especialmente en sistemas con recursos limitados.

## Help

**URL:** [Ayuda](http://127.0.0.1:7657/help)

La página de Ayuda proporciona documentación exhaustiva y recursos para ayudarte a comprender y usar I2P de manera efectiva. Sirve como centro principal para solucionar problemas, aprender y obtener soporte.

**Lo que encontrarás:**

- **Guía de inicio rápido** - Información esencial para nuevos usuarios que comienzan a usar I2P
- **Preguntas frecuentes (FAQ)** - Respuestas a preguntas comunes sobre la instalación, configuración y uso de I2P
- **Solución de problemas** - Soluciones a problemas comunes y cuestiones de conectividad
- **Documentación técnica** - Información detallada sobre protocolos, arquitectura y especificaciones de I2P
- **Guías de aplicaciones** - Instrucciones para usar aplicaciones de I2P como torrents, correo electrónico y servicios ocultos
- **Información de la red** - Comprender cómo funciona I2P y qué lo hace seguro
- **Recursos de soporte** - Enlaces a foros, canales IRC y soporte comunitario

**Obtener Ayuda:**

Si estás experimentando problemas con I2P: 1. Consulta las preguntas frecuentes (FAQ) para preguntas y respuestas comunes 2. Revisa la sección de solución de problemas para tu problema específico 3. Visita el foro de I2P en [i2pforum.i2p](http://i2pforum.i2p) o [i2pforum.net](https://i2pforum.net) 4. Únete al canal IRC #i2p para soporte de la comunidad en tiempo real 5. Busca en la documentación para información técnica detallada

**Consejo:** La página de ayuda siempre es accesible desde la barra lateral de la consola del router, lo que facilita encontrar asistencia cuando la necesites.

## Performance Graphs

**URL:** [Gráficos de Rendimiento](http://127.0.0.1:7657/graphs)

![Gráficos de rendimiento de la consola del router](/images/router-console-graphs.png)

La página de Gráficos de Rendimiento proporciona monitoreo visual en tiempo real del rendimiento de tu router I2P y la actividad de red. Estos gráficos te ayudan a comprender el uso de ancho de banda, las conexiones con peers, el consumo de memoria y el estado general del router.

**Gráficos Disponibles:**

- **Uso de Ancho de Banda**
  - **Tasa de envío de bajo nivel (bytes/seg)** - Tasa de tráfico saliente
  - **Tasa de recepción de bajo nivel (bytes/seg)** - Tasa de tráfico entrante
  - Muestra la utilización actual, promedio y máxima del ancho de banda
  - Ayuda a monitorear si te estás acercando a tus límites de ancho de banda configurados

- **Pares Activos**
  - **router.activePeers promediado durante 60 seg** - Número de pares con los que te estás comunicando activamente
  - Muestra la salud de tu conectividad de red
  - Más pares activos generalmente significa mejor construcción de túneles y participación en la red

- **Uso de Memoria del Router**
  - **router.memoryUsed promediado durante 60 seg** - Consumo de memoria de la JVM
  - Muestra el uso de memoria actual, promedio y máximo en MB
  - Útil para identificar fugas de memoria o determinar si necesitas aumentar el tamaño del heap de Java

**Configurar Visualización de Gráficos:**

Personaliza cómo se muestran y actualizan los gráficos:

- **Tamaño del gráfico** - Establece el ancho (predeterminado: 400 píxeles) y la altura (predeterminado: 100 píxeles)
- **Período de visualización** - Rango de tiempo a mostrar (predeterminado: 60 minutos)
- **Intervalo de actualización** - Con qué frecuencia se actualizan los gráficos (predeterminado: 5 minutos)
- **Tipo de gráfico** - Elije entre visualización de Promedios o Eventos
- **Ocultar leyenda** - Elimina la leyenda de los gráficos para ahorrar espacio
- **UTC** - Usa hora UTC en lugar de hora local en los gráficos
- **Persistencia** - Almacena datos del gráfico en disco para análisis histórico

**Opciones Avanzadas:**

Haz clic en **[Select Stats]** para elegir qué estadísticas graficar: - Métricas de tunnel (tasa de éxito de construcción, cantidad de tunnels, etc.) - Estadísticas de la base de datos de red - Estadísticas de transporte (NTCP2, SSU2) - Rendimiento de tunnels de cliente - Y muchas más métricas detalladas

**Casos de Uso:**

- Monitorea el ancho de banda para asegurar que no excedas tus límites configurados
- Verifica la conectividad de peers al solucionar problemas de red
- Rastrea el uso de memoria para optimizar la configuración del heap de Java
- Identifica patrones de rendimiento a lo largo del tiempo
- Diagnostica problemas de construcción de tunnels correlacionando gráficas

**Consejo:** Haz clic en "Guardar configuración y redibujar gráficas" después de realizar cambios para aplicar tu configuración. Las gráficas se actualizarán automáticamente según tu configuración de intervalo de actualización.
