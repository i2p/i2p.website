---
title: "Notes d'état I2P du 2005-01-25"
date: 2005-01-25
author: "jr"
description: "Notes hebdomadaires sur l’état du développement d’I2P couvrant l’avancement du routage de tunnel 0.5, le portage de SAM vers .NET, la compilation GCJ et les discussions sur le transport UDP"
categories: ["status"]
---

Salut à tous, bref point d’avancement hebdomadaire

* Index

1) statut de la 0.5 2) sam.net 3) avancement de gcj 4) udp 5) ???

* 1) 0.5 status

Au cours de la semaine écoulée, il y a eu beaucoup de progrès du côté de la 0.5. Les problèmes dont nous parlions auparavant ont été résolus, simplifiant considérablement la cryptographie et éliminant le problème de bouclage des tunnels. La nouvelle technique [1] a été implémentée et les tests unitaires sont en place. Ensuite, je vais assembler davantage de code pour intégrer ces tunnels dans le router principal, puis mettre en place l’infrastructure de gestion et de pooling (mise en pool) des tunnels. Une fois que cela sera en place, nous le ferons passer dans le simulateur puis sur un réseau parallèle pour l’éprouver, avant de finaliser et de l’appeler 0.5.

[1] http://dev.i2p.net/cgi-bin/cvsweb.cgi/i2p/router/doc/tunnel-alt.html?rev=HEAD

* 2) sam.net

smeghead a mis au point un nouveau port du protocole SAM vers .net - compatible c#, mono/gnu.NET (youpi smeghead!).  C’est dans cvs sous i2p/apps/sam/csharp/ avec nant et d’autres utilitaires - maintenant, tous les devs .net peuvent commencer à bidouiller avec i2p :)

* 3) gcj progress

smeghead est clairement sur sa lancée - au dernier décompte, avec quelques modifications, le router se compile avec la dernière version de gcj [2] (w00t!). Il ne fonctionne toujours pas, mais les modifications visant à contourner la confusion de gcj avec certaines constructions de classes internes représentent assurément un progrès. Peut-être que smeghead peut nous donner des nouvelles ?

[2] http://gcc.gnu.org/java/

* 4) udp

Pas grand-chose à dire ici, même si Nightblade a soulevé sur le forum une série de préoccupations intéressantes [3] en demandant pourquoi nous optons pour l'UDP. Si vous avez des préoccupations similaires ou d'autres suggestions sur la manière dont nous pouvons traiter les problèmes que j'ai évoqués dans ma réponse, n'hésitez pas à intervenir !

[3] http://forum.i2p.net/viewtopic.php?t=280

* 5) ???

Ouais, ok, je suis encore en retard avec les notes, retirez-le de mon salaire ;) Bref, il se passe plein de choses, donc soit vous passez sur le canal pour la réunion, soit vous consultez ensuite les logs publiés, soit vous écrivez sur la liste si vous avez quelque chose à dire. Ah, au passage, j’ai fini par céder et ouvrir un blog dans i2p [4].

=jr [4] http://jrandom.dev.i2p/ (clé dans http://dev.i2p.net/i2p/hosts.txt)
