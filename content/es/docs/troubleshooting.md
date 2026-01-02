---
title: "Guía de solución de problemas del I2P Router"
description: "Guía exhaustiva de resolución de problemas para incidencias comunes del router I2P, incluidos problemas de conectividad, rendimiento y configuración"
slug: "troubleshooting"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
type: docs
---

Los routers I2P fallan con mayor frecuencia debido a **problemas de reenvío de puertos**, **asignación de ancho de banda insuficiente** y **tiempo de bootstrap insuficiente (tiempo de arranque inicial)**. Estos tres factores explican más del 70% de los problemas reportados. El router requiere al menos **10-15 minutos** tras el inicio para integrarse por completo en la red, **128 KB/sec de ancho de banda mínimo** (se recomiendan 256 KB/sec) y un **reenvío de puertos UDP/TCP** adecuado para alcanzar un estado no bloqueado por firewall. Los usuarios nuevos a menudo esperan conectividad inmediata y reinician prematuramente, lo que restablece el progreso de integración y crea un ciclo frustrante. Esta guía proporciona soluciones detalladas para todos los problemas principales de I2P que afectan a las versiones 2.10.0 y posteriores.

La arquitectura de anonimato de I2P sacrifica de forma inherente la velocidad en favor de la privacidad mediante tunnels cifrados de múltiples saltos. Comprender este diseño fundamental ayuda a los usuarios a establecer expectativas realistas y a solucionar problemas de forma eficaz, en lugar de malinterpretar el comportamiento normal como problemas.

## Router no se inicia o se bloquea inmediatamente

Los fallos de inicio más comunes se deben a **conflictos de puertos**, **incompatibilidad de versiones de Java** o **archivos de configuración corruptos**. Comprueba si ya se está ejecutando otra instancia de I2P antes de investigar problemas más profundos.

**Verifique que no haya procesos en conflicto:**

Linux: `ps aux | grep i2p` o `netstat -tulpn | grep 7657`

Windows: Administrador de tareas → Detalles → busque java.exe con i2p en la línea de comandos

macOS: Monitor de Actividad → busca "i2p"

Si existe un proceso zombi, termínalo: `pkill -9 -f i2p` (Linux/Mac) o `taskkill /F /IM javaw.exe` (Windows)

**Comprueba la compatibilidad de la versión de Java:**

I2P 2.10.0+ requiere **Java 8 como mínimo**, se recomienda Java 11 o posterior. Verifique que su instalación muestre "mixed mode" (no "interpreted mode"):

```bash
java -version
```
Debería mostrar: OpenJDK o Oracle Java, versión 8+, "mixed mode"

**Evite:** GNU GCJ, implementaciones de Java obsoletas, modos solo interpretados

**Conflictos comunes de puertos** se producen cuando varios servicios compiten por los puertos predeterminados de I2P. La consola del router (7657), I2CP (7654), SAM (7656) y el proxy HTTP (4444) deben estar disponibles. Comprueba si hay conflictos: `netstat -ano | findstr "7657 4444 7654"` (Windows) o `lsof -i :7657,4444,7654` (Linux/Mac).

**Corrupción del archivo de configuración** se manifiesta como bloqueos inmediatos con errores de análisis en los registros. Router.config requiere **codificación UTF-8 sin BOM**, usa `=` como separador (no `:`) y prohíbe ciertos caracteres especiales. Haz una copia de seguridad y luego examina: `~/.i2p/router.config` (Linux), `%LOCALAPPDATA%\I2P\router.config` (Windows), `~/Library/Application Support/i2p/router.config` (macOS).

Para restablecer la configuración manteniendo la identidad: Detenga I2P, haga una copia de seguridad de router.keys y del directorio keyData, elimine router.config, reinicie. El router regenera la configuración predeterminada.

**Asignación del heap de Java demasiado baja** causa fallos por OutOfMemoryError. Edita wrapper.config y aumenta `wrapper.java.maxmemory` desde el valor predeterminado de 128 o 256 a **512 como mínimo** (1024 para routers de alto ancho de banda). Esto requiere un apagado completo, esperar 11 minutos y luego reiniciar - hacer clic en "Restart" en la consola no aplicará el cambio.

## Resolver el estado "Network: Firewalled"

El estado firewalled significa que el router no puede recibir conexiones entrantes directas, lo que obliga a depender de introducers (nodos introductores). Aunque el router funciona en este estado, **el rendimiento se degrada significativamente** y la contribución a la red sigue siendo mínima. Alcanzar un estado no firewalled requiere un reenvío de puertos adecuado.

**El router selecciona aleatoriamente un puerto** entre 9000-31000 para comunicaciones. Encuentra tu puerto en http://127.0.0.1:7657/confignet - busca "UDP Port" y "TCP Port" (normalmente el mismo número). Debes reenviar **tanto UDP como TCP** para un rendimiento óptimo, aunque solo UDP permite la funcionalidad básica.

**Habilitar el reenvío automático mediante UPnP** (método más simple):

1. Accede a http://127.0.0.1:7657/confignet
2. Marca "Enable UPnP"
3. Guarda los cambios y reinicia el router
4. Espera 5-10 minutos y verifica que el estado cambie de "Network: Firewalled" a "Network: OK"

UPnP requiere soporte del router (habilitado de forma predeterminada en la mayoría de los routers de consumo fabricados después de 2010) y una configuración de red adecuada.

**Reenvío de puertos manual** (requerido cuando UPnP falla):

1. Anota tu puerto de I2P en http://127.0.0.1:7657/confignet (p. ej., 22648)
2. Encuentra tu dirección IP local: `ipconfig` (Windows), `ip addr` (Linux), Preferencias del Sistema → Red (macOS)
3. Accede a la interfaz de administración de tu router (normalmente 192.168.1.1 o 192.168.0.1)
4. Ve a Redirección de puertos (puede estar en Avanzado, NAT o Servidores virtuales)
5. Crea dos reglas:
   - Puerto externo: [tu puerto de I2P] → IP interna: [tu equipo] → Puerto interno: [igual] → Protocolo: **UDP**
   - Puerto externo: [tu puerto de I2P] → IP interna: [tu equipo] → Puerto interno: [igual] → Protocolo: **TCP**
6. Guarda la configuración y reinicia tu router si es necesario

**Verifica el reenvío de puertos** usando comprobadores en línea después de configurarlo. Si la detección falla, revisa la configuración del cortafuegos - tanto el cortafuegos del sistema como el cortafuegos de cualquier antivirus deben permitir el puerto de I2P.

**Alternativa de Hidden mode (modo oculto)** para redes restrictivas donde el reenvío de puertos no es posible: Actívalo en http://127.0.0.1:7657/confignet → marca "Hidden mode". El router permanece detrás de un cortafuegos pero se optimiza para este estado utilizando exclusivamente SSU introducers (nodos introductores). El rendimiento será más lento pero funcional.

## Router atascado en los estados "Starting" o "Testing"

Estos estados transitorios durante el arranque inicial suelen resolverse en **10-15 minutos para instalaciones nuevas** o **3-5 minutos para routers establecidos**. La intervención prematura a menudo empeora los problemas.

**"Network: Testing"** indica que el router está comprobando la alcanzabilidad mediante varios tipos de conexión (directa, introducers (presentadores), múltiples versiones de protocolo). Esto es **normal durante los primeros 5-10 minutos** tras el arranque. El router prueba múltiples escenarios para determinar la configuración óptima.

**"Rejecting tunnels: starting up"** aparece durante la fase de arranque cuando el router carece de información suficiente sobre pares. El router no participará en el tráfico de retransmisión hasta integrarse adecuadamente. Este mensaje debería desaparecer después de 10-20 minutos, una vez que netDb se pueble con más de 50 routers.

**El desfase del reloj arruina las pruebas de alcanzabilidad.** I2P requiere que la hora del sistema esté dentro de **±60 segundos** de la hora de la red. Una diferencia superior a 90 segundos provoca el rechazo automático de la conexión. Sincroniza el reloj de tu sistema:

Linux: `sudo timedatectl set-ntp true && sudo systemctl restart systemd-timesyncd`

Windows: Panel de control → Fecha y hora → Hora de Internet → Actualizar ahora → Habilitar sincronización automática

macOS: Preferencias del Sistema → Fecha y hora → Activa "Ajustar la fecha y la hora automáticamente"

Después de corregir el desfase del reloj, reinicia I2P por completo para una integración adecuada.

**Asignación de ancho de banda insuficiente** impide realizar pruebas con éxito. El router necesita capacidad adecuada para construir tunnels de prueba. Configúrelo en http://127.0.0.1:7657/config:

- **Mínimo viable:** Entrante 96 KB/sec, Saliente 64 KB/sec
- **Estándar recomendado:** Entrante 256 KB/sec, Saliente 128 KB/sec  
- **Rendimiento óptimo:** Entrante 512+ KB/sec, Saliente 256+ KB/sec
- **Porcentaje de compartición:** 80% (permite que el router aporte ancho de banda a la red)

Un menor ancho de banda puede funcionar, pero prolonga el tiempo de integración de minutos a horas.

**netDb corrupta** debido a un apagado incorrecto o a errores de disco provoca bucles de prueba perpetuos. El router no puede completar las pruebas sin datos de pares válidos:

```bash
# Stop I2P completely
i2prouter stop    # or systemctl stop i2p

# Delete corrupted database (safe - will reseed automatically)
rm -rf ~/.i2p/netDb/*

# Restart and allow 10-15 minutes for reseed
i2prouter start
```
Windows: Elimina el contenido de `%APPDATA%\I2P\netDb\` o `%LOCALAPPDATA%\I2P\netDb\`

**El firewall que bloquea el reseed (obtención inicial de pares)** impide adquirir pares iniciales. Durante el arranque, I2P recupera información del router de servidores de reseed mediante HTTPS. Los firewalls corporativos o de los ISP (proveedores de servicios de Internet) pueden bloquear estas conexiones. Configure el proxy de reseed en http://127.0.0.1:7657/configreseed si opera detrás de redes restrictivas.

## Velocidades lentas, tiempos de espera agotados y fallos en la construcción de tunnels

El diseño de I2P produce de forma inherente **velocidades 3-10x más lentas que clearnet (internet abierta)** debido al cifrado de múltiples saltos, la sobrecarga de paquetes y la imprevisibilidad de las rutas. La construcción de un tunnel recorre múltiples routers, cada uno añadiendo latencia. Comprender esto evita diagnosticar erróneamente un comportamiento normal como problemas.

**Expectativas típicas de rendimiento:**

- Navegación web de sitios .i2p: cargas de página de 10-30 segundos inicialmente, más rápidas tras el establecimiento del tunnel
- Uso de torrents con I2PSnark: 10-100 KB/s por torrent según las semillas y las condiciones de la red  
- Descargas de archivos grandes: se requiere paciencia - archivos de megabytes pueden tardar minutos, los de gigabytes toman horas
- La primera conexión es la más lenta: la creación del tunnel tarda 30-90 segundos; las conexiones posteriores usan tunnels existentes

**Tasa de éxito en la construcción de Tunnel** indica la salud de la red. Consulta en http://127.0.0.1:7657/tunnels:

- **Por encima del 60%:** Funcionamiento normal y saludable
- **40-60%:** Marginal; considere aumentar el ancho de banda o reducir la carga
- **Por debajo del 40%:** Problemático - indica ancho de banda insuficiente, problemas de red o mala selección de pares

**Aumenta la asignación de ancho de banda** como primera optimización. La mayoría de los problemas de lentitud se deben a una escasez de ancho de banda. En http://127.0.0.1:7657/config, aumenta los límites de forma incremental y supervisa las gráficas en http://127.0.0.1:7657/graphs.

**Para DSL/Cable (conexiones de 1-10 Mbps):** - Entrante: 400 KB/sec - Saliente: 200 KB/sec - Compartir: 80% - Memoria: 384 MB (editar wrapper.config)

**Para conexiones de alta velocidad (10-100+ Mbps):** - Entrante: 1500 KB/sec   - Saliente: 1000 KB/sec - Compartir: 80-100% - Memoria: 512-1024 MB - Considere: aumentar los tunnels participantes a 2000-5000 en http://127.0.0.1:7657/configadvanced

**Optimiza la configuración del tunnel** para mejorar el rendimiento. Accede a la configuración específica del tunnel en http://127.0.0.1:7657/i2ptunnel y edita cada tunnel:

- **Cantidad de tunnel:** Aumentar de 2 a 3-4 (más rutas disponibles)
- **Cantidad de respaldo:** Establecer en 1-2 (conmutación por error rápida si el tunnel falla)
- **Longitud del tunnel:** El valor predeterminado de 3 saltos ofrece un buen equilibrio; reducir a 2 mejora la velocidad pero disminuye el anonimato

**Biblioteca criptográfica nativa (jbigi)** ofrece un rendimiento 5-10x mejor que el cifrado en Java puro. Verifica que esté cargada en http://127.0.0.1:7657/logs - busca "jbigi loaded successfully" o "Using native CPUID implementation". Si no aparecen:

Linux: Por lo general se detecta automáticamente y se carga desde ~/.i2p/jbigi-*.so Windows: Verifica que exista jbigi.dll en el directorio de instalación de I2P Si falta: Instala las herramientas de compilación y compila desde el código fuente, o descarga binarios precompilados de los repositorios oficiales

**Mantén el router funcionando de forma continua.** Cada reinicio restablece la integración y requiere 30-60 minutos para reconstruir la red de tunnel y las relaciones con pares. Los routers estables con alto tiempo de actividad reciben selección preferente para la construcción de tunnel, creando una retroalimentación positiva para el rendimiento.

## Alto consumo de CPU y memoria

El uso excesivo de recursos suele indicar **asignación de memoria insuficiente**, **ausencia de bibliotecas criptográficas nativas** o **compromiso excesivo con la participación en la red**. Los routers bien configurados deberían consumir un 10-30% de CPU durante el uso activo y mantener la memoria estable por debajo del 80% del heap (montón de memoria) asignado.

**Los problemas de memoria se manifiestan como:** - Gráficas de memoria con parte superior plana (clavadas en el máximo) - Recolección de basura frecuente (patrón de diente de sierra con caídas pronunciadas) - OutOfMemoryError en los registros (error por falta de memoria) - El router deja de responder bajo carga - Apagado automático debido al agotamiento de recursos

**Aumenta la asignación del heap (área de memoria) de Java** en wrapper.config (requiere un apagado completo):

```bash
# Linux: ~/.i2p/wrapper.config
# Windows: %APPDATA%\I2P\wrapper.config  
# Find and modify:
wrapper.java.maxmemory=512

# Recommendations by usage:
# Light browsing only: 256
# Standard use (browsing + light torrenting): 512
# Heavy use (multiple applications, active torrenting): 768-1024
# Floodfill or very high bandwidth: 1024-2048
```
**Crítico:** Después de editar wrapper.config, **debe apagar por completo** (no reiniciar), esperar 11 minutos para una terminación ordenada y luego iniciar desde cero. El botón "Restart" de la consola del router no recarga la configuración de wrapper.

**La optimización de CPU requiere una biblioteca criptográfica nativa.** Las operaciones de BigInteger en Java puro consumen entre 10 y 20 veces más CPU que las implementaciones nativas. Verifique el estado de jbigi en http://127.0.0.1:7657/logs durante el inicio. Sin jbigi, la CPU se disparará al 50-100% durante la construcción de tunnel y las operaciones de cifrado.

**Reducir la carga de tunnel participante** si el router está sobrecargado:

1. Accede a http://127.0.0.1:7657/configadvanced
2. Establece `router.maxParticipatingTunnels=1000` (predeterminado 8000)
3. Reduce el porcentaje de compartición en http://127.0.0.1:7657/config del 80% al 50%
4. Desactiva el modo floodfill si está habilitado: `router.floodfillParticipant=false`

**Limita el ancho de banda de I2PSnark y los torrents concurrentes.** El uso de torrents consume recursos considerables. En http://127.0.0.1:7657/i2psnark:

- Limita los torrents activos a 3-5 como máximo
- Configura "Límite de ancho de banda de subida" y "Límite de ancho de banda de bajada" en valores razonables (50-100 KB/sec cada uno)
- Detén los torrents cuando no se necesiten activamente
- Evita sembrar docenas de torrents simultáneamente

**Supervisa el uso de recursos** mediante los gráficos integrados en http://127.0.0.1:7657/graphs. La memoria debería mostrar margen disponible, no un tope plano. Los picos de CPU durante la construcción de tunnel son normales; un uso alto y sostenido de CPU indica problemas de configuración.

**Para sistemas con recursos muy limitados** (Raspberry Pi, hardware antiguo), considera **i2pd** (implementación en C++) como alternativa. i2pd requiere ~130 MB de RAM frente a 350+ MB para Java I2P, y utiliza ~7% de CPU frente a 70% bajo cargas similares. Ten en cuenta que i2pd carece de aplicaciones integradas y requiere herramientas externas.

## Problemas con torrents en I2PSnark

La integración de I2PSnark con la arquitectura del router de I2P requiere comprender que **el uso de torrents depende por completo del estado de los tunnels del router**. Los torrents no se iniciarán hasta que el router alcance una integración adecuada con 10 o más pares activos y cuente con tunnels en funcionamiento.

**Los torrents atascados en 0% suelen indicar:**

1. **Router no completamente integrado:** Espera 10-15 minutos después de iniciar I2P antes de esperar actividad de torrents
2. **DHT (tabla hash distribuida) deshabilitado:** Actívalo en http://127.0.0.1:7657/i2psnark → Configuración → marca "Enable DHT" (activado por defecto desde la versión 0.9.2)
3. **Rastreadores no válidos o caídos:** Los torrents de I2P requieren rastreadores específicos de I2P - los rastreadores de clearnet no funcionarán
4. **Configuración de tunnel insuficiente:** Aumenta los tunnels en Configuración de I2PSnark → sección Tunnels

**Configura los tunnels de I2PSnark para un mejor rendimiento:**

- Tunnels entrantes: 3-5 (por defecto 2 para Java I2P, 5 para i2pd)
- Tunnels salientes: 3-5  
- Longitud del tunnel: 3 saltos (reduzca a 2 para mayor velocidad, menos anonimato)
- Cantidad de tunnels: 3 (proporciona un rendimiento constante)

**Rastreadores de torrents esenciales de I2P** para incluir: - tracker2.postman.i2p (principal, el más confiable) - w7tpbzncbcocrqtwwm3nezhnnsw4ozadvi2hmvzdhrqzfxfum7wa.b32.i2p/a

Elimina todos los trackers de clearnet (non-.i2p) - no aportan ningún valor y generan intentos de conexión que agotan el tiempo de espera.

**errores "Torrent not registered"** ocurren cuando falla la comunicación con el tracker. Haz clic derecho en el torrent → "Start" fuerza un reanuncio. Si persiste, verifica la accesibilidad del tracker visitando http://tracker2.postman.i2p en un navegador configurado para I2P. Los trackers inactivos deben reemplazarse por alternativas funcionales.

**No se conectan pares** a pesar del éxito del tracker, lo que sugiere: - Router detrás de un firewall (mejora con el reenvío de puertos, pero no es obligatorio) - Ancho de banda insuficiente (aumenta a 256+ KB/s)   - Enjambre demasiado pequeño (algunos torrents tienen 1-2 semillas; se requiere paciencia) - DHT desactivado (actívalo para el descubrimiento de pares sin tracker)

**Activa DHT y PEX (Intercambio de pares)** en la configuración de I2PSnark. DHT permite encontrar pares sin depender de rastreadores. PEX descubre pares a partir de los pares conectados, acelerando el descubrimiento del enjambre.

**Corrupción de archivos descargados** rara vez ocurre con la comprobación de integridad integrada de I2PSnark. Si se detecta:

1. Clic derecho en el torrent → "Check" fuerza el recálculo del hash de todas las piezas
2. Elimina los datos de torrent dañados (conserva el archivo .torrent)  
3. Clic derecho → "Start" para volver a descargar con verificación de piezas
4. Comprueba el disco en busca de errores si la corrupción persiste: `chkdsk` (Windows), `fsck` (Linux)

**El directorio vigilado no funciona** requiere una configuración adecuada:

1. Configuración de I2PSnark → "Watch directory": Establece la ruta absoluta (p. ej., `/home/user/torrents/watch`)
2. Asegúrate de que el proceso de I2P tenga permisos de lectura: `chmod 755 /path/to/watch`
3. Coloca los archivos .torrent en el directorio de vigilancia - I2PSnark los añade automáticamente
4. Configura "Auto start": Elige si los torrents deben iniciarse inmediatamente al añadirse

**Optimización del rendimiento para el uso de torrents:**

- Limita los torrents activos simultáneos: 3-5 como máximo para conexiones estándar
- Prioriza las descargas importantes: detén temporalmente los torrents de baja prioridad
- Aumenta la asignación de ancho de banda del router: más ancho de banda = mejor rendimiento de torrents
- Ten paciencia: el uso de torrents en I2P es por naturaleza más lento que BitTorrent en la clearnet
- Seed (compartir como fuente) después de descargar: la red prospera gracias a la reciprocidad

## Configuración y solución de problemas de Git a través de I2P

Las operaciones de Git a través de I2P requieren ya sea **configuración de proxy SOCKS** o **tunnels de I2P dedicados** para acceso SSH/HTTP. El diseño de Git asume conexiones de baja latencia, lo que hace que la arquitectura de alta latencia de I2P sea un desafío.

**Configurar Git para usar el proxy SOCKS de I2P:**

Edite ~/.ssh/config (créalo si no existe):

```
Host *.i2p
    ProxyCommand nc -X 5 -x 127.0.0.1:4447 %h %p
    ServerAliveInterval 60
    ServerAliveCountMax 3
    Compression yes
```
Esto encamina todas las conexiones SSH a hosts .i2p a través del proxy SOCKS de I2P (puerto 4447). Los parámetros ServerAlive mantienen la conexión durante la latencia de I2P.

Para operaciones de git vía HTTP/HTTPS, configura git globalmente:

```bash
git config --global http.proxy socks5h://127.0.0.1:4447
git config --global https.proxy socks5h://127.0.0.1:4447
```
Nota: `socks5h` realiza la resolución de DNS a través del proxy - crucial para los dominios .i2p.

**Crear un I2P tunnel dedicado para Git sobre SSH** (más fiable que SOCKS):

1. Accede a http://127.0.0.1:7657/i2ptunnel
2. "Nuevo tunnel de cliente" → "Estándar"
3. Configura:
   - Nombre: Git-SSH  
   - Tipo: Cliente
   - Puerto: 2222 (puerto local para acceso a Git)
   - Destino: [your-git-server].i2p:22
   - Inicio automático: Activado
   - Número de tunnel: 3-4 (más alto para mayor fiabilidad)
4. Guarda e inicia el tunnel
5. Configura SSH para usar el tunnel: `ssh -p 2222 git@127.0.0.1`

**Errores de autenticación de SSH** a través de I2P suelen deberse a:

- Clave no agregada al ssh-agent: `ssh-add ~/.ssh/id_rsa`
- Permisos incorrectos del archivo de la clave: `chmod 600 ~/.ssh/id_rsa`
- Tunnel no se está ejecutando: Verifica en http://127.0.0.1:7657/i2ptunnel que el estado sea verde
- El servidor Git requiere un tipo específico de clave: Genera una clave ed25519 si RSA falla

**Operaciones de Git que agotan el tiempo de espera** se relacionan con las características de latencia de I2P:

- Aumentar el tiempo de espera de Git: `git config --global http.postBuffer 524288000` (búfer de 500 MB)
- Aumentar el límite de baja velocidad: `git config --global http.lowSpeedLimit 1000` y `git config --global http.lowSpeedTime 600` (espera 10 minutos)
- Usar clonación superficial para el checkout inicial: `git clone --depth 1 [url]` (solo trae el último commit, más rápido)
- Clonar durante periodos de baja actividad: la congestión de la red afecta al rendimiento de I2P

**Operaciones lentas de git clone/fetch** son inherentes a la arquitectura de I2P. Un repositorio de 100MB puede tardar entre 30 y 60 minutos a través de I2P, frente a segundos en clearnet (internet abierta). Estrategias:

- Usa clones superficiales: `--depth 1` reduce drásticamente la transferencia de datos inicial
- Obtén de forma incremental: En lugar de un clon completo, obtén ramas específicas: `git fetch origin branch:branch`
- Considera rsync sobre I2P: Para repositorios muy grandes, rsync puede ofrecer mejor rendimiento
- Aumenta la cantidad de tunnels (túneles de I2P): Más tunnels proporcionan mejor rendimiento para transferencias grandes sostenidas

**Los errores "Connection refused"** indican una mala configuración del tunnel:

1. Verifica que el I2P router esté en ejecución: Revisa http://127.0.0.1:7657
2. Confirma que el tunnel esté activo y en verde en http://127.0.0.1:7657/i2ptunnel
3. Prueba el tunnel: `nc -zv 127.0.0.1 2222` (debería conectar si el tunnel está funcionando)
4. Comprueba que el destino sea alcanzable: Navega a la interfaz HTTP del destino si está disponible
5. Revisa los registros del tunnel en http://127.0.0.1:7657/logs en busca de errores específicos

**Mejores prácticas de Git sobre I2P:**

- Mantén el I2P router en ejecución de forma continua para un acceso estable a Git
- Usa claves SSH en lugar de autenticación por contraseña (menos indicaciones interactivas)
- Configura tunnels persistentes en lugar de conexiones SOCKS efímeras
- Considera alojar tu propio servidor Git en I2P para mayor control
- Documenta tus endpoints (puntos de conexión) de Git .i2p para tus colaboradores

## Acceder a eepsites y resolver dominios .i2p

La razón más frecuente por la que los usuarios no pueden acceder a los sitios .i2p es una **configuración incorrecta del proxy del navegador**. Los sitios de I2P existen únicamente dentro de la red de I2P y requieren enrutamiento a través del proxy HTTP de I2P.

**Configura exactamente los ajustes de proxy del navegador:**

**Firefox (recomendado para I2P):**

1. Menú → Configuración → Configuración de red → botón Configuración
2. Selecciona "Configuración manual de proxy"
3. Proxy HTTP: **127.0.0.1** Puerto: **4444**
4. Proxy SSL: **127.0.0.1** Puerto: **4444**  
5. Proxy SOCKS: **127.0.0.1** Puerto: **4447** (opcional, para aplicaciones SOCKS)
6. Marca "Proxy DNS al usar SOCKS v5"
7. OK para guardar

**Ajustes críticos de about:config de Firefox:**

Navega a `about:config` y modifica:

- `media.peerconnection.ice.proxy_only` = **true** (evita filtraciones de IP mediante WebRTC)
- `keyword.enabled` = **false** (evita que las direcciones .i2p se redirijan a motores de búsqueda)
- `network.proxy.socks_remote_dns` = **true** (DNS a través del proxy)

**Limitaciones de Chrome/Chromium:**

Chrome utiliza la configuración de proxy del sistema en lugar de una específica de la aplicación. En Windows: Configuración → busca "proxy" → "Abrir la configuración de proxy del equipo" → Configura HTTP: 127.0.0.1:4444 y HTTPS: 127.0.0.1:4445.

Mejor enfoque: Utiliza las extensiones FoxyProxy o Proxy SwitchyOmega para el enrutamiento selectivo de .i2p.

**"Website Not Found In Address Book" errores** significan que el router no tiene la dirección criptográfica del dominio .i2p. I2P usa libretas de direcciones locales en lugar de DNS centralizado. Soluciones:

**Método 1: Usar servicios de salto** (lo más sencillo para sitios nuevos):

Visita http://stats.i2p y busca el sitio. Haz clic en el enlace de addresshelper (ayuda de direcciones): `http://example.i2p/?i2paddresshelper=base64destination`. Tu navegador muestra "¿Guardar en la libreta de direcciones?" - confirma para añadirlo.

**Método 2: Actualizar las suscripciones de la libreta de direcciones:**

1. Accede a http://127.0.0.1:7657/dns (SusiDNS)
2. Haz clic en la pestaña "Subscriptions"  
3. Verifica las suscripciones activas (predeterminado: http://i2p-projekt.i2p/hosts.txt)
4. Añade suscripciones recomendadas:
   - http://stats.i2p/cgi-bin/newhosts.txt
   - http://notbob.i2p/hosts.txt
   - http://reg.i2p/export/hosts.txt
5. Haz clic en "Update Now" para forzar la actualización inmediata de las suscripciones
6. Espera de 5 a 10 minutos para el procesamiento

**Método 3: Usa direcciones base32** (siempre funciona si el sitio está en línea):

Cada sitio .i2p tiene una dirección base32: 52 caracteres aleatorios seguidos de .b32.i2p (p. ej., `ukeu3k5oycgaauneqgtnvselmt4yemvoilkln7jpvamvfx7dnkdq.b32.i2p`). Las direcciones Base32 omiten la libreta de direcciones - el router realiza una búsqueda criptográfica directa.

**Errores comunes de configuración del navegador:**

- Intentar HTTPS en sitios solo HTTP: La mayoría de los sitios .i2p usan solo HTTP - intentar `https://example.i2p` falla
- Olvidar el prefijo `http://`: El navegador puede buscar en lugar de conectarse - usa siempre `http://example.i2p`
- WebRTC habilitado: Puede filtrar la dirección IP real - desactívalo desde la configuración de Firefox o con extensiones
- DNS sin proxy: El DNS de clearnet (Internet abierta) no puede resolver .i2p - debes enviar las consultas DNS a través del proxy
- Puerto de proxy incorrecto: 4444 para HTTP (no 4445, que es un outproxy (proxy de salida) HTTPS hacia clearnet)

**Router no completamente integrado** impide el acceso a cualquier sitio. Verifique que la integración sea adecuada:

1. Comprueba que http://127.0.0.1:7657 muestre "Network: OK" o "Network: Firewalled" (no "Network: Testing")
2. Los pares activos muestran 10+ como mínimo (50+ óptimo)  
3. Que no aparezca el mensaje "Rejecting tunnels: starting up"
4. Espera 10-15 minutos completos después del arranque del router antes de esperar acceso a .i2p

**La configuración de los clientes de IRC y correo electrónico** sigue patrones de proxy similares:

**IRC:** Los clientes se conectan a **127.0.0.1:6668** (el tunnel proxy de IRC de I2P). Deshabilita la configuración de proxy del cliente de IRC - la conexión a localhost:6668 ya se realiza a través de I2P.

**Correo electrónico (Postman):**  - SMTP: **127.0.0.1:7659** - POP3: **127.0.0.1:7660**   - Sin SSL/TLS (cifrado gestionado por el I2P tunnel) - Credenciales del registro de la cuenta en postman.i2p

Todos estos tunnels deben mostrar el estado "running" (verde) en http://127.0.0.1:7657/i2ptunnel.

## Errores de instalación y problemas con paquetes

Las instalaciones basadas en paquetes (Debian, Ubuntu, Arch) ocasionalmente fallan debido a **cambios en los repositorios**, **expiración de la clave GPG** o **conflictos de dependencias**. Los repositorios oficiales cambiaron de deb.i2p2.de/deb.i2p2.no (fin de vida) a **deb.i2p.net** en versiones recientes.

**Actualizar el repositorio de Debian/Ubuntu a la versión actual:**

```bash
# Remove old repository entries
sudo rm /etc/apt/sources.list.d/i2p.list

# Add current repository
echo "deb [signed-by=/usr/share/keyrings/i2p-archive-keyring.gpg] https://deb.i2p.net/ $(lsb_release -sc) main" | sudo tee /etc/apt/sources.list.d/i2p.list

# Download and install current signing key
curl -o i2p-archive-keyring.gpg https://geti2p.net/_static/i2p-archive-keyring.gpg
sudo cp i2p-archive-keyring.gpg /usr/share/keyrings/

# Update and install
sudo apt update
sudo apt install i2p i2p-keyring
```
**Fallos en la verificación de firmas GPG** se producen cuando las claves del repositorio expiran o cambian:

```bash
# Error: "The following signatures were invalid"
# Solution: Install current keyring package
sudo apt install i2p-keyring

# Manual key import if package unavailable
wget https://geti2p.net/_static/i2p-debian-repo.key.asc
sudo apt-key add i2p-debian-repo.key.asc
```
**El servicio no se inicia después de la instalación del paquete** suele deberse a problemas con el perfil de AppArmor en Debian/Ubuntu:

```bash
# Check service status
sudo systemctl status i2p.service

# Common error: "Failed at step APPARMOR spawning"
# Solution: Reconfigure without AppArmor
sudo dpkg-reconfigure -plow i2p
# Select "No" for AppArmor when prompted

# Alternative: Set profile to complain mode
sudo aa-complain /usr/sbin/wrapper

# Check logs for specific errors  
sudo journalctl -xe -u i2p.service
```
**Problemas de permisos** en I2P instalado mediante paquetes:

```bash
# Fix ownership (package install uses 'i2psvc' user)
sudo chown -R i2psvc:i2psvc /var/lib/i2p /var/log/i2p /run/i2p
sudo chmod 750 /var/log/i2p /var/lib/i2p

# Set file descriptor limits (add to /etc/security/limits.conf)
i2psvc soft nofile 4096  
i2psvc hard nofile 8192
```
**Problemas de compatibilidad con Java:**

I2P 2.10.0 requiere **Java 8 como mínimo**. Los sistemas más antiguos pueden tener Java 7 o anterior:

```bash
# Check Java version
java -version

# Install appropriate Java (Debian/Ubuntu)
sudo apt install openjdk-11-jre-headless

# Set default Java if multiple versions installed
sudo update-alternatives --config java
```
**Errores de configuración del Wrapper (programa gestor de servicios de Java)** impiden el inicio del servicio:

La ubicación de Wrapper.config varía según el método de instalación: - Instalación de usuario: `~/.i2p/wrapper.config` - Instalación desde paquete: `/etc/i2p/wrapper.config` o `/var/lib/i2p/wrapper.config`

Problemas comunes de wrapper.config:

- Rutas incorrectas: `wrapper.java.command` debe apuntar a una instalación válida de Java
- Memoria insuficiente: `wrapper.java.maxmemory` configurado demasiado bajo (aumentar a 512 o más)
- Ubicación del archivo PID incorrecta: `wrapper.pidfile` debe ser una ubicación con permisos de escritura
- Falta el binario del wrapper (envoltorio): Algunas plataformas carecen de un wrapper precompilado (usa runplain.sh como alternativa)

**Errores de actualización y actualizaciones corruptas:**

Las actualizaciones de la consola del router ocasionalmente fallan a mitad de la descarga debido a interrupciones de red. Procedimiento de actualización manual:

1. Descarga i2pupdate_X.X.X.zip desde https://geti2p.net/en/download
2. Verifica que la suma de verificación SHA256 coincida con el hash publicado
3. Copia al directorio de instalación de I2P como `i2pupdate.zip`
4. Reinicia el router - detecta y extrae la actualización automáticamente
5. Espera 5-10 minutos para la instalación de la actualización
6. Verifica la nueva versión en http://127.0.0.1:7657

**La migración desde versiones muy antiguas** (pre-0.9.47) a las versiones actuales puede fallar debido a claves de firma incompatibles o funciones eliminadas. Se requieren actualizaciones incrementales:

- Versiones anteriores a 0.9.9: No pueden verificar las firmas actuales - se necesita una actualización manual
- Versiones con Java 6/7: Se debe actualizar Java antes de actualizar I2P a 2.x
- Grandes saltos de versión: Actualice primero a una versión intermedia (0.9.47 recomendado como punto intermedio)

**Cuándo usar el instalador vs el paquete:**

- **Paquetes (apt/yum):** Lo mejor para servidores, actualizaciones de seguridad automáticas, integración con el sistema, gestión con systemd
- **Instalador (.jar):** Lo mejor para instalación a nivel de usuario, Windows, macOS, instalaciones personalizadas, disponibilidad de la última versión

## Corrupción y recuperación de archivos de configuración

La persistencia de la configuración de I2P depende de varios archivos críticos. La corrupción normalmente se debe a **apagado incorrecto**, **errores de disco** o **errores de edición manual**. Comprender la finalidad de los archivos permite una reparación quirúrgica en lugar de una reinstalación completa.

**Archivos críticos y sus propósitos:**

- **router.keys** (516+ bytes): Identidad criptográfica del router - perderlo crea una identidad nueva
- **router.info** (autogenerado): Información publicada del router - se puede borrar con seguridad, se regenera  
- **router.config** (texto): Configuración principal - ancho de banda, configuración de red, preferencias
- **i2ptunnel.config** (texto): Definiciones de tunnel - tunnels cliente/servidor, claves, destinos
- **netDb/** (directorio): Base de datos de pares - información del router para los participantes de la red
- **peerProfiles/** (directorio): Estadísticas de rendimiento sobre los pares - influye en la selección de tunnels
- **keyData/** (directorio): Claves de destino para eepsites y servicios - perderlas cambia las direcciones
- **addressbook/** (directorio): Asignaciones locales de nombres de host .i2p

**Procedimiento de copia de seguridad completo** antes de realizar modificaciones:

```bash
# Stop I2P first
i2prouter stop  # or: systemctl stop i2p

# Backup directory
BACKUP_DIR=~/i2p-backup-$(date +%Y%m%d-%H%M)
mkdir -p $BACKUP_DIR

# Copy critical files
cp -r ~/.i2p/router.keys $BACKUP_DIR/
cp -r ~/.i2p/*.config $BACKUP_DIR/
cp -r ~/.i2p/keyData $BACKUP_DIR/
cp -r ~/.i2p/addressbook $BACKUP_DIR/
cp -r ~/.i2p/eepsite $BACKUP_DIR/  # if hosting sites

# Optional but recommended
tar -czf $BACKUP_DIR.tar.gz $BACKUP_DIR
```
**Síntomas de corrupción de Router.config:**

- El router no arranca; aparecen errores de análisis en los registros
- La configuración no se mantiene tras reiniciar
- Aparecen valores predeterminados inesperados  
- Caracteres ilegibles al ver el archivo

**Reparar router.config dañado:**

1. Hacer copia de seguridad de lo existente: `cp router.config router.config.broken`
2. Comprobar la codificación del archivo: Debe ser UTF-8 sin BOM
3. Validar la sintaxis: Las claves usan el separador `=` (no `:`), sin espacios finales en las claves, `#` solo para comentarios
4. Corrupción común: caracteres no ASCII en los valores, problemas de fin de línea (CRLF vs LF)
5. Si no es reparable: Eliminar router.config - el router genera la configuración predeterminada, preservando la identidad

**Ajustes esenciales de router.config que se deben conservar:**

```properties
i2np.bandwidth.inboundKBytesPerSecond=512
i2np.bandwidth.outboundKBytesPerSecond=256
router.updatePolicy=notify
routerconsole.lang=en
router.hiddenMode=false
```
**router.keys perdido o no válido** crea una nueva identidad del router. Esto es aceptable a menos que:

- Ejecutando floodfill (pierde el estado de floodfill)
- Alojando eepsites con dirección publicada (pierde la continuidad)  
- Reputación establecida en la red

No es posible la recuperación sin copia de seguridad - genere una nueva: elimine router.keys, reinicie I2P, se creará una nueva identidad.

**Distinción crítica:** router.keys (identidad) vs keyData/* (servicios). Perder router.keys cambia la identidad del router. Perder keyData/mysite-keys.dat cambia la dirección .i2p de tu eepsite - catastrófico si la dirección se ha publicado.

**Realiza copias de seguridad de las claves del eepsite/servicio por separado:**

```bash
# Identify your service keys
ls -la ~/.i2p/keyData/

# Backup with descriptive names  
cp ~/.i2p/keyData/myservice-keys.dat ~/backups/myservice-keys-$(date +%Y%m%d).dat

# Store securely (encrypted if sensitive)
gpg -c ~/backups/myservice-keys-*.dat
```
**Corrupción de NetDb y peerProfiles (perfiles de pares):**

Síntomas: cero pares activos, no se pueden construir tunnels, "Se detectó corrupción de la base de datos" en los registros

Solución segura (todo se resembrará/reconstruirá automáticamente):

```bash
i2prouter stop
rm -rf ~/.i2p/netDb/*
rm -rf ~/.i2p/peerProfiles/*
i2prouter start
# Wait 10-15 minutes for reseed and integration
```
Estos directorios contienen solo información de red en caché - al eliminarlos se fuerza un arranque inicial desde cero, pero no se pierde ningún dato crítico.

**Estrategias de prevención:**

1. **Apagado limpio siempre:** Usa `i2prouter stop` o el botón "Shutdown" de la consola del router - nunca mates el proceso a la fuerza
2. **Copias de seguridad automatizadas:** Tarea cron semanal de copia de ~/.i2p a un disco separado
3. **Supervisión de la salud del disco:** Verifica el estado SMART periódicamente - los discos con fallos corrompen datos
4. **Espacio en disco suficiente:** Mantén más de 1 GB libre - los discos llenos provocan corrupción de datos
5. **UPS (sistema de alimentación ininterrumpida) recomendado:** Los cortes de energía durante las escrituras corrompen archivos
6. **Control de versiones de configuraciones críticas:** Un repositorio Git para router.config, i2ptunnel.config permite revertir cambios

**Los permisos de archivo importan:**

```bash
# Correct permissions (user install)
chmod 600 ~/.i2p/router.keys
chmod 600 ~/.i2p/*.config  
chmod 700 ~/.i2p/keyData
chmod 755 ~/.i2p

# Never run as root - creates permission problems
```
## Mensajes de error comunes explicados

El sistema de registro de I2P proporciona mensajes de error específicos que identifican con precisión los problemas. Comprender estos mensajes acelera la resolución de problemas.

**"No tunnels available"** aparece cuando el router no ha construido suficientes tunnels para funcionar. Esto es **normal durante los primeros 5-10 minutos** tras el arranque. Si persiste más de 15 minutos:

1. Verifica que los pares activos sean > 10 en http://127.0.0.1:7657
2. Comprueba que la asignación de ancho de banda sea adecuada (mínimo 128+ KB/s)
3. Examina la tasa de éxito de los tunnel (túnel de I2P) en http://127.0.0.1:7657/tunnels (debería ser >40%)
4. Revisa los registros para conocer los motivos de rechazo en la construcción de tunnel

**"Clock skew detected"** o **"NTCP2 disconnect code 7"** indican que la hora del sistema difiere del consenso de la red en más de 90 segundos. I2P requiere **precisión de ±60 segundos**. Las conexiones con routers con el reloj desfasado se rechazan automáticamente.

Corregir inmediatamente:

```bash
# Linux  
sudo timedatectl set-ntp true
sudo systemctl restart systemd-timesyncd
date  # Verify correct time

# Windows
# Control Panel → Date and Time → Internet Time → Update now

# Verify after sync
http://127.0.0.1:7657/logs  # Should no longer show clock skew warnings
```
**"Build timeout"** o **"Tunnel build timeout exceeded"** significa que la construcción del tunnel a través de la cadena de pares no se completó dentro de la ventana de tiempo de espera (normalmente 60 segundos). Causas:

- **Pares lentos:** Router seleccionó participantes que no responden para el tunnel
- **Congestión de la red:** La red I2P está experimentando una carga alta
- **Ancho de banda insuficiente:** Tus límites de ancho de banda impiden el establecimiento oportuno de tunnels
- **Router sobrecargado:** Demasiados tunnels participantes consumen recursos

Soluciones: Aumentar el ancho de banda, reducir los tunnels participantes (`router.maxParticipatingTunnels` en http://127.0.0.1:7657/configadvanced), habilitar el reenvío de puertos para una mejor selección de pares.

Aparecen **"Router is shutting down"** o **"Graceful shutdown in progress"** durante un apagado normal o la recuperación tras un fallo. El apagado ordenado puede tardar **hasta 10 minutos**, ya que el router cierra tunnels, notifica a los pares y guarda el estado.

Si queda atascado en el estado de apagado durante más de 11 minutos, fuerce la terminación:

```bash
# Linux  
kill -9 $(pgrep -f i2p)

# Windows
taskkill /F /IM javaw.exe
```
**"java.lang.OutOfMemoryError: Java heap space"** indica agotamiento de la memoria heap. Soluciones inmediatas:

1. Edite wrapper.config: `wrapper.java.maxmemory=512` (o superior)
2. **Se requiere un apagado completo** - un reinicio no aplicará el cambio
3. Espere 11 minutos para el apagado completo  
4. Inicie el router desde cero
5. Verifique la asignación de memoria en http://127.0.0.1:7657/graphs - debería mostrar margen libre

**Errores de memoria relacionados:**

- **"GC overhead limit exceeded":** Se está dedicando demasiado tiempo a la recolección de basura - aumente el heap (memoria heap de la JVM)
- **"Metaspace":** Espacio de metadatos de clases de Java agotado - añada `wrapper.java.additional.X=-XX:MaxMetaspaceSize=256M`

**Específico de Windows:** Kaspersky Antivirus limita el heap de Java a 512 MB independientemente de la configuración de wrapper.config - desinstálalo o añade I2P a las exclusiones.

**"Tiempo de espera de la conexión agotado"** o **"Error de I2CP - puerto 7654"** cuando las aplicaciones intentan conectarse al router:

1. Verifique que el router esté en ejecución: http://127.0.0.1:7657 debería responder
2. Verifique el puerto I2CP: `netstat -an | grep 7654` debería mostrar LISTENING
3. Asegúrese de que el cortafuegos de localhost permita: `sudo ufw allow from 127.0.0.1`  
4. Verifique que la aplicación esté usando el puerto correcto (I2CP=7654, SAM=7656)

**"Certificate validation failed"** o **"RouterInfo corrupt"** durante el reseed (proceso de resembrado inicial de la red):

Causas raíz: desfase del reloj (corrige esto primero), netDb corrupta, certificados de reseed (arranque inicial de la red) inválidos

```bash
# After fixing clock:
i2prouter stop
rm -rf ~/.i2p/netDb/*  # Delete corrupted database
i2prouter start  # Auto-reseeds with fresh data
```
**"Se detectó corrupción de base de datos"** indica corrupción de datos a nivel de disco en netDb o peerProfiles (perfiles de pares):

```bash
# Safe fix - all will rebuild
i2prouter stop  
rm -rf ~/.i2p/netDb/* ~/.i2p/peerProfiles/*
i2prouter start
```
Comprueba la salud del disco con herramientas SMART - la corrupción recurrente sugiere que el almacenamiento está fallando.

## Desafíos específicos de la plataforma

Los distintos sistemas operativos plantean desafíos únicos para el despliegue de I2P relacionados con los permisos, las políticas de seguridad y la integración con el sistema.

### Problemas de permisos y servicios en Linux

I2P instalado como paquete se ejecuta como el usuario del sistema **i2psvc** (Debian/Ubuntu) o **i2p** (otras distribuciones), lo que requiere permisos específicos:

```bash
# Fix package install permissions  
sudo chown -R i2psvc:i2psvc /var/lib/i2p /var/log/i2p /run/i2p
sudo chmod 750 /var/log/i2p /var/lib/i2p
sudo chmod 644 /var/lib/i2p/*.config

# User install permissions (should be your user)
chown -R $USER:$USER ~/.i2p
chmod 700 ~/.i2p
chmod 600 ~/.i2p/router.keys ~/.i2p/*.config
```
**Límites de descriptores de archivo** afectan la capacidad del router para las conexiones. Los límites predeterminados (1024) son insuficientes para routers de alto ancho de banda:

```bash
# Check current limits
ulimit -n

# Temporary increase  
ulimit -n 4096

# Permanent fix: Edit /etc/security/limits.conf
i2psvc soft nofile 4096
i2psvc hard nofile 8192

# Systemd override
sudo mkdir -p /etc/systemd/system/i2p.service.d/
sudo nano /etc/systemd/system/i2p.service.d/override.conf

# Add:
[Service]
LimitNOFILE=8192

sudo systemctl daemon-reload
sudo systemctl restart i2p
```
**Conflictos de AppArmor** comunes en Debian/Ubuntu impiden el inicio del servicio:

```bash
# Error: "Failed at step APPARMOR spawning /usr/sbin/wrapper"
# Cause: AppArmor profile missing or misconfigured

# Solution 1: Disable AppArmor for I2P
sudo aa-complain /usr/sbin/wrapper

# Solution 2: Reconfigure package without AppArmor
sudo dpkg-reconfigure -plow i2p  
# Select "No" when asked about AppArmor

# Solution 3: LXC/Proxmox containers - disable AppArmor in container config
lxc.apparmor.profile: unconfined
```
**Problemas de SELinux** en RHEL/CentOS/Fedora:

```bash
# Temporary: Set permissive mode
sudo setenforce 0

# Permanent: Generate custom policy
sudo ausearch -c 'java' --raw | audit2allow -M i2p_policy
sudo semodule -i i2p_policy.pp

# Or disable SELinux for I2P process (less secure)
sudo semanage permissive -a i2p_t
```
**Solución de problemas del servicio SystemD:**

```bash
# Detailed service status
sudo systemctl status i2p.service -l

# Full logs  
sudo journalctl -xe -u i2p.service

# Follow logs live
sudo journalctl -f -u i2p.service

# Restart with logging
sudo systemctl restart i2p.service && sudo journalctl -f -u i2p.service
```
### Interferencia del cortafuegos de Windows y del antivirus

Windows Defender y los productos antivirus de terceros con frecuencia marcan I2P debido a patrones de comportamiento de red. Una configuración adecuada evita bloqueos innecesarios manteniendo la seguridad.

**Configurar el Firewall de Windows Defender:**

```powershell
# Run PowerShell as Administrator

# Find Java path (adjust for your Java installation)
$javaPath = "C:\Program Files\Eclipse Adoptium\jdk-11.0.16.101-hotspot\bin\javaw.exe"

# Create inbound rules
New-NetFirewallRule -DisplayName "I2P Java" -Direction Inbound -Program $javaPath -Action Allow
New-NetFirewallRule -DisplayName "I2P UDP" -Direction Inbound -Protocol UDP -LocalPort 22648 -Action Allow  
New-NetFirewallRule -DisplayName "I2P TCP" -Direction Inbound -Protocol TCP -LocalPort 22648 -Action Allow

# Add exclusions to Windows Defender
Add-MpPreference -ExclusionPath "C:\Program Files\i2p"
Add-MpPreference -ExclusionPath "$env:APPDATA\I2P"
Add-MpPreference -ExclusionPath "$env:LOCALAPPDATA\I2P"
Add-MpPreference -ExclusionProcess "javaw.exe"
```
Reemplaza el puerto 22648 por tu puerto real de I2P que aparece en http://127.0.0.1:7657/confignet.

**Problema específico de Kaspersky Antivirus:** "Application Control" de Kaspersky limita el heap de Java a 512MB independientemente de la configuración de wrapper.config. Esto provoca OutOfMemoryError (error por falta de memoria) en routers de alto ancho de banda.

Soluciones: 1. Añade I2P a las exclusiones de Kaspersky: Settings → Additional → Threats and Exclusions → Manage Exclusions 2. O desinstala Kaspersky (recomendado para el funcionamiento de I2P)

**Orientación general sobre antivirus de terceros:**

- Añade el directorio de instalación de I2P a las exclusiones  
- Añade %APPDATA%\I2P y %LOCALAPPDATA%\I2P a las exclusiones
- Excluye javaw.exe del análisis de comportamiento
- Desactiva las funciones de "Network Attack Protection" (protección contra ataques de red) que puedan interferir con los protocolos de I2P

### Gatekeeper de macOS bloquea la instalación

Gatekeeper (función de seguridad de macOS) impide la ejecución de aplicaciones no firmadas. Los instaladores de I2P no están firmados con el ID de Desarrollador de Apple, lo que provoca advertencias de seguridad.

**Omitir Gatekeeper (función de seguridad de macOS) para el instalador de I2P:**

```bash
# Method 1: Remove quarantine attribute
xattr -d com.apple.quarantine ~/Downloads/i2pinstall_*.jar
java -jar ~/Downloads/i2pinstall_*.jar

# Method 2: Use System Settings (macOS 13+)
# Try to open installer → macOS blocks it
# System Settings → Privacy & Security → scroll down
# Click "Open Anyway" next to I2P warning
# Confirm in dialog

# Method 3: Control-click installer
# Control-click (right-click) i2pinstall_*.jar
# Select "Open" from menu → "Open" again in dialog
# Bypasses Gatekeeper for this specific file
```
**Después de la instalación, la ejecución** todavía puede generar advertencias:

```bash
# If I2P won't start due to Gatekeeper:
xattr -dr com.apple.quarantine ~/i2p/
```
**Nunca desactives permanentemente Gatekeeper** - riesgo de seguridad para otras aplicaciones. Usa solo excepciones específicas por archivo.

**Configuración del cortafuegos de macOS:**

1. Preferencias del Sistema → Seguridad y privacidad → Firewall → Opciones del Firewall
2. Haz clic en "+" para añadir la aplicación  
3. Navega a la instalación de Java (p. ej., `/Library/Java/JavaVirtualMachines/jdk-11.jdk/Contents/Home/bin/java`)
4. Añádela y configúrala en "Permitir conexiones entrantes"

### Problemas con la aplicación I2P para Android

Las restricciones de versión de Android y las limitaciones de recursos crean desafíos únicos.

**Requisitos mínimos:** - Android 5.0+ (nivel de API 21+) requerido para las versiones actuales - 512MB de RAM mínimo, 1GB+ recomendado   - 100MB de almacenamiento para la aplicación + datos del router - Restricciones de aplicaciones en segundo plano desactivadas para I2P

**La aplicación se cierra inmediatamente:**

1. **Comprueba la versión de Android:** Ajustes → Acerca del teléfono → Versión de Android (debe ser 5.0 o superior)
2. **Desinstala todas las versiones de I2P:** Instala solo una variante:
   - net.i2p.android (Google Play)
   - net.i2p.android.router (F-Droid)  
   Múltiples instalaciones entran en conflicto
3. **Borra los datos de la app:** Ajustes → Aplicaciones → I2P → Almacenamiento → Borrar datos
4. **Vuelve a instalar desde cero**

**La optimización de la batería está forzando el cierre del router:**

Android cierra agresivamente las aplicaciones en segundo plano para ahorrar batería. I2P debe excluirse:

1. Ajustes → Batería → Optimización de batería (o Uso de batería de la aplicación)
2. Busca I2P → No optimizar (o Permitir actividad en segundo plano)
3. Ajustes → Aplicaciones → I2P → Batería → Permitir actividad en segundo plano + Eliminar restricciones

**Problemas de conexión en móviles:**

- **El bootstrap (proceso de arranque) requiere WiFi:** La reseed inicial (descarga de listas de pares) consume una cantidad significativa de datos - usa WiFi, no datos móviles
- **Cambios de red:** I2P no maneja bien los cambios de red - reinicia la aplicación después de una transición entre WiFi y datos móviles
- **Ancho de banda para móviles:** Configura de forma conservadora a 64-128 KB/sec para evitar agotar los datos móviles

**Optimización del rendimiento para móviles:**

1. App de I2P → Menú → Ajustes → Ancho de banda
2. Establece límites adecuados: 64 KB/sec entrante, 32 KB/sec saliente para datos móviles
3. Reduce los tunnels participantes: Ajustes → Avanzado → Máximo de tunnels participantes: 100-200
4. Activa "Detener I2P cuando la pantalla esté apagada" para ahorrar batería

**Uso de torrents en Android:**

- Limitar a 2-3 torrents simultáneos como máximo
- Reducir la agresividad de la DHT (tabla hash distribuida)  
- Usar solo WiFi para torrents
- Aceptar velocidades más lentas en hardware móvil

## Problemas de Reseed (resembrado inicial) y de bootstrap (arranque)

Las instalaciones nuevas de I2P requieren **reseeding** (descarga inicial de información de pares) - obtener información inicial de pares desde servidores HTTPS públicos para unirse a la red. Los problemas de reseeding dejan a los usuarios con cero pares y sin acceso a la red.

**"No active peers" después de una instalación reciente** normalmente indica un fallo en el reseed (proceso inicial de obtención de pares). Síntomas:

- Pares conocidos: 0 o permanece por debajo de 5
- "Network: Testing" persiste durante más de 15 minutos
- Los registros muestran "Reseed failed" o errores de conexión con los servidores de reseed (obtención inicial de pares)

**Por qué falla el reseed (proceso de obtención inicial de pares):**

1. **Cortafuegos que bloquea HTTPS:** Los cortafuegos corporativos/ISP bloquean conexiones con servidores reseed (servidores de arranque para obtener pares iniciales en I2P) (puerto 443)
2. **Errores de certificado SSL:** El sistema carece de certificados raíz actualizados
3. **Requisito de proxy:** La red requiere un proxy HTTP/SOCKS para conexiones externas
4. **Desfase del reloj:** La validación de certificados SSL falla cuando la hora del sistema es incorrecta
5. **Censura geográfica:** Algunos países/ISP bloquean servidores reseed conocidos

**Forzar reseed manual (resembrado inicial de pares):**

1. Accede a http://127.0.0.1:7657/configreseed
2. Haz clic en "Save changes and reseed now"  
3. Supervisa http://127.0.0.1:7657/logs en busca de "Reseed got XX router infos"
4. Espera de 5 a 10 minutos para el procesamiento
5. Comprueba http://127.0.0.1:7657 - Los pares conocidos deberían aumentar a 50+

**Configurar proxy de reseed (proceso de arranque para obtener nodos iniciales de la red)** para redes restrictivas:

http://127.0.0.1:7657/configreseed → Configuración del proxy:

- Proxy HTTP: [proxy-server]:[port]
- O SOCKS5: [socks-server]:[port]  
- Activa "Use proxy for reseed only"
- Credenciales si es necesario
- Guarda y fuerza el reseed (proceso de arranque de la red)

**Alternativa: proxy de Tor para el reseed (proceso inicial para obtener pares y poner en marcha I2P):**

Si Tor Browser o el demonio de Tor están en ejecución:

- Tipo de proxy: SOCKS5
- Host: 127.0.0.1
- Puerto: 9050 (puerto SOCKS predeterminado de Tor)
- Habilitar y resembrar

**Reseed (obtención inicial de pares) manual mediante archivo su3** (último recurso):

Cuando falle todo el reseed (proceso de incorporación inicial a la red) automatizado, obtenga el archivo de reseed por un canal fuera de banda:

1. Descarga i2pseeds.su3 desde una fuente de confianza con una conexión sin restricciones (https://reseed.i2p.rocks/i2pseeds.su3, https://reseed-fr.i2pd.xyz/i2pseeds.su3)
2. Detén I2P por completo
3. Copia i2pseeds.su3 al directorio ~/.i2p/  
4. Inicia I2P - extrae y procesa el archivo automáticamente
5. Elimina i2pseeds.su3 después del procesamiento
6. Verifica que los pares aumenten en http://127.0.0.1:7657

**Errores de certificados SSL durante el reseed (proceso de obtención inicial de pares):**

```
Error: "Reseed: Certificate verification failed"  
Cause: System root certificates outdated or missing
```
Soluciones:

```bash
# Linux - update certificates
sudo apt install ca-certificates
sudo update-ca-certificates

# Windows - install KB updates for root certificate trust
# Or install .NET Framework (includes certificate updates)

# macOS - update system
# Software Update includes certificate trust updates
```
**Atascado en 0 pares conocidos durante más de 30 minutos:**

Indica un fallo completo del reseed (arranque inicial de la red obteniendo nodos iniciales desde servidores de reseed). Secuencia de resolución de problemas:

1. **Verifica que la hora del sistema sea precisa** (problema más común - corrígelo PRIMERO)
2. **Prueba la conectividad HTTPS:** Intenta acceder a https://reseed.i2p.rocks en el navegador - si falla, es un problema de red
3. **Revisa los registros de I2P** en http://127.0.0.1:7657/logs para errores específicos de reseed (proceso de arranque inicial de la red)
4. **Prueba una URL de reseed diferente:** http://127.0.0.1:7657/configreseed → añade una URL de reseed personalizada: https://reseed-fr.i2pd.xyz/
5. **Usa el método manual con archivo su3** si se han agotado los intentos automáticos

**Servidores de reseed (servidores usados para obtener los pares iniciales de la red) ocasionalmente fuera de línea:** I2P incluye múltiples servidores de reseed predefinidos. Si uno falla, el router prueba otros automáticamente. Un fallo total de todos los servidores de reseed es extremadamente raro, pero posible.

**Servidores reseed (arranque inicial de la red) actualmente activos** (a octubre de 2025):

- https://reseed.i2p.rocks/
- https://reseed-fr.i2pd.xyz/
- https://i2p.novg.net/
- https://i2p-projekt.de/

Añádelas como URL personalizadas si tienes problemas con las predeterminadas.

**Para usuarios en regiones con fuerte censura:**

Considera usar puentes Snowflake/Meek a través de Tor para el reseed (arranque inicial de la red), y luego cambiar a una conexión directa a I2P una vez integrado a la red. O bien, obtén i2pseeds.su3 mediante esteganografía, correo electrónico o USB desde fuera de la zona de censura.

## Cuándo buscar ayuda adicional

Esta guía aborda la gran mayoría de los problemas de I2P, pero algunos requieren la atención de los desarrolladores o la experiencia de la comunidad.

**Busca ayuda de la comunidad de I2P cuando:**

- Router se bloquea de forma constante después de seguir todos los pasos de resolución de problemas
- Fugas de memoria que provocan un crecimiento constante que supera el heap asignado
- La tasa de éxito de Tunnel se mantiene por debajo del 20% a pesar de una configuración adecuada  
- Nuevos errores en los registros no cubiertos por esta guía
- Vulnerabilidades de seguridad descubiertas
- Solicitudes de funcionalidades o sugerencias de mejora

**Antes de solicitar ayuda, recopile información de diagnóstico:**

1. Versión de I2P: http://127.0.0.1:7657 (p. ej., "2.10.0")
2. Versión de Java: salida de `java -version`
3. Sistema operativo y versión
4. Estado del router: Estado de la red, Número de pares activos, Tunnels participantes
5. Configuración de ancho de banda: Límites de entrada/salida
6. Estado del reenvío de puertos: Con cortafuegos o OK
7. Extractos relevantes de los registros: Últimas 50 líneas que muestren errores desde http://127.0.0.1:7657/logs

**Canales de soporte oficiales:**

- **Foro:** https://i2pforum.net (clearnet) o http://i2pforum.i2p (dentro de I2P)
- **IRC:** #i2p en Irc2P (irc.postman.i2p vía I2P) o irc.freenode.net (clearnet)
- **Reddit:** https://reddit.com/r/i2p para discusiones de la comunidad
- **Rastreador de errores:** https://i2pgit.org/i2p-hackers/i2p.i2p/-/issues para errores confirmados
- **Lista de correo:** i2p-dev@lists.i2p-projekt.de para consultas de desarrollo

**Las expectativas realistas importan.** I2P es más lento que clearnet (Internet abierta) por su diseño fundamental - el uso de tunnels cifrados de múltiples saltos crea latencia inherente. Un router de I2P que carga páginas en 30 segundos y alcanza velocidades de torrent de 50 KB/sec está **funcionando correctamente**, no está averiado. Los usuarios que esperen velocidades de clearnet quedarán decepcionados independientemente de la optimización de la configuración.

## Conclusión

La mayoría de los problemas de I2P provienen de tres categorías: paciencia insuficiente durante el bootstrap (fase de arranque), que requiere 10-15 minutos; asignación inadecuada de recursos (512 MB de RAM y 256 KB/sec de ancho de banda como mínimo); o reenvío de puertos mal configurado. Comprender la arquitectura distribuida de I2P y su diseño centrado en el anonimato ayuda a los usuarios a distinguir el comportamiento esperado de los problemas reales.

El estado "Firewalled" del router, aunque subóptimo, no impide el uso de I2P - solo limita la contribución a la red y degrada ligeramente el rendimiento. Los usuarios nuevos deberían priorizar la **estabilidad sobre la optimización**: ejecutar el router de forma continua durante varios días antes de ajustar la configuración avanzada, ya que la integración mejora de manera natural con el tiempo de actividad.

Al solucionar problemas, verifique siempre primero lo fundamental: hora correcta del sistema, ancho de banda adecuado, router en ejecución continua y 10 o más pares activos. La mayoría de los problemas se resuelven atendiendo estos aspectos básicos en lugar de ajustar parámetros de configuración poco claros. I2P recompensa la paciencia y el funcionamiento continuo con un mejor rendimiento a medida que el router construye reputación y optimiza la selección de pares a lo largo de días y semanas de tiempo de actividad.
