---
title: "Guía de Traducción"
description: "Ayuda a que I2P sea accesible para usuarios en todo el mundo traduciendo la consola del router y el sitio web"
date: 2025-01-15
layout: "single"
type: "docs"
---

## Visión General

Ayuda a que I2P sea accesible para usuarios en todo el mundo traduciendo la consola del router de I2P y el sitio web a tu idioma. La traducción es un proceso continuo, y las contribuciones de cualquier tamaño son valiosas.

## Plataforma de Traducción

Usamos **Transifex** para todas las traducciones de I2P. Este es el método más fácil y recomendado tanto para traductores nuevos como experimentados.

### Comenzando con Transifex

1. **Crea una cuenta** en [Transifex](https://www.transifex.com/)
2. **Únete al proyecto I2P**: [I2P en Transifex](https://explore.transifex.com/otf/I2P/)
3. **Solicita unirte** a tu equipo de idioma (o solicita un nuevo idioma si no está listado)
4. **Comienza a traducir** una vez aprobado

### ¿Por qué Transifex?

- **Interfaz amigable** - No se requiere conocimiento técnico
- **Memoria de traducción** - Sugiere traducciones basadas en trabajos anteriores
- **Colaboración** - Trabaja con otros traductores en tu idioma
- **Control de calidad** - El proceso de revisión asegura precisión
- **Actualizaciones automáticas** - Los cambios se sincronizan con el equipo de desarrollo

## Qué Traducir

### Consola del Router (Prioridad)

La consola del router de I2P es la interfaz principal con la que los usuarios interactúan cuando ejecutan I2P. Traducirla tiene el impacto más inmediato en la experiencia del usuario.

**Áreas clave a traducir:**

- **Interfaz principal** - Navegación, menús, botones, mensajes de estado
- **Páginas de configuración** - Descripciones de configuraciones y opciones
- **Documentación de ayuda** - Archivos de ayuda incorporados y descripciones emergentes
- **Noticias y actualizaciones** - Fuente de noticias inicial mostrada a los usuarios
- **Mensajes de error** - Mensajes de error y advertencia dirigidos al usuario
- **Configuraciones del proxy** - Páginas de configuración de HTTP, SOCKS y túneles

Todas las traducciones de la consola del router se gestionan a través de Transifex en formato `.po` (gettext).

## Directrices de Traducción

### Estilo y Tono

- **Claro y conciso** - I2P trata con conceptos técnicos; mantén las traducciones simples
- **Terminología consistente** - Usa los mismos términos a lo largo (verifica la memoria de traducción)
- **Formal vs. informal** - Sigue las convenciones para tu idioma
- **Preserva el formato** - Mantén intactos los marcadores de posición como `{0}`, `%s`, `<b>tags</b>`

### Consideraciones Técnicas

- **Codificación** - Usa siempre la codificación UTF-8
- **Marcadores de posición** - No traduzcas los marcadores de posición de variables (`{0}`, `{1}`, `%s`, etc.)
- **HTML/Markdown** - Preserva las etiquetas HTML y el formato Markdown
- **Enlaces** - Mantén los URLs sin cambios a menos que haya una versión localizada
- **Abreviaturas** - Considera si traduces o mantienes el original (ej. "KB/s", "HTTP")

### Probando tus Traducciones

Si tienes acceso a un router I2P:

1. Descarga los archivos de traducción más recientes de Transifex
2. Colócalos en tu instalación de I2P
3. Reinicia la consola del router
4. Revisa las traducciones en contexto
5. Reporta cualquier problema o mejoras necesarias

## Obtener Ayuda

### Soporte Comunitario

- **Canal IRC**: `#i2p-dev` en I2P IRC u OFTC
- **Foro**: Foros de desarrollo de I2P
- **Comentarios en Transifex**: Haz preguntas directamente sobre las cadenas de traducción

### Preguntas Comunes

**P: ¿Con qué frecuencia debo traducir?**  
Traduce a tu propio ritmo. Incluso traducir unas pocas cadenas ayuda. El proyecto es continuo.

**P: ¿Qué hago si mi idioma no está listado?**  
Solicita un nuevo idioma en Transifex. Si hay demanda, el equipo lo añadirá.

**P: ¿Puedo traducir solo o necesito un equipo?**  
Puedes empezar solo. A medida que más traductores se unan a tu idioma, puedes colaborar.

**P: ¿Cómo sé qué necesita traducción?**  
Transifex muestra porcentajes de finalización y resalta las cadenas no traducidas.

**P: ¿Qué hago si no estoy de acuerdo con una traducción existente?**  
Sugiere mejoras en Transifex. Los revisores evaluarán los cambios.

## Avanzado: Traducción Manual (Opcional)

Para traductores experimentados que quieren acceso directo a los archivos fuente:

### Requisitos

- **Git** - Sistema de control de versiones
- **POEdit** o editor de texto - Para editar archivos `.po`
- **Conocimiento básico de línea de comandos**

### Proceso

1. **Clona el repositorio**:
   ```bash
   git clone https://i2pgit.org/i2p-hackers/i2p.i2p.git
   ```

2. **Encuentra los archivos de traducción**:
   - Consola del router: `apps/routerconsole/locale/`
   - Busca `messages_xx.po` (donde `xx` es el código de tu idioma)

3. **Edita las traducciones**:
   - Usa POEdit o un editor de texto
   - Guarda con codificación UTF-8

4. **Prueba localmente** (si tienes I2P instalado)

5. **Envía los cambios**:
   - Crea una solicitud de fusión en [I2P Git](https://i2pgit.org/)
   - O comparte tu archivo `.po` con el equipo de desarrollo

**Nota**: La mayoría de los traductores deberían usar Transifex. La traducción manual es solo para aquellos cómodos con Git y los flujos de trabajo de desarrollo.

## Gracias

Cada traducción ayuda a que I2P sea más accesible para usuarios en todo el mundo. Ya sea que traduzcas unas pocas cadenas o secciones enteras, tu contribución hace una diferencia real ayudando a las personas a proteger su privacidad en línea.

**¿Listo para empezar?** [Únete a I2P en Transifex →](https://explore.transifex.com/otf/I2P/)
