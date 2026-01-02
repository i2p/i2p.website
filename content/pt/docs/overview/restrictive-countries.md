---
title: "Países Estritos/Restritivos"
description: "Como o I2P se comporta em jurisdições com restrições sobre ferramentas de roteamento ou anonimato (Modo Oculto e lista restrita)"
slug: "restrictive-countries"
lastUpdated: "2024-07"
accurateFor: "2.10.0"
type: docs
reviewStatus: "needs-review"
---

Esta implementação do I2P (a implementação Java distribuída neste site) inclui uma "Lista de Países Restritos" usada para ajustar o comportamento do router em regiões onde participar no roteamento para outros pode ser restrito por lei. Embora não tenhamos conhecimento de jurisdições que proíbam o uso do I2P, várias têm proibições amplas sobre retransmissão de tráfego. Routers que parecem estar em países "restritos" são automaticamente colocados em modo Oculto.

O Projeto faz referência a pesquisas de organizações de direitos civis e digitais ao tomar essas decisões. Em particular, as pesquisas contínuas da Freedom House informam nossas escolhas. A orientação geral é incluir países com uma pontuação de Liberdades Civis (CL) de 16 ou menos, ou uma pontuação de Liberdade na Internet de 39 ou menos (não livre).

## Resumo do Modo Oculto

Quando um router é colocado no modo Hidden, três aspectos principais mudam no seu comportamento:

- Não publica um RouterInfo no netDb.
- Não aceita túneis de participação.
- Rejeita conexões diretas a roteadores no mesmo país.

Essas defesas tornam os routers mais difíceis de enumerar de forma confiável e reduzem o risco de violar proibições locais sobre retransmitir tráfego para outros.

## Lista de Países com Restrições Rigorosas (a partir de 2024)

```
/* Afghanistan */ "AF",
/* Azerbaijan */ "AZ",
/* Bahrain */ "BH",
/* Belarus */ "BY",
/* Brunei */ "BN",
/* Burundi */ "BI",
/* Cameroon */ "CM",
/* Central African Republic */ "CF",
/* Chad */ "TD",
/* China */ "CN",
/* Cuba */ "CU",
/* Democratic Republic of the Congo */ "CD",
/* Egypt */ "EG",
/* Equatorial Guinea */ "GQ",
/* Eritrea */ "ER",
/* Ethiopia */ "ET",
/* Iran */ "IR",
/* Iraq */ "IQ",
/* Kazakhstan */ "KZ",
/* Laos */ "LA",
/* Libya */ "LY",
/* Myanmar */ "MM",
/* North Korea */ "KP",
/* Palestinian Territories */ "PS",
/* Pakistan */ "PK",
/* Rwanda */ "RW",
/* Saudi Arabia */ "SA",
/* Somalia */ "SO",
/* South Sudan */ "SS",
/* Sudan */ "SD",
/* Eswatini (Swaziland) */ "SZ",
/* Syria */ "SY",
/* Tajikistan */ "TJ",
/* Thailand */ "TH",
/* Turkey */ "TR",
/* Turkmenistan */ "TM",
/* Venezuela */ "VE",
/* United Arab Emirates */ "AE",
/* Uzbekistan */ "UZ",
/* Vietnam */ "VN",
/* Western Sahara */ "EH",
/* Yemen */ "YE"
```
Se você acredita que um país deve ser adicionado ou removido da lista restrita, por favor abra uma issue: https://i2pgit.org/i2p/i2p.i2p/

Referência: Freedom House – https://freedomhouse.org/
