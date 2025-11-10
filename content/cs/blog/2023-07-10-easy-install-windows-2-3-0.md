---
title: "Byl vydán Easy-Install pro Windows ve verzi 2.3.0"
date: 2023-07-10
author: "idk"
description: "Vydán Easy-Install pro Windows 2.3.0"
categories: ["release"]
API_Translate: pravda
---

Balíček I2P Easy-Install pro Windows ve verzi 2.3.0 byl nyní vydán. Jako obvykle toto vydání obsahuje aktualizovanou verzi I2P router. To se týká i bezpečnostních problémů, které ovlivňují lidi, kteří v síti hostují služby.

Toto bude poslední vydání balíčku Easy-Install, které bude nekompatibilní s I2P Desktop GUI. Byl aktualizován tak, aby obsahoval nové verze všech zahrnutých webextensions. Byla opravena dlouhodobá chyba v I2P in Private Browsing, která způsobovala nekompatibilitu s vlastními motivy. Uživatelům je stále doporučeno, aby *ne*instalovali vlastní motivy. Panely Snark nejsou ve Firefoxu automaticky připínány na začátek pořadí panelů. Kromě používání alternativních cookieStores se panely Snark nyní chovají jako běžné panely prohlížeče.

**Bohužel, toto vydání je stále nepodepsaným `.exe` instalátorem.** Ověřte prosím kontrolní součet instalátoru před jeho použitím. **Aktualizace, na druhou stranu,** jsou podepsány mými I2P podpisovými klíči a proto bezpečné.

Toto vydání bylo zkompilováno pomocí OpenJDK 20. Používá i2p.plugins.firefox ve verzi 1.1.0 jako knihovnu pro spouštění prohlížeče. Používá i2p.i2p ve verzi 2.3.0 jako I2P router a pro poskytování aplikací. Jako vždy se doporučuje, abyste co nejdříve aktualizovali na nejnovější verzi I2P routeru.

- [Easy-Install Bundle Source](http://git.idk.i2p/i2p-hackers/i2p.firefox/-/tree/i2p-firefox-2.3.0)
- [Router Source](http://git.idk.i2p/i2p-hackers/i2p.i2p/-/tree/i2p-2.3.0)
- [Profile Manager Source](http://git.idk.i2p/i2p-hackers/i2p.plugins.firefox/-/tree/1.1.0)
