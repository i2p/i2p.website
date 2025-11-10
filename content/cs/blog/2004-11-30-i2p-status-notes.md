---
title: "Stavové poznámky I2P ze dne 2004-11-30"
date: 2004-11-30
author: "jr"
description: "Týdenní aktualizace stavu I2P zahrnující vydání 0.4.2 a 0.4.2.1, novinky ve vývoji mail.i2p, pokrok v i2p-bt a diskuse o zabezpečení eepsite"
categories: ["status"]
---

Ahoj všichni

## Rejstřík

1. 0.4.2 and 0.4.2.1
2. mail.i2p
3. i2p-bt
4. eepsites(I2P Sites)
5. ???

## 1) 0.4.2 a 0.4.2.1

Od chvíle, kdy jsme konečně vydali 0.4.2, spolehlivost a propustnost sítě na nějakou dobu výrazně vzrostly, dokud jsme nenarazili na zbrusu nové chyby, které jsme přitom sami vytvořili. IRC spojení většině lidí vydrží celé hodiny, i když pro některé, kteří narazili na problémy, to byla poněkud hrbolatá jízda. Nicméně proběhla celá řada oprav a dnes pozdě večer nebo zítra ráno budeme mít k dispozici nové vydání 0.4.2.1 ke stažení.

## 2) mail.i2p

Dneska mi postman nenápadně podstrčil vzkaz, že má pár věcí, které by chtěl probrat - pro více informací se podívejte do zápisů ze schůzky (a pokud to čtete ještě před schůzkou, stavte se).

## 3) i2p-bt

Jednou z nevýhod nového vydání je, že narážíme na určité problémy s i2p-bt portem. Některé z problémů byly ve streamingové knihovně identifikovány, nalezeny a opraveny, ale je zapotřebí další práce, abychom to dostali do stavu, který potřebujeme.

## 4) eepsites(I2P stránky)

V posledních měsících proběhla na mailing listu, na kanálu a na fóru diskuse o některých problémech s tím, jak fungují eepsites(I2P Sites) a eepproxy - nedávno někteří zmiňovali problémy s tím, jak a které hlavičky se filtrují, jiní upozornili na nebezpečí špatně nakonfigurovaných prohlížečů, a je tu také stránka DrWoo, která shrnuje mnohá rizika. Jedna obzvlášť pozoruhodná skutečnost je, že někteří lidé aktivně pracují na appletech, které převezmou kontrolu nad počítačem uživatele, pokud si applet(y) nevypnou. (TAKŽE VYPNĚTE JAVA A JAVASCRIPT VE SVÉM PROHLÍŽEČI)

To samozřejmě vede k diskusi o tom, jak je můžeme zabezpečit. Slyšel jsem návrhy, abychom vytvořili vlastní prohlížeč nebo přibalili prohlížeč s předem nakonfigurovanými bezpečnými nastaveními, ale buďme realisté – to je mnohem víc práce, než do čeho se tu kdokoli pustí. Existují však tři další tábory:

1. Use a fascist HTML filter and tie it in with the proxy
2. Use a fascist HTML filter as part of a script that fetches pages for you
3. Use a secure macro language

První možnost je v zásadě stejná jako to, co máme teď, jen bychom obsah prohnali přes něco jako muffin nebo freenetův anonymizační filtr. Nevýhodou je, že to stále odhaluje HTTP hlavičky, takže bychom museli anonymizovat i HTTP vrstvu.

Ta druhá je velmi podobná tomu, co můžete vidět na `http://duck.i2p/` s CGIproxy, případně tak, jak to můžete vidět ve fproxy Freenetu. To zároveň řeší i HTTP část.

Třetí možnost má své výhody i nevýhody - umožňuje nám používat mnohem poutavější rozhraní (protože můžeme bezpečně použít některé známé bezpečné skripty v JavaScriptu apod.), ale má nevýhodu v podobě zpětné nekompatibility. Možná by šlo toto sloučit s filtrem, který by umožnil vkládat makra do filtrovaného html?

Každopádně, je to důležité vývojové úsilí a řeší jeden z nejvýznamnějších způsobů využití I2P - bezpečné a anonymní interaktivní webové stránky. Má někdo další nápady nebo informace o tom, jak bychom mohli získat to, co je potřeba?

## 5) ???

Tak jo, na schůzku jdu pozdě, takže bych to asi měl podepsat a poslat dál, že?

=jr [uvidíme, jestli se mi podaří zprovoznit gpg správně...]
