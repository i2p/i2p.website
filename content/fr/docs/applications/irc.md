---
title: "IRC sur I2P"
description: "Guide complet des réseaux IRC I2P, clients, tunnels et configuration de serveur (mis à jour 2025)"
slug: "irc"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

## Aperçu

**Points clés**

- I2P fournit un **chiffrement de bout en bout** pour le trafic IRC à travers ses tunnels. **Désactivez SSL/TLS** dans les clients IRC sauf si vous utilisez un outproxy vers le clearnet.
- Le tunnel client **Irc2P** préconfiguré écoute sur **127.0.0.1:6668** par défaut. Connectez votre client IRC à cette adresse et ce port.
- N'utilisez pas le terme « TLS fourni par le routeur ». Utilisez « chiffrement natif d'I2P » ou « chiffrement de bout en bout ».

## Démarrage rapide (Java I2P)

1. Ouvrez le **Gestionnaire de Services Cachés** à l'adresse `http://127.0.0.1:7657/i2ptunnel/` et assurez-vous que le tunnel **Irc2P** est **en cours d'exécution**.
2. Dans votre client IRC, configurez **serveur** = `127.0.0.1`, **port** = `6668`, **SSL/TLS** = **désactivé**.
3. Connectez-vous et rejoignez des canaux comme `#i2p`, `#i2p-dev`, `#i2p-help`.

Pour les utilisateurs d'**i2pd** (routeur C++), créez un tunnel client dans `tunnels.conf` (voir les exemples ci-dessous).

## Réseaux et serveurs

### IRC2P (main community network)

- Serveurs fédérés : `irc.postman.i2p:6667`, `irc.echelon.i2p:6667`, `irc.dg.i2p:6667`.
- Le **tunnel Irc2P** à `127.0.0.1:6668` se connecte automatiquement à l'un de ces serveurs.
- Canaux typiques : `#i2p`, `#i2p-chat`, `#i2p-dev`, `#i2p-help`.

### Ilita network

- Serveurs : `irc.ilita.i2p:6667`, `irc.r4sas.i2p:6667`, `irc.acetone.i2p:6667`, `rusirc.ilita.i2p:6667`.
- Langues principales : russe et anglais. Des interfaces web existent sur certains hôtes.

## Client setup

### Recommended, actively maintained

- **WeeChat (terminal)** — excellent support SOCKS ; facile à scripter.
- **Pidgin (bureau)** — toujours maintenu ; fonctionne bien sous Windows/Linux.
- **Thunderbird Chat (bureau)** — pris en charge dans ESR 128+.
- **The Lounge (web auto‑hébergé)** — client web moderne.

### IRC2P (réseau communautaire principal)

- **LimeChat** (gratuit, open source).
- **Textual** (payant sur l'App Store ; source disponible pour la compilation).

### Réseau Ilita

#### WeeChat via SOCKS5

```
/proxy add i2p socks5 127.0.0.1 4447
/set irc.server.i2p.addresses "127.0.0.1/6668"
/set irc.server.i2p.proxy "i2p"
/connect i2p
```
#### Pidgin

- Protocole : **IRC**
- Serveur : **127.0.0.1**
- Port : **6668**
- Chiffrement : **désactivé**
- Nom d'utilisateur/pseudonyme : au choix

#### Thunderbird Chat

- Type de compte : **IRC**
- Serveur : **127.0.0.1**
- Port : **6668**
- SSL/TLS : **désactivé**
- Optionnel : rejoindre automatiquement les canaux à la connexion

#### Dispatch (SAM v3)

Exemple de valeurs par défaut de `config.toml` :

```
[defaults]
name = "Irc2P"
host = "irc.postman.i2p"
port = 6667
channels = ["#i2p","#i2p-dev"]
ssl = false
```
## Tunnel configuration

### Java I2P defaults

- Tunnel client Irc2P : **127.0.0.1:6668** → serveur en amont sur le **port 6667**.
- Gestionnaire de Services Cachés : `http://127.0.0.1:7657/i2ptunnel/`.

### Recommandé, activement maintenu

`~/.i2pd/tunnels.conf` :

```
[IRC-IRC2P]
type = client
address = 127.0.0.1
port = 6668
destination = irc.postman.i2p
destinationport = 6667
keys = irc-keys.dat
```
Tunnel séparé pour Ilita (exemple) :

```
[IRC-ILITA]
type = client
address = 127.0.0.1
port = 6669
destination = irc.ilita.i2p
destinationport = 6667
keys = irc-ilita-keys.dat
```
### Options macOS

- **Activer SAM** dans Java I2P (désactivé par défaut) via `/configclients` ou `clients.config`.
- Par défaut : **127.0.0.1:7656/TCP** et **127.0.0.1:7655/UDP**.
- Cryptographie recommandée : `SIGNATURE_TYPE=7` (Ed25519) et `i2cp.leaseSetEncType=4,0` (ECIES‑X25519 avec repli ElGamal) ou simplement `4` pour les versions modernes uniquement.

### Exemples de configurations

- Java I2P par défaut : **2 entrants / 2 sortants**.
- i2pd par défaut : **5 entrants / 5 sortants**.
- Pour IRC : **2–3 de chaque** est suffisant ; définissez explicitement pour un comportement cohérent entre les routeurs.

## Configuration du client

- **N'activez pas SSL/TLS** pour les connexions IRC internes I2P. I2P fournit déjà un chiffrement de bout en bout. L'ajout de TLS supplémentaire crée une surcharge sans gain d'anonymat.
- Utilisez des **clés persistantes** pour une identité stable ; évitez de régénérer les clés à chaque redémarrage sauf en phase de test.
- Si plusieurs applications utilisent IRC, privilégiez des **tunnels séparés** (non partagés) pour réduire la corrélation entre services.
- Si vous devez autoriser le contrôle à distance (SAM/I2CP), liez à localhost et sécurisez l'accès avec des tunnels SSH ou des reverse proxies authentifiés.

## Alternative connection method: SOCKS5

Certains clients peuvent se connecter via le proxy SOCKS5 d'I2P : **127.0.0.1:4447**. Pour de meilleurs résultats, privilégiez un tunnel IRC dédié sur le port 6668 ; SOCKS ne peut pas nettoyer les identifiants de la couche application et peut divulguer des informations si le client n'est pas conçu pour l'anonymat.

## Troubleshooting

- **Impossible de se connecter** — assurez-vous que le tunnel Irc2P est en cours d'exécution et que le routeur est entièrement bootstrappé.
- **Blocage lors de la résolution/jonction** — vérifiez que SSL est **désactivé** et que le client pointe vers **127.0.0.1:6668**.
- **Latence élevée** — I2P a une latence élevée par conception. Maintenez un nombre modeste de tunnels (2–3) et évitez les boucles de reconnexion rapides.
- **Utilisation d'applications SAM** — confirmez que SAM est activé (Java) ou non bloqué par un pare-feu (i2pd). Les sessions de longue durée sont recommandées.

## Appendix: Ports and naming

- Ports de tunnel IRC courants : **6668** (Irc2P par défaut), **6667** et **6669** comme alternatives.
- Noms d'hôte `.b32.i2p` : forme standard de 52 caractères ; des formes étendues de 56+ caractères existent pour LS2/certificats avancés. Utilisez les noms d'hôte `.i2p` sauf si vous avez explicitement besoin d'adresses b32.
