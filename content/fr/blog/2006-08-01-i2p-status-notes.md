---
title: "Notes de statut I2P pour 2006-08-01"
date: 2006-08-01
author: "jr"
description: "Solides performances réseau avec des débits de transfert élevés avec I2PSnark, une stabilité du transport NTCP et des clarifications concernant l’accessibilité des eepsites"
categories: ["status"]
---

Salut à tous, voici quelques notes rapides avant la réunion de ce soir. Je me rends compte que vous aurez peut-être diverses questions ou points à soulever, donc nous adopterons un format plus fluide que d'habitude. Il y a juste quelques points que je souhaite mentionner d'abord.

* Network status

Il semble que le réseau se porte plutôt bien, avec des essaims de transferts I2PSnark assez volumineux qui se terminent, et avec des débits de transfert assez substantiels atteints sur des routers individuels — j’ai vu 650KBytes/sec et 17,000 tunnels participants sans incident. Les routers les moins performants semblent aussi bien s’en sortir, la navigation sur des eepsites(Sites I2P) et l’irc avec des tunnels à 2 sauts utilisant en moyenne moins de 1KByte/sec.

Tout n’est pas rose pour tout le monde pour autant, mais nous travaillons à mettre à jour le comportement du router afin de permettre des performances plus régulières et plus utilisables.

* NTCP

Le nouveau transport NTCP ("new" tcp) se porte plutôt bien après avoir surmonté les déboires initiaux. Pour répondre à une question fréquente, à long terme, NTCP et SSU seront tous deux en fonctionnement - nous ne revenons pas au seul TCP.

* eepsite(I2P Site) reachability

N’oubliez pas que les eepsites(I2P Sites) ne sont accessibles que lorsque la personne qui les fait tourner les maintient en ligne - s’ils sont hors ligne, vous ne pouvez rien faire pour y accéder ;) Malheureusement, ces derniers jours, orion.i2p n’a pas été accessible, mais le réseau fonctionne bel et bien - passez faire un tour sur inproxy.tino.i2p ou eepsites(I2P Sites).i2p pour vos besoins d’analyse du réseau.

Quoi qu'il en soit, il se passe beaucoup d'autres choses, mais il serait un peu prématuré d'en parler ici. Bien sûr, si vous avez des questions ou des préoccupations, passez faire un tour sur #i2p d'ici quelques minutes pour notre *cough* réunion hebdomadaire de développement.

Merci pour votre aide, qui nous fait avancer ! =jr
