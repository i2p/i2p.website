---
title: "Notas de estado de I2P del 2004-08-24"
date: 2004-08-24
author: "jr"
description: "Actualización semanal del estado de I2P que abarca el lanzamiento 0.3.4.3, nuevas funciones de la consola del router, el progreso de 0.4 y varias mejoras"
categories: ["status"]
---

Hola a todos, muchas actualizaciones hoy

## Índice

1. 0.3.4.3 status
   1.1) timestamper
   1.2) new router console authentication
2. 0.4 status
   2.1) service & systray integration
   2.2) jbigi & jcpuid
   2.3) i2paddresshelper
3. AMOC vs. restricted routes
4. stasher
5. pages of note
6. ???

## 1) 0.3.4.3 estado

La versión 0.3.4.3 salió el viernes pasado y desde entonces las cosas han ido bastante bien. Ha habido algunos problemas con el código de pruebas de tunnel y de selección de pares recién introducido, pero tras algunos ajustes desde la publicación, es bastante sólido. No sé si el servidor IRC ya está en la nueva revisión, así que en general tenemos que basarnos en pruebas con eepsites(I2P Sites) y los proxies de salida http (squid.i2p y www1.squid.i2p). Las transferencias de archivos grandes (>5MB) en la versión 0.3.4.3 aún no son lo suficientemente fiables, pero en mis pruebas, las modificaciones desde entonces han mejorado aún más las cosas.

La red también ha estado creciendo: hoy más temprano alcanzamos 45 usuarios simultáneos y hemos estado consistentemente en el rango de 38-44 usuarios durante unos días (w00t)! Este es un número saludable por el momento, y he estado monitoreando la actividad general de la red para vigilar posibles peligros. Al pasar a la versión 0.4, vamos a querer aumentar gradualmente la base de usuarios hasta alrededor de la marca de 100 routers y realizar algunas pruebas más antes de seguir creciendo. Al menos, ese es mi objetivo desde la perspectiva de un desarrollador.

### 1.1) timestamper

Una de las cosas más geniales que cambió con la versión 0.3.4.3 y que se me olvidó por completo mencionar fue una actualización del código SNTP. Gracias a la generosidad de Adam Buckley, quien ha accedido a publicar su código SNTP bajo la licencia BSD, hemos fusionado la antigua aplicación Timestamper en el núcleo del I2P SDK y la hemos integrado por completo con nuestro reloj. Esto implica tres cosas: 1. puedes borrar el timestamper.jar (el código ahora está en i2p.jar) 2. puedes eliminar las líneas de clientApp relacionadas de tu configuración 3. puedes actualizar tu configuración para usar las nuevas opciones de sincronización de hora

Las nuevas opciones en el router.config son sencillas, y los valores predeterminados deberían ser suficientes (especialmente cierto, ya que la mayoría de ustedes las están usando involuntariamente :)

Para configurar la lista de servidores SNTP a consultar:

```
time.sntpServerList=pool.ntp.org,pool.ntp.org,pool.ntp.org
```
Para desactivar la sincronización de la hora (solo si eres un gurú de NTP y sabes que el reloj de tu sistema operativo está *siempre* correcto - ejecutar "windows time" NO es suficiente):

```
time.disabled=true
```
Ya no necesitas tener una 'timestamper password', ya que ahora todo está integrado directamente en el código (ah, las alegrías de BSD vs GPL :)

### 1.2) new router console authentication

Esto solo es relevante para quienes estén ejecutando la nueva consola del router, pero si la tienes escuchando en una interfaz pública, quizá quieras aprovechar la autenticación HTTP básica integrada. Sí, la autenticación HTTP básica es absurdamente débil: no te protegerá contra quien intercepte el tráfico de tu red o realice un ataque de fuerza bruta para entrar, pero mantendrá fuera al fisgón ocasional. De todos modos, para usarla, simplemente añade la línea

```
consolePassword=blah
```
a su router.config. Por desgracia, tendrá que reiniciar el router, ya que este parámetro se le pasa a Jetty solo una vez (durante el inicio).

## 2) 0.4 status

Estamos avanzando mucho con la versión 0.4, y esperamos publicar algunas versiones preliminares la próxima semana. Todavía estamos puliendo algunos detalles, así que aún no tenemos definido un proceso de actualización sólido. La versión será compatible con versiones anteriores, así que la actualización no debería ser demasiado dolorosa. De todos modos, permanezcan atentos y sabrán cuando todo esté listo.

### 1.1) generador de marcas de tiempo

Hypercubus está avanzando mucho en la integración del instalador, una aplicación para la bandeja del sistema y algo de código para la gestión de servicios. Básicamente, para la versión 0.4, todos los usuarios de Windows tendrán automáticamente un pequeño icono en la bandeja del sistema (¡Iggy!), aunque podrán desactivarlo (y/o volver a activarlo) a través de la consola web. Además, vamos a incluir el JavaService wrapper, que nos permitirá hacer todo tipo de cosas muy útiles, como ejecutar I2P al iniciar el sistema (o no), reinicio automático bajo ciertas condiciones, reinicio forzado de la JVM a demanda, generar trazas de pila y toda clase de otras ventajas.

### 1.2) nueva autenticación de la consola del router

Una de las grandes actualizaciones de la versión 0.4 será una renovación del código de jbigi, incorporando las modificaciones que Iakin hizo para Freenet, así como la nueva biblioteca nativa "jcpuid" de Iakin. La biblioteca jcpuid funciona únicamente en arquitecturas x86 y, junto con algo de código nuevo de jbigi, determinará cuál es el jbigi 'correcto' que se debe cargar. Por lo tanto, distribuiremos un único jbigi.jar que todos tendrán, y a partir de él se seleccionará el 'correcto' para la máquina actual. Por supuesto, aún podrás compilar tu propio jbigi nativo, anulando lo que jcpuid quiera (simplemente compílalo y cópialo en tu directorio de instalación de I2P, o ponle el nombre "jbigi" y colócalo en un archivo .jar en tu classpath). Sin embargo, debido a las actualizaciones, *no* es retrocompatible - al actualizar, debes o bien recompilar tu propio jbigi o eliminar tu biblioteca nativa existente (para permitir que el nuevo código de jcpuid elija el correcto).

### 2.3) i2paddresshelper

oOo ha creado una utilidad muy práctica para permitir que la gente navegue por eepsites(I2P Sites) sin actualizar su hosts.txt. Ya se ha incorporado a CVS y se desplegará en la próxima versión, pero quizá la gente quiera considerar actualizar los enlaces en consecuencia (cervantes ha actualizado el bbcode [i2p] de forum.i2p para admitirlo con un enlace "Try it [i2p]").

Básicamente, solo creas un enlace al eepsite(sitio de I2P) con el nombre que quieras, y luego le agregas un parámetro especial de URL que especifica el destino:

```
http://wowthisiscool.i2p/?i2paddresshelper=FpCkYW5pw...
```
Internamente, es bastante seguro - no puedes suplantar otra dirección, y el nombre *no* se guarda en hosts.txt, pero te permitirá ver imágenes / etc enlazadas en eepsites(Sitios I2P) que no podrías ver con el viejo truco `http://i2p/base64/`. Si quieres poder usar siempre "wowthisiscool.i2p" para acceder a ese sitio, aún, por supuesto, tendrás que añadir la entrada a tu hosts.txt (hasta que se distribuya el MyI2P address book, claro ;)

## 3) AMOC vs. restricted routes

Mule ha estado esbozando algunas ideas e instándome a explicar algunas cosas y, en el proceso, ha logrado avances para que reevalúe toda la idea de AMOC. En concreto, si eliminamos una de las restricciones que he impuesto a nuestra capa de transporte - permitiéndonos asumir bidireccionalidad -, podríamos desechar por completo el transporte AMOC y, en su lugar, implementar una operación básica de ruta restringida (dejando sentadas las bases para técnicas de ruta restringida más avanzadas, como pares confiables y router tunnels de varios saltos para más adelante).

Si optamos por esta vía, significaría que las personas podrían participar en la red detrás de cortafuegos, NAT, etc., sin necesidad de configuración, además de ofrecer algunas de las propiedades de anonimato de rutas restringidas. A su vez, probablemente implicaría una gran revisión de nuestra hoja de ruta, pero si podemos hacerlo de forma segura, nos ahorraría muchísimo tiempo y valdría mucho la pena el cambio.

Sin embargo, no queremos apresurarnos y necesitaremos revisar detenidamente las implicaciones de anonimato y de seguridad antes de adoptar ese camino. Lo haremos después de que 0.4 haya salido y esté funcionando sin problemas, así que no hay prisa.

## 2) estado de la versión 0.4

Se dice que aum está avanzando bien - no sé si estará en la reunión con una actualización, pero sí nos dejó un fragmento en #i2p esta mañana:

```
<aum> hi all, can't talk long, just a quick stasher update - work is
      continuing on implementing freenet keytypes, and freenet FCP
      compatibility - work in progress, should have a test build
      ready to try out by the end of the week
```
¡Genial!

## 5) pages of note

Solo quiero señalar dos recursos nuevos disponibles que los usuarios de I2P quizá quieran consultar: DrWoo ha preparado una página con un montón de información para personas que desean navegar de forma anónima, y Luckypunk ha publicado una guía práctica que describe sus experiencias con algunas JVMs (máquinas virtuales de Java) en FreeBSD. Hypercubus también publicó la documentación para probar el servicio y la integración con la bandeja del sistema aún no publicados.

## 6) ???

De acuerdo, eso es todo lo que tengo que decir por el momento - pásate por la reunión esta noche a las 21:00 GMT si quieres plantear algo más.

=jr
