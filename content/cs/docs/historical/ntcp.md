---
title: "Diskuse o NTCP"
description: "Historické poznámky k porovnání transportů NTCP a SSU a návrhy na ladění"
slug: "ntcp"
layout: "single"
reviewStatus: "needs-review"
---

## NTCP vs. SSU Diskuse (březen 2007)

### Otázky k NTCP

_Upraveno podle konverzace na IRC mezi zzz a cervantes._

- **Proč má NTCP prioritu před SSU, když NTCP zdánlivě přidává režii a latenci?**  
  NTCP obecně poskytuje lepší spolehlivost než původní implementace SSU.
- **Naráží streamování přes NTCP na klasický TCP-over-TCP collapse (kolaps TCP při vrstvení TCP v TCP)?**  
  Je to možné, ale SSU byl zamýšlen jako lehká možnost na bázi UDP a v praxi se ukázal jako příliš nespolehlivý.

### “NTCP považováno za škodlivé” (zzz, 25. března 2007)

Shrnutí: Vyšší latence a režie NTCP mohou způsobovat přetížení, přesto směrování upřednostňuje NTCP, protože jeho hodnoty skóre nabídek jsou pevně nastavené nižší než u SSU. Analýza poukázala na několik bodů:

- NTCP má aktuálně nižší bid (hodnota nabídky používaná při výběru transportu) než SSU, takže routery preferují NTCP, pokud už není navázána relace SSU.
- SSU implementuje potvrzení přijetí s přísně omezenými časovými limity a statistikami; NTCP se spoléhá na Java NIO TCP s časovými limity ve stylu RFC, které mohou být mnohem delší.
- Většina provozu (HTTP, IRC, BitTorrent) používá streamovací knihovnu I2P, což fakticky vrství TCP nad NTCP. Když obě vrstvy provádějí retransmise, může dojít ke kolapsu. Klasické odkazy zahrnují [TCP over TCP is a bad idea](http://sites.inka.de/~W1011/devel/tcp-tcp.html).
- Časové limity ve streamovací knihovně byly ve verzi 0.8 zvýšeny z 10 s na 45 s; maximální časový limit SSU je 3 s, zatímco časové limity NTCP se předpokládají až kolem 60 s (doporučení RFC). Parametry NTCP je zvenčí těžké zkoumat.
- Terénní pozorování v roce 2007 ukázala, že propustnost odesílání i2psnarku oscilovala, což naznačuje periodický kolaps z přetížení.
- Testy efektivity (vynucení preference SSU) snížily poměry režie tunnelu zhruba z 3.5:1 na 3:1 a zlepšily streamovací metriky (velikost okna, RTT, poměr send/ack).

#### Návrhy z vlákna z roku 2007

1. **Přehodit priority transportů** tak, aby routers preferovaly SSU (obnovením `i2np.udp.alwaysPreferred`).
2. **Označit streamingový provoz** tak, aby SSU snižovalo prioritu pouze u označených zpráv, aniž by to ohrozilo anonymitu.
3. **Zpřísnit limity retransmisí SSU** pro snížení rizika kolapsu.
4. **Prostudovat semi-reliable underlays (polospolehlivé spodní vrstvy)** a určit, zda retransmise pod streamingovou knihovnou jsou čistým přínosem.
5. **Zrevidovat prioritní fronty a časové limity**—například zvýšit časové limity pro streaming nad 45 s, aby se sladily s NTCP.

### Odpověď od jrandom (27. března 2007)

Klíčové protiargumenty:

- NTCP existuje, protože raná nasazení SSU trpěla kolapsem způsobeným zahlcením. I poměrně nízké per‑hop míry retransmisí se mohou napříč vícehopovými tunnels lavinovitě násobit.
- Bez potvrzení na úrovni tunnelu obdrží stav end‑to‑end doručení jen část zpráv; selhání mohou zůstat bez povšimnutí.
- Řízení zahlcení v TCP má za sebou desetiletí optimalizací; NTCP je využívá prostřednictvím vyzrálých implementací TCP.
- Pozorovaná zlepšení efektivity při preferování SSU mohou spíše odrážet chování front v routeru než vlastní výhody protokolu.
- Delší časové limity pro streaming již zlepšovaly stabilitu; před zásadními změnami byly doporučeny další pozorování a sběr dat.

Debata pomohla upřesnit následné ladění transportních protokolů, ale neodráží moderní architekturu NTCP2/SSU2.
