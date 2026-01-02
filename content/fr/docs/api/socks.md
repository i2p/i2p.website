---
title: "Proxy SOCKS"
description: "Utiliser le tunnel SOCKS d'I2P en toute sécurité (mis à jour pour la version 2.10.0)"
slug: "socks"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

> **Attention :** Le tunnel SOCKS transmet les charges utiles des applications sans les nettoyer. De nombreux protocoles divulguent des adresses IP, des noms d'hôtes ou d'autres identifiants. Utilisez SOCKS uniquement avec des logiciels que vous avez vérifiés pour l'anonymat.

---

## 1. Aperçu

I2P fournit la prise en charge des proxys **SOCKS 4, 4a et 5** pour les connexions sortantes via un **client I2PTunnel**. Cela permet aux applications standard d'atteindre les destinations I2P mais **ne peut pas accéder au clearnet**. Il n'existe **aucun outproxy SOCKS**, et tout le trafic reste au sein du réseau I2P.

### Résumé de l'implémentation

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Parameter</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Java I2P</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">i2pd</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Default Port</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">User-defined</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>127.0.0.1:4447</code></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Supported SOCKS Versions</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">4, 4a, 5</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">4, 4a, 5</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">UDP Mode</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Stubbed (non-functional)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Stubbed (non-functional)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Persistent Keys</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">✅ Since 0.9.9</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">✅</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Shared Client Tunnels</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Supported</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Supported</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Outproxy Support</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">❌ None</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">❌ None</td>
    </tr>
  </tbody>
</table>
**Types d'adresses supportés :** - Noms d'hôtes `.i2p` (entrées du carnet d'adresses) - Hachages Base32 (`.b32.i2p`) - Aucun support pour Base64 ou clearnet

---

## 2. Risques de sécurité et limitations

### Fuite au niveau de la couche applicative

SOCKS fonctionne en dessous de la couche application et ne peut pas assainir les protocoles. De nombreux clients (par exemple, navigateurs, IRC, email) incluent des métadonnées qui révèlent votre adresse IP, nom d'hôte ou détails système.

Les fuites courantes incluent : - Les adresses IP dans les en-têtes de courrier électronique ou les réponses CTCP IRC - Les noms réels/noms d'utilisateur dans les charges utiles de protocole - Les chaînes user-agent avec empreintes du système d'exploitation - Les requêtes DNS externes - WebRTC et la télémétrie du navigateur

**I2P ne peut pas empêcher ces fuites**—elles se produisent au-dessus de la couche tunnel. N'utilisez SOCKS que pour des **clients audités** conçus pour l'anonymat.

### Identité de tunnel partagée

Si plusieurs applications partagent un tunnel SOCKS, elles partagent la même identité de destination I2P. Cela permet la corrélation ou l'empreinte digitale entre différents services.

**Atténuation :** Utilisez des **tunnels non partagés** pour chaque application et activez les **clés persistantes** pour maintenir des identités cryptographiques cohérentes entre les redémarrages.

### Mode UDP désactivé

Le support UDP dans SOCKS5 n'est pas implémenté. Le protocole annonce la capacité UDP, mais les appels sont ignorés. Utilisez des clients TCP uniquement.

### Pas d'Outproxy par conception

Contrairement à Tor, I2P n'offre **pas** d'outproxies clearnet basés sur SOCKS. Les tentatives d'accéder à des adresses IP externes échoueront ou exposeront votre identité. Utilisez des proxies HTTP ou HTTPS si l'outproxying est nécessaire.

---

## 3. Contexte historique

Les développeurs déconseillent depuis longtemps l'utilisation de SOCKS pour un usage anonyme. D'après les discussions internes entre développeurs et les [Réunion 81](/fr/blog/2004/03/16/i2p-dev-meeting-march-16-2004/) et [Réunion 82](/fr/blog/2004/03/23/i2p-dev-meeting-march-23-2004/) de 2004 :

> "Transférer du trafic arbitraire n'est pas sûr, et il nous incombe en tant que développeurs de logiciels d'anonymat d'avoir la sécurité de nos utilisateurs finaux au premier plan de nos préoccupations."

Le support SOCKS a été inclus pour des raisons de compatibilité mais n'est pas recommandé pour les environnements de production. Presque toutes les applications internet divulguent des métadonnées sensibles inadaptées au routage anonyme.

---

## 4. Configuration

### Java I2P

1. Ouvrez le [I2PTunnel Manager](http://127.0.0.1:7657/i2ptunnel)  
2. Créez un nouveau tunnel client de type **"SOCKS 4/4a/5"**  
3. Configurez les options :  
   - Port local (n'importe quel port disponible)  
   - Client partagé : *désactiver* pour une identité séparée par application  
   - Clé persistante : *activer* pour réduire la corrélation de clés  
4. Démarrez le tunnel

### i2pd

i2pd inclut le support SOCKS5 activé par défaut sur `127.0.0.1:4447`. La configuration dans `i2pd.conf` sous `[SOCKSProxy]` vous permet d'ajuster le port, l'hôte et les paramètres de tunnel.

---

## 5. Calendrier de développement

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Version</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Change</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Date</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.7.1</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Initial SOCKS 4/4a/5 support</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2010</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.9</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Added persistent keying</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2013</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1.7.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">BOB API deprecated and removed</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2022</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.6.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">I2P-over-Tor blocked to improve network health</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2024</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.10.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Post-quantum hybrid encryption introduced</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2025</td>
    </tr>
  </tbody>
</table>
Le module SOCKS lui-même n'a connu aucune mise à jour majeure du protocole depuis 2013, mais la pile de tunnels environnante a bénéficié d'améliorations en matière de performances et de cryptographie.

---

## 6. Alternatives recommandées

Pour toute application de **production**, **exposée publiquement** ou **critique en matière de sécurité**, utilisez l'une des API I2P officielles au lieu de SOCKS :

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">API</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Description</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Recommended For</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>SAM v3 (3.3)</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Simple Anonymous Messaging API</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Cross-language apps needing socket-like I/O</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Streaming Library</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">TCP-like sockets for Java</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Native Java integrations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>I2CP</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Low-level router communication</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Custom protocols, router-level integration</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>BOB</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deprecated (removed 2022)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Legacy only; migrate to SAM</td>
    </tr>
  </tbody>
</table>
Ces API fournissent une isolation appropriée des destinations, un contrôle de l'identité cryptographique et de meilleures performances de routage.

---

## 7. OnionCat / GarliCat

OnionCat prend en charge I2P via son mode GarliCat (plage IPv6 `fd60:db4d:ddb5::/48`). Toujours fonctionnel mais avec un développement limité depuis 2019.

**Limitations d'utilisation :** - Nécessite une configuration manuelle `.oc.b32.i2p` dans SusiDNS   - Requiert une attribution IPv6 statique   - Non officiellement pris en charge par le projet I2P

Recommandé uniquement pour les configurations VPN-over-I2P avancées.

---

## 8. Bonnes Pratiques

Si vous devez utiliser SOCKS : 1. Créez des tunnels séparés par application. 2. Désactivez le mode client partagé. 3. Activez les clés persistantes. 4. Forcez la résolution DNS SOCKS5. 5. Auditez le comportement du protocole pour détecter les fuites. 6. Évitez les connexions clearnet. 7. Surveillez le trafic réseau pour détecter les fuites.

---

## 9. Résumé technique

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Parameter</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Value</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Supported SOCKS Versions</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">4, 4a, 5</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Transport</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">TCP only</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>UDP Support</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Stubbed (non-functional)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Clearnet Access</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Not supported</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Default Ports</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Java I2P: user-set; i2pd: <code>127.0.0.1:4447</code></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Persistent Keying</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Supported since 0.9.9</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Shared Tunnels</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Supported (discouraged)</td>
    </tr>
  </tbody>
</table>
---

## 10. Conclusion

Le proxy SOCKS dans I2P offre une compatibilité de base avec les applications TCP existantes mais **n'est pas conçu pour garantir un anonymat robuste**. Il ne devrait être utilisé que dans des environnements de test contrôlés et audités.

> Pour les déploiements sérieux, migrez vers **SAM v3** ou l'**API Streaming**. Ces API isolent les identités des applications, utilisent une cryptographie moderne et bénéficient d'un développement continu.

---

### Ressources supplémentaires

- [Documentation officielle SOCKS](/docs/api/socks/)  
- [Spécification SAM v3](/docs/api/samv3/)  
- [Documentation de la bibliothèque Streaming](/docs/specs/streaming/)  
- [Référence I2PTunnel](/docs/specs/implementation/)  
- [Documentation développeur I2P](https://i2pgit.org/I2P_Developers/i2p.i2p)  
- [Forum de la communauté](https://i2pforum.net)
