---
title: "Usando un IDE con I2P"
description: "Configurar Eclipse y NetBeans para desarrollar I2P con Gradle y archivos de proyecto incluidos"
slug: "ides"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
type: docs
reviewStatus: "needs-review"
---

<p> La rama principal de desarrollo de I2P (<code>i2p.i2p</code>) ha sido configurada para permitir a los desarrolladores configurar fácilmente dos de los IDEs más comúnmente utilizados para el desarrollo en Java: Eclipse y NetBeans. </p>

<h2>Eclipse</h2>

<p> Las ramas principales de desarrollo de I2P (<code>i2p.i2p</code> y las ramas derivadas de ella) contienen <code>build.gradle</code> para permitir que la rama se configure fácilmente en Eclipse. </p>

<ol> <li> Asegúrate de tener una versión reciente de Eclipse. Cualquier versión posterior a 2017 debería funcionar. </li> <li> Clona la rama de I2P en algún directorio (por ejemplo, <code>$HOME/dev/i2p.i2p</code>). </li> <li> Selecciona "File → Import..." y luego bajo "Gradle" selecciona "Existing Gradle Project". </li> <li> Para "Project root directory:" elige el directorio donde se clonó la rama de I2P. </li> <li> En el diálogo "Import Options", selecciona "Gradle Wrapper" y presiona Continue. </li> <li> En el diálogo "Import Preview" puedes revisar la estructura del proyecto. Deberían aparecer múltiples proyectos bajo "i2p.i2p". Presiona "Finish". </li> <li> ¡Listo! Tu espacio de trabajo ahora debería contener todos los proyectos dentro de la rama de I2P, y sus dependencias de compilación deberían estar configuradas correctamente. </li> </ol>

<h2>NetBeans</h2>

<p> Las ramas principales de desarrollo de I2P (<code>i2p.i2p</code> y las ramas derivadas de ella) contienen archivos de proyecto de NetBeans. </p>

<!-- Mantener el contenido mínimo y cercano al original; se actualizará más adelante. -->
