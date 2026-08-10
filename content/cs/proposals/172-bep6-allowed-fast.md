---
title: "Rychlé rozšíření (BEP 6) – povolené rychlé připojení s identitou peeru na základě hashovací funkce cíle"
number: "172"
author: "dr|z3d"
created: "2026-08-10"
lastupdated: "2026-08-10"
status: "Návrh"
toc: true
---

## Přehled

BEP 6 (rozšíření Fast Extension) zahrnuje pět funkcí: **Have All / Have None**, **Reject Requests**, **Suggestions** a **Allowed fast**. Protokol na úrovni „drátu“ — bit pro vyjednávání, ID zpráv a sémantika udušování — je nezávislý na přenosovém prostředí a bez dalšího funguje přes I2P streamování. Jedinou částí BEP 6, kterou nelze přímo mapovat na I2P, je **generování množiny Allowed Fast**, protože je definována na základě IPv4 adresy protějšku. Protějšky v I2P žádné IP adresy nemají; identifikují se 32bytovými hashi destinací.

Tento návrh standardizuje generování seznamu povolených rychlých (Allowed Fast) připojení nativně v I2P, takže všechny I2P klienty pro torrenty budou generovat *identické* sady povolených rychlých připojení pro stejného protějška a stejný torrent, čímž se tato funkce stane užitečnou (a ověřitelnou) napříč různými implementacemi.

## Motivace

Noví protějšky potřebují první kousky, než se může na BitTorrentu rozjet systém „za dar za dar“. V síti I2P je tento nástup pomalejší než na clearnetu: nastavení spojení a přenos bloků musí projít několika skoky vysokolatencních tunelů, takže doba mezi připojením a prvním vzájemným uvolněním je delší. Možnost Allowed Fast přímo řeší tento problém – nový protějšek může získat malý počet bloků hned, i když je stále potlačen (choked), což mu umožní rychleji začít s navracením dat.

Referenční BEP 6 vypočítává povolenou rychlou sadu na základě IPv4 adresy protějšku, aby zajistil, že *odesílatel* může vybírat kousky jedinečné pro *příjemce* (jeden uživatel s mnoha IP adresami nemůže shromažďovat mnoho sad). V síti I2P plní stejnou vázací funkci hash destinace protějšku, který je dostupný oběma koncům každého spojení, čímž je sada deterministická *a místně ověřitelná* — což je něco, co schéma založené na IP nemůže nabídnout.

## Úpravy BEP 6

Vyjednávání rozšíření Fast Extension a všechny čtyři typy zpráv jsou převzaty beze změny:

- Vyjednávání: třetí nejméně významný bit posledního rezervovaného bajtu, `reserved[7] |= 0x04`, na obou koncích
- Má vše `<len=0x0001><op=0x0E>`, Nemá nic `<len=0x0001><op=0x0F>`
- Navrhnout kus `<len=0x0005><op=0x0D><index>`
- Zamítnout požadavek `<len=0x000D><op=0x10><index><begin><length>`
- Povoleno rychlé `<len=0x0005><op=0x11><index>`
- Každý požadavek má za následek přesně jednu odpověď (kus nebo zamítnutí); ucpaní již nezamítá implicitně čekající požadavky

Jediná odchylka spočívá v generování sady Allowed Fast, kde jsou bajty IP nahrazeny bajty hashové adresy protějšku.

### Odchylka: bajty hash místo maskované IP

Viz BEP 6, krok (1):

```
x = 0xFFFFFF00 & ip
```
To využívá tři bajty IP adresy protějšku IPv4 a **nuluje 4. bajt**. Jedná se o podsíťovou heuristiku: uživatelé, kteří mohou získat více IP adres ve stejné síti /24, by neměli získat více sad povolených rychlých uzlů.

Naše verze I2P to nahradí prvními čtyřmi byty 32-byte hashovací hodnoty destinace protějšku:

```
x = first 4 bytes of peer destination hash
```
Rozdíl od referenční implementace:

> „To jsou 3 bajty IP následované nulou. Vy jste 4 bajty hash. Liší se to od BEP 6, protože tam není IP a neguluje se 4. bajt.“

Oba konce I2P spojení již znají hash cíle protějšku (jedná se o adresu, ke které/od které bylo spojení vytvořeno), takže není potřeba žádná dodatečná výměna, zjišťování NAT ani detekce externí IP — žádná z těchto věcí v I2P neexistuje.

### Povolený rychlý algoritmus generování

Nechť `hash` je 32mi bytový hash cíle přijímajícího protějšku, `infohash` 20ti bytový infohash torrentu, `sz` počet kousků v torrentu, `k` finální počet kousků v sadě povolených rychlých (10, jak v BEP 6) a `a` výstupní sada:

```
x = hash[0:4]  ++  infohash        (1)
while |a| < k:
    x = SHA1(x)                    (2)
    for i in [0:5] and |a| < k:    (3)
        y = x[i*4 : i*4+4]         (4)
        index = y % sz             (5)
        if index not in a:         (6)
            add index to a         (7)
```
Poznámky:

- 4 bajty hashovací funkce cíle nahrazují 3 maskované bajty IP adresy. Všechny čtyři bajty obsahují entropii hashovací funkce; žádný není vynulován.
- Stejně jako v BEP 6, řetězec SHA1 generuje dlouhou pseudonáhodnou posloupnost, rozdělenou na indexy bloků; `k = 10` odpovídá výchozímu nastavení reference.
- Zpráva Allowed Fast má doporučující charakter: příjemce NESMÍ interpretovat tuto zprávu jako indikaci, že odesílatel blok vlastní — pouze že odesílatel bude tento blok poskytovat i při blokování spojení.

## Výhody

| Oblast             | Výhoda                                                                                                                                                                                       |
| ------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Latence spuštění   | Noví protějšci stahují první kousky i při dusení, čímž se zkracuje tit-for-tat rozběh, který je na víceuzlových I2P tunelech pomalejší                                                           |
| Determinismus      | Množina je čistou funkcí hashové hodnoty cíle + infohash, takže jakákoliv implementace vypočítá stejnou množinu — na rozdíl od IP-založeného BEP 6, kde může pohled odesílatele na IP příjemce lišit (NAT) |
| Ověřitelnost       | Přijímající protějšek zná svůj vlastní hash cíle a může množinu lokálně přepočítat a ověřit, čímž odhalí nekorektně se chovající odesílatele                                                     |
| Žádný IP mechanizmus | Žádné NAT průchody, zjišťování externí IP ani subnet heuristiky — všechno toto je na I2P nemožné nebo bez smyslu                                                                                  |
| Vázání identity    | Jedna povolená rychlá množina na jeden cíl. Uživatel s mnoha cíli získá jednu množinu pro každý — stejnou anti-abusivní vlastnost, kterou poskytovala IP maska na clearnetu                         |
| Soukromí           | Během výpočtu není nikdy přenášena ani naznačena žádná IP adresa                                                                                                                                |
| Šířka pásma        | „Mám vše“ / „Nemám nic“ nahrazuje celé bitové pole u velkých torrentů; Reject odstraňuje redundantní opakované požadavky                                                                        |
## Předpoklady pro implementaci

- **Identita protějšku**: hash cíle protějšku je získán ze streamovacího připojení (cíl relace) a je stejnou hodnotou, kterou používají obě strany. U odchozích připojení použijte cíl, ke kterému jste se připojili; u příchozích připojení použijte cíl, ze kterého připojení přišlo.
- **Vyjednávání**: pošlete `reserved[7] |= 0x04` ve handshake; zprávy Fast Extension posílejte pouze tehdy, byl-li bit nastaven i handshake protějšku; pokud protějšek pošle zprávy Fast Extension bez vyjednání, připojení ukončete.
- **Mám vše / Nemám nic**: hned po handshake pošlete přesně jednu z možností bitfield / Mám vše / Nemám nic. U seedů pošlete „Mám vše“, u ostatních „Nemám nic“, dokud nedostanete první část.
- **Strana odesílání Allowed Fast**: inzerujte pouze části, které skutečně máte; příjemce je může požadovat i když je dusí (choked). Omezte *servírovanou* množinu (např. odmítněte požadavky allowed-fast od protějšku, který již drží více než `k` částí, dle doporučení BEP 6).
- **Strana příjmu Allowed Fast**: množinu uložte; umožněte požadavky na tyto části i když dusíte; volitelně množinu ověřte přepočítáním z vlastního hash cíle a infohash, a ignorujte části, které nejsou ve vypočtené množině.
- **Reject**: každý požadavek musí získat přesně jednu odpověď; při dusení odmítněte všechny požadavky, které nejsou v množině allowed fast, namísto toho, aby byl protějšek beze slova ignorován.
- **Velikost množiny**: pro kompatibilitu použijte `k = 10`; klienti si mohou zvolit nižší `k` při zátěži, ale obě strany by měly inzerovat pouze to, co skutečně poskytují.
- **Omezení části**: `index = y % sz` musí používat celkový počet částí torrentu `sz`; ignorujte indexy >= sz (preventivně), protože řetěz hash není omezen rozsahem částí.
- **Zpětná kompatibilita**: klienti, kteří nevyjednají fast bit, jednoduše nikdy tyto zprávy nevidí; žádné další změny protokolu nejsou vyžadovány.

## Referenční implementace

Algoritmus je malý a samostatný – několik desítek řádků v libovolném jazyce. Všechny tři níže uvedené příklady počítají stejnou množinu pro stejné vstupy (`hash[0:4] ++ infohash`, řetězec SHA1, `y % sz`, s omezením `k = 10`).

### Java

```java
// I2P: peer.getPeerID().getDestHash() is the 32-byte destination hash.
// Big-endian word reads build each candidate piece index from the SHA1 chain.
import java.security.MessageDigest;
import java.util.HashSet;
import java.util.Set;

public static Set<Integer> generateAllowedFastSet(byte[] destHash, byte[] infohash, int pieces) {
    Set<Integer> rv = new HashSet<>(10);
    if (destHash == null || infohash == null || pieces <= 0) {
        return rv;
    }
    byte[] x = new byte[24];
    System.arraycopy(destHash, 0, x, 0, 4);          // 4 hash bytes, no IP, no zeroed 4th byte
    System.arraycopy(infohash, 0, x, 4, Math.min(20, infohash.length));
    MessageDigest md = MessageDigest.getInstance("SHA-1");
    while (rv.size() < 10) {
        x = md.digest(x);
        for (int i = 0; i < 5 && rv.size() < 10; i++) {
            long y = ((x[i * 4] & 0xFFL) << 24) | ((x[i * 4 + 1] & 0xFFL) << 16)
                   | ((x[i * 4 + 2] & 0xFFL) << 8) | (x[i * 4 + 3] & 0xFFL);
            rv.add((int) (y % pieces));
        }
    }
    return rv;
}
```
### C++

```cpp
// Peer identity input is the 32-byte destination hash available on the connection.
#include <cstdint>
#include <set>
#include <vector>

extern std::vector<uint8_t> sha1(const std::vector<uint8_t>& in); // e.g. OpenSSL SHA1()

std::set<int> generate_allowed_fast_set(const std::vector<uint8_t>& dest_hash,
                                        const std::vector<uint8_t>& infohash,
                                        int pieces) {
    std::set<int> rv;
    if (dest_hash.size() < 4 || infohash.size() < 20 || pieces <= 0) { return rv; }
    std::vector<uint8_t> x(dest_hash.begin(), dest_hash.begin() + 4); // 4 hash bytes,
                                                                      // no IP mask
    x.insert(x.end(), infohash.begin(), infohash.begin() + 20);
    while (rv.size() < 10) {
        x = sha1(x);
        for (int i = 0; i < 5 && rv.size() < 10; i++) {
            uint32_t y = (uint32_t(x[i * 4]) << 24) | (uint32_t(x[i * 4 + 1]) << 16) |
                         (uint32_t(x[i * 4 + 2]) << 8) | uint32_t(x[i * 4 + 3]);
            rv.insert(int(y % uint32_t(pieces)));
        }
    }
    return rv;
}
```
### Python

```python
import hashlib

def generate_allowed_fast_set(dest_hash: bytes, infohash: bytes, pieces: int) -> set:
    """4 bytes of the destination hash stand in for the masked IP; no byte is zeroed."""
    rv = set()
    if len(dest_hash) < 4 or len(infohash) < 20 or pieces <= 0:
        return rv
    x = dest_hash[:4] + infohash[:20]
    while len(rv) < 10:
        x = hashlib.sha1(x).digest()
        for i in range(5):
            if len(rv) >= 10:
                break
            y = int.from_bytes(x[i * 4 : i * 4 + 4], "big")
            rv.add(y % pieces)
    return rv
```
## Kompatibilita

- **Kompatibilní na úrovni vedení**: negociační bity a formáty zpráv jsou bajtově identické s clearnet BEP 6; liší se pouze vstup pro generování sady.
- **Neinteroperabilní napříč sítěmi**: klient I2P a klient clearnetu stejně nemohou navázat spojení; odchylka ovlivňuje pouze bajty identifikující peer, nikdy ne formát přenosu.
- **Uvnitř I2P**: všechny klienty implementující tuto výzvu počítají identické povolené rychlé sady a mohou je vzájemně poskytovat a ověřovat. Klienti, kteří ignorují Povolené rychlé, to považují za doporučení bez účinku a ztrácejí pouze výhodu při spuštění.

## Otevřené otázky

1. Má být velikost sady `k` pevně stanovena na 10, nebo by měla být přizpůsobivá podle zatížení (např. menší při vysoké zátěži požadavků), jak to umožňuje BEP 6?
2. Mají příjemci ověřovat sadu vůči své vlastní cílové hodnotě hash a zahazovat nesouladící indexy (ochrana proti chybným nebo zlomyslným odesílatelům)? Doporučuje se ano.
3. Vybrat 4bajtovou *předponu* (bajty 0–3) jako uvedeno, nebo poslední 4 bajty — jakékoli pevné 4bajtové okno poskytuje stejné vlastnosti; použití předpony zachovává přirozené pořadí bajtů ve vzorovém kódu (`hash[0:4]`).

## Předchozí technologie

- Reference: [BEP 6 Fast Extension](https://www.bittorrent.org/beps/bep_0006.html)
- Referenční implementace I2PSnark: `PeerState.sendAllowedFast()` /
  `generateAllowedFastSet()` v
  `apps/i2psnark/java/src/org/klomp/snark/PeerState.java` (@since 0.9.71+)
- Funguje ve spojení s BEP 40 (kanonická priorita peerů) a BEP 21 (částečné seedy), které jsou oba podporovány I2PSnark
