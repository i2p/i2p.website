---
title: "Directrices para Desarrolladores y Estilo de Codificación"
description: "Guía completa para contribuir a I2P: flujo de trabajo, ciclo de lanzamiento, estilo de código, registro de logs, licencias y gestión de problemas"
slug: "dev-guidelines"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
type: docs
---

Lee primero la [Guía para Nuevos Desarrolladores](/docs/develop/new-developers/).

## Directrices Básicas y Estilo de Codificación

La mayoría de lo siguiente debería ser sentido común para cualquiera que haya trabajado en código abierto o en un entorno de programación comercial. Lo siguiente se aplica principalmente a la rama de desarrollo principal i2p.i2p. Las directrices para otras ramas, plugins y aplicaciones externas pueden ser sustancialmente diferentes; consulta con el desarrollador correspondiente para obtener orientación.

### Comunidad

- Por favor, no solo escribas código. Si puedes, participa en otras actividades de desarrollo, incluyendo: discusiones de desarrollo y soporte en IRC e i2pforum.i2p; pruebas; reporte de errores y respuestas; documentación; revisiones de código; etc.
- Los desarrolladores activos deben estar disponibles periódicamente en IRC `#i2p-dev`. Ten en cuenta el ciclo de lanzamiento actual. Adhiérete a los hitos de lanzamiento como el congelamiento de características, congelamiento de etiquetas y la fecha límite de check-in para un lanzamiento.

### Ciclo de Lanzamiento

El ciclo de lanzamiento normal es de 10 a 16 semanas, cuatro lanzamientos al año. A continuación se muestran las fechas límite aproximadas dentro de un ciclo típico de 13 semanas. Las fechas límite reales para cada lanzamiento son establecidas por el gestor de lanzamientos después de consultar con todo el equipo.

- 1–2 días después del lanzamiento anterior: Se permiten check-ins en trunk.
- 2–3 semanas después del lanzamiento anterior: Fecha límite para propagar cambios importantes de otras ramas a trunk.
- 4–5 semanas antes del lanzamiento: Fecha límite para solicitar nuevos enlaces en la página de inicio.
- 3–4 semanas antes del lanzamiento: Congelación de funcionalidades. Fecha límite para nuevas funcionalidades importantes.
- 2–3 semanas antes del lanzamiento: Realizar reunión del proyecto para revisar solicitudes de nuevos enlaces en la página de inicio, si las hay.
- 10–14 días antes del lanzamiento: Congelación de cadenas de texto. No más cambios a cadenas traducidas (etiquetadas). Enviar cadenas a Transifex, anunciar fecha límite de traducción en Transifex.
- 10–14 días antes del lanzamiento: Fecha límite de funcionalidades. Solo correcciones de errores después de este momento. No más funcionalidades, refactorización o limpieza.
- 3–4 días antes del lanzamiento: Fecha límite de traducción. Obtener traducciones de Transifex y hacer check-in.
- 3–4 días antes del lanzamiento: Fecha límite de check-in. No se permiten check-ins después de este momento sin el permiso del responsable del lanzamiento.
- Horas antes del lanzamiento: Fecha límite de revisión de código.

### Git

- Ten una comprensión básica de los sistemas de control de fuente distribuidos, incluso si no has usado git antes. Pide ayuda si la necesitas. Una vez enviado, los check-ins son para siempre; no hay deshacer. Por favor, ten cuidado. Si no has usado git antes, comienza con pasos pequeños. Registra algunos cambios menores y observa cómo va.
- Prueba tus cambios antes de registrarlos. Si prefieres el modelo de desarrollo de check-in antes de probar, usa tu propia rama de desarrollo en tu propia cuenta, y crea un MR una vez que el trabajo esté terminado. No rompas el build. No causes regresiones. En caso de que lo hagas (sucede), por favor no desaparezcas por un largo período después de enviar tu cambio.
- Si tu cambio no es trivial, o quieres que las personas lo prueben y necesitas buenos reportes de prueba para saber si tu cambio fue probado o no, añade un comentario de check-in a `history.txt` e incrementa la revisión del build en `RouterVersion.java`.
- No registres cambios importantes en la rama principal de i2p.i2p al final del ciclo de lanzamiento. Si un proyecto te tomará más de un par de días, crea tu propia rama en git, en tu propia cuenta, y haz el desarrollo allí para no bloquear los lanzamientos.
- Para cambios grandes (en términos generales, más de 100 líneas, o que toquen más de tres archivos), regístralo en una nueva rama en tu propia cuenta de GitLab, crea un MR, y asigna un revisor. Asigna el MR a ti mismo. Fusiona el MR tú mismo una vez que el revisor lo apruebe.
- No crees ramas WIP en la cuenta principal de I2P_Developers (excepto para i2p.www). WIP pertenece a tu propia cuenta. Cuando el trabajo esté terminado, crea un MR. Las únicas ramas en la cuenta principal deben ser para verdaderos forks, como un lanzamiento puntual.
- Haz el desarrollo de manera transparente y con la comunidad en mente. Registra a menudo. Registra o fusiona en la rama principal tan frecuentemente como sea posible, dadas las pautas anteriores. Si estás trabajando en algún proyecto grande en tu propia rama/cuenta, avisa a las personas para que puedan seguirlo y revisar/probar/comentar.

### Estilo de Codificación

- El estilo de codificación en la mayor parte del código es de 4 espacios para la indentación. No uses tabulaciones. No reformatees el código. Si tu IDE o editor quiere reformatear todo, contrólalo. En algunos lugares, el estilo de codificación es diferente. Usa el sentido común. Emula el estilo en el archivo que estás modificando.
- Todas las clases y métodos públicos y package-private nuevos requieren Javadocs. Añade `@since` número-de-versión. Los Javadocs para métodos privados nuevos son deseables.
- Para cualquier Javadocs añadido, no debe haber errores o advertencias de doclint. Ejecuta `ant javadoc` con Oracle Java 14 o superior para verificar. Todos los parámetros deben tener líneas `@param`, todos los métodos no-void deben tener líneas `@return`, todas las excepciones declaradas como lanzadas deben tener líneas `@throws`, y sin errores HTML.
- Las clases en `core/` (i2p.jar) y porciones de i2ptunnel son parte de nuestra API oficial. Hay varios plugins externos y otras aplicaciones que dependen de esta API. Ten cuidado de no hacer cambios que rompan la compatibilidad. No añadas métodos a la API a menos que sean de utilidad general. Los Javadocs para métodos de la API deben ser claros y completos. Si añades o cambias la API, actualiza también la documentación en el sitio web (rama i2p.www).
- Etiqueta cadenas para traducción donde sea apropiado, lo cual es cierto para todas las cadenas de UI. No cambies cadenas etiquetadas existentes a menos que sea realmente necesario, ya que romperá las traducciones existentes. No añadas o cambies cadenas etiquetadas después del congelamiento de etiquetas en el ciclo de lanzamiento para que los traductores tengan oportunidad de actualizar antes del lanzamiento.
- Usa genéricos y clases concurrentes donde sea posible. I2P es una aplicación altamente multi-hilo.
- Familiarízate con los errores comunes de Java que detecta FindBugs/SpotBugs. Ejecuta `ant findbugs` para aprender más.
- Se requiere Java 8 para compilar y ejecutar I2P a partir de la versión 0.9.47. No uses clases o métodos de Java 7 u 8 en subsistemas embebidos: addressbook, core, i2ptunnel.jar (no-UI), mstreaming, router, routerconsole (solo noticias), streaming. Estos subsistemas son usados por Android y aplicaciones embebidas que requieren solo Java 6. Todas las clases deben estar disponibles en Android API 14. Las características del lenguaje Java 7 son aceptables en estos subsistemas si son soportadas por la versión actual del Android SDK y compilan a código compatible con Java 6.
- Try-with-resources no puede usarse en subsistemas embebidos ya que requiere `java.lang.AutoCloseable` en tiempo de ejecución, y esto no está disponible hasta Android API 19 (KitKat 4.4).
- El paquete `java.nio.file` no puede usarse en subsistemas embebidos ya que no está disponible hasta Android API 26 (Oreo 8).
- Aparte de las limitaciones anteriores, las clases, métodos y construcciones de Java 8 pueden usarse solo en los siguientes subsistemas: BOB, desktopgui, i2psnark, i2ptunnel.war (UI), jetty‑i2p.jar, jsonrpc, routerconsole (excepto noticias), SAM, susidns, susimail, systray.
- Los autores de plugins pueden requerir cualquier versión mínima de Java mediante el archivo `plugin.config`.
- Convierte explícitamente entre tipos primitivos y clases; no dependas de autoboxing/unboxing.
- No uses `URL`. Usa `URI`.
- No captures `Exception`. Captura `RuntimeException` y excepciones verificadas individualmente.
- No uses `String.getBytes()` sin un argumento charset UTF‑8. También puedes usar `DataHelper.getUTF8()` o `DataHelper.getASCII()`.
- Especifica siempre un charset UTF‑8 al leer o escribir archivos. Las utilidades de `DataHelper` pueden ser útiles.
- Especifica siempre una localización (por ejemplo `Locale.US`) al usar `String.toLowerCase()` o `String.toUpperCase()`. No uses `String.equalsIgnoreCase()`, ya que no se puede especificar una localización.
- No uses `String.split()`. Usa `DataHelper.split()`.
- No añadas código para formatear fechas y horas. Usa `DataHelper.formatDate()` y `DataHelper.formatTime()`.
- Asegúrate de que los `InputStream`s y `OutputStream`s se cierren en bloques finally.
- Usa `{}` para todos los bloques `for` y `while`, incluso si solo tienen una línea. Si usas `{}` para el bloque `if`, `else` o `if-else`, úsalo para todos los bloques. Pon `} else {` en una sola línea.
- Especifica los campos como `final` donde sea posible.
- No almacenes `I2PAppContext`, `RouterContext`, `Log`, o cualquier otra referencia a router o elementos de contexto en campos estáticos.
- No inicies hilos en constructores. Usa `I2PAppThread` en lugar de `Thread`.

### Registro

Las siguientes directrices se aplican al router, las aplicaciones web y todos los complementos.

- Para cualquier mensaje que no se muestre en el nivel de registro predeterminado (WARN, INFO y DEBUG), a menos que el mensaje sea una cadena estática (sin concatenación), use siempre `log.shouldWarn()`, `log.shouldInfo()` o `log.shouldDebug()` antes de la llamada de registro para evitar la creación innecesaria de objetos.
- Los mensajes de registro que puedan mostrarse en el nivel de registro predeterminado (ERROR, CRIT y `logAlways()`) deben ser breves, claros y comprensibles para un usuario no técnico. Esto incluye el texto de motivo de excepción que también puede mostrarse. Considere traducir si es probable que el error ocurra (por ejemplo, en errores de envío de formularios). De lo contrario, la traducción no es necesaria, pero puede ser útil buscar y reutilizar una cadena que ya esté marcada para traducción en otro lugar.
- Los mensajes de registro que no se muestran en el nivel de registro predeterminado (WARN, INFO y DEBUG) están destinados al uso del desarrollador y no tienen los requisitos anteriores. Sin embargo, los mensajes WARN están disponibles en la pestaña de registro de Android y pueden ayudar a los usuarios a depurar problemas, así que tenga cierto cuidado también con los mensajes WARN.
- Los mensajes de registro INFO y DEBUG deben usarse con moderación, especialmente en rutas de código críticas. Aunque son útiles durante el desarrollo, considere eliminarlos o comentarlos después de que se complete la prueba.
- No registre en stdout o stderr (registro del wrapper).

### Licencias

- Solo registra código que hayas escrito tú mismo. Antes de registrar cualquier código o JARs de bibliotecas de otras fuentes, justifica por qué es necesario, verifica que la licencia sea compatible y obtén la aprobación del gestor de lanzamientos.
- Si obtienes aprobación para añadir código externo o JARs, y hay binarios disponibles en cualquier paquete de Debian o Ubuntu, debes implementar opciones de compilación y empaquetado para usar el paquete externo en su lugar. Lista de verificación de archivos a modificar: `build.properties`, `build.xml`, `debian/control`, `debian/i2p-router.install`, `debian/i2p-router.links`, `debian/rules`, `sub-build.xml`.
- Para cualquier imagen registrada de fuentes externas, es tu responsabilidad verificar primero que la licencia sea compatible. Incluye la información de licencia y fuente en el comentario del registro.

### Errores

- Gestionar incidencias es trabajo de todos; por favor ayuda. Monitorea [GitLab](https://i2pgit.org/I2P_Developers/i2p.i2p/issues) para ver incidencias en las que puedas ayudar. Comenta, corrige y cierra incidencias si puedes.
- Los nuevos desarrolladores deben comenzar corrigiendo incidencias. Cuando tengas una corrección, adjunta tu parche a la incidencia y añade la palabra clave `review-needed`. No cierres la incidencia hasta que haya sido revisada exitosamente y hayas verificado tus cambios. Una vez que hayas hecho esto sin problemas para un par de tickets, puedes seguir el procedimiento normal descrito arriba.
- Cierra una incidencia cuando creas que la has corregido. No tenemos un departamento de pruebas para verificar y cerrar tickets. Si no estás seguro de haberla corregido, ciérrala y añade una nota diciendo "Creo que lo corregí, por favor prueba y reabre si sigue sin funcionar". Añade un comentario con el número de compilación de desarrollo o revisión y establece el milestone a la próxima versión.
