---
title: "Desarrollo de Aplicaciones"
description: "Por qué escribir aplicaciones específicas para I2P, conceptos clave, opciones de desarrollo y una guía simple para comenzar"
slug: "applications"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
type: docs
---

## ¿Por qué escribir código específico para I2P?

Existen múltiples formas de utilizar aplicaciones en I2P. Usando [I2PTunnel](/docs/api/i2ptunnel/), puedes usar aplicaciones regulares sin necesidad de programar soporte explícito para I2P. Esto es muy efectivo para escenarios cliente-servidor, donde necesitas conectarte a un único sitio web. Simplemente puedes crear un tunnel usando I2PTunnel para conectarte a ese sitio web, como se muestra en la Figura 1.

Si tu aplicación está distribuida, requerirá conexiones a una gran cantidad de pares. Usando I2PTunnel, necesitarás crear un nuevo túnel para cada par con el que quieras contactar, como se muestra en la Figura 2. Este proceso puede, por supuesto, automatizarse, pero ejecutar muchas instancias de I2PTunnel crea una gran cantidad de sobrecarga. Además, con muchos protocolos necesitarás forzar a todos a usar el mismo conjunto de puertos para todos los pares — por ejemplo, si quieres ejecutar de manera confiable chat DCC, todos deben acordar que el puerto 10001 es Alice, el puerto 10002 es Bob, el puerto 10003 es Charlie, y así sucesivamente, ya que el protocolo incluye información específica de TCP/IP (host y puerto).

Las aplicaciones de red generales a menudo envían una gran cantidad de datos adicionales que podrían utilizarse para identificar usuarios. Los nombres de host, números de puerto, zonas horarias, conjuntos de caracteres, etc., se envían frecuentemente sin informar al usuario. Por lo tanto, diseñar el protocolo de red específicamente con el anonimato en mente puede evitar comprometer las identidades de los usuarios.

También hay consideraciones de eficiencia que revisar al determinar cómo interactuar sobre I2P. La biblioteca streaming y las cosas construidas sobre ella operan con handshakes similares a TCP, mientras que los protocolos centrales de I2P (I2NP e I2CP) son estrictamente basados en mensajes (como UDP o en algunos casos IP sin procesar). La distinción importante es que con I2P, la comunicación opera sobre una red larga y ancha (long fat network) — cada mensaje de extremo a extremo tendrá latencias no triviales, pero puede contener cargas útiles de hasta varios KB. Una aplicación que necesita una simple solicitud y respuesta puede deshacerse de cualquier estado y eliminar la latencia incurrida por los handshakes de inicio y cierre usando datagramas (mejor esfuerzo) sin tener que preocuparse por la detección de MTU o fragmentación de mensajes.

<figure style="text-align:center; margin: 2rem 0;">
  <img src="/images/i2ptunnel_serverclient.png" alt="Creating a server-client connection using I2PTunnel only requires creating a single tunnel." />
  <figcaption>Figure 1: Creating a server-client connection using I2PTunnel only requires creating a single tunnel.</figcaption>
</figure>
<figure style="text-align:center; margin: 2rem 0;">
  <img src="/images/i2ptunnel_peertopeer.png" alt="Setting up connections for a peer-to-peer applications requires a very large amount of tunnels." />
  <figcaption>Figure 2: Setting up connections for a peer-to-peer applications requires a very large amount of tunnels.</figcaption>
</figure>
En resumen, varias razones para escribir código específico para I2P:

- Crear una gran cantidad de instancias de I2PTunnel consume una cantidad no trivial de recursos, lo cual es problemático para aplicaciones distribuidas (se requiere un nuevo tunnel para cada par).
- Los protocolos de red generales a menudo envían muchos datos adicionales que pueden usarse para identificar usuarios. Programar específicamente para I2P permite la creación de un protocolo de red que no filtra dicha información, manteniendo a los usuarios anónimos y seguros.
- Los protocolos de red diseñados para uso en internet regular pueden ser ineficientes en I2P, que es una red con una latencia mucho mayor.

I2P soporta una [interfaz de plugins](/docs/plugins/) estándar para desarrolladores, de modo que las aplicaciones puedan integrarse y distribuirse fácilmente.

Las aplicaciones escritas en Java y accesibles/ejecutables mediante una interfaz HTML a través del estándar webapps/app.war pueden ser consideradas para su inclusión en la distribución de I2P.

## Conceptos Importantes

Hay algunos cambios que requieren adaptación al usar I2P:

### Destinos

Una aplicación ejecutándose en I2P envía mensajes desde y recibe mensajes hacia un punto final único criptográficamente seguro — un "destination". En términos de TCP o UDP, un destination podría (en gran medida) considerarse el equivalente a un par de nombre de host más número de puerto, aunque existen algunas diferencias.

- Un destino I2P en sí mismo es una construcción criptográfica: todos los datos enviados a uno están cifrados como si hubiera un despliegue universal de IPsec con la ubicación (anonimizada) del punto final firmada como si hubiera un despliegue universal de DNSSEC.
- Los destinos I2P son identificadores móviles: pueden moverse de un router I2P a otro (o incluso pueden hacer "multihome", operar en múltiples routers a la vez). Esto es muy diferente del mundo TCP o UDP donde un único punto final (puerto) debe permanecer en un solo host.
- Los destinos I2P son feos y grandes: entre bastidores, contienen una clave pública ElGamal de 2048 bits para cifrado, una clave pública DSA de 1024 bits para firma, y un certificado de tamaño variable, que puede contener prueba de trabajo o datos ofuscados.

Existen formas de referirse a estos destinos grandes y complejos mediante nombres cortos y amigables (por ejemplo, "irc.duck.i2p"), pero estas técnicas no garantizan la unicidad global (ya que se almacenan localmente en una base de datos en la máquina de cada persona) y el mecanismo actual no es especialmente escalable ni seguro (las actualizaciones de la lista de hosts se gestionan mediante "suscripciones" a servicios de nombres). Puede que algún día exista un sistema de nombres seguro, legible para humanos, escalable y globalmente único, pero las aplicaciones no deberían depender de que esté implementado. Hay disponible [más información sobre el sistema de nombres](/docs/overview/naming/).

Aunque la mayoría de las aplicaciones no necesitan distinguir protocolos y puertos, I2P *sí* los soporta. Las aplicaciones complejas pueden especificar un protocolo, puerto de origen y puerto de destino, mensaje por mensaje, para multiplexar el tráfico en un único destino. Consulta la [página de datagramas](/docs/api/datagrams/) para más detalles. Las aplicaciones simples operan escuchando "todos los protocolos" en "todos los puertos" de un destino.

### Anonimato y Confidencialidad

I2P tiene cifrado de extremo a extremo y autenticación transparentes para todos los datos transmitidos a través de la red — si Bob envía datos al destino de Alice, solo el destino de Alice puede recibirlos, y si Bob está usando la biblioteca de datagramas o streaming, Alice tiene la certeza de que el destino de Bob es quien envió los datos.

Por supuesto, I2P anonimiza de forma transparente los datos enviados entre Alice y Bob, pero no hace nada para anonimizar el contenido de lo que envían. Por ejemplo, si Alice envía a Bob un formulario con su nombre completo, documentos de identidad gubernamentales y números de tarjetas de crédito, no hay nada que I2P pueda hacer. Por lo tanto, los protocolos y aplicaciones deben tener en cuenta qué información están tratando de proteger y qué información están dispuestos a exponer.

### Los datagramas I2P pueden tener hasta varios KB

Las aplicaciones que utilizan datagramas I2P (ya sean crudos o respondibles) pueden concebirse esencialmente en términos de UDP — los datagramas no están ordenados, son de mejor esfuerzo y sin conexión — pero a diferencia de UDP, las aplicaciones no necesitan preocuparse por la detección de MTU y pueden simplemente enviar datagramas grandes. Aunque el límite superior es nominalmente de 32 KB, el mensaje se fragmenta para el transporte, lo que reduce la fiabilidad del conjunto. Actualmente no se recomiendan datagramas de más de 10 KB aproximadamente. Consulta la [página de datagramas](/docs/api/datagrams/) para más detalles. Para muchas aplicaciones, 10 KB de datos son suficientes para una solicitud o respuesta completa, permitiéndoles operar de forma transparente en I2P como una aplicación similar a UDP sin tener que implementar fragmentación, reenvíos, etc.

## Opciones de Desarrollo

Existen varios medios para enviar datos a través de I2P, cada uno con sus propias ventajas y desventajas. La biblioteca streaming lib es la interfaz recomendada, utilizada por la mayoría de las aplicaciones I2P.

### Biblioteca de Streaming

La [biblioteca completa de streaming](/docs/specs/streaming/) es ahora la interfaz estándar. Permite programar usando sockets similares a TCP, como se explica en la [guía de desarrollo de Streaming](#developing-with-the-streaming-library).

### BOB

BOB es el [Basic Open Bridge](/docs/legacy/bob/), que permite a una aplicación en cualquier lenguaje establecer conexiones de streaming hacia y desde I2P. En este momento carece de soporte UDP, pero el soporte UDP está planificado para un futuro cercano. BOB también contiene varias herramientas, como generación de claves de destino y verificación de que una dirección cumple con las especificaciones de I2P. Información actualizada y aplicaciones que usan BOB se pueden encontrar en este [Sitio I2P](http://bob.i2p/).

### SAM, SAM V2, SAM V3

*SAM no es recomendado. SAM V2 está bien, SAM V3 es recomendado.*

SAM es el protocolo [Simple Anonymous Messaging](/docs/legacy/sam/) (Mensajería Anónima Simple), que permite que una aplicación escrita en cualquier lenguaje se comunique con un puente SAM a través de un socket TCP simple y que ese puente multiplexe todo su tráfico I2P, coordinando de forma transparente el cifrado/descifrado y el manejo basado en eventos. SAM admite tres estilos de operación:

- streams, para cuando Alice y Bob quieren enviarse datos de manera confiable y en orden
- repliable datagrams, para cuando Alice quiere enviar a Bob un mensaje al que Bob puede responder
- raw datagrams, para cuando Alice quiere aprovechar el máximo ancho de banda y rendimiento posible, y a Bob no le importa si el remitente de los datos está autenticado o no (por ejemplo, los datos transferidos se autoautentican)

SAMv3 apunta al mismo objetivo que SAM y SAM V2, pero no requiere multiplexación/demultiplexación. Cada stream I2P es manejado por su propio socket entre la aplicación y el puente SAM. Además, los datagramas pueden ser enviados y recibidos por la aplicación a través de comunicaciones de datagramas con el puente SAM.

[SAM V2](/docs/legacy/samv2/) es una nueva versión utilizada por imule que soluciona algunos de los problemas en [SAM](/docs/legacy/sam/).

[SAM V3](/docs/api/samv3/) es utilizado por imule desde la versión 1.4.0.

### I2PTunnel

La aplicación I2PTunnel permite a las aplicaciones construir túneles específicos similares a TCP hacia pares creando aplicaciones I2PTunnel 'cliente' (que escuchan en un puerto específico y se conectan a un destino I2P específico cada vez que se abre un socket hacia ese puerto) o aplicaciones I2PTunnel 'servidor' (que escuchan en un destino I2P específico y cada vez que reciben una nueva conexión I2P hacen outproxy hacia un host/puerto TCP específico). Estos flujos son limpios de 8 bits, y están autenticados y asegurados mediante la misma biblioteca de streaming que usa SAM, pero existe una sobrecarga no trivial involucrada al crear múltiples instancias únicas de I2PTunnel, ya que cada una tiene su propio destino I2P único y su propio conjunto de túneles, claves, etc.

### SOCKS

I2P admite un proxy SOCKS V4 y V5. Las conexiones salientes funcionan bien. La funcionalidad entrante (servidor) y UDP puede estar incompleta y sin probar.

### Ministreaming

*Eliminado*

Solía haber una biblioteca simple de "ministreaming", pero ahora ministreaming.jar contiene solo las interfaces para la biblioteca de streaming completa.

### Datagramas

*Recomendado para aplicaciones tipo UDP*

La [biblioteca Datagram](/docs/api/datagrams/) permite enviar paquetes tipo UDP. Es posible usar:

- Datagramas replicables
- Datagramas sin procesar

### I2CP

*No recomendado*

[I2CP](/docs/specs/i2cp/) en sí es un protocolo independiente del lenguaje, pero para implementar una biblioteca I2CP en algo que no sea Java hay una cantidad significativa de código que escribir (rutinas de cifrado, serialización de objetos, manejo de mensajes asíncronos, etc.). Si bien alguien podría escribir una biblioteca I2CP en C o en algún otro lenguaje, probablemente sería más útil usar la biblioteca SAM de C en su lugar.

### Aplicaciones Web

I2P viene con el servidor web Jetty, y configurarlo para usar el servidor Apache en su lugar es sencillo. Cualquier tecnología de aplicación web estándar debería funcionar.

## Comenzar a Desarrollar — Una Guía Simple

Desarrollar usando I2P requiere una instalación funcional de I2P y un entorno de desarrollo de su elección. Si está usando Java, puede comenzar el desarrollo con la [biblioteca streaming](#developing-with-the-streaming-library) o la biblioteca de datagramas. Usando otro lenguaje de programación, se puede utilizar SAM o BOB.

### Desarrollo con la biblioteca de Streaming

A continuación se presenta una versión recortada y modernizada del ejemplo de la página original. Para el ejemplo completo, consulte la página legacy o nuestros ejemplos de Java en el código base.

```java
// Server example (excerpt)
I2PSocketManager manager = I2PSocketManagerFactory.createManager();
I2PServerSocket server = manager.getServerSocket();
I2PSocket socket = server.accept();
BufferedReader br = new BufferedReader(new InputStreamReader(socket.getInputStream()));
String s;
while ((s = br.readLine()) != null) {
    System.out.println("Received: " + s);
}
```
*Ejemplo de código: servidor básico recibiendo datos.*

```java
// Client example (excerpt)
I2PSocketManager manager = I2PSocketManagerFactory.createManager();
Destination dest = new Destination(serverDestBase64);
I2PSocket socket = manager.connect(dest);
BufferedWriter bw = new BufferedWriter(new OutputStreamWriter(socket.getOutputStream()));
bw.write("Hello I2P!\n");
bw.flush();
```
*Ejemplo de código: cliente conectándose y enviando una línea.*
