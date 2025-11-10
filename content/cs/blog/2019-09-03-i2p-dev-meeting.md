---
title: "Setkání vývojářů I2P - 3. září 2019"
date: 2019-09-03
author: "zzz"
description: "Zápis z vývojářské schůzky I2P ze dne 3. září 2019."
categories: ["meeting"]
---

## Stručné shrnutí

<p class="attendees-inline"><strong>Přítomni:</strong> eyedeekay, sadie, zlatinb, zzz</p>

## Záznam ze schůzky

<div class="irc-log">                Poznámka: příspěvky od sadie se během schůzky nezobrazily, níže jsou vloženy.

20:00:00 <zzz> 0) Ahoj
20:00:00 <zzz> 1) Stav vydání 0.9.42 (zzz)
20:00:48 <zzz> vydání minulý týden proběhlo docela hladce
20:00:56 <zzz> zbývá už jen pár věcí
20:01:27 <zzz> znovu zprovoznit github bridge (nextloop), balíček pro debian sid (mhatta) a android klientskou knihovnu, na kterou jsme u 41 zapomněli (meeh)
20:01:37 <zzz> nextloop, meeh, máte pro ty položky ETA?
20:03:06 <zzz> ještě něco k 1) ?
20:04:02 <zzz> 2) Stav projektu I2P Browser "labs" (sadie, meeh)
20:04:25 <zzz> sadie, meeh, jaký je stav a jaký je další milník?
          <sadie> Beta 5 měla vyjít v pátek, ale objevily se nějaké problémy. Vypadá to, že některé jsou připravené https://i2bbparts.meeh.no/i2p-browser/ ale opravdu jsem potřebovala slyšet od meeh další termín pro tohle
          <sadie> Stránka Lab bude do konce tohoto týdne živá. Další milník pro Browser bude diskuse o požadavcích konzole pro vydání beta 6
20:05:51 <zzz> ještě něco k 2) ?
20:06:43 <zzz> 3) případy použití Outproxy / stav (sadie)
20:06:57 <zzz> sadie, jaký je stav a jaký je další milník?
          <sadie> Kdokoli může sledovat naše poznámky ze schůzek v ticketu 2472. Rozhodli jsme o stavech případů použití a máme seznam požadavků. Dalším milníkem budou uživatelské požadavky pro use case Přátelé a rodina a také vývojové požadavky pro Přátelé a rodina a obecný use case, abychom viděli, kde se mohou překrývat
20:08:05 <zzz> ještě něco k 3) ?
20:08:19 <eyedeekay> Omlouvám se za zpoždění
20:09:01 <zzz> 4) Stav vývoje 0.9.43 (zzz)
20:09:21 <zzz> právě začínáme cyklus 43, který plánujeme vydat zhruba za 7 týdnů
20:09:40 <zzz> aktualizovali jsme roadmapu na webu, ale přidáme ještě pár položek
20:10:06 <zzz> opravoval jsem některé chyby v IPv6 a zrychluji zpracování AES v tunnelu
20:10:30 <zzz> brzy zaměřím pozornost na novou blinding info (zaslepené informace) zprávu I2CP
20:10:59 <zzz> eyedeekay, zlatinb, máte něco k .43?
20:11:46 <eyedeekay> Ne, nemyslím si
20:12:02 <zlatinb> pravděpodobně víc věcí na testnetu
20:12:32 <zzz> jo, máme ještě pár jogger ticketů, na které se podívat, s ohledem na SSU
20:12:48 <zzz> ještě něco k 4) ?
20:14:00 <zzz> 5) Stav návrhů (zzz)
20:14:20 <zzz> naším hlavním zaměřením je velmi komplexní nový návrh šifrování 144
20:14:48 <zzz> v posledních týdnech jsme udělali dobrý pokrok a provedli některé zásadní aktualizace samotného návrhu
20:15:35 <zzz> zbývá pár úklidových prací a děr k zaplnění, ale doufám, že je to v dostatečně dobrém stavu, abychom brzy mohli začít psát některé implementace jednotkových testů, možná do konce měsíce
20:16:17 <zzz> také se znovu podíváme na blinding info zprávu pro návrh 123 (šifrovaný LS2) poté, co ji začnu příští týden implementovat
20:16:52 <zzz> také brzy očekáváme aktualizaci od chisana k návrhu 152 (zprávy pro sestavování tunnelů)
20:17:27 <zzz> minulý měsíc jsme dokončili návrh 147 (prevence napříč sítěmi) a jak i2p, tak i2pd to mají naimplementované a ve vydání .42
20:18:23 <zzz> takže věci se posouvají vpřed; i když 144 působí pomalu a hrozivě, také dělá dobrý pokrok
20:18:27 <zzz> ještě něco k 5) ?
20:20:00 <zzz> 6) Status scrum (zlatinb)
20:20:05 <zzz> můžeš začít, zlatinb
20:20:42 <zlatinb> Ahoj, prosím stručně řekněte: 1) co jste dělali od posledního scrum 2) co plánujete na příští měsíc 3) máte nějaké překážky nebo potřebujete pomoc. Na konci napište EOT
20:21:23 <zlatinb> já: 1) Různé experimenty na testnetu pro zrychlení hromadných přenosů 2) další práce na testnetu, doufejme na větším serveru/síti 3) žádné překážky EOT
20:22:15 <zzz> 1) opravy chyb, změna rozdělení konfigurace, vydání .42, návrhy, workshopy na DEFCONu (viz můj cestopis na i2pforum a na našem webu)
20:23:56 <zzz> 2) opravy chyb, návrh 144, blinding info zpráva, zrychlení, pomoc s výzkumem Outproxy, opravit průvodce SSL rozbitého rozdělením konfigurace
20:24:20 <zzz> více oprav IPv6
20:24:38 <zzz> 3) žádné překážky EOT
20:24:50 <eyedeekay> 1) Od posledního scrumu pracuji na opravách chyb, webu, na návrhu outproxy a věcech souvisejících s i2ptunnels. 2) Pokračovat v reorganizaci a zlepšování prezentace webu. Pracovat na posunu návrhu outproxy 3) žádné překážky EOT
          <sadie> 1) Účast na FOCI, zkoumala jsem možnosti financování, setkala se s potenciálními donory, měla schůzku s Tails (včetně Mhatta), pracovala na brandingu I2P Browseru, aktualizace webu s IDK, udělala drobné změny v konzoli pro poslední vydání
          <sadie> 2) příští měsíc budu pracovat na grantech, vylepšeních konzole a webu, průvodci nastavením, účast na Our Networks v Torontu, posouvání výzkumu I2P Browseru a OutProxy
          <sadie> 3) žádné překážky EOT
20:25:29 <zlatinb> scrum.setTimeout( 60 * 1000 );
20:27:04 <zzz> ok, vypršel čas
20:27:10 <zlatinb> ScrumTimeoutException
20:27:41 <zzz> poslední výzva pro sadie, meeh, nextloop, aby se vrátili k bodům 1)–3)
20:27:52 <zzz> nějaká další témata pro schůzku?
20:28:47 * zzz bere baffer
20:30:00 * zzz ***bafs*** schůzi uzavírá </div>
