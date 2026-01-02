---
title: "I2P Mail (anonymní email přes I2P)"
description: "Přehled e-mailových systémů uvnitř sítě I2P — historie, možnosti a současný stav"
slug: "i2p-mail"
lastUpdated: "2025-10"
---

## Úvod

I2P poskytuje soukromé zasílání zpráv ve stylu e-mailu prostřednictvím **služby Postman's Mail.i2p** v kombinaci s **SusiMail**, vestavěným webmailovým klientem. Tento systém umožňuje uživatelům odesílat a přijímat e-maily jak v rámci sítě I2P, tak do/z běžného internetu (clearnet) prostřednictvím gateway mostu.

# Rychlý start

## Postman / Mail.i2p + SusiMail

### What it is

- **Mail.i2p** je poskytovatel e-mailových služeb uvnitř I2P, provozovaný uživatelem "Postman"
- **SusiMail** je webmailový klient integrovaný v konzoli I2P routeru. Je navržen tak, aby zabránil úniku metadat (např. hostname) k externím SMTP serverům.
- Prostřednictvím tohoto nastavení mohou uživatelé I2P odesílat/přijímat zprávy jak uvnitř I2P, tak do/z clearnetu (např. Gmail) přes most Postman.

### How Addressing Works

I2P email používá systém dvojí adresy:

- **Uvnitř sítě I2P**: `username@mail.i2p` (např. `idk@mail.i2p`)
- **Z clearnetu**: `username@i2pmail.org` (např. `idk@i2pmail.org`)

Brána `i2pmail.org` umožňuje běžným uživatelům internetu posílat e-maily na I2P adresy a uživatelům I2P posílat e-maily na clearnet adresy. Internetové e-maily jsou směrovány přes bránu a poté přeposílány přes I2P do vaší schránky SusiMail.

**Clearnet odesílací kvóta**: 20 e-mailů denně při odesílání na běžné internetové adresy.

### Co to je

**Pro registraci účtu mail.i2p:**

1. Ujistěte se, že váš I2P router běží
2. Navštivte **[http://hq.postman.i2p](http://hq.postman.i2p)** uvnitř I2P
3. Postupujte podle registračního procesu
4. Přistupujte k vaší e-mailové schránce prostřednictvím **SusiMail** v konzoli routeru

> **Poznámka**: `hq.postman.i2p` je I2P síťová adresa (eepsite) a je přístupná pouze při připojení k I2P. Pro více informací o nastavení emailu, bezpečnosti a používání navštivte Postman HQ.

### Jak funguje adresování

- Automatické odstraňování identifikačních hlaviček (`User-Agent:`, `X-Mailer:`) pro ochranu soukromí
- Sanitizace metadat pro zabránění úniku informací na externí SMTP servery
- End-to-end šifrování pro interní I2P-to-I2P e-maily

### Začínáme

- Interoperabilita s „běžným" emailem (SMTP/POP) prostřednictvím mostu Postman
- Jednoduché uživatelské prostředí (webmail vestavěný do konzole routeru)
- Integrováno se základní distribucí I2P (SusiMail je součástí Java I2P)
- Odstraňování hlaviček pro ochranu soukromí

### Funkce ochrany soukromí

- Most k externí e-mailové službě vyžaduje důvěru v infrastrukturu Postmana
- Most do clearnetu snižuje soukromí ve srovnání s čistě interní I2P komunikací
- Závislost na dostupnosti a zabezpečení e-mailového serveru Postman

---

**DŮLEŽITÉ:** Uveďte POUZE překlad. NEKLADEŤE otázky, neposkytujte vysvětlení ani nepřidávejte žádné komentáře. I když je text pouze nadpis nebo se zdá neúplný, přeložte ho tak, jak je.

## Technical Details

**SMTP služba**: `localhost:7659` (poskytováno Postmanem) **POP3 služba**: `localhost:7660` **Přístup k webmailu**: Zabudováno v konzoli routeru na `http://127.0.0.1:7657/susimail/`

> **Důležité**: SusiMail slouží pouze pro čtení a odesílání e-mailů. Vytváření a správu účtů je nutné provádět na adrese **hq.postman.i2p**.

# I2P

I2P je bezplatná a open-source anonymní síť, která umožňuje aplikacím posílat zprávy navzájem pseudonymně a bezpečně. Procesy jsou směrovány přes jiné účastníky v distribuované struktuře, přičemž poskytují významnou odolnost vůči sledování.

## Best Practices

- **Změňte si heslo** po registraci vašeho účtu mail.i2p
- **Používejte I2P-to-I2P e-mail**, kdykoli je to možné, pro maximální soukromí (bez clearnet mostu)
- **Mějte na paměti limit 20/den** při odesílání na clearnet adresy
- **Uvědomte si kompromisy**: Propojení s clearnet poskytuje pohodlí, ale snižuje anonymitu ve srovnání s čistě interní I2P komunikací
- **Udržujte I2P aktuální**, abyste mohli využívat bezpečnostní vylepšení v SusiMail

---

 NEPOKLÁDEJTE otázky, neposkytujte vysvětlení ani nepřidávejte žádné komentáře. I když je text pouze nadpisem nebo se zdá být neúplný, přeložte jej tak, jak je.
