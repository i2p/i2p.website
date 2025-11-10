---
title: "Nové I2P routery"
date: 2025-10-16
author: "idk"
categories: ["community"]
description: "Objevuje se několik nových implementací I2P routeru, včetně projektu emissary v Rustu a go-i2p v Go, které přinášejí nové možnosti pro integraci (embedding) a diverzitu sítě."
---

Je to vzrušující období pro vývoj I2P, naše komunita roste a na scéně se nyní objevuje hned několik nových, plně funkčních prototypů I2P routerů! Z tohoto vývoje jsme nadšení a těší nás, že se s vámi můžeme podělit o tyto novinky.

## Jak to pomáhá síti?

Psaní I2P routers nám pomáhá dokázat, že naše specifikační dokumenty lze použít k vytváření nových I2P routers, otevírá kód novým analytickým nástrojům a obecně zlepšuje bezpečnost a interoperabilitu sítě. Více I2P routers znamená, že potenciální chyby nejsou jednotné; útok na jeden router nemusí fungovat na jiný router, což pomáhá vyhnout se problému monokultury. Možná je však z dlouhodobého hlediska nejzajímavější vyhlídkou zabudování.

## Co je to vkládání?

V kontextu I2P je embedding (vestavění) způsob, jak přímo zahrnout I2P router do jiné aplikace, aniž by byl vyžadován samostatný router běžící na pozadí. Tímto způsobem můžeme I2P učinit snáze použitelným, což usnadňuje růst sítě díky zpřístupnění softwaru. Java i C++ trpí tím, že se mimo své vlastní ekosystémy obtížně používají; C++ vyžaduje křehké ručně psané vazby (bindings) v jazyce C a v případě Javy pak přicházejí obtíže s komunikací s aplikací pro JVM z aplikace, která na JVM neběží.

Ačkoli je tato situace v mnoha ohledech poměrně běžná, věřím, že ji lze zlepšit, aby bylo I2P přístupnější. Jiné jazyky nabízejí elegantnější řešení těchto problémů. Samozřejmě bychom měli vždy brát v potaz a používat stávající pokyny pro Java a C++ routers.

## vyslanec se vynoří z temnoty

Zcela nezávisle na našem týmu vyvinul vývojář jménem altonen implementaci I2P v jazyce Rust s názvem emissary. Přestože je stále poměrně nový a s jazykem Rust nemáme velké zkušenosti, tento fascinující projekt má velký potenciál. Gratulujeme altonenovi k vytvoření emissary, udělalo to na nás velký dojem.

### Why Rust?

Hlavní důvod používat Rust je v zásadě stejný jako důvod používat Javu nebo Go. Rust je kompilovaný programovací jazyk se správou paměti a obrovskou a velmi nadšenou komunitou. Rust také nabízí pokročilé možnosti pro vytváření bindings (propojovacích vazeb) k programovacímu jazyku C, které mohou být snazší na údržbu než v jiných jazycích, a přitom dědí silné záruky bezpečnosti paměti jazyka Rust.

### Do you want to get involved with emissary?

emissary je vyvíjen na Githubu uživatelem altonen. Repozitář najdete zde: [altonen/emissary](https://github.com/altonen/emissary). Rust také trpí nedostatkem ucelených klientských knihoven pro SAMv3, které jsou kompatibilní s oblíbenými síťovými knihovnami a nástroji pro Rust; psaní knihovny pro SAMv3 je skvělý způsob, jak začít.

## go-i2p is getting closer to completion

Přibližně tři roky pracuji na go-i2p a snažím se proměnit začínající knihovnu v plnohodnotný I2P router v čistém jazyce Go, což je další paměťově bezpečný jazyk. Za posledních zhruba šest měsíců byla zásadně přepracována, aby se zlepšil výkon, spolehlivost a udržovatelnost.

### Why Go?

Ačkoli Rust a Go sdílejí mnoho stejných výhod, Go je v mnoha ohledech mnohem snazší se naučit. Už řadu let existují v programovacím jazyce Go vynikající knihovny a aplikace pro používání I2P, včetně nejúplnějších implementací knihoven SAMv3.3. Bez I2P routeru, který můžeme spravovat automaticky (například vestavěný router), to však pro uživatele stále představuje překážku. Cílem go-i2p je tuto mezeru překlenout a odstranit všechny zbytečné komplikace pro vývojáře aplikací pro I2P, kteří pracují v Go.

### Proč Rust?

go-i2p je vyvíjeno na Githubu, v současnosti především uživatelem eyedeekay, a je otevřené příspěvkům komunity na [go-i2p](https://github.com/go-i2p/). V tomto jmenném prostoru existuje mnoho projektů, například:

#### Router Libraries

Tyto knihovny jsme vytvořili, abychom na nich postavili knihovny našeho I2P routeru. Jsou rozděleny do více specializovaných repozitářů, aby se usnadnila revize a aby byly užitečné i pro další lidi, kteří chtějí stavět experimentální, vlastní I2P routery.

- [go-i2p the router itself, most active right now](https://github.com/go-i2p/go-i2p)
- [common our core library for I2P datastructures](https://github.com/go-i2p/common)
- [crypto our library for cryptographic operations](https://github.com/go-i2p/crypto)
- [go-noise a library for implementing noise-based connections](https://github.com/go-i2p/go-noise)
- [noise a low-level library for using the Noise framework](https://github.com/go-i2p/noise)
- [su3 a library for manipulating su3 files](https://github.com/go-i2p/su3)

#### Client libraries

- [onramp a very convenient library for using(or combining) I2P and Tor](https://github.com/go-i2p/onramp)
- [go-sam-go an advanced, efficient, and very complete SAMv3 library](https://github.com/go-i2p/go-sam-go)

## If you don't like Go or Rust and are thinking of writing an I2P Router, what should you do?

No, existuje neaktivní projekt na napsání [I2P router v C#](https://github.com/PeterZander/i2p-cs), pokud chcete provozovat I2P na XBoxu. Ve skutečnosti to zní docela dobře. Pokud ani to není podle vašich představ, můžete to udělat jako altonen a vyvinout úplně nový.

### Chcete se zapojit do emissary?

I2P router můžete napsat z jakéhokoli důvodu, je to svobodná síť, ale pomůže, když budete vědět proč. Je nějaká komunita, kterou chcete posílit, nástroj, o kterém si myslíte, že se k I2P dobře hodí, nebo strategie, kterou chcete vyzkoušet? Určete si, jaký máte cíl, abyste věděli, kde máte začít, a jak bude vypadat "dokončený" stav.

### Decide what language you want to do it in and why

Zde je několik důvodů, proč byste si mohli vybrat jazyk:

- **C**: No need for binding-generation, supported everywhere, can be called from any language, lingua franca of modern computing
- **Typescript**: Massive community, lots of applications, services, and libraries, works with node and deno, seems like it's everywhere right now
- **D**: It's memory safe and not Rust or Go
- **Vala**: It emits C code for the target platform, combining some of the advantages of memory-safe languages with the flexibility of C
- **Python**: Everybody uses Python

Ale zde je několik důvodů, proč byste si tyto jazyky možná nevybrali:

- **C**: Memory management can be challenging, leading to impactful bugs
- **Typescript**: TypeScript is transpiled to JavaScript, which is interpreted and may impact performance
- **D**: Relatively small community
- **Vala**: Not a lot of underlying infrastructure in Vala, you end up using C versions of most libraries
- **Python**: It's an interpreted language which may impact performance

Existují stovky programovacích jazyků a ve všech z nich vítáme udržované I2P knihovny a routers. Volte kompromisy s rozmyslem a začněte.

## go-i2p se blíží dokončení

Ať už chcete pracovat v jazyce Rust, Go, Java, C++ nebo v nějakém jiném jazyce, kontaktujte nás na #i2p-dev na Irc2P. Začněte tam a my vás uvedeme do kanálů zaměřených na router. Jsme také na ramble.i2p v f/i2p, na redditu v r/i2p a na GitHubu a git.idk.i2p. Těšíme se, že se nám brzy ozvete.
