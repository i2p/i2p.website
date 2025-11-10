---
title: "Zpráva z cesty na Def Con- zzz"
date: 2019-08-30
author: "zzz"
description: "Zpráva z cesty na Def Conu- zzz"
categories: ["conferences"]
---

## Zpráva z účasti na Def Conu

idk a já jsme se zúčastnili DEFCONu 27 a uspořádali dva workshopy o I2P pro vývojáře aplikací, s podporou od mhatty a Alexe. Workshop v Monero Village jsem vedl já a idk vedl ten v Crypto/Privacy Village. Zde shrnu workshop v Monero Village a přednášku o Toru, kterou přednesl Roger Dingledine. idk zveřejní zprávu z cesty týkající se svého workshopu.

Na workshopu Monero Village s názvem "I2P for Cryptocurrency Developers" jsme měli asi 8 účastníků. Plánovali jsme probrat specifické síťové požadavky každé aplikace a projít si různé dostupné možnosti i2ptunnel a SAM. Všichni účastníci však byli s I2P poměrně neobeznámeni, takže jsme změnili plán a poskytli úvodní přehled I2P. Vzhledem k tomu, že žádný z účastníků neměl s sebou notebook, pomohli jsme několika z nich nainstalovat I2P do jejich telefonu s Androidem a prošli jsme si některé funkce aplikace. U všech uživatelů se zdálo, že aplikace provede reseed (počáteční stažení adresáře sítě) a vytvoří tunnels poměrně rychle.

Jedna z častých otázek po instalaci aplikace byla "co mám dělat teď?". Aplikace nemá sekci 'zajímavé skryté služby' ani průvodce prvním spuštěním jako naše desktopová aplikace a většina výchozích položek v adresáři je dávno nefunkční. Zkušenost při prvním spuštění bychom mohli vylepšit. Také některé z zajímavějších částí aplikace jsou skryté v pokročilém nastavení; měli bychom tyto položky zrevidovat a zvážit, že některé z nich přestaneme skrývat.

Na přednášky o Toru je vždy užitečné chodit, ne ani tak proto, abychom zjistili, co dělají, ale abychom slyšeli, jak lidem věci vysvětlují a jakou používají terminologii. Rogerova přednáška "The Tor Censorship Arms Race" byla ve velkém sále za účasti asi dvou tisíc lidí. Poskytl velmi stručný přehled Toru s pouhými třemi nebo čtyřmi snímky. Říká, že nyní mají "dva až osm milionů uživatelů denně". Většina přednášky byla přehledem státních pokusů o blokování v průběhu let, počínaje Thajskem a Íránem v letech '06-'07 přes Tunisko, Čínu a Etiopii v roce 2011. Mosty Toru označil za "mizerné závody ve zbrojení". Ukázal nový formulář, který se má zobrazovat novým uživatelům, se zaškrtávacím políčkem "Tor je v mé zemi cenzurován".

Jejich nový pluggable transport (zásuvný transport) "snowflake" používá kombinaci domain fronting (doménový fronting), WebRTC, JavaScriptu, brokerů a proxy serverů s cílem dosáhnout spojení s Tor bridge (mostem v síti Tor). Roger k tomu měl jen jeden snímek a já jsem s tím nebyl obeznámen, takže bychom si měli zjistit víc o tom, o co přesně jde. Stručně se zmínil o několika věcech, na kterých možná budou pracovat dál, včetně "salmon" distribuce bridgeů, FTE/Marionette, decoy routing (klamného směrování) a "cupcake", což je rozšíření snowflake. Ačkoli o nich nemám další informace, mohou to být dobré módní termíny, které se vyplatí sledovat v jejich mailing listech.

Za mnohé z potíží Toru s cenzurou může popularita Toru, ale jejich TLS handshake je obzvlášť problematický a v průběhu let byl středem pozornosti velké části „závodů ve zbrojení“. V některých ohledech jsme na tom lépe, protože jsme převzali několik prvků z jejich aktuálně nejlepšího zásuvného transportu obfs4 a zabudovali je do NTCP2. Máme však potíže s blokováním našeho webu a reseeds, jak o tom budou tento týden na USENIX FOCI prezentovat Sadie a Phong.

Poznámky pro příště: DEFCON určitě doporučuji, pokud si najdeme zázemí v některém Village (tematické sekci na konferenci). Je to obrovská konference a omezené obecné prostory pro setkávání jsou extrémně přeplněné. Monero Village i Crypto/Privacy Village byli skvělými hostiteli a na každém z těch míst jsme měli několik hodin na setkávání s lidmi. Měli bychom hledat více příležitostí ke spolupráci s oběma organizacemi. V Monero Village byli také lidé ze ZCash a měli bychom spolupracovat i s nimi. Jakýkoli budoucí workshop by měl být zaměřen na obecnější publikum. Opravdu potřebujeme standardní prezentaci "Intro to I2P"; na workshopech by se hodila. Nepředpokládejte, že účastníci budou mít s sebou notebooky, u praktických cvičení se zaměřte na Android. V naší aplikaci pro Android je potřeba udělat několik vylepšení. V Las Vegas pijte hodně vody... a držte se dál od výherních automatů.
