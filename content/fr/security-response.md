---  
title: "Processus de Réponse aux Vulnérabilités"  
description: "Processus de signalement et de réponse aux vulnérabilités de sécurité chez I2P"  
layout: "security-response"  
aliases:  
  - /en/research/vrp  
---  

<div id="contact"></div>

## Signaler une Vulnérabilité

Avez-vous découvert un problème de sécurité ? Signalez-le à **security@i2p.net** (PGP encouragé)

<a href="/keys/i2p-security-public.asc" download class="pgp-key-btn">Télécharger la clé PGP</a> | Empreinte numérique de la clé GPG : `40DF FE20 7D79 9BEC 3AE8 7DEA 5F98 BE91 176E 1941`

<div id="guidelines"></div>

## Directives de Recherche

**Veuillez NE PAS :**  
- Exploiter le réseau I2P en direct  
- Mener une ingénierie sociale ou attaquer l'infrastructure d'I2P  
- Perturber les services pour d'autres utilisateurs  

**Veuillez :**  
- Utiliser des réseaux de test isolés lorsqu'il est possible  
- Suivre les pratiques de divulgation coordonnée  
- Nous contacter avant les tests sur le réseau en direct  

<div id="process"></div>

## Processus de Réponse

### 1. Signalement Reçu  
- Réponse dans les **3 jours ouvrables**  
- Gestionnaire de réponse assigné  
- Classification de la sévérité (HAUTE/MOYENNE/BASSE)  

### 2. Enquête & Développement  
- Développement de correctifs privés via des canaux cryptés  
- Tests sur réseau isolé  
- **Sévérité HAUTE :** Notification publique dans les 3 jours (sans détails d'exploit)  

### 3. Déploiement & Divulgation  
- Mise à jour de sécurité déployée  
- Délai maximal de **90 jours** pour divulgation complète  
- Crédit du chercheur optionnel dans les annonces  

### Niveaux de Sévérité

**HAUTE** - Impact sur l'ensemble du réseau, attention immédiate requise  
**MOYENNE** - Routeurs individuels, exploitation ciblée  
**BASSE** - Impact limité, scénarios théoriques  

<div id="communication"></div>

## Communication Sécurisée

Utilisez le chiffrement PGP/GPG pour tous les rapports de sécurité :

```
Empreinte numérique : 40DF FE20 7D79 9BEC 3AE8 7DEA 5F98 BE91 176E 1941
```

Incluez dans votre rapport :  
- Description technique détaillée  
- Étapes pour reproduire  
- Code de preuve de concept (si applicable)  

<div id="timeline"></div>

## Chronologie

| Phase | Délai |  
|-------|-------|  
| Réponse Initiale | 0-3 jours |  
| Enquête | 1-2 semaines |  
| Développement & Tests | 2-6 semaines |  
| Déploiement | 6-12 semaines |  
| Divulgation Complète | 90 jours max |  

<div id="faq"></div>

## FAQ

**Vais-je avoir des problèmes en signalant ?**  
Non. La divulgation responsable est appréciée et protégée.

**Puis-je tester sur le réseau en direct ?**  
Non. Utilisez uniquement des réseaux de test isolés.

**Puis-je rester anonyme ?**  
Oui, bien que cela puisse compliquer la communication.

**Avez-vous une prime de bug ?**  
Pas actuellement. I2P est soutenu par des bénévoles avec des ressources limitées.

<div id="examples"></div>

## Que Signaler

**Dans le cadre :**  
- Vulnérabilités du routeur I2P  
- Défauts de protocole ou de cryptographie  
- Attaques au niveau du réseau  
- Techniques de désanonymisation  
- Problèmes de déni de service  

**Hors de portée :**  
- Applications tierces (contactez les développeurs)  
- Attaques sociales ou physiques  
- Vulnérabilités connues/divulguées  
- Problèmes purement théoriques  

---

**Merci d'aider à sécuriser I2P !**