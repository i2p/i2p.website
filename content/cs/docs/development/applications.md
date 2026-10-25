---
title: "Vývoj aplikací"
description: "Proč psát aplikace specifické pro I2P, klíčové koncepty, možnosti vývoje a průvodce pro začátečníky"
slug: "applications"
aliases:
  - "/cs/docs/develop/applications"
  - "/cs/docs/develop/applications/"
  - "/cs/applications"
  - "/cs/applications/"
lastUpdated: "2013-05"
accurateFor: "0.9.6"
---

## Proč psát kód specifický pro I2P?

Existuje několik způsobů, jak používat aplikace v I2P. Pomocí [I2PTunnel](/docs/api/i2ptunnel/) můžete používat běžné aplikace, aniž byste museli programovat explicitní podporu I2P. To je velmi efektivní pro scénáře klient-server, kde se potřebujete připojit k jediné webové stránce. Můžete jednoduše vytvořit tunnel pomocí I2PTunnel pro připojení k této webové stránce, jak je znázorněno na obrázku 1.

Pokud je vaše aplikace distribuovaná, bude vyžadovat připojení k velkému množství peerů. Při použití I2PTunnel budete muset vytvořit nový tunnel pro každý peer, ke kterému se chcete připojit, jak je ukázáno na obrázku 2. Tento proces lze samozřejmě automatizovat, ale provozování mnoha instancí I2PTunnel vytváří velkou režii. Navíc u mnoha protokolů budete muset přinutit všechny, aby používali stejnou sadu portů pro všechny peery — např. pokud chcete spolehlivě provozovat DCC chat, všichni se musí dohodnout, že port 10001 je Alice, port 10002 je Bob, port 10003 je Charlie atd., protože protokol zahrnuje specifické informace TCP/IP (host a port).

Obecné síťové aplikace často odesílají mnoho dodatečných dat, která by mohla být použita k identifikaci uživatelů. Názvy hostitelů, čísla portů, časová pásma, znakové sady atd. jsou často odesílány bez informování uživatele. Proto může návrh síťového protokolu specificky s ohledem na anonymitu zabránit kompromitování identit uživatelů.

Při rozhodování o tom, jak interagovat nad I2P, je také třeba zvážit hlediska efektivity. Streaming knihovna a věci postavené na ní pracují s handshaky podobnými TCP, zatímco základní I2P protokoly (I2NP a I2CP) jsou striktně založené na zprávách (jako UDP nebo v některých případech raw IP). Důležité rozlišení je, že s I2P probíhá komunikace přes dlouhou širokopásmovou síť — každá end-to-end zpráva bude mít netriviální latence, ale může obsahovat datové části o velikosti až několika KB. Aplikace, která potřebuje jednoduchou žádost a odpověď, se může zbavit jakéhokoliv stavu a snížit latenci způsobenou startup a teardown handshaky pomocí (best effort) datagramů, aniž by se musela starat o detekci MTU nebo fragmentaci zpráv.

![Vytvoření spojení server-klient pomocí I2PTunnel vyžaduje pouze vytvoření jediného tunelu.](/images/i2ptunnel_serverclient.png)

*Obrázek 1: Vytvoření spojení server-klient pomocí I2PTunnel vyžaduje pouze vytvoření jediného tunelu.*

![Nastavení spojení pro peer-to-peer aplikace vyžaduje velmi velké množství tunnelů.](/images/i2ptunnel_peertopeer.png)

*Obrázek 2: Nastavení připojení pro peer-to-peer aplikace vyžaduje velmi velké množství tunnelů.*

Shrnutí, řada důvodů pro psaní kódu specifického pro I2P:

- Vytváření velkého množství instancí I2PTunnel spotřebovává nezanedbatelné množství prostředků, což je problematické pro distribuované aplikace (pro každého peer je vyžadován nový tunnel).
- Obecné síťové protokoly často odesílají mnoho dalších dat, která mohou být použita k identifikaci uživatelů. Programování specificky pro I2P umožňuje vytvoření síťového protokolu, který takové informace neuvolňuje, což udržuje uživatele anonymní a bezpečné.
- Síťové protokoly navržené pro použití na běžném internetu mohou být na I2P neefektivní, což je síť s mnohem vyšší latencí.

I2P podporuje standardní [rozhraní pro pluginy](/docs/specs/plugin/) pro vývojáře, takže aplikace mohou být snadno integrovány a distribuovány.

Aplikace napsané v Javě a přístupné/spustitelné pomocí HTML rozhraní prostřednictvím standardního webapps/app.war mohou být zváženy k zařazení do distribuce I2P.

---

## Důležité koncepty

Existuje několik změn, na které si musíte zvyknout při používání I2P:

### Destination ~= host+port

Aplikace běžící na I2P odesílá zprávy z a přijímá zprávy do jedinečného kryptograficky zabezpečeného koncového bodu — "destination" (cíl). V pojmech TCP nebo UDP by destination mohl být (z velké části) považován za ekvivalent páru hostname plus číslo portu, i když existuje několik rozdílů.

- I2P destination je samo o sobě kryptografický konstrukt — všechna data poslaná na jednu jsou šifrována, jako kdyby existovalo univerzální nasazení IPsec s (anonymizovanou) polohou koncového bodu podepsanou, jako kdyby existovalo univerzální nasazení DNSSEC.
- I2P destinations jsou mobilní identifikátory — mohou být přesunuty z jednoho I2P routeru na druhý (nebo mohou dokonce „multihomovat" — operovat na více routerech současně). To je docela odlišné od světa TCP nebo UDP, kde jeden koncový bod (port) musí zůstat na jednom hostiteli.
- I2P destinations jsou ošklivé a velké — v pozadí obsahují 2048bitový ElGamal veřejný klíč pro šifrování, 1024bitový DSA veřejný klíč pro podepisování a certifikát proměnné velikosti, který může obsahovat proof of work nebo zaslepená data.

Existují způsoby, jak odkazovat na tyto dlouhé a nepřehledné destinace pomocí krátkých a přívětivých názvů (např. "irc.duck.i2p"), ale tyto techniky nezaručují globální jedinečnost (protože jsou uloženy lokálně v databázi na počítači každé osoby) a současný mechanismus není příliš škálovatelný ani bezpečný (aktualizace seznamu hostitelů jsou spravovány pomocí "předplatného" služeb pojmenování). Možná jednoho dne bude existovat nějaký bezpečný, lidsky čitelný, škálovatelný a globálně jedinečný systém pojmenování, ale aplikace by na něm neměly záviset, protože jsou lidé, kteří si nemyslí, že je takové monstrum možné. [Další informace o systému pojmenování](/docs/overview/naming/) jsou k dispozici.

Zatímco většina aplikací nemusí rozlišovat protokoly a porty, I2P je *skutečně* podporuje. Složité aplikace mohou specifikovat protokol, zdrojový port a cílový port pro každou zprávu zvlášť, aby mohly multiplexovat provoz na jednu destinaci. Podrobnosti najdete na [stránce o datagramech](/docs/api/datagrams/). Jednoduché aplikace fungují tak, že naslouchají "všem protokolům" na "všech portech" destinace.

### Anonymita a důvěrnost

I2P má transparentní end-to-end šifrování a autentifikaci pro všechna data předávaná přes síť — pokud Bob pošle na Alicinu destinaci, pouze Alicina destinace to může přijmout, a pokud Bob používá datagramovou nebo streamovací knihovnu, Alice si může být jistá, že Bobova destinace je ta, která data poslala.

Samozřejmě, I2P transparentně anonymizuje data odesílaná mezi Alicí a Bobem, ale nedělá nic pro anonymizaci obsahu toho, co si posílají. Například pokud Alice pošle Bobovi formulář se svým plným jménem, občanskými průkazy a čísly kreditních karet, I2P s tím nemůže nic udělat. Proto by protokoly a aplikace měly mít na paměti, jaké informace se snaží chránit a jaké informace jsou ochotny odhalit.

### I2P Datagramy mohou mít až několik KB

Aplikace, které používají I2P datagramy (buď surové nebo s možností odpovědi), lze v podstatě chápat z hlediska UDP — datagramy jsou neuspořádané, best effort a bezstavové — ale na rozdíl od UDP se aplikace nemusí starat o detekci MTU a mohou jednoduše odesílat velké datagramy. Zatímco horní limit je nominálně 32 KB, zpráva je fragmentována pro přenos, což snižuje spolehlivost celku. Datagramy větší než asi 10 KB se v současnosti nedoporučují. Podrobnosti najdete na [stránce datagramů](/docs/api/datagrams/). Pro mnoho aplikací je 10 KB dat dostatečných pro celý požadavek nebo odpověď, což jim umožňuje transparentně fungovat v I2P jako UDP-podobná aplikace bez nutnosti psát fragmentaci, opakované odesílání atd.

---

## Možnosti vývoje

Existuje několik způsobů odesílání dat přes I2P, každý má své výhody a nevýhody. Streaming lib je doporučené rozhraní, které používá většina I2P aplikací.

### Streaming Lib

[Kompletní streaming knihovna](/docs/api/streaming/) je nyní standardním rozhraním. Umožňuje programování pomocí soketů podobných TCP, jak je vysvětleno v [průvodci vývojem pro streaming](#developing-with-the-streaming-library).

### BOB

BOB je [Basic Open Bridge](/docs/legacy/bob/), který umožňuje aplikaci v jakémkoliv jazyce vytvářet streaming připojení do a z I2P. V tuto chvíli mu chybí podpora UDP, ale podpora UDP je plánována v blízké budoucnosti. BOB také obsahuje několik nástrojů, jako je generování klíčů destinace a ověření, že adresa odpovídá specifikacím I2P. Aktuální informace a aplikace, které používají BOB, lze najít na této [I2P stránce](http://bob.i2p/).

### SAM, SAM V2, SAM V3

*SAM se nedoporučuje. SAM V2 je v pořádku, SAM V3 se doporučuje.*

SAM je protokol [Simple Anonymous Messaging](/docs/legacy/sam/), který umožňuje aplikaci napsané v jakémkoli jazyce komunikovat se SAM bridge přes obyčejný TCP socket a nechat tento bridge multiplexovat veškerý její I2P provoz, transparentně koordinovat šifrování/dešifrování a zpracování založené na událostech. SAM podporuje tři styly provozu:

- streamy, pro případy kdy si Alice a Bob chtějí posílat data spolehlivě a v pořadí
- odpověditelné datagramy, pro případy kdy chce Alice poslat Bobovi zprávu, na kterou Bob může odpovědět
- surové datagramy, pro případy kdy chce Alice vytěžit co nejvíce šířky pásma a výkonu, a Bob se nestará o to, zda je odesílatel dat ověřen či nikoliv (např. přenášená data jsou sama o sobě ověřitelná)

SAM V3 má stejný cíl jako SAM a SAM V2, ale nevyžaduje multiplexování/demultiplexování. Každý I2P stream je zpracováván vlastním socketem mezi aplikací a SAM bridge. Kromě toho mohou být datagramy odesílány a přijímány aplikací prostřednictvím datagramové komunikace se SAM bridge.

[SAM V2](/docs/legacy/samv2/) je nová verze používaná aplikací imule, která opravuje některé problémy v [SAM](/docs/legacy/sam/).

[SAM V3](/docs/api/samv3/) je používán aplikací imule od verze 1.4.0.

### I2PTunnel

Aplikace I2PTunnel umožňuje aplikacím vytvářet specifické TCP-podobné tunnely k protějškům vytvořením buď I2PTunnel 'client' aplikací (které naslouchají na specifickém portu a připojují se ke specifické I2P destinaci pokaždé, když je otevřen socket na tento port) nebo I2PTunnel 'server' aplikací (které naslouchají na specifické I2P destinaci a pokaždé, když obdrží nové I2P připojení, přeposílají jej na specifický TCP host/port). Tyto streamy jsou 8-bitově čisté a jsou autentizovány a zabezpečeny prostřednictvím stejné streaming knihovny, kterou používá SAM, ale je zde nezanedbatelná režie spojená s vytvářením více unikátních I2PTunnel instancí, protože každá má svou vlastní unikátní I2P destinaci a svou vlastní sadu tunnelů, klíčů, atd.

### SOCKS

I2P podporuje SOCKS V4 a V5 proxy. Odchozí připojení fungují dobře. Příchozí (serverová) a UDP funkcionalita může být neúplná a netestovaná.

### Ministreaming

*Odstraněno*

Dříve existovala jednoduchá knihovna "ministreaming", ale nyní ministreaming.jar obsahuje pouze rozhraní pro plnou streaming knihovnu.

### Datagramy

*Doporučeno pro aplikace podobné UDP*

[Datagram knihovna](/docs/api/datagrams/) umožňuje odesílání UDP-podobných paketů. Je možné použít:

- Repliable datagramy
- Raw datagramy

### I2CP

*Nedoporučuje se*

[I2CP](/docs/specs/i2cp/) samotný je protokol nezávislý na programovacím jazyce, ale pro implementaci I2CP knihovny v něčem jiném než Java je třeba napsat značné množství kódu (šifrovací rutiny, marshalling objektů, asynchronní zpracování zpráv, atd.). Zatímco někdo by mohl napsat I2CP knihovnu v C nebo něčem jiném, pravděpodobně by bylo užitečnější použít místo toho C SAM knihovnu.

### Webové aplikace

I2P se dodává s webovým serverem Jetty a konfigurace pro použití serveru Apache je místo toho přímočará. Jakákoli standardní technologie webových aplikací by měla fungovat.

---

## Začněte vyvíjet — Jednoduchý průvodce

Vývoj pomocí I2P vyžaduje funkční instalaci I2P a vývojové prostředí podle vašeho výběru. Pokud používáte Javu, můžete začít vývoj se [streaming library](#developing-with-the-streaming-library) nebo datagram library. Při použití jiného programovacího jazyka lze použít SAM nebo BOB.

### Vývoj se Streaming Library

Následující příklad ukazuje, jak vytvořit TCP-like klientské a serverové aplikace pomocí streaming knihovny.

To bude vyžadovat následující knihovny ve vašem classpath:

- `$I2P/lib/streaming.jar`: Samotná streaming knihovna
- `$I2P/lib/mstreaming.jar`: Factory a rozhraní pro streaming knihovnu
- `$I2P/lib/i2p.jar`: Standardní I2P třídy, datové struktury, API a nástroje

Můžete je získat z instalace I2P, nebo přidat následující závislosti z Maven Central:

- `net.i2p:i2p`
- `net.i2p.client:streaming`

Síťová komunikace vyžaduje použití I2P network socketů. Pro demonstraci vytvoříme aplikaci, kde klient může posílat textové zprávy serveru, který zprávy vytiskne a pošle je zpět klientovi. Jinými slovy, server bude fungovat jako echo.

Začneme inicializací serverové aplikace. To vyžaduje získání I2PSocketManager a vytvoření I2PServerSocket. Neposkytujeme I2PSocketManagerFactory uložené klíče pro existující Destination, takže pro nás vytvoří novou Destination. Proto požádáme I2PSocketManager o I2PSession, abychom mohli zjistit vytvořenou Destination, protože budeme tyto informace později potřebovat zkopírovat a vložit, aby se k nám mohl klient připojit.

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
*Příklad kódu 1: inicializace serverové aplikace.*

Jakmile máme I2PServerSocket, můžeme vytvořit instance I2PSocket pro přijímání připojení od klientů. V tomto příkladu vytvoříme jednu instanci I2PSocket, která dokáže zpracovat pouze jednoho klienta najednou. Skutečný server by musel být schopen zpracovat více klientů. K tomu by bylo nutné vytvořit více instancí I2PSocket, každou v samostatném vlákně. Jakmile vytvoříme instanci I2PSocket, čteme data, vypíšeme je a pošleme zpět klientovi.

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
*Příklad kódu 2: přijímání připojení od klientů a zpracování zpráv.*

Když spustíte výše uvedený serverový kód, měl by vypsat něco takového (ale bez konců řádků, měl by to být jen jeden obrovský blok znaků):

```
y17s~L3H9q5xuIyyynyWahAuj6Jeg5VC~Klu9YPquQvD4vlgzmxn4yy~5Z0zVvKJiS2Lk
poPIcB3r9EbFYkz1mzzE3RYY~XFyPTaFQY8omDv49nltI2VCQ5cx7gAt~y4LdWqkyk3au
...
```
Toto je base64 reprezentace Destination serveru. Klient bude potřebovat tento řetězec pro dosažení serveru.

Nyní vytvoříme klientskou aplikaci. Opět je pro inicializaci potřeba několik kroků. Znovu budeme muset začít získáním I2PSocketManager. Tentokrát nebudeme používat I2PSession a I2PServerSocket. Místo toho použijeme řetězec Destination serveru k navázání našeho spojení. Požádáme uživatele o řetězec Destination a vytvoříme I2PSocket pomocí tohoto řetězce. Jakmile budeme mít I2PSocket, můžeme začít odesílat a přijímat data ze serveru a na server.

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
*Příklad kódu 3: spuštění klienta a jeho připojení k serverové aplikaci.*

Nakonec můžete spustit jak serverovou, tak klientskou aplikaci. Nejprve spusťte serverovou aplikaci. Vypíše řetězec Destination (jak je ukázáno výše). Poté spusťte klientskou aplikaci. Když si vyžádá řetězec Destination, můžete zadat řetězec vypsaný serverem. Klient pak odešle 'Hello I2P!' (spolu s novým řádkem) serveru, který zprávu vypíše a pošle ji zpět klientovi.

Gratulujeme, úspěšně jste komunikovali přes I2P!

---

## Existující aplikace

Kontaktujte nás, pokud byste chtěli přispět.

- [I2P-Bote](http://i2pbote.i2p/) - kontaktujte HungryHobo
- [Syndie](http://syndie.i2p2.de/)
- [IMule](http://www.imule.i2p/)
- [I2Phex](http://forum.i2p/viewforum.php?f=25)

Viz také všechny pluginy na [plugins.i2p](http://plugins.i2p/), aplikace a zdrojový kód uvedený na [echelon.i2p](http://echelon.i2p/) a kód aplikací hostovaný na [git.repo.i2p](http://git.repo.i2p/).

Viz také dodávané aplikace v distribuci I2P - SusiMail a I2PSnark.

---

## Nápady na aplikace

- NNTP server - v minulosti jich několik bylo, momentálně žádný
- Jabber server - v minulosti jich několik bylo a momentálně jeden funguje, s přístupem na veřejný internet
- PGP Key server a/nebo proxy
- Aplikace pro distribuci obsahu / DHT - obnovit feedspace, portovat dijjer, hledat alternativy
- Pomoc s vývojem [Syndie](http://syndie.i2p2.de/)
- Webové aplikace - Možnosti jsou neomezené pro hostování aplikací založených na webovém serveru jako jsou blogy, pastebiny, úložiště, tracking, feedy atd. Funguje jakákoli webová nebo CGI technologie jako Perl, PHP, Python nebo Ruby.
- Obnovit některé staré aplikace, několik jich dříve bylo v balíčku zdrojového kódu i2p - bogobot, pants, proxyscript, q, stasher, socks proxy, i2ping, feedspace
