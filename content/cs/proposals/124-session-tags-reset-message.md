---
title: "Resetovací zpráva pro ElGamal/AES+SessionTags"
number: "124"
author: "orignal"
created: "2016-01-24"
lastupdated: "2016-01-26"
status: "Open"
thread: "http://zzz.i2p/topics/2056"
---

## Přehled

Tento návrh je pro zprávu I2NP, kterou lze použít k resetování relace tagů mezi dvěma destinacemi.

## Motivace

Představte si, že nějaká destinace má spoustu potvrzených tagů k jiné destinaci. Ale tato destinace byla restartována nebo ztratila tyto tagy nějakým jiným způsobem. První destinace stále posílá zprávy s tagy a druhá destinace nemůže dešifrovat. Druhá destinace by měla mít možnost říct první destinaci, aby resetovala (začala od začátku) prostřednictvím dalšího garlic clove stejně, jako posílá aktualizovaný LeaseSet.

## Návrh

### Navrhovaná zpráva

Tento nový clove musí obsahovat typ doručení "destinace" s novou zprávou I2NP nazvanou například "Reset tagů" a obsahující hash identifikace odesílatele. Měla by zahrnovat časové razítko a podpis.

Může být poslána kdykoli, pokud nemůže destinace dešifrovat zprávy.

### Použití

Pokud restartuji svůj router a pokusím se připojit k jiné destinaci, pošlu clove s mým novým LeaseSet, a poslal bych další clove s touto zprávou obsahující mou adresu. Vzdálená destinace obdrží tuto zprávu, smaže všechny odchozí tagy ke mně a začne od ElGamal.

Je docela běžný případ, že destinace je v komunikaci pouze s jednou vzdálenou destinací. V případě restartu by měla poslat tuto zprávu všem společně s první streamovací nebo datagramovou zprávou.
