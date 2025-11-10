---
title: "Strict/Restrictive Countries"
description: "How I2P behaves in jurisdictions with restrictions on routing or anonymity tools (Hidden Mode and strict list)"
slug: "restrictive-countries"
lastUpdated: "2024-07"
accurateFor: "2.10.0"
aliases:
  - "/en/about/restrictive-countries"
  - "/about/restrictive-countries"
  - "/en/about/restrictive-countries/"
  - "/about/restrictive-countries/"
type: docs
reviewStatus: "needs-review"
---

This implementation of I2P (the Java implementation distributed on this site) includes a “Strict Countries List” used to adjust router behavior in regions where participating in routing for others may be restricted by law. While we are not aware of jurisdictions that prohibit using I2P, several have broad prohibitions on relaying traffic. Routers that appear to be in “strict” countries are automatically placed into Hidden mode.

The Project references research from civil and digital rights organizations when making these decisions. In particular, ongoing research by Freedom House informs our choices. General guidance is to include countries with a Civil Liberties (CL) score of 16 or less, or an Internet Freedom score of 39 or less (not free).

## Hidden Mode Summary

When a router is placed into Hidden mode, three key things change about its behavior:

- It does not publish a RouterInfo to the netDb.
- It does not accept participating tunnels.
- It rejects direct connections to routers in the same country.

These defenses make routers more difficult to enumerate reliably, and reduce the risk of violating local prohibitions on relaying traffic for others.

## Strict Countries List (as of 2024)

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

If you believe a country should be added or removed from the strict list, please open an issue: https://i2pgit.org/i2p/i2p.i2p/

Reference: Freedom House – https://freedomhouse.org/

