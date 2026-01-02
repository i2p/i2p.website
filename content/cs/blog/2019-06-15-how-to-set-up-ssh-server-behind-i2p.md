---
title: "Jak nastavit ssh server za I2P pro soukromý přístup"
date: 2019-06-15
author: "idk"
description: "SSH přes I2P"
---

# Jak nastavit SSH server dostupný přes I2P pro osobní přístup

Toto je návod, jak nastavit a doladit I2P tunnel, abyste jej mohli použít pro vzdálený přístup k serveru SSH, s využitím I2P nebo i2pd. Prozatím se předpokládá, že server SSH nainstalujete pomocí správce balíčků a že poběží jako služba.

Poznámky: V tomto návodu předpokládám několik věcí. Bude je potřeba upravit podle komplikací, které se mohou objevit ve vašem konkrétním nastavení, zejména pokud pro izolaci používáte virtuální stroje (VM) nebo kontejnery. Tento postup předpokládá, že I2P router a SSH server běží na stejném localhostu. Měli byste používat nově vygenerované hostitelské klíče SSH, buď díky čerstvě nainstalovanému sshd, nebo smazáním starých klíčů a vynucením jejich opětovného vygenerování. Například:

```
sudo service openssh stop
sudo rm -f /etc/ssh/ssh_host_*
sudo ssh-keygen -N "" -t rsa -f /etc/ssh/ssh_host_rsa_key
sudo ssh-keygen -N "" -t dsa -f /etc/ssh/ssh_host_dsa_key
sudo ssh-keygen -N "" -t ecdsa -f /etc/ssh/ssh_host_ecdsa_key
sudo ssh-keygen -N "" -t ed25519 -f /etc/ssh/ssh_host_ed25519_key
```
## Step One: Set up I2P tunnel for SSH Server

### Using Java I2P

Pomocí webového rozhraní java I2P přejděte na [Hidden Services Manager](http://127.0.0.1:7657/i2ptunnelmgr) a spusťte průvodce pro tunnel.

#### Tunnel Wizard

Protože nastavujete tento tunnel pro SSH server, musíte zvolit typ tunnelu "Server".

**Zástupný snímek obrazovky:** Pomocí průvodce vytvořte "Server" tunnel

Později byste to měli vyladit, ale typ Standard tunnel je pro začátek nejjednodušší.

**Zástupný snímek obrazovky:** Ve variantě "Standard"

Uveďte kvalitní popis:


**Zástupné místo pro snímek obrazovky:** Popište, k čemu slouží

A uveďte, kde bude SSH server dostupný.

**Zástupný snímek obrazovky:** Nasměrujte jej na budoucí umístění vašeho SSH serveru

Prohlédněte si výsledky a uložte svá nastavení.

**Zástupný snímek obrazovky:** Uložte nastavení.

#### Advanced Settings

Nyní se vraťte do Hidden Services Manager (Správce skrytých služeb) a prohlédněte si dostupná pokročilá nastavení. Jedna věc, kterou si určitě budete chtít změnit, je zvolit interaktivní připojení namísto hromadného.

**Zástupný snímek obrazovky:** Nakonfigurujte svůj tunnel (tunel) pro interaktivní připojení

Kromě toho mohou výkon při přístupu k vašemu SSH serveru ovlivnit i tyto další možnosti. Pokud vám tolik nejde o anonymitu, můžete snížit počet skoků, které používáte. Pokud máte potíže s rychlostí, může pomoci vyšší počet tunnel (I2P tunelů). Několik záložních tunnel je pravděpodobně dobrý nápad. Možná to budete muset trochu doladit.

**Zástupný snímek obrazovky:** Pokud vám na anonymitě nezáleží, pak zkraťte délku tunnelu.

Nakonec restartujte tunnel, aby se všechna vaše nastavení projevila.

Další zajímavé nastavení, zejména pokud se rozhodnete provozovat velké množství tunnels, je "Reduce on Idle", které sníží počet tunnels, které běží, když je server delší dobu nečinný.

**Zástupný obrázek:** Snižte při nečinnosti, pokud jste zvolili vysoký počet tunnels

### Using i2pd

V i2pd se veškerá konfigurace provádí pomocí souborů, nikoli prostřednictvím webového rozhraní. Chcete-li pro i2pd nakonfigurovat SSH Service tunnel, upravte následující ukázková nastavení podle vašich požadavků na anonymitu a výkon a zkopírujte je do tunnels.conf

```
[SSH-SERVER]
type = server
host = 127.0.0.1
port = 22
inbound.length = 1
outbound.length = 1
inbound.quantity = 5
outbound.quantity = 5
i2cp.reduceOnIdle = true
keys = ssh-in.dat
```
#### Restart your I2P router

## Krok 1: Nastavte I2P tunnel pro SSH server

V závislosti na tom, jak chcete přistupovat ke svému SSH serveru, možná budete chtít provést několik změn v nastavení. Kromě zřejmých opatření pro zabezpečení SSH, která byste měli dělat na všech SSH serverech(ověřování veřejným klíčem, zákaz přihlášení jako root, atd.), pokud nechcete, aby váš SSH server naslouchal pouze přes váš server tunnel, měli byste změnit AddressFamily na inet a ListenAddress na 127.0.0.1.

```
AddressFamily inet
ListenAddress 127.0.0.1
```
Pokud se rozhodnete používat pro svůj SSH server jiný port než 22, budete muset změnit port v konfiguraci svého I2P tunnelu.

## Step Three: Set up I2P tunnel for SSH Client

Abyste mohli nakonfigurovat své klientské připojení, budete muset mít možnost zobrazit konzoli I2P routeru na SSH serveru. Jednou z výhod tohoto nastavení je, že počáteční připojení k I2P tunnelu je autentizované, což do určité míry snižuje riziko, že vaše první připojení k SSH serveru bude napadeno útokem typu MITM, jaké hrozí ve scénářích Trust-On-First-Use (důvěra při prvním použití).

### Použití Java I2P

#### Průvodce Tunnel

Nejprve spusťte průvodce konfigurací pro tunnel ze správce skrytých služeb a vyberte klientský tunnel.

**Zástupný snímek obrazovky:** Použijte průvodce k vytvoření client tunnel

Poté vyberte standardní typ tunnel (datový tunel v I2P). Tuto konfiguraci doladíte později.

**Zástupný snímek obrazovky:** standardní varianty

Zadejte dobrý popis.

**Zástupný snímek obrazovky:** Přidejte k němu dobrý popis

Toto je jediná mírně záludná část. Přejděte do správce skrytých služeb v konzoli I2P routeru a najděte base64 "local destination" u SSH server tunnelu. Budete muset najít způsob, jak tuto informaci zkopírovat do dalšího kroku. Obvykle si to pošlu sám sobě přes [Tox](https://tox.chat), jakýkoli off-the-record (soukromý, neprotokolovaný) by měl většině lidí stačit.

**Zástupný snímek obrazovky:** Najděte cíl, ke kterému se chcete připojit

Jakmile najdete base64 destinaci, ke které se chcete připojit, která byla přenesena do vašeho klientského zařízení, vložte ji do pole destinace klienta.

**Zástupný snímek obrazovky:** Připojte cílovou adresu

Nakonec nastavte lokální port, ke kterému připojíte svůj SSH klient. Tento lokální port bude připojen k base64 destination a tím i k SSH serveru.

**Zástupný symbol snímku obrazovky:** Vyberte lokální port

Rozhodněte se, zda chcete, aby se spouštěl automaticky.

**Zástupné místo pro snímek obrazovky:** Rozhodněte se, zda chcete, aby se spouštěl automaticky

#### Pokročilá nastavení

Stejně jako dříve budete chtít změnit nastavení tak, aby bylo optimalizované pro interaktivní připojení. Navíc, pokud chcete na serveru nastavit seznam povolených klientů (whitelisting), měli byste zvolit přepínač (radio button) "Generate key to enable persistent client tunnel identity".

**Zástupný snímek obrazovky:** Nakonfigurujte jej tak, aby byl interaktivní

### Using i2pd

Můžete to nastavit přidáním následujících řádků do souboru tunnels.conf a upravit nastavení podle svých požadavků na výkon/anonymitu.

```
[SSH-CLIENT]
type = client
host = 127.0.0.1
port = 7622
inbound.length = 1
outbound.length = 1
inbound.quantity = 5
outbound.quantity = 5
i2cp.dontPublishLeaseSet = true
destination = thisshouldbethebase32ofthesshservertunnelabovebefore.b32.i2p
keys = ssh-in.dat
```
#### Restart the I2P router on the client

## Step Four: Set up SSH client

Existuje mnoho způsobů, jak nastavit klienta SSH pro připojení k vašemu serveru na I2P, ale je pár věcí, které byste měli udělat, abyste zabezpečili svůj klient SSH pro anonymní použití. Nejprve byste jej měli nastavit tak, aby se vůči serveru SSH identifikoval pouze jediným, konkrétním klíčem, abyste neriskovali prozrazení vazby mezi vašimi anonymními a neanonymními připojeními SSH.

Ujistěte se, že váš $HOME/.ssh/config obsahuje následující řádky:

```
IdentitiesOnly yes

Host 127.0.0.1
  IdentityFile ~/.ssh/login_id_ed25519
```
Alternativně můžete vytvořit záznam do .bash_alias, abyste vynutili svá nastavení a automaticky se připojili k I2P. Chápete: je třeba vynutit IdentitiesOnly a poskytnout soubor identity.

```
i2pssh() {
    ssh -o IdentitiesOnly=yes -o IdentityFile=~/.ssh/login_id_ed25519 serveruser@127.0.0.1:7622
}
```
## Step Five: Whitelist only the client tunnel

Je to víceméně volitelné, ale je to docela šikovné a zabrání komukoli, kdo náhodou narazí na vaši destination (I2P cílovou adresu), aby zjistil, že provozujete službu SSH.

Nejprve načtěte trvalou destinaci klientského tunnelu a odešlete ji serveru.

**Zástupný snímek obrazovky:** Získejte destination klienta (cílový identifikátor)

Přidejte base64 destinaci klienta do seznamu povolených destinací serveru. Nyní se k server tunnel připojíte pouze z tohoto konkrétního client tunnel a nikdo jiný se k dané destinaci nepřipojí.

**Zástupný snímek obrazovky:** A vložte jej do seznamu povolených serverů

Vzájemná autentizace je nejlepší.

**Poznámka:** Obrázky odkazované v původním příspěvku je třeba přidat do adresáře `/static/images/`: - server.png, standard.png, describe.png, hostport.png, approve.png - interactive.png, anonlevel.png, idlereduce.png - client.png, clientstandard.png, clientdescribe.png - finddestination.png, fixdestination.png, clientport.png, clientautostart.png - clientinteractive.png, whitelistclient.png, whitelistserver.png
