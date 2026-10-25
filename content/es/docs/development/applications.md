---
title: "Desarrollo de Aplicaciones"
description: "Por qué escribir aplicaciones específicas para I2P, conceptos clave, opciones de desarrollo y una guía para comenzar"
slug: "applications"
aliases:
  - "/es/docs/develop/applications"
  - "/es/docs/develop/applications/"
  - "/es/applications"
  - "/es/applications/"
lastUpdated: "2013-05"
accurateFor: "0.9.6"
---

## ¿Por qué escribir código específico para I2P?

Hay múltiples formas de usar aplicaciones en I2P. Usando [I2PTunnel](/docs/api/i2ptunnel/), puedes usar aplicaciones regulares sin necesidad de programar soporte explícito para I2P. Esto es muy efectivo para escenarios cliente-servidor, donde necesitas conectarte a un solo sitio web. Simplemente puedes crear un tunnel usando I2PTunnel para conectarte a ese sitio web, como se muestra en la Figura 1.

Si tu aplicación está distribuida, requerirá conexiones a una gran cantidad de pares. Usando I2PTunnel, necesitarás crear un nuevo túnel para cada par que quieras contactar, como se muestra en la Figura 2. Este proceso puede por supuesto automatizarse, pero ejecutar muchas instancias de I2PTunnel crea una gran cantidad de sobrecarga. Además, con muchos protocolos necesitarás forzar a todos a usar el mismo conjunto de puertos para todos los pares — p. ej. si quieres ejecutar de manera confiable un chat DCC, todos deben acordar que el puerto 10001 es Alice, el puerto 10002 es Bob, el puerto 10003 es Charlie, y así sucesivamente, ya que el protocolo incluye información específica de TCP/IP (host y puerto).

Las aplicaciones de red generales a menudo envían gran cantidad de datos adicionales que podrían utilizarse para identificar a los usuarios. Nombres de host, números de puerto, zonas horarias, conjuntos de caracteres, etc. se envían frecuentemente sin informar al usuario. Por tanto, diseñar el protocolo de red específicamente con el anonimato en mente puede evitar comprometer las identidades de los usuarios.

También hay consideraciones de eficiencia que revisar al determinar cómo interactuar sobre I2P. La biblioteca de streaming y las cosas construidas sobre ella operan con handshakes similares a TCP, mientras que los protocolos principales de I2P (I2NP e I2CP) están estrictamente basados en mensajes (como UDP o en algunos casos IP sin procesar). La distinción importante es que con I2P, la comunicación está operando sobre una red larga y ancha — cada mensaje de extremo a extremo tendrá latencias no triviales, pero puede contener cargas útiles de hasta varios KB. Una aplicación que necesita una simple solicitud y respuesta puede deshacerse de cualquier estado y eliminar la latencia incurrida por los handshakes de inicio y cierre usando datagramas (de mejor esfuerzo) sin tener que preocuparse por la detección de MTU o fragmentación de mensajes.

![Crear una conexión servidor-cliente usando I2PTunnel solo requiere crear un único túnel.](/images/i2ptunnel_serverclient.png)

*Figura 1: Crear una conexión servidor-cliente usando I2PTunnel solo requiere crear un único túnel.*

![Configurar conexiones para aplicaciones peer-to-peer requiere una cantidad muy grande de túneles.](/images/i2ptunnel_peertopeer.png)

*Figura 2: Configurar conexiones para aplicaciones peer-to-peer requiere una cantidad muy grande de tunnels.*

En resumen, varias razones para escribir código específico para I2P:

- Crear una gran cantidad de instancias de I2PTunnel consume una cantidad considerable de recursos, lo cual es problemático para aplicaciones distribuidas (se requiere un nuevo tunnel para cada peer).
- Los protocolos de red generales a menudo envían muchos datos adicionales que pueden usarse para identificar usuarios. Programar específicamente para I2P permite la creación de un protocolo de red que no filtra dicha información, manteniendo a los usuarios anónimos y seguros.
- Los protocolos de red diseñados para uso en internet regular pueden ser ineficientes en I2P, que es una red con una latencia mucho mayor.

I2P soporta una [interfaz de plugins](/docs/specs/plugin/) estándar para desarrolladores para que las aplicaciones puedan ser fácilmente integradas y distribuidas.

Las aplicaciones escritas en Java y accesibles/ejecutables usando una interfaz HTML a través del webapps/app.war estándar pueden ser consideradas para su inclusión en la distribución de I2P.

---

## Conceptos Importantes

Hay algunos cambios que requieren adaptación al usar I2P:

### Destination ~= host+puerto

Una aplicación que se ejecuta en I2P envía mensajes desde y recibe mensajes hacia un punto final único y criptográficamente seguro — un "destination" (destino). En términos de TCP o UDP, un destination podría considerarse (en gran medida) el equivalente de un par de nombre de host más número de puerto, aunque hay algunas diferencias.

- Un destino I2P en sí mismo es una construcción criptográfica — todos los datos enviados a uno están cifrados como si hubiera un despliegue universal de IPsec con la ubicación (anonimizada) del punto final firmada como si hubiera un despliegue universal de DNSSEC.
- Los destinos I2P son identificadores móviles — pueden moverse de un router I2P a otro (o incluso pueden "multihome" — operar en múltiples routers a la vez). Esto es muy diferente del mundo TCP o UDP donde un solo punto final (puerto) debe permanecer en un solo host.
- Los destinos I2P son feos y grandes — tras bambalinas, contienen una clave pública ElGamal de 2048 bits para cifrado, una clave pública DSA de 1024 bits para firmar, y un certificado de tamaño variable, que puede contener prueba de trabajo o datos enmascarados.

Existen formas existentes de referirse a estos destinos grandes y feos mediante nombres cortos y bonitos (por ejemplo, "irc.duck.i2p"), pero esas técnicas no garantizan la unicidad global (ya que se almacenan localmente en una base de datos en la máquina de cada persona) y el mecanismo actual no es especialmente escalable ni seguro (las actualizaciones a la lista de hosts se gestionan usando "suscripciones" a servicios de nombres). Puede que algún día haya algún sistema de nombres seguro, legible para humanos, escalable y globalmente único, pero las aplicaciones no deberían depender de que esté implementado, ya que hay quienes no creen que tal bestia sea posible. [Más información sobre el sistema de nombres](/docs/overview/naming/) está disponible.

Aunque la mayoría de las aplicaciones no necesitan distinguir protocolos y puertos, I2P *sí* los admite. Las aplicaciones complejas pueden especificar un protocolo, puerto de origen y puerto de destino, por mensaje, para multiplexar tráfico en un solo destino. Consulta la [página de datagramas](/docs/api/datagrams/) para más detalles. Las aplicaciones simples funcionan escuchando "todos los protocolos" en "todos los puertos" de un destino.

### Anonimato y Confidencialidad

I2P tiene cifrado y autenticación transparente de extremo a extremo para todos los datos transmitidos a través de la red — si Bob envía al destino de Alice, solo el destino de Alice puede recibirlo, y si Bob está usando la biblioteca de datagramas o streaming, Alice sabe con certeza que el destino de Bob es quien envió los datos.

Por supuesto, I2P anonimiza de forma transparente los datos enviados entre Alice y Bob, pero no hace nada para anonimizar el contenido de lo que envían. Por ejemplo, si Alice le envía a Bob un formulario con su nombre completo, documentos de identidad gubernamentales y números de tarjetas de crédito, no hay nada que I2P pueda hacer. Por tanto, los protocolos y aplicaciones deben tener en cuenta qué información están tratando de proteger y qué información están dispuestos a exponer.

### Los datagramas I2P pueden tener hasta varios KB

Las aplicaciones que utilizan datagramas I2P (ya sean en bruto o respondibles) pueden pensarse esencialmente en términos de UDP — los datagramas están desordenados, son de mejor esfuerzo y sin conexión — pero a diferencia de UDP, las aplicaciones no necesitan preocuparse por la detección de MTU y pueden simplemente enviar datagramas grandes. Aunque el límite superior es nominalmente de 32 KB, el mensaje se fragmenta para el transporte, reduciendo así la confiabilidad del conjunto. Actualmente no se recomiendan datagramas de más de 10 KB aproximadamente. Consulta la [página de datagramas](/docs/api/datagrams/) para obtener detalles. Para muchas aplicaciones, 10 KB de datos son suficientes para una solicitud o respuesta completa, permitiéndoles operar de forma transparente en I2P como una aplicación similar a UDP sin tener que escribir fragmentación, reenvíos, etc.

---

## Opciones de Desarrollo

Existen varios métodos para enviar datos a través de I2P, cada uno con sus propias ventajas y desventajas. La biblioteca de streaming es la interfaz recomendada, utilizada por la mayoría de aplicaciones I2P.

### Biblioteca de Streaming

La [biblioteca de streaming completa](/docs/api/streaming/) es ahora la interfaz estándar. Permite programar usando sockets similares a TCP, como se explica en la [guía de desarrollo de Streaming](#developing-with-the-streaming-library).

### BOB

BOB es el [Basic Open Bridge](/docs/legacy/bob/), que permite a una aplicación en cualquier lenguaje establecer conexiones de streaming hacia y desde I2P. En este momento carece de soporte UDP, pero el soporte UDP está planeado en el futuro cercano. BOB también contiene varias herramientas, como la generación de claves de destino y la verificación de que una dirección cumple con las especificaciones de I2P. Información actualizada y aplicaciones que usan BOB se pueden encontrar en este [Sitio I2P](http://bob.i2p/).

### SAM, SAM V2, SAM V3

*SAM no es recomendado. SAM V2 está bien, SAM V3 es recomendado.*

SAM es el protocolo [Simple Anonymous Messaging](/docs/legacy/sam/), que permite a una aplicación escrita en cualquier lenguaje comunicarse con un puente SAM a través de un socket TCP simple y hacer que ese puente multiplexe todo su tráfico I2P, coordinando de manera transparente el cifrado/descifrado y el manejo basado en eventos. SAM soporta tres estilos de operación:

- streams, para cuando Alice y Bob quieren enviarse datos de manera confiable y en orden
- datagramas con respuesta, para cuando Alice quiere enviar a Bob un mensaje al que Bob puede responder
- datagramas sin procesar, para cuando Alice quiere aprovechar al máximo el ancho de banda y rendimiento posible, y a Bob no le importa si el remitente de los datos está autenticado o no (por ejemplo, los datos transferidos se autentican por sí mismos)

SAMv3 apunta al mismo objetivo que SAM y SAM V2, pero no requiere multiplexación/demultiplexación. Cada stream I2P es manejado por su propio socket entre la aplicación y el puente SAM. Además, los datagramas pueden ser enviados y recibidos por la aplicación a través de comunicaciones de datagrama con el puente SAM.

[SAM V2](/docs/legacy/samv2/) es una nueva versión utilizada por imule que corrige algunos de los problemas en [SAM](/docs/legacy/sam/).

[SAM V3](/docs/api/samv3/) es usado por imule desde la versión 1.4.0.

### I2PTunnel

La aplicación I2PTunnel permite a las aplicaciones construir túneles específicos similares a TCP hacia pares creando ya sea aplicaciones I2PTunnel 'cliente' (que escuchan en un puerto específico y se conectan a un destino I2P específico cada vez que se abre un socket a ese puerto) o aplicaciones I2PTunnel 'servidor' (que escuchan a un destino I2P específico y cada vez que reciben una nueva conexión I2P realizan un proxy saliente hacia un host/puerto TCP específico). Estos flujos son limpios de 8 bits y están autenticados y asegurados a través de la misma biblioteca de streaming que usa SAM, pero hay una sobrecarga no trivial involucrada en crear múltiples instancias únicas de I2PTunnel, ya que cada una tiene su propio destino I2P único y su propio conjunto de túneles, claves, etc.

### SOCKS

I2P es compatible con un proxy SOCKS V4 y V5. Las conexiones salientes funcionan bien. La funcionalidad entrante (servidor) y UDP puede estar incompleta y sin probar.

### Ministreaming

*Eliminado*

Solía haber una biblioteca simple de "ministreaming", pero ahora ministreaming.jar contiene solo las interfaces para la biblioteca completa de streaming.

### Datagramas

*Recomendado para aplicaciones similares a UDP*

La [biblioteca Datagram](/docs/api/datagrams/) permite enviar paquetes similares a UDP. Es posible usar:

- Datagramas replicables
- Datagramas sin procesar

### I2CP

*No recomendado*

[I2CP](/docs/specs/i2cp/) en sí mismo es un protocolo independiente del lenguaje, pero para implementar una biblioteca I2CP en algo que no sea Java hay una cantidad significativa de código que escribir (rutinas de cifrado, serialización de objetos, manejo de mensajes asíncronos, etc). Aunque alguien podría escribir una biblioteca I2CP en C o algo más, sería muy probablemente más útil usar la biblioteca SAM de C en su lugar.

### Aplicaciones Web

I2P viene con el servidor web Jetty, y configurarlo para usar el servidor Apache en su lugar es sencillo. Cualquier tecnología estándar de aplicaciones web debería funcionar.

---

## Comenzar a Desarrollar — Una Guía Simple

Desarrollar usando I2P requiere una instalación funcional de I2P y un entorno de desarrollo de tu elección. Si estás usando Java, puedes comenzar el desarrollo con la [biblioteca de streaming](#developing-with-the-streaming-library) o la biblioteca de datagramas. Usando otro lenguaje de programación, se puede usar SAM o BOB.

### Desarrollando con la Biblioteca de Streaming

El siguiente ejemplo muestra cómo crear aplicaciones cliente y servidor similares a TCP utilizando la biblioteca de streaming.

Esto requerirá las siguientes bibliotecas en tu classpath:

- `$I2P/lib/streaming.jar`: La biblioteca de streaming en sí
- `$I2P/lib/mstreaming.jar`: Factory e interfaces para la biblioteca de streaming
- `$I2P/lib/i2p.jar`: Clases estándar de I2P, estructuras de datos, API y utilidades

Puedes obtenerlos desde una instalación de I2P, o agregar las siguientes dependencias desde Maven Central:

- `net.i2p:i2p`
- `net.i2p.client:streaming`

La comunicación de red requiere el uso de sockets de red I2P. Para demostrar esto, crearemos una aplicación donde un cliente puede enviar mensajes de texto a un servidor, quien imprimirá los mensajes y los enviará de vuelta al cliente. En otras palabras, el servidor funcionará como un eco.

Comenzaremos inicializando la aplicación del servidor. Esto requiere obtener un I2PSocketManager y crear un I2PServerSocket. No proporcionaremos al I2PSocketManagerFactory las claves guardadas para un Destination existente, por lo que creará un nuevo Destination para nosotros. Entonces le pediremos al I2PSocketManager un I2PSession, para que podamos averiguar el Destination que fue creado, ya que necesitaremos copiar y pegar esa información más tarde para que el cliente pueda conectarse a nosotros.

```java
package i2p.echoserver;

import net.i2p.client.I2PSession;
import net.i2p.client.streaming.I2PServerSocket;
import net.i2p.client.streaming.I2PSocketManager;
import net.i2p.client.streaming.I2PSocketManagerFactory;

public class Main {

    public static void main(String[] args) {
        //Initialize application
        I2PSocketManager manager = I2PSocketManagerFactory.createManager();
        I2PServerSocket serverSocket = manager.getServerSocket();
        I2PSession session = manager.getSession();
        //Print the base64 string, the regular string would look like garbage.
        System.out.println(session.getMyDestination().toBase64());
        //The additional main method code comes here...
    }

}
```
*Ejemplo de código 1: inicializando la aplicación del servidor.*

Una vez que tenemos un I2PServerSocket, podemos crear instancias de I2PSocket para aceptar conexiones de clientes. En este ejemplo, crearemos una sola instancia de I2PSocket, que solo puede manejar un cliente a la vez. Un servidor real tendría que ser capaz de manejar múltiples clientes. Para hacer esto, tendrían que crearse múltiples instancias de I2PSocket, cada una en hilos separados. Una vez que hemos creado la instancia de I2PSocket, leemos datos, los imprimimos y los enviamos de vuelta al cliente.

```java
package i2p.echoserver;

import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.net.ConnectException;
import java.net.SocketTimeoutException;
import net.i2p.I2PException;
import net.i2p.client.streaming.I2PSocket;
import net.i2p.util.I2PThread;

import net.i2p.client.I2PSession;
import net.i2p.client.streaming.I2PServerSocket;
import net.i2p.client.streaming.I2PSocketManager;
import net.i2p.client.streaming.I2PSocketManagerFactory;

public class Main {

    public static void main(String[] args) {
        I2PSocketManager manager = I2PSocketManagerFactory.createManager();
        I2PServerSocket serverSocket = manager.getServerSocket();
        I2PSession session = manager.getSession();
        //Print the base64 string, the regular string would look like garbage.
        System.out.println(session.getMyDestination().toBase64());

        //Create socket to handle clients
        I2PThread t = new I2PThread(new ClientHandler(serverSocket));
        t.setName("clienthandler1");
        t.setDaemon(false);
        t.start();
    }

    private static class ClientHandler implements Runnable {

        public ClientHandler(I2PServerSocket socket) {
            this.socket = socket;
        }

        public void run() {
            while(true) {
                try {
                    I2PSocket sock = this.socket.accept();
                    if(sock != null) {
                        //Receive from clients
                        BufferedReader br = new BufferedReader(new InputStreamReader(sock.getInputStream()));
                        //Send to clients
                        BufferedWriter bw = new BufferedWriter(new OutputStreamWriter(sock.getOutputStream()));
                        String line = br.readLine();
                        if(line != null) {
                            System.out.println("Received from client: " + line);
                            bw.write(line);
                            bw.flush(); //Flush to make sure everything got sent
                        }
                        sock.close();
                    }
                } catch (I2PException ex) {
                    System.out.println("General I2P exception!");
                } catch (ConnectException ex) {
                    System.out.println("Error connecting!");
                } catch (SocketTimeoutException ex) {
                    System.out.println("Timeout!");
                } catch (IOException ex) {
                    System.out.println("General read/write-exception!");
                }
            }
        }

        private I2PServerSocket socket;

    }

}
```
*Ejemplo de código 2: aceptar conexiones de clientes y manejar mensajes.*

Cuando ejecutes el código del servidor anterior, debería imprimir algo como esto (pero sin los saltos de línea, debería ser solo un bloque enorme de caracteres):

```
y17s~L3H9q5xuIyyynyWahAuj6Jeg5VC~Klu9YPquQvD4vlgzmxn4yy~5Z0zVvKJiS2Lk
poPIcB3r9EbFYkz1mzzE3RYY~XFyPTaFQY8omDv49nltI2VCQ5cx7gAt~y4LdWqkyk3au
...
```
Esta es la representación en base64 del Destination del servidor. El cliente necesitará esta cadena para conectarse al servidor.

Ahora, crearemos la aplicación cliente. De nuevo, se requieren varios pasos para la inicialización. Una vez más, necesitaremos comenzar obteniendo un I2PSocketManager. No usaremos un I2PSession y un I2PServerSocket esta vez. En su lugar, usaremos la cadena Destination del servidor para iniciar nuestra conexión. Pediremos al usuario la cadena Destination, y crearemos un I2PSocket usando esta cadena. Una vez que tengamos un I2PSocket, podemos comenzar a enviar y recibir datos hacia y desde el servidor.

```java
package i2p.echoclient;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.InterruptedIOException;
import java.io.OutputStream;
import java.io.OutputStreamWriter;
import java.net.ConnectException;
import java.net.NoRouteToHostException;
import net.i2p.I2PException;
import net.i2p.client.streaming.I2PSocket;
import net.i2p.client.streaming.I2PSocketManager;
import net.i2p.client.streaming.I2PSocketManagerFactory;
import net.i2p.data.DataFormatException;
import net.i2p.data.Destination;

public class Main {

    public static void main(String[] args) {
        I2PSocketManager manager = I2PSocketManagerFactory.createManager();
        System.out.println("Please enter a Destination:");
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String destinationString;
        try {
            destinationString = br.readLine();
        } catch (IOException ex) {
            System.out.println("Failed to get a Destination string.");
            return;
        }
        Destination destination;
        try {
            destination = new Destination(destinationString);
        } catch (DataFormatException ex) {
            System.out.println("Destination string incorrectly formatted.");
            return;
        }
        I2PSocket socket;
        try {
            socket = manager.connect(destination);
        } catch (I2PException ex) {
            System.out.println("General I2P exception occurred!");
            return;
        } catch (ConnectException ex) {
            System.out.println("Failed to connect!");
            return;
        } catch (NoRouteToHostException ex) {
            System.out.println("Couldn't find host!");
            return;
        } catch (InterruptedIOException ex) {
            System.out.println("Sending/receiving was interrupted!");
            return;
        }
        try {
            //Write to server
            BufferedWriter bw = new BufferedWriter(new OutputStreamWriter(socket.getOutputStream()));
            bw.write("Hello I2P!\n");
            //Flush to make sure everything got sent
            bw.flush();
            //Read from server
            BufferedReader br2 = new BufferedReader(new InputStreamReader(socket.getInputStream()));
            String s = null;
            while ((s = br2.readLine()) != null) {
                System.out.println("Received from server: " + s);
            }
            socket.close();
        } catch (IOException ex) {
            System.out.println("Error occurred while sending/receiving!");
        }
    }

}
```
*Ejemplo de código 3: iniciando el cliente y conectándolo a la aplicación del servidor.*

Finalmente, puedes ejecutar tanto la aplicación servidor como la cliente. Primero, inicia la aplicación servidor. Imprimirá una cadena Destination (como se muestra arriba). A continuación, inicia la aplicación cliente. Cuando solicite una cadena Destination, puedes introducir la cadena impresa por el servidor. El cliente entonces enviará 'Hello I2P!' (junto con un salto de línea) al servidor, quien imprimirá el mensaje y lo enviará de vuelta al cliente.

¡Felicidades, te has comunicado exitosamente a través de I2P!

---

## Aplicaciones Existentes

Contáctanos si te gustaría contribuir.

- [I2P-Bote](http://i2pbote.i2p/) - contacta con HungryHobo
- [Syndie](http://syndie.i2p2.de/)
- [IMule](http://www.imule.i2p/)
- [I2Phex](http://forum.i2p/viewforum.php?f=25)

Consulta también todos los plugins en [plugins.i2p](http://plugins.i2p/), las aplicaciones y código fuente listados en [echelon.i2p](http://echelon.i2p/), y el código de aplicaciones alojado en [git.repo.i2p](http://git.repo.i2p/).

Consulta también las aplicaciones incluidas en la distribución de I2P: SusiMail e I2PSnark.

---

## Ideas de Aplicaciones

- Servidor NNTP - ha habido algunos en el pasado, ninguno en este momento
- Servidor Jabber - ha habido algunos en el pasado, y hay uno en este momento, con acceso a internet público
- Servidor de claves PGP y/o proxy
- Aplicaciones de distribución de contenido / DHT - resucitar feedspace, portar dijjer, buscar alternativas
- Ayudar con el desarrollo de [Syndie](http://syndie.i2p2.de/)
- Aplicaciones basadas en web - El cielo es el límite para alojar aplicaciones basadas en servidor web como blogs, pastebins, almacenamiento, seguimiento, feeds, etc. Cualquier tecnología web o CGI como Perl, PHP, Python, o Ruby funcionará.
- Resucitar algunas aplicaciones antiguas, varias previamente en el paquete fuente de i2p - bogobot, pants, proxyscript, q, stasher, socks proxy, i2ping, feedspace
