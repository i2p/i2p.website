---
title: "Países Estrictos/Restrictivos"
description: "Cómo se comporta I2P en jurisdicciones con restricciones sobre herramientas de enrutamiento o anonimato (Modo Oculto y lista estricta)"
slug: "restrictive-countries"
lastUpdated: "2024-07"
accurateFor: "2.10.0"
type: docs
reviewStatus: "needs-review"
---

Esta implementación de I2P (la implementación en Java distribuida en este sitio) incluye una "Lista de Países Estrictos" utilizada para ajustar el comportamiento del router en regiones donde participar en el enrutamiento para otros puede estar restringido por ley. Si bien no tenemos conocimiento de jurisdicciones que prohíban el uso de I2P, varias tienen prohibiciones amplias sobre la retransmisión de tráfico. Los routers que parecen estar en países "estrictos" se colocan automáticamente en modo Oculto.

El Proyecto hace referencia a investigaciones de organizaciones de derechos civiles y digitales al tomar estas decisiones. En particular, la investigación continua de Freedom House informa nuestras elecciones. La orientación general es incluir países con una puntuación de Libertades Civiles (CL) de 16 o menos, o una puntuación de Libertad en Internet de 39 o menos (no libres).

## Resumen del Modo Oculto

Cuando un router se coloca en modo Oculto (Hidden), tres aspectos clave cambian en su comportamiento:

- No publica un RouterInfo en la netDb.
- No acepta túneles participantes.
- Rechaza conexiones directas a routers en el mismo país.

Estas defensas hacen que los routers sean más difíciles de enumerar de manera confiable, y reducen el riesgo de violar prohibiciones locales sobre retransmitir tráfico para otros.

## Lista de Países con Restricciones Estrictas (a partir de 2024)

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
Si crees que un país debería añadirse o eliminarse de la lista estricta, por favor abre un issue: https://i2pgit.org/i2p/i2p.i2p/

Referencia: Freedom House – https://freedomhouse.org/
