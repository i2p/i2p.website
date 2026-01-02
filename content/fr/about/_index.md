---
title: "À propos de I2P"
description: "Découvrez The Invisible Internet Project - un réseau superposé de pair à pair entièrement chiffré conçu pour la communication anonyme."
tagline: "The Invisible Internet Project"
type: "about"
layout: "about"
established: "2002"
---

The Invisible Internet Project a commencé en 2002. La vision pour le projet était que le réseau I2P "offre une anonymat, une confidentialité et une sécurité totale au plus haut niveau possible. Un Internet décentralisé et de pair à pair signifie ne plus s'inquiéter que votre fournisseur d'accès contrôle votre trafic. Cela permettra aux gens de mener des activités sans interruption et de changer notre vision de la sécurité et même de l'Internet, en utilisant la cryptographie à clé publique, la stéganographie IP et l'authentification des messages. L'Internet tel qu'il aurait dû être le sera bientôt."

Depuis, I2P a évolué pour spécifier et implémenter une suite complète de protocoles réseau capable de fournir un haut niveau de confidentialité, de sécurité et d'authentification à une variété d'applications.

## Le réseau I2P

Le réseau I2P est un réseau superposé de pair à pair entièrement chiffré. Un observateur ne peut pas voir le contenu, la source ou la destination d'un message. Personne ne peut voir d'où vient le trafic, où il va ou quel en est le contenu. De plus, les transports I2P offrent une résistance à la reconnaissance et au blocage par les censeurs. Étant donné que le réseau repose sur des pairs pour router le trafic, le blocage basé sur la localisation est un défi qui grandit avec le réseau. Chaque routeur du réseau participe à rendre le réseau anonyme. Sauf dans les cas où cela serait dangereux, tout le monde participe à l'envoi et la réception du trafic réseau.

## Comment se connecter au réseau I2P

Le logiciel de base (Java) comprend un routeur qui introduit et maintient une connexion avec le réseau. Il fournit également des applications et des options de configuration pour personnaliser votre expérience et votre flux de travail. En savoir plus dans notre [documentation](/docs/).

## Que puis-je faire sur le réseau I2P ?

Le réseau fournit une couche applicative pour les services, les applications et la gestion réseau. Le réseau a également son propre DNS unique qui permet l'auto-hébergement et le miroir de contenu depuis Internet (Clearnet). Le réseau I2P fonctionne de la même manière que l'Internet. Le logiciel Java inclut un client BitTorrent et un email ainsi qu'un modèle de site web statique. D'autres applications peuvent facilement être ajoutées à votre console de routeur.

## Aperçu du réseau

I2P utilise la cryptographie pour obtenir une variété de propriétés pour les tunnels qu'il construit et les communications qu'il transporte. Les tunnels I2P utilisent des transports, [NTCP2](/docs/specs/ntcp2/) et [SSU2](/docs/specs/ssu2/), pour dissimuler le trafic transporté. Les connexions sont chiffrées de routeur à routeur et de client à client (de bout en bout). La confidentialité persistante est assurée pour toutes les connexions. Parce que I2P est adressé cryptographiquement, les adresses réseau I2P sont auto-authentifiantes et appartiennent uniquement à l'utilisateur qui les a générées.

Le réseau est composé de pairs ("routeurs") et de tunnels virtuels unidirectionnels entrants et sortants. Les routeurs communiquent entre eux en utilisant des protocoles construits sur des mécanismes de transport existants (TCP, UDP), en passant des messages. Les applications clientes ont leur propre identifiant cryptographique ("Destination") qui leur permet d'envoyer et de recevoir des messages. Ces clients peuvent se connecter à n'importe quel routeur et autoriser l'attribution temporaire ("lease") de certains tunnels qui seront utilisés pour envoyer et recevoir des messages à travers le réseau. I2P possède sa propre base de données réseau interne (en utilisant une modification du DHT Kademlia) pour distribuer les informations de routage et de contact en toute sécurité.

## À propos de la décentralisation et du réseau I2P

Le réseau I2P est presque complètement décentralisé, à l'exception de ce qu'on appelle les serveurs Reseed. Cela est dû au problème de bootstrap de la DHT (Distributed Hash Table). En gros, il n'y a pas de moyen bon et fiable pour se passer d'au moins un nœud de bootstrap permanent que les non-participants au réseau peuvent trouver pour commencer. Une fois connecté au réseau, un routeur ne découvre des pairs qu'en construisant des tunnels "exploratoires", mais pour réaliser la connexion initiale, un hôte de réensemencement est requis pour créer des connexions et embarquer un nouveau routeur sur le réseau. Les serveurs Reseed peuvent observer lorsqu'un nouveau routeur a téléchargé un réensemencement depuis eux, mais rien d'autre sur le trafic du réseau I2P.

## Comparaisons

Il existe de nombreuses autres applications et projets travaillant sur la communication anonyme et I2P a été inspiré par une grande partie de leurs efforts. Ceci n'est pas une liste exhaustive des ressources en matière d'anonymat - à la fois [la Bibliographie sur l'Anonymat de freehaven](http://freehaven.net/anonbib/topic.html) et [les projets liés à GNUnet](https://www.gnunet.org/links/) remplissent bien cette fonction. Cela dit, quelques systèmes se distinguent pour une comparaison plus approfondie. Apprenez-en plus sur la façon dont I2P se compare à d'autres réseaux d'anonymat dans notre [documentation comparative détaillée](/docs/overview/comparison/).
