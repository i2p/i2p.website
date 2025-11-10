---
title: "Vítej Git, sbohem Monotone"
date: 2020-12-10
author: "idk"
description: "Vítej, git, sbohem mtn"
categories: ["Status"]
---

## Vítej, Git, sbohem Monotone

### The I2P Git Migration is nearly concluded

Po více než desetiletí se I2P spoléhalo na letitou službu Monotone pro zajištění svých potřeb správy verzí, avšak během posledních několika let většina světa přešla na dnes univerzální systém správy verzí Git. Ve stejné době se síť I2P stala rychlejší a spolehlivější a byla vyvinuta dostupná náhradní řešení obcházející nemožnost Gitu navazovat přerušené přenosy.

Dnes je pro I2P významný okamžik, protože jsme odstavili starou větev mtn i2p.i2p a oficiálně přesunuli vývoj základních Java knihoven I2P z Monotone na Git.

Ačkoli bylo naše používání mtn v minulosti zpochybňováno a ne vždy to byla populární volba, rád bych této chvíle využil — jakožto možná vůbec poslední projekt používající Monotone — k poděkování vývojářům Monotone, současným i bývalým, ať jsou kdekoli, za software, který vytvořili.

## GPG Signing

Zasílání změn do repozitářů projektu I2P vyžaduje, abyste nastavili podepisování pomocí GPG u svých git commitů, včetně Merge Requests a Pull Requests. Prosím, nakonfigurujte svého klienta Git pro podepisování pomocí GPG dříve, než vytvoříte fork i2p.i2p a cokoli odešlete.

## Podepisování GPG

Oficiálním repozitářem je ten hostovaný na https://i2pgit.org/i2p-hackers/i2p.i2p a na https://git.idk.i2p/i2p-hackers/i2p.i2p, ale na Githubu je k dispozici "Mirror" na https://github.com/i2p/i2p.i2p.

Teď, když používáme git, můžeme synchronizovat repozitáře z naší samohostované (self-hosted) instance Gitlabu na Github a zpět. To znamená, že je možné na Gitlabu vytvořit a odeslat merge request (žádost o sloučení) a když je sloučen, výsledek se synchronizuje s Githubem, a Pull Request (žádost o sloučení) na Githubu se po sloučení objeví na Gitlabu.

To znamená, že nám můžete posílat kód prostřednictvím naší instance Gitlabu nebo přes Github podle toho, co preferujete; nicméně více vývojářů I2P pravidelně sleduje Gitlab než Github. Je pravděpodobnější, že MR (merge request) na Gitlabu budou sloučeny dříve než PR (pull request) na Githubu.

## Oficiální repozitáře a synchronizace s GitLabem/GitHubem

Gratulujeme a děkujeme všem, kteří pomohli s migrací na Git, zejména zzz, eche|on, nextloop a našim operátorům zrcadel webu! I když bude některým z nás Monotone chybět, stal se překážkou pro nové i stávající přispěvatele do vývoje I2P a těší nás, že se můžeme připojit ke světu vývojářů, kteří používají Git ke správě svých distribuovaných projektů.
