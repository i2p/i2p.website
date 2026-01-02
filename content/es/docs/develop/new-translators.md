---
title: "Guía para Nuevos Traductores"
description: "Cómo contribuir con traducciones al sitio web de I2P y a la consola del router utilizando Transifex o métodos manuales"
slug: "new-translators"
lastUpdated: "2025-10"
type: docs
---

¿Quieres ayudar a hacer I2P accesible a más personas en todo el mundo? La traducción es una de las contribuciones más valiosas que puedes hacer al proyecto. Esta guía te mostrará cómo traducir la consola del router.

## Métodos de traducción

Hay dos formas de contribuir con traducciones:

### Método 1: Transifex (Recomendado)

**Esta es la forma más fácil de traducir I2P.** Transifex proporciona una interfaz web que hace que la traducción sea simple y accesible.

1. Regístrate en [Transifex](https://www.transifex.com/otf/I2P/)
2. Solicita unirte al equipo de traducción de I2P
3. Comienza a traducir directamente en tu navegador

No se requieren conocimientos técnicos - ¡solo regístrate y comienza a traducir!

### Método 2: Traducción Manual

Para traductores que prefieren trabajar con git y archivos locales, o para idiomas que aún no están configurados en Transifex.

**Requisitos:** - Familiaridad con el control de versiones git - Editor de texto o herramienta de traducción (se recomienda POEdit) - Herramientas de línea de comandos: git, gettext

**Configuración:** 1. Únete a [#i2p-dev en IRC](/contact/#irc) y preséntate 2. Actualiza el estado de la traducción en el wiki (solicita acceso en IRC) 3. Clona el repositorio apropiado (consulta las secciones a continuación)

---

## Traducción de la Consola del Router

La consola del router es la interfaz web que ves cuando ejecutas I2P. Traducirla ayuda a usuarios que no se sienten cómodos con el inglés.

### Usando Transifex (Recomendado)

1. Ve a [I2P en Transifex](https://www.transifex.com/otf/I2P/)
2. Selecciona el proyecto de la consola del router
3. Elige tu idioma
4. Comienza a traducir

### Traducción Manual de la Consola del Router

**Prerrequisitos:** - Igual que la traducción del sitio web (git, gettext) - Clave GPG (para acceso de confirmación) - Acuerdo de desarrollador firmado

**Clona el repositorio principal de I2P:**

```bash
git clone https://i2pgit.org/I2P_Developers/i2p.i2p.git
cd i2p.i2p
```
**Archivos a traducir:**

La consola del router tiene aproximadamente 15 archivos que necesitan traducción:

1. **Archivos de interfaz principales:**
   - `apps/routerconsole/locale/messages_*.po` - Mensajes principales de la consola
   - `apps/routerconsole/locale-news/messages_*.po` - Mensajes de noticias

2. **Archivos de proxy:**
   - `apps/i2ptunnel/locale/messages_*.po` - Interfaz de configuración de túneles

3. **Locales de aplicaciones:**
   - `apps/susidns/locale/messages_*.po` - Interfaz de libreta de direcciones
   - `apps/susimail/locale/messages_*.po` - Interfaz de correo electrónico
   - Otros directorios de locales específicos de aplicaciones

4. **Archivos de documentación:**
   - `installer/resources/readme/readme_*.html` - Léame de instalación
   - Archivos de ayuda en varias aplicaciones

**Flujo de trabajo de traducción:**

```bash
# Update .po files from source
ant extractMessages

# Edit .po files with POEdit or text editor
poedit apps/routerconsole/locale/messages_es.po

# Build and test
ant updaters
# Install the update and check translations in the console
```
**Envía tu trabajo:** - Crea una solicitud de fusión en [GitLab](https://i2pgit.org/I2P_Developers/i2p.i2p) - O comparte archivos con el equipo de desarrollo en IRC

---

## Herramientas de Traducción

### POEdit (Altamente Recomendado)

[POEdit](https://poedit.net/) es un editor especializado para archivos de traducción .po.

**Características:** - Interfaz visual para el trabajo de traducción - Muestra el contexto de traducción - Validación automática - Disponible para Windows, macOS y Linux

### Editores de Texto

También puedes usar cualquier editor de texto: - VS Code (con extensiones i18n) - Sublime Text - vim/emacs (para usuarios de terminal)

### Comprobaciones de Calidad

Antes de enviar: 1. **Revisa el formato:** Asegúrate de que los marcadores de posición como `%s` y `{0}` permanezcan sin cambios 2. **Prueba tus traducciones:** Instala y ejecuta I2P para ver cómo se ven 3. **Coherencia:** Mantén la terminología coherente en todos los archivos 4. **Longitud:** Algunas cadenas tienen restricciones de espacio en la interfaz de usuario

---

## Consejos para Traductores

### Directrices Generales

- **Mantén la consistencia:** Usa las mismas traducciones para términos comunes en todo el documento
- **Conserva el formato:** Preserva las etiquetas HTML, marcadores de posición (`%s`, `{0}`) y saltos de línea
- **El contexto importa:** Lee cuidadosamente el texto fuente en inglés para comprender el contexto
- **Haz preguntas:** Usa IRC o los foros si algo no está claro

### Términos Comunes de I2P

Algunos términos deben permanecer en inglés o transliterarse cuidadosamente:

- **I2P** - Keep as is
- **eepsite** - Sitio web I2P (puede requerir explicación en tu idioma)
- **tunnel** - Ruta de conexión (evitar terminología de Tor como "circuito")
- **netDb** - Base de datos de red
- **floodfill** - Tipo de router
- **destination** - Punto final de dirección I2P

### Probando Tus Traducciones

1. Compila I2P con tus traducciones
2. Cambia el idioma en la configuración de la consola del router
3. Navega por todas las páginas para verificar:
   - El texto encaja en los elementos de la interfaz
   - No hay caracteres ilegibles (problemas de codificación)
   - Las traducciones tienen sentido en el contexto

---

## Preguntas Frecuentes

### ¿Por qué es tan complejo el proceso de traducción?

El proceso utiliza control de versiones (git) y herramientas de traducción estándar (archivos .po) porque:

1. **Responsabilidad:** Rastrear quién cambió qué y cuándo
2. **Calidad:** Revisar los cambios antes de que se publiquen
3. **Consistencia:** Mantener el formato y estructura adecuados de los archivos
4. **Escalabilidad:** Gestionar traducciones en múltiples idiomas de manera eficiente
5. **Colaboración:** Múltiples traductores pueden trabajar en el mismo idioma

### ¿Necesito conocimientos de programación?

**¡No!** Si usas Transifex, solo necesitas: - Fluidez tanto en inglés como en tu idioma objetivo - Un navegador web - Habilidades informáticas básicas

Para la traducción manual, necesitarás conocimientos básicos de línea de comandos, pero no se requiere programación.

### ¿Cuánto tiempo tarda?

- **Consola del router:** Aproximadamente 15-20 horas para todos los archivos
- **Mantenimiento:** Unas pocas horas por mes para actualizar nuevas cadenas de texto

### ¿Pueden varias personas trabajar en un mismo idioma?

¡Sí! La coordinación es clave: - Usa Transifex para coordinación automática - Para trabajo manual, comunícate en el canal IRC #i2p-dev - Divide el trabajo por secciones o archivos

### ¿Qué pasa si mi idioma no está en la lista?

Solicítalo en Transifex o contacta al equipo en IRC. El equipo de desarrollo puede configurar un nuevo idioma rápidamente.

### ¿Cómo pruebo mis traducciones antes de enviarlas?

- Compila I2P desde el código fuente con tus traducciones
- Instálalo y ejecútalo localmente
- Cambia el idioma en la configuración de la consola

---

## Obtener Ayuda

### Soporte IRC

Únete a [#i2p-dev en IRC](/contact/#irc) para: - Ayuda técnica con herramientas de traducción - Preguntas sobre terminología de I2P - Coordinación con otros traductores - Soporte directo de los desarrolladores

### Foros

- Discusiones sobre traducción en [Foros I2P](http://i2pforum.net/)
- Dentro de I2P: foro de Traducción en zzz.i2p (requiere router I2P)

### Documentación

- [Documentación de Transifex](https://docs.transifex.com/)
- [Documentación de POEdit](https://poedit.net/support)
- [Manual de gettext](https://www.gnu.org/software/gettext/manual/)

---

## Reconocimiento

Todos los traductores son acreditados en: - La consola del router I2P (página Acerca de) - Página de créditos del sitio web - Historial de commits de Git - Anuncios de lanzamiento

Tu trabajo ayuda directamente a personas de todo el mundo a usar I2P de forma segura y privada. ¡Gracias por contribuir!

---

## Próximos Pasos

¿Listo para comenzar a traducir?

1. **Elija su método:**
   - Inicio rápido: [Regístrese en Transifex](https://www.transifex.com/otf/I2P/)
   - Enfoque manual: Únase a [#i2p-dev en IRC](/contact/#irc)

2. **Empieza poco a poco:** Traduce algunas cadenas de texto para familiarizarte con el proceso

3. **Pide ayuda:** No dudes en contactar a través de IRC o foros

**¡Gracias por ayudar a hacer I2P accesible para todos!**
