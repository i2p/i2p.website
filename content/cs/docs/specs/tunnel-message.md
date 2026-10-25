---
title: "Specifikace zpráv tunnel"
description: "Specifikace pro formát tunnel zpráv v I2P"
slug: "tunnel-message"
aliases:
  - "/cs/docs/legacy/tunnel-message"
  - "/cs/docs/legacy/tunnel-message/"
  - "/cs/tunnel_message_spec"
  - "/cs/tunnel_message_spec/"
category: "Návrh"
lastUpdated: "2021-01"
accurateFor: "0.9.49"
---

## Přehled

Tento dokument specifikuje formát tunnel zpráv. Pro obecné informace o tunnelech viz [dokumentace tunnelů](/docs/specs/tunnel-implementation).

## Předběžné zpracování zpráv

*Tunnel gateway* (brána tunelu) je vstup, neboli první skok tunelu. Pro odchozí tunel je gateway tvůrce tunelu. Pro příchozí tunel je gateway na opačném konci od tvůrce tunelu.

Gateway *předzpracovává* [I2NP](/docs/specs/i2np) zprávy jejich fragmentací a kombinováním do tunnel zpráv.

Zatímco I2NP zprávy mají proměnlivou velikost od 0 do téměř 64 KB, tunnel zprávy mají pevnou velikost, přibližně 1 KB. Pevná velikost zpráv omezuje několik typů útoků, které jsou možné pozorováním velikosti zpráv.

Poté, co jsou vytvořeny zprávy tunelu, jsou šifrovány podle popisu v [dokumentaci tunelu](/docs/specs/tunnel-implementation).

### Tunnel Message (Zašifrovaná)

Toto je obsah tunnel data zprávy po zašifrování.

```
+----+----+----+----+----+----+----+----+
|    Tunnel ID      |       IV          |
+----+----+----+----+                   +
|                                       |
+                   +----+----+----+----+
|                   |                   |
+----+----+----+----+                   +
|                                       |
+           Encrypted Data              +
~                                       ~
|                                       |
+                   +-------------------+
|                   |
+----+----+----+----+
```
**Tunnel ID** :: [TunnelId](/docs/specs/common-structures#tunnelid) : 4 bajty. ID dalšího skoku, nenulové.

**IV** :: : 16 bajtů. Inicializační vektor.

**Encrypted Data** :: : 1008 bytů. Šifrovaná zpráva tunelu.

**Celková velikost: 1028 bajtů**

### Zpráva tunelu (dešifrovaná)

Toto je obsah zprávy s daty tunnel po dešifrování.

```
+----+----+----+----+----+----+----+----+
|    Tunnel ID      |       IV          |
+----+----+----+----+                   +
|                                       |
+                   +----+----+----+----+
|                   |     Checksum      |
+----+----+----+----+----+----+----+----+
|          nonzero padding...           |
~                                       ~
|                                       |
+                                  +----+
|                                  |zero|
+----+----+----+----+----+----+----+----+
|                                       |
|       Delivery Instructions  1        |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|                                       |
+       I2NP Message Fragment 1         +
|                                       |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|                                       |
|       Delivery Instructions 2...      |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|                                       |
+       I2NP Message Fragment 2...      +
|                                       |
~                                       ~
|                                       |
+                   +-------------------+
|                   |
+----+----+----+----+
```
**Tunnel ID** :: [TunnelId](/docs/specs/common-structures#tunnelid) : 4 bajty. ID dalšího přeskoču, nenulové.

**IV** :: : 16 bytů. Inicializační vektor.

**Checksum** :: : 4 bajty. Prvních 4 bajtů SHA256 hash z (obsahu zprávy (po nulovém bajtu) + IV).

**Nenulové vyplnění** :: : 0 nebo více bajtů. Náhodná nenulová data pro vyplnění.

**Zero** :: : 1 bajt. Hodnota 0x00.

**Instrukce doručení** :: TunnelMessageDeliveryInstructions : Délka se liší, ale typicky je 7, 39, 43 nebo 47 bajtů. Označuje fragment a směrování pro fragment.

**Message Fragment** :: : 1 až 996 bajtů, skutečné maximum závisí na velikosti instrukce doručení. Částečná nebo úplná I2NP zpráva.

**Celková velikost: 1028 bajtů**

#### Poznámky

- Výplň, pokud existuje, musí být před páry instrukce/zpráva. Neexistuje žádné ustanovení pro výplň na konci.
- Kontrolní součet NEPOKRÝVÁ výplň ani nulový byte. Vezměte zprávu začínající prvními instrukcemi doručení, spojte ji s IV a vypočítejte z toho Hash.

## Pokyny pro doručování zpráv v tunelu

Instrukce jsou kódovány jediným řídicím bajtem, následovaným jakýmikoli potřebnými dodatečnými informacemi. První bit (MSB) v tomto řídicím bajtu určuje, jak se interpretuje zbytek hlavičky - pokud není nastaven, zpráva buď není fragmentována nebo se jedná o první fragment ve zprávě. Pokud je nastaven, jedná se o následující fragment.

Tato specifikace je pouze pro Delivery Instructions uvnitř Tunnel Messages. Poznámka: "Delivery Instructions" se také používají uvnitř Garlic Cloves, kde je formát výrazně odlišný. Podrobnosti najdete v [I2NP dokumentaci](/docs/specs/i2np#garlicclovedeliveryinstructions). NEPOUŽÍVEJTE následující specifikaci pro Garlic Clove Delivery Instructions!

### Instrukce pro doručení prvního fragmentu

Pokud je MSB prvního bajtu 0, jedná se o počáteční fragment I2NP zprávy, nebo o úplnou (nefragmentovanou) I2NP zprávu, a instrukce jsou:

```
+----+----+----+----+----+----+----+----+
|flag|  Tunnel ID (opt)  |              |
+----+----+----+----+----+              +
|                                       |
+                                       +
|         To Hash (optional)            |
+                                       +
|                                       |
+                        +--------------+
|                        |dly | Message
+----+----+----+----+----+----+----+----+
 ID (opt) |extended opts (opt)|  size   |
+----+----+----+----+----+----+----+----+
```
**flag** :: : 1 byte. Pořadí bitů: 76543210   - bit 7: 0 pro specifikaci počátečního fragmentu nebo nefragmentované zprávy   - bity 6-5: typ doručení

    - 0x0 = LOCAL
    - 0x01 = TUNNEL
    - 0x02 = ROUTER
    - 0x03 = unused, invalid
    - Note: LOCAL is used for inbound tunnels only, unimplemented for outbound tunnels
- bit 4: zpoždění zahrnuto? Neimplementováno, vždy 0. Pokud 1, je zahrnut byte zpoždění.
  - bit 3: fragmentováno? Pokud 0, zpráva není fragmentována, následuje celá zpráva. Pokud 1, zpráva je fragmentována a instrukce obsahují Message ID.
  - bit 2: rozšířené možnosti? Neimplementováno, vždy 0. Pokud 1, jsou zahrnuty rozšířené možnosti.
  - bity 1-0: rezervováno, nastaveno na 0 pro kompatibilitu s budoucím použitím

**Tunnel ID** :: [TunnelId](/docs/specs/common-structures#tunnelid) : 4 bajty. Volitelné, přítomné pokud je typ doručení TUNNEL. ID cílového tunnelu, nenulové.

**To Hash** :: : 32 bajtů. Volitelné, přítomné pokud je typ doručení ROUTER nebo TUNNEL. Pokud ROUTER, SHA256 hash routeru. Pokud TUNNEL, SHA256 hash gateway routeru.

**Delay** :: : 1 bajt. Volitelný, přítomen pokud je nastaven příznak pro zahrnutí zpoždění. V tunnel zprávách: Neimplementováno, nikdy není přítomen; původní specifikace: bit 7: typ (0 = přísný, 1 = randomizovaný), bity 6-0: exponent zpoždění (2^hodnota minut).

**Message ID** :: : 4 bajty. Volitelné, přítomné pokud je tato zpráva první ze 2 nebo více fragmentů (tj. pokud je bit fragmentace 1). ID, které jednoznačně identifikuje všechny fragmenty jako náležející k jedné zprávě (současná implementace používá I2NPMessageHeader.msg_id).

**Rozšířené možnosti** :: : 2 nebo více bajtů. Volitelné, přítomné pokud je nastaven příznak rozšířených možností. Neimplementováno, nikdy není přítomné; původní specifikace: Jeden bajt délky a pak tolik bajtů.

**size** :: : 2 bajty. Délka fragmentu, který následuje. Platné hodnoty: 1 až přibližně 960 v tunnel zprávě.

**Celková délka:** Typická délka je: - 3 bajty pro LOCAL doručení (tunnel zpráva) - 35 bajtů pro ROUTER doručení nebo 39 bajtů pro TUNNEL doručení (nefragmentovaná tunnel zpráva) - 39 bajtů pro ROUTER doručení nebo 43 bajty pro TUNNEL doručení (první fragment)

### Instrukce pro doručování navazujících fragmentů

Pokud je MSB prvního bajtu 1, jedná se o následující fragment a instrukce jsou:

```
+----+----+----+----+----+----+----+
|frag|     Message ID    |  size   |
+----+----+----+----+----+----+----+
```
**frag** :: : 1 byte. Pořadí bitů: 76543210. Binární 1nnnnnnd:   - bit 7: 1 pro označení, že se jedná o následující fragment   - bity 6-1: nnnnnn je 6bitové číslo fragmentu od 1 do 63   - bit 0: d je 1 pro označení posledního fragmentu, jinak 0

**Message ID** :: : 4 bajty. Identifikuje sekvenci fragmentů, ke které tento fragment patří. Bude odpovídat message ID počátečního fragmentu (fragment s příznakovým bitem 7 nastaveným na 0 a příznakovým bitem 3 nastaveným na 1).

**size** :: : 2 bajty. Délka fragmentu, který následuje. Platné hodnoty: 1 až 996.

**Celková délka: 7 bajtů**

## Poznámky

### Maximální velikost I2NP zprávy

Zatímco maximální velikost I2NP zprávy je nominálně 64 KB, velikost je dále omezena způsobem fragmentace I2NP zpráv na více 1 KB tunnel zpráv. Maximální počet fragmentů je 64 a počáteční fragment nemusí být dokonale zarovnán na začátku tunnel zprávy. Zpráva tedy musí nominálně vejít do 63 fragmentů.

Maximální velikost počátečního fragmentu je 956 bajtů (za předpokladu režimu doručení TUNNEL); maximální velikost následujícího fragmentu je 996 bajtů. Proto je maximální velikost přibližně 956 + (62 * 996) = 62708 bajtů, nebo 61,2 KB.

### Řazení, seskupování, balení

Tunnel zprávy mohou být zahozeny nebo přeuspořádány. Tunnel gateway, který vytváří tunnel zprávy, může volně implementovat jakoukoliv strategii dávkování, míchání nebo přeuspořádávání pro fragmentaci I2NP zpráv a efektivní zabalení fragmentů do tunnel zpráv. Obecně není možné dosáhnout optimálního zabalení ("problém balení"). Gateway mohou implementovat různé strategie zpoždění a přeuspořádávání.

### Krycí provoz

Zprávy tunnel mohou obsahovat pouze výplň (tj. žádné doručovací instrukce nebo fragmenty zpráv vůbec) pro krycí provoz. Toto není implementováno.

## Reference

- **[I2NP]** [I2NP Protocol](/docs/specs/i2np)
- **[I2NP-GC]** [GarlicClove](/docs/specs/i2np#garlicclove)
- **[I2NP-GCDI]** [GarlicCloveDeliveryInstructions](/docs/specs/i2np#garlicclovedeliveryinstructions)
- **[TUNNEL-IMPL]** [Implementace tunelu](/docs/specs/tunnel-implementation)
