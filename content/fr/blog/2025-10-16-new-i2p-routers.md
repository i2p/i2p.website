---
title: "Nouveaux I2P Routers"
date: 2025-10-16
author: "idk"
categories: ["community"]
description: "Plusieurs nouvelles implémentations de router I2P émergent, dont emissary en Rust et go-i2p en Go, ouvrant de nouvelles possibilités d’intégration et de diversité du réseau."
API_Translate: vrai
---

C'est une période enthousiasmante pour le développement d'I2P, notre communauté grandit et de multiples nouveaux prototypes de routers I2P entièrement fonctionnels émergent sur la scène ! Nous sommes très enthousiastes à propos de cette avancée et ravis de partager la nouvelle avec vous.

## En quoi cela aide-t-il le réseau ?

Développer des I2P routers nous aide à démontrer que nos documents de spécification peuvent être utilisés pour produire de nouveaux I2P routers, ouvre le code à de nouveaux outils d’analyse et améliore généralement la sécurité et l’interopérabilité du réseau. La présence de plusieurs I2P routers signifie que les bogues potentiels ne sont pas uniformes ; une attaque contre un router peut ne pas fonctionner contre un autre router, ce qui évite un problème de monoculture. Cependant, la perspective peut-être la plus passionnante à long terme est l’intégration.

## Qu'est-ce que l'intégration ?

Dans le contexte d’I2P, l’intégration est une manière d’inclure directement un I2P router dans une autre application, sans nécessiter un router autonome s’exécutant en arrière-plan. C’est une façon de rendre I2P plus facile à utiliser, ce qui facilite la croissance du réseau en rendant le logiciel plus accessible. Java et C++ souffrent tous deux d’être difficiles à utiliser en dehors de leurs propres écosystèmes, C++ exigeant des liaisons C écrites à la main et fragiles et, dans le cas de Java, la difficulté de communiquer avec une application JVM depuis une application non-JVM.

Bien que cette situation soit, à bien des égards, plutôt normale, je pense qu’elle peut être améliorée afin de rendre I2P plus accessible. D’autres langages proposent des solutions plus élégantes à ces problèmes. Bien sûr, nous devrions toujours prendre en compte et utiliser les lignes directrices existantes pour les routers Java et C++.

## Un émissaire surgit des ténèbres

Entièrement indépendant de notre équipe, un développeur nommé altonen a développé une implémentation d'I2P en Rust appelée emissary. Bien qu’il soit encore assez récent et que Rust nous soit peu familier, ce projet intrigant est très prometteur. Félicitations à altonen pour la création d’emissary, nous sommes très impressionnés.

### Why Rust?

La principale raison d’utiliser Rust est globalement la même que celle d’utiliser Java ou Go. Rust est un langage de programmation compilé avec gestion de la mémoire et une vaste communauté très enthousiaste. Rust offre également des fonctionnalités avancées pour produire des bindings (liaisons) vers le langage de programmation C, qui peuvent être plus faciles à maintenir que dans d’autres langages, tout en bénéficiant des fortes garanties de sécurité mémoire de Rust.

### Do you want to get involved with emissary?

emissary est développé sur Github par altonen. Vous pouvez trouver le dépôt à l’adresse suivante : [altonen/emissary](https://github.com/altonen/emissary). Rust souffre également d’un manque de bibliothèques clientes SAMv3 complètes compatibles avec les bibliothèques réseau Rust populaires, écrire une bibliothèque SAMv3 est un excellent point de départ.

## go-i2p is getting closer to completion

Depuis environ 3 ans, je travaille sur go-i2p, en essayant de transformer une bibliothèque naissante en un I2P router à part entière, en pur Go, un autre langage à sécurité mémoire. Au cours des 6 derniers mois environ, il a été profondément restructuré afin d’améliorer les performances, la fiabilité et la maintenabilité.

### Why Go?

Bien que Rust et Go partagent de nombreux avantages, à bien des égards Go est beaucoup plus simple à apprendre. Depuis des années, il existe d’excellentes bibliothèques et applications pour utiliser I2P avec le langage de programmation Go, y compris les implémentations les plus complètes des bibliothèques SAMv3.3. Mais sans un router I2P que l’on peut gérer automatiquement (par exemple un router embarqué), cela constitue toujours un obstacle pour les utilisateurs. L’objectif de go-i2p est de combler cet écart et d’éliminer toutes les aspérités pour les développeurs d’applications I2P qui travaillent en Go.

### Pourquoi Rust ?

go-i2p est développé sur Github, principalement par eyedeekay pour le moment, et est ouvert aux contributions de la communauté sur [go-i2p](https://github.com/go-i2p/). Dans cet espace de noms, il existe de nombreux projets, tels que :

#### Router Libraries

Nous avons conçu ces bibliothèques pour produire les bibliothèques de notre I2P router. Elles sont réparties dans plusieurs dépôts dédiés afin de faciliter la revue et de les rendre utiles à d’autres personnes qui souhaitent construire des I2P routers expérimentaux et personnalisés.

- [go-i2p the router itself, most active right now](https://github.com/go-i2p/go-i2p)
- [common our core library for I2P datastructures](https://github.com/go-i2p/common)
- [crypto our library for cryptographic operations](https://github.com/go-i2p/crypto)
- [go-noise a library for implementing noise-based connections](https://github.com/go-i2p/go-noise)
- [noise a low-level library for using the Noise framework](https://github.com/go-i2p/noise)
- [su3 a library for manipulating su3 files](https://github.com/go-i2p/su3)

#### Client libraries

- [onramp a very convenient library for using(or combining) I2P and Tor](https://github.com/go-i2p/onramp)
- [go-sam-go an advanced, efficient, and very complete SAMv3 library](https://github.com/go-i2p/go-sam-go)

## If you don't like Go or Rust and are thinking of writing an I2P Router, what should you do?

Eh bien, il existe un projet dormant pour écrire un [I2P router in C#](https://github.com/PeterZander/i2p-cs) si vous voulez exécuter I2P sur une XBox. Ça a l'air plutôt sympa, en fait. Si cela ne vous convient pas non plus, vous pourriez faire comme altonen et développer un router entièrement nouveau.

### Souhaitez-vous vous impliquer dans emissary ?

Vous pouvez développer un router I2P pour n'importe quelle raison, c'est un réseau libre, mais il vous sera utile de savoir pourquoi. Y a-t-il une communauté que vous souhaitez soutenir, un outil que vous pensez bien adapté à I2P, ou une stratégie que vous voulez essayer ? Déterminez votre objectif pour savoir par où commencer et à quoi ressemblera un état "terminé".

### Decide what language you want to do it in and why

Voici quelques raisons pour lesquelles vous pourriez choisir une langue :

- **C**: No need for binding-generation, supported everywhere, can be called from any language, lingua franca of modern computing
- **Typescript**: Massive community, lots of applications, services, and libraries, works with node and deno, seems like it's everywhere right now
- **D**: It's memory safe and not Rust or Go
- **Vala**: It emits C code for the target platform, combining some of the advantages of memory-safe languages with the flexibility of C
- **Python**: Everybody uses Python

Mais voici quelques raisons pour lesquelles vous pourriez ne pas choisir ces langues :

- **C**: Memory management can be challenging, leading to impactful bugs
- **Typescript**: TypeScript is transpiled to JavaScript, which is interpreted and may impact performance
- **D**: Relatively small community
- **Vala**: Not a lot of underlying infrastructure in Vala, you end up using C versions of most libraries
- **Python**: It's an interpreted language which may impact performance

Il existe des centaines de langages de programmation et nous accueillons des bibliothèques I2P et des router maintenus dans chacun d’entre eux. Choisissez judicieusement vos compromis et commencez.

## go-i2p se rapproche de l’achèvement

Que vous souhaitiez travailler en Rust, Go, Java, C++ ou dans un autre langage, contactez-nous sur #i2p-dev sur Irc2P. Commencez par là, et nous vous orienterons vers des canaux spécifiques au router. Nous sommes aussi présents sur ramble.i2p à f/i2p, sur Reddit à r/i2p, ainsi que sur GitHub et git.idk.i2p. Nous avons hâte d’avoir de vos nouvelles bientôt.
