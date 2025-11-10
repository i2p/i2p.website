---
title: "Aktualizace Jpackage pro Java CVE-2022-21449"
date: 2022-04-21
author: "idk"
description: "Vydány balíčky Jpackage s opravami pro CVE-2022-21449 v Javě"
categories: ["release"]
API_Translate: pravda
---

## Podrobnosti aktualizace

Nové I2P Easy-Install balíčky byly vygenerovány s použitím nejnovější verze Java Virtual Machine (virtuální stroj Java), která obsahuje opravu pro CVE-2022-21449 „Psychic Signatures“. Doporučujeme, aby uživatelé Easy-Install balíčků aktualizovali co nejdříve. Současní uživatelé OSX obdrží aktualizace automaticky, uživatelé Windows by si měli stáhnout instalační program z naší stránky ke stažení a spustit jej obvyklým způsobem.

I2P router na Linuxu používá virtuální stroj Javy (JVM) nakonfigurovaný hostitelským systémem. Uživatelé na těchto platformách by měli přejít na stabilní verzi Javy nižší než Java 14, aby zmírnili zranitelnost, dokud správci balíčků nevydají aktualizace. Ostatní uživatelé používající externí JVM by měli co nejdříve aktualizovat JVM na opravenou verzi.
