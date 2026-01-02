---
title: "Pojmenování a Adresář"
description: "Jak I2P mapuje lidsky čitelné názvy hostitelů na destinace"
slug: "naming"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

I2P adresy jsou dlouhé kryptografické klíče. Systém pojmenování poskytuje přívětivější vrstvu nad těmito klíči **bez zavedení centrální autority**. Všechna jména jsou **lokální**—každý router nezávisle rozhoduje, na jakou destinaci se název hostitele odkazuje.

> **Potřebujete kontext?** [Diskuse o pojmenování](/docs/legacy/naming/) dokumentuje původní designové debaty, alternativní návrhy a filozofické základy decentralizovaného pojmenování v I2P.

---

## 1. Komponenty

Vrstva pojmenování I2P se skládá z několika nezávislých, ale spolupracujících subsystémů:

1. **Služba překladu názvů** – překládá názvy hostitelů na destinace a zpracovává [Base32 názvy hostitelů](#base32-hostnames).
2. **HTTP proxy** – předává vyhledávání `.i2p` do routeru a navrhuje jump služby, když je název neznámý.
3. **Služby přidání hostitele** – formuláře ve stylu CGI, které připojují nové záznamy do místního adresáře.
4. **Jump služby** – vzdálení pomocníci, kteří vrací destinaci pro zadaný název hostitele.
5. **Adresář** – pravidelně stahuje a slučuje vzdálené seznamy hostitelů pomocí místně důvěryhodné "sítě důvěry".
6. **SusiDNS** – webové uživatelské rozhraní pro správu adresářů, odběrů a místních přepsání.

Tento modulární design umožňuje uživatelům definovat vlastní hranice důvěry a automatizovat libovolnou část procesu pojmenovávání podle jejich preferencí.

---

## 2. Služby jmenování

API routeru pro jmenování (`net.i2p.client.naming`) podporuje více backendů prostřednictvím konfigurovatelné vlastnosti `i2p.naming.impl=<class>`. Každá implementace může nabídnout různé strategie vyhledávání, ale všechny sdílejí stejný model důvěry a rozlišení.

### 2.1 Hosts.txt (legacy format)

Starší model používal tři textové soubory kontrolované v pořadí:

1. `privatehosts.txt`
2. `userhosts.txt`
3. `hosts.txt`

Každý řádek ukládá mapování `hostname=base64-destination`. Tento jednoduchý textový formát zůstává plně podporován pro import/export, ale již není výchozí kvůli nízké výkonnosti při překročení několika tisíc položek v seznamu hostitelů.

---

### 2.2 Blockfile Naming Service (default backend)

Představena ve **vydání 0.8.8**, služba Blockfile Naming Service je nyní výchozím backendem. Nahrazuje ploché soubory vysoce výkonným skiplist-based on-disk úložištěm klíč/hodnota (`hostsdb.blockfile`), které poskytuje přibližně **10× rychlejší vyhledávání**.

**Klíčové charakteristiky:** - Ukládá více logických adresářů (soukromý, uživatelský a hosts) v jedné binární databázi. - Udržuje kompatibilitu se starším importem/exportem hosts.txt. - Podporuje reverzní vyhledávání, metadata (datum přidání, zdroj, komentáře) a efektivní ukládání do mezipaměti. - Používá stejné třístupňové pořadí vyhledávání: soukromý → uživatelský → hosts.

Tento přístup zachovává zpětnou kompatibilitu a zároveň výrazně zlepšuje rychlost překladu a škálovatelnost.

---

### 2.1 Hosts.txt (starší formát)

Vývojáři mohou implementovat vlastní backendy jako například: - **Meta** – agreguje více systémů jmen. - **PetName** – podporuje petnames uložené v souboru `petnames.txt`. - **AddressDB**, **Exec**, **Eepget** a **Dummy** – pro externí nebo záložní překlad adres.

Implementace blockfile zůstává **doporučeným** backendem pro obecné použití díky výkonu a spolehlivosti.

---

## 3. Base32 Hostnames

Base32 názvy hostitelů (`*.b32.i2p`) fungují podobně jako Torové adresy `.onion`. Když přistupujete k adrese `.b32.i2p`:

1. Router dekóduje Base32 payload.
2. Rekonstruuje cíl přímo z klíče—**není vyžadováno vyhledávání v adresáři**.

To zaručuje dosažitelnost, i když neexistuje lidsky čitelný název hostitele. Rozšířené Base32 názvy zavedené ve **verzi 0.9.40** podporují **LeaseSet2** a šifrované destinace.

---

## 4. Address Book & Subscriptions

Aplikace adresáře načítá vzdálené seznamy hostitelů přes HTTP a sloučí je lokálně podle uživatelem nakonfigurovaných pravidel důvěry.

### 2.2 Blockfile Naming Service (výchozí backend)

- Odběry jsou standardní `.i2p` URL adresy odkazující na `hosts.txt` nebo kanály přírůstkových aktualizací.
- Aktualizace se stahují pravidelně (standardně každou hodinu) a před sloučením se validují.
- Konflikty se řeší podle principu **kdo dřív přijde, ten dřív mele**, v tomto pořadí priority:  
  `privatehosts.txt` → `userhosts.txt` → `hosts.txt`.

#### Default Providers

Od verze **I2P 2.3.0 (červen 2023)** jsou zahrnuty dva výchozí poskytovatelé odběrů: - `http://i2p-projekt.i2p/hosts.txt` - `http://notbob.i2p/hosts.txt`

Tato redundance zlepšuje spolehlivost při zachování modelu lokální důvěry. Uživatelé mohou přidávat nebo odebírat odběry prostřednictvím SusiDNS.

#### Incremental Updates

Inkrementální aktualizace se získávají prostřednictvím `newhosts.txt` (nahrazuje starší koncept `recenthosts.cgi`). Tento endpoint poskytuje efektivní **delta aktualizace založené na ETag**—vrací pouze nové záznamy od posledního požadavku nebo `304 Not Modified`, pokud nedošlo ke změnám.

---

### 2.3 Alternativní Backendy a Plug-iny

- **Host-add služby** (`add*.cgi`) umožňují ruční odeslání mapování názvu na cíl. Vždy ověřte cíl před přijetím.  
- **Jump služby** odpovídají příslušným klíčem a mohou přesměrovat přes HTTP proxy s parametrem `?i2paddresshelper=`.  
  Běžné příklady: `stats.i2p`, `identiguy.i2p` a `notbob.i2p`.  
  Tyto služby **nejsou důvěryhodné autority**—uživatelé musí rozhodnout, které použít.

---

## 5. Managing Entries Locally (SusiDNS)

SusiDNS je dostupný na: `http://127.0.0.1:7657/susidns/`

Můžete: - Zobrazit a upravovat místní adresáře. - Spravovat a upřednostňovat odběry. - Importovat/exportovat seznamy hostitelů. - Konfigurovat plány stahování.

**Nové v I2P 2.8.1 (březen 2025):** - Přidána funkce "řazení podle nejnovějších". - Vylepšená správa odběrů (oprava pro nekonzistence ETag).

Všechny změny zůstávají **lokální**—adresář každého routeru je jedinečný.

---

## 3. Base32 Hostnames

Podle RFC 9476 I2P zaregistroval **`.i2p.alt`** u GNUnet Assigned Numbers Authority (GANA) k **březnu 2025 (I2P 2.8.1)**.

**Účel:** Zabránit náhodnému úniku DNS z nesprávně nakonfigurovaného softwaru.

- DNS resolvery kompatibilní s RFC 9476 **nebudou přeposílat** domény `.alt` do veřejného DNS.
- Software I2P zachází s `.i2p.alt` jako s ekvivalentem `.i2p`, při překladu odstraňuje příponu `.alt`.
- `.i2p.alt` **není** určena k nahrazení `.i2p`; je to technické opatření, ne rebrandování.

---

## 4. Adresář & Odběry

- **Destination keys:** 516–616 bajtů (Base64)  
- **Názvy hostitelů:** Max 67 znaků (včetně `.i2p`)  
- **Povolené znaky:** a–z, 0–9, `-`, `.` (žádné dvojité tečky, žádná velká písmena)  
- **Vyhrazeno:** `*.b32.i2p`  
- **ETag a Last-Modified:** aktivně používány pro minimalizaci šířky pásma  
- **Průměrná velikost hosts.txt:** ~400 KB pro ~800 hostitelů (ukázkový údaj)  
- **Využití šířky pásma:** ~10 bajtů/sec při stahování každých 12 hodin

---

## 8. Security Model and Philosophy

I2P záměrně obětuje globální jedinečnost výměnou za decentralizaci a bezpečnost—přímou aplikaci **Zookova trojúhelníku**.

**Klíčové principy:** - **Žádná centrální autorita:** všechna vyhledávání jsou lokální.   - **Odolnost vůči únosům DNS:** dotazy jsou šifrovány na veřejné klíče cílových adres.   - **Prevence Sybil útoků:** žádné hlasování ani pojmenování založené na konsenzu.   - **Neměnné mapování:** jakmile lokální asociace existuje, nelze ji vzdáleně přepsat.

Systémy pojmenování založené na blockchainu (např. Namecoin, ENS) zkoumaly řešení všech tří stran Zookova trojúhelníku, ale I2P se jim záměrně vyhýbá kvůli latenci, složitosti a filozofické nekompatibilitě s jeho modelem lokální důvěry.

---

## 9. Compatibility and Stability

- Mezi lety 2023–2025 nebyly žádné funkce jmenných služeb označeny jako zastaralé.
- Formát hosts.txt, jump služby, odběry a všechny implementace API jmenných služeb zůstávají funkční.
- Projekt I2P udržuje přísnou **zpětnou kompatibilitu** při zavádění vylepšení výkonu a bezpečnosti (izolace NetDB, oddělení Sub-DB atd.).

---

## 10. Best Practices

- Udržujte pouze důvěryhodné odběry; vyhněte se velkým, neznámým seznamům hostitelů.
- Před aktualizací nebo přeinstalací zálohujte `hostsdb.blockfile` a `privatehosts.txt`.
- Pravidelně kontrolujte jump services a zakažte ty, kterým již nedůvěřujete.
- Pamatujte: váš adresář definuje vaši verzi světa I2P—**každý název hostitele je lokální**.

---

### Further Reading

- [Diskuze o jménných službách](/docs/legacy/naming/)  
- [Specifikace formátu blockfile](/docs/specs/blockfile/)  
- [Formát konfiguračního souboru](/docs/specs/configuration/)  
- [Javadoc jménné služby](http://idk.i2p/javadoc-i2p/net/i2p/client/naming/package-summary.html)

---
