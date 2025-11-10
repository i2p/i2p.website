---
title: "Lanzamiento del paquete de instalación fácil para Windows 1.9.0"
date: 2022-08-28
author: "idk"
description: "Paquete de instalación fácil para Windows 1.9.0 - Importantes mejoras de estabilidad/compatibilidad"
categories: ["release"]
---

## Esta actualización incluye el nuevo router 1.9.0 y mejoras significativas de calidad de vida para los usuarios del paquete

Esta versión incluye el nuevo router I2P 1.9.0 y se basa en Java 18.02.1.

Los antiguos scripts por lotes se han dejado de usar en favor de una solución más flexible y estable integrada en el propio jpackage. Esto debería corregir todos los errores relacionados con la resolución de rutas y el entrecomillado de rutas que estaban presentes en los scripts por lotes. Después de actualizar, los scripts por lotes se pueden eliminar de forma segura. El instalador los eliminará en la próxima actualización.

Se ha iniciado un subproyecto para gestionar herramientas de navegación: i2p.plugins.firefox, que tiene amplias capacidades para configurar navegadores I2P de forma automática y estable en muchas plataformas. Esto se utilizó para reemplazar los scripts por lotes, pero también funciona como una herramienta de gestión multiplataforma de I2P Browser. Se agradecen las contribuciones aquí: http://git.idk.i2p/idk/i2p.plugins.firefox en el repositorio de código fuente.

Esta versión mejora la compatibilidad con routers de I2P que se ejecutan externamente, como los proporcionados por el instalador IzPack y por implementaciones de router de terceros como i2pd. Al mejorar el descubrimiento de routers externos, requiere menos recursos del sistema, mejora el tiempo de inicio e impide que se produzcan conflictos de recursos.

Además, el perfil se ha actualizado a la última versión del perfil Arkenfox. I2P in Private Browsing y NoScript se han actualizado. El perfil ha sido reestructurado para permitir evaluar diferentes configuraciones para diferentes modelos de amenazas.
