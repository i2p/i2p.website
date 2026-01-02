---
title: "Transport SSU2"
date: 2022-10-11
author: "zzz"
description: "Transport SSU2"
categories: ["development"]
API_Translate: vrai
---

## Aperçu

I2P utilise depuis 2005 le protocole de transport UDP résistant à la censure "SSU". En 17 ans, nous avons eu peu de signalements, voire aucun, de blocage de SSU. Cependant, selon les standards actuels en matière de sécurité, de résistance au blocage et de performances, nous pouvons faire mieux. Beaucoup mieux.

C’est pourquoi, en collaboration avec le [projet i2pd](https://i2pd.xyz/), nous avons créé et implémenté "SSU2", un protocole UDP moderne conçu selon les normes les plus élevées en matière de sécurité et de résistance au blocage. Ce protocole remplacera SSU.

Nous avons combiné un chiffrement conforme aux normes de l’industrie avec les meilleures fonctionnalités des protocoles UDP WireGuard et QUIC, ainsi que les fonctionnalités de résistance à la censure de notre protocole TCP "NTCP2". SSU2 pourrait être l’un des protocoles de transport les plus sécurisés jamais conçus.

Les équipes de Java I2P et d'i2pd finalisent le transport SSU2 et nous l'activerons sur tous les routers dans la prochaine version. Cela achève notre plan mené depuis dix ans visant à mettre à niveau toute la cryptographie de l'implémentation Java I2P d'origine, qui remonte à 2003. SSU2 remplacera SSU, notre seul usage restant de la cryptographie ElGamal.

- Signature types and ECDSA signatures (0.9.8, 2013)
- Ed25519 signatures and leasesets (0.9.15, 2014)
- Ed25519 routers (0.9.22, 2015)
- Destination encryption types and X25519 leasesets (0.9.46, 2020)
- Router encryption types and X25519 routers (0.9.49, 2021)

Après la transition vers SSU2, nous aurons migré tous nos protocoles authentifiés et chiffrés vers des handshakes (phase de négociation initiale) standard du [Noise Protocol](https://noiseprotocol.org/) :

- NTCP2 (0.9.36, 2018)
- ECIES-X25519-Ratchet end-to-end protocol (0.9.46, 2020)
- ECIES-X25519 tunnel build messages (1.5.0, 2021)
- SSU2 (2.0.0, 2022)

Tous les protocoles Noise d'I2P utilisent les algorithmes cryptographiques standard suivants:

- [X25519](https://en.wikipedia.org/wiki/Curve25519)
- [ChaCha20/Poly1305 AEAD](https://www.rfc-editor.org/rfc/rfc8439.html)
- [SHA-256](https://en.wikipedia.org/wiki/SHA-2)

## Objectifs

- Upgrade the asymmetric cryptography to the much faster X25519
- Use standard symmetric authenticated encryption ChaCha20/Poly1305
- Improve the obfuscation and blocking resistance features of SSU
- Improve the resistance to spoofed addresses by adapting strategies from QUIC
- Improved handshake CPU efficiency
- Improved bandwidth efficiency via smaller handshakes and acknowledgements
- Improve the security of the peer test and relay features of SSU
- Improve the handling of peer IP and port changes by adapting the "connection migration" feature of QUIC
- Move away from heuristic code for packet handling to documented, algorithmic processing
- Support a gradual network transition from SSU to SSU2
- Easy extensibility using the block concept from NTCP2

## Conception

I2P utilise plusieurs couches de chiffrement pour protéger le trafic contre des attaquants. La couche la plus basse est la couche de transport, utilisée pour les liaisons point à point entre deux routers. Nous disposons actuellement de deux protocoles de transport : NTCP2, un protocole TCP moderne introduit en 2018, et SSU, un protocole UDP développé en 2005.

SSU2, comme les précédents protocoles de transport d'I2P, n'est pas un canal polyvalent pour les données. Sa tâche principale est d'acheminer de façon sécurisée les messages I2NP de bas niveau d'I2P d'un router au suivant. Chacune de ces connexions point à point constitue un saut dans un tunnel I2P. Les protocoles I2P de couche supérieure fonctionnent au-dessus de ces connexions point à point pour acheminer des garlic messages (messages « garlic ») de bout en bout entre les destinations d'I2P.

La conception d’un transport UDP présente des défis uniques et complexes qui n’existent pas dans les protocoles TCP. Un protocole UDP doit gérer les problèmes de sécurité causés par l’usurpation d’adresse et mettre en œuvre son propre contrôle de congestion. De plus, tous les messages doivent être fragmentés pour tenir dans la taille maximale d’un paquet (MTU) du chemin réseau, puis réassemblés par le récepteur.

Nous nous sommes d'abord fortement appuyés sur notre expérience antérieure avec nos protocoles NTCP2, SSU et de streaming. Ensuite, nous avons attentivement examiné et largement emprunté à deux protocoles UDP récemment développés:

- QUIC ([RFC 9000](https://www.rfc-editor.org/rfc/rfc9000.html), [RFC 9001](https://www.rfc-editor.org/rfc/rfc9001.html), [RFC 9002](https://www.rfc-editor.org/rfc/rfc9002.html))
- [WireGuard](https://www.wireguard.com/protocol/)

La classification et le blocage des protocoles par des attaquants on-path (sur le chemin), tels que des pare-feux étatiques, ne font pas explicitement partie du modèle de menace de ces protocoles. Cependant, cela constitue un élément important du modèle de menace d’I2P, puisque notre mission est de fournir un système de communication anonyme et résistant à la censure aux utilisateurs à risque dans le monde entier. Par conséquent, une grande partie de notre travail de conception a consisté à combiner les enseignements tirés de NTCP2 et SSU avec les fonctionnalités et la sécurité prises en charge par QUIC et WireGuard.

## Performances

Le réseau I2P est un mélange complexe de routers variés. Deux implémentations principales tournent partout dans le monde sur du matériel allant de serveurs de centres de données haute performance jusqu’aux Raspberry Pi et aux téléphones Android. Les routers utilisent à la fois les transports TCP et UDP. Bien que les améliorations de SSU2 soient significatives, nous ne nous attendons pas à ce qu’elles soient perceptibles par l’utilisateur, ni localement ni en termes de vitesses de transfert de bout en bout.

Voici quelques points saillants des améliorations estimées pour SSU2 par rapport à SSU :

- 40% reduction in total handshake packet size
- 50% or more reduction in handshake CPU
- 90% or more reduction in ACK overhead
- 50% reduction in packet fragmentation
- 10% reduction in data phase overhead

## Plan de transition

I2P s’efforce de maintenir la rétrocompatibilité, à la fois pour assurer la stabilité du réseau et pour permettre aux anciens routers de rester utiles et sécurisés. Cependant, il existe des limites, car la compatibilité accroît la complexité du code et les exigences de maintenance.

Les projets Java I2P et i2pd activeront tous deux SSU2 par défaut dans leurs prochaines versions (2.0.0 et 2.44.0) fin novembre 2022. Cependant, ils ont des plans différents pour désactiver SSU. I2pd désactivera SSU immédiatement, car SSU2 représente une amélioration majeure par rapport à son implémentation de SSU. Java I2P prévoit de désactiver SSU à la mi-2023, afin de favoriser une transition progressive et de laisser aux routers plus anciens le temps de se mettre à niveau.

## Résumé


Les fondateurs d’I2P ont dû faire plusieurs choix en matière d’algorithmes et de protocoles cryptographiques. Certains de ces choix étaient meilleurs que d’autres, mais, vingt ans plus tard, la plupart accusent leur âge. Bien sûr, nous savions que cela arriverait, et nous avons passé la dernière décennie à planifier et à mettre en œuvre des mises à niveau cryptographiques.

SSU2 a été le dernier et le plus complexe des protocoles à développer dans notre long processus de mise à niveau. UDP repose sur des hypothèses et un modèle de menace particulièrement exigeants. Nous avons d'abord conçu et déployé trois autres variantes des protocoles Noise, ce qui nous a permis d'acquérir de l'expérience et une compréhension plus approfondie des problèmes de sécurité et de conception des protocoles.

Attendez-vous à ce que SSU2 soit activé dans les versions d’i2pd et de Java I2P prévues pour fin novembre 2022. Si la mise à jour se passe bien, personne ne remarquera rien de différent. Les gains de performances, bien que significatifs, ne seront probablement pas mesurables pour la plupart des gens.

Comme d'habitude, nous vous recommandons de mettre à jour vers la nouvelle version dès qu'elle est disponible. La meilleure façon de maintenir la sécurité et d'aider le réseau est d'utiliser la dernière version.
