---
title: "Directives de rédaction de la documentation d'I2P"
description: "Maintenir la cohérence, l’exactitude et l’accessibilité dans l’ensemble de la documentation technique I2P"
slug: "writing-guidelines"
lastUpdated: "2025-10"
---

**Objectif:** Maintenir la cohérence, l'exactitude et l'accessibilité dans l'ensemble de la documentation technique d'I2P

---

## Principes fondamentaux

### 1. Vérifiez tout

**Ne supposez ni ne devinez jamais.** Toutes les affirmations techniques doivent être vérifiées par rapport à: - Code source I2P actuel (https://i2pgit.org/I2P_Developers/i2p.i2p/src/branch/master) - Documentation officielle de l'API (https://i2p.github.io/i2p.i2p/  - Spécifications de configuration [/docs/specs/](/docs/) - Notes de version récentes [/releases/](/categories/release/)

**Exemple de vérification appropriée :**

```markdown
❌ BAD: "The ClientApp interface probably requires three constructor parameters."
✅ GOOD: "The ClientApp interface requires this constructor signature: 
         public MyClientApp(I2PAppContext context, ClientAppManager manager, String[] args)"
```
### 2. La clarté avant la concision

Écrivez pour des développeurs qui pourraient découvrir I2P pour la première fois. Expliquez les concepts de manière complète plutôt que de supposer des connaissances préalables.

**Exemple:**

```markdown
❌ BAD: "Use the port mapper for service discovery."
✅ GOOD: "The port mapper offers a simple directory for internal TCP services. 
         Register loopback ports so other applications can discover your service 
         without hardcoded addresses."
```
### 3. Priorité à l’accessibilité

La documentation doit être accessible aux développeurs sur le clearnet (internet classique) bien que I2P soit une surcouche réseau. Fournissez toujours des alternatives accessibles sur le clearnet aux ressources internes à I2P.

---

## Exactitude technique

### Documentation de l'API et de l'interface

**Toujours inclure :** 1. Noms de packages complets à la première mention : `net.i2p.app.ClientApp` 2. Signatures de méthodes complètes avec types de retour 3. Noms et types des paramètres 4. Paramètres obligatoires vs optionnels

**Exemple:**

```markdown
The `startup()` method has signature `void startup() throws IOException` and must 
execute without blocking. The method must call `ClientAppManager.notify()` at least 
once to transition from INITIALIZED state.
```
### Propriétés de configuration

Lors de la documentation des fichiers de configuration: 1. Indiquer les noms de propriétés exacts 2. Préciser l'encodage du fichier (UTF-8 pour les configurations I2P) 3. Fournir des exemples complets 4. Documenter les valeurs par défaut 5. Indiquer la version à laquelle les propriétés ont été introduites/modifiées

**Exemple:**

```markdown
### clients.config Properties

**Required:**
- `clientApp.N.main` - Full class name (no default)

**Optional:**
- `clientApp.N.delay` - Seconds before starting (default: 120)
- `clientApp.N.onBoot` - Forces delay=0 if true (default: false, added in 0.9.4)
```
### Constantes et énumérations

Lors de la documentation des constantes, utilisez les noms de code réels :

```markdown
❌ BAD: "Common registrations include console, i2ptunnel, Jetty, sam, and bob"

✅ GOOD: "Common port mapper service constants from `net.i2p.util.PortMapper`:
- `SVC_CONSOLE` - Router console (default port 7657)
- `SVC_HTTP_PROXY` - HTTP proxy (default port 4444)
- `SVC_SAM` - SAM bridge (default port 7656)"
```
### Faire la distinction entre des concepts similaires

I2P comporte plusieurs systèmes qui se recoupent. Précisez toujours quel système vous documentez :

**Exemple :**

```markdown
Note that client registry and port mapper are separate systems:
- **ClientAppManager registry** enables inter-application communication by name lookup
- **PortMapper** maps service names to host:port combinations for service discovery
- **i2ptunnel tunnel types** are configuration values (tunnel.N.type), not service registrations
```
---

## URL et références de la documentation

### Règles d'accessibilité des URL

1. **Références principales** devraient utiliser des URL accessibles sur le clearnet (Internet public)
2. **URL internes à I2P** (domaines .i2p) doivent inclure des indications d’accessibilité
3. **Toujours fournir des alternatives** lors de la création de liens vers des ressources internes à I2P

**Modèle pour les URL internes à I2P :**

```markdown
> **Note:** The I2P network hosts comprehensive documentation at http://idk.i2p/javadoc-i2p/ 
> which requires an I2P router for access. For clearnet access, use the GitHub Pages 
> mirror at https://eyedeekay.github.io/javadoc-i2p/
```
### URLs de référence I2P recommandées

**Spécifications officielles:** - [Configuration](/docs/specs/configuration/) - [Greffon](/docs/specs/plugin/) - [Index de la documentation](/docs/)

**Documentation de l'API (choisir la plus récente):** - La plus récente: https://i2p.github.io/i2p.i2p/ (API 0.9.66 à partir d'I2P 2.10.0) - Miroir Clearnet: https://eyedeekay.github.io/javadoc-i2p/

**Code source:** - GitLab (officiel): https://i2pgit.org/I2P_Developers/i2p.i2p/src/branch/master - miroir GitHub: https://github.com/i2p/i2p.i2p

### Normes de format des liens

```markdown
✅ GOOD: [ClientApp Javadoc](https://i2p.github.io/i2p.i2p/net/i2p/app/ClientApp.html)
✅ GOOD: [Configuration Specification](https://geti2p.net/spec/configuration)

❌ BAD: See the ClientApp docs at http://idk.i2p/...
❌ BAD: [link](url) with no descriptive text
```
---

## Suivi des versions

### Métadonnées du document

Chaque document technique devrait inclure des métadonnées de version dans le frontmatter (en-tête YAML du fichier):

```markdown
---
title: "Document Title"
description: "Brief description"
slug: "url-slug"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
reviewStatus: "verified"
---
```
**Définitions des champs:** - `lastUpdated`: Année et mois de la dernière révision/mise à jour du document - `accurateFor`: Version d'I2P avec laquelle le document a été vérifié - `reviewStatus`: L'une de "draft", "needs-review", "verified", "outdated"

### Références de version dans le contenu

Lorsque vous mentionnez des versions : 1. Utilisez le **gras** pour la version actuelle : "**version 2.10.0** (septembre 2025)" 2. Indiquez à la fois le numéro de version et la date pour les références historiques 3. Indiquez la version de l’API séparément de la version I2P lorsque c’est pertinent

**Exemple:**

```markdown
Managed clients were introduced in **version 0.9.4** (December 17, 2012) and 
remain the recommended architecture as of **version 2.10.0** (September 9, 2025). 
The current API version is **0.9.66**.
```
### Documenter les changements au fil du temps

Pour les fonctionnalités qui ont évolué :

```markdown
**Version history:**
- **0.9.4 (December 2012)** - Managed clients introduced
- **0.9.42 (2019)** - clients.config.d/ directory structure added
- **1.7.0 (2021)** - ShellService added for external program tracking
- **2.10.0 (September 2025)** - Current release, no API changes to managed clients
```
### Avis de dépréciation

Si vous documentez des fonctionnalités dépréciées :

```markdown
> **Deprecated:** This feature was deprecated in version X.Y.Z and will be removed 
> in version A.B.C. Use [alternative feature](link) instead.
```
---

## Normes de terminologie

### Termes officiels d'I2P

Utilisez ces termes exacts de manière cohérente :

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Correct Term</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Avoid</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">I2P router</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">I2P node, I2P client (ambiguous)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">eepsite</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">I2P website, hidden service (Tor term)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">tunnel</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">connection, circuit (Tor term)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">netDb</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">network database, DHT</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">lease set</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">destination info</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">destination</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">address, endpoint</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">base64 destination</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">I2P address, .i2p address</td>
    </tr>
  </tbody>
</table>
### Terminologie des clients gérés

Lors de la documentation des clients gérés :

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Use This</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Not This</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">managed client</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">managed application</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">unmanaged client</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">legacy client, static client</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ClientAppManager</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">application manager, client manager</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">lifecycle methods</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">state methods, control methods</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">client registry</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">application registry, name service</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">port mapper</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">port registry, service directory</td>
    </tr>
  </tbody>
</table>
### Terminologie de la configuration

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Correct</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Incorrect</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>clients.config</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">clients.cfg, client.config</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>clients.config.d/</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">clients.d/, config.d/</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">router.config</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">router.cfg</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">i2ptunnel.config</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">tunnel.config</td>
    </tr>
  </tbody>
</table>
### Noms de packages et de classes

Utilisez toujours des noms entièrement qualifiés lors de la première occurrence, puis des noms courts par la suite:

```markdown
The `net.i2p.app.ClientApp` interface requires implementation of three lifecycle 
methods. When a ClientApp starts, the manager calls `startup()`...
```
---

## Exemples de code et mise en forme

### Exemples de code Java

Utilisez une coloration syntaxique appropriée et des exemples complets:

```markdown
### Example: Registering with Port Mapper

\`\`\`java
// Register HTTP proxy service
context.portMapper().register(
    PortMapper.SVC_HTTP_PROXY, 
    "127.0.0.1", 
    4444
);

// Later, retrieve the port
int port = context.portMapper().getPort(PortMapper.SVC_HTTP_PROXY);
if (port == -1) {
    // Service not registered
}
\`\`\`
```
**Exigences pour les exemples de code :** 1. Inclure des commentaires expliquant les lignes clés 2. Montrer la gestion des erreurs lorsque c'est pertinent 3. Utiliser des noms de variables réalistes 4. Respecter les conventions de codage I2P (indentation de 4 espaces) 5. Afficher les imports s'ils ne sont pas évidents à partir du contexte

### Exemples de configuration

Afficher des exemples de configuration complets et valides :

```markdown
### Example: clients.config.d/ Entry

File: `clients.config.d/00-console.config`

\`\`\`properties
# Router console configuration
clientApp.0.main=net.i2p.router.web.RouterConsoleRunner
clientApp.0.name=Router Console
clientApp.0.args=7657 ::1,127.0.0.1 ./webapps/
clientApp.0.delay=0
clientApp.0.onBoot=true
\`\`\`
```
### Exemples en ligne de commande

Utilisez `$` pour les commandes utilisateur, `#` pour root:

```markdown
\`\`\`bash
# Install I2P on Debian/Ubuntu
$ sudo apt-get install i2p

# Start the router
$ i2prouter start
\`\`\`
```
### Code en ligne

Utilisez des backticks (accent grave inversé) pour : - Noms de méthodes : `startup()` - Noms de classes : `ClientApp` - Noms de propriétés : `clientApp.0.main` - Noms de fichiers : `clients.config` - Constantes : `SVC_HTTP_PROXY` - Noms de packages : `net.i2p.app`

---

## Ton et voix

### Professionnel mais accessible

Rédigez pour un public technique sans condescendance:

```markdown
❌ BAD: "Obviously, you should implement the startup() method."
✅ GOOD: "Managed clients must implement the startup() method to initialize resources."

❌ BAD: "Even a junior dev knows you need to call notify()."
✅ GOOD: "The manager requires at least one notify() call during startup to track state transitions."
```
### Voix active

Utilisez la voix active pour plus de clarté :

```markdown
❌ PASSIVE: "The ClientAppManager is notified by the client when state changes."
✅ ACTIVE: "The client notifies ClientAppManager when state changes."
```
### Forme impérative pour les instructions

Utilisez l’impératif direct dans le contenu procédural :

```markdown
✅ "Implement these three lifecycle methods:"
✅ "Call manager.notify() after changing state."
✅ "Register services using context.portMapper().register()"
```
### Évitez le jargon inutile

Expliquez les termes lors de leur première apparition :

```markdown
✅ GOOD: "The netDb (network database) stores information about I2P routers and destinations."
❌ BAD: "Query the netDb for peer info." (no explanation)
```
### Directives de ponctuation

1. **Pas de tirets cadratins** - utilisez des tirets ordinaires, des virgules ou des points-virgules à la place
2. Utilisez la **virgule d'Oxford** dans les listes: "console, i2ptunnel, et Jetty"
3. **Points à l'intérieur des blocs de code** uniquement lorsque c'est grammaticalement nécessaire
4. Dans les **listes énumératives**, utilisez des points-virgules lorsque les éléments contiennent des virgules

---

## Structure du document

### Ordre standard des sections

Pour la documentation de l’API :

1. **Vue d'ensemble** - ce que fait la fonctionnalité, pourquoi elle existe
2. **Implémentation** - comment l'implémenter/l'utiliser
3. **Configuration** - comment la configurer
4. **Référence de l'API** - descriptions détaillées des méthodes/propriétés
5. **Exemples** - exemples complets et entièrement fonctionnels
6. **Bonnes pratiques** - conseils et recommandations
7. **Historique des versions** - date d'introduction, changements au fil du temps
8. **Références** - liens vers la documentation connexe

### Hiérarchie des titres

Utilisez des niveaux de titres sémantiques :

```markdown
# Document Title (h1 - only one per document)

## Major Section (h2)

### Subsection (h3)

#### Detail Section (h4)

**Bold text for emphasis within sections**
```
### Encadrés d’information

Utilisez des blocs de citation pour les remarques particulières :

```markdown
> **Note:** Additional information that clarifies the main content.

> **Warning:** Important information about potential issues or breaking changes.

> **Deprecated:** This feature is deprecated and will be removed in version X.Y.Z.

> **Status:** Current implementation status or version information.
```
### Listes et organisation

**Listes non ordonnées** pour des éléments sans ordre particulier :

```markdown
- First item
- Second item
- Third item
```
**Listes ordonnées** pour des étapes séquentielles:

```markdown
1. First step
2. Second step
3. Third step
```
**Listes de définitions** pour expliquer des termes :

```markdown
**Term One**
: Explanation of term one

**Term Two**  
: Explanation of term two
```
---

## Écueils courants à éviter

### 1. Systèmes similaires faciles à confondre

**Ne pas confondre:** - registre de ClientAppManager vs. PortMapper - types de tunnels i2ptunnel vs. constantes de service du port mapper - ClientApp vs. RouterApp (contextes différents) - clients gérés vs. non gérés

**Précisez toujours de quel système** vous parlez :

```markdown
✅ "Register with ClientAppManager using manager.register(this) for name-based lookup."
✅ "Register with PortMapper using context.portMapper().register() for port discovery."
```
### 2. Références à des versions obsolètes

**À ne pas faire :** - Présenter d'anciennes versions comme « actuelles » - Pointer vers une documentation d'API obsolète - Utiliser des signatures de méthodes dépréciées dans les exemples

**À faire :** - Consulter les notes de version avant publication - Vérifier que la documentation de l'API correspond à la version actuelle - Mettre à jour les exemples pour utiliser les bonnes pratiques actuelles

### 3. URL inaccessibles

**À ne pas faire:** - Créer des liens uniquement vers des domaines .i2p sans alternatives clearnet (Internet public classique) - Utiliser des URL de documentation cassées ou obsolètes - Créer des liens vers des chemins locaux file://

**À faire :** - Fournir des alternatives clearnet pour tous les liens internes à I2P - Vérifier que les URL sont accessibles avant publication - Utiliser des URL persistantes (geti2p.net, pas un hébergement temporaire)

### 4. Exemples de code incomplets

**À ne pas faire:** - Afficher des extraits sans contexte - Omettre la gestion des erreurs - Utiliser des variables non définies - Omettre les instructions d'importation lorsqu'elles ne sont pas évidentes

**À faire:** - Présenter des exemples complets et compilables - Inclure la gestion des erreurs requise - Expliquer ce que fait chaque ligne importante - Tester les exemples avant publication

### 5. Déclarations ambiguës

```markdown
❌ "Some applications register services."
✅ "Applications implementing ClientApp may register with ClientAppManager 
   using manager.register(this) to enable name-based lookup."

❌ "Configuration files go in the config directory."
✅ "Modern I2P installations store client configurations in 
   $I2P/clients.config.d/ as individual files."
```
---

## Conventions Markdown

### Nommage des fichiers

Utilisez le kebab-case (mots séparés par des tirets) pour les noms de fichiers : - `managed-clients.md` - `port-mapper-guide.md` - `configuration-reference.md`

### Format du Frontmatter (métadonnées d'en-tête)

Toujours inclure le front matter YAML (métadonnées en tête du document):

```yaml
---
title: "Document Title"
description: "Brief description under 160 characters"
slug: "url-slug"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
reviewStatus: "verified"
---
```
### Mise en forme des liens

**Liens internes** (dans la documentation):

```markdown
See [clients.config specification](https://geti2p.net/spec/configuration#clients-config)
```
**Liens externes** (vers d'autres ressources):

```markdown
For more details, see [ClientApp Javadoc](https://i2p.github.io/i2p.i2p/net/i2p/app/ClientApp.html)
```
**Liens vers le dépôt de code**:

```markdown
View source: [ClientApp.java](https://i2pgit.org/I2P_Developers/i2p.i2p/src/branch/master/core/java/src/net/i2p/app/ClientApp.java)
```
### Mise en forme des tableaux

Utilisez des tableaux GitHub-flavored Markdown (Markdown spécifique à GitHub):

```markdown
| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `main` | String | (required) | Full class name |
| `delay` | Integer | 120 | Seconds before start |
| `onBoot` | Boolean | false | Force immediate start |
```
### Étiquettes de langue pour les blocs de code

Indiquez toujours la langue pour la coloration syntaxique :

```markdown
\`\`\`java
// Java code
\`\`\`

\`\`\`bash
# Shell commands
\`\`\`

\`\`\`properties
# Configuration files
\`\`\`

\`\`\`xml
<!-- XML files -->
\`\`\`
```
---

## Liste de contrôle de revue

Avant de publier la documentation, vérifiez :

- [ ] Toutes les affirmations techniques sont vérifiées par rapport au code source ou à la documentation officielle
- [ ] Les numéros de version et les dates sont à jour
- [ ] Toutes les URL sont accessibles depuis le clearnet (ou des alternatives sont fournies)
- [ ] Les exemples de code sont complets et testés
- [ ] La terminologie suit les conventions d’I2P
- [ ] Pas de tirets cadratins (utiliser des tirets normaux ou une autre ponctuation)
- [ ] Le Frontmatter (métadonnées d’en-tête) est complet et exact
- [ ] La hiérarchie des titres est sémantique (h1 → h2 → h3)
- [ ] Les listes et les tableaux sont correctement formatés
- [ ] La section des références inclut toutes les sources citées
- [ ] Le document suit les directives de structure
- [ ] Le ton est professionnel mais accessible
- [ ] Les concepts similaires sont clairement distingués
- [ ] Aucun lien ni référence brisés
- [ ] Les exemples de configuration sont valides et à jour

---

**Commentaires:** Si vous rencontrez des problèmes ou avez des suggestions concernant ces directives, veuillez les soumettre via les canaux officiels de développement d'I2P.
