---
title: "Guía para Nuevos Desarrolladores"
description: "Cómo empezar a contribuir a I2P: materiales de estudio, código fuente, compilación, ideas, publicación, comunidad, traducciones y herramientas"
slug: "new-developers"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
type: docs
notes: actualizar parte de traducción
---

¿Así que quieres empezar a trabajar en I2P? ¡Genial! Aquí tienes una guía rápida para comenzar a contribuir al sitio web o al software, realizar desarrollo o crear traducciones.

¿No estás listo para programar todavía? Prueba [involucrarte](/get-involved/) primero.

## Conoce Java

El router I2P y sus aplicaciones integradas utilizan Java como lenguaje de desarrollo principal. Si no tienes experiencia con Java, siempre puedes consultar [Thinking in Java](https://chenweixiang.github.io/docs/Thinking_in_Java_4th_Edition.pdf)

Estudia la introducción general, otros documentos de "cómo hacer", la introducción técnica y los documentos asociados:

- Cómo introducción: [Introducción a I2P](/docs/overview/intro/)
- Centro de documentación: [Documentación](/docs/)
- Introducción técnica: [Introducción Técnica](/docs/overview/tech-intro/)

Estos te darán una buena visión general de cómo está estructurado I2P y qué diferentes cosas hace.

## Obtener el código de I2P

Para el desarrollo del router I2P o de las aplicaciones integradas, necesitas obtener el código fuente.

### Nuestra forma actual: Git

I2P tiene servicios Git oficiales y acepta contribuciones vía Git en nuestro propio GitLab:

- Dentro de I2P: <http://git.idk.i2p>
- Fuera de I2P: <https://i2pgit.org>

Clona el repositorio principal:

```
git clone https://i2pgit.org/I2P_Developers/i2p.i2p.git
```
También está disponible un espejo de solo lectura en GitHub:

- Espejo en GitHub: [github.com/i2p/i2p.i2p](https://github.com/i2p/i2p.i2p)

```
git clone https://github.com/i2p/i2p.i2p.git
```
## Compilar I2P

Para compilar el código, necesitas el Sun/Oracle Java Development Kit 6 o superior, o un JDK equivalente (se recomienda encarecidamente Sun/Oracle JDK 6) y Apache Ant versión 1.7.0 o superior. Si estás trabajando en el código principal de I2P, ve al directorio `i2p.i2p` y ejecuta `ant` para ver las opciones de compilación.

Para compilar o trabajar en las traducciones de la consola, necesitas las herramientas `xgettext`, `msgfmt` y `msgmerge` del paquete GNU gettext.

Para el desarrollo de nuevas aplicaciones, consulta la [guía de desarrollo de aplicaciones](/docs/develop/applications/).

## Ideas de Desarrollo

Consulta la lista de tareas pendientes (TODO) del proyecto o la lista de problemas en GitLab para obtener ideas:

- Problemas de GitLab: [i2pgit.org/I2P_Developers/i2p.i2p/issues](https://i2pgit.org/I2P_Developers/i2p.i2p/issues)

## Haciendo Disponibles los Resultados

Consulta la parte inferior de la página de licencias para los requisitos de privilegios de commit. Necesitas estos para colocar código en `i2p.i2p` (¡no requerido para el sitio web!).

- [Página de licencias](/docs/develop/licenses#commit)

## ¡Conócenos!

Los desarrolladores se encuentran en IRC. Se les puede contactar en varias redes y en las redes internas de I2P. El lugar habitual para buscar es `#i2p-dev`. ¡Únete al canal y saluda! También tenemos [pautas adicionales para desarrolladores habituales](/docs/develop/dev-guidelines/).

## Traducciones

Traductores del sitio web y la consola del router: Consulta la [Guía para Nuevos Traductores](/docs/develop/new-translators/) para los siguientes pasos.

## Herramientas

I2P es software de código abierto que se desarrolla principalmente utilizando herramientas de código abierto. El proyecto I2P recientemente adquirió una licencia para YourKit Java Profiler. Los proyectos de código abierto son elegibles para recibir una licencia gratuita siempre que se haga referencia a YourKit en el sitio web del proyecto. Por favor, ponte en contacto si estás interesado en realizar análisis de rendimiento del código base de I2P.

YourKit apoya amablemente proyectos de código abierto con sus perfiladores completos. YourKit, LLC es el creador de herramientas innovadoras e inteligentes para perfilar aplicaciones Java y .NET. Echa un vistazo a los productos de software líderes de YourKit:

- [YourKit Java Profiler](http://www.yourkit.com/java/profiler/index.jsp)
- [YourKit .NET Profiler](http://www.yourkit.com/.net/profiler/index.jsp)
