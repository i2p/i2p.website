---
title: "Omezené Trasy"
number: "100"
author: "zzz"
created: "2008-09-14"
lastupdated: "2008-10-13"
status: "Reserve"
thread: "http://zzz.i2p/topics/114"
---

## Úvod


## Myšlenky

- Přidat nový transport "IND" (nepřímý), který zveřejní hash leaseSet ve
  struktuře RouterAddress: "IND: [key=aababababababababb]". Tento transport
  nabízí nejnižší prioritu, když cílový směrovač jej zveřejní. Chcete-li poslat
  peerovi přes tento transport, získejte leaseset z ff peer jako obvykle a
  pošlete jej přímo na lease.

- Peer, který inzeruje IND, musí vytvořit a udržovat sadu tunelů k jinému
  peerovi. Nejedná se o průzkumné tunely ani o tunely klienta, ale o druhou sadu
  směrovačových tunelů.

  - Je 1-hop dostatečný?
  - Jak vybrat peer pro tyto tunely?
  - Musí být "neomezené", ale jak to zjistit? Vyhodnocení dosahu?
    Grafová teorie, algoritmy, datové struktury mohou pomoci zde. Je třeba si o
    tom něco prostudovat. Viz tunely TODO.

- Pokud máte IND tunely, pak váš IND transport musí nabízit (nízkou prioritou)
  pro odesílání zpráv těmito tunely.

- Jak rozhodnout o povolení budování nepřímých tunelů

- Jak implementovat a testovat bez odhalení
