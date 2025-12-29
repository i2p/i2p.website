---
title: "Protokol Datagram2"
number: "163"
author: "zzz, orignal, drzed, eyedeekay"
created: "2023-01-24"
lastupdated: "2025-04-16"
status: "Uzavřeno"
thread: "http://zzz.i2p/topics/3540"
target: "0.9.66"
toc: true
---

## Stav

Schváleno při přezkumu 2025-04-15.
Změny začleněny do specifikací.
Implementováno v Java I2P od API 0.9.66.
Pro stav zkontrolujte implementační dokumentaci.

## Přehled

Vyjmuto z [Prop123](/proposals/123-new-netdb-entries/) jako samostatný návrh.

Offline podpisy nelze ověřit při zpracování odpověditelných datagramů.
Je třeba příznak pro označení offline podpisu, ale není místo pro umístění příznaku.

Bude vyžadovat zcela nové číslo a formát protokolu I2CP,
který bude přidán do specifikace [DATAGRAMS](/docs/api/datagrams/).
Nazvěme to "Datagram2".

## Cíle

- Přidat podporu offline podpisů
- Přidat ochranu proti replay útokům
- Přidat variantu bez podpisů
- Přidat příznaky a pole možností pro rozšiřitelnost

## Necíle

Úplná podpora end-to-end protokolu pro řízení přetížení atd.
To bude build nad nebo alternativou k Datagram2, který je protokolem na nižší úrovni.
Nebylo by rozumné navrhovat vysoce výkonný protokol pouze na vrcholu
Datagram2 kvůli poli "from" a režii podpisu.
Jakýkoli takový protokol by měl provést počáteční handshake s Datagram2 a poté
přepnout na nebalené datagramy (RAW).

## Motivace

Zůstává z práce na LS2, která byla jinak dokončena v roce 2019.

První aplikací, která by měla používat Datagram2, se očekává, že bude
bittorentové UDP oznamy, jak je implementováno v i2psnark a zzzot, viz [Prop160](/proposals/160-udp-trackers/).

## Specifikace odpověditelných datagramů

Pro informaci,
následuje přehled specifikace pro odpověditelné datagramy,
zkopírováno z [Datagrams](/docs/api/datagrams/).
Standardní I2CP číslo protokolu pro odpověditelné datagramy je PROTO_DATAGRAM (17).

```text
+----+----+----+----+----+----+----+----+
  | from                                  |
  +                                       +
  |                                       |
  ~                                       ~
  ~                                       ~
  |                                       |
  +                                       +
  |                                       |
  |                                       |
  +----+----+----+----+----+----+----+----+
  | signature                             |
  +                                       +
  |                                       |
  +                                       +
  |                                       |
  +                                       +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  | payload...
  +----+----+----+----//

  from :: `Destination`
          délka: 387+ bajtů
          Odesílatel a podepisovatel datagramu

  signature :: `Signature`
               Typ podpisu musí odpovídat typu veřejného klíče podepisujícího $from
               délka: 40+ bajtů, jak je uvedeno podle typu podpisu.
               U výchozího typu klíče DSA_SHA1:
                  DSA `Signature` SHA-256 hash payloadu.
               Pro ostatní typy klíčů:
                  `Signature` payloadu.
               Podpis může být ověřen veřejným klíčem podepisujícího $from

  payload ::  Data
              Délka: 0 až přibližně 31,5 KB (viz poznámky)

  Celková délka: Délka payloadu + 423+
```

## Návrh

- Definovat nový protokol 19 - Odpověditelný datagram s možnostmi.
- Definovat nový protokol 20 - Odpověditelný datagram bez podpisu.
- Přidat pole příznaků pro offline podpisy a budoucí rozšíření
- Přesunout podpis po payloadu pro snadnější zpracování
- Nová specifikace podpisu odlišná od odpověditelného datagramu nebo streamingu, aby
  ověření podpisu selhalo, pokud by byl interpretován jako odpověditelný datagram nebo streaming.
  Toho je dosaženo přesunutím podpisu po payloadu,
  a zahrnutím hashe cílového umístění do podpisové funkce.
- Přidat ochranu proti znovuvysílání pro datagramy, jak bylo provedeno v [Prop164](/proposals/164-streaming/) pro streaming.
- Přidat sekci pro libovolné možnosti
- Znovu použít formát offline podpisu z [Common](/docs/specs/common-structures/) a [Streaming](/docs/specs/streaming/).
- Sekce offline podpisu musí být před sekcemi proměnlivé délky
  payloadu a podpisu, jelikož specifikuje délku podpisu.

## Specifikace

### Protokol

Nové číslo I2CP protokolu pro Datagram2 je 19.
Přidat jako PROTO_DATAGRAM2 do [I2CP](/docs/specs/i2cp/).

Nové číslo I2CP protokolu pro Datagram3 je 20.
Přidat jako PROTO_DATAGRAM2 do [I2CP](/docs/specs/i2cp/).

### Formát Datagram2

Přidat Datagram2 do [DATAGRAMS](/docs/api/datagrams/) následujícím způsobem:

```text
+----+----+----+----+----+----+----+----+
  |                                       |
  ~            from                       ~
  ~                                       ~
  |                                       |
  +----+----+----+----+----+----+----+----+
  |  flags  |     options (optional)      |
  +----+----+                             +
  ~                                       ~
  ~                                       ~
  +----+----+----+----+----+----+----+----+
  |                                       |
  ~     offline_signature (optional)      ~
  ~   expires, sigtype, pubkey, offsig    ~
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  ~            payload                    ~
  ~                                       ~
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  ~            signature                  ~
  ~                                       ~
  |                                       |
  +----+----+----+----+----+----+----+----+

  from :: `Destination`
          délka: 387+ bajtů
          Odesílatel a (pokud není offline podepsán) podepisovatel datagramu

  flags :: (2 bajty)
           Pořadí bitů: 15 14 ... 3 2 1 0
           Bity 3-0: Verze: 0x02 (0 0 1 0)
           Bit 4: Pokud 0, žádné možnosti; pokud 1, mapování možností je přidáno
           Bit 5: Pokud 0, žádný offline podpis; pokud 1, offline podepsaný
           Bity 15-6: nevyužito, nastavit na 0 pro kompatibilitu s budoucími použitími

  options :: (2+ bajtů, pokud jsou přítomny)
           Pokud příznak naznačuje, že možnosti jsou přítomny, `Mapping`
           obsahující libovolné textové možnosti

  offline_signature ::
               Pokud příznak naznačuje offline klíče, sekce offline podpisu,
               jak je specifikováno v Common Structures Specification,
               s následujícími 4 poli. Délka: liší se podle typů online a offline
               podpisů, obvykle 102 bajtů pro Ed25519
               Tato sekce může a měla by být generována offline.

    expires :: Expirace časového razítka
               (4 bajty, big endian, sekundy od epocy, přeteče v roce 2106)

    sigtype :: Přechodný typ podpisu (2 bajty, big endian)

    pubkey :: Přechodný veřejný klíč podepisování (délka jak je uvedeno podle typu podpisu),
              obvykle 32 bajtů pro typ podpisu Ed25519.

    offsig :: `Signature`
              Podpis časového razítka expirace, přechodného typu podpisu,
              a veřejného klíče, veřejným klíčem destinace,
              délka: 40+ bajtů, jak je uvedeno podle typu podpisu, obvykle
              64 bajtů pro typ podpisu Ed25519.

  payload ::  Data
              Délka: 0 až cca 61 KB (viz poznámky)

  signature :: `Signature`
               Typ podpisu musí odpovídat typu veřejného klíče podepisujícího $from
               (pokud není offline podepsán) nebo přechodnému typu podpisu
               (pokud je offline podepsán)
               délka: 40+ bajtů, jak je uvedeno podle typu podpisu, obvykle
               64 bajtů pro typ podpisu Ed25519.
               `Signature` payloadu a dalších polí, jak je uvedeno níže.
               Podpis je ověřen veřejným klíčem podepisujícího $from
               (pokud není offline podepsán) nebo přechodným veřejným klíčem
               (pokud je offline podepsán)

```

Celková délka: minimálně 433 + délka payloadu;
typická délka pro odesílatele X25519 a bez offline podpisů:
457 + délka payloadu.
Upozorňujeme, že zpráva bude obvykle komprimována pomocí gzip ve vrstvě I2CP,
což povede k významným úsporám, pokud je z destinace compressovatelná.

Poznámka: Formát offline podpisu je stejný jako ve specifikaci Common Structures [Common](/docs/specs/common-structures/) a [Streaming](/docs/specs/streaming/).

### Podpisy

Podpis je nad následujícími poli.

- Prelude: 32bajtový hash cílové destinace (není zahrnuto v datagramu)
- flags
- options (pokud jsou přítomny)
- offline_signature (pokud je přítomen)
- payload

U odpověditelného datagramu, pro typ klíče DSA_SHA1, byl podpis nad
SHA-256 hash payloadu, nikoli nad payloadem samotným; zde je podpis
vždy nad obsaženými poli (NE hash), bez ohledu na typ klíče.

### Ověření ToHash

Příjemci musí ověřit podpis (používající jejich hash destinace)
a zahodit datagram při selhání, aby se zabránilo znovuvysílání.

### Formát Datagram3

Přidat Datagram3 do [DATAGRAMS](/docs/api/datagrams/) následujícím způsobem:

```text
+----+----+----+----+----+----+----+----+
  |                                       |
  ~            fromhash                   ~
  ~                                       ~
  |                                       |
  +----+----+----+----+----+----+----+----+
  |  flags  |     options (optional)      |
  +----+----+                             +
  ~                                       ~
  ~                                       ~
  +----+----+----+----+----+----+----+----+
  |                                       |
  ~            payload                    ~
  ~                                       ~
  |                                       |
  +----+----+----+----+----+----+----+----+

  fromhash :: `Hash`
              délka: 32 bajtů
              Odesílatel datagramu

  flags :: (2 bajty)
           Pořadí bitů: 15 14 ... 3 2 1 0
           Bity 3-0: Verze: 0x03 (0 0 1 1)
           Bit 4: Pokud 0, žádné možnosti; pokud 1, mapování možností je přidáno
           Bity 15-5: nevyužito, nastavit na 0 pro kompatibilitu s budoucími použitími

  options :: (2+ bajtů, pokud jsou přítomny)
           Pokud příznak naznačuje, že možnosti jsou přítomny, `Mapping`
           obsahující libovolné textové možnosti

  payload ::  Data
              Délka: 0 až cca 61 KB (viz poznámky)

```

Celková délka: minimálně 34 + délka payloadu.

### SAM

Přidat STYLE=DATAGRAM2 a STYLE=DATAGRAM3 do specifikace SAMv3.
Aktualizovat informace o offline podpisech.

### Režie

Tento návrh přidává 2 bajty režie do odpověditelných datagramů pro příznaky.
To je přijatelné.

## Bezpečnostní analýza

Zahrnutí hash cíle do podpisu by mělo být účinné při předcházení znovuvysílacím útokům.

Formát Datagram3 neobsahuje podpisy, takže odesílatel nemůže být ověřen,
a jsou možné útoky typu znovuvysílání. Jakékoli potřebné ověřování musí být provedeno na aplikační úrovni
nebo routerem na vrstvě katrice.

## Poznámky

- Praktická délka je omezena nižšími vrstvami protokolů - specifikace zprávy tunelu [TUNMSG](/docs/specs/implementation/#notes)
  omezuje zprávy na přibližně 61,2 KB a aktuální transporty
  [TRANSPORT](/docs/overview/transport/) omezují zprávy na přibližně 64 KB, takže délka dat zde
  je omezena na přibližně 61 KB.
- Viz důležité poznámky o spolehlivosti velkých datagramů [API](/docs/api/datagrams/). Pro
  nejlepší výsledek, omezte payload na přibližně 10 KB nebo méně.

## Kompatibilita

Žádná. Aplikace musí být přepsány tak, aby směrovaly zprávy I2CP protokolu Datagram2
podle protokolu a/nebo portu.
Zprávy Datagram2, které jsou chybně směrovány a interpretovány jako
Odpověditelné datagramy nebo streamingové zprávy, selžou na základě podpisu, formátu nebo obou.

## Migrace

Každá UDP aplikace musí samostatně detekovat podporu a migrovat.
Nejvýraznější UDP aplikací je bittorrent.

### Bittorrent

Bittorrent DHT: Pravděpodobně potřebuje rozšíření příznaku,
např. i2p_dg2, koordinace s BiglyBT

Bittorrent UDP Oznámení [Prop160](/proposals/160-udp-trackers/): Design od počátku.
Koordinace s BiglyBT, i2psnark, zzzot

### Ostatní

Bote: Nepravděpodobné, že se přistěhuje, není aktivně udržováno

Streamr: Nikdo jej nepoužívá, žádná migrace neplánovaná

SAM UDP aplikace: Žádné známé

## Reference

* [API](/docs/api/datagrams/)
* [BT-SPEC](/docs/applications/bittorrent/)
* [Common](/docs/specs/common-structures/)
* [DATAGRAMS](/docs/api/datagrams/)
* [I2CP](/docs/specs/i2cp/)
* [Prop123](/proposals/123-new-netdb-entries/)
* [Prop160](/proposals/160-udp-trackers/)
* [Prop164](/proposals/164-streaming/)
* [Streaming](/docs/specs/streaming/)
* [TRANSPORT](/docs/overview/transport/)
* [TUNMSG](/docs/specs/implementation/#notes)
