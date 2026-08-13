---
title: "I2PControl JSON-RPC"
description: "API de gestion de router distant via l'application web I2PControl"
slug: "i2pcontrol"
lastUpdated: "2026-07-10"
accurateFor: "2.12.0"
reviewStatus: "needs-review"
---

# Documentation de l'API I2PControl

-------------vérifier ajout d'éléments--------------

I2PControl est une API **JSON-RPC 2.0** intégrée au router I2P (depuis la version 0.9.39). Elle permet la surveillance et le contrôle authentifiés du router via des requêtes JSON structurées.

> **Mot de passe par défaut :** `itoopie` — il s'agit du paramètre d'usine par défaut et **doit être changé** immédiatement pour la sécurité.

## 1. Vue d'ensemble et accès

| Implémentation             | Point de terminaison par défaut                 | Protocole | Activé par défaut                             | Notes                  |
|----------------------------|----------------------------------|----------|------------------------------------------------|------------------------|
| Java I2P (2.10.0+)         | `http://127.0.0.1:7657/jsonrpc/` | HTTP     | ❌ Doit être activé via les applications web (console du routeur) | Application web incluse         |
| i2pd (implémentation C++)  | `https://127.0.0.1:7650/`        | HTTPS    | ✅ Activé par défaut                           | Comportement hérité du greffon |
---

Dans le cas de Java I2P, vous devez aller dans **Console du routeur → WebApps → I2PControl** et l'activer (régler pour démarrer automatiquement). Une fois actif, toutes les méthodes nécessitent que vous vous authentifiiez d'abord et receviez un jeton de session.

## 2. Format JSON-RPC

---

```json
{
  "jsonrpc": "2.0",
  "id": "1",
  "method": "MethodName",
  "params": {
    /* named parameters */
  }
}
```
Toutes les requêtes suivent la structure JSON-RPC 2.0 :

```json
{
  "jsonrpc": "2.0",
  "id": "1",
  "result": { /* data */ }
}
```
Une réponse réussie inclut un champ `result` ; en cas d'échec, un objet `error` est retourné :

```json
{
  "jsonrpc": "2.0",
  "id": "1",
  "error": {
    "code": -32001,
    "message": "Invalid password"
  }
}
```
ou

## 3. Flux d'authentification

### Requête (Authentifier)

```bash
curl -s -H "Content-Type: application/json" \
  -d '{
        "jsonrpc": "2.0",
        "id": "1",
        "method": "Authenticate",
        "params": {
          "API": 1,
          "Password": "itoopie"
        }
      }' \
  http://127.0.0.1:7657/jsonrpc/
```
### Réponse réussie

```json
{
  "jsonrpc": "2.0",
  "id": "1",
  "result": {
    "Token": "a1b2c3d4e5",
    "API": 1
  }
}
```
| Champ       | Direction  | Type   | Description                                               |
|-------------|------------|--------|-----------------------------------------------------------|
| `API`       | Requête    | long   | Version de l'API I2PControl demandée par le client. Utilisez `1`. |
| `Password`  | Requête    | String | Mot de passe utilisé pour s'authentifier auprès d'I2PControl.     |
| `API`       | Réponse    | long   | Version principale de l'API implémentée par le serveur.           |
| `Token`     | Réponse    | String | Jeton d'authentification utilisé pour les requêtes suivantes.     |
---

Vous devez inclure ce `Token` dans toutes les requêtes suivantes dans les `params`.

## 4. Méthodes et points de terminaison

### 4.1 RouterInfo

---

Récupère les données de télémétrie clés concernant le router.

```bash
curl -s -H "Content-Type: application/json" \
  -d '{
        "jsonrpc": "2.0",
        "id": "2",
        "method": "RouterInfo",
        "params": {
          "Token": "a1b2c3d4e5",
          "i2p.router.version": "",
          "i2p.router.status": "",
          "i2p.router.net.status": "",
          "i2p.router.net.tunnels.participating": "",
          "i2p.router.net.bw.inbound.1s": "",
          "i2p.router.net.bw.outbound.1s": ""
        }
      }' \
  http://127.0.0.1:7657/jsonrpc/
```
**Exemple de requête**

#### Énumération des codes de statut (`i2p.router.net.status`)

| Clé                                    | Type   | Description                                                             |
|----------------------------------------|--------|-------------------------------------------------------------------------|
| `i2p.router.status`                    | Chaîne | Statut du routeur en format libre, traduit, destiné à être affiché.             |
| `i2p.router.uptime`                    | long   | Temps de fonctionnement du routeur en millisecondes. Les anciennes versions d'i2pd peuvent retourner une chaîne. |
| `i2p.router.version`                   | Chaîne | Version complète du routeur.                                                    |
| `i2p.router.net.status`                | long   | Code d'état du réseau ; voir le tableau ci-dessous.                               |
| `i2p.router.net.bw.inbound.1s`         | double | Bande passante entrante actuelle en octets par seconde.                          |
| `i2p.router.net.bw.inbound.15s`        | double | Bande passante moyenne entrante sur 15 secondes en octets par seconde.                |
| `i2p.router.net.bw.outbound.1s`        | double | Bande passante sortante actuelle en octets par seconde.                         |
| `i2p.router.net.bw.outbound.15s`       | double | Bande passante moyenne sortante sur 15 secondes en octets par seconde.               |
| `i2p.router.net.tunnels.participating` | long   | Nombre de tunnels auxquels ce routeur participe.                |
#### Énumération du code d'état (`i2p.router.net.status`)

| Code | Signification                                          |
|------|--------------------------------------------------------|
| 0    | OK                                                     |
| 1    | TEST EN COURS                                          |
| 2    | FIREWALLED                                             |
| 3    | CACHÉ                                                  |
| 4    | WARN_FIREWALLED_AND_FAST                               |
| 5    | WARN_FIREWALLED_AND_FLOODFILL                          |
| 6    | WARN_FIREWALLED_WITH_INBOUND_TCP                     |
| 7    | WARN_FIREWALLED_WITH_UDP_DISABLED                    |
| 8    | ERROR_I2CP                                             |
| 9    | ERROR_CLOCK_SKEW                                       |
| 10   | ERROR_PRIVATE_TCP_ADDRESS                              |
| 11   | ERROR_SYMMETRIC_NAT                                    |
| 12   | ERROR_UDP_PORT_IN_USE                                  |
| 13   | ERROR_NO_ACTIVE_PEERS_CHECK_CONNECTION_AND_FIREWALL    |
| 14   | ERROR_UDP_DISABLED_AND_TCP_UNSET                     |
#### Champs du NetDB et des pairs

| Clé                                  | Type    | Description                                        |
|--------------------------------------|---------|----------------------------------------------------|
| `i2p.router.netdb.knownpeers`        | long    | Nombre de pairs connus, à l'exception du routeur local. |
| `i2p.router.netdb.activepeers`       | long    | Nombre de pairs actifs.                            |
| `i2p.router.netdb.fastpeers`         | long    | Nombre de pairs classés comme rapides.             |
| `i2p.router.netdb.highcapacitypeers` | long    | Nombre de pairs classés comme haute capacité.      |
| `i2p.router.netdb.isreseeding`       | boolean | Indique si un reseed est en cours.                 |
**Champs de réponse (result)**   Selon la documentation officielle (GetI2P) :   - `i2p.router.status` (String) — un statut lisible par l'homme   - `i2p.router.uptime` (long) — millisecondes (ou chaîne pour les anciennes versions d'i2pd) :contentReference[oaicite:0]{index=0}   - `i2p.router.version` (String) — chaîne de version :contentReference[oaicite:1]{index=1}   - `i2p.router.net.bw.inbound.1s`, `i2p.router.net.bw.inbound.15s` (double) — bande passante entrante en B/s :contentReference[oaicite:2]{index=2}   - `i2p.router.net.bw.outbound.1s`, `i2p.router.net.bw.outbound.15s` (double) — bande passante sortante en B/s :contentReference[oaicite:3]{index=3}   - `i2p.router.net.status` (long) — code de statut numérique (voir l'énumération ci-dessous) :contentReference[oaicite:4]{index=4}   - `i2p.router.net.tunnels.participating` (long) — nombre de tunnels participants :contentReference[oaicite:5]{index=5}   - `i2p.router.netdb.activepeers`, `fastpeers`, `highcapacitypeers` (long) — statistiques des pairs netDB :contentReference[oaicite:6]{index=6}   - `i2p.router.netdb.isreseeding` (boolean) — indique si le réamorçage est actif :contentReference[oaicite:7]{index=7}   - `i2p.router.netdb.knownpeers` (long) — total des pairs connus :contentReference[oaicite:8]{index=8}

### 4.2 GetRate

---

| Paramètre | Type   | Description                        |
|-----------|--------|------------------------------------|
| `Stat`    | String | Nom du RateStat du routeur.        |
| `Period`  | long   | Période de mesure en millisecondes.|
Utilisé pour récupérer les métriques de débit (par exemple bande passante, succès des tunnels) sur une fenêtre de temps donnée.

```bash
curl -s -H "Content-Type: application/json" \
  -d '{
        "jsonrpc": "2.0",
        "id": "3",
        "method": "GetRate",
        "params": {
          "Token": "a1b2c3d4e5",
          "Stat": "bw.combined",
          "Period": 60000
        }
      }' \
  http://127.0.0.1:7657/jsonrpc/
```
**Exemple de requête**

```json
{
  "jsonrpc": "2.0",
  "id": "3",
  "result": {
    "Result": 12345.67
  }
}
```
**Exemple de Réponse**

### 4.3 RouterManager

---

| Paramètre          | Résultat          | Description                                                           |
|--------------------|-------------------|-----------------------------------------------------------------------|
| `Restart`          | null              | Lance un redémarrage immédiat du routeur.                             |
| `RestartGraceful`  | null              | Redémarre après l'expiration des tunnels auxquels il participe.       |
| `Shutdown`         | null              | Lance une fermeture immédiate du routeur.                             |
| `ShutdownGraceful` | null              | Ferme le routeur après l'expiration des tunnels auxquels il participe.|
| `Reseed`           | null              | Démarre un reseed du routeur.                                         |
| `FindUpdates`      | boolean ou String | Bloquant. Recherche une mise à jour signée du routeur.                |
| `Update`           | String            | Bloquant. Démarre une mise à jour signée du routeur et retourne son statut final. |
Effectuer des actions administratives.

```bash
curl -s -H "Content-Type: application/json" \
  -d '{
        "jsonrpc": "2.0",
        "id": "4",
        "method": "RouterManager",
        "params": {
          "Token": "a1b2c3d4e5",
          "Restart": true
        }
      }' \
  http://127.0.0.1:7657/jsonrpc/
```
**Paramètres / méthodes autorisés**   - `Restart`, `RestartGraceful`   - `Shutdown`, `ShutdownGraceful`   - `Reseed`, `FindUpdates`, `Update` :contentReference[oaicite:10]{index=10}

```json
{
  "jsonrpc": "2.0",
  "id": "4",
  "result": {
    "Restart": null
  }
}
```
**Exemple de requête**

### 4.4 NetworkSetting

**Réponse réussie**

---

| Clé                             | Valeur acceptée                                      | Description                                                  |
|---------------------------------|-----------------------------------------------------|--------------------------------------------------------------|
| `i2p.router.net.ntcp.port`      | Chaîne, 1–65535                                     | Port NTCP ; un changement nécessite un redémarrage.          |
| `i2p.router.net.ntcp.hostname`  | Chaîne                                              | Nom d'hôte NTCP ; un changement nécessite un redémarrage.    |
| `i2p.router.net.ntcp.autoip`    | `always`, `true` ou `false`                         | Sélection automatique de l'adresse NTCP.                      |
| `i2p.router.net.ssu.port`       | Chaîne, 1–65535                                     | Port SSU ; un changement nécessite un redémarrage.           |
| `i2p.router.net.ssu.hostname`   | Chaîne                                              | Nom d'hôte externe SSU ; un changement nécessite un redémarrage. |
| `i2p.router.net.ssu.autoip`     | `ssu`, `local,ssu`, `upnp,ssu` ou `local,upnp,ssu` | Sources de découverte d'adresse SSU.                         |
| `i2p.router.net.ssu.detectedip` | null                                                | Adresse SSU détectée en lecture seule.                        |
| `i2p.router.net.upnp`           | Chaîne                                              | Paramètre UPnP.                                              |
| `i2p.router.net.bw.share`       | Chaîne, 0–100                                       | Pourcentage de bande passante disponible pour les tunnels participatifs. |
| `i2p.router.net.bw.in`          | Chaîne d'entier non négatif                         | Limite de bande passante entrante en Kio/s.                  |
| `i2p.router.net.bw.out`         | Chaîne d'entier non négatif                         | Limite de bande passante sortante en Kio/s.                  |
| `i2p.router.net.laptopmode`     | Chaîne                                              | Paramètre du mode portable.                                 |
Obtenir ou définir les paramètres de configuration réseau (ports, upnp, partage de bande passante, etc.)

```bash
curl -s -H "Content-Type: application/json" \
  -d '{
        "jsonrpc": "2.0",
        "id": "5",
        "method": "NetworkSetting",
        "params": {
          "Token": "a1b2c3d4e5",
          "i2p.router.net.ntcp.port": null,
          "i2p.router.net.ssu.port": null,
          "i2p.router.net.bw.share": null,
          "i2p.router.net.upnp": null
        }
      }' \
  http://127.0.0.1:7657/jsonrpc/
```
**Exemple de requête (obtenir les valeurs actuelles)**

```json
{
  "jsonrpc": "2.0",
  "id": "5",
  "result": {
    "i2p.router.net.ntcp.port": "1234",
    "i2p.router.net.ssu.port": "5678",
    "i2p.router.net.bw.share": "50",
    "i2p.router.net.upnp": "true",
    "SettingsSaved": false,
    "RestartNeeded": false
  }
}
```
**Exemple de réponse**

> Note : les versions d'i2pd antérieures à 2.41 peuvent retourner des types numériques au lieu de chaînes de caractères — les clients doivent gérer les deux. :contentReference[oaicite:11]{index=11}

### 4.5 Paramètres avancés

---

| Paramètre | Type                | Description                                                           |
|-----------|---------------------|-----------------------------------------------------------------------|
| `get`     | Chaîne de caractères | Renvoie un paramètre dans un objet résultat `get`.                     |
| `getAll`  | n/a                 | Renvoie la carte complète de configuration à l'intérieur de `getAll`. |
| `set`     | Map<String, String> | Met à jour les paramètres fournis sans supprimer les autres clés.    |
| `setAll`  | Map<String, String> | **Destructif :** remplace tous les paramètres et supprime les clés non fournies. |
Permet de manipuler les paramètres internes du router.

**Exemple de requête**

```bash
curl -s -H "Content-Type: application/json" \
  -d '{
        "jsonrpc": "2.0",
        "id": "6",
        "method": "AdvancedSettings",
        "params": {
          "Token": "a1b2c3d4e5",
          "set": {
            "router.sharePercentage": "75",
            "i2np.flushInterval": "6000"
          }
        }
      }' \
  http://127.0.0.1:7657/jsonrpc/
```
**Exemple de réponse**

```json
{
  "jsonrpc": "2.0",
  "id": "6",
  "result": {}
}
```
---

### Codes d'erreur JSON-RPC2 standard

---

| Paramètre | Type   | Description                 |
|-----------|--------|-----------------------------|
| `Echo`    | Chaîne | Valeur renvoyée en tant que `Result`. |
```json
{
  "jsonrpc": "2.0",
  "id": "7",
  "method": "Echo",
  "params": {
    "Token": "a1b2c3d4e5",
    "Echo": "hello"
  }
}
```
```json
{
  "jsonrpc": "2.0",
  "id": "7",
  "result": {
    "Result": "hello"
  }
}
```
---

### Codes d'erreur spécifiques à I2PControl

Gère lui-même I2PControl. Le gestionnaire Java actuel prend en charge les modifications de mot de passe.

| Paramètre             | Type   | Description                                                                |
|-----------------------|--------|----------------------------------------------------------------------------|
| `i2pcontrol.password` | Chaîne | Définit un nouveau mot de passe I2PControl et annule les jetons d'authentification existants. |
Le résultat contient `SettingsSaved`. Si le mot de passe a été modifié, le résultat contient également `"i2pcontrol.password": null`. Les paramètres d'adresse et de port d'écoute du plugin autonome hérité ne sont pas actifs dans le gestionnaire Java actuel.

> **Mot de passe par défaut :** `itoopie` — il s'agit du paramètre d'usine par défaut et **doit être changé** immédiatement pour la sécurité.

## 5. Codes d'erreur

### Codes d'erreur standard JSON-RPC2

| Code   | Signification         |
|--------|-----------------------|
| -32700 | Erreur d'analyse JSON |
| -32600 | Requête invalide      |
| -32601 | Méthode non trouvée   |
| -32602 | Paramètres invalides  |
| -32603 | Erreur interne        |
### Codes d'erreur spécifiques à I2PControl

| Code   | Signification                                                                              |
|--------|----------------------------------------------------------------------------------------------|
| -32001 | Mot de passe fourni invalide                                                                 |
| -32002 | Aucun jeton d'authentification présenté                                                      |
| -32003 | Le jeton d'authentification n'existe pas                                                     |
| -32004 | Le jeton d'authentification fourni a expiré et sera supprimé                                 |
| -32005 | La version de l'API I2PControl utilisée n'a pas été spécifiée, mais doit l'être obligatoirement |
| -32006 | La version de l'API I2PControl spécifiée n'est pas prise en charge par I2PControl            |
> **Mot de passe par défaut :** `itoopie` — il s'agit du paramètre d'usine par défaut et **doit être changé** immédiatement pour la sécurité.

## 6. Utilisation et bonnes pratiques

- Toujours inclure le paramètre `Token` (sauf lors de l'authentification).
- Changer le mot de passe par défaut (`itoopie`) lors de la première utilisation.
- Pour Java I2P, s'assurer que l'application web I2PControl est activée via WebApps.
- Se préparer à de légères variations : certains champs peuvent être des nombres ou des chaînes, selon la version d'I2P.
- Encapsuler les longues chaînes de statut pour un affichage convivial.

> **Mot de passe par défaut :** `itoopie` — il s'agit du paramètre d'usine par défaut et **doit être changé** immédiatement pour la sécurité.
