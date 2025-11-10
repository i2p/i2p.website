---
title: "Nuevos I2P Routers"
date: 2025-10-16
author: "idk"
categories: ["community"]
description: "Están surgiendo múltiples nuevas implementaciones de router I2P, incluyendo emissary en Rust y go-i2p en Go, lo que abre nuevas posibilidades para la integración y la diversidad de la red."
API_Translate: verdadero
---

Es un momento emocionante para el desarrollo de I2P; nuestra comunidad está creciendo y ahora están apareciendo múltiples prototipos nuevos de I2P router (enrutador) completamente funcionales. Estamos muy entusiasmados con este desarrollo y con compartir esta noticia con ustedes.

## ¿Cómo ayuda esto a la red?

Desarrollar routers I2P nos ayuda a demostrar que nuestros documentos de especificación pueden utilizarse para producir nuevos routers I2P, abre el código a nuevas herramientas de análisis y, en general, mejora la seguridad y la interoperabilidad de la red. La existencia de múltiples routers I2P implica que los posibles errores no sean uniformes; un ataque contra un router puede no funcionar contra otro distinto, evitando así un problema de monocultivo. Sin embargo, quizá la perspectiva más emocionante a largo plazo sea la integración.

## ¿Qué es la incrustación?

En el contexto de I2P, embedding (integración embebida) es una forma de incluir un router de I2P en otra aplicación directamente, sin requerir un router independiente ejecutándose en segundo plano. Esta es una forma de hacer que I2P sea más fácil de usar, lo que facilita el crecimiento de la red al hacer que el software sea más accesible. Tanto Java como C++ adolecen de ser difíciles de usar fuera de sus propios ecosistemas; C++ requiere enlaces en C escritos a mano y frágiles y, en el caso de Java, la dificultad de comunicarse con una aplicación de la JVM desde una aplicación que no se ejecuta sobre la JVM.

Si bien en muchos sentidos esta situación es bastante normal, creo que puede mejorarse para hacer que I2P sea más accesible. Otros lenguajes tienen soluciones más elegantes a estos problemas. Por supuesto, siempre debemos considerar y utilizar las directrices existentes para los routers de Java y C++.

## El emisario aparece de la oscuridad

Completamente independiente de nuestro equipo, un desarrollador llamado altonen ha desarrollado una implementación en Rust de I2P llamada emissary. Aunque aún es bastante nuevo y Rust nos resulta poco familiar, este intrigante proyecto tiene un gran potencial. Felicitaciones a altonen por crear emissary; estamos bastante impresionados.

### Why Rust?

La razón principal para usar Rust es esencialmente la misma que la de usar Java o Go. Rust es un lenguaje de programación compilado con gestión de memoria y una comunidad enorme y sumamente entusiasta. Rust también ofrece características avanzadas para crear bindings (enlaces) al lenguaje de programación C, que pueden ser más fáciles de mantener que en otros lenguajes y, al mismo tiempo, heredan las sólidas garantías de seguridad de memoria de Rust.

### Do you want to get involved with emissary?

emissary es desarrollado por altonen en GitHub. Puedes encontrar el repositorio en: [altonen/emissary](https://github.com/altonen/emissary). Rust también adolece de una falta de bibliotecas de cliente SAMv3 completas que sean compatibles con las bibliotecas y herramientas de redes más populares de Rust; escribir una biblioteca SAMv3 es un excelente punto de partida.

## go-i2p is getting closer to completion

Desde hace aproximadamente 3 años he estado trabajando en go-i2p, tratando de convertir una biblioteca incipiente en un I2P router completamente funcional escrito en Go puro, otro lenguaje con seguridad de memoria. En los últimos 6 meses aproximadamente, se ha reestructurado drásticamente para mejorar el rendimiento, la fiabilidad y la mantenibilidad.

### Why Go?

Si bien Rust y Go comparten muchas de las mismas ventajas, en muchos aspectos Go es mucho más sencillo de aprender. Durante años, han existido excelentes bibliotecas y aplicaciones para usar I2P en el lenguaje de programación Go, incluidas las implementaciones más completas de las bibliotecas SAMv3.3. Pero sin un router de I2P que podamos gestionar automáticamente (como un router integrado), sigue suponiendo una barrera para los usuarios. El objetivo de go-i2p es salvar esa brecha y eliminar todas las fricciones para los desarrolladores de aplicaciones de I2P que trabajan en Go.

### ¿Por qué Rust?

go-i2p se desarrolla en Github, principalmente por eyedeekay en este momento y está abierto a contribuciones de la comunidad en [go-i2p](https://github.com/go-i2p/). Dentro de este espacio de nombres (namespace) existen muchos proyectos, como:

#### Router Libraries

Desarrollamos estas bibliotecas para crear nuestras bibliotecas del router I2P. Están distribuidas en varios repositorios especializados para facilitar la revisión y hacerlas útiles para otras personas que quieran construir routers I2P experimentales y personalizados.

- [go-i2p the router itself, most active right now](https://github.com/go-i2p/go-i2p)
- [common our core library for I2P datastructures](https://github.com/go-i2p/common)
- [crypto our library for cryptographic operations](https://github.com/go-i2p/crypto)
- [go-noise a library for implementing noise-based connections](https://github.com/go-i2p/go-noise)
- [noise a low-level library for using the Noise framework](https://github.com/go-i2p/noise)
- [su3 a library for manipulating su3 files](https://github.com/go-i2p/su3)

#### Client libraries

- [onramp a very convenient library for using(or combining) I2P and Tor](https://github.com/go-i2p/onramp)
- [go-sam-go an advanced, efficient, and very complete SAMv3 library](https://github.com/go-i2p/go-sam-go)

## If you don't like Go or Rust and are thinking of writing an I2P Router, what should you do?

Bueno, hay un proyecto inactivo para escribir un [I2P router en C#](https://github.com/PeterZander/i2p-cs) si quieres ejecutar I2P en un XBox. De hecho, suena bastante interesante. Si eso tampoco te convence, podrías hacer como altonen y desarrollar uno completamente nuevo.

### ¿Quieres participar en emissary?

Puedes desarrollar un router I2P por cualquier motivo; es una red libre, pero te ayudará saber por qué. ¿Hay una comunidad a la que quieras empoderar, una herramienta que creas que encaja bien con I2P o una estrategia que quieras probar? Determina cuál es tu objetivo para saber por dónde debes empezar y cómo se verá un estado "terminado".

### Decide what language you want to do it in and why

Aquí hay algunas razones por las que podrías elegir un idioma:

- **C**: No need for binding-generation, supported everywhere, can be called from any language, lingua franca of modern computing
- **Typescript**: Massive community, lots of applications, services, and libraries, works with node and deno, seems like it's everywhere right now
- **D**: It's memory safe and not Rust or Go
- **Vala**: It emits C code for the target platform, combining some of the advantages of memory-safe languages with the flexibility of C
- **Python**: Everybody uses Python

Pero aquí tienes algunas razones por las que podrías no elegir esos lenguajes:

- **C**: Memory management can be challenging, leading to impactful bugs
- **Typescript**: TypeScript is transpiled to JavaScript, which is interpreted and may impact performance
- **D**: Relatively small community
- **Vala**: Not a lot of underlying infrastructure in Vala, you end up using C versions of most libraries
- **Python**: It's an interpreted language which may impact performance

Hay cientos de lenguajes de programación y damos la bienvenida a bibliotecas de I2P mantenidas y routers en todos ellos. Elige sabiamente los compromisos y comienza.

## go-i2p está cada vez más cerca de completarse

Ya sea que quieras trabajar en Rust, Go, Java, C++ u otro lenguaje, ponte en contacto con nosotros en #i2p-dev en Irc2P. Empieza ahí y te incorporaremos a canales específicos del router. También estamos presentes en ramble.i2p en f/i2p, en reddit en r/i2p, y en GitHub y git.idk.i2p. Esperamos tener noticias tuyas pronto.
