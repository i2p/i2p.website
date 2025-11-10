---
title: "Jak zpřístupnit vaše stávající webové stránky jako I2P eepSite"
date: 2019-06-02
author: "idk"
description: "Poskytování I2P zrcadla"
categories: ["tutorial"]
---

Tento příspěvek na blogu slouží jako obecný průvodce provozováním zrcadla služby na clearnetu jako eepSite. Navazuje na předchozí příspěvek na blogu o základních tunelech I2PTunnel.

Bohužel je pravděpodobně nemožné *zcela* pokrýt všechny možné případy zpřístupnění existujícího webu jako eepSite; škála serverového softwaru je zkrátka příliš rozmanitá, nemluvě o praktických zvláštnostech každého konkrétního nasazení softwaru. Místo toho se pokusím co nejkonkrétněji popsat obecný postup přípravy služby k nasazení na eepWeb nebo do jiných skrytých služeb.

Velká část této příručky bude čtenáře brát jako účastníka rozhovoru, zejména když to budu myslet opravdu vážně, oslovím čtenáře přímo(tj. použiji "you" místo "one") a často budu uvádět sekce otázkami, o nichž si myslím, že by si je čtenář mohl klást. Jde koneckonců o "proces", do něhož se administrátor musí cítit být "zapojen", stejně jako při hostování jakékoli jiné služby.

**Zřeknutí se odpovědnosti:**

I když by to bylo skvělé, pravděpodobně je pro mě nemožné poskytnout konkrétní pokyny pro každý jednotlivý typ softwaru, který by někdo mohl použít k hostování webových stránek. Z tohoto důvodu tento návod vyžaduje určité předpoklady na straně autora a na straně čtenáře trochu kritického myšlení a zdravého rozumu. Aby bylo jasno, **předpokládal jsem, že osoba následující tento návod již provozuje službu na běžném webu, kterou lze spojit se skutečnou identitou nebo organizací**, a tudíž pouze nabízí anonymní přístup, nikoli za účelem vlastní anonymizace.

Proto se **vůbec nepokouší o anonymizaci** spojení z jednoho serveru na druhý. Pokud chcete provozovat novou, s vámi nepropojitelnou skrytou službu, která hostuje obsah, jenž s vámi není spojen, pak byste to neměli dělat na svém vlastním clearnet (veřejný internet) serveru ani ze svého vlastního domu.
