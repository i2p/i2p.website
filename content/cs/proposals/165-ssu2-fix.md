---
title: "Návrh I2P č. 165: Oprava SSU2"
number: "165"
author: "weko, orignal, the Anonymous, zzz"
created: "2024-01-19"
lastupdated: "2024-11-17"
status: "Otevřeno"
thread: "http://i2pforum.i2p/viewforum.php?f=13"
target: "0.9.62"
---

Návrh od weko, orignal, the Anonymous a zzz.


### Přehled

Tento dokument navrhuje změny v SSU2 po útoku na I2P, který využil zranitelnosti v SSU2. Hlavním cílem je zvýšit bezpečnost a zabránit útokům typu Distributed Denial of Service (DDoS) a pokusům o de-anonymizaci.

### Model hrozby

Útočník vytváří nové falešné routerové informace (RI) (router neexistuje): je to běžná RI, ale vloží adresu, port, klíče s a i z opravdového Bobova routeru, a poté zaplaví síť. Když se snažíme připojit k tomuto (jak si myslíme opravdovému) routeru, jako Alice se můžeme připojit k této adrese, ale nemůžeme si být jisti, co se stalo s opravdovou Bobovou RI. To je možné a bylo použito pro útok typu Distributed Denial of Service (vytvořit velké množství takových RIs a zaplavit síť), také to může usnadnit de-anonymizační útoky tím, že budou "nasazeny" dobré routery a útočníkovy routery nebudou napadány, pokud zakážeme IP s mnoha RIs (místo toho, abychom lépe rozprostřeli stavbu tunelu k těmto RI jako k jednomu routeru).

### Možné opravy

#### 1. Oprava s podporou starých (před změnou) routerů

.. _overview-1:

Přehled
^^^^^^^^

Náhradní řešení pro podporu SSU2 připojení ke starým routerům.

Chování
^^^^^^^^^

Bobův routerový profil by měl mít příznak 'ověřený', který je ve výchozím nastavení pro všechny nové routery (zatím bez profilu) false. Když je příznak 'ověřený' false, nikdy neděláme připojení pomocí SSU2 jako Alice k Bobovi - nemůžeme si být jisti RI. Pokud Bob se připojil k nám (Alice) pomocí NTCP2 nebo SSU2 nebo my (Alice) jsme se jednou připojili k Bobovi pomocí NTCP2 (můžeme ověřit Bobův RouterIdent v těchto případech) - příznak je nastaven na true.

Problémy
^^^^^^^^

Takže existuje problém s falešnou povodní SSU2-pouze RI: nemůžeme to ověřit sami a jsme nuceni čekat, kdy se opravdový router s námi spojí.

#### 2. Ověření RouterIdent během vytváření spojení

.. _overview-2:

Přehled
^^^^^^^^

Přidání bloku „RouterIdent“ pro SessionRequest a SessionCreated.

Možný formát bloku RouterIdent
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

1 bajtový příznak, 32 bajtů RouterIdent. Příznak_0: 0 pokud je to přijímačův RouterIdent; 1 pokud je to odesílatelův RouterIdent

Chování
^^^^^^^^

Alice (měla by(1), může(2)) poslat v uživatelských datech blok RouterIdent s Příznak_0 = 0 a Bobovým RouterIdent. Bob (měl by(3), může(4)) ověřit, jestli je to jeho RouterIdent, a pokud ne: ukončit relaci s důvodem „Špatný RouterIdent“, pokud je to jeho RouterIdent: poslat blok RI s 1 v Příznak_0 a Bobovým RouterIdent.

S (1) Bob nepodporuje staré routery. S (2) Bob podporuje staré routery, ale může být obětí DDoS ze stran routerů, které se snaží navázat spojení s falešnými RIs. S (3) Alice nepodporuje staré routery. S (4) Alice podporuje staré routery a používá hybridní schéma: Oprava 1 pro staré routery a Oprava 2 pro nové routery. Pokud RI říká nová verze, ale během připojení jsme neobdrželi blok RouterIdent - ukončit a odstranit RI.

.. _problems-1:

Problémy
^^^^^^^^

Útočník může maskovat své falešné routery jako staré a s (4) stejně čekáme na 'ověření' jako v opravě 1.

Poznámky
^^^^^

Místo 32 bajtového RouterIdent, můžeme pravděpodobně použít 4 bajtový siphash-of-the-hash, nějaký HKDF nebo něco jiného, což by mělo stačit.

#### 3. Bob nastaví i = RouterIdent

.. _overview-3:

Přehled
^^^^^^^^

Bob používá svůj RouterIdent jako klíč i.

.. _behavior-1:

Chování
^^^^^^^^

Bob (měl by(1), může(2)) používá svůj vlastní RouterIdent jako klíč i pro SSU2.

Alice s (1) se připojí jen pokud i = Bobův RouterIdent. Alice s (2) používá hybridní schéma (oprava 3 a 1): pokud i = Bobův RouterIdent, můžeme navázat spojení, jinak bychom to měli nejprve ověřit (viz oprava 1).

S (1) Alice nepodporuje staré routery. S (2) Alice podporuje staré routery.

.. _problems-2:

Problémy
^^^^^^^^

Útočník může maskovat své falešné routery jako staré a s (2) stejně čekáme na 'ověření' jako v opravě 1.

.. _notes-1:

Poznámky
^^^^^

Pro úsporu velikosti RI je lepší přidat zpracování, pokud není zadán klíč i. Pokud je, pak i = RouterIdent. V takovém případě Bob nepodporuje staré routery.

#### 4. Přidání dalšího MixHash do KDF zprávy SessionRequest

.. _overview-4:

Přehled
^^^^^^^^

Přidat MixHash(Bobův ident hash) do NOISE stavu zprávy "SessionRequest", např. h = SHA256 (h || Bobův ident hash). Musí to být poslední MixHash použitý jako ad pro ENCRYPT nebo DECRYPT. Musí být zaveden další příznak záhlaví SSU2 "Ověř Bobův ident" = 0x02.

.. _behavior-4:

Chování
^^^^^^^^

- Alice přidá MixHash s Bobovým ident hashem z Bobovy RouterInfo a použije jej jako ad pro ENCRYPT a nastaví příznak "Ověř Bobův ident"
- Bob zkontroluje příznak "Ověř Bobův ident" a přidá MixHash s vlastním ident hashem a použije jej jako ad pro DECRYPT. Pokud AEAD/Chacha20/Poly1305 selže, Bob zavře relaci.

Kompatibilita se staršími routery
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Alice musí zkontrolovat Bobovu verzi routeru a pokud splňuje minimální verzi podporující tento návrh, přidá tento MixHash a nastaví příznak "Ověř Bobův ident". Pokud je router starší, Alice MixHash nepřidává a příznak "Ověř Bobův ident" nenastavuje.
- Bob zkontroluje příznak "Ověř Bobův ident" a přidá tento MixHash, pokud je nastaven. Starší routery tento příznak nenastavují a tento MixHash by neměl být přidán.

.. _problems-4:

Problémy
^^^^^^^^

- Útočník může tvrdit, že falešné routery mají starší verzi. V určitou chvíli by starší routery měly být používány s opatrností a po ověření jinými způsoby.


### Zpětná kompatibilita

Popis v opravách.


### Aktuální stav

i2pd: Oprava 1.
