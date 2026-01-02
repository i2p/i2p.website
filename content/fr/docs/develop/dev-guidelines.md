---
title: "Directives pour les développeurs et style de codage"
description: "Directives complètes pour contribuer à I2P : flux de travail, cycle de publication, style de codage, journalisation, licences et gestion des problèmes"
slug: "dev-guidelines"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
type: docs
---

Lisez d'abord le [Guide des nouveaux développeurs](/docs/develop/new-developers/).

## Directives de base et style de code

La plupart des points suivants devraient être du bon sens pour quiconque a travaillé sur des projets open source ou dans un environnement de programmation commercial. Ce qui suit s'applique principalement à la branche de développement principale i2p.i2p. Les directives pour les autres branches, plugins et applications externes peuvent être substantiellement différentes ; consultez le développeur approprié pour obtenir des conseils.

### Communauté

- Veuillez ne pas vous contenter d'écrire du code. Si vous le pouvez, participez à d'autres activités de développement, notamment : les discussions de développement et le support sur IRC et i2pforum.i2p ; les tests ; les rapports de bugs et les réponses ; la documentation ; les revues de code ; etc.
- Les développeurs actifs devraient être disponibles périodiquement sur IRC `#i2p-dev`. Soyez conscient du cycle de publication actuel. Respectez les jalons de publication tels que le gel des fonctionnalités, le gel des tags et la date limite de check-in pour une version.

### Cycle de publication

Le cycle de publication normal est de 10 à 16 semaines, soit quatre publications par an. Voici les échéances approximatives dans un cycle typique de 13 semaines. Les échéances réelles pour chaque publication sont fixées par le responsable de publication après consultation avec l'équipe complète.

- 1–2 jours après la version précédente : Les commits sur trunk sont autorisés.
- 2–3 semaines après la version précédente : Date limite pour propager les changements majeurs des autres branches vers trunk.
- 4–5 semaines avant la version : Date limite pour demander de nouveaux liens sur la page d'accueil.
- 3–4 semaines avant la version : Gel des fonctionnalités. Date limite pour les nouvelles fonctionnalités majeures.
- 2–3 semaines avant la version : Tenir une réunion de projet pour examiner les demandes de nouveaux liens pour la page d'accueil, le cas échéant.
- 10–14 jours avant la version : Gel des chaînes de caractères. Plus aucune modification aux chaînes traduites (étiquetées). Pousser les chaînes vers Transifex, annoncer la date limite de traduction sur Transifex.
- 10–14 jours avant la version : Date limite des fonctionnalités. Uniquement des corrections de bugs après cette date. Plus de fonctionnalités, de refactorisation ou de nettoyage.
- 3–4 jours avant la version : Date limite de traduction. Récupérer les traductions depuis Transifex et les valider.
- 3–4 jours avant la version : Date limite de commit. Aucun commit après cette date sans l'autorisation du responsable de la version.
- Quelques heures avant la version : Date limite de revue de code.

### Git

- Avoir une compréhension de base des systèmes de contrôle de source distribués, même si vous n'avez jamais utilisé git auparavant. Demandez de l'aide si nécessaire. Une fois poussés, les commits sont permanents ; il n'y a pas d'annulation. Soyez prudent. Si vous n'avez jamais utilisé git auparavant, commencez par de petites étapes. Validez quelques petits changements et voyez comment cela se passe.
- Testez vos modifications avant de les valider. Si vous préférez le modèle de développement commit‑avant‑test, utilisez votre propre branche de développement dans votre propre compte, et créez une MR une fois le travail terminé. Ne cassez pas le build. Ne provoquez pas de régressions. Si cela arrive (ça arrive), ne disparaissez pas pendant une longue période après avoir poussé votre modification.
- Si votre modification n'est pas triviale, ou si vous voulez que les gens la testent et avez besoin de bons rapports de test pour savoir si votre modification a été testée ou non, ajoutez un commentaire de commit dans `history.txt` et incrémentez la révision du build dans `RouterVersion.java`.
- Ne validez pas de changements majeurs dans la branche principale i2p.i2p tard dans le cycle de publication. Si un projet vous prendra plus de quelques jours, créez votre propre branche dans git, dans votre propre compte, et effectuez le développement là-bas pour ne pas bloquer les publications.
- Pour les grands changements (en général, plus de 100 lignes, ou touchant plus de trois fichiers), validez-les dans une nouvelle branche sur votre propre compte GitLab, créez une MR, et assignez un réviseur. Assignez-vous la MR. Fusionnez la MR vous-même une fois que le réviseur l'approuve.
- Ne créez pas de branches WIP dans le compte principal I2P_Developers (sauf pour i2p.www). Les WIP appartiennent à votre propre compte. Lorsque le travail est terminé, créez une MR. Les seules branches du compte principal devraient être pour de véritables forks, comme une publication ponctuelle.
- Effectuez le développement de manière transparente et avec la communauté à l'esprit. Validez souvent. Validez ou fusionnez dans la branche principale aussi fréquemment que possible, compte tenu des directives ci-dessus. Si vous travaillez sur un grand projet dans votre propre branche/compte, informez-en les gens afin qu'ils puissent suivre et réviser/tester/commenter.

### Style de codage

- Le style de codage dans la majeure partie du code est de 4 espaces pour l'indentation. N'utilisez pas de tabulations. Ne reformatez pas le code. Si votre IDE ou éditeur veut tout reformater, maîtrisez-le. Dans certains endroits, le style de codage est différent. Utilisez le bon sens. Imitez le style du fichier que vous modifiez.
- Toutes les nouvelles classes et méthodes publiques et package-private nécessitent des Javadocs. Ajoutez `@since` numéro-de-version. Les Javadocs pour les nouvelles méthodes privées sont souhaitables.
- Pour toutes les Javadocs ajoutées, il ne doit y avoir aucune erreur ou avertissement doclint. Exécutez `ant javadoc` avec Oracle Java 14 ou supérieur pour vérifier. Tous les paramètres doivent avoir des lignes `@param`, toutes les méthodes non-void doivent avoir des lignes `@return`, toutes les exceptions déclarées levées doivent avoir des lignes `@throws`, et aucune erreur HTML.
- Les classes dans `core/` (i2p.jar) et des parties de i2ptunnel font partie de notre API officielle. Il existe plusieurs plugins hors arborescence et autres applications qui dépendent de cette API. Faites attention à ne pas apporter de modifications qui rompent la compatibilité. N'ajoutez pas de méthodes à l'API sauf si elles sont d'utilité générale. Les Javadocs pour les méthodes d'API doivent être claires et complètes. Si vous ajoutez ou modifiez l'API, mettez également à jour la documentation sur le site web (branche i2p.www).
- Balisez les chaînes pour la traduction lorsque cela est approprié, ce qui est vrai pour toutes les chaînes d'interface utilisateur. Ne modifiez pas les chaînes balisées existantes sauf si c'est vraiment nécessaire, car cela cassera les traductions existantes. N'ajoutez pas ou ne modifiez pas les chaînes balisées après le gel des balises dans le cycle de publication afin que les traducteurs aient la possibilité de mettre à jour avant la sortie.
- Utilisez les génériques et les classes concurrentes dans la mesure du possible. I2P est une application hautement multi-threadée.
- Familiarisez-vous avec les pièges Java courants qui sont détectés par FindBugs/SpotBugs. Exécutez `ant findbugs` pour en savoir plus.
- Java 8 est requis pour compiler et exécuter I2P depuis la version 0.9.47. N'utilisez pas de classes ou méthodes Java 7 ou 8 dans les sous-systèmes embarqués : addressbook, core, i2ptunnel.jar (non-UI), mstreaming, router, routerconsole (news uniquement), streaming. Ces sous-systèmes sont utilisés par Android et des applications embarquées qui ne nécessitent que Java 6. Toutes les classes doivent être disponibles dans Android API 14. Les fonctionnalités du langage Java 7 sont acceptables dans ces sous-systèmes si elles sont prises en charge par la version actuelle du SDK Android et qu'elles compilent en code compatible Java 6.
- Try-with-resources ne peut pas être utilisé dans les sous-systèmes embarqués car il nécessite `java.lang.AutoCloseable` dans le runtime, et ceci n'est pas disponible avant Android API 19 (KitKat 4.4).
- Le package `java.nio.file` ne peut pas être utilisé dans les sous-systèmes embarqués car il n'est pas disponible avant Android API 26 (Oreo 8).
- Outre les limitations ci-dessus, les classes, méthodes et constructions Java 8 peuvent être utilisées uniquement dans les sous-systèmes suivants : BOB, desktopgui, i2psnark, i2ptunnel.war (UI), jetty-i2p.jar, jsonrpc, routerconsole (sauf news), SAM, susidns, susimail, systray.
- Les auteurs de plugins peuvent exiger n'importe quelle version minimale de Java via le fichier `plugin.config`.
- Convertissez explicitement entre les types primitifs et les classes ; ne vous fiez pas à l'autoboxing/unboxing.
- N'utilisez pas `URL`. Utilisez `URI`.
- N'attrapez pas `Exception`. Attrapez `RuntimeException` et les exceptions vérifiées individuellement.
- N'utilisez pas `String.getBytes()` sans argument charset UTF-8. Vous pouvez également utiliser `DataHelper.getUTF8()` ou `DataHelper.getASCII()`.
- Spécifiez toujours un charset UTF-8 lors de la lecture ou de l'écriture de fichiers. Les utilitaires `DataHelper` peuvent être utiles.
- Spécifiez toujours une locale (par exemple `Locale.US`) lors de l'utilisation de `String.toLowerCase()` ou `String.toUpperCase()`. N'utilisez pas `String.equalsIgnoreCase()`, car une locale ne peut pas être spécifiée.
- N'utilisez pas `String.split()`. Utilisez `DataHelper.split()`.
- N'ajoutez pas de code pour formater les dates et heures. Utilisez `DataHelper.formatDate()` et `DataHelper.formatTime()`.
- Assurez-vous que les `InputStream`s et `OutputStream`s sont fermés dans des blocs finally.
- Utilisez `{}` pour tous les blocs `for` et `while`, même si une seule ligne. Si vous utilisez `{}` pour le bloc `if`, `else` ou `if-else`, utilisez-le pour tous les blocs. Mettez `} else {` sur une seule ligne.
- Spécifiez les champs comme `final` partout où c'est possible.
- Ne stockez pas `I2PAppContext`, `RouterContext`, `Log`, ou toute autre référence aux éléments du router ou du contexte dans des champs statiques.
- Ne démarrez pas de threads dans les constructeurs. Utilisez `I2PAppThread` au lieu de `Thread`.

### Journalisation

Les directives suivantes s'appliquent au router, aux applications web et à tous les plugins.

- Pour tous les messages qui ne sont pas affichés au niveau de log par défaut (WARN, INFO et DEBUG), sauf si le message est une chaîne statique (sans concaténation), utilisez toujours `log.shouldWarn()`, `log.shouldInfo()` ou `log.shouldDebug()` avant l'appel au log pour éviter une allocation d'objets inutile.
- Les messages de log susceptibles d'être affichés au niveau de log par défaut (ERROR, CRIT et `logAlways()`) doivent être brefs, clairs et compréhensibles pour un utilisateur non technique. Cela inclut le texte des raisons d'exception qui peuvent également être affichés. Envisagez de traduire si l'erreur est susceptible de se produire (par exemple, lors d'erreurs de soumission de formulaire). Sinon, la traduction n'est pas nécessaire, mais il peut être utile de rechercher et de réutiliser une chaîne déjà marquée pour la traduction ailleurs.
- Les messages de log qui ne sont pas affichés au niveau de log par défaut (WARN, INFO et DEBUG) sont destinés à l'usage des développeurs et n'ont pas les exigences ci-dessus. Cependant, les messages WARN sont disponibles dans l'onglet log Android et peuvent aider les utilisateurs à déboguer des problèmes, donc faites également attention aux messages WARN.
- Les messages de log INFO et DEBUG doivent être utilisés avec parcimonie, en particulier dans les chemins de code critiques. Bien qu'utiles pendant le développement, envisagez de les supprimer ou de les mettre en commentaire une fois les tests terminés.
- Ne loguez pas vers stdout ou stderr (wrapper log).

### Licences

- Ne soumettez que du code que vous avez écrit vous-même. Avant de soumettre du code ou des fichiers JAR de bibliothèques provenant d'autres sources, justifiez pourquoi c'est nécessaire, vérifiez que la licence est compatible et obtenez l'approbation du gestionnaire de version.
- Si vous obtenez l'approbation pour ajouter du code externe ou des fichiers JAR, et que des binaires sont disponibles dans un paquet Debian ou Ubuntu, vous devez implémenter des options de compilation et d'empaquetage pour utiliser le paquet externe à la place. Liste des fichiers à modifier : `build.properties`, `build.xml`, `debian/control`, `debian/i2p-router.install`, `debian/i2p-router.links`, `debian/rules`, `sub-build.xml`.
- Pour toute image soumise provenant de sources externes, il est de votre responsabilité de vérifier d'abord que la licence est compatible. Incluez la licence et les informations sur la source dans le commentaire de soumission.

### Bugs

- La gestion des problèmes est l'affaire de tous ; merci d'aider. Surveillez [GitLab](https://i2pgit.org/I2P_Developers/i2p.i2p/issues) pour les problèmes sur lesquels vous pouvez aider. Commentez, corrigez et fermez les problèmes si vous le pouvez.
- Les nouveaux développeurs devraient commencer par corriger des problèmes. Lorsque vous avez un correctif, joignez votre patch au problème et ajoutez le mot-clé `review-needed`. Ne fermez pas le problème tant qu'il n'a pas été examiné avec succès et que vous n'avez pas vérifié vos modifications. Une fois que vous avez fait cela sans accroc pour quelques tickets, vous pouvez suivre la procédure normale ci-dessus.
- Fermez un problème lorsque vous pensez l'avoir corrigé. Nous n'avons pas de département de test pour vérifier et fermer les tickets. Si vous n'êtes pas sûr de l'avoir corrigé, fermez-le et ajoutez une note disant "Je pense l'avoir corrigé, veuillez tester et rouvrir si c'est toujours cassé". Ajoutez un commentaire avec le numéro de build de développement ou la révision et définissez le jalon pour la prochaine version.
