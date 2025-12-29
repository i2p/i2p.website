---
title: "20 años de privacidad: una breve historia de I2P"
date: 2021-08-28
slug: "20-years-of-privacy-a-brief-history-of-i2p"
author: "sadie"
description: "Una historia de I2P tal como la conocemos"
categories: ["general"]
API_Translate: verdadero
---

## La invisibilidad es la mejor defensa: construir una internet dentro de otra internet

> "Creo que la mayoría de las personas quieren esta tecnología para poder expresarse libremente. Es una sensación reconfortante cuando sabes que puedes hacerlo. Al mismo tiempo, podemos superar algunos de los problemas que se observan en Internet cambiando la forma en que se conciben la seguridad y la privacidad, así como el grado en que se valoran."

En octubre de 2001, 0x90 (Lance James) tuvo un sueño. Comenzó como un "deseo de comunicación instantánea con otros usuarios de Freenet para hablar sobre temas de Freenet e intercambiar claves de Freenet, manteniendo al mismo tiempo el anonimato, la privacidad y la seguridad". Se llamó IIP — el Proyecto de IRC Invisible.

El Invisible IRC Project se basaba en un ideal y en el marco subyacente a The InvisibleNet. En una entrevista de 2002, 0x90 describió el proyecto como centrado en "la innovación de tecnología de redes inteligentes", con el objetivo de "proporcionar los estándares más altos de seguridad y privacidad en Internet, ampliamente utilizada pero notoriamente insegura".

Para 2003, varios otros proyectos similares se habían iniciado, siendo los más grandes Freenet, GNUNet y Tor. Todos estos proyectos tenían objetivos amplios: cifrar y anonimizar diversos tipos de tráfico. Para IIP, quedó claro que IRC por sí solo no era un objetivo lo bastante grande. Lo que se necesitaba era una capa de anonimización para todos los protocolos.

A comienzos de 2003, un nuevo desarrollador anónimo, "jrandom", se unió al proyecto. Su objetivo explícito era ampliar el alcance de IIP. jrandom deseaba reescribir la base de código de IIP en Java y rediseñar los protocolos basándose en publicaciones recientes y en las decisiones de diseño iniciales que Tor y Freenet estaban tomando. Algunos conceptos, como "onion routing", se modificaron para convertirse en "garlic routing" (enrutamiento tipo 'garlic').

A finales del verano de 2003, jrandom tomó el control del proyecto y lo renombró como The Invisible Internet Project o "I2P". Publicó un documento que exponía la filosofía del proyecto y situaba sus objetivos técnicos y su diseño en el contexto de las mixnets (redes de mezcla) y las capas de anonimización. También publicó la especificación de dos protocolos (I2CP e I2NP) que sentaron las bases de la red que I2P utiliza hoy en día.

Para el otoño de 2003, I2P, Freenet y Tor se estaban desarrollando rápidamente. jrandom publicó la versión 0.2 de I2P el 1 de noviembre de 2003 y continuó con lanzamientos rápidos durante los siguientes tres años.

En febrero de 2005, zzz instaló I2P por primera vez. Para el verano de 2005, zzz había puesto en marcha zzz.i2p y stats.i2p, que se convirtieron en recursos centrales para el desarrollo de I2P. En julio de 2005, jrandom publicó la versión 0.6, que incluía el innovador protocolo de transporte SSU (Secure Semi-reliable UDP) para el descubrimiento de IP y el atravesamiento de cortafuegos.

Desde finales de 2006 y durante 2007, el desarrollo central de I2P se ralentizó drásticamente, ya que jrandom centró su atención en Syndie. En noviembre de 2007, sobrevino un desastre cuando jrandom envió un mensaje críptico en el que decía que tendría que ausentarse durante un año o más. Por desgracia, nunca se volvió a saber de jrandom.

La segunda etapa del desastre ocurrió el 13 de enero de 2008, cuando el proveedor de alojamiento de casi todos los servidores de i2p.net sufrió un corte de energía y no restableció completamente el servicio. Complication, welterde y zzz tomaron decisiones rápidamente para volver a poner el proyecto en marcha, trasladándose a i2p2.de y cambiando de CVS a monotone para el control de versiones.

El proyecto se dio cuenta de que había dependido en exceso de recursos centralizados. El trabajo realizado a lo largo de 2008 descentralizó el proyecto y distribuyó los roles entre varias personas. A partir de la versión 0.7.6, el 31 de julio de 2009, zzz pasó a firmar las siguientes 49 versiones.

Para mediados de 2009, zzz había llegado a comprender mucho mejor la base de código e identificó muchos problemas de escalabilidad. La red experimentó un crecimiento debido tanto a sus capacidades de anonimización como de elusión. Se habilitaron actualizaciones automáticas dentro de la red.

In Fall 2010, zzz declared a moratorium on I2P development until the website documentation was complete and accurate. It took 3 months.

A partir de 2010, zzz, ech, hottuna y otros colaboradores asistieron al CCC (Chaos Communications Congress) anualmente hasta las restricciones por la COVID. El proyecto construyó comunidad y celebró lanzamientos de forma conjunta.

En 2013, se creó Anoncoin como la primera criptomoneda con soporte integrado para I2P, con desarrolladores como meeh proporcionando infraestructura a la red I2P.

En 2014, str4d comenzó a contribuir a I2PBote y, en Real World Crypto, se iniciaron discusiones sobre la actualización de la criptografía de I2P. Para finales de 2014, la mayor parte de la nueva criptografía de firma se había completado, incluyendo ECDSA y EdDSA.

En 2015, I2PCon tuvo lugar en Toronto, con charlas, apoyo de la comunidad y asistentes de América y Europa. En 2016, en Real World Crypto Stanford, str4d dio una charla sobre los avances en la migración criptográfica.

NTCP2 se implementó en 2018 (versión 0.9.36), proporcionando resistencia frente a la censura basada en DPI (inspección profunda de paquetes) y reduciendo la carga de la CPU mediante criptografía más rápida y moderna.

En 2019, el equipo asistió a más conferencias, incluidas DefCon y Monero Village, acercándose a desarrolladores e investigadores. La investigación de Hoàng Nguyên Phong sobre la censura en I2P fue aceptada en FOCI de USENIX, lo que llevó a la creación de I2P Metrics.

En el CCC 2019, se tomó la decisión de migrar de Monotone a GitLab. El 10 de diciembre de 2020, el proyecto cambió oficialmente de Monotone a Git, uniéndose al mundo de los desarrolladores que usan Git.

0.9.49 (2021) inició la migración a un cifrado ECIES-X25519 nuevo y más rápido para routers, culminando años de trabajo de especificación. La migración tomaría varias versiones.

## 1.5.0 — El lanzamiento de aniversario anticipado

Después de 9 años de versiones 0.9.x, el proyecto pasó directamente de la 0.9.50 a la 1.5.0 como reconocimiento a casi 20 años de trabajo para proporcionar anonimato y seguridad. Esta versión finalizó la implementación de mensajes de construcción de tunnel más pequeños para reducir el uso de ancho de banda y continuó la transición al cifrado X25519.

**Felicidades, equipo. Hagamos otros 20.**
