---
title: "Vysokourovňová roadmapa pro rok 2018"
date: 2018-02-11
slug: "high-level-roadmap-for-2018"
author: "str4d"
description: "Rok 2018 bude rokem nových protokolů, nových spoluprací a vytříbenějšího zaměření."
categories: ["roadmap"]
---

Jedním z mnoha témat, o nichž jsme na 34C3 diskutovali, bylo, na co bychom se měli v nadcházejícím roce zaměřit. Především jsme chtěli mít roadmapu, která jasně vymezuje, co chceme s jistotou dokončit, oproti tomu, co by bylo velmi vhodné mít, a zároveň pomůže zapojit nováčky do obou kategorií. Zde je, k čemu jsme dospěli:

## Priorita: Nová krypto(grafie!)

Řada současných primitiv a protokolů si stále zachovává své původní návrhy zhruba z roku 2005 a potřebuje vylepšení. Už několik let máme řadu otevřených návrhů s nápady, ale pokrok byl pomalý. Shodli jsme se, že toto musí být naší nejvyšší prioritou pro rok 2018. Základní komponenty jsou:

- New transport protocols (to replace NTCP and SSU). See Prop111.
- New onion-encryption protocol for building and using tunnels.
- New NetDB datatypes to enable enhanced Destinations. See Prop123.
- Upgraded end-to-end protocol (replacing ElGamal).

Práce na této prioritě spadá do několika oblastí:

- Writing proposals.
- Writing working implementations of them that we can test.
- Reviewing proposals.

Nemůžeme vydat nové specifikace protokolu napříč celou sítí bez práce na všech těchto oblastech.

## Výhodou: Opětovné použití kódu

Jednou z výhod zahájení výše uvedené práce právě teď je, že v posledních několika letech probíhaly nezávislé snahy vytvořit jednoduché protokoly a protokolové rámce, které splňují mnoho cílů, jež jsme si stanovili pro naše vlastní protokoly, a uchytily se ve širší komunitě. Využitím této práce získáme efekt "force multiplier" (multiplikátor účinku):

- We benefit from protocol designs, security proofs, and code written by others, reducing the amount of work we need to do for the same level of feature-completeness and security assurances.

- Work we do can be leveraged by other communities, increasing their interest in collaborating with us, and thinking about I2P as a whole.

Moje návrhy budou konkrétně využívat [Noise Protocol Framework](https://noiseprotocol.org/) a [SPHINX packet format](https://katzenpost.mixnetworks.org/docs/specs/sphinx.html). Mám na ně domluvenou spolupráci s několika lidmi mimo I2P!

## Priorita: spolupráce s Clearnetem (veřejným internetem)

V této souvislosti jsme za posledních zhruba šest měsíců postupně budovali zájem. Na PETS2017, 34C3 a RWC2018 jsem vedl velmi dobré diskuse o tom, jak můžeme zlepšit spolupráci se širší komunitou. To je opravdu důležité, abychom zajistili co nejvíce odborného posouzení nových protokolů. Největší překážkou, kterou jsem zaznamenal, je skutečnost, že se většina spolupráce na vývoji I2P v současnosti odehrává uvnitř samotného I2P, což výrazně zvyšuje úsilí potřebné k přispění.

Dvě priority v této oblasti jsou:

- Set up a project-run development forum that is accessible both inside and outside I2P.

- Set up mailing lists for review and discussion of proposals (possibly connected to the above forum).

Další cíle, které jsou považovány za užitečné, ale nikoli nezbytné:

- Set up a usable git-to-mtn pathway, to enable us to effectively solicit clearnet contributions on GitHub while keeping the canonical dev environment on Monotone.

- Write a "position paper" that accurately explains I2P to academic audiences, and puts it in context with existing literature.

Očekávám, že spolupráce s lidmi mimo I2P budou probíhat výhradně na GitHubu, aby bylo tření minimální.

## Priorita: Příprava na dlouhodobá vydání

I2P je nyní v Debianu Sid (jejich nestabilní repozitář), který by se měl přibližně za rok a půl stabilizovat, a zároveň bylo I2P také převzato do repozitáře Ubuntu k zařazení do příštího vydání LTS v dubnu. Začneme mít verze I2P, které budou přetrvávat po celé roky, a musíme zajistit, že dokážeme zvládnout jejich přítomnost v síti.

Hlavním cílem je během příštího roku nasadit co nejvíce nových protokolů, jak je reálně možné, abychom stihli příští stabilní vydání Debianu. U těch, které si vyžádají víceleté zavádění, bychom měli změny pro dopřednou kompatibilitu začlenit co nejdříve.

## Priorita: přeměna stávajících aplikací na pluginy

Model Debianu podporuje mít pro jednotlivé komponenty samostatné balíčky. Shodli jsme se, že oddělení v současnosti společně dodávaných Java aplikací od základního Java routeru by bylo přínosné z několika důvodů:

- It codifies the boundary between the applications and the router.

- It should make it easier to get these apps running with non-Java routers.

- It would enable third parties to create "I2P bundles" containing just the applications they want.

V kombinaci s dřívějšími prioritami to posouvá hlavní projekt I2P více směrem k např. linuxovému jádru. Budeme více času věnovat samotné síti a ponecháme na vývojářích třetích stran, aby se soustředili na aplikace, které síť používají (což je po naší práci v posledních několika letech na API a knihovnách výrazně snazší).

## Dobré mít: Vylepšení aplikace

Existuje celá řada vylepšení na úrovni aplikací, na kterých bychom chtěli pracovat, ale vzhledem k našim dalším prioritám na to aktuálně nemáme kapacity vývojářů. Toto je oblast, kde bychom velmi rádi viděli nové přispěvatele! Jakmile bude výše uvedené oddělení dokončeno, bude pro někoho výrazně snazší pracovat na konkrétní aplikaci nezávisle na hlavním Java routeru.

Jednou z takových aplikací, s níž bychom velmi uvítali pomoc, je I2P Android. Budeme ji udržovat aktuální s hlavními vydáními I2P a podle možností opravovat chyby, ale je toho mnoho, co by se dalo udělat pro zlepšení základního kódu i použitelnosti.

## Priorita: stabilizace Susimailu a I2P-Bote

Přesto bychom se v nejbližší době chtěli zaměřit konkrétně na opravy pro Susimail a I2P-Bote (některé z nich již byly zahrnuty do 0.9.33). V posledních několika letech na nich bylo odvedeno méně práce než na jiných aplikacích I2P, a proto jim chceme věnovat čas, abychom jejich codebase (kódovou základnu) přivedli na odpovídající úroveň a aby bylo pro nové přispěvatele snazší se do nich zapojit!

## Výhodou by bylo: Třídění tiketů

Máme velký počet nevyřízených tiketů v několika subsystémech a aplikacích I2P. V rámci výše uvedeného úsilí o stabilizaci bychom rádi pročistili některé z našich starších dlouhodobě otevřených problémů. Ještě důležitější je, že chceme zajistit, aby naše tikety byly správně uspořádané, aby noví přispěvatelé mohli najít vhodné tikety, na kterých mohou pracovat.

## Priorita: Podpora uživatelů

Jedním z aspektů výše uvedeného, na který se zaměříme, je udržování kontaktu s uživateli, kteří si najdou čas nahlásit problémy. Děkujeme! Čím kratší se nám podaří udělat zpětnovazební smyčku, tím rychleji dokážeme vyřešit problémy, s nimiž se setkávají noví uživatelé, a tím pravděpodobnější je, že se budou nadále zapojovat do komunity.

## Budeme rádi za vaši pomoc!


That all looks very ambitious, and it is! But many of the items above overlap, and with careful planning we can make a serious dent in them.

Pokud máte zájem pomoci s některým z výše uvedených cílů, přijďte si s námi popovídat! Najdete nás na OFTC a Freenode (#i2p-dev) a na Twitteru (@GetI2P).
