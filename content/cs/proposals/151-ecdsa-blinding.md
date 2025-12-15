---
title: "Zaslepení klíče ECDSA"
number: "151"
author: "orignal"
created: "2019-05-21"
lastupdated: "2019-05-29"
status: "Otevřeno"
thread: "http://zzz.i2p/topics/2717"
toc: true
---

## Motivace

Někteří lidé nemají rádi EdDSA nebo RedDSA. Měli bychom nabídnout nějaké alternativy a umožnit jim zaslepení podpisů ECDSA.

## Přehled

Tento návrh popisuje zaslepení klíčů pro typy podpisů ECDSA 1, 2, 3.

## Návrh

Funguje stejně jako RedDSA, ale vše je ve formátu Big Endian.
Jsou povoleny pouze stejné typy podpisů, např. 1->1, 2->2, 3->3.

### Definice

B
    Základní bod křivky

L
   Řád skupiny eliptické křivky. Vlastnost křivky.

DERIVE_PUBLIC(a)
    Převod soukromého klíče na veřejný, násobením B na eliptické křivce

alpha
    32-bajtové náhodné číslo známé těm, kdo znají cíl.

GENERATE_ALPHA(destination, date, secret)
    Generuje alpha pro aktuální datum, pro ty, kteří znají cíl a tajemství.

a
    Nezaslepený 32-bajtový podpisový soukromý klíč použitý k podepsání cíle

A
    Nezaslepený 32-bajtový podpisový veřejný klíč v cíli,
    = DERIVE_PUBLIC(a), na odpovídající křivce

a'
    Zaslepený 32-bajtový podpisový soukromý klíč použitý k podepsání šifrovaného leasesetu
    Toto je platný soukromý klíč ECDSA.

A'
    Zaslepený 32-bajtový podpisový veřejný klíč ECDSA v cíli,
    může být generován pomocí DERIVE_PUBLIC(a'), nebo z A a alpha.
    Toto je platný veřejný klíč ECDSA na křivce

H(p, d)
    Hash funkce SHA-256, která bere personalizační řetězec p a data d, a
    vytváří výstup o délce 32 bajtů.

    Použijte SHA-256 následovně::

        H(p, d) := SHA-256(p || d)

HKDF(salt, ikm, info, n)
    Kryptografická funkce pro odvození klíče, která bere vstupní materiál klíče ikm (který
    by měl mít dobrou entropii, ale není vyžadováno, aby byl jednotně náhodným řetězcem), sůl
    o délce 32 bajtů a kontextově specifické 'info', a vytváří výstup
    o n bajtech vhodný pro použití jako klíčový materiál.

    Použijte HKDF podle specifikace v [RFC-5869](https://tools.ietf.org/html/rfc5869), použitím hash funkce HMAC SHA-256
    podle specifikace v [RFC-2104](https://tools.ietf.org/html/rfc2104). To znamená, že SALT_LEN je maximálně 32 bajtů.

### Výpočty zaslepení

Každý den (UTC) musí být generován nový tajný alpha a zaslepené klíče.
Tajný alpha a zaslepené klíče se počítají následujícím způsobem.

GENERATE_ALPHA(destination, date, secret), pro všechny strany:

```text
// GENERATE_ALPHA(destination, date, secret)

  // tajemství je volitelné, jinak nulové
  A = veřejný podpisový klíč cíle
  stA = typ podpisu A, 2 bajty big endian (0x0001, 0x0002 nebo 0x0003)
  stA' = typ podpisu zaslepeného veřejného klíče A', 2 bajty big endian, vždy stejný jako stA
  keydata = A || stA || stA'
  datestring = 8 bajtů ASCII YYYYMMDD z aktuálního data UTC
  secret = UTF-8 kódovaný řetězec
  seed = HKDF(H("I2PGenerateAlpha", keydata), datestring || secret, "i2pblinding1", 64)
  // treat seed as a 64 byte big-endian value
  alpha = seed mod L
```


BLIND_PRIVKEY(), pro vlastníka publikujícího leaseset:

```text
// BLIND_PRIVKEY()

  alpha = GENERATE_ALPHA(destination, date, secret)
  a = soukromý podpisový klíč cíle
  // sčítání pomocí skalární aritmetiky
  zaslepený podpisový soukromý klíč = a' = BLIND_PRIVKEY(a, alpha) = (a + alpha) mod L
  zaslepený podpisový veřejný klíč = A' = DERIVE_PUBLIC(a')
```


BLIND_PUBKEY(), pro klienty stahující leaseset:

```text
// BLIND_PUBKEY()

  alpha = GENERATE_ALPHA(destination, date, secret)
  A = veřejný podpisový klíč cíle
  // sčítání pomocí prvků skupiny (bodů na křivce)
  zaslepený veřejný klíč = A' = BLIND_PUBKEY(A, alpha) = A + DERIVE_PUBLIC(alpha)
```


Obě metody výpočtu A' vedou ke stejnému výsledku, jak je požadováno.

## b33 adresa

Veřejný klíč ECDSA je pár (X,Y), takže pro P256, například, je to 64 bajtů, spíše než 32 jako pro RedDSA.
Buď adresa b33 bude delší, nebo může být veřejný klíč uložen v komprimovaném formátu jako v bitcoin peněženkách.

## Odkazy

* [RFC-2104](https://tools.ietf.org/html/rfc2104)
* [RFC-5869](https://tools.ietf.org/html/rfc5869)
