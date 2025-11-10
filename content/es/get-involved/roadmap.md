---
title: "Hoja de Ruta de Desarrollo de I2P"
description: "Planes de desarrollo actuales y hitos históricos para la red I2P"
---

<div style="background: var(--color-bg-secondary); border-left: 4px solid var(--color-primary); padding: 1.5rem; margin-bottom: 2rem; border-radius: var(--radius-md);">

**I2P sigue un modelo de desarrollo incremental** con lanzamientos aproximadamente cada 13 semanas. Esta hoja de ruta cubre las versiones de Java para escritorio y Android en un solo camino de lanzamiento estable.

**Última Actualización:** Agosto 2025

</div>

## 🎯 Próximos Lanzamientos

<div style="border-left: 3px solid var(--color-accent); padding-left: 1.5rem; margin-bottom: 2rem;">

### Versión 2.11.0
<div style="display: inline-block; background: var(--color-accent); color: white; padding: 0.25rem 0.75rem; border-radius: var(--radius-md); font-size: 0.875rem; margin-bottom: 1rem;">
Objetivo: Principios de diciembre de 2025
</div>

- Hybrid PQ MLKEM Ratchet final, habilitado por defecto (prop. 169)
- Jetty 12, requiere Java 17+
- Continuar trabajo en PQ (transportes) (prop. 169)
- Soporte de búsqueda I2CP para parámetros de registro de servicio LS (prop. 167)
- Regulación por túnel
- Subsistema de estadísticas compatible con Prometheus
- Soporte SAM para Datagram 2/3

</div>

---

## 📦 Lanzamientos Recientes

### Lanzamientos de 2025

<div style="background: var(--color-bg-secondary); padding: 1.5rem; border-radius: var(--radius-md); margin-bottom: 1.5rem; border-left: 4px solid var(--color-success);">

**Versión 2.10.0** <span style="color: var(--color-text-muted); font-size: 0.9rem;">— Lanzado el 8 de septiembre de 2025</span>

- i2psnark soporte de rastreador UDP (prop. 160)
- Parámetros del registro de servicio LS de I2CP (parcial) (prop. 167)
- API de búsqueda asincrónica I2CP
- Hybrid PQ MLKEM Ratchet Beta (prop. 169)
- Continuación del trabajo en PQ (transportes) (prop. 169)
- Parámetros de ancho de banda de construcción de túneles (prop. 168) Parte 2 (manejo)
- Continuación del trabajo en la regulación por túnel
- Eliminar código de transporte ElGamal no utilizado
- Eliminar código de "active throttle" antiguo de SSU2
- Eliminar soporte de registro de estadísticas antiguo
- Limpieza de subsistema de estadísticas/gráficos
- Mejoras y correcciones en modo oculto

</div>

<div style="background: var(--color-bg-secondary); padding: 1.5rem; border-radius: var(--radius-md); margin-bottom: 1.5rem; border-left: 4px solid var(--color-success);">

**Versión 2.9.0** <span style="color: var(--color-text-muted); font-size: 0.9rem;">— Lanzado el 2 de junio de 2025</span>

- Mapa Netdb
- Implementar Datagram2, Datagram3 (prop. 163)
- Iniciar trabajo en el parámetro de registro de servicio LS (prop. 167)
- Iniciar trabajo en PQ (prop. 169)
- Continuar trabajo en la regulación por túnel
- Parámetros de ancho de banda de construcción de túneles (prop. 168) Parte 1 (envío)
- Usar /dev/random para PRNG por defecto en Linux
- Eliminar código de renderizado de LS redundante
- Mostrar registro de cambios en HTML
- Reducir uso de hilos del servidor HTTP
- Corregir auto-floodfill enrollment
- Actualización del envoltorio a 3.5.60

</div>

<div style="background: var(--color-bg-secondary); padding: 1.5rem; border-radius: var(--radius-md); margin-bottom: 1.5rem; border-left: 4px solid var(--color-success);">

**Versión 2.8.2** <span style="color: var(--color-text-muted); font-size: 0.9rem;">— Lanzado el 29 de marzo de 2025</span>

- Corregir error de corrupción SHA256

</div>

<div style="background: var(--color-bg-secondary); padding: 1.5rem; border-radius: var(--radius-md); margin-bottom: 1.5rem; border-left: 4px solid var(--color-success);">

**Versión 2.8.1** <span style="color: var(--color-text-muted); font-size: 0.9rem;">— Lanzado el 17 de marzo de 2025</span>

- Corregir fallo del instalador en Java 21+
- Corregir error de "loopback"
- Corregir pruebas de túneles para túneles de cliente salientes
- Corregir instalación en rutas con espacios
- Actualizar contenedor Docker desactualizado y bibliotecas de contenedores
- Burbujas de notificación de consola
- Ordenar por lo más reciente en SusiDNS
- Usar el grupo SHA256 en Noise
- Correcciones y mejoras en el tema oscuro de la consola
- Soporte .i2p.alt

</div>

<div style="background: var(--color-bg-secondary); padding: 1.5rem; border-radius: var(--radius-md); margin-bottom: 1.5rem; border-left: 4px solid var(--color-success);">

**Versión 2.8.0** <span style="color: var(--color-text-muted); font-size: 0.9rem;">— Lanzado el 3 de febrero de 2025</span>

- Mejoras en la publicación de RouterInfo
- Mejorar la eficiencia de ACK de SSU2
- Mejorar el manejo de mensajes duplicados de relé SSU2
- Tiempos de espera de búsqueda más rápidos/variables
- Mejoras en la expiración de LS
- Cambiar límite NAT simétrico
- Hacer cumplir el POST en más formularios
- Correcciones en el tema oscuro de SusiDNS
- Limpieza de pruebas de ancho de banda
- Nueva traducción al chino Gan
- Añadir opción de interfaz en kurdo
- Nueva compilación Jammy
- Izpack 5.2.3
- rrd4j 3.10

</div>

<div style="margin: 3rem 0; padding: 1rem 0; border-top: 2px solid var(--color-border); border-bottom: 2px solid var(--color-border);">
  <h3 style="margin: 0; color: var(--color-primary);">📅 Lanzamientos de 2024</h3>
</div>

<div style="background: var(--color-bg-secondary); padding: 1.5rem; border-radius: var(--radius-md); margin-bottom: 1.5rem; border-left: 4px solid var(--color-primary);">

**Versión 2.7.0** <span style="color: var(--color-text-muted); font-size: 0.9rem;">— 8 de octubre de 2024</span>

- i2ptunnel servidor HTTP reduce el uso de hilos
- Túneles UDP Genéricos en I2PTunnel
- Proxy de navegador en I2PTunnel
- Migración de sitio web
- Corrección para túneles que se vuelven amarillos
- Refactorización de la consola /netdb

</div>

<div style="background: var(--color-bg-secondary); padding: 1.5rem; border-radius: var(--radius-md); margin-bottom: 1.5rem; border-left: 4px solid var(--color-primary);">

**Versión 2.6.1** <span style="color: var(--color-text-muted); font-size: 0.9rem;">— 6 de agosto de 2024</span>

- Corregir problemas de tamaño de iframe en la consola
- Convertir gráficos a SVG
- Informe de estado de traducción en paquete

</div>

<div style="background: var(--color-bg-secondary); padding: 1.5rem; border-radius: var(--radius-md); margin-bottom: 1.5rem; border-left: 4px solid var(--color-primary);">

**Versión 2.6.0** <span style="color: var(--color-text-muted); font-size: 0.9rem;">— 19 de julio de 2024</span>

- Reducir uso de memoria netdb
- Eliminar código SSU1
- Corregir filtraciones y bloqueos de archivos temporales de i2psnark
- PEX más eficiente en i2psnark
- Actualización JS de gráficos de consola
- Mejoras en el renderizado de gráficos
- Búsqueda JS en susimail
- Manejo de mensajes más eficiente en OBEP
- Búsquedas I2CP de destino local más eficientes
- Corregir problemas de alcance de variables JS

</div>

<div style="background: var(--color-bg-secondary); padding: 1.5rem; border-radius: var(--radius-md); margin-bottom: 1.5rem; border-left: 4px solid var(--color-primary);">

**Versión 2.5.2** <span style="color: var(--color-text-muted); font-size: 0.9rem;">— 15 de mayo de 2024</span>

- Corregir truncamiento HTTP
- Publicar capacidad G si se detecta NAT simétrico
- Actualización a rrd4j 3.9.1-preview

</div>

<div style="background: var(--color-bg-secondary); padding: 1.5rem; border-radius: var(--radius-md); margin-bottom: 1.5rem; border-left: 4px solid var(--color-primary);">

**Versión 2.5.1** <span style="color: var(--color-text-muted); font-size: 0.9rem;">— 6 de mayo de 2024</span>

- Mitigaciones DDoS NetDB
- Lista de bloqueo Tor
- Correcciones y búsqueda de Susimail
- Continuar eliminando código SSU1
- Actualización a Tomcat 9.0.88

</div>

<div style="background: var(--color-bg-secondary); padding: 1.5rem; border-radius: var(--radius-md); margin-bottom: 1.5rem; border-left: 4px solid var(--color-primary);">

**Versión 2.5.0** <span style="color: var(--color-text-muted); font-size: 0.9rem;">— 8 de abril de 2024</span>

- Mejoras en iframes de consola
- Rediseño del limitador de ancho de banda i2psnark
- Javascript de arrastrar y soltar para i2psnark y susimail
- Mejoras en el manejo de errores SSL de i2ptunnel
- Soporte de conexión HTTP persistente en i2ptunnel
- Comenzar a eliminar código SSU1
- Mejoras en el manejo de solicitudes de etiqueta de relé en SSU2
- Correcciones de prueba de pares SSU2
- Mejoras en Susimail (carga, markdown, soporte de correo HTML)
- Ajustes en la selección de pares de túnel
- Actualización a RRD4J 3.9
- Actualización de gradlew a 8.5

</div>

<div style="background: var(--color-bg-secondary); padding: 1.5rem; border-radius: var(--radius-md); margin-bottom: 1.5rem; border-left: 4px solid var(--color-primary);">

**Versión 2.4.0** <span style="color: var(--color-text-muted); font-size: 0.9rem;">— 18 de diciembre de 2023</span>

- Gestión de contexto NetDB/NetDB segmentado
- Manejar capacidades de congestión depriorizando enrutadores sobrecargados
- Revivir biblioteca auxiliar de Android
- Selector de archivos torrent locales en i2psnark
- Correcciones en el manejador de búsqueda NetDB
- Deshabilitar SSU1
- Prohibir enrutadores publicando en el futuro
- Correcciones SAM
- Correcciones Susimail
- Correcciones UPnP

</div>

---

### Lanzamientos de 2023-2022

<details>
<summary>Haga clic para expandir lanzamientos de 2023-2022</summary>

**Versión 2.3.0** — Lanzado el 28 de junio de 2023

- Mejoras en la selección de pares de túnel
- Expiración configurada por el usuario de la lista de bloqueo
- Limitar ráfagas rápidas de búsqueda desde la misma fuente
- Corregir fuga de información de detección de repetición
- Correcciones NetDB para multihome leaseSets
- Correcciones NetDB para leaseSets recibidos como respuesta antes de ser recibidos como tienda

**Versión 2.2.1** — Lanzado el 12 de abril de 2023

- Correcciones de empaquetado

**Versión 2.2.0** — Lanzado el 13 de marzo de 2023

- Mejoras en la selección de pares de túnel
- Corrección en la repetición de streaming

**Versión 2.1.0** — Lanzado el 10 de enero de 2023

- Correcciones SSU2
- Correcciones de congestión en la construcción de túneles
- Correcciones en la prueba de pares SSU y detección NAT simétrica
- Corregir leaseSets cifrados LS2 rotos
- Opción para deshabilitar SSU 1 (preliminar)
- Acolchado comprimible (propuesta 161)
- Nueva pestaña de estado de pares en la consola
- Añadir soporte de torsocks al proxy SOCKS y otras mejoras y correcciones de SOCKS

**Versión 2.0.0** — Lanzado el 21 de noviembre de 2022

- Migración de conexión SSU2
- Reconocimientos inmediatos SSU2
- Habilitar SSU2 por defecto
- Autenticación proxy SHA-256 digest en i2ptunnel
- Actualizar proceso de construcción de Android para usar AGP moderno
- Soporte de autoconfiguración del navegador I2P multiplataforma (escritorio)

**Versión 1.9.0** — Lanzado el 22 de agosto de 2022

- Implementación de prueba de ventilación y relé SSU2
- Correcciones SSU2
- Mejoras SSU MTU/PMTU
- Habilitar SSU2 para una pequeña porción de enrutadores
- Añadir detector de interbloqueos
- Más correcciones en la importación de certificados
- Corregir reinicio de DHT en i2psnark tras reinicio de enrutador

**Versión 1.8.0** — Lanzado el 23 de mayo de 2022

- Correcciones y mejoras de la familia de enrutadores
- Correcciones de reinicio suave
- Correcciones y mejoras de rendimiento SSU
- Correcciones y mejoras independientes de I2PSnark
- Evitar penalización Sybil para familias de confianza
- Reducir tiempo de espera de respuesta en la construcción de túneles
- Correcciones UPnP
- Eliminar fuente BOB
- Correcciones en la importación de certificados
- Tomcat 9.0.62
- Refactorización para soportar SSU2 (propuesta 159)
- Implementación inicial del protocolo base SSU2 (propuesta 159)
- Popup de autorización SAM para aplicaciones de Android
- Mejorar soporte para instalaciones de directorios personalizados en i2p.firefox

**Versión 1.7.0** — Lanzado el 21 de febrero de 2022

- Eliminar BOB
- Nuevo editor de torrents i2psnark
- Correcciones y mejoras independientes de i2psnark
- Mejoras en la fiabilidad NetDB
- Añadir mensajes emergentes en la bandeja del sistema
- Mejoras de rendimiento NTCP2
- Eliminar túnel saliente cuando falla el primer salto
- Retroceso a exploratorio para respuesta de construcción de túnel tras fallos repetidos en túneles de cliente
- Restaurar restricciones de misma IP para túneles
- Refactorizar soporte UDP en i2ptunnel para puertos I2CP
- Continuar trabajo en SSU2, iniciar la implementación (propuesta 159)
- Crear paquete Debian/Ubuntu del perfil del navegador I2P
- Crear plugin del perfil del navegador I2P
- Documentación de I2P para aplicaciones de Android
- Mejoras en i2pcontrol
- Mejoras en soporte de plugins
- Nuevo plugin outproxy local
- Soporte de etiquetas de mensaje IRCv3

</details>

---

### Lanzamientos de 2021

<details>
<summary>Haga clic para expandir lanzamientos de 2021</summary>

**Versión 1.6.1** — Lanzado el 29 de noviembre de 2021

- Acelerar el cambio de claves de enrutadores a ECIES
- Mejoras de rendimiento SSU
- Mejorar la seguridad de la prueba de pares SSU
- Añadir selección de tema al asistente de nueva instalación
- Continuar trabajo en SSU2 (propuesta 159)
- Enviar nuevos mensajes de construcción de túneles (propuesta 157)
- Incluir herramienta de configuración automática del navegador en el instalador IzPack
- Hacer plugins de Fork-and-Exec manejables
- Documentar procesos de instalación de jpackage
- Completar, documentar herramientas de generación de plugins Go/Java
- Plugin de remanente para HTTPS
