---
title: "Pomocníci pro ověřené adresy"
number: "135"
author: "zzz"
created: "2017-02-25"
lastupdated: "2017-02-25"
status: "Open"
thread: "http://zzz.i2p/topics/2241"
toc: true
---

## Přehled

Tento návrh přidává autentizační mechanismus k URL adresních pomocníků.


## Motivace

URL adresních pomocníků jsou inherentně nezabezpečené. Kdokoli může vložit parametr adresního pomocníka do odkazu, dokonce i do obrázku, a může vložit libovolný cíl do parametru URL "i2paddresshelper". V závislosti na implementaci uživatelského HTTP proxy, toto mapování hostname/cíl, pokud momentálně není v adresáři, může být přijato, buď s nebo bez mezistupňové obrazovky pro uživatele k přijetí.


## Návrh

Důvěryhodné přeskakovací servery a služby registrace do adresáře by poskytovaly nové odkazy adresního pomocníka, které přidávají autentizační parametry. Dva nové parametry by byly základní 64 podpis a řetězec podepsáno kym.

Tyto služby by generovaly a poskytovaly certifikát veřejného klíče. Tento certifikát by byl dostupný ke stažení a zahrnutí do softwaru HTTP proxy. Uživatelé a vývojáři softwaru by se rozhodli, zda takovým službám důvěřovat zahrnutím certifikátu.

Při setkání s odkazem adresního pomocníka by HTTP proxy zkontrolovalo dodatečné autentizační parametry a pokusilo se ověřit podpis. Po úspěšném ověření by proxy pokračovalo jako dříve, buď přijetím nového záznamu nebo zobrazením mezistupňové obrazovky uživateli. Při selhání ověření by proxy mohlo odmítnout adresního pomocníka nebo ukázat uživateli další informace.

Pokud nejsou přítomny žádné autentizační parametry, může HTTP proxy přijmout, odmítnout nebo poskytnout uživateli informace.

Přeskakovací služby by byly důvěryhodné jako obvykle, ale s dodatečným autentizačním krokem. Odkazy adresních pomocníků na jiných stránkách by musely být upraveny.


## Důsledky pro bezpečnost

Tento návrh přidává bezpečnost zavedením autentizace od důvěryhodných registračních / přeskakovacích služeb.


## Specifikace

TBD.

Dva nové parametry by mohly být i2paddresshelpersig a i2paddresshelpersigner?

Přijaté typy podpisů TBD. Pravděpodobně ne RSA, protože by základní 64 podpisy byly velmi dlouhé.

Algoritmus podpisu: TBD. Možná pouze hostname=b64dest (stejně jako návrh 112 pro autentizaci registrace)

Možný třetí nový parametr: Registrační autentizační řetězec (část po "#!") k použití pro dodatečné ověření HTTP proxy. Jakékoli "#" v řetězci by muselo být escapováno jako "&#35;" nebo "&num;", nebo nahrazeno nějakým jiným specifikovaným (TBD) znakem bezpečným pro URL.


## Migrace

Staré HTTP proxy, které nepodporují nové autentizační parametry, je budou ignorovat a předávat webovému serveru, což by mělo být neškodné.

Nové HTTP proxy, které volitelně podporují autentizační parametry, budou fungovat dobře se starými odkazy adresních pomocníků, které je neobsahují.

Nové HTTP proxy, které vyžadují autentizační parametry, nenechají projít staré odkazy adresních pomocníků, které je neobsahují.

Politiky implementace proxy se mohou vyvíjet během migračního období.

## Problémy

Majitel webové stránky nemohl vytvořit adresního pomocníka pro svou vlastní stránku, protože by potřeboval podpis od důvěryhodného přeskakovacího serveru. Musel by jej zaregistrovat na důvěryhodném serveru a získat autentizovaný URL adresního pomocníka od tohoto serveru. Existuje způsob, jak by stránka mohla vytvořit vlastní autentizovaný URL adresního pomocníka?

Alternativně by proxy mohla zkontrolovat Referer pro požadavek adresního pomocníka. Pokud by Referer byl přítomen, obsahoval b32 a b32 odpovídalo destinaci pomocníka, pak by mohl být povolen jako vlastní referral. Jinak by mohl být považován za požadavek třetí strany a odmítnut.
