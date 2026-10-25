---
title: "Desenvolvimento de Aplicações"
description: "Por que escrever aplicativos específicos para I2P, conceitos-chave, opções de desenvolvimento e um guia para iniciantes"
slug: "applications"
aliases:
  - "/pt/docs/develop/applications"
  - "/pt/docs/develop/applications/"
  - "/pt/applications"
  - "/pt/applications/"
lastUpdated: "2013-05"
accurateFor: "0.9.6"
---

## Por que Escrever Código Específico para I2P?

Existem várias maneiras de usar aplicações no I2P. Usando [I2PTunnel](/docs/api/i2ptunnel/), você pode usar aplicações regulares sem precisar programar suporte explícito ao I2P. Isso é muito eficaz para cenários cliente-servidor, onde você precisa se conectar a um único website. Você pode simplesmente criar um tunnel usando I2PTunnel para se conectar a esse website, como mostrado na Figura 1.

Se sua aplicação for distribuída, ela exigirá conexões com uma grande quantidade de pares. Usando I2PTunnel, você precisará criar um novo tunnel para cada par que deseja contactar, como mostrado na Figura 2. Este processo pode, é claro, ser automatizado, mas executar muitas instâncias de I2PTunnel cria uma grande quantidade de overhead. Além disso, com muitos protocolos você precisará forçar todos a usar o mesmo conjunto de portas para todos os pares — por exemplo, se você quiser executar de forma confiável o chat DCC, todos precisam concordar que a porta 10001 é Alice, a porta 10002 é Bob, a porta 10003 é Charlie, e assim por diante, já que o protocolo inclui informações específicas do TCP/IP (host e porta).

Aplicações de rede gerais frequentemente enviam muitos dados adicionais que poderiam ser usados para identificar usuários. Nomes de host, números de porta, fusos horários, conjuntos de caracteres, etc. são frequentemente enviados sem informar o usuário. Assim sendo, projetar o protocolo de rede especificamente com anonimato em mente pode evitar comprometer as identidades dos usuários.

Também há considerações de eficiência a revisar ao determinar como interagir sobre o I2P. A biblioteca de streaming e as coisas construídas sobre ela operam com handshakes similares ao TCP, enquanto os protocolos principais do I2P (I2NP e I2CP) são estritamente baseados em mensagens (como UDP ou em algumas instâncias IP bruto). A distinção importante é que com I2P, a comunicação está operando sobre uma rede longa e gorda — cada mensagem de ponta a ponta terá latências não triviais, mas pode conter payloads de até vários KB. Uma aplicação que precisa de uma solicitação e resposta simples pode se livrar de qualquer estado e reduzir a latência incorrida pelos handshakes de inicialização e finalização usando datagramas (melhor esforço) sem ter que se preocupar com detecção de MTU ou fragmentação de mensagens.

![Criar uma conexão servidor-cliente usando I2PTunnel requer apenas criar um único túnel.](/images/i2ptunnel_serverclient.png)

*Figura 1: Criar uma conexão servidor-cliente usando I2PTunnel requer apenas a criação de um único tunnel.*

![Configurar conexões para aplicações peer-to-peer requer uma quantidade muito grande de tunnels.](/images/i2ptunnel_peertopeer.png)

*Figura 2: Configurar conexões para aplicações peer-to-peer requer uma quantidade muito grande de tunnels.*

Em resumo, várias razões para escrever código específico para I2P:

- Criar uma grande quantidade de instâncias I2PTunnel consome uma quantidade não trivial de recursos, o que é problemático para aplicações distribuídas (um novo tunnel é necessário para cada peer).
- Protocolos de rede gerais frequentemente enviam muitos dados adicionais que podem ser usados para identificar usuários. Programar especificamente para I2P permite a criação de um protocolo de rede que não vaza tais informações, mantendo os usuários anônimos e seguros.
- Protocolos de rede projetados para uso na internet regular podem ser ineficientes no I2P, que é uma rede com latência muito mais alta.

O I2P suporta uma [interface de plugins](/docs/specs/plugin/) padrão para desenvolvedores, de modo que as aplicações possam ser facilmente integradas e distribuídas.

Aplicações escritas em Java e acessíveis/executáveis usando uma interface HTML via o webapps/app.war padrão podem ser consideradas para inclusão na distribuição I2P.

---

## Conceitos Importantes

Existem algumas mudanças que requerem adaptação ao usar o I2P:

### Destination ~= host+porta

Uma aplicação executando no I2P envia mensagens de e recebe mensagens para um ponto final único e criptograficamente seguro — um "destination". Em termos de TCP ou UDP, um destination poderia (em grande parte) ser considerado o equivalente de um par de nome de host mais número de porta, embora existam algumas diferenças.

- Um I2P destination em si é uma construção criptográfica — todos os dados enviados para um são criptografados como se houvesse uma implantação universal de IPsec com a localização (anonimizada) do ponto final assinada como se houvesse uma implantação universal de DNSSEC.
- I2P destinations são identificadores móveis — eles podem ser movidos de um I2P router para outro (ou podem até mesmo ter "multihome" — operar em múltiplos routers simultaneamente). Isso é bem diferente do mundo TCP ou UDP onde um único ponto final (porta) deve permanecer em um único host.
- I2P destinations são feios e grandes — por trás dos panos, eles contêm uma chave pública ElGamal de 2048 bits para criptografia, uma chave pública DSA de 1024 bits para assinatura, e um certificado de tamanho variável, que pode conter prova de trabalho ou dados ofuscados.

Existem maneiras de se referir a esses destinos grandes e feios por nomes curtos e bonitos (por exemplo, "irc.duck.i2p"), mas essas técnicas não garantem unicidade global (já que são armazenados localmente em uma base de dados na máquina de cada pessoa) e o mecanismo atual não é especialmente escalável nem seguro (atualizações da lista de hosts são gerenciadas usando "subscrições" a serviços de nomeação). Pode haver algum sistema de nomeação seguro, legível por humanos, escalável e globalmente único algum dia, mas as aplicações não devem depender de ele estar implementado, já que há aqueles que não acreditam que tal coisa seja possível. [Mais informações sobre o sistema de nomeação](/docs/overview/naming/) estão disponíveis.

Embora a maioria das aplicações não precise distinguir protocolos e portas, o I2P *oferece* suporte a eles. Aplicações complexas podem especificar um protocolo, porta de origem e porta de destino, por mensagem, para multiplexar tráfego em um único destino. Consulte a [página de datagramas](/docs/api/datagrams/) para detalhes. Aplicações simples operam escutando "todos os protocolos" em "todas as portas" de um destino.

### Anonimato e Confidencialidade

O I2P tem criptografia e autenticação transparentes de ponta a ponta para todos os dados transmitidos pela rede — se Bob enviar para o destino de Alice, apenas o destino de Alice pode recebê-los, e se Bob estiver usando a biblioteca de datagramas ou streaming, Alice tem certeza de que o destino de Bob é quem enviou os dados.

Naturalmente, o I2P anonimiza de forma transparente os dados enviados entre Alice e Bob, mas não faz nada para anonimizar o conteúdo do que eles enviam. Por exemplo, se Alice enviar para Bob um formulário com seu nome completo, documentos de identidade do governo e números de cartão de crédito, não há nada que o I2P possa fazer. Assim sendo, protocolos e aplicações devem ter em mente quais informações estão tentando proteger e quais informações estão dispostos a expor.

### Datagramas I2P Podem Ter Até Vários KB

Aplicações que usam datagramas I2P (sejam brutos ou respondíveis) podem essencialmente ser pensadas em termos de UDP — os datagramas são desordenados, de melhor esforço e sem conexão — mas ao contrário do UDP, as aplicações não precisam se preocupar com detecção de MTU e podem simplesmente enviar datagramas grandes. Embora o limite superior seja nominalmente de 32 KB, a mensagem é fragmentada para transporte, reduzindo assim a confiabilidade do conjunto. Datagramas acima de cerca de 10 KB não são recomendados atualmente. Consulte a [página de datagramas](/docs/api/datagrams/) para detalhes. Para muitas aplicações, 10 KB de dados são suficientes para uma solicitação ou resposta inteira, permitindo que operem transparentemente no I2P como uma aplicação similar ao UDP sem ter que implementar fragmentação, reenvios, etc.

---

## Opções de Desenvolvimento

Existem várias formas de enviar dados através do I2P, cada uma com suas próprias vantagens e desvantagens. A streaming lib é a interface recomendada, utilizada pela maioria das aplicações I2P.

### Biblioteca de Streaming

A [biblioteca de streaming completa](/docs/api/streaming/) é agora a interface padrão. Ela permite programar usando sockets semelhantes ao TCP, como explicado no [guia de desenvolvimento de Streaming](#developing-with-the-streaming-library).

### BOB

BOB é a [Basic Open Bridge](/docs/legacy/bob/), permitindo que uma aplicação em qualquer linguagem faça conexões de streaming para e do I2P. Neste momento não possui suporte UDP, mas o suporte UDP está planejado para o futuro próximo. BOB também contém várias ferramentas, como geração de chaves de destino e verificação de que um endereço está em conformidade com as especificações do I2P. Informações atualizadas e aplicações que usam BOB podem ser encontradas neste [Site I2P](http://bob.i2p/).

### SAM, SAM V2, SAM V3

*SAM não é recomendado. SAM V2 é aceitável, SAM V3 é recomendado.*

SAM é o protocolo [Simple Anonymous Messaging](/docs/legacy/sam/) (Mensagens Anônimas Simples), que permite que uma aplicação escrita em qualquer linguagem se comunique com uma ponte SAM através de um socket TCP simples e tenha essa ponte multiplexando todo o seu tráfego I2P, coordenando de forma transparente a criptografia/descriptografia e o manuseio baseado em eventos. SAM suporta três estilos de operação:

- streams, para quando Alice e Bob querem enviar dados um ao outro de forma confiável e em ordem
- datagrams respondíveis, para quando Alice quer enviar uma mensagem para Bob que Bob pode responder
- datagrams brutos, para quando Alice quer obter o máximo de largura de banda e desempenho possível, e Bob não se importa se o remetente dos dados é autenticado ou não (por exemplo, os dados transferidos são auto-autenticantes)

O SAM V3 tem o mesmo objetivo que o SAM e SAM V2, mas não requer multiplexação/demultiplexação. Cada stream I2P é gerenciado por seu próprio socket entre a aplicação e a ponte SAM. Além disso, datagramas podem ser enviados e recebidos pela aplicação através de comunicações de datagrama com a ponte SAM.

[SAM V2](/docs/legacy/samv2/) é uma nova versão usada pelo imule que corrige alguns dos problemas no [SAM](/docs/legacy/sam/).

[SAM V3](/docs/api/samv3/) é usado pelo imule desde a versão 1.4.0.

### I2PTunnel

A aplicação I2PTunnel permite que aplicações construam tunnels específicos similares ao TCP para peers criando aplicações I2PTunnel 'cliente' (que escutam numa porta específica e conectam a um destino I2P específico sempre que um socket para essa porta é aberto) ou aplicações I2PTunnel 'servidor' (que escutam num destino I2P específico e sempre que recebem uma nova conexão I2P fazem outproxy para um host/porta TCP específico). Estes streams são 8-bit clean, e são autenticados e protegidos através da mesma biblioteca de streaming que o SAMv3 usa, mas há uma sobrecarga não trivial envolvida na criação de múltiplas instâncias I2PTunnel únicas, já que cada uma tem seu próprio destino I2P único e seu próprio conjunto de tunnels, chaves, etc.

### SOCKS

O I2P suporta um proxy SOCKS V4 e V5. As conexões de saída funcionam bem. As funcionalidades de entrada (servidor) e UDP podem estar incompletas e não testadas.

### Ministreaming

*Removido*

Costumava haver uma biblioteca simples de "ministreaming", mas agora o ministreaming.jar contém apenas as interfaces para a biblioteca completa de streaming.

### Datagramas

*Recomendado para aplicações do tipo UDP*

A [biblioteca Datagram](/docs/api/datagrams/) permite enviar pacotes similares a UDP. É possível usar:

- Datagramas replicáveis
- Datagramas brutos

### I2CP

*Não recomendado*

O [I2CP](/docs/specs/i2cp/) em si é um protocolo independente de linguagem, mas para implementar uma biblioteca I2CP em algo diferente de Java há uma quantidade significativa de código a ser escrito (rotinas de criptografia, marshalling de objetos, tratamento assíncrono de mensagens, etc). Embora alguém pudesse escrever uma biblioteca I2CP em C ou outra linguagem, provavelmente seria mais útil usar a biblioteca SAM em C.

### Aplicações Web

O I2P vem com o servidor web Jetty, e configurá-lo para usar o servidor Apache em vez disso é simples. Qualquer tecnologia padrão de aplicação web deve funcionar.

---

## Comece a Desenvolver — Um Guia Simples

Desenvolver usando I2P requer uma instalação funcional do I2P e um ambiente de desenvolvimento de sua escolha. Se você estiver usando Java, pode começar o desenvolvimento com a [biblioteca de streaming](#developing-with-the-streaming-library) ou biblioteca de datagramas. Usando outra linguagem de programação, SAM ou BOB podem ser usados.

### Desenvolvendo com a Biblioteca Streaming

O exemplo a seguir mostra como criar aplicações cliente e servidor semelhantes ao TCP usando a biblioteca de streaming.

Isso exigirá as seguintes bibliotecas no seu classpath:

- `$I2P/lib/streaming.jar`: A própria biblioteca de streaming
- `$I2P/lib/mstreaming.jar`: Factory e interfaces para a biblioteca de streaming
- `$I2P/lib/i2p.jar`: Classes padrão do I2P, estruturas de dados, API e utilitários

Você pode obtê-los de uma instalação do I2P, ou adicionar as seguintes dependências do Maven Central:

- `net.i2p:i2p`
- `net.i2p.client:streaming`

A comunicação de rede requer o uso de sockets de rede I2P. Para demonstrar isso, vamos criar uma aplicação onde um cliente pode enviar mensagens de texto para um servidor, que irá imprimir as mensagens e enviá-las de volta para o cliente. Em outras palavras, o servidor funcionará como um eco.

Começaremos inicializando a aplicação do servidor. Isso requer obter um I2PSocketManager e criar um I2PServerSocket. Não forneceremos ao I2PSocketManagerFactory as chaves salvas para um Destination existente, então ele criará um novo Destination para nós. Assim, pediremos ao I2PSocketManager um I2PSession, para que possamos descobrir o Destination que foi criado, pois precisaremos copiar e colar essa informação mais tarde para que o cliente possa se conectar a nós.

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
*Exemplo de código 1: inicializando a aplicação do servidor.*

Uma vez que temos um I2PServerSocket, podemos criar instâncias de I2PSocket para aceitar conexões de clientes. Neste exemplo, criaremos uma única instância de I2PSocket, que só pode lidar com um cliente por vez. Um servidor real teria que ser capaz de lidar com múltiplos clientes. Para fazer isso, múltiplas instâncias de I2PSocket teriam que ser criadas, cada uma em threads separadas. Uma vez que criamos a instância de I2PSocket, lemos os dados, imprimimos e os enviamos de volta para o cliente.

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
*Exemplo de código 2: aceitando conexões de clientes e tratando mensagens.*

Quando você executa o código do servidor acima, ele deve imprimir algo assim (mas sem as quebras de linha, deve ser apenas um bloco enorme de caracteres):

```
y17s~L3H9q5xuIyyynyWahAuj6Jeg5VC~Klu9YPquQvD4vlgzmxn4yy~5Z0zVvKJiS2Lk
poPIcB3r9EbFYkz1mzzE3RYY~XFyPTaFQY8omDv49nltI2VCQ5cx7gAt~y4LdWqkyk3au
...
```
Esta é a representação em base64 do Destination do servidor. O cliente precisará desta string para alcançar o servidor.

Agora, vamos criar a aplicação cliente. Novamente, várias etapas são necessárias para a inicialização. Novamente, precisaremos começar obtendo um I2PSocketManager. Não usaremos um I2PSession e um I2PServerSocket desta vez. Em vez disso, usaremos a string de Destination do servidor para iniciar nossa conexão. Pediremos ao usuário a string de Destination e criaremos um I2PSocket usando esta string. Uma vez que tenhamos um I2PSocket, podemos começar a enviar e receber dados de e para o servidor.

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
*Exemplo de código 3: iniciando o cliente e conectando-o à aplicação do servidor.*

Por fim, você pode executar tanto a aplicação servidor quanto a cliente. Primeiro, inicie a aplicação servidor. Ela irá imprimir uma string de Destination (como mostrado acima). Em seguida, inicie a aplicação cliente. Quando ela solicitar uma string de Destination, você pode inserir a string impressa pelo servidor. O cliente então enviará 'Hello I2P!' (junto com uma quebra de linha) para o servidor, que imprimirá a mensagem e a enviará de volta para o cliente.

Parabéns, você se comunicou com sucesso através do I2P!

---

## Aplicações Existentes

Entre em contato conosco se você gostaria de contribuir.

- [I2P-Bote](http://i2pbote.i2p/) - contactar HungryHobo
- [Syndie](http://syndie.i2p2.de/)
- [IMule](http://www.imule.i2p/)
- [I2Phex](http://forum.i2p/viewforum.php?f=25)

Veja também todos os plugins em [plugins.i2p](http://plugins.i2p/), as aplicações e código fonte listados em [echelon.i2p](http://echelon.i2p/), e o código de aplicações hospedado em [git.repo.i2p](http://git.repo.i2p/).

Veja também as aplicações incluídas na distribuição I2P - SusiMail e I2PSnark.

---

## Ideias de Aplicações

- Servidor NNTP - houve alguns no passado, nenhum no momento
- Servidor Jabber - houve alguns no passado, e há um no momento, com acesso à internet pública
- Servidor de chaves PGP e/ou proxy
- Aplicações de Distribuição de Conteúdo / DHT - ressuscitar feedspace, portar dijjer, procurar alternativas
- Ajudar com o desenvolvimento do [Syndie](http://syndie.i2p2.de/)
- Aplicações baseadas na web - O céu é o limite para hospedar aplicações baseadas em servidor web como blogs, pastebins, armazenamento, rastreamento, feeds, etc. Qualquer tecnologia web ou CGI como Perl, PHP, Python ou Ruby funcionará.
- Ressuscitar algumas aplicações antigas, várias anteriormente no pacote fonte do i2p - bogobot, pants, proxyscript, q, stasher, socks proxy, i2ping, feedspace
