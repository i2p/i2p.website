---
title: "Setkání vývojářů I2P - 4. srpna 2020"
date: 2020-08-04
author: "i2p"
description: "Zápis z vývojářské schůzky I2P ze dne 4. srpna 2020."
categories: ["meeting"]
---

## Rychlé shrnutí

<p class="attendees-inline"><strong>Přítomni:</strong> eyedeekay, zlatinb, zzz</p>

## Záznam ze schůzky

<div class="irc-log">

(04:00:50 PM) eyedeekay1: Ahoj zlatinb zzz mikalvmeeh eche|on, pokud jste připraveni, zahájíme schůzku.
(04:00:50 PM) eyedeekay1: 1) Ahoj
(04:00:50 PM) eyedeekay1: 2) vydání 0.9.47
(04:00:50 PM) eyedeekay1: 3) Následné kroky k měsíčním schůzkám
(04:00:50 PM) eyedeekay1: 4) aktualizace Gitu
(04:01:38 PM) eyedeekay1: Ahoj všem, nejprve se omlouvám, že jsem si nevšiml, že jsem v názvu oznámení uvedl špatné datum.
(04:02:38 PM) zzz: ahoj
(04:02:58 PM) eyedeekay1: ahoj zzz
(04:03:31 PM) zlatinb: ahoj
(04:03:42 PM) eyedeekay1: Ahoj zlatinb
(04:04:49 PM) eyedeekay1: Dobře, tedy 2) vydání 0.9.47
(04:05:27 PM) eyedeekay1: Nevypadá to, že stihnu dokončit rekeyOnIdle včas pro 0.9.47.
(04:05:58 PM) eyedeekay1: Co bude zahrnuto, jsou především aktualizace vizuálních prvků z mé strany.
(04:06:19 PM) eyedeekay1: Má k tématu vydání 0.9.47 něco zzz nebo zlatinb?
(04:06:43 PM) zzz: souhrn je na http://zzz.i2p/topics/2905
(04:06:49 PM) zzz: zmrazení tagu za týden od zítřka
(04:06:53 PM) zzz: vydání zhruba za 3 týdny
(04:07:07 PM) zzz: diff má asi 18 500 řádků, což je docela typické
(04:07:23 PM) zzz: vypadá to dobře. Mám pár věcí k dokončení
(04:07:40 PM) zzz: ale jsem poměrně přesvědčen, že můžeme zůstat podle plánu
(04:07:49 PM) zzz: EOT
(04:08:08 PM) eyedeekay1: Včera jsem viděl, že toho přišlo docela dost, snažím se se na to dívat průběžně, jak to posíláš. Je opravdu vzrušující vidět tvoji práci. Moc díky.
(04:08:41 PM) zzz: to byly jen různé drobnosti, co mi týdny ležely v pracovním prostoru, nic zvláštního
(04:09:42 PM) eyedeekay1: I tak je to poučné sledovat, nevím, kde co je; když tě vidím pracovat, pomáhá mi to rozpoznat, kde se co děje
(04:09:43 PM) zzz: jen se snažím věci vyčistit a pushnout. někdy něco testuju celé měsíce
(04:10:28 PM) zzz: jasně, procházet změny ostatních je skvělý způsob učení a jak zachytit chyby, pokračuj
(04:10:39 PM) eyedeekay1: Zařídím
(04:10:42 PM) eyedeekay1: Pokud není nic dalšího, přejdu k 3) timeout 1 m
(04:12:40 PM) eyedeekay1: 2) Následné kroky k měsíční schůzce:
(04:12:53 PM) eyedeekay1: Toto je měsíční schůzka.
(04:12:53 PM) eyedeekay1: Nenastavil jsem WebIRC gateway (WebIRC bránu), protože jak tomu rozumím, bylo by to v rozporu s našimi IRC pravidly.
(04:13:13 PM) eyedeekay1: Nyní mám kopii pravidel pro oznamování schůzek a bylo mi vyjasněno, kdo za tato oznámení odpovídá.
(04:13:25 PM) eyedeekay1: Oznámení na 1. září, tentokrát se správným datem, bylo zveřejněno. Zatím bez témat, prosím přidávejte je podle potřeby: http://zzz.i2p/topics/2931-meeting-tues-september-1-8pm-utc
(04:14:55 PM) eyedeekay1: To samozřejmě přijde krátce po vydání 0.9.47
(04:15:45 PM) eyedeekay1: Má k bodu 2) ještě někdo něco?
(04:17:57 PM) eyedeekay1: 3) přechod na Git
(04:18:34 PM) eyedeekay1: Přechod na Git se konečně rozjíždí, máme plán a začínáme ho realizovat
(04:19:08 PM) eyedeekay1: nextloop a já děláme pokrok v tom, abychom několik dalších významných mtn větví zazrcadlili na github
(04:19:27 PM) eyedeekay1: tyto jsou zatím pouze pro čtení až do dokončení příslušných fází migrace na Git, tj. zatím žádné pull requesty ani MRs
(04:20:04 PM) eyedeekay1: Podrobný popis těchto fází viz: http://zzz.i2p/topics/2920-flipping-the-switch-on-git#10
(04:20:42 PM) eyedeekay1: Pro nextloopa i pro mě by bylo užitečné, kdybych dal nextloopovi oprávnění vytvářet repozitáře v jmenném prostoru i2p na githubu a zapisovat do repozitářů, které vytvoří.
(04:20:47 PM) zzz: dobrá práce při sepsání plánu
(04:21:24 PM) eyedeekay1: Díky, zzz, jsem rád, že je to konečně v použitelné podobě
(04:22:17 PM) zzz: není to dokonalé, ale je to „použitelné“ v tom smyslu, že k tomu můžeme dávat komentáře
(04:24:39 PM) eyedeekay1: Další věc, kterou budeme přesouvat, je web, což je fajn, protože je poměrně jednoduchý a nic na něm nezávisí; to by se mělo stát tento týden
(04:25:26 PM) eyedeekay1: Ale co se týče nextloopa, rád bych věděl, zda se setkává s širokým souhlasem, abychom mu dali oprávnění vytvářet/psát do repozitářů na githubu za nás?
(04:25:54 PM) zzz: ok. čekám na tvou úpravu plánu/harmonogramu, aby to nekolidovalo s vydáním .47
(04:26:25 PM) eyedeekay1: OK, mám to otevřené v editoru :)
(04:26:48 PM) zzz: Budeš se muset zeptat lidí, kteří jsou aktuálně správci githubu, ti tu nejsou a já nejsem členem (té skupiny).
(04:27:39 PM) eyedeekay1: Doposud se tento návrh setkává s jejich souhlasem, i když mám stále jednoho, kdo nereaguje.
(04:29:05 PM) zzz: Za mě je to v pořádku, pokud vy dva máte spolehlivý způsob komunikace a zálohu. Nemyslím, že potřebujeme další nekomunikující správce :)
(04:29:53 PM) eyedeekay1: Myslím, že to zvládneme
(04:30:06 PM) eyedeekay1: Takže nextloop dostane práva na githubu
(04:31:40 PM) zzz: Lidé, kteří dlouho nereagují a mají spoustu oprávnění, mohou být dobří jako záloha pro nejhorší případ („kdyby někoho přejel autobus“), ale je to také potenciální bezpečnostní riziko, takže je potřeba to řídit.
(04:33:12 PM) eyedeekay1: Jo
(04:33:20 PM) eyedeekay1: Pokud je tady k bodu 3) ještě něco, tak teď; jinak uvidíme upravený plán ve vlákně na zzz.i2p pravděpodobně během příštího dne.
(04:33:45 PM) zzz: super
(04:34:18 PM) mikalvmeeh: (Jsem tu jen napůl, nestihl jsem pozdrav)
(04:34:56 PM) eyedeekay1: Dobře, prošli jsme plánovaná témata, má někdo ještě něco?
(04:36:43 PM) eyedeekay1: timeout 1 m
(04:38:51 PM) eyedeekay1: *bafs* Dobře, tímto tuto schůzku uzavírám. Prosím, pamatujte na 1. září, další naplánovanou schůzku ve stejný čas, 20:00 UTC
(04:39:12 PM) eyedeekay1: Děkuji všem za účast </div>
