---
title: "Notas de estado de I2P del 2006-09-12"
date: 2006-09-12
author: "jr"
description: "Versión 0.6.1.25 con mejoras en la estabilidad de la red, optimizaciones de I2PSnark y un rediseño integral de Syndie con foros distribuidos sin conexión"
categories: ["status"]
---

Hola a todos, aquí están nuestras *ejem* notas de estado semanales

* Index:

1) 0.6.1.25 y estado de la red 2) I2PSnark 3) Syndie (qué/por qué/cuándo) 4) preguntas sobre criptografía de Syndie 5) ???

* 1) 0.6.1.25 and net status

El otro día publicamos la versión 0.6.1.25, que incluye la avalancha de correcciones de errores acumuladas durante el último mes, así como el trabajo de zzz en I2PSnark y el de Complication para intentar que nuestro código de sincronización de tiempo sea un poco más robusto. En este momento la red parece bastante estable, aunque IRC ha estado un poco inestable en los últimos días (por razones no relacionadas con I2P). Con quizá la mitad de la red actualizada a la última versión, las tasas de éxito en la construcción de tunnel no han cambiado mucho, aunque el rendimiento global parece haber aumentado (probablemente debido a un aumento en el número de personas que usan I2PSnark).

* 2) I2PSnark

Las actualizaciones de zzz a I2PSnark incluyeron optimizaciones del protocolo, así como cambios en las interfaces web, tal como se describe en el registro de cambios [1]. También ha habido algunas pequeñas actualizaciones de I2PSnark desde la versión 0.6.1.25, y quizás zzz pueda darnos un panorama de lo que ocurre durante la reunión de esta noche.

[1] <http://dev.i2p.net/cgi-bin/cvsweb.cgi/i2p/history.txt?rev=HEAD>

* 3) Syndie

Como ya saben, mi tiempo se ha centrado en renovar Syndie, aunque "revamp" quizá no sea la palabra adecuada. Quizá puedan considerar lo que está actualmente desplegado como una "prueba de concepto", ya que el nuevo Syndie ha sido rediseñado y reimplementado desde cero, aunque muchos conceptos permanecen. Cuando me refiera a Syndie más abajo, me estaré refiriendo al nuevo Syndie.

* 3.1) What is Syndie

Syndie es, en su nivel más básico, un sistema para gestionar foros distribuidos sin conexión. Si bien su estructura da lugar a un gran número de configuraciones diferentes, la mayoría de las necesidades se satisfarán seleccionando una de las opciones de cada uno de los siguientes tres criterios:  - Tipos de foros:    - Un solo autor (blog típico)    - Varios autores (blog multiautor)**    - Abierto (grupos de noticias, aunque se pueden incluir restricciones para que solo
      los usuarios autorizados** puedan abrir hilos nuevos, mientras que cualquiera puede comentar en
      esos nuevos hilos)  - Visibilidad:    - Cualquiera puede leer cualquier cosa    - Solo las personas autorizadas* pueden leer las publicaciones, pero se exponen ciertos metadatos    - Solo las personas autorizadas* pueden leer las publicaciones, o incluso saber quién está publicando    - Solo las personas autorizadas* pueden leer las publicaciones, y nadie sabe quién está
      publicando  - Comentarios/respuestas:    - Cualquiera puede comentar o enviar respuestas privadas al autor/propietario
      del foro    - Solo las personas autorizadas** pueden comentar, y cualquiera puede enviar respuestas
      privadas    - Nadie puede comentar, pero cualquiera puede enviar respuestas privadas    - Nadie puede comentar, y nadie puede enviar respuestas privadas

 * reading is authorized by giving people the symmetric key or passphrase
   to decrypt the post.  Alternately, the post may include a publicly
   visible prompt, where the correct answer serves to generate the
   correct decryption key.

** publicar, actualizar y/o comentar se autoriza proporcionando a esos    usuarios claves privadas asimétricas con las que firmar las publicaciones, donde la    clave pública correspondiente se incluye en los metadatos del foro como    autorizada para publicar, gestionar o comentar en el foro.  Alternativamente, las    claves públicas de firma de los usuarios autorizados individualmente pueden figurar en    los metadatos.

Las publicaciones individuales pueden contener muchos elementos diferentes:  - Cualquier número de páginas, con datos fuera de banda para cada página que especifiquen
    el tipo de contenido, el idioma, etc.  Se puede usar cualquier formato, ya que
    depende de la aplicación cliente representar el contenido de forma segura - el texto plano
    debe ser admitido, y los clientes que puedan deberían admitir HTML.  - Cualquier número de adjuntos (nuevamente, con datos fuera de banda que describan el
    adjunto)  - Un avatar pequeño para la publicación (pero si no se especifica, el
    avatar predeterminado del autor se usa)  - Un conjunto de referencias a otras publicaciones, foros, archivos, URLs, etc (que
    pueden incluir las claves necesarias para publicar, administrar o leer los
    foros referenciados)

En general, Syndie opera en la *capa de contenido* - las publicaciones individuales están contenidas en archivos zip cifrados, y participar en el foro significa simplemente compartir estos archivos. No hay dependencias con respecto a cómo se transfieren los archivos (a través de I2P, Tor, Freenet, gnutella, bittorrent, RSS, usenet, email), pero se incluirán herramientas sencillas de agregación y distribución con la versión estándar de Syndie.

La interacción con el contenido de Syndie se realizará de varias maneras. En primer lugar, hay una interfaz de texto programable mediante scripts, que permite, tanto desde la línea de comandos como de forma interactiva, leer desde, escribir en, administrar y sincronizar los foros. Por ejemplo, el siguiente es un script sencillo para generar una nueva publicación de "mensaje del día" -

login     menu post     create --channel 0000000000000000000000000000000000000000     addpage --in /etc/motd --content-type text/plain     addattachment --in ~/webcam.png --content-type image/png     listauthkeys --authorizedOnly true     authenticate 0     authorize 0     set --subject "Today's MOTD"     set --publicTags motd     execute     exit

Simplemente pásalo por el ejecutable syndie y ya está: cat motd-script | ./syndie > syndie.log

Además, se está trabajando en una interfaz gráfica de Syndie, que incluye el renderizado seguro de texto plano y páginas HTML (por supuesto, con soporte para la integración transparente con las funciones de Syndie).

Las aplicaciones basadas en el antiguo código "sucker" de Syndie permitirán la extracción (scraping) y la reescritura de páginas y sitios web normales para que puedan utilizarse como publicaciones de Syndie de una o varias páginas, incluyendo imágenes y otros recursos como adjuntos.

Más adelante, se planean complementos de firefox/mozilla que detecten e importen archivos con formato Syndie y referencias de Syndie, y que además notifiquen a la interfaz gráfica local de Syndie que un foro, tema, etiqueta, autor o resultado de búsqueda determinado debe llevarse al primer plano.

Por supuesto, dado que Syndie es, en esencia, una capa de contenido con un formato de archivo definido y algoritmos criptográficos, probablemente con el tiempo surgirán otras aplicaciones o implementaciones alternativas.

* 3.2) Why does Syndie matter?

He oído a varias personas preguntar en los últimos meses por qué estoy trabajando en una herramienta de foros/blogs - ¿qué tiene eso que ver con ofrecer anonimato fuerte?

La respuesta: *todo*.

Para resumir brevemente:  - El diseño de Syndie, como aplicación cliente sensible al anonimato, cuidadosamente
    evita los complejos problemas de sensibilidad de datos que casi todas
    las aplicaciones no concebidas con el anonimato en mente sí padecen.
  - Al operar en la capa de contenido, Syndie no depende del
    rendimiento ni de la fiabilidad de redes distribuidas como I2P, Tor o
    Freenet, aunque puede aprovecharlas cuando sea apropiado.
  - Al hacerlo, puede operar plenamente con mecanismos pequeños y ad-hoc para
    la distribución de contenido - mecanismos que quizá no justifiquen el esfuerzo
    de adversarios poderosos para contrarrestarlos (ya que el 'beneficio' de detener
    a apenas unas pocas docenas de personas probablemente exceda el costo de montar los
    ataques)
  - Esto implica que Syndie será útil incluso sin que la usen unos cuantos millones
    de personas - grupos pequeños y no relacionados deberían configurar su propio
    esquema privado de distribución de Syndie sin requerir ninguna
    interacción con, ni siquiera el conocimiento por parte de, otros grupos.
  - Dado que Syndie no depende de la interacción en tiempo real, incluso puede
    aprovechar sistemas y técnicas de anonimato de alta latencia para evitar los
    ataques a los que todos los sistemas de baja latencia son vulnerables (como
    ataques de intersección pasivos, ataques de temporización pasivos y activos, y
    ataques de mezcla activos).

En general, considero que Syndie es incluso más importante para la misión central de I2P (proporcionar un anonimato sólido a quienes lo necesitan) que el propio router. No es la panacea, pero es un paso clave.

* 3.3) When can we use Syndie?

Si bien se ha completado gran parte del trabajo (incluida casi toda la interfaz de texto y una buena parte de la GUI (interfaz gráfica de usuario)), todavía queda trabajo por hacer. La primera versión de Syndie incluirá la siguiente funcionalidad básica:

 - Scriptable text interface, packaged up as a typical java application,
   or buildable with a modern GCJ
 - Support for all forum types, replies, comments, etc.
 - Manual syndication, transferring .snd files.
 - HTTP syndication, including simple CGI scripts to operate archives,
   controllable through the text interface.
 - Specs for the file formats, encryption algorithms, and database
   schema.

El criterio que usaré para lanzarlo será "totalmente funcional". El usuario promedio no va a ponerse a experimentar con una aplicación basada en texto, pero espero que algunos entusiastas sí lo hagan.

Las versiones posteriores mejorarán las capacidades de Syndie en varias dimensiones:  - Interfaz de usuario:   - GUI basada en SWT   - Complementos del navegador web   - Interfaz de texto basada en scraping web (recuperando y reescribiendo páginas)   - Interfaz de lectura para IMAP/POP3/NNTP  - Compatibilidad de contenido   - Texto plano   - HTML (renderizado seguro dentro de la GUI, no en un navegador)   - BBCode (?)  - Sindicación   - Feedspace, Feedtree y otras herramientas de sincronización de baja latencia   - Freenet (almacenando archivos .snd en CHK@s y archivos que hacen referencia
    a los archivos .snd en SSK@s y USK@s)   - Correo electrónico (enviar a través de SMTP/mixmaster/mixminion, leer mediante
    procmail/etc)   - Usenet (enviar a través de NNTP o remailers, leer mediante (con proxy)
    NNTP)  - Búsqueda de texto completo con integración de Lucene  - Extensión de HSQLDB para el cifrado completo de la base de datos  - Heurísticas adicionales para la gestión de archivos

Lo que se produce y cuándo se produce depende de cuándo se hacen las cosas.

* 4) Open questions for Syndie

Actualmente, Syndie se ha implementado con las primitivas criptográficas estándar de I2P - SHA256, AES256/CBC, ElGamal2048, DSA. Sin embargo, la última es la excepción, ya que utiliza claves públicas de 1024 bits y depende de SHA1 (que se está debilitando rápidamente). Uno de los rumores que he oído en el campo ha sido la ampliación de DSA con SHA256 y, aunque eso es factible (aunque aún no está estandarizado), solo ofrece claves públicas de 1024 bits.

Como Syndie aún no se ha lanzado públicamente y no hay preocupación por la compatibilidad con versiones anteriores, podemos permitirnos intercambiar las primitivas criptográficas. Una línea de pensamiento es optar por firmas ElGamal2048 o RSA2048 en lugar de DSA, mientras que otra línea de pensamiento es considerar ECC (con firmas ECDSA y cifrado asimétrico ECIES), quizá en los niveles de seguridad de 256 bits o 521 bits (equivalentes a tamaños de clave simétrica de 128 bits y 256 bits, respectivamente).

En cuanto a los problemas de patentes relacionados con ECC (criptografía de curva elíptica), estos parecen ser pertinentes únicamente para optimizaciones concretas (compresión de puntos) y algoritmos que no necesitamos (EC MQV). No hay mucho soporte para Java, aunque la bouncycastle lib parece tener algo de código. Sin embargo, probablemente tampoco sería muy problemático añadir pequeños wrappers (envoltorios) a libtomcrypt, openssl o crypto++, como hicimos con libGMP (lo que nos dio jbigi).

¿Alguna opinión al respecto?

* 5) ???

Hay mucho que digerir más arriba, por eso (por sugerencia de cervantes) estoy enviando estas notas de estado tan pronto. Si tienes comentarios, preguntas, inquietudes o sugerencias, pásate por #i2p esta noche a las 20:00 UTC en irc.freenode.net/irc.postman.i2p/irc.freshcoffee.i2p para nuestra *ejem* reunión semanal!

=jr
