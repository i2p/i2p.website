---
title: "Notes d’état d’I2P du 2004-08-31"
date: 2004-08-31
author: "jr"
description: "Mise à jour hebdomadaire de l’état d’I2P couvrant la dégradation des performances réseau, la planification de la version 0.3.5, les besoins en documentation et l’avancement du DHT Stasher"
categories: ["status"]
---

Bon, les gars et les filles, c'est encore mardi !

## Index:

1. 0.3.4.3
2. 0.3.5 and 0.4
3. docs
4. stasher update
5. ???

## 1) 0.3.4.3

Eh bien, comme vous l’avez tous remarqué, bien que le nombre d’utilisateurs sur le réseau soit resté assez stable, les performances se sont considérablement dégradées ces derniers jours. La cause en est une série de bogues dans le code de sélection des pairs et d’acheminement des messages, révélés lorsqu’il y a eu une attaque par déni de service mineure (DoS) la semaine dernière. Il en a résulté qu’en gros, les tunnels de tout le monde n’ont cessé d’échouer, ce qui a un effet boule de neige. Donc non, ce n’est pas que chez vous — le réseau a été horrible pour le reste d’entre nous aussi ;)

Mais la bonne nouvelle, c'est que nous avons corrigé les problèmes assez rapidement, et les correctifs sont dans CVS depuis la semaine dernière, mais la qualité du réseau restera médiocre pour les utilisateurs jusqu'à la sortie de la prochaine version. À ce propos...

## 2) 0.3.5 et 0.4

Bien que la prochaine version inclue toutes les nouveautés que nous avons prévues pour la version 0.4 (nouveau programme d'installation, nouveau standard d'interface web, nouvelle interface i2ptunnel, systray (zone de notification) & service Windows, améliorations du multithreading, corrections de bogues, etc), la manière dont la dernière version s'est dégradée au fil du temps était révélatrice. Je souhaite que nous avancions plus lentement sur ces versions, en leur laissant le temps de se déployer plus largement et de laisser apparaître les accrocs. Même si le simulateur peut explorer les bases, il n'a aucun moyen de simuler les problèmes réseau inhérents que nous observons sur le réseau en production (du moins, pas encore).

Par conséquent, la prochaine version sera la 0.3.5 - avec un peu de chance la dernière version 0.3.*, mais peut-être pas, si d’autres problèmes surviennent. En revenant sur la façon dont le réseau fonctionnait lorsque j’étais hors ligne en juin, les choses ont commencé à se dégrader au bout d’environ deux semaines. Par conséquent, je pense qu’il vaut mieux attendre avant de nous faire passer au palier de version 0.4 jusqu’à ce que nous puissions maintenir un haut degré de fiabilité pendant au moins deux semaines. Cela ne veut pas dire que nous ne travaillerons pas entre-temps, bien sûr.

Quoi qu’il en soit, comme mentionné la semaine dernière, hypercubus travaille d’arrache-pied sur le nouveau système d’installation, tout en gérant le fait que je remanie des éléments et que j’exige la prise en charge de systèmes farfelus. Nous devrions régler les derniers détails dans les prochains jours afin de publier une version 0.3.5 dans les prochains jours.

## 3) documentation

Une des choses importantes que nous devons faire pendant ces deux semaines de "fenêtre de test" avant 0.4, c'est de documenter à fond. Ce que je me demande, c'est ce qui, selon vous, manque à notre documentation - quelles questions avez-vous auxquelles nous devons répondre ? Même si j'aimerais dire "ok, maintenant, allez écrire ces documents", je suis réaliste, donc tout ce que je demande, c'est que vous puissiez identifier ce que ces documents devraient aborder.

Par exemple, l’un des documents sur lesquels je travaille actuellement est une révision du modèle de menace, que je décrirais désormais comme une série de cas d’utilisation expliquant comment I2P peut répondre aux besoins de différentes personnes, y compris les fonctionnalités, les adversaires que cette personne redoute, et la manière dont elle se protège.

Si vous estimez que votre question ne nécessite pas un document complet pour y répondre, formulez-la simplement sous forme de question et nous pourrons l’ajouter à la FAQ.

## 4) mise à jour de stasher

Aum est passé sur le canal plus tôt aujourd’hui avec une mise à jour (pendant que je le bombardais de questions) :

```
<aum> quick stasher update, with apologies for tomorrow's meeting:
<aum> infinite-level splitfiles working, have successfully
      inserted and retrieved large files
<jrandom> w00t
<aum> splitfile fragmentation/reassembly transparently occuring
      within stasher
<aum> freenet interface working
<jrandom> wow
<jrandom> so FUQID/FIW works?
<aum> use of fcp splitfile commands in freenet clients strictly
      forbidden (at this stage)
<aum> most clients such as fuqid/fiw should allow setting
      extremely large splitfile sizes, which should prevent them
      trying to talk splitfiles
<aum> if not, then i can dummy up something
<jrandom> r0x0r aum, that kicks ass!
<aum> hooks are in for detailed freenet key support
<jrandom> detailed freenet key support?
<aum> yes, specific chk@, ssk@, ksk@
<jrandom> ok great, so they're all verified @ each node, etc?
<aum> no - only verifiable by the requestor
<aum> my thinking is, given KSK@fred = 'mary',
<aum> to store as SHA1(SHA1("KSK@fred")) = E(mary), where key
      for E is SHA1("KSK@fred")
<aum> ie, crypto key is SHA1(uri), and kademlia key is
      SHA1(SHA1(uri))
<jrandom> hm
<aum> so a possessor of the URI can decyrpt, but owner of a
      datastore cannot decrypt (and therefore has plausible
      deniability)
<jrandom> well, ksks are inherently insecure, so thats no big
      loss, but what about ssk?
<deer> <detonate> those keys aren't very large
<aum> SSK as for freenet
<jrandom> so the SSKs are verified at each node?
<aum> except i'm looking to use same encryption over the top
<aum> not feasible to verify SSK at the target node
<jrandom> why not?  freenet does
<aum> well maybe it is feasible,
<aum> i guess i shouldn't be so lazy
<aum> i was trying to keep the kademlia and freenet layers
      separate
<jrandom> heh, you're not being lazy, there's a truckload of
      work here, and you're doing a great job
<aum> verifying on target node will cause some pathological
      couplings between the two layers, and force deviation
      from pure kademlia
<jrandom> i dont think its possible to do SSKs or CHKs
      securely without having the node validate the key
      properties
<aum> not correct
<aum> fred asks mary, 'gimme SSK@madonna'
<aum> mary sends back what she thinks is 'SSK@madonna'
<aum> fred tests it, barfs, then goes on to ask the next node
<aum> anyway, i MUST go - but am open to continuing discussion
      over email, or tomorrow
<aum> bbl guys
<jrandom> mallory floods the net with 'SSK@madonna' ==
      'sexDrugsRockNRoll'
<jrandom> l8r aum
```
Donc, comme vous pouvez le voir, beaucoup, beaucoup de progrès. Même si les clés sont validées au-dessus de la couche DHT (table de hachage distribuée), c’est vraiment trop cool (à mon humble avis). Allez aum !

## 5) ???

Ok, c'est tout ce que j'ai à dire (tant mieux, la réunion commence dans quelques instants)... passez faire un saut et dites ce que vous voulez !

=jr
