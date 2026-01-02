---
title: "Format du filtre d'accès"
description: "Syntaxe des fichiers de filtre du contrôle d'accès des tunnels"
slug: "filter-format"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
type: docs
---

Les filtres d’accès permettent aux opérateurs de serveur I2PTunnel d’autoriser, refuser ou limiter le débit des connexions entrantes en fonction de la Destination source et du taux récent de connexions. Le filtre est un fichier texte brut de règles. Le fichier est lu de haut en bas et la **première règle correspondante prévaut**.

> Les modifications apportées à la définition du filtre prennent effet **au redémarrage du tunnel**. Certaines versions peuvent relire les listes basées sur des fichiers à l’exécution, mais prévoyez un redémarrage pour garantir que les modifications sont appliquées.

## Format de fichier

- Une règle par ligne.  
- Les lignes vides sont ignorées.  
- `#` commence un commentaire qui s'étend jusqu'à la fin de la ligne.  
- Les règles sont évaluées dans l'ordre ; la première correspondance est utilisée.

## Seuils

Un **seuil** définit combien de tentatives de connexion provenant d’une seule Destination sont autorisées dans une fenêtre temporelle glissante.

- **Numérique:** `N/S` signifie autoriser `N` connexions par période de `S` secondes. Exemple : `15/5` autorise jusqu'à 15 connexions toutes les 5 secondes. La tentative `N+1` dans la fenêtre de temps est rejetée.  
- **Mots-clés:** `allow` signifie aucune limite. `deny` signifie toujours rejeter.

## Syntaxe des règles

Les règles prennent la forme suivante :

```
<threshold> <scope> <target>
```
Où :

- `<threshold>` est `N/S`, `allow`, ou `deny`  
- `<scope>` est l'un de `default`, `explicit`, `file`, ou `record` (voir ci-dessous)  
- `<target>` dépend de la portée

### Règle par défaut

S’applique si aucune autre règle ne correspond. Une **seule** règle par défaut est autorisée. Si elle est omise, les destinations inconnues sont autorisées sans restriction.

```
15/5 default
allow default
deny default
```
### Règle explicite

Cible une destination spécifique par son adresse Base32 (par exemple `example1.b32.i2p`) ou par sa clé complète.

```
15/5 explicit example1.b32.i2p
deny explicit example2.b32.i2p
allow explicit example3.b32.i2p
```
### Règle basée sur des fichiers

Cible **toutes** les Destinations répertoriées dans un fichier externe. Chaque ligne contient une Destination ; les commentaires `#` et les lignes vides sont autorisés.

```
15/5 file /var/i2p/throttled.txt
deny file /var/i2p/blocked.txt
allow file /var/i2p/trusted.txt
```
> Note opérationnelle : Certaines implémentations relisent périodiquement les listes de fichiers. Si vous modifiez une liste pendant que le tunnel est en cours d’exécution, attendez-vous à un court délai avant que les modifications ne soient prises en compte. Redémarrez pour les appliquer immédiatement.

### Enregistreur (contrôle progressif)

Un **enregistreur** surveille les tentatives de connexion et écrit dans un fichier les Destinations qui dépassent un seuil. Vous pouvez ensuite référencer ce fichier dans une règle `file` afin d’appliquer des limitations de débit ou des blocages aux tentatives ultérieures.

```
# Start permissive
allow default

# Record Destinations exceeding 30 connections in 5 seconds
30/5 record /var/i2p/aggressive.txt

# Apply throttling to recorded Destinations
15/5 file /var/i2p/aggressive.txt
```
> Vérifiez la prise en charge de l’enregistreur dans votre build avant de vous y fier. Utilisez des listes `file` pour un comportement garanti.

## Ordre d’évaluation

Mettez d'abord les règles spécifiques, puis les règles générales. Un modèle courant :

1. Autorisations explicites pour les pairs de confiance  
2. Refus explicites pour les utilisateurs abusifs connus  
3. Listes d'autorisation/interdiction basées sur des fichiers
4. Enregistreurs pour une limitation progressive
5. Règle par défaut servant de fourre-tout

## Exemple complet

```
# Moderate limits by default
30/10 default

# Always allow trusted peers
allow explicit friend1.b32.i2p
allow explicit friend2.b32.i2p

# Block known bad actors
deny file /var/i2p/blocklist.txt

# Throttle aggressive sources
15/5 file /var/i2p/throttle.txt

# Automatically populate the throttle list
60/5 record /var/i2p/throttle.txt
```
## Notes d'implémentation

- Le filtre d'accès fonctionne au niveau de la couche tunnel, avant le traitement applicatif, afin que le trafic abusif puisse être rejeté en amont.  
- Placez le fichier de filtre dans votre répertoire de configuration I2PTunnel et redémarrez le tunnel pour appliquer les modifications.  
- Partagez des listes basées sur des fichiers entre plusieurs tunnels si vous souhaitez une politique cohérente entre les services.
