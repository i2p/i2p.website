---
title: "Přehledový plán vývoje pro rok 2018"
date: 2018-02-11
slug: "high-level-roadmap-for-2018"
author: "str4d"
description: "Rok 2018 bude rokem nových protokolů, nových spoluprací a vytříbenějšího zaměření"
categories: ["roadmap"]
---

Jedním z mnoha témat, o kterých jsme na 34C3 diskutovali, bylo, na co bychom se měli v nadcházejícím roce zaměřit. Zejména jsme chtěli mít roadmapu (plán), která jasně vymezí, co chceme určitě stihnout, oproti tomu, co by bylo opravdu příjemné mít, a zároveň umožní pomoci se začleněním nově příchozích do obou kategorií. Tady je, k čemu jsme dospěli:

## Priorita: Nová krypto(grafie!)

Mnoho současných primitiv a protokolů si stále zachovává své původní návrhy z doby kolem roku 2005 a potřebuje vylepšení. Už několik let máme řadu otevřených návrhů s nápady, ale postup vpřed byl pomalý. Shodli jsme se, že toto musí být naší nejvyšší prioritou pro rok 2018. Základní komponenty jsou:

- New transport protocols (to replace NTCP and SSU). See [Prop111](https://geti2p.net/spec/proposals/111).
- New onion-encryption protocol for building and using tunnels.
- New NetDB datatypes to enable enhanced Destinations. See [Prop123](https://geti2p.net/spec/proposals/123).
- Upgraded end-to-end protocol (replacing ElGamal).

Práce na této prioritě spadá do několika oblastí:

- Writing proposals.
- Writing working implementations of them that we can test.
- Reviewing proposals.

Nemůžeme napříč celou sítí nasadit nové specifikace protokolu, aniž bychom odvedli práci ve všech těchto oblastech.

## Vítané: Znovupoužití kódu

Jednou z výhod zahájení výše uvedené práce právě nyní je, že během posledních několika let probíhaly nezávislé snahy vytvořit jednoduché protokoly a rámce protokolů, které splňují mnoho cílů, jež máme pro naše vlastní protokoly, a uchytily se v širší komunitě. Využitím této práce získáme „násobící efekt“:

- We benefit from protocol designs, security proofs, and code written by others, reducing the amount of work we need to do for the same level of feature-completeness and security assurances.

- Work we do can be leveraged by other communities, increasing their interest in collaborating with us, and thinking about I2P as a whole.

Mé návrhy budou konkrétně využívat [Noise Protocol Framework](https://noiseprotocol.org/) a [formát paketů SPHINX](https://katzenpost.mixnetworks.org/docs/specs/sphinx.html). Na těchto návrzích mám domluvenou spolupráci s několika lidmi mimo I2P!

## Priorita: spolupráce s Clearnetem (veřejným internetem)

K tomuto tématu jsme během posledních zhruba šesti měsíců postupně budovali zájem. Na PETS2017, 34C3 a RWC2018 jsem vedl několik velmi dobrých diskusí o tom, jak můžeme zlepšit spolupráci se širší komunitou. To je opravdu důležité, abychom zajistili, že pro nové protokoly získáme co nejvíce odborných posouzení. Největší překážkou, kterou jsem zaznamenal, je skutečnost, že většina spolupráce na vývoji I2P se v současnosti odehrává uvnitř samotného I2P, což výrazně zvyšuje úsilí potřebné k přispění.

The two priorities in this area are:

- Set up a project-run development forum that is accessible both inside and outside I2P.

- Set up mailing lists for review and discussion of proposals (possibly connected to the above forum).

Other goals which are classed as nice-to-have:

- Set up a usable git-to-mtn pathway, to enable us to effectively solicit clearnet contributions on GitHub while keeping the canonical dev environment on Monotone.

- Write a "position paper" that accurately explains I2P to academic audiences, and puts it in context with existing literature.

Očekávám, že spolupráce s lidmi mimo I2P budou probíhat výhradně na GitHubu, aby se minimalizovaly překážky.

## Priorita: Příprava na dlouhodobá vydání

I2P je nyní v Debianu Sid (jejich nestabilním repozitáři), který se zhruba za rok a půl stabilizuje, a také byl zařazen do repozitáře Ubuntu pro zahrnutí do příštího vydání LTS (s dlouhodobou podporou) v dubnu. Začneme mít verze I2P, které budou přetrvávat po celé roky, a musíme zajistit, že dokážeme zvládnout jejich přítomnost v síti.

Primárním cílem je během příštího roku nasadit co nejvíce nových protokolů, abychom stihli příští stabilní vydání Debianu. U těch, které vyžadují víceleté nasazení, bychom měli co nejdříve zapracovat změny pro dopřednou kompatibilitu.

## Priorita: Převést stávající aplikace na pluginy

Model Debianu podporuje mít samostatné balíčky pro samostatné komponenty. Shodli jsme se, že oddělení aktuálně přibalených Java aplikací od jádrového Java routeru by bylo z několika důvodů přínosné:

- It codifies the boundary between the applications and the router.

- It should make it easier to get these apps running with non-Java routers.

- It would enable third parties to create "I2P bundles" containing just the applications they want.

In combination with the earlier priorities, this moves the main I2P project more in the direction of e.g. the Linux kernel. We will spend more time focusing on the network itself, leaving third-party developers to focus on applications that use the network (something that is significantly easier to do after our work in the last few years on APIs and libraries).

## Volitelné: Vylepšení aplikace

Existuje řada vylepšení na úrovni aplikace, na kterých chceme pracovat, ale v současnosti na to nemáme kapacitu vývojářů s ohledem na naše další priority. V této oblasti bychom velmi rádi přivítali nové přispěvatele! Jakmile bude výše uvedené oddělení dokončeno, bude pro kohokoli výrazně snazší pracovat na konkrétní aplikaci nezávisle na hlavním Java routeru.

Jednou z takových aplikací, s níž bychom rádi získali pomoc, je I2P Android. Budeme ji udržovat aktuální v souladu s hlavními vydáními I2P a podle možností opravovat chyby, ale je toho mnoho, co by se dalo udělat pro zlepšení podkladového kódu i použitelnosti.

## Priorita: Stabilizace Susimailu a I2P-Bote

To ale neznamená, že bychom se v nejbližší době nechtěli cíleně zaměřit na opravy pro Susimail a I2P-Bote (některé z nich už jsou ve verzi 0.9.33). V posledních několika letech dostávaly méně pozornosti než jiné aplikace I2P, proto chceme věnovat čas tomu, abychom jejich kódové základny dostali na odpovídající úroveň a aby pro nové přispěvatele bylo snazší se do nich zapojit!

## Dobré mít: Třídění tiketů

Máme velké množství nevyřízených tickets (záznamů v systému sledování problémů) v řadě subsystémů a aplikací I2P. V rámci výše uvedeného stabilizačního úsilí bychom rádi dali do pořádku některé z našich starších, dlouhodobých problémů. Ještě důležitější je, že chceme zajistit, aby naše tickets byly správně uspořádané, aby noví přispěvatelé mohli snadno najít vhodné tickets, na kterých mohou pracovat.

## Priorita: Podpora uživatelů

Jedním z aspektů výše uvedeného, na který se zaměříme, je udržování kontaktu s uživateli, kteří si najdou čas na hlášení problémů. Děkujeme! Čím kratší dokážeme udělat cyklus zpětné vazby, tím rychleji budeme moci řešit problémy, s nimiž se noví uživatelé potýkají, a tím pravděpodobnější je, že zůstanou aktivně zapojeni do komunity.

## Budeme rádi za vaši pomoc!

To všechno působí velmi ambiciózně, a je to tak! Ale mnoho z výše uvedených bodů se překrývá a při pečlivém plánování v nich můžeme výrazně pokročit.

Pokud máte zájem pomoci s některým z výše uvedených cílů, přijďte si s námi popovídat! Najdete nás na OFTC a Freenode (#i2p-dev) a na Twitteru (@GetI2P).
