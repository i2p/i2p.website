---
title: "Discussion sur NTCP"
description: "Notes historiques comparant les transports NTCP et SSU et des idées d’optimisation proposées"
slug: "ntcp"
layout: "single"
reviewStatus: "needs-review"
---

## Discussion NTCP (protocole de transport chiffré sur TCP d'I2P) vs. SSU (mars 2007)

### Questions sur NTCP

_Adapté d'une conversation sur IRC entre zzz et cervantes._

- **Pourquoi NTCP est-il prioritaire par rapport à SSU alors que NTCP semble ajouter de la surcharge et de la latence ?**  
  NTCP offre généralement une meilleure fiabilité que l'implémentation SSU d'origine.
- **Le streaming sur NTCP se heurte-t-il à l'effondrement classique du TCP-sur-TCP ?**  
  C'est possible, mais SSU était censé être l'option UDP légère et s'est révélé trop peu fiable en pratique.

### « NTCP (protocole de transport d'I2P) considéré nuisible » (zzz, 25 mars 2007)

Résumé : la latence et la surcharge plus élevées de NTCP peuvent provoquer de la congestion, mais le routage privilégie NTCP parce que ses scores de bid (valeurs d'enchère) sont codés en dur à un niveau inférieur à ceux de SSU. L’analyse a soulevé plusieurs points :

- NTCP a actuellement un coût inférieur à SSU, si bien que les routers préfèrent NTCP, sauf si une session SSU est déjà établie.
- SSU met en œuvre des accusés de réception avec des temporisations strictement bornées et des statistiques ; NTCP s’appuie sur Java NIO TCP avec des temporisations de type RFC, potentiellement bien plus longues.
- La plupart du trafic (HTTP, IRC, BitTorrent) utilise la bibliothèque de streaming d’I2P, ce qui revient à superposer TCP à NTCP. Lorsque les deux couches retransmettent, un effondrement est possible. Les références classiques incluent [TCP over TCP is a bad idea](http://sites.inka.de/~W1011/devel/tcp-tcp.html).
- Les temporisations de la bibliothèque de streaming sont passées de 10 s à 45 s dans la version 0.8 ; le délai d’expiration maximal de SSU est de 3 s, tandis que les délais d’expiration de NTCP sont supposés avoisiner 60 s (recommandation RFC). Les paramètres NTCP sont difficiles à inspecter de l’extérieur.
- Des observations sur le terrain en 2007 ont montré que le débit d’envoi d’i2psnark oscillait, ce qui suggère des épisodes périodiques d’effondrement par congestion.
- Des tests d’efficacité (en forçant la préférence pour SSU) ont réduit les rapports de surcharge de tunnel d’environ 3.5:1 à 3:1 et amélioré les métriques de streaming (taille de fenêtre, RTT, ratio envoi/accusé de réception).

#### Propositions du fil de discussion de 2007

1. **Inverser les priorités de transport** pour que les routers préfèrent SSU (en restaurant `i2np.udp.alwaysPreferred`).
2. **Marquer le trafic de streaming** afin que SSU n’offre une enchère plus faible que pour les messages marqués, sans compromettre l’anonymat.
3. **Resserrer les limites de retransmission de SSU** pour réduire le risque d’effondrement.
4. **Étudier les sous-couches semi-fiables** afin de déterminer si les retransmissions en dessous de la bibliothèque de streaming sont un bénéfice net.
5. **Réexaminer les files de priorité et les délais d’expiration**—par exemple, augmenter les délais d’expiration du streaming au-delà de 45 s pour s’aligner sur NTCP.

### Réponse de jrandom (27 mars 2007)

Principaux contre-arguments :

- NTCP existe parce que les premiers déploiements de SSU ont subi un effondrement dû à la congestion. Même des taux de retransmission modestes par saut peuvent exploser à travers des tunnels multi-sauts.
- Sans accusés de réception au niveau du tunnel, seule une fraction des messages reçoit un statut de livraison de bout en bout ; les échecs peuvent être silencieux.
- Le contrôle de congestion TCP bénéficie de plusieurs décennies d’optimisations ; NTCP en tire parti via des piles TCP matures.
- Les gains d’efficacité observés lorsqu’on privilégie SSU pourraient refléter le comportement de mise en file d’attente du router plutôt que des avantages intrinsèques du protocole.
- Des délais d’expiration de streaming plus longs amélioraient déjà la stabilité ; davantage d’observations et de données étaient encouragées avant des changements majeurs.

Le débat a contribué à affiner les réglages de transport ultérieurs, mais il ne reflète pas l'architecture NTCP2/SSU2 moderne.
