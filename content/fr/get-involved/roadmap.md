---
title: "Feuille de Route de Développement d'I2P"
description: "Plans de développement actuels et jalons historiques pour le réseau I2P"
---

<div style="background: var(--color-bg-secondary); border-left: 4px solid var(--color-primary); padding: 1.5rem; margin-bottom: 2rem; border-radius: var(--radius-md);">

**I2P suit un modèle de développement incrémental** avec des versions environ toutes les 13 semaines. Cette feuille de route couvre les versions Java de bureau et Android dans une seule voie de version stable.

**Dernière mise à jour :** Août 2025

</div>

## 🎯 Prochaines Versions

<div style="border-left: 3px solid var(--color-accent); padding-left: 1.5rem; margin-bottom: 2rem;">

### Version 2.11.0
<div style="display: inline-block; background: var(--color-accent); color: white; padding: 0.25rem 0.75rem; border-radius: var(--radius-md); font-size: 0.875rem; margin-bottom: 1rem;">
Cible : Début décembre 2025
</div>

- Hybrid PQ MLKEM Ratchet final, activé par défaut (prop. 169)
- Jetty 12, nécessite Java 17+
- Continuation des travaux sur PQ (transports) (prop. 169)
- Support de recherche I2CP pour les paramètres d'enregistrement de service LS (prop. 167)
- Limitation par tunnel
- Sous-système de stat compatible Prometheus
- Support SAM pour Datagram 2/3

</div>

---

## 📦 Versions Récentes

### Versions 2025

<div style="background: var(--color-bg-secondary); padding: 1.5rem; border-radius: var(--radius-md); margin-bottom: 1.5rem; border-left: 4px solid var(--color-success);">

**Version 2.10.0** <span style="color: var(--color-text-muted); font-size: 0.9rem;">— Publiée le 8 septembre 2025</span>

- Support de tracker UDP i2psnark (prop. 160)
- Paramètres d'enregistrement de service LS I2CP (partiel) (prop. 167)
- API de recherche asynchrone I2CP
- Hybrid PQ MLKEM Ratchet Beta (prop. 169)
- Continuation des travaux sur PQ (transports) (prop. 169)
- Paramètres de bande passante de construction de tunnel (prop. 168) Partie 2 (traitement)
- Continuer le travail sur la limitation par tunnel
- Supprimer le code ElGamal inutilisé pour le transport
- Supprimer le code ancien "active throttle" SSU2
- Supprimer le support de journalisation de stat ancien
- Nettoyage du sous-système de stat/graphique
- Améliorations et corrections du mode caché

</div>

<div style="background: var(--color-bg-secondary); padding: 1.5rem; border-radius: var(--radius-md); margin-bottom: 1.5rem; border-left: 4px solid var(--color-success);">

**Version 2.9.0** <span style="color: var(--color-text-muted); font-size: 0.9rem;">— Publiée le 2 juin 2025</span>

- Carte netdb
- Implémentation de Datagram2, Datagram3 (prop. 163)
- Commencer le travail sur le paramètre d'enregistrement de service LS (prop. 167)
- Commencer le travail sur PQ (prop. 169)
- Continuer le travail sur la limitation par tunnel
- Paramètres de bande passante de construction de tunnel (prop. 168) Partie 1 (envoi)
- Utilisation de /dev/random pour PRNG par défaut sous Linux
- Supprimer le code redondant de rendu LS
- Afficher le changelog en HTML
- Réduire l'utilisation des threads de serveur HTTP
- Corriger l'inscription auto-floodfill
- Mise à jour de Wrapper vers 3.5.60

</div>

<div style="background: var(--color-bg-secondary); padding: 1.5rem; border-radius: var(--radius-md); margin-bottom: 1.5rem; border-left: 4px solid var(--color-success);">

**Version 2.8.2** <span style="color: var(--color-text-muted); font-size: 0.9rem;">— Publiée le 29 mars 2025</span>

- Correction d'un bug de corruption SHA256

</div>

<div style="background: var(--color-bg-secondary); padding: 1.5rem; border-radius: var(--radius-md); margin-bottom: 1.5rem; border-left: 4px solid var(--color-success);">

**Version 2.8.1** <span style="color: var(--color-text-muted); font-size: 0.9rem;">— Publiée le 17 mars 2025</span>

- Correction d'échec d'installation sur Java 21+
- Correction du bug de "bouclage"
- Corrige les tests de tunnel pour les tunnels clients sortants
- Corriger l'installation dans les chemins avec des espaces
- Mise à jour des conteneurs Docker obsolètes et des bibliothèques de conteneurs
- Bulles de notification de console
- Trie par les plus récents dans SusiDNS
- Utiliser le pool SHA256 dans Noise
- Corrections et améliorations du thème sombre de la console
- Support .i2p.alt

</div>

<div style="background: var(--color-bg-secondary); padding: 1.5rem; border-radius: var(--radius-md); margin-bottom: 1.5rem; border-left: 4px solid var(--color-success);">

**Version 2.8.0** <span style="color: var(--color-text-muted); font-size: 0.9rem;">— Publiée le 3 février 2025</span>

- Améliorations de publication RouterInfo
- Amélioration de l'efficacité des confirmations SSU2
- Amélioration de la gestion des messages de relais dupliqués SSU2
- Délai d'expiration de recherche plus rapide / variable
- Améliorations de l'expiration LS
- Changement de la capacité NAT symétrique
- Imposer POST dans plus de formulaires
- Corrections du thème sombre de SusiDNS
- Nettoyage de tests de bande passante
- Nouvelle traduction en chinois Gan
- Ajouter l'option d'interface utilisateur kurde
- Nouvelle construction Jammy
- Izpack 5.2.3
- rrd4j 3.10

</div>

<div style="margin: 3rem 0; padding: 1rem 0; border-top: 2px solid var(--color-border); border-bottom: 2px solid var(--color-border);">
  <h3 style="margin: 0; color: var(--color-primary);">📅 Versions 2024</h3>
</div>

<div style="background: var(--color-bg-secondary); padding: 1.5rem; border-radius: var(--radius-md); margin-bottom: 1.5rem; border-left: 4px solid var(--color-primary);">

**Version 2.7.0** <span style="color: var(--color-text-muted); font-size: 0.9rem;">— 8 octobre 2024</span>

- Réduction de l'utilisation de thread du serveur HTTP i2ptunnel
- Tunnels UDP génériques dans I2PTunnel
- Proxy de navigateur dans I2PTunnel
- Migration de site Web
- Correction pour tunnels devenant jaunes
- Refactorisation de la console /netdb

</div>

<div style="background: var(--color-bg-secondary); padding: 1.5rem; border-radius: var(--radius-md); margin-bottom: 1.5rem; border-left: 4px solid var(--color-primary);">

**Version 2.6.1** <span style="color: var(--color-text-muted); font-size: 0.9rem;">— 6 août 2024</span>

- Correction des problèmes de taille d'iframe dans la console
- Convertir les graphiques en SVG
- Rapport d'état de traduction groupé

</div>

<div style="background: var(--color-bg-secondary); padding: 1.5rem; border-radius: var(--radius-md); margin-bottom: 1.5rem; border-left: 4px solid var(--color-primary);">

**Version 2.6.0** <span style="color: var(--color-text-muted); font-size: 0.9rem;">— 19 juillet 2024</span>

- Réduire l'utilisation de la mémoire netdb
- Supprimer le code SSU1
- Corriger les fuites de fichiers temporaires i2psnark et les blocages
- PEX plus efficace dans i2psnark
- Actualisation JS des graphiques de la console
- Améliorations du rendu des graphiques
- Recherche JS dans Susimail
- Gestion plus efficace des messages à OBEP
- Recherches I2CP de destination locale plus efficaces
- Corriger les problèmes de portée de variable JS

</div>

<div style="background: var(--color-bg-secondary); padding: 1.5rem; border-radius: var(--radius-md); margin-bottom: 1.5rem; border-left: 4px solid var(--color-primary);">

**Version 2.5.2** <span style="color: var(--color-text-muted); font-size: 0.9rem;">— 15 mai 2024</span>

- Corriger la troncation HTTP
- Publier la capacité G si NAT symétrique détecté
- Mise à jour vers rrd4j 3.9.1-preview

</div>

<div style="background: var(--color-bg-secondary); padding: 1.5rem; border-radius: var(--radius-md); margin-bottom: 1.5rem; border-left: 4px solid var(--color-primary);">

**Version 2.5.1** <span style="color: var(--color-text-muted); font-size: 0.9rem;">— 6 mai 2024</span>

- Atténuations DDoS NetDB
- Liste de blocage Tor
- Corrections et recherche dans Susimail
- Continuer à supprimer le code SSU1
- Mise à jour vers Tomcat 9.0.88

</div>

<div style="background: var(--color-bg-secondary); padding: 1.5rem; border-radius: var(--radius-md); margin-bottom: 1.5rem; border-left: 4px solid var(--color-primary);">

**Version 2.5.0** <span style="color: var(--color-text-muted); font-size: 0.9rem;">— 8 avril 2024</span>

- Améliorations de l'iframe de console
- Redesign du limiteur de bande passante i2psnark
- Drag-and-Drop en Javascript pour i2psnark et susimail
- Améliorations du traitement des erreurs SSL i2ptunnel
- Support des connexions HTTP persistantes i2ptunnel
- Commencer à supprimer le code SSU1
- Améliorations de la gestion des requêtes de tags de relais SSU2
- Corrections de tests de pair SSU2
- Améliorations Susimail (chargement, markdown, support des emails HTML)
- Ajustements de la sélection des pairs de tunnel
- Mise à jour RRD4J vers 3.9
- Mise à jour de gradlew vers 8.5

</div>

<div style="background: var(--color-bg-secondary); padding: 1.5rem; border-radius: var(--radius-md); margin-bottom: 1.5rem; border-left: 4px solid var(--color-primary);">

**Version 2.4.0** <span style="color: var(--color-text-muted); font-size: 0.9rem;">— 18 décembre 2023</span>

- Gestion des contextes NetDB / NetDB segmenté
- Gérer les capacités de congestion en dépriorisant les routeurs surchargés
- Réanimer la bibliothèque d'assistance Android
- Sélecteur de fichiers torrent local i2psnark
- Corrections du gestionnaire de recherche NetDB
- Désactiver SSU1
- Interdire les routeurs publiant dans le futur
- Corrections SAM
- Corrections susimail
- Corrections UPnP

</div>

---

### Publications 2023-2022

<details>
<summary>Cliquez pour développer les publications 2023-2022</summary>

**Version 2.3.0** — Publiée le 28 juin 2023

- Améliorations de la sélection des pairs de tunnel
- Expiration configurable par l'utilisateur de la liste de blocage
- Throttler les rafales rapides de recherche depuis la même source
- Corriger la fuite d'information de détection de rejouement
- Correctifs NetDB pour les leaseSets multihomed
- Correctifs NetDB pour les leaseSets reçus en réponse avant d'être reçus en stock

**Version 2.2.1** — Publiée le 12 avril 2023

- Corrections d'emballage

**Version 2.2.0** — Publiée le 13 mars 2023

- Améliorations de la sélection des pairs de tunnel
- Correction de rejouement en streaming

**Version 2.1.0** — Publiée le 10 janvier 2023

- Corrections SSU2
- Corrections de congestion de construction de tunnel
- Corrections de test de pair SSU et détection de NAT symétrique
- Corriger les leaseSets chiffrés LS2 cassés
- Option pour désactiver SSU 1 (préliminaire)
- Remplissage compressible (proposition 161)
- Nouvel onglet d'état des pairs de la console
- Ajouter le support torsocks au proxy SOCKS et autres améliorations et corrections SOCKS

**Version 2.0.0** — Publiée le 21 novembre 2022

- Migration de connexion SSU2
- Acknowledgments immédiats SSU2
- Activer SSU2 par défaut
- Authentification proxy digest SHA-256 dans i2ptunnel
- Mise à jour du processus de construction Android pour utiliser AGP moderne
- Support d'auto-configuration I2P sur plusieurs plates-formes (bureau)

**Version 1.9.0** — Publiée le 22 août 2022

- Test de pair et mise en œuvre de relais SSU2
- Correctifs SSU2
- Améliorations MTU/PMTU SSU
- Activer SSU2 pour une petite partie des routeurs
- Ajouter un détecteur de deadlock
- Plus de correctifs d'importation de certificat
- Corriger la relance du DHT i2psnark après un redémarrage de routeur

**Version 1.8.0** — Publiée le 23 mai 2022

- Corrections et améliorations de la famille de routeurs
- Corrections de redémarrage logiciel
- Correctifs et améliorations de performance SSU
- Correctifs et améliorations de I2PSnark standalone
- Eviter la pénalité Sybil pour les familles de confiance
- Réduire le temps d'attente de réponse de construction de tunnel
- Correctifs UPnP
- Supprimer la source BOB
- Correctifs d'importation de certificat
- Tomcat 9.0.62
- Refactorisation pour supporter SSU2 (proposition 159)
- Implémentation initiale du protocole de base SSU2 (proposition 159)
- Fenêtre d'autorisation SAM pour les applications Android
- Améliorer le support pour les installations de répertoires personnalisés dans i2p.firefox

**Version 1.7.0** — Publiée le 21 février 2022

- Supprimer BOB
- Nouvelle interface d'édition de torrent i2psnark
- Correctifs et améliorations standalone i2psnark
- Améliorations de fiabilité NetDB
- Ajouter des messages pop-up dans la barre d'outils système
- Améliorations des performances NTCP2
- Supprimer le tunnel sortant quand le premier saut échoue
- Repli sur l'exploration pour la réponse de construction de tunnel après des échecs répétés de construction de tunnel client
- Restaurer les restrictions de même IP de tunnel
- Refactorisation du support UDP i2ptunnel pour les ports I2CP
- Continuer le travail sur SSU2, démarrer l'implémentation (proposition 159)
- Créer un paquet Debian/Ubuntu du profil du navigateur I2P
- Créer un plugin du profil du navigateur I2P
- Documenter I2P pour les applications Android
- Améliorations d'i2pcontrol
- Améliorations du support des plugins
- Nouveau plugin de proxy local
- Support des tags de message IRCv3

</details>

---

### Publications 2021

<details>
<summary>Cliquez pour développer les publications 2021</summary>

**Version 1.6.1** — Publiée le 29 novembre 2021

- Accélérer le réencodage des routers vers ECIES
- Améliorations des performances SSU
- Améliorer la sécurité des tests de pair SSU
- Ajouter la sélection de thème à l'assistant d'installation
- Continuer le travail sur SSU2 (proposition 159)
- Envoyer de nouveaux messages de construction de tunnel (proposition 157)
- Inclure un outil de configuration automatique du navigateur dans l'installateur IzPack
- Rendre les plugins Fork-and-Exec gérables
- Documenter les processus d'installation jpackage
- Compléter, documenter les outils de génération de plugins Go/Java
- Plugin de réensemencement pour
